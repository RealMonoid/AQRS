"""Preserve local acceptance records and reconstruct an explicitly bounded exposure index."""

import argparse
import hashlib
import json
import os
import sqlite3
import subprocess
from collections import Counter
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile

ROOT = Path(__file__).resolve().parents[1]
SUFFIXES = {
    ".json",
    ".md",
    ".yaml",
    ".yml",
    ".sqlite3",
    ".py",
    ".log",
    ".txt",
    ".checksum",
}
EXCLUDED = {"aqrs-a06", "m2-e15", "__pycache__", "site-packages", "wheelhouse", ".venv"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def verify(bundle, manifest, restore=None):
    """Check every member before optionally restoring to a new directory."""
    expected = json.loads(manifest.read_text(encoding="utf-8"))
    return verify_members(bundle, expected, restore)


def verify_members(bundle, expected, restore=None):
    if digest(bundle.read_bytes()) != expected["bundle_sha256"]:
        raise ValueError("Evidence bundle digest mismatch.")
    with ZipFile(bundle) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or set(names) != set(expected["files"]):
            raise ValueError("Evidence member inventory mismatch.")
        if len({name.casefold() for name in names}) != len(names):
            raise ValueError("Nonportable case-colliding evidence members.")
        for name in names:
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name:
                raise ValueError("Unsafe evidence member path.")
            reserved = {
                "CON",
                "PRN",
                "AUX",
                "NUL",
                *(f"COM{i}" for i in range(1, 10)),
                *(f"LPT{i}" for i in range(1, 10)),
            }
            if path.as_posix() != name or any(
                part.endswith((".", " ")) or part.split(".")[0].upper() in reserved
                for part in path.parts
            ):
                raise ValueError("Nonportable evidence member path.")
            data = archive.read(name)
            if digest(data) != expected["files"][name]["sha256"]:
                raise ValueError(f"Evidence member digest mismatch: {name}")
            if name.endswith(".sqlite3"):
                with closing(sqlite3.connect(":memory:")) as db:
                    db.deserialize(data)
                    if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                        raise ValueError(f"Evidence journal integrity failure: {name}")
        if restore is not None:
            restore.mkdir(parents=True, exist_ok=False)
            for name in names:
                target = restore / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(name))
    return len(names)


def verify_campaign(root, campaign, replay_revision):
    slug = campaign.lower()
    evidence = root / "evidence"
    manifest = evidence / f"{slug}-verification.json"
    expected = json.loads(manifest.read_text(encoding="utf-8"))
    if expected["work_item"] != campaign:
        raise ValueError("Verification receipt belongs to a different campaign.")

    if campaign == "M2-E14":
        reports = {"windows": expected["windows_report_sha256"]}
    else:
        reports = {
            platform: expected["comparison"]["report_sha256"][platform]
            for platform in ("windows", "ubuntu")
        }
    for platform, sha256 in reports.items():
        member = f"artifacts/{slug}/{platform}/report.json"
        if expected["files"][member]["sha256"] != sha256:
            raise ValueError(f"Verification receipt report digest mismatch: {member}.")
    count = verify_members(evidence / f"{slug}-acceptance.zip", expected)

    if replay_revision is not None:
        path = "evidence/m2-e18-replay/windows.json"
        git = {
            "cwd": root,
            "stderr": subprocess.PIPE,
            "env": {**os.environ, "GIT_NO_LAZY_FETCH": "1"},
        }
        try:
            commit = (
                subprocess.check_output(
                    [
                        "git",
                        "rev-parse",
                        "--verify",
                        "--end-of-options",
                        f"{replay_revision}^{{commit}}",
                    ],
                    **git,
                )
                .decode("ascii")
                .strip()
            )
            report = subprocess.check_output(
                ["git", "cat-file", "blob", f"{commit}:{path}"], **git
            )
        except subprocess.CalledProcessError as error:
            raise ValueError(
                f"Cannot read the local Git replay report at {replay_revision}."
            ) from error
        if digest(report) != reports["windows"]:
            raise ValueError(
                f"Windows replay report digest mismatch at {replay_revision}."
            )
    return count


