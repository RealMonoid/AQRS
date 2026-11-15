"""Bounded Spot data acquisition and offline qualification; no research outcomes."""

import argparse
import csv
import json
import sys
from datetime import UTC, date, datetime, timedelta
from hashlib import sha256
from pathlib import Path
from time import monotonic
from urllib.request import HTTPRedirectHandler, build_opener

import numpy as np
import yaml

from aqrs.binance_spot_pilot import (
    ACTIVITY_COLUMNS,
    IMPORT_ERRORS,
    INPUT_LIMIT,
    load_spot_day,
    require_spot_identity,
)
from aqrs.config import UniqueKeysLoader, fields, load, validate_governor
from aqrs.governor import supervise
from aqrs.market import Bars, validate, write_dataset
from aqrs.platform_guard import capability
from aqrs.provenance import snapshot
from aqrs.storage import fingerprint, write_json
from aqrs.study_admission import unqualified_entry

BASE = "https://data.binance.vision/data/spot/daily/klines"
MAX_STORAGE = 128 * 1024 * 1024




def build_plan(scope: dict, limits: dict, *, acquire: bool) -> dict:
    fields(scope, "id symbols start end")
    if not isinstance(scope["id"], str) or not 1 <= len(scope["id"]) <= 80:
        raise ValueError("Expected a short scope identifier.")
    symbols = scope["symbols"]
    if (
        not isinstance(symbols, list)
        or not 1 <= len(symbols) <= 2
        or any(not isinstance(s, str) for s in symbols)
        or len(set(symbols)) != len(symbols)
    ):
        raise ValueError("Expected one or two distinct symbols.")
    if any(not isinstance(scope[k], str) for k in ("start", "end")):
        raise ValueError("Dates must use YYYY-MM-DD strings.")
    start, end = (date.fromisoformat(scope[k]) for k in ("start", "end"))
    if start.isoformat() != scope["start"] or end.isoformat() != scope["end"]:
        raise ValueError("Dates must use YYYY-MM-DD.")
    days = (end - start).days + 1
    if (
        not 1 <= days <= 31
        or start < date(2017, 1, 1)
        or end >= datetime.now(UTC).date()
    ):
        raise ValueError("Expected 1–31 complete historical UTC days from 2017 onward.")
    entries = []
    for symbol in symbols:
        for index in range(days):
            day = start + timedelta(days=index)
            require_spot_identity(symbol, day)
            name = f"{symbol}-1m-{day}.zip"
            entries.append(
                {
                    "symbol": symbol,
                    "day": day.isoformat(),
                    "name": name,
                    "url": f"{BASE}/{symbol}/1m/{name}",
                }
            )
    limits = json.loads(json.dumps(limits))
    validate_governor(limits)
    issue = capability(limits["memory_mode"])
    if issue:
        raise ValueError(issue)
    if limits["max_research_trials_per_campaign"] < len(symbols):
        raise ValueError(
            "Data worker count exceeds the configured trial-count ceiling."
        )
    if limits["max_peak_rss_mb_per_trial"] < 512:
        raise ValueError(
            "The conservative 512 MiB preparation estimate exceeds the RSS policy."
        )
    # Never let an unrelated configuration increase this increment's admitted limits.
    worker_seconds = min(120, limits["max_wall_seconds_per_trial"])
    campaign_seconds = min(300, limits["max_wall_seconds_per_campaign"])
    plan = {
        "schema_version": "1",
        "scope": scope,
        "scope_id": fingerprint(scope),
        "entries": entries,
        "archive_count": len(entries),
        "bar_count": len(entries) * 1440,
        "max_requests": 2 * len(entries) if acquire else 0,
        "max_download_bytes": len(entries) * (INPUT_LIMIT + 4096) if acquire else 0,
        "max_storage_bytes": MAX_STORAGE,
        "planned_fits": 0,
        "research_trials": 0,
        "data_workers": len(symbols),
        "worker_seconds": worker_seconds,
        "campaign_seconds": campaign_seconds,
        "max_rss_mb": min(4096, limits["max_peak_rss_mb_per_trial"]),
        "memory_mode": limits["memory_mode"],
        "acquire": acquire,
        "limits": limits,
        "protected_date": "2026-01-06",
        "evidence_status": "NOT_EVALUATED",
        "research_ready": False,
        "estimate_method": "512 MiB allowance; online first-day timing times remaining days times two",
    }
    return plan


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Archive redirects are forbidden.")


