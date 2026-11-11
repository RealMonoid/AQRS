from pathlib import Path
from time import monotonic

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from aqrs.market import FEATURE_NAMES, Bars, features, targets
from aqrs.storage import write_json
from aqrs.worker import reserve_fit

RIDGE_ALPHA = 1.0
DIAGNOSTIC_IDS = {
    "rank_correlation": "AQRS-DIAG-RANK-V1",
    "prediction_mean": "AQRS-DIAG-PREDICTION-MEAN-V1",
    "prediction_std": "AQRS-DIAG-PREDICTION-SD-V1",
    "target_mean": "AQRS-DIAG-TARGET-MEAN-V1",
    "target_std": "AQRS-DIAG-TARGET-SD-V1",
}


def model():
    return make_pipeline(StandardScaler(), Ridge(alpha=RIDGE_ALPHA, solver="svd"))


def cost_components(costs: dict, notional: float) -> dict[str, float]:
    return {
        "fees": notional * 2 * costs["fee_bps_per_side"] / 10_000,
        "spread": notional * costs["quoted_spread_bps"] / 10_000,
        "slippage": notional * 2 * costs["slippage_bps_per_side"] / 10_000,
    }


def simulate(
    bars: Bars,
    indices: np.ndarray,
    scores: np.ndarray,
    horizon: int,
    allow_short: bool,
    notional: float,
    threshold: float,
    costs: dict,
) -> dict:
    trades = []
    decisions = {"long": 0, "short": 0, "flat": 0}
    free_at = 0
    components = cost_components(costs, notional)
    round_trip = sum(components.values())
    for index, score in zip(indices, scores, strict=True):
        signal = int(index)
        entry = signal + 1
        direction = int(score > threshold) - int(allow_short and score < -threshold)
        if entry < free_at or direction == 0:
            decisions["flat"] += 1
            continue
        exit_index = entry + horizon
        entry_price, exit_price = bars.values[[entry, exit_index], 1]
        gross = float(notional * direction * (exit_price / entry_price - 1))
        side = "long" if direction > 0 else "short"
        decisions[side] += 1
        trades.append(
            {
                "decision": side,
                "signal_index": signal,
                "available_at": bars.time(signal, close=True),
                "entry_index": entry,
                "entry_at": bars.time(entry),
                "entry_price": float(entry_price),
                "exit_index": exit_index,
                "exit_at": bars.time(exit_index),
                "exit_price": float(exit_price),
                "gross_pnl": gross,
                "net_pnl": gross - round_trip,
                **components,
            }
        )
        free_at = exit_index
    equity = np.cumsum([0.0, *(trade["net_pnl"] for trade in trades)])
    return {
        "observations": len(indices),
        "trade_count": len(trades),
        "economic_evidence": {
            "status": "NO_TRADES"
            if not trades
            else "SINGLE_TRADE"
            if len(trades) == 1
            else "DESCRIPTIVE_ONLY",
            "supports_economic_claim": False,
            "independent_sample_size": None,
            "reason": "Trade counts alone do not establish precision or economic evidence.",
        },
        "decisions": decisions,
        "gross_pnl": sum(trade["gross_pnl"] for trade in trades),
        "net_pnl": float(equity[-1]),
        "turnover": 2 * notional * len(trades),
        "held_bars": horizon * len(trades),
        "max_drawdown": float(np.max(np.maximum.accumulate(equity) - equity)),
        "cost_totals": {
            name: value * len(trades) for name, value in components.items()
        },
        "trades": trades,
    }


