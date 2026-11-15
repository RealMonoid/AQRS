import json
import sqlite3
import subprocess
from contextlib import closing
from datetime import UTC, datetime
from os import fsdecode
from pathlib import Path

from aqrs.storage import canonical

SCHEMA = """
CREATE TABLE IF NOT EXISTS campaigns (
    run_id TEXT PRIMARY KEY,
    timestamp_utc TEXT NOT NULL,
    execution_status TEXT NOT NULL,
    config_fingerprint TEXT NOT NULL,
    config_json TEXT NOT NULL,
    manifest_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS experiments (
    experiment_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES campaigns(run_id),
    candidate_id TEXT NOT NULL,
    timestamp_utc TEXT NOT NULL,
    execution_status TEXT NOT NULL,
    evidence_status TEXT NOT NULL,
    evidence_key TEXT,
    duplicate_of TEXT REFERENCES experiments(experiment_id),
    metadata_json TEXT NOT NULL,
    metrics_json TEXT,
    UNIQUE (run_id, candidate_id)
);
CREATE INDEX IF NOT EXISTS experiments_evidence ON experiments(evidence_key);
"""

VARIANT_LEDGER = """
CREATE TABLE IF NOT EXISTS variant_exposures (
    source TEXT NOT NULL,
    symbol TEXT NOT NULL,
    period_start TEXT NOT NULL,
    period_end TEXT NOT NULL,
    variant_key TEXT NOT NULL,
    first_experiment_id TEXT NOT NULL,
    PRIMARY KEY (source, symbol, period_start, period_end, variant_key)
);
"""


def now() -> str:
    return datetime.now(UTC).isoformat()


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path, timeout=3)
    try:
        db.execute("PRAGMA foreign_keys = ON")
        db.executescript(SCHEMA)
    except BaseException:
        db.close()
        raise
    return db


def begin(
    db,
    run_id: str,
    config_hash: str,
    config: dict,
    manifest: dict,
    *,
    rejection: dict | None = None,
) -> None:
    with db:
        db.execute(
            "INSERT INTO campaigns VALUES (?, ?, ?, ?, ?, ?)",
            (
                run_id,
                now(),
                "REJECTED_PREFLIGHT" if rejection else "RUNNING",
                config_hash,
                canonical(config),
                canonical(manifest),
            ),
        )
        db.executemany(
            "INSERT INTO experiments VALUES (?, ?, ?, ?, ?, 'NOT_EVALUATED',"
            " NULL, NULL, ?, NULL)",
            [
                (
                    f"{run_id}:{candidate['id']}",
                    run_id,
                    candidate["id"],
                    now(),
                    "REJECTED_PREFLIGHT" if rejection else "PROPOSED",
                    canonical(candidate | rejection if rejection else candidate),
                )
                for candidate in config["research"]["candidates"]
            ],
        )


def project_ledger_path() -> Path:
    """Return the ledger shared by all AQRS installations for this OS user."""
    return Path.home() / ".aqrs" / "variant-ledger.sqlite3"


def legacy_checkout_artifacts() -> list[Path]:
    """Find legacy locations in the active checkout and its linked worktrees."""
    source_root = Path(__file__).resolve().parents[1]
    root = source_root.parent
    if source_root.name != "src" or not (root / "pyproject.toml").is_file():
        return []
    roots = [root]
    if (root / ".git").exists():
        try:
            output = subprocess.check_output(
                ["git", "worktree", "list", "--porcelain", "-z"],
                cwd=root,
                timeout=3,
                stderr=subprocess.DEVNULL,
            )
        except (OSError, subprocess.SubprocessError):
            pass  # Git is optional for a standalone checkout.
        else:
            roots.extend(
                Path(fsdecode(record.removeprefix(b"worktree ")))
                for record in output.split(b"\0")
                if record.startswith(b"worktree ")
            )
    return list(dict.fromkeys(root / "artifacts" for root in roots))


def has_table(db: sqlite3.Connection, name: str) -> bool:
    return (
        db.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (name,)
        ).fetchone()
        is not None
    )


def legacy_reservations(db: sqlite3.Connection):
    """Import both prior reservation formats without changing their files."""
    if has_table(db, "variant_exposures"):
        for source, symbol, start, end, key, attempt in db.execute(
            "SELECT source, symbol, period_start, period_end, variant_key, "
            "first_experiment_id FROM variant_exposures"
        ):
            yield source, symbol.strip().upper(), start, end, key, attempt
    if not has_table(db, "variant_reservations"):
        return
    for start, end, key, attempt, config in db.execute(
        "SELECT r.period_start, r.period_end, r.variant_key, r.first_experiment_id, "
        "c.config_json FROM variant_reservations r "
        "JOIN experiments e ON e.experiment_id = r.first_experiment_id "
        "JOIN campaigns c ON c.run_id = e.run_id"
    ):
        market = json.loads(config)["market"]
        yield (
            market["source"],
            market["symbol"].strip().upper(),
            start,
            end,
            key,
            attempt,
        )


