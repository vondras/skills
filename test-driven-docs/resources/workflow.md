# Acceptance-Test-Driven Documentation Workflow


## ATDD frontmatter manifest

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

## Phase 1 — Document contract

Before drafting, establish a contract. If the document already has ATDD frontmatter, use it as the starting contract manifest and check it for gaps or drift. If the user supplied enough context, infer a reasonable first version and label assumptions. If not, ask only the questions needed to avoid wasted work.

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

For each test, produce:

- status: PASS, PARTIAL, FAIL, CONTRADICTORY, or NOT_APPLICABLE
- answer found in the document(s)
- supporting evidence from the document(s)
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
