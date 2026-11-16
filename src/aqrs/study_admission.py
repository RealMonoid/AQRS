"""FR-005 admission at the application boundary, not a general scientific judge.

Structured requests cover synthetic bar rules and Ridge. A caller cannot
replace a required supervised detectability check by supplying PASS.
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
from hashlib import sha256
from pathlib import Path
from secrets import compare_digest, token_bytes
from time import monotonic
from uuid import uuid4

import psutil

from aqrs import journal
from aqrs.admission import AdmissionRejected
from aqrs.storage import fingerprint

POLICY = "FR005_SYNTHETIC_STUDY_V2"
_parent = ContextVar("study_parent_admission", default=None)
_worker = ContextVar("study_worker_admission", default=None)


def reject(
    code: str,
    reason: str,
    action: str = "Correct the reported condition and start a fresh checked attempt.",
) -> AdmissionRejected:
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


def effect_variation(study: dict) -> dict:
    value = study.get(
        "effect_variation",
        {
            "decision_case": "fluctuating",
            "quiet": 0.04,
            "volatile": 0.16,
        },
    )
    if (
        not isinstance(value, dict)
        or set(value) != {"decision_case", "quiet", "volatile"}
        or value["decision_case"] not in ("constant", "fluctuating")
        or any(
            type(value[k]) not in (int, float)
            or not 0 <= value[k] <= 1
            for k in ("quiet", "volatile")
        )
    ):
        raise reject(
            "INVALID_VARIATION",
            "Invalid effect_variation assumption.",
            "Specify decision_case constant/fluctuating and quiet/volatile amplitudes from 0 to 1.",
        )
    return value.copy()


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
    keys = {
        "question",
        "rule",
        "minimum_effect",
        "on_advantage",
        "on_no_advantage",
        "on_inconclusive",
    }
    if not keys <= set(study) <= keys | {"effect_variation"} or any(
        not isinstance(study[k], str) or not study[k].strip()
        for k in keys - {"minimum_effect"}
    ):
        raise reject(
            "STUDY_FIELDS_REQUIRED",
            "Specify question, rule, minimum_effect and all three outcome actions.",
            "Complete the structured study request.",
        )
    effect = study["minimum_effect"]
    if type(effect) not in (int, float) or not 0 < effect < 0.5:
        raise reject(
            "INVALID_EFFECT",
            "minimum_effect must be an accuracy gap strictly between 0 and 0.5.",
            "State the smallest relevant advantage over the stronger constant control as a fraction.",
        )
    effect_variation(study)
    if study["rule"] not in {"bar_reversal", "volume_movement", "ridge"} or any(
        c["model"] != study["rule"] for c in config["research"]["candidates"]
    ):
        raise reject(
            "RULE_MISMATCH",
            "The study rule must match every candidate: bar_reversal, volume_movement or ridge.",
            "Use one supported synthetic rule consistently.",
        )
    if config["market"]["source"] not in {"synthetic", "synthetic_csv"}:
        raise reject(
            "SOURCE_NOT_ALLOWED",
            "This study procedure only admits synthetic data.",
            "Retain the market-research stop.",
        )
    input_file = None
    if config["market"]["source"] == "synthetic_csv":
        path = (base / config["market"]["csv_path"]).resolve()
        if path.is_file():
            stat = path.stat()
            input_file = [str(path), stat.st_size, stat.st_mtime_ns]
    return {
        "policy": POLICY,
        "decision": "STRUCTURED_SYNTHETIC_REQUEST",
        "study": study.copy(),
        "review_basis": "Required fields only; question meaning is not judged. Bar-rule detectability is checked; Ridge detectability is unsupported.",
        "configuration": fingerprint(config),
        "source": source_identity(),
        "input_file": input_file,
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

    def check(self, *, ready: bool = False) -> None:
        if monotonic() >= self.deadline:
            raise reject(
                "ADMISSION_EXPIRED",
                "The admitted campaign validity has expired.",
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
            )
        current = assess(self.config, self.base)
        if current != self.decision:
            raise reject(
                "ADMISSION_CHANGED",
                "The admitted source, configuration or prerequisite changed.",
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
            )
        if (
            ready
            and self.config["study"]["rule"] != "ridge"
            and not (
                manifest.get("detectability", {}).get("admitted") is True
                and manifest["detectability"].get("configuration")
                == current["configuration"]
            )
        ):
            raise reject(
                "DETECTABILITY_REQUIRED",
                "No successful detectability check is bound to this study.",
                "Run the bounded detectability check before accessing study inputs.",
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


def authorize_worker(request: dict) -> tuple[dict, bytes]:
    context = require_parent(validate=False)
    context.check(ready=request.get("stage") != "detectability")
    if "prefix" in request and not request.get("prefix_sha256"):
        raise reject(
            "DATA_IDENTITY_REQUIRED",
            "Prepared input has no admitted byte identity.",
            "Use the input identity returned by the admitted preparation stage.",
        )
    if (
        request.get("stage") == "prepare"
        and context.config["market"]["source"] == "synthetic_csv"
        and context.decision["input_file"] is None
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
        )
    launch_id = uuid4().hex
    release_secret = token_bytes(32)
    payload = {
        "decision": context.decision,
        "base": str(context.base),
        "configuration": context.config,
        "owner_process": context.owner_process,
        "deadline": context.deadline,
        "release_digest": sha256(release_secret).hexdigest(),
    }
    with closing(journal.connect(context.database)) as db, db:
        db.execute(
            "INSERT INTO study_launches VALUES (?, ?, ?, ?, 0)",
            (launch_id, context.run_id, fingerprint(request), json.dumps(payload)),
        )
    admitted = request | {
        "_admission": {
            "journal": str(context.database),
            "run_id": context.run_id,
            "launch_id": launch_id,
        }
    }
    return admitted, release_secret


@contextmanager
def admitted_worker(request: dict, read_release):
    if not isinstance(request, dict):
        raise reject(
            "ADMISSION_REQUIRED",
            "Worker request must be an admitted object.",
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
            context.check(ready=request.get("stage") != "detectability")
            # The one-time proof travels only over the supervisor-owned pipe.
            # A copied journal receipt cannot supply this in-memory capability.
            secret = read_release()
            if (
                not isinstance(secret, bytes)
                or len(secret) != 32
                or not compare_digest(
                    sha256(secret).hexdigest(), payload["release_digest"]
                )
            ):
                raise reject(
                    "WORKER_CHANNEL_INVALID",
                    "The worker has no valid one-time supervisor-channel proof.",
                )
            cursor = db.execute(
                "UPDATE study_launches SET consumed = 1 WHERE launch_id = ? AND consumed = 0",
                (reference["launch_id"],),
            )
            if cursor.rowcount != 1:
                raise reject(
                    "WORKER_ADMISSION_INVALID",
                    "Worker admission was already consumed.",
                )
    token = _worker.set(True)
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
            block_unqualified(entry)

        return stopped

    return decorate
