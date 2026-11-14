"""Three preregistered exploratory E22 filters; offline, counted and supervised."""

import argparse
import csv
import io
import json
import re
import subprocess
import sys
from contextlib import closing
from datetime import timedelta
from hashlib import sha256
from pathlib import Path
from statistics import NormalDist
from time import monotonic
from zipfile import ZipFile

import numpy as np

from aqrs import journal
from aqrs import predictive_spot as base
from aqrs.config import load
from aqrs.platform_guard import capability
from aqrs.provenance import snapshot
from aqrs.storage import fingerprint, write_json
from aqrs.worker import reserve_fit
from aqrs.worker import run as run_worker

QUESTIONS = {
    "large_move": ("M2-E23", 2, "abs(close/open-1)"),
    "relative_volume": ("M2-E24", 3, "volume/mean(volume[t-336*k], k=1..4)"),
    "taker_imbalance": ("M2-E25", 4, "abs(2*taker_buy_base/volume-1)"),
}
ALPHA = 0.005
LAGS = (7, 14)
WEEK = 7 * 48
WARMUP = 4 * WEEK
CARD = "m2-e23-to-e25-test-card-three-e22-filters"
# Bound by the preserved m2-e22-verification.json; do not silently replace inputs.
E22_ACQUISITION_SHA256 = (
    "3c54380a794dc53952c8ff4abd9577923651d95c17f4b3dda865964541c9a31f"
)


def definition(key: str) -> dict:
    if key not in QUESTIONS:
        raise ValueError("Unregistered filter question.")
    work_item, slot, formula = QUESTIONS[key]
    return {
        "work_item": work_item,
        "variant": f"{work_item}_REVERSAL_{key.upper()}_V1",
        "slot": slot,
        "evaluation_variant_limit": 10,
        "prior_variant": base.VARIANT,
        "original_input_receipt_sha256": E22_ACQUISITION_SHA256,
        "symbol": "BTCUSDT",
        "months": list(base.MONTHS),
        "training": ["2024-09-01", "2024-11-30"],
        "evaluation": ["2024-12-01", "2025-11-30"],
        "feature": formula,
        "threshold": "Training finite features at t<=TRAIN-2; linear 80th percentile; strict >.",
        "timing": "Feature at close t selects next bar t+1; group by target UTC day.",
        "ineligible": "Undefined/zero-denominator feature is in neither group.",
        "contrasts": [
            "selected_minus_unselected",
            "selected_minus_up",
            "selected_minus_down",
        ],
        "uncertainty": "Paired daily ratio influence HAC; all calendar days.",
        "hac_lags": [7, 14, 28] if key == "relative_volume" else [7, 14],
        "alpha": ALPHA,
        "coverage": "Both groups occupy >=180 target days and all twelve target months.",
        "gate": "All registered contrast/lag lower bounds >0 and coverage; exploratory only.",
        "multiplicity_limit": "Nominal ten-slot screen is not adaptive or retroactive family-error control.",
        "costs": base.definition()["costs"],
        "cost_stage": "Only after predictive pass; long/flat next-open/following-open; 25 bps.",
        "fits": 2,
        "workers": 1,
        "retries": 0,
        "resamples": 0,
        "network_requests": 0,
        "test_card": f"docs/MILESTONE_STATUS.md#{CARD}",
        "holdout": base.definition()["holdout"],
        "future_lock_start": "2026-12-01T00:00:00Z",
    }


def parse_activity(
    month: str, payload: bytes, checksum: bytes
) -> tuple[base.Bars, np.ndarray]:
    bars = base.parse_month(month, payload, checksum)
    with ZipFile(io.BytesIO(payload)) as zipped:
        with zipped.open(f"BTCUSDT-30m-{month}.csv") as compressed:
            with io.TextIOWrapper(compressed, encoding="ascii", newline="") as source:
                buy = np.array(
                    [float(row[9]) for row in csv.reader(source, strict=True)]
                )
    if not np.isfinite(buy).all() or np.any(buy < 0) or np.any(buy > bars.values[:, 5]):
        raise ValueError("Invalid taker activity volume.")
    return bars, buy


