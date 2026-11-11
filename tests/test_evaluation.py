import json
from dataclasses import replace

import numpy as np
import pytest

from aqrs import evaluation
from aqrs.evaluation import evaluate, simulate
from aqrs.market import build_folds, features, generate, validate


@pytest.mark.parametrize(
    "actual,predicted,expected",
    [
        ([1, 2, 3, 4], [1, 2, 3, 4], 1.0),
        ([1, 2, 3, 4], [4, 3, 2, 1], -1.0),
        ([1, 2, 3, 4], [2, 4, 1, 3], 0.0),
        ([1, 1, 2, 3], [1, 2, 2, 3], 5 / 6),
    ],
)
def test_prediction_diagnostics_preserve_sign_zero_and_average_ties(
    actual, predicted, expected
):
    actual = np.array(actual, dtype=float) / 10_000
    predicted = np.array(predicted, dtype=float) / 10_000
    before = actual.copy(), predicted.copy()
    metrics = evaluation.prediction_metrics(actual, predicted)
    diagnostic = metrics["diagnostics"]
    assert diagnostic["rank_correlation"] == pytest.approx(expected, abs=1e-12)
    assert diagnostic["rank_status"] == "DEFINED"
    assert diagnostic["scope"] == "DESCRIPTIVE_ONLY"
    assert diagnostic["independent_sample_size"] is None
    assert diagnostic["supports_economic_claim"] is False
    np.testing.assert_array_equal(actual, before[0])
    np.testing.assert_array_equal(predicted, before[1])
    json.dumps(metrics, allow_nan=False)


def test_prediction_dispersion_uses_simple_returns_and_population_standard_deviation():
    metrics = evaluation.prediction_metrics(
        np.array([0, 0.002, 0.004, 0.006]), np.array([0, 0.001, 0.002, 0.003])
    )
    diagnostic = metrics["diagnostics"]
    assert diagnostic["prediction_mean"] == pytest.approx(0.0015)
    assert diagnostic["prediction_std"] == pytest.approx(0.001118033988749895)
    assert diagnostic["target_mean"] == pytest.approx(0.003)
    assert diagnostic["target_std"] == pytest.approx(0.00223606797749979)
    assert metrics["mae"] == pytest.approx(0.0015)
    assert metrics["zero_mae"] == pytest.approx(0.003)


@pytest.mark.parametrize(
    "actual,predicted,status",
    [
        ([1, 2], [0, 0], "CONSTANT_PREDICTION"),
        ([1, 1], [0, 1], "CONSTANT_TARGET"),
        ([1], [2], "INSUFFICIENT_OBSERVATIONS"),
    ],
)
def test_undefined_rank_is_null_with_a_reason(actual, predicted, status):
    metrics = evaluation.prediction_metrics(np.array(actual), np.array(predicted))
    assert metrics["diagnostics"]["rank_correlation"] is None
    assert metrics["diagnostics"]["rank_status"] == status
    json.dumps(metrics, allow_nan=False)


@pytest.mark.parametrize(
    "actual,predicted",
    [
        ([], []),
        ([1, 2], [1]),
        ([[1, 2]], [[1, 2]]),
        ([1, np.nan], [1, 2]),
        ([1, 2], [1, np.inf]),
    ],
)
def test_prediction_metrics_reject_invalid_or_misaligned_pairs(actual, predicted):
    with pytest.raises(ValueError):
        evaluation.prediction_metrics(np.array(actual), np.array(predicted))


def test_opposite_fold_associations_remain_visible_without_extra_fits(tmp_path):
    class FixedForecast:
        # Deliberate fixture forecast, not a trained or deployable research model.
        def fit(self, x, y):
            return self

        def predict(self, x):
            return np.array([1, 2, 3, 4]) / 10_000

    bars = generate(7, 80, 5, "SYNTH")
    opened = bars.values[:, 1].copy()
    opened[21:26] = 100 * np.cumprod([1, 1.001, 1.002, 1.003, 1.004])
    opened[31:36] = 100 * np.cumprod([1, 1.004, 1.003, 1.002, 1.001])
    bars.values[:, 1:5] = opened[:, None]
    np.save(tmp_path / "prefix.npy", bars.values, allow_pickle=False)
    result = evaluate(
        {
            "prefix": str(tmp_path / "prefix.npy"),
            "bar_minutes": 5,
            "symbol": "SYNTH",
            "folds": [[12, 16, 20, 24], [12, 26, 30, 34]],
            "horizon": 1,
            "features": ["past_return"],
            "allow_short": False,
            "notional": 1,
            "costs": {
                "fee_bps_per_side": 0,
                "quoted_spread_bps": 0,
                "slippage_bps_per_side": 0,
                "decision_buffer_bps": 0,
            },
        },
        tmp_path,
        model_factory=FixedForecast,
    )
    assert [
        f["prediction"]["diagnostics"]["rank_correlation"] for f in result["folds"]
    ] == pytest.approx([1, -1])
    assert json.loads((tmp_path / "fits.json").read_text()) == 2
    assert result["prediction"]["observations"] == 8
    exposure = result["diagnostic_exposure"]
    assert len(exposure) == 15
    assert {row["view"] for row in exposure} == {"aggregate", "fold_1", "fold_2"}
    assert len({row["diagnostic_id"] for row in exposure}) == 5
    aggregate = [row for row in exposure if row["view"] == "aggregate"]
    assert all(row["validation_intervals"] == [[20, 24], [30, 34]] for row in aggregate)
    assert all(row["horizon_bars"] == 1 for row in exposure)


