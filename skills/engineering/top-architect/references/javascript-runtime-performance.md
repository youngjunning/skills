# JavaScript Runtime Performance

Use this reference when JavaScript or TypeScript runtime memory, CPU, latency, allocation, caching, or hot-path behavior materially affects an architecture decision. The goal is a reproducible diagnosis and the smallest fix at the correct ownership boundary.

## 1. Define the performance contract

Before changing code, record:

- the user or operational outcome that is failing;
- the executable, JavaScript runtime and exact version;
- development, test, bundled, compiled, or production build mode;
- process scope, including child processes and excluded processes;
- workload, data size, concurrency, session count, and lifecycle point;
- warmup, sampling interval, observation window, repetitions, and aggregation;
- baseline, target, allowed regression, and stop condition.

Use comparable metrics. RSS, private or physical footprint, heap used, heap capacity, external/native memory, array buffers, and process-tree totals answer different questions. Record more than one when diagnosing, but choose one primary metric for the decision.

Do not infer runtime savings from bundle size, executable size, minification, tree shaking, or fewer installed dependencies. Those changes can improve delivery or startup without reducing retained memory after the same workload.

## 2. Classify the observed memory

Separate these shapes before naming a cause:

1. **Startup footprint:** modules, runtime infrastructure, static registries, prompts, schemas, and eagerly initialized clients retained before useful work.
2. **Steady-state footprint:** objects intentionally kept after warmup for the normal operating window.
3. **Per-unit growth:** memory retained per session, conversation, connection, tab, request, model, toolset, or workspace.
4. **Transient peak:** buffers, serialization, screenshots, large tool results, streams, compaction copies, or concurrent requests that become collectible.
5. **Native or external memory:** sockets, runtime internals, image buffers, WebAssembly, database clients, browser automation, or native libraries not fully represented by JavaScript heap usage.
6. **Allocator retention:** freed objects whose pages remain reserved by the runtime. Stable post-GC plateaus can be healthy even when RSS does not immediately fall.

A leak claim requires repeated lifecycle evidence. One large heap snapshot, one long-lived process, or an RSS increase after a single operation is only a lead.

## 3. Audit ownership and lifetime first

For each long-lived resource, identify the owner and answer:

1. Where is it created?
2. What key makes it reachable?
3. What bounds its count or size?
4. Which success, error, timeout, cancellation, disconnect, replacement, and shutdown paths release it?
5. Is disposal idempotent, awaited, and observable?
6. Can an old instance remain reachable after a rebuild or configuration change?

Inspect sessions, conversations, agents, model/provider clients, MCP clients, browser/CDP sessions, WebSockets, streams, timers, event listeners, abort listeners, background tasks, registries, caches, logs, message histories, tool outputs, screenshots, and generated prompts.

Prefer an explicit lifecycle contract over periodic cleanup. Use TTL, LRU, count, byte, or tenant bounds only when inactive state must remain resident. State what happens at the bound: reject, evict, compact, persist, or degrade.

## 4. Reduce essential work before tuning syntax

Use this priority order:

1. Remove unintended retention and duplicated ownership.
2. Reduce the amount of data or number of live units.
3. Replace avoidable quadratic or repeated scans with a suitable algorithm or index.
4. Avoid repeated parsing, serialization, normalization, copying, and intermediate collections in measured hot paths.
5. Apply JavaScript micro-patterns only after the remaining path is both frequent and material.

For repeated lookups over large stable collections, build a `Set` or `Map` once at the owning lifetime. Do not rebuild the index per request or retain an unbounded index for one-off lookups.

For large data pipelines, combine adjacent `filter`, `map`, and `reduce` passes when intermediate arrays materially affect allocation or latency. Keep the clearer form for small or cold paths.

Memoize only pure or explicitly invalidated results. Every cache needs a key model, size or byte bound, expiry or invalidation rule, observability, and a reason its hit rate justifies retained memory. Prefer `WeakMap` only when object reachability is the intended lifetime and its non-enumerability is acceptable.

Cache deep property access, collection length, normalized strings, or parsed schemas only inside demonstrated tight loops. Prefer early returns and empty-input checks when they avoid material downstream work.

## 5. Preserve failure and cancellation semantics

Performance fixes must not weaken correctness. Verify:

- aborted streams stop producers and release consumers;
- timeouts cancel underlying work rather than only rejecting the caller;
- listener and timer cleanup happens on errors and partial initialization;
- session replacement disposes the old instance before making the new one authoritative;
- shutdown waits for required cleanup without hanging indefinitely;
- retries do not multiply clients, timers, or registrations;
- cleanup errors remain diagnosable and do not silently convert a failed operation into success.

Where a shared framework owns the lifecycle, add the cleanup or bounding contract there and cover it with a reusable regression test. Product code should configure policy, not fork the shared mechanism.

## 6. Use a falsifiable experiment

For suspected retained growth, use a repeated lifecycle such as:

`warm up → measure → create/use/delete N units → settle/GC → measure → repeat for several rounds`

Record per round:

- units created, completed, cancelled, failed, and explicitly deleted;
- live registry/session/cache counts;
- primary memory metric plus heap and external/native support metrics;
- peak and post-settle values;
- elapsed time, GC conditions, and runtime health errors.

Interpret the shape:

- a bounded rise followed by a stable plateau suggests warmup or allocator retention;
- growth proportional to live units may be intentional capacity cost;
- growth proportional to completed or deleted units indicates suspected retention;
- high peaks that recover suggest allocation pressure rather than a leak;
- unstable runtime, crash/retry loops, or mismatched workloads invalidate attribution.

Use heap snapshots, allocation profiles, retained paths, or runtime-specific diagnostics only after the process-level shape identifies which lifecycle to inspect. Do not assume V8-specific behavior for Bun or another JavaScript engine.

## 7. Compare options at the ownership boundary

For a consequential remediation, compare at least:

1. **Lifecycle fix:** dispose, evict, compact, or stop resources at the current owner.
2. **Architecture change:** move state, narrow the session, lazy-load a subsystem, isolate a process, or change a shared runtime contract.
3. **Capacity policy:** set a documented bound or restart/idle policy when retained state is intentional and recovery is safe.

Prefer the lifecycle fix when it removes accidental retention without changing user behavior. Choose an architecture change when ownership is wrong or the subsystem is not needed for most workloads. Use a capacity policy only when the retained state is essential, measurable, recoverable, and bounded.

## 8. Report what the evidence proves

Separate observation, inference, and recommendation. A useful performance conclusion states:

1. the comparable before and after values;
2. the workload and lifecycle scope;
3. the mechanism supported by profiling or retained-path evidence;
4. the user or operational impact;
5. what remains unverified;
6. the review trigger if workload, concurrency, runtime version, or architecture changes.

If no comparable baseline exists, establish one instead of inventing an improvement percentage. If the runtime is unhealthy, fix health first and rerun before attributing memory or CPU to the product architecture.
