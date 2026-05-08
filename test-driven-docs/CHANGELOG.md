# Changelog

## 2026-05-07 — Material feedback incorporation

- Tightened `SKILL.md` frontmatter description to reduce over-triggering.
- Moved detailed workflow behavior out of `SKILL.md` into `resources/workflow.md`.
- Added `resources/document-set-audit.md` making Mode F explicit: per-document Mode D/E evaluation for each document, followed by set-level audit.
- Added `resources/severity-calibration.md` with concrete critical/high/medium/low examples.
- Updated `resources/questions.schema.yaml` to support either `document` or `document_set`.
- Updated `resources/evaluation.schema.yaml` to support explicit `artifact_type: single_document|document_set` and separate document-set sections:
  - `per_document_evaluations`
  - `set_level_evaluation`
  - `consolidated_fix_plan`
- Updated `resources/evaluator-prompt.md` so document-set audits do not collapse multiple docs into one corpus.
- Reworked `resources/examples/example.docset.evaluation.yaml` to show Mode F as composed per-document evaluation plus set-level audit.
- Added `resources/examples/example.docset.questions.yaml`.
- Fixed the rate-limit example wording from "40 minutes earlier" to "40 requests per minute."
- Added `scripts/validate_artifacts.py` for deterministic YAML/schema/count validation.

## 2026-05-07 — ATDD frontmatter manifest support

- Added `resources/frontmatter-manifest.md` defining YAML frontmatter as the document-local ATDD manifest.
- Added `resources/tddoc.frontmatter.schema.yaml` for validating document-local manifests.
- Updated `SKILL.md`, `resources/workflow.md`, `resources/document-set-audit.md`, and `resources/evaluator-prompt.md` to use frontmatter for identity, routing, authority, test-suite discovery, document-set membership, and metadata-drift checks.
- Updated `resources/authoring-template.md` with an ATDD frontmatter scaffold.
- Added `resources/examples/s3-to-snowflake-external-table-ingestion-runbook.md` as a frontmatter-backed document example.
- Updated `scripts/validate_artifacts.py` to validate ATDD frontmatter, referenced suite/evaluation files, related-document paths, and optional document body hashes.
