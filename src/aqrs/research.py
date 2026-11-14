import csv
import os
from contextlib import closing
from dataclasses import replace
from datetime import date, timedelta
from importlib.metadata import version
from pathlib import Path
from time import monotonic
from uuid import uuid4

import numpy as np

from aqrs import __version__, journal, worker
from aqrs.admission import AdmissionRejected, data_scope
from aqrs.binance_spot_pilot import (
    IMPORT_ERRORS,
    M1_HOLDOUT_DAY,
    import_day,
    import_manifest,
    require_m1_development_day,
)
from aqrs.config import validate_data_admission, variant_limit
from aqrs.governor import supervise
from aqrs.market import generate, read_synthetic_csv, validate, write_dataset
from aqrs.planning import preflight
from aqrs.provenance import snapshot
from aqrs.storage import fingerprint, write_json, write_text


def spot_holdout(market: dict) -> dict:
    require_m1_development_day(market["day"])
    return {
        "purpose": "final_holdout_reserved",
        "start_at": f"{M1_HOLDOUT_DAY}T00:00:00+00:00",
        "end_at": f"{M1_HOLDOUT_DAY + timedelta(days=1)}T00:00:00+00:00",
        "authorized_reads": 0,
        "access_measurement": "not_instrumented",
        "evaluated": False,
    }


def run(
    config: dict,
    base: Path,
    *,
    plan_only: bool,
    rejection: AdmissionRejected | None = None,
) -> tuple[dict, int]:
    started = monotonic()
    run_id = uuid4().hex
    output = base / config["project"]["artifact_dir"] / run_id
    market = config["market"]
    database = (base / config["journal"]["sqlite_path"]).resolve()
    try:
        if rejection is not None:
            raise rejection
        validate_data_admission(config)
    except AdmissionRejected as denial:
        if plan_only:
            raise denial
        return reject_data_request(config, database, run_id, denial)
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
        elif market["source"] == "synthetic_csv":
            plan["source_data_validated"] = False
        write_json(output / "plan.json", plan)
        return plan, 0 if plan["preflight_status"] == "ADMITTED" else 2

    report = {
        "run_id": run_id,
        "schema_version": "2",
        "provenance": snapshot(output, Path(worker.__file__)),
        "zero_cost_components": [
            key for key, value in config["costs"].items() if value == 0
        ],
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
            "Observations and forward targets can overlap. No market significance is inferred."
            if any(
                c["model"] == "bar_reversal" for c in config["research"]["candidates"]
            )
            else "Observations and forward targets can overlap. No statistical significance is inferred.",
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
        except (Exception, KeyboardInterrupt) as error:
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
        "reason_code": report["plan"].get("reason_code"),
    }, {"COMPLETED": 0, "REJECTED_PREFLIGHT": 2, "CANCELLED": 130}.get(status, 1)


def reject_data_request(config, database: Path, run_id: str, denial: AdmissionRejected):
    manifest = {
        "run_id": run_id,
        "execution_status": "REJECTED_PREFLIGHT",
        "evaluation_status": "NOT_COMPLETED",
        "output_dir": None,
        "journal_path": str(database),
        "reason_code": denial.code,
        "stop_reason": str(denial),
    }
    with closing(journal.connect(database)) as db:
        journal.begin(
            db,
            run_id,
            fingerprint(config),
            config,
            manifest,
            rejection={"reason_code": denial.code, "stop_reason": str(denial)},
        )
    return manifest, 2


def reserve_campaign_variants(config, db, report, plan):
    """Bind the scheduled evaluation window and variants from config alone."""
    start, step = data_scope(config["market"])
    research = config["research"]
    evaluation_start = start + research["train_bars"] * step
    evaluation_end = evaluation_start + (
        research["validation_bars"] * research["walk_forward_folds"] * step
    )
    period = (evaluation_start.isoformat(), evaluation_end.isoformat())
    market = config["market"]
    variant_scope = {
        "source": market["source"],
        "symbol": market["symbol"].upper(),
        "input_start": start.isoformat(),
        "n_bars": market["n_bars"],
        "bar_minutes": market["bar_minutes"],
        "seed": config["project"]["seed"] if market["source"] == "synthetic" else None,
        "research": {
            k: research[k]
            for k in (
                "horizon_bars",
                "train_bars",
                "validation_bars",
                "walk_forward_folds",
            )
        },
    }
    variants = {
        c["id"]: fingerprint(
            variant_scope
            | {
                "model": c["model"],
                "features": sorted(c.get("features", [])),
                "costs": config["costs"] if c["model"] == "ridge" else None,
                "execution": config["execution_simulation"]
                if c["model"] == "ridge"
                else None,
            }
        )
        for c in research["candidates"]
    }
    limit = variant_limit(config["resource_governor"])
    admission = journal.reserve_variants(db, report["run_id"], period, variants, limit)
    report["variant_admission"] = {
        "evaluation_start_at": period[0],
        "evaluation_end_at": period[1],
        "variant_keys": variants,
        **admission,
    }
    if not admission["allowed"]:
        plan.update(
            preflight_status="REJECTED_PREFLIGHT",
            reason_code="VARIANT_LIMIT",
            stop_reason=f"Variant limit of {limit} reached for the UTC evaluation period.",
        )


