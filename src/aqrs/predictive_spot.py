"""Frozen M2-E22 predictive-first study; official monthly Spot archives only."""

import argparse
import csv
import io
import json
import re
import subprocess
import sys
from calendar import monthrange
from contextlib import closing
from datetime import UTC, date, datetime, timedelta
from hashlib import sha256
from math import sqrt
from pathlib import Path
from statistics import NormalDist
from time import monotonic
from urllib.request import build_opener
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile

import numpy as np

from aqrs import journal
from aqrs.binance_spot_pilot import require_spot_identity
from aqrs.config import load
from aqrs.governor import supervise
from aqrs.market import Bars, validate
from aqrs.platform_guard import capability
from aqrs.provenance import snapshot
from aqrs.spot_dataset import NoRedirect
from aqrs.storage import fingerprint, write_json
from aqrs.worker import reserve_fit
from aqrs.worker import run as run_worker

VARIANT = "REVERSAL_30M_E22_V1"
RUN_ID = "m2-e22-20261114-01"
TRAIN = 91 * 48
ROWS = 456 * 48
START = datetime(2024, 9, 1, tzinfo=UTC)
MONTHS = tuple(
    [f"2024-{m:02d}" for m in range(9, 13)] + [f"2025-{m:02d}" for m in range(1, 12)]
)
BASE = "https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/30m"
INPUT_LIMIT = 1024 * 1024
STORAGE_LIMIT = 128 * 1024 * 1024


def definition() -> dict:
    return {
        "variant": VARIANT,
        "attempt_id": RUN_ID,
        "symbol": "BTCUSDT",
        "bar_minutes": 30,
        "months": list(MONTHS),
        "training": ["2024-09-01", "2024-11-30"],
        "evaluation": ["2024-12-01", "2025-11-30"],
        "holdout": [["2026-01-06", "2026-01-06"], ["2026-09-01", "2026-10-31"]],
        "rule": "Reverse prior completed open-to-close sign; zero uses training majority.",
        "target": "Next bar open-to-close sign; zero scores 0.5 for either direction.",
        "controls": ["always_up", "always_down", "training_majority_tie_up"],
        "hac_lags": [7, 14],
        "one_sided_alpha": 0.05,
        "planning_effect": 0.02,
        "gate": "All four HAC lower bounds above zero versus both constant directions.",
        "costs": {
            "fee_bps_per_side": 10,
            "quoted_spread_bps": 1,
            "slippage_bps_per_side": 2,
        },
        "cost_stage": "Conditional on predictive pass; next-open to following-open long/flat.",
        "diagnostic_views": {"prediction": 1104, "conditional_costs": 12},
        "fits": 1,
        "workers": 2,
        "retries": 0,
        "resamples": 0,
        "test_card": "docs/MILESTONE_STATUS.md#m2-e22-test-card-predictive-first-spot-reversal",
    }


def require_month(month: str) -> date:
    first = date.fromisoformat(month + "-01")
    for offset in range(monthrange(first.year, first.month)[1]):
        require_spot_identity("BTCUSDT", first + timedelta(days=offset))
    if month not in MONTHS:
        raise ValueError("Month is outside the frozen M2-E22 development scope.")
    return first


def fetch(url: str, allowed: set[str], limit: int) -> bytes:
    if url not in allowed or not url.startswith(BASE + "/"):
        raise ValueError("URL is outside the fixed archive allowlist.")
    with build_opener(NoRedirect).open(url, timeout=10) as response:
        size = response.headers.get("Content-Length")
        if size is not None and int(size) > limit:
            raise ValueError("Response exceeds the fixed input limit.")
        payload = response.read(limit + 1)
    if len(payload) > limit:
        raise ValueError("Response exceeds the fixed input limit.")
    return payload


