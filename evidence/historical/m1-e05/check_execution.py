"""Verify one scripted execution against the M1-E05 source-day reference."""

import csv
import io
import json
import os
import platform
import subprocess
import sys
from datetime import date
from decimal import Decimal
from hashlib import sha256
from math import isclose
from pathlib import Path
from time import perf_counter
from zipfile import ZipFile

DAY = date(2026, 1, 5)
DIGEST = "a29b45bdb88d5090cfecc61423dab084364a34db96b0788ab77cefc9d4b9567d"
FINGERPRINT = "7ec539e452f4efc7063947409a905f9c3e975b06ddf2585d252cb1ef72457893"
SIGNAL = 720
ENTRY = 721
EXIT = 736
CROSS_BOUNDARY_SIGNAL = 1424
TOLERANCE = 1e-10


def require(condition, message):
    if not condition:
        raise ValueError(message)


def source_opens(archive):
    with ZipFile(archive) as zipped:
        with zipped.open(f"BTCUSDT-1m-{DAY}.csv") as member:
            with io.TextIOWrapper(member, encoding="ascii", newline="") as text:
                rows = csv.reader(text)
                opens = {}
                for index, row in enumerate(rows):
                    if index in (ENTRY, EXIT):
                        opens[index] = Decimal(row[1])
                    if index == EXIT:
                        break
    return opens[ENTRY], opens[EXIT]


