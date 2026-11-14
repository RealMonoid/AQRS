import json
import sqlite3
from contextlib import closing
from datetime import UTC, datetime
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
    """Anchor the ledger to the installed project, independent of a run config."""
    source_root = Path(__file__).resolve().parents[1]
    if source_root.name == "src" and (source_root.parent / "pyproject.toml").is_file():
        return source_root.parent / "artifacts" / "variant-ledger.sqlite3"
    return Path.home() / ".aqrs" / "variant-ledger.sqlite3"


def legacy_reservations(db: sqlite3.Connection):
    """Recover 302ab6b reservations without changing their source journal."""
    if not db.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'variant_reservations'"
    ).fetchone():
        return
    for start, end, key, attempt, config in db.execute(
        "SELECT r.period_start, r.period_end, r.variant_key, r.first_experiment_id, "
        "c.config_json FROM variant_reservations r "
        "JOIN experiments e ON e.experiment_id = r.first_experiment_id "
        "JOIN campaigns c ON c.run_id = e.run_id"
    ):
        market = json.loads(config)["market"]
        yield market["source"], market["symbol"].upper(), start, end, key, attempt


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
    path = project_ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    default_journal = (path.parent / "research.sqlite3").resolve()
    insert = "INSERT OR IGNORE INTO variant_exposures VALUES (?, ?, ?, ?, ?, ?)"
    with closing(sqlite3.connect(path, timeout=3)) as ledger, ledger:
        ledger.execute("BEGIN IMMEDIATE")
        ledger.execute(VARIANT_LEDGER)
        if default_journal != journal_path and default_journal.exists():
            uri = default_journal.as_uri() + "?mode=ro"
            with closing(sqlite3.connect(uri, uri=True, timeout=3)) as previous:
                ledger.executemany(insert, legacy_reservations(previous))
        ledger.executemany(insert, legacy_reservations(db))
        used = {
            key
            for (key,) in ledger.execute(
                "SELECT DISTINCT variant_key FROM variant_exposures "
                "WHERE source = ? AND symbol = ? AND period_start < ? AND period_end > ?",
                (*scope, period[1], period[0]),
            )
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
