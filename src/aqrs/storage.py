import json
from hashlib import sha256
from pathlib import Path


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False)


def fingerprint(value: object) -> str:
    return sha256(canonical(value).encode("utf-8")).hexdigest()


def write_text(path: Path, text: str) -> None:
    staging = path.with_name(path.name + ".tmp")
    staging.write_text(text, encoding="utf-8")
    staging.replace(path)


def write_json(path: Path, value: object) -> None:
    write_text(
        path, json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False) + "\n"
    )
