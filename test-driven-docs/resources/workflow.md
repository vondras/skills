---
tddoc:
  version: 1
  artifact_type: document
  id: test-driven-docs-workflow
  document_set: test-driven-docs-skill-docset
  role_in_set: reference
  title: Test-Driven Documentation Workflow
  audience:
    primary:
      - skill operator
  purpose: >
    Describe the six phases of the test-driven documentation workflow and the
    output shape for each mode (A–F), so that the skill operator knows exactly
    what to produce at each step.
  non_goals:
    - Define when to invoke the skill or select a mode (that is SKILL.md).
    - Define Mode F composition rules and gates (that is resources/document-set-audit.md).
    - Provide evidence-bound evaluation instructions (that is resources/evaluator-prompt.md).
  expected_reader_actions:
    - Execute the correct phase sequence for the selected mode.
    - Produce the prescribed output artifact for the selected mode.
    - Apply frontmatter manifest rules during Phase 1 and Phase 4.
  source_of_truth:
    authority: authoritative_for_workflow_procedure
    precedence:
      - This document is authoritative for per-phase procedure and mode output shapes.
      - resources/document-set-audit.md is authoritative for Mode F composition and gates.
      - resources/evaluator-prompt.md is authoritative for evidence-bound evaluation rules.
    conflict_resolution: >
      If this document and resources/document-set-audit.md disagree on Mode F
      procedure, resources/document-set-audit.md wins on composition and gates.
  authoritative_for:
    - phase execution order
    - mode output shapes
    - frontmatter manifest handling during workflow
    - metadata drift handling
  related_documents:
    - path: ../SKILL.md
      relationship: entry_point_for
    - path: ./document-set-audit.md
      relationship: elaborated_by
    - path: ./evaluator-prompt.md
      relationship: elaborated_by
    - path: ./frontmatter-manifest.md
      relationship: elaborated_by
  freshness:
    owner: skill-maintainer
    expectation: Review on each skill version bump or when referenced resources change.
    last_reviewed: "2026-05-08"
  tests:
    suite: ./workflow.questions.yaml
---

# Test-Driven Documentation Workflow


## Test-driven-docs frontmatter manifest

When a document has YAML frontmatter with an `tddoc` key, treat it as the document-local manifest. It is not the full artifact store unless it uses `tests_inline` for a small document.

Use frontmatter for:

- document identity and title
- role in a document set
- audience and purpose summary
- source-of-truth and precedence boundaries
- authoritative topics and related documents
- freshness owner and review expectation
- pointers to the external question suite and latest evaluation
- compact evaluation status/hash attestation

Default precedence:

1. External question-suite files referenced by frontmatter are authoritative for full tests.
2. Frontmatter is authoritative for document identity, role, audience, source-of-truth boundary, authoritative topics, document-set membership, and artifact routing.
3. Generated evaluation files are never authoritative over the document, manifest, or test suite.
4. If frontmatter and referenced artifacts disagree, fail evaluation with a metadata-drift finding.

For the full manifest shape, use `resources/frontmatter-manifest.md` and validate with `resources/tddoc.frontmatter.schema.yaml`.

## Metadata drift

Treat each of the following as a metadata-drift finding that fails evaluation and requires re-derivation or re-evaluation before continuing:

- Referenced `tests.suite` file does not exist on disk.
- Referenced `evaluation.latest` file does not exist on disk.
- `evaluation.document_hash` does not match the current document body hash.
- A path listed in `related_documents[].path` does not exist on disk.

When metadata drift is detected: report the finding, fall back to deriving a minimal test suite or re-running evaluation as applicable, and flag the frontmatter as stale in the fix plan.

## Phase 1 — Document contract

Before drafting, establish a contract. If the document already has test-driven-docs frontmatter, use it as the starting contract manifest and check it for gaps or drift. Load the referenced `tests.suite` as the starting test suite — do not re-derive from scratch — but still run the suite expansion pass (see Suite expansion below) to surface any coverage gaps or logically-implied tests the suite may be missing. Do not treat any `evaluation.status` stamp in frontmatter as proof the document currently passes; evaluation stamps are attestations of a prior run only. If the user supplied enough context, infer a reasonable first version and label assumptions. If not, ask only the questions needed to avoid wasted work.

