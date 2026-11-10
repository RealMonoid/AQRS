import argparse
import json
import sqlite3
import sys
from pathlib import Path

from aqrs.config import load
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
    args = parser.parse_args()
    try:
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
