# Non-fiction Deslop Gate

Use this reference for articles, ATA, blogs, technical documentation, proposals, reports, product copy, speeches, and other reader-facing prose. It is adapted from the deslop discipline used by the fiction writing workflow, but contains no fiction-specific rules.

## Purpose

Deslop removes writing that sounds generated, padded, or over-produced while keeping the author's facts, judgment, evidence, terminology, and voice. It is a final quality gate, not a synonym for simplification and not permission to rewrite a document into a generic house style.

Run it after the structure and facts are stable and before delivery. Use the smallest change that fixes the pattern. Never delete a paragraph merely because its wording is weak; preserve its information or rewrite it with a concrete actor, action, object, evidence, or consequence.

## Scope router

| Content | Required pass |
| --- | --- |
| Article, ATA, blog, product or project introduction | Gates A–E + quick checks |
| Technical documentation, proposal, report, speech | Gates A–D + E where the document makes broad claims |
| Short transactional copy | Gates A, B, E + quick checks |
| Code, configuration, logs, legal text, machine-readable data, verbatim quotation | Do not rewrite; inspect only for surrounding prose if requested |

## Two-pass workflow for long Markdown

Use a baseline-and-rescan pass when the document is long enough that repeated patterns are easy to miss.

1. **Inventory clusters before editing.** Search for repeated binary reversals, rhetorical setup, pronoun-led sentence openings, chatty explanatory transitions, bold spans, em dashes, decorative arrows, slogan-like one-line endings, and metaphor families. Counts are navigation aids, not quality scores or mandatory limits.
2. **Separate source language from narrator language.** Preserve verified product labels, UI names, quotations, domain terms, code, and deliberate voice. Review narrator-added emphasis and metaphor more aggressively.
3. **Edit from large to small.** Remove repeated claims and competing metaphors first; then repair paragraph templates, vague actors, and unsupported certainty; reduce decorative formatting last.
4. **Re-scan the same categories.** Read each survivor in context. Keep it only when it carries a real contrast, navigation function, product identity, or necessary emphasis.
5. **Compare the before and after meaning.** Numbers, conditions, states, links, code, examples, and decision boundaries must remain intact even when the prose becomes shorter.

Do not optimize for the lowest marker count. A technical article may legitimately need bold labels, arrow flows, or one defined metaphor. The failure mode is clustering and repetition without additional information.

## Gate A — Empty language and jargon

Replace abstract or inflated wording with the specific action, object, scope, or result.

Flag:

- filler openers and padding: “在当今……”“随着……不断发展”“值得注意的是”“从某种意义上说”;
- business jargon without a concrete meaning: “赋能”“重塑”“全链路”“闭环”“抓手”“生态”“范式”“协同创新”“降本增效”;
- AI vocabulary tells: “深入探讨”“精心打造”“量身定制”“无缝衔接”“充分体现”“彰显重要性”;
- paired adjectives that say little: “简单而强大”“优雅且稳健”“轻量但全面”;
- standalone intensifiers and hedges: “真正地”“本质上”“显著地”“无疑”“毋庸置疑”.
- colloquial or promotional narration in nonfiction: “说白了”“搞定”“神器”“炸裂”“秒杀”“一把梭”“翻车”“跑偏” when a precise standard-written verb, condition, failure, or result is available.

Do not mechanically delete every adverb or alter faithful prompts, dialogue, quotations, interview responses, or UI copy. Keep wording that changes a factual claim or belongs to a required source register; replace narrator-added colloquialism and emphasis with the exact action, state, or consequence.

## Gate B — Template structure

Prefer direct statements over familiar AI patterns:

- negation-reversal: “不是 X，而是 Y”“不只是 X，更是 Y”“问题不在 X，而在 Y”;
- throat-clearing: “下面我们来……”“让我们一起……”“本文将带你……”;
- pedagogical hand-holding: “我们先拆解一下”“不妨想象”“可以把它理解为……”;
- self-posed Q&A: “结果是什么？……”“最关键的一点？……”;
- meta-commentary: “接下来我会……”“前面已经提到……”“本文最后总结……”;
- narrator-centered framing: consecutive sentences or paragraphs opened with “我 / 我们 / 你 / 他 / 她 / 他们” when the subject is recoverable or a specific role, team, product, or system would be clearer;
- conversational technical narration: “这句话看起来像……”“说白了……”“你会发现……”“真正执行时却会……” when the phrasing simulates a chat but does not clarify the actor, mechanism, condition, or result;
- repeated sentence openings or three-item parallel lists that add rhythm but no distinction;
- listicle paragraphs disguised as prose.

