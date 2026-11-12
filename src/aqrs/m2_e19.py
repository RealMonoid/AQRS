"""Coverage-first comparison of volatility gates on the M2-E18 rule."""

import argparse
import sys
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path
from time import monotonic
from uuid import uuid4

import numpy as np

from aqrs import journal
from aqrs.config import load
from aqrs.discovery import HORIZON, ROWS, folds_for_window, volume_inputs
from aqrs.governor import supervise
from aqrs.m2_e14 import (
    D01_PATH,
    E17_PATH,
    E18,
    d01_archive_rows,
    e17_training_id,
    read_json,
    read_window,
    verify_training_prefix,
)
from aqrs.market import features, validate
from aqrs.platform_guard import capability
from aqrs.provenance import snapshot
from aqrs.storage import fingerprint, write_json
from aqrs.worker import reserve_fit
from aqrs.worker import run as run_worker

ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = "M2-E19"
COVERAGE = "VOL_REGIME_COVERAGE_E19_V1"
QUANTILE = 0.75
MIN_DAYS = 2
MIN_ENTRIES = 4
DATASET_ID = "f24e81c97227b0932978a240ae20411f6ffea7242bed11294c43b16ce9904568"


def cutoff(values, request, directory):
    if not len(values) or not np.isfinite(values).all():
        raise ValueError("Invalid training sample for cutoff calibration.")
    reserve_fit(request, directory, 2)
    value = float(np.quantile(values, QUANTILE, method="linear"))
    completed = directory / "fits.json"
    write_json(completed, 1 + (read_json(completed) if completed.exists() else 0))
    return value


def coverage_days(bars, signals, passed, validation):
    days = {}
    for index in range(validation.start, validation.stop, 1440):
        days[bars.time(index)[:10]] = {"accepted": 0, "rejected": 0}
    free_at = 0
    for signal, accepted in zip(signals, passed, strict=True):
        entry = int(signal) + 1
        if entry >= free_at:
            days[bars.time(entry)[:10]]["accepted" if accepted else "rejected"] += 1
            free_at = entry + HORIZON
    return days


def coverage(bars, request, directory):
    positive, _ = volume_inputs(bars)
    volatility = features(bars)[:, 2]
    folds = []
    for train, validation in folds_for_window():
        threshold = cutoff(volatility[train][positive[train]], request, directory)
        signals = np.flatnonzero(positive[validation]) + validation.start
        passed = volatility[signals] >= threshold
        days = coverage_days(bars, signals, passed, validation)
        qualified = sum(min(counts.values()) >= MIN_ENTRIES for counts in days.values())
        folds.append(
            {
                "cutoff": threshold,
                "eligible": len(signals),
                "days": days,
                "qualified_days": qualified,
            }
        )
    return {
        "folds": folds,
        "passes": all(fold["qualified_days"] >= MIN_DAYS for fold in folds),
        "estimator_fits": 0,
    }


def load_bars(request, directory):
    bars = read_window(
        Path(request["archives"]), request["allowlist"], scratch=directory, campaign=E18
    )
    validate(bars)
    if len(bars.values) != ROWS or bars.fingerprint != DATASET_ID:
        raise ValueError("The input does not match the complete M2-E18 dataset.")
    verify_training_prefix(bars, request["training_id"])
    return bars


def worker(request, directory):
    if request["stage"] != "coverage":
        raise ValueError("Unknown pilot stage.")
    return coverage(load_bars(request, directory), request, directory)


def run_coverage(archives, output):
    config, _ = load(ROOT / "configs/research.yaml")
    limits = config["resource_governor"]
    memory_mode = limits["memory_mode"]
    issue = capability(memory_mode)
    if issue:
        raise ValueError(issue)
    if (
        limits["max_model_fits_per_campaign"] < 2
        or limits["max_wall_seconds_per_trial"] < 30
        or limits["max_wall_seconds_per_campaign"] < 30
        or limits["max_peak_rss_mb_per_trial"] < 512
    ):
        raise ValueError("The coverage plan exceeds the effective limits.")
    allowlist = d01_archive_rows(read_json(ROOT / D01_PATH))
    training_id = e17_training_id(read_json(ROOT / E17_PATH), allowlist)
    request = {
        "stage": "coverage",
        "archives": str(archives.resolve()),
        "allowlist": allowlist,
        "training_id": training_id,
        "fit_limit": 2,
    }
    plan = {
        "candidate_id": COVERAGE,
        "dataset_id": DATASET_ID,
        "training_id": training_id,
        "input_archives": allowlist,
        "planned_trials": 1,
        "estimator_fits": 0,
        "calibrations": 2,
        "max_wall_seconds": 30,
        "max_rss_mib": 512,
        "memory_mode": memory_mode,
        "min_days_per_fold": MIN_DAYS,
        "min_entries_per_arm_per_day": MIN_ENTRIES,
        "quantile": QUANTILE,
    }
    output.mkdir(parents=True, exist_ok=False)
    source = snapshot(output, Path(__file__), (ROOT / "configs/research.yaml",))
    run_id = uuid4().hex
    stamp = datetime.now(UTC).isoformat()
    config["research"]["candidates"] = [{"id": COVERAGE}]
    with closing(journal.connect(output / "research.sqlite3")) as db:
        journal.begin(db, run_id, fingerprint(plan), config, plan)
        meta = {
            "evidence_key": fingerprint(plan),
            "source_id": source["source_id"],
            "dataset_id": DATASET_ID,
        }
        journal.start_experiment(db, run_id, COVERAGE, meta)
        outcome = supervise(
            output,
            request,
            30,
            monotonic() + 30,
            512,
            command=[sys.executable, "-B", "-m", "aqrs.m2_e19", "--worker"],
        )
        result = outcome.get("result", {})
        verdict = (
            ("QUALIFIED" if result["passes"] else "DEFER")
            if outcome["execution_status"] == "COMPLETED"
            else "NOT_EVALUATED"
        )
        report = {
            "work_item": CAMPAIGN,
            "run_id": run_id,
            "timestamp_utc": stamp,
            "plan": plan,
            "source": source,
            "outcome": outcome,
            "decision": verdict,
        }
        journal.finish_experiment(
            db,
            run_id,
            {
                "candidate_id": COVERAGE,
                "experiment_id": f"{run_id}:{COVERAGE}",
                "execution_status": outcome["execution_status"],
                "evidence_status": "INSUFFICIENT_EVIDENCE"
                if result
                else "NOT_EVALUATED",
                "metrics": result,
            },
            meta,
        )
        journal.finish_campaign(db, run_id, outcome["execution_status"], plan)
    write_json(output / "coverage.json", report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--archives", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.worker:
        run_worker(args.worker, worker)
        return 0
    if args.archives is None or args.output is None:
        parser.error("--archives and --output are required.")
    report = run_coverage(args.archives, args.output)
    print(f"{CAMPAIGN} coverage: {report['decision']}")
    return int(report["decision"] == "NOT_EVALUATED")


if __name__ == "__main__":
    raise SystemExit(main())
