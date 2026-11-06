import json
import os
import sys
from pathlib import Path

from aqrs.platform_guard import arm_parent_loss_guard
from aqrs.storage import write_json


def run(directory: Path, evaluate) -> None:
    write_json(directory / "ready.json", os.getpid())
    # The supervisor sends one byte only after the worker is contained.
    stdin_fd = sys.stdin.fileno()
    if os.read(stdin_fd, 1) != b"1":
        return
    arm_parent_loss_guard(stdin_fd)
    request = json.loads((directory / "request.json").read_text(encoding="utf-8"))
    write_json(directory / "result.json", evaluate(request, directory))


def evaluate(request: dict, directory: Path) -> dict:
    from aqrs.evaluation import evaluate as evaluate_trial

    return evaluate_trial(request, directory)


if __name__ == "__main__":
    run(Path(sys.argv[1]), evaluate)
