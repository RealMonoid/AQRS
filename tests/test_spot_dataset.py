"""Known-answer tests for bounded Spot data preparation, without market data."""

import csv
import importlib
import io
import json
import subprocess
import sys
from datetime import UTC, date, datetime, time
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import numpy as np
import pytest

from aqrs import binance_spot_pilot as spot


def make_day(root, symbol="ETHUSDT", day=date(2025, 12, 1), damage=None):
    stem = f"{symbol}-1m-{day}"
    root.mkdir(parents=True, exist_ok=True)
    archive = root / f"{stem}.zip"
    unit = 1_000_000 if day >= date(2025, 1, 1) else 1000
    start = int(datetime.combine(day, time.min, UTC).timestamp()) * unit
    rows = [
        [
            start + i * 60 * unit,
            10,
            12,
            9,
            11,
            4,
            start + (i + 1) * 60 * unit - 1,
            44,
            2,
            1,
            11,
            0,
        ]
        for i in range(1440)
    ]
    if damage:
        damage(rows)
    text = io.StringIO()
    csv.writer(text).writerows(rows)
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as zipped:
        zipped.writestr(f"{stem}.csv", text.getvalue())
    checksum = archive.with_suffix(".zip.CHECKSUM")
    checksum.write_text(f"{sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n")
    return archive, checksum


@pytest.mark.parametrize("day", [date(2024, 12, 31), date(2025, 1, 1)])
def test_spot_day_keeps_activity_and_exact_availability(tmp_path, day):
    archive, checksum = make_day(tmp_path, day=day)
    result = spot.load_spot_day(archive, checksum, day, symbol="ETHUSDT")
    assert result.bars.symbol == "ETHUSDT"
    assert result.bars.time(0) == f"{day}T00:00:00+00:00"
    assert result.bars.time(0, close=True) == f"{day}T00:01:00+00:00"
    assert result.activity.shape == (1440, 4)
    np.testing.assert_array_equal(result.activity[0], [44, 2, 1, 11])
    assert result.source_timestamp_unit == (
        "milliseconds" if day.year == 2024 else "microseconds"
    )
    assert result.digest == sha256(archive.read_bytes()).hexdigest()


def test_new_loader_preserves_legacy_bars_and_fingerprint(tmp_path):
    day = date(2026, 1, 5)
    archive, checksum = make_day(tmp_path, "BTCUSDT", day)
    old, digest = spot.import_day(archive, checksum, day)
    new = spot.load_spot_day(archive, checksum, day, symbol="BTCUSDT")
    assert new.bars.fingerprint == old.fingerprint
    assert new.digest == digest
    with pytest.raises(ValueError, match="2025"):
        spot.import_day(archive, checksum, date(2024, 12, 31))


@pytest.mark.parametrize("symbol", ["../BTCUSDT", "", "ethusdt", "ETH/USDT"])
def test_invalid_symbols_are_rejected_before_io(tmp_path, symbol):
    with pytest.raises(ValueError, match="symbol"):
        spot.load_spot_day(
            tmp_path / "absent.zip",
            tmp_path / "absent.checksum",
            date(2025, 12, 1),
            symbol=symbol,
        )


@pytest.mark.parametrize("symbol", ["BTCUSDT", "ETHUSDT"])
def test_reserved_day_is_rejected_before_io_for_every_symbol(tmp_path, symbol):
    with pytest.raises(ValueError, match="reserved"):
        spot.load_spot_day(
            tmp_path / "absent.zip",
            tmp_path / "absent.checksum",
            date(2026, 1, 6),
            symbol=symbol,
        )


@pytest.mark.parametrize(
    "column,value",
    [(7, -1), (8, 1.5), (8, -1), (8, 2**53), (9, 5), (10, 45), (9, "nan"), (7, "inf")],
)
def test_invalid_activity_is_rejected(tmp_path, column, value):
    archive, checksum = make_day(
        tmp_path, damage=lambda r: r[0].__setitem__(column, value)
    )
    with pytest.raises(ValueError, match="activity"):
        spot.load_spot_day(archive, checksum, date(2025, 12, 1), symbol="ETHUSDT")


def test_wrong_symbol_filename_is_rejected_before_io(tmp_path):
    with pytest.raises(ValueError, match="filename"):
        spot.load_spot_day(
            tmp_path / "BTCUSDT-1m-2025-12-01.zip",
            tmp_path / "absent",
            date(2025, 12, 1),
            symbol="ETHUSDT",
        )