def fetch_bytes(url: str, allowed: set[str], limit: int) -> bytes:
    if url not in allowed or not url.startswith(BASE + "/"):
        raise ValueError("URL is outside the fixed archive allowlist.")
    with build_opener(NoRedirect()).open(url, timeout=10) as response:
        if response.geturl() != url:
            raise ValueError("Archive redirect or URL mismatch.")
        length = response.headers.get("Content-Length")
        if length is not None and int(length) > limit:
            raise ValueError("Response exceeds the size limit.")
        payload = response.read(limit + 1)
    if len(payload) > limit:
        raise ValueError("Response exceeds the size limit.")
    return payload


def storage_size(root: Path) -> int:
    return sum(p.stat().st_size for p in root.rglob("*") if p.is_file())


def process_symbol(request: dict, directory: Path) -> dict:
    """Run all archive reads and derived writes inside the external supervisor."""
    plan = request["plan"]
    root = Path(request["output"])
    symbol = request["symbol"]
    entries = [e for e in plan["entries"] if e["symbol"] == symbol]
    archive_root = (
        root / "archives" if plan["acquire"] else Path(request["archive_dir"])
    )
    receipts, daily, activity = [], [], []
    started = monotonic()
    try:
        if plan["acquire"]:
            archive_root.mkdir(exist_ok=True)
        allowed = {url for e in entries for url in (e["url"], e["url"] + ".CHECKSUM")}
        for index, entry in enumerate(entries):
            archive = archive_root / entry["name"]
            checksum = archive.with_suffix(".zip.CHECKSUM")
            if plan["acquire"]:
                for url, target, limit in (
                    (entry["url"], archive, INPUT_LIMIT),
                    (entry["url"] + ".CHECKSUM", checksum, 4096),
                ):
                    if target.exists():
                        raise FileExistsError(
                            "Archive target already exists; retries are not automatic."
                        )
                    target.write_bytes(fetch_bytes(url, allowed, limit))
            result = load_spot_day(
                archive, checksum, date.fromisoformat(entry["day"]), symbol=symbol
            )
            daily.append(result.bars.values)
            activity.append(result.activity)
            receipts.append(
                entry
                | {
                    "sha256": result.digest,
                    "checksum_sha256": sha256(checksum.read_bytes()).hexdigest(),
                    "source_timestamp_unit": result.source_timestamp_unit,
                }
            )
            write_json(
                root / f"{symbol}-progress.json", {"validated_archives": receipts}
            )
            if storage_size(root) > MAX_STORAGE:
                raise ValueError("Preparation storage limit exceeded.")
            if index == 0 and plan["acquire"]:
                elapsed = monotonic() - started
                estimated_remaining = 2 * elapsed * (len(entries) - 1) + 5
                remaining = (
                    min(request["worker_deadline"], request["campaign_deadline"])
                    - monotonic()
                )
                write_json(
                    root / f"{symbol}-timing.json",
                    {
                        "first_day_seconds": elapsed,
                        "estimated_remaining_seconds": estimated_remaining,
                        "remaining_seconds": remaining,
                        "safety_factor": 2,
                    },
                )
                if estimated_remaining > remaining:
                    return {
                        "execution_status": "REJECTED_PREFLIGHT",
                        "error": "First-day extrapolation exceeds remaining acquisition time.",
                        "validated_archive_count": len(receipts),
                    }
        bars = Bars(np.concatenate(daily), symbol, 1)
        validate(bars)
        extra = np.concatenate(activity)
        staging = root / f"{symbol}-incomplete"
        staging.mkdir()
        write_dataset(bars, staging / "dataset.csv")
        activity_path = staging / "activity.csv"
        with activity_path.open("w", encoding="utf-8", newline="") as output:
            writer = csv.writer(output)
            writer.writerow(["bar_open_time", "available_at", *ACTIVITY_COLUMNS])
            for index, (quote, trades, buy_base, buy_quote) in enumerate(extra):
                writer.writerow(
                    [
                        bars.time(index),
                        bars.time(index, close=True),
                        quote,
                        int(trades),
                        buy_base,
                        buy_quote,
                    ]
                )
        manifest = {
            "schema_version": "1",
            "symbol": symbol,
            "bar_minutes": 1,
            "bar_count": len(bars.values),
            "dataset_id": bars.fingerprint,
            "activity_sha256": sha256(activity_path.read_bytes()).hexdigest(),
            "dataset_sha256": sha256(
                (staging / "dataset.csv").read_bytes()
            ).hexdigest(),
            "first_bar_open_utc": bars.time(0),
            "last_bar_available_utc": bars.time(-1, close=True),
            "archives": receipts,
            "scope_id": plan["scope_id"],
            "qualified": True,
            "research_ready": False,
            "data_role": "DEVELOPMENT",
            "evidence_status": "NOT_EVALUATED",
        }
        write_json(staging / "manifest.json", manifest)
        if storage_size(root) > MAX_STORAGE:
            raise ValueError("Preparation storage limit exceeded.")
        staging.rename(root / symbol)
        return {"execution_status": "COMPLETED", "manifest": manifest}
    except (*IMPORT_ERRORS, TimeoutError) as error:
        return {
            "execution_status": "FAILED",
            "error": f"{type(error).__name__}: {error}",
            "validated_archive_count": len(receipts),
        }


