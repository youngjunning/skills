# Architecture review checklist

Use the checklist to find material risks, not to score a design for style. Mark each item `yes`, `no`, or `unknown`, and attach evidence for non-trivial claims.

## Problem and value

- Is the user or business outcome explicit?
- Are the current problem and the proposed solution separate?
- Are success measures quantifiable and scoped?
- Are non-goals and hard constraints visible?

## Boundaries and data

- Does each component or service have a clear responsibility and owner?
- Are interfaces, contracts, versioning, and compatibility defined?
- Is data ownership, lifecycle, consistency, retention, and sensitive data handling clear?
- Are synchronous, asynchronous, timeout, retry, idempotency, and failure boundaries explicit?

## Runtime and operations

- Are workload shape, capacity dimensions, latency, availability, and cost assumptions stated?
- Is the critical path observable and diagnosable?
- Are degraded behavior, containment, recovery, rollback, and data correction designed?
- Can the system be deployed and changed incrementally?
- Can support teams operate it without the original designers?

## Options and evidence

- Were at least two credible options considered when the decision is consequential?
- Are tradeoffs tied to the stated outcome and constraints rather than preference?
- Is the riskiest assumption tested first?
- Does each test or metric say what it proves and what it does not prove?
- Is there a clear review trigger for changing the decision?

## Delivery and people

- Is there a walking skeleton or first vertical slice?
- Does the plan fit team skills, ownership, and the deadline?
- Does the design reduce cognitive load for future maintainers?
- Are adoption, migration, training, and user experience considered?
- Is technical debt attached to an owner and repayment trigger?

## AI and Agent systems

- Are model behavior, orchestration, tools, state, policy, and data boundaries separated?
- Are tool permissions, schemas, timeouts, retries, idempotency, escalation, and auditability explicit?
- Are quality, safety, privacy, latency, cost, and recovery evaluated on representative tasks?
- Are prompts, models, tools, knowledge sources, schemas, and eval sets versioned when needed?
- Is uncertainty observable, and is there a safe degraded or human path?
