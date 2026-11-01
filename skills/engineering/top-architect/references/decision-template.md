# Architecture decision template

Use this template for an ADR, design memo, or a decision that deserves a durable record. Keep only sections that change the decision.

## Decision

- **Status:** proposed / accepted / superseded
- **Decision:** one sentence with the chosen boundary or action
- **Owner:** person or team responsible for follow-through
- **Date:** when the decision was made
- **Review trigger:** the observable fact that should cause reconsideration

## Outcome and constraints

- **User or business outcome:**
- **Users and affected systems:**
- **Success measures:** metric, target, scope, unit, and time window
- **Hard constraints:** deadline, budget, SLO, compliance, data, contracts, team, or platform limits
- **Non-goals:**
- **Known assumptions:** fact / estimate / hypothesis

## Context and model

Describe only the relevant user journey, data lifecycle, ownership, interfaces, runtime path, and failure boundaries. Link to a diagram only when it removes ambiguity.

## Options

| Option | Value | Complexity | Risk | Cost/operability | Migration | When it wins |
| --- | --- | --- | --- | --- | --- | --- |
| A |  |  |  |  |  |  |
| B |  |  |  |  |  |  |

State the chosen option, the rejected alternatives, and which facts would change the choice.

## Evidence plan

| Assumption or claim | Why it matters | Smallest useful check | Pass condition | What it cannot prove |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Delivery and evolution

1. First releasable slice and its acceptance condition.
2. Boundary or contract needed for the next slice.
3. Migration, compatibility, rollout, rollback, and data-correction path.
4. Observability, support ownership, and user adoption plan.
5. Technical debt, repayment trigger, and stop condition.

## Consequences

- **Positive:**
- **Negative or deferred:**
- **Risks:** cause → impact → mitigation → owner
- **Open decisions:** question → decision owner → unblock condition