def read_archives(raw: Path, inputs: list[dict]) -> tuple[base.Bars, np.ndarray]:
    if [r.get("month") for r in inputs] != list(base.MONTHS):
        raise ValueError("Input scope differs from the frozen E22 months.")
    for record in inputs:
        base.require_month(record["month"])
        for key in ("archive_sha256", "checksum_sha256"):
            if not re.fullmatch(r"[0-9a-f]{64}", record.get(key, "")):
                raise ValueError("Input scope lacks registered checksums.")
    chunks, activity = [], []
    for record in inputs:
        stem = f"BTCUSDT-30m-{record['month']}.zip"
        payloads = []
        for name, digest, limit in (
            (stem, record["archive_sha256"], base.INPUT_LIMIT),
            (stem + ".CHECKSUM", record["checksum_sha256"], 4096),
        ):
            path = raw / name
            if path.stat().st_size > limit:
                raise ValueError("Archive input exceeds its registered byte limit.")
            payload = path.read_bytes()
            if len(payload) > limit or sha256(payload).hexdigest() != digest:
                raise ValueError("Archive input differs from its registered digest.")
            payloads.append(payload)
        bars, buy = parse_activity(record["month"], *payloads)
        chunks.append(bars.values)
        activity.append(buy)
    bars = base.Bars(np.concatenate(chunks), "BTCUSDT", 30)
    base.check_bars(bars)
    return bars, np.concatenate(activity)


def features(bars: base.Bars, buy: np.ndarray) -> dict[str, np.ndarray]:
    base.check_bars(bars)
    volume = bars.values[:, 5]
    if (
        buy.shape != volume.shape
        or not np.isfinite(buy).all()
        or np.any((buy < 0) | (buy > volume))
    ):
        raise ValueError("Invalid activity shape or values.")
    relative = np.full(base.ROWS, np.nan)
    indices = np.arange(WARMUP, base.ROWS)
    reference = np.mean(
        np.stack([volume[indices - WEEK * k] for k in range(1, 5)]), axis=0
    )
    relative[indices] = np.divide(
        volume[indices],
        reference,
        out=np.full(len(indices), np.nan),
        where=reference > 0,
    )
    share = np.divide(buy, volume, out=np.full(base.ROWS, np.nan), where=volume > 0)
    return {
        "large_move": np.abs(bars.values[:, 4] / bars.values[:, 1] - 1),
        "relative_volume": relative,
        "taker_imbalance": np.abs(2 * share - 1),
    }


def calibrate(feature: np.ndarray) -> float:
    training = feature[: base.TRAIN - 1]
    finite = training[np.isfinite(training)]
    if not len(finite):
        raise ValueError("No eligible training values for the registered threshold.")
    return float(np.quantile(finite, 0.8, method="linear"))


def ratio(numerator: np.ndarray, denominator: np.ndarray) -> tuple[float, np.ndarray]:
    x, n = np.asarray(numerator, float), np.asarray(denominator, float)
    if (
        x.shape != (365,)
        or n.shape != x.shape
        or not np.isfinite(x).all()
        or not np.isfinite(n).all()
        or np.any(n < 0)
        or n.sum() <= 0
    ):
        raise ValueError("Invalid daily ratio contributions.")
    estimate = float(x.sum() / n.sum())
    return estimate, (x - estimate * n) / n.mean()


def interval(estimate: float, influence: np.ndarray, lag: int) -> dict:
    se = base.hac(influence, lag)["se"]
    radius = NormalDist().inv_cdf(1 - ALPHA) * se
    return {
        "estimate": estimate,
        "se": se,
        "lower": estimate - radius,
        "upper": estimate + radius,
        "lags": lag,
        "one_sided_alpha": ALPHA,
    }


