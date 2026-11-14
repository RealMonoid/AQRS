"""Fixed M2-E14 comparisons over qualified minute bars."""

from math import fsum
from pathlib import Path

import numpy as np

from aqrs.evaluation import (
    DIAGNOSTIC_IDS,
    cost_components,
    model,
    prediction_metrics,
    simulate,
)
from aqrs.market import Bars, build_folds, features, targets
from aqrs.storage import write_json
from aqrs.worker import reserve_fit

CANDIDATES = ("VOL_CONFIRM_V1", "RIDGE_INCREMENT_V1")
ROWS = 14_400
HORIZON = 30
DAY = 1440
BAND = 480
COSTS = {
    "fee_bps_per_side": 10,
    "quoted_spread_bps": 1,
    "slippage_bps_per_side": 2,
    "decision_buffer_bps": 2,
}
FORECAST_ROLES = ("three_feature_ridge", "one_feature_ridge")
GROUP_VIEWS = ("aggregate", "fold_1", "fold_2", "utc_day", "utc_8h_band_by_day")


def folds_for_window():
    return build_folds(ROWS, HORIZON, 4 * DAY, 3 * DAY, 2)


def volume_inputs(bars: Bars):
    close = bars.values[:, 4]
    positive = np.zeros(len(close), dtype=bool)
    positive[5:] = close[5:] > close[:-5]
    return positive, features(bars)[:, 1]


def match_volume(high, low, band_start, band_stop):
    # The keys are signal indices. A hold starts at the next open.
    def eligible(indices):
        return indices[
            (indices + 1 >= band_start) & (indices + HORIZON + 1 < band_stop)
        ]

    high, low = eligible(high), eligible(low)
    match = None
    no_partner = 0
    capped = 0
    for signal in high:
        left = np.searchsorted(low, signal - HORIZON, side="right")
        right = np.searchsorted(low, signal + HORIZON)
        nearest = list(low[left - 1 : left]) + list(low[right : right + 1])
        if not nearest:
            no_partner += 1
        elif match is None:
            control = min(nearest, key=lambda other: (abs(other - signal), other))
            match = (int(signal), int(control))
        else:
            capped += 1
    return match, {
        "pair_count": int(match is not None),
        "empty_bands": int(not len(high) and not len(low)),
        "high_events_without_eligible_partner": no_partner,
        "events_unselected_under_pair_cap": capped,
    }


def partition(folds):
    yield "aggregate", None, 0, ROWS
    for number, (_, validation) in enumerate(folds, 1):
        yield f"fold_{number}", None, validation.start, validation.start + 3 * DAY
        day_start = validation.start
        for day in range(day_start, day_start + 3 * DAY, DAY):
            yield "utc_day", day, day, day + DAY
            for band in range(day, day + DAY, BAND):
                yield "utc_8h_band_by_day", band, band, band + BAND


def compare_policies(bars, indices, scores, *, threshold, reference, folds=()):
    simulations = {
        name: simulate(bars, indices, score, HORIZON, False, 1, threshold, COSTS)
        for name, score in scores.items()
    }
    result = {
        "trades": {name: value["trades"] for name, value in simulations.items()},
        "utc_day": {},
        "utc_8h_band_by_day": {},
    }
    for view, group, start, stop in partition(folds):
        count = int(np.count_nonzero((indices + 1 >= start) & (indices + 1 < stop)))
        policies = {}
        for name, sim in simulations.items():
            trades = [t for t in sim["trades"] if start <= t["entry_index"] < stop]
            policies[name] = {
                "trade_count": len(trades),
                "skip_count": count - len(trades),
                "gross_bps": 10_000 * fsum(t["gross_pnl"] for t in trades),
                "net_bps": 10_000 * fsum(t["net_pnl"] for t in trades),
                "turnover": 2 * len(trades),
            }
        differences = {
            name: (row["net_bps"] - policies[reference]["net_bps"]) / count
            if count
            else None
            for name, row in policies.items()
            if name != reference
        }
        summary = {
            "eligible_count": count,
            "policies": policies,
            "net_difference_bps_per_eligible_opportunity": differences,
        }
        if group is None:
            result[view] = summary
        else:
            result[view][bars.time(group)] = summary
    return result


