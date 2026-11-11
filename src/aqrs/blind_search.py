"""Finite blind-search diagnostic with a publication barrier and no acquisition path."""

import argparse
import csv
import json
import math
import subprocess
import sys
import time
from hashlib import sha256
from pathlib import Path

import numpy as np

from aqrs import journal
from aqrs.blind_input import qualify, safe_under, utc_stamp, write_open_fixture
from aqrs.config import load
from aqrs.governor import supervise
from aqrs.platform_guard import capability
from aqrs.storage import canonical, fingerprint, write_json, write_text
from aqrs.worker import reserve_fit, run

ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATHS = [
    "src/aqrs/blind_input.py", "src/aqrs/blind_search.py", "src/aqrs/governor.py",
    "src/aqrs/platform_guard.py", "src/aqrs/worker.py", "src/aqrs/journal.py",
    "src/aqrs/storage.py", "src/aqrs/config.py", "configs/blind_search.json",
    "configs/research.yaml", "docs/CONTRACTS.md", "docs/RESEARCH_PROTOCOL.md",
]


def load_plan() -> dict:
    return json.loads((ROOT / "configs/blind_search.json").read_text(encoding="utf-8"))


def load_governor() -> dict:
    return load(ROOT / "configs/research.yaml")[0]


def candidates(plan: dict) -> list[dict]:
    singles, pairs = [], []
    for feature in range(6):
        for tail in range(2):
            singles.append({"id": f"S{len(singles) + 1:02}", "terms": [[feature, tail]],
                            "hypothesis": f"The {['low', 'high'][tail]} {plan['features'][feature]} tail changes the next three-minute return."})
    for left, right in plan["pairs"]:
        for tail in range(2):
            pairs.append({"id": f"P{len(pairs) + 1:02}", "terms": [[left, tail], [right, tail]],
                          "hypothesis": f"The joint {['low', 'high'][tail]} {plan['features'][left]} and {plan['features'][right]} tail adds information beyond either parent."})
    return singles[:6] + pairs[:6] + singles[6:] + pairs[6:]


def features(bars: np.ndarray) -> np.ndarray:
    close, volume = bars[:, 4], bars[:, 5]
    result = np.full((len(bars), 6), np.nan)
    for column, lag in enumerate((1, 5, 20)):
        result[lag:, column] = (close[lag:] / close[:-lag] - 1) * 10000
    sums = np.concatenate(([0.0], np.cumsum(volume)))
    previous = (sums[20:-1] - sums[:-21]) / 20
    result[20:, 3] = np.divide(volume[20:], previous, out=np.zeros(len(previous)), where=previous != 0)
    spread = bars[:, 2] - bars[:, 3]
    result[:, 4] = spread / close * 10000
    result[:, 5] = np.divide(close - bars[:, 3], spread, out=np.full(len(bars), 0.5), where=spread != 0)
    return result


