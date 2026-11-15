"""Run the one authorized state-persistence coverage count without outcomes."""

import argparse
import json
import sys
from contextlib import closing
from datetime import date
from hashlib import sha256
from pathlib import Path
from time import monotonic

import numpy as np

from aqrs import journal, worker
from aqrs.binance_spot_pilot import IMPORT_ERRORS, INPUT_LIMIT, load_spot_day
from aqrs.config import load, validate_governor
from aqrs.governor import supervise
from aqrs.market import Bars, build_folds, validate
from aqrs.platform_guard import capability
from aqrs.provenance import snapshot
from aqrs.storage import fingerprint, write_json
from aqrs.study_admission import unqualified_entry

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs/research.yaml"
D01 = ROOT / "evidence/aqrs-d01-verification.json"
EXPOSURE = ROOT / "evidence/exposure.json"
INPUT = ROOT / "artifacts/aqrs-d01/data/archives"
OUTPUT = ROOT / "artifacts/m2-e15/count-v1"
VARIANT = "M2-E15-COUNT-V1"
DAYS = tuple(f"2025-12-{i:02}" for i in range(1, 11))
ARCHIVE_SCOPE_ID = "29eeb399fc8c6924b6e060a2ffc1b0034dd6c8a008e55104e761272e9ed3f078"
DATASET_ID = "f24e81c97227b0932978a240ae20411f6ffea7242bed11294c43b16ce9904568"
SYMBOL = "BTCUSDT"
DAY = 1_440
ROWS = 10 * DAY
HORIZON = 30
BASELINE_AGE, PERSISTENT_AGE = 5, 30




