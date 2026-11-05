# AI engineering and delivery

Use when designing, reviewing, or delivering AI applications, knowledge-assisted products, Skills, Agents, or digital employees. Business value and product scope remain the starting point; this reference turns them into AI-specific design, artifacts, and operating evidence. Apply the relevant sections rather than prescribing a stack.

## Identify the delivered unit

Clarify the project's vocabulary and existing implementation. These are decision boundaries, not a mandatory sequence of products or separately deployed services:

| Unit | Design responsibility | Delivery and acceptance |
| --- | --- | --- |
| Skill | Package reusable domain methods, instructions, context and, when needed, scripts/resources. Define when it applies, inputs/preconditions, dependencies, expected result, and failure/escalation behavior. | A discoverable, versioned capability that representative tasks can select and use correctly, with examples/evals and dependency/compatibility evidence. |
| Agent | Interpret a bounded goal, choose capabilities and actions, maintain task state, use tools, verify results, and recover or hand off. Decide where model reasoning improves on fixed execution. | A runnable execution loop/harness with scoped state and authority, observable traces, budgets, verified task outcomes, and recovery evidence. |
| Digital employee | An operational product organized around explicit business duties. Define who assigns work, receives results, supervises exceptions, and owns service quality. It may combine Skills, Agents, deterministic workflows, and people. | A service integrated with real intake, business systems, task handover, workload/service limits, escalation and support, measured on sustained accepted business outcomes. |

Agree on what “digital employee” means locally: a role's task set, operating responsibility, and service interface. A persona or job title alone leaves these undecided. Start with a bounded duty and expand only when adoption, quality, and operating capacity support it.

