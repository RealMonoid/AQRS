# Explicit __wrapped__ calls below test preserved inner algorithms; FR-005 entry tests use the guarded functions.
import json
import sys
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from time import monotonic

import numpy as np
import pytest

from aqrs.config import load
from aqrs.governor import supervise
from aqrs.market import Bars
from scripts import m2_e15_count as count

ROOT = Path(__file__).resolve().parents[1]


def trigger_fixture(age):
    closes = np.array([105, 100, 109, 109, 109, 103, 110] + [108] * (age - 1) + [109])
    return closes, closes - 1


@pytest.mark.parametrize(
    "age, expected", [(5, [(6, 11)]), (6, [(6, 12)]), (30, [(6, 36)]), (31, [])]
)
def test_trigger_age_and_expiry(age, expected):
    closes, lows = trigger_fixture(age)
    assert list(count.episodes(closes, lows, slice(6, len(closes)))) == expected


def test_invalidation_precedes_trigger_and_training_state_is_clear():
    closes, lows = trigger_fixture(6)
    # Starting at 7 drops setup 6. A different in-fold setup can still fire.
    assert list(count.episodes(closes, lows, slice(7, len(closes)))) == [(10, 12)]
    assert list(count.episodes(closes, lows, slice(6, len(closes) - 1))) == []
    lows[-1] = 100
    assert list(count.episodes(closes, lows, slice(6, len(closes)))) == []


def test_cooling_consumption_and_restart():
    closes = np.array([105, 100, 109, 109, 109, 103, 110, 111, 107, 108, 109, 108, 110])
    lows = closes - 1
    # At 8 the episode cools; 9 consumes. A new crossing at 10 can cool at 11.
    assert list(count.episodes(closes, lows, slice(6, len(closes)))) == [
        (6, 9),
        (10, 12),
    ]


def test_cooling_bar_with_positive_one_minute_return_cannot_trigger():
    closes = np.array([105, 100, 120, 109, 109, 103, 110, 111, 112])
    assert list(count.episodes(closes, closes - 1, slice(6, len(closes)))) == [(6, 8)]


def test_future_changes_keep_prefix_and_do_not_revive_consumed_episode():
    closes, lows = trigger_fixture(6)
    baseline = list(count.episodes(closes, lows, slice(6, len(closes))))
    more = np.r_[closes, 500, 501, 502, 503]
    assert list(count.episodes(more, more - 1, slice(6, len(more)))) == baseline


def test_folds_and_band_credit(monkeypatch):
    timestamps = datetime(2025, 12, 1, tzinfo=UTC).timestamp() + 60 * np.arange(14400)
    bars = Bars(np.column_stack((timestamps, np.ones((14400, 5)))), "BTCUSDT", 1)
    boundaries = []

    def fixture(_closes, _lows, validation):
        boundaries.append((validation.start, validation.stop))
        for offset in (7, 479, 480, 959, 1447, 1919, 2399):
            trigger = validation.start + offset
            yield trigger - 6, trigger

    monkeypatch.setattr(count, "episodes", fixture)
    result = count.summarize(bars)
    assert boundaries == [(5760, 10049), (10080, 14369)]
    assert result["coverage_pass"] is True
    assert result["credited_bands"] == 12
    assert result["credited_days"] == 4
    assert len(result["disagreements"]) == 14
    assert result["disagreements"][1]["available_at"] == "2025-12-05T08:00:00+00:00"


def test_thin_or_uneven_coverage_misses():
    assert count.coverage_pass(12, 4, [9, 3]) is False
    assert count.coverage_pass(12, 3, [6, 6]) is False
    assert count.coverage_pass(11, 4, [6, 5]) is False


def test_preflight_guards_and_scope(monkeypatch):
    monkeypatch.setattr(
        count,
        "capability",
        lambda mode: None if mode == "observed_rss" else "No strict cap.",
    )
    config, _ = load(ROOT / "configs/research.yaml")
    limits = config["resource_governor"]
    plan = count.build_plan(limits)
    assert plan["preflight_status"] == "ADMITTED"
    assert plan["planned_workers"] == 1
    assert plan["planned_fits"] == plan["planned_trials"] == 0
    assert plan["worker_seconds"] == 20
    for change in (
        {"memory_mode": "strict"},
        {"max_peak_rss_mb_per_trial": 128},
        {"max_wall_seconds_per_campaign": 0.5},
    ):
        assert (
            count.build_plan(limits | change)["preflight_status"]
            == "REJECTED_PREFLIGHT"
        )
    receipt = json.loads(
        (ROOT / "evidence/aqrs-d01-verification.json").read_text(encoding="utf-8")
    )
    archives = count.archive_scope(receipt)
    assert len(archives) == 10
    assert archives[-1]["name"] == "BTCUSDT-1m-2025-12-10.zip"
    manifest = receipt["acquisition"]["workers"][0]["result"]["manifest"]
    manifest["archives"][0]["day"] = "2026-01-06"
    with pytest.raises(ValueError, match="scope"):
        count.archive_scope(receipt)


def test_exact_worker_rejects_changed_scope_before_market_io(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Market importer was called.")

    monkeypatch.setattr(count, "load_spot_day", forbidden)
    result = count.count_worker.__wrapped__({"archives": [{"day": "2026-01-06"}]}, tmp_path)
    assert result["input_status"] == "REJECTED"


def test_existing_watchdog_runs_actual_worker_with_rejected_scope(tmp_path):
    outcome = supervise(
        tmp_path,
        {"archives": []},
        20,
        monotonic() + 30,
        512,
        command=[sys.executable, "-B", "-m", "scripts.m2_e15_count", "--worker"],
    )
    assert not outcome["started"] and outcome["execution_status"] == "REJECTED_PREFLIGHT"
    assert outcome["reason_code"] == "ENTRY_UNQUALIFIED"
    assert outcome["started_fits"] == 0


def test_changed_archive_or_sidecar_is_rejected_before_parsing(tmp_path, monkeypatch):
    source = tmp_path / "input"
    source.mkdir()
    payload = b"unparsed archive"
    sidecar = b"unparsed sidecar"
    name = "BTCUSDT-1m-2025-12-01.zip"
    (source / name).write_bytes(payload)
    (source / (name + ".CHECKSUM")).write_bytes(sidecar)
    row = {
        "name": name,
        "day": "2025-12-01",
        "sha256": sha256(payload).hexdigest(),
        "checksum_sha256": sha256(sidecar).hexdigest(),
    }

    def forbidden(*args, **kwargs):
        pytest.fail("Substituted bytes reached the importer.")

    monkeypatch.setattr(count, "load_spot_day", forbidden)
    for field in ("sha256", "checksum_sha256"):
        with pytest.raises(ValueError, match="digest"):
            count.read_day(source, row | {field: "0" * 64}, tmp_path)



def test_real_count_entry_cannot_launch_unqualified_worker(tmp_path):
    import sqlite3
    import subprocess
    result = subprocess.run([sys.executable, "-B", str(Path(count.__file__)), "run"],
                            cwd=tmp_path, capture_output=True, text=True, timeout=20)
    assert result.returncode == 1 and "not qualified" in result.stderr
    with sqlite3.connect(tmp_path / "artifacts/research.sqlite3") as db:
        assert db.execute("SELECT execution_status FROM campaigns").fetchone() == ("REJECTED_PREFLIGHT",)
