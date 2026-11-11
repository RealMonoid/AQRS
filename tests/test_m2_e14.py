import json
import os
import runpy
import sqlite3
import subprocess
import sys
from datetime import UTC, date, datetime
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pytest

from aqrs import binance_spot_pilot, m2_e14
from aqrs.discovery import (
    COSTS,
    HORIZON,
    compare_policies,
    match_volume,
    ridge_trial,
    volume_inputs,
    volume_trial,
)
from aqrs.market import Bars, generate

ROOT = Path(__file__).resolve().parents[1]


def test_pair_uses_next_open_intervals_and_strict_band_end():
    # The control at 99 overlaps. The controls at 70 and 130 touch the
    # high-volume hold and are equidistant. The earlier one wins.
    pair, coverage = match_volume(
        np.array([100, 448, 449]), np.array([70, 99, 130, 418]), 0, 480
    )
    assert pair == (100, 70)
    assert coverage["high_events_without_eligible_partner"] == 0
    assert coverage["events_unselected_under_pair_cap"] == 1
    assert match_volume(np.array([449]), np.array([419]), 0, 480)[0] is None
    assert match_volume(np.array([100]), np.array([71, 129]), 0, 480)[0] is None
    assert match_volume(np.array([70]), np.array([-1, 100]), 0, 480)[0] == (70, 100)


def test_future_prices_and_volume_do_not_change_earlier_event_inputs():
    original = generate(5, 100, 1, "SYNTH")
    values = original.values.copy()
    values[51:, 1:5] *= 2
    values[51:, 5] *= 2
    changed = Bars(values, original.symbol, 1)
    for before, after in zip(
        volume_inputs(original), volume_inputs(changed), strict=True
    ):
        np.testing.assert_array_equal(before[:51], after[:51])


def fixed_volume_fixture(effect):
    rows = 14_400
    opened = np.full(rows, 100.0)
    closed = opened.copy()
    volume = np.ones(rows)
    for signal, size in [(100, 1), (200, 2), (300, 3), (400, 4)]:
        closed[signal] = 101
        volume[signal] = size
    for start in (5760, 10080):
        closed[[start + 100, start + 150]] = 101
        volume[start + 100] = 16
        opened[start + 131] *= 1 + effect / 10_000
    timestamps = datetime(2024, 1, 1, tzinfo=UTC).timestamp() + np.arange(rows) * 60
    return Bars(
        np.column_stack(
            [
                timestamps,
                opened,
                np.maximum(opened, closed),
                np.minimum(opened, closed),
                closed,
                volume,
            ]
        ),
        "SYNTH",
        1,
    )


@pytest.mark.parametrize("effect", [0, 30])
def test_volume_path_matches_known_null_and_planted_effect(effect, tmp_path):
    result = volume_trial(fixed_volume_fixture(effect), {"fit_limit": 2}, tmp_path)
    assert result["paired"]["aggregate"]["pair_count"] == 2
    assert result["paired"]["fold_1"]["pair_count"] == 1
    assert result["paired"]["fold_2"]["pair_count"] == 1
    assert result["paired"]["aggregate"]["empty_bands"] == 16
    assert result["paired"]["aggregate"][
        "mean_paired_net_difference_bps"
    ] == pytest.approx(effect)
    assert result["comparison"]["aggregate"]["eligible_count"] == 4
    assert result["cutoffs"][0] == pytest.approx(3.25)


def test_flat_movement_screen_reserves_no_estimator_fit(tmp_path):
    data = fixed_volume_fixture(0)
    result = ridge_trial(data, {"fit_limit": 4}, tmp_path)
    assert result["evaluation_status"] == "SCREENED_OUT"
    assert result["diagnostic_exposure"][0]["view"] == "fold_1_training"
    assert not (tmp_path / "started_fits.json").exists()


