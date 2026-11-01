# 团队项目外宣风格

Use this profile when the user requests 团队项目外宣、团队项目介绍、阶段成果对外表达，或希望读者先看懂产品形态和真实工作方式，再理解技术与团队价值。它适合 ATA、项目介绍、阶段性对外文章和面向协作方的产品说明；不自动替代发布公告、用户手册、ADR、个人博客或正式新闻稿的体裁要求。

## Source and scope

This profile was refreshed on 2026-08-20 from two internal team-project articles supplied for style analysis:

- one focused product introduction, weighted most for visible product surface, representative task flow, delivery-state boundaries and human control;
- one annual multi-project retrospective, weighted most for business framing, scenario selection, staged decision evolution, outcome evidence, platform extraction and portfolio navigation.

The second sample contains about 13,800 visible characters, 12 article headings, 14 article images and 12 video demonstrations. These counts show that artifacts carry a material share of the proof; they are not length, heading or media quotas. Both samples are internal and limited, so treat the profile as a reusable hypothesis about writing decisions rather than a timeless organization-wide standard. Refresh it when more representative material is available.

The corpus receives weight for these mechanisms:

- the product appears before its history or architecture;
- a recognizable user and one real task carry the explanation;
- technical components are introduced through responsibility in that task;
- current capability, gray rollout, future validation and stable operation remain separate states;
- human confirmation is placed where business responsibility changes;
- team contribution is visible without turning the article into a credit dispute.
- a portfolio article starts from a business constraint and a few operating goals, then selects representative projects instead of listing every initiative;
- scenarios are ordered by a meaningful gradient such as simple to complex, controlled to open-ended, or point solution to shared platform;
- each scenario exposes the decision trail: why it was chosen, which constraints mattered, what alternatives failed, what changed and what remained hard;
- repeated frontline friction earns the move from project delivery to platform capability;
- architecture diagrams, product screenshots, timelines and real demonstrations are assigned different proof responsibilities;
- an overview article acts as a hub into deeper technical or case articles rather than absorbing every detail itself.

Do not carry source-specific product names, people, internal systems, dates, links, metrics, stage labels or rollout claims into another project. Style transfers; facts do not.

## Communication goal

For a focused product introduction, the reader should be able to answer five questions after one pass:

1. What does the product look like in the user's existing work?
2. What can the user do with it right now?
3. How does one representative task move from intent to observable result?
4. Which decisions stay with people, and where can the system stop or recover?
5. What is shipped, in gray rollout, planned, or still awaiting evidence?

For an annual review or multi-project portfolio, the reader should instead be able to answer:

1. Which business constraint and operating goals connect the projects?
2. Why were these representative scenarios chosen, and how do they differ in difficulty or leverage?
3. Which technical or product decisions changed after contact with real constraints?
4. What evidence exists at the levels of feasibility, adoption, business result and scale?
5. Which repeated problems became shared product or platform capabilities, and what remains next?

An article that explains architecture but leaves the product or selected initiatives invisible has missed this profile. An article that creates excitement but hides current state or responsibility boundaries has also missed it.

## Voice contract

- Speak as a team that has built and inspected the product, not as a detached commentator or a heroic individual.
- Use the actual user role as the recurring subject. Prefer “客服小二打开订单页” over “用户可以体验智能化能力”.
- Keep the relationship direct and peer-to-peer. Explain what the reader will see, do and decide without ceremonial corporate language.
- Sound confident about verified behavior and deliberately bounded about rollout, scale, quality and business effect.
- Use `我们` only when shared ownership, a collective decision, or ongoing team work is itself relevant. Otherwise prefer the exact team, role, product, system, or an omitted recoverable subject. Use `我` only when the author is named and the verified first-person action materially affects the account.
- Replace vague `他 / 她 / 他们` with the user role, approver, operator, team, or system when responsibility matters. Keep pronouns only when the antecedent is clear and repetition of the role would harm readability.
- Let contribution appear through concrete ownership, delivered capability and acknowledgements. Do not make origin or credit claims stronger than the evidence.
- Build credibility by showing consequential reversals: where the first approach missed a requirement, which evidence forced the change, and why the next design was better suited. A failed path is useful when it changes the decision model, not when it merely adds drama.