def registration():
    return {
        "work_item": "M2-E15",
        "variant_id": VARIANT,
        "kind": "count_only",
        "status": "registered",
        "input_scope_id": ARCHIVE_SCOPE_ID,
        "dataset_id": DATASET_ID,
        "forward_outcomes": False,
        "entry_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def require_registration():
    expected = registration()
    entries = json.loads(EXPOSURE.read_text(encoding="utf-8"))["manual_screens"]
    (observed,) = [
        item for item in entries if item["work_item"] == expected["work_item"]
    ]
    if any(observed.get(key) != value for key, value in expected.items()):
        raise ValueError(
            "A prospective exposure record must bind the count and entry bytes."
        )
    return observed


def archive_scope(receipt):
    (manifest,) = [
        row["result"]["manifest"]
        for row in receipt["acquisition"]["workers"]
        if row["result"]["manifest"]["symbol"] == SYMBOL
    ]
    if manifest["qualified"] is not True or manifest["bar_minutes"] != 1:
        raise ValueError("The D01 BTCUSDT scope is not qualified.")
    archives = [
        {key: item[key] for key in ("name", "day", "sha256", "checksum_sha256")}
        for item in manifest["archives"]
        if item["day"] in DAYS
    ]
    if fingerprint(archives) != ARCHIVE_SCOPE_ID:
        raise ValueError("The D01 archive scope differs from the registered scope.")
    return archives


def build_plan(limits):
    limits = dict(limits)
    validate_governor(limits)
    worker_seconds = min(20, limits["max_wall_seconds_per_trial"])
    campaign_seconds = min(300, limits["max_wall_seconds_per_campaign"])
    max_rss_mb = min(512, limits["max_peak_rss_mb_per_trial"])
    reasons = []
    if issue := capability(limits["memory_mode"]):
        reasons.append(issue)
    if worker_seconds < 20 or campaign_seconds < 20 or max_rss_mb < 512:
        reasons.append("The bounded 20-second and 512 MiB allowance does not fit.")
    return {
        "preflight_status": "REJECTED_PREFLIGHT" if reasons else "ADMITTED",
        "rejection_reasons": reasons,
        "estimate_method": "Conservative fixed allowance for ten offline archives and one scan.",
        "estimated_wall_seconds": 20,
        "estimated_memory_mb": 512,
        "worker_seconds": worker_seconds,
        "campaign_seconds": campaign_seconds,
        "max_rss_mb": max_rss_mb,
        "memory_mode": limits["memory_mode"],
        "planned_workers": 1,
        "planned_trials": 0,
        "planned_fits": 0,
        "planned_seeds": 0,
        "planned_folds": 2,
        "auto_retry_count": 0,
        "archive_count": len(DAYS),
        "bar_count": ROWS,
        "limits_id": fingerprint(limits),
    }


def read_day(root, row, scratch):
    archive_name = row["name"]
    for name, maximum, digest_field in (
        (archive_name, INPUT_LIMIT, "sha256"),
        (archive_name + ".CHECKSUM", 4096, "checksum_sha256"),
    ):
        path = root / name
        if path.resolve() != path or path.is_symlink() or not path.is_file():
            raise ValueError("Expected a regular file at the admitted archive path.")
        with path.open("rb") as source:
            content = source.read(maximum + 1)
        if len(content) > maximum or sha256(content).hexdigest() != row[digest_field]:
            raise ValueError(
                "D01 archive or sidecar digest differs from the registration."
            )
        (scratch / name).write_bytes(content)
    return load_spot_day(
        scratch / archive_name,
        scratch / (archive_name + ".CHECKSUM"),
        date.fromisoformat(row["day"]),
        symbol=SYMBOL,
    ).bars.values


def episodes(closes, lows, validation):
    """Yield common setup/trigger indices, resetting state at the fold boundary."""
    setup = None
    cooled = False
    for index in range(validation.start, validation.stop):
        positive = closes[index] > closes[index - BASELINE_AGE]
        if setup is not None:
            age = index - setup
            if age > PERSISTENT_AGE or lows[index] <= closes[setup - BASELINE_AGE]:
                setup = None
            elif cooled and closes[index] > closes[index - 1]:
                yield setup, index
                setup = None
            elif not positive:
                cooled = True
        if (
            setup is None
            and positive
            and closes[index - 1] <= closes[index - BASELINE_AGE - 1]
        ):
            setup = index
            cooled = False


def coverage_pass(bands, days, fold_bands):
    return bands >= 12 and days >= 4 and min(fold_bands) >= 4


def summarize(bars):
    folds, disagreements = [], []
    bands = set()
    for number, (_, validation) in enumerate(
        build_folds(ROWS, HORIZON, 4 * DAY, 3 * DAY, 2), 1
    ):
        fold_bands = set()
        shared = persistent_only = 0
        for setup, trigger in episodes(
            bars.values[:, 4], bars.values[:, 3], validation
        ):
            age = trigger - setup
            if age <= BASELINE_AGE:
                shared += 1
                continue
            persistent_only += 1
            available = bars.time(trigger, close=True)
            band = (available[:10], int(available[11:13]) // 8)
            fold_bands.add(band)
            disagreements.append(
                {
                    "fold": number,
                    "setup_index": setup,
                    "signal_index": trigger,
                    "available_at": available,
                    "age_minutes": age,
                    "utc_band": band[1],
                }
            )
        bands.update(fold_bands)
        folds.append(
            {
                "fold": number,
                "eligible_signals": [validation.start, validation.stop],
                "rolling_signals": shared,
                "persistent_signals": shared + persistent_only,
                "credited_bands": len(fold_bands),
            }
        )
    days = len({day for day, _ in bands})
    return {
        "folds": folds,
        "disagreements": disagreements,
        "credited_bands": len(bands),
        "credited_days": days,
        "coverage_pass": coverage_pass(
            len(bands), days, [f["credited_bands"] for f in folds]
        ),
    }


@unqualified_entry("scripts.m2_e15_count.count_worker")
def count_worker(request, directory):
    try:
        archives = archive_scope(json.loads(D01.read_text(encoding="utf-8")))
        if request["archives"] != archives or INPUT.resolve() != INPUT:
            raise ValueError("Worker request differs from the registered D01 scope.")
        scratch = directory / "inputs"
        scratch.mkdir()
        bars = Bars(
            np.concatenate([read_day(INPUT, row, scratch) for row in archives]),
            SYMBOL,
            1,
        )
        validate(bars)
        if len(bars.values) != ROWS or bars.fingerprint != DATASET_ID:
            raise ValueError("Dataset identity differs from the registered E18 window.")
        return {
            "input_status": "VALID",
            "dataset_id": bars.fingerprint,
            **summarize(bars),
        }
    except (*IMPORT_ERRORS, KeyError, TypeError) as error:
        return {"input_status": "REJECTED", "input_error": str(error)}


@unqualified_entry("scripts.m2_e15_count.execute")
def execute(plan, archives, registered):
    started = monotonic()
    OUTPUT.mkdir(parents=True, exist_ok=False)
    definition = {
        "research": {"candidates": [{"id": VARIANT}]},
        "days": DAYS,
        "symbol": SYMBOL,
        "horizon": HORIZON,
        "ages": [BASELINE_AGE, PERSISTENT_AGE],
        "input_archives": archives,
        "coverage": {"bands": 12, "days": 4, "bands_per_fold": 4},
        "forward_outcomes": False,
        "independent_confirmation": False,
    }
    run_id = VARIANT.lower()
    report = {
        "run_id": run_id,
        "config_id": fingerprint(definition),
        "configuration": definition,
        "plan": plan,
        "started_at": journal.now(),
        "registration": registered,
        "provenance": snapshot(OUTPUT, Path(__file__), (CONFIG, D01, EXPOSURE)),
    }
    metadata = {"evidence_key": fingerprint([definition, DATASET_ID])}
    with closing(journal.connect(OUTPUT / "research.sqlite3")) as db:
        journal.begin(db, run_id, report["config_id"], definition, report)
        journal.start_experiment(db, run_id, VARIANT, metadata)
        deadline = started + plan["campaign_seconds"]
        if deadline - monotonic() < plan["worker_seconds"]:
            outcome = {
                "execution_status": "REJECTED_PREFLIGHT",
                "started": False,
                "stop_reason": "Insufficient remaining time for the planned worker.",
            }
        else:
            outcome = supervise(
                OUTPUT,
                {"archives": archives, "fit_limit": 0},
                plan["worker_seconds"],
                deadline,
                plan["max_rss_mb"],
                command=[
                    sys.executable,
                    "-B",
                    "-E",
                    str(Path(__file__).resolve()),
                    "--worker",
                ],
            )
        result = outcome.get("result", {})
        status = outcome["execution_status"]
        if status == "COMPLETED" and (
            result.get("input_status") != "VALID" or outcome["started_fits"]
        ):
            status = "FAILED"
        report.update(
            execution_status=status,
            worker=outcome,
            coverage_decision=("PASS" if result["coverage_pass"] else "MISS")
            if status == "COMPLETED"
            else "NOT_EVALUATED",
            journal_integrity=db.execute("PRAGMA integrity_check").fetchone()[0],
        )
        journal.finish_experiment(
            db,
            run_id,
            {
                "experiment_id": f"{run_id}:{VARIANT}",
                "candidate_id": VARIANT,
                "execution_status": status,
                "evidence_status": "NOT_EVALUATED",
                "metrics": outcome,
            },
            metadata,
        )
        journal.finish_campaign(db, run_id, status, report)
    write_json(OUTPUT / "report.json", report)
    print(f"{status}: {report['coverage_decision']}. Receipt: {OUTPUT / 'report.json'}")
    return 0 if status == "COMPLETED" else 1


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--worker":
        worker.run(Path(sys.argv[2]), count_worker)
        return 0
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("plan", "run"))
    action = parser.parse_args().action
    try:
        config, _ = load(CONFIG)
        archives = archive_scope(json.loads(D01.read_text(encoding="utf-8")))
        plan = build_plan(config["resource_governor"])
        if action == "plan" or plan["preflight_status"] != "ADMITTED":
            print(json.dumps(plan, indent=2))
            return 0 if plan["preflight_status"] == "ADMITTED" else 1
        return execute(plan, archives, require_registration())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Count stopped: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
