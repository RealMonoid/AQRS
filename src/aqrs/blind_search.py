"""Finite blind-search diagnostic with a publication barrier and no acquisition path."""

import argparse
import json
import math
import re
import secrets
import subprocess
import sys
import time
from hashlib import sha256
from pathlib import Path

import numpy as np

from aqrs import journal
from aqrs.blind_audit import (
    inspect_closure,
    make_verdict,
    summary_text,
    terminal_receipt,
)
from aqrs.blind_evidence import (
    check_storage,
    file_record,
    prediction_status,
    verify_csv,
    write_csv,
    write_features,
)
from aqrs.blind_input import (
    ACTIVITY_COLUMNS,
    qualify_input,
    read_manifest,
    safe_under,
    utc_stamp,
    write_open_fixture,
)
from aqrs.blind_sequence import (
    BRANCH,
    SERIES,
    append_gap,
    assert_owned,
    bind_delivery,
    claim_paths,
    published_state,
    record_once,
    write_once,
)
from aqrs.config import load
from aqrs.governor import supervise
from aqrs.platform_guard import capability
from aqrs.provenance import snapshot
from aqrs.storage import canonical, fingerprint, write_json, write_text
from aqrs.worker import reserve_fit, run

ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATHS = [f"src/aqrs/{path.name}" for path in sorted(Path(__file__).parent.glob("*.py"))] + [
    ".gitattributes", "configs/blind_search.json", "pyproject.toml",
    "configs/research.yaml", "docs/CONTRACTS.md", "docs/RESEARCH_PROTOCOL.md",
]


def load_plan() -> dict:
    return json.loads((ROOT / "configs/blind_search.json").read_text(encoding="utf-8"))


def load_governor() -> dict:
    return load(ROOT / "configs/research.yaml")[0]


def candidates(plan: dict, activity_columns: tuple[str, ...] | list[str] = ()) -> list[dict]:
    singles, pairs = [], []
    for feature in range(6):
        for tail in range(2):
            singles.append({"id": f"S{len(singles) + 1:02}", "terms": [[feature, tail]],
                            "hypothesis": f"The {['low', 'high'][tail]} {plan['features'][feature]} tail changes the next three-minute return."})
    for left, right in plan["pairs"]:
        for tail in range(2):
            pairs.append({"id": f"P{len(pairs) + 1:02}", "terms": [[left, tail], [right, tail]],
                          "hypothesis": f"The joint {['low', 'high'][tail]} {plan['features'][left]} and {plan['features'][right]} tail adds information beyond either parent."})
    tail_slots = []
    for offset, field in enumerate(ACTIVITY_COLUMNS):
        for tail in range(2):
            slot = 2 * offset + tail
            if field in activity_columns:
                name = plan["features"][6 + offset]
                direction = ("low", "high")[tail]
                tail_slots.append({"id": f"T{slot + 1:02}", "terms": [[6 + offset, tail]],
                                   "hypothesis": f"The {direction} {name} tail changes the next three-minute return."})
            else:
                tail_slots.append(pairs[6 + slot])
    return singles[:6] + pairs[:6] + singles[6:] + tail_slots


def available_activity(bars: np.ndarray) -> list[str]:
    return [name for index, name in enumerate(ACTIVITY_COLUMNS, start=6)
            if index < bars.shape[1] and np.isfinite(bars[0, index])]


def features(bars: np.ndarray) -> np.ndarray:
    close, volume = bars[:, 4], bars[:, 5]
    result = np.full(bars.shape, np.nan)
    for column, lag in enumerate((1, 5, 20)):
        result[lag:, column] = (close[lag:] / close[:-lag] - 1) * 10000
    sums = np.concatenate(([0.0], np.cumsum(volume)))
    previous = (sums[20:-1] - sums[:-21]) / 20
    result[20:, 3] = np.divide(volume[20:], previous, out=np.zeros(len(previous)), where=previous != 0)
    spread = bars[:, 2] - bars[:, 3]
    result[:, 4] = spread / close * 10000
    result[:, 5] = np.divide(close - bars[:, 3], spread, out=np.full(len(bars), 0.5), where=spread != 0)
    activity = available_activity(bars)
    if "buy_volume" in activity:
        result[:, 6] = np.divide(bars[:, 6], volume, out=np.zeros(len(bars)), where=volume > 0)
    if "sell_volume" in activity:
        share = np.divide(bars[:, 7], volume, out=np.zeros(len(bars)), where=volume > 0)
        prior = np.lib.stride_tricks.sliding_window_view(share[:-1], 20).mean(axis=1)
        result[20:, 7] = share[20:] - prior
    if "trade_count" in activity:
        trades = bars[:, 8]
        prior = np.lib.stride_tricks.sliding_window_view(trades[:-1], 20).mean(axis=1)
        result[20:, 8] = np.divide(trades[20:], prior, out=np.zeros(len(prior)), where=prior > 0)
    return result


