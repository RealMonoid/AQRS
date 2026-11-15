# Explicit __wrapped__ calls below test preserved inner algorithms; FR-005 entry tests use the guarded functions.
"""Known-answer engineering fixtures; never load an external blind inbox."""

import json
from hashlib import sha256
from itertools import combinations
from pathlib import Path

import numpy as np
import pytest

from aqrs import blind_search as blind
from aqrs.blind_input import ACTIVITY_COLUMNS, qualify, write_open_fixture


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


def rewrite_csv(delivery, lines):
    path = delivery / "D001.csv"
    payload = ("\n".join(lines) + "\n").encode("utf-8")
    path.write_bytes(payload)
    manifest_path = delivery / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256(payload).hexdigest()
    manifest["datasets"][0]["sha256"] = digest
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return digest, len(payload)


def test_all_minute_activity_fields_preserve_the_search_input(delivery):
    _, original = qualify(delivery, "D001", "internal_open")
    rows = (delivery / "D001.csv").read_text(encoding="utf-8").splitlines()
    rows[0] += ",buy_volume,sell_volume,trade_count"
    for index in range(1, len(rows)):
        volume = float(rows[index].rsplit(",", 1)[1])
        buy = volume * 0.4
        rows[index] += f",{buy:.40f},{volume - buy:.40f},9007199254740991"
    digest, size = rewrite_csv(delivery, rows)
    assert 12 * 1024**2 < size <= 16 * 1024**2
    _, augmented = qualify(delivery, "D001", "internal_open", digest)
    np.testing.assert_array_equal(augmented, original)


def test_partial_minute_activity_header_is_accepted(delivery):
    rows = (delivery / "D001.csv").read_text(encoding="utf-8").splitlines()
    digest, _ = rewrite_csv(delivery, [rows[0] + ",sell_volume,trade_count"] +
                            [row + ",0.5,7" for row in rows[1:]])
    _, bars = qualify(delivery, "D001", "internal_open", digest)
    assert bars.shape == (86400, 6)
    _, staged = qualify(delivery, "D001", "internal_open", digest, retain_activity=True)
    assert np.isnan(staged[:, 6]).all()
    assert np.all(staged[:, 7] == 0.5) and np.all(staged[:, 8] == 7)


def test_order_flow_slot_allocation_for_every_header_subset():
    plan = blind.load_plan()
    for size in range(4):
        for present in combinations(ACTIVITY_COLUMNS, size):
            selected = blind.candidates(plan, present)
            assert len({row["id"] for row in selected}) == 24
            for index, field in enumerate(ACTIVITY_COLUMNS):
                expected = ([f"T{2 * index + n:02}" for n in (1, 2)] if field in present
                            else [f"P{2 * index + n:02}" for n in (7, 8)])
                assert [row["id"] for row in selected[18 + 2 * index:20 + 2 * index]] == expected


def test_order_flow_features_and_training_are_causal():
    bars = np.ones((2880, 9))
    bars[:, 5:9] = [10, 4, 6, 8]
    bars[20, 6:9] = [7, 3, 12]
    bars[21, 5:9] = 0
    features = blind.features(bars)
    np.testing.assert_allclose(features[20, 6:], [0.7, -0.3, 1.5])
    np.testing.assert_allclose(features[21, 6:], [0, -0.585, 0])
    future = bars.copy()
    future[1440:, 6:9] = [0, 10, 1]
    np.testing.assert_array_equal(blind.features(future)[:1440], features[:1440])
    plan = {**blind.load_plan(), "train_fraction": 0.5}
    assert blind.prepare_arrays(bars, plan) == blind.prepare_arrays(future, plan)
    no_history = bars.copy()
    no_history[:20, 8] = 0
    assert blind.features(no_history)[20, 8] == 0



def test_blind_registration_stops_before_input_or_calibration(tmp_path, monkeypatch):
    from aqrs.admission import AdmissionRejected
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(blind, "supervise", lambda *a, **k: pytest.fail("Unqualified calibration"))
    with pytest.raises(AdmissionRejected, match="not qualified"):
        blind.register(tmp_path, "AQRS-B01-OPEN", "internal_open", "D001", "", None)
    assert not (tmp_path / "artifacts/aqrs-b01/runs").exists()


