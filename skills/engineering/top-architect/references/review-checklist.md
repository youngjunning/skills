# Business, product, and architecture review

Review material consequences rather than completeness for its own sake. Select applicable questions; record evidence or unknowns. For each finding give severity, affected actor/outcome, evidence, mechanism, smallest useful fix, and verification. Retain the existing product direction unless the assignment asks to reconsider it or evidence exposes a blocking premise.

## Business and opportunity

- Who benefits, uses, pays/sponsors, approves, and operates? Where do incentives conflict?
- Is the current workflow and its actual alternative understood? Is the bottleneck supported by evidence?
- What creates value, and what could prevent value capture or internal benefit?
- Are domain rules, data access, procurement/distribution, and integration constraints reflected?
- Are material costs, exceptions, support burden, opportunity cost, and ownership included?
- Would a simpler process, existing tool, buy/partner, smaller scope, or deferral serve the outcome?

## Product and adoption

- Is there an initial segment and complete journey from trigger to accepted result?
- Does the promise address the observed job? Are essential scope and exclusions explicit?
- Can users reach first value with realistic data, onboarding, permissions, and learning?
- Are ambiguity, interruption, correction, failure, cancellation, and human recovery usable?
- Why would users switch or return? What evidence supports adoption beyond interest or demos?
- Does the metric measure the accepted outcome with a denominator, baseline/time window, and guardrails?

## Technical boundaries and data

- Do domain invariants, authoritative state, responsibilities, and owners align?
- Are module/service boundaries justified by current needs?
- Are contracts, versioning, compatibility, and consumer impact explicit?
- Are data lifecycle, rights/access, tenant separation, retention, and recovery covered where relevant?
- Do consistency, concurrency, retries, idempotency, timeouts, cancellation, and compensation protect the business operation?

## AI and runtime

- Is the delivered unit explicit: Skill, Agent execution, or an ongoing digital employee service? Are reusable knowledge, authoritative business rules and deterministic code placed appropriately?
- Do model choice, context/memory, authorized knowledge access and tool integration fit the real tasks and current environment?
- Do Skills have useful discovery boundaries, preconditions, dependencies, accepted outputs, regression cases, ownership, versioning and retirement?
- Is the Agent loop/state recoverable and bounded? When multiple Agents are proposed, is the benefit supported, with delegation, shared-state and acceptance ownership defined?
- For digital employees, are business duties, intake, workload/service limits, result recipients, human handoff, support and operating ownership defined and tested across repeated work?
- Are model reasoning, orchestration, tools, state, policy, and permissions distinct?
- Is autonomy appropriate for severity/reversibility, with bounded execution, verification, audit, and accountable recovery?
- Do representative evals cover exceptions, partial effects, intervention, and end-to-end accepted outcomes?
- Do full cost and latency include retries, abandoned attempts, human review, and rework?
- Does the AI release identify the relevant model/prompt/Skill/tool/data/runtime versions, actual loaded configuration, regression evidence, rollout, in-flight task handling and result correction?
- Are workload, capacity, resource bounds, and quality budgets supported by comparable measurements?
- Does performance work address the demonstrated bottleneck and ownership/lifecycle before micro-optimization?

## Evidence, delivery, and operation

- Were credible alternatives considered on comparable scope, quality, and time horizon?
- Is the riskiest assumption tested with a bounded check and go/change/stop condition?
- Does the first slice deliver a usable outcome within team capacity and dependencies?
- Are rollout, compatibility, migration, rollback/data correction, observability, and support owned?
- Are technical readiness, deployment, consumer acceptance, adoption, and outcome improvement reported separately?
- Is there an observable review/stop trigger and an owner for cost, debt, and ongoing operation?

For AI depth, use [ai-engineering.md](ai-engineering.md); for other technical concerns use the matching reference linked from SKILL.md. For a narrow review, a few evidenced findings are sufficient; do not manufacture a business audit or numeric score.
