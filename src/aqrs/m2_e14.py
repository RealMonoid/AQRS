"""Guarded entry for the fixed BTCUSDT discovery comparisons."""

import argparse
import json
import os
import re
import subprocess
import sys
from contextlib import closing
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from time import monotonic
from uuid import uuid4
from zipfile import BadZipFile, ZipFile

import numpy as np

from aqrs import journal
from aqrs.binance_spot_pilot import load_spot_day
from aqrs.config import load
from aqrs.discovery import (
    CANDIDATES,
    COSTS,
    FORECAST_ROLES,
    GROUP_VIEWS,
    HORIZON,
    ROWS,
    folds_for_window,
    ridge_trial,
    volume_trial,
)
from aqrs.evaluation import DIAGNOSTIC_IDS, evaluate
from aqrs.governor import supervise
from aqrs.market import Bars, generate, validate
from aqrs.platform_guard import capability
from aqrs.provenance import snapshot
from aqrs.storage import fingerprint, write_json, write_text
from aqrs.worker import run as run_worker

ROOT = Path(__file__).resolve().parents[2]
SYMBOL = "BTCUSDT"
STATUS_PATH = "docs/MILESTONE_STATUS.md"
EXPOSURE_PATH = "evidence/exposure.json"
D01_PATH = "evidence/aqrs-d01-verification.json"
E17_PATH = "evidence/m2-e17-verification.json"
MANIFEST_PATH = "evidence/manifest.json"


@dataclass(frozen=True)
class Campaign:
    name: str
    first_day: date
    variants: tuple[str, str]
    evidence_files: tuple[str, ...]

    @property
    def days(self):
        return tuple(
            (self.first_day + timedelta(days=i)).isoformat() for i in range(10)
        )

    @property
    def definition_files(self):
        return (STATUS_PATH, EXPOSURE_PATH, *self.evidence_files)

    @property
    def branch(self):
        return f"codex/{self.name.lower()}"


E14 = Campaign("M2-E14", date(2025, 12, 25), CANDIDATES, (MANIFEST_PATH,))
E18 = Campaign(
    "M2-E18",
    date(2025, 12, 1),
    ("VOL_CONFIRM_E18_V1", "RIDGE_INCREMENT_E18_V1"),
    (D01_PATH, E17_PATH),
)
CAMPAIGNS = {campaign.name: campaign for campaign in (E14, E18)}
DAYS = E14.days
STAGES = {"timing": 5, "prepare": 20, CANDIDATES[0]: 25, CANDIDATES[1]: 30}
FIT_LIMITS = {"timing": 1, "prepare": 0, CANDIDATES[0]: 2, CANDIDATES[1]: 4}
POLICY_METRICS = [
    "eligible_count",
    "actions_and_skips",
    "gross_and_net_bps",
    "turnover",
    "trade_count",
]
VOLUME_TABLES = {
    "paired_events": [
        "pair_count",
        "empty_bands",
        "high_events_without_eligible_partner",
        "events_unselected_under_pair_cap",
        "event_and_control_gross_and_net_bps",
        "paired_net_difference_bps",
    ],
    "volume_filter_and_positive_move_baseline": [
        *POLICY_METRICS,
        "net_difference_bps_per_eligible_opportunity",
    ],
}
DIAGNOSTIC_COUNTS = {CANDIDATES[0]: 54, CANDIDATES[1]: 61}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def archive_rows(manifest: dict):
    rows = []
    for day in DAYS:
        folder = "m2-e12" if day.startswith("2025") else "m2-e03"
        name = f"{folder}/{SYMBOL}-1m-{day}.zip"
        digest = manifest["files"][f"artifacts/{name}"]["sha256"]
        if not re.fullmatch("[0-9a-f]{64}", digest):
            raise ValueError("Invalid pinned archive digest.")
        rows.append({"day": day, "name": name, "sha256": digest})
    return rows


