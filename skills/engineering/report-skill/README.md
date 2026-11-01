# Report Skill / 决策型工程汇报

A decision-ready, evidence-first reporting skill for coding agents. It turns engineering and project work into a report that helps the next reader judge the result, challenge the evidence, and take action.

面向编码 Agent 的决策型汇报 Skill：不复述执行过程，而是把目标、结果、影响、证据、交付状态和下一步组织成可判断、可追踪的工程汇报。

## Why this skill / 为什么需要它

Many updates describe effort instead of outcomes: files changed, commands run, meetings held, and tasks checked off. They also blur local, committed, pushed, deployed, and production-verified states.

This skill makes five questions explicit:

1. What target or user problem mattered?
2. What result changed versus the target or baseline?
3. What evidence proves it, and what remains inference?
4. What delivery state is actually true?
5. What decision, owner, risk, or blocker needs attention now?

它会区分 activity、output、outcome 与 impact，也会把以下交付状态分别陈述：

- working tree / 工作区
- staged / 已暂存
- committed / 已提交
- pushed / 已推送
- deployed / 已部署
- production verified / 已完成生产验证

## Use it when / 适用场景

- leadership or project progress updates / 管理层与项目进展汇报
- implementation, refactoring, or engineering handoff / 实现、重构与工程交接
- diagnosis, incidents, and postmortems / 排障、事故与复盘
- tests, builds, CI, review, and release decisions / 测试、构建、CI、评审与发布判断
- Git, deployment, and production verification / Git、部署与线上验证
- technical decisions and alternatives / 技术决策与方案选择
- performance and resource comparisons / 性能与资源前后对比

Use it when the user requests a formal report or a complex delivery needs structured evidence, risks, blockers, or handoff actions. Ordinary Q&A, brief status replies, small changes, and routine Git/test results receive a direct reply; a topic keyword alone does not trigger the skill.

## Install / 安装

Place this repository in your Codex skills directory, or install it through your team’s Skill distribution workflow. The runtime entry point is [`SKILL.md`](SKILL.md).

## Invoke / 调用

```text
Use $report-skill to turn this work into a decision-ready report:
lead with the result versus target, connect verified impact to evidence,
preserve the exact delivery state, and make any action or decision explicit.
```

中文示例：

```text
使用 $report-skill 汇报这项工作：先给目标达成判断，再说明已验证的影响和证据，
明确当前交付状态，并把需要的决策、Owner、风险或阻塞直接写出来。
```

Markdown reports begin with the actual result. Omit skill attribution and fixed banners unless the user requests tool provenance.

The report itself never starts with “我会用 report-skill……” or a checklist of what the agent plans to inspect. Tool narration is not a result.

## Reporting model / 汇报模型

### Decision layer / 决策层

The first one to three sentences state:

- result versus target;
- verified impact;
- current decision, boundary, or critical risk.

### Evidence layer / 证据层

The report then provides only the detail needed to challenge the conclusion:

- behavioral delta and intentionally unchanged scope;
- tests, observations, metrics, commits, artifacts, and URLs;
- what each piece of evidence proves and does not prove;
- root cause or alternative explanations when relevant;
- exact lifecycle and rollback state.

### Action layer / 行动层

Every remaining item is classified and made executable:

- **Pending implementation / 待实现:** required code, configuration, migration, documentation, automation, or delivery artifact does not exist yet or has not reached its required lifecycle state.
- **Pending verification / 待验证:** the implementation exists, but required test, build, deployment, target-host, or acceptance evidence is still missing.
- **Risk / 风险:** an uncertain adverse outcome, with cause, impact, and mitigation.
- **Blocker / 阻塞:** a present condition preventing the next step, with an unblock condition.
- **Decision / 决策:** an external choice, with a recommendation and tradeoff.

When one outcome needs both work and later acceptance, write two linked entries in dependency order. Do not collapse them into a generic `待办`, and do not use `待验证` for implementation that is still incomplete.

Empty categories are omitted. The skill audits them internally but does not print repetitive “无”.

## Cross-company synthesis / 大厂方法融合

The reporting style is synthesized from public first-party material rather than copied from a rumored company template:

- Tencent: user value, integrity, proactivity, and collaboration.
- Alibaba: customer priority, trust, ownership, change, and a rising baseline.
- ByteDance: candid and clear communication, first-hand facts, and real impact.
- Microsoft: create clarity, deliver success, customer obsession, and shared contribution.
- Google: measurable goals and blameless learning from failure.
- Tesla: first-principles reasoning, end-to-end ownership, and real-world verification.
- Amazon: customer-backwards thinking, ownership, Dive Deep, results, and complete written narratives.

These are operating principles, not claims that every team at those companies uses one identical report format. Sources and inference boundaries are recorded in [`references/reporting-principles.md`](references/reporting-principles.md).

## Report types / 汇报类型

Choose by the reader’s next decision:

