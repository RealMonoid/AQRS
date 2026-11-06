import numpy as np
import pytest

from aqrs.evaluation import evaluate, simulate
from aqrs.market import features, generate


def test_matched_policy_uses_next_open_and_costs_cannot_improve_fixed_trades():
    bars = generate(7, 80, 5, "SYNTH")
    indices = np.arange(12, 24)
    scores = np.tile([0.1, 0, -0.1], 4)
    costs = {"fee_bps_per_side": 4, "quoted_spread_bps": 3, "slippage_bps_per_side": 2}
    low = simulate(bars, indices, scores, 3, True, 1, 0.01, costs)
    high = simulate(
        bars, indices, scores, 3, True, 1, 0.01, costs | {"fee_bps_per_side": 8}
    )
    assert low["trade_count"] == high["trade_count"] > 0
    for first, second in zip(low["trades"], high["trades"], strict=True):
        assert first["entry_index"] == first["signal_index"] + 1
        assert first["exit_index"] == first["signal_index"] + 4
        assert first["entry_at"] == first["available_at"]
        assert first["gross_pnl"] == second["gross_pnl"]
        assert first["net_pnl"] > second["net_pnl"]
    assert low["gross_pnl"] - low["net_pnl"] == pytest.approx(
        0.0015 * low["trade_count"]
    )


def test_fit_uses_only_training_statistics_and_controls_match_rows(tmp_path):
    bars = generate(7, 160, 5, "SYNTH")
    np.save(tmp_path / "prefix.npy", bars.values[:140], allow_pickle=False)
    request = {
        "prefix": str(tmp_path / "prefix.npy"),
        "bar_minutes": 5,
        "symbol": "SYNTH",
        "folds": [[12, 46, 50, 70], [12, 66, 70, 90]],
        "horizon": 3,
        "features": ["past_return"],
        "allow_short": True,
        "notional": 1,
        "costs": {
            "fee_bps_per_side": 4,
            "quoted_spread_bps": 3,
            "slippage_bps_per_side": 2,
            "decision_buffer_bps": 2,
        },
    }
    result = evaluate(request, tmp_path)
    assert result["folds"][0]["training_feature_means"] == pytest.approx(
        features(bars)[12:46, :1].mean(axis=0)
    )
    assert result["prediction"]["observations"] == 40
    assert {row["observations"] for row in result["trading"].values()} == {40}
    assert result["trading"]["no_trade"]["trade_count"] == 0
    assert all(t["exit_index"] < 140 for t in result["trading"]["candidate"]["trades"])