def prepare_arrays(bars: np.ndarray, plan: dict, directory: Path | None = None,
                   feature_path: Path | None = None) -> dict:
    end = int((len(bars) // 1440) * plan["train_fraction"]) * 1440
    values = features(bars)
    activity = available_activity(bars)
    active_indices = list(range(6)) + [6 + ACTIVITY_COLUMNS.index(name) for name in activity]
    cutoffs = [None] * len(plan["features"])
    for fit, column in enumerate(active_indices, start=1):
        if directory is not None:
            reserve_fit({"fit_limit": plan["calibration_fits"]}, directory, plan["calibration_fits"])
        cutoffs[column] = np.quantile(values[20:end, column], plan["quantiles"]).tolist()
        if directory is not None:
            write_json(directory / "fits.json", fit)
    prepared = {"cutoffs": cutoffs, "evaluation_start": end, "evaluation_end": len(bars),
                "train_start": 20, "train_end": end, "calibration_fits": len(active_indices),
                "activity_columns": activity}
    if feature_path is not None:
        prepared["feature_table"] = write_features(feature_path, bars, values, plan, end)
    return prepared


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
            detail: Path | None = None, verify_detail: Path | None = None) -> dict:
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
        decision = "NO_INCREMENTAL_EVIDENCE"
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
    result["parent_gate_failures"] = {
        name: [label for label, passed in {
            "coverage": value["coverage_pass"], "stability": value["stable"],
            "interval_excludes_zero": value["excludes_zero"],
            "same_direction": value["estimate_bps"] is not None and base["estimate_bps"] is not None
            and value["estimate_bps"] * base["estimate_bps"] > 0,
        }.items() if not passed]
        for name, value in contrasts.items() if name != "complement"
    }
    if detail is not None or verify_detail is not None:
        matched = {name: {(row["day"], row["band"]) for row in summary["strata"] if row["matched"]}
                   for name, summary in contrasts.items()}

        def rows():
            for row, index in enumerate(indices):
                group = (int(days[row]), int(bands[row]))
                yield [int(index), utc_stamp(bars[index, 0] + 60), utc_stamp(bars[index + 1, 0]),
                       utc_stamp(bars[index + 4, 0]), int(event[row]),
                       *[int(mask[row]) for mask in controls.values()], outcomes[row], net[row],
                       *group, *[int(group in matched[name]) for name in controls]]

        header = ["signal_index", "available_at", "entry_at", "exit_at", "event", *controls,
                  "gross_long_bps", "candidate_net_bps", "evaluation_day", "utc_band",
                  *[f"{name}_matched" for name in controls]]
        if verify_detail is not None:
            result["opportunity_rows_match"] = verify_csv(verify_detail, header, rows())
        else:
            record = write_csv(detail, header, rows())
            result.update(opportunity_file=record["file"], opportunity_sha256=record["sha256"],
                          opportunity_bytes=record["bytes"])
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
    return {"planned_trials": trials, "planned_fits": plan["calibration_fits"], "predictive_model_fits": 0,
            "resamples": 0, "parallel_trials": 1, "estimated_wall_seconds": estimate,
            "estimate_method": "Sum of enforced worker upper bounds, not extrapolated average speed.",
            "memory_estimate_mb": plan["estimated_rss_mb"], "limits": limits,
            "estimated_run_storage_bytes": plan["estimated_run_storage_mib"] * 1024**2,
            "trial_count_exception": approval is not None, "auto_retry_count": 0}


def authorize(root: Path, approval_path: Path | None, dataset_id: str, dataset_digest: str,
              source: str, plan: dict) -> dict | None:
    if source == "internal_open":
        return None
    if approval_path is None:
        raise ValueError("Owner start authorization is required before input access.")
    inbox = root.absolute() / "artifacts/blind-test/inbox"
    if approval_path.suffix.lower() != ".json" or approval_path.absolute().is_relative_to(inbox):
        raise ValueError("The authorization must be a JSON file outside the blind inbox.")
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
    return git_bytes(*args).decode("utf-8").strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, timeout=20, check=True).stdout


def source_hashes() -> dict:
    return {name: sha256((ROOT / name).read_text(encoding="utf-8").encode()).hexdigest()
            for name in SOURCE_PATHS}


def verify_snapshot(output: Path, hashes: dict) -> None:
    for name, expected in hashes.items():
        if not name.startswith("src/aqrs/"):
            continue
        path = safe_under(output, output / "source/aqrs" / Path(name).name)
        if sha256(path.read_text(encoding="utf-8").encode()).hexdigest() != expected:
            raise ValueError("Execution source snapshot changed.")
    entry = safe_under(output, output / "source/pilot.py")
    if sha256(entry.read_text(encoding="utf-8").encode()).hexdigest() != hashes["src/aqrs/blind_search.py"]:
        raise ValueError("Execution entry snapshot changed.")


def worker_command(output: Path) -> list[str]:
    return [sys.executable, "-B", "-E", str(output / "source/pilot.py"), "worker"]


