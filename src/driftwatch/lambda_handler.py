"""AWS Lambda entry point for the scheduled drift check.

Tier 2 scaffolding: imports the driftwatch library and adapts its result to
CloudWatch — no drift-detection logic lives here. The event/environment
contract (how the baseline and current S3 locations are passed in) is set by
the Terraform module that wires the schedule and IAM role.
"""

from __future__ import annotations

from typing import Any


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Entry point invoked on the CloudWatch Events schedule.

    TODO(author): once `driftwatch.core` exports a public entry point, call
    it here with baseline/current locations resolved from `event` or
    environment variables, then publish the drift score via
    `cloudwatch:PutMetricData` so the Terraform-defined alarm can act on it.
    """
    raise NotImplementedError(
        "lambda_handler depends on driftwatch.core's public API (Tier 1)."
    )