@pytest.mark.parametrize("effect", [0, 30])
def test_matched_costs_and_all_opportunity_denominator(effect):
    start = datetime(2024, 1, 1, tzinfo=UTC).timestamp()
    opened = np.full(90, 100.0)
    opened[43] *= 1 + effect / 10000
    values = np.column_stack(
        [start + np.arange(90) * 60, opened, opened, opened, opened, np.ones(90)]
    )
    summary = compare_policies(
        Bars(values, "SYNTH", 1),
        np.array([12, 13, 43, 44]),
        {"candidate": [0.004, 0.0027, 0, 0.004], "control": [0, 0.004, 0.004, 0]},
        threshold=0.0027,
        reference="control",
    )
    assert summary["aggregate"]["eligible_count"] == 4
    assert summary["aggregate"]["policies"]["candidate"]["skip_count"] == 2
    assert summary["aggregate"]["policies"]["control"]["net_bps"] == pytest.approx(-50)
    assert summary["aggregate"]["net_difference_bps_per_eligible_opportunity"][
        "candidate"
    ] == (pytest.approx(effect / 4))
    assert COSTS["decision_buffer_bps"] == 2 and HORIZON == 30


@pytest.mark.parametrize("campaign", ["M2-E14", "M2-E18"])
def test_market_entry_rejects_missing_authorization_before_any_work(
    tmp_path, monkeypatch, campaign
):
    def forbidden(*args, **kwargs):
        pytest.fail("Admission reached work or the archive loader.")

    monkeypatch.setattr(m2_e14, "supervise", forbidden)
    monkeypatch.setattr(m2_e14, "load_spot_day", forbidden)
    with pytest.raises(ValueError, match="authorization"):
        m2_e14.run_campaign(
            tmp_path / "out",
            ROOT / "configs/research.yaml",
            market_root=tmp_path,
            campaign=m2_e14.CAMPAIGNS[campaign],
        )
    assert not (tmp_path / "out").exists()


def test_market_entry_rejects_tight_fit_limit(tmp_path, monkeypatch):
    config = tmp_path / "tight.yaml"
    config.write_text(
        (ROOT / "configs/research.yaml")
        .read_text()
        .replace("max_model_fits_per_campaign: 12", "max_model_fits_per_campaign: 6"),
        encoding="utf-8",
    )

    def forbidden(*args, **kwargs):
        pytest.fail("A tight limit admitted worker execution.")

    monkeypatch.setattr(m2_e14, "supervise", forbidden)
    with pytest.raises(ValueError, match="fit count"):
        m2_e14.run_campaign(tmp_path / "out", config)


def test_reserved_scope_and_wrong_digest_reject_before_evaluation(
    tmp_path, monkeypatch
):
    _, archives = m2_e14.frozen_definition(ROOT)
    calls = []

    def fake_import(*args, **kwargs):
        calls.append(args)
        return type("Result", (), {"digest": "0" * 64})()

    monkeypatch.setattr(m2_e14, "load_spot_day", fake_import)
    changed = [*archives[:-1], archives[-1] | {"day": "2026-01-06"}]
    with pytest.raises(ValueError, match="allowlist"):
        m2_e14.read_window(tmp_path, changed)
    assert calls == []
    with pytest.raises(ValueError, match="digest"):
        m2_e14.read_window(tmp_path, archives)
    assert len(calls) == 1


def test_preserved_bundle_stages_only_the_ten_allowlisted_pairs(tmp_path, monkeypatch):
    _, archives = m2_e14.frozen_definition(ROOT)
    path = tmp_path / "acceptance.zip"
    with ZipFile(path, "w") as bundle:
        for row in archives:
            member = f"artifacts/{row['name']}"
            bundle.writestr(member, b"archive")
            bundle.writestr(member + ".CHECKSUM", b"checksum")
        bundle.writestr("artifacts/m2-e12/BTCUSDT-1m-2026-01-06.zip", b"reserved")

    def inspect(root, scope):
        assert scope == archives
        expected = {
            row["name"] + suffix for row in archives for suffix in ("", ".CHECKSUM")
        }
        assert {
            p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()
        } == expected
        return "qualified"

    monkeypatch.setattr(m2_e14, "read_archive_directory", inspect)
    assert m2_e14.read_window(path, archives) == "qualified"


def test_replaced_archive_and_sidecar_are_rejected_before_csv_decode(
    tmp_path, monkeypatch
):
    archive = tmp_path / "BTCUSDT-1m-2025-12-25.zip"
    archive.write_bytes(b"replaced data")
    checksum = archive.with_suffix(".zip.CHECKSUM")
    checksum.write_text(sha256(archive.read_bytes()).hexdigest() + "  " + archive.name)

    def forbidden(*args, **kwargs):
        pytest.fail("Unregistered archive reached ZIP decoding.")

    monkeypatch.setattr(binance_spot_pilot, "ZipFile", forbidden)
    with pytest.raises(ValueError, match="historical receipt"):
        binance_spot_pilot.load_spot_day(
            archive,
            checksum,
            date(2025, 12, 25),
            symbol="BTCUSDT",
            expected_digest="0" * 64,
        )