def execute(
    config, db, output: Path, report: dict, started: float, *, base: Path
) -> None:
    run_id = report["run_id"]
    market = config["market"]
    real_spot = market["source"] == "binance_vision_spot"
    plan, folds = preflight(config, output, started, validate_only=True)
    limits = config["resource_governor"]
    deadline = started + limits["max_wall_seconds_per_campaign"]
    prepared = None
    if plan["preflight_status"] == "ADMITTED":
        reserve_campaign_variants(config, db, report, plan)
    if plan["preflight_status"] == "ADMITTED":
        preparation = supervise(
            output,
            {
                "stage": "prepare",
                "_worker_entry": str((output / "source/pilot.py").resolve()),
                "config": config,
                "base": str(base),
                "output": str(output.resolve()),
                "holdout_start": plan["holdout_start"],
                "folds": [[tr.start, tr.stop, va.start, va.stop] for tr, va in folds],
            },
            limits["max_wall_seconds_per_campaign"],
            deadline,
            limits["max_peak_rss_mb_per_trial"],
        )
        report["preparation"] = {k: v for k, v in preparation.items() if k != "result"}
        if preparation["execution_status"] == "COMPLETED":
            prepared = preparation["result"]
            plan, folds = preflight(
                config, output, started, input_error=prepared.get("input_error")
            )
        else:
            plan.update(
                preflight_status="REJECTED_PREFLIGHT",
                admission_execution_status=preparation["execution_status"],
                stop_reason=preparation["stop_reason"],
            )
    plan.update(run_id=run_id, config_fingerprint=report["config_fingerprint"])
    if report.get("preparation"):
        usage = report["preparation"]
        plan["peak_rss_mb"] = (
            max(plan["peak_rss_mb"] or 0, usage.get("peak_rss_mb") or 0) or None
        )
        plan["sampled_cpu_seconds"] += usage.get("sampled_cpu_seconds", 0)
    if prepared:
        report.update(
            {
                k: v
                for k, v in prepared.items()
                if k not in {"prefix_fingerprint", "input_error"}
            }
        )
    if real_spot:
        plan.update(
            holdout=report["holdout"],
            source_data_validated=bool(prepared and not prepared.get("input_error")),
        )
    elif market["source"] == "synthetic_csv":
        plan["source_data_validated"] = bool(
            prepared and not prepared.get("input_error")
        )
    report["plan"] = plan
    write_json(output / "plan.json", plan)
    research = config["research"]
    horizon = research["horizon_bars"]
    request = {}
    research_id = None
    prefix_path = output / "research-prefix.npy"
    if plan["preflight_status"] == "ADMITTED":
        request = {
            "_worker_entry": str((output / "source/pilot.py").resolve()),
            "prefix": str(prefix_path),
            "bar_minutes": market["bar_minutes"],
            "symbol": market["symbol"],
            "horizon": horizon,
            "costs": config["costs"],
            "allow_short": config["execution_simulation"]["allow_short"],
            "notional": config["execution_simulation"]["notional_per_trade"],
            "folds": [[tr.start, tr.stop, va.start, va.stop] for tr, va in folds],
            "fit_limit": len(folds),
        }
        if real_spot:
            request["real_spot"] = True
        research_id = fingerprint(
            {
                "prefix_fingerprint": prepared["prefix_fingerprint"],
                "folds": request["folds"],
                "horizon": horizon,
                "costs": config["costs"],
                "execution": config["execution_simulation"],
                "source_fingerprint": report["source_fingerprint"],
                "dependencies": report["dependencies"],
            }
        )

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
            plan["started_fits"] += trial.get("started_fits", trial["completed_fits"])
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
        report["stop_reason"] = plan["stop_reason"]
        if plan.get("reason_code"):
            report["reason_code"] = plan["reason_code"]
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