def test_storage_rejection_precedes_input(tmp_path, monkeypatch):
    from types import SimpleNamespace

    monkeypatch.setattr("aqrs.blind_evidence.shutil.disk_usage", lambda path: SimpleNamespace(free=1))
    with pytest.raises(ValueError, match="Insufficient disk space"):
        blind.register.__wrapped__(tmp_path, "AQRS-B01-OPEN", "internal_open", "D001", "", None)
    assert not (tmp_path / "artifacts").exists()


@pytest.mark.parametrize(("header", "values", "reason"), [
    (",sell_volume,buy_volume", ",0.5,0.5", "header"),
    (",trade_count,trade_count", ",1,1", "header"),
    (",buy_volume,trade_count", ",0.5", "field count"),
    (",buy_volume", ",nan", "side volume"),
    (",sell_volume", ",-0.5", "side volume"),
    (",sell_volume", ",3", "side volume"),
    (",buy_volume,sell_volume", ",0,0", "sum"),
    (",trade_count", ",1.0", "trade count"),
    (",trade_count", ",9007199254740992", "trade count"),
    (",trade_count", ",", "trade count"),
])
def test_invalid_minute_activity_rejected_with_matching_digest(delivery, header, values, reason):
    rows = (delivery / "D001.csv").read_text(encoding="utf-8").splitlines()
    rows[0] += header
    rows[1] += values
    digest, _ = rewrite_csv(delivery, rows)
    with pytest.raises(ValueError, match=reason):
        qualify(delivery, "D001", "internal_open", digest)


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
    original_stat = Path.stat

    def guard(path):
        assert path.name != "D002.csv"
        return original(path)

    def guard_stat(path, *args, **kwargs):
        assert path.name != "D002.csv"
        return original_stat(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_bytes", guard)
    monkeypatch.setattr(Path, "stat", guard_stat)
    qualify(delivery, "D001", "internal_open", manifest["datasets"][0]["sha256"])
    def reject_csv(path):
        assert path.suffix != ".csv", "No CSV bytes may be read."
        return original(path)

    monkeypatch.setattr(Path, "read_bytes", reject_csv)
    with pytest.raises(ValueError, match="Authorized digest"):
        qualify(delivery, "D001", "internal_open", "0" * 64)


@pytest.mark.parametrize("mutation", ["gap", "ohlc", "nan", "header", "calendar"])
def test_invalid_payload_rejected_with_matching_digest(delivery, mutation):
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
    rewrite_csv(delivery, rows)
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
        blind.execute.__wrapped__(tmp_path, "AQRS-B01-REPLAY", "0" * 40, "codex/aqrs-b01-blind-preparation", None)


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
    monkeypatch.setattr(blind, "git_bytes", lambda *args: (tmp_path / "preregistration.jsonl").read_bytes())
    with pytest.raises(ValueError, match="Source changed"):
        blind.publication(tmp_path, "1" * 40, "codex/aqrs-b01-blind-preparation", {"source_hashes": {}})


def test_data_mutation_rejected_before_measurement(tmp_path, monkeypatch):
    (tmp_path / "bars.npy").write_bytes(b"changed")
    monkeypatch.setattr(blind, "measure", lambda *a, **k: pytest.fail("Measurement must not start."))
    with pytest.raises(ValueError, match="data changed"):
        blind.evaluate_worker.__wrapped__({"stage": "candidate", "plan": {}, "output": str(tmp_path),
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

def test_legacy_registration_rejects_even_a_modified_local_source(tmp_path, monkeypatch, mutate_source):
    from aqrs.admission import AdmissionRejected
    monkeypatch.chdir(tmp_path)
    if mutate_source:
        (tmp_path / "unqualified-source.py").write_text("# Unqualified fixture.\n")
    with pytest.raises(AdmissionRejected, match="not qualified"):
        blind.register(tmp_path, "AQRS-B01-OPEN", "internal_open", "D001", "", None)
    assert not (tmp_path / "artifacts/aqrs-b01/runs").exists()
