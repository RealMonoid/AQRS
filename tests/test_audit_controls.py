"""Regression checks for audit admission, status and persistence boundaries."""

import json
import sqlite3
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path
from time import monotonic

import numpy as np
import pytest
import yaml

from aqrs import journal, planning, research
from aqrs.config import load
from aqrs.market import generate
from scripts import m2_isolation_forest_pilot as isolation
from scripts import m2_supervised_pilot as supervised

ROOT = Path(__file__).resolve().parents[1]
EXECUTION_STATUSES = {
    "PROPOSED",
    "RUNNING",
    "COMPLETED",
    "FAILED",
    "CANCELLED",
    "REJECTED_PREFLIGHT",
    "BUDGET_EXHAUSTED",
    "TIMED_OUT",
    "MEMORY_LIMIT",
}
EVIDENCE_STATUSES = {
    "NOT_EVALUATED",
    "REJECTED",
    "INSUFFICIENT_EVIDENCE",
    "RESEARCH_PROMISING",
    "FINAL_TEST_PASSED",
}


def archived_limits(output, **changes):
    config, _ = load(ROOT / "configs/research.yaml")
    config["resource_governor"].update(changes)
    source = output / "source"
    source.mkdir(exist_ok=True)
    (source / "research.yaml").write_text(yaml.safe_dump(config), encoding="utf-8")
    return config


def completed(result, fits):
    return {
        "execution_status": "COMPLETED",
        "completed_fits": fits,
        "runtime_wall_seconds": 0.1,
        "started": True,
        "peak_rss_mb": 32,
        "sampled_cpu_seconds": 0.01,
        "stop_reason": None,
        "result": result,
    }


@pytest.mark.parametrize(
    "elapsed, expected", [(0, "ADMITTED"), (301, "REJECTED_PREFLIGHT")]
)
def test_preflight_accounts_for_elapsed_setup_without_timing_fit(
    tmp_path, monkeypatch, elapsed, expected
):
    config, _ = load(ROOT / "configs/research.yaml")
    config["resource_governor"]["preflight"]["measure_representative_pilot"] = False

    def forbidden(*args, **kwargs):
        pytest.fail("A disabled timing pilot must never start a worker.")

    monkeypatch.setattr(planning, "supervise", forbidden)
    plan, _ = planning.preflight(config, tmp_path, monotonic() - elapsed)
    assert plan["preflight_status"] == expected
    assert plan["completed_fits"] == plan["started_trials"] == 0
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize(
    "limits",
    [
        {"max_model_fits_per_campaign": 5},
        {"memory_mode": "strict"},
    ],
)
def test_supervised_actual_entry_rejects_limits_before_archive_or_fit(
    tmp_path, monkeypatch, limits
):
    archived_limits(tmp_path, **limits)

    def forbidden(*args, **kwargs):
        pytest.fail("Admission must reject before archive access or a worker launch.")

    monkeypatch.setattr(supervised, "read_window", forbidden)
    monkeypatch.setattr(supervised, "supervise", forbidden)
    report = {"preflight": {}, "trials": {}, "per_day": {}}
    with pytest.raises(ValueError):
        supervised.compare(
            tmp_path, report, None, "negative", {"costs": supervised.COSTS}
        )


def test_supervised_actual_entry_rejects_duplicate_governor_keys(tmp_path, monkeypatch):
    archived_limits(tmp_path)
    path = tmp_path / "source/research.yaml"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "  max_model_fits_per_campaign: 12",
        "  max_model_fits_per_campaign: 12\n  max_model_fits_per_campaign: 5",
    )
    path.write_text(text, encoding="utf-8")

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid configuration must fail before archive access or fitting.")

    monkeypatch.setattr(supervised, "read_window", forbidden)
    monkeypatch.setattr(supervised, "supervise", forbidden)
    with pytest.raises(ValueError, match="Duplicate"):
        supervised.compare(tmp_path, {}, None, "duplicate", {"costs": supervised.COSTS})


