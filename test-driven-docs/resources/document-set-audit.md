---
tddoc:
  version: 1
  artifact_type: document
  id: test-driven-docs-document-set-audit
  document_set: test-driven-docs-skill-docset
  role_in_set: reference
  title: Mode F — Document-Set Audit
  audience:
    primary:
      - skill operator
  purpose: >
    Define the required composition, procedure, gate logic, and output shape for
    Mode F document-set audits so that the skill operator can run a complete and
    correct set-level evaluation.
  non_goals:
    - Define the general six-phase workflow (that is resources/workflow.md).
    - Define evidence-bound evaluation rules for individual documents (that is resources/evaluator-prompt.md).
    - Define mode selection criteria (that is SKILL.md).
  expected_reader_actions:
    - Inventory the document set and assign roles.
    - Run per-document evaluation for each document in the set.
    - Build and run the set-level test suite.
    - Apply the gate logic to determine overall pass/fail.
    - Produce output in the prescribed shape.
  source_of_truth:
    authority: authoritative_for_mode_f
    precedence:
      - This document is authoritative for Mode F composition, procedure, and gate logic.
      - resources/workflow.md is authoritative for per-phase procedure for Modes A–E.
      - resources/evaluator-prompt.md is authoritative for evidence-bound evaluation rules applied per document.
    conflict_resolution: >
      If resources/workflow.md and this document disagree on Mode F procedure,
      this document wins.
  authoritative_for:
    - Mode F composition rules
    - document-set audit procedure
    - Mode F gate logic
    - Mode F output shape
  related_documents:
    - path: ../SKILL.md
      relationship: entry_point_for
    - path: ./workflow.md
      relationship: extends
    - path: ./evaluator-prompt.md
      relationship: uses
    - path: ./frontmatter-manifest.md
      relationship: uses
  freshness:
    owner: skill-maintainer
    expectation: Review on each skill version bump or when referenced resources change.
    last_reviewed: "2026-05-08"
  tests:
    suite: ./document-set-audit.questions.yaml
---

# Mode F — Document-Set Audit

A document-set audit evaluates a collection of related docs as a documentation system. It must not collapse the set into one big context blob and ask whether the answer exists somewhere.

## Required composition

Mode F is:

```text
Mode F = per-document Mode E/D evaluation for each document + set-level audit
```

The two layers answer different questions:

1. **Per-document evaluation** — Can each document answer the questions it individually claims or needs to answer?
2. **Set-level evaluation** — Can the document set function coherently for a reader moving across documents?

A corpus-level answer does not rescue a document that is expected to be independently complete. If `runbook.md` omits rollback but `operations-guide.md` contains rollback, the set may partially cover rollback, but `runbook.md` still fails its local rollback test unless it clearly routes to the authoritative location.

## Procedure

### 1. Inventory the set

For each document, identify:

- document name
- test-driven-docs frontmatter manifest, if present
- role in the set: entry point, runbook, reference, ADR, glossary, policy, tutorial, deep-dive, index, etc.
- apparent or declared audience
- topics it claims authority for via `authoritative_for`
- topics it appears to own but does not declare
- topics it references but does not own
- related documents declared in frontmatter

### 2. Run per-document evaluation

For each document:

- Use the document's supplied contract/tests when present.
- If the document has test-driven-docs frontmatter, use referenced `tests.suite` or `tests_inline` before deriving tests.
- If no tests exist, derive a minimal suite from frontmatter, title, purpose, apparent audience, headings, and role in the set.
- Label derived tests as derived.
- **Run the suite expansion pass** (see `resources/workflow.md` Suite expansion) before evaluating: surface untested content sections and derive per-document candidate tests implied by the document's audience, purpose, authoritative_for, and body. Emit candidates under fix-plan category **suite_expansion**.
- Evaluate using the same evidence rules as Mode D/E.
- Do not give credit for information in another document unless this document clearly routes to that other document as authoritative for the question.

### 3. Build the set-level test suite

Derive candidate set-level tests using the following procedure. Do not start from a blank rubric; generate questions from the inputs already produced in Step 1.

**Step 3a — Establish derivation inputs**

Collect from the Step 1 inventory:

- The combined declared audience across all documents in the set.
- The authoritative-topic map: for each topic declared or apparent, which document owns it?
- The routing map: which documents refer to which others, and for what purpose?
- Undeclared but apparent topics that no document claims.

