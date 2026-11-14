"""Declare and check research data scope without opening a dataset."""

import re
from datetime import UTC, date, datetime, time, timedelta

SYNTHETIC_START = datetime(2024, 1, 1, tzinfo=UTC)
M1_HOLDOUT_DAY = date(2026, 1, 6)
SPOT_HOLDOUT_START = date(2026, 9, 1)
SPOT_HOLDOUT_END = date(2026, 11, 1)
# The shared command applies these reservations to every declared source.
LOCKED_PERIODS = (
    (M1_HOLDOUT_DAY, M1_HOLDOUT_DAY + timedelta(days=1)),
    (SPOT_HOLDOUT_START, SPOT_HOLDOUT_END),
)
SOURCES = ("synthetic", "synthetic_csv", "binance_vision_spot")


class AdmissionRejected(ValueError):
    def __init__(self, code: str, reason: str):
        super().__init__(reason)
        self.code = code


def utc_timestamp(value: str) -> datetime:
    if not isinstance(value, str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:Z|\+00:00)",
        value,
    ):
        raise ValueError("Expected a UTC timestamp with seconds and Z or +00:00.")
    return datetime.fromisoformat(value)


def check_unlocked(start: datetime, end: datetime) -> None:
    for first_day, end_day in LOCKED_PERIODS:
        if start < datetime.combine(end_day, time.min, UTC) and end > datetime.combine(
            first_day, time.min, UTC
        ):
            raise AdmissionRejected(
                "LOCKED_PERIOD",
                f"Requested UTC interval overlaps the reserved period "
                f"{first_day} through {end_day} (exclusive).",
            )


def data_scope(market: dict) -> tuple[datetime, timedelta]:
    source = market["source"]
    if source not in SOURCES:
        raise AdmissionRejected("UNKNOWN_SOURCE", "Unknown data source.")
    try:
        if source == "synthetic_csv":
            start = utc_timestamp(market.get("start_at"))
        elif source == "binance_vision_spot":
            day = date.fromisoformat(market.get("day"))
            start = datetime.combine(day, time.min, UTC)
        else:
            start = SYNTHETIC_START
        step = timedelta(minutes=market["bar_minutes"])
        end = start + market["n_bars"] * step
    except (TypeError, ValueError, OverflowError) as error:
        raise AdmissionRejected(
            "INVALID_DATA_SCOPE",
            "Declare a valid UTC start and extent before opening research data. "
            "For synthetic_csv set market.start_at.",
        ) from error
    check_unlocked(start, end)
    return start, step
