---
tddoc:
  version: 1
  artifact_type: document
  id: s3-to-snowflake-external-table-ingestion-runbook
  title: S3-to-Snowflake External Table Ingestion Runbook
  role_in_set: operational_runbook
  document_set: s3-snowflake-ingestion-docset
  audience:
    primary:
      - data platform engineer
      - analytics engineer
    secondary:
      - support engineer
      - release owner
  purpose: >
    Explain how files dropped into S3 are automatically discovered and made
    available to dbt staging models in Snowflake.
  non_goals:
    - Define the upstream vendor file contract.
    - Replace Terraform module documentation.
    - Document all Snowflake external table features.
  expected_reader_actions:
    - Configure or review AWS notification resources.
    - Configure or review Snowflake external table objects.
    - Validate that a newly dropped file is queryable downstream.
    - Diagnose missing-file ingestion failures.
  source_of_truth:
    authority: authoritative_for_operating_procedure
    precedence:
      - Terraform is authoritative for AWS infrastructure.
      - Snowflake DDL/dbt code are authoritative for deployed database objects.
      - This document is authoritative for the human operating procedure.
    conflict_resolution: >
      If this document disagrees with deployed Terraform, Snowflake DDL, or dbt
      code, treat deployed configuration as factual truth and update this
      document through review.
  authoritative_for:
    - ingestion operating procedure
    - missing-file diagnosis path
  related_documents:
    - path: ./example.contract.yaml
      relationship: contract_example
    - path: ./example.questions.yaml
      relationship: tested_by
  freshness:
    expectation: Review quarterly and on ingestion-path changes.
    owner: data-platform
    last_reviewed: "2026-05-07"
  tests:
    suite: ./example.questions.yaml
    blocking:
      - orientation-001
      - execution-001
      - operations-001
      - governance-001
  evaluation:
    latest: ./example.evaluation.yaml
    status: fail
    evaluated_at: "2026-05-07"
    evaluator: test-driven-docs
    document_hash: sha256:46f7b41e21f05d8edae514a3b5f02253828a4e76f27be3969a53907c7587725e
---

# S3-to-Snowflake External Table Ingestion Runbook

## Purpose

This runbook explains how files dropped into an S3 bucket are discovered by Snowflake external table refresh plumbing and made available to dbt staging models.

## Audience

Primary readers are data platform engineers and analytics engineers. Secondary readers are support engineers and release owners.

## Source of Truth and Precedence

Terraform is authoritative for AWS infrastructure. Snowflake DDL and dbt code are authoritative for deployed database objects. This runbook is authoritative for the human operating procedure.

If this runbook disagrees with deployed Terraform, Snowflake DDL, or dbt code, treat deployed configuration as factual truth and update this runbook through review.

## Standard Path

1. A file lands in the configured S3 bucket and prefix.
2. AWS notification plumbing signals Snowflake that new external-table metadata may be available.
3. Snowflake refreshes external table metadata.
4. dbt staging models query the external table through the configured source.

## Validation

Confirm the S3 object exists, confirm the AWS notification fired, confirm Snowflake external table metadata includes the file, and confirm the dbt staging model can query the expected rows.
