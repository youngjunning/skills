# Business, product, and architecture decision

Use for a requested ADR, decision memo, or durable project decision. Retain only fields that affect this choice. Place it in the project's existing location.

## Decision and status

Decision or provisional recommendation, owner, date, status, next decision, and observable review trigger. State the evidence most likely to reverse the recommendation.

## Business problem and product promise

- Target user/segment and workflow; beneficiary, buyer/sponsor, approver, and operator when different.
- Observed problem and current alternative; source and limits of the evidence.
- Value mechanism and binding constraint: money, time/capacity, risk, quality, or another explicit outcome.
- First complete user journey, accepted result, exception/recovery path, and adoption or integration barrier.
- Scope/exclusions, deadline, budget/team capacity, domain rules, and existing commitments.
- Primary outcome: baseline, target (measured or proposed), denominator, time window, evidence source; relevant guardrails.
- Critical assumptions and unknowns. For a narrow technical ADR, summarize the established business/product context rather than reopening it.

## Options and system consequences

Compare viable options while the choice is open, including existing/manual/buy/defer paths when credible.

| Option | User/business effect | Product scope and adoption | Contracts and failure behavior | Total cost and team fit | Evidence and uncertainty |
| --- | --- | --- | --- | --- | --- |
| A | | | | | |
| B | | | | | |

Describe domain invariants, authoritative state, data lifecycle, boundaries, and interfaces at the needed depth. State the chosen option, opportunity cost, rejected alternatives, and costs accepted.

## Evidence and next decision

| Claim or assumption | Smallest useful check | Baseline/source | Pass/change/stop condition | Limits | Owner/timebox |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Use verified inputs for economics or show missing variables. Evaluate complete accepted outcomes, including human work and unsuccessful attempts. Keep proposed targets and expected benefits distinct from results.

## Delivery and accountability

First useful slice, dependencies and sequencing, acceptance owner/evidence, rollout boundary, migration/compatibility, rollback and data correction, observability, support, and adoption path. Match commitments to available capacity. Link to existing plans rather than duplicating them.

Track separately: implementation/tests, artifact/publication/deployment, target-environment acceptance, actual adoption, and outcome improvement. Record residual risks, operational cost/debt owner, recovery path, and the trigger for expand/change/stop.
