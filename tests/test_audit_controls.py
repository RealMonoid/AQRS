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


@pytest.mark.parametrize("campaign,count", [("M2-E14", 29), ("M2-E18", 60)])
def test_campaign_archive_verification_reuses_preserved_receipts(campaign, count):
    from scripts.evidence_archive import verify_campaign

    assert verify_campaign(ROOT, campaign, None) == count


def test_campaign_archive_rejects_the_superseded_replay(tmp_path):
    import shutil
    import subprocess
    from zipfile import ZipFile

    from scripts.evidence_archive import verify_campaign

    evidence = tmp_path / "evidence"
    replay = evidence / "m2-e18-replay/windows.json"
    replay.parent.mkdir(parents=True)
    for suffix in ("acceptance.zip", "verification.json"):
        shutil.copyfile(
            ROOT / f"evidence/m2-e18-{suffix}", evidence / f"m2-e18-{suffix}"
        )
    with ZipFile(evidence / "m2-e18-acceptance.zip") as archive:
        original = archive.read("artifacts/m2-e18/windows/report.json")

    def git(*args):
        return subprocess.run(
            ["git", *args], cwd=tmp_path, check=True, capture_output=True
        )

    git("init")
    (tmp_path / ".gitattributes").write_text("*.json -text\n", encoding="utf-8")
    for data in (original + b"\n", original):
        replay.write_bytes(data)
        git("add", "evidence/m2-e18-replay/windows.json")
        git(
            "-c",
            "user.name=AQRS test",
            "-c",
            "user.email=test@example.invalid",
            "-c",
            "commit.gpgsign=false",
            "commit",
            "-m",
            "Replay byte fixture",
        )
    assert verify_campaign(tmp_path, "M2-E18", "HEAD") == 60
    with pytest.raises(ValueError, match="replay report digest mismatch"):
        verify_campaign(tmp_path, "M2-E18", "HEAD^")


@pytest.mark.parametrize(
    "other",
    [
        ["--build"],
        ["--restore", "unused"],
        ["--verify-exposure"],
        ["--consolidate-exposure"],
        ["--verify-supervised-replay", "unused"],
        ["--source-revision", "HEAD"],
    ],
)
def test_campaign_verification_rejects_competing_modes_before_io(monkeypatch, other):
    import sys

    from scripts import evidence_archive

    def forbidden(*args):
        pytest.fail("Conflicting verification modes reached evidence I/O.")

    monkeypatch.setattr(evidence_archive, "verify_campaign", forbidden)
    monkeypatch.setattr(
        sys, "argv", ["evidence_archive", "--campaign", "M2-E18", *other]
    )
    with pytest.raises(SystemExit) as stopped:
        evidence_archive.main()
    assert stopped.value.code == 2


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


@pytest.mark.parametrize("layout", ["flat", "nested", "both", "absent", "empty"])
def test_exposure_index_keeps_diagnostic_views_on_duplicate_model_attempts(
    tmp_path, layout
):
    from scripts.evidence_archive import build

    config = {"research": {"candidates": [{"id": "synthetic"}]}}
    manual_screen = {
        "analysis_id": "SYNTHETIC-PRECISION-P01",
        "kind": "report_based_precision_planning",
        "source_bundle_revision": "recorded-evidence-revision",
    }
    look = {
        "diagnostic_id": "AQRS-DIAG-RANK-V1",
        "metric": "rank_correlation",
        "view": "aggregate",
        "validation_intervals": [[12, 20]],
        "horizon_bars": 3,
    }
    metrics = {
        "flat": {"diagnostic_exposure": [look]},
        "nested": {"result": {"diagnostic_exposure": [look]}},
        "both": {
            "diagnostic_exposure": [look],
            "result": {"diagnostic_exposure": [look]},
        },
        "absent": {},
        "empty": {"result": {"diagnostic_exposure": []}},
    }[layout]
    with closing(journal.connect(tmp_path / "artifacts/journal.sqlite3")) as db:
        for run_id in ("first", "repeat"):
            journal.begin(db, run_id, "config", config, {})
            journal.finish_experiment(
                db,
                run_id,
                {
                    "experiment_id": f"{run_id}:synthetic",
                    "candidate_id": "synthetic",
                    "execution_status": "COMPLETED",
                    "evidence_status": "INSUFFICIENT_EVIDENCE",
                    "metrics": metrics,
                },
                {"evidence_key": "same-model-and-data"},
            )
        build(tmp_path)
        index_path = tmp_path / "evidence/exposure.json"
        index = json.loads(index_path.read_text(encoding="utf-8"))
        assert [screen["work_item"] for screen in index["manual_screens"]] == [
            "M2-E02",
            "M2-E03",
            "M2-E12",
        ]
        index["manual_screens"].append(manual_screen)
        index_path.write_text(json.dumps(index), encoding="utf-8")
        build(tmp_path)
    rebuilt = json.loads(index_path.read_text(encoding="utf-8"))
    assert rebuilt["manual_screens"] == index["manual_screens"]
    index = rebuilt
    assert len(index["variants"]) == 1
    assert len(index["attempts"]) == 2
    assert index["attempts"][1]["duplicate_of_in_original_journal"] == "first:synthetic"
    expected = None if layout == "absent" else [] if layout == "empty" else [look]
    assert [attempt.get("diagnostic_exposure") for attempt in index["attempts"]] == [
        expected,
        expected,
    ]
    if layout == "absent":
        assert all("diagnostic_exposure" not in a for a in index["attempts"])