Minimum contract:

```yaml
document_contract:
  title: ""
  audience:
    primary: []
    secondary: []
  purpose: ""
  non_goals: []
  expected_reader_actions: []
  source_of_truth_boundary: ""
  freshness_expectation: ""
  success_criteria: []
```

Resolve these source-of-truth questions:

- Is this document authoritative, explanatory, illustrative, or derived?
- What system or artifact wins when this document conflicts with another source?
- Who owns updates?
- What freshness or review cadence is expected?
- What is explicitly out of scope?

## Phase 2 — Reader question inventory

Generate questions by reader intent. Default categories:

- orientation — reader understands why the document exists and whether it applies
- execution — reader knows what to do and in what order
- decisions — reader can make required choices using stated criteria
- edge cases — reader can handle plausible abnormal paths
- governance — reader understands ownership, approvals, evidence, auditability, and prohibited uses
- operations — reader can validate success, monitor behavior, recover, and escalate
- maintenance — reader understands how the document and underlying process/system are kept current

Question rules:

- Questions must be answerable from the target document or document set.
- Questions must map to reader actions, decisions, or material risks.
- Avoid vague questions such as "Is rollback explained?"
- Prefer specific questions such as "Who may initiate rollback, under what trigger conditions, and how is success validated?"
- Do not require exhaustive edge cases unless they are plausible and material.

## Phase 3 — Convert questions into documentation tests

Each material question becomes a test with expected answer properties.

```yaml
- id: rollback-001
  category: operations
  severity: critical
  reader_role: release owner
  question: "How do I roll back a failed deployment?"
  expected_answer_properties:
    - identifies who may initiate rollback
    - defines rollback trigger conditions
    - provides ordered rollback steps
    - states how rollback success is validated
    - states what to do if rollback fails
  failure_risk: "A failed deployment may remain unresolved or be rolled back unsafely."
  blocking: true
```

A test is good when an evaluator can distinguish complete, partial, missing, contradictory, and inferred answers.

## Suite expansion

When a suite is loaded (supplied by the operator, referenced via frontmatter, or just derived), run a suite expansion pass before evaluation. The goal is to ensure the audit tests the document as thoroughly as the document's own content and context demand — not merely as thoroughly as the existing suite asks.

### Per-document expansion

1. **Surface untested content** — compare the document's sections, topics, and procedures against the loaded tests; flag any content block with no corresponding test as a *suite under-coverage finding*.
2. **Derive candidate per-document tests** — using the document's `audience`, `purpose`, `authoritative_for`, existing test categories, and body, generate logically-implied questions not already in the suite. Examples: a rollback procedure with no smoke-test question, an auth document covering rotation with no revocation question, a workflow document that gained a phase without a corresponding test.

### Set-level expansion

3. **Derive candidate set-level tests** — using the set's combined audience, the inventory of authoritative topics per document, and the standard Layer-2 categories (discoverability, routing, manifest consistency, source of truth, terminology, escalation, ownership), generate reader-journey questions the set's audience requires that no current test asserts.

### Handling candidates

For all three expansion types (per-document untested content, per-document logically-implied questions, set-level reader-journey questions):