def prepare_arrays(bars: np.ndarray, plan: dict, directory: Path | None = None) -> dict:
    end = int((len(bars) // 1440) * plan["train_fraction"]) * 1440
    values = features(bars)
    cutoffs = []
    for column in range(6):
        if directory is not None:
            reserve_fit({"fit_limit": 6}, directory, 6)
        cutoffs.append(np.quantile(values[20:end, column], plan["quantiles"]).tolist())
        if directory is not None:
            write_json(directory / "fits.json", column + 1)
    return {"cutoffs": cutoffs, "evaluation_start": end, "evaluation_end": len(bars),
            "train_start": 20, "train_end": end, "calibration_fits": 6}


def forward_bps(bars: np.ndarray, indices: np.ndarray) -> np.ndarray:
    return (bars[indices + 4, 1] / bars[indices + 1, 1] - 1) * 10000


def round_trip_cost(costs: dict) -> float:
    return 2 * costs["fee_bps_per_side"] + costs["quoted_spread_bps"] + 2 * costs["slippage_bps_per_side"]


def interval(values: list[float], plan: dict) -> dict:
    from scipy.stats import t

    if not values:
        return {"estimate_bps": None, "interval_bps": None, "blocks": 0}
    mean = float(np.mean(values))
    bounds = None
    if len(values) >= 2:
        critical = float(t.ppf(1 - plan["alpha"] / (2 * plan["endpoint_slots"]), len(values) - 1))
        half = critical * float(np.std(values, ddof=1)) / math.sqrt(len(values))
        bounds = [mean - half, mean + half]
    return {"estimate_bps": mean, "interval_bps": bounds, "blocks": len(values)}


def block_summary(daily: dict[int, float], day_count: int, plan: dict) -> dict:
    blocks = []
    block_ids = []
    for day in range(0, day_count - 1, 2):
        if day in daily and day + 1 in daily:
            blocks.append((daily[day] + daily[day + 1]) / 2)
            block_ids.append(day // 2)
    result = interval(blocks, plan)
    first = [v for i, v in zip(block_ids, blocks) if i < (day_count // 2) // 2]
    second = [v for i, v in zip(block_ids, blocks) if i >= (day_count // 2) // 2]
    means = [float(np.mean(part)) if part else None for part in (first, second)]
    result.update(block_values_bps=blocks, block_ids=block_ids,
                  half_counts=[len(first), len(second)], half_means_bps=means,
                  daily_values_bps={str(k): v for k, v in daily.items()})
    result["coverage_pass"] = len(blocks) >= plan["min_blocks"] and min(len(first), len(second)) >= plan["min_half_blocks"]
    result["stable"] = all(x is not None for x in means) and means[0] * means[1] > 0
    bounds = result["interval_bps"]
    result["excludes_zero"] = bounds is not None and (bounds[0] > 0 or bounds[1] < 0)
    return result


def contrast(outcomes, event, control, days, bands, day_count, plan) -> dict:
    daily = {}
    strata = []
    event_count = control_count = 0
    for day in range(day_count):
        differences = []
        for band in range(3):
            selected = (days == day) & (bands == band)
            left, right = outcomes[selected & event], outcomes[selected & control]
            matched = bool(len(left) and len(right))
            row = {"day": day, "band": band, "events": len(left), "controls": len(right), "matched": matched}
            if matched:
                difference = float(np.mean(left) - np.mean(right))
                row["difference_bps"] = difference
                differences.append(difference)
                event_count += len(left)
                control_count += len(right)
            strata.append(row)
        if differences:
            daily[day] = float(np.mean(differences))
    result = block_summary(daily, day_count, plan)
    result.update(matched_events=event_count, matched_controls=control_count, strata=strata)
    result["coverage_pass"] &= min(event_count, control_count) >= plan["min_per_arm"]
    result["passes"] = result["coverage_pass"] and result["stable"] and result["excludes_zero"]
    return result


def measure(bars: np.ndarray, prepared: dict, candidate: dict, plan: dict, cost_bps: float,
            detail: Path | None = None) -> dict:
    indices = np.arange(20, len(bars) - 4, 4)
    indices = indices[indices >= prepared["evaluation_start"]]
    values = features(bars)[indices]
    atoms = []
    mechanical = []
    for column, tail in candidate["terms"]:
        cutoff = prepared["cutoffs"][column][tail]
        atoms.append(values[:, column] <= cutoff if tail == 0 else values[:, column] >= cutoff)
        mechanical.append({"feature": plan["features"][column], "operator": "<=" if tail == 0 else ">=", "threshold": cutoff})
    event = np.logical_and.reduce(atoms)
    controls = {"complement": ~event}
    if len(atoms) == 2:
        controls.update(parent_a=atoms[0] & ~atoms[1], parent_b=atoms[1] & ~atoms[0])
    outcomes = forward_bps(bars, indices)
    days = (indices - prepared["evaluation_start"]) // 1440
    bands = (indices % 1440) // 480
    day_count = (len(bars) - prepared["evaluation_start"]) // 1440
    contrasts = {name: contrast(outcomes, event, control, days, bands, day_count, plan)
                 for name, control in controls.items()}
    base = contrasts["complement"]
    if not base["coverage_pass"]:
        decision = "INSUFFICIENT_COVERAGE"
    elif not base["stable"]:
        decision = "UNSTABLE"
    elif not base["excludes_zero"]:
        decision = "BELOW_THRESHOLD"
    elif any(not value["passes"] or value["estimate_bps"] * base["estimate_bps"] <= 0
             for value in contrasts.values()):
        decision = "EXPLAINED_BY_SIMPLER_CONDITION"
    else:
        decision = "EFFECT_CLAIMED"
    net = np.where(event, outcomes - cost_bps, 0)
    net_daily = {day: float(np.mean(net[days == day])) for day in range(day_count) if np.any(days == day)}
    net_summary = block_summary(net_daily, day_count, plan)
    result = {"candidate_id": candidate["id"], "mechanical_rule": {"all": mechanical},
              "decision": decision, "effect_claimed": decision == "EFFECT_CLAIMED",
              "rationale": "Fixed coverage, stability, simultaneous interval and parent-control gates.",
              "contrasts": contrasts, "eligible_opportunities": len(indices),
              "event_count": int(event.sum()), "skipped_opportunities": int((~event).sum()),
              "conditional_event_gross_bps": float(np.mean(outcomes[event])) if event.any() else None,
              "all_opportunity_net": net_summary, "no_trade_bps": 0,
              "round_trip_cost_bps": cost_bps, "market_evidence": False,
              "uncertainty_assumption": "Stable, sufficiently independent two-day block means; not verified for arbitrary generators."}
    if detail is not None:
        with detail.open("x", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerow(["signal_index", "available_at", "entry_at", "exit_at", "event",
                             *controls, "gross_long_bps", "candidate_net_bps"])
            for row, index in enumerate(indices):
                writer.writerow([int(index), utc_stamp(bars[index, 0] + 60), utc_stamp(bars[index + 1, 0]),
                                 utc_stamp(bars[index + 4, 0]), int(event[row]),
                                 *[int(mask[row]) for mask in controls.values()], outcomes[row], net[row]])
        result["opportunity_file"] = detail.name
        result["opportunity_sha256"] = sha256(detail.read_bytes()).hexdigest()
    return result


def preflight(plan: dict, config: dict, trials: int, approval: dict | None) -> dict:
    limits = config["resource_governor"]
    issue = capability(limits["memory_mode"])
    if issue:
        raise ValueError(issue)
    cap = limits["max_research_trials_per_campaign"]
    if approval is not None:
        if approval.get("approved_trials") != 24 or approval.get("trial_count_exception") is not True:
            raise ValueError("An explicit 24-trial exception is required.")
        cap = 24
    if trials > cap:
        raise ValueError("24 trials exceed the unchanged default trial limit; owner approval is required.")
    estimate = plan["preparation_seconds"] + trials * plan["candidate_seconds"]
    if (plan["calibration_fits"] > limits["max_model_fits_per_campaign"]
            or estimate > limits["max_wall_seconds_per_campaign"]
            or plan["estimated_rss_mb"] > limits["max_peak_rss_mb_per_trial"]
            or plan["preparation_seconds"] > limits["max_wall_seconds_per_trial"]
            or plan["candidate_seconds"] > limits["max_wall_seconds_per_trial"]):
        raise ValueError("Full plan exceeds a configured Governor limit.")
    return {"planned_trials": trials, "planned_fits": 6, "predictive_model_fits": 0,
            "resamples": 0, "parallel_trials": 1, "estimated_wall_seconds": estimate,
            "estimate_method": "Sum of enforced worker upper bounds, not extrapolated average speed.",
            "memory_estimate_mb": plan["estimated_rss_mb"], "limits": limits,
            "trial_count_exception": approval is not None, "auto_retry_count": 0}


def authorize(root: Path, approval_path: Path | None, dataset_id: str, dataset_digest: str,
              source: str, plan: dict) -> dict | None:
    if source == "internal_open":
        return None
    if approval_path is None:
        raise ValueError("Owner start authorization is required before input access.")
    path = safe_under(root, approval_path)
    if path.stat().st_size > 16384:
        raise ValueError("Authorization record is too large.")
    approval = json.loads(path.read_text(encoding="utf-8"))
    required = {"owner_start_approved", "approved_trials", "trial_count_exception", "plan_sha256",
                "dataset_id", "dataset_sha256", "attempt_id", "max_wall_seconds", "owner_instruction"}
    if set(approval) != required or approval["owner_start_approved"] is not True:
        raise ValueError("Invalid owner authorization record.")
    if (approval["dataset_id"] != dataset_id or approval["dataset_sha256"] != dataset_digest
            or approval["plan_sha256"] != fingerprint(plan)
            or type(approval["max_wall_seconds"]) is not int or not 1 <= approval["max_wall_seconds"] <= 300
            or not isinstance(approval["owner_instruction"], str) or not approval["owner_instruction"].strip()):
        raise ValueError("Owner authorization does not match this dataset and frozen plan.")
    return approval


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                            encoding="utf-8", timeout=20, check=True)
    return result.stdout.strip()


def source_hashes() -> dict:
    return {name: sha256((ROOT / name).read_text(encoding="utf-8").encode()).hexdigest()
            for name in SOURCE_PATHS}


def publication(registration_dir: Path, revision: str, branch: str, registration: dict) -> None:
    if len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision):
        raise ValueError("Expected an exact publication commit.")
    if branch != "codex/aqrs-b01-blind-preparation":
        raise ValueError("Unexpected publication branch.")
    remote = git("ls-remote", "--exit-code", "origin", f"refs/heads/{branch}")
    if remote.split()[0] != revision:
        raise ValueError("Publication revision is not the remote branch head.")
    for name in ("registration.json", "preregistration.jsonl"):
        path = registration_dir / name
        relative = path.relative_to(ROOT).as_posix()
        if git("show", f"{revision}:{relative}") != path.read_text(encoding="utf-8").strip():
            raise ValueError("Published registration differs from local bytes.")
    if source_hashes() != registration["source_hashes"]:
        raise ValueError("Source changed after registration.")
    for name, digest in registration["source_hashes"].items():
        published = git("show", f"{revision}:{name}") + "\n"
        if sha256(published.encode()).hexdigest() != digest:
            raise ValueError("Registered source was not published in the same revision.")


def dataset_report(dataset_id: str, source: str, results: list, untested: list,
                   status: str) -> dict:
    complete = status == "COMPLETED" and not untested
    return {"dataset_id": dataset_id, "dataset_type": "synthetic", "source": source,
            "market_evidence": False, "execution_status": status, "complete": complete,
            "effect_claimed": any(row.get("effect_claimed", False) for row in results),
            "claimed_candidates": [r["candidate_id"] for r in results if r.get("effect_claimed")],
            "results": results, "untested_candidates": untested,
            "interpretation": "Synthetic diagnostic only; incomplete is not a completed null. No real-world alpha has been demonstrated."}


def evaluate_worker(request: dict, directory: Path) -> dict:
    plan = request["plan"]
    output = Path(request["output"])
    if request["stage"] == "prepare":
        manifest, bars = qualify(Path(request["inbox"]), request["dataset_id"], request["source"])
        prepared = prepare_arrays(bars, plan, directory)
        path = output / "bars.npy"
        np.save(path, bars, allow_pickle=False)
        return {"manifest": manifest, "prepared": prepared, "bars_sha256": sha256(path.read_bytes()).hexdigest()}
    path = output / "bars.npy"
    if sha256(path.read_bytes()).hexdigest() != request["bars_sha256"]:
        raise ValueError("Qualified data changed after registration.")
    bars = np.load(path, allow_pickle=False)
    detail = output / f"{request['candidate']['id']}-opportunities.csv"
    return measure(bars, request["prepared"], request["candidate"], plan, request["cost_bps"], detail)


def register(root: Path, attempt: str, source: str, dataset_id: str,
             expected_digest: str, approval_path: Path | None) -> Path:
    import re

    if not re.fullmatch(r"AQRS-B01-[A-Z0-9-]{1,48}", attempt):
        raise ValueError("Invalid attempt ID.")
    plan, config = load_plan(), load_governor()
    approval = authorize(root, approval_path, dataset_id, expected_digest, source, plan)
    if approval and approval["attempt_id"] != attempt:
        raise ValueError("Authorization attempt ID mismatch.")
    if approval:
        config["resource_governor"]["max_wall_seconds_per_campaign"] = min(
            config["resource_governor"]["max_wall_seconds_per_campaign"], approval["max_wall_seconds"])
    selected = candidates(plan)
    if source == "internal_open":
        if attempt != "AQRS-B01-OPEN" or dataset_id != "D001":
            raise ValueError("Only the named open rehearsal is allowed.")
        selected = [c for c in selected if c["id"] in plan["open_rehearsal_candidates"]]
    budget = preflight(plan, config, len(selected), approval)
    inbox = safe_under(root, root / ("artifacts/aqrs-b01/rehearsal/input" if source == "internal_open"
                                    else "artifacts/blind-test/inbox"))
    output = safe_under(root, root / "artifacts/aqrs-b01/runs" / attempt)
    output.mkdir(parents=True, exist_ok=False)
    registration_dir = safe_under(root, root / "evidence/blind" / attempt)
    registration_dir.mkdir(parents=True, exist_ok=False)
    if source == "internal_open":
        write_open_fixture(inbox)
    started = time.monotonic()
    receipt = supervise(output, {"stage": "prepare", "inbox": str(inbox), "output": str(output),
                                "source": source, "dataset_id": dataset_id, "plan": plan},
                        plan["preparation_seconds"], started + config["resource_governor"]["max_wall_seconds_per_campaign"],
                        config["resource_governor"]["max_peak_rss_mb_per_trial"],
                        command=[sys.executable, "-B", "-m", "aqrs.blind_search", "worker"])
    write_json(output / "preparation.json", receipt)
    if receipt["execution_status"] != "COMPLETED":
        raise ValueError("Preparation stopped; inspect preparation.json. No automatic retry.")
    data = receipt["result"]
    entry = next(e for e in data["manifest"]["datasets"] if e["id"] == dataset_id)
    if source == "external_blind" and entry["sha256"] != expected_digest:
        raise ValueError("Authorized input digest mismatch.")
    registration = {"schema": "aqrs.blind-registration.v1", "attempt_id": attempt,
                    "dataset_id": dataset_id, "source": source, "dataset_type": "synthetic", "market_evidence": False,
                    "created_at": journal.now(), "plan": plan, "plan_sha256": fingerprint(plan),
                    "source_hashes": source_hashes(), "dataset": entry, "prepared": data["prepared"],
                    "bars_sha256": data["bars_sha256"], "budget": budget, "approval": approval,
                    "preparation_wall_seconds": receipt["runtime_wall_seconds"],
                    "preparation_peak_rss_mb": receipt["peak_rss_mb"], "costs": config["costs"],
                    "candidate_ids": [c["id"] for c in selected], "full_space": candidates(plan)}
    entries = []
    for order, candidate in enumerate(selected):
        entries.append({"attempt_id": attempt, "candidate_id": candidate["id"], "order": order,
                        "hypothesis": candidate["hypothesis"], "rule": candidate, "parameters": data["prepared"]["cutoffs"],
                        "available_at": "bar close t", "entry": "open[t+1]", "exit": "open[t+4]",
                        "dataset": entry, "evaluation": data["prepared"], "plan_sha256": fingerprint(plan),
                        "source_hashes": registration["source_hashes"],
                        "controls": ["complement"] + (["parent_a", "parent_b"] if len(candidate["terms"]) == 2 else []),
                        "metrics": None, "decision": "PENDING", "reason": "Awaiting verified publication and authorized execution.",
                        "budget_allocated_seconds": plan["candidate_seconds"], "budget_consumed_seconds": 0,
                        "measurement_rule": "RESEARCH_PROTOCOL.md section 11; plan and source hashes bind exact gates."})
    write_json(registration_dir / "registration.json", registration)
    write_text(registration_dir / "preregistration.jsonl", "".join(canonical(row) + "\n" for row in entries))
    return registration_dir


def execute(root: Path, attempt: str, revision: str, branch: str, approval_path: Path | None) -> dict:
    registration_dir = safe_under(root, root / "evidence/blind" / attempt)
    registration = json.loads((registration_dir / "registration.json").read_text(encoding="utf-8"))
    plan = load_plan()
    approval = authorize(root, approval_path, registration["dataset_id"], registration["dataset"]["sha256"],
                         registration["source"], plan)
    if approval != registration["approval"] or registration["plan_sha256"] != fingerprint(plan):
        raise ValueError("Authorization or frozen plan changed after registration.")
    publication(registration_dir, revision, branch, registration)
    config = load_governor()
    if approval:
        config["resource_governor"]["max_wall_seconds_per_campaign"] = min(
            config["resource_governor"]["max_wall_seconds_per_campaign"], approval["max_wall_seconds"])
    budget = preflight(plan, config, len(registration["candidate_ids"]), approval)
    if budget != registration["budget"]:
        raise ValueError("Budget changed after registration.")
    output = safe_under(root, root / "artifacts/aqrs-b01/runs" / attempt)
    with (output / "execution-reservation.json").open("x", encoding="utf-8") as stream:
        stream.write(canonical({"revision": revision, "timestamp": journal.now()}))
    selected = [c for c in candidates(plan) if c["id"] in registration["candidate_ids"]]
    db = journal.connect(output / "research.sqlite3")
    journal.begin(db, attempt, fingerprint(registration), {"research": {"candidates": selected}}, registration)
    results = []
    status = "COMPLETED"
    consumed = registration["preparation_wall_seconds"]
    deadline = time.monotonic() + budget["limits"]["max_wall_seconds_per_campaign"] - consumed
    started = time.monotonic()
    try:
        for candidate in selected:
            metadata = {"evidence_key": fingerprint([registration["dataset"], candidate, plan]),
                        "registration_revision": revision, "dataset_type": "synthetic", "market_evidence": False}
            journal.start_experiment(db, attempt, candidate["id"], metadata)
            receipt = supervise(output, {"stage": "candidate", "output": str(output), "plan": plan,
                                        "candidate": candidate, "prepared": registration["prepared"],
                                        "bars_sha256": registration["bars_sha256"],
                                        "cost_bps": round_trip_cost(registration["costs"])},
                                plan["candidate_seconds"], deadline, budget["limits"]["max_peak_rss_mb_per_trial"],
                                command=[sys.executable, "-B", "-m", "aqrs.blind_search", "worker"])
            result = receipt.pop("result", None)
            row = {"candidate_id": candidate["id"], "effect_claimed": False,
                   "decision": "NOT_EVALUATED", "resource": receipt}
            if result is not None:
                row.update(result)
            results.append(row)
            write_json(output / f"{candidate['id']}-result.json", row)
            journal.finish_experiment(db, attempt, {
                "experiment_id": f"{attempt}:{candidate['id']}", "candidate_id": candidate["id"],
                "execution_status": receipt["execution_status"], "evidence_status": "INSUFFICIENT_EVIDENCE" if result else "NOT_EVALUATED",
                "metrics": row}, metadata)
            if receipt["execution_status"] != "COMPLETED":
                status = receipt["execution_status"]
                break
    except (Exception, KeyboardInterrupt) as error:
        status = "CANCELLED" if isinstance(error, KeyboardInterrupt) else "FAILED"
        write_json(output / "failure.json", {"type": type(error).__name__, "reason": str(error)})
    finally:
        untested = [c["id"] for c in selected if c["id"] not in {r["candidate_id"] for r in results}]
        with db:
            db.execute("UPDATE experiments SET execution_status = 'CANCELLED', evidence_status = 'NOT_EVALUATED' WHERE run_id = ? AND execution_status IN ('RUNNING','PROPOSED')", (attempt,))
        report = dataset_report(registration["dataset_id"], registration["source"], results, untested, status)
        report.update(attempt_id=attempt, registration_revision=revision,
                      source_hashes=registration["source_hashes"], dataset=registration["dataset"],
                      plan_sha256=registration["plan_sha256"], budget=budget,
                      runtime_wall_seconds=consumed + time.monotonic() - started,
                      started_trials=sum(r["resource"]["started"] for r in results),
                      started_fits=6, completed_fits=6, full_search_space=registration["full_space"],
                      out_of_rehearsal_scope=[c["id"] for c in candidates(plan) if c not in selected])
        write_json(output / "report.json", report)
        lines = ["# AQRS-B01 synthetic diagnostic", "", report["interpretation"], "",
                 f"Source: {report['source']}. Complete: {report['complete']}. Effect claimed: {report['effect_claimed']}.",
                 f"Execution: {status}. Registration: {revision}.", ""]
        for row in results:
            lines.append(f"- {row['candidate_id']}: {row['decision']}; details in {row['candidate_id']}-result.json.")
        lines.append(f"\nUntested: {', '.join(untested) or 'none'}. No automatic retry.")
        write_text(output / "report.md", "\n".join(lines) + "\n")
        journal.finish_campaign(db, attempt, status, report)
        db.close()
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["register-open", "register", "execute", "worker"])
    parser.add_argument("worker_directory", nargs="?")
    parser.add_argument("--attempt", default="AQRS-B01-OPEN")
    parser.add_argument("--dataset-id", default="D001")
    parser.add_argument("--dataset-sha256", default="")
    parser.add_argument("--authorization", type=Path)
    parser.add_argument("--published-revision")
    parser.add_argument("--branch", default="codex/aqrs-b01-blind-preparation")
    args = parser.parse_args()
    if args.action == "worker":
        run(Path(args.worker_directory), evaluate_worker)
        return
    try:
        if args.action in {"register", "register-open"}:
            directory = register(ROOT, args.attempt, "internal_open" if args.action == "register-open" else "external_blind",
                                 args.dataset_id, args.dataset_sha256, args.authorization)
            print(f"Registered without outcomes: {directory.relative_to(ROOT)}. Publish before execution.")
        else:
            if not args.published_revision:
                raise ValueError("A verified publication revision is required.")
            report = execute(ROOT, args.attempt, args.published_revision, args.branch, args.authorization)
            print(canonical({key: report[key] for key in ("attempt_id", "execution_status", "complete", "effect_claimed")}))
            if report["execution_status"] != "COMPLETED":
                raise SystemExit(1)
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(f"STOP: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
