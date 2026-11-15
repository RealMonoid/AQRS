"""FR-005 admission at the application boundary, not a general scientific judge.

The only automatically qualified contract is the public synthetic engineering
workflow. A caller cannot qualify a new scientific question by supplying PASS.
The local journal and installed application are trusted; arbitrary Python or
an operator rewriting either is outside this application-interface boundary.
"""

import json
import os
import sqlite3
from contextlib import closing, contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from time import monotonic
from uuid import uuid4

import psutil

from aqrs import journal
from aqrs.admission import AdmissionRejected
from aqrs.storage import fingerprint

QUESTION = "Can the configured synthetic workflow execute and report its declared measurements within its guards?"
DESIGN = "common_synthetic_workflow_v1"
POLICY = "FR005_ENGINEERING_V1"
_parent = ContextVar("study_parent_admission", default=None)
_worker = ContextVar("study_worker_admission", default=None)


def reject(code: str, reason: str, action: str) -> AdmissionRejected:
    error = AdmissionRejected(code, reason)
    error.required_action = action
    error.resumption_condition = (
        "The corrected request passes current question, design, prerequisite "
        "and execution checks; the rejected request is not retried unchanged."
    )
    return error


def source_identity() -> str:
    return fingerprint(
        {
            p.name: p.read_text(encoding="utf-8")
            for p in sorted(Path(__file__).parent.glob("*.py"))
        }
    )


def assess(config: dict, base: Path) -> dict:
    """Check an operational question against the qualified contract before I/O."""
    study = config.get("study")
    if (
        not isinstance(study, dict)
        or not isinstance(study.get("question"), str)
        or not study["question"].strip()
    ):
        raise reject(
            "QUESTION_UNCLEAR",
            "No operational research question was supplied.",
            "Specify the intended question, measurement and decision; do not invent a substitute.",
        )
    if study["question"] != QUESTION:
        raise reject(
            "QUESTION_UNREVIEWED",
            "This question has no qualified review in the installed procedure contract.",
            "Clarify and independently qualify the intended question and design; retain the original objective.",
        )
    if (
        set(study) != {"question", "design", "claim", "prerequisites"}
        or study.get("design") != DESIGN
        or study.get("claim") != "engineering"
    ):
        raise reject(
            "DESIGN_UNQUALIFIED",
            "The design or claim is not supported by this reviewed engineering procedure.",
            "Provide a qualified method/design for the intended claim. A PASS field or synthetic label is not a scientific review.",
        )
    if config["market"]["source"] not in {"synthetic", "synthetic_csv"}:
        raise reject(
            "SCIENTIFIC_REVIEW_REQUIRED",
            "The engineering procedure cannot admit a market study.",
            "Qualify the scientific review and satisfy the existing market authorization before research.",
        )
    prerequisites = study["prerequisites"]
    if not isinstance(prerequisites, list) or any(
        not isinstance(p, str) or not p.strip() for p in prerequisites
    ):
        raise reject(
            "PREREQUISITES_UNCLEAR",
            "Prerequisites must be explicit file references.",
            "Declare the files required for this action, or an empty list when none are required.",
        )
    stamps = {}
    for name in prerequisites:
        path = (base / name).resolve()
        if not path.is_file():
            raise reject(
                "PREREQUISITE_MISSING",
                f"Required prerequisite is unavailable: {name}",
                "Establish the named prerequisite or park this dependent action.",
            )
        stat = path.stat()
        stamps[name] = [stat.st_size, stat.st_mtime_ns]
    if config["market"]["source"] == "synthetic_csv":
        path = (base / config["market"]["csv_path"]).resolve()
        stamps["declared_input"] = None
        if path.is_file():
            stat = path.stat()
            stamps["declared_input"] = [str(path), stat.st_size, stat.st_mtime_ns]
    return {
        "policy": POLICY,
        "decision": "ADMITTED_ENGINEERING_ONLY",
        "question": QUESTION,
        "design": DESIGN,
        "review_basis": "Installed deterministic engineering contract and public behavioral qualification; not scientific-review qualification.",
        "configuration": fingerprint(config),
        "source": source_identity(),
        "prerequisites": stamps,
        "supports_market_claim": False,
    }


