---
name: browser-performance-audit
description: "Perform a browser tab performance audit: collect Navigation Timing, Core Web Vitals, resource loading, console errors, and DOM structure, then cross-validate and output prioritized optimization suggestions. Use when the user asks to evaluate page performance, diagnose slow loading, analyze memory leaks, or investigate long-session degradation."
---

# Browser Performance Audit

## When to Use

- User asks to "evaluate/audit/test page performance"
- User reports a page is slow, laggy, or consuming too much memory
- User wants to understand what's blocking first paint or interactivity
- User suspects long-session degradation (memory leak, DOM bloat)
- Keywords: 性能评测, 页面性能, 加载慢, Core Web Vitals, FCP, LCP, 内存泄漏, 长时劣化

## Prerequisites

- `builtin_browser` MCP tools must be available (javascript_tool, read_console_messages, read_page, read_network_requests, tabs_create, navigate)
- Call `qw_mcp_get` on each browser tool before first use in a session. Signatures differ: `tabs_create` takes **no arguments at all** and returns a new tabId, while `navigate`, `javascript_tool` and `read_network_requests` all require an explicit `tabId`.
- Never audit a tab that was already open. See the iron laws below — this is not a soft preference.

## Iron laws

These exist because ignoring them has already produced a fully fabricated
diagnosis. A real case: an audit reported FCP 4824ms, 130 first-screen scripts
and 6.7MB HTML, and derived two optimization proposals from those numbers. All of
it was wrong — sampling happened on a tab open ~19 minutes. After one clean
navigation the true values were FCP 908ms and 13 scripts, and both proposals were
void. The "2.8s gap between first-paint and FCP" that drove the whole analysis
was an artifact of the resource-timing 250-entry cap.

**1. Clean navigation is mandatory, not advisory.** For any first-load question,
create a fresh tab and navigate it yourself in the current turn. If page age is
large, the correct action is to re-navigate — **not** to ask the user whether to
proceed with an accumulated-state audit. There is no valid "continue anyway" path
for first-load metrics.

**2. `javascript_tool` forbids top-level `return`.** Its contract states the
result of the last expression is returned automatically and `return` must not be
used. Every multi-statement probe must be an IIFE. Getting `undefined` on a first
probe attempt almost always means it was written as bare statements — rewrite as
IIFE rather than concluding the API is unavailable.

**3. Count resources from `read_network_requests`, not resource timing.** The
page buffer caps at 250 entries and silently evicts the oldest. `read_network_requests`
is not bound by it. Use resource timing only for per-resource cache/protocol
probing, always alongside its truncation flag.

**4. Never present an accumulated metric as a first-screen figure.** DOM nodes,
`outerHTML` size, element counts and JS heap describe *right now*. Label each one
with its sample age.

**5. No proposal without a verified bottleneck.** See "Falsify before proposing".

## Steps

### 0. Clean navigation (required for first-load audits)

```
tabs_create                                    → returns tabId (no arguments)
read_network_requests { tabId, clear: true }    → drop stale records
navigate { tabId, url }
```

Immediately after navigation completes, raise the buffer for the new document:

```javascript
(() => { performance.setResourceTimingBufferSize(3000); return 'ok'; })()
```

Note this helps but does not guarantee completeness — the buffer cannot be
pre-set before the document exists, since the performance timeline is rebuilt per
document. Treat resource timing as best-effort regardless.

If the target requires authentication, a fresh tab inherits the user's session,
which is the reason to use `builtin_browser` rather than an isolated automation
profile. If the page redirects to a login form, stop and report it — do not
measure the login page.

Skip this step only when the user explicitly asks about accumulated runtime state
(long-session degradation), in which case label the entire report accordingly.

### 1. Environment Confirmation

Identify the target tab and check page age:

```javascript
// Inject via javascript_tool
(() => {
  const nav = performance.getEntriesByType('navigation')[0] || {};
  const now = performance.now();
  const pageAgeMs = now;
  const ua = navigator.userAgent;
  return JSON.stringify({
    url: location.href,
    pageAgeSeconds: Math.round(pageAgeMs / 1000),
    navigationType: nav.type, // "navigate", "reload", "back_forward"
    ua,
    warning: pageAgeMs > 300000 ? "Page has been open > 5 min. Resource Timing buffer may have overflowed; DOM and heap reflect accumulated state, not first-load. Recommend reload for accurate first-load audit." : null
  });
})()
```

If `warning` is non-null and the user asked a first-load question, go back to
step 0 and re-navigate. Do **not** offer to proceed with the aged sample — that
is exactly how the fabricated-diagnosis case happened. Only proceed on an aged
document when the user explicitly asked about accumulated runtime state, and then
label every number in the report with its sample age.

### 2. Navigation & Rendering Timing