@pytest.mark.parametrize(
    "metrics",
    [
        {
            "diagnostic_exposure": [],
            "result": {"diagnostic_exposure": [{"view": "fold"}]},
        },
        {"diagnostic_exposure": None},
        {"result": {"diagnostic_exposure": {"view": "fold"}}},
        {"result": {"diagnostic_exposure": ["not-a-view-record"]}},
    ],
)
def test_exposure_rejects_conflicting_or_unknown_diagnostic_formats(metrics):
    from scripts.evidence_archive import diagnostic_views

    with pytest.raises(ValueError, match="diagnostic exposure"):
        diagnostic_views(metrics)


@pytest.fixture
def exposure_archive(tmp_path):
    from scripts.evidence_archive import build, digest, write

    config = {"research": {"candidates": [{"id": "synthetic"}]}}
    with closing(journal.connect(tmp_path / "artifacts/journal.sqlite3")) as db:
        for run in ("original", "replay"):
            journal.begin(db, run, "fixed", config, {})
            journal.finish_experiment(
                db,
                run,
                {
                    "experiment_id": f"{run}:synthetic",
                    "candidate_id": "synthetic",
                    "execution_status": "COMPLETED",
                    "evidence_status": "INSUFFICIENT_EVIDENCE",
                    "metrics": {
                        "result": {
                            "diagnostic_exposure": [
                                {"diagnostic_id": "known", "view": "aggregate"}
                            ]
                        }
                    },
                },
                {"evidence_key": "same-data-and-model"},
            )
    build(tmp_path)
    path = tmp_path / "evidence/exposure.json"
    index = json.loads(path.read_text(encoding="utf-8"))
    index["archive_sources"] = [
        {
            "work_item": "EXAMPLE",
            "bundle": "evidence/acceptance.zip",
            "sha256": digest((tmp_path / "evidence/acceptance.zip").read_bytes()),
            "receipt": "evidence/manifest.json",
        }
    ]
    index["future_registrations"] = [
        {"work_item": "EXAMPLE", "variant_id": "synthetic", "status": "PLANNED_NOT_RUN"}
    ]
    index["manual_screens"].append(
        {
            "analysis_id": "legacy-unknown",
            "registration": "historical_timing_unverified",
        }
    )
    write(path, index)
    return tmp_path, path


def test_exposure_consolidation_is_idempotent_and_preserves_legacy(exposure_archive):
    from scripts.evidence_archive import build, consolidate_exposure, verify_exposure

    root, path = exposure_archive
    before = json.loads(path.read_text(encoding="utf-8"))
    summary = consolidate_exposure(root)
    first = path.read_bytes()
    assert consolidate_exposure(root) == verify_exposure(root) == summary
    assert path.read_bytes() == first
    result = json.loads(first)
    assert result["manual_screens"] == before["manual_screens"]
    assert result["unknown_exposure"] == before["unknown_exposure"]
    assert summary["attempts"] == summary["recorded_diagnostic_views"] == 2
    assert len(result["variants"]) == 1
    assert result["future_registrations"][0]["status"] == "COMPLETED"
    assert (
        result["future_registrations"][0]["status_before_reconciliation"]
        == "PLANNED_NOT_RUN"
    )
    assert all(a["independent_confirmation"] is False for a in result["attempts"])
    bundle = (root / "evidence/acceptance.zip").read_bytes()
    with pytest.raises(ValueError, match="Frozen archive"):
        build(root)
    assert path.read_bytes() == first
    assert (root / "evidence/acceptance.zip").read_bytes() == bundle


