# Web architecture pattern lens

Use this reference when a consequential architecture decision involves browser rendering, frontend state, component boundaries, JavaScript delivery, or user-perceived performance. It distills the decision value of the PatternsDev skill collection without turning every implementation pattern into an architecture requirement.

## Operating rules

1. Start with a user journey, not a framework. Name the content, interaction, freshness, personalization, SEO, accessibility, device, network, and hosting constraints that change the decision.
2. Separate five layers that are often conflated: rendering, data/state ownership, component composition, resource delivery, and runtime behavior.
3. Prefer the simplest viable pattern. A pattern earns its place by removing an observed cost or enabling a required capability.
4. Record the downside and removal condition. Every cache, global store, event bus, hydration boundary, and abstraction creates a new failure or debugging surface.
5. Prove claims in the target path. Use production-like data, network and device profiles, real hosting/proxy behavior, browser traces, bundle analysis, and accessibility checks as appropriate.
6. Treat framework APIs, library preferences, browser support, and performance metrics as time-sensitive. Verify current official documentation before prescribing version-specific code.

## 1. Choose the rendering boundary

Choose per route or stable page class. Do not force one rendering mode across the whole product when journeys have materially different constraints.

| Direction | Prefer when | Main cost or failure mode | Evidence needed |
| --- | --- | --- | --- |
| Static rendering / SSG | Content is public, cacheable, and does not vary per request | Build time, invalidation, and stale content | Freshness SLA, build duration, cache behavior, representative page size |
| Incremental static regeneration | Content is mostly static but controlled staleness is acceptable | Revalidation semantics and temporarily divergent versions | Revalidation window, invalidation test, stale-content consequence |
| SSR | Public or personalized HTML must be current per request | Server capacity, TTFB, cache complexity, and hydration cost | Server latency distribution, cache hit rate, concurrency, failure behavior |
| Streaming SSR | A useful shell can arrive before slow page regions and the delivery path preserves streaming | Suspense and error-boundary complexity; proxies or platforms may buffer | First-byte and first-content trace through the real CDN/proxy path |
| CSR | The product is interaction-heavy, commonly authenticated, and SEO or immediate HTML is not critical | Blank or incomplete first view, client CPU, bundle and data waterfalls | Cold-load budget on representative devices and networks |
| Islands | Most content is static and only isolated regions need interactivity | Cross-island state and coordination can become awkward | Client-JavaScript reduction and proof that islands remain independently owned |
| React Server Components | Non-interactive work and data access can remain on the server in a supporting framework | Server/client boundary complexity, serialization, caching, framework coupling | Client bundle delta, boundary correctness, mutation and cache behavior |
| Progressive or selective hydration | Server-rendered regions have different interaction priorities | More boundaries, fallbacks, and hard-to-reproduce hydration failures | Interaction readiness for critical regions and hydration-error telemetry |

Decision sequence:

1. Classify route data as static, periodically fresh, per-request dynamic, personalized, or real-time.
2. Mark which content must exist in initial HTML and which controls must be interactive immediately.
3. Establish cache and invalidation ownership before choosing SSG, ISR, SSR, or a server-component model.
4. Add streaming or selective hydration only when a trace shows a blocked shell or interaction, and the hosting path supports the mechanism.
5. Keep a simple CSR path for authenticated tools when it meets the actual load and device budget.

Do not assume that server rendering eliminates client JavaScript, that streaming improves every page, or that a hybrid model is free. Rendering and hydration are separate decisions.

## 2. Choose state and communication boundaries

Start with explicit local flow, then widen only when ownership or lifecycle requires it.

| Need | Smallest useful mechanism | Escalate when | Warning sign |
| --- | --- | --- | --- |
| Parent/child data and actions | Props and events/callbacks | The same state crosses distant owners or routes | Prop drilling is being used as the only justification without examining ownership |
| Reusable stateful behavior | React hook or Vue composable | Multiple consumers need coordinated shared state | A hook/composable silently becomes a global mutable singleton |
| Stable subtree dependency | React Context/provider or Vue provide/inject | Updates are frequent, workflows are complex, or debugging needs stronger tooling | One provider carries unrelated concerns or causes broad rerenders |
| Application workflow state | A scoped store; use a framework store when tooling and lifecycle justify it | Multiple processes, tabs, services, or durable recovery own the workflow | All server data and ephemeral UI state are placed in one global store |
| Server state | A query/cache layer when caching, deduplication, invalidation, retries, or optimistic updates are required | Consistency rules exceed a client cache's authority | `useEffect`/watchers duplicate fetch and cache behavior across screens |
| One-to-many notifications | Observer or typed event channel | Ordering, replay, durability, or cross-process delivery matters | Implicit event chains cannot be traced or unsubscribed safely |
| Many participants need coordination | Mediator or explicit orchestrator | The process needs durable state, retries, or distributed ownership | The mediator becomes a god object containing all business logic |
| Operations need queue, undo, audit, or replay | Command objects with an explicit lifecycle | Commands cross a process boundary or require durable execution | Boilerplate wraps simple direct calls without lifecycle value |
| Exactly one resource lifetime | Module-scoped instance or dependency-injected singleton | The lifetime differs by request, tenant, test, or runtime | Hidden mutable global state makes isolation impossible |
| Cross-cutting interception | Proxy, middleware, decorator, or wrapper | The concern is a security or service boundary needing explicit enforcement | Invisible interception changes semantics or sits on a hot path |

