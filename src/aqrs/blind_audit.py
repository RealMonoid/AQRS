"""Close a blind dataset only on auditable evidence and render its short receipt."""

import json
from hashlib import sha256
from pathlib import Path

from aqrs.blind_evidence import file_record
from aqrs.blind_input import safe_under
from aqrs.blind_sequence import append_gap, record_once
from aqrs.journal import now
from aqrs.storage import canonical, fingerprint


def terminal_receipt(output: Path, overview: dict, *, bars_digest: str | None = None) -> None:
    artifacts = dict(overview["artifacts"])
    artifacts["run-manifest.json"] = file_record(output / "run-manifest.json")
    artifacts["gaps.jsonl"] = file_record(output / "gaps.jsonl")
    for name in ("report.md", "research.sqlite3"):
        path = output / name
        if path.is_file():
            artifacts[name] = file_record(path)
    if bars_digest is not None and (output / "bars.npy").is_file():
        record = file_record(output / "bars.npy")
        if record["sha256"] == bars_digest:
            artifacts["bars.npy"] = record
    record_once(output / "terminal.json", {
        "schema": "aqrs.blind-terminal.v1", "attempt_id": overview["attempt_id"],
        "dataset_id": overview["dataset_id"], "execution_status": overview["execution_status"],
        "complete": overview["complete"], "artifacts": artifacts,
        "preregistration": overview.get("preregistration"),
        "registration_revision": overview.get("registration_revision"),
        "registration_sha256": overview.get("registration_sha256"),
        "registered_candidates": overview.get("registered_candidates", []), "finished_at": now(),
        "delivery": overview.get("delivery"),
    })


def inspect_closure(output: Path, terminal: dict, read_published_ledger) -> tuple[list[dict], dict]:
    required = {"search-plan.json", "preparation.json", "features.csv", "predictions.json", "report.json",
                "report.md", "research.sqlite3", "run-manifest.json", "gaps.jsonl", "bars.npy"}
    required.update(f"{identifier}-opportunities.csv" for identifier in terminal["registered_candidates"])
    required.update(f"{identifier}-result.json" for identifier in terminal["registered_candidates"])
    gaps = []
    verified = {}
    for name in sorted(required):
        try:
            path = safe_under(output, output / name)
            record = terminal["artifacts"].get(name)
            if not path.is_file() or record is None:
                gaps.append(("MISSING_EVIDENCE", name))
            elif file_record(path) != record:
                gaps.append(("CHANGED_EVIDENCE", name))
            else:
                verified[name] = record
        except (OSError, ValueError):
            gaps.append(("CHANGED_EVIDENCE", name))
    ledger = terminal["preregistration"]
    if ledger is None:
        gaps.append(("MISSING_EVIDENCE", "preregistration.jsonl"))
    elif not read_published_ledger(ledger, terminal["registration_revision"], terminal["registration_sha256"]):
        gaps.append(("CHANGED_EVIDENCE", "preregistration.jsonl"))
    if not terminal["complete"] or terminal["execution_status"] != "COMPLETED":
        gaps.append(("INCOMPLETE_EXECUTION", terminal["execution_status"]))
    report = json.loads((output / "report.json").read_text(encoding="utf-8")) if "report.json" in verified else {}
    overview = json.loads((output / "run-manifest.json").read_text(encoding="utf-8")) if "run-manifest.json" in verified else {}
    if terminal["complete"] and (len(terminal["registered_candidates"]) != 24
            or [row["candidate_id"] for row in report.get("results", [])] != terminal["registered_candidates"]
            or any(row.get("resource", {}).get("execution_status") != "COMPLETED" for row in report.get("results", []))):
        gaps.append(("INCOMPLETE_CANDIDATE_EVIDENCE", "report.json#/results"))
    gap_rows = []
    prior_gap_bytes = (output / "gaps.jsonl").read_bytes() if "gaps.jsonl" in verified else b""
    for line in prior_gap_bytes.splitlines():
        try:
            row = json.loads(line)
            if (not isinstance(row, dict) or set(row) != {"recorded_at", "stage", "code", "item"}
                    or not all(isinstance(value, str) for value in row.values())):
                raise ValueError("Invalid gap row.")
        except (TypeError, ValueError):
            row = {"recorded_at": now(), "stage": "closure", "code": "INVALID_GAP_LOG", "item": "gaps.jsonl"}
        gap_rows.append(row)
    for code, item in gaps:
        gap_rows.append({"recorded_at": now(), "stage": "closure", "code": code, "item": item})
        if "gaps.jsonl" in verified:
            append_gap(output, "closure", code, item)
    gap_payload = "".join(canonical(row) + "\n" for row in gap_rows).encode("utf-8")
    if gap_payload != prior_gap_bytes or gaps:
        verified.pop("gaps.jsonl", None)
    return gap_rows, {"verified": verified, "report": report, "overview": overview,
                      "gaps_sha256": sha256(gap_payload).hexdigest(), "ledger": ledger}


