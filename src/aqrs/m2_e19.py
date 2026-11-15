"""Coverage-first comparison of volatility gates on the M2-E18 rule."""

import argparse
import os
import subprocess
import sys
from contextlib import closing
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path
from time import monotonic
from uuid import uuid4

import numpy as np
from scipy.special import logsumexp

from aqrs import journal
from aqrs.config import load
from aqrs.discovery import (
    COSTS,
    HORIZON,
    ROWS,
    compare_policies,
    folds_for_window,
    volume_inputs,
)
from aqrs.governor import supervise
from aqrs.m2_e14 import (
    D01_PATH,
    E17_PATH,
    E18,
    Campaign,
    claim_market_attempt,
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
from aqrs.study_admission import unqualified_entry
from aqrs.worker import reserve_fit
from aqrs.worker import run as run_worker

ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = "M2-E19"
COVERAGE = "VOL_REGIME_COVERAGE_E19_V1"
CHALLENGER = "VOL_REGIME_HMM_E19_V1"
PILOT = Campaign(CAMPAIGN, E18.first_day, (COVERAGE, CHALLENGER), ())
COVERAGE_PATH = "evidence/m2-e19-coverage.json"
PUBLICATION_REF = "refs/heads/codex/m2-e19-regime-filter"
MODEL_VERSION = "0.3.3"
MODEL_PARAMETERS = {
    "n_components": 2,
    "covariance_type": "diag",
    "random_state": 42,
    "n_iter": 100,
    "tol": 0.01,
    "implementation": "scaling",
}
MIN_DELTA_BPS = 0.10
QUANTILE = 0.75
MIN_DAYS = 2
MIN_ENTRIES = 4
DATASET_ID = "f24e81c97227b0932978a240ae20411f6ffea7242bed11294c43b16ce9904568"




def cutoff(values, request, directory):
    if not len(values) or not np.isfinite(values).all():
        raise ValueError("Invalid training sample for cutoff calibration.")
    reserve_fit(request, directory, 2)
    value = float(np.quantile(values, QUANTILE, method="linear"))
    complete_charge(directory)
    return value


def complete_charge(directory):
    completed = directory / "fits.json"
    write_json(completed, 1 + (read_json(completed) if completed.exists() else 0))


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


def fit_hmm(volatility, request, directory):
    from hmmlearn.hmm import GaussianHMM

    reserve_fit(request, directory, 4)
    model = GaussianHMM(**MODEL_PARAMETERS).fit(volatility[:, None])
    complete_charge(directory)
    history = list(model.monitor_.history)
    gain = history[-1] - history[-2] if len(history) >= 2 else np.inf
    if not np.isfinite(history).all() or not -1e-7 <= gain <= MODEL_PARAMETERS["tol"]:
        raise ValueError(
            "The fixed HMM did not reach the registered convergence tolerance."
        )
    return model


def forward(model, observations):
    """Return probabilities using only the current and preceding observations."""
    means = model.means_.ravel()
    variances = model.covars_.ravel()
    if (
        not np.isfinite(means).all()
        or not np.isfinite(variances).all()
        or np.any(variances <= 0)
    ):
        raise ValueError("Invalid HMM emissions.")
    emissions = -0.5 * (
        np.log(2 * np.pi * variances) + (observations[:, None] - means) ** 2 / variances
    )
    with np.errstate(divide="ignore"):
        previous = np.log(model.startprob_)
        transitions = np.log(model.transmat_)
    result = np.empty_like(emissions)
    for index, emission in enumerate(emissions):
        state = previous + emission
        state -= logsumexp(state)
        result[index] = np.exp(state)
        previous = logsumexp(state[:, None] + transitions, axis=0)
    if not np.isfinite(result).all():
        raise ValueError("Invalid forward probabilities.")
    return result


def high_state_probabilities(model, observations):
    return forward(model, observations)[:, np.argmax(model.means_.ravel())]


def require_causal_prefix(score, observations, split):
    complete = score(observations)
    changed = observations.copy()
    changed[split:] *= 3
    if not (
        np.array_equal(complete[:split], score(changed)[:split])
        and np.array_equal(complete[:split], score(observations[:split]))
    ):
        raise ValueError("Future inputs altered past regime scores.")


def paired_decision(comparison):
    folds = []
    for fold, days in zip(
        ("fold_1", "fold_2"), (E18.days[4:7], E18.days[7:]), strict=True
    ):
        active_days = sum(
            min(
                comparison["utc_day"][f"{day}T00:00:00+00:00"]["policies"][role][
                    "trade_count"
                ]
                for role in ("rolling_volatility", "hmm")
            )
            >= MIN_ENTRIES
            for day in days
        )
        net_delta = comparison[fold]["net_difference_bps_per_eligible_opportunity"][
            "hmm"
        ]
        folds.append(
            {"active_days": active_days, "delta_net_bps_per_opportunity": net_delta}
        )
    positive = comparison["aggregate"]["policies"]["hmm"]["net_bps"] > 0
    advances = positive and all(
        fold["active_days"] >= MIN_DAYS
        and fold["delta_net_bps_per_opportunity"] is not None
        and fold["delta_net_bps_per_opportunity"] >= MIN_DELTA_BPS
        for fold in folds
    )
    return {
        "decision": "ADVANCE" if advances else "DEFER",
        "folds": folds,
        "above_flat": positive,
    }


def compare(bars, request, directory):
    positive, _ = volume_inputs(bars)
    volatility = features(bars)[:, 2]
    indices, simple, hmm, model_evidence = [], [], [], []
    folds = folds_for_window()
    for (train, validation), counted in zip(
        folds, request["coverage_folds"], strict=True
    ):
        signals = np.flatnonzero(positive[validation]) + validation.start
        simple_mask = volatility[signals] >= counted["cutoff"]
        if (
            len(signals) != counted["eligible"]
            or coverage_days(bars, signals, simple_mask, validation) != counted["days"]
        ):
            raise ValueError(
                "The fixed volatility comparison differs from the coverage receipt."
            )
        data = volatility[train.start : validation.stop] * 10_000
        n_train = train.stop - train.start
        model = fit_hmm(data[:n_train], request, directory)
        train_probability = high_state_probabilities(model, data[:n_train])
        posterior_cutoff = cutoff(
            train_probability[positive[train]], request, directory
        )

        def score(values):
            return high_state_probabilities(model, values)

        require_causal_prefix(score, data, validation.start - train.start + 1)
        hmm_mask = score(data)[signals - train.start] >= posterior_cutoff
        indices.append(signals)
        simple.append(simple_mask)
        hmm.append(hmm_mask)
        model_evidence.append(
            {
                "means_volatility_bps": model.means_.ravel().tolist(),
                "variances": model.covars_.ravel().tolist(),
                "transition": model.transmat_.tolist(),
                "start_probability": model.startprob_.tolist(),
                "iterations": model.monitor_.iter,
                "final_likelihood_gain": float(
                    np.diff(list(model.monitor_.history))[-1]
                ),
                "hmm_cutoff": posterior_cutoff,
                "volatility_cutoff": counted["cutoff"],
                "hmm_signal_count": int(hmm_mask.sum()),
                "volatility_signal_count": int(simple_mask.sum()),
                "gate_disagreements": int(np.count_nonzero(hmm_mask != simple_mask)),
            }
        )
    indices = np.concatenate(indices)
    comparison = compare_policies(
        bars,
        indices,
        {
            "hmm": np.concatenate(hmm),
            "rolling_volatility": np.concatenate(simple),
            "unfiltered": np.ones(len(indices)),
            "flat": np.zeros(len(indices)),
        },
        threshold=0,
        reference="rolling_volatility",
        folds=folds,
    )
    return {
        "comparison": comparison,
        "models": model_evidence,
        **paired_decision(comparison),
    }


@unqualified_entry("src.aqrs.m2_e19.worker")
def worker(request, directory):
    stage = request["stage"]
    if stage == "timing":
        (train, validation) = folds_for_window()[-1]
        rng = np.random.default_rng(42)
        count = validation.stop - train.start
        values = rng.normal(
            np.where((np.arange(count) // 60) % 2, 16.0, 4.0), 1, size=count
        )
        model = fit_hmm(values[: train.stop - train.start], request, directory)
        require_causal_prefix(
            lambda sample: high_state_probabilities(model, sample),
            values,
            validation.start - train.start + 1,
        )
        return {"timing_rows": count, "timing_estimator_fits": 1}
    if stage == "coverage":
        return coverage(load_bars(request, directory), request, directory)
    if stage == "compare":
        return compare(load_bars(request, directory), request, directory)
    raise ValueError("Unknown pilot stage.")


def subprocess_git(*arguments):
    return subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=15,
    ).stdout.strip()


def require_admission(path, windows_report=None):
    admission = read_json(path)
    counted = read_json(ROOT / COVERAGE_PATH)
    revision = subprocess_git("rev-parse", "HEAD")
    if (
        not admission.get("reviewer")
        or admission.get("verdict") != "APPROVED"
        or admission.get("revision") != revision
        or admission.get("coverage_id") != fingerprint(counted)
        or subprocess_git("status", "--porcelain")
        or counted.get("work_item") != CAMPAIGN
        or counted.get("decision") != "QUALIFIED"
        or counted["plan"]["dataset_id"] != DATASET_ID
        or counted["outcome"]["execution_status"] != "COMPLETED"
        or counted["outcome"]["completed_fits"] != 2
        or counted["outcome"]["result"]["estimator_fits"] != 0
        or not counted["outcome"]["result"]["passes"]
    ):
        raise ValueError(
            "A clean reviewed revision and its qualifying zero-estimator-fit receipt are required."
        )
    if subprocess_git(
        "ls-remote", "--exit-code", "origin", PUBLICATION_REF
    ).split() != [revision, PUBLICATION_REF]:
        raise ValueError("The exact reviewed outcome revision is not published.")
    if sys.platform == "linux":
        if os.geteuid() == 0 or windows_report is None:
            raise ValueError(
                "Ubuntu replay requires non-root execution and the valid Windows report."
            )
        windows = read_json(windows_report)
        if (
            fingerprint(windows) != admission.get("windows_report_id")
            or windows.get("work_item") != CAMPAIGN
            or windows["source"]["git"]["commit"] != revision
            or not windows["source"]["platform"].startswith("Windows")
            or windows["plan"]["dataset_id"] != DATASET_ID
            or windows["outcome"]["execution_status"] != "COMPLETED"
            or windows["outcome"]["completed_fits"] != 4
        ):
            raise ValueError("The Windows report does not qualify this Ubuntu replay.")
    if version("hmmlearn") != MODEL_VERSION:
        raise ValueError("The fixed hmmlearn version is required.")
    return admission, counted["outcome"]["result"]["folds"]


@unqualified_entry("src.aqrs.m2_e19.run_pilot")
def run_pilot(archives, output, admission_path=None, windows_report=None):
    outcome_stage = admission_path is not None
    admission, coverage_folds = (
        require_admission(admission_path, windows_report)
        if outcome_stage
        else (None, None)
    )
    config, _ = load(ROOT / "configs/research.yaml")
    limits = config["resource_governor"]
    memory_mode = limits["memory_mode"]
    issue = capability(memory_mode)
    if issue:
        raise ValueError(issue)
    candidate = CHALLENGER if outcome_stage else COVERAGE
    stage = "compare" if outcome_stage else "coverage"
    trial_seconds = 60 if outcome_stage else 30
    campaign_seconds = 105 if outcome_stage else 30
    if (
        limits["max_model_fits_per_campaign"] < (7 if outcome_stage else 2)
        or limits["max_research_trials_per_campaign"] < (2 if outcome_stage else 1)
        or (outcome_stage and not limits["preflight"]["measure_representative_pilot"])
        or limits["max_wall_seconds_per_trial"] < trial_seconds
        or limits["max_wall_seconds_per_campaign"] < campaign_seconds
        or limits["max_peak_rss_mb_per_trial"] < 512
    ):
        raise ValueError("The pilot plan exceeds the effective limits.")
    allowlist = d01_archive_rows(read_json(ROOT / D01_PATH))
    training_id = e17_training_id(read_json(ROOT / E17_PATH), allowlist)
    request = {
        "stage": stage,
        "archives": str(archives.resolve()),
        "allowlist": allowlist,
        "training_id": training_id,
        "fit_limit": 4 if outcome_stage else 2,
        "coverage_folds": coverage_folds,
    }
    plan = {
        "candidate_id": candidate,
        "dataset_id": DATASET_ID,
        "training_id": training_id,
        "input_archives": allowlist,
        "planned_trials": 2 if outcome_stage else 1,
        "estimator_fits": 3 if outcome_stage else 0,
        "calibrations": 4 if outcome_stage else 2,
        "max_wall_seconds": campaign_seconds,
        "max_rss_mib": 512,
        "memory_mode": memory_mode,
        "min_days_per_fold": MIN_DAYS,
        "min_entries_per_arm_per_day": MIN_ENTRIES,
        "quantile": QUANTILE,
    }
    if outcome_stage:
        plan.update(
            admission=admission,
            model_parameters=MODEL_PARAMETERS,
            model_version=MODEL_VERSION,
            costs=COSTS,
            min_delta_bps=MIN_DELTA_BPS,
            horizon_bars=HORIZON,
        )
    if output.exists():
        raise FileExistsError(output)
    run_id = uuid4().hex
    if outcome_stage:
        claim_market_attempt(ROOT, allowlist, run_id, campaign=PILOT)
    output.mkdir(parents=True, exist_ok=False)
    source = snapshot(output, Path(__file__), (ROOT / "configs/research.yaml",))
    stamp = datetime.now(UTC).isoformat()
    config["research"]["candidates"] = [{"id": candidate}]
    command = [
        sys.executable,
        "-B",
        str((output / "source/pilot.py").resolve()),
        "--worker",
    ]
    timing = None
    with closing(journal.connect(output / "research.sqlite3")) as db:
        journal.begin(db, run_id, fingerprint(plan), config, plan)
        meta = {
            "evidence_key": fingerprint(plan),
            "source_id": source["source_id"],
            "dataset_id": DATASET_ID,
        }
        journal.start_experiment(db, run_id, candidate, meta)
        deadline = monotonic() + (75 if outcome_stage else 30)
        if outcome_stage:
            timing = supervise(
                output,
                {"stage": "timing", "fit_limit": 1},
                15,
                deadline,
                512,
                command=command,
            )
        if timing is not None and (
            timing["execution_status"] != "COMPLETED"
            or timing["runtime_wall_seconds"]
            * 2
            * limits["preflight"]["runtime_estimate_safety_factor"]
            > trial_seconds
        ):
            outcome = {
                "execution_status": "REJECTED_PREFLIGHT",
                "stop_reason": "The representative timing stage did not qualify the market fit.",
            }
        else:
            outcome = supervise(
                output, request, trial_seconds, deadline, 512, command=command
            )
        result = outcome.get("result", {})
        verdict = "NOT_EVALUATED"
        if outcome["execution_status"] == "COMPLETED":
            verdict = (
                result["decision"]
                if outcome_stage
                else ("QUALIFIED" if result["passes"] else "DEFER")
            )
        report = {
            "work_item": CAMPAIGN,
            "run_id": run_id,
            "timestamp_utc": stamp,
            "plan": plan,
            "source": source,
            "timing": timing,
            "outcome": outcome,
            "decision": verdict,
        }
        journal.finish_experiment(
            db,
            run_id,
            {
                "candidate_id": candidate,
                "experiment_id": f"{run_id}:{candidate}",
                "execution_status": outcome["execution_status"],
                "evidence_status": "INSUFFICIENT_EVIDENCE"
                if result
                else "NOT_EVALUATED",
                "metrics": result,
            },
            meta,
        )
        journal.finish_campaign(db, run_id, outcome["execution_status"], plan)
    write_json(output / ("report.json" if outcome_stage else "coverage.json"), report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--archives", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--admission",
        type=Path,
        help="Review receipt for the frozen outcome comparison.",
    )
    parser.add_argument(
        "--windows-report",
        type=Path,
        help="Completed Windows result for Ubuntu replay.",
    )
    args = parser.parse_args()
    if args.worker:
        run_worker(args.worker, worker)
        return 0
    if args.archives is None or args.output is None:
        parser.error("--archives and --output are required.")
    report = run_pilot(args.archives, args.output, args.admission, args.windows_report)
    print(f"{CAMPAIGN}: {report['decision']}")
    return int(report["decision"] == "NOT_EVALUATED")


if __name__ == "__main__":
    raise SystemExit(main())