Additional pattern gates:

- Use a factory when creation genuinely varies by environment, configuration, or type; use a constructor or literal when it does not.
- Use flyweight or prototype sharing only after memory evidence shows many similar objects are material. Keep intrinsic and extrinsic state explicit.
- Prefer native modules for encapsulation and dependency visibility. Dynamic import is a delivery decision, not a substitute for a clean module boundary.
- Prefer composition, hooks, or composables over mixins for new code. Mixins and HOCs remain reasonable mainly for established APIs or truly cross-cutting wrappers.

For every shared-state mechanism, record owner, scope, source of truth, initialization, mutation authority, persistence, synchronization, teardown, and observability.

## 3. Choose component composition patterns

Component patterns are local API design unless they change team ownership, deployment, performance, or product extension boundaries. Do not elevate every refactor into system architecture.

Use this escalation path:

1. Plain component with explicit props, events, and local state.
2. Extract a hook or composable when stateful behavior is repeated.
3. Use composition or explicit variants when boolean props create invalid combinations.
4. Use compound components for a cohesive family such as tabs, menus, or form controls that shares state and invariants.
5. Use headless/renderless or data-provider patterns when behavior must support materially different presentations or a component-library API.
6. Separate presentation from data/workflow logic when independent testing, reuse, or ownership benefits are real. Modern hooks and composables often provide the seam without a dedicated container component.
7. Use dynamic components for runtime view selection and preserve state only when that is the intended lifecycle.
8. Use render props, HOCs, raw render functions, or JSX-generating abstractions when a simpler hook, composable, slot, or template cannot express the API. Account for nesting, naming, tooling, and team familiarity.

Framework mapping:

- React: hooks for reusable behavior; Context for stable subtree dependencies; compound components and slots/children for coordinated APIs; server/client boundaries for delivery, not merely file organization.
- Vue: props/events first; composables for reusable behavior; provide/inject for scoped dependencies; Pinia or another store when workflow scale and tooling justify it; scoped slots/renderless components for template-level inversion of control.

Validate a shared component API with representative consumers. Count invalid prop combinations, required adapters, rerender scope, accessibility behavior, bundle impact, migration work, and the ability to remove or replace the abstraction.

## 4. Design the resource-loading path

Model the critical journey as a dependency graph: HTML, critical CSS, fonts, hero media, first-party JavaScript, data, and third-party resources. Optimize the blocking chain before individual file sizes.

| Technique | Use when | Do not use as a default when | Verify |
| --- | --- | --- | --- |
| Static import | Code is required for the initial route | The module is heavy and conditional | Initial bundle and execution cost |
| Dynamic import / bundle splitting | A stable route, feature, or interaction boundary defers meaningful code | The extra request and fallback cost exceed the saved work | Chunk graph, cache behavior, error and fallback UX |
| Route-based splitting | Routes have distinct feature sets | Shared dependencies are duplicated or every navigation becomes a waterfall | Cold and warm navigation traces |
| Import on interaction | A costly widget is genuinely optional | Users predictably need it immediately after the action | Action-to-ready latency and early-input handling |
| Import on visibility | Below-fold content is non-critical | It affects initial HTML, SEO, accessibility, or layout stability | Layout shift, viewport timing, and fallback behavior |
| Preload | A critical current-page resource is discovered too late | The browser already discovers it early or priority contention appears | Waterfall priority and unused-preload warnings |
| Prefetch | The next resource is likely and idle bandwidth is available | Probability is low, data is metered, or content becomes stale quickly | Hit rate, wasted bytes, and critical-request contention |
| Tree shaking | Unused ESM exports materially inflate bundles | Side effects or package shape make elimination unsafe | Analyzer output and runtime regression tests |
| Compression | Text transfer is material | It is treated as a substitute for removing or splitting code | Encodings, transferred bytes, server/CDN configuration |
| Third-party deferral or facade | External scripts dominate critical-path work | Compliance or business requirements need earlier execution | Long tasks, Core Web Vitals, lost events, consent and fallback behavior |
| Virtualization | Large collections cause measured DOM or scroll cost | Lists are small or the accessibility/variable-height cost is unacceptable | Frame time, memory, keyboard and screen-reader behavior |
| View transitions | Motion materially improves spatial continuity | Browser support, reduced-motion, or frozen-DOM cost is unacceptable | Fallbacks, reduced-motion behavior, interaction latency |