**Step 3b — Generate per-category candidate tests**

For each standard Layer-2 category, derive at least one candidate test from the Step 3a inputs:

- **discoverability** — using only document names, titles, and opening purpose statements, can a reader new to the set identify which document to consult for a given task — without a separate index or prior knowledge of the layout?
- **reader routing** — do documents contain explicit cross-references and routing signals that guide readers once they are in the right place?
- **manifest consistency** — do frontmatter IDs, document-set membership, related-doc links, and referenced artifacts line up?
- **source-of-truth boundaries** — which doc/system is authoritative for each topic? Are there topics on the authoritative-topic map with no declared owner?
- **cross-document contradictions** — do any documents assert conflicting factual or procedural claims?
- **duplication and drift risk** — is the same fact repeated in multiple places?
- **terminology consistency** — is the same concept named consistently across the set?
- **coverage gaps** — does the combined audience require any reader questions that no test currently asserts? For each gap, identify which document should own the answer.
- **stale references** — links, version names, ownership, dates, process names
- **escalation and ownership** — can a reader determine who to escalate to for each topic area?

**Step 3c — Add audience-specific candidate tests**

For each declared audience segment across the set, generate at least one reader-journey question: starting from their entry point, can they complete their primary task using only the documents, explicit routing signals, and authoritative claims?

**Step 3d — Classify severity and surface for review**

- Classify each candidate test using `resources/severity-calibration.md`.
- Surface candidate tests under fix-plan category **suite_expansion** for operator review before running set-level evaluation.

Each finalized set-level test should declare `expected_documents` or `acceptable_documents: any`.

### 4. Run set-level evaluation

Evaluate the full corpus for the set-level tests. Record:

- `found_in`: which docs answer the test, and to what extent
- `expected_in`: which docs were expected to answer it
- `cross_document_findings`: contradictions, duplication, drift, routing gaps, and missing authoritative source issues

A set-level test passes only if the reader can reasonably find the right document and know it is authoritative.

### 5. Consolidate the fix plan

Separate fixes into:

- **suite_expansion** — candidate tests surfaced during the expansion pass (per-document or set-level) that the operator should add to the suite or consciously discard; distinct from content fixes
- **per-document fixes** — a specific doc is incomplete or ambiguous
- **cross-document fixes** — contradictions, duplicated facts, terminology drift, or precedence conflicts
- **set-level fixes** — missing doc, missing ownership model, or source-of-truth map; for discoverability failures, prefer renaming a document, improving its title or purpose statement, or adding targeted cross-references over creating a new routing or index document

## Gate logic

Mode F overall status is `fail` if any of these are true:

- any per-document blocking critical/high test is not PASS
- any set-level blocking critical/high test is not PASS
- any blocking cross-document contradiction exists
- no document is authoritative for a critical/high reader action
- frontmatter declares conflicting authority or stale/missing artifact references that affect critical/high tests

Mode F may return `pass_with_warnings` only when all blocking critical/high tests pass and all remaining issues are medium/low or non-blocking.

Mode F returns `pass` only when all per-document and set-level tests pass or non-passing tests are legitimately NOT_APPLICABLE.

## Output shape

```yaml
evaluation:
  artifact_type: document_set
  document_set:
    - "doc-a.md"
    - "doc-b.md"
  overall_status: fail

  per_document_evaluations:
    - document: "doc-a.md"
      overall_status: fail
      summary:
        total: 3
        passed: 2
        partial: 1
        failed: 0
        contradictory: 0
        not_applicable: 0
      results: []

  set_level_evaluation:
    summary:
      total: 4
      passed: 2
      partial: 1
      failed: 1
      contradictory: 1
      not_applicable: 0
    results: []
    cross_document_findings: []

  consolidated_fix_plan:
    - target: "doc-a.md"
      kind: suite_expansion
      reason: "Rollback section has no test exercising trigger conditions or success validation."
      fix: "Add test: 'Under what conditions may rollback be initiated, and how is success validated?'"
    - target: "doc-a.md"
      kind: per_document
      reason: "Local rollback guidance missing."
      fix: "Add rollback authority, trigger conditions, validation, and escalation."
    - target: "docs-index.md"
      kind: set_level
      reason: "Reader routing unclear."
      fix: "Add routing table mapping tasks to authoritative documents."
```
