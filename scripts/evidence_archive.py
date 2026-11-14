"""Preserve local acceptance records and reconstruct an explicitly bounded exposure index."""

import argparse
import hashlib
import json
import os
import sqlite3
import subprocess
from collections import Counter
from contextlib import closing
from copy import deepcopy
from datetime import UTC, datetime
from io import BytesIO
from math import isclose
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
SUPERVISED_REFERENCE_RUN = "9de172568b9842f0840345abd548fe53"
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


def supervised_source(revision):
    """Read the selected Git objects without fetching missing source."""

    def git(*args):
        return subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            env=os.environ | {"GIT_NO_LAZY_FETCH": "1", "GIT_ALLOW_PROTOCOL": ""},
            timeout=10,
        )

    commit = git("rev-parse", "--verify", "--end-of-options", revision + "^{commit}")
    commit = commit.decode("ascii").strip()
    paths = {
        "source/pilot.py": "scripts/m2_supervised_pilot.py",
        "source/research.yaml": "configs/research.yaml",
        "source/m1-e04.yaml": "configs/m1-e04.yaml",
    }
    package = git("ls-tree", "-z", "--name-only", commit, "src/aqrs/")
    paths.update(
        (f"source/aqrs/{PurePosixPath(path).name}", path)
        for path in package.decode("utf-8").split("\0")
        if path.endswith(".py")
    )
    return commit, {
        name: digest(git("show", f"{commit}:{path}")) for name, path in paths.items()
    }


def supervised_receipt(output, platform, expected_source, expected_config):
    from aqrs.storage import fingerprint

    report = json.loads((output / "report.json").read_text(encoding="utf-8"))
    configuration = report["configuration"]
    models = {"ridge", "lightgbm"}
    if (
        report["schema_version"] != "2"
        or not report["platform"].startswith(platform + "-")
        or report["execution_status"] != "COMPLETED"
        or report["evaluation_status"] != "COMPLETED"
        or report["journal_integrity"] != "ok"
        or report["config_id"] != fingerprint(configuration)
        or configuration != expected_config
        or report["holdout"]["start_at"] != "2026-01-06T00:00:00Z"
        or report["holdout"]["authorized_reads"] != 0
        or report["holdout"]["evaluated"] is not False
        or report["plan"]["preflight_status"] != "ADMITTED"
        or report["plan"]["planned_fits"] != 6
        or [fold["validation_rows"] for fold in report["folds"]] != [1409, 1409]
        or [fold["validation_day"] for fold in report["folds"]]
        != ["2026-01-03", "2026-01-04"]
        or set(report["per_day"]) != models
        or any(len(days) != 2 for days in report["per_day"].values())
        or len(report["paired_deltas"]) != 2
    ):
        raise ValueError(f"Incomplete supervised receipt for {platform}.")
    for field, fits in (("preflight", 1), ("trials", 2)):
        outcomes = report[field]
        seconds = 30 if field == "preflight" else 120
        if outcomes.keys() != models or any(
            row["execution_status"] != "COMPLETED"
            or not row["started"]
            or row["started_fits"] != fits
            or row["completed_fits"] != fits
            or not 0 < row["peak_rss_mb"] <= 4096
            or not 0 < row["runtime_wall_seconds"] <= seconds
            for row in outcomes.values()
        ):
            raise ValueError(f"Incomplete supervised receipt for {platform}: {field}.")

    provenance = report["provenance"]
    if provenance["files"] != expected_source or provenance["source_id"] != fingerprint(
        expected_source
    ):
        raise ValueError(f"Supervised source digest mismatch for {platform}.")
    for name, expected in expected_source.items():
        if digest((output / name).read_bytes()) != expected:
            raise ValueError(f"Archived source digest mismatch for {platform}: {name}.")

    uri = (output / "research.sqlite3").resolve().as_uri() + "?mode=ro"
    with closing(sqlite3.connect(uri, uri=True)) as db:
        campaign = db.execute(
            "SELECT run_id, execution_status, config_fingerprint, config_json, manifest_json FROM campaigns"
        ).fetchall()
        rows = db.execute(
            "SELECT candidate_id, execution_status, evidence_status, evidence_key, metadata_json, metrics_json "
            "FROM experiments WHERE run_id = ?",
            (report["run_id"],),
        ).fetchall()
        if (
            db.execute("PRAGMA integrity_check").fetchone() != ("ok",)
            or len(campaign) != 1
            or campaign[0][:3] != (report["run_id"], "COMPLETED", report["config_id"])
            or json.loads(campaign[0][3]) != configuration
            or json.loads(campaign[0][4]) != report
            or {row[0] for row in rows} != models
            or any(
                (status, evidence) != ("COMPLETED", "INSUFFICIENT_EVIDENCE")
                or key != fingerprint([configuration, report["dataset_id"], name])
                or json.loads(metadata)["source_id"] != provenance["source_id"]
                or json.loads(metrics) != report["trials"][name]
                for name, status, evidence, key, metadata, metrics in rows
            )
        ):
            raise ValueError(f"Journal and supervised receipt disagree for {platform}.")
    return report


