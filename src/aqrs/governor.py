import json
import os
import sqlite3
import subprocess
import sys
import threading
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from traceback import extract_tb

import psutil

from aqrs.platform_guard import WindowsJob, stop_tree, tree_usage
from aqrs.storage import write_json
from aqrs.study_admission import (
    authorize_worker,
    record_stopped,
    reject,
    require_parent,
)

ADMISSION_MAX_AGE_SECONDS = 5.0


class _AdmissionWatch:
    """Keep metadata I/O off the deadline watcher; stale checks fail closed."""

    def __init__(self, check):
        self.stop = threading.Event()
        self.state = (time.monotonic(), None)
        self.thread = threading.Thread(target=self._observe, args=(check,), daemon=True)
        self.thread.start()

    def _observe(self, check):
        while not self.stop.is_set():
            issue = None
            try:
                check()
            except (ValueError, OSError, sqlite3.Error, TypeError, KeyError) as error:
                issue = (getattr(error, "code", "ADMISSION_UNVERIFIABLE"), str(error))
            self.state = (time.monotonic(), issue)
            if issue or self.stop.wait(0.25):
                return

    def issue(self):
        checked, issue = self.state
        if issue:
            return issue
        # Engineering freshness limit; the worker deadline is never extended.
        if time.monotonic() - checked > ADMISSION_MAX_AGE_SECONDS:
            return (
                "ADMISSION_WATCH_STALE",
                "Current admission could not be rechecked within five seconds.",
            )
        return None


def supervise(
    workdir: Path,
    request: dict,
    trial_seconds: float,
    campaign_deadline: float,
    max_rss_mb: float,
    *,
    command: list[str] | None = None,
) -> dict:
    """Dispatch research only after durable, current study admission."""
    try:
        if command is not None:
            error = reject(
                "ENTRY_UNQUALIFIED",
                "Custom research worker commands require a qualified admission contract.",
                "Qualify the requested entry before dispatch; use the common admitted entry.",
            )
            record_stopped("common.custom_command", error, {"command": command})
            raise error
        context = require_parent(validate=False)
        admitted, release_secret = authorize_worker(request)
    except (ValueError, OSError, sqlite3.Error, TypeError, KeyError) as error:
        return {
            "execution_status": "REJECTED_PREFLIGHT",
            "stop_reason": str(error),
            "reason_code": getattr(error, "code", "ADMISSION_STORAGE_FAILED"),
            "required_action": getattr(
                error,
                "required_action",
                "Restore a verifiable qualified study admission.",
            ),
            "resumption_condition": getattr(
                error,
                "resumption_condition",
                "A fresh checked request satisfies the missing prerequisite.",
            ),
            "started": False,
            "peak_rss_mb": None,
            "sampled_cpu_seconds": 0.0,
            "completed_fits": 0,
            "started_fits": 0,
            "runtime_wall_seconds": 0.0,
        }
    return _supervise_process(
        workdir,
        admitted,
        trial_seconds,
        campaign_deadline,
        max_rss_mb,
        admission_watch=lambda: context.check(
            ready=request.get("stage") != "detectability"
        ),
        release_secret=release_secret,
    )


def _supervise_process(
    workdir: Path,
    request: dict,
    trial_seconds: float,
    campaign_deadline: float,
    max_rss_mb: float,
    *,
    command: list[str] | None = None,
    admission_watch=None,
    release_secret: bytes = b"",
) -> dict:
    """Private process-containment primitive; no research permission is issued."""
    started_at = time.monotonic()
    trial_deadline = started_at + trial_seconds
    deadline = min(trial_deadline, campaign_deadline)
    outcome = {
        "execution_status": "BUDGET_EXHAUSTED",
        "stop_reason": "Campaign wall-time budget exhausted.",
        "started": False,
        "peak_rss_mb": None,
        "sampled_cpu_seconds": 0.0,
        "completed_fits": 0,
        "started_fits": 0,
        "runtime_wall_seconds": 0.0,
    }
    if started_at >= deadline:
        return outcome

    command = command or (
        [sys.executable, "-B", "-E", request["_worker_entry"]]
        if request.get("_worker_entry")
        else [sys.executable, "-B", "-m", "aqrs.worker"]
    )
    windows = sys.platform == "win32"
    env = dict(os.environ)
    for key in (
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "OMP_NUM_THREADS",
        "BLIS_NUM_THREADS",
    ):
        env[key] = "1"

    with TemporaryDirectory(prefix="worker-", dir=workdir) as temporary:
        directory = Path(temporary)
        write_json(directory / "request.json", request)
        job = process = watcher = None
        try:
            job = WindowsJob() if windows else None
            with (directory / "worker.log").open("wb") as log:
                process = subprocess.Popen(
                    [*command, str(directory)],
                    stdin=subprocess.PIPE,
                    stdout=log,
                    stderr=log,
                    start_new_session=not windows,
                    env=env,
                    creationflags=subprocess.CREATE_NO_WINDOW if windows else 0,
                )
                if admission_watch is not None:
                    watcher = _AdmissionWatch(admission_watch)
                _watch(
                    process,
                    job,
                    directory,
                    deadline,
                    campaign_deadline <= trial_deadline,
                    max_rss_mb,
                    outcome,
                    watcher,
                    release_secret,
                )
        except KeyboardInterrupt:
            outcome.update(
                execution_status="CANCELLED", stop_reason="Cancelled by operator."
            )
        except (OSError, ImportError, psutil.Error) as error:
            frame = extract_tb(error.__traceback__)[-1]
            location = f"{Path(frame.filename).name}:{frame.name}"
            outcome.update(
                execution_status="FAILED"
                if outcome["started"]
                else "REJECTED_PREFLIGHT",
                stop_reason=f"Worker containment or observation failed at {location} "
                f"({type(error).__name__}, errno {getattr(error, 'errno', None)}).",
            )
        finally:
            if watcher is not None:
                watcher.stop.set()
            if process is not None:
                stop_tree(process, job)
            elif job is not None:
                job.close()
        fits = directory / "fits.json"
        if fits.exists():
            outcome["completed_fits"] = _read(fits)
        started_fits = directory / "started_fits.json"
        if started_fits.exists():
            outcome["started_fits"] = _read(started_fits)
        outcome["runtime_wall_seconds"] = time.monotonic() - started_at
        return outcome


