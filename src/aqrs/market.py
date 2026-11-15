import csv
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from io import StringIO
from pathlib import Path

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

from aqrs.admission import SYNTHETIC_START, utc_timestamp

FEATURE_NAMES = ("past_return", "relative_volume", "rolling_volatility")
WARMUP = 12
SYNTHETIC_CSV_FIELDS = (
    "bar_open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "dataset_type",
)
MAX_SYNTHETIC_CSV_BYTES = 32 * 1024**2


@dataclass(frozen=True)
class Bars:
    values: np.ndarray
    symbol: str
    bar_minutes: int

    @property
    def fingerprint(self) -> str:
        digest = sha256(f"{self.symbol}|{self.bar_minutes}|".encode("utf-8"))
        digest.update(self.values.astype("<f8", copy=False).tobytes())
        return digest.hexdigest()

    def time(self, index: int, *, close: bool = False) -> str:
        seconds = self.values[index, 0] + (60 * self.bar_minutes if close else 0)
        return datetime.fromtimestamp(seconds, UTC).isoformat()


def generate(seed: int, n_bars: int, bar_minutes: int, symbol: str) -> Bars:
    rng = np.random.Generator(np.random.PCG64(seed))
    shocks = rng.normal(0, 0.0015, size=(4, n_bars))
    opens = 30_000 * np.exp(np.cumsum(shocks[0]))
    closes = opens * np.exp(shocks[1])
    highs = np.maximum(opens, closes) * (1 + np.abs(shocks[2]))
    lows = np.minimum(opens, closes) / (1 + np.abs(shocks[3]))
    volumes = rng.lognormal(2, 0.4, n_bars)
    seconds = SYNTHETIC_START.timestamp()
    timestamps = seconds + 60 * bar_minutes * np.arange(n_bars)
    values = np.column_stack([timestamps, opens, highs, lows, closes, volumes])
    return Bars(values, symbol, bar_minutes)


def read_synthetic_csv(
    path: Path, n_bars: int, bar_minutes: int, symbol: str, *, start_at: datetime
) -> tuple[Bars, str]:
    """Read declared synthetic OHLCV and bind the exact bytes used."""
    if not path.is_file():
        raise ValueError("Expected a regular local CSV file.")
    with path.open("rb") as stream:
        payload = stream.read(MAX_SYNTHETIC_CSV_BYTES + 1)
    if len(payload) > MAX_SYNTHETIC_CSV_BYTES:
        raise ValueError("CSV exceeds 32 MiB.")
    rows = csv.reader(StringIO(payload.decode("utf-8-sig"), newline=""), strict=True)
    if tuple(next(rows, ())) != SYNTHETIC_CSV_FIELDS:
        raise ValueError("Unexpected CSV header.")
    values = np.empty((n_bars, 6), dtype=float)
    first_open = start_at.timestamp()
    step_seconds = 60 * bar_minutes
    count = 0
    for count, row in enumerate(rows, 1):
        if count > n_bars:
            raise ValueError("CSV row count exceeds n_bars.")
        if len(row) != len(SYNTHETIC_CSV_FIELDS) or row[-1] != "synthetic":
            raise ValueError(f"CSV row {count} must be marked synthetic.")
        opened = utc_timestamp(row[0]).timestamp()
        if opened != first_open + (count - 1) * step_seconds:
            raise ValueError(f"CSV row {count} is outside the declared UTC cadence.")
        values[count - 1] = [opened, *map(float, row[1:6])]
    if count != n_bars:
        raise ValueError("CSV row count does not match n_bars.")
    bars = Bars(values, symbol, bar_minutes)
    validate(bars)
    return bars, sha256(payload).hexdigest()


def bar_reversal_predictions(
    bars: Bars, train: slice, evaluation: slice
) -> tuple[int, np.ndarray, np.ndarray]:
    signs = np.sign(bars.values[:, 4] - bars.values[:, 1]).astype(int)
    majority = 1 if np.sum(signs[train]) >= 0 else -1
    prediction = -signs[evaluation.start - 1 : evaluation.stop - 1].copy()
    prediction[prediction == 0] = majority
    return majority, prediction, signs[evaluation]


def volume_movement_predictions(
    bars: Bars, train: slice, evaluation: slice
) -> tuple[tuple[float, float], np.ndarray, np.ndarray]:
    """Use completed-bar volume to predict next-bar absolute movement."""
    _, opens, _, _, closes, volumes = bars.values.T
    volume_median = float(np.median(volumes[train]))
    movement_median = float(np.median(np.abs(closes[train] / opens[train] - 1)))
    previous_volume = volumes[evaluation.start - 1 : evaluation.stop - 1]
    actual_movement = np.abs(closes[evaluation] / opens[evaluation] - 1)
    prediction = np.where(previous_volume > volume_median, 1, -1)
    actual = np.where(actual_movement > movement_median, 1, -1)
    return (volume_median, movement_median), prediction, actual


