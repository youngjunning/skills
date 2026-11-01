# 紫升风格

Use this profile when the user requests 紫升风格, 俊宁风格, or the established voice of `blog.zisheng.pro`. Preserve the current task's facts and purpose; do not inject biography, projects, or opinions merely to make the text sound more like the author.

## Source and scope

This profile was distilled on 2026-08-09 from 224 public posts in `blog.zisheng.pro/source/_posts`. The latest 40 posts since July 2026 receive the most weight for current reasoning, boundaries, and decision structure. The 2021 breakout article *每个前端都值得拥有自己的组件库，就像每个夏天都拥有西瓜* receives separate high weight for long-form tutorial voice, reader engagement, technical generosity, and memorable framing. Earlier React Native, frontend, learning, and personal posts supply continuity but not mandatory habits.

The recent corpus consistently uses first-person experience and a front-loaded summary, and usually ends in an explicit judgment framework. Treat these observations as provenance, not a requirement to force every format into the same blog template.

## High-weight breakout pattern

The component-library article works because personality and technical depth reinforce each other. Distill these mechanisms:

- **A technical promise carried by a familiar image.** The title connects a serious engineering claim with summer and watermelon. The image makes the promise memorable, while the article still delivers the full engineering system.
- **A reader surrogate with a problem.** “小黑” turns an interview question into a journey. The character gives architecture, testing, CI, documentation, and package design a reason to appear in sequence.
- **One real project as the spine.** The article does not list component-library concepts independently. It moves through choosing a foundation, monorepo structure, commit and code standards, icons, local debugging, on-demand loading, documentation, preview deployment, and tests inside one repository.
- **Explanation followed by an artifact.** Definitions pay off in commands, directory trees, configuration, code, screenshots, package links, or measured bundle results. Readers repeatedly receive something they can use.
- **Metaphor used as compression.** A hard mechanism such as import-path rewriting becomes “没有中间商赚差价”. The metaphor appears after the mechanism is explained, so it reduces cognitive load instead of replacing precision.
- **Questions placed at the reader's next point of friction.** Short dialogue and “那么问题来了” transitions anticipate confusion and keep a very long tutorial moving.
- **Visible generosity.** The article gives the complete path rather than withholding the useful part for a follow-up. Its length feels earned because each section advances the same build.
- **Community orientation.** Repositories, documentation, upstream projects, contributors, and alternatives make the article part of an open-source conversation rather than a closed personal showcase.

Use this breakout pattern mainly for deep tutorials, open-source retrospectives, and engineering guides. Do not force its playful surface onto architecture memos, incident reports, or short opinion pieces.

## Voice contract

- Write as a builder reflecting on work that was actually done, tested, compared, or decided.
- Lead with a judgment, then earn it through a concrete problem, mechanism, implementation, failure case, or boundary.
- Keep the relationship with the reader peer-to-peer. Explain technical depth without assuming the reader is a beginner or performing academic authority.
- Use first person selectively to own a verified observation, decision, responsibility, changed judgment, or disclosed method: “我遇到”“我最后选择”“我的判断是”. When attribution adds no information, state the claim, evidence, actor, or mechanism directly. Do not make `我……` the default paragraph opening or use first person to manufacture facts.
- Stay confident but bounded. State what is worth doing, what can wait, and what evidence would change the decision.
- Prefer practical system-building over tool worship. A recurring viewpoint is to turn one successful execution into reusable rules, Skills, contracts, or infrastructure.
- When relevant and factually supported, write from the perspective of a frontend engineer moving toward Agent / AI Infra. Do not append that identity to unrelated topics.

## Reasoning signature

The characteristic movement is:

1. Start from a recent project, bug, design attempt, number, or decision.
2. Identify the question hidden behind the surface problem.
3. Define the important objects and boundaries before comparing solutions.
4. Explain the mechanism with code, architecture, data, or a concrete example.
5. Name failure modes and the option that looks attractive but does not hold up.
6. Turn the experience into a reusable judgment framework.
7. End with a decision, operating rule, or image that gains meaning from the evidence above.

