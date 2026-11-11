"""Run the frozen M2-E08 comparison on the four approved development archives."""

import platform
import sys
from contextlib import closing
from datetime import date
from pathlib import Path
from time import monotonic
from uuid import uuid4

from aqrs import journal
from aqrs.governor import supervise
from aqrs.platform_guard import capability
from aqrs.storage import fingerprint, write_json
from aqrs.worker import run as run_worker

DAYS = tuple(date(2026, 1, day) for day in (1, 2, 3, 4))
DIGESTS = (
    "5065b4a0412fcf952a1384a140217e3ec4f0497edc5528289f198589d0736a17",
    "7ad5ae21dafe8c77150676144a9537bf975c660cfd7048114fb5300750f328fa",
    "ed939ed8dec11c5465ea0a8289255b7b1b70c72f55452ee6c6d8540b07662d8b",
    "2e7d3ed70432fc17187325ae5b8c5c7066cb5d8c9283c54f1514f109a1b06906",
)
MODELS = ("ridge", "lightgbm")
PARAMETERS = {
    "n_estimators": 32,
    "learning_rate": 0.05,
    "num_leaves": 7,
    "max_depth": 3,
    "min_child_samples": 50,
    "deterministic": True,
    "force_col_wise": True,
    "n_jobs": 1,
    "random_state": 42,
    "verbosity": -1,
}
FEATURES = ["past_return", "relative_volume", "rolling_volatility"]
COSTS = {
    "fee_bps_per_side": 10,
    "quoted_spread_bps": 1,
    "slippage_bps_per_side": 2,
    "decision_buffer_bps": 2,
}


def read_window(archive_root, days=DAYS):
    import numpy as np

    from aqrs.binance_spot_pilot import import_day
    from aqrs.market import Bars, validate

    if days != DAYS:
        raise ValueError("Input days differ from the frozen four-day allowlist.")
    daily = []
    for day, expected in zip(days, DIGESTS, strict=True):
        archive = archive_root / f"BTCUSDT-1m-{day.isoformat()}.zip"
        bars, digest = import_day(archive, archive.with_suffix(".zip.CHECKSUM"), day)
        if digest != expected:
            raise ValueError(f"Archive digest differs from M2-E03 for {day}.")
        daily.append(bars.values)
    window = Bars(np.concatenate(daily), "BTCUSDT", bar_minutes=1)
    validate(window)
    return window


def evaluate_worker(request, directory):
    from aqrs.evaluation import evaluate, model

    name = request["model"]
    if name == "ridge":
        factory = model
    elif name == "lightgbm":
        from lightgbm import LGBMRegressor, __version__

        if __version__ != "4.6.0":
            raise ValueError("Expected LightGBM 4.6.0.")

        def factory():
            return LGBMRegressor(**PARAMETERS)
    else:
        raise ValueError("Unregistered model.")
    return evaluate(request, directory, model_factory=factory)


def per_day(result):
    trades = result["trading"]["candidate"]["trades"]
    days = []
    for fold in result["folds"]:
        start, stop = fold["val_start"], fold["val_stop_exclusive"]
        selected = [row for row in trades if start <= row["signal_index"] < stop]
        days.append(
            {
                "mae": fold["prediction"]["mae"],
                "net_pnl": sum(row["net_pnl"] for row in selected),
                "trade_count": len(selected),
                "turnover": 2 * len(selected),
            }
        )
    return days


