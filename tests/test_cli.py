import json
import os
import shutil
import sqlite3
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from pathlib import Path
from random import Random
from zipfile import ZipFile

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def isolated_cli_project(tmp_path, monkeypatch):
    """Use the normal CLI with a temporary user directory."""
    copy_application(tmp_path / "test application")
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path / "test home"))


def copy_application(root):
    shutil.copytree(
        ROOT / "src/aqrs",
        root / "src/aqrs",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    shutil.copyfile(ROOT / "pyproject.toml", root / "pyproject.toml")


def ledger_path(tmp_path):
    return tmp_path / "test home" / ".aqrs" / "variant-ledger.sqlite3"


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
    assert set(tmp_path.iterdir()) == {tmp_path / "test application"}
    invalid = subprocess.run(
        command + ["--sd-bps", "nan"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert invalid.returncode == 2
    assert set(tmp_path.iterdir()) == {tmp_path / "test application"}


def config_at(tmp_path, **limits):
    config = yaml.safe_load(
        (ROOT / "configs/research.yaml").read_text(encoding="utf-8")
    )
    config["project"].update(path_base=".", artifact_dir="research results Ã¼")
    config["journal"]["sqlite_path"] = "research results Ã¼/journal.sqlite3"
    config["market"].update(n_bars=240, bar_minutes=1440)
    config["study"]["minimum_effect"] = 0.4
    config["research"].update(train_bars=60, validation_bars=30, walk_forward_folds=2)
    config["resource_governor"].update(limits)
    path = tmp_path / "research config.yaml"
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    return path


@pytest.mark.parametrize(
    "missing_field",
    [
        None,
        "question",
        "rule",
        "minimum_effect",
        "on_advantage",
        "on_no_advantage",
        "on_inconclusive",
    ],
)
def test_ridge_cli_restores_real_work_and_requires_study_fields(
    tmp_path, missing_field
):
    path = config_at(tmp_path)
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    config["study"]["rule"] = "ridge"
    config["market"]["bar_minutes"] = 5
    config["research"].update(
        horizon_bars=3,
        candidates=[
            {"id": "C_LAG", "model": "ridge", "features": ["past_return"]},
            {
                "id": "C_VOLUME",
                "model": "ridge",
                "features": ["past_return", "relative_volume"],
            },
        ],
    )
    config["costs"] = dict.fromkeys(
        config["costs"], 0
    )  # Public execution fixture, not economic evidence.
    if missing_field:
        del config["study"][missing_field]
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    outcome = cli("run", path)
    summary = json.loads(outcome.stdout)
    if missing_field:
        assert outcome.returncode == 2, outcome.stdout or outcome.stderr
        assert summary["started_workers"] == summary["started_fits"] == 0
        return
    assert outcome.returncode == 0, outcome.stdout or outcome.stderr
    output = Path(summary["output_dir"])
    report = json.loads((output / "report.json").read_text(encoding="utf-8"))
    assert report["detectability"]["status"] == "NOT_APPLICABLE"
    assert "detectability_execution" not in report
    assert report["plan"]["completed_fits"] == report["plan"]["planned_fits"] == 5
    assert report["plan"]["started_trials"] == 2
    assert all("prediction" in trial["metrics"] for trial in report["trials"])
    assert all(
        trial["next_action"] == config["study"]["on_inconclusive"]
        for trial in report["trials"]
    )
    assert "Detectability is not evaluated for Ridge" in (
        output / "report.md"
    ).read_text(encoding="utf-8")


def cli(action, path, *, project=None):
    source = (project or path.parent / "test application") / "src"
    entry = (
        "import runpy, sys; from pathlib import Path; "
        "test_home = Path(sys.argv.pop(1)); "
        "Path.home = classmethod(lambda cls: test_home); "
        "runpy.run_module('aqrs', run_name='__main__', alter_sys=True)"
    )
    return subprocess.run(
        [
            sys.executable,
            "-c",
            entry,
            str(path.parent / "test home"),
            "research",
            action,
            "--config",
            str(path),
        ],
        check=False,
        cwd=path.parent,
        env=os.environ
        | {
            "PYTHONPATH": os.pathsep.join(
                part for part in (str(source), os.environ.get("PYTHONPATH")) if part
            )
        },
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=45,
    )


def reversal_config(
    tmp_path,
    symbol,
    bar_minutes,
    year,
    pattern,
    *,
    volumes=(1,),
    n_bars=160,
    validation_bars=34,
    start=None,
):
    path = config_at(tmp_path)
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    config["market"].update(
        source="synthetic_csv",
        csv_path="input.csv",
        symbol=symbol,
        bar_minutes=bar_minutes,
        n_bars=n_bars,
    )
    config["research"].update(
        horizon_bars=1,
        train_bars=40,
        validation_bars=validation_bars,
        candidates=[{"id": "REVERSAL", "model": "bar_reversal"}],
    )
    start = start or datetime(year, 1, 7, 12, tzinfo=UTC)
    config["market"]["start_at"] = start.isoformat()
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    rows = ["bar_open_time,open,high,low,close,volume,dataset_type"]
    for i in range(n_bars):
        opened = start + timedelta(minutes=i * bar_minutes)
        close = 100 + pattern[i % len(pattern)]
        volume = volumes[i % len(volumes)]
        rows.append(f"{opened.isoformat()},100,102,98,{close},{volume},synthetic")
    path.with_name("input.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    return path


@pytest.mark.parametrize(
    "symbol,minutes,year,pattern,n_bars,validation_bars,decision,accuracy",
    [
        ("TEST_ALPHA", 5, 2024, (1, -1), 14500, 5762, "REVERSAL_ADVANTAGE", 1.0),
        (
            "TEST_BETA",
            30,
            2025,
            (1, -1, -1, 1),
            2500,
            962,
            "NO_REVERSAL_ADVANTAGE",
            0.5,
        ),
    ],
)
def test_common_run_scores_synthetic_csv_reversal(
    tmp_path,
    symbol,
    minutes,
    year,
    pattern,
    n_bars,
    validation_bars,
    decision,
    accuracy,
):
    path = reversal_config(
        tmp_path,
        symbol,
        minutes,
        year,
        pattern,
        n_bars=n_bars,
        validation_bars=validation_bars,
    )
    result = cli("run", path)
    assert result.returncode == 0, result.stderr or result.stdout
    output = Path(json.loads(result.stdout)["output_dir"])
    report = json.loads((output / "report.json").read_text(encoding="utf-8"))
    plan = report["plan"]
    assert report["dataset_type"] == "synthetic"
    assert report["timeframe_minutes"] == minutes
    assert report["data_manifest"]["symbol"] == symbol
    assert report["data_manifest"]["start_at"].startswith(str(year))
    assert (
        report["data_manifest"]["input_sha256"]
        == sha256(path.with_name("input.csv").read_bytes()).hexdigest()
    )
    assert report["holdout"]["observations"] == n_bars // 5
    assert plan["preflight_status"] == "ADMITTED" and plan["started_trials"] == 1
    assert plan["source_data_validated"] is True
    assert plan["planned_pilot_fits"] == 0
    assert plan["planned_fits"] == plan["started_fits"] == plan["completed_fits"] == 2
    assert (output / "report.md").read_text(encoding="utf-8").count(decision) == 1
    with sqlite3.connect(output / report["journal_path"]) as db:
        status, evidence, metadata, metrics = db.execute(
            "SELECT execution_status, evidence_status, metadata_json, metrics_json FROM experiments"
        ).fetchone()
    assert status == "COMPLETED" and evidence == "INSUFFICIENT_EVIDENCE"
    metadata = json.loads(metadata)
    assert metadata["model_type"] == "bar_reversal"
    assert metadata["workflow_question"] == report["trials"][0]["workflow_question"]
    assert metadata["workflow_learning"] == report["trials"][0]["workflow_learning"]
    directional = json.loads(metrics)["directional_reversal"]
    assert directional["decision"] == decision
    assert directional["accuracy"] == accuracy
    assert directional["observations"] == 2 * (validation_bars - 2)
    assert (
        directional["always_up_accuracy"] == directional["always_down_accuracy"] == 0.5
    )
    assert directional["scored_utc_days"] == 41
    assert set(directional["contrasts"]) == {"always_up", "always_down"}
    for bounds in directional["contrasts"].values():
        assert set(bounds) == {"7", "14"}
        if decision == "REVERSAL_ADVANTAGE":
            assert all(b["lower_95_one_sided"] > 0 for b in bounds.values())
        else:
            assert all(b["upper_95_one_sided"] == 0 for b in bounds.values())


def test_reversal_random_null_does_not_advance_on_one_extra_hit(tmp_path):
    # Fair independent directions. Seed 6 deliberately reproduces a positive
    # raw gap on the fixed validation rows; it is not a calibration sample.
    pattern = Random(6).choices((-1, 1), k=2400)
    path = reversal_config(
        tmp_path,
        "TEST_RANDOM_NULL",
        30,
        2026,
        pattern,
        n_bars=2400,
        validation_bars=770,
    )
    result = cli("run", path)
    assert result.returncode == 0, result.stderr or result.stdout
    output = Path(json.loads(result.stdout)["output_dir"])
    report = json.loads((output / "report.json").read_text(encoding="utf-8"))
    directional = report["trials"][0]["metrics"]["directional_reversal"]
    assert directional["observations"] == 1536
    assert directional["accuracy"] == pytest.approx(785 / 1536)
    assert directional["always_down_accuracy"] == pytest.approx(784 / 1536)
    assert directional["decision"] == "INCONCLUSIVE"
    assert directional["uncertainty_status"] == "ESTIMATED"
    worse_gap = directional["contrasts"]["always_down"]
    assert set(worse_gap) == {"7", "14"}
    assert all(bound["mean"] == pytest.approx(1 / 1536) for bound in worse_gap.values())
    assert all(bound["lower_95_one_sided"] <= 0 for bound in worse_gap.values())


@pytest.mark.parametrize(
    "volumes, decision, accuracy",
    [
        ((3, 1), "VOLUME_MOVEMENT_ADVANTAGE", 1.0),
        ((2,), "NO_VOLUME_MOVEMENT_ADVANTAGE", 0.5),
    ],
)
def test_common_run_scores_volume_movement(tmp_path, volumes, decision, accuracy):
    path = reversal_config(
        tmp_path,
        "TEST_VOLUME",
        30,
        2025,
        (0.5, 1.5),
        volumes=volumes,
        n_bars=2500,
        validation_bars=962,
    )
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    config["research"]["candidates"] = [{"id": "VOLUME", "model": "volume_movement"}]
    config["study"]["rule"] = "volume_movement"
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    result = cli("run", path)
    assert result.returncode == 0, result.stderr or result.stdout
    output = Path(json.loads(result.stdout)["output_dir"])
    report = json.loads((output / "report.json").read_text(encoding="utf-8"))
    plan = report["plan"]
    assert plan["started_trials"] == 1 and plan["planned_pilot_fits"] == 0
    assert plan["planned_fits"] == plan["started_fits"] == plan["completed_fits"] == 2
    admission = report["variant_admission"]
    assert set(admission["variant_keys"]) == {"VOLUME"}
    assert (
        len(set(admission["variant_keys"].values())) == admission["requested_new"] == 1
    )
    trial = report["trials"][0]
    comparison = trial["metrics"]["volume_movement"]
    assert comparison["observations"] == 1920
    assert comparison["accuracy"] == accuracy
    assert (
        comparison["always_above_accuracy"]
        == comparison["always_below_accuracy"]
        == 0.5
    )
    assert comparison["decision"] == decision
    assert comparison["scored_utc_days"] == 41
    assert set(comparison["contrasts"]) == {"always_above", "always_below"}
    for limits in comparison["contrasts"].values():
        assert set(limits) == {"7", "14"}
    if accuracy == 1.0:
        assert all(
            bound["lower_95_one_sided"] > 0
            for limits in comparison["contrasts"].values()
            for bound in limits.values()
        )
    else:
        assert all(
            bound["upper_95_one_sided"] == 0
            for bound in comparison["contrasts"]["always_below"].values()
        )
    assert (output / "report.md").read_text(encoding="utf-8").count(decision) == 1
    with sqlite3.connect(output / report["journal_path"]) as db:
        status, metadata, metrics = db.execute(
            "SELECT execution_status, metadata_json, metrics_json "
            "FROM experiments WHERE experiment_id = ?",
            (trial["experiment_id"],),
        ).fetchone()
    assert status == "COMPLETED"
    metadata = json.loads(metadata)
    assert metadata["folds"] == report["research_intervals"]
    assert metadata["workflow_question"] == trial["workflow_question"]
    assert json.loads(metrics)["volume_movement"] == comparison


@pytest.mark.parametrize("model", ["bar_reversal", "volume_movement"])
@pytest.mark.parametrize("source", ["binance_vision_spot", "unknown"])
def test_bar_rule_rejects_foreign_source_before_campaign(tmp_path, model, source):
    path = reversal_config(tmp_path, "TEST_ALPHA", 5, 2024, (1, -1))
    path.with_name("input.csv").unlink()
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    config["market"]["source"] = source
    config["research"]["candidates"][0]["model"] = model
    config["study"]["rule"] = model
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    result = cli("run", path)
    assert result.returncode == 2
    assert_admission_rejection(
        result,
        tmp_path,
        config,
        "UNKNOWN_SOURCE" if source == "unknown" else "SOURCE_NOT_ALLOWED_FOR_CANDIDATE",
    )


def assert_admission_rejection(result, base, config, reason_code):
    assert result.returncode == 2, result.stderr or result.stdout
    summary = json.loads(result.stdout)
    assert summary["execution_status"] == "REJECTED_PREFLIGHT"
    assert summary["reason_code"] == reason_code
    with sqlite3.connect(base / config["journal"]["sqlite_path"]) as db:
        (manifest,) = db.execute(
            "SELECT manifest_json FROM campaigns WHERE run_id = ?",
            (summary["run_id"],),
        ).fetchone()
        attempts = db.execute(
            "SELECT execution_status, evidence_status, metadata_json "
            "FROM experiments WHERE run_id = ?",
            (summary["run_id"],),
        ).fetchall()
    manifest = json.loads(manifest)
    if reason_code == "PREREQUISITE_MISSING":
        assert not manifest["preparation"]["started"]
    else:
        assert "preparation" not in manifest
    assert manifest["stop_reason"] == summary["stop_reason"]
    assert len(attempts) == len(config["research"]["candidates"])
    for status, evidence, metadata in attempts:
        assert (status, evidence) == ("REJECTED_PREFLIGHT", "NOT_EVALUATED")
        assert json.loads(metadata)["reason_code"] == reason_code
    return summary


@pytest.mark.parametrize("model", ["ridge", "bar_reversal", "volume_movement"])
@pytest.mark.parametrize(
    "defect",
    [
        "protected",
        "protected_later",
        "future",
        "crosses_future",
        "unknown",
        "missing_scope",
    ],
)
def test_common_admission_blocks_data_for_each_candidate(tmp_path, model, defect):
    path = reversal_config(tmp_path, "PROTECTED_TEST", 5, 2024, (1, -1))
    path.with_name("input.csv").unlink()
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    if model == "ridge":
        config["research"]["candidates"] = [
            {"id": "RIDGE", "model": "ridge", "features": ["past_return"]}
        ]
    else:
        config["research"]["candidates"][0]["model"] = model
    config["study"]["rule"] = model
    if defect == "protected":
        # The interval crosses midnight into the protected day. The
        # training/input scope alone is sufficient for rejection.
        config["market"]["start_at"] = "2026-01-05T23:55:00Z"
    elif defect == "protected_later":
        config["market"]["start_at"] = "2026-10-31T23:55:00+00:00"
    elif defect == "future":
        config["market"]["start_at"] = "2027-03-01T00:00:00Z"
    elif defect == "crosses_future":
        config["market"]["start_at"] = "2026-11-30T23:55:00Z"
    elif defect == "unknown":
        config["market"]["source"] = "unknown"
    else:
        del config["market"]["start_at"]
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    assert_admission_rejection(
        cli("run", path),
        tmp_path,
        config,
        {
            "protected": "LOCKED_PERIOD",
            "protected_later": "LOCKED_PERIOD",
            "future": "LOCKED_PERIOD",
            "crosses_future": "LOCKED_PERIOD",
            "unknown": "UNKNOWN_SOURCE",
            "missing_scope": "INVALID_DATA_SCOPE",
        }[defect],
    )


def test_common_cli_counts_variants_across_invocations_and_output_directories(tmp_path):
    path = reversal_config(tmp_path, "COUNTING_TEST", 1440, 2024, (1, -1))
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    config["resource_governor"]["preflight"]["measure_representative_pilot"] = False

    def launch():
        path.write_text(yaml.safe_dump(config), encoding="utf-8")
        return cli("run", path)

    # Ten overlapping temporal designs consume ten distinct variants.
    first = launch()
    assert first.returncode == 0, first.stderr or first.stdout
    first_summary = json.loads(first.stdout)
    for train_bars in range(41, 50):
        config["research"]["train_bars"] = train_bars
        outcome = launch()
        assert outcome.returncode == 0, outcome.stderr or outcome.stdout
    config["research"]["train_bars"] = 40

    config["project"]["artifact_dir"] = "fresh output"
    config["research"].update(
        horizon_bars=1,
        candidates=[{"id": "RENAMED", "model": "bar_reversal"}],
    )
    rerun = launch()
    assert rerun.returncode == 0, rerun.stderr or rerun.stdout
    second_summary = json.loads(rerun.stdout)
    assert first_summary["run_id"] != second_summary["run_id"]
    assert first_summary["output_dir"] != second_summary["output_dir"]

    path.with_name("input.csv").unlink()
    config["research"]["train_bars"] = 50
    assert_admission_rejection(launch(), tmp_path, config, "VARIANT_LIMIT")
    config["research"]["train_bars"] += 1
    assert_admission_rejection(launch(), tmp_path, config, "VARIANT_LIMIT")
    config["research"]["train_bars"] -= 1
    config["market"]["start_at"] = "2024-01-07T12:05:00Z"
    assert_admission_rejection(launch(), tmp_path, config, "VARIANT_LIMIT")
    config["market"]["start_at"] = "2024-01-07T12:00:00Z"
    config["resource_governor"]["max_variants_per_evaluation_period"] = 1000
    assert_admission_rejection(launch(), tmp_path, config, "VARIANT_LIMIT")
    del config["resource_governor"]["max_variants_per_evaluation_period"]
    original_journal = config["journal"]["sqlite_path"]
    config["journal"]["sqlite_path"] = "alternate.sqlite3"
    assert_admission_rejection(launch(), tmp_path, config, "VARIANT_LIMIT")
    config["research"]["candidates"] = [{"id": "VOLUME", "model": "volume_movement"}]
    config["study"]["rule"] = "volume_movement"
    assert_admission_rejection(launch(), tmp_path, config, "VARIANT_LIMIT")
    config["journal"]["sqlite_path"] = original_journal

    with sqlite3.connect(ledger_path(tmp_path)) as ledger:
        assert ledger.execute("SELECT COUNT(*) FROM variant_exposures").fetchone() == (
            10,
        )
    with sqlite3.connect(tmp_path / config["journal"]["sqlite_path"]) as db:
        assert db.execute("SELECT COUNT(*) FROM experiments").fetchone() == (15,)
        first_meta, rerun_meta = [
            json.loads(
                db.execute(
                    "SELECT metadata_json FROM experiments WHERE run_id = ?",
                    (run_id,),
                ).fetchone()[0]
            )
            for run_id in (first_summary["run_id"], second_summary["run_id"])
        ]
    assert first_meta["variant_key"] == rerun_meta["variant_key"]


@pytest.mark.parametrize("change", ["symbol", "source", "adjacent"])
def test_variant_budget_is_scoped_to_source_symbol_and_overlapping_period(
    tmp_path, change
):
    path = reversal_config(
        tmp_path,
        "TEST_SCOPE",
        1440,
        2024,
        (1, -1),
        n_bars=300,
        start=datetime(2024, 1, 1, tzinfo=UTC),
    )
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    config["resource_governor"]["max_variants_per_evaluation_period"] = 1
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    first = cli("run", path)
    assert first.returncode == 0, first.stderr or first.stdout
    if change == "symbol":
        config["market"]["symbol"] = "SECOND_SYMBOL"
    elif change == "source":
        config["market"].update(source="synthetic", scenario="null")
        del config["market"]["start_at"], config["market"]["csv_path"]
    else:
        config["research"]["train_bars"] += 2 * config["research"]["validation_bars"]
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    second = cli("run", path)
    assert second.returncode == 0, second.stderr or second.stdout
    with sqlite3.connect(ledger_path(tmp_path)) as ledger:
        assert ledger.execute("SELECT COUNT(*) FROM variant_exposures").fetchone() == (
            2,
        )


def test_concurrent_cli_requests_cannot_both_take_the_last_slot(tmp_path):
    first = reversal_config(tmp_path, "RACE_TEST", 1440, 2024, (1, -1))
    config = yaml.safe_load(first.read_text(encoding="utf-8"))
    config["resource_governor"].update(max_variants_per_evaluation_period=1)
    config["resource_governor"]["preflight"]["measure_representative_pilot"] = False
    first.write_text(yaml.safe_dump(config), encoding="utf-8")
    second = first.with_name("second.yaml")
    config["research"]["train_bars"] += 1
    config["journal"]["sqlite_path"] = "concurrent.sqlite3"
    second.write_text(yaml.safe_dump(config), encoding="utf-8")
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(cli, ("run", "run"), (first, second)))
    assert sorted(r.returncode for r in results) == [0, 2], [
        r.stderr or r.stdout for r in results
    ]
    assert sorted(json.loads(r.stdout)["variant_ledger_created"] for r in results) == [
        False,
        True,
    ]
    rejected = next(r for r in results if r.returncode == 2)
    rejected_config = yaml.safe_load(
        (first if rejected is results[0] else second).read_text(encoding="utf-8")
    )
    assert_admission_rejection(rejected, tmp_path, rejected_config, "VARIANT_LIMIT")
    with sqlite3.connect(ledger_path(tmp_path)) as ledger:
        assert ledger.execute("SELECT COUNT(*) FROM variant_exposures").fetchone() == (
            1,
        )


def test_old_project_reservations_are_not_imported(tmp_path):
    from contextlib import closing

    from aqrs import journal

    path = reversal_config(tmp_path, "LEGACY_TEST", 1440, 2024, (1, -1))
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    database = tmp_path / "test application" / "artifacts" / "research.sqlite3"
    with closing(journal.connect(database)) as db:
        journal.begin(db, "old-run", "old-config", config, {})
        with db:
            db.execute(
                "CREATE TABLE variant_reservations "
                "(period_start, period_end, variant_key, first_experiment_id)"
            )
            db.execute(
                "INSERT INTO variant_reservations VALUES (?, ?, ?, ?)",
                (
                    "2024-01-07T15:20:00+00:00",
                    "2024-01-07T21:00:00+00:00",
                    "old-variant",
                    "old-run:REVERSAL",
                ),
            )
    original = database.read_bytes()
    config["resource_governor"]["max_variants_per_evaluation_period"] = 1
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    result = cli("run", path)
    assert result.returncode == 0, result.stdout or result.stderr
    assert database.read_bytes() == original
    with sqlite3.connect(ledger_path(tmp_path)) as db:
        rows = db.execute(
            "SELECT first_experiment_id FROM variant_exposures"
        ).fetchall()
        assert len(rows) == 1 and rows[0][0] != "old-run:REVERSAL"


def test_cli_reports_ledger_creation_after_deletion(tmp_path):
    path = reversal_config(tmp_path, "NEW_LEDGER", 1440, 2024, (1, -1))
    path.with_name("input.csv").unlink()

    def check_creation(expected):
        result = cli("run", path)
        assert result.returncode == 2, result.stderr or result.stdout
        summary = json.loads(result.stdout)
        assert summary["reason_code"] == "PREREQUISITE_MISSING"
        assert summary["variant_ledger_created"] is expected
        output = Path(summary["output_dir"])
        report = json.loads((output / "report.json").read_text(encoding="utf-8"))
        assert report["variant_ledger_created"] is expected
        markdown = (output / "report.md").read_text(encoding="utf-8")
        assert ("Variant ledger initialized" in markdown) is expected

    check_creation(True)
    check_creation(False)
    ledger_path(tmp_path).unlink()
    check_creation(True)


def test_cli_shares_ledger_across_project_copies(tmp_path):
    path = reversal_config(tmp_path, "SHARED_LEDGER", 1440, 2024, (1, -1))
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    config["resource_governor"]["max_variants_per_evaluation_period"] = 1
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    first = cli("run", path)
    assert first.returncode == 0, first.stdout or first.stderr
    path.with_name("input.csv").unlink()
    config["journal"]["sqlite_path"] = "second copy.sqlite3"
    config["research"]["train_bars"] += 1
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    second_copy = tmp_path / "second checkout"
    copy_application(second_copy)
    summary = assert_admission_rejection(
        cli("run", path, project=second_copy), tmp_path, config, "VARIANT_LIMIT"
    )
    assert summary["variant_ledger_created"] is False
    assert ledger_path(tmp_path).is_file()


def test_cli_does_not_import_legacy_ledgers_from_linked_worktrees(tmp_path):
    from contextlib import closing

    first = tmp_path / "test application"
    second = tmp_path / "second checkout"
    for arguments in (
        ["init", "--quiet"],
        [
            "-c",
            "user.name=AQRS",
            "-c",
            "user.email=aqrs@example.invalid",
            "-c",
            "commit.gpgSign=false",
            "commit",
            "--allow-empty",
            "--quiet",
            "-m",
            "Fixture",
        ],
        ["worktree", "add", "--quiet", "--detach", str(second)],
    ):
        subprocess.run(["git", *arguments], cwd=first, check=True, capture_output=True)
    copy_application(second)
    prior_ledgers = [
        root / "artifacts" / "variant-ledger.sqlite3" for root in (first, second)
    ]
    for index, old_path in enumerate(prior_ledgers):
        old_path.parent.mkdir()
        with closing(sqlite3.connect(old_path)) as old_ledger, old_ledger:
            old_ledger.execute(
                "CREATE TABLE variant_exposures "
                "(source, symbol, period_start, period_end, variant_key, first_experiment_id)"
            )
            old_ledger.execute(
                "INSERT INTO variant_exposures VALUES (?, ?, ?, ?, ?, ?)",
                (
                    "synthetic_csv",
                    "  LEGACY_SYMBOL  " if index else "LEGACY_SYMBOL",
                    "2024-01-07T15:20:00+00:00",
                    "2024-01-07T21:00:00+00:00",
                    f"old-variant-{index}",
                    f"old-run-{index}:REVERSAL",
                ),
            )
    prior_contents = [p.read_bytes() for p in prior_ledgers]
    path = reversal_config(tmp_path, "LEGACY_SYMBOL", 1440, 2024, (1, -1))
    path.with_name("input.csv").unlink()
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    config["resource_governor"]["max_variants_per_evaluation_period"] = 2
    path.write_text(yaml.safe_dump(config), encoding="utf-8")

    summary = assert_admission_rejection(
        cli("run", path, project=second), tmp_path, config, "PREREQUISITE_MISSING"
    )
    assert summary["variant_ledger_created"] is True
    assert [p.read_bytes() for p in prior_ledgers] == prior_contents
    for old_path in prior_ledgers:
        old_path.unlink()
    summary = assert_admission_rejection(
        cli("run", path, project=first), tmp_path, config, "PREREQUISITE_MISSING"
    )
    assert summary["variant_ledger_created"] is False

    with sqlite3.connect(ledger_path(tmp_path)) as db:
        rows = db.execute("SELECT variant_key FROM variant_exposures").fetchall()
    assert len(rows) == 1 and not rows[0][0].startswith("old-variant")


def test_cli_symbol_padding_shares_quota_and_variant_identity(tmp_path):
    path = reversal_config(tmp_path, "TEST_SYMBOL", 1440, 2024, (1, -1))
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    config["resource_governor"]["max_variants_per_evaluation_period"] = 1
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    first = cli("run", path)
    assert first.returncode == 0, first.stdout or first.stderr
    config["market"]["symbol"] = "  TEST_SYMBOL \t"
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    rerun = cli("run", path)
    assert rerun.returncode == 0, rerun.stderr or rerun.stdout
    report = json.loads(
        (Path(json.loads(rerun.stdout)["output_dir"]) / "report.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["variant_admission"]["requested_new"] == 0
    assert report["variant_admission"]["symbol"] == "TEST_SYMBOL"
    path.with_name("input.csv").unlink()
    config["research"]["train_bars"] += 1
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    assert_admission_rejection(cli("run", path), tmp_path, config, "VARIANT_LIMIT")
    config["market"]["symbol"] = " \t "
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    blank = cli("run", path)
    assert blank.returncode == 2 and "symbol must be a nonempty string" in blank.stderr


@pytest.mark.parametrize(
    "defect", ["timestamp", "marker", "declared_start", "fit_budget"]
)
def test_reversal_rejects_invalid_csv_before_trial(tmp_path, defect):
    path = reversal_config(tmp_path, "TEST_ALPHA", 1440, 2024, (1, -1))
    csv_path = path.with_name("input.csv")
    text = csv_path.read_text(encoding="utf-8")
    if defect == "timestamp":
        text = text.replace("2024-01-08T12:00:00+00:00", "2024-01-08T11:59:00+00:00", 1)
    elif defect == "marker":
        text = text.replace(",synthetic\n", ",real\n", 1)
    elif defect == "declared_start":
        config = yaml.safe_load(path.read_text(encoding="utf-8"))
        config["market"]["start_at"] = "2024-01-07T12:05:00Z"
        path.write_text(yaml.safe_dump(config), encoding="utf-8")
    if defect == "fit_budget":
        csv_path.unlink()
        config = yaml.safe_load(path.read_text(encoding="utf-8"))
        config["resource_governor"]["max_model_fits_per_campaign"] = 1
        path.write_text(yaml.safe_dump(config), encoding="utf-8")
    else:
        csv_path.write_text(text, encoding="utf-8")
    result = cli("run", path)
    assert result.returncode == 2, result.stderr or result.stdout
    summary = json.loads(result.stdout)
    output = Path(summary["output_dir"])
    plan = json.loads((output / "plan.json").read_text(encoding="utf-8"))
    if defect == "fit_budget":
        assert "Fit count exceeds the campaign limit" in plan["stop_reason"]
        assert plan["planned_fits"] == 2
    else:
        assert "Synthetic CSV" in plan["stop_reason"]
    assert plan["started_trials"] == plan["started_fits"] == 0
    assert not (output / "dataset.csv").exists()
    if defect != "fit_budget":
        with sqlite3.connect(output.parent / "journal.sqlite3") as db:
            (metadata,) = db.execute(
                "SELECT metadata_json FROM experiments WHERE run_id = ?",
                (summary["run_id"],),
            ).fetchone()
        assert summary["reason_code"] == "INVALID_SYNTHETIC_CSV"
        assert json.loads(metadata)["reason_code"] == "INVALID_SYNTHETIC_CSV"
    if defect == "declared_start":
        assert "outside the declared UTC cadence" in plan["stop_reason"]


@pytest.mark.parametrize("model", ["bar_reversal", "volume_movement"])
def test_bar_rule_scores_and_identity_exclude_reserved_csv_rows(tmp_path, model):
    volume_rule = model == "volume_movement"
    path = reversal_config(
        tmp_path,
        "TEST_ALPHA",
        1440,
        2024,
        (0.5, 1.5) if volume_rule else (1, -1),
        volumes=(3, 1),
    )
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    config["research"]["candidates"][0]["model"] = model
    config["study"]["rule"] = model
    path.write_text(yaml.safe_dump(config), encoding="utf-8")

    def run():
        result = cli("run", path)
        assert result.returncode == 0, result.stderr or result.stdout
        output = Path(json.loads(result.stdout)["output_dir"])
        return json.loads((output / "report.json").read_text(encoding="utf-8"))

    before = run()
    key = "volume_movement" if volume_rule else "directional_reversal"
    comparison = before["trials"][0]["metrics"][key]
    assert comparison["accuracy"] == 1.0
    assert comparison["decision"].endswith("ADVANTAGE")
    assert comparison["uncertainty_status"] == "ESTIMATED"
    csv_path = path.with_name("input.csv")
    rows = csv_path.read_text(encoding="utf-8").splitlines()
    for i in range(129, len(rows)):
        timestamp = rows[i].split(",")[0]
        rows[i] = f"{timestamp},200,230,198,229,1000,synthetic"
    csv_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    after = run()
    assert before["dataset_fingerprint"] != after["dataset_fingerprint"]
    assert before["holdout"] == after["holdout"]
    assert before["trials"][0]["metrics"] == after["trials"][0]["metrics"]
    with sqlite3.connect(
        tmp_path / after["configuration"]["journal"]["sqlite_path"]
    ) as db:
        first, second = db.execute(
            "SELECT experiment_id, duplicate_of FROM experiments ORDER BY rowid"
        ).fetchall()
    assert second[1] == first[0]


def read_report(result):
    assert result.returncode == 0, result.stderr or result.stdout
    path = Path(json.loads(result.stdout)["output_dir"])
    assert (path / "dataset.csv").exists()
    markdown = (path / "report.md").read_text(encoding="utf-8")
    assert "No real-world alpha" in markdown
    assert "Synthetic detectability" in markdown
    return json.loads((path / "report.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("variant", ["evaluated", "foreign_day", "screened_out"])
def test_common_market_entry_requires_scientific_qualification(tmp_path, variant):
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
    assert result.returncode == 2
    summary = json.loads(result.stdout)
    assert summary["reason_code"] == "SOURCE_NOT_ALLOWED_FOR_CANDIDATE"
    assert summary["output_dir"] is None
    assert (
        summary["study_data_accesses"]
        == summary["started_workers"]
        == summary["started_fits"]
        == 0
    )


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
    assert_admission_rejection(result, tmp_path, config, "LOCKED_PERIOD")
    assert {child.name for child in (tmp_path / "output").iterdir()} == {
        "journal.sqlite3"
    }

    with pytest.raises(ValueError, match="reserved"):
        import_day.__wrapped__(
            tmp_path / "missing.zip", tmp_path / "missing.checksum", date(2026, 1, 6)
        )
    with pytest.raises(ValueError, match="reserved"):
        import_day.__wrapped__(
            tmp_path / "BTCUSDT-1m-2026-01-06.zip",
            tmp_path / "missing.checksum",
            date(2026, 1, 5),
        )


def test_legacy_supervised_entry_cannot_snapshot_or_launch_without_admission(
    tmp_path, monkeypatch
):
    import runpy

    from aqrs.admission import AdmissionRejected

    monkeypatch.chdir(tmp_path)
    entry = runpy.run_path(str(ROOT / "scripts/m2_supervised_pilot.py"))["main"]
    with pytest.raises(AdmissionRejected, match="not qualified"):
        entry(tmp_path / "blocked")
    assert not (tmp_path / "blocked").exists()


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
    assert plan["planned_trials"] == 1
    assert plan["planned_fits"] == 2
    assert plan["preflight_status"] == "ADMITTED"
    first = read_report(cli("run", config))
    second = read_report(cli("run", config))
    assert first["run_id"] != second["run_id"]
    assert first["dataset_fingerprint"] == second["dataset_fingerprint"]
    assert first["holdout"]["purpose"] == "final_holdout_reserved"
    assert [t["metrics"] for t in first["trials"]] == [
        t["metrics"] for t in second["trials"]
    ]
    assert first["plan"]["completed_fits"] == 2
    assert first["plan"]["sampled_cpu_seconds"] > 0
    assert all(t["evidence_status"] == "INSUFFICIENT_EVIDENCE" for t in first["trials"])
    with sqlite3.connect(tmp_path / "research results Ã¼/journal.sqlite3") as db:
        assert db.execute("PRAGMA integrity_check").fetchone() == ("ok",)
        assert db.execute("SELECT COUNT(*) FROM campaigns").fetchone() == (2,)
        assert db.execute("SELECT COUNT(*) FROM experiments").fetchone() == (2,)
        for (stored,) in db.execute("SELECT metrics_json FROM experiments"):
            comparison = json.loads(stored)["directional_reversal"]
            assert comparison["observations"] == 56
        assert db.execute(
            "SELECT COUNT(*) FROM experiments WHERE duplicate_of IS NOT NULL"
        ).fetchone() == (1,)
    with sqlite3.connect(ledger_path(tmp_path)) as ledger:
        assert ledger.execute("SELECT COUNT(*) FROM variant_exposures").fetchone() == (
            1,
        )


def test_cli_journals_rejected_budget_and_strict_memory_without_fits(tmp_path):
    path = config_at(tmp_path)
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    config["research"]["walk_forward_folds"] = 37_500
    config["resource_governor"]["preflight"]["measure_representative_pilot"] = False
    path.write_text(yaml.safe_dump(config), encoding="utf-8")

    for fixture, fits in ((path, 37_500), (None, 2)):
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
        ).fetchall() == [("REJECTED_PREFLIGHT", "NOT_EVALUATED", 2)]


def test_real_timeout_is_journaled_and_retry_links_prior_attempt(tmp_path, monkeypatch):
    import time

    from test_governor import probe

    from aqrs import research
    from aqrs.config import load
    from aqrs.governor import _supervise_process, supervise

    config, base = load(config_at(tmp_path))
    config["resource_governor"]["preflight"]["measure_representative_pilot"] = False
    calls = []

    def first_blocks(directory, request, trial_seconds, deadline, rss):
        if request.get("stage") in {"detectability", "prepare"}:
            return supervise(directory, request, trial_seconds, deadline, rss)
        calls.append(request["model"])
        if len(calls) == 1:
            return _supervise_process(
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
    assert len(calls) == 1
    rerun, code = research.run(config, base, plan_only=False)
    assert code == 0 and len(calls) == 2
    with sqlite3.connect(base / config["journal"]["sqlite_path"]) as db:
        timed_out = db.execute(
            "SELECT experiment_id, evidence_status, metrics_json FROM experiments "
            "WHERE execution_status = 'TIMED_OUT'"
        ).fetchall()
        assert timed_out == [(f"{failed['run_id']}:REVERSAL", "NOT_EVALUATED", None)]
        metadata, duplicate = db.execute(
            "SELECT metadata_json, duplicate_of FROM experiments WHERE experiment_id = ?",
            (f"{rerun['run_id']}:REVERSAL",),
        ).fetchone()
        assert json.loads(metadata)["prior_attempt_id"] == timed_out[0][0]
        assert duplicate is None


def test_cancellation_stops_remaining_candidates(tmp_path, monkeypatch):
    from aqrs import research
    from aqrs.config import load
    from aqrs.governor import supervise

    config, base = load(config_at(tmp_path))
    config["research"]["candidates"].append({"id": "SECOND", "model": "bar_reversal"})
    calls = []

    def cancel_trial(*args):
        if args[1].get("stage") in {"detectability", "prepare"}:
            return supervise(*args)
        calls.append(args)
        return {
            "execution_status": "CANCELLED",
            "stop_reason": "Cancelled by operator.",
            "completed_fits": 0,
            "peak_rss_mb": None,
            "started": True,
            "runtime_wall_seconds": 0.1,
        }

    monkeypatch.setattr(research, "supervise", cancel_trial)
    summary, code = research.run(config, base, plan_only=False)
    assert code == 130 and summary["execution_status"] == "CANCELLED"
    assert len(calls) == 1
    with sqlite3.connect(base / config["journal"]["sqlite_path"]) as db:
        assert db.execute(
            "SELECT execution_status, evidence_status FROM experiments"
        ).fetchall() == [("CANCELLED", "NOT_EVALUATED"), ("CANCELLED", "NOT_EVALUATED")]


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

    def admitted_preparation(request):
        from aqrs.study_admission import admitted_worker, authorize_worker

        admitted, secret = authorize_worker(request)
        with admitted_worker(admitted, lambda: secret):
            return research.prepare_data(request)

    def changed_preparation(directory, request, *args):
        if request.get("stage") == "prepare":
            return {
                "execution_status": "COMPLETED",
                "stop_reason": None,
                "started": True,
                "completed_fits": 0,
                "peak_rss_mb": None,
                "result": admitted_preparation(request),
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
            journal.start_experiment(
                db, run_id, "REVERSAL", {"evidence_key": "same-key"}
            )
        for db, run_id in ((first, "earlier"), (second, "later")):
            trial = {
                "experiment_id": f"{run_id}:REVERSAL",
                "candidate_id": "REVERSAL",
                "execution_status": "COMPLETED",
                "evidence_status": "INSUFFICIENT_EVIDENCE",
            }
            journal.finish_experiment(db, run_id, trial, {"evidence_key": "same-key"})
        earlier, later = first.execute(
            "SELECT metadata_json, duplicate_of FROM experiments WHERE candidate_id = 'REVERSAL' "
            "ORDER BY rowid"
        ).fetchall()
        assert "prior_attempt_id" not in json.loads(earlier[0])
        assert json.loads(later[0])["prior_attempt_id"] == "earlier:REVERSAL"
        assert later[1] == "earlier:REVERSAL"
