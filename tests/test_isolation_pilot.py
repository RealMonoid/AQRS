# Explicit __wrapped__ calls below test preserved inner algorithms; FR-005 entry tests use the guarded functions.
"""Verify the registered M2-E10 boundaries without fitting any estimator."""

from dataclasses import replace
from datetime import UTC, datetime

import numpy as np
import pytest

from aqrs.market import features, generate
from scripts import m2_isolation_forest_pilot as pilot


@pytest.fixture
def bars():
    window = generate(42, pilot.ROWS, 1, "BTCUSDT")
    window.values[:, 0] += (
        datetime(2026, 1, 1, tzinfo=UTC).timestamp() - window.values[0, 0]
    )
    return window


def test_only_registered_dates_and_in_hour_exits(bars, tmp_path):
    with pytest.raises(ValueError, match="allowlist"):
        pilot.prior.read_window(tmp_path, pilot.prior.DAYS[1:])
    with pytest.raises(ValueError, match="registered development days"):
        foreign = bars.values.copy()
        foreign[:, 0] += 60
        pilot.fixed_folds(replace(bars, values=foreign))

    folds = pilot.fixed_folds(bars)
    assert [(tr.stop - tr.start, va.stop - va.start) for tr, va in folds] == [
        (2837, 1409),
        (4277, 1409),
    ]
    for train, val in folds:
        assert train.stop + 30 == val.start - 1
        with pytest.raises(ValueError, match="validation boundaries"):
            pilot.alerts(slice(val.start, val.stop + 1), np.ones(1410))
        assert pilot.alerts(val, np.ones(1409)) == list(
            range(val.start, val.start + 1440, 60)
        )
        for minute in range(29):
            flags = np.arange(1409) % 60 >= minute
            for index in pilot.alerts(val, flags):
                assert index % 60 == minute
                assert (index + 31) // 60 == index // 60
        assert pilot.alerts(val, np.arange(1409) % 60 >= 29) == []


def test_fit_and_both_cutoffs_use_training_only(bars, tmp_path, monkeypatch):
    folds = pilot.fixed_folds(bars)
    matrix = features(bars)
    file = tmp_path / "development.npy"
    np.save(file, bars.values, allow_pickle=False)
    request = {"window": str(file), "dataset_id": bars.fingerprint}
    fits, scoring, quantiles = [], [], []
    original_cutoff = pilot.cutoff

    def spy_cutoff(values):
        quantiles.append(values.copy())
        return original_cutoff(values)

    class Spy:
        def fit(self, inputs):
            fits.append(inputs.copy())

        def score_samples(self, inputs):
            scoring.append(inputs.copy())
            return -inputs[:, 0]

    monkeypatch.setattr(pilot, "cutoff", spy_cutoff)
    monkeypatch.setattr(pilot, "estimator", Spy)
    control_dir, challenger_dir = tmp_path / "control", tmp_path / "challenger"
    control_dir.mkdir()
    challenger_dir.mkdir()
    control = pilot.evaluate_worker.__wrapped__(request | {"phase": pilot.CONTROL}, control_dir)
    assert fits == []
    challenger = pilot.evaluate_worker.__wrapped__(
        request
        | {
            "phase": pilot.CHALLENGER,
            "volatility_cutoffs": [day["volatility_cutoff"] for day in control],
        },
        challenger_dir,
    )
    assert len(quantiles) == 4
    assert len(fits) == 2
    for i, (train, validation) in enumerate(folds):
        np.testing.assert_array_equal(quantiles[i], matrix[train, 2])
        np.testing.assert_array_equal(quantiles[2 + i], matrix[train, 0])
        np.testing.assert_array_equal(fits[i], matrix[train])
        np.testing.assert_array_equal(scoring[3 * i], matrix[train])
        np.testing.assert_array_equal(scoring[3 * i + 1], matrix[validation])
        prefix = challenger[i]["future_check"]["prefix_rows"]
        np.testing.assert_array_equal(
            scoring[3 * i + 2][:prefix], matrix[validation][:prefix]
        )
        assert not np.array_equal(
            scoring[3 * i + 2][prefix:], matrix[validation][prefix:]
        )
        assert challenger[i]["future_check"]["max_score_difference"] == 0


