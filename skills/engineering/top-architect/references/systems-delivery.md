# Systems and reliable delivery

Use for consequential architecture, AI/Agent execution, stateful/distributed workflows, migration, or operating delivery. Relate choices to the product promise and domain constraints. Apply relevant sections; a single-process tool may need only ownership, failure handling, and reproducible delivery.

## Domain, boundaries, and state

- Identify domain terms, business invariants, authoritative records, state transitions, and who can authorize each transition. Model expiry, cancellation, correction, reconciliation, and partial completion where needed.
- Choose module, process, service, and deployment boundaries separately. Use coupling, ownership, failure containment, scaling, trust, and change cadence to justify separation. A bounded context can begin as a module.
- Give public APIs, events, schemas, packages, and tools explicit contracts: versioning, compatibility, ordering, cancellation, errors, and ownership.
- Define data collection, classification, access, provenance, retention, deletion, and recovery. Keep tenant and trust boundaries visible; derive controls from actual data and actions.
- State consistency requirements per business operation. For remote effects, account for duplicate delivery, idempotency, races, deadlines, backpressure, bounded retries, and reconciliation or compensation. An HTTP timeout does not prove the remote action never happened.

## Runtime quality and economics

Translate product acceptance into workload and quality budgets: active users/tasks, arrival pattern, concurrency, data volume, latency percentiles, availability, error severity, resource bounds, and cost per accepted unit. Record assumptions and baseline.

Find the critical path, scarce resource, and single points of failure. Design timeouts, bounded queues, admission control, isolation, degradation, and observability where justified. Capacity estimates and mature patterns are priors; confirm consequential claims with comparable measurement.

For memory/CPU, establish executable/version, build mode, process scope, workload, lifecycle point, sampling window, sample count, and metric. Distinguish startup, steady-state retention, per-session growth, transient peaks, native memory, and process-tree pressure. Fix ownership and unnecessary work before local tuning. JS/TS detail belongs in [javascript-runtime-performance.md](javascript-runtime-performance.md).

## AI and Agent systems

Separate model reasoning from orchestration, authoritative state, authorization/policy, data, and execution. The model may propose an action; the trusted execution path enforces the capability contract.

Define allowed actions, permissions, input/output schema, tenant/session scope, deadlines, idempotency, cancellation, verification, human handoff, and audit. Match autonomy to action severity and reversibility. Treat model output, retrieved content, and remote UI/data according to trust level; a tool connection or sandbox is not a grant of business authority.

Evaluate representative complete tasks: ambiguity, stale state, partial failure, intervention, and recovery. Report accepted completion, severe-error rate, human effort, end-to-end latency, and full cost. Compare deterministic automation, assistance, and autonomy while the choice is open. Surface uncertainty and use calibrated confidence thresholds. Keep an accountable fallback for unsupported cases.

Version prompts, models, tools, schemas, retrieval sources, and eval cases when they affect reproducibility. Use the formal entrypoint and target environment for acceptance. A debug harness, fixed fixture, mock, or lower-layer check proves only its own scope.

## First useful slice and rollout

Deliver a complete path from input to accepted result with a narrow segment and manageable failure exposure. Name dependencies, owners, team capacity, skills, acceptance, and remaining manual work. Create platform boundaries when demonstrated consumers need them.

For existing users/data, specify compatibility, sequencing, migration/rehearsal, rollout cohorts, detection, abort/rollback, and data correction. A code rollback may not reverse writes or external effects. Keep schema, migration, service deployment, and consumer adoption as distinct gates under the project's actual process.

For libraries, CLIs, and frameworks, verify source/build outputs, package contents, published dependencies, installation, and consumer contracts independently. Keep one toolchain authority per concern and a reproducible contributor path. See [framework-source-benchmarks.md](framework-source-benchmarks.md) and [cli-architecture.md](cli-architecture.md) when those branches apply.

## Operate the promise

Specify owners and observable signals for the journey, dependencies, errors, cost, and capacity. Define who handles incidents, stuck/duplicate work, support, and recovery when the author is unavailable. Use runbooks or automation proportional to actual operating risk.

Verify onboarding and adoption as well as availability: integrations work, intended users complete the journey, operators diagnose failures, and outcomes are measured against the baseline. Hand off evidence, limits, and next actions. A passing test or deployed endpoint does not establish user value.

Review after a bounded period or observable trigger: outcome fails to improve, severity/support load exceeds tolerance, cost crosses budget, assumptions change, or maintenance exceeds capacity. Give debt a consequence, owner, and repayment/retirement trigger. Reducing scope or retiring a system is a valid engineering outcome.