def d01_archive_rows(receipt: dict):
    (manifest,) = [
        worker["result"]["manifest"]
        for worker in receipt["acquisition"]["workers"]
        if worker["result"]["manifest"]["symbol"] == SYMBOL
    ]
    if manifest["qualified"] is not True or manifest["bar_minutes"] != 1:
        raise ValueError("The D01 BTCUSDT manifest is not qualified.")
    rows = []
    for day in E18.days:
        (item,) = [record for record in manifest["archives"] if record["day"] == day]
        if item["name"] != f"{SYMBOL}-1m-{day}.zip" or item["symbol"] != SYMBOL:
            raise ValueError(
                "The D01 archive identity differs from the registered scope."
            )
        row = {key: item[key] for key in ("name", "day", "sha256", "checksum_sha256")}
        if not all(
            re.fullmatch("[0-9a-f]{64}", row[key])
            for key in ("sha256", "checksum_sha256")
        ):
            raise ValueError("Invalid qualified D01 archive or checksum digest.")
        rows.append(row)
    return rows


def e17_training_id(receipt: dict, archives: list):
    definition = receipt["registered_definition"]["definition"]
    outcome = receipt["execution_receipt"]["outcome"]
    result = outcome["result"]
    if (
        receipt["work_item"] != "M2-E17"
        or outcome["execution_status"] != "COMPLETED"
        or definition["prospective_window"] != list(E18.days)
        or definition["input_archives"] != archives[:4]
        or result["qualified_training_days"] != list(E18.days[:4])
        or result["input_rows"] != 5760
        or result["threshold_bps"] != 27
        or result["clears_hurdle"] is not True
        or not re.fullmatch("[0-9a-f]{64}", result["training_dataset_id"])
    ):
        raise ValueError(
            "The M2-E17 training receipt differs from the registered prefix."
        )
    return result["training_dataset_id"]


def verify_training_prefix(bars: Bars, expected: str):
    training = Bars(bars.values[:5760], bars.symbol, bars.bar_minutes)
    if training.fingerprint != expected:
        raise ValueError("The qualified training fingerprint differs from M2-E17.")
    return expected


def frozen_definition(root: Path, campaign=E14):
    registrations = read_json(root / EXPOSURE_PATH)["future_registrations"]
    entries = [
        record for record in registrations if record["variant_id"] in campaign.variants
    ]
    intervals = {
        f"fold_{i}": [v.start, v.stop] for i, (_, v) in enumerate(folds_for_window(), 1)
    }
    if len(entries) != 2 or {r["variant_id"] for r in entries} != set(
        campaign.variants
    ):
        raise ValueError(f"Missing or duplicate {campaign.name} registrations.")
    for record in entries:
        plan = record.get("diagnostic_plan", {})
        if (
            record.get("status") != "PLANNED_NOT_RUN"
            or record.get("work_item") != campaign.name
            or record.get("data_scope") != list(campaign.days)
            or plan.get("validation_intervals") != intervals
            or plan.get("horizon_bars") != HORIZON
            or plan.get("status") != "PLANNED_NOT_RUN"
        ):
            raise ValueError(
                f"{campaign.name} scope or diagnostic registration differs."
            )
        if record["variant_id"] == campaign.variants[0]:
            if (
                plan.get("views") != list(GROUP_VIEWS)
                or plan.get("tables") != VOLUME_TABLES
            ):
                raise ValueError("Missing or changed volume diagnostic registration.")
        else:
            forecast = plan.get("forecast", {})
            if (
                forecast.get("roles") != list(FORECAST_ROLES)
                or forecast.get("diagnostic_ids") != list(DIAGNOSTIC_IDS.values())
                or forecast.get("views") != list(GROUP_VIEWS[:3])
                or forecast.get("count") != 30
                or forecast.get("comparison_metrics")
                != [
                    "mae",
                    "zero_mae",
                    "relative_mae_reduction_vs_controls",
                ]
                or forecast.get("training_screen")
                != {
                    "metric": "training_abs_move_p90",
                    "view": "fold_1_training",
                    "interval": [12, 5729],
                }
                or plan.get("policy", {}).get("views") != list(GROUP_VIEWS)
                or plan.get("policy", {}).get("roles")
                != [*FORECAST_ROLES, "momentum", "flat"]
                or plan.get("policy", {}).get("metrics")
                != [
                    *POLICY_METRICS,
                    "net_difference_bps_per_eligible_opportunity_vs_one_feature_ridge",
                ]
            ):
                raise ValueError("Missing or changed Ridge diagnostic registration.")
    card = (root / STATUS_PATH).read_text(encoding="utf-8")
    if f"### {campaign.name} guarded campaign entry Test Card" not in card:
        raise ValueError(f"The {campaign.name} implementation Test Card is missing.")
    if campaign == E18:
        archives = d01_archive_rows(read_json(root / D01_PATH))
        prefix = e17_training_id(read_json(root / E17_PATH), archives)
    else:
        archives = archive_rows(read_json(root / MANIFEST_PATH))
        prefix = None
    identity = [entries, archives, COSTS, intervals]
    if prefix:
        identity.append(prefix)
    definition_id = fingerprint(identity)
    return definition_id, archives


