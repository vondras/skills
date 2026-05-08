---
tddoc:
  version: 1
  artifact_type: document
  id: {{ id }}
  title: {{ title }}
  role_in_set: {{ role_in_set }}
  document_set: {{ document_set }}
  audience:
    primary:
      - {{ primary_audience }}
    secondary: []
  purpose: >
    {{ purpose }}
  non_goals: []
  expected_reader_actions: []
  source_of_truth:
    authority: {{ authority }}
    precedence: []
    conflict_resolution: >
      {{ conflict_resolution }}
  authoritative_for: []
  related_documents: []
  freshness:
    expectation: {{ freshness_expectation }}
    owner: {{ owner }}
  tests:
    suite: ./{{ id }}.questions.yaml
    blocking: []
  evaluation:
    latest: ./{{ id }}.eval.yaml
    status: not_evaluated
---

# {{ title }}

## Purpose

State why this document exists and what problem it solves.

## Audience

Identify the primary and secondary readers. Be explicit about who should not use this document as authoritative guidance.

## Source of Truth and Precedence

State whether this document is authoritative, explanatory, illustrative, or derived.

Define what wins if this document conflicts with another system or artifact.

## Scope and Non-Goals

### In Scope

-

### Out of Scope

-

## Standard Path

Describe the normal path in ordered steps.

## Decisions and Precedence Rules

Describe required decisions, decision criteria, and conflict resolution rules.

## Exceptions and Edge Cases

Describe plausible abnormal paths that materially affect reader action or risk.

## Controls, Evidence, and Governance

Describe ownership, required approvals, audit evidence, prohibited actions, and review expectations.

## Validation and Observability

Describe how the reader knows the action/process/system worked.

## Failure Handling and Escalation

Describe failure triggers, rollback/recovery, escalation paths, and ownership.

## Maintenance and Review Cadence

Describe who owns this document, when it must be reviewed, and what events trigger updates.

## Open Questions

List unresolved questions explicitly. Do not hide known ambiguity in confident prose.