def publication(registration_dir: Path, revision: str, branch: str, registration: dict) -> None:
    if len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision):
        raise ValueError("Expected an exact publication commit.")
    if branch != BRANCH:
        raise ValueError("Unexpected publication branch.")
    remote = git("ls-remote", "--exit-code", "origin", f"refs/heads/{branch}")
    if remote.split()[0] != revision:
        raise ValueError("Publication revision is not the remote branch head.")
    for name in ("registration.json", "preregistration.jsonl"):
        path = safe_under(registration_dir, registration_dir / name)
        relative = path.relative_to(ROOT).as_posix()
        if name == "preregistration.jsonl":
            matches = git_bytes("show", f"{revision}:{relative}") == path.read_bytes()
        else:
            matches = git("show", f"{revision}:{relative}") == path.read_text(encoding="utf-8").strip()
        if not matches:
            raise ValueError("Published registration differs from local bytes.")
    if source_hashes() != registration["source_hashes"]:
        raise ValueError("Source changed after registration.")
    verify_published_source(revision, registration["source_hashes"])


def verify_published_source(revision: str, hashes: dict) -> None:
    for name, digest in hashes.items():
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


def candidate_ledger(registration: dict, selected: list[dict]) -> str:
    rows = []
    for order, candidate in enumerate(selected):
        rows.append({"attempt_id": registration["attempt_id"], "candidate_id": candidate["id"], "order": order,
                     "hypothesis": candidate["hypothesis"], "rule": candidate, "parameters": registration["prepared"]["cutoffs"],
                     "available_at": "bar close t", "entry": "open[t+1]", "exit": "open[t+4]",
                     "dataset": registration["dataset"], "evaluation": registration["prepared"],
                     "plan_sha256": registration["plan_sha256"], "source_hashes": registration["source_hashes"],
                     "controls": ["complement"] + (["parent_a", "parent_b"] if len(candidate["terms"]) == 2 else []),
                     "metrics": None, "decision": "PENDING", "reason": "Awaiting verified publication and authorized execution.",
                     "budget_allocated_seconds": registration["plan"]["candidate_seconds"], "budget_consumed_seconds": 0,
                     "measurement_rule": "RESEARCH_PROTOCOL.md section 11; plan and source hashes bind exact gates."})
    return "".join(canonical(row) + "\n" for row in rows)


def evaluate_worker(request: dict, directory: Path) -> dict:
    plan = request["plan"]
    output = Path(request["output"])
    if request["stage"] == "prepare":
        manifest, bars, manifest_digest = qualify_input(Path(request["inbox"]), request["dataset_id"], request["source"],
                                                        request.get("expected_digest"), retain_activity=True,
                                                        expected_manifest_sha256=request.get("manifest_sha256"))
        prepared = prepare_arrays(bars, plan, directory, output / "features.csv")
        path = output / "bars.npy"
        np.save(path, bars, allow_pickle=False)
        return {"manifest": manifest, "manifest_sha256": manifest_digest, "prepared": prepared,
                "bars_sha256": file_record(path)["sha256"]}
    path = output / "bars.npy"
    if file_record(path)["sha256"] != request["bars_sha256"]:
        raise ValueError("Qualified data changed after registration.")
    bars = np.load(path, allow_pickle=False)
    if available_activity(bars) != request["prepared"]["activity_columns"]:
        raise ValueError("Staged activity columns do not match registration.")
    pending = safe_under(output, output / "pending-opportunities")
    pending.mkdir(exist_ok=True)
    detail = pending / f"{request['candidate']['id']}-opportunities.csv"
    return measure(bars, request["prepared"], request["candidate"], plan, request["cost_bps"], detail)


def claim_start(root: Path, attempt: str, dataset_id: str, digest: str, approval_path: Path | None, branch: str = BRANCH) -> Path:
    if not re.fullmatch(r"AQRS-B01-[A-Z0-9-]{1,48}", attempt) or attempt == "AQRS-B01-OPEN":
        raise ValueError("Invalid external attempt ID.")
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ValueError("Expected a lowercase SHA-256 dataset digest.")
    token_path, claim_path = claim_paths(root, dataset_id)
    plan = load_plan()
    approval = authorize(root, approval_path, dataset_id, digest, "external_blind", plan)
    if approval["attempt_id"] != attempt:
        raise ValueError("Authorization attempt ID mismatch.")
    config = load_governor()
    config["resource_governor"]["max_wall_seconds_per_campaign"] = min(
        config["resource_governor"]["max_wall_seconds_per_campaign"], approval["max_wall_seconds"])
    preflight(plan, config, len(candidates(plan)), approval)
    state = published_state(git, git_bytes, branch)
    if state["active"] or state["next_id"] != dataset_id:
        raise ValueError("Only the next dataset can be reserved after the preceding verdict is published.")
    hashes = source_hashes()
    if state["first"] and (state["first"]["source_hashes"] != hashes or state["first"]["plan_sha256"] != fingerprint(plan)):
        raise ValueError("The blind series source or plan is frozen.")
    verify_published_source(state["revision"], hashes)
    token = {"token": secrets.token_hex(32)}
    record_once(token_path, token)
    record_once(claim_path, {"schema": "aqrs.blind-start.v1", "dataset_id": dataset_id,
                             "attempt_id": attempt, "dataset_sha256": digest, "created_at": journal.now(),
                             "owner_token_sha256": fingerprint(token), "approval_sha256": fingerprint(approval),
                             "source_hashes": hashes, "plan_sha256": fingerprint(plan),
                             "previous_verdict_sha256": fingerprint(state["previous"]) if state["previous"] else None,
                             "admission_base_revision": state["revision"]})
    return claim_path