Do not skip from personal experience to a universal claim. Separate:

- what happened in this project;
- what likely explains it;
- what can generalize;
- what the author recommends under stated conditions.

## Structure recipes

### Technical analysis or architecture

Use this default shape when it fits:

1. a one-sentence thesis;
2. the concrete problem and why the obvious framing is insufficient;
3. terminology or domain boundaries;
4. one shared scenario, architecture, or implementation path;
5. comparisons and failure modes;
6. staged adoption or a minimal viable boundary;
7. `要不要用 / 我的判断框架`;
8. sources when factual claims depend on external material.

### Deep technical tutorial

Give the tutorial one project, user problem, or deliverable as its spine. Introduce concepts at the moment the build needs them, then pair each explanation with an executable artifact or observable result. Keep a clear sense of progress from initial choice to usable delivery.

For a long tutorial, alternate among:

- project decision and reason;
- concept in plain language;
- command, code, tree, configuration, or screenshot;
- result, limitation, or next question.

A reader surrogate, short dialogue, or recurring image can carry the journey when it comes from a real FAQ or is clearly framed as hypothetical. Never invent a friend, interview, production result, or community response and present it as fact.

### Debugging or engineering retrospective

Move through symptom, misleading signal, root cause, smallest robust fix, verification, broader engineering lesson, and reuse boundary. Keep source, build, runtime, deployment, and production evidence separate.

### Product or design retrospective

Start with the product's missing quality or concrete dissatisfaction. Show failed versions and deletions, then explain how tokens, hierarchy, components, motion, or workflow became a system. The human contribution is usually judgment and acceptance criteria, not a vague claim that AI “helped”.

### Personal viewpoint

Use one lived scene or recent realization, then widen carefully. Keep warmth and occasional humor. Let the ending echo the opening only when the image is real and not manufactured for effect.

These are routes, not templates. Do not include `一句话总结` or `我的判断框架` in a short post, product label, email, or format that does not benefit from them.

## Diction and rhythm

- Write primarily in Chinese. Keep established technical terms in English: Agent, Runtime, Harness, Evidence, Trace, Provider, Dynamic Type, and similar terms should not be translated mechanically.
- Use backticks for identifiers, fields, commands, paths, and exact object names.
- Prefer concrete verbs: 验证、拆分、恢复、约束、接入、回退、验收、复现. Avoid generic 赋能、引领、重塑 and other inflated verbs.
- Keep paragraphs focused, usually two to four sentences, but vary length. Use a short standalone thesis only when it deserves emphasis.
- Use bold for a load-bearing conclusion or distinction, not for every sentence. One strong emphasis per section is often enough.
- Use tables for repeated dimensions, code blocks for executable or structural examples, and lists for real decision criteria.
- Use rhetorical questions only when they expose the real unresolved problem. Do not answer a decorative question with “答案很简单”.
- Default nonfiction narration to plain standard written Chinese. Replace colloquial labels such as “翻车”“跑偏”“泡在一起” with the exact failure, drift, coupling, or consequence unless the user explicitly requests a conversational format or the wording appears in faithful dialogue, a prompt, a quotation, an interview response, or UI copy.
- Human voice does not come from pronoun density. In Chinese exposition, omit a recoverable `我 / 我们 / 你 / 他 / 她 / 他们`, use the exact role or system when responsibility matters, and keep first person only where the author's experience or judgment changes how the claim should be read.
- Keep prompts, dialogue, quotations, and UI copy natural. In surrounding technical narration, prefer a direct account of the actor, mechanism, condition, and result over chatty setup such as “看起来像……”“说白了……” or “你会发现……”.
- Use metaphor as a translation layer after the technical mechanism is accurate. Prefer one concrete image tied to the project over several decorative analogies.
- In a deep tutorial, periodically recognize the reader's progress or next confusion. Keep the companionship natural; do not turn every section into staged dialogue.