def reserve_variants(
    db: sqlite3.Connection,
    journal_path: Path,
    run_id: str,
    scope: tuple[str, str],
    period: tuple[str, str],
    variants: dict[str, str],
    limit: int,
) -> dict:
    """Count distinct overlapping variants and reserve the campaign atomically."""
    path = project_ledger_path().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    previous_paths = [path.with_name("research.sqlite3")]
    for directory in legacy_checkout_artifacts():
        previous_paths.extend(
            (directory / "variant-ledger.sqlite3", directory / "research.sqlite3")
        )
    insert = "INSERT OR IGNORE INTO variant_exposures VALUES (?, ?, ?, ?, ?, ?)"
    with closing(sqlite3.connect(path, timeout=3)) as ledger, ledger:
        ledger.execute("BEGIN IMMEDIATE")
        created = not has_table(ledger, "variant_exposures")
        ledger.execute(VARIANT_LEDGER)
        for previous_path in dict.fromkeys(p.resolve() for p in previous_paths):
            if previous_path in (path, journal_path) or not previous_path.is_file():
                continue
            uri = previous_path.as_uri() + "?mode=ro"
            with closing(sqlite3.connect(uri, uri=True, timeout=3)) as previous:
                ledger.executemany(insert, legacy_reservations(previous))
        if path != journal_path:
            ledger.executemany(insert, legacy_reservations(db))
        used = {
            key
            for symbol, key in ledger.execute(
                "SELECT DISTINCT symbol, variant_key FROM variant_exposures "
                "WHERE source = ? AND period_start < ? AND period_end > ?",
                (scope[0], period[1], period[0]),
            )
            if symbol.strip().upper() == scope[1]
        }
        new = set(variants.values()) - used
        requested_new = len(new)
        allowed = not new or len(used) + requested_new <= limit
        if allowed:
            ledger.executemany(
                insert,
                (
                    (*scope, *period, key, f"{run_id}:{candidate_id}")
                    for candidate_id, key in variants.items()
                ),
            )
        return {
            "ledger_path": str(path),
            "ledger_created": created,
            "limit": limit,
            "used_before": len(used),
            "requested_new": requested_new,
            "allowed": allowed,
        }


def finish_experiment(db, run_id: str, trial: dict, metadata: dict) -> None:
    key = metadata.get("evidence_key")
    with db:
        db.execute("BEGIN IMMEDIATE")
        previous_attempt = db.execute(
            "SELECT experiment_id FROM experiments WHERE evidence_key = ? "
            "AND rowid < (SELECT rowid FROM experiments WHERE experiment_id = ?) "
            "ORDER BY rowid DESC LIMIT 1",
            (key, trial["experiment_id"]),
        ).fetchone()
        if previous_attempt:
            metadata["prior_attempt_id"] = previous_attempt[0]
        previous = db.execute(
            "SELECT experiment_id FROM experiments WHERE evidence_key = ? "
            "AND execution_status = 'COMPLETED' AND duplicate_of IS NULL ORDER BY rowid LIMIT 1",
            (key,),
        ).fetchone()
        db.execute(
            "UPDATE experiments SET execution_status = ?, evidence_status = ?, evidence_key = ?, "
            "duplicate_of = ?, metadata_json = ?, metrics_json = ? "
            "WHERE run_id = ? AND candidate_id = ? AND execution_status IN ('PROPOSED', 'RUNNING')",
            (
                trial["execution_status"],
                trial["evidence_status"],
                key,
                previous[0] if previous else None,
                canonical(metadata),
                canonical(trial["metrics"]) if "metrics" in trial else None,
                run_id,
                trial["candidate_id"],
            ),
        )


def start_experiment(db, run_id: str, candidate_id: str, metadata: dict) -> None:
    with db:
        db.execute(
            "UPDATE experiments SET execution_status = 'RUNNING', metadata_json = ?, evidence_key = ? "
            "WHERE run_id = ? AND candidate_id = ? AND execution_status = 'PROPOSED'",
            (canonical(metadata), metadata["evidence_key"], run_id, candidate_id),
        )


def finish_campaign(db, run_id: str, status: str, manifest: dict) -> None:
    with db:
        db.execute(
            "UPDATE campaigns SET execution_status = ?, manifest_json = ? WHERE run_id = ?",
            (status, canonical(manifest), run_id),
        )