def owned_sequence(root: Path, dataset_id: str, attempt: str, approval: dict, branch: str) -> tuple[dict, dict]:
    state = published_state(git, git_bytes, branch)
    return state, assert_owned(root, state, dataset_id, attempt, approval, source_hashes())


def register(root: Path, attempt: str, source: str, dataset_id: str,
             expected_digest: str, approval_path: Path | None, branch: str = BRANCH) -> Path:
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
    delivery = None
    claim = None
    if source == "external_blind":
        state, claim = owned_sequence(root, dataset_id, attempt, approval, branch)
    inbox = safe_under(root, root / ("artifacts/aqrs-b01/rehearsal/input" if source == "internal_open"
                                    else "artifacts/blind-test/inbox"))
    output = safe_under(root, root / "artifacts/aqrs-b01/runs" / attempt)
    check_storage(root, budget)
    if claim:
        manifest, digest = read_manifest(inbox, source)
        delivery = bind_delivery(manifest, digest, dataset_id, state["previous"])
        entry = next(row for row in manifest["datasets"] if row["id"] == dataset_id)
        if entry["sha256"] != expected_digest:
            raise ValueError("Authorized digest does not match the declared dataset.")
    output.mkdir(parents=True, exist_ok=False)
    write_once(output / "gaps.jsonl", "")
    registration_dir = safe_under(root, root / "evidence/blind" / attempt)
    registration_dir.mkdir(parents=True, exist_ok=False)
    hashes = source_hashes()
    execution_source = snapshot(output, Path(__file__))
    verify_snapshot(output, hashes)
    write_json(output / "search-plan.json", {"schema": "aqrs.blind-plan-snapshot.v1", "plan": plan,
                                             "plan_sha256": fingerprint(plan), "source_hashes": hashes,
                                             "source_revision": execution_source["git"]["commit"]})
    write_json(output / "predictions.json", prediction_status(dataset_id))
    overview = {"schema": "aqrs.blind-run.v1", "attempt_id": attempt, "dataset_id": dataset_id,
                "source": source, "execution_status": "PREPARING", "complete": False,
                "delivery": delivery,
                "created_at": journal.now(), "execution_source": execution_source,
                "source_hashes": hashes, "plan_sha256": fingerprint(plan), "configuration": config,
                "budget": budget, "input_files": [], "trials": [],
                "artifacts": {name: file_record(output / name) for name in ("search-plan.json", "predictions.json")}}
    write_json(output / "run-manifest.json", overview)
    if source == "internal_open":
        write_open_fixture(inbox)
    started = time.monotonic()
    receipt = supervise(output, {"stage": "prepare", "inbox": str(inbox), "output": str(output),
                                "source": source, "dataset_id": dataset_id, "plan": plan,
                                "manifest_sha256": delivery["manifest_sha256"] if delivery else None,
                                "expected_digest": expected_digest if source == "external_blind" else None},
                        plan["preparation_seconds"], started + config["resource_governor"]["max_wall_seconds_per_campaign"],
                        config["resource_governor"]["max_peak_rss_mb_per_trial"],
                        command=worker_command(output))
    write_json(output / "preparation.json", receipt)
    overview["artifacts"]["preparation.json"] = file_record(output / "preparation.json")
    overview["preparation"] = {key: value for key, value in receipt.items() if key != "result"}
    if receipt["execution_status"] != "COMPLETED":
        append_gap(output, "preparation", "INCOMPLETE_EXECUTION", receipt["execution_status"])
        overview.update(execution_status=receipt["execution_status"], stopped_at=journal.now(),
                        candidate_resolution="NOT_REGISTERED", untested_candidate_count=len(selected))
        report = dataset_report(dataset_id, source, [], [], receipt["execution_status"])
        report.update(candidate_resolution="NOT_REGISTERED", untested_candidate_count=len(selected))
        report["stop_reason"] = receipt.get("stop_reason")
        write_json(output / "report.json", report)
        overview["artifacts"]["report.json"] = file_record(output / "report.json")
        write_json(output / "run-manifest.json", overview)
        terminal_receipt(output, overview)
        raise ValueError("Preparation stopped; inspect preparation.json. No automatic retry.")
    verify_snapshot(output, hashes)
    data = receipt["result"]
    fits = data["prepared"]["calibration_fits"]
    if not receipt["started_fits"] == receipt["completed_fits"] == fits <= budget["planned_fits"]:
        raise ValueError("Preparation calibration charges do not match registration.")
    full_space = candidates(plan, data["prepared"]["activity_columns"])
    if source == "external_blind":
        selected = full_space
    entry = next(e for e in data["manifest"]["datasets"] if e["id"] == dataset_id)
    if source == "external_blind" and entry["sha256"] != expected_digest:
        raise ValueError("Authorized input digest mismatch.")
    overview["input_files"] = [{"file": "manifest.json", "sha256": data["manifest_sha256"], "verified": True},
                               {"file": entry["file"], "sha256": entry["sha256"], "verified": True}]
    overview["artifacts"]["features.csv"] = data["prepared"]["feature_table"]
    registration = {"schema": "aqrs.blind-registration.v1", "attempt_id": attempt,
                    "dataset_id": dataset_id, "source": source, "dataset_type": "synthetic", "market_evidence": False,
                    "created_at": journal.now(), "plan": plan, "plan_sha256": fingerprint(plan),
                    "source_hashes": hashes, "execution_source": execution_source,
                    "dataset": entry, "prepared": data["prepared"],
                    "delivery": delivery, "start_sha256": fingerprint(claim) if claim else None,
                    "input_files": overview["input_files"], "plan_artifact": overview["artifacts"]["search-plan.json"],
                    "prediction_artifact": overview["artifacts"]["predictions.json"],
                    "preparation_artifact": overview["artifacts"]["preparation.json"],
                    "preparation": overview["preparation"],
                    "bars_sha256": data["bars_sha256"], "budget": budget, "approval": approval,
                    "preparation_wall_seconds": receipt["runtime_wall_seconds"],
                    "preparation_peak_rss_mb": receipt["peak_rss_mb"], "costs": config["costs"],
                    "candidate_ids": [c["id"] for c in selected], "full_space": full_space}
    ledger = registration_dir / "preregistration.jsonl"
    with ledger.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(candidate_ledger(registration, selected))
    registration["preregistration_artifact"] = file_record(ledger)
    write_json(registration_dir / "registration.json", registration)
    overview.update(execution_status="AWAITING_PUBLICATION", registered_candidates=registration["candidate_ids"])
    write_json(output / "run-manifest.json", overview)
    return registration_dir


