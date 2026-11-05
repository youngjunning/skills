# Business and product judgment

Use for industry workflows, opportunity selection, product scope and priorities, build/buy choices, or a technical investment whose value is uncertain. Apply only lenses that could change the decision. Separate observed behavior, the user's position, external facts, and hypotheses.

## Understand how the business works

Model one transaction or workflow before generalizing to an industry:

| Lens | Evidence to seek | Consequence for a decision |
| --- | --- | --- |
| Actors and incentives | User, beneficiary, buyer, budget owner, approver, operator, partner; how each is measured. | A user saving time may not control budget; a partner may resist losing margin. |
| Value chain | Trigger → decision → work/fulfillment → acceptance/settlement → aftercare; how information, money, and responsibility move. | Improve the binding bottleneck and preserve the domain's acceptance rules. |
| Economics | Revenue mechanism or internal value, variable cost, human handling, error cost, fixed integration/operating burden, time horizon. | A narrow segment with frequent costly work can beat a broad segment with weak need. |
| Domain rules | Eligibility, inventory/capacity, pricing, entitlements, reconciliation, refunds, deadlines, audit or regulated obligations when relevant. | Make rules into explicit state, invariants, and exception paths before automating. |
| Current alternative | Existing software, manual labor, outsourcing, spreadsheet, or doing nothing. | Compare against what users actually use, including its strengths and switching cost. |
| Access and constraints | Reachable customers, procurement, integrations, data quality/rights, channel control, skills, seasonality. | Distribution or trusted data access may dominate implementation difficulty. |

Use actual workflow evidence, existing tickets/support records, operating metrics, user research, or authoritative domain material. Requests, repeated usage, observed pain, and paid commitment support different claims. Browse primary sources for changing rules, prices, competitor capabilities, or unfamiliar domain facts. Organization-specific economics comes from authorized context, not generic averages.

Describe the opportunity compactly:

> For [actor/segment] doing [job under a trigger], the current [alternative] causes [evidenced pain]. Improving [bottleneck] could create [value mechanism], subject to [critical assumption or constraint].

For internal platforms, use sponsoring teams, operational capacity, reliability, and adoption commitments. For open source, consider maintainers, contributors, downstream consumers, compatibility, and support effort. Revenue is optional; a credible value mechanism is not.

## Turn a problem into a usable promise

Trace the whole experience:

1. **Trigger and reach:** when the need arises and how intended users encounter the product.
2. **First value:** setup, data/integration, permissions, learning, and time to an accepted result.
3. **Core loop:** input → work → feedback → verified outcome; success in the user's terms.
4. **Exceptions:** incomplete data, ambiguity, interruption, failure, correction, cancellation, escalation, and who remains responsible.
5. **Repeat value:** why users return, what builds trust, and how the result fits the existing workflow.

Select a first segment using pain, frequency, reachability, ability/willingness to adopt, and serviceable delivery cost. Establish a complete narrow journey before a universal promise. State exclusions and the manual/human boundary. Include interaction, accessibility, privacy, and control where they affect that journey; product sense includes ease of use and trustworthy failure behavior.

Connect the promise to engineering requirements. For example, “an operator can correct a proposed action before it commits” implies a review state, clear diff, authority boundary, cancellation, and audit record. It does not by itself imply a new microservice.

## Prioritize and judge alternatives

Compare work on the bottleneck it affects, expected magnitude/range, evidence quality, implementation and operating cost, dependencies, and reversibility. Consider opportunity cost against the next credible use of the same team and budget. Reuse the project's prioritization method; scoring makes tradeoffs explicit but is not measured truth.

Use build, buy, partner, manual service, smaller scope, or defer when credible. For buy/partner, examine fit, integration, data control, permission model, reliability, support, lock-in, and exit cost. For build, include ongoing ownership. For bespoke requests, distinguish reusable segment need from one customer's exception; state who funds and maintains customization and what commitment would justify it.

Where strategy matters, explain positioning against the current alternative and why value could persist: workflow integration, trusted distribution, permissioned data, domain expertise, operational learning, or switching cost. Treat each as a hypothesis requiring evidence; a model wrapper, architecture diagram, or unverified “data moat” does not establish defensibility.

## Economics per accepted outcome

Choose a unit matching delivered value: completed order, reconciled invoice, resolved case, retained active account, accepted document, or an internal workflow result. Keep time horizon, currency, volume, and scope consistent.

Estimate with supplied or verified inputs; otherwise show the formula and missing variables:

```text
cost per accepted outcome =
  (all attempt costs + human review/rework + failure/support costs
   + relevant fixed operating/integration cost allocated over the period)
  / accepted outcomes in that period

incremental contribution over a period =
  attributable incremental revenue or avoided variable cost
  - incremental delivery, acquisition, support, and operating cost
```

Count retries, unsuccessful and abandoned work in costs; define independent acceptance. Separate one-time setup from recurring cost. Avoid double-counting review as both time saved and an unchanged expense. Time saved is capacity until evidence shows cost reduction, revenue, or another valued outcome. Consider error severity and tail exposure alongside averages; rare expensive failures can dominate design.

Use sensitivity ranges for variables that could reverse the choice: volume, accepted completion, intervention, usage price, integration effort, adoption/retention, or support burden. Record an observable break-even/review condition instead of invented ROI. If inputs are unavailable, propose a bounded evidence-gathering step.

## Metrics and validation

Choose a primary outcome and relevant guardrails: accepted completion with correction cost, resolution time with reopen rate, conversion with refunds, activation with repeat use, or throughput with error severity and operator load. State denominator, eligible population, time window, and source. Label proposed targets as proposals.

| Risk | Useful check | Limit |
| --- | --- | --- |
| Weak or misunderstood problem | Observe work; inspect past cases; interview through authorized channels. | Interest or complaints do not prove adoption or budget. |
| Interaction does not fit the job | Test a prototype on representative tasks, including recovery. | Usability does not prove feasibility or recurring value. |
| Hidden manual work produces the benefit | Bounded concierge/pilot trial with time and exception accounting. | A heavily assisted pilot does not prove autonomous scale. |
| Data/integrations cannot support the promise | Sample authorized data and run a narrow integration spike. | A happy path does not establish rights, coverage, or recovery. |
| Economics or adoption is uncertain | Measure accepted outcomes, full handling cost, repeat use, and commitment. | A selected pilot group may not generalize to the segment. |

Specify budget/timebox, eligible cases, baseline, acceptance, stopping condition, and the decision after the check. Keep sales commitments, contacting users, spending, production experiments, and public claims within existing authorization.

## Decision checkpoint

Conclude at the appropriate level: invest, run a bounded pilot, narrow scope/segment, use an existing solution, or stop. Tie the choice to evidence and the assumption that would reverse it. Name owners for product acceptance, business outcome, engineering operation, and next review when responsibilities differ.
