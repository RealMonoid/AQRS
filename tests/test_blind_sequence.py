"""Offline publication and evidence checks for the sequential blind runner."""

import json
from hashlib import sha256

import pytest

from aqrs import blind_search as blind
from aqrs.blind_input import write_open_fixture
from aqrs.blind_sequence import BRANCH, SERIES, published_state
from aqrs.storage import fingerprint


def test_inbox_authorization_path_rejects_before_file_probe(tmp_path, monkeypatch):
    from pathlib import Path

    path = tmp_path / "artifacts/blind-test/inbox/D002.csv"
    monkeypatch.setattr(Path, "lstat", lambda self: pytest.fail("No file probe is allowed."))
    with pytest.raises(ValueError, match="outside the blind inbox"):
        blind.authorize(tmp_path, path, "D002", "0" * 64, "external_blind", {})


@pytest.mark.parametrize("groups", [
    [["D001-start.json"], ["D001-verdict.json"], ["D001-gaps.jsonl", "D001-summary.txt"]],
    [["D001-start.json", "D001-verdict.json", "D001-gaps.jsonl", "D001-summary.txt"]],
    [["D001-start.json"], ["D002-start.json"], ["D001-verdict.json", "D001-gaps.jsonl", "D001-summary.txt"]],
])
def test_sequence_rejects_bad_commit_order_before_loading_records(groups):
    paths = [f"{SERIES}/{name}" for group in groups for name in group]
    history = "\n".join(line for index, group in enumerate(groups, 1)
                        for line in (f"{index:040x}", *[f"A\t{SERIES}/{name}" for name in group]))
    outputs = {"ls-remote": "a" * 40, "rev-parse": "a" * 40, "ls-tree": "\n".join(paths), "log": history}
    with pytest.raises(ValueError, match="out of order or split a closure"):
        published_state(lambda action, *args: outputs[action], lambda *args: pytest.fail("No record read."))