def _read(path: Path, deadline: float = float("inf")):
    # Windows readers can encounter transient sharing errors around an atomic rename.
    read_deadline = min(deadline, time.monotonic() + 0.25)
    while True:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except PermissionError:
            if sys.platform != "win32" or time.monotonic() >= read_deadline:
                raise
            time.sleep(0.01)


def _watch(
    process,
    job,
    directory,
    deadline,
    campaign_limited,
    max_rss_mb,
    outcome,
    admission_watch=None,
    release_secret: bytes = b"",
):
    ready = directory / "ready.json"
    pid = process.pid
    while True:
        if time.monotonic() >= deadline:
            status = "BUDGET_EXHAUSTED" if campaign_limited else "TIMED_OUT"
            boundary = "Campaign" if campaign_limited else "Trial"
            outcome.update(
                execution_status=status, stop_reason=f"{boundary} wall-time limit."
            )
            return

        if admission_watch is not None and (issue := admission_watch.issue()):
            outcome.update(
                execution_status="CANCELLED"
                if outcome["started"]
                else "REJECTED_PREFLIGHT",
                reason_code=issue[0],
                stop_reason=issue[1],
                required_action="Restore the failed prerequisite and reassess the affected study.",
                resumption_condition="A new attempt passes current admission; no automatic retry.",
            )
            return

        code = process.poll()
        if code is not None:
            result = directory / "result.json"
            if code == 4 and (directory / "admission_stop.json").exists():
                outcome.update(
                    execution_status="REJECTED_PREFLIGHT",
                    **_read(directory / "admission_stop.json"),
                )
            elif code == 3 and (directory / "budget_stop.json").exists():
                outcome.update(
                    execution_status="BUDGET_EXHAUSTED",
                    stop_reason="Fit budget exhausted before fit.",
                )
            elif code == 0 and outcome["started"]:
                try:
                    metrics = _read(result, deadline)
                except FileNotFoundError:
                    outcome.update(
                        execution_status="FAILED",
                        stop_reason="Worker result is missing.",
                    )
                else:
                    outcome.update(
                        execution_status="COMPLETED", stop_reason=None, result=metrics
                    )
            else:
                outcome.update(
                    execution_status="FAILED", stop_reason=f"Worker exited with {code}."
                )
            return

        ready_pid = None
        if not outcome["started"]:
            try:
                ready_pid = _read(ready, deadline)
            except FileNotFoundError:
                pass
        if ready_pid is not None:
            pid = ready_pid
            if job is not None:
                job.attach(pid)
            rss, cpu_seconds = tree_usage(pid)
            if rss <= max_rss_mb and time.monotonic() < deadline:
                process.stdin.write(b"1" + release_secret)
                process.stdin.flush()
                outcome["started"] = True
        else:
            try:
                rss, cpu_seconds = tree_usage(pid)
            except psutil.NoSuchProcess:
                # The interpreter may exit just before its launcher reports the exit code.
                time.sleep(0.01)
                continue
        outcome["peak_rss_mb"] = max(outcome["peak_rss_mb"] or 0, rss)
        outcome["sampled_cpu_seconds"] = max(
            outcome["sampled_cpu_seconds"], cpu_seconds
        )
        if rss > max_rss_mb:
            outcome.update(
                execution_status="MEMORY_LIMIT",
                stop_reason="Sampled tree RSS exceeded limit.",
            )
            return
        time.sleep(0.02)