def prepare_data(request: dict) -> dict:
    """Prepare the research prefix under the same external campaign deadline."""
    config = request["config"]
    market, research = config["market"], config["research"]
    start_at, _ = data_scope(market)
    output, base = Path(request["output"]), Path(request["base"])
    real_spot = market["source"] == "binance_vision_spot"
    result = {}
    if real_spot:
        day = date.fromisoformat(market["day"])
        archive = base / market["archive_dir"] / f"{market['symbol']}-1m-{day}.zip"
        started = monotonic()
        try:
            bars, digest = import_day(
                archive, archive.with_suffix(".zip.CHECKSUM"), day
            )
        except IMPORT_ERRORS as error:
            detail = type(error).__name__ if isinstance(error, OSError) else str(error)
            return {"input_error": f"Binance archive rejected: {detail}"}
        result["stage_wall_seconds"] = {"import": monotonic() - started}
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
            "holdout": spot_holdout(market),
        }
        result["data_manifest"] = manifest
        write_json(output / "data_manifest.json", manifest)
    elif market["source"] == "synthetic_csv":
        try:
            bars, digest = read_synthetic_csv(
                base / market["csv_path"],
                market["n_bars"],
                market["bar_minutes"],
                market["symbol"],
                start_at=start_at,
            )
            result["data_manifest"] = {
                "source": "synthetic_csv",
                "dataset_type": "synthetic",
                "input_sha256": digest,
                "symbol": bars.symbol,
                "bar_minutes": bars.bar_minutes,
                "observations": len(bars.values),
                "start_at": bars.time(0),
                "end_at": bars.time(-1, close=True),
            }
        except (OSError, ValueError, OverflowError, csv.Error) as error:
            detail = (
                str(error) if isinstance(error, ValueError) else type(error).__name__
            )
            return {"input_error": f"Synthetic CSV rejected: {detail}"}
        write_json(output / "data_manifest.json", result["data_manifest"])
    else:
        bars = generate(
            config["project"]["seed"],
            market["n_bars"],
            market["bar_minutes"],
            market["symbol"],
        )
        validate(bars)
    holdout_start = request["holdout_start"]
    prefix = replace(bars, values=bars.values[:holdout_start])
    np.save(output / "research-prefix.npy", prefix.values, allow_pickle=False)
    write_dataset(bars, output / "dataset.csv.tmp")
    (output / "dataset.csv.tmp").replace(output / "dataset.csv")
    result.update(
        dataset_fingerprint=bars.fingerprint,
        dataset_path="dataset.csv",
        prefix_fingerprint=prefix.fingerprint,
    )
    if not real_spot:
        result["holdout"] = {
            "purpose": "final_holdout_reserved",
            "start_index": holdout_start,
            "start_at": bars.time(holdout_start),
            "end_at": bars.time(-1, close=True),
            "observations": len(bars.values) - holdout_start,
            "evaluated": False,
        }
    result["research_intervals"] = [
        {
            "train": [bars.time(a), bars.time(b)],
            "validation": [bars.time(c), bars.time(d)],
            "label_last_required_at": bars.time(b + research["horizon_bars"]),
        }
        for a, b, c, d in request["folds"]
    ]
    return result