def require_replay_agreement(left, right, path):
    if type(left) is type(right):
        if isinstance(left, dict) and left.keys() == right.keys():
            for key in left:
                require_replay_agreement(left[key], right[key], f"{path}.{key}")
            return
        if isinstance(left, list) and len(left) == len(right):
            for index, (a, b) in enumerate(zip(left, right, strict=True)):
                require_replay_agreement(a, b, f"{path}[{index}]")
            return
        if isinstance(left, float):
            if isclose(left, right, rel_tol=0, abs_tol=1e-8):
                return
        elif left == right:
            return
    raise ValueError(f"Replay mismatch at {path}.")


def verify_supervised_replay(windows, ubuntu, revision):
    commit, source = supervised_source(revision)
    configurations = json.loads(
        (ROOT / "evidence/configurations.json").read_text(encoding="utf-8")
    )
    expected_config = configurations[SUPERVISED_REFERENCE_RUN]
    first = supervised_receipt(windows, "Windows", source, expected_config)
    first_data = supervised_dataset(windows, first["dataset_id"])
    if ubuntu is None:
        print(
            f"Verified source-bound supervised Windows receipt at {commit} for {first['run_id']}."
        )
        return
    second = supervised_receipt(ubuntu, "Linux", source, expected_config)
    if first["run_id"] == second["run_id"]:
        raise ValueError("Replay requires two distinct run IDs.")
    if first_data != supervised_dataset(ubuntu, second["dataset_id"]):
        raise ValueError("Replay dataset bytes differ.")
    for key in ("config_id", "dataset_id", "folds", "decision"):
        if first[key] != second[key]:
            raise ValueError(f"Replay mismatch at {key}.")
    for key in ("per_day", "paired_deltas"):
        require_replay_agreement(first[key], second[key], key)
    for model in first["trials"]:
        left, right = (
            {
                key: value
                for key, value in report["trials"][model]["result"].items()
                if key != "stage_wall_seconds"
            }
            for report in (first, second)
        )
        require_replay_agreement(left, right, model)
    print(
        f"Verified source-bound supervised replay at {commit} "
        f"for {first['run_id']} and {second['run_id']} (absolute tolerance 1e-8)."
    )


def supervised_dataset(output, dataset_id):
    from io import BytesIO

    import numpy as np

    from aqrs.market import Bars, validate

    with (output / "development.npy").open("rb") as stream:
        payload = stream.read(512 * 1024 + 1)
    if len(payload) > 512 * 1024:
        raise ValueError("Supervised dataset snapshot exceeds its size limit.")
    values = np.load(BytesIO(payload), allow_pickle=False)
    if not isinstance(values, np.ndarray) or values.shape != (5760, 6):
        raise ValueError("Invalid supervised dataset snapshot shape.")
    bars = Bars(values, "BTCUSDT", 1)
    validate(bars)
    if bars.time(0) != "2026-01-01T00:00:00+00:00" or bars.fingerprint != dataset_id:
        raise ValueError(
            "Supervised dataset snapshot does not match its recorded identity."
        )
    return digest(payload)


