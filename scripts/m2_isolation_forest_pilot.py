"""Run the authorized M2-E10 volatility alert comparison and verify its replay."""

import json
import platform
import sys
from contextlib import closing
from dataclasses import replace
from datetime import UTC, datetime
from hashlib import sha256
from math import isclose
from numbers import Integral
from pathlib import Path
from time import monotonic
from uuid import uuid4

from aqrs import journal
from aqrs.governor import supervise
from aqrs.platform_guard import capability
from aqrs.storage import fingerprint, write_json
from aqrs.worker import reserve_fit
from aqrs.worker import run as run_worker

if __package__:
    from . import m2_supervised_pilot as prior
else:
    import m2_supervised_pilot as prior

CONTROL, CHALLENGER = ARMS = ("volatility_only", "isolation_forest")
ROWS, DAY, HORIZON = 5760, 1440, 30
PARAMETERS = {
    "n_estimators": 64,
    "max_samples": 256,
    "contamination": "auto",
    "max_features": 1.0,
    "bootstrap": False,
    "n_jobs": 1,
    "random_state": 42,
    "warm_start": False,
}
LIMITS = {
    "timing_seconds": 5,
    "trial_seconds": 120,
    "campaign_seconds": 300,
    "rss_mb": 4096,
}
ROOT = Path("artifacts/m2-e10")
CONFIG = {
    "variant": "M2-E10/1",
    "days": [day.isoformat() for day in prior.DAYS],
    "archive_digests": prior.DIGESTS,
    "features": prior.FEATURES,
    "horizon": HORIZON,
    "costs": prior.COSTS,
    "scikit_learn": "1.9.1",
    "isolation_forest": PARAMETERS,
    "calibration_quantile": 0.9,
    "last_eligible_minute": 28,
    "screen_bps": 27,
    "minimum_pairs_per_day": 4,
    "minimum_mean_difference_bps": 5,
    "numeric_replay_tolerance": 1e-8,
    "limits": LIMITS,
    "research": {"candidates": [{"id": name} for name in ARMS]},
}


def fixed_folds(bars):
    from aqrs.market import build_folds, validate

    validate(bars)
    expected_start = datetime(2026, 1, 1, tzinfo=UTC).timestamp()
    if (
        bars.values.shape != (ROWS, 6)
        or bars.values[0, 0] != expected_start
        or bars.bar_minutes != 1
        or bars.symbol != "BTCUSDT"
    ):
        raise ValueError("Expected the four registered development days in UTC.")
    return build_folds(ROWS, HORIZON, 2 * DAY, DAY, 2)


def alerts(validation, flags):
    import numpy as np

    if (
        validation.start % DAY != 0
        or validation.stop != validation.start + DAY - HORIZON - 1
        or len(flags) != validation.stop - validation.start
    ):
        raise ValueError("Invalid validation boundaries for UTC hour alerts.")
    indices = []
    for minute in range(0, DAY, 60):
        matches = np.flatnonzero(flags[minute : minute + 29])
        if len(matches):
            indices.append(validation.start + minute + int(matches[0]))
    return indices


def cutoff(training_values):
    import numpy as np

    if not np.isfinite(training_values).all():
        raise ValueError("Calibration inputs must be finite.")
    return float(
        np.quantile(training_values, CONFIG["calibration_quantile"], method="linear")
    )


def estimator():
    from sklearn import __version__
    from sklearn.ensemble import IsolationForest

    if __version__ != CONFIG["scikit_learn"]:
        raise ValueError("Expected scikit-learn 1.9.1.")
    return IsolationForest(**PARAMETERS)


