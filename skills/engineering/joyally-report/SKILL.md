---
name: joyally-report
description: Turn completed or ongoing work into clear, evidence-based communication for a person. Use for progress and completion updates, engineering handoffs, bug diagnoses, reviews, incident summaries, release conclusions, and decision briefs, including brief updates after small changes or tests. Scale the response to the decision: a few sentences for a small update, structured sections for consequential work. Do not activate for unrelated factual Q&A or simple acknowledgments.
---

# Joyally Report

Turn verified work into a decision artifact. The report should let its reader understand the outcome, judge the evidence, see what remains uncertain, and take the next action without reconstructing the work from a tool diary.

## When to use

Use this workflow whenever the agent needs to tell a person what work achieved, where it stands, what evidence supports it, or what needs attention. Include brief status and completion replies, small changes, test outcomes, diagnoses, reviews, and complex handoffs. An unrelated factual question or acknowledgment does not need this workflow. A topic keyword alone does not demand a formal report.

Scale the output to the reader's decision. For a small change or progress update, use one to three direct sentences with no template or heading. For a consequential delivery, failure, or handoff, add only the sections needed to show evidence and next action. Do not turn every update into an audit of all possible risks.

## Output modes

Use `markdown` mode by default for interactive Codex CLI/TUI, Codex App/chat, IDE chat, PRs, issues, and documents. These surfaces own presentation; the skill supplies clean Markdown source with headings, ordered lists, inline code, links, and compact tables only when they make the decision easier to scan.

Use `terminal` mode for `codex exec` or other redirected stdout, plain-text terminals, CI logs, copied command output, or when the user explicitly requests `REPORT_FORMAT=terminal`. Follow an explicit `REPORT_FORMAT=markdown` as well.

The skill only produces report source; it cannot install or invoke a renderer in the host UI. If an interactive Codex surface displays raw Markdown markers, preserve Markdown mode and identify that as a client presentation-path problem; do not silently weaken the report format. Offer terminal mode only as an explicit compatibility fallback while the renderer issue is diagnosed. Never claim that Markdown is rendered merely because Markdown source was emitted.

Do not mix the two modes in one report.

### List formatting

Report output must not contain unordered lists. Never begin report items with Markdown or plain-text bullet markers such as `-`, `*`, or `+`, including nested items.

Use the smallest suitable alternative: numbered Markdown lists (`1.`, `2.`, `3.`), Roman numerals (`I.`, `II.`, `III.`), circled numbers (`①`, `②`, `③`), short labeled paragraphs, or a compact table. Nested details should use numbered subitems such as `1.1`, `1.2`, and `1.3`, or separate sentences. Hyphens inside ordinary prose, technical names, commands, and numeric ranges are not list markers and remain allowed.

### Terminal mode

Terminal reports must be plain text:

- Start with the report's result or title; include a skill attribution only when the user requests it.
- Use ASCII separators such as `============================================================`; do not rely on Markdown headings, blockquotes, tables, links, or bold markers.
- Put the verdict in the first section with one status emoji: `✅`, `⚠️`, `⛔`, or `⏳`.
- Use short sections such as `结论`, `待实现`, `待验证`, `变更`, `证据`, `状态`, `风险`, `阻塞`, and `需要决定`; omit empty sections.
- Use two-space indented evidence lines and the fixed status emoji vocabulary: `✅`, `⚠️`, `⛔`, `⏳`, and `ℹ️`; do not pair them with redundant bracketed English tags or place emoji on ordinary prose.
- If the destination explicitly requires ASCII-only output, replace the emoji with the plain words `PASS`, `WARN`, `BLOCKED`, `TODO`, or `INFO` without brackets.
- Do not emit ANSI color escape codes by default. Use ANSI colors only when the user explicitly requests color and the destination is a confirmed interactive terminal; never put ANSI codes in Codex chat, Markdown, files, CI logs, or copied command output.
- Keep lines short enough for a normal terminal; wrap long paths and commands onto indented continuation lines.
- Show paths as `path/to/file:line` and commands as separate indented lines beginning with `$`. Do not emit Markdown links or tables.
- Keep lifecycle states explicit: `working tree`, `staged`, `committed`, `pushed`, `deployed`, and `production verified`.

