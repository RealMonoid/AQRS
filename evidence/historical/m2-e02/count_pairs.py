"""Count eligible event and control pairs on the fixed M2-E02 development day."""

import json
from datetime import date
from decimal import Decimal
from pathlib import Path

from aqrs.binance_spot_pilot import import_day

DAY = date(2026, 1, 5)
ARCHIVE_SHA256 = "a29b45bdb88d5090cfecc61423dab084364a34db96b0788ab77cefc9d4b9567d"
DATASET_ID = "7ec539e452f4efc7063947409a905f9c3e975b06ddf2585d252cb1ef72457893"
BLOCK_MINUTES = 8 * 60
HOLD_MINUTES = 15
LOOKBACK = 5
VOLATILITY_MINUTES = 15
THRESHOLD_RATIO = Decimal("0.995")


def first_pair(events, controls, volatility):
    for event in events:
        comparable = [
            control
            for control in controls
            if control // 60 == event // 60
            and abs(control - event) >= HOLD_MINUTES
            and max(volatility[control], volatility[event])
            <= 2 * min(volatility[control], volatility[event])
        ]
        if comparable:
            control = min(comparable, key=lambda minute: (abs(minute - event), minute))
            return {"event_entry_minute_utc": event, "control_entry_minute_utc": control}
    return None


def scan(close_values):
    if len(close_values) != 3 * BLOCK_MINUTES:
        raise ValueError("Expected exactly one verified development day.")
    # The last bar completes at the holdout boundary and cannot be an observation.
    closes = [Decimal(str(price)) for price in close_values[:-1]]
    below = [False] * LOOKBACK + [
        current <= earlier * THRESHOLD_RATIO
        for earlier, current in zip(closes, closes[LOOKBACK:])
    ]
    # Store each return at the index of its ending close.
    absolute_returns = [Decimal(0)] + [
        abs(current / previous - 1) for previous, current in zip(closes, closes[1:])
    ]
    blocks = []
    for start in range(0, len(close_values), BLOCK_MINUTES):
        end = start + BLOCK_MINUTES
        triggers = []
        events = []
        controls = []
        volatility = {}
        for minute in range(max(start, LOOKBACK + 2), end):
            index = minute - 1  # The previous minute's close is known at entry.
            is_event = below[index] and not below[index - 1]
            if is_event:
                triggers.append(minute)
            volatility_end = index - LOOKBACK
            if volatility_end < VOLATILITY_MINUTES or minute + HOLD_MINUTES >= end:
                continue
            first_return = volatility_end - VOLATILITY_MINUTES + 1
            volatility[minute] = (
                sum(absolute_returns[first_return : volatility_end + 1])
                / VOLATILITY_MINUTES
            )
            if is_event:
                events.append(minute)
            if not below[index]:
                controls.append(minute)
        blocks.append(
            {
                "block_start_minute_utc": start,
                "trigger_count": len(triggers),
                "eligible_trigger_count": len(events),
                "pair": first_pair(events, controls, volatility),
            }
        )
    return blocks


def main():
    archive = Path("artifacts/m1-e02/BTCUSDT-1m-2026-01-05.zip")
    bars, digest = import_day(archive, archive.with_suffix(".zip.CHECKSUM"), DAY)
    if digest != ARCHIVE_SHA256 or bars.fingerprint != DATASET_ID:
        raise ValueError("Development archive or dataset differs from the M1 record.")
    blocks = scan(bars.values[:, 4])
    decision = "PROPOSE_OUTCOME_EXERCISE" if all(row["pair"] for row in blocks) else "DEFER"
    print(
        json.dumps(
            {
                "variant_id": "M2-E02",
                "development_day_utc": DAY.isoformat(),
                "archive_sha256": digest,
                "dataset_id": bars.fingerprint,
                "holdout_reads": 0,
                "forward_returns_evaluated": 0,
                "blocks": blocks,
                "decision": decision,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
