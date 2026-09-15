# driftwatch — Model Drift Monitor on AWS

A monitoring pipeline that detects statistical drift in ML model outputs relative to a baseline
distribution, alerts when drift crosses a threshold, and ships as an installable Python tool
rather than a one-off script.

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

A model's predictions can quietly diverge from the distribution it was trained and validated
against — through input data changes, upstream schema drift, or shifting real-world conditions.
Without monitoring, that divergence is invisible until it shows up as a downstream failure.
Statistical drift tests turn "the model might be behaving differently now" into a measurable,
alertable signal.

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

Core drift detection is implemented: `driftwatch.core.detect_drift` runs a Kolmogorov-Smirnov
test per feature via Evidently AI and returns a structured per-feature result, with unit tests
covering the happy path, mismatched/non-numeric columns, empty input, and threshold behavior.
The `driftwatch check` CLI command reads baseline/current CSVs and reports drift with a non-zero
exit code.

Not yet built: the Lambda handler (stub only), all Terraform-provisioned AWS infrastructure
(S3, CloudWatch, SNS, IAM), and support for reading directly from S3 URIs. CI runs ruff, mypy,
and pytest on every push and PR to `main`.

## License

TBD.