def closing_facts(evidence: dict, evaluable: bool) -> dict:
    report, overview = evidence["report"], evidence["overview"]
    trials = overview.get("trials", [])
    complete = [trial for trial in trials if trial["execution_status"] == "COMPLETED"]
    kinds = {"price or total-volume single rules": "S", "order-flow single rules": "T", "conjunction rules": "P"}
    counts = {label: sum(row["candidate_id"].startswith(prefix) for row in complete) for label, prefix in kinds.items()}
    best = {}
    if evaluable:
        for name, section, absolute in (("largest_absolute_control_contrast", "complement", True),
                                        ("highest_net_per_opportunity", "all_opportunity_net", False)):
            values = []
            for index, row in enumerate(report["results"]):
                summary = row["contrasts"][section] if absolute else row[section]
                if summary["estimate_bps"] is not None:
                    pointer = f"/results/{index}/" + ("contrasts/" if absolute else "") + section
                    values.append({"candidate_id": row["candidate_id"], "estimate_basis_points": summary["estimate_bps"],
                                   "interval_basis_points": summary["interval_bps"], "evidence": "report.json#" + pointer})
            if values:
                best[name] = max(values, key=lambda row: abs(row["estimate_basis_points"]) if absolute else row["estimate_basis_points"])
    return {"completed_by_kind": counts if overview else None, "best": best,
            "effect_claimed": report.get("effect_claimed") if evaluable else None,
            "claimed_candidates": report.get("claimed_candidates") if evaluable else None,
            "started_trials": report.get("started_trials"), "completed_fits": report.get("completed_fits"),
            "runtime_wall_seconds": overview.get("runtime_wall_seconds"),
            "planned_budget": overview.get("budget")}


def summary_text(verdict: dict) -> str:
    facts = verdict["facts"]
    identity = verdict["dataset_id"]
    verdict_file = f"{identity}-verdict.json"
    gap_file = f"{identity}-gaps.jsonl"
    ledger = verdict["preregistration"]["path"] if verdict["preregistration"] else None
    lines = [f"Dataset {verdict['dataset_id']} — synthetic blind diagnostic",
             f"Verdict: {verdict['verdict']}. Evidence gaps: {verdict['gap_count']}. [{verdict_file}; {gap_file}]",
             f"Local evidence directory: artifacts/aqrs-b01/runs/{verdict['attempt_id']}/",
             f"Published candidate ledger: {ledger}." if ledger else f"Candidate ledger unavailable. [{gap_file}]",
             "Completed candidate rules [run-manifest.json#/trials; published candidate ledger]:"]
    if facts["completed_by_kind"] is None:
        lines.append(f"  Counts unavailable. [{gap_file}]")
    else:
        lines.extend(f"  {label}: {count}" for label, count in facts["completed_by_kind"].items())
    lines.append("Basis point = 0.01 percentage points.")
    if not facts["best"]:
        lines.append(f"Best measurements unavailable for this verdict. [{verdict_file}#/facts/best; {gap_file}]")
    for label, row in facts["best"].items():
        lines.append(f"{label.replace('_', ' ')}: {row['candidate_id']}, {row['estimate_basis_points']:.6g} basis points [{row['evidence']}]")
    lines.append(f"Effect claimed: {facts['effect_claimed']}; candidates: {facts['claimed_candidates']}. [{verdict_file}#/facts; report.json#/effect_claimed and /claimed_candidates]")
    lines.append(f"Used: {facts['started_trials']} trials, {facts['completed_fits']} calibrations, {facts['runtime_wall_seconds']} seconds. [report.json#/started_trials and /completed_fits; run-manifest.json#/runtime_wall_seconds]")
    lines.append("Budget limits and measurements: run-manifest.json#/budget and /trials.")
    lines.append("Local evidence: search-plan.json, features.csv, candidate opportunity files,")
    lines.append(f"predictions.json, report.json and run-manifest.json. [{verdict_file}#/verified_artifacts]")
    lines.append(f"Replay after publication: python -m aqrs.blind_search replay --dataset-id {verdict['dataset_id']} --published-revision REVISION --candidate FIRST --candidate SECOND")
    lines.append("Replace REVISION with the verdict commit and FIRST/SECOND with two measured candidate identifiers.")
    lines.append("Recorded values: report.json#/results; replay prints recorded and recomputed values.")
    assert len(lines) <= 40
    return "\n".join(lines) + "\n"


def make_verdict(claim: dict, delivery: dict, terminal: dict, gap_rows: list[dict], evidence: dict) -> dict:
    evaluable = not gap_rows and terminal["complete"]
    return {"schema": "aqrs.blind-verdict.v1", "dataset_id": claim["dataset_id"], "attempt_id": claim["attempt_id"],
            "verdict": "EVALUABLE" if evaluable else "NOT_EVALUABLE", "closed_at": now(),
            "start_sha256": fingerprint(claim), "source_hashes": claim["source_hashes"],
            "plan_sha256": claim["plan_sha256"], "delivery": delivery,
            "registration_revision": terminal["registration_revision"], "registration_sha256": terminal["registration_sha256"],
            "gap_count": len(gap_rows),
            "gaps_sha256": evidence["gaps_sha256"], "verified_artifacts": evidence["verified"],
            "preregistration": evidence["ledger"], "facts": closing_facts(evidence, evaluable)}
