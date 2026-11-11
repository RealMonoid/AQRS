"""Known-answer engineering fixtures; never load an external blind inbox."""

import json
from pathlib import Path

import numpy as np
import pytest

from aqrs import blind_search as blind
from aqrs.blind_input import qualify, write_open_fixture


@pytest.fixture
def delivery(tmp_path):
    inbox = tmp_path / "input"
    write_open_fixture(inbox)
    return inbox


def test_input_valid_and_tamper_rejected(delivery):
    manifest, arrays = qualify(delivery, "D001", "internal_open")
    assert manifest["source"] == "internal_open"
    assert arrays.shape == (86400, 6)
    with (delivery / "D001.csv").open("a") as stream:
        stream.write("invalid\n")
    with pytest.raises(ValueError, match="digest"):
        qualify(delivery, "D001", "internal_open")


def test_unexpected_file_rejected_before_payload(delivery, monkeypatch):
    (delivery / "forbidden.txt").write_text("Do not read this file.")
    original = Path.read_bytes

    def guard(path):
        assert path.name not in {"forbidden.txt", "D001.csv"}
        return original(path)

    monkeypatch.setattr(Path, "read_bytes", guard)
    with pytest.raises(ValueError, match="allowlist"):
        qualify(delivery, "D001", "internal_open")


def test_only_authorized_payload_is_opened(delivery, monkeypatch):
    manifest_path = delivery / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    second = dict(manifest["datasets"][0], id="D002", file="D002.csv")
    manifest["datasets"].append(second)
    manifest_path.write_text(json.dumps(manifest))
    (delivery / "D002.csv").write_text("This payload is outside the approved dataset.")
    original = Path.read_bytes

    def guard(path):
        assert path.name != "D002.csv"
        return original(path)

    monkeypatch.setattr(Path, "read_bytes", guard)
    qualify(delivery, "D001", "internal_open", manifest["datasets"][0]["sha256"])
    monkeypatch.setattr(Path, "read_bytes", lambda path: pytest.fail("No CSV bytes may be read."))
    with pytest.raises(ValueError, match="Authorized digest"):
        qualify(delivery, "D001", "internal_open", "0" * 64)


@pytest.mark.parametrize("mutation", ["gap", "ohlc", "nan", "header", "calendar"])
def test_invalid_payload_rejected_with_matching_digest(delivery, mutation):
    from hashlib import sha256

    path = delivery / "D001.csv"
    rows = path.read_text().splitlines()
    row = rows[30].split(",")
    if mutation == "gap":
        row[0] = rows[29].split(",")[0]
    elif mutation == "ohlc":
        row[2] = "0.1"
    elif mutation == "nan":
        row[5] = "nan"
    elif mutation == "header":
        rows[0] += ",label"
    else:
        row[0] = "2026-01-06T00:00:00Z"
    rows[30] = ",".join(row)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    manifest = json.loads((delivery / "manifest.json").read_text())
    manifest["datasets"][0]["sha256"] = sha256(path.read_bytes()).hexdigest()
    (delivery / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError):
        qualify(delivery, "D001", "internal_open")


def test_frozen_space_counts_and_past_only_features():
    plan = blind.load_plan()
    space = blind.candidates(plan)
    assert len(space) == len({c["id"] for c in space}) == 24
    assert [c["id"] for c in space[:6]] == [f"S{i:02}" for i in range(1, 7)]
    rng = np.random.default_rng(9)
    bars = np.column_stack((np.arange(1000) * 60, np.ones((1000, 4)), rng.uniform(1, 2, 1000)))
    bars[:, 2] = 1.1
    bars[:, 3] = 0.9
    prior = blind.features(bars)
    bars[700:, 1:] *= 2
    assert np.array_equal(prior[:700], blind.features(bars)[:700], equal_nan=True)


def test_next_open_label_and_costs():
    bars = np.column_stack((np.arange(40) * 60, np.ones((40, 5))))
    bars[21, 1] = 100
    bars[24, 1] = 101
    assert blind.forward_bps(bars, np.array([20]))[0] == pytest.approx(100)
    assert blind.round_trip_cost({"fee_bps_per_side": 4, "quoted_spread_bps": 3,
                                  "slippage_bps_per_side": 2}) == 15