def parse_month(month: str, payload: bytes, checksum: bytes) -> Bars:
    first = require_month(month)
    stem = f"BTCUSDT-30m-{month}"
    if len(payload) > INPUT_LIMIT or len(checksum) > 4096:
        raise ValueError("Input exceeds the fixed byte limit.")
    if checksum.decode("ascii").split() != [sha256(payload).hexdigest(), stem + ".zip"]:
        raise ValueError("Archive checksum or published filename mismatch.")
    n = monthrange(first.year, first.month)[1] * 48
    unit = 1000 if first.year < 2025 else 1_000_000
    start = int(datetime(first.year, first.month, 1, tzinfo=UTC).timestamp())
    values = np.empty((n, 6))
    with ZipFile(io.BytesIO(payload)) as zipped:
        members = zipped.infolist()
        if len(members) != 1 or members[0].filename != stem + ".csv":
            raise ValueError("Expected one correctly named monthly CSV.")
        member = members[0]
        if (
            member.file_size > INPUT_LIMIT
            or member.flag_bits & 1
            or member.compress_type not in (ZIP_STORED, ZIP_DEFLATED)
        ):
            raise ValueError("Unsafe or oversized archive member.")
        with zipped.open(member) as compressed:
            with io.TextIOWrapper(compressed, encoding="ascii", newline="") as source:
                count = 0
                for count, row in enumerate(csv.reader(source, strict=True), 1):
                    if count > n or len(row) != 12:
                        raise ValueError("Wrong monthly row/field count.")
                    seconds = start + (count - 1) * 1800
                    if (
                        int(row[0]) != seconds * unit
                        or int(row[6]) != (seconds + 1800) * unit - 1
                    ):
                        raise ValueError("Invalid timestamp units or cadence.")
                    values[count - 1] = [seconds, *map(float, row[1:6])]
                if count != n:
                    raise ValueError("Incomplete monthly archive.")
    bars = Bars(values, "BTCUSDT", 30)
    validate(bars)
    return bars


def acquire_month(month: str, output: Path) -> tuple[Bars, dict]:
    require_month(month)  # Must precede every network/file operation.
    stem = f"BTCUSDT-30m-{month}.zip"
    url = f"{BASE}/{stem}"
    allowed = {url, url + ".CHECKSUM"}
    payload = fetch(url, allowed, INPUT_LIMIT)
    checksum = fetch(url + ".CHECKSUM", allowed, 4096)
    bars = parse_month(month, payload, checksum)
    (output / stem).write_bytes(payload)
    (output / (stem + ".CHECKSUM")).write_bytes(checksum)
    return bars, {
        "month": month,
        "url": url,
        "checksum_url": url + ".CHECKSUM",
        "archive_sha256": sha256(payload).hexdigest(),
        "checksum_sha256": sha256(checksum).hexdigest(),
        "rows": len(bars.values),
        "bytes": len(payload) + len(checksum),
    }


def check_bars(bars: Bars) -> None:
    validate(bars)
    if (
        bars.symbol != "BTCUSDT"
        or bars.bar_minutes != 30
        or len(bars.values) != ROWS
        or bars.values[0, 0] != START.timestamp()
    ):
        raise ValueError("Dataset differs from the frozen complete development window.")


def predictions(bars: Bars) -> tuple[int, np.ndarray, np.ndarray]:
    check_bars(bars)
    signs = np.sign(bars.values[:, 4] - bars.values[:, 1]).astype(int)
    baseline = 1 if np.sum(signs[:TRAIN]) >= 0 else -1
    pred = -signs[TRAIN - 1 : -1].copy()
    pred[pred == 0] = baseline
    return baseline, pred, signs[TRAIN:]


def hac(values: np.ndarray, lags: int) -> dict:
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or len(x) <= lags or not np.isfinite(x).all() or lags < 0:
        raise ValueError("Invalid daily HAC input.")
    centered = x - x.mean()
    n = len(x)
    variance = float(centered @ centered / n)
    for lag in range(1, lags + 1):
        variance += (
            2 * (1 - lag / (lags + 1)) * float(centered[lag:] @ centered[:-lag] / n)
        )
    se = sqrt(max(0, variance) / n)
    radius = NormalDist().inv_cdf(0.95) * se
    return {
        "lags": lags,
        "mean": float(x.mean()),
        "se": se,
        "lower_95_one_sided": float(x.mean() - radius),
        "upper_95_one_sided": float(x.mean() + radius),
    }