@unqualified_entry("src.aqrs.spot_dataset.prepare")
def prepare(
    plan: dict, output: Path, *, archive_dir: Path | None = None
) -> tuple[dict, int]:
    started = monotonic()
    # Rebuild admission from the frozen scope before any source/archive access.
    if build_plan(plan["scope"], plan["limits"], acquire=plan["acquire"]) != plan:
        raise ValueError("Plan differs from validated scope and limits.")
    if not plan["acquire"] and archive_dir is None:
        raise ValueError("Offline qualification requires --archive-dir.")
    output.mkdir(parents=True, exist_ok=False)
    deadline = started + plan["campaign_seconds"]
    report = {
        "schema_version": "1",
        "execution_status": "RUNNING",
        "plan": plan,
        "evidence_status": "NOT_EVALUATED",
        "research_ready": False,
        "workers": [],
        "started_at": datetime.now(UTC).isoformat(),
        "protected_access": {
            "authorized_reads": 0,
            "access_measurement": "not_instrumented",
        },
    }
    write_json(output / "plan.json", plan)
    write_json(output / "report.json", report)
    try:
        report["source"] = snapshot(output, Path(__file__))
        for symbol in plan["scope"]["symbols"]:
            request = {
                "plan": plan,
                "output": str(output.resolve()),
                "symbol": symbol,
                "archive_dir": str(archive_dir.resolve()) if archive_dir else None,
                "worker_deadline": monotonic() + plan["worker_seconds"],
                "campaign_deadline": deadline,
            }
            outcome = supervise(
                output,
                request,
                plan["worker_seconds"],
                deadline,
                plan["max_rss_mb"],
                command=[
                    sys.executable,
                    "-B",
                    "-E",
                    str((output / "source/pilot.py").resolve()),
                    "--worker",
                ],
            )
            report["workers"].append(outcome)
            status = outcome["execution_status"]
            if status == "COMPLETED":
                status = outcome["result"]["execution_status"]
            write_json(output / "report.json", report)
            if status != "COMPLETED":
                report["execution_status"] = status
                break
        else:
            report["execution_status"] = "COMPLETED"
    except KeyboardInterrupt:
        report["execution_status"] = "CANCELLED"
    except (OSError, ValueError) as error:
        report.update(
            execution_status="FAILED", error=f"{type(error).__name__}: {error}"
        )
    report["elapsed_seconds"] = monotonic() - started
    report["storage_bytes"] = storage_size(output)
    write_json(output / "report.json", report)
    return report, 0 if report["execution_status"] == "COMPLETED" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["plan", "acquire", "qualify"])
    parser.add_argument("--scope", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=Path("configs/research.yaml"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--archive-dir", type=Path)
    args = parser.parse_args()
    try:
        with args.scope.open("rb") as source:
            payload = source.read(65537)
        if len(payload) > 65536:
            raise ValueError("Scope configuration exceeds size limit.")
        scope = yaml.load(payload.decode("utf-8"), Loader=UniqueKeysLoader)
        config, _ = load(args.config)
        plan = build_plan(
            scope, config["resource_governor"], acquire=args.action != "qualify"
        )
        if args.action == "plan":
            print(json.dumps(plan, indent=2))
            return 0
        if args.output is None:
            raise ValueError("Preparation requires a new --output directory.")
        report, code = prepare(plan, args.output, archive_dir=args.archive_dir)
        print(
            json.dumps(
                {
                    "execution_status": report["execution_status"],
                    "report": str(args.output / "report.json"),
                },
                indent=2,
            )
        )
        return code
    except (ValueError, OSError, yaml.YAMLError) as error:
        print(f"Spot preparation rejected: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--worker":
        from aqrs.worker import run

        run(Path(sys.argv[2]), process_symbol)
    else:
        raise SystemExit(main())