```javascript
(() => {
  const nav = performance.getEntriesByType('navigation')[0] || {};
  const paint = {};
  performance.getEntriesByType('paint').forEach(e => { paint[e.name] = Math.round(e.startTime); });

  return JSON.stringify({
    protocol: nav.nextHopProtocol,
    redirectTime: Math.round((nav.redirectEnd || 0) - (nav.redirectStart || 0)),
    dnsTime: Math.round((nav.domainLookupEnd || 0) - (nav.domainLookupStart || 0)),
    tcpTime: Math.round((nav.connectEnd || 0) - (nav.connectStart || 0)),
    tlsTime: nav.secureConnectionStart > 0 ? Math.round((nav.connectEnd || 0) - nav.secureConnectionStart) : 0,
    ttfb: Math.round(nav.responseStart || 0),
    responseTime: Math.round((nav.responseEnd || 0) - (nav.responseStart || 0)),
    domInteractive: Math.round(nav.domInteractive || 0),
    domContentLoaded: Math.round(nav.domContentLoadedEventEnd || 0),
    loadComplete: Math.round(nav.loadEventEnd || 0),
    firstPaint: paint['first-paint'] || null,
    firstContentfulPaint: paint['first-contentful-paint'] || null,
    transferSize: nav.transferSize,
    encodedBodySize: nav.encodedBodySize,
    decodedBodySize: nav.decodedBodySize
  });
})()
```

### 3. Core Web Vitals & Long Tasks

```javascript
(() => {
  // LCP - read from existing entries
  const lcpEntries = performance.getEntriesByType('largest-contentful-paint');
  const lcp = lcpEntries.length > 0 ? Math.round(lcpEntries[lcpEntries.length - 1].startTime) : null;

  // CLS - approximate from layout-shift entries
  const layoutShifts = performance.getEntriesByType('layout-shift');
  let cls = 0;
  let sessionValue = 0;
  let sessionEntries = [];
  layoutShifts.forEach(entry => {
    if (!entry.hadRecentInput) {
      if (sessionEntries.length && entry.startTime - sessionEntries[sessionEntries.length - 1].startTime > 5000) {
        cls = Math.max(cls, sessionValue);
        sessionValue = 0;
        sessionEntries = [];
      }
      sessionValue += entry.value;
      sessionEntries.push(entry);
    }
  });
  cls = Math.max(cls, sessionValue);

  // Long Tasks
  const longTasks = performance.getEntriesByType('longtask');
  const totalBlockingTime = longTasks.reduce((sum, t) => sum + Math.max(0, t.duration - 50), 0);

  return JSON.stringify({
    lcp,
    cls: Math.round(cls * 10000) / 10000,
    longTaskCount: longTasks.length,
    totalBlockingTime: Math.round(totalBlockingTime),
    longestTask: longTasks.length > 0 ? Math.round(Math.max(...longTasks.map(t => t.duration))) : 0
  });
})()
```

Note: LCP and layout-shift entries require `PerformanceObserver` with `buffered: true` to have been registered. If entries are empty, it means no observer was set up. In that case, note the limitation and skip.

### 4. Resource Loading Analysis

**Authoritative resource inventory comes from `read_network_requests`, not from
resource timing.** Call it first — it is not bound by the page's 250-entry buffer:

```
read_network_requests { tabId, limit: 1000 }
```

Use it to establish true counts by type, failed requests, and total volume. Only
then use resource timing below for per-resource cache/protocol detail, and treat
its aggregate counts as a lower bound whenever `bufferFull` is true.

```javascript
(() => {
  const resources = performance.getEntriesByType('resource');
  const bufferFull = resources.length >= 250; // Chrome default limit

  const byType = {};
  const byProtocol = {};
  let cacheHits = 0;
  let totalTransfer = 0;
  let totalDecoded = 0;

  resources.forEach(r => {
    const type = r.initiatorType || 'other';
    if (!byType[type]) byType[type] = { count: 0, transferKB: 0, avgDurationMs: 0, durations: [] };
    byType[type].count++;
    byType[type].transferKB += (r.transferSize || 0) / 1024;
    byType[type].durations.push(r.duration);

    const proto = r.nextHopProtocol || '(empty)';
    byProtocol[proto] = (byProtocol[proto] || 0) + 1;

    if (r.transferSize === 0 && r.decodedBodySize > 0) cacheHits++;
    totalTransfer += r.transferSize || 0;
    totalDecoded += r.decodedBodySize || 0;
  });

  // Compute averages
  Object.values(byType).forEach(v => {
    v.avgDurationMs = Math.round(v.durations.reduce((a, b) => a + b, 0) / v.durations.length);
    v.transferKB = Math.round(v.transferKB);
    delete v.durations;
  });

  return JSON.stringify({
    totalResources: resources.length,
    bufferFull,
    bufferWarning: bufferFull ? "Resource Timing buffer is full (250). Early entries may have been evicted. Numbers below are INCOMPLETE." : null,
    cacheHitRate: resources.length > 0 ? Math.round(cacheHits / resources.length * 100) + '%' : 'N/A',
    totalTransferKB: Math.round(totalTransfer / 1024),
    totalDecodedKB: Math.round(totalDecoded / 1024),
    byInitiatorType: byType,
    byProtocol
  });
})()
```