def economics(bars: Bars, pred: np.ndarray, baseline: int) -> dict:
    forward = (bars.values[TRAIN + 1 :, 1] / bars.values[TRAIN:-1, 1] - 1) * 10000
    result = {
        "status": "COMPLETED_ILLUSTRATIVE",
        "opportunities": len(forward),
        "round_trip_cost_bps": 25,
        "cash_bps_per_opportunity": 0,
    }
    for name, active in (
        ("reversal", pred[:-1] > 0),
        ("training_majority", np.full(len(forward), baseline > 0)),
    ):
        gross = np.where(active, forward, 0)
        net = gross - 25 * active
        count = int(active.sum())
        result[name] = {
            "trades": count,
            "flat": len(forward) - count,
            "gross_bps_per_opportunity": float(gross.mean()),
            "net_bps_per_opportunity": float(net.mean()),
            "gross_bps_per_trade": float(gross.sum() / count) if count else None,
            "net_bps_per_trade": float(net.sum() / count) if count else None,
        }
    return result


def measure(bars: Bars) -> dict:
    baseline, pred, truth = predictions(bars)
    hits = np.where(truth == 0, 0.5, pred == truth)
    daily_hits = hits.reshape(365, 48).mean(axis=1)
    controls, contrasts, daily = {}, {}, []
    for name, direction in (("always_up", 1), ("always_down", -1)):
        scores = (
            np.where(truth == 0, 0.5, truth == direction).reshape(365, 48).mean(axis=1)
        )
        controls[name] = scores
        contrasts[name] = {str(lag): hac(daily_hits - scores, lag) for lag in (7, 14)}
    bounds = [row for comparison in contrasts.values() for row in comparison.values()]
    if all(row["lower_95_one_sided"] > 0 for row in bounds):
        decision = "PREDICTIVE_PASS"
    elif any(
        all(row["upper_95_one_sided"] < 0.02 for row in comp.values())
        for comp in contrasts.values()
    ):
        decision = "BELOW_RELEVANT_EFFECT"
    else:
        decision = "INCONCLUSIVE"
    for i in range(365):
        daily.append(
            {
                "day": (date(2024, 12, 1) + timedelta(days=i)).isoformat(),
                "targets": 48,
                "candidate_hits": float(daily_hits[i] * 48),
                "up_hits": float(controls["always_up"][i] * 48),
                "down_hits": float(controls["always_down"][i] * 48),
            }
        )
    prediction = {
        "decision": decision,
        "target_count": len(truth),
        "days": 365,
        "candidate_accuracy": float(hits.mean()),
        "baseline_direction": baseline,
        "training_majority_accuracy": float(
            controls["always_up" if baseline == 1 else "always_down"].mean()
        ),
        "always_up_accuracy": float(controls["always_up"].mean()),
        "always_down_accuracy": float(controls["always_down"].mean()),
        "zero_targets": int((truth == 0).sum()),
        "contrasts": contrasts,
        "effective_independent_count": None,
        "protected_confirmation": False,
    }
    costs = (
        economics(bars, pred, baseline)
        if decision == "PREDICTIVE_PASS"
        else {"status": "NOT_RUN_PREDICTION_GATE"}
    )
    exposure = [
        *[
            {"metric": "accuracy", "view": "aggregate", "arm": arm}
            for arm in (VARIANT, "always_up", "always_down", "training_majority")
        ],
        {"metric": "zero_target_count", "view": "aggregate"},
        *[
            {"metric": "accuracy", "view": row["day"], "arm": arm}
            for row in daily
            for arm in (VARIANT, "always_up", "always_down")
        ],
        *[
            {"metric": "paired_accuracy_HAC_interval", "control": name, "lags": lag}
            for name in controls
            for lag in (7, 14)
        ],
    ]
    if decision == "PREDICTIVE_PASS":
        exposure.extend(
            {"metric": metric, "view": "conditional_costs", "arm": arm}
            for arm in ("reversal", "training_majority")
            for metric in costs[arm]
        )
    return {
        "prediction": prediction,
        "daily": daily,
        "costs": costs,
        "diagnostic_exposure": exposure,
    }


