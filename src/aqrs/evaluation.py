from pathlib import Path
from time import monotonic

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from aqrs.market import FEATURE_NAMES, Bars, features, targets
from aqrs.storage import write_json

RIDGE_ALPHA = 1.0


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
    }
    if move <= threshold:
        screened = {
            "feasibility": feasibility | {"status": "SCREENED_OUT"},
            "rationale": "Training move scale does not clear illustrative costs and buffer.",
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
        "trading": trading,
        "incremental_net_pnl_vs_momentum": (
            trading["candidate"]["net_pnl"] - trading["momentum"]["net_pnl"]
        ),
    }
    if real_spot:
        result["stage_wall_seconds"] = timings
    return result


def prediction_metrics(actual: np.ndarray, prediction: np.ndarray) -> dict:
    mae = float(np.mean(np.abs(actual - prediction)))
    zero_mae = float(np.mean(np.abs(actual)))
    return {
        "observations": len(actual),
        "mae": mae,
        "zero_mae": zero_mae,
        "mae_improvement_vs_zero": zero_mae - mae,
    }
