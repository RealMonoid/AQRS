import os
import sqlite3
from contextlib import closing
from dataclasses import replace
from datetime import date, timedelta
from importlib.metadata import version
from pathlib import Path
from time import monotonic
from uuid import uuid4

import numpy as np

from aqrs import __version__, journal
from aqrs.binance_spot_pilot import (
    IMPORT_ERRORS,
    M1_HOLDOUT_DAY,
    import_day,
    import_manifest,
    require_m1_development_day,
)
from aqrs.governor import supervise
from aqrs.market import generate, validate, write_dataset
from aqrs.planning import preflight
from aqrs.storage import fingerprint, write_json, write_text


def spot_holdout(market: dict) -> dict:
    require_m1_development_day(market["day"])
    return {
        "purpose": "final_holdout_reserved",
        "start_at": f"{M1_HOLDOUT_DAY}T00:00:00+00:00",
        "end_at": f"{M1_HOLDOUT_DAY + timedelta(days=1)}T00:00:00+00:00",
        "authorized_reads": 0,
        "evaluated": False,
    }


def run(config: dict, base: Path, *, plan_only: bool) -> tuple[dict, int]:
    started = monotonic()
    run_id = uuid4().hex
    output = base / config["project"]["artifact_dir"] / run_id
    market = config["market"]
    real_spot = market["source"] == "binance_vision_spot"
    holdout = spot_holdout(market) if real_spot else None
    output.mkdir(parents=True, exist_ok=False)
    config_hash = fingerprint(config)
    if plan_only:
        plan, _ = preflight(config, output, started)
        plan.update(
            run_id=run_id, config_fingerprint=config_hash, output_dir=str(output)
        )
        if real_spot:
            plan.update(holdout=holdout, source_data_validated=False)
        write_json(output / "plan.json", plan)
        return plan, 0 if plan["preflight_status"] == "ADMITTED" else 2

    database = base / config["journal"]["sqlite_path"]
    report = {
        "run_id": run_id,
        "dataset_type": "real" if real_spot else "synthetic",
        "config_fingerprint": config_hash,
        "configuration": config,
        "code_version": __version__,
        "source_fingerprint": fingerprint(
            {
                path.name: path.read_text(encoding="utf-8")
                for path in sorted(Path(__file__).parent.glob("*.py"))
            }
        ),
        "dependencies": {
            name: version(name) for name in ("numpy", "scikit-learn", "scipy")
        },
        "seed": config["project"]["seed"],
        "scenario": config["market"]["scenario"],
        "timeframe_minutes": config["market"]["bar_minutes"],
        "horizon_bars": config["research"]["horizon_bars"],
        "dataset_fingerprint": None,
        "execution_status": "RUNNING",
        "evaluation_status": "NOT_COMPLETED",
        "holdout": holdout,
        "trials": [],
        "journal_path": os.path.relpath(database, output)
        if database.anchor == output.anchor
        else str(database),
        "output_dir_from_journal": (
            os.path.relpath(output, database.parent)
            if database.anchor == output.anchor
            else str(output)
        ),
        "limitations": [
            "No real-world alpha has been demonstrated. This is a one-day engineering pilot."
            if real_spot
            else "No real-world alpha has been demonstrated. This is a synthetic engineering exercise.",
            "Observations and forward targets can overlap. No statistical significance is inferred.",
            "Next-bar opens and constant illustrative costs approximate fills.",
        ],
    }
    if real_spot:
        report["cost_assumption_status"] = "estimated"
    with closing(journal.connect(database)) as db:
        journal.begin(db, run_id, config_hash, config, report)
        try:
            execute(config, db, output, report, started, base=base)
            write_reports(output, report)
        except (OSError, ValueError, sqlite3.Error, KeyboardInterrupt) as error:
            status = "CANCELLED" if isinstance(error, KeyboardInterrupt) else "FAILED"
            report.update(
                execution_status=status,
                stop_reason=f"Campaign ended ({type(error).__name__}).",
            )
            with db:
                db.execute(
                    "UPDATE experiments SET execution_status = ? "
                    "WHERE run_id = ? AND execution_status IN ('PROPOSED', 'RUNNING')",
                    (status, run_id),
                )
            journal.finish_campaign(db, run_id, status, report)
            raise
        journal.finish_campaign(db, run_id, report["execution_status"], report)

    status = report["execution_status"]
    return {
        "run_id": run_id,
        "execution_status": status,
        "evaluation_status": report["evaluation_status"],
        "output_dir": str(output),
        "stop_reason": report["plan"]["stop_reason"],
    }, {"COMPLETED": 0, "REJECTED_PREFLIGHT": 2, "CANCELLED": 130}.get(status, 1)


