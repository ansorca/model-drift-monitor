# driftwatch — Model Drift Monitor on AWS

🚧 **Work in progress.** Core drift detection works; the AWS/Terraform side doesn't exist yet.
See [Status](#status) for exactly what's built versus pending.

## Purpose

A model's predictions can quietly diverge from the distribution it was trained and validated
against — through input data changes, upstream schema drift, or shifting real-world conditions.
Without monitoring, that divergence is invisible until it shows up as a downstream failure.

driftwatch is a monitoring pipeline that detects that kind of statistical drift in ML model
outputs relative to a baseline distribution, alerts when drift crosses a threshold, and ships as
an installable Python tool rather than a one-off script.

## What it does

- Ingests prediction logs from S3 (CSV or JSON Lines)
- Compares a current batch of predictions against a reference baseline distribution
- Runs statistical drift tests — Kolmogorov-Smirnov test and/or Population Stability Index (PSI)
  — via [Evidently AI](https://www.evidentlyai.com/)
- Produces a structured drift report per feature: `feature`, `drift_score`, `threshold`, `drifted`
- Exits non-zero when drift is detected, so it can gate a CI/CD pipeline
- Runs on a schedule as an AWS Lambda function and raises a CloudWatch alarm (routed through SNS)
  when the drift score breaches its threshold

## Why drift detection matters

Statistical drift tests turn "the model might be behaving differently now" into a measurable,
alertable signal, instead of something that's only obvious after it's already caused a problem.

- **KS test** — compares two distributions and asks whether they're statistically distinguishable.
- **PSI (Population Stability Index)** — buckets a feature's values and measures how much the
  proportion of observations in each bucket has shifted between baseline and current data.

## Architecture

```
S3 (prediction logs)
      │
      ▼
Lambda (scheduled) ──imports──▶ driftwatch (library)
      │                              │
      │                        drift statistics
      │                        (KS test / PSI via Evidently AI)
      ▼
CloudWatch alarm ──▶ SNS topic ──▶ email / webhook
```

All AWS infrastructure — S3 bucket, Lambda function, CloudWatch alarm, SNS topic, IAM roles — is
provisioned via Terraform. Nothing is created manually in the console.

## Design goals

- **Library first, tool second.** Drift detection logic lives in a single library API
  (`from driftwatch import detect_drift`). The CLI and the Lambda handler are both just callers
  of that library — no duplicated logic between them.
- **Ships as an installable tool**, not a script: `pip install .` and a `driftwatch` CLI entry
  point with useful `--help`, e.g.:
  ```
  driftwatch check --baseline s3://bucket/baseline.csv --current s3://bucket/current.csv
  ```
- **Least-privilege IAM.** The Lambda execution role gets only the permissions it needs
  (`s3:GetObject` on the ingestion bucket, `cloudwatch:PutMetricData`) — nothing broader.
- **Reproducible infrastructure.** `terraform apply` stands up the full stack; `terraform destroy`
  tears it down cleanly, with no orphaned resources.

## Status

This project is under active development. Nothing below is final until every box is checked.

**Drift detection library**
- [x] `detect_drift` / `ks_test` run a per-feature Kolmogorov-Smirnov test via Evidently AI
- [x] Unit tests covering happy path, mismatched/non-numeric columns, empty input, threshold
  behavior
- [ ] PSI (Population Stability Index) as a second statistical test
- [ ] Re-export `detect_drift` from the top-level `driftwatch` package (currently only reachable
  via `driftwatch.core`)

**CLI**
- [x] `driftwatch check --baseline ... --current ...` reads CSVs, reports drift, exits non-zero
  on detection
- [ ] Reading directly from `s3://` URIs (local file paths only so far)
- [ ] End-to-end CLI test against sample data

**AWS infrastructure**
- [ ] S3 bucket for prediction log ingestion
- [ ] Lambda function running the drift check on a schedule (handler is currently a stub)
- [ ] CloudWatch alarm on threshold breach
- [ ] SNS topic routing alerts to email/webhook
- [ ] Least-privilege IAM for the Lambda role

**Terraform**
- [ ] Not started — none of the AWS infrastructure above is provisioned yet

**Repo hygiene**
- [x] CI (ruff, mypy, pytest) runs on every push and PR to `main`; merge to `main` is blocked
  until it's green
- [x] Sample baseline/drifted prediction logs included under `sample_data/`
- [ ] "Design decisions" section explaining the non-obvious choices (e.g. what the drift
  threshold represents)

## License

TBD.