def execute(root: Path, attempt: str, revision: str, branch: str, approval_path: Path | None) -> dict:
    if not re.fullmatch(r"AQRS-B01-[A-Z0-9-]{1,48}", attempt):
        raise ValueError("Invalid attempt ID.")
    registration_dir = safe_under(root, root / "evidence/blind" / attempt)
    registration_path = safe_under(registration_dir, registration_dir / "registration.json")
    registration = json.loads(registration_path.read_text(encoding="utf-8"))
    if registration["attempt_id"] != attempt:
        raise ValueError("Registration attempt ID mismatch.")
    if registration["source"] == "internal_open" and (attempt != "AQRS-B01-OPEN" or registration["dataset_id"] != "D001"):
        raise ValueError("Only the named open rehearsal is allowed.")
    plan = load_plan()
    approval = authorize(root, approval_path, registration["dataset_id"], registration["dataset"]["sha256"],
                         registration["source"], plan)
    if (approval != registration["approval"] or registration["plan_sha256"] != fingerprint(plan)
            or registration["plan"] != plan):
        raise ValueError("Authorization or frozen plan changed after registration.")
    if approval is not None and approval["attempt_id"] != attempt:
        raise ValueError("Authorization attempt ID mismatch.")
    if registration["source"] == "external_blind":
        state, claim = owned_sequence(root, registration["dataset_id"], attempt, approval, branch)
        if revision != state["revision"] or registration["start_sha256"] != fingerprint(claim):
            raise ValueError("Registration does not match the active published start.")
    full_space = candidates(plan, registration["prepared"]["activity_columns"])
    expected_candidates = full_space
    if registration["source"] == "internal_open":
        expected_candidates = [c for c in expected_candidates if c["id"] in plan["open_rehearsal_candidates"]]
    if (registration["candidate_ids"] != [c["id"] for c in expected_candidates]
            or registration["full_space"] != full_space):
        raise ValueError("Registration does not match the frozen candidate space.")
    publication(registration_dir, revision, branch, registration)
    ledger = safe_under(registration_dir, registration_dir / "preregistration.jsonl")
    if (file_record(ledger) != registration["preregistration_artifact"]
            or ledger.read_bytes() != candidate_ledger(registration, expected_candidates).encode("utf-8")):
        raise ValueError("Published candidate ledger does not match the registered rules.")
    config = load_governor()
    if approval:
        config["resource_governor"]["max_wall_seconds_per_campaign"] = min(
            config["resource_governor"]["max_wall_seconds_per_campaign"], approval["max_wall_seconds"])
    budget = preflight(plan, config, len(registration["candidate_ids"]), approval)
    if budget != registration["budget"]:
        raise ValueError("Budget changed after registration.")
    if config["costs"] != registration["costs"]:
        raise ValueError("Costs changed after registration.")
    output = safe_under(root, root / "artifacts/aqrs-b01/runs" / attempt)
    check_storage(output, budget)
    records = (registration["plan_artifact"], registration["prediction_artifact"],
               registration["preparation_artifact"], registration["prepared"]["feature_table"])
    for record in records:
        if file_record(safe_under(output, output / record["file"])) != record:
            raise ValueError("Pre-run evidence differs from the published registration.")
    with (output / "execution-reservation.json").open("x", encoding="utf-8") as stream:
        stream.write(canonical({"revision": revision, "timestamp": journal.now()}))
    overview = {"schema": "aqrs.blind-run.v1", "attempt_id": attempt, "dataset_id": registration["dataset_id"],
                "source": registration["source"], "execution_status": "RUNNING", "complete": False,
                "delivery": registration["delivery"],
                "created_at": registration["created_at"], "started_at": journal.now(), "registration_revision": revision,
                "registration_sha256": fingerprint(registration),
                "execution_source": registration["execution_source"], "source_hashes": registration["source_hashes"],
                "plan_sha256": registration["plan_sha256"], "configuration": config, "budget": budget,
                "input_files": registration["input_files"], "preparation": registration["preparation"],
                "registered_candidates": registration["candidate_ids"], "trials": [],
                "artifacts": {record["file"]: record for record in records},
                "preregistration": {"path": ledger.relative_to(root).as_posix(), **registration["preregistration_artifact"]}}
    write_json(output / "run-manifest.json", overview)
    selected = expected_candidates
    db = journal.connect(output / "research.sqlite3")
    journal.begin(db, attempt, fingerprint(registration), {"research": {"candidates": selected}}, registration)
    results = []
    status = "COMPLETED"
    consumed = registration["preparation_wall_seconds"]
    deadline = time.monotonic() + budget["limits"]["max_wall_seconds_per_campaign"] - consumed
    started = time.monotonic()
    try:
        for candidate in selected:
            verify_snapshot(output, registration["source_hashes"])
            metadata = {"evidence_key": fingerprint([registration["dataset"], candidate, plan]),
                        "registration_revision": revision, "dataset_type": "synthetic", "market_evidence": False}
            journal.start_experiment(db, attempt, candidate["id"], metadata)
            receipt = supervise(output, {"stage": "candidate", "output": str(output), "plan": plan,
                                        "candidate": candidate, "prepared": registration["prepared"],
                                        "bars_sha256": registration["bars_sha256"],
                                        "cost_bps": round_trip_cost(registration["costs"])},
                                plan["candidate_seconds"], deadline, budget["limits"]["max_peak_rss_mb_per_trial"],
                                command=worker_command(output))
            try:
                verify_snapshot(output, registration["source_hashes"])
                if receipt["execution_status"] == "COMPLETED":
                    result = receipt["result"]
                    name = f"{candidate['id']}-opportunities.csv"
                    staged = safe_under(output, output / "pending-opportunities" / name)
                    record = file_record(staged)
                    if record != {"file": result["opportunity_file"], "sha256": result["opportunity_sha256"],
                                  "bytes": result["opportunity_bytes"]} or (output / name).exists():
                        raise ValueError("Opportunity evidence does not match the completed worker receipt.")
                    staged.replace(output / name)
            except (KeyError, ValueError, OSError):
                receipt.pop("result", None)
                receipt.update(execution_status="FAILED", stop_reason="Source or opportunity evidence verification failed; measurements discarded.")
            result = receipt.pop("result", None)
            row = {"candidate_id": candidate["id"], "effect_claimed": False,
                   "decision": "NOT_EVALUATED", "resource": receipt}
            if result is not None:
                row.update(result)
            results.append(row)
            result_path = output / f"{candidate['id']}-result.json"
            write_json(result_path, row)
            overview["artifacts"][result_path.name] = file_record(result_path)
            overview["trials"].append({"candidate_id": candidate["id"], **receipt})
            if result is not None:
                overview["artifacts"][row["opportunity_file"]] = {"file": row["opportunity_file"],
                                                                  "sha256": row["opportunity_sha256"],
                                                                  "bytes": row["opportunity_bytes"]}
            write_json(output / "run-manifest.json", overview)
            journal.finish_experiment(db, attempt, {
                "experiment_id": f"{attempt}:{candidate['id']}", "candidate_id": candidate["id"],
                "execution_status": receipt["execution_status"], "evidence_status": "INSUFFICIENT_EVIDENCE" if result else "NOT_EVALUATED",
                "metrics": row}, metadata)
            if receipt["execution_status"] != "COMPLETED":
                append_gap(output, "candidate", receipt["execution_status"], candidate["id"])
                status = receipt["execution_status"]
                break
    except (Exception, KeyboardInterrupt) as error:
        status = "CANCELLED" if isinstance(error, KeyboardInterrupt) else "FAILED"
        append_gap(output, "execution", status, type(error).__name__)
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
                      started_fits=registration["prepared"]["calibration_fits"],
                      completed_fits=registration["prepared"]["calibration_fits"], full_search_space=registration["full_space"],
                      activity_columns=registration["prepared"]["activity_columns"],
                      out_of_rehearsal_scope=[c["id"] for c in full_space if c not in selected])
        write_json(output / "report.json", report)
        overview.update(execution_status=status, complete=report["complete"], finished_at=journal.now(),
                        runtime_wall_seconds=report["runtime_wall_seconds"], untested_candidates=untested)
        overview["artifacts"]["report.json"] = file_record(output / "report.json")
        overview["indexed_artifact_bytes"] = sum(record["bytes"] for record in overview["artifacts"].values())
        lines = ["# AQRS-B01 synthetic diagnostic", "", report["interpretation"], "",
                 f"Source: {report['source']}. Complete: {report['complete']}. Effect claimed: {report['effect_claimed']}.",
                 f"Execution: {status}. Registration: {revision}.", ""]
        for row in results:
            lines.append(f"- {row['candidate_id']}: {row['decision']}; details in {row['candidate_id']}-result.json.")
        lines.append(f"\nUntested: {', '.join(untested) or 'none'}. No automatic retry.")
        write_text(output / "report.md", "\n".join(lines) + "\n")
        journal.finish_campaign(db, attempt, status, report)
        db.close()
        write_json(output / "run-manifest.json", overview)
        terminal_receipt(output, overview, bars_digest=registration["bars_sha256"])
    return report