def test_supervised_screen_is_evaluation_state_and_keeps_frozen_costs(
    tmp_path, monkeypatch
):
    effective = archived_limits(tmp_path)
    assert effective["costs"] != supervised.COSTS
    bars = generate(42, 5760, 1, "BTCUSDT")
    monkeypatch.setattr(supervised, "read_window", lambda _: bars)
    calls = []

    def worker(directory, request, *args, **kwargs):
        calls.append(request)
        if "pilot_rows" in request:
            return completed({"fit_wall_seconds": 0.01}, 1)
        assert request["costs"] == supervised.COSTS
        return completed({"feasibility": {"status": "SCREENED_OUT"}}, 0)

    monkeypatch.setattr(supervised, "supervise", worker)
    config = {
        "costs": supervised.COSTS,
        "research": {"candidates": [{"id": name} for name in supervised.MODELS]},
    }
    report = {
        "provenance": {"source_id": "synthetic-source"},
        "preflight": {},
        "trials": {},
        "per_day": {},
    }
    with closing(journal.connect(tmp_path / "journal.sqlite3")) as db:
        journal.begin(db, "screen", "synthetic-config", config, report)
        status = supervised.compare(tmp_path, report, db, "screen", config)
        assert status == "COMPLETED"
        assert report["evaluation_status"] == "SCREENED_OUT"
        statuses = {
            row[0] for row in db.execute("SELECT execution_status FROM experiments")
        }
        assert statuses <= EXECUTION_STATUSES
    assert len(calls) >= 3
    assert all(
        row["execution_status"] == "COMPLETED" for row in report["trials"].values()
    )


def isolation_fixture(positive):
    bars = generate(42, isolation.ROWS, 1, "BTCUSDT")
    bars.values[:, 0] += (
        datetime(2026, 1, 1, tzinfo=UTC).timestamp() - bars.values[0, 0]
    )
    bars.values[:, 1:5] = 100
    if positive:
        bars.values[:2880, 1] = 100 * np.exp(0.02 * np.sin(np.arange(2880) / 40))
        for start in (2880, 4320):
            for hour in range(4):
                bars.values[start + hour * 60 + 32, 1] = 102
        bars.values[:, 4] = bars.values[:, 1]
        bars.values[:, 2] = bars.values[:, 1] * 1.001
        bars.values[:, 3] = bars.values[:, 1] * 0.999
    return bars


@pytest.mark.parametrize("positive", [False, True])
def test_isolation_screen_and_positive_branch_keep_contract_statuses(
    tmp_path, monkeypatch, positive
):
    archived_limits(tmp_path)
    bars = isolation_fixture(positive)
    folds = isolation.fixed_folds(bars)
    monkeypatch.setattr(isolation.prior, "read_window", lambda _: bars)

    def worker(directory, request, *args, **kwargs):
        if request["phase"] == "timing":
            return completed({}, 1)
        offset = int(request["phase"] == isolation.CHALLENGER)
        results = [
            {
                "alerts": [val.start + hour * 60 + offset for hour in range(4)],
                "volatility_cutoff": 0.01,
            }
            for _, val in folds
        ]
        return completed(results, 2)

    monkeypatch.setattr(isolation, "supervise", worker)
    report = {
        "run_id": "isolation",
        "config_id": "synthetic-config",
        "provenance": {"source_id": "synthetic-source"},
        "replay_of": None,
        "trials": {},
        "evidence_status": "NOT_EVALUATED",
    }
    with closing(journal.connect(tmp_path / "journal.sqlite3")) as db:
        journal.begin(
            db, report["run_id"], report["config_id"], isolation.CONFIG, report
        )
        status = isolation.compare(tmp_path, report, db, monotonic() + 300)
        assert status == "COMPLETED"
        assert report["evidence_status"] in EVIDENCE_STATUSES
        if positive:
            assert report["research_decision"] == "PROPOSE_FOLLOW_UP"
            assert report["evidence_status"] == "INSUFFICIENT_EVIDENCE"
        else:
            assert report["evaluation_status"] == "SCREENED_OUT"
            assert report["trials"] == {}