def preflight(limits: dict) -> dict:
    guard = capability(limits.get("memory_mode", "observed_rss"))
    trial = min(120, limits["max_wall_seconds_per_trial"])
    campaign_seconds = min(300, limits["max_wall_seconds_per_campaign"])
    rss = min(4096, limits["max_peak_rss_mb_per_trial"])
    if (
        guard
        or not limits["enabled"]
        or not limits["fail_closed_on_unenforceable_limits"]
        or not limits["preflight"]["enabled"]
        or limits["auto_retry_count"] != 0
        or limits["max_research_trials_per_campaign"] < 2
        or limits["max_model_fits_per_campaign"] < 1
        or limits["max_parallel_trials"] < 1
        or 2 * trial > campaign_seconds
        or trial <= 0
        or rss < 512
    ):
        raise ValueError(
            guard or "Frozen study does not fit the active Governor limits."
        )
    return {
        "status": "READY",
        "workers": 2,
        "calibration_fits": 1,
        "model_fits": 0,
        "concurrency": 1,
        "retries": 0,
        "trial_seconds": trial,
        "campaign_seconds": campaign_seconds,
        "estimated_wall_seconds": 2 * trial,
        "rss_mb": rss,
        "estimate_basis": "Conservative permitted worker upper bounds; no linear compute assumption.",
    }


def synthetic_bars() -> Bars:
    signs = np.resize([1, -1], ROWS)
    values = np.column_stack(
        [
            START.timestamp() + 1800 * np.arange(ROWS),
            np.full(ROWS, 100),
            np.full(ROWS, 102),
            np.full(ROWS, 98),
            100 + signs,
            np.ones(ROWS),
        ]
    )
    return Bars(values, "BTCUSDT", 30)


def worker(request: dict, directory: Path) -> dict:
    output = Path(request["output"])
    if request["stage"] == "acquire":
        receipts, chunks = [], []
        started = monotonic()
        if request["synthetic"]:
            bars = synthetic_bars()
        else:
            for month in MONTHS:
                require_month(month)
            raw = output / "raw"
            raw.mkdir()
            for month in MONTHS:
                url = f"{BASE}/BTCUSDT-30m-{month}.zip"
                receipt = {
                    "month": month,
                    "url": url,
                    "checksum_url": url + ".CHECKSUM",
                    "status": "RUNNING",
                    "started_utc": journal.now(),
                }
                receipts.append(receipt)
                write_json(
                    output / "acquisition.json",
                    {"status": "IN_PROGRESS", "archives": receipts},
                )
                try:
                    bars, completed = acquire_month(month, raw)
                except Exception as error:
                    receipt.update(
                        status="FAILED",
                        error=f"{type(error).__name__}: {error}"[:1000],
                        ended_utc=journal.now(),
                    )
                    result = {"status": "FAILED", "archives": receipts}
                    write_json(output / "acquisition.json", result)
                    return result
                receipt.update(completed, status="COMPLETED", ended_utc=journal.now())
                chunks.append(bars.values)
                write_json(
                    output / "acquisition.json",
                    {"status": "IN_PROGRESS", "archives": receipts},
                )
                if len(receipts) == 1:
                    estimate = 2 * (monotonic() - started) * len(MONTHS) + 5
                    if estimate > request["trial_seconds"]:
                        return {
                            "status": "REJECTED_PREFLIGHT",
                            "archives": receipts,
                            "estimated_acquisition_seconds": estimate,
                            "reason": "First-month conservative extrapolation exceeds worker limit.",
                        }
            bars = Bars(np.concatenate(chunks), "BTCUSDT", 30)
        check_bars(bars)
        np.save(output / "bars.npy", bars.values, allow_pickle=False)
        result = {
            "status": "COMPLETED",
            "archives": receipts,
            "rows": ROWS,
            "dataset_id": bars.fingerprint,
            "staged_sha256": sha256((output / "bars.npy").read_bytes()).hexdigest(),
            "diagnostic_exposure": [],
        }
        write_json(output / "acquisition.json", result)
        return result
    path = output / "bars.npy"
    if (
        path.stat().st_size > 2 * 1024 * 1024
        or sha256(path.read_bytes()).hexdigest() != request["staged_sha256"]
    ):
        raise ValueError("Staged research data changed or exceeded its limit.")
    bars = Bars(np.load(path, allow_pickle=False), "BTCUSDT", 30)
    reserve_fit(request, directory, 1)
    result = measure(bars)
    write_json(directory / "fits.json", 1)
    return result