### Markdown mode

Markdown reports begin with the result and use real Markdown structure instead of bracketed section labels. Prefer `##` headings, short ordered lists, inline code, clickable file links, and the smallest useful table. The examples in `references/report-types.md` define content; render them using the selected output mode.

## Attribution

- Omit skill names, attribution lines, badges, and fixed opening text by default, in both output modes.
- Disclose the skill name only when the user asks for tool provenance; this does not require turning a brief reply into a report.
- Do not narrate the reporting process. Never open with “我会用 joyally-report……”, “下面进行影响评估”, a checklist of what will be inspected, or other tool-centric meta commentary. Lead with the result that matters to the reader.

## Reporting standard

### 1. Establish the decision context

Before writing, determine:

- **Reader and decision:** who will read this, and what must they understand, approve, verify, merge, release, or do next?
- **Objective and target:** what outcome was expected, for whom, by when, and against what baseline or acceptance condition?
- **Actual state:** inspect changed files, behavior, commands, tests, Git state, deployment state, and target-environment evidence.
- **Material delta:** what changed versus the target, baseline, or previous update? Separate activity, output, outcome, and user/business impact.

If the objective, baseline, or impact has not been established, say so. Do not convert implementation effort into an outcome claim.

### 2. Lead with judgment

The first one to three sentences must answer the highest-value questions for this reader:

1. Did the work meet the target, miss it, or remain blocked?
2. What verified user, customer, business, or engineering impact resulted?
3. What decision, risk, or next action requires attention now?

Put the conclusion before chronology. For longer reports, keep the decision layer readable on one screen, then add drill-down evidence. Use the smallest report type from [report-types.md](references/report-types.md) that supports the reader’s next action.

### 2.1 Put unfinished work first

When the user asks for a report, progress update, status, handoff, or asks what remains, make unfinished required work the most prominent part of the decision layer. Do not let a long completion inventory create a false sense that the objective is finished.

- If any material required work remains, state the highest-impact unfinished item in the first one to three sentences and place the relevant `阻塞`, `待实现`, `待验证`, or `风险` section immediately after the conclusion, within the first screen when the format has a visible first screen.
- Order open work by decision impact: current blockers first, then required implementation, then failed or unverified acceptance gates, then residual risks. Completed work is supporting context, not the headline.
- Classify every unfinished item by actual lifecycle state before writing it. Missing code, configuration, migration, documentation, automation, or release work is `待实现`; an implemented result whose required test, target-host build, deployment check, or user acceptance evidence is missing is `待验证`. Never merge both states into a generic `待办` or a single ambiguous item.
- If one outcome still needs both implementation and later verification, report two linked items in dependency order. Do not describe the verification as immediately actionable until its prerequisite implementation exists.
- For each unfinished item, state what is incomplete, why it matters, the next concrete action, the owner when known, and the completion or unblock condition. Include a deadline only when one is actually known.
- Treat work as unfinished only when it is required by the stated objective, acceptance criteria, explicit commitment, or next delivery gate. Do not inflate optional improvements or unrelated backlog into incomplete delivery.
- If an item is implemented but not committed, pushed, deployed, production-verified, or accepted where that later state is required, report the missing lifecycle gate explicitly rather than calling the work complete.
- If the audit finds no known required unfinished work, say so briefly in the conclusion; do not add empty open-work sections.

### 3. Write from facts to consequence

Use this chain for every material claim:

`objective or problem → observed change → evidence → impact or consequence → next action`

