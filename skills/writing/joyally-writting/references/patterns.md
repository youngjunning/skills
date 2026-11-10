# Writing quality patterns

Use this reference for detailed Chinese and English pattern detection. Rewrite repeated patterns and clusters; do not ban a useful phrase solely because it appears once.

## A. Filler, jargon, and inflated diction

Cut throat-clearing and announce the point directly.

| Avoid | Better move |
| --- | --- |
| 值得注意的是、需要指出的是、众所周知、毋庸置疑 | State the fact or evidence |
| 在当今快速发展的时代、随着……不断发展 | Name the concrete change and date or scope |
| 本质上、从某种意义上说、可以说 | Commit to the claim or remove it |
| 赋能、抓手、范式、生态、协同、全链路、闭环 | Keep only when it is a defined domain term; otherwise name the action |
| seamless, robust, transformative, groundbreaking, cutting-edge | State the measurable improvement |
| leverage, utilize, harness, foster, navigate | use, build, handle, or the specific verb |
| at its core, it is worth noting, in today's landscape | Delete and start with the substance |

Delete decorative intensifiers and confidence theater: 真正、极其、显著、深度、全面、无疑、really, truly, deeply, fundamentally, certainly, remarkably.

Do not purge every adverb mechanically. Keep one when it changes the fact, timing, degree, or manner.

## B. Template structures

### Binary reversal

AI often states what a thing is not before saying what it is.

```text
不是 X，而是 Y。
不仅是 X，更是 Y。
问题不在 X，真正的问题在 Y。
Not X. Y.
The answer isn't X. It's Y.
Less about X, more about Y.
```

State Y directly unless X is a real misconception that the argument must rebut.

### Mechanical symmetry

Flag three or more consecutive clauses or sentences with the same grammar:

```text
它能识别……它能分析……它能生成……
首先……其次……最后……
更快、更准、更智能。
```

Combine related points, vary the third sentence, or keep only the differentiating item.

### Rhetorical setup and self-Q&A

```text
结果呢？令人震惊。
这意味着什么？答案很简单。
Why does this matter? Because...
The result? Devastating.
```

Turn the pair into one direct statement.

### Pedagogical hand-holding

Cut “让我们来看看”, “接下来深入探讨”, “可以把它理解为”, “Here's the thing”, “Let's unpack this”, and “Think of it as”. Start with the content.

### Pronoun-led narration and register drift

Chinese expository prose rarely needs every clause to restate its speaker, reader, or previously named actor. Review repeated `我 / 我们 / 你 / 他 / 她 / 他们` openings and make the actor as specific as the evidence allows:

| Draft | Better move |
| --- | --- |
| 我认为这个方案更稳妥 | State the verified criterion: `该方案保留了断线恢复和审计记录`；retain `我的判断是` only when personal judgment or accountability matters |
| 你可以打开设置页并选择 Provider | Use the procedure directly: `打开设置页，选择 Provider` |
| 他会在提交前审核申请 | Name the role: `采购管理员在提交前审核申请` |
| 这句话看起来像一个 prompt，真正执行时却会穿过整个浏览器系统 | Name the mechanism: `该任务由完整的浏览器系统协同执行，链路如下` |

Do not optimize for zero pronouns. Keep them when they establish verified experience, collective ownership, viewpoint, deliberate reader relationship, or an unambiguous continuation. Preserve natural wording inside prompts, dialogue, quotations, interview answers, and UI copy when fidelity matters. English normally requires explicit subjects; improve actor choice and sentence structure instead of deleting pronouns mechanically.

### Dramatic fragmentation

```text
速度。质量。突破。
就是这样。没有更多。
He shipped it. Publicly. In production.
```

Use a complete sentence unless fragments reflect an established authorial voice.

## C. Vague claims and hidden actors

Replace announced importance with the concrete impact:

