"""Known-answer and guarded execution checks; no market data or network."""

import csv
import io
import json
import sqlite3
import sys
from calendar import monthrange
from copy import deepcopy
from datetime import UTC, date, datetime
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import numpy as np
import pytest

from aqrs import predictive_spot as study
from aqrs.binance_spot_pilot import import_day, require_spot_identity
from aqrs.config import load
from aqrs.market import Bars


def test_registration_file_matches_git_lf_bytes(tmp_path, monkeypatch):
    (tmp_path / "evidence").mkdir()
    monkeypatch.setattr(
        study, "__file__", str(tmp_path / "src/aqrs/predictive_spot.py")
    )
    monkeypatch.setattr(study, "register", lambda root: {"status": "PLANNED_NOT_RUN"})
    monkeypatch.setattr(sys, "argv", ["predictive_spot", "--register"])
    assert study.main() == 0
    payload = (tmp_path / "evidence/m2-e22-preregistration.json").read_bytes()
    assert b"\r\n" not in payload


def fixture_bars(pattern=(1, -1)):
    n = 456 * 48
    signs = np.resize(pattern, n)
    values = np.column_stack(
        [
            datetime(2024, 9, 1, tzinfo=UTC).timestamp() + 1800 * np.arange(n),
            np.full(n, 100),
            np.full(n, 102),
            np.full(n, 98),
            100 + signs,
            np.ones(n),
        ]
    )
    return Bars(values, "BTCUSDT", 30)


def month_payload(month, damage=None):
    first = date.fromisoformat(month + "-01")
    n = monthrange(first.year, first.month)[1] * 48
    unit = 1000 if first.year < 2025 else 1_000_000
    start = int(datetime(first.year, first.month, 1, tzinfo=UTC).timestamp())
    rows = [
        [
            (start + i * 1800) * unit,
            100,
            102,
            98,
            101,
            1,
            (start + (i + 1) * 1800) * unit - 1,
            101,
            1,
            0.5,
            50.5,
            0,
        ]
        for i in range(n)
    ]
    if damage:
        damage(rows)
    text = io.StringIO()
    csv.writer(text).writerows(rows)
    payload = io.BytesIO()
    stem = f"BTCUSDT-30m-{month}"
    with ZipFile(payload, "w", ZIP_DEFLATED) as zipped:
        zipped.writestr(stem + ".csv", text.getvalue())
    data = payload.getvalue()
    checksum = f"{sha256(data).hexdigest()}  {stem}.zip\n".encode()
    return data, checksum


@pytest.mark.parametrize("day", ["2026-01-06", "2026-09-01", "2026-10-31"])
def test_holdout_guard(day):
    with pytest.raises(ValueError, match="reserved"):
        require_spot_identity("BTCUSDT", date.fromisoformat(day))