- Prefer first-hand evidence: observed behavior, raw measurements, tests, logs, commits, artifacts, URLs, and target-environment checks.
- Distinguish **observation**, **inference**, and **recommendation**. Mark estimates and hypotheses.
- When metrics and anecdotes disagree, report both and investigate the gap; do not select the more flattering signal.
- Explain why evidence is sufficient or insufficient. A passing build does not prove deployment, and deployment does not prove user acceptance.
- Give metrics a baseline, target, time window, unit, scope, sample count, and denominator when relevant.
- Report changed behavior and intentional scope boundaries. Avoid completion inventories, raw command lists, and unfiltered logs.

### 4. Preserve delivery truth

Keep these states separate whenever they matter to the claim:

`working tree → staged → committed → pushed → deployed → production verified`

Never infer a later state from an earlier one. “完成”, “修复”, “发布”, “上线”, and “验证通过” must be followed by a path, command result, commit, artifact, URL, or reproducible observation that proves that exact state.

### 5. Make ownership actionable

Every remaining action or dependency must name:

- the next concrete action;
- its owner, when known;
- its completion or unblock condition;
- its deadline, only when actually known.

Do not invent owners or dates. If the reader must authorize, supply, or choose something, state a direct `【需要决定】` or `【需要提供】` request near the top instead of hiding it at the end.

## Style principles

Apply these principles without imitating company slogans or pretending access to private internal templates. The public-source synthesis is documented in [reporting-principles.md](references/reporting-principles.md).

- **Value first:** connect engineering output to the user, customer, business, reliability, or delivery result it serves.
- **Candid and clear:** expose bad news, missed targets, and uncertainty directly. Use precise, concise language; do not manage up or inflate effort.
- **Results over activity:** “implemented”, “held a meeting”, and “ran tests” are inputs or outputs. State the resulting behavior and target delta.
- **First principles and root causes:** identify the governing constraint or mechanism instead of repeating symptoms or inherited assumptions.
- **Clarity and ownership:** make priorities, cross-team dependencies, owners, and the requested decision unmistakable.
- **Learning without blame:** for failures and incidents, describe system conditions, contributing factors, detection gaps, and durable actions rather than assigning personal blame.
- **Deep enough to decide:** be concise at the top, but preserve the evidence and reasoning needed to challenge the conclusion.
- **Raise the next bar:** after reporting the current result, state the next measurable threshold only when it is relevant and authorized.

## Open-item classification

Audit every substantive report for implementation gaps, verification gaps, risks, and blockers. Keep the concepts separate, but omit empty categories instead of emitting repetitive “无”.

- **Pending implementation / 待实现:** required behavior or delivery work does not exist yet, is only partially implemented, or has not reached its required source/package/deployment state. State the concrete artifact or behavior that must be produced.
- **Pending verification / 待验证:** the implementation exists at the claimed lifecycle state, but a required test, build, deployment check, target-host check, or acceptance result has not been observed. State what already exists, the exact missing evidence, and the pass condition.
- **Risk / 风险:** an uncertain future adverse outcome with a cause and impact. State likelihood or supporting evidence when known, mitigation, and owner when known.
- **Blocker / 阻塞:** a present condition that prevents the next required step. State the blocked step and exact unblock condition.

Do not use `待验证` to make unfinished implementation sound more complete. Source code that exists only locally may still be `待实现` relative to a required published or deployed outcome. Conversely, do not call target-host acceptance `待实现` when the required code and artifact already exist.

One fact can create linked entries, but it does not make the categories interchangeable:

```text
【待验证】滚动高亮已实现并通过 Chromium 验收；Safari 验收未执行。完成条件：6 个目录标题全部正确切换。
【风险】Warning：当前只有 Chromium 证据，WebKit 行为可能不同 → Safari 用户可能看到错误高亮 → 合并前完成 Safari 验收。
【阻塞】Safari 验收是发布门槛 → 当前不能发布 → 目标设备验收通过后解除。
```

Use this risk form when a material uncertainty exists:

`<Critical | Warning | Info>: <uncertain adverse outcome and cause> → <impact> → <mitigation> → <owner when known>`

- `Critical`: credible severe impact requiring mitigation before safe merge, release, deployment, or acceptance.
- `Warning`: credible residual risk that may materially affect behavior or delivery but does not currently block the handoff.
- `Info`: explicit limitation or low-impact uncertainty worth preserving.