def test_unexpected_parent_exception_leaves_terminal_journal(tmp_path, monkeypatch):
    config, _ = load(ROOT / "configs/research.yaml")
    config["project"]["artifact_dir"] = "output"
    config["journal"]["sqlite_path"] = "journal.sqlite3"

    def broken(*args, **kwargs):
        raise KeyError("Planted orchestration failure")

    monkeypatch.setattr(research, "execute", broken)
    with pytest.raises(KeyError, match="Planted orchestration failure"):
        research.run(config, tmp_path, plan_only=False)
    with sqlite3.connect(tmp_path / "journal.sqlite3") as db:
        statuses = [
            row[0] for row in db.execute("SELECT execution_status FROM campaigns")
        ]
        assert statuses == ["FAILED"]
        trials = list(
            db.execute(
                "SELECT execution_status, evidence_status, metrics_json FROM experiments"
            )
        )
        assert trials and all(
            row == ("FAILED", "NOT_EVALUATED", None) for row in trials
        )
        manifest = json.loads(
            db.execute("SELECT manifest_json FROM campaigns").fetchone()[0]
        )
        assert manifest["execution_status"] == "FAILED"


def test_fit_ceiling_rejects_before_estimator_call(tmp_path):
    from aqrs.evaluation import evaluate

    class ForbiddenEstimator:
        def fit(self, *args):
            pytest.fail("A zero remaining fit allowance must reject before fit.")

    with pytest.raises(RuntimeError, match="Fit budget"):
        evaluate(
            {"pilot_rows": 10, "pilot_columns": 1, "fit_limit": 0},
            tmp_path,
            model_factory=ForbiddenEstimator,
        )


def test_preparation_timeout_is_terminal_without_candidate_start(tmp_path, monkeypatch):
    from test_governor import probe

    from aqrs.governor import supervise

    config, _ = load(ROOT / "configs/research.yaml")
    config["project"]["artifact_dir"] = "output"
    config["journal"]["sqlite_path"] = "journal.sqlite3"
    config["resource_governor"]["preflight"]["measure_representative_pilot"] = False
    calls = []

    def blocked(directory, request, seconds, deadline, rss):
        calls.append(request)
        assert request["stage"] == "prepare"
        return supervise(
            directory,
            request,
            10,
            monotonic() + 1.5,
            rss,
            command=probe("import time; time.sleep(60)"),
        )

    monkeypatch.setattr(research, "supervise", blocked)
    summary, code = research.run(config, tmp_path, plan_only=False)
    assert code == 1 and summary["execution_status"] == "BUDGET_EXHAUSTED"
    assert len(calls) == 1
    report = json.loads((Path(summary["output_dir"]) / "report.json").read_text())
    assert report["plan"]["completed_fits"] == report["plan"]["started_trials"] == 0
    assert all(t["evidence_status"] == "NOT_EVALUATED" for t in report["trials"])


def test_core_provenance_recovers_source_and_flags_free_costs(tmp_path, monkeypatch):
    from hashlib import sha256

    config, _ = load(ROOT / "configs/research.yaml")
    config["project"]["artifact_dir"] = "output"
    config["journal"]["sqlite_path"] = "journal.sqlite3"
    config["resource_governor"]["max_model_fits_per_campaign"] = 1
    config["costs"] = dict.fromkeys(config["costs"], 0)
    summary, code = research.run(config, tmp_path, plan_only=False)
    assert code == 2
    output = Path(summary["output_dir"])
    report = json.loads((output / "report.json").read_text())
    assert report["schema_version"] == "2"
    assert "commit" in report["provenance"]["git"]
    for relative, digest in report["provenance"]["files"].items():
        assert sha256((output / relative).read_bytes()).hexdigest() == digest
    assert set(report["zero_cost_components"]) == set(config["costs"])
    assert "Zero-cost" in (output / "report.md").read_text()


