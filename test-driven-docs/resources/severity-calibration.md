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
