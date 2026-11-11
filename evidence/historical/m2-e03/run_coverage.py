"""Acquire and count only the four authorized M2-E03 development days."""

import json
import runpy
import subprocess
import sys
from datetime import UTC, date, datetime
from hashlib import sha256
from itertools import permutations
from pathlib import Path
from time import perf_counter
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, build_opener

from aqrs.binance_spot_pilot import ARCHIVE_BASE, INPUT_LIMIT, import_day

LOCAL = Path("artifacts/m2-e03")
PRIOR = Path("artifacts/m2-e02")
DAYS = tuple(date(2026, 1, number) for number in (1, 2, 3, 4))
BLOCK_STARTS = [0, 480, 960]
FILES = {}
for day in DAYS:
    name = f"BTCUSDT-1m-{day.isoformat()}.zip"
    FILES[f"{ARCHIVE_BASE}/{name}"] = (name, INPUT_LIMIT)
    FILES[f"{ARCHIVE_BASE}/{name}.CHECKSUM"] = (f"{name}.CHECKSUM", 4096)


class RefuseRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, new_url):
        raise HTTPError(request.full_url, code, "Redirect refused", headers, response)


def fetch(opener, url):
    if url not in FILES:
        raise ValueError("URL is outside the authorized file allowlist.")
    name, limit = FILES[url]
    target = LOCAL / name
    if target.exists():
        raise FileExistsError(target)
    print(f"Requesting {url}", flush=True)
    with opener.open(url, timeout=10) as response:
        payload = response.read(limit + 1)
    if len(payload) > limit:
        raise ValueError(f"Response exceeds the byte limit for {name}.")
    with target.open("xb") as output:
        output.write(payload)
    print(f"Saved {name}, {len(payload)} bytes", flush=True)


def acquire():
    opener = build_opener(RefuseRedirect())
    for url in FILES:
        fetch(opener, url)


def covering_dates(daily):
    for distinct in permutations(daily, len(BLOCK_STARTS)):
        if all(day["blocks"][band]["pair"] for band, day in enumerate(distinct)):
            return [day["development_day_utc"] for day in distinct]
    return []


def count():
    previous = json.loads((PRIOR / "coverage.json").read_text(encoding="utf-8"))
    previous_day = previous["coverage"]
    scanner = PRIOR / "count_pairs.py"
    if (
        previous["execution_status"] != "COMPLETED"
        or previous["exit_code"] != 0
        or previous_day["development_day_utc"] != "2026-01-05"
        or [row["block_start_minute_utc"] for row in previous_day["blocks"]] != BLOCK_STARTS
        or sha256(scanner.read_bytes()).hexdigest() != previous["script_sha256"]
    ):
        raise ValueError("The M2-E02 coverage receipt or scanner differs from its recorded scope.")
    scan = runpy.run_path(str(scanner))["scan"]
    daily = []
    for day in DAYS:
        archive = LOCAL / f"BTCUSDT-1m-{day.isoformat()}.zip"
        bars, digest = import_day(archive, archive.with_suffix(".zip.CHECKSUM"), day)
        daily.append(
            {
                "development_day_utc": day.isoformat(),
                "archive_sha256": digest,
                "dataset_id": bars.fingerprint,
                "blocks": scan(bars.values[:, 4]),
            }
        )
    daily.append(previous_day)
    dates = covering_dates(daily)
    print(json.dumps({
        "daily": daily,
        "covering_dates_by_time_band": dates,
        "decision": "PROPOSE_OUTCOME_EXERCISE" if dates else "DEFER",
        "holdout_reads": 0,
        "forward_returns_evaluated": 0,
    }))


def phase(mode, deadline):
    command = [sys.executable, "-B", (LOCAL / "run_coverage.py").as_posix(), mode]
    start = perf_counter()
    try:
        result = subprocess.run(command, timeout=deadline, capture_output=True, check=False)
    except subprocess.TimeoutExpired as error:
        return {
            "status": "TIMED_OUT",
            "exit_code": None,
            "wall_seconds": round(perf_counter() - start, 3),
            "deadline_seconds": deadline,
            "stdout": (error.stdout or b"").decode("utf-8", errors="replace"),
            "stderr": (error.stderr or b"").decode("utf-8", errors="replace"),
        }
    return {
        "status": "COMPLETED" if result.returncode == 0 else "FAILED",
        "exit_code": result.returncode,
        "wall_seconds": round(perf_counter() - start, 3),
        "deadline_seconds": deadline,
        "stdout": result.stdout.decode("utf-8", errors="replace"),
        "stderr": result.stderr.decode("utf-8", errors="replace"),
    }


def main():
    with (LOCAL / "coverage.json").open("x", encoding="utf-8") as output:
        acquisition = phase("acquire", 60)
        coverage = phase("count", 30) if acquisition["exit_code"] == 0 else None
        record = {
            "variant_id": "M2-E03",
            "attempt": 1,
            "recorded_at_utc": datetime.now(UTC).isoformat(),
            "command": [".venv/Scripts/python.exe", "-B", (LOCAL / "run_coverage.py").as_posix()],
            "python": sys.version.split()[0],
            "script_sha256": sha256((LOCAL / "run_coverage.py").read_bytes()).hexdigest(),
            "acquisition": acquisition,
            "count": coverage,
        }
        completed = coverage is not None and coverage["exit_code"] == 0
        if completed:
            record["coverage"] = json.loads(coverage.pop("stdout"))
        json.dump(record, output, indent=2)
        output.write("\n")
    print(json.dumps(record, indent=2))
    return 0 if completed else 1


if __name__ == "__main__":
    if sys.argv[1:] == ["acquire"]:
        acquire()
    elif sys.argv[1:] == ["count"]:
        count()
    elif not sys.argv[1:]:
        raise SystemExit(main())
    else:
        raise SystemExit("Expected no arguments, acquire, or count.")
