"""Prospective filter checks on artificial inputs only; never market data."""

import json
import sqlite3
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pytest
from test_predictive_spot import month_payload

from aqrs import predictive_spot as base
from aqrs import reversal_filters as study
from aqrs.config import load


def test_ratio_influence_retains_empty_days_and_matches_delta_variance():
    counts = np.resize([0, 2, 8, 4], 365).astype(float)
    numerators = counts * np.resize([0, 0.3, 0.8, 0.5], 365)
    estimate, influence = study.ratio(numerators, counts)
    assert estimate == pytest.approx(numerators.sum() / counts.sum())
    assert len(influence) == 365
    assert abs(influence.mean()) < 1e-14
    assert np.all(influence[counts == 0] == 0)
    covariance = np.cov(np.stack([numerators, counts]), bias=True)
    gradient = np.array([1, -estimate]) / counts.mean()
    expected_se = np.sqrt(gradient @ covariance @ gradient / 365)
    result = study.interval(estimate, influence, 0)
    assert result["se"] == pytest.approx(expected_se)
    assert result["lower"] == pytest.approx(
        estimate - NormalDist().inv_cdf(0.995) * expected_se
    )
    assert result["estimate"] == estimate


def test_paired_ratio_contrast_accounts_for_shared_days():
    counts = np.resize([5, 15, 30], 365)
    hits = counts * np.resize([0.4, 0.6, 0.8], 365)
    value, influence = study.ratio(hits, counts)
    result = study.interval(value - value, influence - influence, 7)
    assert result["estimate"] == result["se"] == result["lower"] == 0


@pytest.mark.parametrize("key", ["large_move", "relative_volume", "taker_imbalance"])
def test_known_conditional_effect_and_null(key):
    bars, activity = study.synthetic_inputs()
    planted = study.measure(bars, activity, key)
    assert planted["prediction"]["decision"] == "EXPLORATORY_PREDICTIVE_PASS"
    assert planted["prediction"]["selected_cases"] > 0
    expected_lags = {"7", "14", "28"} if key == "relative_volume" else {"7", "14"}
    assert (
        set(planted["prediction"]["contrasts"]["selected_minus_unselected"])
        == expected_lags
    )
    assert planted["costs"]["status"] == "COMPLETED_ILLUSTRATIVE"
    null_bars, null_activity = study.synthetic_inputs(null=True)
    null = study.measure(null_bars, null_activity, key)
    assert null["prediction"]["decision"] != "EXPLORATORY_PREDICTIVE_PASS"
    assert null["costs"]["status"] == "NOT_RUN_PREDICTION_GATE"


def test_training_threshold_and_predictions_are_causal():
    bars, activity = study.synthetic_inputs()
    before = study.features(bars, activity)
    changed = bars.values.copy()
    changed[base.TRAIN + 100 :, 5] *= 20
    later = study.features(base.Bars(changed, "BTCUSDT", 30), activity)
    for key in before:
        np.testing.assert_array_equal(
            before[key][: base.TRAIN + 100], later[key][: base.TRAIN + 100]
        )
        first = study.calibrate(before[key])
        second = study.calibrate(later[key])
        assert first == second
    assert np.isnan(before["relative_volume"][:1344]).all()


