from __future__ import annotations

import argparse
from datetime import UTC, datetime


def cmd_healthcheck() -> None:
    now = datetime.now(UTC).isoformat()
    print(f"[ok] scraper CLI is working | utc={now}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="scraper",
        description="iPhone Price Monitor CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("healthcheck", help="Validate the CLI runs")

    args = parser.parse_args()

    if args.command == "healthcheck":
        cmd_healthcheck()
    else:
        raise SystemExit("Unknown command")


if __name__ == "__main__":
    main()