| Type | Reader decision | 类型 | 读者要做的判断 |
| --- | --- | --- | --- |
| Leadership/project status | Is the target met, what is the impact, and what needs attention? | 管理层/项目进展 | 是否达标、影响如何、需要关注什么？ |
| Completed delivery | Can this be merged, verified, released, or continued? | 完成交付 | 能否合并、验收、发布或继续？ |
| In progress | What is the landing point, forecast, and critical path? | 进行中 | 当前落点、预测和关键路径是什么？ |
| Failure/blocker | What stopped progress, and what unblocks it? | 失败/阻塞 | 什么阻止了推进，如何解除？ |
| Bug diagnosis | Is the cause established, and does the fix cover the scope? | Bug 诊断 | 根因是否成立，修复是否覆盖？ |
| Incident/postmortem | What was the impact, mechanism, recovery, and durable learning? | 事故/复盘 | 影响、机制、恢复与长期改进是什么？ |
| Technical decision | Which option should be chosen, and why? | 技术决策 | 该选哪个方案，为什么？ |
| Review/release | Can the change pass the next delivery gate? | 评审/发布 | 能否通过下一交付门槛？ |
| Performance comparison | Is the metric comparable and materially improved? | 性能对比 | 数据是否可比，提升是否有意义？ |

Templates and examples are in [`references/report-types.md`](references/report-types.md). Strict measurement rules are in [`references/performance-comparison.md`](references/performance-comparison.md).

## Output modes / 输出模式

交互式 Codex CLI/TUI、Codex App/chat、IDE chat、PR、Issue 和文档默认使用 `markdown`。report-skill 负责生成干净的 Markdown source，宿主 presentation layer 负责标题、列表、代码、颜色和列宽的最终显示。

汇报正文禁止使用无序列表。多个事项使用阿拉伯数字、罗马数字、带圆圈数字、短标签段落或表格；嵌套事项使用 `1.1`、`1.2` 等编号。

`codex exec` 或其他 redirected stdout、纯文本终端、CI 日志和复制的命令输出使用 `terminal`。也可以通过 `REPORT_FORMAT=terminal` 或 `REPORT_FORMAT=markdown` 显式选择。

report-skill 不能替宿主安装或调用 Markdown renderer。如果交互式 Codex 界面显示原始 Markdown 标记，应保留 Markdown source 并把它视为 client presentation-path 问题；不要让 Skill 静默降级。排障期间可以显式请求 terminal compatibility fallback。不能把 ANSI 控制字符写回报告正文；目标要求 ASCII-only 时，用不带方括号的 `PASS`、`WARN`、`BLOCKED`、`TODO` 或 `INFO` 替换 emoji。

### Markdown format / Markdown 格式

Adapt this structure; do not fill it mechanically.

```markdown

## 结论 ✅

<result versus target, verified impact, and current decision or boundary>

## 待实现

1. ⏳ <missing implementation or delivery artifact, next action, and completion condition>

## 待验证

1. ⏳ <implemented state, missing evidence, and pass condition>

## 变更

<behavioral delta, key paths, and intentionally unchanged scope>

## 证据

1. ✅ <test, measurement, and observation; explain what it proves>
2. ⚠️ <limitation and what it does not prove>

## 状态

<only relevant local / commit / push / deploy / production states>
```

### Terminal fallback / 终端降级格式

```text
============================================================
<short report title>
============================================================

结论 ✅
  <target result, verified impact, and current boundary>

证据
  ✅ <test, measurement, observation, or artifact>
  ⚠️ <limitation and what it does not prove>

状态
  <working tree / commit / push / deploy / production states>

待实现
  ⏳ <missing implementation or delivery artifact, next action, and completion condition>

待验证
  ⏳ <implemented state, missing evidence, and pass condition>
============================================================
```

终端模式不要使用 Markdown 表格、链接、引用符号、粗体标记或依赖 CJK 宽度对齐的表格；长路径和命令应换行并保持缩进。

## Example / 示例

```markdown

## 结论 ⚠️

目录滚动高亮已修复；Chromium 验收通过，Safari 尚未验收，因此当前可交接但不能声称跨浏览器完成。

## 证据

1. ✅ `pnpm test toc` 通过，覆盖激活区间计算。
2. ✅ Chromium 逐段滚动 6 个标题均正确切换。

## 状态

仅本地修改，未提交、未推送。

## 待验证

1. ⏳ 滚动高亮已实现并通过 Chromium 验收；Safari 尚未执行。完成条件：6 个标题全部正确切换。

## 风险

1. ⚠️ WebKit 行为可能不同 → Safari 用户可能看到错误高亮 → 合并前完成 Safari 验收。
```

## Repository layout / 仓库结构

```text
SKILL.md                                  Runtime reporting rules / 运行规则
references/report-types.md                Decision-specific formats / 场景模板
references/reporting-principles.md        Public-source synthesis / 公开资料研究
references/performance-comparison.md      Comparable measurement rules / 性能对比规则
agents/openai.yaml                        Agent-facing metadata / Agent 元数据
```

## License / 许可

No license file is currently included. Add an explicit license before distributing this Skill outside the intended team or personal environment.

当前仓库未包含许可证文件。若要向团队外或公开分发，请先补充明确的 License。