def data_module():
    return importlib.import_module("aqrs.spot_dataset")


def scope():
    return {
        "id": "FIXTURE",
        "symbols": ["BTCUSDT", "ETHUSDT"],
        "start": "2025-12-01",
        "end": "2025-12-02",
    }


def limits():
    from aqrs.config import load

    return load(Path(__file__).resolve().parents[1] / "configs/research.yaml")[0][
        "resource_governor"
    ]


def test_plan_is_data_only_and_explicit():
    plan = data_module().build_plan(scope(), limits(), acquire=True)
    assert plan["archive_count"] == 4
    assert plan["bar_count"] == 5760
    assert plan["max_requests"] == 8
    assert plan["planned_fits"] == plan["research_trials"] == 0
    assert len(plan["entries"]) == 4
    assert plan["entries"][0]["url"].endswith("BTCUSDT/1m/BTCUSDT-1m-2025-12-01.zip")


@pytest.mark.parametrize(
    "change",
    [
        {"start": "2026-01-05", "end": "2026-01-07"},
        {"symbols": ["BTCUSDT", "BTCUSDT"]},
        {"symbols": ["../BTCUSDT"]},
        {"symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"]},
        {"end": "2026-01-01"},
        {"end": "2025-11-30"},
        {"url": "https://example.com"},
        {"start": 20251201},
        {"end": None},
    ],
)
def test_plan_rejects_invalid_scope(change):
    with pytest.raises(ValueError):
        data_module().build_plan(scope() | change, limits(), acquire=True)


def test_strict_memory_or_too_many_workers_rejected_before_io():
    for change in (
        {"memory_mode": "strict"},
        {"max_research_trials_per_campaign": 1},
        {"max_peak_rss_mb_per_trial": 16},
    ):
        with pytest.raises(ValueError):
            data_module().build_plan(scope(), limits() | change, acquire=True)


def test_network_scope_redirect_and_size_guards(monkeypatch):
    module = data_module()
    called = []
    monkeypatch.setattr(module, "build_opener", lambda *a: called.append(a))
    with pytest.raises(ValueError, match="allowlist"):
        module.fetch_bytes("https://example.com", {"https://data.binance.vision/x"}, 16)
    assert not called
    with pytest.raises(ValueError, match="redirect"):
        module.NoRedirect().redirect_request(
            None, None, 302, "Moved", {}, "https://example.com"
        )

    class Response(io.BytesIO):
        headers = {}

        def geturl(self):
            return module.BASE + "/x"

    class Opener:
        def open(self, *a, **kw):
            return Response(b"x" * 17)

    monkeypatch.setattr(module, "build_opener", lambda *a: Opener())
    with pytest.raises(ValueError, match="size"):
        module.fetch_bytes(module.BASE + "/x", {module.BASE + "/x"}, 16)


def test_offline_cli_qualifies_two_symbols_without_overwriting(tmp_path):
    module = data_module()
    inputs = tmp_path / "input space"
    for symbol in scope()["symbols"]:
        for day in [date(2025, 12, 1), date(2025, 12, 2)]:
            make_day(inputs, symbol, day)
    config = tmp_path / "scope.json"
    config.write_text(json.dumps(scope()), encoding="utf-8")
    output = tmp_path / "qualified"
    command = [
        sys.executable,
        "-B",
        "-m",
        module.__name__,
        "qualify",
        "--scope",
        str(config),
        "--archive-dir",
        str(inputs),
        "--output",
        str(output),
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=35)
    assert result.returncode == 0, result.stderr + result.stdout
    report = json.loads((output / "report.json").read_text())
    assert report["execution_status"] == "COMPLETED"
    assert report["research_ready"] is False
    assert len(report["workers"]) == 2
    for symbol in scope()["symbols"]:
        manifest = json.loads((output / symbol / "manifest.json").read_text())
        assert manifest["bar_count"] == 2880
        assert manifest["symbol"] == symbol
        assert len(manifest["archives"]) == 2
        assert manifest["activity_sha256"]
        with (output / symbol / "activity.csv").open() as source:
            rows = list(csv.DictReader(source))
        assert len(rows) == 2880 and rows[0]["trade_count"] == "2"
        assert rows[1440]["bar_open_time"] == "2025-12-02T00:00:00+00:00"
    before = (output / "report.json").read_bytes()
    repeated = subprocess.run(command, capture_output=True, timeout=10)
    assert repeated.returncode != 0
    assert (output / "report.json").read_bytes() == before


