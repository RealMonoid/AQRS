"""Extend the fixed price-drop coverage count to seven approved development days."""

import json
import runpy
import sys
from datetime import UTC, date, datetime
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import aqrs.binance_spot_pilot as importer

LOCAL = Path("artifacts/m2-e12")
RUNNER = Path("artifacts/m2-e03/run_coverage.py")
SCANNER = Path("artifacts/m2-e02/count_pairs.py")
PRIOR_RECEIPT = Path("artifacts/m2-e03/coverage.json")
PINNED = {
    RUNNER: "84bbc524a3942f4edf52e3622e16cd506be92e5cfe828a4111d43105e60e2184",
    SCANNER: "7dbd34edb8bb4c71ea012541dc64a7f1c2a657eef56a420f34739ebce608bd9f",
    PRIOR_RECEIPT: "fd77d9a94e776aad03c63cee6194bedf5ba24ce0da4c995441f235984ddf0c8a",
}
DAYS = tuple(date(2025, 12, day) for day in range(25, 32))
ACQUISITION_SECONDS = 120
COUNT_SECONDS = 30


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def scoped_runner():
    for path, expected in PINNED.items():
        if digest(path) != expected:
            raise ValueError(
                f"Archived evidence differs from its recorded digest: {path}"
            )
    spec = spec_from_file_location("m2_e03_coverage", RUNNER)
    runner = module_from_spec(spec)
    spec.loader.exec_module(runner)
    runner.LOCAL = LOCAL
    runner.DAYS = DAYS
    runner.FILES = {}
    for day in DAYS:
        name = f"BTCUSDT-1m-{day.isoformat()}.zip"
        url = f"{importer.ARCHIVE_BASE}/{name}"
        runner.FILES[url] = (name, importer.INPUT_LIMIT)
        runner.FILES[f"{url}.CHECKSUM"] = (f"{name}.CHECKSUM", 4096)
    return runner


def prior_days():
    receipt = json.loads(PRIOR_RECEIPT.read_text(encoding="utf-8"))
    coverage = receipt["coverage"]
    days = coverage["daily"]
    if (
        receipt["variant_id"] != "M2-E03"
        or receipt["count"]["exit_code"] != 0
        or coverage["holdout_reads"] != 0
        or coverage["forward_returns_evaluated"] != 0
        or [row["development_day_utc"] for row in days]
        != [f"2026-01-0{day}" for day in range(1, 6)]
    ):
        raise ValueError(
            "Expected exactly the five prior count-only development records."
        )
    return days


def count(runner):
    previous = prior_days()
    scan = runpy.run_path(str(SCANNER))["scan"]
    new = []
    for day in DAYS:
        archive = LOCAL / f"BTCUSDT-1m-{day.isoformat()}.zip"
        bars, archive_digest = importer.import_day(
            archive, archive.with_suffix(".zip.CHECKSUM"), day
        )
        new.append(
            {
                "development_day_utc": day.isoformat(),
                "archive_sha256": archive_digest,
                "dataset_id": bars.fingerprint,
                "bar_count": len(bars.values),
                "blocks": scan(bars.values[:, 4]),
            }
        )
    dates = runner.covering_dates(new + previous)
    print(
        json.dumps(
            {
                "daily": new,
                "reused_dates": [row["development_day_utc"] for row in previous],
                "covering_dates_by_time_band": dates,
                "decision": "PROPOSE_OUTCOME_EXERCISE" if dates else "DEFER",
                "holdout_reads": 0,
                "forward_returns_evaluated": 0,
                "model_fits": 0,
            }
        )
    )


def main(runner):
    script = LOCAL / "run_coverage.py"
    with (LOCAL / "coverage.json").open("x", encoding="utf-8") as output:
        acquisition = runner.phase("acquire", ACQUISITION_SECONDS)
        scan = (
            runner.phase("count", COUNT_SECONDS)
            if acquisition["exit_code"] == 0
            else None
        )
        completed = scan is not None and scan["exit_code"] == 0
        record = {
            "variant_id": "M2-E12",
            "attempt": 1,
            "recorded_at_utc": datetime.now(UTC).isoformat(),
            "command": [".venv/Scripts/python.exe", "-B", script.as_posix()],
            "python": sys.version.split()[0],
            "file_allowlist": list(runner.FILES),
            "source_sha256": {
                **{path.as_posix(): expected for path, expected in PINNED.items()},
                script.as_posix(): digest(script),
                "src/aqrs/binance_spot_pilot.py": digest(Path(importer.__file__)),
            },
            "acquisition": acquisition,
            "count": scan,
        }
        if completed:
            record["coverage"] = json.loads(scan.pop("stdout"))
        json.dump(record, output, indent=2)
        output.write("\n")
    print(json.dumps(record, indent=2))
    return 0 if completed else 1


if __name__ == "__main__":
    mode = sys.argv[1:]
    runner = scoped_runner()
    prior_days()
    if mode == ["acquire"]:
        runner.acquire()
    elif mode == ["count"]:
        count(runner)
    elif not mode:
        raise SystemExit(main(runner))
    else:
        raise SystemExit("Expected no arguments, acquire, or count.")