- Classify candidate-test severity using `resources/severity-calibration.md`.
- Surface candidates for operator review rather than silently appending them to the suite.
- Emit findings under fix-plan category **suite_expansion** — distinct from *per-document fixes* (correct a document's content) and *set-level fixes* (fix routing, structure, or ownership).

Suite expansion runs after suite load and before evaluation. It shapes what evaluation will examine.

## Phase 4 — Author or revise the document

Use the contract and test suite as acceptance criteria. The final document should answer tests naturally through coherent structure, not by appending a large FAQ.

Recommended operational/process/governance structure:

```markdown
# Title

## Purpose

## Audience

## Source of Truth and Precedence

## Scope and Non-Goals

## Standard Path

## Decisions and Precedence Rules

## Exceptions and Edge Cases

## Controls, Evidence, and Governance

## Validation and Observability

## Failure Handling and Escalation

## Maintenance and Review Cadence

## Open Questions
```

Use only the sections that fit the artifact.

## Phase 5 — Evaluation

Evaluate using only the supplied document(s). Do not rely on outside knowledge, common sense, or prior author intent.

Use a two-phase flow:

1. **Phase 1 — Evaluator reading pass**: use `question`, `reader_role`, the document body, and structural frontmatter fields (`id`, `document_set`, `authoritative_for`, `related_documents`, source-of-truth declarations, etc.) as evidence. Do **not** read `tddoc.tests_inline` or `tddoc.evaluation` — `tests_inline` embeds grading rubric items and `evaluation.status` records a prior verdict, both of which bias the reading pass. Do not expose or use `expected_answer_properties` or `failure_risk` during this phase.
2. **Phase 2 — Grading pass**: apply `expected_answer_properties` and `failure_risk` to assign status and complete all grading fields.

This model uses a single evaluator agent with phased instructions (soft convention) rather than two separate agent invocations.

**Design decisions:**
- Hard vs. soft separation: soft (single agent, phased instructions). Equivalent bias-reduction; lower coordination cost.
- `failure_risk` is not renamed. Schema descriptions mark it as grading-only; a rename would require updating all existing `.questions.yaml` files.
- Structural frontmatter is available in Phase 1 for metadata and manifest tests; only `tddoc.tests_inline` and `tddoc.evaluation` are excluded to prevent rubric and verdict leakage.

For each test result, produce:

- status: PASS, PARTIAL, FAIL, CONTRADICTORY, or NOT_APPLICABLE
- answer found in the document body
- supporting evidence from the document body
- missing expected answer properties
- unsupported assumptions or inferences
- operational/documentation risk
- minimal fix

A test passes only if the document gives a target reader enough information to act correctly without unstated author context.

## Phase 6 — Remediation

Recommend the smallest safe change that satisfies the failed or partial test. Identify whether the fix is:

- new section
- added paragraph
- revised precedence rule
- table row
- example
- warning/callout
- deleted or narrowed claim
- source-of-truth clarification
- new document or routing/index change

Do not rewrite the whole document when targeted changes will suffice.

## Output modes

### Mode A — Contract only

Use when the user wants to define the document before writing.

Output:

```markdown
# Document Contract

## Assumptions

## Contract

## Open Questions
```

### Mode B — Test suite only

Use when the user wants acceptance criteria/questions.

Output:

```markdown
# Documentation Acceptance Tests

## Coverage Model

## Blocking Tests

## Non-Blocking Tests

## Risks Not Covered
```

### Mode C — Author document

Use when the user wants the actual document created or revised.

Output the document, and include a short coverage note only when useful.

### Mode D — Evaluate document

Use when the user supplies a single document and wants gap analysis.

If the user supplies a test suite, evaluate against it. If the document frontmatter references a test suite or contains `tests_inline`, use that before deriving tests. If the user supplies only a document with no usable tests, derive a default test suite from the document type and apparent audience. Surface the derived suite before evaluation or label each test with "derived because ..." so the user can challenge the rubric.

Regardless of how the suite was obtained, run the **Suite expansion** pass (see Suite expansion section above) before evaluating: surface untested content and candidate tests, emit them under fix-plan category **suite_expansion**, then proceed to evaluation.

Output:

```markdown
# Documentation Evaluation

## Derived or Supplied Test Suite

## Overall Result

## Coverage Summary

## Blocking Findings

## Non-Blocking Findings

## Minimal Fix Plan

## Test-by-Test Results
```

### Mode E — Full workflow

Use when the user asks to create a single document from scratch and wants the test-driven process applied.

Output:

1. contract or frontmatter manifest
2. test suite
3. authored document
4. evaluation
5. remediation if needed

Default to phase-by-phase delivery for real documents. Skip that pacing only if the user explicitly asks for everything at once or the document is small enough for a single readable response.

### Mode F — Document-set audit

Use when the user supplies multiple related documents and wants to know whether the set serves its readers.

Mode F always includes:

1. Mode D/E-style per-document evaluation for each document.
2. Set-level evaluation across the corpus.

See `resources/document-set-audit.md` for the detailed procedure, output shape, and gates.
