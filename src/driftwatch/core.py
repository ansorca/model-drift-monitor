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