def compare(output, report, db, run_id, config):
    import numpy as np

    from aqrs.market import build_folds
    from aqrs.planning import make_plan

    started = monotonic()
    deadline = started + 300
    issue = capability("observed_rss")
    if issue:
        raise ValueError(issue)
    report["plan"] = make_plan(2, 2, 1, 5, 6, 120, 300, pilot_fits=2)
    if report["plan"]["preflight_status"] != "ADMITTED":
        raise ValueError("The frozen campaign exceeds its fit or time budget.")
    bars = read_window(Path("artifacts/m2-e03"))
    report["dataset_id"] = bars.fingerprint
    prefix = output / "development.npy"
    np.save(prefix, bars.values, allow_pickle=False)
    folds = build_folds(len(bars.values), 30, 2880, 1440, 2)
    report["folds"] = [
        {
            "train_rows": train.stop - train.start,
            "validation_rows": val.stop - val.start,
            "validation_day": bars.time(val.start)[:10],
            "last_training_exit": bars.time(train.stop + 30),
            "last_validation_exit": bars.time(val.stop + 30),
        }
        for train, val in folds
    ]
    request = {
        "prefix": str(prefix.resolve()),
        "symbol": bars.symbol,
        "bar_minutes": bars.bar_minutes,
        "horizon": 30,
        "folds": [[tr.start, tr.stop, va.start, va.stop] for tr, va in folds],
        "features": FEATURES,
        "allow_short": False,
        "notional": 1,
        "costs": COSTS,
        "real_spot": True,
    }
    command = [sys.executable, "-B", str(Path(__file__).resolve()), "--worker"]
    for model_name in MODELS:
        pilot = supervise(
            output,
            {"model": model_name, "pilot_rows": 4277, "pilot_columns": len(FEATURES)},
            30,
            deadline,
            4096,
            command=command,
        )
        report["preflight"][model_name] = pilot
        if pilot["execution_status"] != "COMPLETED" or pilot["completed_fits"] != 1:
            return "REJECTED_PREFLIGHT"
    estimates = {
        name: max(2, 2 * pilot["runtime_wall_seconds"])
        + 2 * max(1, 2 * pilot["result"]["fit_wall_seconds"])
        for name, pilot in report["preflight"].items()
    }
    report["plan"]["estimated_trial_seconds"] = estimates
    if (
        max(estimates.values()) > 120
        or sum(estimates.values()) > deadline - monotonic()
    ):
        return "REJECTED_PREFLIGHT"
    for name in MODELS:
        metadata = {"evidence_key": fingerprint([config, bars.fingerprint, name])}
        journal.start_experiment(db, run_id, name, metadata)
        outcome = supervise(
            output, request | {"model": name}, 120, deadline, 4096, command=command
        )
        status = outcome["execution_status"]
        result = outcome.get("result", {})
        if status == "COMPLETED" and result["feasibility"]["status"] == "SCREENED_OUT":
            status = "SCREENED_OUT"
        if status == "COMPLETED" and outcome["completed_fits"] != 2:
            status = "FAILED"
        report["trials"][name] = outcome | {"execution_status": status}
        journal.finish_experiment(
            db,
            run_id,
            {
                "experiment_id": f"{run_id}:{name}",
                "candidate_id": name,
                "execution_status": status,
                "evidence_status": "INSUFFICIENT_EVIDENCE"
                if status == "COMPLETED"
                else "NOT_EVALUATED",
                "metrics": outcome,
            },
            metadata,
        )
        if status != "COMPLETED":
            return status
        report["per_day"][name] = per_day(result)
    ridge, lightgbm = (report["per_day"][name] for name in MODELS)
    report["paired_deltas"] = [
        {
            "mae_improvement": a["mae"] - b["mae"],
            "net_pnl_improvement": b["net_pnl"] - a["net_pnl"],
        }
        for a, b in zip(ridge, lightgbm, strict=True)
    ]
    positive = all(
        row["mae_improvement"] > 0 and row["net_pnl_improvement"] > 0
        for row in report["paired_deltas"]
    )
    report["decision"] = (
        "CONSIDER_FOLLOW_UP"
        if positive and sum(row["net_pnl"] for row in lightgbm) > 0
        else "DEFER"
    )
    return "COMPLETED"


def main(output):
    output.mkdir(parents=True, exist_ok=False)
    config = {
        "variant": "M2-E08/1",
        "days": [day.isoformat() for day in DAYS],
        "archive_digests": list(DIGESTS),
        "lightgbm_version": "4.6.0",
        "lightgbm_parameters": PARAMETERS,
        "features": FEATURES,
        "horizon": 30,
        "costs": COSTS,
        "seed": 42,
        "research": {"candidates": [{"id": name} for name in MODELS]},
    }
    run_id = uuid4().hex
    report = {
        "run_id": run_id,
        "configuration": config,
        "config_id": fingerprint(config),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "holdout": {"start_at": "2026-01-06T00:00:00Z", "reads": 0},
        "preflight": {},
        "trials": {},
        "per_day": {},
    }
    with closing(journal.connect(output / "research.sqlite3")) as db:
        journal.begin(db, run_id, report["config_id"], config, report["holdout"])
        try:
            status = compare(output, report, db, run_id, config)
        except (OSError, ValueError) as error:
            report["stop_reason"] = str(error)
            status = "REJECTED_PREFLIGHT" if not report["trials"] else "FAILED"
        report["execution_status"] = status
        with db:
            db.execute(
                "UPDATE experiments SET execution_status = 'CANCELLED' "
                "WHERE run_id = ? AND execution_status = 'PROPOSED'",
                (run_id,),
            )
        journal.finish_campaign(db, run_id, status, report)
        report["journal_integrity"] = db.execute("PRAGMA integrity_check").fetchone()[0]
        write_json(output / "report.json", report)
    print(f"{status} {run_id} {output}")
    return 0 if status == "COMPLETED" and report["journal_integrity"] == "ok" else 2


if __name__ == "__main__":
    if sys.argv[1] == "--worker":
        run_worker(Path(sys.argv[2]), evaluate_worker)
    else:
        raise SystemExit(main(Path(sys.argv[1])))