@pytest.mark.parametrize(
    "fault",
    [
        "missing",
        "duplicate",
        "views",
        "planned",
        "independence",
        "parent",
        "unknown",
        "definition",
        "registration_source",
        "registration_link",
    ],
)
def test_exposure_verifier_rejects_broken_flow(exposure_archive, fault):
    from scripts.evidence_archive import consolidate_exposure, verify_exposure

    root, path = exposure_archive
    consolidate_exposure(root)
    index = json.loads(path.read_text(encoding="utf-8"))
    if fault == "missing":
        index["attempts"].pop()
    elif fault == "duplicate":
        index["attempts"].append(index["attempts"][0])
    elif fault == "views":
        index["attempts"][0]["diagnostic_exposure"] = []
    elif fault == "planned":
        index["future_registrations"][0]["status"] = "PLANNED_NOT_RUN"
    elif fault == "independence":
        index["attempts"][0]["independent_confirmation"] = True
    elif fault == "parent":
        index["variants"][0]["lineage"] = {"parent_variant_ids": ["missing"]}
    elif fault == "definition":
        index["variants"][0]["definition"]["horizon"] = 999
    elif fault == "registration_source":
        index["future_registrations"][0]["work_item"] = "missing"
    elif fault == "registration_link":
        index["future_registrations"][0]["attempt_ids"] = ["missing:attempt"]
    else:
        index["unknown_exposure"] = ""
    with pytest.raises(ValueError):
        verify_exposure(root, index)


def test_exposure_consolidation_fails_before_write_on_corrupt_source(exposure_archive):
    from scripts.evidence_archive import consolidate_exposure

    root, path = exposure_archive
    before = path.read_bytes()
    bundle = root / "evidence/acceptance.zip"
    bundle.write_bytes(bundle.read_bytes() + b"corruption")
    with pytest.raises(ValueError, match="digest mismatch"):
        consolidate_exposure(root)
    assert path.read_bytes() == before


def test_exposure_duplicate_archive_attempt_is_not_silently_merged(exposure_archive):
    from scripts.evidence_archive import consolidate_exposure, write

    root, path = exposure_archive
    index = json.loads(path.read_text(encoding="utf-8"))
    duplicate = root / "evidence/duplicate.zip"
    duplicate.write_bytes((root / "evidence/acceptance.zip").read_bytes())
    index["archive_sources"].append(
        index["archive_sources"][0]
        | {
            "work_item": "DUPLICATE",
            "bundle": "evidence/duplicate.zip",
        }
    )
    write(path, index)
    before = path.read_bytes()
    with pytest.raises(ValueError, match="Duplicate experiment_id"):
        consolidate_exposure(root)
    assert path.read_bytes() == before


