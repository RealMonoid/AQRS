"""Fixed count-only price-drop coverage; no forward returns or file access."""

from collections.abc import Mapping, Sequence
from decimal import Decimal, InvalidOperation

VARIANT_ID = "PRICE_DROP_V2"
BLOCK_MINUTES = 480
HOLD_MINUTES = 15
LOOKBACK = 5
VOLATILITY_MINUTES = 15
THRESHOLD_RATIO = Decimal("0.995")


def first_pair(
    events: Sequence[int],
    controls: Sequence[int],
    volatility: Mapping,
) -> dict | None:
    """Match an earlier control ending before the event-defining lookback.

    Eligibility and volatility must already use only information available at
    each entry. This retrospective contrast does not identify a causal effect.
    """
    for event in sorted(events):
        comparable = [
            control
            for control in controls
            if control // 60 == event // 60
            and control + HOLD_MINUTES <= event - LOOKBACK
            and max(volatility[control], volatility[event])
            <= 2 * min(volatility[control], volatility[event])
        ]
        if comparable:
            return {
                "event_entry_minute_utc": event,
                "control_entry_minute_utc": max(comparable),
            }
    return None


def scan(close_values: Sequence) -> list[dict]:
    """Count a caller-validated UTC day of 1,440 contiguous minute closes.

    This function cannot validate timestamps or authorize a dataset. Callers
    must use the importer and campaign admission before supplying real data.
    Historical PRICE_DROP_V1 counts cannot establish this variant's coverage.
    """
    if len(close_values) != 3 * BLOCK_MINUTES:
        raise ValueError("Expected exactly one verified development day.")
    try:
        all_closes = [Decimal(str(price)) for price in close_values]
        if any(not price.is_finite() or price <= 0 for price in all_closes):
            raise ValueError("Expected positive finite closes.")
    except InvalidOperation as error:
        raise ValueError("Expected positive finite closes.") from error
    # Retain V1's observation boundary: the final close is not an observation.
    closes = all_closes[:-1]
    below = [False] * LOOKBACK + [
        current <= earlier * THRESHOLD_RATIO
        for earlier, current in zip(closes, closes[LOOKBACK:])
    ]
    absolute_returns = [Decimal(0)] + [
        abs(current / previous - 1) for previous, current in zip(closes, closes[1:])
    ]
    blocks = []
    for start in range(0, len(close_values), BLOCK_MINUTES):
        end = start + BLOCK_MINUTES
        triggers, events, controls = [], [], []
        volatility = {}
        for minute in range(max(start, LOOKBACK + 2), end):
            index = minute - 1  # Previous completed close, before entry.
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
