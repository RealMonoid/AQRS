import platform
import sys
from pathlib import Path
from time import monotonic

from aqrs.governor import supervise
from aqrs.market import build_folds
from aqrs.platform_guard import capability


def make_plan(
    candidates: int,
    folds: int,
    seeds: int,
    seconds_per_fit: float,
    max_fits: int,
    max_trial_seconds: float,
    max_campaign_seconds: float,
    *,
    pilot_fits: int = 0,
    max_trials: int = 2,
    max_seeds: int = 1,
) -> dict:
    trials = candidates * seeds
    fits = trials * folds + pilot_fits
    estimate = fits * seconds_per_fit
    rejection = []
    if fits > max_fits:
        rejection.append("Fit count exceeds the campaign limit.")
    if trials > max_trials or seeds > max_seeds:
        rejection.append("Trial or seed count exceeds the campaign limit.")
    if folds * seconds_per_fit > max_trial_seconds or estimate > max_campaign_seconds:
        rejection.append("Estimated wall time exceeds the trial or campaign limit.")
    return {
        "planned_trials": trials,
        "planned_fits": fits,
        "planned_baseline_fits": 0,
        "planned_pilot_fits": pilot_fits,
        "planned_folds_per_trial": folds,
        "planned_seeds": seeds,
        "estimated_wall_seconds": estimate,
        "preflight_status": "REJECTED_PREFLIGHT" if rejection else "ADMITTED",
        "rejection_reasons": rejection,
    }


def preflight(config: dict, directory: Path, started: float) -> tuple[dict, list]:
    limits = config["resource_governor"]
    settings = limits["preflight"]
    research = config["research"]
    market = config["market"]
    holdout_start = int(market["n_bars"] * (1 - research["final_holdout_fraction"]))
    trial_limit = limits["max_wall_seconds_per_trial"]
    campaign_limit = limits["max_wall_seconds_per_campaign"]
    memory_limit = limits["max_peak_rss_mb_per_trial"]
    pilot_fits = int(settings["measure_representative_pilot"])
    factor = settings["runtime_estimate_safety_factor"]
    plan = make_plan(
        len(research["candidates"]),
        research["walk_forward_folds"],
        1,
        1.0,
        limits["max_model_fits_per_campaign"],
        trial_limit,
        campaign_limit,
        pilot_fits=pilot_fits,
        max_trials=limits["max_research_trials_per_campaign"],
        max_seeds=limits["max_seeds"],
    )
    # Heuristic admission estimates are separate from enforced wall and sampled RSS limits.
    memory_estimate = 256 + 4096 * market["n_bars"] / 1024**2
    plan.update(
        configuration_version="0.1",
        limits=limits,
        seed=config["project"]["seed"],
        estimated_memory_mb=memory_estimate,
        started_trials=0,
        completed_fits=0,
        holdout_start=holdout_start,
        runtime_wall_seconds=0.0,
        peak_rss_mb=None,
        sampled_cpu_seconds=0.0,
        max_wall_seconds_per_trial=trial_limit,
        max_wall_seconds_per_campaign=campaign_limit,
        max_memory_mb=memory_limit,
        auto_retry_count=0,
        stop_reason=None,
        runtime_estimate_safety_factor=factor,
        estimate_method="fixed conservative M0 allowances",
        memory_estimate_method="256 MiB interpreter allowance plus 4096 bytes per input bar",
        memory_mode=limits["memory_mode"],
        process_tree_mode={
            "win32": "Windows Job Object",
            "linux": "POSIX process group",
        }.get(sys.platform, "unsupported"),
        platform=(
            f"Windows NT {platform.version()} {platform.machine()}"
            if sys.platform == "win32"
            else platform.platform()
        ),
        python=platform.python_version(),
    )
    reasons = plan["rejection_reasons"]
    folds = []
    guard_issue = capability(limits["memory_mode"])
    if guard_issue:
        reasons.append(guard_issue)
    if memory_estimate > memory_limit:
        reasons.append("Estimated memory exceeds the trial RSS limit.")
    if not reasons:
        try:
            folds = build_folds(
                holdout_start,
                research["horizon_bars"],
                research["train_bars"],
                research["validation_bars"],
                research["walk_forward_folds"],
            )
        except ValueError as error:
            reasons.append(str(error))
    if not reasons and pilot_fits:
        largest_train = folds[-1][0]
        pilot = supervise(
            directory,
            {
                "pilot_rows": largest_train.stop - largest_train.start,
                "pilot_columns": max(
                    len(c["features"]) for c in research["candidates"]
                ),
            },
            min(5, trial_limit),
            started + campaign_limit,
            memory_limit,
        )
        plan.update(
            pilot=pilot,
            completed_fits=pilot["completed_fits"],
            peak_rss_mb=pilot["peak_rss_mb"],
            sampled_cpu_seconds=pilot.get("sampled_cpu_seconds", 0.0),
            estimate_method="bounded largest-shape Ridge pilot with conservative M0 allowances",
        )
        if pilot["execution_status"] != "COMPLETED":
            reasons.append(f"Pilot did not complete: {pilot['stop_reason']}")
    if not reasons:
        pilot = plan.get("pilot", {})
        pilot_wall = pilot.get("runtime_wall_seconds", 0.0)
        fit_seconds = max(
            1.0, factor * pilot.get("result", {}).get("fit_wall_seconds", 0.0)
        )
        trial_estimate = max(2.0, factor * pilot_wall) + len(folds) * fit_seconds
        campaign_estimate = (
            3 + max(0.0, pilot_wall) + plan["planned_trials"] * trial_estimate
        )
        plan.update(
            estimated_wall_seconds=campaign_estimate,
            estimated_trial_seconds=trial_estimate,
        )
        if trial_estimate > trial_limit or campaign_estimate > campaign_limit:
            reasons.append("Estimated wall time exceeds the trial or campaign limit.")
    plan["preflight_status"] = "REJECTED_PREFLIGHT" if reasons else "ADMITTED"
    plan["stop_reason"] = " ".join(reasons) if reasons else None
    plan["runtime_wall_seconds"] = monotonic() - started
    return plan, folds