def score_fold(
    model, bars, matrix, train, validation, volatility_cutoff, fit_completed
):
    import numpy as np

    from aqrs.market import features

    model.fit(matrix[train])
    fit_completed()
    anomaly_cutoff = cutoff(-model.score_samples(matrix[train]))
    scores = -model.score_samples(matrix[validation])
    high_volatility = matrix[validation, 2] > volatility_cutoff
    selected = alerts(validation, high_volatility & (scores > anomaly_cutoff))

    # Hold the fitted model and the training cutoffs fixed while changing future input.
    prefix_length = 12 * 60 + 29
    split = validation.start + prefix_length
    changed = bars.values.copy()
    changed[split:, 1:5] *= 1.25
    changed[split:, 5] *= 2
    changed_features = features(replace(bars, values=changed))[validation]
    changed_scores = -model.score_samples(changed_features)
    if not np.isfinite(scores).all() or not np.isfinite(changed_scores).all():
        raise ValueError("Anomaly scores must be finite.")
    earlier_changed = alerts(
        validation,
        (changed_features[:, 2] > volatility_cutoff)
        & (changed_scores > anomaly_cutoff),
    )
    delta = float(
        np.max(np.abs(scores[:prefix_length] - changed_scores[:prefix_length]))
    )
    if not delta <= CONFIG["numeric_replay_tolerance"] or (
        [index for index in selected if index < split]
        != [index for index in earlier_changed if index < split]
    ):
        raise ValueError(
            "Future perturbation changed earlier anomaly scores or alerts."
        )
    return {
        "alerts": selected,
        "anomaly_cutoff": anomaly_cutoff,
        "future_check": {"prefix_rows": prefix_length, "max_score_difference": delta},
    }


def evaluate_worker(request, directory):
    import numpy as np

    from aqrs.market import Bars, features

    if request["phase"] == "timing":
        # Match the larger training fold and include its training and both scoring passes.
        matrix = np.random.default_rng(42).normal(size=(4277, len(prior.FEATURES)))
        model = estimator()
        started = monotonic()
        reserve_fit(request, directory, 1)
        model.fit(matrix)
        write_json(directory / "fits.json", 1)
        cutoff(-model.score_samples(matrix))
        model.score_samples(matrix[:1409])
        model.score_samples(matrix[-1409:])
        return {"fit_and_score_seconds": monotonic() - started}

    bars = Bars(np.load(request["window"], allow_pickle=False), "BTCUSDT", 1)
    folds = fixed_folds(bars)
    if bars.fingerprint != request["dataset_id"]:
        raise ValueError("Worker data differ from the verified development window.")
    matrix = features(bars)
    completed = 0

    def charge():
        nonlocal completed
        completed += 1
        write_json(directory / "fits.json", completed)

    days = []
    for number, (train, validation) in enumerate(folds):
        reserve_fit(request, directory, len(folds))
        if request["phase"] == CONTROL:
            volatility_cutoff = cutoff(matrix[train, 2])
            charge()
            selected = alerts(validation, matrix[validation, 2] > volatility_cutoff)
            days.append({"volatility_cutoff": volatility_cutoff, "alerts": selected})
        elif request["phase"] == CHALLENGER:
            days.append(
                score_fold(
                    estimator(),
                    bars,
                    matrix,
                    train,
                    validation,
                    request["volatility_cutoffs"][number],
                    charge,
                )
            )
        else:
            raise ValueError("Unregistered trial.")
    return days