def test_market_binding_rejects_changed_definition_or_missing_review(
    tmp_path, monkeypatch
):
    definition, archives = m2_e14.frozen_definition(ROOT)
    config, _ = m2_e14.load(ROOT / "configs/research.yaml")
    revision = "a" * 40
    receipt = tmp_path / "admission.json"
    record = {
        "owner_approved": True,
        "definition_id": definition,
        "archive_scope": archives,
        "governor_id": m2_e14.fingerprint(config),
        "published_revision": revision,
        "review": {"revision": revision, "status": "PASS"},
        "verification": {"revision": revision, "windows": "PASS", "ubuntu": "PASS"},
        "ci_run_url": "https://github.com/example/example/actions/runs/1",
    }
    verified = []
    monkeypatch.setattr(
        m2_e14, "verify_publication", lambda *args: verified.append(args)
    )
    for changed in (record | {"definition_id": "wrong"}, record | {"review": None}):
        m2_e14.write_json(receipt, changed)
        with pytest.raises(ValueError, match="mismatched"):
            m2_e14.require_admission(receipt, definition, archives, config, ROOT)
    assert verified == []
    m2_e14.write_json(receipt, record)
    assert (
        m2_e14.require_admission(receipt, definition, archives, config, ROOT)[0]
        == record
    )
    assert verified == [(ROOT, revision, m2_e14.E14)]


@pytest.mark.parametrize("variant", m2_e14.CANDIDATES)
def test_missing_diagnostic_metric_rejects_registration(tmp_path, variant):
    exposure = m2_e14.read_json(ROOT / "evidence/exposure.json")
    entry = next(
        r for r in exposure["future_registrations"] if r["variant_id"] == variant
    )
    plan = entry["diagnostic_plan"]
    if variant == m2_e14.CANDIDATES[0]:
        plan["tables"]["paired_events"] = []
    else:
        plan["policy"]["metrics"] = []
    (tmp_path / "evidence").mkdir()
    m2_e14.write_json(tmp_path / "evidence/exposure.json", exposure)
    with pytest.raises(ValueError, match="diagnostic registration"):
        m2_e14.frozen_definition(tmp_path)


def test_publication_check_rejects_other_remote_revision(monkeypatch):
    monkeypatch.setattr(
        m2_e14, "git_bytes", lambda *args: b"b" * 40 + b" refs/heads/codex/m2-e14"
    )
    with pytest.raises(ValueError, match="remote branch head"):
        m2_e14.verify_publication(ROOT, "a" * 40)


def test_market_attempt_claim_uses_scope_and_git_common_dir(tmp_path, monkeypatch):
    _, archives = m2_e14.frozen_definition(ROOT)
    monkeypatch.setattr(m2_e14, "git_bytes", lambda *args: str(tmp_path).encode())
    m2_e14.claim_market_attempt(tmp_path / "first_worktree", archives, "first")
    with pytest.raises(FileExistsError):
        m2_e14.claim_market_attempt(tmp_path / "second_worktree", archives, "second")
    (marker,) = (tmp_path / "aqrs-m2-e14").glob("*.used")
    assert marker.read_text(encoding="utf-8").strip() == "first"


