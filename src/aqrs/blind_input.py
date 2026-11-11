"""Strict, local-only input for the AQRS-B01 synthetic diagnostic."""

import csv
import io
import json
import re
import stat
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from math import isclose, isfinite
from pathlib import Path

import numpy as np

from aqrs.storage import write_json

SCHEMA = "aqrs.external-synthetic-minute.v1"
HEADER = ["timestamp_utc", "open", "high", "low", "close", "volume"]
ACTIVITY_COLUMNS = ("buy_volume", "sell_volume", "trade_count")
STAMP = re.compile(r"2000-\d{2}-\d{2}T\d{2}:\d{2}:00Z")
MIB = 1024 * 1024


def unique_object(pairs):
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError("Duplicate JSON keys.")
    return result


def plain_path(path: Path, directory: bool = False) -> None:
    info = path.lstat()
    if path.is_symlink() or getattr(info, "st_file_attributes", 0) & 0x400:
        raise ValueError("Links and reparse points are forbidden.")
    kind = stat.S_ISDIR if directory else stat.S_ISREG
    if not kind(info.st_mode):
        raise ValueError("Expected a plain directory or regular file.")


def safe_under(root: Path, path: Path) -> Path:
    root = root.absolute()
    path = path.absolute()
    try:
        parts = path.relative_to(root).parts
    except ValueError as error:
        raise ValueError("Path is outside the agreed root.") from error
    if ".." in parts:
        raise ValueError("Parent traversal is forbidden.")
    current = root
    plain_path(current, True)
    for part in parts:
        current /= part
        if current.exists() or current.is_symlink():
            plain_path(current, current.is_dir())
    return path


def stamp_seconds(value: str) -> int:
    if not STAMP.fullmatch(value):
        raise ValueError("Timestamp must be an artificial year-2000 UTC minute.")
    return int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp())