def test_matched_policy_uses_next_open_and_costs_cannot_improve_fixed_trades():
    bars = generate(7, 80, 5, "SYNTH")
    indices = np.arange(12, 24)
    scores = np.tile([0.1, 0, -0.1], 4)
    costs = {"fee_bps_per_side": 4, "quoted_spread_bps": 3, "slippage_bps_per_side": 2}
    low = simulate(bars, indices, scores, 3, True, 1, 0.01, costs)
    high = simulate(
        bars, indices, scores, 3, True, 1, 0.01, costs | {"fee_bps_per_side": 8}
    )
    assert low["trade_count"] == high["trade_count"] > 0
    for first, second in zip(low["trades"], high["trades"], strict=True):
        assert first["entry_index"] == first["signal_index"] + 1
        assert first["exit_index"] == first["signal_index"] + 4
        assert first["entry_at"] == first["available_at"]
        assert first["gross_pnl"] == second["gross_pnl"]
        assert first["net_pnl"] > second["net_pnl"]
    assert low["gross_pnl"] - low["net_pnl"] == pytest.approx(
        0.0015 * low["trade_count"]
    )


def test_future_bars_do_not_change_an_earlier_momentum_decision():
    bars = generate(7, 80, 5, "SYNTH")
    signal = 40
    bars.values[signal, 1:5] = bars.values[signal - 1, 4] * 1.01
    changed_values = bars.values.copy()
    changed_values[signal + 1, 1:5] *= 1.5
    changed_values[signal + 1 :, 5] *= 2
    changed = replace(bars, values=changed_values)
    validate(bars)
    validate(changed)

    original_features = features(bars)
    changed_features = features(changed)
    np.testing.assert_array_equal(
        original_features[: signal + 1], changed_features[: signal + 1]
    )
    assert not np.array_equal(
        original_features[signal + 1], changed_features[signal + 1]
    )

    indices = np.array([signal])
    costs = {"fee_bps_per_side": 4, "quoted_spread_bps": 3, "slippage_bps_per_side": 2}
    original = simulate(
        bars, indices, original_features[indices, 0], 3, True, 1, 0.0017, costs
    )
    perturbed = simulate(
        changed, indices, changed_features[indices, 0], 3, True, 1, 0.0017, costs
    )
    assert original["decisions"] == perturbed["decisions"]
    assert original["decisions"] == {"long": 1, "short": 0, "flat": 0}
    before = original["trades"][0]
    after = perturbed["trades"][0]
    signal_time = bars.time(signal, close=True)
    assert before["available_at"] == after["available_at"] == signal_time
    assert before["entry_index"] == after["entry_index"] == signal + 1
    assert before["exit_index"] == after["exit_index"] == signal + 4
    assert before["entry_price"] != after["entry_price"]
    assert before["net_pnl"] != after["net_pnl"]


def test_fit_uses_only_training_statistics_and_controls_match_rows(tmp_path):
    bars = generate(7, 160, 5, "SYNTH")
    np.save(tmp_path / "prefix.npy", bars.values[:140], allow_pickle=False)
    request = {
        "prefix": str(tmp_path / "prefix.npy"),
        "bar_minutes": 5,
        "symbol": "SYNTH",
        "folds": [[12, 46, 50, 70], [12, 66, 70, 90]],
        "horizon": 3,
        "features": ["past_return"],
        "allow_short": True,
        "notional": 1,
        "costs": {
            "fee_bps_per_side": 4,
            "quoted_spread_bps": 3,
            "slippage_bps_per_side": 2,
            "decision_buffer_bps": 2,
        },
    }
    result = evaluate(request, tmp_path)
    assert result["folds"][0]["training_feature_means"] == pytest.approx(
        features(bars)[12:46, :1].mean(axis=0)
    )
    assert result["prediction"]["observations"] == 40
    assert {row["observations"] for row in result["trading"].values()} == {40}
    assert result["trading"]["no_trade"]["trade_count"] == 0
    assert result["feasibility"]["scope"] == "TRAINING_MOVEMENT_SCALE_ONLY"
    assert result["feasibility"]["predictability_established"] is False
    assert "not a calibrated horizon forecast" in result["benchmark_scope"]["momentum"]
    assert all(t["exit_index"] < 140 for t in result["trading"]["candidate"]["trades"])


