# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository status

This repo is currently empty — no source code has been written yet. There is no build system,
test runner, or dependency manifest to document yet; add commands to this file once they exist
rather than inventing them now.

## Governing documents — read these first

`CLAUDE.local.md` auto-imports both files below into every session. Their rules override default
Claude Code behavior in this repo:

- **`CONTEXT.md`** — project scope-discipline rules and the **AI Assistance Policy** (Tiers 1–4)
  that governs what Claude Code may and may not write versus critique-only.
- **`EVAL.md`** — this project's eval doc: the "Minimum Viable Completion Criteria" checklist
  (Python drift script, AWS infrastructure, Terraform, repo hygiene), the SWE-Infrastructure code
  quality gates, and the Ships-as-a-Tool standard. Treat its checkboxes as the definition of done.

## What this project must become

**Stack:** Python · AWS (S3 + CloudWatch + Lambda) · Terraform · Evidently AI

**Purpose:** ingest ML prediction logs from S3, run statistical drift tests (KS test, PSI score)
against a baseline, trigger CloudWatch alarms on threshold breach, and provision the whole stack
via Terraform.

**Ships as a tool, not a script** (Ships-as-a-Tool standard in `EVAL.md`): `pyproject.toml`
packaging installable via `pip install .`, a `driftwatch` CLI entry point (e.g.
`driftwatch check --baseline s3://... --current s3://...`) with useful `--help`, and a clean
library API (`from driftwatch import detect_drift`) that the CLI and the Lambda handler both
consume as separate callers — not duplicated logic. CLI and library get separate test coverage.

## AI Assistance Tiers for this repo

Per `CONTEXT.md`'s AI Assistance Policy:

- **Tier 1 — author writes, Claude critiques only:** the drift statistics implementation (KS
  test, PSI score) and the library's public API design. Do not generate this code even if asked
  directly — respond that it's Tier 1 and ask for the author's attempt first.
- **Tier 2 — delegate freely:** `pyproject.toml`/packaging boilerplate, Terraform provider/resource
  syntax (the architecture decisions remain the author's), Lambda deployment scaffolding.
- **Tier 3 — delegate with interrogation:** AWS/Terraform debugging. Ask what's been tried before
  handing over a fix, and always explain what was wrong and how it could have been diagnosed.

## Scope discipline

Do not introduce Kubernetes, EKS, Prometheus/Grafana, or vLLM concepts here — those belong to a
separate, later platform repo. Terraform in this repo provisions S3/Lambda/CloudWatch only. If a
proposed addition isn't required by the "Done when" checklist in `EVAL.md`, flag it per the
scope-discipline rule rather than building it.