## Reasoning signature

The characteristic movement is:

1. Place the reader in a familiar work surface and identify the visible change.
2. State the immediate friction removed for the user.
3. Name the current delivery stage and bound what the article will explain.
4. Walk through one representative task from user intent to business-state readback.
5. Introduce product and technical layers only where they explain that path.
6. Explain why the chosen product form fits the work, including where a lighter solution is enough.
7. Locate human responsibility by action impact, reversibility and authorization.
8. Turn expected value into rollout questions or acceptance evidence instead of declaring success early.
9. Close with the next observable milestone, project origin when relevant, team acknowledgement and useful related material.

The key proof is the last observable result. A click, successful API response, model message or completed tool call does not by itself prove that the user's task succeeded. When the domain has a source of truth, return to it and describe the state that must actually change.

## Structure recipes

### Full project introduction

Choose only the sections the project needs; do not copy the source outline mechanically.

1. **Visible product moment:** what remains familiar, what appears or changes, and what the user no longer has to do.
2. **Current state:** what exists now, who can access it, and the next delivery gate.
3. **Surface or mode map:** a compact table when several visible regions or modes need comparison.
4. **One task loop:** a numbered path from user request through execution, confirmation, recovery and result readback.
5. **Responsibility map:** define product, runtime, platform or service names by what each owns in the same task.
6. **Why this form:** connect fragmented systems, authenticated context, task duration or recovery needs to the chosen product shape; also name when a simpler tool is sufficient.
7. **Human control:** group actions by impact and explain approval, refusal, stop, rollback or prohibition behavior.
8. **Rollout evidence:** list the questions and measurements the next stage must answer.
9. **Origin and team:** link longer history instead of letting it consume the product opening; acknowledge verified contributors and related work.

### Short milestone announcement

Use one concrete user scene, the capability now available, the verified delivery state, one important boundary, and the next evidence gate. Omit the full architecture unless it changes the reader's decision.

### Technical project introduction

Keep the visible product and user task first. Then map each technical term to an owned responsibility, input, output and failure boundary. Use an arrow flow or small diagram when four or more layers would otherwise become a paragraph of nouns.

### Annual review or project portfolio

Use this shape when one article must explain several initiatives without becoming a status inventory:

1. **Business thesis:** name the domain constraint and one to three operating goals that make the work cohere.
2. **Prior learning:** compress the previous cycle into the few lessons that changed scenario selection or delivery strategy.
3. **Representative gradient:** choose two or three initiatives that reveal increasing complexity, leverage or organizational reach. Do not follow the organization chart.
4. **Repeated case loop:** for each initiative, explain **why this problem -> constraints -> alternatives -> decision -> delivered capability -> scoped result -> remaining hard problem**.
5. **Cross-case synthesis:** identify which lessons survived across scenarios and which depended on a specific task.
6. **Platform extraction:** show the repeated delivery friction, affected roles and shared capability that justified a platform or product investment.
7. **Evolution map:** use a timeline or stage model to make strategy changes and rejected assumptions visible.
8. **Future boundary:** separate the next operating hypothesis from current results and name the evidence that would validate it.
9. **Portfolio navigation:** link focused case studies, technical deep-dives and demonstrations; keep the overview responsible for the map.

### Platform born from field friction

Do not introduce a platform as a vision detached from delivery. Start with repeated problems observed across projects or roles: configuration complexity, testing cost, evaluation maintenance, operating feedback, reuse or onboarding. Show why local fixes no longer scale, define the platform's product principles, then map each principle to a visible workflow and adoption result. State which parts are shipped, in trial or still proposed.

## Product-surface techniques

