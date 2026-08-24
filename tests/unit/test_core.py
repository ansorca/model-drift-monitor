"""Unit tests for driftwatch.core (Tier 1 drift-detection logic).

Author-owned per CONTEXT.md's AI Assistance Policy — write these alongside
core.py as its public API takes shape. The placeholder below only proves
pytest collection and the package import path work.
"""


def test_package_imports() -> None:
    import driftwatch

    assert driftwatch.__version__