Rewrite to state the point, use a real transition, name the responsible role or system, or make the list explicit. Chinese exposition can omit a subject that is already clear. Use a direct imperative instead of “你可以……” in procedural writing. Keep a personal pronoun when it establishes verified experience, responsibility, viewpoint, or deliberate reader relationship; keep a contrast when the contrast itself is evidence-bearing.

Treat quoted prompts, dialogue, interview responses, UI messages, and other spoken artifacts as a separate register. Preserve their natural pronouns and wording when fidelity matters. Review the surrounding explanation more strictly: `打开三家供应商的网站……提交采购申请前先让我确认` can remain as a task prompt, while prose such as `这句话看起来像一个 prompt，真正执行时却会穿过整个浏览器系统` should name the mechanism directly, for example `该任务由完整的浏览器系统协同执行，链路如下`.

## Gate C — Agency, evidence, and certainty

Every material claim should have an actor, source, scope, or observable result.

Flag:

- passive claims with no owner: “系统被设计为……”“问题得到解决”;
- false agency: “数据告诉我们”“市场需要”“决策自然形成”“能力推动业务增长”;
- vague authority: “业内普遍认为”“研究表明”“用户反馈显示” without a named source or sample;
- vague importance: “意义重大”“影响深远”“这是关键一步” without the specific consequence;
- a demo, API response, model answer, or build being presented as proof of adoption, stability, scale, or business impact.

Rewrite with the responsible person or team, the actual observation, the comparison scope, and the current delivery state. Narrow the claim when evidence does not support the stronger version.

## Gate D — Rhythm and formatting

Check the document as a reader would see it:

- break metronomic paragraphs and vary sentence length;
- remove decorative em dashes, arrows, stars, and excessive bold labels from body prose;
- avoid making every section end with a slogan or one-line punchline;
- use a table or genuine list when repeated fields are being compared;
- keep headings, links, code blocks, quoted text, and required attribution unchanged unless the task explicitly includes them.

For Markdown, inspect formatting as a system rather than one marker at a time. Many individually defensible bold spans, em dashes, arrows, and blockquotes can combine into an over-produced page. Keep emphasis for stable labels and load-bearing distinctions; rewrite sentence-level emphasis that merely instructs the reader what to feel.

Do not optimize for a fixed paragraph length or ban a punctuation mark mechanically. The test is whether formatting carries information or merely signals emphasis.

## Gate E — Composition and tone

Review the whole piece for patterns that sentence-level edits cannot fix:

- grandiose stakes for a local change;
- invented concept labels that pretend to be established terms;
- fractal summaries that preview and repeat the same point at every level;
- one-point dilution, where several sections restate one thesis without adding evidence or a decision;
- dead metaphors repeated throughout the article;
- dismissive balance formulas such as “尽管存在挑战，但……” without engaging the challenge;
- signposted conclusions such as “综上所述”“最后总结一下”;
- internal editing or repository narration that the target reader does not need.

Also inventory metaphor families across the whole document. Product-owned names such as a branded UI label may stay, but narrator-added metaphors should not shift repeatedly among magic, mining, finance, medicine, combat, and manufacturing unless each one explains a distinct mechanism. Prefer one useful framing and plain engineering language elsewhere.

Keep one useful metaphor or framing when it clarifies a mechanism. Remove or define invented labels. End with the next decision, observable milestone, operating boundary, or implication rather than a generic uplift.

## Quick checks

Before delivery, ask:

- Can the first section be understood without a long preface?
- Does each section add a new fact, mechanism, comparison, decision, or boundary?
- Can every broad claim be tied to a person, source, sample, date, or observed result?
- Are shipped, tested, gray, planned, and stable states kept separate?
- Did any “不是……而是……” or self-posed question survive only because it is genuinely necessary?
- Does each retained `我 / 我们 / 你 / 他 / 她 / 他们` establish experience, ownership, viewpoint, instruction, quotation fidelity, or a clear antecedent?
- Is conversational wording confined to a genre, voice, prompt, dialogue, quotation, or UI context that actually benefits from it?
- Is every non-fiction explanatory sentence rigorous, accurate, plain, and free of narrator-added colloquialism, vague claims, and promotional inflation?
- Did any paragraph become more abstract after editing?
- Are private names, domains, identifiers, unpublished metrics, and internal process details appropriate for the target audience?
- Is the final paragraph a useful implication or next step rather than a slogan?

## Result

Classify the pass internally:

- `clean`: no repeated deslop pattern worth editing;
- `light`: a few local wording or structure fixes;
- `moderate`: several paragraphs or one section rewritten;
- `heavy`: the piece required a structural rewrite while preserving its facts and purpose.

Do not append this classification to the delivered prose unless the user asks for an editorial audit or the result blocks delivery. Do not invent a numeric “AI score”. The gate is passed when the identified patterns are resolved or intentionally retained with a documented reason.