def execute(
    config, db, output: Path, report: dict, started: float, *, base: Path
) -> None:
    run_id = report["run_id"]
    market = config["market"]
    real_spot = market["source"] == "binance_vision_spot"
    bars = None
    input_error = None
    if real_spot:
        day = date.fromisoformat(market["day"])
        archive = base / market["archive_dir"] / f"{market['symbol']}-1m-{day}.zip"
        import_started = monotonic()
        try:
            bars, digest = import_day(
                archive, archive.with_suffix(".zip.CHECKSUM"), day
            )
        except IMPORT_ERRORS as error:
            detail = type(error).__name__ if isinstance(error, OSError) else str(error)
            input_error = f"Binance archive rejected: {detail}"
        report["stage_wall_seconds"] = {"import": monotonic() - import_started}
        if bars is not None:
            manifest = import_manifest(bars, digest, day) | {
                "retrieved_on": market["retrieved_on"],
                "venue": "Binance",
                "market_type": "spot",
                "source_timestamp_unit": "microseconds",
                "session": "continuous UTC days",
                "terms_url": "https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md",
                "quality_checks_passed": [
                    "published checksum",
                    "complete ordered unique UTC minute cadence",
                    "exact source close boundary",
                    "valid OHLC and volume",
                ],
                "holdout": report["holdout"],
            }
            report["data_manifest"] = manifest
            write_json(output / "data_manifest.json", manifest)
    plan, folds = preflight(config, output, started, input_error=input_error)
    plan.update(run_id=run_id, config_fingerprint=report["config_fingerprint"])
    if real_spot:
        plan.update(holdout=report["holdout"], source_data_validated=bars is not None)
    report["plan"] = plan
    write_json(output / "plan.json", plan)
    limits = plan["limits"]
    deadline = started + limits["max_wall_seconds_per_campaign"]
    research = config["research"]
    horizon = research["horizon_bars"]
    admitted = plan["preflight_status"] == "ADMITTED"
    request = {}
    research_id = None
    prefix_path = output / "research-prefix.npy"

    if admitted:
        if bars is None:
            bars = generate(
                report["seed"],
                market["n_bars"],
                market["bar_minutes"],
                market["symbol"],
            )
            validate(bars)
        holdout_start = plan["holdout_start"]
        prefix = replace(bars, values=bars.values[:holdout_start])
        np.save(prefix_path, prefix.values, allow_pickle=False)
        write_dataset(bars, output / "dataset.csv.tmp")
        (output / "dataset.csv.tmp").replace(output / "dataset.csv")
        report.update(dataset_fingerprint=bars.fingerprint, dataset_path="dataset.csv")
        if not real_spot:
            report["holdout"] = {
                "purpose": "final_holdout_reserved",
                "start_index": holdout_start,
                "start_at": bars.time(holdout_start),
                "end_at": bars.time(-1, close=True),
                "observations": len(bars.values) - holdout_start,
                "evaluated": False,
            }
        intervals = [
            {
                "train": [bars.time(train.start), bars.time(train.stop)],
                "validation": [bars.time(val.start), bars.time(val.stop)],
                "label_last_required_at": bars.time(train.stop + horizon),
            }
            for train, val in folds
        ]
        request = {
            "prefix": str(prefix_path),
            "bar_minutes": market["bar_minutes"],
            "symbol": market["symbol"],
            "horizon": horizon,
            "costs": config["costs"],
            "allow_short": config["execution_simulation"]["allow_short"],
            "notional": config["execution_simulation"]["notional_per_trade"],
            "folds": [
                [train.start, train.stop, val.start, val.stop] for train, val in folds
            ],
        }
        if real_spot:
            request["real_spot"] = True
        research_id = fingerprint(
            {
                "prefix_fingerprint": prefix.fingerprint,
                "folds": request["folds"],
                "horizon": horizon,
                "costs": config["costs"],
                "execution": config["execution_simulation"],
                "source_fingerprint": report["source_fingerprint"],
                "dependencies": report["dependencies"],
            }
        )
        report["research_intervals"] = intervals

    trials = report["trials"]
    try:
        # Configuration order is a fixed, auditable priority. No outcome can insert another trial.
        for priority, candidate in enumerate(research["candidates"], 1):
            trial = run_candidate(
                db,
                output,
                report,
                plan,
                request,
                candidate,
                priority,
                research_id,
                deadline,
            )
            trials.append(trial)
            plan["started_trials"] += int(trial["started"])
            plan["completed_fits"] += trial["completed_fits"]
            plan["sampled_cpu_seconds"] += trial.get("sampled_cpu_seconds", 0.0)
            if trial["peak_rss_mb"] is not None:
                plan["peak_rss_mb"] = max(
                    plan["peak_rss_mb"] or 0, trial["peak_rss_mb"]
                )
    finally:
        prefix_path.unlink(missing_ok=True)

    statuses = [trial["execution_status"] for trial in trials]
    report["execution_status"] = next(
        (s for s in statuses if s != "COMPLETED"), "COMPLETED"
    )
    plan["runtime_wall_seconds"] = monotonic() - started
    if report["execution_status"] != "COMPLETED":
        plan["stop_reason"] = next(
            trial["stop_reason"] for trial in trials if trial["stop_reason"]
        )
    if report["execution_status"] == "COMPLETED":
        screened_out = all(
            trial.get("metrics", {}).get("feasibility", {}).get("status")
            == "SCREENED_OUT"
            for trial in trials
        )
        report["evaluation_status"] = "SCREENED_OUT" if screened_out else "COMPLETED"
    if len(trials) == 2 and all(
        "prediction" in trial.get("metrics", {}) for trial in trials
    ):
        first, second = (trial["metrics"] for trial in trials)
        report["second_minus_first"] = {
            "reference_candidate": trials[0]["candidate_id"],
            "challenger_candidate": trials[1]["candidate_id"],
            "mae_change": second["prediction"]["mae"] - first["prediction"]["mae"],
            "net_pnl_change": (
                second["trading"]["candidate"]["net_pnl"]
                - first["trading"]["candidate"]["net_pnl"]
            ),
        }