def test_volume_filter_does_not_select_a_pure_weekly_calendar_pattern():
    bars = base.synthetic_bars()
    ix = np.arange(base.ROWS)
    bars.values[:, 5] = (1 + 9 * ((ix % 48) >= 42)) * (1 + 0.2 * ((ix // 48) % 7))
    feature = study.features(bars, bars.values[:, 5] / 2)["relative_volume"]
    np.testing.assert_allclose(feature[1344:], 1)
    threshold = study.calibrate(feature)
    assert not np.any(feature > threshold)
    bars.values[base.TRAIN + 10, 5] *= 3
    changed = study.features(bars, bars.values[:, 5] / 2)["relative_volume"]
    assert changed[base.TRAIN + 10] == pytest.approx(3)
    assert study.calibrate(changed) == threshold


def test_empty_filter_is_inconclusive_and_does_not_compute_costs(monkeypatch):
    bars = base.synthetic_bars()
    monkeypatch.setattr(
        study, "economics", lambda *args: pytest.fail("Cost stage must not run")
    )
    result = study.measure(bars, np.full(base.ROWS, 0.5), "large_move")
    assert result["prediction"]["decision"] == "INSUFFICIENT_COVERAGE"
    assert result["prediction"]["selected_cases"] == 0


def test_activity_parser_preserves_named_field_and_rejects_impossible_buy_volume():
    payload, checksum = month_payload("2024-09")
    bars, activity = study.parse_activity("2024-09", payload, checksum)
    assert len(activity) == len(bars.values)
    assert np.all(activity == 0.5)
    bad_payload, bad_checksum = month_payload(
        "2024-09", lambda rows: rows[0].__setitem__(9, 2)
    )
    with pytest.raises(ValueError, match="activity"):
        study.parse_activity("2024-09", bad_payload, bad_checksum)


def test_costs_preserve_full_opportunity_grid_and_fixed_unfiltered_control():
    bars, _ = study.synthetic_inputs()
    baseline, pred, _ = base.predictions(bars)
    selected = np.arange(len(pred)) % 3 == 0
    result = study.economics(bars, pred, baseline, selected)
    assert result["opportunities"] == len(pred) - 1
    for name in ("filtered", "unfiltered_reversal", "training_majority"):
        row = result[name]
        assert row["trades"] + row["flat"] == result["opportunities"]
        if row["trades"]:
            assert row["gross_bps_per_trade"] - row[
                "net_bps_per_trade"
            ] == pytest.approx(25)
    assert result["filtered"]["trades"] <= result["unfiltered_reversal"]["trades"]


def test_bad_scope_and_checksum_fail_before_archive_read(tmp_path, monkeypatch):
    def blocked(*args, **kwargs):
        pytest.fail("Out-of-scope paths must not be opened")

    monkeypatch.setattr(Path, "read_bytes", blocked)
    with pytest.raises(ValueError, match="scope"):
        study.read_archives(tmp_path, [{"month": "2026-12"}])


def test_unknown_variant_and_tighter_governor_are_rejected():
    with pytest.raises(ValueError):
        study.definition("unregistered_filter")
    config, _ = load(Path("configs/research.yaml"))
    assert study.preflight(config["resource_governor"])["fits"] == 2
    for key, value in [
        ("max_model_fits_per_campaign", 1),
        ("max_research_trials_per_campaign", 0),
        ("max_wall_seconds_per_trial", 0),
        ("max_wall_seconds_per_campaign", 1),
    ]:
        limits = deepcopy(config["resource_governor"])
        limits[key] = value
        with pytest.raises(ValueError):
            study.preflight(limits)


def test_guarded_worker_and_terminal_failure_journal(tmp_path):
    config, _ = load(Path("configs/research.yaml"))
    output = tmp_path / "good"
    report = study.campaign(
        output, "large_move", config["resource_governor"], synthetic=True
    )
    assert report["execution_status"] == "COMPLETED"
    assert report["worker"]["started_fits"] == 2
    assert report["worker"]["completed_fits"] == 2
    assert report["journal_integrity"] == "ok"
    with pytest.raises(FileExistsError):
        study.campaign(
            output, "large_move", config["resource_governor"], synthetic=True
        )
    failed = study.campaign(
        tmp_path / "failure",
        "large_move",
        config["resource_governor"],
        synthetic=True,
        inject_failure=True,
    )
    assert failed["execution_status"] == "FAILED"
    with sqlite3.connect(tmp_path / "failure/research.sqlite3") as db:
        assert db.execute("select execution_status from experiments").fetchall() == [
            ("FAILED",)
        ]
    assert json.loads((tmp_path / "failure/report.json").read_text())["results"] is None


def test_offline_archive_digests_are_enforced(tmp_path):
    inputs = []
    for month in base.MONTHS:
        payload, checksum = month_payload(month)
        stem = f"BTCUSDT-30m-{month}.zip"
        (tmp_path / stem).write_bytes(payload)
        (tmp_path / (stem + ".CHECKSUM")).write_bytes(checksum)
        inputs.append(
            {
                "month": month,
                "archive_sha256": sha256(payload).hexdigest(),
                "checksum_sha256": sha256(checksum).hexdigest(),
            }
        )
    bars, buy = study.read_archives(tmp_path, inputs)
    assert len(bars.values) == base.ROWS
    assert np.all(buy == 0.5)
    (tmp_path / "BTCUSDT-30m-2024-09.zip").write_bytes(b"changed")
    with pytest.raises(ValueError, match="digest"):
        study.read_archives(tmp_path, inputs)


def test_failed_preflight_never_starts_worker(tmp_path, monkeypatch):
    config, _ = load(Path("configs/research.yaml"))
    config["resource_governor"]["max_model_fits_per_campaign"] = 1
    monkeypatch.setattr(
        study, "snapshot", lambda *args: pytest.fail("Preflight must precede staging")
    )
    result = study.campaign(
        tmp_path / "rejected", "large_move", config["resource_governor"], synthetic=True
    )
    assert result["execution_status"] == "REJECTED_PREFLIGHT"
    assert result["worker"] is None
    with sqlite3.connect(tmp_path / "rejected/research.sqlite3") as db:
        assert db.execute("select execution_status from experiments").fetchall() == [
            ("REJECTED_PREFLIGHT",)
        ]


def test_registration_rejects_replaced_original_input_receipt(tmp_path):
    paths = (
        "configs/research.yaml",
        "docs/RESEARCH_PROTOCOL.md",
        "AGENTS.md",
        "tests/test_reversal_filters.py",
        "tests/test_predictive_spot.py",
        "docs/MILESTONE_STATUS.md",
    )
    for name in paths:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("placeholder")
    (tmp_path / "docs/MILESTONE_STATUS.md").write_text(
        "## M2-E23 to E25 Test Card: fixed\n## Research and backtesting learning\n"
    )
    receipt = tmp_path / "artifacts/m2-e22/run-01/acquisition.json"
    receipt.parent.mkdir(parents=True)
    receipt.write_text(
        json.dumps(
            {
                "status": "COMPLETED",
                "archives": [
                    {
                        "month": month,
                        "archive_sha256": "a" * 64,
                        "checksum_sha256": "b" * 64,
                    }
                    for month in base.MONTHS
                ],
            }
        )
    )
    with pytest.raises(ValueError, match="original E22"):
        study.register(tmp_path, "large_move")