@dataclass(frozen=True)
class BarRule:
    predictions: Callable[
        [Bars, slice, slice], tuple[int | tuple[float, float], np.ndarray, np.ndarray]
    ]
    result_key: str
    decision_stem: str
    controls: tuple[str, str]
    label: str
    target: str
    hypothesis: str
    parameters: dict[str, str]
    version: str = "1"


BAR_RULES = {
    "bar_reversal": BarRule(
        predictions=bar_reversal_predictions,
        result_key="directional_reversal",
        decision_stem="REVERSAL",
        controls=("always_up", "always_down"),
        label="reversal",
        target="direction",
        hypothesis="The next bar direction may reverse the last completed bar.",
        parameters={"flat_signal": "training_majority", "majority_tie": "up"},
        version="2",
    ),
    "volume_movement": BarRule(
        predictions=volume_movement_predictions,
        result_key="volume_movement",
        decision_stem="VOLUME_MOVEMENT",
        controls=("always_above", "always_below"),
        label="volume-movement",
        target="absolute movement",
        hypothesis="Above-median volume may predict above-median next-bar movement.",
        parameters={
            "thresholds": "per_fold_training_medians",
            "return": "absolute_open_to_close_simple_return",
            "tie": "below",
        },
    ),
}


def validate(bars: Bars) -> None:
    values = bars.values
    if values.ndim != 2 or values.shape[1] != 6 or not len(values):
        raise ValueError("Expected a nonempty OHLCV series.")
    if not np.isfinite(values).all():
        raise ValueError("OHLCV data contain nonfinite values.")
    times, opens, highs, lows, closes, volumes = values.T
    if bars.bar_minutes < 1 or not np.all(np.diff(times) == 60 * bars.bar_minutes):
        raise ValueError(
            "Bar timestamps must be unique and match the configured cadence."
        )
    if np.any(lows <= 0) or np.any(volumes < 0):
        raise ValueError("Expected positive prices and nonnegative volume.")
    if np.any(lows > np.minimum(opens, closes)) or np.any(
        highs < np.maximum(opens, closes)
    ):
        raise ValueError("OHLC price bounds are inconsistent.")


def features(bars: Bars) -> np.ndarray:
    closes, volumes = bars.values[:, 4:6].T
    result = np.full((len(closes), len(FEATURE_NAMES)), np.nan)
    returns = closes[1:] / closes[:-1] - 1
    result[1:, 0] = returns
    if len(closes) > WARMUP:
        trailing_volume = sliding_window_view(volumes[:-1], WARMUP).mean(axis=1)
        result[WARMUP:, 1] = np.divide(
            volumes[WARMUP:],
            trailing_volume,
            out=np.zeros_like(trailing_volume),
            where=trailing_volume > 0,
        )
        result[WARMUP:, 2] = sliding_window_view(returns, WARMUP).std(axis=1)
    return result


def targets(bars: Bars, horizon: int) -> np.ndarray:
    opens = bars.values[:, 1]
    return opens[horizon + 1 :] / opens[1:-horizon] - 1


def build_folds(
    research_rows: int,
    horizon: int,
    train_bars: int,
    validation_bars: int,
    count: int,
) -> list[tuple[slice, slice]]:
    gap = horizon + 1
    if train_bars - gap <= WARMUP:
        raise ValueError("Training interval leaves no rows after warm-up and purge.")
    if validation_bars <= gap:
        raise ValueError("Validation interval leaves no rows after purge.")
    if train_bars + count * validation_bars > research_rows:
        raise ValueError("Validation labels would enter the reserved holdout.")
    return [
        (
            slice(WARMUP, cutoff - gap),
            slice(cutoff, cutoff + validation_bars - gap),
        )
        for cutoff in range(
            train_bars, train_bars + count * validation_bars, validation_bars
        )
    ]


def write_dataset(bars: Bars, path: Path) -> None:
    fingerprint = bars.fingerprint
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(
            [
                "bar_open_time",
                "bar_close_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "symbol",
                "dataset_id",
            ]
        )
        for index, (_, *ohlcv) in enumerate(bars.values):
            writer.writerow(
                [
                    bars.time(index),
                    bars.time(index, close=True),
                    *ohlcv,
                    bars.symbol,
                    fingerprint,
                ]
            )