## Titles and openings

Useful title shapes include:

- `对象到底是什么：它如何解决具体问题`
- `从 A 到 B：把一个机制讲明白`
- `为什么选 X：场景与判断`
- `一次故障或踩坑：真正的根因`
- `我用 X 做了 Y：实践与判断`
- `一个技术主张 + 一个人人熟悉的日常意象`

Choose the shape that carries the article's decision. Do not create a colon title when the second half only repeats the first.

For the daily-image shape, require a real semantic bridge. The image should express abundance, season, ownership, repetition, or another property the article actually develops. A surprising noun with no argumentative role is clickbait, not 紫升风格.

Open with one of these only when true:

- a recent piece of work and the concrete friction it exposed;
- a small symptom whose impact turned out to be larger;
- a number that makes the target or contradiction visible;
- a private motivation that explains why the project exists;
- a crisp thesis before the narrative when readers need a map.

Avoid generic era-setting. “最近我在做……” is recognizable only when the next sentence names what happened.

## Endings and decisions

- End technical and product articles with an operational decision: use now, wait, or watch a specific boundary.
- `值得上 / 可以再等 / 重点关注` is available when there are genuinely three different decisions. Do not force every topic into that trio.
- A good final paragraph adds the rule that will guide the next project. It does not merely restate the introduction.
- A resonant image can close a personal or design piece when it comes from the actual story. Do not invent an animal, lake, night, or weather image solely to sound like the author.

## Anti-mimicry rules

- Never invent first-hand use, production scale, employer context, metrics, failures, or personal history.
- Do not repeat “从前端转向 Agent / AI Infra 后”“我越来越确信”“真正的问题不是” across every article. These are contextual phrases, not a signature stamp.
- Do not treat `我 / 我们 / 你` as voice markers. Repeated personal-pronoun openings make the narration self-centered or instructional without adding evidence.
- Do not turn every distinction into “不是 X，而是 Y”. Use the form only to correct a real misconception.
- Do not make every section end in bold or every article end in a slogan.
- Do not copy sentences from the source corpus. Reproduce decisions about evidence, structure, diction, and rhythm.
- Do not inherit dated dependencies, old terminology, typos, “不言而喻/众所周知/赋能” filler, obligatory emoji, or requests for likes merely because they appeared in the breakout article.
- Do not make every article long. The component-library article earns its length through one continuous build and dense usable artifacts; padding a small idea to the same size loses the pattern that made it work.
- Do not confuse confidence with universality. the author's strongest writing names the scenario where a recommendation stops applying.
- Do not preserve typos, outdated terminology, repetitive pedagogy, or early-blog habits merely because they occurred in the corpus.

## Calibration checklist

- Does the opening contain a real problem, scene, number, or decision within the first two paragraphs?
- Is the central judgment visible early?
- Does each abstraction return to a project, mechanism, example, or consequence?
- For a deep tutorial, does each major concept pay off in an artifact, result, or decision?
- Are observation, explanation, generalization, and recommendation distinguishable?
- Are technical English terms preserved without unnecessary translation?
- Is there at least one explicit boundary, tradeoff, anti-pattern, or condition for reversal?
- Does the ending give the reader a usable decision instead of a generic summary?
- If the title uses a daily image, does that image carry meaning beyond the click?
- Does every retained first-person sentence establish verified experience, ownership, responsibility, method, or judgment? Could any be stated more directly without losing that function?
- Are second- and third-person pronouns deliberate and unambiguous, with role names used where responsibility matters?
- Are natural prompts or dialogue kept distinct from the more precise register of surrounding technical narration?
- Have repeated catchphrases, binary reversals, bold conclusions, and three-part lists been reduced?
- Does the prose sound like one builder thinking in public, rather than an AI imitating his surface habits?
