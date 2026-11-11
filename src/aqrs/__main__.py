import argparse
import json
import sqlite3
import sys
from pathlib import Path

from aqrs.config import load
from aqrs.planning import mean_precision_plan
from aqrs.research import run


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="aqrs", description="Offline market research."
    )
    group = parser.add_subparsers(dest="group", required=True)
    research = group.add_parser(
        "research", help="Plan or run a bounded research campaign."
    )
    actions = research.add_subparsers(dest="action", required=True)
    for action in ("plan", "run"):
        command = actions.add_parser(action)
        command.add_argument("--config", type=Path, required=True)
    precision = actions.add_parser(
        "precision", help="Calculate conditional mean precision without data or fits."
    )
    precision.add_argument("--sd-bps", type=float, required=True)
    precision.add_argument("--effect-bps", type=float, required=True)
    precision.add_argument("--independent-units", type=int, required=True)
    precision.add_argument("--alpha", type=float, default=0.05)
    precision.add_argument("--power", type=float, default=0.8)
    args = parser.parse_args()
    try:
        if args.action == "precision":
            result = mean_precision_plan(
                args.sd_bps,
                args.effect_bps,
                args.independent_units,
                alpha=args.alpha,
                power=args.power,
            )
            code = 0
        else:
            config, base = load(args.config)
            result, code = run(config, base, plan_only=args.action == "plan")
    except ValueError as error:
        print(f"AQRS configuration or data error: {error}", file=sys.stderr)
        return 2
    except (OSError, sqlite3.Error) as error:
        print(
            f"AQRS storage or operating-system error ({type(error).__name__}).",
            file=sys.stderr,
        )
        return 1
    except KeyboardInterrupt:
        print("AQRS campaign cancelled by operator.", file=sys.stderr)
        return 130
    print(json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