@dataclass
class _Run:
    database: Path
    run_id: str
    config: dict
    base: Path
    decision: dict
    owner_process: tuple[int, float]
    deadline: float

    def check(self) -> None:
        if monotonic() >= self.deadline:
            raise reject(
                "ADMISSION_EXPIRED",
                "The admitted campaign validity has expired.",
                "Register a new checked attempt within the authorized budget.",
            )
        try:
            owner = psutil.Process(self.owner_process[0])
            alive = (
                owner.is_running()
                and owner.create_time() == self.owner_process[1]
                and owner.status() != psutil.STATUS_ZOMBIE
            )
        except psutil.Error:
            alive = False
        if not alive:
            raise reject(
                "ADMISSION_PARENT_LOST",
                "The admission issuer is no longer alive.",
                "Start a new checked attempt; stale RUNNING records cannot resume a study.",
            )
        current = assess(self.config, self.base)
        if current != self.decision:
            raise reject(
                "ADMISSION_CHANGED",
                "The admitted source, configuration or prerequisite changed.",
                "Reassess the changed study before resuming.",
            )
        with closing(
            sqlite3.connect(self.database.as_uri() + "?mode=ro", uri=True, timeout=1)
        ) as db:
            row = db.execute(
                "SELECT execution_status, config_fingerprint, manifest_json FROM campaigns WHERE run_id = ?",
                (self.run_id,),
            ).fetchone()
        manifest = json.loads(row[2]) if row else None
        if (
            not row
            or row[0] != "RUNNING"
            or row[1] != current["configuration"]
            or not isinstance(manifest, dict)
            or manifest.get("study_admission") != self.decision
        ):
            raise reject(
                "ADMISSION_REVOKED",
                "Current durable campaign admission is missing, changed or revoked.",
                "Restore valid current admission through a new checked attempt.",
            )


@contextmanager
def admitted_run(database: Path, run_id: str, config: dict, base: Path, decision: dict):
    context = _Run(
        database.resolve(),
        run_id,
        config,
        base.resolve(),
        decision,
        (os.getpid(), psutil.Process().create_time()),
        monotonic() + config["resource_governor"]["max_wall_seconds_per_campaign"],
    )
    context.check()
    token = _parent.set(context)
    try:
        yield
    finally:
        _parent.reset(token)


def require_parent(*, validate: bool = True) -> _Run:
    context = _parent.get()
    if context is None:
        error = reject(
            "ADMISSION_REQUIRED",
            "No checked parent study admission is active.",
            "Use the admitted common research entry; direct execution is not approved.",
        )
        record_stopped("common.parent", error)
        raise error
    if validate:
        context.check()
    return context


def authorize_worker(request: dict) -> dict:
    context = require_parent()
    if "prefix" in request and not request.get("prefix_sha256"):
        raise reject(
            "DATA_IDENTITY_REQUIRED",
            "Prepared input has no admitted byte identity.",
            "Use the input identity returned by the admitted preparation stage.",
        )
    if (
        request.get("stage") == "prepare"
        and context.config["market"]["source"] == "synthetic_csv"
        and context.decision["prerequisites"].get("declared_input") is None
    ):
        raise reject(
            "PREREQUISITE_MISSING",
            "The declared synthetic input file is unavailable.",
            "Provide the declared input before analysis; acquisition requires its own admission.",
        )
    if "_admission" in request:
        raise reject(
            "FORGED_ADMISSION",
            "A caller cannot supply a worker admission record.",
            "Dispatch a fresh request through the checked parent entry.",
        )
    entry = request.get("_worker_entry")
    if entry and Path(entry).read_text(encoding="utf-8") != Path(__file__).with_name(
        "worker.py"
    ).read_text(encoding="utf-8"):
        raise reject(
            "ENTRY_UNQUALIFIED",
            "The requested worker differs from the qualified common entry.",
            "Qualify the changed worker before execution.",
        )
    launch_id = uuid4().hex
    payload = {
        "decision": context.decision,
        "base": str(context.base),
        "configuration": context.config,
        "owner_process": context.owner_process,
        "deadline": context.deadline,
    }
    with closing(journal.connect(context.database)) as db, db:
        db.execute(
            "INSERT INTO study_launches VALUES (?, ?, ?, ?, 0)",
            (launch_id, context.run_id, fingerprint(request), json.dumps(payload)),
        )
    return request | {
        "_admission": {
            "journal": str(context.database),
            "run_id": context.run_id,
            "launch_id": launch_id,
        }
    }