def diagnostic_views(metrics):
    """Preserve absent versus empty; mirrored lists count once, conflicts fail."""
    if metrics is None:
        return None
    if not isinstance(metrics, dict):
        raise ValueError("Unsupported metrics format.")
    containers = [metrics]
    if isinstance(metrics.get("result"), dict):
        containers.append(metrics["result"])
    lists = [c["diagnostic_exposure"] for c in containers if "diagnostic_exposure" in c]
    if not lists:
        return None
    if any(
        not isinstance(v, list) or any(not isinstance(e, dict) for e in v)
        for v in lists
    ):
        raise ValueError("Unsupported diagnostic exposure format.")
    if any(v != lists[0] for v in lists[1:]):
        raise ValueError("Conflicting flat and nested diagnostic exposure.")
    return lists[0]


def merge_variants(target, additions):
    for key, value in additions.items():
        if key in target:
            if target[key]["definition"] != value["definition"]:
                raise ValueError(f"Conflicting variant definition: {key}")
            target[key]["attempt_ids"].extend(value["attempt_ids"])
        else:
            target[key] = value


def journal_projection(data, name):
    """Read a committed SQLite snapshot without executing research code."""
    attempts, variants, configurations = [], {}, {}
    with closing(sqlite3.connect(":memory:")) as db:
        db.deserialize(data)
        db.execute("PRAGMA query_only=ON")
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError(f"Journal integrity failure: {name}")
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
            variant_id = metadata.get("prospective_variant_id") or (
                "historical-"
                + digest(json.dumps(signature, sort_keys=True).encode())[:16]
            )
            definition = variants.setdefault(
                variant_id,
                {
                    "variant_id": variant_id,
                    "definition": signature,
                    "registration": "prospective_market_definition"
                    if metadata.get("prospective_variant_id")
                    else "retrospective_reconstruction",
                    "attempt_ids": [],
                },
            )
            if definition["definition"] != signature:
                raise ValueError(
                    f"Conflicting journal definitions for variant: {variant_id}"
                )
            definition["attempt_ids"].append(eid)
            market = config.get("market", {})
            inputs = report.get("input_archives", config.get("input_archives", []))
            scope = (
                config.get("days")
                or metadata.get("dataset_scope")
                or report.get("dataset_scope")
                or [item["day"] for item in inputs if "day" in item]
            ) or ([market["day"]] if "day" in market else ["synthetic"])
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
                    "journal": name,
                    "independent_confirmation": False,
                    "kind": "synthetic_engineering"
                    if scope == ["synthetic"]
                    else "development_attempt_or_platform_replay",
                }
            )
            attempts[-1].update(
                {
                    "source_id": metadata.get(
                        "source_id", report.get("provenance", {}).get("source_id")
                    ),
                    "registered_variant_id": metadata.get(
                        "prospective_variant_id", config.get("variant")
                    ),
                    "definition_id": metadata.get(
                        "definition_id", config.get("definition_id")
                    ),
                    "published_revision": metadata.get(
                        "published_revision", config.get("published_revision")
                    ),
                }
            )
            if attempts[-1]["dataset_id"] is None:
                attempts[-1]["dataset_id"] = metadata.get(
                    "dataset_id",
                    report.get("worker", {}).get("result", {}).get("dataset_id"),
                )
            # Replays keep their own diagnostic looks, even for the same model.
            diagnostics = diagnostic_views(json.loads(metrics) if metrics else None)
            if diagnostics is not None:
                attempts[-1]["diagnostic_exposure"] = diagnostics
    return attempts, variants, configurations


def unique_rows(rows, key):
    result = {row[key]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f"Duplicate {key} identities require review.")
    return result