| AI-like | Specific |
| --- | --- |
| 这具有重要意义 | It cuts review time from two days to four hours |
| 其影响是深远的 | Name who changes behavior and how |
| 数据告诉我们 | Name the metric and the person drawing the conclusion |
| 市场正在奖励这种模式 | Buyers are paying more for X, according to Y |
| 决策逐渐浮现 | Name who decided and when |
| Studies show / experts argue | Cite the study or expert; otherwise remove the authority claim |

Passive voice is not always wrong. Rewrite it when it hides responsibility or weakens a decision.

## D. Rhythm and formatting

- Break runs of four sentences whose lengths fall within roughly 30% of one another.
- Avoid making every paragraph four to six sentences long.
- Do not end every section with a punchline or uplift.
- Limit em dashes and semicolons when they become a house rhythm.
- Use three-item lists only when there are three distinct items, not because three sounds complete.
- Keep bold-first bullets only for genuine labels or scan-heavy reference material.
- Avoid decorative arrows, stars, and emoji in serious prose unless the product format calls for them.
- Prefer short paragraphs for mobile reading, but do not split every sentence into its own paragraph.

## E. Repetition and composition

Flag:

- the thesis restated at the start and end of every section;
- one metaphor extended across the full piece;
- several historical or company analogies named without analysis;
- a conclusion that only repeats the introduction;
- the same noun or adjective clustered locally without intentional emphasis;
- paragraphs that can be removed without losing evidence, logic, or voice.

Keep one strong formulation. Each later paragraph should add evidence, consequence, limitation, or a decision.

## F. Tone tropes

### Grandiose stakes

Scope “redefines the future”, “changes everything”, “next era”, and “historic turning point” to what the evidence supports.

### Faux vulnerability

Remove polished disclaimers such as “我知道这听起来很夸张”, “坦白说”, or “I'll be the first to admit” unless they introduce a specific personal risk or mistake.

### Invented concept labels

AI names ordinary observations “the X paradox”, “Y trap”, or “Z effect”. Describe the behavior plainly. Keep a label only if it is useful, defined, and reused consistently.

### Dismissive balance

“尽管存在挑战，仍然……” and “Despite its challenges...” often acknowledge risk without analyzing it. Either explain the risk and mitigation or remove the clause.

### Signposted conclusion

Delete “综上所述”, “总而言之”, “In conclusion”, and “To sum up”. Start the final paragraph with the actual conclusion.

## Product writing: concept distance

A product article can be accurate and polished while still leaving the reader unable to picture the product. Flag the draft when its stated promise is product-facing and one or more of these are true:

- history, architecture, or a glossary occupies the opening before the reader knows what appears on screen;
- the article names many layers and components but never walks through one normal user task;
- a concept image, future workflow, disabled feature, or planned capability is described as current product behavior;
- product introduction, project history, technical architecture, and personal reflection all compete to be the main story;
- the title still promises an origin story after the body has been rewritten as a product guide, or vice versa.

Repair the structure in this order:

1. State who opens the product, what they see, and the first useful action available now.
2. Walk through one representative task, including visible progress, user control, failure or recovery, and the observable result.
3. Explain only the concepts needed to understand that task.
4. Compress the remaining history to the minimum context, or move it into a linked companion article.
5. Retitle each resulting piece according to what it now delivers.

Do not fake concreteness. Use a verified screenshot or current implementation evidence when available; otherwise label the visual as illustrative and state the current boundary. Do not invent a personal anecdote to create warmth. A credible human voice names the actual moment, constraint, tradeoff, or decision that changed the author's view.

## Fast audit checklist

- Does the opening reach the point in the first two sentences?
- If the title promises a product, can the reader picture its current surface and explain one normal task after the first section?
- Can every claim name an actor, object, metric, example, or consequence?
- Are any questions answered immediately by the author?
- Are binary reversals doing real argumentative work?
- Do three-item lists contain three distinct facts?
- Does each paragraph advance the piece?
- Are sources named?
- Are personal pronouns carrying viewpoint, responsibility, instruction, or quotation fidelity rather than merely framing the narration?
- Does explanatory prose state the mechanism directly while prompts, dialogue, quotations, and UI copy retain their appropriate spoken register?
- Does the ending add a decision or consequence rather than another summary?
