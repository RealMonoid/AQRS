"""Verify the M1-E06 reports and journals without rerunning the campaigns."""

import hashlib
import json
import math
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOLERANCE = 1e-10
ARCHIVE_SHA256 = "a29b45bdb88d5090cfecc61423dab084364a34db96b0788ab77cefc9d4b9567d"
DATASET_ID = "7ec539e452f4efc7063947409a905f9c3e975b06ddf2585d252cb1ef72457893"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def compare(left, right, key):
    if isinstance(left, dict):
        assert isinstance(right, dict) and left.keys() == right.keys(), key
        for name in left:
            compare(left[name], right[name], f"{key}.{name}")
    elif isinstance(left, list):
        assert isinstance(right, list) and len(left) == len(right), key
        for index, (first, second) in enumerate(zip(left, right, strict=True)):
            compare(first, second, f"{key}[{index}]")
    elif isinstance(left, float):
        assert isinstance(right, (int, float)), key
        assert math.isclose(left, right, rel_tol=0, abs_tol=TOLERANCE), key
    else:
        assert type(left) is type(right) and left == right, key


def verify_platform(root, worker_mode):
    [report_path] = root.glob("*/report.json")
    report = read(report_path)
    plan = report["plan"]
    [trial] = report["trials"]
    metrics = trial["metrics"]
    manifest = read(report_path.parent / "data_manifest.json")
    assert manifest == report["data_manifest"]
    assert manifest["archive_sha256"] == ARCHIVE_SHA256
    assert report["dataset_fingerprint"] == manifest["dataset_id"] == DATASET_ID
    assert manifest["bar_count"] == 1440
    assert report["holdout"] == manifest["holdout"] == plan["holdout"]
    assert report["holdout"]["start_at"] == "2026-01-06T00:00:00+00:00"
    assert report["holdout"]["end_at"] == "2026-01-07T00:00:00+00:00"
    assert report["holdout"]["authorized_reads"] == 0 and not report["holdout"]["evaluated"]
    assert report["configuration"]["research"]["horizon_bars"] == 30
    assert plan["preflight_status"] == "ADMITTED" and plan["source_data_validated"]
    assert plan["planned_trials"] == plan["started_trials"] == 1
    assert plan["planned_fits"] == plan["completed_fits"] == 3
    assert plan["planned_pilot_fits"] == 1 and trial["completed_fits"] == 2
    assert plan["process_tree_mode"] == worker_mode
    assert plan["runtime_wall_seconds"] <= 300 and trial["runtime_wall_seconds"] <= 120
    assert plan["peak_rss_mb"] <= 4096 and plan["stop_reason"] is None and plan["auto_retry_count"] == 0
    assert report["execution_status"] == trial["execution_status"] == "COMPLETED"
    assert trial["evidence_status"] == "INSUFFICIENT_EVIDENCE"
    assert metrics["feasibility"]["status"] == "PASSED"
    assert [
        (fold["train_start"], fold["train_stop_exclusive"], fold["val_start"], fold["val_stop_exclusive"])
        for fold in metrics["folds"]
    ] == [(12, 689, 720, 1049), (12, 1049, 1080, 1409)]
    assert metrics["prediction"]["observations"] == 658
    assert set(metrics["trading"]) == {"candidate", "momentum", "no_trade"}
    for policy in metrics["trading"].values():
        assert policy["observations"] == 658 and policy["decisions"]["short"] == 0
        assert policy["trade_count"] == len(policy["trades"])
        for trade in policy["trades"]:
            assert trade["decision"] == "long"
            assert trade["entry_index"] == trade["signal_index"] + 1
            assert trade["exit_index"] == trade["entry_index"] + 30
            assert trade["exit_index"] < (1080 if trade["signal_index"] < 1080 else 1440)
            compare(trade["fees"], 0.002, "fees")
            compare(trade["spread"], 0.0001, "spread")
            compare(trade["slippage"], 0.0004, "slippage")
            compare(trade["gross_pnl"] - trade["net_pnl"], 0.0025, "round-trip cost")
    assert metrics["trading"]["no_trade"]["trades"] == []
    assert (report_path.parent / "report.md").is_file()
    assert read(report_path.parent / "plan.json") == plan
    timings = report["stage_wall_seconds"] | metrics["stage_wall_seconds"]
    assert set(timings) == {"import", "features", "simulation"}
    assert all(isinstance(value, float) and value >= 0 for value in timings.values())
    with sqlite3.connect((root / "research.sqlite3").resolve().as_uri() + "?mode=ro", uri=True) as db:
        assert db.execute("PRAGMA integrity_check").fetchall() == [("ok",)]
        assert db.execute("SELECT run_id,execution_status,evidence_status FROM experiments").fetchall() == [
            (report["run_id"], "COMPLETED", "INSUFFICIENT_EVIDENCE")
        ]
    return report, {
        "run_id": report["run_id"],
        "platform": plan["platform"],
        "python": plan["python"],
        "guard": plan["process_tree_mode"],
        "estimated_wall_seconds": plan["estimated_wall_seconds"],
        "wall_seconds": plan["runtime_wall_seconds"],
        "sampled_peak_rss_mib": plan["peak_rss_mb"],
        "stages_wall_seconds": timings,
        "completed_fits": plan["completed_fits"],
        "dataset_csv_sha256": hashlib.sha256((report_path.parent / "dataset.csv").read_bytes()).hexdigest(),
        "journal_integrity": "ok",
    }


def main():
    windows, left = verify_platform(ROOT, "Windows Job Object")
    ubuntu, right = verify_platform(ROOT / "ubuntu", "POSIX process group")
    for key in (
        "configuration", "config_fingerprint", "source_fingerprint", "dependencies",
        "holdout", "research_intervals", "data_manifest",
    ):
        assert windows[key] == ubuntu[key], key
    assert left["dataset_csv_sha256"] == right["dataset_csv_sha256"]
    windows_metrics, ubuntu_metrics = (
        {key: value for key, value in report["trials"][0]["metrics"].items() if key != "stage_wall_seconds"}
        for report in (windows, ubuntu)
    )
    compare(windows_metrics, ubuntu_metrics, "metrics")
    result = {
        "status": "MATCHED",
        "scope": "Technical reproduction on reused development data",
        "metric_absolute_tolerance": TOLERANCE,
        "lineage": read(ROOT / "lineage.json"),
        "configuration_fingerprint": windows["config_fingerprint"],
        "source_fingerprint": windows["source_fingerprint"],
        "dataset_fingerprint": windows["dataset_fingerprint"],
        "holdout": windows["holdout"],
        "feasibility": windows_metrics["feasibility"],
        "prediction": windows_metrics["prediction"],
        "trading": {
            name: {key: policy[key] for key in ("trade_count", "gross_pnl", "net_pnl")}
            for name, policy in windows_metrics["trading"].items()
        },
        "windows": left,
        "ubuntu": right,
    }
    text = json.dumps(result, indent=2) + "\n"
    (ROOT / "verification.json").write_text(text, encoding="utf-8", newline="\n")
    archived_bytes = sum(path.stat().st_size for path in ROOT.rglob("*") if path.is_file())
    assert archived_bytes <= 2 * 1024**2
    print(text, end="")
    print(f"Archived bytes: {archived_bytes}")


if __name__ == "__main__":
    main()
