"""Tests for the driftwatch CLI entry point.

These exercise the argument parser and command dispatch only — drift-detection
logic itself is tested separately in tests/unit/, against driftwatch.core.
"""

import pytest

from driftwatch.cli import build_parser, main


def test_check_parses_required_arguments() -> None:
    parser = build_parser()
    args = parser.parse_args(
        ["check", "--baseline", "s3://bucket/baseline.csv", "--current", "s3://bucket/current.csv"]
    )
    assert args.command == "check"
    assert args.baseline == "s3://bucket/baseline.csv"
    assert args.current == "s3://bucket/current.csv"
    assert args.threshold is None


def test_check_requires_baseline_and_current() -> None:
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["check", "--baseline", "s3://bucket/baseline.csv"])


def test_main_without_command_prints_help(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        main([])
    captured = capsys.readouterr()
    assert "usage" in captured.err.lower() or "usage" in captured.out.lower()