def test_evaluator_reports_training_means_for_an_unscaled_estimator(tmp_path):
    class UnscaledEstimator:
        def fit(self, features, targets):
            return self

        def predict(self, features):
            return np.zeros(len(features))

    bars = generate(7, 80, 5, "SYNTH")
    np.save(tmp_path / "prefix.npy", bars.values, allow_pickle=False)
    request = {
        "prefix": str(tmp_path / "prefix.npy"),
        "bar_minutes": bars.bar_minutes,
        "symbol": bars.symbol,
        "folds": [[12, 36, 40, 60]],
        "horizon": 3,
        "features": ["past_return"],
        "allow_short": False,
        "notional": 1,
        "costs": {
            "fee_bps_per_side": 0,
            "quoted_spread_bps": 0,
            "slippage_bps_per_side": 0,
            "decision_buffer_bps": 0,
        },
    }
    result = evaluate(request, tmp_path, model_factory=UnscaledEstimator)
    assert result["folds"][0]["training_feature_means"] == pytest.approx(
        features(bars)[12:36, :1].mean(axis=0)
    )
    assert result["trading"]["candidate"]["decisions"] == {
        "long": 0,
        "short": 0,
        "flat": 20,
    }
    assert result["prediction"]["diagnostics"]["rank_correlation"] is None
    assert result["prediction"]["diagnostics"]["rank_status"] == "CONSTANT_PREDICTION"
    assert result["prediction"]["diagnostics"]["prediction_std"] == 0
    assert (
        result["folds"][0]["prediction"]["diagnostics"]["rank_status"]
        == "CONSTANT_PREDICTION"
    )
    assert json.loads((tmp_path / "fits.json").read_text()) == 1


def test_future_bars_do_not_change_an_earlier_fitted_candidate_decision(
    tmp_path, monkeypatch
):
    bars = generate(7, 80, 5, "SYNTH")
    bars.values[:, 1:5] = (100 * np.exp(0.0005 * np.arange(80) ** 2))[:, None]
    horizon = 3
    [(train, validation)] = build_folds(len(bars.values), horizon, 40, 8, 1)
    first_future = validation.stop
    changed_values = bars.values.copy()
    changed_values[first_future, 1:5] *= 1.5
    changed_values[first_future:, 5] *= 2
    validate(bars)
    validate(replace(bars, values=changed_values))

    def capture_scores(bars, indices, scores, *args):
        return simulate(bars, indices, scores, *args) | {"scores": scores.copy()}

    monkeypatch.setattr(evaluation, "simulate", capture_scores)
    request = {
        "bar_minutes": bars.bar_minutes,
        "symbol": bars.symbol,
        "folds": [[train.start, train.stop, validation.start, validation.stop]],
        "horizon": horizon,
        "features": ["past_return"],
        "allow_short": True,
        "notional": 1,
        "costs": {
            "fee_bps_per_side": 4,
            "quoted_spread_bps": 3,
            "slippage_bps_per_side": 2,
            "decision_buffer_bps": 2,
        },
    }
    results = []
    for name, values in (("original", bars.values), ("perturbed", changed_values)):
        directory = tmp_path / name
        directory.mkdir()
        prefix = directory / "prefix.npy"
        np.save(prefix, values, allow_pickle=False)
        results.append(evaluate(request | {"prefix": str(prefix)}, directory))
        assert json.loads((directory / "fits.json").read_text(encoding="utf-8")) == 1

    before, after = results
    training_means = before["folds"][0]["training_feature_means"]
    assert training_means == after["folds"][0]["training_feature_means"]
    original = before["trading"]["candidate"]
    perturbed = after["trading"]["candidate"]
    assert np.ptp(original["scores"]) > 0
    np.testing.assert_allclose(
        original["scores"],
        perturbed["scores"],
        rtol=0,
        atol=1e-12,
        err_msg="Candidate scores changed after a future-only perturbation.",
    )
    assert original["decisions"] == perturbed["decisions"]
    assert original["decisions"]["long"] > 0
    decision_fields = (
        "decision",
        "signal_index",
        "available_at",
        "entry_at",
        "exit_at",
    )
    for first, second in zip(original["trades"], perturbed["trades"], strict=True):
        assert all(first[key] == second[key] for key in decision_fields)
    last = original["trades"][-1]
    changed_last = perturbed["trades"][-1]
    assert last["signal_index"] == first_future - 1
    assert last["entry_index"] == changed_last["entry_index"] == first_future
    assert last["entry_price"] != changed_last["entry_price"]
    assert last["net_pnl"] != changed_last["net_pnl"]
