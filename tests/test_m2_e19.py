import numpy as np
import pytest

from aqrs import m2_e19
from aqrs.market import generate


def test_coverage_counts_only_non_overlapping_entries():
    bars = generate(42, 100, 1, "SYNTH")
    assert m2_e19.coverage_days(
        bars,
        np.array([12, 13, 42, 72]),
        np.array([True, False, False, True]),
        slice(12, 73),
    ) == {bars.time(12)[:10]: {"accepted": 2, "rejected": 1}}


def test_coverage_requires_both_folds_without_a_price_outcome(tmp_path):
    bars = generate(42, m2_e19.ROWS, 1, "SYNTH")
    original = m2_e19.coverage(bars, {"fit_limit": 2}, tmp_path)
    changed = bars.values.copy()
    changed[:, 1] *= 2
    second = tmp_path / "different-opens"
    second.mkdir()
    assert (
        m2_e19.coverage(type(bars)(changed, bars.symbol, 1), {"fit_limit": 2}, second)
        == original
    )
    assert original["estimator_fits"] == 0
    assert m2_e19.read_json(tmp_path / "fits.json") == 2


def test_extra_archive_is_rejected_before_import(tmp_path, monkeypatch):
    allowlist = m2_e19.d01_archive_rows(m2_e19.read_json(m2_e19.ROOT / m2_e19.D01_PATH))
    allowlist.append({"name": "BTCUSDT-1m-2026-01-06.zip"})
    monkeypatch.setattr(
        "aqrs.m2_e14.load_spot_day", lambda *a, **kw: pytest.fail("Archive read")
    )
    with pytest.raises(ValueError, match="fixed BTCUSDT scope"):
        m2_e19.load_bars({"archives": str(tmp_path), "allowlist": allowlist}, tmp_path)