def campaign(
    output: Path,
    limits: dict,
    *,
    synthetic: bool = False,
    registration: dict | None = None,
) -> dict:
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    config = definition() | {
        "research": {"candidates": [{"id": "acquisition"}, {"id": VARIANT}]},
        "days": ["synthetic"]
        if synthetic
        else [(START.date() + timedelta(days=i)).isoformat() for i in range(456)],
    }
    report = {
        "run_id": RUN_ID,
        "started_utc": journal.now(),
        "configuration": config,
        "synthetic": synthetic,
        "workers": {},
        "results": None,
        "registration": registration,
        "governor_limits": limits,
    }
    started = monotonic()
    with closing(journal.connect(output / "research.sqlite3")) as db:
        journal.begin(db, RUN_ID, fingerprint(config), config, report)
        status = "REJECTED_PREFLIGHT"
        try:
            if not synthetic and (
                registration is None or registration["definition"] != definition()
            ):
                raise ValueError(
                    "Published frozen registration is required before market acquisition."
                )
            report["plan"] = plan = preflight(limits)
            report["provenance"] = snapshot(output, Path(__file__).resolve())
            write_json(output / "registration.json", registration)
            write_json(output / "report.json", report)
            deadline = started + plan["campaign_seconds"]
            command = [
                sys.executable,
                "-B",
                "-E",
                str(output / "source/pilot.py"),
                "--worker",
            ]
            request = {
                "output": str(output),
                "synthetic": synthetic,
                "trial_seconds": plan["trial_seconds"],
                "fit_limit": 1,
            }
            for stage, candidate in (("acquire", "acquisition"), ("analysis", VARIANT)):
                metadata = {
                    "prospective_variant_id": "E22_ACQUISITION_V1"
                    if stage == "acquire"
                    else VARIANT,
                    "evidence_key": fingerprint([config, stage]),
                    "source_id": report["provenance"]["source_id"],
                    "published_revision": (registration or {}).get(
                        "published_revision"
                    ),
                    "dataset_scope": config["days"],
                }
                journal.start_experiment(db, RUN_ID, candidate, metadata)
                outcome = supervise(
                    output,
                    request | {"stage": stage},
                    plan["trial_seconds"],
                    deadline,
                    plan["rss_mb"],
                    command=command,
                )
                result = outcome.get("result", {})
                status = outcome["execution_status"]
                if status == "COMPLETED" and result.get("status") in {
                    "REJECTED_PREFLIGHT",
                    "FAILED",
                }:
                    status = result["status"]
                if (
                    stage == "analysis"
                    and status == "COMPLETED"
                    and outcome["completed_fits"] != 1
                ):
                    status = "FAILED"
                outcome["execution_status"] = status
                report["workers"][stage] = outcome
                if stage == "acquire" and status != "COMPLETED":
                    receipt_path = output / "acquisition.json"
                    partial = (
                        json.loads(receipt_path.read_text(encoding="utf-8"))
                        if receipt_path.exists()
                        else {"archives": []}
                    )
                    partial.update(
                        status=status,
                        ended_utc=journal.now(),
                        stop_reason=result.get("reason") or outcome.get("stop_reason"),
                    )
                    for archive in partial["archives"]:
                        if archive["status"] == "RUNNING":
                            archive.update(
                                status=status,
                                error=outcome.get("stop_reason"),
                                ended_utc=journal.now(),
                            )
                    write_json(receipt_path, partial)
                journal.finish_experiment(
                    db,
                    RUN_ID,
                    {
                        "experiment_id": f"{RUN_ID}:{candidate}",
                        "candidate_id": candidate,
                        "execution_status": status,
                        "evidence_status": "INSUFFICIENT_EVIDENCE"
                        if stage == "analysis" and status == "COMPLETED"
                        else "NOT_EVALUATED",
                        "metrics": outcome,
                    },
                    metadata,
                )
                write_json(output / "report.json", report)
                if status != "COMPLETED":
                    break
                if stage == "acquire":
                    report["dataset_id"] = result["dataset_id"]
                    request["staged_sha256"] = result["staged_sha256"]
                else:
                    report["results"] = result
            if (
                sum(p.stat().st_size for p in output.rglob("*") if p.is_file())
                > STORAGE_LIMIT
            ):
                status = "BUDGET_EXHAUSTED"
                report["stop_reason"] = "Local artifact storage limit exceeded."
        except (Exception, KeyboardInterrupt) as error:
            status = "FAILED" if report["workers"] else "REJECTED_PREFLIGHT"
            report["stop_reason"] = f"{type(error).__name__}: {error}"
        report.update(
            execution_status=status,
            ended_utc=journal.now(),
            elapsed_seconds=monotonic() - started,
        )
        with db:
            db.execute(
                "UPDATE experiments SET execution_status = ? WHERE run_id = ? "
                "AND execution_status IN ('PROPOSED','RUNNING')",
                (status, RUN_ID),
            )
        report["journal_integrity"] = db.execute("PRAGMA integrity_check").fetchone()[0]
        journal.finish_campaign(db, RUN_ID, status, report)
        write_json(output / "report.json", report)
    return report


