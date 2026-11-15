"""FR-005 tests observe real admission before any study worker or data read."""

import json
import sqlite3
import threading
import time
from contextlib import closing
from pathlib import Path

import pytest
import yaml

from aqrs import research

ROOT = Path(__file__).resolve().parents[1]
QUESTION = "Can the configured synthetic workflow execute and report its declared measurements within its guards?"


@pytest.fixture
def study_config(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path / "home"))
    monkeypatch.setattr("aqrs.journal.legacy_checkout_artifacts", lambda: [])
    config = yaml.safe_load(
        (ROOT / "configs/research.yaml").read_text(encoding="utf-8")
    )
    config["project"].update(artifact_dir="results", path_base=".")
    config["journal"]["sqlite_path"] = "results/journal.sqlite3"
    config["market"]["n_bars"] = 240
    config["research"].update(train_bars=60, validation_bars=30, walk_forward_folds=2)
    config["study"] = {
        "question": QUESTION,
        "design": "common_synthetic_workflow_v1",
        "claim": "engineering",
        "prerequisites": [],
    }
    return config


def test_unclear_question_stops_before_worker(study_config, tmp_path, monkeypatch):
    study_config["study"]["question"] = ""
    starts = []

    def forbidden_worker(*args, **kwargs):
        starts.append(1)
        raise AssertionError("An unclear question must not reach a worker.")

    monkeypatch.setattr(research, "supervise", forbidden_worker)
    result, code = research.run(study_config, tmp_path, plan_only=False)
    assert code == 2
    assert result["reason_code"] == "QUESTION_UNCLEAR"
    assert result["required_action"] and result["resumption_condition"]
    assert starts == []


@pytest.mark.parametrize(
    "change, reason",
    [
        ({"question": "Does it work?"}, "QUESTION_UNREVIEWED"),
        (
            {"question": "Will the strategy profit and never lose?"},
            "QUESTION_UNREVIEWED",
        ),
        ({"design": "use_any_available_20_rows"}, "DESIGN_UNQUALIFIED"),
        ({"claim": "market_alpha"}, "DESIGN_UNQUALIFIED"),
        ({"PASS": True}, "DESIGN_UNQUALIFIED"),
        ({"prerequisites": ["missing-method-evidence.json"]}, "PREREQUISITE_MISSING"),
    ],
)
def test_bad_plan_is_recorded_before_data_or_workers(
    study_config, tmp_path, monkeypatch, change, reason
):
    study_config["study"].update(change)
    study_config["market"].update(
        source="synthetic_csv",
        csv_path="not-opened.csv",
        start_at="2024-02-01T00:00:00Z",
    )
    calls = []

    def forbidden(*args, **kwargs):
        calls.append(1)
        raise AssertionError("Blocked study work was reached.")

    monkeypatch.setattr(research, "supervise", forbidden)
    monkeypatch.setattr(research, "read_synthetic_csv", forbidden)
    result, code = research.run(study_config, tmp_path, plan_only=False)
    assert code == 2 and result["reason_code"] == reason
    assert calls == []
    assert (
        result["study_data_accesses"]
        == result["started_workers"]
        == result["started_fits"]
        == 0
    )
    with sqlite3.connect(tmp_path / "results/journal.sqlite3") as db:
        status, manifest = db.execute(
            "SELECT execution_status, manifest_json FROM campaigns"
        ).fetchone()
    assert status == "REJECTED_PREFLIGHT"
    recorded = json.loads(manifest)
    assert recorded["required_action"] and recorded["resumption_condition"]
    assert recorded["reason_code"] == reason


def test_valid_engineering_case_really_starts(study_config, tmp_path):
    result, code = research.run(study_config, tmp_path, plan_only=False)
    assert code == 0, result
    report = json.loads((Path(result["output_dir"]) / "report.json").read_text())
    assert report["study_admission"]["decision"] == "ADMITTED_ENGINEERING_ONLY"
    assert report["study_admission"]["supports_market_claim"] is False
    assert report["plan"]["started_trials"] == 2
    assert report["plan"]["completed_fits"] > 0
    with sqlite3.connect(tmp_path / "results/journal.sqlite3") as db:
        launches = db.execute("SELECT consumed FROM study_launches").fetchall()
    assert len(launches) == 4 and all(row == (1,) for row in launches)