def git_bytes(root: Path, *arguments: str):
    return subprocess.run(
        ["git", *arguments], cwd=root, check=True, capture_output=True, timeout=20
    ).stdout


def verify_publication(root: Path, revision: str, campaign=E14):
    if not re.fullmatch("[0-9a-f]{40}", revision):
        raise ValueError("An exact publication revision is required.")
    remote = git_bytes(
        root, "ls-remote", "--exit-code", "origin", f"refs/heads/{campaign.branch}"
    )
    if remote.split()[0].decode("ascii") != revision:
        raise ValueError("The publication revision is not the remote branch head.")
    if git_bytes(root, "rev-parse", "HEAD").decode("ascii").strip() != revision:
        raise ValueError("Run from the exact published checkout.")
    source = root / "src/aqrs"
    paths = [
        *campaign.definition_files,
        *(p.relative_to(root).as_posix() for p in sorted(source.glob("*.py"))),
    ]
    hashes = {}
    for path in paths:
        published = git_bytes(root, "show", f"{revision}:{path}").replace(
            b"\r\n", b"\n"
        )
        if (root / path).read_bytes().replace(b"\r\n", b"\n") != published:
            raise ValueError(f"Published definition or source differs: {path}")
        if path.startswith("src/aqrs/"):
            archived_path = "source/aqrs/" + Path(path).name
        else:
            archived_path = "source/" + Path(path).name
        hashes[archived_path] = sha256(published).hexdigest()
    hashes["source/pilot.py"] = hashes["source/aqrs/m2_e14.py"]
    return hashes


def require_admission(path, definition_id, archives, config, root, campaign=E14):
    if path is None:
        raise ValueError("Owner authorization is required before market input access.")
    receipt = read_json(path)
    if not isinstance(receipt, dict):
        raise ValueError(f"Expected a {campaign.name} authorization object.")
    revision = receipt.get("published_revision", "")
    if (
        receipt.get("owner_approved") is not True
        or receipt.get("definition_id") != definition_id
        or receipt.get("archive_scope") != archives
        or receipt.get("governor_id") != fingerprint(config)
        or receipt.get("review") != {"revision": revision, "status": "PASS"}
        or receipt.get("verification")
        != {"revision": revision, "windows": "PASS", "ubuntu": "PASS"}
        or not isinstance(receipt.get("ci_run_url"), str)
        or not receipt["ci_run_url"].startswith("https://github.com/")
    ):
        raise ValueError(
            f"Incomplete or mismatched {campaign.name} authorization or verification record."
        )
    if campaign == E18 and (
        receipt.get("campaign_id") != campaign.name
        or receipt.get("training_dataset_id")
        != e17_training_id(read_json(root / E17_PATH), archives)
    ):
        raise ValueError(
            "Mismatched E18 campaign or training identity in authorization."
        )
    return receipt, verify_publication(root, revision, campaign)