def test_evidence_bundle_checks_integrity_and_restores(tmp_path):
    from hashlib import sha256
    from zipfile import ZipFile

    from scripts.evidence_archive import verify

    bundle = tmp_path / "evidence.zip"
    payload = b"historical evidence"
    with ZipFile(bundle, "w") as z:
        z.writestr("artifacts/receipt.txt", payload)
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "bundle_sha256": sha256(bundle.read_bytes()).hexdigest(),
                "files": {
                    "artifacts/receipt.txt": {"sha256": sha256(payload).hexdigest()}
                },
            }
        )
    )
    assert verify(bundle, manifest, tmp_path / "restored") == 1
    assert (tmp_path / "restored/artifacts/receipt.txt").read_bytes() == payload
    bundle.write_bytes(bundle.read_bytes() + b"corruption")
    with pytest.raises(ValueError, match="digest mismatch"):
        verify(bundle, manifest)


def test_evidence_bundle_preserves_committed_wal_and_index_identity(tmp_path):
    from hashlib import sha256

    from scripts.evidence_archive import build, verify

    artifacts = tmp_path / "artifacts"
    artifacts.mkdir()
    source = artifacts / "journal.sqlite3"
    config = {"research": {"candidates": [{"id": "synthetic"}]}}
    with closing(journal.connect(source)) as db:
        db.execute("PRAGMA journal_mode=WAL")
        journal.begin(db, "wal-run", "synthetic-config", config, {})
        before = sha256(source.read_bytes()).hexdigest()
        assert source.with_name(source.name + "-wal").exists()
        assert build(tmp_path) == 1
        evidence = tmp_path / "evidence"
        restore = tmp_path / "restored"
        verify(evidence / "acceptance.zip", evidence / "manifest.json", restore)
        assert sha256(source.read_bytes()).hexdigest() == before
        assert db.execute("SELECT run_id FROM campaigns").fetchall() == [("wal-run",)]
        indexed = json.loads((evidence / "exposure.json").read_text(encoding="utf-8"))
        with closing(
            sqlite3.connect(restore / "artifacts/journal.sqlite3")
        ) as restored:
            assert restored.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
            assert restored.execute("SELECT run_id FROM campaigns").fetchall() == [
                ("wal-run",)
            ]
            assert {
                row[0]
                for row in restored.execute("SELECT experiment_id FROM experiments")
            } == {row["experiment_id"] for row in indexed["attempts"]}


def test_real_lightgbm_comparison_uses_archived_workers(tmp_path, monkeypatch):
    from importlib.metadata import version

    assert version("lightgbm") == "4.6.0"
    bars = generate(42, 5760, 1, "BTCUSDT")
    monkeypatch.setattr(supervised, "read_window", lambda _: bars)
    output = tmp_path / "synthetic supervised integration"
    assert supervised.main(output) == 0
    report = json.loads((output / "report.json").read_text())
    assert report["execution_status"] == report["evaluation_status"] == "COMPLETED"
    assert set(report["trials"]) == {"ridge", "lightgbm"}
    assert sum(t["completed_fits"] for t in report["preflight"].values()) == 2
    assert sum(t["completed_fits"] for t in report["trials"].values()) == 4
    assert report["configuration"]["costs"] == supervised.COSTS


def test_language_checker_includes_suffixless_documentation(tmp_path):
    from scripts.check_language_policy import collect_files

    docs = tmp_path / "docs"
    docs.mkdir()
    document = docs / "imported_handoff"
    document.write_text("Imported source needs review.", encoding="utf-8")
    assert document in list(collect_files(tmp_path))