def economics(
    bars: base.Bars, pred: np.ndarray, majority: int, selected: np.ndarray
) -> dict:
    result = base.economics(bars, pred, majority)
    result["unfiltered_reversal"] = result.pop("reversal")
    forward = (
        bars.values[base.TRAIN + 1 :, 1] / bars.values[base.TRAIN : -1, 1] - 1
    ) * 10000
    active = selected[:-1] & (pred[:-1] > 0)
    gross = np.where(active, forward, 0)
    net = gross - 25 * active
    count = int(active.sum())
    result["filtered"] = {
        "trades": count,
        "flat": int(len(forward) - count),
        "gross_bps_per_trade": float(gross.sum() / count) if count else None,
        "net_bps_per_trade": float(net.sum() / count) if count else None,
        "gross_bps_per_opportunity": float(gross.mean()),
        "net_bps_per_opportunity": float(net.mean()),
    }
    result["owner_decision_required"] = bool(count and net.sum() > 0)
    return result


def measure(bars: base.Bars, buy: np.ndarray, key: str) -> dict:
    specification = definition(key)
    feature = features(bars, buy)[key]
    threshold = calibrate(feature)
    majority, pred, truth = base.predictions(bars)
    values = feature[base.TRAIN - 1 : -1]
    eligible = np.isfinite(values)
    selected = eligible & (values > threshold)
    other = eligible & ~selected
    hits = np.where(truth == 0, 0.5, pred == truth)
    scores = {
        "up": np.where(truth == 0, 0.5, truth == 1),
        "down": np.where(truth == 0, 0.5, truth == -1),
    }

    def totals(x):
        return np.asarray(x, float).reshape(365, 48).sum(axis=1)

    dates = [
        (base.START.date() + timedelta(days=91 + i)).isoformat() for i in range(365)
    ]
    sn, un = totals(selected), totals(other)
    sh, uh = totals(selected * hits), totals(other * hits)
    days = {
        "selected": int(np.count_nonzero(sn)),
        "unselected": int(np.count_nonzero(un)),
    }
    months = {
        name: sorted({dates[i][:7] for i, n in enumerate(counts) if n > 0})
        for name, counts in (("selected", sn), ("unselected", un))
    }
    coverage = all(days[name] >= 180 and len(months[name]) == 12 for name in days)
    prediction = {
        "decision": "INSUFFICIENT_COVERAGE",
        "selected_cases": int(sn.sum()),
        "unselected_cases": int(un.sum()),
        "ineligible_cases": int((~eligible).sum()),
        "days": days,
        "months": months,
        "threshold": threshold,
        "training_majority": majority,
        "selected_accuracy": float(sh.sum() / sn.sum()) if sn.sum() else None,
        "unselected_accuracy": float(uh.sum() / un.sum()) if un.sum() else None,
        "selected_controls": {
            name: float((selected * value).sum() / sn.sum()) if sn.sum() else None
            for name, value in scores.items()
        },
        "contrasts": {},
        "protected_confirmation": False,
        "effective_independent_count": None,
        "family_error_calibrated": False,
    }
    if sn.sum() and un.sum():
        sr, si = ratio(sh, sn)
        ur, ui = ratio(uh, un)
        comparisons = {"selected_minus_unselected": (sr - ur, si - ui)}
        for name, value in scores.items():
            comparisons[f"selected_minus_{name}"] = ratio(
                totals(selected * (hits - value)), sn
            )
        prediction["contrasts"] = {
            name: {
                str(lag): interval(value, influence, lag)
                for lag in specification["hac_lags"]
            }
            for name, (value, influence) in comparisons.items()
        }
        if coverage:
            bounds = [
                b
                for comparison in prediction["contrasts"].values()
                for b in comparison.values()
            ]
            prediction["decision"] = (
                "EXPLORATORY_PREDICTIVE_PASS"
                if all(b["lower"] > 0 for b in bounds)
                else "INCONCLUSIVE"
            )
            if all(
                b["upper"] <= 0
                for b in prediction["contrasts"]["selected_minus_unselected"].values()
            ):
                prediction["decision"] = "NO_STRONGER_ACCURACY"
    daily = [
        {
            "day": dates[i],
            "selected": int(sn[i]),
            "unselected": int(un[i]),
            "selected_hits": float(sh[i]),
            "unselected_hits": float(uh[i]),
            **{
                f"selected_{name}_hits": float(totals(selected * value)[i])
                for name, value in scores.items()
            },
        }
        for i in range(365)
    ]
    costs = (
        economics(bars, pred, majority, selected)
        if prediction["decision"] == "EXPLORATORY_PREDICTIVE_PASS"
        else {"status": "NOT_RUN_PREDICTION_GATE"}
    )
    return {
        "definition": specification,
        "prediction": prediction,
        "daily": daily,
        "costs": costs,
        "diagnostic_exposure": [
            *[
                {"metric": metric, "view": "aggregate"}
                for metric in (
                    "selected_accuracy",
                    "unselected_accuracy",
                    "selected_up_accuracy",
                    "selected_down_accuracy",
                    "selection_counts",
                    "calendar_coverage",
                )
            ],
            *[
                {"metric": name, "lags": lag}
                for name in prediction["contrasts"]
                for lag in specification["hac_lags"]
            ],
            *[{"metric": "daily_counts_and_hits", "view": day} for day in dates],
            *(
                [
                    {"metric": "conditional_costs", "arm": arm}
                    for arm in (
                        "filtered",
                        "unfiltered_reversal",
                        "training_majority",
                        "cash",
                    )
                ]
                if costs["status"] == "COMPLETED_ILLUSTRATIVE"
                else []
            ),
        ],
    }