def require_windows_result(path, receipt, campaign=E14):
    if os.geteuid() == 0 or path is None:
        raise ValueError(
            "Ubuntu market replay requires a non-root user and valid Windows receipt."
        )
    payload = path.read_bytes()
    if sha256(payload).hexdigest() != receipt.get("windows_report_sha256"):
        raise ValueError("The Windows result differs from the admitted report digest.")
    report = json.loads(payload)
    source = report.get("provenance", {})
    plan = report.get("plan", {})
    config = report.get("configuration", {})
    if (
        report.get("platform") != "win32"
        or not re.fullmatch("[0-9a-f]{32}", str(report.get("run_id")))
        or not re.fullmatch("[0-9a-f]{64}", str(report.get("dataset_id")))
        or report.get("execution_status") != "COMPLETED"
        or report.get("journal_integrity") != "ok"
        or report.get("dataset_scope") != list(campaign.days)
        or not source.get("files")
        or source.get("source_id") != fingerprint(source["files"])
        or any(
            plan.get(key) != 7
            for key in ("planned_fits", "started_fits", "completed_fits")
        )
        or report.get("admission", {}).get("governor_id") != receipt["governor_id"]
        or config.get("published_revision") != receipt["published_revision"]
        or config.get("definition_id") != receipt["definition_id"]
        or any(
            report.get("trials", {})
            .get(name, {})
            .get("result", {})
            .get("evaluation_status")
            != "COMPLETED"
            for name in campaign.variants
        )
    ):
        raise ValueError(
            "The Windows result does not qualify this Ubuntu market replay."
        )
    if campaign == E18:
        training_id = (
            report.get("stages", {})
            .get("prepare", {})
            .get("result", {})
            .get("training_dataset_id")
        )
        if (
            config.get("campaign_id") != campaign.name
            or config.get("variant") != campaign.name
            or not training_id
            or training_id != receipt.get("training_dataset_id")
        ):
            raise ValueError(
                "The Windows campaign or training identity differs from E18."
            )
    return report


def claim_market_attempt(root, archives, run_id, campaign=E14):
    common_dir = Path(
        git_bytes(root, "rev-parse", "--path-format=absolute", "--git-common-dir")
        .decode("utf-8")
        .strip()
    )
    ledger = common_dir / f"aqrs-{campaign.name.lower()}"
    ledger.mkdir(exist_ok=True)
    marker = ledger / f"{fingerprint(archives)}.{sys.platform}.used"
    with marker.open("x", encoding="utf-8") as stream:
        stream.write(run_id + "\n")


def make_campaign_plan(config: dict):
    limits = config["resource_governor"]
    trial_seconds = min(120, limits["max_wall_seconds_per_trial"])
    campaign_seconds = min(300, limits["max_wall_seconds_per_campaign"])
    rss = min(4096, limits["max_peak_rss_mb_per_trial"])
    if limits["max_model_fits_per_campaign"] < sum(FIT_LIMITS.values()):
        raise ValueError("The planned fit count exceeds the campaign limit.")
    issue = capability(limits["memory_mode"])
    if issue:
        raise ValueError(issue)
    if (
        limits["max_research_trials_per_campaign"] < 2
        or not limits["preflight"]["measure_representative_pilot"]
        or trial_seconds < max(STAGES.values())
        or campaign_seconds < sum(STAGES.values())
        or rss < 512
    ):
        raise ValueError("The frozen M2-E14 resource plan exceeds effective limits.")
    return {
        "planned_trials": 2,
        "planned_fits": sum(FIT_LIMITS.values()),
        "planned_estimator_fits": 5,
        "planned_cutoff_calibrations": 2,
        "planned_seeds": 1,
        "resamples": 0,
        "auto_retry_count": 0,
        "estimated_wall_seconds": sum(STAGES.values()),
        "estimate_method": "Sum of enforced stage bounds, with a supervised representative Ridge timing fit.",
        "max_wall_seconds_per_trial": trial_seconds,
        "max_wall_seconds_per_campaign": campaign_seconds,
        "max_peak_rss_mb": rss,
        "memory_mode": limits["memory_mode"],
        "estimated_peak_rss_mb": 512,
        "started_fits": 0,
        "completed_fits": 0,
    }


