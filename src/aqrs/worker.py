import json
import os
import sys
from pathlib import Path

from aqrs.platform_guard import arm_parent_loss_guard
from aqrs.storage import write_json


class FitBudgetExhausted(RuntimeError):
    pass


def reserve_fit(request: dict, directory: Path, default: int) -> None:
    """Charge a trusted worker before an estimator or calibration starts."""
    path = directory / "started_fits.json"
    used = json.loads(path.read_text()) if path.exists() else 0
    limit = request.get("fit_limit", default)
    if type(limit) is not int or limit < 0 or used >= limit:
        raise FitBudgetExhausted("Fit budget exhausted before fit.")
    write_json(path, used + 1)


def run(directory: Path, evaluate) -> None:
    write_json(directory / "ready.json", os.getpid())
    # The supervisor sends one byte only after the worker is contained.
    stdin_fd = sys.stdin.fileno()
    if os.read(stdin_fd, 1) != b"1":
        return
    arm_parent_loss_guard(stdin_fd)
    request = json.loads((directory / "request.json").read_text(encoding="utf-8"))
    from aqrs.worker import FitBudgetExhausted as FitStop

    try:
        result = evaluate(request, directory)
    except FitStop:
        write_json(
            directory / "budget_stop.json",
            {"reason": "Fit budget exhausted before fit."},
        )
        raise SystemExit(3)
    write_json(directory / "result.json", result)


def evaluate(request: dict, directory: Path) -> dict:
    if request.get("stage") == "prepare":
        from aqrs.research import prepare_data

        return prepare_data(request)
    from aqrs.evaluation import evaluate as evaluate_trial
    from aqrs.evaluation import evaluate_bar_rule
    from aqrs.market import BAR_RULES

    if rule := BAR_RULES.get(request.get("model")):
        return evaluate_bar_rule(request, directory, rule)
    return evaluate_trial(request, directory)


if __name__ == "__main__":
    run(Path(sys.argv[1]), evaluate)