def synthetic_inputs(*, null: bool = False) -> tuple[base.Bars, np.ndarray]:
    ix = np.arange(base.ROWS)
    # Daily rotation avoids making the planted event a fixed weekly clock slot.
    event = (ix % 8) == ((ix // 48) % 8)
    signs = np.resize([1, 1, -1, -1], base.ROWS)
    locations = np.flatnonzero(event & (ix < base.ROWS - 1))
    signs[locations] = np.where(np.arange(len(locations)) % 2, -1, 1)
    signs[locations + 1] = -signs[locations]
    if null:
        no_hit = np.arange(len(locations)) % 4 >= 2
        signs[locations[no_hit] + 1] *= -1
    magnitude = np.where(event, 1.0, 0.1)
    volume = np.where(event, 10.0, 1.0)
    values = np.column_stack(
        [
            base.START.timestamp() + ix * 1800,
            np.full(base.ROWS, 100),
            np.full(base.ROWS, 102),
            np.full(base.ROWS, 98),
            100 + magnitude * signs,
            volume,
        ]
    )
    return base.Bars(values, "BTCUSDT", 30), volume * np.where(event, 0.95, 0.5)


def preflight(limits: dict) -> dict:
    guard = capability(limits.get("memory_mode", "observed_rss"))
    trial = min(120, limits["max_wall_seconds_per_trial"])
    campaign = min(300, limits["max_wall_seconds_per_campaign"])
    rss = min(4096, limits["max_peak_rss_mb_per_trial"])
    if (
        guard
        or not limits["enabled"]
        or not limits["fail_closed_on_unenforceable_limits"]
        or not limits["preflight"]["enabled"]
        or limits["auto_retry_count"] != 0
        or limits["max_research_trials_per_campaign"] < 1
        or limits["max_model_fits_per_campaign"] < 2
        or limits["max_parallel_trials"] < 1
        or trial <= 0
        or campaign < trial
        or rss < 512
    ):
        raise ValueError(guard or "Filter question exceeds active Governor limits.")
    return {
        "workers": 1,
        "fits": 2,
        "trial_seconds": trial,
        "campaign_seconds": campaign,
        "rss_mb": rss,
        "estimate_basis": "One permitted worker upper bound; no retries or network.",
    }


def worker(request: dict, directory: Path) -> dict:
    definition(request["key"])
    if request.get("inject_failure"):
        raise ValueError("Synthetic injected failure before archive access.")
    bars, buy = (
        synthetic_inputs()
        if request["synthetic"]
        else read_archives(Path(request["raw"]), request["inputs"])
    )
    reserve_fit(request, directory, 2)
    reserve_fit(request, directory, 2)
    result = measure(bars, buy, request["key"])
    write_json(directory / "fits.json", 2)
    return result


def campaign(
    output: Path,
    key: str,
    limits: dict,
    *,
    synthetic: bool = False,
    registration: dict | None = None,
    raw: Path | None = None,
    inject_failure: bool = False,
) -> dict:
    spec = definition(key)
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    run_id = spec["work_item"].lower() + "-20261114-01"
    variant = spec["variant"]
    config = spec | {"research": {"candidates": [{"id": variant}]}}
    report = {
        "run_id": run_id,
        "started_utc": journal.now(),
        "configuration": config,
        "synthetic": synthetic,
        "registration": registration,
        "worker": None,
        "results": None,
    }
    started = monotonic()
    with closing(journal.connect(output / "research.sqlite3")) as db:
        journal.begin(db, run_id, fingerprint(config), config, report)
        metadata = {
            "prospective_variant_id": variant,
            "evidence_key": fingerprint(spec),
            "dataset_scope": spec["evaluation"],
        }
        status = "REJECTED_PREFLIGHT"
        try:
            if not synthetic and (
                registration is None
                or registration["definition"] != spec
                or raw is None
                or inject_failure
            ):
                raise ValueError(
                    "Verified published registration and fixed inputs are required."
                )
            report["plan"] = plan = preflight(limits)
            report["governor_limits"] = limits
            report["provenance"] = snapshot(output, Path(__file__).resolve())
            metadata.update(
                source_id=report["provenance"]["source_id"],
                published_revision=(registration or {}).get("published_revision"),
            )
            journal.start_experiment(db, run_id, variant, metadata)
            write_json(output / "report.json", report)
            request = {
                "key": key,
                "synthetic": synthetic,
                "raw": str(raw) if raw else None,
                "inputs": (registration or {}).get("inputs", []),
                "fit_limit": 2,
                "inject_failure": inject_failure,
            }
            outcome = base.supervise(
                output,
                request,
                plan["trial_seconds"],
                started + plan["campaign_seconds"],
                plan["rss_mb"],
                command=[
                    sys.executable,
                    "-B",
                    "-E",
                    str(output / "source/pilot.py"),
                    "--worker",
                ],
            )
            report["worker"] = outcome
            status = outcome["execution_status"]
            if status == "COMPLETED" and (
                outcome["started_fits"] != 2 or outcome["completed_fits"] != 2
            ):
                status = "FAILED"
                report["stop_reason"] = (
                    "Calibration accounting differs from the fixed plan."
                )
            if status == "COMPLETED":
                report["results"] = outcome["result"]
        except (Exception, KeyboardInterrupt) as error:
            status = "FAILED" if report["worker"] else "REJECTED_PREFLIGHT"
            report["stop_reason"] = f"{type(error).__name__}: {error}"
        report.update(
            execution_status=status,
            ended_utc=journal.now(),
            elapsed_seconds=monotonic() - started,
        )
        journal.finish_experiment(
            db,
            run_id,
            {
                "experiment_id": f"{run_id}:{variant}",
                "candidate_id": variant,
                "execution_status": status,
                "evidence_status": "INSUFFICIENT_EVIDENCE"
                if status == "COMPLETED"
                else "NOT_EVALUATED",
                "metrics": report["worker"],
            },
            metadata,
        )
        report["journal_integrity"] = db.execute("PRAGMA integrity_check").fetchone()[0]
        journal.finish_campaign(db, run_id, status, report)
        write_json(output / "report.json", report)
    return report


def register(root: Path, key: str) -> dict:
    spec = definition(key)
    payload = (root / "artifacts/m2-e22/run-01/acquisition.json").read_bytes()
    if sha256(payload).hexdigest() != E22_ACQUISITION_SHA256:
        raise ValueError(
            "Input metadata differs from the preserved original E22 receipt."
        )
    receipt = json.loads(payload)
    inputs = [
        {k: r[k] for k in ("month", "archive_sha256", "checksum_sha256")}
        for r in receipt["archives"]
    ]
    if receipt["status"] != "COMPLETED" or [r["month"] for r in inputs] != list(
        base.MONTHS
    ):
        raise ValueError(
            "Expected completed E22 input metadata; no archive is opened here."
        )
    paths = sorted((root / "src/aqrs").glob("*.py")) + [
        root / name
        for name in (
            "configs/research.yaml",
            "docs/RESEARCH_PROTOCOL.md",
            "AGENTS.md",
            "tests/test_reversal_filters.py",
            "tests/test_predictive_spot.py",
        )
    ]
    card = (
        (root / "docs/MILESTONE_STATUS.md")
        .read_text(encoding="utf-8")
        .split("## M2-E23 to E25 Test Card:", 1)[1]
        .split("## Research and backtesting learning", 1)[0]
    )
    return {
        "definition": spec,
        "registered_at": journal.now(),
        "inputs": inputs,
        "test_card": card,
        "files": {
            p.relative_to(root).as_posix(): sha256(p.read_bytes()).hexdigest()
            for p in paths
        },
        "status": "PLANNED_NOT_RUN",
        "metrics": None,
    }


def published_registration(root: Path, key: str, revision: str) -> dict:
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Expected full published source revision.")

    def git(*args):
        return subprocess.check_output(["git", *args], cwd=root, timeout=30)

    if (
        git("rev-parse", "HEAD").decode().strip() != revision
        or git("remote", "get-url", "origin").decode().strip()
        != "https://github.com/RealMonoid/AQRS.git"
    ):
        raise ValueError("Source checkout or publication remote differs.")
    if revision not in {
        line.split()[0]
        for line in git("ls-remote", "origin", "refs/heads/*").decode().splitlines()
    }:
        raise ValueError("Source is not a published branch head.")
    name = f"evidence/{QUESTIONS[key][0].lower()}-preregistration.json"
    payload = (root / name).read_bytes()
    if payload != git("show", f"{revision}:{name}"):
        raise ValueError("Registration differs from publication.")
    registered = json.loads(payload)
    expected = register(root, key)
    if any(
        registered[field] != expected[field]
        for field in ("definition", "inputs", "test_card", "files")
    ):
        raise ValueError("Registered definition, inputs, card or source changed.")
    for name, digest in registered["files"].items():
        if sha256(git("show", f"{revision}:{name}")).hexdigest() != digest:
            raise ValueError(f"Source differs from published bytes: {name}")
    return registered | {"published_revision": revision, "verified_utc": journal.now()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key", choices=QUESTIONS, required=True)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--register", action="store_true")
    actions.add_argument("--run", metavar="PUBLISHED_SHA")
    actions.add_argument("--smoke", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    work = QUESTIONS[args.key][0].lower()
    if args.register:
        path = root / f"evidence/{work}-preregistration.json"
        path.write_bytes(
            (
                json.dumps(register(root, args.key), indent=2, allow_nan=False) + "\n"
            ).encode()
        )
        print(f"Registered {work}; metadata only, no market archive opened.")
        return 0
    config, _ = load(root / "configs/research.yaml")
    registration = (
        published_registration(root, args.key, args.run) if args.run else None
    )
    output = args.smoke or root / f"artifacts/{work}/run-01"
    report = campaign(
        output,
        args.key,
        config["resource_governor"],
        synthetic=bool(args.smoke),
        registration=registration,
        raw=root / "artifacts/m2-e22/run-01/raw",
    )
    print(f"{report['execution_status']} {output}")
    return 0 if report["execution_status"] == "COMPLETED" else 2


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--worker":
        if (
            Path(journal.__file__).resolve().parent
            != Path(__file__).resolve().parent / "aqrs"
        ):
            raise SystemExit("Worker must use archived AQRS source.")
        run_worker(Path(sys.argv[2]), worker)
    else:
        raise SystemExit(main())
