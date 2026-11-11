"""Check the frozen M2-E09 platform replays without starting a fit."""

import json
import sqlite3
from contextlib import closing
from hashlib import sha256
from math import isclose
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOLERANCE = 1e-8


def compare(left, right, key):
    if isinstance(left, dict) and isinstance(right, dict):
        assert left.keys() == right.keys(), key
        for field in left:
            compare(left[field], right[field], f"{key}.{field}")
    elif isinstance(left, list) and isinstance(right, list):
        assert len(left) == len(right), key
        for index, (a, b) in enumerate(zip(left, right, strict=True)):
            compare(a, b, f"{key}[{index}]")
    elif isinstance(left, float) or isinstance(right, float):
        assert isclose(left, right, rel_tol=0, abs_tol=TOLERANCE), (key, left, right)
    else:
        assert left == right, (key, left, right)


def inspect(platform):
    folder = ROOT / platform
    report = json.loads((folder / "report.json").read_text(encoding="utf-8"))
    assert report["execution_status"] == "COMPLETED"
    assert report["journal_integrity"] == "ok"
    assert report["holdout"] == {"start_at": "2026-01-06T00:00:00Z", "reads": 0}
    assert report["configuration"]["days"] == [
        "2026-01-01",
        "2026-01-02",
        "2026-01-03",
        "2026-01-04",
    ]
    assert report["plan"]["planned_fits"] == 6
    assert [row["completed_fits"] for row in report["preflight"].values()] == [1, 1]
    assert [row["completed_fits"] for row in report["trials"].values()] == [2, 2]
    assert [fold["validation_rows"] for fold in report["folds"]] == [1409, 1409]
    database = (folder / "research.sqlite3").as_uri() + "?mode=ro"
    with closing(sqlite3.connect(database, uri=True)) as db:
        assert db.execute("PRAGMA integrity_check").fetchone() == ("ok",)
        assert db.execute(
            "SELECT run_id, execution_status FROM campaigns"
        ).fetchall() == [(report["run_id"], "COMPLETED")]
        journal = db.execute(
            "SELECT candidate_id, execution_status, evidence_status, evidence_key "
            "FROM experiments ORDER BY candidate_id"
        ).fetchall()
    assert [row[:3] for row in journal] == [
        ("lightgbm", "COMPLETED", "INSUFFICIENT_EVIDENCE"),
        ("ridge", "COMPLETED", "INSUFFICIENT_EVIDENCE"),
    ]
    data_sha = sha256((folder / "development.npy").read_bytes()).hexdigest()
    return report, journal, data_sha


def main():
    windows, windows_journal, windows_sha = inspect("windows")
    ubuntu, ubuntu_journal, ubuntu_sha = inspect("ubuntu")
    assert windows_sha == ubuntu_sha
    assert windows_journal == ubuntu_journal
    for key in ("config_id", "dataset_id", "configuration", "folds", "decision"):
        assert windows[key] == ubuntu[key], key
    for model in ("ridge", "lightgbm"):
        baseline = windows["trials"][model]["result"]
        replay = ubuntu["trials"][model]["result"]
        compare(
            {
                key: value
                for key, value in baseline.items()
                if key != "stage_wall_seconds"
            },
            {
                key: value
                for key, value in replay.items()
                if key != "stage_wall_seconds"
            },
            model,
        )
    compare(windows["per_day"], ubuntu["per_day"], "per_day")
    compare(windows["paired_deltas"], ubuntu["paired_deltas"], "paired_deltas")
    result = {
        "status": "MATCHED",
        "absolute_tolerance": TOLERANCE,
        "dataset_bytes_sha256": windows_sha,
        "dataset_id": windows["dataset_id"],
        "config_id": windows["config_id"],
        "windows_run_id": windows["run_id"],
        "ubuntu_run_id": ubuntu["run_id"],
        "decision": windows["decision"],
        "per_day": windows["per_day"],
        "holdout_reads": 0,
        "fits_per_platform": 6,
    }
    (ROOT / "comparison.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