def ledger_payload(root: Path, attempt: str, ledger: dict, revision: str) -> bytes:
    relative = f"evidence/blind/{attempt}/preregistration.jsonl"
    if ledger["path"] != relative or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Invalid candidate ledger reference.")
    path = safe_under(root, root / relative)
    payload = path.read_bytes()
    if (len(payload) != ledger["bytes"] or sha256(payload).hexdigest() != ledger["sha256"]
            or payload != git_bytes("show", f"{revision}:{relative}")):
        raise ValueError("Candidate ledger differs from its published evidence.")
    return payload


def close_dataset(root: Path, attempt: str, dataset_id: str, digest: str, approval_path: Path | None,
                  branch: str = BRANCH) -> list[Path]:
    approval = authorize(root, approval_path, dataset_id, digest, "external_blind", load_plan())
    state, claim = owned_sequence(root, dataset_id, attempt, approval, branch)
    output = safe_under(root, root / "artifacts/aqrs-b01/runs" / attempt)
    terminal_path = safe_under(output, output / "terminal.json")
    if not terminal_path.is_file():
        raise ValueError("No terminal receipt. The dataset remains open and later inputs are blocked.")
    terminal = json.loads(terminal_path.read_text(encoding="utf-8"))
    if terminal["dataset_id"] != dataset_id or terminal["attempt_id"] != attempt or not terminal["delivery"]:
        raise ValueError("Terminal receipt does not match the active dataset and delivery.")
    targets = [safe_under(root, root / SERIES / f"{dataset_id}-{suffix}")
               for suffix in ("verdict.json", "gaps.jsonl", "summary.txt")]
    if any(path.exists() for path in targets):
        raise ValueError("Closure already exists locally. Publish the original records.")
    record_once(safe_under(output, output / "closing-reservation.json"), {"recorded_at": journal.now()})

    def check_ledger(record, revision, registration_digest):
        try:
            git("merge-base", "--is-ancestor", revision, state["revision"])
            registered = json.loads(git_bytes("show", f"{revision}:evidence/blind/{attempt}/registration.json"))
            return fingerprint(registered) == registration_digest and bool(ledger_payload(root, attempt, record, revision))
        except (KeyError, OSError, ValueError, subprocess.SubprocessError):
            return False

    gaps, evidence = inspect_closure(output, terminal, check_ledger)
    verdict = make_verdict(claim, terminal["delivery"], terminal, gaps, evidence)
    summary = summary_text(verdict)
    verdict["summary_sha256"] = sha256(summary.encode("utf-8")).hexdigest()
    write_once(targets[1], "".join(canonical(row) + "\n" for row in gaps))
    write_once(targets[2], summary)
    record_once(targets[0], verdict)
    return targets


