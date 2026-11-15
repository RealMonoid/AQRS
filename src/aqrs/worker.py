import json
import os
import sqlite3
import sys
from contextlib import ExitStack
from pathlib import Path

from aqrs.admission import AdmissionRejected
from aqrs.platform_guard import arm_parent_loss_guard
from aqrs.storage import write_json
from aqrs.study_admission import admitted_worker, require_worker


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
    from aqrs.worker import FitBudgetExhausted as FitStop

    with ExitStack() as stack:
        try:
            request = json.loads(
                (directory / "request.json").read_text(encoding="utf-8")
            )
            callback = getattr(evaluate, "__code__", None)
            if callback is None:
                raise AdmissionRejected(
                    "ENTRY_UNQUALIFIED", "The worker callback is not qualified."
                )
            entry = Path(callback.co_filename)
            if not entry.is_file() or entry.read_text(encoding="utf-8") != Path(
                __file__
            ).read_text(encoding="utf-8"):
                raise AdmissionRejected(
                    "ENTRY_UNQUALIFIED",
                    "The worker callback is not the qualified common entry.",
                )
            stack.enter_context(admitted_worker(request))
        except AdmissionRejected as error:
            write_json(
                directory / "admission_stop.json",
                {"reason_code": error.code, "stop_reason": str(error)},
            )
            raise SystemExit(4)
        except (OSError, sqlite3.Error, ValueError, TypeError, KeyError) as error:
            write_json(
                directory / "admission_stop.json",
                {
                    "reason_code": "ADMISSION_UNVERIFIABLE",
                    "stop_reason": f"Worker admission could not be verified ({type(error).__name__}).",
                },
            )
            raise SystemExit(4)
        try:
            result = evaluate(request, directory)
        except AdmissionRejected as error:
            write_json(
                directory / "admission_stop.json",
                {
                    "reason_code": error.code,
                    "stop_reason": str(error),
                    "required_action": getattr(
                        error, "required_action", "Restore current admission."
                    ),
                    "resumption_condition": getattr(
                        error, "resumption_condition", "A fresh admission passes."
                    ),
                },
            )
            raise SystemExit(4)
        except FitStop:
            write_json(
                directory / "budget_stop.json",
                {"reason": "Fit budget exhausted before fit."},
            )
            raise SystemExit(3)
    write_json(directory / "result.json", result)


def evaluate(request: dict, directory: Path) -> dict:
    require_worker()
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