def test_failed_qualification_persists_incomplete_receipt(tmp_path):
    module = data_module()
    plan = module.build_plan(scope(), limits(), acquire=False)
    output = tmp_path / "failed"
    report, code = module.prepare(plan, output, archive_dir=tmp_path / "absent")
    assert code != 0 and report["execution_status"] == "FAILED"
    assert not (output / "BTCUSDT" / "manifest.json").exists()
    persisted = json.loads((output / "report.json").read_text())
    assert persisted["execution_status"] == "FAILED"
    assert persisted["workers"][0]["result"]["error"]


@pytest.mark.parametrize(
    "damage",
    [
        lambda r: r.pop(20),
        lambda r: r[1].__setitem__(0, r[0][0]),
        lambda r: r[0].__setitem__(0, r[0][0] // 1000),
        lambda r: r[0].__setitem__(6, r[0][6] + 1),
    ],
)
def test_new_loader_rejects_incomplete_or_wrong_time_data(tmp_path, damage):
    archive, checksum = make_day(tmp_path, damage=damage)
    with pytest.raises(ValueError):
        spot.load_spot_day(archive, checksum, date(2025, 12, 1), symbol="ETHUSDT")


def test_new_loader_rejects_corrupt_and_oversized_archives(tmp_path):
    archive, checksum = make_day(tmp_path)
    archive.write_bytes(archive.read_bytes()[:-5])
    with pytest.raises(ValueError, match="SHA-256"):
        spot.load_spot_day(archive, checksum, date(2025, 12, 1), symbol="ETHUSDT")
    archive.write_bytes(b"x" * (spot.INPUT_LIMIT + 1))
    with pytest.raises(ValueError, match="size limit"):
        spot.load_spot_day(archive, checksum, date(2025, 12, 1), symbol="ETHUSDT")
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as zipped:
        zipped.writestr("ETHUSDT-1m-2025-12-01.csv", b"0" * (spot.INPUT_LIMIT + 1))
    checksum.write_text(f"{sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n")
    with pytest.raises(ValueError, match="Uncompressed"):
        spot.load_spot_day(archive, checksum, date(2025, 12, 1), symbol="ETHUSDT")


def test_acquisition_stops_on_bad_second_archive_without_publishing(
    tmp_path, monkeypatch
):
    from time import monotonic

    module = data_module()
    plan = module.build_plan(scope() | {"symbols": ["ETHUSDT"]}, limits(), acquire=True)
    inputs = tmp_path / "input"
    payloads = {}
    for entry in plan["entries"]:
        archive, checksum = make_day(
            inputs, "ETHUSDT", date.fromisoformat(entry["day"])
        )
        payloads[entry["url"]] = archive.read_bytes()
        payloads[entry["url"] + ".CHECKSUM"] = checksum.read_bytes()
    payloads[plan["entries"][1]["url"]] = b"bad zip"
    calls = []

    def fetch(url, allowed, limit):
        assert url in allowed
        calls.append(url)
        return payloads[url]

    monkeypatch.setattr(module, "fetch_bytes", fetch)
    output = tmp_path / "output"
    output.mkdir()
    result = module.process_symbol(
        {
            "plan": plan,
            "output": str(output),
            "symbol": "ETHUSDT",
            "worker_deadline": monotonic() + 120,
            "campaign_deadline": monotonic() + 300,
        },
        tmp_path,
    )
    assert result["execution_status"] == "FAILED"
    assert result["validated_archive_count"] == 1
    assert len(calls) == 4
    assert not (output / "ETHUSDT" / "manifest.json").exists()


def test_data_entry_persists_exhausted_deadline(tmp_path):
    module = data_module()
    plan = module.build_plan(
        scope(),
        limits()
        | {"max_wall_seconds_per_trial": 0.01, "max_wall_seconds_per_campaign": 0.01},
        acquire=False,
    )
    report, code = module.prepare(
        plan, tmp_path / "timeout", archive_dir=tmp_path / "absent"
    )
    assert code == 1
    assert report["execution_status"] in {"TIMED_OUT", "BUDGET_EXHAUSTED"}
    assert report["workers"][0]["started_fits"] == 0
    assert not (tmp_path / "timeout" / "BTCUSDT" / "manifest.json").exists()