def archive_projection(root, index):
    """Derive attempts from bound journals only; never open market payload members."""
    sources = index.get("archive_sources", [])
    if not sources:
        raise ValueError("No bound archive sources; exposure coverage is unverified.")
    unique_rows(sources, "work_item")
    unique_rows(sources, "bundle")
    known_variants = unique_rows(index["variants"], "variant_id")
    attempts, variants, signatures = [], {}, {}
    decoded_bytes = 0
    for source in sources:
        relative = PurePosixPath(source["bundle"])
        if (
            relative.is_absolute()
            or ".." in relative.parts
            or "\\" in source["bundle"]
            or ":" in source["bundle"]
        ):
            raise ValueError("Archive path must be repository-relative.")
        path = root / relative
        if (
            not path.resolve().is_relative_to(root.resolve())
            or path.stat().st_size > 150_000_000
        ):
            raise ValueError("Archive exceeds the bounded repository scope.")
        payload = path.read_bytes()
        if digest(payload) != source["sha256"]:
            raise ValueError(f"Exposure source digest mismatch: {source['bundle']}")
        if source.get("receipt", "").endswith(".json"):
            receipt_path = (root / source["receipt"]).resolve()
            if not receipt_path.is_relative_to(root.resolve()):
                raise ValueError("Receipt path must stay in the repository.")
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            bound_digest = receipt.get(
                "bundle_sha256", receipt.get("evidence_bundle", {}).get("sha256")
            )
            if bound_digest != source["sha256"]:
                raise ValueError("Exposure source and published receipt disagree.")
        with ZipFile(BytesIO(payload)) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)):
                raise ValueError("Duplicate archive member identities require review.")
            journals = sorted(n for n in names if n.endswith(".sqlite3"))
            if not journals:
                raise ValueError("Exposure archive contains no journals.")
            for name in journals:
                size = archive.getinfo(name).file_size
                decoded_bytes += size
                if size >= 20_000_000 or decoded_bytes > 150_000_000:
                    raise ValueError("Exposure metadata exceeds its storage budget.")
                rows, definitions, _ = journal_projection(archive.read(name), name)
                for row in rows:
                    original = row["variant_id"]
                    variant_id = source.get("variant_ids", {}).get(
                        row["candidate_id"], original
                    )
                    signature = definitions[original]["definition"]
                    if variant_id in signatures and signatures[variant_id] != signature:
                        raise ValueError(
                            f"Conflicting archived definitions for variant: {variant_id}"
                        )
                    signatures[variant_id] = signature
                    row.update(
                        variant_id=variant_id, archive_source=source["work_item"]
                    )
                    row["kind"] = source.get("attempt_kinds", {}).get(
                        row["candidate_id"], row["kind"]
                    )
                    definition = deepcopy(
                        known_variants.get(variant_id, definitions[original])
                    )
                    historical_digest = source.get(
                        "historical_definition_digests", {}
                    ).get(variant_id)
                    if historical_digest:
                        # This protects a restored declaration, not its historical truth.
                        if (
                            digest(
                                json.dumps(
                                    definition["definition"], sort_keys=True
                                ).encode()
                            )
                            != historical_digest
                        ):
                            raise ValueError(
                                f"Historical definition digest mismatch: {variant_id}"
                            )
                        definition["journal_configuration_signature"] = signature
                    elif definition["definition"] != signature:
                        raise ValueError(
                            f"Index definition differs from archived configuration: {variant_id}"
                        )
                    definition.update(variant_id=variant_id, attempt_ids=[])
                    variants.setdefault(variant_id, definition)["attempt_ids"].append(
                        row["experiment_id"]
                    )
                    attempts.append(row)
    unique_rows(attempts, "experiment_id")
    for variant in variants.values():
        variant["attempt_ids"].sort()
    return sorted(attempts, key=lambda r: r["experiment_id"]), sorted(
        variants.values(), key=lambda r: r["variant_id"]
    )


def registration_attempts(registration, attempts):
    if registration.get("kind") == "diagnostic_definition":
        return [
            a
            for a in attempts
            if any(
                d.get("diagnostic_id") == registration["variant_id"]
                for d in a.get("diagnostic_exposure", [])
            )
        ]
    return [
        a
        for a in attempts
        if a["archive_source"] == registration["work_item"]
        and registration["variant_id"]
        in (a["variant_id"], a["registered_variant_id"], a["candidate_id"])
    ]


