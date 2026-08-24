"""Command-line entry point for driftwatch.

Tier 2 scaffolding: thin argparse wrapper around the driftwatch library. No
drift-detection logic lives here — once `driftwatch.core` exports a public
entry point, `_run_check` below should call it and format its result, not
reimplement it.
"""

from __future__ import annotations

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="driftwatch",
        description="Detect statistical drift between a baseline and a current prediction log.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser(
        "check", help="Compare a current dataset against a baseline and report drift."
    )
    check.add_argument(
        "--baseline", required=True, help="S3 URI or local path to the baseline dataset."
    )
    check.add_argument(
        "--current", required=True, help="S3 URI or local path to the current dataset."
    )
    check.add_argument(
        "--threshold",
        type=float,
        default=None,
        help="Override the default drift threshold.",
    )

    return parser


def _run_check(args: argparse.Namespace) -> int:
    # TODO(author): call driftwatch.core's public API once it exists, e.g.
    #   from driftwatch import detect_drift
    #   report = detect_drift(args.baseline, args.current, threshold=args.threshold)
    # and print/exit based on its result (see EVAL.md: non-zero exit on drift).
    raise NotImplementedError(
        "driftwatch check is not implemented yet — see src/driftwatch/core.py (Tier 1)."
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "check":
        return _run_check(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
