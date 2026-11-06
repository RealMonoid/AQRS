import json
import os
import subprocess
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from traceback import extract_tb

import psutil

from aqrs.platform_guard import WindowsJob, stop_tree, tree_usage
from aqrs.storage import write_json


def supervise(
    workdir: Path,
    request: dict,
    trial_seconds: float,
    campaign_deadline: float,
    max_rss_mb: float,
    *,
    command: list[str] | None = None,
) -> dict:
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
        "runtime_wall_seconds": 0.0,
    }
    if started_at >= deadline:
        return outcome

    command = command or [sys.executable, "-m", "aqrs.worker"]
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
        job = process = None
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
                _watch(
                    process,
                    job,
                    directory,
                    deadline,
                    campaign_deadline <= trial_deadline,
                    max_rss_mb,
                    outcome,
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
            if process is not None:
                stop_tree(process, job)
            elif job is not None:
                job.close()
        fits = directory / "fits.json"
        if fits.exists():
            outcome["completed_fits"] = _read(fits)
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


def _watch(process, job, directory, deadline, campaign_limited, max_rss_mb, outcome):
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

        code = process.poll()
        if code is not None:
            result = directory / "result.json"
            if code == 0 and outcome["started"]:
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
                process.stdin.write(b"1")
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