def reconcile_registrations(index):
    for entry in index["future_registrations"]:
        rows = registration_attempts(entry, index["attempts"])
        if not rows:
            continue
        entry.setdefault("status_before_reconciliation", entry["status"])
        entry["attempt_ids"] = [a["experiment_id"] for a in rows]
        entry["status"] = (
            "USED_IN_RECORDED_ATTEMPTS"
            if entry.get("kind") == "diagnostic_definition"
            else "COMPLETED"
            if all(a["execution_status"] == "COMPLETED" for a in rows)
            else "ATTEMPTED"
        )
        if "completed_diagnostic_views" in entry:
            entry["completed_diagnostic_views"] = sum(
                len(a.get("diagnostic_exposure", [])) for a in rows
            )
        if "diagnostic_plan" in entry and "status" in entry["diagnostic_plan"]:
            plan = entry["diagnostic_plan"]
            plan.setdefault("status_before_reconciliation", plan["status"])
            plan["status"] = "RECORDED_SEE_ATTEMPTS"
        if "research_admission" in entry:
            entry.setdefault(
                "admission_at_registration", entry.pop("research_admission")
            )


def verify_exposure(root, index=None):
    """Compare the entire projection with its sources and cross-record references."""
    if index is None:
        index = json.loads(
            (root / "evidence/exposure.json").read_text(encoding="utf-8")
        )
    attempts, variants = archive_projection(root, index)
    actual = unique_rows(index["attempts"], "experiment_id")
    expected = unique_rows(attempts, "experiment_id")
    if actual.keys() != expected.keys():
        raise ValueError("Exposure attempt inventory differs from archived journals.")
    for eid, row in expected.items():
        if actual[eid] != row:
            raise ValueError(f"Exposure attempt/diagnostic mismatch: {eid}")
    if sorted(index["variants"], key=lambda r: r["variant_id"]) != variants:
        raise ValueError("Variant attempt links differ from archived journals.")
    if index["evidence_counts"] != dict(
        Counter(a["evidence_status"] for a in attempts)
    ):
        raise ValueError("Exposure evidence counts disagree.")
    reconciled = deepcopy(index)
    for entry in index["future_registrations"]:
        matches = {a["experiment_id"] for a in registration_attempts(entry, attempts)}
        linked = entry.get("attempt_ids", [])
        if len(linked) != len(set(linked)) or not set(linked) <= matches:
            raise ValueError(
                "Registration refers to a missing or incompatible attempt."
            )
        if (
            entry["status"] in {"COMPLETED", "ATTEMPTED", "USED_IN_RECORDED_ATTEMPTS"}
            and not matches
        ):
            raise ValueError("Executed registration has no matching archived attempt.")
    reconcile_registrations(reconciled)
    if reconciled["future_registrations"] != index["future_registrations"]:
        raise ValueError("Executed registration status or diagnostic count is stale.")
    for screen in index["manual_screens"]:
        ids = screen.get("attempt_ids", [])
        if screen.get("source_attempt_id"):
            ids = [*ids, screen["source_attempt_id"]]
        if any(eid not in actual for eid in ids):
            raise ValueError("Manual screen refers to a missing attempt.")
        if any(
            actual[eid]["variant_id"] != screen["variant_id"]
            for eid in screen.get("attempt_ids", [])
        ):
            raise ValueError("Manual screen refers to a different variant.")
    for entry in index["future_registrations"]:
        observed = entry.get("observed_attempt", {})
        if "receipt_sha256" in observed:
            receipt_path = (root / observed["receipt"]).resolve()
            if (
                not receipt_path.is_relative_to(root.resolve())
                or digest(receipt_path.read_bytes()) != observed["receipt_sha256"]
            ):
                raise ValueError(
                    "Training observation receipt differs from its binding."
                )
    variant_ids = {v["variant_id"] for v in variants}
    for variant in variants:
        if any(
            parent not in variant_ids
            for parent in variant.get("lineage", {}).get("parent_variant_ids", [])
        ):
            raise ValueError("Lineage refers to a missing parent variant.")
    if not index.get("unknown_exposure"):
        raise ValueError("Historical exposure uncertainty must remain explicit.")
    return {
        "attempts": len(attempts),
        "variants": len(variants),
        "recorded_diagnostic_views": sum(
            len(a.get("diagnostic_exposure", [])) for a in attempts
        ),
        "attempts_without_diagnostic_records": sum(
            "diagnostic_exposure" not in a for a in attempts
        ),
    }