- Describe the first screen as a user would encounter it: familiar area, new area, available action and visible feedback.
- Anchor each capability to a user moment. “Supports Browser Tools” is weaker than showing which page action the tool performs and how the user sees its state.
- Use one representative task as the spine. Additional features should clarify that task or be deferred to a compact table.
- When modes differ, compare what each can change, when to use it and what feedback the user receives.
- Show interruption and recovery where they matter. Long-running Agent work is not credible if the article only describes the happy path.
- Introduce internal layers after the reader has seen the task they support. Define each layer with one ownership sentence before listing technical details.
- In a portfolio article, the first visible object can be the business objective and scenario map rather than a product screen. Move quickly to the first representative task; a portfolio label is not permission for a long trend preface.
- Use the overview as a hub. Give each linked deep-dive a one-sentence reason to open it instead of presenting a bare catalog of related links.

## Evidence and delivery-state discipline

Keep these states explicit and separate:

- implemented in source;
- visible in a running product;
- available to a controlled gray cohort;
- released to the intended population;
- accepted through real task evidence;
- stable at the claimed scale.

Use exact dates, percentages, user counts, completion rates and performance gains only when verified. If value will be evaluated during gray rollout, phrase it as a question or acceptance criterion: whether completion rate rises, manual steps fall, recovery works, or users continue using the product. Do not convert an intended metric into an achieved result.

Organize maturity evidence as a ladder when the project evolves over time: **technical feasibility -> controlled trial -> user or business acceptance -> broader coverage -> stable operation -> repeatable delivery by other roles**. A later rung does not retroactively prove an earlier claim, and one scenario's scale does not transfer automatically to another.

For every quantitative result, preserve the metric definition, time window, population or traffic scope, comparison baseline and known caveat. If a metric changes after expansion, state that correction near the original claim. Prefer a few decision-bearing measures over a dense parade of percentages.

For each material claim, prefer one of these evidence forms:

- a current interface or screenshot;
- a step that can be reproduced;
- an observable business-state change;
- a measured result with its scope;
- a named release or rollout state;
- a maintained technical document that explains the mechanism.

Match artifacts to claims:

- an architecture diagram explains responsibility, control or information flow;
- a product screenshot proves a visible surface or workflow exists at the captured stage;
- a before-and-after comparison supports a usability or complexity claim only when the compared scope is equivalent;
- a timeline shows decision evolution and the evidence behind each turn;
- an audio or video demonstration proves observed behavior in that case, not aggregate business effect, reliability or scale.

## Human responsibility and safety

Avoid the vague slogan “human in the loop”. State where responsibility changes:

- read-only lookup may proceed within an authorized scope;
- reversible edits should expose the proposed change and recovery path;
- external communication or formal submission requires confirmation before impact;
- high-impact or irreversible actions require stronger authorization or must remain unavailable.

Explain what the user can approve, reject, stop, undo or take over, and what happens to the task afterward. Confirmation points should follow business responsibility, not interrupt every technical step.

## Team attribution

- Default to the team as the delivery subject when the work is collective.
- Name individual contributors only when names are approved for the target audience and their roles are verified.
- Prefer concrete contribution language—product decisions, implementation, signing, business integration, testing, environment support—over generic praise.
- Put a long origin story in a related article when it competes with the current product explanation.
- For a large portfolio, group acknowledgements by verified responsibility or collaborating function. Move an exhaustive approved name list to a closing acknowledgement or appendix so it does not interrupt the argument.
- Do not claim that one person initiated, owned or completed the project unless provenance supports that conclusion and the team agrees with the framing.
- For public material, remove internal aliases, systems, domains, package scopes, release identifiers and operational details unless each item is approved for disclosure.

## Diction and rhythm