def read_window(
    market_root: Path,
    archives: list,
    *,
    scratch: Path | None = None,
    campaign=E14,
):
    # Validate the full scope before calling the importer on the first file.
    try:
        if campaign == E18:
            by_name = {row["name"]: row for row in archives}
            expected = []
            for day in campaign.days:
                name = f"{SYMBOL}-1m-{day}.zip"
                row = by_name[name]
                if not all(
                    re.fullmatch("[0-9a-f]{64}", row[key])
                    for key in ("sha256", "checksum_sha256")
                ):
                    raise ValueError("Invalid D01 archive or checksum digest.")
                expected.append(
                    {
                        "day": day,
                        "name": name,
                        "sha256": row["sha256"],
                        "checksum_sha256": row["checksum_sha256"],
                    }
                )
        else:
            expected = archive_rows(
                {"files": {f"artifacts/{row['name']}": row for row in archives}}
            )
    except (KeyError, TypeError) as error:
        raise ValueError("Archive allowlist is incomplete.") from error
    if archives != expected:
        raise ValueError("Archive allowlist differs from the fixed BTCUSDT scope.")
    if market_root.is_file():
        if market_root.name != "acceptance.zip":
            raise ValueError(
                "Expected the preserved acceptance bundle or archive directory."
            )
        with TemporaryDirectory(prefix="discovery-spot-", dir=scratch) as temporary:
            root = Path(temporary).resolve()
            # Stage only the admitted archives and checksums, under the
            # qualification deadline. Never unpack the whole bundle.
            with ZipFile(market_root) as bundle:
                names = bundle.namelist()
                for row in archives:
                    archive = root / row["name"]
                    archive.parent.mkdir(exist_ok=True)
                    for suffix, limit in (("", 1_000_000), (".CHECKSUM", 4096)):
                        member = f"artifacts/{row['name']}{suffix}"
                        if (
                            names.count(member) != 1
                            or bundle.getinfo(member).file_size > limit
                        ):
                            raise ValueError(
                                "Preserved bundle member is missing, duplicated or too large."
                            )
                        archive.with_name(archive.name + suffix).write_bytes(
                            bundle.read(member)
                        )
            return read_archive_directory(root, archives)
    return read_archive_directory(market_root.resolve(), archives)


def read_archive_directory(root: Path, archives: list):
    paths = []
    for row in archives:
        archive = root / row["name"]
        checksum = archive.with_suffix(".zip.CHECKSUM")
        if any(p.resolve() != p for p in (archive, checksum)):
            raise ValueError(
                "Archive and checksum paths must resolve to their admitted names."
            )
        paths.append((archive, checksum, row))
    daily = []
    for archive, checksum, row in paths:
        spot = load_spot_day(
            archive,
            checksum,
            date.fromisoformat(row["day"]),
            symbol=SYMBOL,
            expected_digest=row["sha256"],
            expected_checksum_digest=row.get("checksum_sha256"),
        )
        if spot.digest != row["sha256"]:
            raise ValueError(
                "Observed Spot digest differs from the historical receipt."
            )
        daily.append(spot.bars.values)
    return Bars(np.concatenate(daily), SYMBOL, 1)