def consolidate_exposure(root):
    """Replace only the projection after complete validation; preserve all sources."""
    path = root / "evidence/exposure.json"
    previous = json.loads(path.read_text(encoding="utf-8"))
    result = deepcopy(previous)
    result["attempts"], result["variants"] = archive_projection(root, previous)
    if not set(unique_rows(previous["attempts"], "experiment_id")) <= {
        a["experiment_id"] for a in result["attempts"]
    }:
        raise ValueError(
            "Consolidation would lose existing attempts; restore their sources first."
        )
    result["evidence_counts"] = dict(
        Counter(a["evidence_status"] for a in result["attempts"])
    )
    reconcile_registrations(result)
    summary = verify_exposure(root, result)
    with TemporaryDirectory(prefix="exposure-", dir=path.parent) as temporary:
        staged = Path(temporary) / "exposure.json"
        write(staged, result)
        staged.replace(path)
    return summary


def build(root):
    target = root / "evidence"
    target.mkdir(exist_ok=True)
    index_path = target / "exposure.json"
    if index_path.exists() and json.loads(index_path.read_text(encoding="utf-8")).get(
        "archive_sources"
    ):
        raise ValueError(
            "Frozen archive sources exist. Use --consolidate-exposure; --build must not replace them."
        )
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
    for name, data in journal_snapshots.items():
        rows, definitions, configs = journal_projection(data, name)
        attempts.extend(rows)
        merge_variants(variants, definitions)
        configurations.update(configs)
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
            "scope": "Reconstruction from the 26 archived journals plus documented manual screens; not a proof that every historical manual selection is known.",
            "unknown_exposure": "Unrecorded manual inspection cannot be reconstructed. Existing development windows are exposed; no effective independent sample size or adjusted significance is claimed.",
            "variants": list(variants.values()),
            "attempts": attempts,
            "manual_screens": previous.get("manual_screens", manual),
            "engineering_checks": ["M1-E05", "M2-E01", "M2-E04", "M2-E05", "M2-E06"],
            "evidence_counts": dict(Counter(a["evidence_status"] for a in attempts)),
        },
    )
    write(target / "configurations.json", configurations)
    return verify(bundle, target / "manifest.json")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--consolidate-exposure",
        action="store_true",
        help="Rebuild only the index from its bound archived journals, without research execution.",
    )
    parser.add_argument(
        "--verify-exposure",
        action="store_true",
        help="Read-only check of all bound attempts, diagnostic views and registration links.",
    )
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
        "--verify-supervised-replay",
        nargs="+",
        type=Path,
        metavar="RECEIPT_DIR",
        help="Verify a Windows receipt, or compare it with a second receipt from Ubuntu.",
    )
    parser.add_argument(
        "--source-revision",
        help="Git source revision for supervised replay verification.",
    )
    args = parser.parse_args()
    if args.consolidate_exposure or args.verify_exposure:
        if (
            (args.consolidate_exposure and args.verify_exposure)
            or args.build
            or args.verify
            or args.restore
            or args.verify_supervised_replay
            or args.source_revision
        ):
            parser.error(
                "Exposure maintenance requires exactly one mode and no other actions."
            )
        try:
            result = (
                consolidate_exposure(ROOT)
                if args.consolidate_exposure
                else verify_exposure(ROOT)
            )
        except (ValueError, KeyError, TypeError, OSError, sqlite3.Error) as error:
            parser.error(str(error))
        print(json.dumps(result, sort_keys=True))
        return
    if args.verify_supervised_replay:
        if args.build or args.restore is not None or not args.source_revision:
            parser.error(
                "Supervised replay verification requires --source-revision and is read-only."
            )
        if len(args.verify_supervised_replay) > 2:
            parser.error(
                "Provide a Windows directory and at most one Ubuntu directory."
            )
        windows, ubuntu = (args.verify_supervised_replay + [None])[:2]
        try:
            verify_supervised_replay(windows, ubuntu, args.source_revision)
        except (
            ValueError,
            KeyError,
            TypeError,
            OSError,
            sqlite3.Error,
            subprocess.SubprocessError,
        ) as error:
            parser.error(str(error))
        return
    if args.source_revision:
        parser.error("--source-revision requires --verify-supervised-replay.")
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
