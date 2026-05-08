---
name: test-driven-docs
description: Use when a user wants to create, revise, or evaluate operational documentation by defining the reader questions it must answer and testing the document against those questions. Best for runbooks, ADRs, architecture docs, governance/process docs, implementation plans, onboarding docs, repo instructions, and multi-document audits where completeness, source-of-truth boundaries, or cross-document contradictions matter.
---

# Acceptance-Test-Driven Documentation

## Purpose

Use this skill to make documentation testable. A document is complete only when the target reader can answer the declared questions, make the intended decisions, and avoid known failure modes using the document itself.

The basic workflow is:

1. Define the document contract.
2. Define the reader questions.
3. Convert questions into acceptance tests.
4. Author or revise against those tests.
5. Evaluate with evidence from the document only.
6. Return gaps, risks, and minimal fixes.

## Use this skill when

- creating or revising documentation where ambiguity creates operational, delivery, compliance, governance, or maintenance risk
- reviewing whether a document answers its intended reader questions
- generating documentation acceptance criteria
- creating or hardening runbooks, ADRs, architecture docs, governance/process docs, implementation plans, onboarding docs, or repo/agent instructions
- auditing a related documentation set for coverage, routing, source-of-truth conflicts, duplication, drift, and contradictions

Do not force the full workflow onto short informal notes, creative writing, or lightweight edits unless the user asks for coverage/evaluation or the document has clear correctness risk.

## Mode selection

Pick the smallest mode that satisfies the user request.

- **Mode A — Contract only**: scope the document before writing.
- **Mode B — Test suite only**: produce reader questions / acceptance criteria.
- **Mode C — Author document**: draft or revise the document against known intent.
- **Mode D — Evaluate document**: evaluate a single supplied document.
- **Mode E — Full workflow**: contract → tests → draft → evaluation → fixes for one document.
- **Mode F — Document-set audit**: evaluate multiple related documents as a documentation system.

Detailed mode behavior lives in `resources/workflow.md`. Frontmatter manifest behavior lives in `resources/frontmatter-manifest.md`.

## Critical invariant for Mode F

Mode F does **not** replace single-document evaluation. It composes it.

A document-set audit must run two layers:

1. **Per-document evaluation** — run Mode D/E-style evaluation against each document in the set, using its own contract/tests when supplied or a derived minimal suite when not supplied.
2. **Set-level evaluation** — evaluate the corpus for coverage, routing, precedence, terminology consistency, contradictions, duplication, stale references, and source-of-truth boundaries.

A document set passes only if every blocking per-document critical/high test passes, every blocking set-level critical/high test passes, and no blocking cross-document contradiction remains.

More detail is in `resources/document-set-audit.md`.

## Operating principles

- Treat the document or document set as an artifact with acceptance criteria.
- Use YAML frontmatter as the document-local ATDD manifest when the document needs durable routing, ownership, source-of-truth, or evaluation metadata.
- Keep full question suites and generated evaluations external by default; frontmatter should point to them unless the document is small enough for inline tests.
- Define audience, purpose, non-goals, source-of-truth boundaries, and expected reader actions before authoring.
- Organize tests by reader intent, not by planned document section.
- Convert important questions into expected answer properties.
- Require evidence from the document for every evaluation pass.
- Mark unsupported inference as a failure or partial, not a pass.
- Block on critical/high gaps unless the user explicitly accepts the risk.
- Prefer the smallest safe documentation change that closes the failed test.
- Preserve coherent document structure; do not degrade the document into a FAQ dump.

## Artifact files

Use these resources as needed:

- `resources/workflow.md` — full workflow and output modes
- `resources/document-set-audit.md` — Mode F procedure and gates
- `resources/evaluator-prompt.md` — evidence-bound evaluator instructions
- `resources/authoring-template.md` — default operational document template
- `resources/severity-calibration.md` — examples for critical/high/medium/low classification
- `resources/frontmatter-manifest.md` — YAML frontmatter manifest rules, precedence, and examples
- `resources/contract.schema.yaml` — contract schema
- `resources/questions.schema.yaml` — question/test-suite schema; supports `document` or `document_set`
- `resources/evaluation.schema.yaml` — evaluation-result schema; supports single-document and document-set outputs
- `resources/tddoc.frontmatter.schema.yaml` — document-local ATDD frontmatter manifest schema
- `scripts/validate_artifacts.py` — deterministic YAML/schema/count validation helper

## Interaction rules

- If the user gives a document and asks for review, evaluate before rewriting.
- If the user gives only an idea, start with a contract and tests.
- If the user supplies only a document and no test suite, first inspect any ATDD frontmatter for a referenced suite or inline tests; otherwise derive a test suite and label it as derived before evaluating.
- If the user supplies multiple documents, use Mode F unless they explicitly ask to evaluate only one document. Use ATDD frontmatter to establish each document's role, authority, routing, and local tests when present.
- If evaluating something authored in the same session, evaluate adversarially and do not give credit for prior discussion or intent not present in the final document.
- If the user asks for files, provide complete file contents or an updated package.
- If the user asks for CI implementation, use deterministic checks where possible and mark LLM-based judgment as non-deterministic unless constrained by fixed model/version/settings.