def test_ubuntu_replay_requires_exact_complete_windows_report(tmp_path, monkeypatch):
    monkeypatch.setattr(os, "geteuid", lambda: 1000, raising=False)
    path = tmp_path / "windows.json"
    revision = "a" * 40
    definition = "b" * 64
    files = {"source/pilot.py": "c" * 64}
    receipt = {
        "published_revision": revision,
        "definition_id": definition,
        "governor_id": "governor",
    }
    report = {
        "run_id": "e" * 32,
        "dataset_id": "d" * 64,
        "platform": "win32",
        "execution_status": "COMPLETED",
        "journal_integrity": "ok",
        "dataset_scope": list(m2_e14.DAYS),
        "provenance": {"files": files, "source_id": m2_e14.fingerprint(files)},
        "plan": {"planned_fits": 7, "started_fits": 7, "completed_fits": 7},
        "admission": {"governor_id": "governor"},
        "configuration": {"published_revision": revision, "definition_id": definition},
        "trials": {
            name: {"result": {"evaluation_status": "COMPLETED"}}
            for name in m2_e14.CANDIDATES
        },
    }
    m2_e14.write_json(path, report)
    with pytest.raises(ValueError, match="digest"):
        m2_e14.require_windows_result(path, receipt)
    receipt["windows_report_sha256"] = sha256(path.read_bytes()).hexdigest()
    assert m2_e14.require_windows_result(path, receipt) == report
    with pytest.raises(ValueError, match="does not qualify"):
        m2_e14.require_windows_result(path, receipt, m2_e14.E18)
    training_id = "f" * 64
    scoped = report | {
        "dataset_scope": list(m2_e14.E18.days),
        "configuration": report["configuration"]
        | {"campaign_id": "M2-E18", "variant": "M2-E18"},
        "stages": {"prepare": {"result": {"training_dataset_id": training_id}}},
        "trials": {
            name: {"result": {"evaluation_status": "COMPLETED"}}
            for name in m2_e14.E18.variants
        },
    }
    scoped_admission = receipt | {"training_dataset_id": training_id}
    for altered, accepts in (
        (scoped, True),
        (
            scoped
            | {"stages": {"prepare": {"result": {"training_dataset_id": "0" * 64}}}},
            False,
        ),
        (
            scoped
            | {"configuration": scoped["configuration"] | {"campaign_id": "M2-E14"}},
            False,
        ),
    ):
        m2_e14.write_json(path, altered)
        scoped_admission["windows_report_sha256"] = sha256(
            path.read_bytes()
        ).hexdigest()
        if accepts:
            assert (
                m2_e14.require_windows_result(path, scoped_admission, m2_e14.E18)
                == altered
            )
        else:
            with pytest.raises(ValueError, match="campaign or training identity"):
                m2_e14.require_windows_result(path, scoped_admission, m2_e14.E18)
    m2_e14.write_json(path, report | {"plan": {}})
    receipt["windows_report_sha256"] = sha256(path.read_bytes()).hexdigest()
    with pytest.raises(ValueError, match="does not qualify"):
        m2_e14.require_windows_result(path, receipt)


@pytest.mark.parametrize("campaign", ["M2-E14", "M2-E18"])
def test_synthetic_cli_persists_both_trials_and_bound_diagnostics(tmp_path, campaign):
    volume_id, ridge_id = (
        m2_e14.CANDIDATES
        if campaign == "M2-E14"
        else ("VOL_CONFIRM_E18_V1", "RIDGE_INCREMENT_E18_V1")
    )
    output = tmp_path / "artifacts/open"
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "aqrs.m2_e14",
            *(["--campaign", campaign] if campaign == "M2-E18" else []),
            "--synthetic",
            "--output",
            str(output),
            "--config",
            str(ROOT / "configs/research.yaml"),
        ],
        cwd=ROOT,
        env=os.environ | {"PYTHONPATH": str(ROOT / "src")},
        capture_output=True,
        text=True,
        timeout=90,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    report = json.loads((output / "report.json").read_text(encoding="utf-8"))
    assert report["execution_status"] == "COMPLETED"
    assert report["configuration"]["campaign_id"] == campaign
    assert report["plan"]["planned_fits"] == 7
    assert report["plan"]["started_fits"] == report["plan"]["completed_fits"] == 7
    assert report["dataset_scope"] == ["synthetic"]
    assert report["trials"][volume_id]["result"]["evaluation_status"] == "COMPLETED"
    ridge = report["trials"][ridge_id]["result"]
    assert ridge["comparison"]["aggregate"]["eligible_count"] == 8578
    views = [v for v in ridge["diagnostic_exposure"] if v["kind"] == "forecast_metric"]
    assert len(views) == 30
    assert {view["role"] for view in views} == {
        "three_feature_ridge",
        "one_feature_ridge",
    }
    assert {view["attempt_id"] for view in views} == {f"{report['run_id']}:{ridge_id}"}
    assert {view["source_id"] for view in views} == {report["provenance"]["source_id"]}
    with sqlite3.connect(output / "research.sqlite3") as db:
        assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        rows = db.execute(
            "SELECT candidate_id, execution_status, evidence_status, metrics_json "
            "FROM experiments ORDER BY candidate_id"
        ).fetchall()
    assert [row[:3] for row in rows] == [
        (ridge_id, "COMPLETED", "INSUFFICIENT_EVIDENCE"),
        (volume_id, "COMPLETED", "INSUFFICIENT_EVIDENCE"),
    ]
    assert json.loads(rows[0][3])["diagnostic_exposure"] == ridge["diagnostic_exposure"]
    build_archive = runpy.run_path(str(ROOT / "scripts/evidence_archive.py"))["build"]
    assert build_archive(tmp_path) > 0
    consolidated = json.loads(
        (tmp_path / "evidence/exposure.json").read_text(encoding="utf-8")
    )
    recorded = next(
        a for a in consolidated["attempts"] if a["candidate_id"] == ridge_id
    )
    assert recorded["kind"] == "synthetic_engineering"
    assert recorded["diagnostic_exposure"] == ridge["diagnostic_exposure"]
    assert recorded["source_binding"]["attempt_id"] == views[0]["attempt_id"]
    assert recorded["source_binding"]["source_id"] == views[0]["source_id"]
    if campaign == "M2-E18":
        with sqlite3.connect(output / "research.sqlite3") as db:
            db.execute(
                "UPDATE experiments SET candidate_id = ? WHERE candidate_id = ?",
                ("VOL_CONFIRM_V1", volume_id),
            )
        with pytest.raises(ValueError, match="scope or candidate registration"):
            build_archive(tmp_path)