def register(root: Path) -> dict:
    paths = sorted((root / "src/aqrs").glob("*.py")) + [
        root / "configs/research.yaml",
        root / "docs/MILESTONE_STATUS.md",
        root / "docs/RESEARCH_PROTOCOL.md",
        root / "tests/test_predictive_spot.py",
    ]
    return {
        "definition": definition(),
        "registered_at": journal.now(),
        "files": {
            p.relative_to(root).as_posix(): sha256(p.read_bytes()).hexdigest()
            for p in paths
        },
        "status": "PLANNED_NOT_RUN",
        "metrics": None,
    }


def published_registration(root: Path, revision: str) -> dict:
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Expected a full published commit SHA.")

    def git(*args):
        return subprocess.check_output(["git", *args], cwd=root, timeout=30)

    if git("rev-parse", "HEAD").decode().strip() != revision:
        raise ValueError("Checkout differs from the frozen published revision.")
    remote = git("remote", "get-url", "origin").decode().strip()
    if remote != "https://github.com/RealMonoid/AQRS.git":
        raise ValueError("Unexpected publication remote.")
    if revision not in {
        line.split()[0]
        for line in git("ls-remote", "origin", "refs/heads/*").decode().splitlines()
    }:
        raise ValueError("Frozen revision is not a currently published branch head.")
    relative = "evidence/m2-e22-preregistration.json"
    payload = (root / relative).read_bytes()
    if payload != git("show", f"{revision}:{relative}"):
        raise ValueError("Local registration differs from published content.")
    registration = json.loads(payload)
    if registration["definition"] != definition():
        raise ValueError("Study definition changed after registration.")
    expected_paths = set(register(root)["files"])
    if set(registration["files"]) != expected_paths:
        raise ValueError("Source inventory differs from registration.")
    for name, digest in registration["files"].items():
        if sha256((root / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f"Frozen source changed: {name}")
        if sha256(git("show", f"{revision}:{name}")).hexdigest() != digest:
            raise ValueError(f"Registration differs from published source: {name}")
    return registration | {
        "published_revision": revision,
        "verified_utc": journal.now(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--register", action="store_true")
    action.add_argument("--run", metavar="PUBLISHED_SHA")
    action.add_argument("--smoke", type=Path, metavar="NEW_OUTPUT")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    if args.register:
        path = root / "evidence/m2-e22-preregistration.json"
        path.write_bytes((json.dumps(register(root), indent=2) + "\n").encode("utf-8"))
        print(f"Registered {VARIANT}; no market data accessed.")
        return 0
    config, _ = load(root / "configs/research.yaml")
    registration = published_registration(root, args.run) if args.run else None
    output = args.smoke or root / "artifacts/m2-e22/run-01"
    report = campaign(
        output,
        config["resource_governor"],
        synthetic=bool(args.smoke),
        registration=registration,
    )
    print(f"{report['execution_status']} {output}")
    return 0 if report["execution_status"] == "COMPLETED" else 2


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--worker":
        source = Path(__file__).resolve().parent
        if Path(journal.__file__).resolve().parent != source / "aqrs":
            raise SystemExit("Worker must import the archived AQRS source.")
        run_worker(Path(sys.argv[2]), worker)
    else:
        raise SystemExit(main())