def run_candidate(
    db, output, report, plan, request, candidate, priority, research_id, deadline
):
    run_id = report["run_id"]
    candidate_id = candidate["id"]
    metadata = {
        "candidate_id": candidate_id,
        "family": "linear",
        "version": "1",
        "hypothesis": "The configured trailing features may predict the next-open horizon return.",
        "feature_list": candidate["features"],
        "model_type": candidate["model"],
        "model_params": {"alpha": 1.0, "solver": "svd", "transform": "StandardScaler"},
        "seed": report["seed"],
        "scenario": report["scenario"],
        "priority": priority,
        "code_version": __version__,
        "source_fingerprint": report["source_fingerprint"],
        "config_fingerprint": report["config_fingerprint"],
        "dataset_fingerprint": report["dataset_fingerprint"],
        "target_horizon_bars": report["horizon_bars"],
        "holdout_reserved_interval": report["holdout"],
        "folds": report.get("research_intervals", []),
        "cost_model": report["configuration"]["costs"],
        "artifacts": ["plan.json", "report.json", "report.md"]
        + (["dataset.csv"] if research_id else [])
        + (["data_manifest.json"] if "data_manifest" in report else []),
        "evidence_key": fingerprint(
            [research_id, candidate["model"], candidate["features"]]
        )
        if research_id
        else None,
    }
    outcome = {
        "execution_status": (
            "CANCELLED"
            if plan.get("pilot", {}).get("execution_status") == "CANCELLED"
            else "REJECTED_PREFLIGHT"
        ),
        "stop_reason": plan["stop_reason"],
        "started": False,
        "completed_fits": 0,
        "peak_rss_mb": None,
        "sampled_cpu_seconds": 0.0,
        "runtime_wall_seconds": 0.0,
    }
    previous = report["trials"][-1] if report["trials"] else {}
    blocked = {"CANCELLED", "BUDGET_EXHAUSTED", "REJECTED_PREFLIGHT"}
    if previous.get("execution_status") in blocked:
        outcome.update(
            execution_status=previous["execution_status"],
            stop_reason=previous["stop_reason"],
        )
    elif plan["preflight_status"] == "ADMITTED":
        journal.start_experiment(db, run_id, candidate_id, metadata)
        outcome = supervise(
            output,
            request | {"features": candidate["features"]},
            plan["max_wall_seconds_per_trial"],
            deadline,
            plan["max_memory_mb"],
        )
    metrics = outcome.pop("result", None)
    trial = {
        "experiment_id": f"{run_id}:{candidate_id}",
        "candidate_id": candidate_id,
        "priority": priority,
        "features": candidate["features"],
        **outcome,
        "evidence_status": "INSUFFICIENT_EVIDENCE" if metrics else "NOT_EVALUATED",
    }
    if metrics:
        trial["metrics"] = metrics
    journal.finish_experiment(db, run_id, trial, metadata | outcome)
    return trial


