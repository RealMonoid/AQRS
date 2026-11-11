"""Recoverable execution source and environment identity."""

import platform
import subprocess
from hashlib import sha256
from importlib.metadata import distributions
from pathlib import Path

from aqrs.storage import fingerprint


def snapshot(output: Path, entry: Path, support: tuple[Path, ...] = ()) -> dict:
    package = Path(__file__).resolve().parent
    paths = (
        {"source/pilot.py": entry}
        | {f"source/{path.name}": path for path in support}
        | {f"source/aqrs/{path.name}": path for path in sorted(package.glob("*.py"))}
    )
    hashes = {}
    for relative, source in paths.items():
        payload = source.read_bytes()
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        hashes[relative] = sha256(payload).hexdigest()
    git = {"commit": None, "dirty": None}
    try:
        root = package.parent.parent
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=3,
            check=True,
        )
        dirty = subprocess.run(
            ["git", "--no-optional-locks", "status", "--porcelain"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=3,
            check=True,
        )
        git = {"commit": commit.stdout.strip(), "dirty": bool(dirty.stdout.strip())}
    except (OSError, subprocess.SubprocessError):
        pass
    return {
        "source_id": fingerprint(hashes),
        "files": hashes,
        "git": git,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "dependencies": dict(sorted((d.name, d.version) for d in distributions())),
    }