def build(root):
    target = root / "evidence"
    target.mkdir(exist_ok=True)
    paths = []
    for path in sorted((root / "artifacts").rglob("*")):
        if not path.is_file() or EXCLUDED.intersection(path.relative_to(root).parts):
            continue
        if path.suffix.lower() not in SUFFIXES and not (
            path.suffix == ".zip" and path.name.startswith("BTCUSDT-1m-")
        ):
            continue
        if "2026-01-06" in path.name:
            raise ValueError("Protected date encountered: refusing to open payload.")
        if path.stat().st_size >= 20_000_000:
            raise ValueError(
                f"Evidence member exceeds the 20 MB archive scope: {path.name}"
            )
        paths.append(path)
    if sum(p.stat().st_size for p in paths) > 150_000_000:
        raise ValueError("Evidence selection exceeds the 150 MB uncompressed budget.")
    files = {}
    actual_bytes = 0
    journal_snapshots = {}
    bundle = target / "acceptance.zip"
    with ZipFile(bundle, "w", compression=ZIP_DEFLATED) as archive:
        for path in paths:
            name = path.relative_to(root).as_posix()
            if path.suffix == ".sqlite3":
                with closing(
                    sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
                ) as source:
                    source.execute("PRAGMA query_only=ON")
                    with TemporaryDirectory(prefix="journal-", dir=target) as temporary:
                        with closing(
                            sqlite3.connect(Path(temporary) / "snapshot.sqlite3")
                        ) as copy:
                            source.backup(copy)
                            copy.execute("PRAGMA journal_mode=DELETE")
                            data = copy.serialize()
                            journal_snapshots[name] = data
            else:
                data = path.read_bytes()
            actual_bytes += len(data)
            if len(data) >= 20_000_000 or actual_bytes > 150_000_000:
                raise ValueError(
                    "Serialized evidence exceeds the declared storage budget."
                )
            files[name] = {"sha256": digest(data), "bytes": len(data)}
            archive.writestr(name, data)
    write(
        target / "manifest.json",
        {
            "schema_version": "1",
            "created_at": datetime.now(UTC).isoformat(),
            "scope": "Historical acceptance receipts, journals, source snapshots, scripts, configurations and approved development ZIPs; excludes environments, wheels, vendor sources and reproducible CSV/NPY intermediates.",
            "historical_source_limit": "M2-E08/E09 execution source identity remains unproven. Archiving a later reference script does not repair that gap.",
            "journal_storage": "SQLite read-only backup snapshots include committed WAL state; logical records are preserved, byte identity with original storage files is not claimed.",
            "bundle_sha256": digest(bundle.read_bytes()),
            "files": files,
        },
    )
    attempts, variants, configurations = [], {}, {}
    for path in paths:
        if path.suffix != ".sqlite3":
            continue
        with closing(sqlite3.connect(":memory:")) as db:
            db.deserialize(journal_snapshots[path.relative_to(root).as_posix()])
            db.execute("PRAGMA query_only=ON")
            if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError(f"Journal integrity failure: {path}")
            campaigns = {
                r[0]: (json.loads(r[1]), json.loads(r[2]))
                for r in db.execute(
                    "SELECT run_id,config_json,manifest_json FROM campaigns"
                )
            }
            for run_id, (config, _) in campaigns.items():
                configurations[run_id] = config
            for (
                eid,
                rid,
                cid,
                at,
                execution,
                evidence,
                duplicate,
                metadata,
                metrics,
            ) in db.execute(
                "SELECT experiment_id,run_id,candidate_id,timestamp_utc,execution_status,"
                "evidence_status,duplicate_of,metadata_json,metrics_json FROM experiments"
            ):
                config, report = campaigns[rid]
                metadata = json.loads(metadata)
                candidate = next(
                    (c for c in config["research"]["candidates"] if c["id"] == cid), {}
                )
                signature = {
                    "registered_variant": config.get("variant"),
                    "candidate": candidate,
                    "market_semantics": {
                        k: config.get("market", {}).get(k)
                        for k in ("source", "symbol", "bar_minutes", "scenario")
                    },
                    "research": {
                        k: v
                        for k, v in config.get("research", {}).items()
                        if k != "candidates"
                    },
                    "costs": config.get("costs"),
                    "execution": config.get("execution_simulation"),
                    "features": config.get("features"),
                    "horizon": config.get("horizon"),
                    "seed": config.get("seed", config.get("project", {}).get("seed")),
                    "model_parameters": config.get(
                        "lightgbm_parameters", config.get("isolation_forest")
                    ),
                }
                market = config.get("market", {})
                scope = config.get("days") or (
                    [market["day"]] if "day" in market else ["synthetic"]
                )
                campaign_id = config.get("campaign_id")
                discovery = campaign_id in {"M2-E14", "M2-E18"}
                registered_market = discovery and config.get("variant") == campaign_id
                if discovery:
                    from aqrs.m2_e14 import CAMPAIGNS

                    campaign = CAMPAIGNS[campaign_id]
                    expected_scope = list(campaign.days) if registered_market else ["synthetic"]
                    expected_variant = campaign_id if registered_market else f"{campaign_id}-SYNTHETIC"
                    candidate_ids = [row["id"] for row in config["research"]["candidates"]]
                    if (
                        candidate_ids != list(campaign.variants)
                        or cid not in campaign.variants
                        or scope != expected_scope
                        or config.get("variant") != expected_variant
                    ):
                        raise ValueError("Discovery campaign scope or candidate registration differs.")
                variant_id = cid if registered_market else (
                    "historical-"
                    + digest(json.dumps(signature, sort_keys=True).encode())[:16]
                )
                variants.setdefault(
                    variant_id,
                    {
                        "variant_id": variant_id,
                        "definition": signature,
                        "registration": "prospective_market_definition"
                        if registered_market else "retrospective_reconstruction",
                        "attempt_ids": [],
                    },
                )["attempt_ids"].append(eid)
                attempts.append(
                    {
                        "experiment_id": eid,
                        "variant_id": variant_id,
                        "run_id": rid,
                        "candidate_id": cid,
                        "timestamp_utc": at,
                        "data_scope": scope,
                        "dataset_id": report.get(
                            "dataset_id", report.get("dataset_fingerprint")
                        ),
                        "execution_status": execution,
                        "evidence_status": evidence,
                        "duplicate_of_in_original_journal": duplicate,
                        "journal": path.relative_to(root).as_posix(),
                        "independent_confirmation": False,
                        "kind": "synthetic_engineering"
                        if scope == ["synthetic"]
                        else "development_attempt_or_platform_replay",
                    }
                )
                # Replays keep their own diagnostic looks, even for the same model.
                metrics_record = json.loads(metrics) if metrics else {}
                diagnostics = metrics_record.get("diagnostic_exposure")
                if diagnostics is not None:
                    attempts[-1]["diagnostic_exposure"] = diagnostics
                if discovery:
                    if (
                        execution == "COMPLETED"
                        and metrics_record.get("result", {}).get("evaluation_status") == "COMPLETED"
                        and not diagnostics
                    ):
                        raise ValueError("Completed discovery comparison lacks diagnostic receipts.")
                    binding = {
                        "attempt_id": eid,
                        "prospective_variant_id": cid,
                        "definition_id": config["definition_id"],
                        "published_revision": config["published_revision"],
                        "dataset_scope": scope,
                        "dataset_id": attempts[-1]["dataset_id"],
                        "source_id": report["provenance"]["source_id"],
                    }
                    if any(
                        any(view.get(key) != value for key, value in binding.items())
                        for view in diagnostics or []
                    ):
                        raise ValueError("Discovery diagnostic attempt binding differs from its campaign.")
                    attempts[-1]["source_binding"] = binding
    if len({a["experiment_id"] for a in attempts}) != len(attempts):
        raise ValueError(
            "Duplicate attempt identities across source journals require review."
        )
    manual = [
        {
            "work_item": item,
            "variant_id": "PRICE_DROP_V1",
            "kind": "count_only",
            "data_scope": dates,
            "receipt": receipt,
            "forward_outcomes": False,
            "registration": "historical_timing_unverified",
        }
        for item, dates, receipt in (
            ("M2-E02", ["2026-01-05"], "artifacts/m2-e02"),
            ("M2-E03", ["2026-01-01/2026-01-05"], "artifacts/m2-e03"),
            (
                "M2-E12",
                ["2025-12-25/2025-12-31", "2026-01-01/2026-01-05"],
                "artifacts/m2-e12/coverage.json",
            ),
        )
    ]
    previous = (
        json.loads((target / "exposure.json").read_text())
        if (target / "exposure.json").exists()
        else {}
    )
    write(
        target / "exposure.json",
        {
            "schema_version": "1",
            "future_registrations": previous.get("future_registrations", []),
            "scope": "Reconstruction from the 26 archived journals plus documented count-only screens; not a proof that every historical manual selection is known.",
            "unknown_exposure": "Unrecorded manual inspection cannot be reconstructed. Existing development windows are exposed; no effective independent sample size or adjusted significance is claimed.",
            "variants": list(variants.values()),
            "attempts": attempts,
            "manual_screens": manual,
            "engineering_checks": ["M1-E05", "M2-E01", "M2-E04", "M2-E05", "M2-E06"],
            "evidence_counts": dict(Counter(a["evidence_status"] for a in attempts)),
        },
    )
    write(target / "configurations.json", configurations)
    return verify(bundle, target / "manifest.json")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--build",
        action="store_true",
        help="Replace the historical bundle and index from local records.",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify the versioned bundle without local artifacts.",
    )
    parser.add_argument(
        "--restore", type=Path, help="Restore verified members to a new directory."
    )
    parser.add_argument(
        "--campaign",
        choices=("M2-E14", "M2-E18"),
        help="Verify a campaign archive and its receipt without writing files.",
    )
    parser.add_argument(
        "--replay-revision",
        help="Also verify the E18 Windows replay report bytes at this local Git revision.",
    )
    args = parser.parse_args()
    if args.replay_revision is not None and args.campaign != "M2-E18":
        parser.error("--replay-revision requires --campaign M2-E18.")
    if args.campaign:
        if args.build or args.restore is not None:
            parser.error("--campaign cannot be combined with --build or --restore.")
        try:
            count = verify_campaign(ROOT, args.campaign, args.replay_revision)
        except (BadZipFile, KeyError, OSError, ValueError, sqlite3.Error) as error:
            parser.exit(1, f"{args.campaign} verification failed: {error}\n")
        print(f"Verified {count} preserved evidence files for {args.campaign}.")
        if args.replay_revision is not None:
            print(f"Verified the Windows replay report at {args.replay_revision}.")
        return

    count = (
        build(ROOT)
        if args.build
        else verify(
            ROOT / "evidence/acceptance.zip",
            ROOT / "evidence/manifest.json",
            args.restore,
        )
    )
    print(f"Verified {count} preserved evidence files.")


if __name__ == "__main__":
    main()
