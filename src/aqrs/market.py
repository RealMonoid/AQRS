import csv
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

FEATURE_NAMES = ("past_return", "relative_volume", "rolling_volatility")
WARMUP = 12


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
    seconds = datetime(2024, 1, 1, tzinfo=UTC).timestamp()
    timestamps = seconds + 60 * bar_minutes * np.arange(n_bars)
    values = np.column_stack([timestamps, opens, highs, lows, closes, volumes])
    return Bars(values, symbol, bar_minutes)


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
