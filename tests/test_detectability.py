"""Public engineering cases; owner blind plans remain unseen."""

import json
from pathlib import Path

import numpy as np
import pytest
import yaml

from aqrs import research
from aqrs.admission import AdmissionRejected
from aqrs.detectability import check, estimate, layout, simulated_series
from aqrs.evaluation import score_bar_rule
from aqrs.market import BAR_RULES
from aqrs.study_admission import assess

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def config(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path / "home"))
    c = yaml.safe_load((ROOT / "configs/research.yaml").read_text(encoding="utf-8"))
    c["project"].update(path_base=".", artifact_dir="output")
    c["journal"]["sqlite_path"] = "journal.sqlite3"
    c["study"].update(rule="volume_movement", minimum_effect=0.03)
    c["research"].update(
        train_bars=1440,
        validation_bars=1442,
        walk_forward_folds=2,
        candidates=[{"id": "VOLUME", "model": "volume_movement"}],
    )
    c["market"]["n_bars"] = 5406
    return c


@pytest.mark.parametrize(
    "field",
    [
        "question",
        "rule",
        "minimum_effect",
        "on_advantage",
        "on_no_advantage",
        "on_inconclusive",
    ],
)
def test_missing_field_stops_before_dispatch(config, tmp_path, monkeypatch, field):
    del config["study"][field]
    monkeypatch.setattr(
        research, "supervise", lambda *a, **k: pytest.fail("Dispatch reached")
    )
    result, code = research.run(config, tmp_path, plan_only=False)
    assert code == 2 and result["started_workers"] == result["started_fits"] == 0


def test_question_is_not_a_fixed_sentence_or_an_llm_judgment(config, tmp_path):
    config["study"]["question"] = "My separate prospective synthetic question"
    assert assess(config, tmp_path)["study"]["question"] == config["study"]["question"]


@pytest.mark.parametrize("effect", [0, -0.1, 0.5, True, "0.03", float("nan")])
def test_invalid_effect_rejected(config, tmp_path, effect):
    config["study"]["minimum_effect"] = effect
    with pytest.raises(AdmissionRejected, match="accuracy gap"):
        assess(config, tmp_path)


@pytest.mark.parametrize("rule", ["bar_reversal", "volume_movement"])
def test_planted_gap_is_relative_to_actual_controls_and_shared_scorer(config, rule):
    config["study"]["rule"] = rule
    config["research"]["candidates"][0]["model"] = rule
    folds = layout(config)
    rng = np.random.default_rng(
        79139
    )  # Different from the production simulation stream.
    observed = []
    for _ in range(96):
        bars, control, accuracy = simulated_series(config, folds, rng)
        assert accuracy - control == pytest.approx(0.03)
        scores = score_bar_rule(bars, folds, BAR_RULES[rule])[
            BAR_RULES[rule].result_key
        ]
        observed.append(
            scores["accuracy"]
            - max(scores[f"{name}_accuracy"] for name in BAR_RULES[rule].controls)
        )
    # Finite draws fluctuate; no realization is forced to have the desired score.
    assert np.std(observed) > 0.025
    assert np.mean(observed) == pytest.approx(0.03, abs=0.025)
    if rule == "volume_movement":
        assert control > 0.54  # Includes training-relative prevalence drift.


def test_low_detection_has_prospective_scope_guidance(config):
    result = check(config)
    assert not result["admitted"] and result["planned"]["detection_rate"] < 0.8
    assert result["planned"]["evaluation_days"] == 60
    sufficient = result["first_sufficient_tested_scope"]
    assert sufficient["detection_rate"] >= 0.8
    assert sufficient["evaluation_days"] > 60
    assert config["research"]["validation_bars"] == 1442


