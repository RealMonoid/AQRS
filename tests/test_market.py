import csv
import io
from dataclasses import replace
from datetime import date
from hashlib import sha256
from zipfile import ZipFile

import numpy as np
import pytest

from aqrs.binance_spot_pilot import import_day
from aqrs.market import build_folds, features, generate, targets, validate


def test_utc_bars_reproduce_and_bad_bars_are_rejected():
    bars = generate(7, 100, 5, "SYNTH")
    assert bars.fingerprint == generate(7, 100, 5, "SYNTH").fingerprint
    assert bars.fingerprint != generate(8, 100, 5, "SYNTH").fingerprint
    assert bars.time(1).endswith("+00:00")
    for row, column, bad in [(1, 0, bars.values[0, 0]), (3, 2, 0), (3, 5, np.nan)]:
        values = bars.values.copy()
        values[row, column] = bad
        with pytest.raises(ValueError):
            validate(replace(bars, values=values))


def test_features_use_only_completed_bars():
    bars = generate(7, 100, 5, "SYNTH")
    values = bars.values.copy()
    values[41:, 1:5] *= 1.5
    changed = replace(bars, values=values)
    np.testing.assert_array_equal(features(bars)[:41], features(changed)[:41])
    assert np.isnan(features(bars)[:12, 2]).all()
    assert features(bars)[40, 0] == pytest.approx(
        bars.values[40, 4] / bars.values[39, 4] - 1
    )
    assert bars.time(41) == bars.time(40, close=True)


def test_horizon_and_purged_research_prefix():
    bars = generate(7, 200, 5, "SYNTH")
    prefix = replace(bars, values=bars.values[:160])
    y = targets(prefix, 3)
    assert y[20] == pytest.approx(bars.values[24, 1] / bars.values[21, 1] - 1)
    assert len(y) == 156
    folds = build_folds(160, 3, 40, 20, 3)
    for train, val in folds:
        assert train.stop - 1 + 4 < val.start
        assert val.stop - 1 + 4 < val.start + 20
        assert val.stop - 1 + 4 < 160
        assert np.isfinite(y[val]).all()
    with pytest.raises(ValueError):
        build_folds(80, 3, 40, 20, 3)


@pytest.mark.parametrize(
    ("damage", "error"),
    [
        ("none", None),
        ("missing", "Invalid UTC minute cadence"),
        ("close", "Invalid inclusive close"),
        ("checksum", "Archive SHA-256"),
    ],
)
def test_binance_spot_pilot_requires_intact_utc_day(tmp_path, damage, error):
    day = date(2026, 1, 5)
    stem = f"BTCUSDT-1m-{day}"
    archive = tmp_path / f"{stem}.zip"
    checksum = tmp_path / f"{stem}.zip.CHECKSUM"
    rows = []
    for index in range(1440):
        open_us = 1_767_571_200_000_000 + index * 60_000_000
        rows.append([open_us, 10, 12, 9, 11, 4, open_us + 59_999_999, 0, 0, 0, 0, 0])
    if damage == "missing":
        del rows[1]
    if damage == "close":
        rows[0][6] += 1
    content = io.StringIO()
    csv.writer(content).writerows(rows)
    with ZipFile(archive, "w") as zipped:
        zipped.writestr(f"{stem}.csv", content.getvalue())
    digest = (
        "0" * 64 if damage == "checksum" else sha256(archive.read_bytes()).hexdigest()
    )
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="ascii")

    if error:
        with pytest.raises(ValueError, match=error):
            import_day(archive, checksum, day)
        return
    bars, actual_digest = import_day(archive, checksum, day)
    assert actual_digest == digest
    assert len(bars.values) == 1440
    assert bars.time(0) == "2026-01-05T00:00:00+00:00"
    assert bars.time(0, close=True) == "2026-01-05T00:01:00+00:00"
    assert bars.time(-1, close=True) == "2026-01-06T00:00:00+00:00"