def utc_stamp(seconds: float) -> str:
    return datetime.fromtimestamp(seconds, UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_manifest(inbox: Path, source: str) -> dict:
    plain_path(inbox, True)
    # Names are inspected without opening an unexpected file, even the manifest.
    names = {path.name for path in inbox.iterdir()}
    if "manifest.json" not in names or any(
        name != "manifest.json" and not re.fullmatch(r"D\d{3}\.csv", name)
        for name in names
    ):
        raise ValueError("Input allowlist violation; unexpected contents were not opened.")
    for name in names:
        plain_path(inbox / name)
    path = inbox / "manifest.json"
    if path.stat().st_size > 65536:
        raise ValueError("Manifest exceeds 64 KiB.")
    manifest = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    expected = {"schema": SCHEMA, "dataset_type": "synthetic", "source": source,
                "timezone": "UTC", "bar_seconds": 60, "price_reference": "mid"}
    if set(manifest) != set(expected) | {"datasets"}:
        raise ValueError("Unexpected manifest fields.")
    if any(type(manifest[key]) is not type(value) or manifest[key] != value
           for key, value in expected.items()):
        raise ValueError("Manifest provenance or time contract mismatch.")
    datasets = manifest["datasets"]
    if not isinstance(datasets, list) or not 1 <= len(datasets) <= 16:
        raise ValueError("Expected one through 16 datasets.")
    size = 0
    for index, entry in enumerate(datasets, 1):
        if not isinstance(entry, dict) or set(entry) != {
            "id", "file", "sha256", "rows", "start_utc", "end_utc"
        }:
            raise ValueError("Unexpected dataset fields.")
        identifier = f"D{index:03}"
        if entry["id"] != identifier or entry["file"] != f"{identifier}.csv":
            raise ValueError("Dataset IDs and filenames must be consecutive and neutral.")
        if type(entry["rows"]) is not int or not 43200 <= entry["rows"] <= 86400:
            raise ValueError("Dataset must contain 30 through 60 complete days.")
        if entry["rows"] % 1440 or not isinstance(entry["sha256"], str) or not re.fullmatch(
            r"[0-9a-f]{64}", entry["sha256"]
        ):
            raise ValueError("Invalid row count or digest.")
        start, end = (stamp_seconds(entry[key]) for key in ("start_utc", "end_utc"))
        if start % 86400 or end != start + (entry["rows"] - 1) * 60:
            raise ValueError("Invalid complete-day endpoints.")
        path = inbox / entry["file"]
        if path.name not in names:
            raise ValueError("Declared input is missing.")
        file_size = path.stat().st_size
        if file_size > 16 * MIB:
            raise ValueError("CSV exceeds 16 MiB.")
        size += file_size
    if names != {"manifest.json"} | {entry["file"] for entry in datasets}:
        raise ValueError("Input allowlist does not match the manifest.")
    if size > 256 * MIB:
        raise ValueError("Delivery exceeds 256 MiB.")
    return manifest


def validate_activity(columns: list[str], values: list[str], volume: float) -> dict[str, float]:
    activity = {}
    side_volumes = []
    for column, token in zip(columns, values, strict=True):
        if column == "trade_count":
            if not re.fullmatch(r"[0-9]{1,16}", token) or int(token) >= 2**53:
                raise ValueError("Invalid minute trade count.")
            activity[column] = int(token)
            continue
        side = float(token)
        if not isfinite(side) or side < 0 or (side > volume and not isclose(side, volume, rel_tol=1e-9)):
            raise ValueError("Invalid minute side volume.")
        side_volumes.append(side)
        activity[column] = side
    if len(side_volumes) == 2 and not isclose(sum(side_volumes), volume, rel_tol=1e-9):
        raise ValueError("Minute buy and sell volumes must sum to total volume.")
    return activity


def qualify(inbox: Path, dataset_id: str, source: str, expected_digest: str | None = None,
            *, retain_activity: bool = False) -> tuple[dict, np.ndarray]:
    manifest = read_manifest(inbox, source)
    if dataset_id not in {entry["id"] for entry in manifest["datasets"]}:
        raise ValueError("Requested dataset is absent.")
    selected = None
    for entry in manifest["datasets"]:
        if entry["id"] != dataset_id:
            continue
        if expected_digest is not None and entry["sha256"] != expected_digest:
            raise ValueError("Authorized digest does not match the declared dataset.")
        path = inbox / entry["file"]
        plain_path(path)
        payload = path.read_bytes()
        if len(payload) > 16 * MIB or sha256(payload).hexdigest() != entry["sha256"]:
            raise ValueError("CSV size or digest mismatch.")
        reader = csv.reader(io.StringIO(payload.decode("utf-8")), strict=True)
        header = next(reader, [])
        width = len(HEADER)
        activity = header[width:]
        if header[:width] != HEADER or activity != [name for name in ACTIVITY_COLUMNS if name in activity]:
            raise ValueError("CSV header mismatch.")
        rows = []
        for row in reader:
            if len(row) != len(header):
                raise ValueError("CSV field count must match the header.")
            bar = [stamp_seconds(row[0]), *map(float, row[1:width])]
            if activity:
                aggregates = validate_activity(activity, row[width:], bar[-1])
                if retain_activity:
                    bar.extend(aggregates.get(name, np.nan) for name in ACTIVITY_COLUMNS)
            rows.append(bar)
        data = np.asarray(rows, dtype=np.float64)
        expected_width = width + (len(ACTIVITY_COLUMNS) if activity and retain_activity else 0)
        if data.shape != (entry["rows"], expected_width) or not np.isfinite(data[:, :width]).all():
            raise ValueError("CSV row count or finite-value violation.")
        if not np.all(np.diff(data[:, 0]) == 60):
            raise ValueError("CSV minute cadence violation.")
        if data[0, 0] != stamp_seconds(entry["start_utc"]) or data[-1, 0] != stamp_seconds(entry["end_utc"]):
            raise ValueError("CSV endpoint mismatch.")
        if np.any(data[:, 1:5] <= 0) or np.any(data[:, 5] < 0):
            raise ValueError("Invalid prices or volume.")
        if (np.any(data[:, 3] > np.minimum(data[:, 1], data[:, 4]))
                or np.any(data[:, 2] < np.maximum(data[:, 1], data[:, 4]))):
            raise ValueError("OHLC ordering violation.")
        if entry["id"] == dataset_id:
            selected = data
    return manifest, selected


def write_open_fixture(inbox: Path) -> None:
    """Known effect: high completed volume at t predicts +100 bps at t+4/t+1."""
    inbox.mkdir(parents=True, exist_ok=False)
    n = 86400
    rng = np.random.default_rng(42)
    volume = rng.uniform(1, 2, n)
    price = np.full(n, 100.0)
    for t in range(20, n - 4, 4):
        if volume[t] >= 1.8:
            price[t + 2:t + 5] = [100 + 1 / 3, 100 + 2 / 3, 101]
    path = inbox / "D001.csv"
    start = datetime(2000, 1, 1, tzinfo=UTC)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(HEADER)
        for index in range(n):
            writer.writerow([(start + timedelta(minutes=index)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                             price[index], price[index] + 0.01, price[index] - 0.01,
                             price[index], volume[index]])
    write_json(inbox / "manifest.json", {
        "schema": SCHEMA, "dataset_type": "synthetic", "source": "internal_open",
        "timezone": "UTC", "bar_seconds": 60, "price_reference": "mid", "datasets": [{
            "id": "D001", "file": "D001.csv", "sha256": sha256(path.read_bytes()).hexdigest(),
            "rows": n, "start_utc": "2000-01-01T00:00:00Z",
            "end_utc": "2000-02-29T23:59:00Z",
        }],
    })
