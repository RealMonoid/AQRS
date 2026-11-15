"""FR-005 tests observe real admission before any study worker or data read."""

import json
import sqlite3
import threading
import time
from contextlib import closing
from importlib import import_module
from pathlib import Path

import pytest
import yaml

from aqrs import research

ROOT = Path(__file__).resolve().parents[1]
QUESTION = "Can the configured synthetic workflow execute and report its declared measurements within its guards?"


@pytest.fixture
def study_config(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path / "home"))
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
    from hashlib import sha256

    from aqrs.admission import AdmissionRejected
    from aqrs.study_admission import admitted_worker, authorize_worker

    request, secret = authorize_worker(
        {"pilot_rows": 40, "pilot_columns": 1, "fit_limit": 1}
    )
    with sqlite3.connect(admitted_context) as db:
        stored = db.execute("SELECT payload_json FROM study_launches").fetchone()[0]
    assert json.loads(stored)["release_digest"] == sha256(secret).hexdigest()
    assert secret.hex() not in stored + json.dumps(request)
    assert set(request["_admission"]) == {"journal", "run_id", "launch_id"}
    with pytest.raises(AdmissionRejected, match="changed, unregistered"):
        with admitted_worker(request | {"fit_limit": 100}, lambda: secret):
            pytest.fail("Changed request was admitted.")
    with admitted_worker(request, lambda: secret):
        pass
    with pytest.raises(AdmissionRejected, match="already consumed"):
        with admitted_worker(request, lambda: secret):
            pytest.fail("Consumed worker approval was reused.")
    with pytest.raises(AdmissionRejected, match="caller cannot supply"):
        authorize_worker(request)


@pytest.mark.parametrize("proof_length", [0, 17])
def test_real_worker_rejects_missing_or_truncated_channel_proof(
    admitted_context, tmp_path, proof_length
):
    import os
    import subprocess
    import sys

    from aqrs.storage import write_json
    from aqrs.study_admission import authorize_worker

    request, secret = authorize_worker(
        {"pilot_rows": 40, "pilot_columns": 1, "fit_limit": 1}
    )
    directory = tmp_path / "incomplete-release"
    directory.mkdir()
    write_json(directory / "request.json", request)
    result = subprocess.run(
        [sys.executable, "-m", "aqrs.worker", str(directory)],
        env=dict(os.environ, PYTHONPATH=str(ROOT / "src")),
        input=b"1" + secret[:proof_length],
        capture_output=True,
        start_new_session=os.name == "posix",
        timeout=10,
    )
    assert result.returncode == 4, result.stderr
    record = json.loads((directory / "admission_stop.json").read_text())
    assert record["reason_code"] == "WORKER_CHANNEL_INVALID"
    assert not (directory / "started_fits.json").exists()
    with sqlite3.connect(admitted_context) as db:
        assert db.execute("SELECT consumed FROM study_launches").fetchone() == (0,)


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


def test_stale_monitor_stops_before_the_trial_deadline(tmp_path):
    from test_governor import probe

    from aqrs.governor import _supervise_process

    release = threading.Event()
    begin = time.monotonic()
    try:
        result = _supervise_process(
            tmp_path,
            {},
            12,
            begin + 15,
            512,
            command=probe("import time; time.sleep(20)"),
            admission_watch=lambda: release.wait(15),
        )
    finally:
        release.set()
    assert result["execution_status"] == "CANCELLED"
    assert result["reason_code"] == "ADMISSION_WATCH_STALE"
    assert time.monotonic() - begin < 8
    assert result["completed_fits"] == 0


LEGACY_ENTRIES = [
    ("aqrs.m2_e14", "run_campaign"),
    ("aqrs.m2_e14", "worker"),
    ("aqrs.m2_e19", "run_pilot"),
    ("aqrs.m2_e19", "worker"),
    ("aqrs.predictive_spot", "campaign"),
    ("aqrs.predictive_spot", "worker"),
    ("aqrs.predictive_spot", "acquire_month"),
    ("aqrs.blind_search", "register"),
    ("aqrs.blind_search", "execute"),
    ("aqrs.blind_search", "replay_evidence"),
    ("aqrs.blind_search", "evaluate_worker"),
    ("aqrs.spot_dataset", "prepare"),
    ("aqrs.binance_spot_pilot", "import_day"),
    ("aqrs.spot_dataset", "process_symbol"),
    ("scripts.m2_supervised_pilot", "main"),
    ("scripts.m2_supervised_pilot", "compare"),
    ("scripts.m2_supervised_pilot", "evaluate_worker"),
    ("scripts.m2_isolation_forest_pilot", "main"),
    ("scripts.m2_isolation_forest_pilot", "compare"),
    ("scripts.m2_isolation_forest_pilot", "evaluate_worker"),
    ("scripts.m2_e15_count", "execute"),
    ("scripts.m2_e15_count", "count_worker"),
]


