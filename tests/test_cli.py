import json
import sqlite3
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def config_at(tmp_path, **limits):
    config = yaml.safe_load(
        (ROOT / "configs/research.yaml").read_text(encoding="utf-8")
    )
    config["project"].update(path_base=".", artifact_dir="research results ü")
    config["journal"]["sqlite_path"] = "research results ü/journal.sqlite3"
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
    assert "No real-world alpha" in (path / "report.md").read_text(encoding="utf-8")
    return json.loads((path / "report.json").read_text(encoding="utf-8"))


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
    with sqlite3.connect(tmp_path / "research results ü/journal.sqlite3") as db:
        assert db.execute("PRAGMA integrity_check").fetchone() == ("ok",)
        assert db.execute("SELECT COUNT(*) FROM campaigns").fetchone() == (2,)
        assert db.execute("SELECT COUNT(*) FROM experiments").fetchone() == (4,)
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
    with sqlite3.connect(tmp_path / "research results ü/journal.sqlite3") as db:
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
        raise AssertionError("A candidate started after cancellation.")

    monkeypatch.setattr(planning, "supervise", cancel)
    monkeypatch.setattr(research, "supervise", unexpected)
    summary, code = research.run(config, base, plan_only=False)
    assert code == 130 and summary["execution_status"] == "CANCELLED"

    config["resource_governor"]["preflight"]["measure_representative_pilot"] = False
    calls = []

    def cancel_trial(*args):
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

    monkeypatch.setattr(research, "generate", change_holdout)
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