def check():
    import numpy as np
    import psutil

    from aqrs import evaluation
    from aqrs.binance_spot_pilot import import_day
    from aqrs.config import load
    from aqrs.market import build_folds, features

    environment = platform.system()
    if environment == "Linux":
        require(os.getuid() == 1000 and not os.getenv("DISPLAY"), "Expected a headless, non-root guest.")
        require(platform.freedesktop_os_release()["ID"] == "ubuntu", "Expected Ubuntu.")
    else:
        require(environment == "Windows", "Unexpected execution platform.")
    process = psutil.Process()
    sampled_rss = [process.memory_info().rss]
    config_path = Path("configs/m1-e04.yaml")
    config, base = load(config_path)
    market = config["market"]
    research = config["research"]
    costs = config["costs"]
    execution = config["execution_simulation"]
    require(
        market["day"] == DAY.isoformat()
        and research["horizon_bars"] == 15
        and execution["allow_short"] is False
        and execution["notional_per_trade"] == 1.0
        and costs == {
            "fee_bps_per_side": 10.0,
            "quoted_spread_bps": 1.0,
            "slippage_bps_per_side": 2.0,
            "decision_buffer_bps": 2.0,
        },
        "The frozen campaign assumptions differ from the approved check.",
    )
    archive = base / market["archive_dir"] / f"BTCUSDT-1m-{DAY}.zip"
    started = perf_counter()
    bars, digest = import_day(archive, archive.with_suffix(".zip.CHECKSUM"), DAY)
    import_seconds = perf_counter() - started
    sampled_rss.append(process.memory_info().rss)
    require(digest == DIGEST and bars.fingerprint == FINGERPRINT, "Unexpected dataset identity.")
    require(len(bars.values) == 1440, "Expected exactly one UTC day.")

    folds = build_folds(
        len(bars.values),
        research["horizon_bars"],
        research["train_bars"],
        research["validation_bars"],
        research["walk_forward_folds"],
    )
    validation_indices = set()
    for _, window in folds:
        validation_indices.update(range(window.start, window.stop))
    require(SIGNAL in validation_indices, "Approved signal is outside validation.")
    require(
        CROSS_BOUNDARY_SIGNAL not in validation_indices
        and max(validation_indices) == CROSS_BOUNDARY_SIGNAL - 1
        and bars.time(CROSS_BOUNDARY_SIGNAL) == "2026-01-05T23:44:00+00:00"
        and CROSS_BOUNDARY_SIGNAL + 16 == len(bars.values),
        "Holdout boundary exclusion failed.",
    )

    started = perf_counter()
    matrix = features(bars)
    feature_seconds = perf_counter() - started
    sampled_rss.append(process.memory_info().rss)
    require(np.isfinite(matrix[SIGNAL]).all(), "Fixture features are not finite.")
    indices = np.array([SIGNAL])
    arguments = (15, False, 1.0, 0.0027, costs)
    started = perf_counter()
    long_result = evaluation.simulate(bars, indices, np.array([0.01]), *arguments)
    flat_result = evaluation.simulate(bars, indices, np.array([0.0]), *arguments)
    simulation_seconds = perf_counter() - started
    sampled_rss.append(process.memory_info().rss)

    reference_entry, reference_exit = source_opens(archive)
    expected_gross = reference_exit / reference_entry - 1
    expected_costs = {"fees": Decimal("0.0020"), "spread": Decimal("0.0001"), "slippage": Decimal("0.0004")}
    expected_net = expected_gross - sum(expected_costs.values())

    require(long_result["trade_count"] == 1 and long_result["decisions"] == {"long": 1, "short": 0, "flat": 0}, "Expected one long trade.")
    require(
        flat_result["trades"] == [] and flat_result["trade_count"] == 0
        and flat_result["decisions"] == {"long": 0, "short": 0, "flat": 1}
        and flat_result["gross_pnl"] == flat_result["net_pnl"] == 0
        and all(cost == 0 for cost in flat_result["cost_totals"].values()),
        "Flat control incurred a trade or a cost.",
    )
    [trade] = long_result["trades"]
    require(
        trade["signal_index"] == SIGNAL and trade["entry_index"] == ENTRY and trade["exit_index"] == EXIT
        and trade["available_at"] == trade["entry_at"] == "2026-01-05T12:01:00+00:00"
        and trade["exit_at"] == "2026-01-05T12:16:00+00:00",
        "Simulation did not follow the fixed time contract.",
    )
    for key, value in expected_costs.items():
        require(isclose(trade[key], float(value), abs_tol=TOLERANCE, rel_tol=0), f"Cost mismatch for {key}.")
        require(isclose(long_result["cost_totals"][key], float(value), abs_tol=TOLERANCE, rel_tol=0), f"Cost total mismatch for {key}.")
    reference = {
        "entry_price": str(reference_entry), "exit_price": str(reference_exit),
        "gross_pnl": str(expected_gross), "net_pnl": str(expected_net),
        "costs": {name: str(value) for name, value in expected_costs.items()},
    }
    for key in ("entry_price", "exit_price", "gross_pnl", "net_pnl"):
        require(isclose(trade[key], float(reference[key]), abs_tol=TOLERANCE, rel_tol=0), f"Trade mismatch for {key}.")
    for key in ("gross_pnl", "net_pnl"):
        require(isclose(long_result[key], float(reference[key]), abs_tol=TOLERANCE, rel_tol=0), f"Result mismatch for {key}.")

    source_root = Path(evaluation.__file__).parent
    source_hashes = {
        path.name: sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
        for path in sorted(source_root.glob("*.py"))
    }
    return {
        "status": "PASS",
        "scope": "M1-E05 engineering check",
        "platform": platform.platform(),
        "python": platform.python_version(),
        "source_hashes": source_hashes,
        "configuration_sha256": sha256(config_path.read_text(encoding="utf-8").encode("utf-8")).hexdigest(),
        "archive_sha256": digest,
        "dataset_fingerprint": bars.fingerprint,
        "observations": len(bars.values),
        "scripted_score": 0.01,
        "decision_threshold": 0.0027,
        "tolerance": TOLERANCE,
        "stages_seconds": {"import": import_seconds, "features": feature_seconds, "simulation_and_flat_control": simulation_seconds},
        "sampled_peak_worker_rss_mib": max(sampled_rss) / 1024**2,
        "trade": trade,
        "reference": reference,
        "flat_control": flat_result,
        "last_eligible_signal_utc": bars.time(max(validation_indices)),
        "excluded_signal_utc": bars.time(CROSS_BOUNDARY_SIGNAL),
        "holdout_authorized_reads": 0,
        "research_trials": 0,
        "model_fits": 0,
    }


def main():
    if sys.argv[1:] == ["--worker"]:
        print(json.dumps(check(), allow_nan=False))
        return 0
    require(sys.argv[1:] == [], "Run the engineering check without arguments.")
    started = perf_counter()
    worker = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "--worker"],
        timeout=30,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if worker.returncode:
        sys.stderr.write(worker.stderr)
        return worker.returncode
    report = json.loads(worker.stdout)
    report["wall_seconds"] = perf_counter() - started
    print(json.dumps(report, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
