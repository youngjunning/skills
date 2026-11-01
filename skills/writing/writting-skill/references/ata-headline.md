# ATA headline writing

Use this reference only when the user wants to select topics, write, revise, audit or study an article for the top-level `ATA 头条` module. The module is a distinct fixed-position surface. Do not extend these rules to ATA's separate `推荐`、`最新` or `最热` feeds or make them a preference for all technical writing.

This reference improves how a real contribution is expressed and evaluated. It does not authorize clickbait, invented evidence, trend forcing, keyword stuffing, or claims about an undisclosed selection algorithm.

## Evidence boundary

The logged-in ATA homepage observed on 2026-09-09 displayed six numbered headline titles in a module visually separate from other article surfaces. The module did not show author, date, summary, view count, likes, comments, cover or an explanation such as `AI 推荐`.

That observation proves only the visible surface. It does not reveal whether candidates or order come from an editor, rules, a ranking model, an LLM-assisted review, an experiment, or a hybrid workflow. Keep three layers distinct:

| Layer | What may be said |
| --- | --- |
| Observation | The exact headline title, position, article page, capture time and visible article evidence |
| Inference | A content feature may help selection because it explains several headline examples better than alternatives |
| Unknown | Candidate source, model, prompt, feature weight, threshold, manual intervention and causal lift |

Use wording such as “当前六篇头条共同出现……”“这可能便于语义筛选或人工判断……”“需要跨期入选与落选对照才能确认……”. Do not write “ATA 算法偏爱……” or “这样写一定会上头条”.

## Current corpus signal

The observed six-title set repeatedly used three content shapes:

- a specific business or engineering object connected to a concrete gap;
- a visible capability transition, often expressed as `从 X 到 Y` or an equivalent change;
- a named mechanism, product or implementation artifact that makes the promise technically identifiable.

Most titles concerned AI, Agent, digital employees or AI-assisted R&D, while one centered on demand clustering and supply gaps. One generic introduction title was also present, so no title shape is a necessary condition.

In a follow-up discussion on 2026-10-30, the user supplied another headline screenshot and observed a preference for frontier AI technology, especially AI combined with business. The visible titles included AI-native business workflows, AI-assisted engineering and applied Agent work; a browser-automation execution-loop article occupied position 4. This is a second supplied snapshot, not continuous monitoring; the screenshot's capture time and the full text of those articles were not independently verified. Do not reconstruct truncated titles or infer article results from titles alone.

Together, these observations support a working editorial preference: when choosing among adequately evidenced topics for `ATA 头条`, give particular attention to an emerging AI capability applied to a concrete business or engineering problem. The recurring signal is the connection between capability, task, mechanism and outcome. A title containing AI does not establish technical novelty, business value or selection causality. Keep this preference provisional; neither a permanent AI quota nor an undisclosed ranking weight has been established.

One sampled headline opened with `一句话结论`, then a concrete supply problem, formal definitions, an eight-step solution, equations, exact coverage data, comparison results, tradeoffs and a lifecycle boundary. At capture time it had 106 views, 28 likes and 8 comments. Its headline placement therefore cannot be explained by a high current view count alone. Depth, editorial judgment, strategic relevance, author context or timing remain competing explanations.

## AI-and-business topic assessment

Assess topic fit before choosing a title. For a supplied draft, recover its existing contribution first; when selecting among topics, compare the evidence already available rather than suggesting a new AI project merely to attract a headline slot.

Ask what AI capability is new or newly practical in this setting, which user or business task it changes, why the previous workflow was insufficient, and which implementation decision connects the capability to the result. Frontier relevance can come from a model capability, Agent execution mechanism, evaluation method or engineering approach; using the newest model or attaching a trend term is insufficient.

Use this contribution chain as a planning aid, not a compulsory sequence of headings:

```text
AI capability -> real business or engineering problem -> decisive mechanism -> verifiable outcome
```

Choose the strongest claim the material supports:

| Available material | Editorial action |
| --- | --- |
| Emerging AI capability, a concrete task, a distinctive mechanism and scoped outcome evidence | Prioritize this angle among similarly substantiated ATA-headline candidates; connect the implementation to the task result. |
| A frontier technical mechanism with reproducible evaluation but no business deployment | Write a bounded technical contribution; explain relevance without claiming production adoption or business impact. |
| A real business use of established AI with substantive implementation or lessons | Lead with the proven contribution; do not relabel the technology as frontier. |
| A trend recap, renamed API wrapper or demo without a distinctive contribution | Identify the missing evidence or narrow the claim; do not fill the gap with an invented scenario or benefit. |
| A useful non-AI engineering contribution | Preserve the topic and assess its actual merit; do not add an AI narrative to improve apparent headline fit. |