def test_two_deliveries_with_immutable_verdict_and_replay(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    for name in blind.SOURCE_PATHS:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text((blind.ROOT / name).read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(blind, "ROOT", root)
    remote = tmp_path / "remote.git"
    blind.git("init", "--bare", str(remote))
    blind.git("init", "-b", BRANCH)
    blind.git("config", "user.name", "Synthetic verification")
    blind.git("config", "user.email", "fixture@example.invalid")
    blind.git("config", "core.autocrlf", "true")
    blind.git("remote", "add", "origin", str(remote))

    def publish(paths):
        blind.git("add", "--", *[path.relative_to(root).as_posix() for path in paths])
        blind.git("commit", "-m", "Publish synthetic fixture evidence")
        blind.git("push", "origin", BRANCH)
        return blind.git("rev-parse", "HEAD")

    publish([root / name for name in blind.SOURCE_PATHS])
    inbox = root / "artifacts/blind-test/inbox"
    write_open_fixture(inbox)
    manifest_path = inbox / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["source"] = "external_blind"
    first = manifest["datasets"][0]
    (inbox / "D002.csv").write_bytes((inbox / "D001.csv").read_bytes())
    manifest["datasets"].append({**first, "id": "D002", "file": "D002.csv"})
    delivery = json.dumps(manifest).encode("utf-8")
    manifest_path.write_bytes(delivery)

    def approval(dataset_id, digest):
        attempt = f"AQRS-B01-{dataset_id}"
        auth = root / f"{dataset_id}-authorization.json"
        auth.write_text(json.dumps({"owner_start_approved": True, "approved_trials": 24,
                                    "trial_count_exception": True, "plan_sha256": fingerprint(blind.load_plan()),
                                    "dataset_id": dataset_id, "dataset_sha256": digest, "attempt_id": attempt,
                                    "max_wall_seconds": 300, "owner_instruction": "Synthetic verification only."}),
                        encoding="utf-8")
        return attempt, dataset_id, digest, auth

    one = approval("D001", first["sha256"])
    two = approval("D002", first["sha256"])

    def register(args):
        attempt, dataset_id, digest, auth = args
        return blind.register(root, attempt, "external_blind", dataset_id, digest, auth)

    def execute(args, revision):
        return blind.execute(root, args[0], revision, BRANCH, args[3])

    with pytest.raises(ValueError, match="Only the next dataset"):
        blind.claim_start(root, *two)
    start = blind.claim_start(root, *one)
    with pytest.raises(ValueError, match="no active published start"):
        register(one)
    publish([start])
    token = root / "artifacts/aqrs-b01/sequence/D001.json"
    held_token = token.with_suffix(".held")
    token.rename(held_token)
    with pytest.raises(ValueError, match="does not own"):
        register(one)
    held_token.rename(token)
    prereg = register(one)
    prereg_revision = publish([prereg / "registration.json", prereg / "preregistration.jsonl"])
    with pytest.raises(ValueError, match="No terminal receipt"):
        blind.close_dataset(root, *one)
    result = execute(one, prereg_revision)
    assert result["complete"] and result["started_trials"] == 24
    closure = blind.close_dataset(root, *one)
    with pytest.raises(ValueError, match="Only the next dataset"):
        blind.claim_start(root, *two)
    verdict_path = root / SERIES / "D001-verdict.json"
    first_verdict = verdict_path.read_bytes()
    verdict = json.loads(first_verdict)
    assert verdict["verdict"] == "EVALUABLE" and verdict["gap_count"] == 0
    assert sum(verdict["facts"]["completed_by_kind"].values()) == 24
    summary = (root / SERIES / "D001-summary.txt").read_text(encoding="utf-8")
    assert len(summary.splitlines()) <= 40
    assert "D001-verdict.json" in summary and "D001-gaps.jsonl" in summary
    assert "evidence/blind/AQRS-B01-D001/preregistration.jsonl" in summary
    output_one = root / "artifacts/aqrs-b01/runs" / one[0]
    recorded = json.loads((output_one / "report.json").read_text(encoding="utf-8"))
    for item in verdict["facts"]["best"].values():
        reference = item["evidence"].removeprefix("report.json#/")
        value = recorded
        for part in reference.split("/"):
            value = value[int(part)] if isinstance(value, list) else value[part]
        assert value["estimate_bps"] == item["estimate_basis_points"]
        assert value["interval_bps"] == item["interval_basis_points"]
        assert item["evidence"] in summary
    assert verdict["facts"]["started_trials"] == recorded["started_trials"]
    assert verdict["facts"]["effect_claimed"] == recorded["effect_claimed"]
    closure_revision = publish(closure)
    replay = blind.replay_evidence(root, "D001", closure_revision, ["S01", "P01"])
    assert replay["matches"]
    assert all(row["opportunity_rows_match"] and row["expected"] == row["recomputed"] for row in replay["comparisons"])
    correction = blind.add_correction(root, "D001", "Synthetic correction record.")
    assert json.loads(correction.read_text(encoding="utf-8"))["after_dataset_id"] == "D001"
    publish([correction])

    publish([blind.claim_start(root, *two)])
    manifest_path.write_bytes(delivery + b"\n")
    with pytest.raises(ValueError, match="Finish the current delivery"):
        register(two)
    manifest_path.write_bytes(delivery)
    prereg_two = register(two)
    two_revision = publish([prereg_two / "registration.json", prereg_two / "preregistration.jsonl"])
    monkeypatch.setattr(blind, "supervise", lambda *args, **kwargs: {
        "execution_status": "TIMED_OUT", "started": True, "stop_reason": "Synthetic timeout fixture.",
    })
    assert execute(two, two_revision)["execution_status"] == "TIMED_OUT"
    output = root / "artifacts/aqrs-b01/runs" / two[0]
    (output / "features.csv").unlink()
    (output / "preparation.json").unlink()
    (output / "S01-result.json").unlink()
    closure_two = blind.close_dataset(root, *two)
    verdict_two = json.loads((root / SERIES / "D002-verdict.json").read_text(encoding="utf-8"))
    assert verdict_two["verdict"] == "NOT_EVALUABLE" and verdict_two["facts"]["effect_claimed"] is None
    gap_rows = [json.loads(line) for line in (root / SERIES / "D002-gaps.jsonl").read_text(encoding="utf-8").splitlines()]
    assert {"features.csv", "preparation.json", "S01-result.json"} <= {
        row["item"] for row in gap_rows if row["code"] == "MISSING_EVIDENCE"
    }
    publish(closure_two)

    inbox.rename(root / "finished-delivery")
    write_open_fixture(inbox)
    (inbox / "D001.csv").rename(inbox / "D003.csv")
    digest = sha256((inbox / "D003.csv").read_bytes()).hexdigest()
    new_delivery = {**manifest, "datasets": [{**first, "id": "D003", "file": "D003.csv", "sha256": digest}]}
    manifest_path.write_text(json.dumps(new_delivery), encoding="utf-8")
    three = approval("D003", digest)
    publish([blind.claim_start(root, *three)])
    assert published_state(blind.git, blind.git_bytes)["active"]["dataset_id"] == "D003"
    with pytest.raises(ValueError, match="Preparation stopped"):
        register(three)
    assert verdict_path.read_bytes() == first_verdict
    assert blind.git_bytes("show", f"HEAD:{SERIES}/D001-verdict.json") == first_verdict
    verdict_path.write_bytes(first_verdict + b"\n")
    publish([verdict_path])
    with pytest.raises(ValueError, match="append-only"):
        published_state(blind.git, blind.git_bytes)