def add_correction(root: Path, dataset_id: str, note: str, branch: str = BRANCH) -> Path:
    claim_paths(root, dataset_id)
    state = published_state(git, git_bytes, branch)
    if state["active"] or not state["previous"] or dataset_id > state["previous"]["dataset_id"] or not note.strip():
        raise ValueError("Corrections require a closed dataset and are recorded between datasets.")
    prior = json.loads(git_bytes("show", f"{state['revision']}:{SERIES}/{dataset_id}-verdict.json"))
    path = safe_under(root, root / SERIES / f"C{state['corrections'] + 1:06}-correction.json")
    record_once(path, {"schema": "aqrs.blind-correction.v1", "corrects_dataset_id": dataset_id,
                       "after_dataset_id": state["previous"]["dataset_id"], "verdict_sha256": fingerprint(prior),
                       "recorded_at": journal.now(), "note": note})
    return path


def replay_evidence(root: Path, dataset_id: str, revision: str, identifiers: list[str], branch: str = BRANCH) -> dict:
    claim_paths(root, dataset_id)
    if len(identifiers) != 2 or len(set(identifiers)) != 2 or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Provide the full published verdict revision and two distinct candidate IDs.")
    state = published_state(git, git_bytes, branch)
    git("merge-base", "--is-ancestor", revision, state["revision"])
    verdict = json.loads(git_bytes("show", f"{revision}:{SERIES}/{dataset_id}-verdict.json"))
    plan = load_plan()
    if verdict["source_hashes"] != source_hashes() or verdict["plan_sha256"] != fingerprint(plan):
        raise ValueError("Use the frozen source and plan identified by this verdict.")
    attempt = verdict["attempt_id"]
    output = safe_under(root, root / "artifacts/aqrs-b01/runs" / attempt)
    required = ["bars.npy", "report.json", *[f"{identifier}-opportunities.csv" for identifier in identifiers]]
    for name in required:
        record = verdict["verified_artifacts"].get(name)
        if record is None or file_record(safe_under(output, output / name)) != record:
            raise ValueError("Replay requires the unchanged published evidence for both candidates.")
    rows = ledger_payload(root, attempt, verdict["preregistration"], verdict["registration_revision"])
    registration = json.loads(git_bytes("show", f"{verdict['registration_revision']}:evidence/blind/{attempt}/registration.json"))
    if fingerprint(registration) != verdict["registration_sha256"]:
        raise ValueError("Replay registration differs from the published verdict.")
    cost = round_trip_cost(registration["costs"])
    registered = {row["candidate_id"]: row for row in map(json.loads, rows.splitlines())}
    report = json.loads((output / "report.json").read_text(encoding="utf-8"))
    measured = {row["candidate_id"]: (index, row) for index, row in enumerate(report["results"])}
    bars = np.load(output / "bars.npy", allow_pickle=False)
    comparisons = []
    for identifier in identifiers:
        if identifier not in registered or identifier not in measured:
            raise ValueError("Candidate has no recorded measurement.")
        entry = registered[identifier]
        index, recorded = measured[identifier]
        observed = measure(bars, entry["evaluation"], entry["rule"], plan, cost,
                           verify_detail=output / f"{identifier}-opportunities.csv")
        rows_match = observed.pop("opportunity_rows_match")
        expected = {key: recorded[key] for key in observed}
        keys = ("decision", "event_count", "contrasts", "all_opportunity_net", "round_trip_cost_bps")
        comparisons.append({"candidate_id": identifier, "evidence": f"report.json#/results/{index}",
                            "expected": {key: expected[key] for key in keys},
                            "recomputed": {key: observed[key] for key in keys}, "opportunity_rows_match": rows_match,
                            "matches": rows_match and canonical(observed) == canonical(expected)})
    return {"schema": "aqrs.blind-replay.v1", "dataset_id": dataset_id, "verdict_revision": revision,
            "comparisons": comparisons, "matches": all(row["matches"] for row in comparisons)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["claim", "register-open", "register", "execute", "close", "correct", "replay", "worker"])
    parser.add_argument("worker_directory", nargs="?")
    parser.add_argument("--attempt", default="AQRS-B01-OPEN")
    parser.add_argument("--dataset-id", default="D001")
    parser.add_argument("--dataset-sha256", default="")
    parser.add_argument("--authorization", type=Path)
    parser.add_argument("--published-revision")
    parser.add_argument("--branch", default=BRANCH)
    parser.add_argument("--candidate", action="append", default=[])
    parser.add_argument("--note", default="")
    args = parser.parse_args()
    if args.action == "worker":
        run(Path(args.worker_directory), evaluate_worker)
        return
    try:
        if args.action == "claim":
            path = claim_start(ROOT, args.attempt, args.dataset_id, args.dataset_sha256, args.authorization, args.branch)
            print(f"Publish this start before reading input: {path.relative_to(ROOT)}")
        elif args.action == "close":
            paths = close_dataset(ROOT, args.attempt, args.dataset_id, args.dataset_sha256, args.authorization, args.branch)
            print("Publish the closure files together before opening the next dataset:")
            for path in paths:
                print(path.relative_to(ROOT))
        elif args.action == "correct":
            print(add_correction(ROOT, args.dataset_id, args.note, args.branch).relative_to(ROOT))
        elif args.action == "replay":
            result = replay_evidence(ROOT, args.dataset_id, args.published_revision or "", args.candidate, args.branch)
            print(canonical(result))
            if not result["matches"]:
                raise SystemExit(1)
        elif args.action in {"register", "register-open"}:
            directory = register(ROOT, args.attempt, "internal_open" if args.action == "register-open" else "external_blind",
                                 args.dataset_id, args.dataset_sha256, args.authorization, args.branch)
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