def test_plan_has_no_timing_worker(study_config, tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Declarative planning must not start a worker.")

    monkeypatch.setattr("aqrs.planning.supervise", forbidden)
    result, code = research.run(study_config, tmp_path, plan_only=True)
    assert code == 0 and result["execution_authorized"] is False
    assert result["started_fits"] == result["started_trials"] == 0


def test_direct_paths_and_unapproved_supervisor_stop(tmp_path, monkeypatch):
    from aqrs import governor, worker
    from aqrs.admission import AdmissionRejected

    def forbidden(*args, **kwargs):
        raise AssertionError("Popen must not be reached without admission.")

    monkeypatch.setattr(governor.subprocess, "Popen", forbidden)
    with pytest.raises(AdmissionRejected, match="No checked parent"):
        research.execute(None, None, tmp_path, {}, 0, base=tmp_path)
    with pytest.raises(AdmissionRejected, match="No checked worker"):
        research.prepare_data({})
    with pytest.raises(AdmissionRejected, match="No checked worker"):
        worker.evaluate({}, tmp_path)
    result = governor.supervise(tmp_path, {}, 1, 10**10, 512)
    assert result["reason_code"] == "ADMISSION_REQUIRED" and not result["started"]


@pytest.fixture
def admitted_context(study_config, tmp_path):
    from aqrs import journal
    from aqrs.storage import fingerprint
    from aqrs.study_admission import admitted_run, assess

    database = tmp_path / "journal.sqlite3"
    decision = assess(study_config, tmp_path)
    with closing(journal.connect(database)) as db:
        journal.begin(
            db,
            "admission-test",
            fingerprint(study_config),
            study_config,
            {"study_admission": decision},
        )
    with admitted_run(database, "admission-test", study_config, tmp_path, decision):
        yield database


def test_changed_and_replayed_worker_requests_are_rejected(admitted_context):
    from aqrs.admission import AdmissionRejected
    from aqrs.study_admission import admitted_worker, authorize_worker

    request = authorize_worker({"pilot_rows": 40, "pilot_columns": 1, "fit_limit": 1})
    with pytest.raises(AdmissionRejected, match="changed, unregistered"):
        with admitted_worker(request | {"fit_limit": 100}):
            pytest.fail("Changed request was admitted.")
    with admitted_worker(request):
        pass
    with pytest.raises(AdmissionRejected, match="already consumed"):
        with admitted_worker(request):
            pytest.fail("Consumed worker approval was reused.")
    with pytest.raises(AdmissionRejected, match="caller cannot supply"):
        authorize_worker(request)


def test_revoked_record_and_changed_config_stop_before_dispatch(
    admitted_context, study_config, tmp_path, monkeypatch
):
    from aqrs import governor

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid admission reached Popen.")

    monkeypatch.setattr(governor.subprocess, "Popen", forbidden)
    study_config["study"]["design"] = "unreviewed"
    result = governor.supervise(tmp_path, {}, 10, time.monotonic() + 20, 512)
    assert result["reason_code"] == "DESIGN_UNQUALIFIED" and not result["started"]
    study_config["study"]["design"] = "common_synthetic_workflow_v1"
    with sqlite3.connect(admitted_context) as db:
        db.execute("UPDATE campaigns SET execution_status = 'CANCELLED'")
    result = governor.supervise(tmp_path, {}, 10, time.monotonic() + 20, 512)
    assert result["reason_code"] == "ADMISSION_REVOKED" and not result["started"]


def test_missing_input_is_rejected_before_popen(study_config, tmp_path, monkeypatch):
    from aqrs import governor

    study_config["market"].update(
        source="synthetic_csv", csv_path="missing.csv", start_at="2024-02-01T00:00:00Z"
    )

    def forbidden(*args, **kwargs):
        pytest.fail("Unavailable input reached Popen.")

    monkeypatch.setattr(governor, "_supervise_process", forbidden)
    result, code = research.run(study_config, tmp_path, plan_only=False)
    assert code == 2 and result["reason_code"] == "PREREQUISITE_MISSING"
    report = json.loads((Path(result["output_dir"]) / "report.json").read_text())
    assert not report["preparation"]["started"]
    assert report["plan"]["started_trials"] == report["plan"]["completed_fits"] == 0


def test_storage_failure_prevents_launch(study_config, tmp_path, monkeypatch):
    def unavailable(*args, **kwargs):
        raise sqlite3.OperationalError("Journal unavailable")

    def forbidden(*args, **kwargs):
        pytest.fail("Unrecorded admission reached a worker.")

    monkeypatch.setattr(research.journal, "connect", unavailable)
    monkeypatch.setattr(research, "supervise", forbidden)
    with pytest.raises(sqlite3.OperationalError, match="Journal unavailable"):
        research.run(study_config, tmp_path, plan_only=False)


def test_lost_prerequisite_stops_a_running_process(tmp_path):
    from test_governor import probe

    from aqrs.admission import AdmissionRejected
    from aqrs.governor import _supervise_process

    started = tmp_path / "started"
    prerequisite = tmp_path / "prerequisite"
    prerequisite.touch()

    def check():
        if not prerequisite.exists():
            raise AdmissionRejected(
                "PREREQUISITE_MISSING", "Required capability was revoked."
            )

    def revoke():
        end = time.monotonic() + 5
        while not started.exists() and time.monotonic() < end:
            time.sleep(0.01)
        prerequisite.unlink(missing_ok=True)

    thread = threading.Thread(target=revoke)
    thread.start()
    begin = time.monotonic()
    result = _supervise_process(
        tmp_path,
        {},
        10,
        begin + 12,
        512,
        command=probe(f"Path({str(started)!r}).touch(); import time; time.sleep(10)"),
        admission_watch=check,
    )
    thread.join(timeout=6)
    assert (
        result["execution_status"] == "CANCELLED"
        and result["reason_code"] == "PREREQUISITE_MISSING"
    )
    assert result["started"] and time.monotonic() - begin < 5
    assert result["completed_fits"] == 0


def test_slow_admission_io_cannot_delay_the_wall_watchdog(tmp_path):
    from test_governor import probe

    from aqrs.governor import _supervise_process

    release = threading.Event()
    begin = time.monotonic()
    try:
        result = _supervise_process(
            tmp_path,
            {},
            0.7,
            begin + 10,
            512,
            command=probe("import time; time.sleep(10)"),
            admission_watch=lambda: release.wait(10),
        )
    finally:
        release.set()
    assert result["execution_status"] == "TIMED_OUT"
    assert time.monotonic() - begin < 3
