"""Synthetic regressions for causal controls and research-evidence boundaries."""

from datetime import UTC, datetime
from importlib import import_module, util
from pathlib import Path

import numpy as np
import pytest

from aqrs.evaluation import simulate
from aqrs.market import Bars, targets, validate
from scripts import m2_isolation_forest_pilot as pilot


@pytest.fixture(scope="module")
def historical_scanner():
    path = (
        Path(__file__).resolve().parents[1]
        / "evidence/historical/m2-e02/count_pairs.py"
    )
    spec = util.spec_from_file_location("historical_count_pairs", path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def planted_drop():
    closes = np.full(1440, 100.0)
    closes[85:90] = [99.9, 99.8, 99.7, 99.6, 99.5]
    closes[90:] = 99.5
    return closes


def test_historical_control_contains_the_planted_trigger(
    historical_scanner, planted_drop
):
    pair = historical_scanner.scan(planted_drop)[0]["pair"]
    assert pair == {"event_entry_minute_utc": 90, "control_entry_minute_utc": 75}
    # This is a count-only reproduction: the control hold covers the trigger window.
    assert pair["control_entry_minute_utc"] + 15 == pair["event_entry_minute_utc"]


def test_control_exit_excludes_a_next_open_jump_at_the_lookback_boundary(planted_drop):
    events = import_module("aqrs.events")
    opened = np.r_[100.0, planted_drop[:-1]]
    opened[85] = 99.5  # close[84] is 100; shared timestamp does not imply equal price.
    start = datetime(2024, 1, 1, tzinfo=UTC).timestamp()
    values = np.column_stack(
        [
            start + 60 * np.arange(1440),
            opened,
            np.maximum(opened, planted_drop),
            np.minimum(opened, planted_drop),
            planted_drop,
            np.ones(1440),
        ]
    )
    bars = Bars(values, "SYNTH", 1)
    validate(bars)
    pair = events.scan(planted_drop)[0]["pair"]
    control, event = pair["control_entry_minute_utc"], pair["event_entry_minute_utc"]
    assert control + 15 < event - 5
    outcomes = [
        simulate(
            bars,
            np.array([entry - 1]),
            np.ones(1),
            15,
            False,
            1,
            0,
            pilot.prior.COSTS,
        )
        for entry in [control, event]
    ]
    assert outcomes[0]["gross_pnl"] == outcomes[1]["gross_pnl"] == 0
    assert outcomes[0]["net_pnl"] == outcomes[1]["net_pnl"]


def test_full_day_price_drop_v2_excludes_the_trigger_from_the_control_hold(
    planted_drop,
):
    events = import_module("aqrs.events")
    assert events.scan(planted_drop) == [
        {
            "block_start_minute_utc": 0,
            "trigger_count": 1,
            "eligible_trigger_count": 1,
            "pair": {"event_entry_minute_utc": 90, "control_entry_minute_utc": 69},
        },
        {
            "block_start_minute_utc": 480,
            "trigger_count": 0,
            "eligible_trigger_count": 0,
            "pair": None,
        },
        {
            "block_start_minute_utc": 960,
            "trigger_count": 0,
            "eligible_trigger_count": 0,
            "pair": None,
        },
    ]


@pytest.mark.parametrize("effect_bps", [0, 30])
def test_design_self_check_rejects_v1_bias_and_recovers_v2_effect(
    historical_scanner, planted_drop, effect_bps
):
    # The trigger exists in both cases; only the post-entry outcome differs.
    # A completely constant price series would never challenge event selection.
    events = import_module("aqrs.events")
    opened = np.r_[100.0, planted_drop[:-1]]
    opened[105:] *= 1 + effect_bps / 10_000
    closed = planted_drop.copy()
    closed[105:] *= 1 + effect_bps / 10_000
    start = datetime(2024, 1, 1, tzinfo=UTC).timestamp()
    values = np.column_stack(
        [
            start + 60 * np.arange(1440),
            opened,
            np.maximum(opened, closed),
            np.minimum(opened, closed),
            closed,
            np.ones(1440),
        ]
    )
    bars = Bars(values, "SYNTH", 1)
    validate(bars)
    advantages = []
    for scanner in (historical_scanner.scan, events.scan):
        pair = scanner(bars.values[:, 4])[0]["pair"]
        outcomes = [
            simulate(
                bars,
                np.array([pair[key] - 1]),
                np.ones(1),
                15,
                False,
                1,
                0,
                pilot.prior.COSTS,
            )["net_pnl"]
            for key in ("event_entry_minute_utc", "control_entry_minute_utc")
        ]
        advantages.append(10_000 * (outcomes[0] - outcomes[1]))
    assert advantages == pytest.approx([50 + effect_bps, effect_bps], abs=1e-10)
    # The design check must reject the known biased definition, including under null.
    admitted = [abs(advantage - effect_bps) <= 1e-10 for advantage in advantages]
    assert admitted == [False, True]


@pytest.mark.parametrize("controls", [[70], [75], [105], [75, 105], []])
def test_v2_leaves_event_unmatched_without_an_uncontaminated_earlier_control(controls):
    events = import_module("aqrs.events")
    volatility = dict.fromkeys([90, *controls], 1.0)
    assert events.first_pair([90], controls, volatility) is None


def test_v2_requires_strict_boundary_and_preserves_first_event_and_nearest_control():
    events = import_module("aqrs.events")
    volatility = dict.fromkeys([60, 65, 69, 70, 71, 75, 90, 95], 1.0)
    expected = {"event_entry_minute_utc": 90, "control_entry_minute_utc": 69}
    for controls in ([75, 65, 60, 70, 69], [69, 70, 60, 65, 75]):
        assert events.first_pair([90, 95], controls, volatility) == expected
    assert events.first_pair([90], [71], volatility) is None


def test_v2_keeps_same_hour_and_prior_volatility_comparability():
    events = import_module("aqrs.events")
    volatility = {59: 2.0, 65: 1.0, 70: 0.99, 90: 2.0}
    assert events.first_pair([90], [59, 70], volatility) is None
    assert events.first_pair([90], [59, 70, 65], volatility) == {
        "event_entry_minute_utc": 90,
        "control_entry_minute_utc": 65,
    }
    assert events.first_pair([90], [69], {69: 0.0, 90: 0.0}) == {
        "event_entry_minute_utc": 90,
        "control_entry_minute_utc": 69,
    }
    assert events.first_pair([90], [69], {69: 0.0, 90: 1.0}) is None


def test_future_closes_cannot_change_an_earlier_count_pair(planted_drop):
    events = import_module("aqrs.events")
    original = events.scan(planted_drop)
    changed = planted_drop.copy()
    changed[90:] = np.linspace(150.0, 500.0, len(changed) - 90)
    # Entry minute 90 uses close index 89. Everything replaced is future information.
    assert events.scan(changed)[0]["pair"] == original[0]["pair"]
    assert original[0]["pair"]["event_entry_minute_utc"] == 90


@pytest.mark.parametrize("count", [0, 1439, 1441])
def test_count_scan_requires_exactly_one_day(count):
    events = import_module("aqrs.events")
    with pytest.raises(ValueError):
        events.scan(np.full(count, 100.0))


@pytest.mark.parametrize(
    "bad_close", [0.0, -1.0, float("nan"), float("inf"), -float("inf")]
)
@pytest.mark.parametrize("index", [0, 1439])
def test_count_scan_validates_all_closes_including_the_excluded_last_close(
    bad_close, index
):
    events = import_module("aqrs.events")
    closes = np.full(1440, 100.0)
    closes[index] = bad_close
    with pytest.raises(ValueError):
        events.scan(closes)


@pytest.fixture
def opportunity_bars():
    prices = np.full(1440, 100.0)
    # Four independent clock-hour opportunities: control only, candidate only,
    # both at different times, and both at the same time. Later hours skip both.
    prices[[31, 91, 151, 153, 211]] = [99.0, 102.0, 101.0, 99.5, 100.5]
    start = datetime(2024, 1, 1, tzinfo=UTC).timestamp()
    values = np.column_stack(
        [start + 60 * np.arange(1440), prices, prices, prices, prices, np.ones(1440)]
    )
    bars = Bars(values, "SYNTH", 1)
    validate(bars)
    return bars


def simulate_alerts(bars, indices):
    return simulate(
        bars,
        np.asarray(indices, dtype=int),
        np.ones(len(indices)),
        pilot.HORIZON,
        False,
        1,
        0,
        pilot.prior.COSTS,
    )


def test_common_opportunities_include_skips_and_preserve_the_legacy_comparison(
    opportunity_bars,
):
    bars = opportunity_bars
    control, candidate = [0, 120, 180], [60, 122, 180]
    returns = targets(bars, pilot.HORIZON)
    result = pilot.paired_day(bars, slice(0, 1409), returns, control, candidate)
    legacy_hours = []
    for hour in range(24):
        c = next((index for index in control if index // 60 == hour), None)
        a = next((index for index in candidate if index // 60 == hour), None)
        difference = (
            float(10_000 * (abs(returns[a]) - abs(returns[c])))
            if c is not None and a is not None
            else None
        )
        legacy_hours.append(
            {
                "hour_utc": bars.time(hour * 60),
                "control_index": c,
                "challenger_index": a,
                "difference_bps": difference,
            }
        )
    assert result["hours"] == legacy_hours
    assert result["paired_hours"] == 2
    assert result["simultaneous_hours"] == 1
    assert result["control_only_hours"] == result["challenger_only_hours"] == 1
    assert result["mean_difference_bps"] == pytest.approx(-25.0)

    common = result["common_opportunity_trading"]
    assert common["opportunities"] == 24
    assert common["control_trade_count"] == common["candidate_trade_count"] == 3
    # The legacy absolute-movement comparison is negative; the full net difference
    # is positive. Excluding asymmetric action hours answers a different question.
    assert common["sum_incremental_net_bps"] == pytest.approx(150.0)
    assert common["mean_incremental_net_bps"] == pytest.approx(150.0 / 24)
    expected = (
        simulate_alerts(bars, candidate)["net_pnl"]
        - simulate_alerts(bars, control)["net_pnl"]
    ) * 10_000
    assert common["sum_incremental_net_bps"] == pytest.approx(expected, abs=1e-10)


@pytest.mark.parametrize(
    ("control", "candidate", "expected_bps"),
    [([], [], 0.0), ([0], [], 125.0), ([], [60], 175.0), ([180], [180], 0.0)],
    ids=["neither", "control-only", "candidate-only", "both"],
)
def test_each_action_skip_case_keeps_the_full_opportunity_denominator(
    opportunity_bars, control, candidate, expected_bps
):
    bars = opportunity_bars
    result = pilot.paired_day(
        bars, slice(0, 1409), targets(bars, pilot.HORIZON), control, candidate
    )
    common = result["common_opportunity_trading"]
    assert common["opportunities"] == 24
    assert common["control_trade_count"] == len(control)
    assert common["candidate_trade_count"] == len(candidate)
    assert common["sum_incremental_net_bps"] == pytest.approx(expected_bps)
    assert common["mean_incremental_net_bps"] == pytest.approx(expected_bps / 24)
    expected = (
        simulate_alerts(bars, candidate)["net_pnl"]
        - simulate_alerts(bars, control)["net_pnl"]
    ) * 10_000
    assert common["sum_incremental_net_bps"] == pytest.approx(expected, abs=1e-10)


def test_precision_plan_matches_a_hand_calculation_and_exposes_insufficient_capacity():
    plan = import_module("aqrs.planning").mean_precision_plan(10.0, 5.0, 16)
    # One-sided z(.95) + z(.80) = 1.6448536269514722 + .8416212335729143.
    # ceil((2.4864748605243865 * 10 / 5)^2) = 25 assumed independent units.
    assert plan["planning_only"] is True
    assert plan["required_independent_units"] == 25
    assert plan["standard_error_bps"] == pytest.approx(2.5)
    assert plan["detectable_mean_bps"] == pytest.approx(6.216187151310966)
    assert plan["target_within_assumed_capacity"] is False
    enough = import_module("aqrs.planning").mean_precision_plan(10.0, 5.0, 25)
    assert enough["planning_only"] is True
    assert enough["standard_error_bps"] == pytest.approx(2.0)
    assert enough["detectable_mean_bps"] == pytest.approx(4.972949721048773)
    assert enough["target_within_assumed_capacity"] is True


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("sd_bps", 0),
        ("sd_bps", -1),
        ("sd_bps", float("nan")),
        ("sd_bps", float("inf")),
        ("sd_bps", True),
        ("effect_bps", 0),
        ("effect_bps", -1),
        ("effect_bps", float("nan")),
        ("effect_bps", float("inf")),
        ("effect_bps", True),
        ("independent_units", 0),
        ("independent_units", -1),
        ("independent_units", 1.5),
        ("independent_units", float("nan")),
        ("independent_units", float("inf")),
        ("independent_units", True),
        ("alpha", 0),
        ("alpha", 1),
        ("alpha", -0.05),
        ("alpha", float("nan")),
        ("alpha", float("inf")),
        ("alpha", True),
        ("power", 0),
        ("power", 1),
        ("power", -0.8),
        ("power", float("nan")),
        ("power", float("inf")),
        ("power", True),
    ],
)
def test_precision_plan_rejects_invalid_assumptions(field, value):
    calculate = import_module("aqrs.planning").mean_precision_plan
    inputs = {
        "sd_bps": 10.0,
        "effect_bps": 5.0,
        "independent_units": 16,
        "alpha": 0.05,
        "power": 0.8,
    }
    inputs[field] = value
    with pytest.raises(ValueError):
        calculate(**inputs)


def test_precision_plan_keeps_a_small_positive_alpha_numerically_valid():
    calculate = import_module("aqrs.planning").mean_precision_plan
    plan = calculate(10.0, 5.0, 16, alpha=1e-300)
    assert plan["planning_only"] is True
    assert plan["required_independent_units"] > 25
    assert np.isfinite(plan["detectable_mean_bps"])
    assert plan["target_within_assumed_capacity"] is False


def test_precision_plan_rejects_unrepresentable_normal_approximation():
    calculate = import_module("aqrs.planning").mean_precision_plan
    with pytest.raises(ValueError):
        calculate(10.0, 1e-300, 16)


@pytest.mark.parametrize(
    ("indices", "status"),
    [([], "NO_TRADES"), ([60], "SINGLE_TRADE"), ([60, 120], "DESCRIPTIVE_ONLY")],
)
def test_trade_counts_never_establish_an_economic_claim(
    opportunity_bars, indices, status
):
    result = simulate_alerts(opportunity_bars, indices)
    assert result["trade_count"] == len(indices)
    evidence = result["economic_evidence"]
    assert evidence["status"] == status
    assert evidence["supports_economic_claim"] is False


@pytest.mark.parametrize("indices", [[-1], [29], [0, 2], [60, 0], [0, 0], [1440]])
def test_common_opportunities_reject_alerts_that_cannot_map_to_one_trade_per_hour(
    opportunity_bars, indices
):
    with pytest.raises(ValueError):
        pilot.paired_day(
            opportunity_bars,
            slice(0, 1409),
            targets(opportunity_bars, pilot.HORIZON),
            indices,
            [],
        )