@pytest.mark.parametrize("named_day", ["2026-09-01", "2026-10-31"])
def test_legacy_import_rejects_protected_name_before_open(named_day, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("A protected archive must not be opened under another declared day")

    monkeypatch.setattr(Path, "open", forbidden)
    stem = f"BTCUSDT-1m-{named_day}.zip"
    with pytest.raises(ValueError, match="filename|reserved"):
        import_day(Path(stem), Path(stem + ".CHECKSUM"), date(2026, 8, 31))


@pytest.mark.parametrize("month", ["2026-01", "2026-09", "2026-10", "2025-12"])
def test_forbidden_month_rejected_before_fetch(month, monkeypatch, tmp_path):
    def forbidden(*args, **kwargs):
        pytest.fail("Network must not be called for out-of-scope month")

    monkeypatch.setattr(study, "fetch", forbidden)
    with pytest.raises(ValueError):
        study.acquire_month(month, tmp_path)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("month", ["2024-09", "2025-01"])
def test_archive_units_and_checksum(month):
    data, checksum = month_payload(month)
    bars = study.parse_month(month, data, checksum)
    assert len(bars.values) == monthrange(int(month[:4]), int(month[5:]))[1] * 48
    with pytest.raises(ValueError, match="checksum"):
        study.parse_month(month, data + b"x", checksum)


def test_archive_rejects_duplicate_timestamp():
    data, checksum = month_payload("2025-01", lambda r: r[1].__setitem__(0, r[0][0]))
    with pytest.raises(ValueError, match="cadence"):
        study.parse_month("2025-01", data, checksum)


def test_known_reversal_and_independent_pattern():
    perfect = study.measure(fixture_bars())
    assert perfect["prediction"]["target_count"] == 17520
    assert perfect["prediction"]["candidate_accuracy"] == 1
    assert perfect["prediction"]["decision"] == "PREDICTIVE_PASS"
    assert perfect["costs"]["status"] == "COMPLETED_ILLUSTRATIVE"
    assert perfect["costs"]["reversal"]["net_bps_per_trade"] == -25
    null = study.measure(fixture_bars((1, 1, -1, -1)))
    assert null["prediction"]["candidate_accuracy"] == 0.5
    assert null["prediction"]["decision"] == "BELOW_RELEVANT_EFFECT"
    assert null["costs"]["status"] == "NOT_RUN_PREDICTION_GATE"
    assert len(null["diagnostic_exposure"]) == 1104
    assert len(perfect["diagnostic_exposure"]) == 1116


def test_flat_ties_and_no_cost_gate_before_prediction():
    result = study.measure(fixture_bars((0,)))
    assert result["prediction"]["target_count"] == 17520
    assert result["prediction"]["candidate_accuracy"] == 0.5
    assert result["prediction"]["baseline_direction"] == 1
    assert result["costs"]["status"] == "NOT_RUN_PREDICTION_GATE"


def test_causal_feature_and_training_only_baseline():
    bars = fixture_bars()
    baseline, pred, truth = study.predictions(bars)
    assert np.array_equal(pred, truth)
    changed = Bars(bars.values.copy(), bars.symbol, bars.bar_minutes)
    changed.values[10000:, 4] = 101
    other_base, other_pred, _ = study.predictions(changed)
    assert baseline == other_base
    assert np.array_equal(
        pred[: 10000 - 91 * 48 + 1], other_pred[: 10000 - 91 * 48 + 1]
    )


def test_hac_matches_independent_bartlett_matrix():
    x = np.array([0, 1, -1, 2, 0, -2, 1, 1], dtype=float)
    centered = x - x.mean()
    lags = 2
    weights = np.maximum(
        0, 1 - np.abs(np.arange(8)[:, None] - np.arange(8)) / (lags + 1)
    )
    expected = np.sqrt(centered @ weights @ centered / len(x) ** 2)
    assert study.hac(x, lags)["se"] == pytest.approx(expected)


def test_shifted_majority_cannot_create_predictive_pass():
    bars = fixture_bars((-1, -1, -1, -1, 1))
    bars.values[: 91 * 48, 4] = 101
    prediction = study.measure(bars)["prediction"]
    assert prediction["candidate_accuracy"] > prediction["training_majority_accuracy"]
    assert prediction["candidate_accuracy"] < prediction["always_down_accuracy"]
    assert prediction["decision"] != "PREDICTIVE_PASS"


def test_flat_economic_baseline_keeps_all_predictive_targets():
    bars = fixture_bars()
    bars.values[: 91 * 48, 4] = 99
    result = study.measure(bars)
    assert result["prediction"]["target_count"] == 17520
    assert result["prediction"]["decision"] == "PREDICTIVE_PASS"
    assert result["costs"]["training_majority"]["trades"] == 0


def test_changed_staged_data_fails_with_persistent_journal(tmp_path, monkeypatch):
    config, _ = load(Path("configs/research.yaml"))
    original = study.supervise

    def tamper_after_acquisition(output, request, *args, **kwargs):
        outcome = original(output, request, *args, **kwargs)
        if request["stage"] == "acquire":
            with (output / "bars.npy").open("ab") as staged:
                staged.write(b"changed")
        return outcome

    monkeypatch.setattr(study, "supervise", tamper_after_acquisition)
    output = tmp_path / "failed-worker"
    report = study.campaign(output, config["resource_governor"], synthetic=True)
    assert report["execution_status"] == "FAILED"
    assert report["workers"]["analysis"]["started_fits"] == 0
    with sqlite3.connect(output / "research.sqlite3") as db:
        assert (
            db.execute(
                "select execution_status from experiments where candidate_id = ?",
                (study.VARIANT,),
            ).fetchone()[0]
            == "FAILED"
        )


@pytest.mark.parametrize("failed_month", ["2024-09", "2024-10"])
def test_acquisition_failure_keeps_attempted_month_and_reason(
    tmp_path, monkeypatch, failed_month
):
    def acquisition(month, output):
        if month == failed_month:
            raise ValueError("Synthetic checksum failure")
        data, checksum = month_payload(month)
        return study.parse_month(month, data, checksum), {
            "month": month,
            "bytes": len(data),
        }

    monkeypatch.setattr(study, "acquire_month", acquisition)
    request = {
        "output": str(tmp_path),
        "stage": "acquire",
        "synthetic": False,
        "trial_seconds": 120,
    }
    result = study.worker(request, tmp_path)
    assert result["status"] == "FAILED"
    receipt = json.loads((tmp_path / "acquisition.json").read_text())
    assert receipt["archives"][-1]["month"] == failed_month
    assert receipt["archives"][-1]["status"] == "FAILED"
    assert "Synthetic checksum failure" in receipt["archives"][-1]["error"]


def test_plan_respects_tighter_limits():
    config, _ = load(Path("configs/research.yaml"))
    limits = config["resource_governor"]
    assert study.preflight(limits)["status"] == "READY"
    for key, value in [
        ("max_model_fits_per_campaign", 0),
        ("max_research_trials_per_campaign", 1),
        ("max_wall_seconds_per_campaign", 200),
    ]:
        bad = deepcopy(limits)
        bad[key] = value
        with pytest.raises(ValueError):
            study.preflight(bad)


def test_supervised_synthetic_completion_failure_and_duplicate(tmp_path):
    config, _ = load(Path("configs/research.yaml"))
    output = tmp_path / "run"
    report = study.campaign(output, config["resource_governor"], synthetic=True)
    assert report["execution_status"] == "COMPLETED"
    assert report["workers"]["analysis"]["started_fits"] == 1
    assert report["workers"]["analysis"]["completed_fits"] == 1
    assert report["results"]["prediction"]["decision"] == "PREDICTIVE_PASS"
    with sqlite3.connect(output / "research.sqlite3") as db:
        assert db.execute("select count(*) from experiments").fetchone()[0] == 2
        assert db.execute(
            "select distinct execution_status from experiments"
        ).fetchall() == [("COMPLETED",)]
    with pytest.raises(FileExistsError):
        study.campaign(output, config["resource_governor"], synthetic=True)
    bad = deepcopy(config["resource_governor"])
    bad["max_model_fits_per_campaign"] = 0
    failed = tmp_path / "failed"
    rejected = study.campaign(failed, bad, synthetic=True)
    assert rejected["execution_status"] == "REJECTED_PREFLIGHT"
    assert rejected["workers"] == {}
    assert json.loads((failed / "report.json").read_text())["journal_integrity"] == "ok"
