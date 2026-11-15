import sys
import time
from pathlib import Path

from aqrs.governor import _supervise_process as supervise
from aqrs.planning import make_plan


def probe(code):
    # This probe tests the OS containment primitive, not research admission.
    source = "import os, sys; from pathlib import Path\n"
    source += "from aqrs.storage import write_json\nfrom aqrs.platform_guard import arm_parent_loss_guard\n"
    source += "def evaluate(request, directory):\n    " + code + "\n"
    source += "directory = Path(sys.argv[1]); write_json(directory / 'ready.json', os.getpid())\n"
    source += "fd = sys.stdin.fileno()\nif os.read(fd, 1) == b'1':\n"
    source += "    arm_parent_loss_guard(fd)\n    result = evaluate({}, directory)\n    write_json(directory / 'result.json', result)\n"
    return [sys.executable, "-c", source]


def test_preflight_rejects_theoretical_eight_year_plan():
    plan = make_plan(5000, 5, 3, 3600, 12, 120, 300)
    assert plan["planned_fits"] == 75_000
    assert plan["estimated_wall_seconds"] == 270_000_000
    assert plan["preflight_status"] == "REJECTED_PREFLIGHT"
    trials = make_plan(3, 1, 1, 1, 12, 120, 300)
    assert trials["preflight_status"] == "REJECTED_PREFLIGHT"


def test_watchdog_kills_blocking_worker_and_descendant(tmp_path):
    sentinel = tmp_path / "survived"
    child = f"import time; from pathlib import Path; time.sleep(2); Path({str(sentinel)!r}).touch()"
    task = (
        f"import subprocess, sys, time; subprocess.Popen([sys.executable, '-c', {child!r}]);"
        f"from pathlib import Path; Path({str(tmp_path / 'spawned')!r}).touch(); time.sleep(60)"
    )
    started = time.monotonic()
    result = supervise(tmp_path, {}, 1.5, started + 10, 512, command=probe(task))
    assert result["execution_status"] == "TIMED_OUT"
    assert time.monotonic() - started < 5
    assert (tmp_path / "spawned").exists()
    time.sleep(2.1)
    assert not sentinel.exists()


def test_rss_pressure_and_campaign_exhaustion(tmp_path):
    started = time.monotonic()
    task = "import time; buffer = bytearray(96 * 1024**2); time.sleep(20)"
    result = supervise(tmp_path, {}, 4, started + 10, 64, command=probe(task))
    assert result["execution_status"] == "MEMORY_LIMIT"
    assert result["peak_rss_mb"] > 64
    result = supervise(
        tmp_path,
        {},
        10,
        time.monotonic() + 1.2,
        512,
        command=probe("import time; time.sleep(60)"),
    )
    assert result["execution_status"] == "BUDGET_EXHAUSTED"
    assert result["started"]
    result = supervise(
        tmp_path,
        {},
        4,
        started,
        512,
        command=probe("raise AssertionError('must not start')"),
    )
    assert result["execution_status"] == "BUDGET_EXHAUSTED"
    assert not result["started"]


def test_failed_worker_does_not_supply_results(tmp_path):
    result = supervise(
        Path(tmp_path),
        {},
        5,
        time.monotonic() + 10,
        512,
        command=probe("raise ValueError('broken fit')"),
    )
    assert result["execution_status"] == "FAILED"
    assert result["completed_fits"] == 0
    assert "result" not in result
    assert sys.platform in {"win32", "linux"}


def test_parent_loss_terminates_worker_and_descendant(tmp_path):
    import subprocess

    import psutil

    sentinel = tmp_path / "survived"
    child = f"import time; from pathlib import Path; time.sleep(5); Path({str(sentinel)!r}).touch()"
    worker_ready = tmp_path / "worker"
    task = (
        f"import os, subprocess, time; child = subprocess.Popen([sys.executable, '-c', {child!r}]);"
        f"from aqrs.storage import write_text; "
        f"write_text(Path({str(worker_ready)!r}), f'{{os.getpid()}} {{child.pid}}'); time.sleep(60)"
    )
    supervisor_ready = tmp_path / "supervisor"
    harness = (
        "import os, time; from pathlib import Path; from aqrs.governor import _supervise_process as supervise; "
        f"Path({str(supervisor_ready)!r}).write_text(str(os.getpid())); "
        f"supervise(Path({str(tmp_path)!r}), {{}}, 15, time.monotonic() + 20, 512, "
        f"command={probe(task)!r})"
    )
    proc = subprocess.Popen([sys.executable, "-c", harness])
    try:
        deadline = time.monotonic() + 5
        while not worker_ready.exists() or not worker_ready.stat().st_size:
            assert proc.poll() is None and time.monotonic() < deadline
            time.sleep(0.02)
        pids = [int(pid) for pid in worker_ready.read_text().split()]
        assert len(pids) == 2
        supervisor = psutil.Process(int(supervisor_ready.read_text()))
        supervisor.kill()
        proc.wait(timeout=5)
        deadline = time.monotonic() + 4

        def alive(pid):
            try:
                return psutil.Process(pid).status() != psutil.STATUS_ZOMBIE
            except psutil.NoSuchProcess:
                return False

        while any(alive(pid) for pid in pids):
            assert time.monotonic() < deadline
            time.sleep(0.02)
        assert not sentinel.exists()
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=5)