def test_positive_redundant_and_null_known_answers(delivery):
    _, bars = qualify(delivery, "D001", "internal_open")
    plan = blind.load_plan()
    prepared = blind.prepare_arrays(bars, plan)
    catalog = {c["id"]: c for c in blind.candidates(plan)}
    positive = blind.measure(bars, prepared, catalog["S08"], plan, 15)
    redundant = blind.measure(bars, prepared, catalog["P02"], plan, 15)
    assert positive["effect_claimed"]
    assert positive["contrasts"]["complement"]["interval_bps"][0] > 0
    assert not redundant["effect_claimed"]
    assert redundant["decision"] == "NO_INCREMENTAL_EVIDENCE"
    assert redundant["parent_gate_failures"]
    bars[:, 1:5] = 100
    null = blind.measure(bars, blind.prepare_arrays(bars, plan), catalog["S08"], plan, 15)
    assert not null["effect_claimed"]


def test_default_governor_blocks_24_and_missing_approval_before_input(tmp_path):
    plan = blind.load_plan()
    config = blind.load_governor()
    with pytest.raises(ValueError, match="24|trial"):
        blind.preflight(plan, config, 24, None)
    with pytest.raises(ValueError, match="authorization"):
        blind.authorize(tmp_path, None, "D001", "0" * 64, "external_blind", plan)
    config["resource_governor"]["memory_mode"] = "strict"
    with pytest.raises(ValueError, match="strict"):
        blind.preflight(plan, config, 2, None)


def test_calibration_cannot_see_evaluation(delivery):
    _, bars = qualify(delivery, "D001", "internal_open")
    plan = blind.load_plan()
    before = blind.prepare_arrays(bars, plan)
    bars[before["evaluation_start"]:, 5] *= 1000
    after = blind.prepare_arrays(bars, plan)
    assert before["cutoffs"] == after["cutoffs"]


def test_no_claim_on_incomplete_run():
    report = blind.dataset_report("D001", "external_blind", [], ["S01"], "TIMED_OUT")
    assert not report["complete"]
    assert not report["effect_claimed"]
    assert report["market_evidence"] is False


def test_reparse_and_path_escape_rejected(tmp_path):
    from aqrs.blind_input import safe_under

    with pytest.raises(ValueError, match="outside|traversal"):
        safe_under(tmp_path, tmp_path / ".." / "forbidden.csv")


def test_real_link_rejected_before_traversal(tmp_path):
    import sys

    from aqrs.blind_input import safe_under

    target = tmp_path / "target"
    target.mkdir()
    link = tmp_path / "link"
    if sys.platform == "win32":
        import _winapi

        _winapi.CreateJunction(str(target), str(link))
    else:
        link.symlink_to(target, target_is_directory=True)
    with pytest.raises(ValueError, match="Links and reparse"):
        safe_under(tmp_path, link / "data.csv")


def test_copied_attempt_registration_rejected_before_publication(tmp_path, monkeypatch):
    directory = tmp_path / "evidence/blind/AQRS-B01-REPLAY"
    directory.mkdir(parents=True)
    (directory / "registration.json").write_text(json.dumps({"attempt_id": "AQRS-B01-ORIGINAL"}))
    monkeypatch.setattr(blind, "publication", lambda *a: pytest.fail("Publication must not be consulted."))
    with pytest.raises(ValueError, match="Registration attempt ID mismatch"):
        blind.execute(tmp_path, "AQRS-B01-REPLAY", "0" * 40, "codex/aqrs-b01-blind-preparation", None)


def test_publication_rejects_wrong_remote_before_outcomes(tmp_path, monkeypatch):
    monkeypatch.setattr(blind, "git", lambda *args: "1" * 40 + "\trefs/heads/codex/aqrs-b01-blind-preparation")
    with pytest.raises(ValueError, match="remote branch"):
        blind.publication(tmp_path, "0" * 40, "codex/aqrs-b01-blind-preparation", {})


def test_registered_source_mutation_rejected(tmp_path, monkeypatch):
    for name in ("registration.json", "preregistration.jsonl"):
        (tmp_path / name).write_text("{}\n")
    monkeypatch.setattr(blind, "ROOT", tmp_path)
    monkeypatch.setattr(blind, "source_hashes", lambda: {"changed": "hash"})
    monkeypatch.setattr(blind, "git", lambda *args: "1" * 40 if args[0] == "ls-remote" else "{}")
    with pytest.raises(ValueError, match="Source changed"):
        blind.publication(tmp_path, "1" * 40, "codex/aqrs-b01-blind-preparation", {"source_hashes": {}})


