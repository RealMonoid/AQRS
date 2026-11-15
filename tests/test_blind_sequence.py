"""Offline publication and evidence checks for the sequential blind runner."""


import pytest

from aqrs import blind_search as blind
from aqrs.blind_sequence import SERIES, published_state


def test_inbox_authorization_path_rejects_before_file_probe(tmp_path, monkeypatch):
    from pathlib import Path

    path = tmp_path / "artifacts/blind-test/inbox/D002.csv"
    monkeypatch.setattr(Path, "lstat", lambda self: pytest.fail("No file probe is allowed."))
    with pytest.raises(ValueError, match="outside the blind inbox"):
        blind.authorize(tmp_path, path, "D002", "0" * 64, "external_blind", {})


@pytest.mark.parametrize("groups", [
    [["D001-start.json"], ["D001-verdict.json"], ["D001-gaps.jsonl", "D001-summary.txt"]],
    [["D001-start.json", "D001-verdict.json", "D001-gaps.jsonl", "D001-summary.txt"]],
    [["D001-start.json"], ["D002-start.json"], ["D001-verdict.json", "D001-gaps.jsonl", "D001-summary.txt"]],
])
def test_sequence_rejects_bad_commit_order_before_loading_records(groups):
    paths = [f"{SERIES}/{name}" for group in groups for name in group]
    history = "\n".join(line for index, group in enumerate(groups, 1)
                        for line in (f"{index:040x}", *[f"A\t{SERIES}/{name}" for name in group]))
    outputs = {"ls-remote": "a" * 40, "rev-parse": "a" * 40, "ls-tree": "\n".join(paths), "log": history}
    with pytest.raises(ValueError, match="out of order or split a closure"):
        published_state(lambda action, *args: outputs[action], lambda *args: pytest.fail("No record read."))



def test_direct_blind_replay_cannot_bypass_current_admission(tmp_path, monkeypatch):
    from aqrs.admission import AdmissionRejected
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(blind, "measure", lambda *a, **k: pytest.fail("Unqualified replay"))
    with pytest.raises(AdmissionRejected, match="not qualified"):
        blind.replay_evidence(tmp_path, "D001", "1" * 40, ["S01", "P01"])
    assert not (tmp_path / "artifacts/aqrs-b01/runs").exists()