def charge_completed(directory: Path, used: int):
    write_json(directory / "fits.json", used)


def table_views(table, values):
    return [
        {"kind": "comparison_table", "table": table, "view": view, "group": group}
        for view in GROUP_VIEWS
        for group in (values[view] if view in GROUP_VIEWS[-2:] else (None,))
    ]


def volume_trial(bars: Bars, request: dict, directory: Path):
    positive, relative = volume_inputs(bars)
    folds = folds_for_window()
    populations, cutoffs, high_flags, bands = [], [], [], []
    for train, validation in folds:
        training_values = relative[train][positive[train]]
        if not training_values.size:
            return {
                "evaluation_status": "UNAVAILABLE",
                "reason": "No positive training moves for volume calibration.",
                "diagnostic_exposure": [],
            }
        reserve_fit(request, directory, 2)
        cutoff = float(np.quantile(training_values, 0.75, method="linear"))
        cutoffs.append(cutoff)
        charge_completed(directory, len(cutoffs))
        signals = np.flatnonzero(positive[validation]) + validation.start
        high = relative[signals] >= cutoff
        populations.append(signals)
        high_flags.append(high)
        for start in range(validation.start, validation.start + 3 * DAY, BAND):
            pair, counts = match_volume(
                signals[high], signals[~high], start, start + BAND
            )
            bands.append(
                {"band_start": bars.time(start), "index": start, "pair": pair, **counts}
            )
    indices = np.concatenate(populations)
    comparison = compare_policies(
        bars,
        indices,
        {
            "volume_filter": np.concatenate(high_flags),
            "positive_move_baseline": np.ones(len(indices)),
        },
        threshold=0,
        reference="positive_move_baseline",
        folds=folds,
    )
    for band in bands:
        if band["pair"] is None:
            continue
        for role, signal in zip(("event", "control"), band["pair"], strict=True):
            trade = simulate(
                bars, np.array([signal]), [1], HORIZON, False, 1, 0, COSTS
            )["trades"][0]
            band[role] = trade
        band["paired_net_difference_bps"] = 10_000 * (
            band["event"]["net_pnl"] - band["control"]["net_pnl"]
        )
    paired = {"utc_day": {}, "utc_8h_band_by_day": {}}
    for view, group, start, stop in partition(folds):
        rows = [band for band in bands if start <= band["index"] < stop]
        matches = [band for band in rows if band["pair"] is not None]
        summary = {
            key: sum(row[key] for row in rows)
            for key in (
                "pair_count",
                "empty_bands",
                "high_events_without_eligible_partner",
                "events_unselected_under_pair_cap",
            )
        }
        summary.update(
            {
                f"mean_{role}_{metric}_bps": (
                    10_000
                    * fsum(band[role][f"{metric}_pnl"] for band in matches)
                    / len(matches)
                    if matches
                    else None
                )
                for role in ("event", "control")
                for metric in ("gross", "net")
            }
        )
        summary["mean_paired_net_difference_bps"] = (
            fsum(band["paired_net_difference_bps"] for band in matches) / len(matches)
            if matches
            else None
        )
        if group is None:
            paired[view] = summary
        else:
            paired[view][bars.time(group)] = summary
    paired["matches"] = [band for band in bands if band["pair"] is not None]
    summary = paired["aggregate"]
    coverage = (
        summary["pair_count"] >= 12
        and sum(d["pair_count"] > 0 for d in paired["utc_day"].values()) >= 4
        and all(paired[fold]["pair_count"] >= 4 for fold in ("fold_1", "fold_2"))
    )
    gates = {
        "coverage": coverage,
        "event_net_at_least_5_bps": (
            summary["mean_event_net_bps"] is not None
            and summary["mean_event_net_bps"] >= 5
        ),
        "pair_difference_at_least_2_bps": (
            summary["mean_paired_net_difference_bps"] is not None
            and summary["mean_paired_net_difference_bps"] >= 2
        ),
    }
    return {
        "evaluation_status": "COMPLETED",
        "cutoffs": cutoffs,
        "paired": paired,
        "comparison": comparison,
        "gates": gates,
        "diagnostic_exposure": table_views("paired_events", paired)
        + table_views("volume_filter_and_positive_move_baseline", comparison),
    }


