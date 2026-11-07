# Performance Comparison

Use this workflow for package size, installed size, memory, CPU, startup time, latency, throughput, battery, network, or other resource/performance reports. Start by naming the target or decision the measurement informs; a statistically valid delta is not automatically a meaningful user or business improvement.

## 1. Establish the comparison pair

Record both `before` and `after` with:

- artifact or commit identity, version, architecture, and build mode;
- machine, OS, power mode, and relevant tool version;
- workload and state, such as cold start, warm start, idle after 60 seconds, fixed page set, or fixed request set;
- included process tree or service boundary;
- metric definition, command/tool, unit, sample count, and aggregation method.
- target or acceptance threshold, when one exists, plus the user or operational consequence the metric is expected to influence.

Treat the current measurement as a new baseline when no raw, compatible `before` evidence is available. Do not reconstruct a precise historical number from memory, screenshots without units, or a different metric.

## 2. Apply comparison gates

Calculate a delta only when these gates match or the difference is explicitly normalized:

1. Same metric semantics: compare RSS with RSS and Physical Footprint with Physical Footprint. Never use their ratio as an improvement claim.
2. Same scope: compare the same app/process tree. State whether embedded services, helpers, extensions, Runway, or background agents are included.
3. Same workload and lifecycle state: do not compare idle CPU with page-load peak, or cold start with warm start.
4. Same artifact dimension: compare DMG with DMG and installed App with installed App; do not compare compressed and expanded sizes.
5. Same architecture and build mode: keep arm64/x64 and Debug/Release separate.
6. Same measurement window: use comparable duration, delay, sample count, and aggregation such as median, p95, max, or stable range.

If a gate fails, write `不可直接比较` and state the exact mismatch plus the next measurement needed.

## 3. Calculate and interpret

For lower-is-better metrics such as size, memory, CPU, startup time, and latency:

```text
absolute_delta = after - before
improvement_percent = (before - after) / before * 100%
```

For higher-is-better metrics such as throughput:

```text
absolute_delta = after - before
improvement_percent = (after - before) / before * 100%
```

Keep adequate precision for the source data, normally one decimal place for percentages. Distinguish:

- measurement change: the observed delta;
- attribution: whether evidence proves the code change caused it;
- practical significance: whether the change matters to users or operations;
- noise: repeated-run variation or an unknown confidence interval.

Do not turn a proxy into the final outcome. For example, lower startup time may improve perceived responsiveness, but that user impact remains unverified until it is measured or observed under a defined acceptance path.

Do not call a single noisy sample an optimization or regression. Prefer at least 3 samples for stable resource readings and repeated runs with median plus range or p95 for timing metrics.

## 4. Report format

Use the selected report-for-human output mode. Markdown mode is the default and may use the smallest useful table:

```markdown
## 结论 ⚠️

<result versus target; improved / regressed / unchanged within observed noise / new baseline only; practical consequence>

## 对比条件

<artifact, machine, architecture, workload, scope, method, samples>

| Metric | Before | After | Delta | Change | Judgment |
|---|---:|---:|---:|---:|---|
| Installed App | 600 MB | 428 MB | -172 MB | -28.7% | improved |
| Physical Footprint | unavailable | 596 MB | — | — | baseline only |

## 归因

<what evidence links the change to the implementation; unknown when not proved>
```

Terminal mode uses labeled metric blocks:

```text
============================================================
Performance comparison
============================================================

结论 ⚠️
  <result versus target; practical consequence>

对比条件
  <artifact, machine, architecture, workload, scope, method, samples>

Installed App
  before: 600 MB
  after: 428 MB
  delta: -172 MB (-28.7%)
  judgment: improved

Physical Footprint
  before: unavailable
  after: 596 MB
  judgment: baseline only

归因
  <what evidence links the change to the implementation>
============================================================
```

For a first measurement, state `当前只能建立 baseline，不能声称提升百分比`. Preserve enough raw evidence for the next run to reuse the exact workload and commands.

## 5. Chromium-style multi-process apps

- Prefer a process-tree Physical Footprint or platform-equivalent metric for actual memory pressure.
- Report RSS only as an upper-bound/process accounting view when shared pages may be counted repeatedly.
- Separate stable idle CPU from transient activity peaks and state that macOS `100% CPU` is approximately one fully occupied logical core.
- Record the number and roles of browser, renderer, GPU, utility, crash handler, and embedded-service processes.
- State explicitly when Runway, server, extensions, or other product-owned processes are absent; absence makes a whole-product comparison incomplete.