Outcomes may concern task completion, quality, reliability, accessibility, human workload, cost or latency. Use only observed results with an appropriate baseline and scope; do not require revenue claims. A proposed outcome remains a hypothesis, and a successful demo does not establish production value.

When asked to select or audit topics, state the strongest supported angle and any material evidence gap. Preserve the author's chosen topic unless a change is authorized; headline fit never replaces the [publication-value gate](publication-value.md).

## Headline-semantic gate

Because the headline module exposes the title as its primary content signal, read the title without the summary, cover or body. A technical reader or semantic evaluator should recover most of these elements:

- the concrete object, role, system or workflow;
- the real problem, gap, decision or capability change;
- the mechanism, product or artifact that makes the article non-generic;
- the result or destination the body will verify;
- the relevant business or engineering scenario.

If the title cannot be understood without prior project knowledge, expand the opaque project name with its category or value. If the title promises several unrelated contributions, narrow it to the one that the article proves best.

Useful shapes include the following, but they are not templates to apply mechanically:

```text
从 <old constraint> 到 <new capability>: <decisive mechanism>
<specific object>: <real gap or decision>
<product or mechanism>: <capability it gives a known role or system>
<verified result>: <what changed and how>
```

Keep numbers only when the body defines their baseline, population, time window and verification method. Keep AI, Agent, Harness, Skill, MCP, RAG or model names only when they materially change the mechanism, constraint, result or decision. Avoid project-code-only titles and generic endings such as “介绍”“探索与实践”“赋能升级” unless the preceding words already identify the contribution.

## Promise-parity gate

The body must repay the title immediately. Within the opening and first substantive section:

1. state a one-sentence conclusion precise enough to challenge;
2. show the real task, user, incident, artifact, interface, benchmark or business gap named by the title;
3. explain why the obvious path was insufficient;
4. identify the mechanism or decision that changed the outcome;
5. state the current result and delivery boundary.

Do not spend the first screen on industry trends, a long project history or a generic definition. A headline title with delayed evidence is a promise failure even if the later article is technically deep.

## Evidence-bearing body

Organize the article so a reviewer can verify and transfer its contribution:

- define the problem and terms before presenting formulas or architecture;
- pair each major mechanism with code, data, a diagram, an artifact, a failed path or an observed behavior;
- connect numbers to scope, denominator, baseline, time and verification method;
- distinguish shipped, tested, gray, planned and illustrative states;
- explain rejected alternatives, tradeoffs and conditions where the approach stops applying;
- end with a reusable decision, method or boundary rather than a project slogan.

Make claims specific enough for peers to challenge. A detailed correction and source update are stronger evidence of technical usefulness than generic praise.

## Headline audit

Before delivering an ATA-headline-oriented article, answer:

1. Can the title stand alone in a six-line headline module?
2. Does it name one concrete contribution rather than a broad topic?
3. Can a reader identify the object, problem or change and technical differentiator?
4. Does the first screen deliver the title's object and a defensible conclusion?
5. Does the body expose mechanism, evidence, tradeoff and applicability boundary?
6. If an AI angle is used, does a specific capability change a real task through an explained mechanism, with novelty and outcomes supported separately?
7. Are quantitative and impact claims reproducible and scoped?
8. Would the article remain worth publishing if it never entered `ATA 头条`?

For an AI-and-business angle, check that the title and first screen connect the AI capability to the task and its supported result. For frontier research or a non-AI topic, keep its actual contribution and evidence boundary rather than forcing this angle.

If question 8 fails, return to [publication-value.md](publication-value.md). Headline suitability cannot substitute for publication value.

## Headline reverse-engineering protocol

When studying the module, capture only the headline surface and matched article evidence:

```text
capture time and account context
positions 1 through 6
article ID and exact title
publication and update time
author and organization
article type, knowledge system, tags, circles and specials
views, likes, comments, notes, rewards and AI-assistance label at capture time
opening conclusion and heading outline
mechanisms, artifacts, quantitative evidence and stated boundaries
```

Repeat the capture across several replacement cycles. Match each selected article with similar non-selected articles from the same period, subject and organization before attributing selection to a title or content feature. Record entry and exit time when possible; observe interaction changes without manufacturing them.

The smallest defensible model is a hypothesis set, not one asserted pipeline:

- manual editorial selection;
- rule-based eligibility and ordering;
- semantic or LLM-assisted candidate review;
- learned ranking with editorial constraints;
- a hybrid of these mechanisms.

Use new observations to eliminate hypotheses. A rank change after an edit remains observational unless timing, competing inventory, author, topic, editorial action and simultaneous changes are controlled.
