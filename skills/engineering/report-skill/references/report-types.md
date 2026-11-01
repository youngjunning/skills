# Report Types

Choose the type by the next reader’s decision. Do not combine types unless the same reader genuinely needs both decisions. Keep the conclusion and action layer short; add detail only when it changes the judgment.

The examples below define content and section selection, not a mandatory literal layout. Select the output mode using `SKILL.md`. Markdown mode is the default: turn labels such as `【结论】` into `## 结论` headings and use numbered, Roman-numeral, or circled-number lists where helpful; never use unordered lists. In `terminal` mode, render them with plain-text sections and status emoji; convert tables into labeled metric blocks. Keep the same emoji-only status vocabulary in both modes.

## 1. Leadership or project status

Use when a manager, stakeholder, or cross-functional owner needs the result versus target, impact, forecast, and decisions—not a file-level handoff.

```text
【结论】灰度目标已达成：7 天内覆盖率从 20% 提升到 100%，核心成功率保持 99.95%；可以按计划全量。
【目标与结果】目标：8 月 19 日前全量且成功率 ≥99.9%；实际：按期、100%、99.95%。
【影响】1,240 个日活任务已切换；未观察到失败率上升。
【关键判断】两次超时来自旧客户端重试策略，不是新链路容量不足；旧客户端保护继续保留一周。
【需要决定】建议今天全量；若同意，由发布 Owner 在 18:00 前执行。
【待验证】发布覆盖率和成功率已验证；用户留存需要完整 14 天窗口。完成条件：8 月 26 日按同口径复盘留存指标。
【风险】Warning：留存指标至少需要 14 天窗口 → 当前不能声称业务留存提升 → 8 月 26 日复盘。
```

Use a compact scorecard only when several repeated fields need comparison. Markdown mode may use a table:

| Dimension | Target | Actual | Judgment |
| --- | ---: | ---: | --- |
| Delivery | Aug 19 | Aug 19 | met |
| Coverage | 100% | 100% | met |
| Success rate | >=99.9% | 99.95% | met |

Terminal mode uses labeled rows:

```text
Delivery
  target: Aug 19
  actual: Aug 19
  judgment: met

Coverage
  target: 100%
  actual: 100%
  judgment: met
```

## 2. Completed engineering delivery

Use when another engineer needs to merge, verify, release, or continue a completed change.

```text
【结论】目录滚动高亮已修复；Chromium 验收通过，Safari 尚未验收，因此当前可交接但不能声称跨浏览器完成。
【变更】src/toc.ts、src/article.css；未改路由和数据结构。
【证据】pnpm test toc 通过，覆盖激活区间计算；Chromium 逐段滚动 6 个标题均正确切换。
【状态】仅本地修改，未提交、未推送。
【待验证】滚动高亮已实现并通过 Chromium 验收；Safari 尚未执行。完成条件：6 个标题全部正确切换。
【风险】Warning：WebKit 的 sticky/scroll 行为可能不同 → Safari 用户可能看到错误高亮 → 合并前完成 Safari 验收。
```

## 3. In progress

Use when the work has a concrete intermediate landing point. Report the achieved outcome, forecast, and critical path; do not inventory every completed task.

```text
【当前落点】Adapter 接口和 Codex Provider 已迁移；现有 Codex 路径的 18 条用例通过。
【待实现】第二个 Provider 和失败重试尚未实现；流式字段契约确定后补齐映射与重试逻辑。
【待验证】现有 Codex Provider 已通过单元测试，但端到端验收尚未执行；第二个 Provider 完成后再验证两条 Provider 路径。
【关键路径】Provider Owner 确认字段 → 补映射 → 跑两条集成用例。
【阻塞】流式字段契约未确认 → 阻塞第二个 Provider 映射 → Provider Owner 提供字段定义后解除。
【状态】仅本地修改，未提交、未推送。
```

## 4. Failure or blocker

Use when permission, environment, dependency, or a current fault prevents the requested next step.

```text
【结论】实现与本地测试已完成，但目标环境 Smoke Test 被 403 阻塞，因此不能给出可发布判断。
【根因】当前 token 缺少 required scope；请求结构已由本地 mock 验证。
【影响】阻塞目标环境验收，不影响已完成的本地实现。
【已排除】刷新 token 和切换 staging 凭证均返回同一 scope 错误。
【需要提供】凭证 Owner 补充 scope 或提供可用 token。
【阻塞】缺少 required scope → 无法执行 Smoke Test → 可用凭证到位后解除。
【待验证】实现和本地 mock 已通过；目标环境 Smoke Test 尚未执行。完成条件：使用具备 required scope 的凭证完成目标环境验证。
【风险】Warning：真实鉴权和网关行为仍未知 → 本地通过的请求可能在目标环境失败 → 发布前完成 Smoke Test。
```