The [Agent Skills format](https://agentskills.io/home) supports instructions with optional scripts, references, and assets loaded as needed. When interoperability matters, check the current specification and target client's actual support. Keep tool schemas, application contracts, skill packaging, and permissions distinct; a skill definition does not itself grant execution rights.

## Choose the smallest useful automation

Compare existing software, deterministic workflow, assistive generation/recommendation, bounded Agent execution, and ongoing role-based service where credible. Use error severity, ambiguity, frequency, workflow variability, latency, full handling cost, and human control to choose. A fixed task may need only a script; an adaptive task may need a model loop; ongoing business responsibility adds operating obligations beyond either.

Trace one job through intake → context/data → capability selection → action → independent acceptance → handoff/support. Define eligible inputs, authoritative records, required outputs, completion evidence, excluded cases, permissions, budget, and terminal states. Preserve the current application and runtime unless they fail a concrete requirement.

## Model, context, data, and tools

- **Model fit:** select by representative quality, modalities, structured/tool behavior, latency, context needs, cost, data handling and availability. Verify changing capabilities/prices from current primary sources or the actual environment. Compare alternatives under the same tasks and total-cost assumptions; use routing/fallback only for an observed need and test its quality/permission behavior.
- **Context and memory:** separate instructions, task state, domain knowledge, conversation history, and durable memory. Define scope, authority, lifetime, provenance, retrieval, compaction and invalidation where relevant. Persist facts or preferences only with the appropriate ownership/authorization. A larger context window does not establish relevant or trustworthy context.
- **Knowledge and retrieval:** when external knowledge is needed, compare direct authorized access, retrieval, and existing structured APIs. Define source ownership/freshness, access filtering, citation/verification, and unknown handling. Evaluate retrieval failures separately from reasoning. Introduce a vector store or other new indexing system only when existing access cannot serve the demonstrated query/workload.
- **Tool integration:** prefer supported APIs or deterministic execution for stable actions; use GUI/computer use when required by the workflow. Define typed inputs/results, identity, side effects, deadlines, idempotency, error/retry/cancellation behavior, and verification. Evaluate tool descriptions and selection as well as implementation. MCP or another transport is an integration choice, not an architecture or authorization guarantee.

When capability gaps persist, compare prompt/context/tool improvements, retrieval, model substitution and fine-tuning against representative error evidence, authorized data, evaluation quality and operating cost. For managed APIs versus self-hosted inference, consider data locality, latency/capacity, reliability, hardware/operations and exit cost. Use existing model access and deployment paths until a measured constraint justifies a new one; neither model training nor a model gateway is a default prerequisite.

Keep retrieved content, remote interfaces, and generated plans at their actual trust level. Enforce authorization and invariants in the trusted execution path. A model choice, fallback, delegated Agent, or Skill change must preserve those limits.

## Skill lifecycle

1. Identify a repeatable domain task and its real examples, exceptions, evidence sources, and current operator method. Decide what belongs in procedural instructions versus reference knowledge, authoritative business rules/configuration, or deterministic code. Distill necessary knowledge; collect only authorized context.
2. Define discovery/activation boundaries and the capability contract. Use the project's packaging standard, progressive disclosure, and existing scripts/tools; avoid adding a wrapper for every command.
3. Test intended invocation, neighboring tasks that should not activate it, incomplete inputs, misleading context, dependency failure, and result verification. Check whether different supported callers can actually use it when portability is promised.
4. Version the instructions and relevant resources/dependencies. Review changes, run representative regressions, release through the existing channel, observe failures, and retire or repair stale capabilities.

Judge a Skill by correct selection, execution/decision quality, accepted results, and maintenance cost. Skill count and successful installation do not establish usefulness. If traces are used to propose new skills or improve them, define provenance, data rights, review/eval, rollout, and rollback; production feedback is not an automatic permission to rewrite operating rules.

## Agent execution and collaboration

Choose a loop and state model suited to the job: planning/actions, observation, verification, waiting, retry, cancellation, resume, and terminal outcomes. A prescribed graph, Planner/Executor split, or multi-Agent team is an option, not the default deliverable. Make model decisions observable while orchestration owns bounded execution.

Define task/session identity, state persistence, concurrency/resource ownership, deadlines, iteration/token/tool budgets, progress evidence, and result acceptance. Detect repeated actions, stalled progress and goal drift, with explicit stop/replan/escalation conditions. On interruption or ambiguous remote effects, reconcile authoritative state before retrying. Long-running work needs a recoverable checkpoint and an owner for stuck work.

Add multiple Agents only for a current advantage such as independent expertise, parallel work, context separation, or trust isolation that exceeds coordination overhead. Specify delegation inputs/results, shared-state ownership, task dependencies, cancellation, conflicting results, and one accountable final acceptance path. Delegation cannot widen permissions; more agents can amplify errors and cost.

## Digital employee integration and operation

Start from one business duty. Record eligible tasks, trigger/intake channel, assignment/priority, required systems and identity, operating/service coverage, workload and queue limits, output recipients, acceptance, and exclusions. Distinguish the business owner who sets rules, the operator who handles exceptions, and the engineering owner who maintains execution.

Design the normal work cycle and the exception cycle: acquire a task, obtain authorized context, act or propose, submit evidence/result, update the authoritative record, and hand over unresolved work. Humans need a usable review surface, enough evidence to decide, explicit handoff reasons, and the ability to pause/revoke or take over. Transfer task ownership explicitly so a person and Agent cannot independently commit the same work. Define what happens during dependency outages, backlog growth, ambiguous rules, and unavailable reviewers.

Prefer a bounded pilot in an existing business workflow. Verify repeated operation across the actual workload and service period, including task handover and support; one selected chat or task completion is insufficient. Measure accepted outcomes, severe errors, correction/reopen rate, human review and handling time, waiting/backlog, end-to-end latency, full cost, and sustained use as relevant. Time saved is capacity until evidence shows a further business effect.

Separate arriving requests, eligible work, admitted tasks, accepted results, rejected/deferred cases, and backlog. Report the reasons and denominators so narrow admission cannot hide poor workflow coverage.

## Evaluation, release, and continuing improvement

Use layered evidence while keeping the end-to-end job authoritative:

| Layer | What to exercise | What success does not establish |
| --- | --- | --- |
| Model/context/retrieval | Representative inputs, grounded reasoning, source freshness/authorization, missing/irrelevant context, tool selection. | Safe execution, completed tasks, or adoption. |
| Skill | Appropriate invocation, preconditions, dependency behavior, procedure, accepted output, non-trigger cases. | Agent recovery or an operating role's service quality. |
| Agent | Complete tasks, partial effects, invalid/stale state, permissions, interruption/resume, escalation, budgets and collaboration when present. | Sustained business service or production acceptance in another environment. |
| Digital employee | Repeated intake-to-result operation, business-system reconciliation, human handoff, outages/load and ongoing support. | Broader industry applicability, job replacement, or financial impact without evidence. |

Define datasets/cases, eligible population, baseline, outcome/guardrail metrics, environment, versions, evaluator/acceptance rule, and failure taxonomy. Repeat stochastic tasks when run-to-run variation could change the decision. Include unsuccessful and abandoned attempts in denominators/costs as appropriate. Keep development cases separate from held-out or newly sampled acceptance cases when the claim depends on generalization. Calibrate model-based grading against independent evidence or human review; model self-assessment alone cannot approve consequential effects.

Release the smallest useful artifact with versioned model settings, prompts, Skills, tool contracts, relevant data/retrieval snapshot or freshness policy, runtime/configuration, eval evidence, and ownership. Verify the target runtime actually loads and uses the intended versions/configuration. Bind only the components that affect this release; reuse the repository's lockfiles, manifests, tests, and delivery chain rather than requiring a new control plane or registry.

Run offline regressions and representative integration/target-environment checks before a bounded rollout. Shadow or dry-run operation can validate decisions without exercising real effects, but record that limit. A configuration rollback may not undo writes, messages, payments, or knowledge/memory changes: define reconciliation and data correction separately. Re-evaluate consequential model, Skill, tool, prompt, data or policy changes; monitor drift, quality, cost and support after release.

When several behavior-changing components move together, compare the baseline, material individual changes, and final combination as needed to attribute gains/regressions and detect interactions. Scale the comparison to risk rather than requiring every possible combination.

Close with a runnable capability, acceptance evidence, operating owner, known limits, rollout/rollback and human handoff, plus the next expand/change/stop decision. A proposal, installed Skill, passing eval, deployed Agent, and adopted digital employee service are distinct delivery states.