def evaluate(request: dict, directory: Path, *, model_factory=None) -> dict:
    if model_factory is None:
        model_factory = model
    if "pilot_rows" in request:
        rng = np.random.default_rng(0)
        x = rng.normal(size=(request["pilot_rows"], request["pilot_columns"]))
        y = rng.normal(size=len(x))
        started = monotonic()
        reserve_fit(request, directory, 1)
        model_factory().fit(x, y)
        elapsed = monotonic() - started
        write_json(directory / "fits.json", 1)
        return {"fit_wall_seconds": elapsed, "rows": len(x), "columns": x.shape[1]}

    bars = Bars(
        np.load(request["prefix"], allow_pickle=False),
        request["symbol"],
        request["bar_minutes"],
    )
    horizon = request["horizon"]
    real_spot = request.get("real_spot", False)
    started = monotonic()
    all_features = features(bars)
    timings = {"features": monotonic() - started, "simulation": None}
    x = all_features[:, [FEATURE_NAMES.index(name) for name in request["features"]]]
    y = targets(bars, horizon)
    costs = request["costs"]
    threshold = (
        sum(cost_components(costs, 1).values()) + costs["decision_buffer_bps"] / 10_000
    )
    first_start, first_stop, _, _ = request["folds"][0]
    move = float(np.quantile(np.abs(y[first_start:first_stop]), 0.9))
    feasibility = {
        "training_abs_move_p90": move,
        "required_net_margin_threshold": threshold,
        "scope": "TRAINING_MOVEMENT_SCALE_ONLY",
        "predictability_established": False,
        "reason": "Absolute movement above costs does not establish a conditional net edge.",
    }
    if move <= threshold:
        screened = {
            "feasibility": feasibility | {"status": "SCREENED_OUT"},
            "rationale": "Training move scale does not clear illustrative costs and buffer.",
            "diagnostic_exposure": [],
        }
        if real_spot:
            screened["stage_wall_seconds"] = timings
        return screened

    folds = []
    all_predictions = []
    all_indices = []
    for fit_count, (train_start, train_stop, val_start, val_stop) in enumerate(
        request["folds"], 1
    ):
        train = slice(train_start, train_stop)
        val = slice(val_start, val_stop)
        x_train = x[train]
        reserve_fit(request, directory, len(request["folds"]))
        fitted = model_factory().fit(x_train, y[train])
        write_json(directory / "fits.json", fit_count)
        prediction = fitted.predict(x[val])
        scaler = getattr(fitted, "named_steps", {}).get("standardscaler")
        training_means = scaler.mean_ if scaler is not None else x_train.mean(axis=0)
        all_predictions.append(prediction)
        all_indices.extend(range(val_start, val_stop))
        folds.append(
            {
                "train_start": train_start,
                "train_stop_exclusive": train_stop,
                "val_start": val_start,
                "val_stop_exclusive": val_stop,
                "label_last_required_at": bars.time(train_stop - 1 + horizon + 1),
                "training_feature_means": training_means.tolist(),
                "prediction": prediction_metrics(y[val], prediction),
            }
        )
    indices = np.array(all_indices)
    prediction = np.concatenate(all_predictions)
    started = monotonic()
    trading = {
        name: simulate(
            bars,
            indices,
            scores,
            horizon,
            request["allow_short"],
            request["notional"],
            threshold,
            costs,
        )
        for name, scores in {
            "candidate": prediction,
            "momentum": all_features[indices, 0],
            "no_trade": np.zeros(len(indices)),
        }.items()
    }
    timings["simulation"] = monotonic() - started
    result = {
        "feasibility": feasibility | {"status": "PASSED"},
        "rationale": "One day of research folds is insufficient evidence of real-world alpha."
        if real_spot
        else "Synthetic research folds are insufficient evidence of real-world alpha.",
        "folds": folds,
        "prediction": prediction_metrics(y[indices], prediction),
        "diagnostic_exposure": [
            {
                "diagnostic_id": diagnostic_id,
                "metric": metric,
                "view": view,
                "validation_intervals": intervals,
                "horizon_bars": horizon,
            }
            for view, intervals in [
                ("aggregate", [[fold[2], fold[3]] for fold in request["folds"]]),
                *[
                    (f"fold_{index}", [[fold[2], fold[3]]])
                    for index, fold in enumerate(request["folds"], 1)
                ],
            ]
            for metric, diagnostic_id in DIAGNOSTIC_IDS.items()
        ],
        "trading": trading,
        "benchmark_scope": {
            "momentum": "Raw one-bar return used as a score, not a calibrated horizon forecast.",
            "no_trade": "Flat policy; zero return is not evidence of a profitable strategy.",
        },
        "incremental_net_pnl_vs_momentum": (
            trading["candidate"]["net_pnl"] - trading["momentum"]["net_pnl"]
        ),
    }
    if real_spot:
        result["stage_wall_seconds"] = timings
    return result


def prediction_metrics(actual: np.ndarray, prediction: np.ndarray) -> dict:
    """Describe fixed OOS predictions; never infer significance or admit a policy."""
    actual = np.asarray(actual, dtype=float)
    prediction = np.asarray(prediction, dtype=float)
    if (
        actual.ndim != 1
        or prediction.shape != actual.shape
        or not actual.size
        or not np.isfinite(actual).all()
        or not np.isfinite(prediction).all()
    ):
        raise ValueError("Prediction metrics require nonempty aligned finite vectors.")
    mae = float(np.mean(np.abs(actual - prediction)))
    zero_mae = float(np.mean(np.abs(actual)))
    correlation = None
    if len(actual) < 2:
        rank_status = "INSUFFICIENT_OBSERVATIONS"
    elif np.all(prediction == prediction[0]):
        rank_status = "CONSTANT_PREDICTION"
    elif np.all(actual == actual[0]):
        rank_status = "CONSTANT_TARGET"
    else:
        rank_status = "DEFINED"
        correlation = float(
            np.corrcoef(_average_ranks(actual), _average_ranks(prediction))[0, 1]
        )
    return {
        "observations": len(actual),
        "mae": mae,
        "zero_mae": zero_mae,
        "mae_improvement_vs_zero": zero_mae - mae,
        "diagnostics": {
            "scope": "DESCRIPTIVE_ONLY",
            "rank_correlation": correlation,
            "rank_status": rank_status,
            "prediction_mean": float(np.mean(prediction)),
            "prediction_std": float(np.std(prediction)),
            "target_mean": float(np.mean(actual)),
            "target_std": float(np.std(actual)),
            "return_units": "simple_return",
            "independent_sample_size": None,
            "supports_economic_claim": False,
        },
    }


def _average_ranks(values: np.ndarray) -> np.ndarray:
    """One-based ranks with equal values sharing their average occupied rank."""
    _, inverse, counts = np.unique(values, return_inverse=True, return_counts=True)
    ranks = np.cumsum(counts) - (counts - 1) / 2
    return ranks[inverse]
