# Explicit __wrapped__ calls below test preserved inner algorithms; FR-005 entry tests use the guarded functions.
from datetime import UTC, datetime
from types import SimpleNamespace

import numpy as np
import pytest

from aqrs import m2_e19
from aqrs.market import generate


def test_coverage_counts_only_non_overlapping_entries():
    bars = generate(42, 100, 1, "SYNTH")
    assert m2_e19.coverage_days(
        bars,
        np.array([12, 13, 42, 72]),
        np.array([True, False, False, True]),
        slice(12, 73),
    ) == {bars.time(12)[:10]: {"accepted": 2, "rejected": 1}}


def test_coverage_requires_both_folds_without_a_price_outcome(tmp_path):
    bars = generate(42, m2_e19.ROWS, 1, "SYNTH")
    original = m2_e19.coverage(bars, {"fit_limit": 2}, tmp_path)
    changed = bars.values.copy()
    changed[:, 1] *= 2
    second = tmp_path / "different-opens"
    second.mkdir()
    assert (
        m2_e19.coverage(type(bars)(changed, bars.symbol, 1), {"fit_limit": 2}, second)
        == original
    )
    assert original["estimator_fits"] == 0
    assert m2_e19.read_json(tmp_path / "fits.json") == 2


def test_extra_archive_is_rejected_before_import(tmp_path, monkeypatch):
    allowlist = m2_e19.d01_archive_rows(m2_e19.read_json(m2_e19.ROOT / m2_e19.D01_PATH))
    allowlist.append({"name": "BTCUSDT-1m-2026-01-06.zip"})
    monkeypatch.setattr(
        "aqrs.m2_e14.load_spot_day", lambda *a, **kw: pytest.fail("Archive read")
    )
    with pytest.raises(ValueError, match="fixed BTCUSDT scope"):
        m2_e19.load_bars({"archives": str(tmp_path), "allowlist": allowlist}, tmp_path)


def test_forward_matches_independent_two_state_calculation_and_rejects_lookahead():
    model = SimpleNamespace(
        means_=np.array([[0.0], [2.0]]),
        covars_=np.array([[[1.0]], [[1.0]]]),
        startprob_=np.array([0.8, 0.2]),
        transmat_=np.array([[0.9, 0.1], [0.2, 0.8]]),
    )
    observations = np.array([0.0, 2.0, 1.0, 1.5])
    first = np.array([0.8, 0.2 * np.exp(-2)])
    first /= first.sum()
    second = (first @ model.transmat_) * np.array([np.exp(-2), 1.0])
    second /= second.sum()

    def score(values):
        return m2_e19.high_state_probabilities(model, values)

    assert score(observations)[:2] == pytest.approx([first[1], second[1]])
    m2_e19.require_causal_prefix(score, observations, 2)
    with pytest.raises(ValueError, match="altered past regime scores"):
        m2_e19.require_causal_prefix(
            lambda sample: score(sample) + sample[-1], observations, 2
        )


@pytest.mark.parametrize("gross_gain_bps", [0, 100])
def test_cost_comparison_distinguishes_null_and_planted_edge(
    gross_gain_bps, tmp_path, monkeypatch
):
    bars = generate(42, 14_400, 1, "SYNTH")
    values = bars.values.copy()
    values[:, 0] += datetime(2025, 12, 1, tzinfo=UTC).timestamp() - values[0, 0]
    values[:, 1] = 100
    positive = np.zeros(len(values), dtype=bool)
    positive[20:5700:60] = True
    volatility = np.full(len(values), 0.0002)
    expected_hmm = []
    for day in (4, 5, 7, 8):
        for k in range(8):
            signal = day * 1440 + 60 * (k + 1)
            positive[signal] = True
            if k % 2 == 0:
                volatility[signal - 1 : signal + 1] = [0.0003, 0.0001]
                values[signal + 31, 1] = 100 + gross_gain_bps / 100
                expected_hmm.append(signal + 1)
            else:
                volatility[signal - 1 : signal + 1] = [0.0001, 0.0003]
    bars = type(bars)(values, bars.symbol, 1)
    monkeypatch.setattr(m2_e19, "volume_inputs", lambda _: (positive, None))
    monkeypatch.setattr(m2_e19, "features", lambda _: np.column_stack([volatility] * 3))
    trains = iter(train for train, _ in m2_e19.folds_for_window())
    model = SimpleNamespace(
        means_=np.array([[1.0], [3.0]]),
        covars_=np.ones((2, 1, 1)),
        transmat_=np.full((2, 2), 0.5),
        startprob_=np.full(2, 0.5),
        monitor_=SimpleNamespace(history=[0.0, 0.0], iter=2),
    )

    def fixed_fit(sample, *_):
        np.testing.assert_array_equal(sample, volatility[next(trains)] * 10_000)
        return model

    monkeypatch.setattr(m2_e19, "fit_hmm", fixed_fit)
    monkeypatch.setattr(
        m2_e19,
        "high_state_probabilities",
        lambda model, data: np.r_[0.0, data[:-1] / 4],
    )
    count_dir = tmp_path / "count"
    count_dir.mkdir()
    count = m2_e19.coverage(bars, {"fit_limit": 2}, count_dir)
    assert count["passes"]
    result = m2_e19.compare(
        bars, {"coverage_folds": count["folds"], "fit_limit": 2}, tmp_path
    )
    assert result["decision"] == ("ADVANCE" if gross_gain_bps else "DEFER")
    assert result["above_flat"] == bool(gross_gain_bps)
    assert [fold["active_days"] for fold in result["folds"]] == [2, 2]
    for fold in result["folds"]:
        assert fold["delta_net_bps_per_opportunity"] == pytest.approx(
            gross_gain_bps / 2
        )
    assert [
        trade["entry_index"] for trade in result["comparison"]["trades"]["hmm"]
    ] == expected_hmm
    assert result["comparison"]["aggregate"]["policies"]["hmm"][
        "net_bps"
    ] == pytest.approx(16 * (gross_gain_bps - 25))


def test_bad_admission_stops_before_launch(tmp_path, monkeypatch):
    admission = tmp_path / "invalid.json"
    admission.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(
        m2_e19, "supervise", lambda *a, **kw: pytest.fail("Worker started")
    )
    with pytest.raises(ValueError, match="clean reviewed revision"):
        m2_e19.run_pilot.__wrapped__(tmp_path, tmp_path / "output", admission)
    assert not (tmp_path / "output").exists()
