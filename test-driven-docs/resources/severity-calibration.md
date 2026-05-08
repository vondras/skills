---
tddoc:
  version: 1
  artifact_type: document
  id: test-driven-docs-severity-calibration
  document_set: test-driven-docs-skill-docset
  role_in_set: reference
  title: Severity Calibration
  audience:
    primary:
      - test writer
      - evaluator
  purpose: >
    Provide concrete examples for each severity level (critical, high, medium,
    low) so that test writers classify tests consistently and evaluators apply
    the correct blocking threshold.
  non_goals:
    - Define the full evaluation procedure (that is resources/evaluator-prompt.md).
    - Define status definitions (that is resources/evaluator-prompt.md).
  expected_reader_actions:
    - Classify a new test as critical, high, medium, or low using the examples.
    - Determine whether a finding should block release or generate a warning.
  source_of_truth:
    authority: authoritative_for_severity_calibration
    precedence:
      - This document is authoritative for severity classification examples and the blocking threshold.
      - resources/evaluator-prompt.md is authoritative for overall-status rules and when blocking applies.
    conflict_resolution: >
      If this document and resources/evaluator-prompt.md disagree on whether a
      finding blocks, resources/evaluator-prompt.md wins on the gate rule;
      this document wins on the example-based classification.
  authoritative_for:
    - severity classification examples
    - blocking threshold guidance
  related_documents:
    - path: ./evaluator-prompt.md
      relationship: used_by
    - path: ../SKILL.md
      relationship: entry_point_for
  freshness:
    owner: skill-maintainer
    expectation: Review on each skill version bump or when referenced resources change.
    last_reviewed: "2026-05-08"
  tests:
    suite: ./severity-calibration.questions.yaml
---

# Severity Calibration

Use severity to limit edge-case explosion. Critical/high findings should usually block release or merge. Medium/low findings normally produce warnings unless the user defines stricter gates.

## Critical

Wrong or missing information can cause production, compliance, financial, security, safety, or governance harm.

Examples:

- rollback authority missing in a production deployment runbook
- retention requirement ambiguous in a compliance document
- access-control/prohibited-use rule contradicted across docs
- incident escalation path missing for a customer-impacting system
- source-of-truth conflict on a value readers will act on, such as a rate limit, deadline, retention window, or approval authority

## High

Wrong or missing information can cause blocked delivery, substantial rework, bad operational behavior, repeated escalation, or durable drift.

Examples:

- owner or escalation route missing
- standard path documented but exception path omitted for a common failure mode
- runbook gives validation steps but no failure interpretation
- document set has no routing/index for common reader tasks
- duplicated factual values likely to drift across docs

## Medium

Wrong or missing information can cause local confusion, inconsistent execution, minor rework, or avoidable support questions.

Examples:

- uncommon edge case lacks an example
- terminology is inconsistent but context usually disambiguates it
- maintenance cadence is implied but not explicit
- troubleshooting section lacks examples for non-critical warnings

## Low

Wrong or missing information mainly affects polish, convenience, or discoverability.

Examples:

- glossary term undefined but inferable
- optional example missing
- heading names are slightly inconsistent
- minor navigation improvement would help but current flow is usable