def test_e18_pins_the_d01_dates_and_registered_training_prefix():
    previous = m2_e14.read_json(ROOT / "evidence/m2-e14-verification.json")
    assert m2_e14.frozen_definition(ROOT)[0] == previous["definition_id"]
    campaign = m2_e14.CAMPAIGNS["M2-E18"]
    definition, archives = m2_e14.frozen_definition(ROOT, campaign)
    assert definition != previous["definition_id"]
    assert [record["day"] for record in archives] == [
        f"2025-12-{i:02d}" for i in range(1, 11)
    ]
    assert all(
        record["name"] == f"BTCUSDT-1m-{record['day']}.zip" for record in archives
    )
    assert all(len(record["checksum_sha256"]) == 64 for record in archives)
    expected = m2_e14.read_json(ROOT / "evidence/m2-e17-verification.json")
    assert m2_e14.e17_training_id(expected, archives) == (
        "84b5179bc227facbfab46cf5c786f7c7a432c412f7d9186295787cf2bad470c9"
    )
    altered = [archives[0] | {"sha256": "0" * 64}, *archives[1:]]
    with pytest.raises(ValueError, match="training receipt"):
        m2_e14.e17_training_id(expected, altered)


def test_e18_rejects_cross_scope_before_archive_open(tmp_path, monkeypatch):
    _, previous = m2_e14.frozen_definition(ROOT)

    def forbidden(*args, **kwargs):
        pytest.fail("The E18 loader reached archive qualification for E14 dates.")

    monkeypatch.setattr(m2_e14, "read_archive_directory", forbidden)
    with pytest.raises(ValueError, match="allowlist"):
        m2_e14.read_window(tmp_path, previous, campaign=m2_e14.CAMPAIGNS["M2-E18"])


def test_e18_verifies_the_actual_training_prefix():
    bars = generate(42, 14_400, 1, "BTCUSDT")
    expected = Bars(bars.values[:5760], bars.symbol, 1).fingerprint
    assert m2_e14.verify_training_prefix(bars, expected) == expected
    with pytest.raises(ValueError, match="training fingerprint"):
        m2_e14.verify_training_prefix(bars, "0" * 64)


def test_e18_rejects_changed_sidecar_before_decoding(tmp_path, monkeypatch):
    campaign = m2_e14.CAMPAIGNS["M2-E18"]
    _, archives = m2_e14.frozen_definition(ROOT, campaign)
    first = tmp_path / archives[0]["name"]
    first.write_bytes(b"unused archive")
    first.with_suffix(".zip.CHECKSUM").write_bytes(b"changed sidecar")

    def forbidden(*args, **kwargs):
        pytest.fail("Changed sidecar reached ZIP decoding.")

    monkeypatch.setattr(binance_spot_pilot, "ZipFile", forbidden)
    with pytest.raises(ValueError, match="checksum bytes"):
        m2_e14.read_window(tmp_path, archives, campaign=campaign)