def ridge_trial(bars: Bars, request: dict, directory: Path):
    folds = folds_for_window()
    actual = targets(bars, HORIZON)
    x = features(bars)
    threshold = (
        sum(cost_components(COSTS, 1).values()) + COSTS["decision_buffer_bps"] / 10_000
    )
    movement = float(np.quantile(np.abs(actual[folds[0][0]]), 0.9))
    movement_view = {
        "kind": "training_screen",
        "metric": "training_abs_move_p90",
        "view": "fold_1_training",
        "interval": [folds[0][0].start, folds[0][0].stop],
    }
    if movement <= threshold:
        return {
            "evaluation_status": "SCREENED_OUT",
            "training_abs_move_p90": movement,
            "diagnostic_exposure": [movement_view],
        }
    fit_count = 0
    forecasts = {role: [] for role in FORECAST_ROLES}
    validation_indices = []
    for train, validation in folds:
        validation_indices.append(np.arange(validation.start, validation.stop))
        for role, columns in zip(
            FORECAST_ROLES, (slice(None), slice(0, 1)), strict=True
        ):
            reserve_fit(request, directory, 4)
            estimator = model().fit(x[train, columns], actual[train])
            fit_count += 1
            charge_completed(directory, fit_count)
            forecasts[role].append(estimator.predict(x[validation, columns]))
    indices = np.concatenate(validation_indices)
    scores = {
        role: np.concatenate(predictions) for role, predictions in forecasts.items()
    }
    prediction = {
        "aggregate": {
            role: prediction_metrics(actual[indices], score)
            for role, score in scores.items()
        }
    }
    for i, (_, validation) in enumerate(folds):
        prediction[f"fold_{i + 1}"] = {
            role: prediction_metrics(actual[validation], values[i])
            for role, values in forecasts.items()
        }
    reductions = {}
    for view, metrics in prediction.items():
        candidate, control = (metrics[role] for role in FORECAST_ROLES)
        reductions[view] = {
            name: (reference - candidate["mae"]) / reference if reference else None
            for name, reference in (
                ("zero", candidate["zero_mae"]),
                ("one_feature", control["mae"]),
            )
        }
    comparison = compare_policies(
        bars,
        indices,
        scores | {"momentum": x[indices, 0], "flat": np.zeros(len(indices))},
        threshold=threshold,
        reference=FORECAST_ROLES[1],
        folds=folds,
    )
    selected = comparison["aggregate"]["policies"][FORECAST_ROLES[0]]
    coverage = (
        selected["trade_count"] >= 12
        and sum(
            day["policies"][FORECAST_ROLES[0]]["trade_count"] > 0
            for day in comparison["utc_day"].values()
        )
        >= 4
        and all(
            comparison[fold]["policies"][FORECAST_ROLES[0]]["trade_count"] >= 4
            for fold in ("fold_1", "fold_2")
        )
    )
    incremental = comparison["aggregate"]["net_difference_bps_per_eligible_opportunity"]
    gates = {
        "coverage": coverage,
        "relative_mae_reduction_at_least_1_percent_each_fold": all(
            value is not None and value >= 0.01
            for fold in ("fold_1", "fold_2")
            for value in reductions[fold].values()
        ),
        "net_at_least_5_bps_per_trade": (
            selected["trade_count"] > 0
            and selected["net_bps"] / selected["trade_count"] >= 5
        ),
        "incremental_net_at_least_2_bps_per_eligible_opportunity": incremental[
            FORECAST_ROLES[0]
        ]
        >= 2,
    }
    return {
        "evaluation_status": "COMPLETED",
        "training_abs_move_p90": movement,
        "predictions": prediction,
        "relative_mae_reductions": reductions,
        "comparison": comparison,
        "gates": gates,
        "diagnostic_exposure": [
            {
                "kind": "forecast_metric",
                "role": role,
                "diagnostic_id": diagnostic_id,
                "view": view,
            }
            for view in prediction
            for role in FORECAST_ROLES
            for diagnostic_id in DIAGNOSTIC_IDS.values()
        ]
        + [{"kind": "forecast_comparison", "view": view} for view in prediction]
        + table_views("ridge_policies", comparison)
        + [movement_view],
    }