### 5. DOM Structure & Memory

```javascript
(() => {
  const allElements = document.querySelectorAll('*').length;
  const scripts = document.querySelectorAll('script[src]').length;
  const inlineScripts = document.querySelectorAll('script:not([src])').length;
  const stylesheets = document.querySelectorAll('link[rel="stylesheet"]').length;
  const iframes = document.querySelectorAll('iframe').length;
  const images = document.querySelectorAll('img').length;
  const maxDepth = (() => {
    let max = 0;
    const walk = (el, depth) => {
      if (depth > max) max = depth;
      if (depth > 32) return; // safety cap
      for (const child of el.children) walk(child, depth + 1);
    };
    walk(document.documentElement, 0);
    return max;
  })();

  // Memory (Chromium only)
  const memory = performance.memory ? {
    usedJSHeapMB: Math.round(performance.memory.usedJSHeapSize / 1048576),
    totalJSHeapMB: Math.round(performance.memory.totalJSHeapSize / 1048576),
    heapLimitMB: Math.round(performance.memory.jsHeapSizeLimit / 1048576)
  } : null;

  return JSON.stringify({
    totalDOMNodes: allElements,
    externalScripts: scripts,
    inlineScripts,
    stylesheets,
    iframes,
    images,
    maxDOMDepth: maxDepth,
    memory
  });
})()
```

### 6. Console Errors

Call `read_console_messages` on the target tab. Categorize messages by level (error, warning). Focus on:

- Uncaught exceptions and unhandled promise rejections
- Failed network requests (4xx/5xx, CORS errors)
- Deprecation warnings that may affect future compatibility

### 7. Cross-Validation

After collecting all data, perform these sanity checks:

1. **Buffer overflow detection**: If `bufferFull` is true AND navigation timing shows page age > 60s, warn that resource data is incomplete and first-load analysis cannot be done from current state.
2. **Timing consistency**: Compare `firstContentfulPaint` with the earliest resource `startTime`. If the earliest resource startTime is orders of magnitude larger than FCP (e.g., > 100x), the buffer has rotated and early resources are lost — do NOT use resource timing for waterfall analysis.
3. **Accumulated state detection**: If DOM nodes > 5000 but external scripts < 20, the page likely uses keep-alive/SPA routing that accumulates DOM without new script loads. Flag this as "accumulated state" and note that DOM count reflects runtime, not first-load.
4. **Memory baseline**: If `usedJSHeapMB` > 200MB on a page open < 5 minutes, flag as potential memory issue. If page has been open > 30 minutes and heap is > 100MB, note that delta from initial load would be needed to judge leak.

### 7.5 Falsify before proposing

For every candidate optimization, write down three things and **drop the proposal
if any of them fails**:

The measured evidence that the bottleneck exists, quoted with metric name and
value. The counter-test that would disprove it, and its result. Whether that
evidence is a true first-screen metric or an accumulated one — if accumulated, the
proposal is void until re-measured on a clean navigation.

Worked example of a correctly killed proposal. Candidate: enlarge disk/code cache
to speed up boot scripts. Evidence sought: boot resources with non-zero
`transferSize` and meaningful `duration`. Actual probe result: `transferSize: 0`,
`decodedBodySize: 11440`, `proto: h2`, `duration: 2.6ms` — already a cache hit.
The problem does not exist; the proposal was dropped before being presented.

Two recurring premise failures worth checking explicitly. A caching proposal is
void if the targeted resources already show `transferSize === 0` — and note that
caching changes carry cross-session staleness risk, raising the bar further. A
connection-level proposal (preconnect, domain sharding, reducing request count)
is largely void if `nextHopProtocol` is already `h2`/`h3`, since multiplexing has
captured most of that gain.

When an earlier number turns out wrong, lead the report with the correction and
show a before/after table. A plainly stated retraction is far cheaper than a wrong
recommendation that reaches implementation.

### 8. Report Template

Structure the final output as:

```
## Performance Audit Summary

**Target**: [URL]
**Measured at**: [page age] after navigation
**Type**: [first-load | accumulated-state]

### Key Metrics
| Metric | Value | Rating |
|--------|-------|--------|
| TTFB | Xms | Good/Needs Work/Poor |
| FCP | Xms | ... |
| LCP | Xms | ... |
| CLS | X | ... |
| TBT | Xms | ... |
| DOM Nodes | X | ... |
| JS Heap | XMB | ... |

Rating thresholds (per web.dev):
- FCP: Good < 1800ms, Poor > 3000ms
- LCP: Good < 2500ms, Poor > 4000ms
- CLS: Good < 0.1, Poor > 0.25
- TBT: Good < 200ms, Poor > 600ms
- TTFB: Good < 800ms, Poor > 1800ms

### Critical Issues
[Items that severely impact UX — must fix]

### Important Improvements
[Items with measurable benefit — should fix]

### Suggestions
[Nice-to-have optimizations — consider fixing]

### Data Validity Notes
[Any cross-validation warnings about measurement accuracy]
```

For each issue, include: what it is, estimated impact, who owns the fix (browser-layer vs site-layer), and risk assessment.

## Pitfalls

- **`javascript_tool` rejects top-level `return`**: The tool returns the value of the last expression and its contract explicitly forbids `return`. Any multi-statement probe must be wrapped as `(() => { ... })()`. An `undefined` result on a first attempt is almost always this mistake, not a missing API.
- **Recognizing buffer truncation in the wild**: The signal is an entry count pinned at exactly 250 plus `startTime` values orders of magnitude larger than any paint timestamp (e.g. 10^6 ms). The downstream symptom is a "mysterious gap" between paint and resource completion that no code path explains — that gap is the artifact, not a real bottleneck.
- **Recognizing keep-alive accumulation**: DOM nodes, heap and element counts all grow with page age while paint timing stays constant across clean reloads. Confirm by comparing two clean navigations against one aged sample: if the two clean runs agree and the aged one is the outlier, the aged numbers are accumulation, not regression.
- **Large HTML size is not proof of server-side data injection**: On keep-alive architectures, switching views often only sets `content-visibility: hidden` and leaves the old subtree in the document, so `outerHTML` size is cumulative by design. Verify what the server actually returned before blaming the response.
- **Long-session degradation needs two phases, not one sample**: Separate one-time mount cost from a genuine leak by sampling after each incremental view activation, then holding the page idle and continuing to sample. A curve that plateaus once all views are active means bounded mount cost; continued growth while idle means a real leak. With only one phase measured, both hypotheses stay open and neither should be asserted.
- **`Glob` silently returns nothing for ignore-excluded paths**: Zero matches looks identical to "directory does not exist". When a directory is known or likely to exist but `Glob` finds nothing, re-check with Bash `ls`/`find` before concluding it is absent.
- **Resource Timing Buffer 250-entry limit**: Chrome's default buffer holds 250 resource entries. On heavy SPA pages, early entries get evicted after a few minutes. Always check `bufferFull` before drawing conclusions from resource data. A page that loaded 130 scripts at boot may show only 30 if measured late.
- **Accumulated-state measurement bias**: On keep-alive SPA pages (e.g., using `content-visibility: hidden`), DOM only grows. Measuring DOM nodes or `outerHTML` size after the page has been open reflects accumulated state, NOT first-load cost. Always note page age.
- **`performance.memory` is Chromium-only**: Firefox and Safari don't expose it. The API is also deprecated in favor of `measureUserAgentSpecificMemory()` (requires cross-origin isolation). Check availability before using.
- **`transferSize: 0` ambiguity**: This can mean either disk cache hit (when `decodedBodySize > 0`) OR CORS opaque response (when `decodedBodySize === 0`). Always check `decodedBodySize` to distinguish.
- **LCP/CLS entries may be empty**: These require `PerformanceObserver` with `buffered: true` to have been set up by the page or injected early. If the page doesn't register one, and we inject after load, entries may be unavailable. Note this limitation rather than reporting "LCP = 0".
- **SPA navigation breaks Navigation Timing**: If the page does client-side routing, `performance.getEntriesByType('navigation')` still reflects the initial hard navigation, not subsequent route changes. Clarify which navigation is being measured.

## Verification

Every item below must be a yes before writing any conclusion.

- Navigation was performed in this session (step 0) and reported page age is small
- Paint and navigation timing pass the order-of-magnitude sanity check against each other
- Every DOM/heap number is explicitly labeled as accumulated state, with its sample age
- Resource counts come from `read_network_requests`; any resource-timing figure is presented together with its `bufferFull` flag
- Each proposal names its supporting metric and its counter-test result (step 7.5)
- Any earlier conclusion contradicted by clean data is explicitly retracted, not quietly dropped
- Confirm all injected scripts are pure reads with no side effects (no DOM mutation, no network requests, no `localStorage` writes)
- After Step 7 cross-validation, if any warning fires, prominently note it in the report rather than presenting potentially invalid data as fact
- Compare `nav.startTime` (should be 0) with first resource entry's `startTime` — if the gap is unreasonably large (> 60s), the measurement is from an accumulated session
- For memory leak investigation, take two measurements 5+ minutes apart and compare delta rather than relying on a single snapshot