def test_exposure_archived_value_stream_and_p04_views():
    """Read archived receipts only: no research entry, estimator or data payload."""
    from scripts.evidence_archive import verify_exposure

    index = json.loads((ROOT / "evidence/exposure.json").read_text(encoding="utf-8"))
    summary = verify_exposure(ROOT, index)
    assert summary["attempts"] >= 95 and summary["variants"] >= 15
    known = {
        "AQRS-A06": (80, 0),
        "M2-E14": (2, 55),
        "M2-E18": (4, 230),
        "M2-E19": (4, 0),
        "M2-E20-P04": (4, 60),
        "M2-E15": (1, 0),
    }
    for source, (attempts, views) in known.items():
        rows = [a for a in index["attempts"] if a["archive_source"] == source]
        assert len(rows) == attempts
        assert sum(len(a.get("diagnostic_exposure", [])) for a in rows) == views
    variants = {v["variant_id"]: v for v in index["variants"]}
    receipt = json.loads(
        (ROOT / "evidence/m2-e20-p04-verification.json").read_text(encoding="utf-8")
    )
    rows = [a for a in index["attempts"] if a["archive_source"] == "M2-E20-P04"]
    assert {a["experiment_id"] for a in rows} == {
        a["experiment_id"] for a in receipt["attempts"]
    }
    assert len(rows) == 4 and all(len(a["diagnostic_exposure"]) == 15 for a in rows)
    assert all(a["independent_confirmation"] is False for a in rows)
    for row in rows:
        variant = variants[row["variant_id"]]
        assert variant["definition"]["registered_variant"] == "M2-E08/1"
        assert variant["lineage"]["work_items"] == ["M2-E08", "M2-E09", "M2-E20-P04"]
        assert len(variant["attempt_ids"]) >= 5
    for family in ("VOL_CONFIRM", "RIDGE_INCREMENT"):
        assert variants[f"{family}_E18_V1"]["lineage"]["parent_variant_ids"] == [
            f"{family}_V1"
        ]
        assert (
            "m2-e17" in variants[f"{family}_E18_V1"]["lineage"]["prerequisite_refs"][0]
        )
    assert (
        "VOL_CONFIRM_E18_V1"
        in variants["VOL_REGIME_HMM_E19_V1"]["lineage"]["parent_variant_ids"]
    )
    scopes = {
        a["dataset_id"]
        for a in index["attempts"]
        if a["archive_source"] in {"M2-E18", "M2-E19"}
    }
    assert len(scopes) == 1 and None not in scopes
    for entry in index["future_registrations"]:
        if entry["work_item"] in {"M2-E14", "M2-E18"}:
            assert entry["status"] == "COMPLETED" and entry["attempt_ids"]
    assert {s["work_item"] for s in index["manual_screens"]} >= {
        "M2-E02",
        "M2-E03",
        "M2-E12",
        "M2-E15",
        "M2-E19",
    }
    assert any(
        r["variant_id"] == "M2-E17-TRAIN-MOVE-P90-V1"
        for r in index["future_registrations"]
    )


@pytest.mark.parametrize(
    "variant_id", ["historical-fc181f3f5e358ac1", "VOL_REGIME_HMM_E19_V1"]
)
def test_exposure_rejects_changed_archived_variant_definition(variant_id):
    from scripts.evidence_archive import verify_exposure

    index = json.loads((ROOT / "evidence/exposure.json").read_text(encoding="utf-8"))
    next(v for v in index["variants"] if v["variant_id"] == variant_id)["definition"][
        "horizon"
    ] = 999
    with pytest.raises(ValueError, match="definition"):
        verify_exposure(ROOT, index)


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


