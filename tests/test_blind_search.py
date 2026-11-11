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
    assert redundant["decision"] == "EXPLAINED_BY_SIMPLER_CONDITION"
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

