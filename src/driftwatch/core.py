from dataclasses import dataclass

import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

"""Core drift-detection library.

Tier 1 (per CONTEXT.md's AI Assistance Policy): the drift statistics
implementation (KS test, PSI score) and this module's public API are
author-written. Claude Code does not generate this module's logic — write a
first pass, then ask for a critique.

Once implemented, `driftwatch/__init__.py` should re-export the public
entry point (e.g. `detect_drift`) so both `driftwatch/cli.py` and
`driftwatch/lambda_handler.py` can import it as `from driftwatch import ...`
rather than duplicating logic.
"""


@dataclass
class DriftResult:
    """Class to hold drift detection results for a single feature."""

    feature_name: str
    ks_statistic: float
    drift_detected: bool


def ks_test(baseline_data: pd.DataFrame, 
            production_data: pd.DataFrame, 
            ks_p_value_threshold: float = 0.05
) -> list[DriftResult]:
    """Perform a Kolmogorov-Smirnov test to detect drift between two datasets.

    Args:
        baseline_data: The baseline dataset (e.g., training data).
        production_data: The production dataset (e.g., live inference data).
        ks_p_value_threshold: The maximum ks p-value before drift is detected.

    Returns:
        A list of DriftResults objects containing feature names and drift detection results.
    """
    # baseline_data: Your training or validation feature array
    # production_data: Your live inference feature array

    if baseline_data.empty or production_data.empty:
        raise ValueError("Input arrays must not be empty.")

    for feature in baseline_data.columns:
        if feature not in production_data.columns:
            raise ValueError(f"Feature '{feature}' is missing in production data.")

    for feature in production_data.columns:
        if feature not in baseline_data.columns:
            raise ValueError(f"Feature '{feature}' is missing in baseline data.")

    for feature in baseline_data.columns:
        if not pd.api.types.is_numeric_dtype(baseline_data[feature]):
            raise ValueError(f"Feature '{feature}' in baseline data is not numeric.")
        if not pd.api.types.is_numeric_dtype(production_data[feature]):
            raise ValueError(f"Feature '{feature}' in production data is not numeric.")


    report = Report([
            DataDriftPreset(num_method="ks", num_threshold=ks_p_value_threshold)
            ])

    drift_results =  [DriftResult(x["config"]["column"],
                                    float(x["value"]),
                                    x["value"] < ks_p_value_threshold)
                        for x in report.run(production_data, baseline_data).dict()["metrics"] 
                        if x["config"]["type"] == "evidently:metric_v2:ValueDrift" ]


    return drift_results


def detect_drift(
    baseline_data: pd.DataFrame,
    production_data: pd.DataFrame,
    ks_p_value_threshold: float = 0.05,
) -> list[DriftResult]:
    """Detect drift between two datasets.

    Args:
        baseline_data: The baseline dataset (e.g., training data).
        production_data: The production dataset (e.g., live inference data).
        ks_p_value_threshold: The maximum ks p-value before drift is detected.

    Returns:
        A list of DriftResults objects containing feature names and drift detection results.
    """
    return ks_test(baseline_data, production_data, ks_p_value_threshold=ks_p_value_threshold)