Do not label “尚未测试” as a risk by itself. An unexecuted required test is `待验证`; a required test harness or test case that has not been written is `待实现`; the behavior that could escape is the risk; the failed release gate, if any, is the blocker.

## Risk and learning audit

Before sending, check only the categories relevant to the work:

- **Outcome and value:** target miss, no established baseline, unverified user/business impact, or a proxy metric mistaken for the goal.
- **Correctness:** untested branches, regressions, data loss, compatibility, concurrency, security, and migration hazards.
- **Verification:** what each test proves, what it does not prove, and which acceptance path is missing.
- **Delivery:** uncommitted work, failed build/package/CI, unpushed commits, undeployed artifacts, or unverified production behavior.
- **Dependencies and ownership:** credentials, permissions, upstream services, cross-team handoffs, environment failures, or unresolved decisions.
- **Scope and reversibility:** deferred requirements, temporary fallbacks, rollback conditions, and one-way decisions.
- **Learning:** root cause, detection gap, repeated-failure mechanism, and durable prevention when a failure occurred.

One high-impact failed or unverified gate outweighs a long list of completed tasks.

## Default completion report

Adapt the structure to the decision; do not fill sections mechanically.

Markdown mode is the default:

```markdown

## 结论 ✅

<target result, verified impact, and current boundary>

## 阻塞

1. ⛔ <highest-impact current condition and exact unblock condition>

## 待实现

1. ⏳ <missing implementation or delivery artifact, next action, owner when known, and completion condition>

## 待验证

1. ⏳ <implemented state, missing evidence, owner when known, and pass condition>

## 风险

1. ⚠️ <cause> → <impact> → <mitigation>

## 变更

<behavioral delta, key paths, and intentionally unchanged scope>

## 证据

1. ✅ <test, measurement, observation, or artifact>
2. ⚠️ <limitation and what it does not prove>

## 状态

<relevant working tree / commit / push / deploy / production states>

## 需要决定

<decision, recommendation, and tradeoff>
```

Omit empty sections. Use terminal mode as the plain-text fallback:

```text
============================================================
<short report title>
============================================================

结论 ✅
  <target result, verified impact, and current boundary>

阻塞
  ⛔ <highest-impact current condition and exact unblock condition>

待实现
  ⏳ <missing implementation or delivery artifact, next action, owner when known, and completion condition>

待验证
  ⏳ <implemented state, missing evidence, owner when known, and pass condition>

风险
  ⚠️ <cause> -> <impact> -> <mitigation>

变更
  <behavioral delta, key paths, and intentionally unchanged scope>

证据
  ✅ <test, measurement, observation, or artifact>
  ⚠️ <limitation and what it does not prove>

状态
  <relevant working tree / commit / push / deploy / production states>

需要决定
  <decision, recommendation, and tradeoff>
============================================================
```

For performance or resource claims, follow [performance-comparison.md](references/performance-comparison.md): preserve raw measurements, compare only compatible samples, and label a measurement as a baseline when no comparable predecessor exists.

## Final gate

Before sending, verify that the report answers:

- What target or problem did this work address, and why does it matter?
- What is the actual result versus the target or baseline?
- What evidence proves the stated result, and what remains inference?
- Which lifecycle state is true right now?
- What can still fail, remain unverified, or prevent the next step?
- Are pending implementation, pending verification, risks, and blockers correctly separated and omitted when empty?
- Does every `待验证` item name the implementation evidence that already exists, and every `待实现` item name the missing artifact or behavior?
- Is the owner or decision request explicit where action is needed?
- Can a busy reader understand the judgment before reading the details?
- If required work remains, is the most important unfinished item visible in the opening decision layer instead of buried after completed work?
- Does the report avoid all unordered-list markers and use numbering, labeled paragraphs, or tables instead?
- Have all tool narration, self-congratulation, jargon, and low-value chronology been removed?
- Does the output obey the selected mode without relying on unsupported rendering?