@pytest.mark.parametrize("module,entry", LEGACY_ENTRIES)
def test_unqualified_legacy_entry_is_durably_blocked_before_its_body(
    tmp_path, monkeypatch, module, entry
):
    from aqrs.admission import AdmissionRejected

    function = getattr(import_module(module), entry)
    monkeypatch.chdir(tmp_path)
    # No body arguments are supplied: even argument-dependent I/O cannot run.
    with pytest.raises(AdmissionRejected) as stopped:
        function()
    assert stopped.value.code == "ENTRY_UNQUALIFIED"
    with sqlite3.connect(tmp_path / "artifacts/research.sqlite3") as db:
        row = db.execute(
            "SELECT execution_status, manifest_json FROM campaigns"
        ).fetchone()
    assert row[0] == "REJECTED_PREFLIGHT"
    record = json.loads(row[1])
    assert (
        record["study_data_accesses"]
        == record["started_workers"]
        == record["started_fits"]
        == 0
    )
    assert record["required_action"] and record["resumption_condition"]


@pytest.mark.parametrize(
    "study,reason",
    [
        ({"question": ""}, "QUESTION_UNCLEAR"),
        ({"design": "unqualified-method"}, "DESIGN_UNQUALIFIED"),
        ({"prerequisites": ["absent-proof"]}, "PREREQUISITE_MISSING"),
    ],
)
def test_real_cli_rejects_bad_study(study_config, tmp_path, study, reason):
    import os
    import subprocess
    import sys

    study_config["study"].update(study)
    path = tmp_path / "research.yaml"
    path.write_text(yaml.safe_dump(study_config), encoding="utf-8")
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
    result = subprocess.run(
        [sys.executable, "-m", "aqrs", "research", "run", "--config", str(path)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 2, result.stderr
    record = json.loads(result.stdout)
    assert record["reason_code"] == reason
    assert (
        record["study_data_accesses"]
        == record["started_workers"]
        == record["started_fits"]
        == 0
    )


@pytest.mark.parametrize(
    "reference", [None, {"journal": "absent", "run_id": "fake", "launch_id": "fake"}]
)
def test_real_worker_rejects_missing_or_forged_admission(tmp_path, reference):
    from aqrs.governor import _supervise_process

    request = {"stage": "prepare", "config": {}}
    if reference:
        request["_admission"] = reference
    result = _supervise_process(tmp_path, request, 8, time.monotonic() + 10, 512)
    assert result["execution_status"] == "REJECTED_PREFLIGHT"
    assert result["reason_code"] in {"ADMISSION_REQUIRED", "ADMISSION_UNVERIFIABLE"}
    assert result["required_action"] and result["resumption_condition"]
    assert result["completed_fits"] == result["started_fits"] == 0


def test_real_worker_rejects_changed_input_before_parsing(admitted_context, tmp_path):
    from aqrs.governor import supervise

    path = tmp_path / "changed.npy"
    path.write_bytes(b"This would fail parsing if reached.")
    result = supervise(
        tmp_path,
        {"prefix": str(path), "prefix_sha256": "0" * 64},
        8,
        time.monotonic() + 10,
        512,
    )
    assert result["reason_code"] == "DATA_CHANGED"
    assert result["execution_status"] == "REJECTED_PREFLIGHT"
    assert result["started_fits"] == result["completed_fits"] == 0


def test_changed_source_stops_before_dispatch(admitted_context, tmp_path, monkeypatch):
    from aqrs.governor import supervise

    monkeypatch.setattr(
        "aqrs.study_admission.source_identity", lambda: "changed-source"
    )
    result = supervise(tmp_path, {}, 8, time.monotonic() + 10, 512)
    assert not result["started"] and result["reason_code"] == "ADMISSION_CHANGED"


def test_repeat_is_a_new_attempt_and_correction_reaches_assessment(
    study_config, tmp_path
):
    study_config["study"]["question"] = ""
    first, first_code = research.run(study_config, tmp_path, plan_only=False)
    second, second_code = research.run(study_config, tmp_path, plan_only=False)
    assert first_code == second_code == 2 and first["run_id"] != second["run_id"]
    with sqlite3.connect(tmp_path / "results/journal.sqlite3") as db:
        assert db.execute("SELECT COUNT(*) FROM campaigns").fetchone()[0] == 2
    study_config["study"]["question"] = QUESTION
    plan, code = research.run(study_config, tmp_path, plan_only=True)
    assert code == 0 and plan["preflight_status"] == "ADMITTED"


def test_lost_prerequisite_prevents_next_dependent_trial(
    study_config, tmp_path, monkeypatch
):
    prerequisite = tmp_path / "review-evidence"
    prerequisite.touch()
    study_config["study"]["prerequisites"] = [prerequisite.name]
    actual_supervise = research.supervise
    dispatched = []

    def supervised(*args, **kwargs):
        outcome = actual_supervise(*args, **kwargs)
        dispatched.append(outcome)
        if (
            len(dispatched) == 2
        ):  # Preparation, then first candidate; timing is in planning.
            prerequisite.unlink()
        return outcome

    monkeypatch.setattr(research, "supervise", supervised)
    result, code = research.run(study_config, tmp_path, plan_only=False)
    assert code == 2 and result["reason_code"] == "PREREQUISITE_MISSING"
    report = json.loads((Path(result["output_dir"]) / "report.json").read_text())
    assert report["trials"][0]["execution_status"] == "COMPLETED"
    assert report["trials"][1]["started"] is False
    assert result["required_action"] and result["resumption_condition"]


@pytest.mark.parametrize("issuer_exits", [True, False])
def test_real_worker_rejects_orphan_or_copied_receipt(
    study_config, tmp_path, issuer_exits
):
    import os
    import subprocess
    import sys

    from aqrs.governor import _supervise_process

    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(study_config), encoding="utf-8")
    code = """
import json, os, sys
from pathlib import Path
from contextlib import closing
from aqrs import journal
from aqrs.storage import fingerprint, write_json
from aqrs.study_admission import assess, admitted_run, authorize_worker
root=Path(sys.argv[1]); config=json.loads((root/'config.json').read_text())
decision=assess(config,root); database=root/'orphan.sqlite3'
with closing(journal.connect(database)) as db:
    journal.begin(db,'orphan',fingerprint(config),config,{'study_admission':decision})
with admitted_run(database,'orphan',config,root,decision):
    request,secret=authorize_worker({'pilot_rows':40,'pilot_columns':1,'fit_limit':1})
    write_json(root/'grant.json', request)
    # Test-only pipe handoff: never persist the production release secret.
    print(secret.hex(), flush=True)
    if sys.argv[2] == "exit":
        os._exit(0)
    sys.stdin.read(1)
"""
    parent = subprocess.Popen(
        [sys.executable, "-c", code, str(tmp_path), "exit" if issuer_exits else "wait"],
        env=dict(os.environ, PYTHONPATH=str(ROOT / "src")),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        deadline = time.monotonic() + 10
        while not (tmp_path / "grant.json").exists():
            assert time.monotonic() < deadline and parent.poll() is None
            time.sleep(0.01)
        if issuer_exits:
            assert parent.wait(timeout=10) == 0
        secret = bytes.fromhex(parent.stdout.readline().strip())
        assert len(secret) == 32
        request = json.loads((tmp_path / "grant.json").read_text())
        result = _supervise_process(
            tmp_path,
            request,
            8,
            time.monotonic() + 10,
            512,
            release_secret=secret if issuer_exits else bytes(32),
        )
        assert result["execution_status"] == "REJECTED_PREFLIGHT"
        assert result["reason_code"] == (
            "ADMISSION_PARENT_LOST" if issuer_exits else "WORKER_CHANNEL_INVALID"
        )
        assert result["started_fits"] == result["completed_fits"] == 0
    finally:
        if parent.poll() is None:
            parent.communicate("x", timeout=10)
    with sqlite3.connect(tmp_path / "orphan.sqlite3") as db:
        assert db.execute("SELECT consumed FROM study_launches").fetchone() == (0,)


def test_expired_grant_stops_before_dispatch(admitted_context, tmp_path, monkeypatch):
    from aqrs import study_admission
    from aqrs.governor import supervise

    monkeypatch.setattr(study_admission, "monotonic", lambda: float("inf"))
    result = supervise(tmp_path, {}, 8, time.monotonic() + 10, 512)
    assert not result["started"] and result["reason_code"] == "ADMISSION_EXPIRED"


def test_prerequisite_named_declared_input_cannot_lose_its_binding(
    study_config, tmp_path, monkeypatch
):
    from aqrs import governor, journal
    from aqrs.storage import fingerprint
    from aqrs.study_admission import admitted_run, assess

    prerequisite = tmp_path / "declared_input"
    prerequisite.write_text("Initial evidence")
    (tmp_path / "input.csv").write_text("Not accessed by this admission test.")
    study_config["study"]["prerequisites"] = [prerequisite.name]
    study_config["market"].update(
        source="synthetic_csv", csv_path="input.csv", start_at="2024-02-01T00:00:00Z"
    )
    database = tmp_path / "journal.sqlite3"
    decision = assess(study_config, tmp_path)
    with closing(journal.connect(database)) as db:
        journal.begin(
            db,
            "collision",
            fingerprint(study_config),
            study_config,
            {"study_admission": decision},
        )
    monkeypatch.setattr(
        governor.subprocess,
        "Popen",
        lambda *a, **k: pytest.fail("Changed prerequisite reached Popen."),
    )
    with admitted_run(database, "collision", study_config, tmp_path, decision):
        prerequisite.write_text("Changed evidence, with another size")
        result = governor.supervise(
            tmp_path,
            {"pilot_rows": 40, "pilot_columns": 1},
            8,
            time.monotonic() + 10,
            512,
        )
    assert not result["started"] and result["reason_code"] == "ADMISSION_CHANGED"
