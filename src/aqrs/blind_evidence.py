"""Machine-readable evidence for the bounded AQRS-B01 runner."""

import csv
import shutil
from hashlib import file_digest
from math import isnan
from pathlib import Path

from aqrs.blind_input import utc_stamp


def file_record(path: Path) -> dict:
    with path.open("rb") as stream:
        digest = file_digest(stream, "sha256").hexdigest()
    return {"file": path.name, "sha256": digest, "bytes": path.stat().st_size}


def check_storage(path: Path, budget: dict) -> None:
    if shutil.disk_usage(path).free < budget["estimated_run_storage_bytes"]:
        raise ValueError("Insufficient disk space for the AQRS-B01 evidence budget.")


def write_csv(path: Path, header, rows) -> dict:
    if path.exists():
        raise FileExistsError(path)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)
    temporary.replace(path)
    return file_record(path)


def verify_csv(path: Path, header, rows) -> bool:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        if next(reader, None) != header:
            return False
        try:
            return all(actual == [str(value) for value in expected]
                       for actual, expected in zip(reader, rows, strict=True))
        except (ValueError, csv.Error):
            return False


def write_features(path: Path, bars, values, plan: dict, training_end: int) -> dict:
    names = plan["features"]

    def rows():
        for index, (bar, row) in enumerate(zip(bars, values, strict=True)):
            partition = ("warmup" if index < plan["warmup"] else
                         "calibration" if index < training_end else "evaluation")
            cells = ["" if isnan(value) else format(value, ".17g") for value in row]
            yield [index, utc_stamp(bar[0]), utc_stamp(bar[0] + 60), partition,
                   *cells, *([""] * (len(names) - len(cells)))]

    return write_csv(path, ["bar_index", "bar_open_time", "available_at", "partition", *names], rows())


def prediction_status(dataset_id: str) -> dict:
    return {"schema": "aqrs.blind-predictions.v1", "dataset_id": dataset_id,
            "status": "NOT_APPLICABLE", "model_candidate_count": 0,
            "columns": ["candidate_id", "fold", "bar_open_time", "available_at", "prediction", "actual"],
            "records": [], "reason": "The frozen plan contains threshold rules only."}