- Write primarily in Chinese and preserve established English technical terms such as Agent, Runtime, Tools, MCP and Browser Kernel.
- Prefer visible verbs: 打开、读取、选择、点击、等待、确认、停止、恢复、回读、交付. Avoid 赋能、重塑、引领、全链路升级 and similar abstract promotion.
- Keep paragraphs focused, usually two to four sentences. A short sentence can carry a boundary or verified conclusion.
- Use tables for repeated comparisons such as visible area / user action / purpose, mode / capability / scenario, or action impact / system behavior / human responsibility.
- Use a numbered list for the one representative task. Do not turn unrelated feature inventory into a long numbered process.
- Use a compact arrow flow when several product and technical names must be connected in one task.
- Use bold for role names or one load-bearing boundary, not as decoration.
- Repeat the actual user role when it preserves perspective; reduce generic “用户”“业务方”“相关人员”.

## Openings and endings

For a focused introduction, open with the product's current appearance or a familiar task. Within the first three paragraphs, establish:

- what the user still recognizes;
- what has changed;
- what friction disappears;
- what stage the project is actually in.

For an annual portfolio, open with the durable business constraint, the operating goal and the first representative scenario. Summarize prior-year learning only when it explains why the current choices differ. The reader should reach a concrete problem and decision within the opening section.

Avoid starting with an AI era statement, a long project history, an organization mission or a stack inventory. A technology milestone can provide a date boundary, but it should not replace the team's own problem statement.

End with the next evidence-bearing step: gray rollout, real-user verification, adoption threshold, reliability gate or a concrete follow-up. A portfolio may end with one bounded operating thesis for the next cycle, followed by the experiments or measures that would test it. Acknowledge the team and link related material when useful, but do not substitute a broad prediction, “敬请期待” or a slogan for the next observable milestone.

## Anti-mimicry rules

- Do not reuse source product names, role aliases, colleague names, dates, links, metrics, stage labels or exact flow counts in another project unless they are that project's independently verified facts.
- Do not force every article into “长什么样、怎么工作、谁来接管” or announce that it answers exactly three questions.
- Do not make every project use two modes, a right sidebar, a gray rollout or the same risk table.
- Do not copy source sentences, slogans, proverbs, catchphrases or conversational fillers as style markers.
- Do not turn a team article into a personal founder story, and do not erase verified individual work merely to sound collective.
- Do not place architecture, platform vision or project history before the reader can picture one normal user task.
- Do not present an illustrative mockup as the current UI or a planned behavior as shipped.
- Do not overclaim “closed loop”, “production-ready”, “stable” or “completed” when only implementation, a demo or a gray plan is verified.
- Do not imitate the source's length, initiative count, metric density or media volume. A portfolio earns breadth through a governing business thesis and comparable case loops, not accumulation.
- Do not present a product or platform as inevitable. Preserve the repeated friction and failed local alternatives that justified the investment.
- Do not let an expansive future section blur current results. Name future claims as hypotheses and attach an evidence gate.

## Calibration checklist

- For a focused introduction, can the reader picture the product and its first useful action within the first two paragraphs?
- For a portfolio article, can the reader state the common business goal and the progression connecting the selected initiatives?
- Does each selected initiative keep an actual user or operator role visible rather than addressing an abstract market?
- Does one representative task reach an observable domain result?
- Does each representative initiative explain why it was chosen, what constrained it, what decision changed and what remained hard?
- Are technical names introduced through ownership in that task?
- Does the article explain both why this product form fits and when a simpler option is enough?
- Are implementation, gray rollout, release, real-task acceptance and stable operation kept separate?
- Are feasibility, adoption, business effect, scale and cross-role repeatability supported by evidence at their own level?
- Are expected benefits framed as validation questions until evidence exists?
- Does every metric retain its scope and caveat, including any decline or correction after expansion?
- Are approval, refusal, stop, recovery and final human responsibility located precisely?
- Is a platform justified by repeated field friction and visible workflows rather than vision language alone?
- Does team attribution match verified contribution and disclosure permission?
- Have internal names, systems, URLs, IDs and metrics been reviewed for the target audience?
- Has source-specific structure and wording been removed so the result fits the new project rather than imitating the corpus?
- Does the ending name the next observable milestone instead of repeating the opening?