def worker(request: dict, directory: Path):
    stage = request["stage"]
    if stage == "timing":
        return evaluate(request, directory)
    if stage == "prepare":
        training_id = None
        try:
            campaign = CAMPAIGNS[request.get("campaign", E14.name)]
            if campaign == E18 and request["market_root"] is not None:
                source = Path(__file__).resolve().parent
                archives = d01_archive_rows(read_json(source / Path(D01_PATH).name))
                if request["archives"] != archives:
                    raise ValueError(
                        "The request differs from the archived D01 allowlist."
                    )
                training_id = e17_training_id(
                    read_json(source / Path(E17_PATH).name), archives
                )
            bars = (
                read_window(
                    Path(request["market_root"]),
                    request["archives"],
                    scratch=directory,
                    campaign=campaign,
                )
                if request["market_root"] is not None
                else generate(42, ROWS, 1, "SYNTH")
            )
            validate(bars)
            if len(bars.values) != ROWS:
                raise ValueError("Expected the complete ten-day input.")
            if training_id is not None:
                verify_training_prefix(bars, training_id)
        except (ValueError, OSError, KeyError, BadZipFile) as error:
            return {"qualification_error": str(error)}
        np.save(request["bars_path"], bars.values, allow_pickle=False)
        identity = {"dataset_id": bars.fingerprint, "symbol": bars.symbol}
        if training_id is not None:
            identity["training_dataset_id"] = training_id
        return identity
    bars = Bars(np.load(request["bars_path"], allow_pickle=False), request["symbol"], 1)
    if bars.fingerprint != request["dataset_id"]:
        raise ValueError("The staged input changed before evaluation.")
    trial = {CANDIDATES[0]: volume_trial, CANDIDATES[1]: ridge_trial}[stage]
    return trial(bars, request, directory)