def paired_day(bars, validation, returns, baseline, challenger):
    start = validation.start
    if (
        bars.bar_minutes != 1
        or validation.stop != start + DAY - HORIZON - 1
        or start < 0
        or start + DAY > len(bars.values)
    ):
        raise ValueError("Expected one complete minute-data validation day.")
    for arm in (baseline, challenger):
        if any(
            isinstance(index, bool)
            or not isinstance(index, Integral)
            or not start <= index < validation.stop
            or (index - start) % 60 > CONFIG["last_eligible_minute"]
            for index in arm
        ) or list(arm) != sorted(set(arm)):
            raise ValueError("Expected ordered, unique, in-hour alert indices.")
        if len({(index - start) // 60 for index in arm}) != len(arm):
            raise ValueError("At most one alert per arm and hour is permitted.")
    by_hour = [
        {(index - start) // 60: index for index in arm}
        for arm in (baseline, challenger)
    ]
    hours = []
    differences = []
    for hour in range(24):
        control_index, challenger_index = (arm.get(hour) for arm in by_hour)
        delta = None
        if control_index is not None and challenger_index is not None:
            delta = float(
                10_000 * (abs(returns[challenger_index]) - abs(returns[control_index]))
            )
            differences.append(delta)
        hours.append(
            {
                "hour_utc": bars.time(start + hour * 60),
                "control_index": control_index,
                "challenger_index": challenger_index,
                "difference_bps": delta,
            }
        )
    # Reuse the same fills, notional and costs as the existing trading diagnostic.
    policies = [diagnostic(bars, arm) for arm in (baseline, challenger)]
    net_by_hour = [
        {
            (trade["signal_index"] - start) // 60: trade["net_pnl"] * 10_000
            for trade in policy["trades"]
        }
        for policy in policies
    ]
    all_hours = [
        {
            "hour_utc": bars.time(start + hour * 60),
            "control_acts": hour in by_hour[0],
            "candidate_acts": hour in by_hour[1],
            "control_net_bps": net_by_hour[0].get(hour, 0.0),
            "candidate_net_bps": net_by_hour[1].get(hour, 0.0),
            "incremental_net_bps": net_by_hour[1].get(hour, 0.0)
            - net_by_hour[0].get(hour, 0.0),
        }
        for hour in range(24)
    ]
    incremental = sum(row["incremental_net_bps"] for row in all_hours)
    return {
        "day": bars.time(start)[:10],
        "hours": hours,
        "paired_hours": len(differences),
        "mean_difference_bps": sum(differences) / len(differences)
        if differences
        else None,
        "simultaneous_hours": sum(
            row["control_index"] is not None
            and row["control_index"] == row["challenger_index"]
            for row in hours
        ),
        "control_only_hours": len(baseline) - len(differences),
        "challenger_only_hours": len(challenger) - len(differences),
        "common_opportunity_trading": {
            "opportunities": 24,
            "control_trade_count": policies[0]["trade_count"],
            "candidate_trade_count": policies[1]["trade_count"],
            "sum_incremental_net_bps": incremental,
            "mean_incremental_net_bps": incremental / 24,
            "hours": all_hours,
            "supports_economic_claim": False,
            "used_for_legacy_decision": False,
            "scope": "Descriptive long-or-flat policy contrast over all fixed UTC hours.",
        },
    }


def diagnostic(bars, indices):
    import numpy as np

    from aqrs.evaluation import simulate

    result = simulate(
        bars,
        np.array(indices, dtype=int),
        np.ones(len(indices)),
        HORIZON,
        False,
        1,
        0,
        prior.COSTS,
    )
    if result["trade_count"] != len(indices):
        raise ValueError("Registered alerts must admit non-overlapping long trades.")
    result["net_bps_per_alert"] = (
        10_000 * result["net_pnl"] / len(indices) if indices else None
    )
    return result


def governor_limits(source):
    from aqrs.config import load

    effective, _ = load(source)
    limits = effective["resource_governor"]
    for key, required in {
        "max_research_trials_per_campaign": 2,
        "max_seeds": 1,
        "max_model_fits_per_campaign": 5,
        "max_parallel_trials": 1,
        "max_wall_seconds_per_trial": LIMITS["trial_seconds"],
        "max_wall_seconds_per_campaign": LIMITS["campaign_seconds"],
        "max_peak_rss_mb_per_trial": LIMITS["rss_mb"],
    }.items():
        if limits[key] < required:
            raise ValueError(f"The registered pilot exceeds Governor limit {key}.")
    if limits["memory_mode"] != "observed_rss" or limits["auto_retry_count"] != 0:
        raise ValueError(
            "The Governor does not permit the registered guard and retry mode."
        )
    preflight = limits["preflight"]
    if (
        not all(
            preflight[key]
            for key in (
                "enabled",
                "require_explicit_fit_count",
                "measure_representative_pilot",
                "reject_if_estimated_over_budget",
            )
        )
        or preflight["runtime_estimate_safety_factor"] > 2
    ):
        raise ValueError(
            "The current preflight settings differ from the registered plan."
        )
    return limits


def compare(output, report, db, deadline):
    import numpy as np

    from aqrs.market import targets
    from aqrs.planning import make_plan

    project_limits = governor_limits(output / "source/research.yaml")
    issue = capability(project_limits["memory_mode"])
    if issue:
        raise ValueError(issue)
    plan = make_plan(
        2, 2, 1, 1, 5, LIMITS["trial_seconds"], LIMITS["campaign_seconds"], pilot_fits=1
    )
    plan.update(
        planned_model_fits=3,
        planned_control_calibrations=2,
        estimated_memory_mb=256 + 4096 * ROWS / 1024**2,
        memory_estimate_method="256 MiB allowance plus 4096 bytes per bar",
        runtime_estimate_safety_factor=2,
        estimate_method="Two folds at twice measured timing-worker wall time, with a five-second minimum per trial",
        memory_mode="observed_rss",
        auto_retry_count=0,
        project_limits=project_limits,
        process_tree_mode="Windows Job Object"
        if sys.platform == "win32"
        else "POSIX process group",
    )
    report["plan"] = plan
    if (
        plan["preflight_status"] != "ADMITTED"
        or plan["estimated_memory_mb"] > LIMITS["rss_mb"]
    ):
        report["stop_reason"] = (
            "The registered plan exceeds its fit, time or RSS limits."
        )
        return "REJECTED_PREFLIGHT"
    bars = prior.read_window(Path("artifacts/m2-e03"))
    folds = fixed_folds(bars)
    command = [sys.executable, "-B", "-E", str(output / "source/pilot.py"), "--worker"]
    timing = supervise(
        output,
        {"phase": "timing"},
        LIMITS["timing_seconds"],
        deadline,
        LIMITS["rss_mb"],
        command=command,
    )
    report["timing"] = timing
    if timing["execution_status"] != "COMPLETED" or timing["completed_fits"] != 1:
        plan["preflight_status"] = "REJECTED_PREFLIGHT"
        report["stop_reason"] = (
            timing["stop_reason"] or "Timing worker did not complete exactly one fit."
        )
        return "REJECTED_PREFLIGHT"
    # Include interpreter startup, all scoring passes, and room for input checks.
    trial_estimate = max(5, 4 * timing["runtime_wall_seconds"])
    plan["estimated_trial_seconds"] = trial_estimate
    plan["estimated_wall_seconds"] = timing["runtime_wall_seconds"] + 2 * trial_estimate
    if (
        trial_estimate > LIMITS["trial_seconds"]
        or 2 * trial_estimate > deadline - monotonic()
    ):
        plan["preflight_status"] = "REJECTED_PREFLIGHT"
        report["stop_reason"] = (
            "Measured preflight exceeds the remaining trial or campaign time."
        )
        return "REJECTED_PREFLIGHT"

    report["dataset_id"] = bars.fingerprint
    report["folds"] = [
        {
            "train_start": train.start,
            "train_stop_exclusive": train.stop,
            "validation_start": validation.start,
            "validation_stop_exclusive": validation.stop,
            "validation_day": bars.time(validation.start)[:10],
            "last_training_exit": bars.time(train.stop + HORIZON),
            "last_validation_exit": bars.time(validation.stop + HORIZON),
        }
        for train, validation in folds
    ]
    returns = targets(bars, HORIZON)
    screen = 10_000 * cutoff(np.abs(returns[folds[0][0]]))
    report["economic_screen_bps"] = screen
    report["economic_screen_scope"] = (
        "Training movement scale only; passing does not establish predictability or net edge."
    )
    if screen <= CONFIG["screen_bps"]:
        report["stop_reason"] = (
            "Training-only 90th percentile absolute move did not exceed 27 bps."
        )
        report["evaluation_status"] = "SCREENED_OUT"
        return "COMPLETED"
    window = output / "development.npy"
    np.save(window, bars.values, allow_pickle=False)
    request = {"window": str(window), "dataset_id": bars.fingerprint}
    run_id = report["run_id"]
    for name in ARMS:
        metadata = {
            "evidence_key": fingerprint([report["config_id"], bars.fingerprint, name]),
            "source_id": report["provenance"]["source_id"],
            "replay_of": report["replay_of"],
        }
        journal.start_experiment(db, run_id, name, metadata)
        outcome = supervise(
            output,
            request | {"phase": name},
            LIMITS["trial_seconds"],
            deadline,
            LIMITS["rss_mb"],
            command=command,
        )
        units = outcome["completed_fits"]
        if name == CONTROL:
            outcome.update(completed_control_calibrations=units, completed_fits=0)
        status = outcome["execution_status"]
        if status == "COMPLETED" and units != len(folds):
            status = "FAILED"
            outcome.update(
                execution_status=status, stop_reason="Unexpected budget charge."
            )
        report["trials"][name] = outcome
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
            report["stop_reason"] = outcome["stop_reason"]
            return status
        if name == CONTROL:
            request["volatility_cutoffs"] = [
                row["volatility_cutoff"] for row in outcome["result"]
            ]

    results = [report["trials"][name]["result"] for name in ARMS]
    report["days"] = [
        paired_day(bars, validation, returns, control["alerts"], challenger["alerts"])
        for (_, validation), control, challenger in zip(folds, *results, strict=True)
    ]
    report["trading_diagnostic"] = {
        name: diagnostic(bars, [index for day in arm for index in day["alerts"]])
        for name, arm in zip(ARMS, results, strict=True)
    } | {"flat": {"net_pnl": 0, "trade_count": 0, "turnover": 0}}
    if monotonic() >= deadline:
        report["stop_reason"] = "Campaign wall-time limit."
        return "BUDGET_EXHAUSTED"
    advance = all(
        row["paired_hours"] >= CONFIG["minimum_pairs_per_day"]
        and row["mean_difference_bps"] >= CONFIG["minimum_mean_difference_bps"]
        for row in report["days"]
    )
    report["research_decision"] = "PROPOSE_FOLLOW_UP" if advance else "DEFER"
    report["evidence_status"] = "INSUFFICIENT_EVIDENCE"
    report["evaluation_status"] = "COMPLETED"
    report["development_screen_met"] = advance
    return "COMPLETED"


def valid_receipt(output, expected_platform):
    report = json.loads((output / "report.json").read_text(encoding="utf-8"))
    if (
        report["execution_status"] != "COMPLETED"
        or report["journal_integrity"] != "ok"
        or report["config_id"] != fingerprint(CONFIG)
        or fingerprint(report["configuration"]) != report["config_id"]
        or report["system"] != expected_platform
        or report["holdout"].get("authorized_reads", report["holdout"].get("reads"))
        != 0
        or report["runtime_seconds"] > LIMITS["campaign_seconds"]
        or report["plan"]["preflight_status"] != "ADMITTED"
        or report["plan"]["planned_fits"] != 5
        or report["plan"]["auto_retry_count"] != 0
        or report["economic_screen_bps"] <= CONFIG["screen_bps"]
        or report["budget"]["completed_fits"] != 3
        or report["budget"]["completed_control_calibrations"] != 2
        or report["budget"]["started_trials"] != 2
        or report["timing"]["completed_fits"] != 1
        or report["trials"][CONTROL]["completed_control_calibrations"] != 2
        or report["trials"][CHALLENGER]["completed_fits"] != 2
    ):
        raise ValueError(f"Invalid completed {expected_platform} pilot receipt.")
    for outcome, seconds in zip(
        [report["timing"], *(report["trials"][name] for name in ARMS)],
        [LIMITS["timing_seconds"], LIMITS["trial_seconds"], LIMITS["trial_seconds"]],
        strict=True,
    ):
        if (
            outcome["execution_status"] != "COMPLETED"
            or not outcome["started"]
            or not 0 < outcome["peak_rss_mb"] <= LIMITS["rss_mb"]
            or not 0 < outcome["runtime_wall_seconds"] <= seconds
        ):
            raise ValueError("A supervised worker did not satisfy its receipt limits.")
    provenance = report["provenance"]
    if fingerprint(provenance["files"]) != provenance["source_id"]:
        raise ValueError("Invalid source fingerprint.")
    for name, digest in provenance["files"].items():
        if sha256((output / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f"Archived source digest mismatch for {name}.")
    import sqlite3

    uri = (output / "research.sqlite3").resolve().as_uri() + "?mode=ro"
    with closing(sqlite3.connect(uri, uri=True)) as db:
        campaign = db.execute(
            "SELECT execution_status, config_fingerprint, manifest_json FROM campaigns WHERE run_id = ?",
            (report["run_id"],),
        ).fetchone()
        rows = db.execute(
            "SELECT candidate_id, execution_status, evidence_key, metrics_json "
            "FROM experiments WHERE run_id = ?",
            (report["run_id"],),
        ).fetchall()
        if (
            db.execute("PRAGMA integrity_check").fetchone()[0] != "ok"
            or campaign is None
            or campaign[:2] != ("COMPLETED", report["config_id"])
            or json.loads(campaign[2]) != report
            or {row[0] for row in rows} != set(ARMS)
            or any(
                status != "COMPLETED"
                or key != fingerprint([report["config_id"], report["dataset_id"], name])
                or json.loads(metrics) != report["trials"][name]
                for name, status, key, metrics in rows
            )
        ):
            raise ValueError("Journal and pilot receipt disagree.")
    return report


def require_agreement(a, b, path):
    if type(a) is not type(b):
        raise ValueError(f"Replay type mismatch at {path}.")
    if isinstance(a, dict) and a.keys() == b.keys():
        for key in a:
            require_agreement(a[key], b[key], f"{path}.{key}")
    elif isinstance(a, list) and len(a) == len(b):
        for i, (left, right) in enumerate(zip(a, b, strict=True)):
            require_agreement(left, right, f"{path}[{i}]")
    elif isinstance(a, float):
        if not isclose(a, b, rel_tol=0, abs_tol=CONFIG["numeric_replay_tolerance"]):
            raise ValueError(f"Replay numeric mismatch at {path}.")
    elif a != b:
        raise ValueError(f"Replay mismatch at {path}.")


def verify_replay():
    windows = valid_receipt(ROOT / "windows", "Windows")
    ubuntu = valid_receipt(ROOT / "ubuntu", "Linux")
    if ubuntu["replay_of"] != windows["run_id"]:
        raise ValueError("Ubuntu receipt does not identify the Windows attempt.")
    for key in (
        "dataset_id",
        "config_id",
        "folds",
        "economic_screen_bps",
        "days",
        "trading_diagnostic",
        "research_decision",
        "evidence_status",
    ):
        require_agreement(windows[key], ubuntu[key], key)
    for name in ARMS:
        require_agreement(
            windows["trials"][name]["result"], ubuntu["trials"][name]["result"], name
        )
    if windows["provenance"]["source_id"] != ubuntu["provenance"]["source_id"]:
        raise ValueError("Source differs between attempts.")
    write_json(
        ROOT / "comparison.json",
        {
            "status": "MATCH",
            "windows_run_id": windows["run_id"],
            "ubuntu_run_id": ubuntu["run_id"],
            "dataset_id": windows["dataset_id"],
            "config_id": windows["config_id"],
            "source_id": windows["provenance"]["source_id"],
            "absolute_tolerance": CONFIG["numeric_replay_tolerance"],
        },
    )
    print("Windows and Ubuntu receipts match.")


def main():
    import os

    started = monotonic()
    system = platform.system()
    if system not in {"Windows", "Linux"}:
        raise ValueError(
            "The authorized platforms are native Windows and headless Ubuntu."
        )
    replay = None
    if system == "Linux":
        release = platform.freedesktop_os_release()
        if (
            os.getuid() == 0
            or os.environ.get("DISPLAY")
            or release["ID"] != "ubuntu"
            or release["VERSION_ID"] != "24.04"
        ):
            raise ValueError(
                "Replay requires a non-root, headless Ubuntu 24.04 session."
            )
        replay = valid_receipt(ROOT / "windows", "Windows")
    output = (ROOT / ("windows" if system == "Windows" else "ubuntu")).resolve()
    output.mkdir(parents=True, exist_ok=False)
    provenance = prior.archive_source(
        output,
        entry=Path(__file__).resolve(),
        support=(Path(prior.__file__).resolve(), Path("configs/research.yaml")),
    )
    run_id = uuid4().hex
    report = {
        "run_id": run_id,
        "replay_of": replay["run_id"] if replay else None,
        "configuration": CONFIG,
        "config_id": fingerprint(CONFIG),
        "system": system,
        "platform": platform.platform(),
        "python": platform.python_version(),
        "provenance": provenance,
        "holdout": {
            "start_at": "2026-01-06T00:00:00Z",
            "authorized_reads": 0,
            "access_measurement": "not_instrumented",
            "evaluated": False,
        },
        "schema_version": "2",
        "evaluation_status": "NOT_COMPLETED",
        "trials": {},
        "evidence_status": "NOT_EVALUATED",
    }
    with closing(journal.connect(output / "research.sqlite3")) as db:
        journal.begin(db, run_id, report["config_id"], CONFIG, report)
        try:
            if replay and replay["provenance"]["source_id"] != provenance["source_id"]:
                raise ValueError("Replay source differs from the Windows snapshot.")
            status = compare(output, report, db, started + LIMITS["campaign_seconds"])
        except Exception as error:
            report["stop_reason"] = str(error)
            status = "FAILED" if report["trials"] else "REJECTED_PREFLIGHT"
            if status == "REJECTED_PREFLIGHT" and "plan" in report:
                report["plan"]["preflight_status"] = status
        workers = [report.get("timing", {}), *report["trials"].values()]
        report["budget"] = {
            "started_trials": sum(
                trial["started"] for trial in report["trials"].values()
            ),
            "completed_fits": sum(
                worker.get("completed_fits", 0) for worker in workers
            ),
            "completed_control_calibrations": report["trials"]
            .get(CONTROL, {})
            .get("completed_control_calibrations", 0),
            "peak_rss_mb": max(
                (
                    worker["peak_rss_mb"]
                    for worker in workers
                    if worker.get("peak_rss_mb") is not None
                ),
                default=None,
            ),
        }
        report["runtime_seconds"] = monotonic() - started
        report["journal_integrity"] = db.execute("PRAGMA integrity_check").fetchone()[0]
        if report["journal_integrity"] != "ok":
            status = "FAILED"
        report["execution_status"] = status
        with db:
            db.execute(
                "UPDATE experiments SET execution_status = 'CANCELLED' WHERE run_id = ? "
                "AND execution_status IN ('PROPOSED', 'RUNNING')",
                (run_id,),
            )
        journal.finish_campaign(db, run_id, status, report)
        write_json(output / "report.json", report)
    print(f"{status} {run_id} {output}")
    return 0 if status == "COMPLETED" else 2


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--worker":
        if (
            Path(journal.__file__).resolve().parent
            != Path(__file__).resolve().parent / "aqrs"
        ):
            raise SystemExit(
                "The pilot worker must import AQRS from the archived source."
            )
        run_worker(Path(sys.argv[2]), evaluate_worker)
    elif sys.argv[1:] == ["--verify-replay"]:
        verify_replay()
    elif len(sys.argv) == 1:
        raise SystemExit(main())
    else:
        raise SystemExit("Expected no arguments or --verify-replay.")