def test_weak_plan_stops_before_reading_even_an_invalid_csv(config, tmp_path):
    config["market"].update(
        source="synthetic_csv", csv_path="input.csv", start_at="2024-01-01T00:00:00Z"
    )
    (tmp_path / "input.csv").write_text("This must not be parsed", encoding="utf-8")
    summary, code = research.run(config, tmp_path, plan_only=False)
    assert code == 2 and summary["reason_code"] == "INSUFFICIENT_DETECTABILITY"
    report = json.loads((Path(summary["output_dir"]) / "report.json").read_text())
    assert "preparation" not in report
    assert report["plan"]["started_trials"] == report["plan"]["started_fits"] == 0
    assert not report["variant_ledger_created"]


@pytest.mark.parametrize("rule", ["bar_reversal", "volume_movement"])
def test_adequate_plan_runs_common_workers_and_records_outcome_action(
    config, tmp_path, rule
):
    config["study"].update(rule=rule, minimum_effect=0.20)
    config["research"]["candidates"][0]["model"] = rule
    summary, code = research.run(config, tmp_path, plan_only=False)
    assert code == 0, summary
    report = json.loads((Path(summary["output_dir"]) / "report.json").read_text())
    assert report["detectability"]["admitted"]
    assert report["plan"]["started_trials"] == 1
    assert report["trials"][0]["next_action"] in [
        config["study"][name]
        for name in ("on_advantage", "on_no_advantage", "on_inconclusive")
    ]


def test_detectability_runs_under_existing_wall_guard(config, tmp_path):
    config["resource_governor"]["max_wall_seconds_per_trial"] = 5
    config["market"].update(n_bars=100000, bar_minutes=1)
    config["research"].update(train_bars=25000, validation_bars=25000)
    config["study"]["minimum_effect"] = 0.00001
    # This fits the preflight memory/fit estimate, but the simulation and guidance
    # must still obey the actual external deadline.
    summary, code = research.run(config, tmp_path, plan_only=False)
    assert code != 0
    report = json.loads((Path(summary["output_dir"]) / "report.json").read_text())
    assert report["plan"]["started_trials"] == 0
    assert report["detectability_execution"]["execution_status"] == "TIMED_OUT"


def test_very_short_design_remains_undecidable(config):
    config["research"].update(train_bars=60, validation_bars=10, walk_forward_folds=1)
    config["market"]["n_bars"] = 100
    config["study"]["minimum_effect"] = 0.2
    result = estimate(config, 1)
    assert result["detections"] == 0


@pytest.mark.parametrize("completed_before_failure", [0, 1])
def test_failed_fold_is_started_but_not_completed(
    config, tmp_path, monkeypatch, completed_before_failure
):
    from dataclasses import replace

    from aqrs import evaluation
    from aqrs.storage import write_json

    folds = layout(config)
    bars, _, _ = simulated_series(config, folds, np.random.default_rng(52))
    monkeypatch.setattr(evaluation, "load_prefix", lambda request: bars.values)
    started = []

    def reserve(*args):
        started.append(1)
        write_json(tmp_path / "started_fits.json", len(started))

    monkeypatch.setattr(evaluation, "reserve_fit", reserve)
    rule = BAR_RULES["volume_movement"]
    original = rule.predictions
    calls = []

    def failing(*args):
        calls.append(1)
        if len(calls) > completed_before_failure:
            raise RuntimeError("Injected failure during fold scoring")
        return original(*args)

    with pytest.raises(RuntimeError, match="Injected failure"):
        evaluation.evaluate_bar_rule(
            {"folds": folds, "symbol": bars.symbol, "bar_minutes": bars.bar_minutes},
            tmp_path,
            replace(rule, predictions=failing),
        )
    assert (
        json.loads((tmp_path / "started_fits.json").read_text())
        == completed_before_failure + 1
    )
    complete = tmp_path / "fits.json"
    assert (
        json.loads(complete.read_text()) if complete.exists() else 0
    ) == completed_before_failure


def test_hypothetical_guidance_identifies_unsupported_row_extent(config, monkeypatch):
    from aqrs import detectability

    monkeypatch.setattr(detectability, "REPETITIONS", 1)
    config["market"].update(n_bars=201821, bar_minutes=5)
    config["research"]["validation_bars"] = 80008
    result = estimate(config, 4)
    assert result["required_total_bars"] == 201821
    assert not result["within_configuration_row_limits"]
