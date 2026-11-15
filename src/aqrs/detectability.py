"""Conditional operating characteristics for the two synthetic bar rules."""

from copy import deepcopy
from math import ceil, sqrt

import numpy as np

from aqrs.admission import SYNTHETIC_START, utc_timestamp
from aqrs.evaluation import score_bar_rule
from aqrs.market import BAR_RULES, Bars, build_folds
from aqrs.storage import fingerprint

REPETITIONS = 256
MIN_DETECTION = 0.80
SIMULATION_SEED = 20261116


def layout(config):
    market, research = config["market"], config["research"]
    end = int(market["n_bars"] * (1 - research["final_holdout_fraction"]))
    return [
        [tr.start, tr.stop, va.start, va.stop]
        for tr, va in build_folds(
            end,
            1,
            research["train_bars"],
            research["validation_bars"],
            research["walk_forward_folds"],
        )
    ]


def simulated_series(config, folds, rng):
    """Plant a population accuracy gap; individual realizations remain random.

    Volume labels and predictions both drift relative to fold training medians.
    Weekly random effects cluster the prediction advantage within calendar days.
    Their declared amplitudes are stress assumptions, not estimates from a CSV.
    """
    market, study = config["market"], config["study"]
    n = folds[-1][3] + 1
    # Preserve calendar geometry for simulated scope guidance. This does not
    # authorize acquisition/access at the prospective dates; run admission does.
    start = (
        utc_timestamp(market["start_at"])
        if market["source"] == "synthetic_csv"
        else SYNTHETIC_START
    )
    times = start.timestamp() + 60 * market["bar_minutes"] * np.arange(n)
    days = (times // 86400).astype(int)
    week = (days - days[0]) // 7
    turbulent = (week % 2).astype(bool)
    q = np.where(turbulent, 0.60, 0.50)
    evaluation = np.concatenate([np.arange(a, b) for _, _, a, b in folds])
    baseline = (
        float(q[evaluation].mean()) if study["rule"] == "volume_movement" else 0.5
    )
    accuracy = baseline + study["minimum_effect"]
    if accuracy >= 1:
        raise ValueError(
            "The requested gap is impossible under the declared drifting control prevalence."
        )
    # Symmetric, persistent random effects preserve the planted expected gap.
    amplitude = np.minimum(
        np.where(turbulent, 0.16, 0.04), min(accuracy - 0.2, 1 - accuracy) * 0.99
    )
    shocks = rng.choice([-1.0, 1.0], int(week.max()) + 1)
    probability = accuracy + amplitude * shocks[week]
    signs = rng.choice([-1, 1], n)
    movement = rng.uniform(0.001, 0.003, n)
    volumes = rng.uniform(1, 3, n)
    values = np.column_stack(
        [
            times,
            np.full(n, 100.0),
            np.full(n, 102.0),
            np.full(n, 98.0),
            100 * (1 + signs * movement),
            volumes,
        ]
    )
    for tr_start, tr_end, va_start, va_end in folds:
        indices = np.arange(va_start, va_end)
        if study["rule"] == "bar_reversal":
            flips = np.where(rng.random(len(indices)) < probability[indices], -1, 1)
            previous = np.sign(values[va_start - 1, 4] - 100)
            signs_at = previous * np.cumprod(flips)
            values[indices, 4] = 100 * (
                1 + signs_at * np.where(turbulent[indices], 0.003, 0.001)
            )
        else:
            volume_median = np.median(values[tr_start:tr_end, 5])
            movement_median = np.median(np.abs(values[tr_start:tr_end, 4] / 100 - 1))
            rate = q[indices]
            predicted = rng.random(len(indices)) < rate
            values[indices - 1, 5] = volume_median * np.where(predicted, 1.5, 0.5)
            p = probability[indices]
            # Joint probabilities give P(correct)=p and P(label above)=rate.
            chance_above = np.where(
                predicted, (p + 2 * rate - 1) / (2 * rate), (1 - p) / (2 * (1 - rate))
            )
            actual = rng.random(len(indices)) < chance_above
            values[indices, 4] = 100 * (
                1 + movement_median * np.where(actual, 1.5, 0.5)
            )
    values[:, 2] = np.maximum(values[:, 1], values[:, 4]) * 1.001
    values[:, 3] = np.minimum(values[:, 1], values[:, 4]) / 1.001
    return Bars(values, market["symbol"], market["bar_minutes"]), baseline, accuracy


def binomial_interval(successes, count):
    """Descriptive 95% Wilson interval for finite Monte Carlo uncertainty."""
    p, z = successes / count, 1.959963984540054
    denominator = 1 + z * z / count
    center = (p + z * z / (2 * count)) / denominator
    radius = z * sqrt(p * (1 - p) / count + z * z / (4 * count * count)) / denominator
    return [max(0.0, center - radius), min(1.0, center + radius)]


def estimate(config, multiplier):
    folds = layout(config)
    rng = np.random.default_rng(np.random.SeedSequence([SIMULATION_SEED, multiplier]))
    rule = BAR_RULES[config["study"]["rule"]]
    detections = 0
    accuracies, controls = [], []
    for _ in range(REPETITIONS):
        bars, expected_control, expected_accuracy = simulated_series(config, folds, rng)
        scores = score_bar_rule(bars, folds, rule)[rule.result_key]
        detections += scores["decision"] == f"{rule.decision_stem}_ADVANTAGE"
        accuracies.append(scores["accuracy"])
        controls.append(max(scores[f"{name}_accuracy"] for name in rule.controls))
    evaluated_bars = sum(b - a for _, _, a, b in folds)
    return {
        "detections": detections,
        "series": REPETITIONS,
        "detection_rate": detections / REPETITIONS,
        "monte_carlo_interval_95": binomial_interval(detections, REPETITIONS),
        "evaluation_bars": evaluated_bars,
        "evaluation_days": evaluated_bars * config["market"]["bar_minutes"] / 1440,
        "validation_bars_per_fold": config["research"]["validation_bars"],
        "required_total_bars": config["market"]["n_bars"],
        "expected_control_accuracy": expected_control,
        "expected_rule_accuracy": expected_accuracy,
        "mean_realized_rule_accuracy": float(np.mean(accuracies)),
        "mean_realized_stronger_control_accuracy": float(np.mean(controls)),
    }


def check(config):
    """Run only in a resource-contained worker; never inspect submitted outcomes."""
    assessments = []
    for multiplier in (1, 2, 4, 8, 16):
        prospective = deepcopy(config)
        research = prospective["research"]
        research["validation_bars"] *= multiplier
        if multiplier != 1:
            prospective["market"]["n_bars"] = (
                ceil(
                    (
                        research["train_bars"]
                        + research["validation_bars"] * research["walk_forward_folds"]
                    )
                    / (1 - research["final_holdout_fraction"])
                )
                + 1
            )
        result = estimate(prospective, multiplier)
        assessments.append(result)
        if result["detection_rate"] >= MIN_DETECTION:
            break
    admitted = assessments[0]["detection_rate"] >= MIN_DETECTION
    sufficient = assessments[-1]["detection_rate"] >= MIN_DETECTION
    return {
        "configuration": fingerprint(config),
        "admitted": admitted,
        "threshold": MIN_DETECTION,
        "minimum_effect": config["study"]["minimum_effect"],
        "effect_units": "accuracy fraction above the stronger constant control",
        "planned": assessments[0],
        "assessed_scopes": assessments,
        "first_sufficient_tested_scope": assessments[-1] if sufficient else None,
        "guidance": (
            "The requested scope reaches the conditional detection target."
            if admitted
            else "Use the first sufficient tested scope as prospective planning guidance; it is not a proven minimum or permission to extend this study."
            if sufficient
            else "No sufficient scope found through the largest assessed scope; the necessary extent remains unresolved."
        ),
        "simulation_series": len(assessments) * REPETITIONS,
        "simulation_rule_evaluations": len(assessments)
        * REPETITIONS
        * config["research"]["walk_forward_folds"],
        "model_fits": 0,
        "assumptions": "Alternating seven-day quiet/volatile phases; volume label/control prevalence 0.50/0.60 relative to fold training medians; symmetric weekly accuracy shocks of up to 0.04/0.16. No submitted outcomes are used. Population gap is exact in expectation, not forced in each realization.",
        "limitations": "Conditional on this synthetic process; no judgment of question meaning, universal power guarantee or market admission.",
    }