def run_candidate(
    db, output, report, plan, request, candidate, priority, research_id, deadline
):
    run_id = report["run_id"]
    candidate_id = candidate["id"]
    reversal = candidate["model"] == "bar_reversal"
    features = candidate.get("features", [])
    metadata = {
        "candidate_id": candidate_id,
        "family": "rule_based" if reversal else "linear",
        "version": "2" if reversal else "1",
        "hypothesis": (
            "The next bar direction may reverse the last completed bar."
            if reversal
            else "The configured trailing features may predict the next-open horizon return."
        ),
        "feature_list": features,
        "model_type": candidate["model"],
        "model_params": {"flat_signal": "training_majority", "majority_tie": "up"}
        if reversal
        else {"alpha": 1.0, "solver": "svd", "transform": "StandardScaler"},
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
        "evidence_key": fingerprint([research_id, candidate["model"], features])
        if research_id
        else None,
    }
    if reversal:
        metadata["workflow_question"] = (
            "Can a synthetic reversal rule use the shared preflight, budget and journal?"
        )
    if admission := report.get("variant_admission"):
        metadata.update(
            variant_key=admission["variant_keys"][candidate_id],
            evaluation_start_at=admission["evaluation_start_at"],
            evaluation_end_at=admission["evaluation_end_at"],
        )
    if plan.get("reason_code"):
        metadata["reason_code"] = plan["reason_code"]
    outcome = {
        "execution_status": (
            plan.get("admission_execution_status", "CANCELLED")
            if plan.get("admission_execution_status")
            or plan.get("pilot", {}).get("execution_status") == "CANCELLED"
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
            request | {"features": features, "model": candidate["model"]},
            plan["max_wall_seconds_per_trial"],
            deadline,
            plan["max_memory_mb"],
        )
    metrics = outcome.pop("result", None)
    trial = {
        "experiment_id": f"{run_id}:{candidate_id}",
        "candidate_id": candidate_id,
        "priority": priority,
        "features": features,
        **outcome,
        "evidence_status": "INSUFFICIENT_EVIDENCE" if metrics else "NOT_EVALUATED",
    }
    if metrics:
        trial["metrics"] = metrics
    if reversal:
        trial["workflow_question"] = metadata["workflow_question"]
        learning = (
            "The common preflight, supervised worker and journal handled the synthetic reversal rule."
            if outcome["execution_status"] == "COMPLETED" and metrics
            else "No workflow conclusion: the synthetic reversal trial did not complete."
        )
        metadata["workflow_learning"] = trial["workflow_learning"] = learning
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
    if report.get("zero_cost_components"):
        lines.append(
            "- Zero-cost assumptions: "
            + ", ".join(report["zero_cost_components"])
            + ". No realistic-cost claim follows."
        )
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
        if directional := metrics.get("directional_reversal"):
            lines += [
                "",
                f"Workflow question: {trial['workflow_question']}",
                trial["workflow_learning"],
                f"**{directional['decision']}** on {directional['observations']} observations. "
                f"Reversal accuracy {directional['accuracy']:.2%}, always up "
                f"{directional['always_up_accuracy']:.2%}, always down "
                f"{directional['always_down_accuracy']:.2%}.",
                f"Daily uncertainty: {directional['uncertainty_status']} "
                f"across {directional['scored_utc_days']} scored UTC days.",
            ]
            for control, bounds in directional["contrasts"].items():
                for lag, bound in bounds.items():
                    lines.append(
                        f"- Against {control}, lag {lag} days: "
                        f"one-sided 95% lower bound {bound['lower_95_one_sided'] * 100:+.3f} pp."
                    )
        if metrics.get("feasibility", {}).get("scope"):
            lines.append(
                "The training movement screen checks scale against assumed costs; "
                "it does not establish predictability or net profitability."
            )
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
        ]
        if diagnostic := prediction.get("diagnostics"):
            rank = diagnostic["rank_correlation"]
            rank_text = f"{rank:.6f}" if rank is not None else diagnostic["rank_status"]
            lines += [
                "",
                "### Descriptive diagnostics",
                "",
                f"Spearman rank correlation: {rank_text}. Average ranks handle ties; "
                "this measures monotonic association, not all possible signal information.",
                f"Prediction mean/SD: {diagnostic['prediction_mean'] * 10_000:.4f} / "
                f"{diagnostic['prediction_std'] * 10_000:.4f} bps; target mean/SD: "
                f"{diagnostic['target_mean'] * 10_000:.4f} / "
                f"{diagnostic['target_std'] * 10_000:.4f} bps. SD uses population scaling.",
                "All eligible prediction rows are included, even when the policy is flat. "
                "These diagnostics make no significance or economic claim. Overlapping "
                "targets and pooled folds do not establish independent or stable evidence.",
                "",
                "| Fold | Observations | Rank correlation | Prediction SD (bps) | Target SD (bps) |",
                "|---|---:|---:|---:|---:|",
            ]
            for index, fold in enumerate(metrics.get("folds", []), 1):
                fold_prediction = fold["prediction"]
                if fold_diagnostic := fold_prediction.get("diagnostics"):
                    rank = fold_diagnostic["rank_correlation"]
                    rank_text = (
                        f"{rank:.6f}"
                        if rank is not None
                        else fold_diagnostic["rank_status"]
                    )
                    lines.append(
                        f"| {index} | {fold_prediction['observations']} | {rank_text} | "
                        f"{fold_diagnostic['prediction_std'] * 10_000:.4f} | "
                        f"{fold_diagnostic['target_std'] * 10_000:.4f} |"
                    )
        lines += [
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
        for name, value in metrics["trading"].items():
            if value.get("economic_evidence"):
                lines.append(
                    f"- {name}: {value['economic_evidence']['status']}. "
                    "Trade count is not an independent sample-size or precision estimate."
                )
        for name, scope in metrics.get("benchmark_scope", {}).items():
            lines.append(f"- {name} benchmark: {scope}")
    lines += [
        "",
        "See `report.json` for fold boundaries, fit metrics and individual simulated fills.",
    ]
    write_text(output / "report.md", "\n".join(lines) + "\n")
