import json
import sqlite3
import subprocess
import sys
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_precision_cli_is_planning_only_and_leaves_no_campaign(tmp_path):
    command = [
        sys.executable,
        "-B",
        "-m",
        "aqrs",
        "research",
        "precision",
        "--sd-bps",
        "20",
        "--effect-bps",
        "2",
        "--independent-units",
        "18",
    ]
    result = subprocess.run(
        command,
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["planning_only"] is True
    assert plan["required_independent_units"] == 619
    assert plan["target_within_assumed_capacity"] is False
    assert list(tmp_path.iterdir()) == []
    invalid = subprocess.run(
        command + ["--sd-bps", "nan"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert invalid.returncode == 2
    assert list(tmp_path.iterdir()) == []


def config_at(tmp_path, **limits):
    config = yaml.safe_load(
        (ROOT / "configs/research.yaml").read_text(encoding="utf-8")
    )
    config["project"].update(path_base=".", artifact_dir="research results Ã¼")
    config["journal"]["sqlite_path"] = "research results Ã¼/journal.sqlite3"
    config["market"]["n_bars"] = 240
    config["research"].update(train_bars=60, validation_bars=30, walk_forward_folds=2)
    config["resource_governor"].update(limits)
    path = tmp_path / "research config.yaml"
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    return path


def cli(action, path):
    return subprocess.run(
        [sys.executable, "-m", "aqrs", "research", action, "--config", str(path)],
        check=False,
        cwd=path.parent,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=45,
    )


def read_report(result):
    assert result.returncode == 0, result.stderr or result.stdout
    path = Path(json.loads(result.stdout)["output_dir"])
    assert (path / "dataset.csv").exists()
    markdown = (path / "report.md").read_text(encoding="utf-8")
    assert "No real-world alpha" in markdown
    assert "does not establish predictability or net profitability" in markdown
    assert "not a calibrated horizon forecast" in markdown
    assert "Spearman rank correlation" in markdown
    assert "Descriptive diagnostics" in markdown
    assert "no significance or economic claim" in markdown
    assert "| Fold | Observations | Rank correlation |" in markdown
    return json.loads((path / "report.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("variant", ["evaluated", "foreign_day", "screened_out"])
def test_binance_campaign_isolates_day_and_preserves_spot_policy(tmp_path, variant):
    foreign_day = variant == "foreign_day"
    path = config_at(tmp_path)
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    config["market"].update(
        source="binance_vision_spot",
        symbol="BTCUSDT",
        scenario="historical",
        bar_minutes=1,
        n_bars=1440,
        archive_dir=".",
        day="2026-01-05",
        retrieved_on="2026-11-08",
    )
    del config["research"]["final_holdout_fraction"]
    config["research"].update(horizon_bars=15, train_bars=720, validation_bars=360)
    config["research"]["candidates"] = config["research"]["candidates"][:1]
    config["execution_simulation"]["allow_short"] = False
    config["costs"].update(fee_bps_per_side=10, quoted_spread_bps=1)
    config["resource_governor"]["preflight"]["measure_representative_pilot"] = (
        foreign_day
    )
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    stem = "BTCUSDT-1m-2026-01-05"
    archive = tmp_path / f"{stem}.zip"
    first_open = 1_767_571_200_000_000 + (86_400_000_000 if foreign_day else 0)
    rows = []
    for index in range(1440):
        opened = first_open + index * 60_000_000
        price = 100 + (index % 40) * (0.001 if variant == "screened_out" else 0.5)
        rows.append(
            f"{opened},{price},{price},{price},{price},1,{opened + 59_999_999},0,0,0,0,0\n"
        )
    with ZipFile(archive, "w") as zipped:
        zipped.writestr(f"{stem}.csv", "".join(rows))
    digest = sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(".zip.CHECKSUM").write_text(
        f"{digest}  {archive.name}\n", encoding="ascii"
    )

    result = cli("run", path)
    assert result.returncode == (2 if foreign_day else 0), (
        result.stderr or result.stdout
    )
    summary = json.loads(result.stdout)
    output = Path(summary["output_dir"])
    report = json.loads((output / "report.json").read_text(encoding="utf-8"))
    assert report["holdout"]["start_at"] == "2026-01-06T00:00:00+00:00"
    assert report["holdout"]["authorized_reads"] == 0
    if foreign_day:
        assert report["plan"]["completed_fits"] == report["plan"]["started_trials"] == 0
        assert "Invalid UTC minute cadence" in report["plan"]["stop_reason"]
        assert not (output / "dataset.csv").exists()
        return
    if variant == "screened_out":
        assert summary["execution_status"] == "COMPLETED"
        assert (
            summary["evaluation_status"]
            == report["evaluation_status"]
            == "SCREENED_OUT"
        )
        assert report["plan"]["completed_fits"] == 0
        assert "simulation were skipped" in (output / "report.md").read_text(
            encoding="utf-8"
        )
        return
    assert summary["evaluation_status"] == report["evaluation_status"] == "COMPLETED"
    assert report["data_manifest"]["archive_sha256"] == digest
    assert report["stage_wall_seconds"]["import"] >= 0
    metrics = report["trials"][0]["metrics"]
    assert metrics["stage_wall_seconds"]["features"] >= 0
    assert metrics["stage_wall_seconds"]["simulation"] >= 0
    trades = metrics["trading"]["momentum"]["trades"]
    assert trades
    for trade in trades:
        assert trade["decision"] == "long"
        assert trade["entry_index"] == trade["signal_index"] + 1
        assert trade["exit_index"] == trade["signal_index"] + 16
        assert trade["exit_index"] < (1080 if trade["signal_index"] < 1080 else 1440)
        assert trade["fees"] == pytest.approx(0.0020)
        assert trade["spread"] == pytest.approx(0.0001)
        assert trade["slippage"] == pytest.approx(0.0004)
        assert trade["gross_pnl"] - trade["net_pnl"] == pytest.approx(0.0025)


def test_reserved_spot_day_is_rejected_before_io(tmp_path):
    from datetime import date

    from aqrs.binance_spot_pilot import import_day

    config = yaml.safe_load((ROOT / "configs/m1-e04.yaml").read_text(encoding="utf-8"))
    config["market"]["day"] = "2026-01-06"
    config["project"].update(path_base=".", artifact_dir="output")
    config["journal"]["sqlite_path"] = "output/journal.sqlite3"
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    result = cli("run", path)
    assert result.returncode == 2
    assert "2026-01-05" in result.stderr
    assert not (tmp_path / "output").exists()

    with pytest.raises(ValueError, match="reserved"):
        import_day(
            tmp_path / "missing.zip", tmp_path / "missing.checksum", date(2026, 1, 6)
        )
    with pytest.raises(ValueError, match="reserved"):
        import_day(
            tmp_path / "BTCUSDT-1m-2026-01-06.zip",
            tmp_path / "missing.checksum",
            date(2026, 1, 5),
        )


def test_supervised_pilot_receipt_binds_recoverable_source(tmp_path, monkeypatch):
    import runpy
    from importlib.metadata import version

    from aqrs import journal

    pilot = ROOT / "scripts/m2_supervised_pilot.py"
    main = runpy.run_path(str(pilot))["main"]
    monkeypatch.setitem(main.__globals__, "compare", lambda *args: "REJECTED_PREFLIGHT")
    output = tmp_path / "receipt"
    assert main(output) == 2

    report = json.loads((output / "report.json").read_text(encoding="utf-8"))
    provenance = report["provenance"]
    files = provenance["files"]
    assert files["source/pilot.py"] == sha256(pilot.read_bytes()).hexdigest()
    assert (
        files["source/aqrs/journal.py"]
        == sha256(Path(journal.__file__).read_bytes()).hexdigest()
    )
    assert all(
        sha256((output / name).read_bytes()).hexdigest() == digest
        for name, digest in files.items()
    )
    assert provenance["dependencies"]["scikit-learn"] == version("scikit-learn")
    with sqlite3.connect(output / "research.sqlite3") as db:
        (manifest,) = db.execute("SELECT manifest_json FROM campaigns").fetchone()
    assert json.loads(manifest)["provenance"] == provenance

    monkeypatch.setenv("PYTHONSAFEPATH", "1")
    worker = tmp_path / "worker"
    worker.mkdir()
    restored = subprocess.run(
        [
            sys.executable,
            "-B",
            "-E",
            str(output / "source/pilot.py"),
            "--worker",
            str(worker),
        ],
        cwd=tmp_path,
        input="",
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert restored.returncode == 0, restored.stderr
    assert (worker / "ready.json").is_file()
    assert not (worker / "result.json").exists()


def test_cli_reproduces_results_and_keeps_distinct_campaigns(tmp_path, monkeypatch):
    # The audit hook is inherited by each Python worker through sitecustomize.
    (tmp_path / "sitecustomize.py").write_text(
        "import sys\n"
        "def offline(event, args):\n"
        "    if event in ('socket.connect', 'socket.getaddrinfo', 'socket.sendto'):\n"
        "        raise RuntimeError('Network access is disabled during the offline smoke test.')\n"
        "sys.addaudithook(offline)\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("PYTHONPATH", str(tmp_path))
    config = config_at(tmp_path)
    result = cli("plan", config)
    assert result.returncode == 0, result.stderr or result.stdout
    plan = json.loads(result.stdout)
    assert plan["planned_trials"] == 2
    assert plan["planned_fits"] == 5
    assert plan["preflight_status"] == "ADMITTED"
    first = read_report(cli("run", config))
    second = read_report(cli("run", config))
    assert first["run_id"] != second["run_id"]
    assert first["dataset_fingerprint"] == second["dataset_fingerprint"]
    assert first["holdout"]["purpose"] == "final_holdout_reserved"
    assert [t["metrics"] for t in first["trials"]] == [
        t["metrics"] for t in second["trials"]
    ]
    assert first["plan"]["completed_fits"] == 5
    assert first["plan"]["sampled_cpu_seconds"] > 0
    assert all(t["evidence_status"] == "INSUFFICIENT_EVIDENCE" for t in first["trials"])
    with sqlite3.connect(tmp_path / "research results Ã¼/journal.sqlite3") as db:
        assert db.execute("PRAGMA integrity_check").fetchone() == ("ok",)
        assert db.execute("SELECT COUNT(*) FROM campaigns").fetchone() == (2,)
        assert db.execute("SELECT COUNT(*) FROM experiments").fetchone() == (4,)
        for (stored,) in db.execute("SELECT metrics_json FROM experiments"):
            exposure = json.loads(stored)["diagnostic_exposure"]
            assert len(exposure) == 15
            assert {row["view"] for row in exposure} == {
                "aggregate",
                "fold_1",
                "fold_2",
            }
        assert db.execute(
            "SELECT COUNT(*) FROM experiments WHERE duplicate_of IS NOT NULL"
        ).fetchone() == (2,)


def test_cli_journals_rejected_budget_and_strict_memory_without_fits(tmp_path):
    path = config_at(tmp_path)
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    config["research"]["walk_forward_folds"] = 37_500
    config["resource_governor"]["preflight"]["measure_representative_pilot"] = False
    path.write_text(yaml.safe_dump(config), encoding="utf-8")

    for fixture, fits in ((path, 75_000), (None, 5)):
        result = cli("run", fixture or config_at(tmp_path, memory_mode="strict"))
        assert result.returncode == 2, result.stderr or result.stdout
        summary = json.loads(result.stdout)
        report = json.loads(
            (Path(summary["output_dir"]) / "report.json").read_text(encoding="utf-8")
        )
        assert report["plan"]["planned_fits"] == fits
        assert report["plan"]["started_trials"] == report["plan"]["completed_fits"] == 0
        assert report["execution_status"] == "REJECTED_PREFLIGHT"
    with sqlite3.connect(tmp_path / "research results Ã¼/journal.sqlite3") as db:
        assert db.execute(
            "SELECT execution_status, evidence_status, COUNT(*) FROM experiments "
            "GROUP BY 1, 2"
        ).fetchall() == [("REJECTED_PREFLIGHT", "NOT_EVALUATED", 4)]


def test_real_timeout_is_journaled_and_retry_links_prior_attempt(tmp_path, monkeypatch):
    import time

    from test_governor import probe

    from aqrs import research
    from aqrs.config import load
    from aqrs.governor import supervise

    config, base = load(config_at(tmp_path))
    config["resource_governor"]["preflight"]["measure_representative_pilot"] = False
    calls = []

    def first_blocks(directory, request, trial_seconds, deadline, rss):
        if request.get("stage") == "prepare":
            return supervise(directory, request, trial_seconds, deadline, rss)
        calls.append(request["features"])
        if len(calls) == 1:
            return supervise(
                directory,
                request,
                0.8,
                time.monotonic() + 10,
                rss,
                command=probe("import time; time.sleep(60)"),
            )
        return supervise(directory, request, trial_seconds, deadline, rss)

    monkeypatch.setattr(research, "supervise", first_blocks)
    failed, code = research.run(config, base, plan_only=False)
    assert code == 1 and failed["execution_status"] == "TIMED_OUT"
    assert len(calls) == 2
    rerun, code = research.run(config, base, plan_only=False)
    assert code == 0 and len(calls) == 4
    with sqlite3.connect(base / config["journal"]["sqlite_path"]) as db:
        timed_out = db.execute(
            "SELECT experiment_id, evidence_status, metrics_json FROM experiments "
            "WHERE execution_status = 'TIMED_OUT'"
        ).fetchall()
        assert timed_out == [(f"{failed['run_id']}:C_LAG", "NOT_EVALUATED", None)]
        metadata, duplicate = db.execute(
            "SELECT metadata_json, duplicate_of FROM experiments WHERE experiment_id = ?",
            (f"{rerun['run_id']}:C_LAG",),
        ).fetchone()
        assert json.loads(metadata)["prior_attempt_id"] == timed_out[0][0]
        assert duplicate is None


def test_cancellation_stops_remaining_candidates(tmp_path, monkeypatch):
    from aqrs import planning, research
    from aqrs.config import load

    config, base = load(config_at(tmp_path))

    def cancel(*args):
        return {
            "execution_status": "CANCELLED",
            "stop_reason": "Cancelled by operator.",
            "completed_fits": 0,
            "peak_rss_mb": None,
        }

    def unexpected(*args):
        if args[1].get("stage") == "prepare":
            from aqrs.governor import supervise

            return supervise(*args)
        raise AssertionError("A candidate started after cancellation.")

    monkeypatch.setattr(planning, "supervise", cancel)
    monkeypatch.setattr(research, "supervise", unexpected)
    summary, code = research.run(config, base, plan_only=False)
    assert code == 130 and summary["execution_status"] == "CANCELLED"

    config["resource_governor"]["preflight"]["measure_representative_pilot"] = False
    calls = []

    def cancel_trial(*args):
        if args[1].get("stage") == "prepare":
            from aqrs.governor import supervise

            return supervise(*args)
        calls.append(args)
        return cancel() | {"started": True, "runtime_wall_seconds": 0.1}

    monkeypatch.setattr(research, "supervise", cancel_trial)
    summary, code = research.run(config, base, plan_only=False)
    assert code == 130 and summary["execution_status"] == "CANCELLED"
    assert len(calls) == 1
    with sqlite3.connect(base / config["journal"]["sqlite_path"]) as db:
        assert db.execute(
            "SELECT DISTINCT execution_status, evidence_status FROM experiments"
        ).fetchall() == [("CANCELLED", "NOT_EVALUATED")]


def test_unwritable_journal_prevents_worker_launch(tmp_path, monkeypatch):
    import sqlite3

    import pytest

    from aqrs import planning, research
    from aqrs.config import load

    config, base = load(config_at(tmp_path))
    (base / config["journal"]["sqlite_path"]).mkdir(parents=True)

    def unexpected(*args):
        raise AssertionError("Worker started without a journal.")

    monkeypatch.setattr(planning, "supervise", unexpected)
    monkeypatch.setattr(research, "supervise", unexpected)
    with pytest.raises(sqlite3.OperationalError):
        research.run(config, base, plan_only=False)


def test_holdout_changes_do_not_affect_research_metrics_or_priority(
    tmp_path, monkeypatch
):
    from dataclasses import replace

    from aqrs import research
    from aqrs.config import load
    from aqrs.market import generate

    config, base = load(config_at(tmp_path))
    config["resource_governor"]["preflight"]["measure_representative_pilot"] = False
    first, code = research.run(config, base, plan_only=False)
    assert code == 0

    def change_holdout(*args):
        bars = generate(*args)
        values = bars.values.copy()
        values[192:, 1:5] *= 10
        return replace(bars, values=values)

    original_supervise = research.supervise

    def changed_preparation(directory, request, *args):
        if request.get("stage") == "prepare":
            return {
                "execution_status": "COMPLETED",
                "stop_reason": None,
                "started": True,
                "completed_fits": 0,
                "peak_rss_mb": None,
                "result": research.prepare_data(request),
            }
        return original_supervise(directory, request, *args)

    monkeypatch.setattr(research, "generate", change_holdout)
    monkeypatch.setattr(research, "supervise", changed_preparation)
    second, code = research.run(config, base, plan_only=False)
    assert code == 0
    original, changed = (
        json.loads(
            (Path(summary["output_dir"]) / "report.json").read_text(encoding="utf-8")
        )
        for summary in (first, second)
    )
    assert original["dataset_fingerprint"] != changed["dataset_fingerprint"]
    assert original["holdout"] == changed["holdout"]
    assert original["research_intervals"] == changed["research_intervals"]
    for before, after in zip(original["trials"], changed["trials"], strict=True):
        assert before["priority"] == after["priority"]
        assert before["metrics"] == after["metrics"]


def test_prior_attempt_links_follow_reservation_order(tmp_path):
    from contextlib import closing

    from aqrs import journal
    from aqrs.config import load

    config, _ = load(config_at(tmp_path))
    database = tmp_path / "overlapping.sqlite3"
    with (
        closing(journal.connect(database)) as first,
        closing(journal.connect(database)) as second,
    ):
        for db, run_id in ((first, "earlier"), (second, "later")):
            journal.begin(db, run_id, "config", config, {})
            journal.start_experiment(db, run_id, "C_LAG", {"evidence_key": "same-key"})
        for db, run_id in ((first, "earlier"), (second, "later")):
            trial = {
                "experiment_id": f"{run_id}:C_LAG",
                "candidate_id": "C_LAG",
                "execution_status": "COMPLETED",
                "evidence_status": "INSUFFICIENT_EVIDENCE",
            }
            journal.finish_experiment(db, run_id, trial, {"evidence_key": "same-key"})
        earlier, later = first.execute(
            "SELECT metadata_json, duplicate_of FROM experiments WHERE candidate_id = 'C_LAG' "
            "ORDER BY rowid"
        ).fetchall()
        assert "prior_attempt_id" not in json.loads(earlier[0])
        assert json.loads(later[0])["prior_attempt_id"] == "earlier:C_LAG"
        assert later[1] == "earlier:C_LAG"
