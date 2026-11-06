import sqlite3
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


def begin(db, run_id: str, config_hash: str, config: dict, manifest: dict) -> None:
    with db:
        db.execute(
            "INSERT INTO campaigns VALUES (?, ?, 'RUNNING', ?, ?, ?)",
            (run_id, now(), config_hash, canonical(config), canonical(manifest)),
        )
        db.executemany(
            "INSERT INTO experiments VALUES (?, ?, ?, ?, 'PROPOSED', 'NOT_EVALUATED',"
            " NULL, NULL, ?, NULL)",
            [
                (
                    f"{run_id}:{candidate['id']}",
                    run_id,
                    candidate["id"],
                    now(),
                    canonical(candidate),
                )
                for candidate in config["research"]["candidates"]
            ],
        )


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