def test_data_mutation_rejected_before_measurement(tmp_path, monkeypatch):
    (tmp_path / "bars.npy").write_bytes(b"changed")
    monkeypatch.setattr(blind, "measure", lambda *a, **k: pytest.fail("Measurement must not start."))
    with pytest.raises(ValueError, match="data changed"):
        blind.evaluate_worker({"stage": "candidate", "plan": {}, "output": str(tmp_path),
                               "bars_sha256": "0" * 64}, tmp_path)


def test_execution_snapshot_detects_mutation(tmp_path):
    from aqrs.provenance import snapshot

    snapshot(tmp_path, Path(blind.__file__))
    hashes = blind.source_hashes()
    blind.verify_snapshot(tmp_path, hashes)
    path = tmp_path / "source/aqrs/blind_input.py"
    path.write_text(path.read_text() + "\n# Changed fixture.\n")
    with pytest.raises(ValueError, match="snapshot changed"):
        blind.verify_snapshot(tmp_path, hashes)


def test_subcost_effect_not_removed_by_cost_gate(delivery):
    _, bars = qualify(delivery, "D001", "internal_open")
    bars[:, 1:5] = 100 + (bars[:, 1:5] - 100) / 100
    plan = blind.load_plan()
    candidate = next(c for c in blind.candidates(plan) if c["id"] == "S08")
    result = blind.measure(bars, blind.prepare_arrays(bars, plan), candidate, plan, 15)
    assert result["effect_claimed"]
    assert result["all_opportunity_net"]["interval_bps"][1] < 0


@pytest.mark.parametrize("mutate_source", [False, True])
def test_guarded_registration_and_terminal_stop(tmp_path, monkeypatch, mutate_source):
    import sqlite3

    original_root = blind.ROOT
    for name in blind.SOURCE_PATHS:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text((original_root / name).read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(blind, "ROOT", tmp_path)
    directory = blind.register(tmp_path, "AQRS-B01-OPEN", "internal_open", "D001", "", None)
    registration = json.loads((directory / "registration.json").read_text())
    entries = [json.loads(line) for line in (directory / "preregistration.jsonl").read_text().splitlines()]
    assert len(entries) == 2 and all(row["metrics"] is None for row in entries)
    assert registration["prepared"]["calibration_fits"] == 6
    publication_checked = []
    monkeypatch.setattr(blind, "publication", lambda *args: publication_checked.append(True))

    def stop(*args, **kwargs):
        assert publication_checked
        receipt = {"execution_status": "TIMED_OUT", "started": True, "stop_reason": "Fixture timeout.",
                   "peak_rss_mb": 10, "runtime_wall_seconds": 1, "started_fits": 0, "completed_fits": 0}
        if mutate_source:
            path = tmp_path / "artifacts/aqrs-b01/runs/AQRS-B01-OPEN/source/aqrs/blind_input.py"
            path.write_text(path.read_text() + "\n# Simulated source mutation.\n")
            receipt.update(execution_status="COMPLETED", result={"effect_claimed": True})
        return receipt

    monkeypatch.setattr(blind, "supervise", stop)
    report = blind.execute(tmp_path, "AQRS-B01-OPEN", "1" * 40, "codex/aqrs-b01-blind-preparation", None)
    expected = "FAILED" if mutate_source else "TIMED_OUT"
    assert not report["complete"] and report["execution_status"] == expected
    assert not report["effect_claimed"] and report["started_trials"] == 1
    assert len(report["untested_candidates"]) == 1
    db = sqlite3.connect(tmp_path / "artifacts/aqrs-b01/runs/AQRS-B01-OPEN/research.sqlite3")
    assert {r[0] for r in db.execute("SELECT execution_status FROM experiments")} == {expected, "CANCELLED"}
    db.close()
    with pytest.raises(FileExistsError):
        blind.execute(tmp_path, "AQRS-B01-OPEN", "1" * 40, "codex/aqrs-b01-blind-preparation", None)

