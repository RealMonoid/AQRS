"""Append-only admission and closure records for the external blind series."""

import json
import re
from hashlib import sha256
from pathlib import Path

from aqrs.blind_input import safe_under
from aqrs.journal import now
from aqrs.storage import canonical, fingerprint

SERIES = "evidence/blind/sequence"
BRANCH = "codex/aqrs-b01-blind-preparation"
RUNS = "artifacts/aqrs-b01/runs"
PARTS = {"start.json", "verdict.json", "gaps.jsonl", "summary.txt"}


def write_once(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def record_once(path: Path, data: dict) -> None:
    write_once(path, canonical(data) + "\n")


def published_state(git, git_bytes, branch: str = BRANCH) -> dict:
    if branch != BRANCH:
        raise ValueError("Unexpected publication branch.")
    revision = git("ls-remote", "--exit-code", "origin", f"refs/heads/{branch}").split()[0]
    if git("rev-parse", "HEAD") != revision:
        raise ValueError("Local HEAD must match the published sequence before admission.")
    names = set(git("ls-tree", "-r", "--name-only", revision, "--", SERIES).splitlines())
    changes = git("log", "--reverse", "--first-parent", "--diff-merges=first-parent", "--format=%H",
                  "--name-status", "--no-renames", revision, "--", SERIES).splitlines()
    groups = []
    seen = set()
    for line in changes:
        if re.fullmatch(r"[0-9a-f]{40}", line):
            groups.append(set())
        elif line:
            if not groups or not line.startswith("A\t") or line[2:] in seen:
                raise ValueError("Published sequence history must be append-only.")
            groups[-1].add(line[2:])
            seen.add(line[2:])
    if seen != names:
        raise ValueError("Published sequence history must be append-only.")
    closed = corrections = 0
    has_active = False
    for group in groups:
        prefix = f"{SERIES}/D{closed + 1:03}-"
        closure = {prefix + part for part in PARTS - {"start.json"}}
        if not has_active and closed < 999 and group == {prefix + "start.json"}:
            has_active = True
        elif has_active and group == closure:
            closed += 1
            has_active = False
        elif not has_active and closed and group == {f"{SERIES}/C{corrections + 1:06}-correction.json"}:
            correction = json.loads(git_bytes("show", f"{revision}:{next(iter(group))}"))
            target = correction["corrects_dataset_id"]
            if (not re.fullmatch(r"D[0-9]{3}", target) or not 1 <= int(target[1:]) <= closed
                    or correction["after_dataset_id"] != f"D{closed:03}"):
                raise ValueError("Published correction does not identify its actual sequence position.")
            original = json.loads(git_bytes("show", f"{revision}:{SERIES}/{target}-verdict.json"))
            if correction["verdict_sha256"] != fingerprint(original):
                raise ValueError("Published correction does not bind the original verdict.")
            corrections += 1
        else:
            raise ValueError("Published sequence commits are out of order or split a closure.")

    def raw(dataset_id, part):
        return git_bytes("show", f"{revision}:{SERIES}/{dataset_id}-{part}")

    def read(index, part):
        return json.loads(raw(f"D{index:03}", part))

    previous = read(closed, "verdict.json") if closed else None
    if previous:
        identity = f"D{closed:03}"
        if (previous["dataset_id"] != identity or previous["verdict"] not in {"EVALUABLE", "NOT_EVALUABLE"}
                or previous["start_sha256"] != fingerprint(read(closed, "start.json"))
                or previous["gaps_sha256"] != sha256(raw(identity, "gaps.jsonl")).hexdigest()
                or previous["summary_sha256"] != sha256(raw(identity, "summary.txt")).hexdigest()):
            raise ValueError("Published closure records do not agree.")
    active = read(closed + 1, "start.json") if has_active else None
    first = read(1, "start.json") if closed or active else None
    return {"revision": revision, "next_id": f"D{closed + 1:03}" if closed < 999 else None,
            "previous": previous, "active": active, "first": first, "corrections": corrections}


def claim_paths(root: Path, dataset_id: str) -> tuple[Path, Path]:
    if not re.fullmatch(r"D[0-9]{3}", dataset_id) or dataset_id == "D000":
        raise ValueError("Expected a dataset ID from D001 through D999.")
    return (safe_under(root, root / "artifacts/aqrs-b01/sequence" / f"{dataset_id}.json"),
            safe_under(root, root / SERIES / f"{dataset_id}-start.json"))


def assert_owned(root: Path, state: dict, dataset_id: str, attempt: str, approval: dict, hashes: dict) -> dict:
    claim = state["active"]
    if state["next_id"] != dataset_id or not claim or claim["dataset_id"] != dataset_id or claim["attempt_id"] != attempt:
        raise ValueError("This dataset has no active published start in sequence.")
    token_path, _ = claim_paths(root, dataset_id)
    if not token_path.is_file():
        raise ValueError("This workspace does not own the published start token.")
    token = json.loads(token_path.read_text(encoding="utf-8"))
    if (claim["owner_token_sha256"] != fingerprint(token) or claim["approval_sha256"] != fingerprint(approval)
            or claim["source_hashes"] != hashes or claim["source_hashes"] != state["first"]["source_hashes"]
            or claim["previous_verdict_sha256"] != (fingerprint(state["previous"]) if state["previous"] else None)):
        raise ValueError("Start ownership, authorization, frozen source or preceding verdict differs.")
    return claim


def bind_delivery(manifest: dict, digest: str, dataset_id: str, previous: dict | None) -> dict:
    rows = manifest["datasets"]
    binding = {"manifest_sha256": digest, "first_dataset_id": rows[0]["id"], "last_dataset_id": rows[-1]["id"]}
    earlier = previous["delivery"] if previous else None
    if earlier and previous["dataset_id"] != earlier["last_dataset_id"]:
        if binding != earlier:
            raise ValueError("Finish the current delivery before changing its manifest.")
    elif binding["first_dataset_id"] != dataset_id:
        raise ValueError("The new delivery must begin with the next dataset ID.")
    if dataset_id not in {row["id"] for row in rows}:
        raise ValueError("The current dataset is absent from this delivery.")
    return binding


def append_gap(output: Path, stage: str, code: str, item: str) -> None:
    with (output / "gaps.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(canonical({"recorded_at": now(), "stage": stage, "code": code, "item": item}) + "\n")
