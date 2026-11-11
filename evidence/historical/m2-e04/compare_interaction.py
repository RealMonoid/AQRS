"""Compare the existing Ridge pipeline on fixed synthetic interaction fixtures."""

import json
import sys

import numpy as np

from aqrs.evaluation import RIDGE_ALPHA, model, prediction_metrics

STATES = np.array([[-1, -1], [-1, 1], [1, -1], [1, 1]])
TRAIN_ROWS = 32
EVALUATION_ROWS = 16
TOLERANCE = 1e-10


def fixtures():
    features = np.tile(STATES, (12, 1))
    cross_term = features[:, 0] * features[:, 1]
    xor = -cross_term
    null = np.repeat(np.tile([1, -1], 6), len(STATES))
    return features, cross_term, xor, null


def check_balance(features, xor, null):
    for start, stop in ((0, TRAIN_ROWS), (TRAIN_ROWS, TRAIN_ROWS + EVALUATION_ROWS)):
        rows = features[start:stop]
        for feature in rows.T:
            for value in (-1, 1):
                group = xor[start:stop][feature == value]
                if len(group) != (stop - start) // 2 or group.sum() != 0:
                    raise ValueError("XOR targets must balance within each feature value.")
        for state in STATES:
            group = null[start:stop][np.all(rows == state, axis=1)]
            if len(group) != (stop - start) // 4 or group.sum() != 0:
                raise ValueError("Null targets must balance within each joint state.")


def main():
    features, cross_term, xor, null = fixtures()
    check_balance(features, xor, null)
    representations = (
        ("additive", features),
        ("interaction", np.column_stack((features, cross_term))),
    )
    cases = {}
    fits = 0
    for name, target in (("xor", xor), ("null", null)):
        metrics = {}
        for representation, inputs in representations:
            pipeline = model()
            print(f"Starting fit {fits + 1}: {name}/{representation}", file=sys.stderr, flush=True)
            pipeline.fit(inputs[:TRAIN_ROWS], target[:TRAIN_ROWS])
            fits += 1
            prediction = pipeline.predict(inputs[TRAIN_ROWS:])
            metrics[representation] = prediction_metrics(target[TRAIN_ROWS:], prediction)
        additive = metrics["additive"]["mae"]
        interaction = metrics["interaction"]["mae"]
        improvement = additive - interaction
        expected = improvement >= 0.90 if name == "xor" else abs(interaction - 1) <= TOLERANCE
        cases[name] = {
            "metrics": metrics,
            "mae_improvement_vs_additive": improvement,
            "passed": abs(additive - 1) <= TOLERANCE and expected,
        }
    print(json.dumps({
        "variant_id": "M2-E04",
        "training_rows_per_fixture": TRAIN_ROWS,
        "evaluation_rows_per_fixture": EVALUATION_ROWS,
        "ridge_alpha": RIDGE_ALPHA,
        "fits": fits,
        "market_data_reads": 0,
        "holdout_reads": 0,
        "cases": cases,
        "passed": all(case["passed"] for case in cases.values()),
    }, indent=2))


if __name__ == "__main__":
    main()