def write_reports(output: Path, report: dict) -> None:
    write_json(output / "plan.json", report["plan"])
    write_json(output / "report.json", report)
    plan = report["plan"]
    lines = [
        f"# AQRS {report['dataset_type']} research report",
        "",
        f"Run **{report['run_id']}** ended with **{report['execution_status']}**.",
        f"Candidate evaluation **{report['evaluation_status']}**.",
        "",
        *report["limitations"],
        "",
        f"- Seed {report['seed']}, scenario {report['scenario']}, bar length "
        f"{report['timeframe_minutes']} minutes, horizon {report['horizon_bars']} bars.",
        f"- Dataset fingerprint `{report['dataset_fingerprint']}`.",
        f"- Configuration fingerprint `{report['config_fingerprint']}`.",
        f"- Preflight {plan['preflight_status']}, {plan['started_trials']}/{plan['planned_trials']} "
        f"trials started, {plan['completed_fits']}/{plan['planned_fits']} fits completed, including pilot.",
        f"- Memory mode {plan['memory_mode']}, sampled peak {plan['peak_rss_mb']} MiB.",
        f"- Sampled worker CPU time across pilot and trials was {plan['sampled_cpu_seconds']:.3f} seconds.",
    ]
    if report["evaluation_status"] == "SCREENED_OUT":
        lines.append(
            "- The economic screen completed. Candidate fits and simulation were skipped."
        )
    if report["holdout"]:
        lines.append(
            f"- Reserved holdout begins at {report['holdout']['start_at']} and was not evaluated."
        )
    if report.get("stage_wall_seconds"):
        lines.append(
            f"- Archive import took {report['stage_wall_seconds']['import']:.6f} seconds."
        )
    if plan["stop_reason"]:
        lines.append(f"- Stop reason: {plan['stop_reason']}")
    lines += ["", "## Cost assumptions", ""]
    for name, value in report["configuration"]["costs"].items():
        lines.append(f"- `{name}` = {value} bps")
    for trial in report["trials"]:
        lines += [
            "",
            f"## {trial['candidate_id']}",
            "",
            f"Execution **{trial['execution_status']}**, evidence **{trial['evidence_status']}**.",
        ]
        if trial["stop_reason"]:
            lines.append(trial["stop_reason"])
        metrics = trial.get("metrics", {})
        if not metrics:
            continue
        lines += ["", metrics["rationale"]]
        if metrics.get("stage_wall_seconds"):
            timings = metrics["stage_wall_seconds"]
            lines.append(
                f"- Feature calculation took {timings['features']:.6f} seconds."
            )
            seconds = timings["simulation"]
            lines.append(
                "- Execution simulation was skipped."
                if seconds is None
                else f"- Execution simulation took {seconds:.6f} seconds."
            )
        if "prediction" not in metrics:
            continue
        prediction = metrics["prediction"]
        lines += [
            "",
            f"MAE on {prediction['observations']} out-of-sample observations was "
            f"{prediction['mae']:.8f}; zero-return MAE was {prediction['zero_mae']:.8f}. "
            "MAE is measured in simple returns and lower is better.",
            "",
            "| Policy | Trades | Gross PnL | Net PnL | Turnover | Max drawdown |",
            "|---|---:|---:|---:|---:|---:|",
        ]
        for name, value in metrics["trading"].items():
            lines.append(
                f"| {name} | {value['trade_count']} | {value['gross_pnl']:.6f} | "
                f"{value['net_pnl']:.6f} | {value['turnover']:.6f} | {value['max_drawdown']:.6f} |"
            )
        lines += [
            "",
            "PnL, turnover and drawdown use abstract notional units. Higher net PnL and "
            "lower realized-equity drawdown are favorable.",
            f"Incremental net PnL against momentum was {metrics['incremental_net_pnl_vs_momentum']:.6f}.",
        ]
    lines += [
        "",
        "See `report.json` for fold boundaries, fit metrics and individual simulated fills.",
    ]
    write_text(output / "report.md", "\n".join(lines) + "\n")