@pytest.mark.parametrize(
    "change, message",
    [
        ("none", "Verified source-bound supervised replay"),
        ("windows_only", "Verified source-bound supervised Windows receipt"),
        ("source", "source digest mismatch"),
        ("snapshot", "Archived source digest mismatch"),
        ("journal", "Journal and supervised receipt disagree"),
        ("incomplete", "Incomplete supervised receipt"),
        ("configuration", "Incomplete supervised receipt"),
        ("dataset", "dataset snapshot does not match its recorded identity"),
        ("dataset_bytes", "Replay dataset bytes differ"),
        ("decision", "Replay mismatch at ridge.trading.candidate.trade_count"),
        ("metric", "Replay mismatch at ridge.prediction.mae"),
    ],
)
def test_supervised_replay_verification(tmp_path, change, message):
    import subprocess
    import sys
    from hashlib import sha256

    from aqrs.storage import fingerprint, write_json

    def git(*args):
        return subprocess.check_output(["git", *args], cwd=ROOT)

    revision = git("rev-parse", "HEAD").decode().strip()
    source = {
        "source/pilot.py": "scripts/m2_supervised_pilot.py",
        "source/research.yaml": "configs/research.yaml",
        "source/m1-e04.yaml": "configs/m1-e04.yaml",
    }
    source.update(
        (f"source/aqrs/{path.name}", path.relative_to(ROOT).as_posix())
        for path in (ROOT / "src/aqrs").glob("*.py")
    )
    configuration = {
        "variant": "M2-E08/1",
        "days": [day.isoformat() for day in supervised.DAYS],
        "archive_digests": list(supervised.DIGESTS),
        "features": supervised.FEATURES,
        "horizon": 30,
        "lightgbm_parameters": supervised.PARAMETERS,
        "lightgbm_version": "4.6.0",
        "costs": supervised.COSTS,
        "research": {"candidates": [{"id": name} for name in supervised.MODELS]},
        "seed": 42,
    }
    if change == "configuration":
        configuration["seed"] = 43
    bars = generate(42, 5760, 1, "BTCUSDT")
    bars.values[:, 0] += (
        datetime(2026, 1, 1, tzinfo=UTC).timestamp() - bars.values[0, 0]
    )
    dataset_id = bars.fingerprint
    systems = ("Windows",) if change == "windows_only" else ("Windows", "Linux")
    for system in systems:
        output = tmp_path / system
        hashes = {}
        for target, path in source.items():
            data = git("show", f"{revision}:{path}")
            if change == "source" and path == "configs/research.yaml":
                data += b"\n"
            (output / target).parent.mkdir(parents=True, exist_ok=True)
            (output / target).write_bytes(data)
            hashes[target] = sha256(data).hexdigest()
        dataset = bars.values.copy()
        if change == "dataset" and system == "Linux":
            dataset[0, 5] *= 2
        if change == "dataset_bytes" and system == "Linux":
            dataset = np.asfortranarray(dataset)
        np.save(output / "development.npy", dataset, allow_pickle=False)
        report = {
            "schema_version": "2",
            "run_id": system,
            "platform": f"{system}-test",
            "execution_status": "COMPLETED",
            "evaluation_status": "COMPLETED",
            "configuration": configuration,
            "config_id": fingerprint(configuration),
            "dataset_id": dataset_id,
            "provenance": {"files": hashes, "source_id": fingerprint(hashes)},
            "holdout": {
                "start_at": "2026-01-06T00:00:00Z",
                "authorized_reads": 0,
                "evaluated": False,
            },
            "journal_integrity": "ok",
            "folds": [
                {"validation_rows": 1409, "validation_day": f"2026-01-0{day}"}
                for day in (3, 4)
            ],
            "plan": {"preflight_status": "ADMITTED", "planned_fits": 6},
            "preflight": {
                name: completed({}, 1) | {"started_fits": 1}
                for name in supervised.MODELS
            },
            "trials": {},
            "per_day": {name: [{"mae": 0.125}] * 2 for name in supervised.MODELS},
            "paired_deltas": [{"mae_improvement": 0.0}] * 2,
            "decision": "DEFER",
        }
        if system == "Linux" and change == "incomplete":
            report["evaluation_status"] = "SCREENED_OUT"
        with closing(journal.connect(output / "research.sqlite3")) as db:
            journal.begin(db, system, report["config_id"], configuration, report)
            for name in supervised.MODELS:
                altered = system == "Linux" and name == "ridge"
                mae = 0.125
                if altered:
                    mae += 2e-8 if change == "metric" else 1e-9
                count = int(altered and change == "decision")
                result = {
                    "trading": {"candidate": {"trade_count": count}},
                    "prediction": {"mae": mae},
                    "stage_wall_seconds": {"simulation": float(len(system))},
                }
                outcome = completed(result, 2) | {"started_fits": 2}
                report["trials"][name] = outcome
                metadata = {
                    "source_id": report["provenance"]["source_id"],
                    "evidence_key": fingerprint([configuration, dataset_id, name]),
                }
                journal.start_experiment(db, system, name, metadata)
                journal.finish_experiment(
                    db,
                    system,
                    {
                        "experiment_id": f"{system}:{name}",
                        "candidate_id": name,
                        "execution_status": "COMPLETED",
                        "evidence_status": "INSUFFICIENT_EVIDENCE",
                        "metrics": outcome,
                    },
                    metadata,
                )
            journal.finish_campaign(db, system, "COMPLETED", report)
            if system == "Linux" and change == "journal":
                with db:
                    db.execute("UPDATE experiments SET evidence_key = 'wrong'")
        write_json(output / "report.json", report)
        if change == "snapshot" and system == "Linux":
            (output / "source/pilot.py").write_bytes(b"Changed snapshot")

    result = subprocess.run(
        [
            sys.executable,
            "-B",
            "scripts/evidence_archive.py",
            "--verify-supervised-replay",
            *(str(tmp_path / system) for system in systems),
            "--source-revision",
            revision,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == (0 if change in {"none", "windows_only"} else 2), (
        result.stderr
    )
    assert message in result.stdout + result.stderr


def test_language_checker_includes_suffixless_documentation(tmp_path):
    from scripts.check_language_policy import collect_files

    docs = tmp_path / "docs"
    docs.mkdir()
    document = docs / "imported_handoff"
    document.write_text("Imported source needs review.", encoding="utf-8")
    assert document in list(collect_files(tmp_path))