@contextmanager
def admitted_worker(request: dict):
    if not isinstance(request, dict):
        raise reject(
            "ADMISSION_REQUIRED",
            "Worker request must be an admitted object.",
            "Use the checked common entry.",
        )
    reference = request.get("_admission")
    if not isinstance(reference, dict) or set(reference) != {
        "journal",
        "run_id",
        "launch_id",
    }:
        raise reject(
            "ADMISSION_REQUIRED",
            "Worker admission is missing or malformed.",
            "Use a fresh checked parent dispatch.",
        )
    database = Path(reference["journal"]).resolve()
    clean = {k: v for k, v in request.items() if k != "_admission"}
    with closing(
        sqlite3.connect(database.as_uri() + "?mode=rw", uri=True, timeout=1)
    ) as db:
        with db:
            row = db.execute(
                "SELECT run_id, request_fingerprint, payload_json, consumed FROM study_launches WHERE launch_id = ?",
                (reference["launch_id"],),
            ).fetchone()
            if (
                not row
                or row[0] != reference["run_id"]
                or row[1] != fingerprint(clean)
                or row[3]
            ):
                raise reject(
                    "WORKER_ADMISSION_INVALID",
                    "Worker request is changed, unregistered or already consumed.",
                    "Issue a new checked attempt; never replay a launch record.",
                )
            payload = json.loads(row[2])
            context = _Run(
                database,
                reference["run_id"],
                payload["configuration"],
                Path(payload["base"]),
                payload["decision"],
                tuple(payload["owner_process"]),
                payload["deadline"],
            )
            context.check()
            # The current process is allowed for isolated context checks; a real
            # worker must descend from the original issuer, including Windows launchers.
            ancestry = [psutil.Process(), *psutil.Process().parents()]
            if not any(
                (p.pid, p.create_time()) == context.owner_process for p in ancestry
            ):
                raise reject(
                    "ADMISSION_PARENT_MISMATCH",
                    "The worker is not supervised by its admission issuer.",
                    "Use a fresh dispatch from the admitted parent.",
                )
            cursor = db.execute(
                "UPDATE study_launches SET consumed = 1 WHERE launch_id = ? AND consumed = 0",
                (reference["launch_id"],),
            )
            if cursor.rowcount != 1:
                raise reject(
                    "WORKER_ADMISSION_INVALID",
                    "Worker admission was already consumed.",
                    "Issue a new checked attempt.",
                )
    token = _worker.set(context)
    try:
        yield
    finally:
        _worker.reset(token)


def require_worker() -> None:
    context = _worker.get()
    if context is None:
        error = reject(
            "ADMISSION_REQUIRED",
            "No checked worker admission is active.",
            "Use the supervised admitted worker entry.",
        )
        record_stopped("common.worker", error)
        raise error
    context.check()


def record_stopped(entry: str, error: AdmissionRejected, request=None) -> None:
    """Record a rejected direct entry without touching its study input."""
    config = {"entry": entry, "request": request, "research": {"candidates": []}}
    record = {
        "reason_code": error.code,
        "stop_reason": str(error),
        "required_action": error.required_action,
        "resumption_condition": error.resumption_condition,
        "study_data_accesses": 0,
        "started_workers": 0,
        "started_fits": 0,
    }
    try:
        with closing(
            journal.connect(Path.cwd() / "artifacts" / "research.sqlite3")
        ) as db:
            journal.begin(
                db, uuid4().hex, fingerprint(config), config, record, rejection=record
            )
    except (OSError, sqlite3.Error) as failure:
        raise reject(
            "ADMISSION_STORAGE_FAILED",
            "The entry is blocked and its rejection record could not be saved.",
            "Restore journal storage before requesting execution.",
        ) from failure


def block_unqualified(entry: str, request=None) -> None:
    error = reject(
        "ENTRY_UNQUALIFIED",
        f"FR-005 admission is not qualified for {entry}.",
        "Qualify this entry and its study contract before execution; use the admitted common synthetic workflow for engineering checks.",
    )
    record_stopped(entry, error, request)
    raise error


def unqualified_entry(entry: str):
    """Keep legacy launchers closed while preserving their numerical functions."""

    def decorate(function):
        @wraps(function)
        def stopped(*args, **kwargs):
            # Preserve declared arguments, never inspect referenced files/arrays.
            request = json.loads(
                json.dumps(
                    {"args": args, "kwargs": kwargs},
                    default=lambda value: (
                        str(value)
                        if isinstance(value, Path)
                        else {"type": type(value).__name__}
                    ),
                )
            )
            block_unqualified(entry, request)

        return stopped

    return decorate
