
import pandas as pd
import pytest

import driftwatch
from driftwatch.core import DriftResult, ks_test


def test_package_imports() -> None:
    assert driftwatch.__version__


def test_core_ks_test_no_drift_in_identical_datasets() -> None:
    baseline_data = pd.DataFrame(
        {"feature1": [1, 2, 3, 4, 5, 6], "feature2": [10, 20, 30, 40, 50, 60]}
    )
    production_data = pd.DataFrame(
        {"feature1": [1, 2, 3, 4, 5, 6], "feature2": [10, 20, 30, 40, 50, 60]}
    )

    result: list[DriftResult] = ks_test(baseline_data, production_data)

    assert all(not drift_results.drift_detected for drift_results in result), (
        "Expected no drift detected for identical datasets"
    )


def test_core_ks_test_detects_drift_in_different_datasets() -> None:
    baseline_data = pd.DataFrame(
        {"feature1": [1, 2, 3, 4, 5, 6], "feature2": [10, 20, 30, 40, 50, 60]}
    )
    production_data = pd.DataFrame(
        {"feature1": [10, 20, 30, 40, 50, 60], "feature2": [100, 200, 300, 400, 500, 600]}
    )

    result: list[DriftResult] = ks_test(baseline_data, production_data)

    assert any(drift_results.drift_detected for drift_results in result), (
        "Expected drift detected for different datasets"
    )


def test_core_ks_test_detects_drift_if_one_feature_changes() -> None:
    baseline_data = pd.read_csv("./sample_data/baseline.csv").drop(columns=["timestamp"])
    production_data = pd.read_csv("./sample_data/current_with_drift.csv").drop(
        columns=["timestamp"]
    )

    result: list[DriftResult] = ks_test(baseline_data, production_data)

    drifted_features: list[str] = [
        drift_results.feature_name for drift_results in result if drift_results.drift_detected
    ]
    assert (
        len(drifted_features) == 2
        and drifted_features[0] == "feature_1"
        and drifted_features[1] == "prediction"
    ), "Expected drift detected for 'feature2' and 'prediction' when they change in production data"
    assert any(drift_results.drift_detected for drift_results in result), (
        "Expected drift detected when one feature changes"
    )


def test_core_ks_test_raises_error_for_missing_feature() -> None:
    baseline_data = pd.DataFrame({"feature1": [1, 2, 3, 4, 5, 6]})
    production_data = pd.DataFrame({"feature2": [10, 20, 30, 40, 50, 60]})

    with pytest.raises(ValueError, match="Feature 'feature1' is missing in production data."):
        ks_test(baseline_data, production_data)


def test_core_ks_test_raises_error_for_non_numeric_feature() -> None:
    baseline_data = pd.DataFrame(
        {"feature1": [1, 2, 3, 4, 5, 6], "feature2": ["a", "b", "c", "d", "e", "f"]}
    )
    production_data = pd.DataFrame(
        {"feature1": [1, 2, 3, 4, 5, 6], "feature2": ["g", "h", "i", "j", "k", "l"]}
    )

    with pytest.raises(ValueError, match="Feature 'feature2' in baseline data is not numeric."):
        ks_test(baseline_data, production_data)


def test_core_ks_test_raises_error_for_empty_datasets() -> None:
    baseline_data = pd.DataFrame({"feature1": [], "feature2": []})
    production_data = pd.DataFrame({"feature1": [], "feature2": []})

    with pytest.raises(ValueError, match="Input arrays must not be empty."):
        ks_test(baseline_data, production_data)


def test_core_ks_test_zero_variance_feature() -> None:
    baseline_data = pd.DataFrame({"feature1": [1, 1, 1, 1, 1], "feature2": [10, 20, 30, 40, 50]})
    production_data = pd.DataFrame({"feature1": [1, 1, 1, 1, 1], "feature2": [10, 20, 30, 40, 50]})

    result: list[DriftResult] = ks_test(baseline_data, production_data)

    assert all(not drift_results.drift_detected for drift_results in result), (
        "Expected no drift detected for zero variance feature"
    )


def test_core_ks_test_boundary_threshold() -> None:
    baseline_data = pd.DataFrame({"feature1": [1, 2, 3, 4, 5]})
    production_data = pd.DataFrame(
        {"feature1": [5, 15, 18, 22, 25]}
    )

    # Using a very low ks score threshold to ensure drift is detected
    result: list[DriftResult] = ks_test(baseline_data, 
                                        production_data, 
                                        ks_p_value_threshold=0.01)

    assert all(drift_results.drift_detected for drift_results in result), (
        "Expected drift detected with low ks p-value threshold"
    )