Use the PRPL idea as a checklist—prioritize critical resources, render the initial route, prepare likely next routes, and lazily load the rest—not as a requirement to adopt a named application architecture.

Apply micro-optimizations only to measured hot paths. For loops, lookups, DOM work, memoization, and render reduction, preserve correctness and readability unless profiling proves the path matters.

## 5. Web performance evidence contract

Do not say "faster" without a baseline and target. For the affected journey, record:

- page/route, user population, device and network profile;
- cold or warm cache, authenticated state, geography, and sample count;
- transferred and uncompressed bytes, request count, chunk count, and third-party share;
- user-centered paint, interaction, and layout metrics appropriate to the current Web Vitals definition;
- server latency, streaming behavior, hydration or client execution time, long tasks, memory, and error rate when relevant;
- before/after distributions rather than one favorable run.

Match evidence to the claim:

- Bundle analysis proves composition and size, not user-perceived speed.
- A local Lighthouse run is a diagnostic sample, not production acceptance.
- Server logs do not prove browser interaction readiness.
- A passing build does not prove CDN compression, proxy streaming, cache invalidation, or third-party behavior.
- Lab traces reveal mechanisms; field telemetry reveals population impact. Use both when the decision warrants it.

## 6. AI interface extension

For chat, copilot, or Agent UI, combine this reference with the main skill's AI and Agent architecture lens.

- Keep provider credentials and privileged tools behind a server-side authorization boundary.
- Model request, queued, streaming, tool-running, approval-needed, completed, cancelled, failed, retrying, and partially recovered states explicitly.
- Define what partial tokens, tool results, citations, and persisted messages mean after cancellation, timeout, retry, or reconnect.
- Make concurrency policy visible: disable, queue, branch, or allow parallel submissions intentionally.
- Separate reusable message/input presentation from conversation state, transport, tool execution, and persistence.
- Provide cancellation, retry, error recovery, accessibility announcements, and human approval for consequential actions.
- Evaluate task success, latency, cost, safety, privacy, recovery, and user control together. A smooth token stream is only a presentation result.

## 7. Coverage map to PatternsDev skills

This map ensures the upstream collection is represented without loading 58 separate tutorials into an architecture discussion.

- **System structure and behavioral patterns:** `singleton-pattern`, `observer-pattern`, `proxy-pattern`, `prototype-pattern`, `module-pattern`, `mixin-pattern`, `mediator-pattern`, `flyweight-pattern`, `factory-pattern`, `command-pattern`, `provider-pattern`.
- **JavaScript delivery and browser performance:** `loading-sequence`, `static-import`, `dynamic-import`, `import-on-visibility`, `import-on-interaction`, `route-based`, `bundle-splitting`, `prpl`, `tree-shaking`, `preload`, `prefetch`, `third-party`, `virtual-lists`, `compression`, `js-performance-patterns`, `vite-bundle-optimization`, `view-transitions`.
- **Cross-framework rendering:** `islands-architecture`.
- **React component architecture:** `hooks-pattern`, `hoc-pattern`, `compound-pattern`, `render-props-pattern`, `presentational-container-pattern`, `react-composition-2026`, `react-render-optimization`.
- **React application, data, and AI UI:** `react-2026`, `react-data-fetching`, `ai-ui-patterns`.
- **React rendering and hydration:** `client-side-rendering`, `server-side-rendering`, `static-rendering`, `incremental-static-rendering`, `streaming-ssr`, `progressive-hydration`, `react-selective-hydration`, `react-server-components`.
- **Vue component and state architecture:** `components`, `composables`, `script-setup`, `state-management`, `provide-inject`, `dynamic-components`, `async-components`, `render-functions`, `renderless-components`, `container-presentational`, `data-provider`.

## Provenance

Architecture synthesis based on [PatternsDev/skills](https://github.com/PatternsDev/skills), inspected at commit `48bf58a488cd210bcfad280b09c3a00403964d9d` (58 individual skills). The upstream material is organized as focused JavaScript, React, and Vue tutorials. This reference preserves their decision signals and tradeoffs while avoiding framework-specific code duplication. Refresh version-specific advice against the upstream repository and official platform documentation when currency matters.