## 5. Bug diagnosis

Use when the reader needs to judge the cause, affected scope, and whether the proposed or completed fix covers the observed problem.

```text
【结论】中文输入法确认候选词时误发送，根因是 keydown 未检查 composition 状态；最小修复已覆盖当前复现路径。
【范围】Chrome 与桌面 WebView 可复现；英文输入不受影响。
【证据】最小页面稳定复现；加入 isComposing 与 keyCode 229 guard 后，拼音、五笔、英文 Enter、Shift+Enter 均通过手测。
【待实现】WebDriver composition 自动化用例尚未编写；完成条件：四条输入路径进入 CI。
【风险】Info：当前回归依赖手测 → 后续键盘事件改动可能让问题复发且不被 CI 捕获 → 补自动化用例。
```

## 6. Incident or postmortem

Use for a production or operational failure that needs impact, mechanism, recovery, and durable learning. Keep it blameless and system-focused.

```text
【结论】14:07–14:26 的发布导致 12.4% 请求失败；14:26 回滚后恢复。直接触发是 schema 不兼容，系统性原因是灰度未覆盖旧客户端流量。
【影响】18,420 次请求失败；未发现数据丢失。
【时间线】14:07 发布；14:11 首次告警；14:18 定位；14:26 回滚；14:29 指标恢复。
【根因】新字段被服务端按必填读取，但 31% 旧客户端未发送；发布检查只验证了新客户端。
【修复】字段读取改为向后兼容，回滚已完成；目标环境回放通过。
【待实现】发布 Owner 在下次发布前把旧客户端流量加入灰度门槛；完成条件：门槛在 CI 中阻止不兼容 schema。
【风险】Warning：历史 schema 仍有两处同类假设 → 可能再次触发兼容故障 → 一周内完成同类扫描并补契约测试。
```

Do not name a person as “root cause”. Name the action or condition, then explain why the system allowed it to reach users.

## 7. Technical decision

Use when an owner must choose a path before work continues. State the recommendation, objective, options, evidence, tradeoffs, and reversibility.

```text
【建议】选方案 B：保留 SQLite，新增异步索引表。
【目标】本版本把 p95 查询控制在 200 ms 内，同时避免不可逆的数据迁移。
【依据】现有压测下 B 为 146 ms；A 为 91 ms，但需要 3 周迁移且回滚复杂。
【代价】复杂查询仍由应用层处理；数据增长到当前 3 倍时需重新评估。
【可逆性】B 可删除索引表回退；A 的双写迁移不可一键回退。
【需要决定】请 Owner 确认 B；确认后进入实现。
【风险】Warning：数据量增长会抬高应用层查询延迟 → 达到 p95 180 ms 时启动第二阶段评估。
```

## 8. Review or release

Use when deciding whether code can merge, enter an environment, release, or be accepted.

```text
【结论】暂不发布：构建和 migration dry-run 通过，但目标窄屏验收是发布门槛且尚未完成。
【Review】未发现代码级阻断问题；空状态在 320 px 宽度缺少证据。
【证据】Release 构建通过；migration dry-run 0 error；桌面 Chrome 验收通过。
【回滚】保留上一镜像标签，migration 向后兼容。
【阻塞】窄屏验收未完成 → 阻塞生产部署 → 320 px 与 375 px 截图验收通过后解除。
【待验证】实现和 Release 构建已完成；补齐 320 px 与 375 px 两档窄屏截图，验收通过后再发起部署。
```

## 9. Performance comparison

Use when the reader must judge package size, memory, CPU, startup time, latency, throughput, battery, network, or another measurable resource. Follow [performance-comparison.md](performance-comparison.md); never calculate progress from incompatible samples.

```text
【结论】安装体积下降 28.7%；内存只有当前 baseline，不能判断提升。
【对比条件】同一 arm64 Release 构建、同一安装口径；内存旧数据为 RSS、当前数据为 Physical Footprint，口径不一致。
Installed App
  before: 600 MB
  after: 428 MB
  delta: -172 MB (-28.7%)
  judgment: improved

Physical Footprint
  before: unavailable
  after: 596 MB
  judgment: baseline only
【归因】安装体积变化与目标 artifact 一致；内存变化未证明。
【阻塞】缺少兼容的旧内存样本 → 阻塞内存前后结论 → 同条件重测旧版本后解除。
【待验证】当前版本 Physical Footprint baseline 已采集；旧版本同口径样本尚未采集。完成条件：同条件重测旧版本并形成可比结论。
```

## Do not use a report

Answer directly for a single command result, a brief factual answer, or a simple clarification. A concise answer is better than a ceremonial report with empty sections.