def run_campaign(
    output: Path,
    config_path: Path,
    *,
    market_root=None,
    admission=None,
    windows_report=None,
    root=ROOT,
    campaign=E14,
):
    started = monotonic()
    if market_root is not None and admission is None:
        raise ValueError("Owner authorization is required before market input access.")
    config, _ = load(config_path)
    plan = make_campaign_plan(config)
    deadline = started + plan["max_wall_seconds_per_campaign"]
    definition_id, archives = frozen_definition(root, campaign)
    receipt, published_hashes = (
        require_admission(admission, definition_id, archives, config, root, campaign)
        if market_root is not None
        else (None, {})
    )
    revision = receipt["published_revision"] if receipt else None
    windows = (
        require_windows_result(windows_report, receipt, campaign)
        if receipt and sys.platform == "linux"
        else None
    )
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    provenance = snapshot(
        output,
        Path(__file__),
        support=(config_path, *(root / p for p in campaign.definition_files)),
    )
    for path, expected in published_hashes.items():
        normalized = (output / path).read_bytes().replace(b"\r\n", b"\n")
        if sha256(normalized).hexdigest() != expected:
            raise ValueError(
                f"The execution snapshot differs from the published revision: {path}"
            )
    if windows and windows["provenance"]["source_id"] != provenance["source_id"]:
        raise ValueError("The Ubuntu execution source differs from the Windows result.")
    run_id = uuid4().hex
    scope = list(campaign.days) if receipt else ["synthetic"]
    configuration = {
        "campaign_id": campaign.name,
        "variant": campaign.name if receipt else f"{campaign.name}-SYNTHETIC",
        "days": scope,
        "market": {
            "source": "binance_vision_spot" if receipt else "synthetic",
            "symbol": SYMBOL if receipt else "SYNTH",
            "bar_minutes": 1,
        },
        "definition_id": definition_id,
        "costs": COSTS,
        "horizon": HORIZON,
        "seed": 42,
        "research": {"candidates": [{"id": name} for name in campaign.variants]},
        "published_revision": revision,
    }
    report = {
        "run_id": run_id,
        "platform": sys.platform,
        "local_utc_offset_minutes": int(
            datetime.now().astimezone().utcoffset().total_seconds() // 60
        ),
        "dataset_scope": scope,
        "provenance": provenance,
        "configuration": configuration,
        "plan": plan,
        "trials": {},
        "stages": {},
        "admission": receipt,
        "dataset_id": None,
        "execution_status": "RUNNING",
        "holdout": {"day": "2026-01-06", "authorized_reads": 0},
    }
    command = [sys.executable, "-B", "-E", str(output / "source/pilot.py"), "--worker"]
    bars_path = output / "development.npy"

    def stage(name, **values):
        outcome = supervise(
            output,
            values | {"stage": name, "fit_limit": FIT_LIMITS[name]},
            STAGES[name],
            deadline,
            plan["max_peak_rss_mb"],
            command=command,
        )
        plan["started_fits"] += outcome["started_fits"]
        plan["completed_fits"] += outcome["completed_fits"]
        return outcome

    with closing(journal.connect(output / "research.sqlite3")) as db:
        journal.begin(db, run_id, fingerprint(configuration), configuration, report)
        status = "REJECTED_PREFLIGHT"
        try:
            if monotonic() >= deadline:
                raise ValueError("Campaign deadline expired before preflight.")
            if receipt:
                claim_market_attempt(root, archives, run_id, campaign)
            timing = stage("timing", pilot_rows=10_037, pilot_columns=3)
            report["stages"]["timing"] = timing
            if (
                timing["execution_status"] != "COMPLETED"
                or timing["completed_fits"] != 1
            ):
                raise ValueError("Representative timing fit did not complete.")
            factor = max(
                2,
                config["resource_governor"]["preflight"][
                    "runtime_estimate_safety_factor"
                ],
            )
            if (
                4 * factor * timing["result"]["fit_wall_seconds"]
                >= STAGES[CANDIDATES[1]]
                or deadline - monotonic() < sum(STAGES.values()) - STAGES["timing"]
            ):
                raise ValueError(
                    "Effective limits do not allow the remaining frozen stages."
                )
            prepared = stage(
                "prepare",
                bars_path=str(bars_path),
                archives=archives,
                campaign=campaign.name,
                market_root=str(market_root.resolve()) if receipt else None,
            )
            report["stages"]["prepare"] = prepared
            status = prepared["execution_status"]
            if prepared.get("result", {}).get("qualification_error"):
                status = "FAILED"
                report["stop_reason"] = prepared["result"]["qualification_error"]
            if (
                status == "COMPLETED"
                and windows
                and prepared["result"]["dataset_id"] != windows["dataset_id"]
            ):
                raise ValueError(
                    "The Ubuntu qualified dataset differs from the Windows result."
                )
            if status == "COMPLETED":
                report["dataset_id"] = prepared["result"]["dataset_id"]
                for role, name in zip(CANDIDATES, campaign.variants, strict=True):
                    attempt = f"{run_id}:{name}"
                    binding = {
                        "attempt_id": attempt,
                        "prospective_variant_id": name,
                        "dataset_scope": scope,
                        "dataset_id": report["dataset_id"],
                        "published_revision": revision,
                        "source_id": provenance["source_id"],
                        "definition_id": definition_id,
                    }
                    metadata = binding | {
                        "evidence_key": fingerprint(
                            [definition_id, report["dataset_id"], name]
                        )
                    }
                    journal.start_experiment(db, run_id, name, metadata)
                    outcome = stage(
                        role, bars_path=str(bars_path), **prepared["result"]
                    )
                    status = outcome["execution_status"]
                    result = outcome.get("result", {})
                    if (
                        result.get("evaluation_status") == "COMPLETED"
                        and outcome["completed_fits"] != FIT_LIMITS[role]
                    ):
                        status = "FAILED"
                        outcome.update(
                            execution_status=status,
                            stop_reason="Fit ledger differs from plan.",
                        )
                    diagnostics = [
                        view | binding | {"horizon_bars": HORIZON}
                        for view in result.get("diagnostic_exposure", [])
                    ]
                    if result.get("evaluation_status") == "COMPLETED" and (
                        len(diagnostics) != DIAGNOSTIC_COUNTS[role]
                        or len({fingerprint(view) for view in diagnostics})
                        != len(diagnostics)
                    ):
                        status = "FAILED"
                        outcome.update(
                            execution_status=status,
                            stop_reason="Diagnostic ledger differs from plan.",
                        )
                    if result:
                        result["diagnostic_exposure"] = diagnostics
                        result["development_screen"] = (
                            "NOT_ASSESSED"
                            if status != "COMPLETED"
                            else "PROPOSE_FOLLOW_UP"
                            if receipt
                            and result.get("gates")
                            and all(result["gates"].values())
                            else "DEFER"
                            if receipt
                            else "SYNTHETIC_ENGINEERING"
                        )
                        result["effective_independent_units"] = None
                    report["trials"][name] = outcome
                    journal.finish_experiment(
                        db,
                        run_id,
                        {
                            "experiment_id": attempt,
                            "candidate_id": name,
                            "execution_status": status,
                            "evidence_status": "INSUFFICIENT_EVIDENCE"
                            if status == "COMPLETED" and result.get("gates")
                            else "NOT_EVALUATED",
                            "metrics": outcome | {"diagnostic_exposure": diagnostics},
                        },
                        metadata,
                    )
                    if status != "COMPLETED":
                        break
        except Exception as error:
            if status == "COMPLETED":
                status = "FAILED"
            report["stop_reason"] = str(error)
        with db:
            db.execute(
                "UPDATE experiments SET execution_status = 'CANCELLED' "
                "WHERE run_id = ? AND execution_status IN ('PROPOSED', 'RUNNING')",
                (run_id,),
            )
        report["execution_status"] = status
        report["journal_integrity"] = db.execute("PRAGMA integrity_check").fetchone()[0]
        journal.finish_campaign(db, run_id, status, report)
        write_json(output / "report.json", report)
        lines = [
            f"# {campaign.name} discovery comparison",
            "",
            f"Execution: {status}. Dataset scope: {', '.join(scope)}.",
            "Claim scope: descriptive development results with illustrative costs.",
            f"Reserved fit and calibration charges: {plan['started_fits']}/{plan['planned_fits']}.",
        ]
        for name in campaign.variants:
            result = report["trials"].get(name, {}).get("result", {})
            lines.extend(
                ["", f"## {name}", "", result.get("evaluation_status", "NOT_EVALUATED")]
            )
            for gate, passed in result.get("gates", {}).items():
                lines.append(f"- {gate}: {'PASS' if passed else 'MISS'}")
            if "development_screen" in result:
                lines.append(f"Development screen: {result['development_screen']}.")
        if "stop_reason" in report:
            lines.extend(["", f"Stop reason: {report['stop_reason']}"])
        write_text(output / "report.md", "\n".join(lines) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", choices=CAMPAIGNS, default=E14.name)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--synthetic", action="store_true")
    source.add_argument(
        "--market-root",
        type=Path,
        help="Archive directory or preserved acceptance.zip.",
    )
    parser.add_argument("--admission", type=Path)
    parser.add_argument("--windows-report", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/research.yaml")
    args = parser.parse_args()
    try:
        report = run_campaign(
            args.output,
            args.config,
            market_root=args.market_root,
            admission=args.admission,
            windows_report=args.windows_report,
            campaign=CAMPAIGNS[args.campaign],
        )
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        parser.exit(2, f"REJECTED_PREFLIGHT: {error}\n")
    print(f"{report['execution_status']} {report['run_id']} {args.output}")
    return (
        0
        if report["execution_status"] == "COMPLETED"
        and report["journal_integrity"] == "ok"
        else 2
    )


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--worker":
        if (
            Path(journal.__file__).resolve().parent
            != Path(__file__).resolve().parent / "aqrs"
        ):
            raise SystemExit("The worker must import AQRS from the archived source.")
        run_worker(Path(sys.argv[2]), worker)
    else:
        raise SystemExit(main())