def test_future_dependent_scores_fail_closed(bars):
    class LeakySpy:
        def fit(self, inputs):
            pass

        def score_samples(self, inputs):
            return inputs[:, 2] + np.max(inputs[:, 2])

    train, val = pilot.fixed_folds(bars)[0]
    with pytest.raises(ValueError, match="Future perturbation"):
        pilot.score_fold(LeakySpy(), bars, features(bars), train, val, 0, lambda: None)


def test_pairs_and_cost_diagnostic_keep_separate_meanings(bars):
    from aqrs.market import targets

    _, val = pilot.fixed_folds(bars)[0]
    base = val.start
    returns = targets(bars, pilot.HORIZON)
    control = [base, base + 60, base + 120]
    challenger = [base, base + 62]
    day = pilot.paired_day(bars, val, returns, control, challenger)
    delta = 10_000 * (abs(returns[base + 62]) - abs(returns[base + 60]))
    assert len(day["hours"]) == 24
    assert day["paired_hours"] == 2
    assert day["simultaneous_hours"] == 1
    assert day["control_only_hours"] == 1
    assert day["challenger_only_hours"] == 0
    assert day["hours"][0]["difference_bps"] == 0
    assert day["hours"][2]["difference_bps"] is None
    assert day["hours"][23]["control_index"] is None
    assert day["mean_difference_bps"] == delta / 2

    diagnostic = pilot.diagnostic(bars, control)
    assert diagnostic["decisions"] == {"long": 3, "short": 0, "flat": 0}
    assert sum(diagnostic["cost_totals"].values()) == pytest.approx(3 * 0.0025)
    assert diagnostic["net_pnl"] == pytest.approx(sum(returns[control]) - 3 * 0.0025)
    assert diagnostic["turnover"] == 6
    assert pilot.diagnostic(bars, [])["net_bps_per_alert"] is None


def test_replay_discrete_results_are_exact_and_floats_use_absolute_tolerance():
    pilot.require_agreement(
        {"alert": 20, "value": [2.0]}, {"alert": 20, "value": [2.0 + 5e-9]}, "test"
    )
    with pytest.raises(ValueError, match="test.alert"):
        pilot.require_agreement({"alert": 20}, {"alert": 21}, "test")
    with pytest.raises(ValueError, match="test.value"):
        pilot.require_agreement({"value": 2.0}, {"value": 2.0 + 2e-8}, "test")


def test_governor_and_archive_checks_precede_timing_fit(tmp_path, monkeypatch):
    from pathlib import Path

    source = tmp_path / "source"
    source.mkdir()
    limits = source / "research.yaml"
    configuration = (
        Path(__file__).resolve().parents[1] / "configs/research.yaml"
    ).read_text()
    tighter = configuration.replace(
        "max_model_fits_per_campaign: 12", "max_model_fits_per_campaign: 4"
    )
    limits.write_text(tighter, encoding="utf-8")
    monkeypatch.setattr(pilot, "capability", lambda _: None)

    def unexpected(*args, **kwargs):
        pytest.fail("Preflight must stop before the timing worker.")

    monkeypatch.setattr(pilot, "supervise", unexpected)
    with pytest.raises(ValueError, match="max_model_fits_per_campaign"):
        pilot.compare.__wrapped__(tmp_path, {}, None, 0)

    limits.write_text(configuration, encoding="utf-8")

    def foreign_archive(path):
        raise ValueError("Planted foreign archive.")

    monkeypatch.setattr(pilot.prior, "read_window", foreign_archive)
    with pytest.raises(ValueError, match="Planted foreign archive"):
        pilot.compare.__wrapped__(tmp_path, {}, None, 0)
