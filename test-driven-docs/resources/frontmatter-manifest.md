# ATDD Frontmatter Manifest

Use YAML frontmatter as the document-local ATDD manifest. The manifest makes the document discoverable, routable, and auditable, but it should not become the full artifact store.

## Default split

- Frontmatter is authoritative for document identity, role, audience summary, purpose summary, source-of-truth boundaries, freshness expectations, artifact routing, and set relationships.
- External question-suite files are authoritative for full documentation tests when referenced by frontmatter.
- External evaluation files are generated evidence and are never authoritative over the document, manifest, or test suite.
- Inline tests are allowed only for small documents where the test suite remains readable.

## Precedence

When ATDD metadata appears in document frontmatter, apply this precedence:

1. Explicit external files referenced by frontmatter are authoritative for full tests.
2. Frontmatter is authoritative for document identity, role, audience, source-of-truth boundary, authoritative topics, document-set membership, and artifact routing.
3. Generated evaluation files are attestations of a prior evaluation run, not the source of truth.
4. If frontmatter and referenced artifacts disagree, fail evaluation with a metadata-drift finding.

## Recommended manifest

```yaml
---
tddoc:
  version: 1
  artifact_type: document

  id: s3-to-snowflake-ingestion-runbook
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
    - path: ./s3-to-snowflake-architecture.md
      relationship: explained_by
    - path: ./s3-to-snowflake-terraform.md
      relationship: implemented_by

  freshness:
    expectation: Review quarterly and on ingestion-path changes.
    owner: data-platform
    last_reviewed: 2026-05-07

  tests:
    suite: ./s3-to-snowflake-ingestion.questions.yaml
    blocking:
      - orientation-001
      - execution-001
      - operations-001
      - governance-001

  evaluation:
    latest: ./s3-to-snowflake-ingestion.eval.yaml
    status: pass_with_warnings
    evaluated_at: 2026-05-07
    document_hash: sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
---
```

## Inline tests

Inline tests are acceptable for short ADRs, small repo instructions, or compact docs where an external file would add more overhead than value.

```yaml
---
tddoc:
  version: 1
  artifact_type: document
  id: adr-007-memgraph
  title: ADR-007 — Use Memgraph for Phase 1 Asset Graph
  tests_inline:
    - id: decision-001
      category: decision
      severity: critical
      reader_role: engineer
      question: What decision was made?
      expected_answer_properties:
        - identifies chosen graph database
        - states decision scope
        - states whether decision is reversible
      failure_risk: Reader cannot distinguish decision from exploration.
      blocking: true
---
```

Do not inline large generated evaluations.

## Evaluation stamps

The document may carry a compact evaluation stamp so CI and reviewers can see the last known evaluation state.

```yaml
evaluation:
  latest: ./my-doc.eval.yaml
  status: fail
  evaluated_at: 2026-05-07
  evaluator: test-driven-docs
  document_hash: sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
```

The full evaluation body belongs in the external file referenced by `evaluation.latest`.

## Document-set use

For Mode F, frontmatter should be used to establish document role, routing, authority, and document-set membership before deriving tests.

Useful fields:

```yaml
document_set: jira-workflow-docset
role_in_set: policy
authoritative_for:
  - workflow-state-precedence
  - handoff-required-fields
related_documents:
  - path: ./story-writing-guide.md
    relationship: depends_on
  - path: ./scrum-master-playbook.md
    relationship: operationalizes
```

Mode F should report failures when:

- two documents claim authority for the same topic but disagree
- no document claims authority for a critical/high reader action
- a document references a missing related document
- an answer exists somewhere but not in the document that claims or should claim authority
- routing is ambiguous
