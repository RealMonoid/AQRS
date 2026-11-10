"""Import one UTC day of Binance Vision BTCUSDT spot minute bars offline."""

import argparse
import csv
import io
import json
import sys
from datetime import UTC, date, datetime, time
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZIP_STORED, BadZipFile, ZipFile
from zlib import error as CompressionError

import numpy as np

from aqrs.market import Bars, validate, write_dataset

ARCHIVE_BASE = "https://data.binance.vision/data/spot/daily/klines/BTCUSDT/1m"
SYMBOL = "BTCUSDT"
M1_DEVELOPMENT_DAY = date(2026, 1, 5)
M1_HOLDOUT_DAY = date(2026, 1, 6)
MINUTES_PER_DAY = 1440
MICROSECONDS_PER_SECOND = 1_000_000
MINUTE_US = 60 * MICROSECONDS_PER_SECOND
INPUT_LIMIT = 512 * 1024
IMPORT_ERRORS = (ValueError, OSError, BadZipFile, CompressionError, csv.Error)


def require_m1_development_day(day: str) -> None:
    if day != M1_DEVELOPMENT_DAY.isoformat():
        raise ValueError(f"The M1 spot campaign only admits {M1_DEVELOPMENT_DAY} UTC.")


def import_day(archive: Path, checksum: Path, day: date) -> tuple[Bars, str]:
    reserved_archive = f"{SYMBOL}-1m-{M1_HOLDOUT_DAY}.zip".casefold()
    reserved_names = {reserved_archive, f"{reserved_archive}.checksum"}
    if day == M1_HOLDOUT_DAY or reserved_names.intersection(
        (archive.name.casefold(), checksum.name.casefold())
    ):
        raise ValueError(
            f"{M1_HOLDOUT_DAY} UTC is reserved and cannot be opened by the spot importer."
        )
    if day < date(2025, 1, 1):
        raise ValueError("The pilot expects microsecond archives from 2025 onward.")
    stem = f"{SYMBOL}-1m-{day.isoformat()}"
    with archive.open("rb") as source:
        payload = source.read(INPUT_LIMIT + 1)
    with checksum.open("rb") as source:
        published = source.read(4097)
    if len(payload) > INPUT_LIMIT or len(published) > 4096:
        raise ValueError("Archive or checksum exceeds the pilot size limit.")
    digest = sha256(payload).hexdigest()
    if published.decode("ascii").split() != [digest, f"{stem}.zip"]:
        raise ValueError("Archive SHA-256 or published filename does not match.")

    first_open = int(datetime.combine(day, time.min, UTC).timestamp())
    values = np.empty((MINUTES_PER_DAY, 6), dtype=np.float64)
    with ZipFile(io.BytesIO(payload)) as zipped:
        members = zipped.infolist()
        if len(members) != 1 or members[0].filename != f"{stem}.csv":
            raise ValueError("Expected exactly one CSV for the selected UTC day.")
        member = members[0]
        if member.file_size > INPUT_LIMIT:
            raise ValueError("Uncompressed CSV exceeds the pilot size limit.")
        if member.flag_bits & 1 or member.compress_type not in (
            ZIP_STORED,
            ZIP_DEFLATED,
        ):
            raise ValueError("Expected an unencrypted stored or deflated CSV.")
        with zipped.open(member) as compressed:
            with io.TextIOWrapper(compressed, encoding="ascii", newline="") as source:
                rows = csv.reader(source, strict=True)
                count = 0
                for count, row in enumerate(rows, start=1):
                    if count > MINUTES_PER_DAY or len(row) != 12:
                        raise ValueError(
                            "Expected 1,440 rows with 12 kline fields each."
                        )
                    open_seconds = first_open + (count - 1) * 60
                    open_us = open_seconds * MICROSECONDS_PER_SECOND
                    if int(row[0]) != open_us:
                        raise ValueError(f"Invalid UTC minute cadence at row {count}.")
                    if int(row[6]) != open_us + MINUTE_US - 1:
                        raise ValueError(f"Invalid inclusive close at row {count}.")
                    # Bars derives availability at the next minute boundary.
                    values[count - 1] = [open_seconds, *map(float, row[1:6])]
                if count != MINUTES_PER_DAY:
                    raise ValueError("Expected a full UTC day of 1,440 minutes.")
    bars = Bars(values, SYMBOL, bar_minutes=1)
    validate(bars)
    return bars, digest


def import_manifest(bars: Bars, digest: str, day: date) -> dict:
    source = f"{ARCHIVE_BASE}/{SYMBOL}-1m-{day.isoformat()}.zip"
    return {
        "source_url": source,
        "checksum_url": f"{source}.CHECKSUM",
        "archive_sha256": digest,
        "dataset_id": bars.fingerprint,
        "symbol": bars.symbol,
        "bar_minutes": bars.bar_minutes,
        "bar_count": len(bars.values),
        "first_bar_open_utc": bars.time(0),
        "last_bar_open_utc": bars.time(-1),
        "last_bar_available_utc": bars.time(-1, close=True),
    }


def publish(bars: Bars, digest: str, day: date, output: Path) -> None:
    report = import_manifest(bars, digest, day)
    if output.exists():
        raise FileExistsError("Output directory already exists.")
    with TemporaryDirectory(dir=output.parent) as staging:
        result = Path(staging) / "result"
        result.mkdir()
        write_dataset(bars, result / "dataset.csv")
        (result / "import_report.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
        result.rename(output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day", type=date.fromisoformat, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--checksum", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        bars, digest = import_day(args.archive, args.checksum, args.day)
        publish(bars, digest, args.day, args.output)
    except IMPORT_ERRORS as error:
        print(f"Import rejected: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
