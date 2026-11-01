# SwiftUI Performance Patterns Reference

## Table of Contents

- [Performance Optimization](#performance-optimization)
- [Bound Untrusted Text Before Rendering](#bound-untrusted-text-before-rendering)
- [Selector-Driven Snapshot Loading](#selector-driven-snapshot-loading)
- [Anti-Patterns](#anti-patterns)
- [Summary Checklist](#summary-checklist)

## Performance Optimization

### 1. Avoid Redundant State Updates

SwiftUI doesn't compare values before triggering updates:

```swift
// BAD - triggers update even if value unchanged
.onReceive(publisher) { value in
    self.currentValue = value  // Always triggers body re-evaluation
}

// GOOD - only update when different
.onReceive(publisher) { value in
    if self.currentValue != value {
        self.currentValue = value
    }
}
```

### 2. Optimize Hot Paths

Hot paths are frequently executed code (scroll handlers, animations, gestures):

```swift
// BAD - updates state on every scroll position change
.onPreferenceChange(ScrollOffsetKey.self) { offset in
    shouldShowTitle = offset.y <= -32  // Fires constantly during scroll!
}

// GOOD - only update when threshold crossed
.onPreferenceChange(ScrollOffsetKey.self) { offset in
    let shouldShow = offset.y <= -32
    if shouldShow != shouldShowTitle {
        shouldShowTitle = shouldShow  // Fires only when crossing threshold
    }
}
```

### 3. Pass Only What Views Need

**Avoid passing large "config" or "context" objects.** Pass only the specific values each view needs.

```swift
// Good - pass specific values
ThemeSelector(theme: config.theme)
FontSizeSlider(fontSize: config.fontSize)

// Avoid - passing entire config (creates broad dependency)
ThemeSelector(config: config)  // Notified of ALL config changes
```

With `ObservableObject`, any `@Published` change triggers all observers. With `@Observable`, views update only when accessed properties change, but passing entire objects still creates broader dependencies than necessary.

### 4. Use Equatable Views

For views with expensive bodies, conform to `Equatable`:

```swift
struct ExpensiveView: View, Equatable {
    let data: SomeData

    static func == (lhs: Self, rhs: Self) -> Bool {
        lhs.data.id == rhs.data.id  // Custom equality check
    }

    var body: some View {
        // Expensive computation
    }
}

// Usage
ExpensiveView(data: data)
    .equatable()  // Use custom equality
```

**Caution**: If you add new state or dependencies to your view, remember to update your `==` function!

### 5. POD Views for Fast Diffing

**POD (Plain Old Data) views use `memcmp` for fastest diffing.** A view is POD if it only contains simple value types and no property wrappers.

```swift
// POD view - fastest diffing
struct FastView: View {
    let title: String
    let count: Int
    
    var body: some View {
        Text("\(title): \(count)")
    }
}

// Non-POD view - uses reflection or custom equality
struct SlowerView: View {
    let title: String
    @State private var isExpanded = false  // Property wrapper makes it non-POD
    
    var body: some View {
        Text(title)
    }
}
```

**Advanced Pattern**: Wrap expensive non-POD views in POD parent views:

```swift
// POD wrapper for fast diffing
struct ExpensiveView: View {
    let value: Int
    
    var body: some View {
        ExpensiveViewInternal(value: value)
    }
}

// Internal view with state
private struct ExpensiveViewInternal: View {
    let value: Int
    @State private var item: Item?
    
    var body: some View {
        // Expensive rendering
    }
}
```

**Why**: The POD parent uses fast `memcmp` comparison. Only when `value` changes does the internal view get diffed.

### 6. Lazy Loading

Use lazy containers for large collections:

```swift
// BAD - creates all views immediately
ScrollView {
    VStack {
        ForEach(items) { item in
            ExpensiveRow(item: item)
        }
    }
}

// GOOD - creates views on demand
ScrollView {
    LazyVStack {
        ForEach(items) { item in
            ExpensiveRow(item: item)
        }
    }
}
```

**iOS 26+ note**: Nested scroll views containing lazy stacks now automatically defer loading their children until they are about to appear, matching the behavior of top-level lazy stacks. This benefits patterns like horizontal photo carousels inside a vertical scroll view.

> Source: "What's new in SwiftUI" (WWDC25, session 256)

### 7. Task Cancellation

Cancel async work when view disappears:

```swift
struct DataView: View {
    @State private var data: [Item] = []

    var body: some View {
        List(data) { item in
            Text(item.name)
        }
        .task {
            // Automatically cancelled when view disappears
            data = await fetchData()
        }
    }
}
```

### 8. Debug View Updates

**Use `Self._printChanges()` or `Self._logChanges()` to debug unexpected view updates.**

```swift
struct DebugView: View {
    @State private var count = 0
    @State private var name = ""
    
    var body: some View {
        #if DEBUG
        let _ = Self._logChanges()  // Xcode 15.1+: logs to com.apple.SwiftUI subsystem
        #endif
        
        VStack {
            Text("Count: \(count)")
            Text("Name: \(name)")
        }
    }
}
```

- `Self._printChanges()`: Prints which properties changed to standard output.
- `Self._logChanges()` (iOS 17+): Logs to the `com.apple.SwiftUI` subsystem with category "Changed Body Properties", using `os_log` for structured output.

Both print `@self` when the view value itself changed and `@identity` when the view's persistent data was recycled.

**Why**: This helps identify which state changes are causing view updates. Isolating redraw triggers into single-responsibility subviews is often the fix -- extracting a subview means SwiftUI can skip its body when its inputs haven't changed.

### 9. Eliminate Unnecessary Dependencies

**Narrow state scope to reduce update fan-out.** Instead of passing an entire `@Observable` model to a row view (which creates a dependency on all accessed properties), pass only the specific values the view needs as `let` properties.

```swift
// Bad - broad dependency on entire model
struct ItemRow: View {
    @Environment(AppModel.self) private var model
    let item: Item
    var body: some View { Text(item.name).foregroundStyle(model.theme.primaryColor) }
}

// Good - narrow dependency
struct ItemRow: View {
    let item: Item
    let themeColor: Color
    var body: some View { Text(item.name).foregroundStyle(themeColor) }
}
```

**Avoid storing frequently-changing values in the environment.** Every write to *any* environment key forces every view that reads *any* key in that subtree to be checked. So a high-frequency value (scroll offset, window/container size, drag translation, per-frame animation progress, timer ticks, hover location) flowing into an `@Entry` or `.environment(\.key, value)` becomes an invalidation storm.

Instead, hold the value in an `@Observable` model and expose a **coarsened** value — a boolean threshold rather than the raw measurement — so views invalidate only when crossing a meaningful boundary:

```swift
@MainActor @Observable
final class ViewportModel {
    var width: CGFloat = 0 { didSet { isWide = width > 600 } }
    private(set) var isWide = false   // readers invalidate only when this flips
}
```

The same shape applies per row in a list: storing the raw offset on a model and having every row read it still invalidates all visible rows every frame. Give each item its own `@Observable` whose properties track only that item's derived state (e.g. `isVisible`), so each row invalidates at most twice (enter/leave) regardless of scroll speed — see item #10 below.

For purely visual effects driven by scroll position (opacity, scale, rotation), prefer `scrollTransition` or `visualEffect(in:)` — they push the per-frame work to the renderer and skip body re-evaluation entirely. Reach for the `@Observable` + coarsening pattern only when the scroll-derived value must drive non-rendering logic (model updates, prefetches, sibling state).

> Source: "Optimize SwiftUI performance with Instruments" (WWDC25, session 306)

### 10. @Observable Dependency Granularity

**Consider per-item `@Observable` state holders (one per row/item) to narrow update scope.** When multiple list items share a dependency on the same `@Observable` array, changing one element causes all items to re-evaluate their bodies.

```swift
// BAD - all item views depend on the full favorites array
@Observable
class ModelData {
    var favorites: [Landmark] = []

    func isFavorite(_ landmark: Landmark) -> Bool {
        favorites.contains(landmark)
    }
}

struct LandmarkRow: View {
    let landmark: Landmark
    @Environment(ModelData.self) private var model

    var body: some View {
        HStack {
            Text(landmark.name)
            if model.isFavorite(landmark) {
                Image(systemName: "heart.fill")
            }
        }
    }
}

// GOOD - each item has its own observable view model
@Observable
class LandmarkViewModel {
    var isFavorite: Bool = false
}

struct LandmarkRow: View {
    let landmark: Landmark
    let viewModel: LandmarkViewModel

    var body: some View {
        HStack {
            Text(landmark.name)
            if viewModel.isFavorite {
                Image(systemName: "heart.fill")
            }
        }
    }
}
```

**Why**: With the bad pattern, toggling one favorite marks the entire array as changed, causing every `LandmarkRow` to re-run its body. With per-item view models, only the toggled item's body runs.

> Source: "Optimize SwiftUI performance with Instruments" (WWDC25, session 306)

### 11. Off-Main-Thread Closures

**SwiftUI may call certain closures on a background thread for performance.** These closures must be `Sendable` and should avoid accessing `@MainActor`-isolated state directly. Instead, capture needed values in the closure's capture list.

Closures that may run off the main thread:
- `Shape.path(in:)`
- `visualEffect` closure
- `Layout` protocol methods
- `onGeometryChange` transform closure

```swift
// BAD - accessing @MainActor state directly
.visualEffect { content, geometry in
    content.blur(radius: self.pulse ? 5 : 0)  // Compiler error: @MainActor isolated
}

// GOOD - capture the value
.visualEffect { [pulse] content, geometry in
    content.blur(radius: pulse ? 5 : 0)
}
```

> Source: "Explore concurrency in SwiftUI" (WWDC25, session 266)

### 12. Common Performance Issues

**Be aware of common performance bottlenecks in SwiftUI:**

- View invalidation storms from broad state changes
- Unstable identity in lists causing excessive diffing
- Heavy work in `body` (formatting, sorting, image decoding)
- Layout thrash from deep stacks or preference chains

**When performance issues arise**, suggest the user profile with Instruments (SwiftUI template) to identify specific bottlenecks.

## Bound Untrusted Text Before Rendering

Visual truncation is not a resource boundary. `Text(value).lineLimit(1)`,
clipping, and `.truncationMode(...)` can still make SwiftUI, CoreText, AppKit
tables, and the Accessibility server inspect or shape the entire `value`.
Agent transcripts, prompts, log messages, file contents, and server labels can
therefore make every unrelated click feel slow when they accidentally enter a
title or row-label field.

Apply the boundary before the value reaches the main actor:

1. Normalize repeated whitespace and newlines in one bounded pass.
2. Stop reading after the product's maximum presentation length; do not
   normalize the whole blob and truncate afterward.
3. Enforce the same limit at ingestion as defense in depth, while keeping the
   authoritative source data outside the derived UI store unchanged.
4. Publish only the bounded value in immutable UI snapshots.
5. Test both a normal title and an adversarial multi-thousand-character input.

When profiling through UI automation, Accessibility can contaminate the
measurement. A hang dominated by
`CopyAppKitUIElementAttributeValueNoCatch`, `_AXUIElement*`, or
`SwiftUIAccessibilityTextResolver` during a full tree capture is evidence about
the probe, not yet evidence about normal pointer input. Re-record the same
scenario with coordinate/input-only actions and no Accessibility snapshot
inside the measurement window. Conversely, an unexpectedly huge AX tree is
useful product evidence that presentation data was never bounded.

## Selector-Driven Snapshot Loading

Use this pattern when a tab, segmented control, sidebar destination, date range, filter, or similar exclusive selection triggers SQLite/GRDB reads, filesystem work, decoding, aggregation, chart preparation, or another expensive content refresh.

### Diagnose the full interaction path

Follow the event across all layers:

```text
click / key input
  -> selection intent
  -> debounce / task scheduling
  -> persistent reads and preparation
  -> observable publication
  -> view invalidation
  -> layout and render
```

Do not attribute lag to the feature that happens to be visible. A shared app-state write, synchronous repository call, repeated snapshot assembly, or broad environment dependency can keep the same lag after the visible module is removed.

### Required loading semantics

1. **No-op repeated selection.** Guard `newSelection != selectedSelection` before writes, persistence, animation, navigation, or reloads.
2. **Separate intent from content.** Update the selector's lightweight intent immediately. Keep the current immutable content snapshot visible until the requested snapshot is complete; optionally show a narrow loading affordance.
3. **Coalesce bursts before I/O.** Use a short, trace-tuned debounce for rapid exclusive switching. Roughly 200–300 ms is a reasonable starting experiment, not a universal constant.
4. **Single-flight the loader.** Serialize each store's persistent reads so rapid requests cannot run several full query batches concurrently.
5. **Use cooperative cancellation plus latest-wins.** `Task.cancel()` does not interrupt synchronous SQLite, filesystem, decoding, or repository calls. Check cancellation between units of work and guard the final apply with a generation, request identity, and selected value.
6. **Publish atomically.** Build totals, rows, labels, chart points, and derived collections off the main actor, then assign one `Equatable`, immutable snapshot. Do not publish each field separately and invalidate the screen several times for one selection.
7. **Cache completed selections.** Cache by the full selection/filter key and invalidate that cache when the underlying source refreshes. A cache hit should not start another query.
8. **Narrow the render boundary.** Let the selector observe only intent. Pass the content snapshot or narrow values into real child `View` types; move sorting, formatting, and chart-series generation out of `body`.

Conceptual model:

```swift
@MainActor @Observable
final class ContentStore<Selection: Hashable, Snapshot: Equatable> {
    private(set) var selection: Selection
    private(set) var snapshot: Snapshot

    @ObservationIgnored private var task: Task<Void, Never>?
    @ObservationIgnored private var generation: UInt64 = 0
    @ObservationIgnored private var cache: [Selection: Snapshot] = [:]

    func select(_ next: Selection) {
        guard next != selection else { return }
        selection = next
        task?.cancel()
        generation &+= 1

        if let cached = cache[next] {
            snapshot = cached
            return
        }

        let request = generation
        task = Task {
            try? await Task.sleep(for: .milliseconds(250))
            guard !Task.isCancelled else { return }
            let loaded = try? await loader.load(next) // serialized off-main loader
            guard !Task.isCancelled,
                  generation == request,
                  selection == next,
                  let loaded else { return }
            cache[next] = loaded
            if snapshot != loaded { snapshot = loaded }
        }
    }
}
```

Treat this as a responsibility template, not copy-paste architecture. Keep the actual loader outside the main actor and make its mutable cache/cursor state actor- or lock-isolated.

### Regression and trace gates

Add tests that prove:

- selecting the active value starts no load;
- selection intent changes immediately while content waits for completion;
- rapid `A -> B -> C` applies only `C`;
- returning to a cached selection starts no query.

For Instruments comparison, replay the same cadence against baseline and candidate, scope the same logical time window, and include the post-debounce final snapshot apply. Compare at least:

- hitch count, total hitch time, and worst hitch;
- `Potentially expensive app update(s)` / render narratives;
- main-thread sampled work or running coverage;
- overlapping SwiftUI updates and cause-graph fan-in when available.

Keep only changes supported by the trace. If a styling, material, gradient, animation, or subview extraction experiment does not improve the same scenario, revert it rather than bundling an unproven optimization.

## Anti-Patterns

### 1. Creating Objects in Body

```swift
// BAD - creates new formatter every body call
var body: some View {
    let formatter = DateFormatter()
    formatter.dateStyle = .long
    return Text(formatter.string(from: date))
}

// GOOD - static or stored formatter
private static let dateFormatter: DateFormatter = {
    let f = DateFormatter()
    f.dateStyle = .long
    return f
}()

var body: some View {
    Text(Self.dateFormatter.string(from: date))
}
```

### 2. Heavy Computation in Body

**Keep view body simple and pure.** Avoid side effects, dispatching, or complex logic.

```swift
// BAD - sorts array every body call
var body: some View {
    List(items.sorted { $0.name < $1.name }) { item in Text(item.name) }
}

// GOOD - compute once, update via onChange or a computed property in the model
@State private var sortedItems: [Item] = []

var body: some View {
    List(sortedItems) { item in Text(item.name) }
        .onChange(of: items) { _, newItems in
            sortedItems = newItems.sorted { $0.name < $1.name }
        }
}
```

Move sorting, filtering, and formatting into models or computed properties. The `body` should be a pure structural representation of state.

### 3. Unnecessary State

```swift
// BAD - derived state stored separately
@State private var items: [Item] = []
@State private var itemCount: Int = 0  // Unnecessary!

// GOOD - compute derived values
@State private var items: [Item] = []

var itemCount: Int { items.count }  // Computed property
```

### 11. Persistent I/O on the Main Actor

Treat every user-facing SwiftUI model as latency-sensitive. Do not run SQLite/GRDB reads or writes, filesystem reads, package validation, network calls, process calls, or repeated JSON decode/encode work directly inside `@MainActor` actions, `configure()`, `onChange`, Combine sinks, computed properties read by `body`, or button handlers.

Preferred pattern:

- Capture the current UI intent on the main actor.
- Show immediate lightweight feedback.
- Run persistent I/O in a cancellable background task.
- Return a small immutable snapshot to the main actor.
- Apply the snapshot only if it still matches the latest generation, selected item, or task identity.

For window-sized surfaces such as learning centers, dashboards, settings panes, and inspectors:

- Initial load should build one background snapshot instead of issuing several synchronous repository calls from `configure()`.
- Live updates should debounce or cancel stale work and must not invalidate unrelated full-load tasks.
- Background preparation triggered by a high-frequency publisher must track its own task and source identity. Do not use a visible UI phase as the only in-flight guard; coalesce repeated snapshots for the same session or generation.
- Cache empty or otherwise non-actionable preparation results for a short cooldown so an unchanged source cannot immediately restart the same extraction and repository work. Explicit user actions may bypass this negative cache.
- User writes should not be overwritten by an older background snapshot; use separate generation tokens for independent streams when needed.
- Cache decoded records such as profile JSON, overlay JSON, and row-derived view data outside SwiftUI `body` hot paths, with a fallback decode on cache miss.
- If a test previously asserted immediately after a now-background operation, update the test to wait for the observable completion state instead of reintroducing synchronous work.

## Summary Checklist

- [ ] State updates check for value changes before assigning
- [ ] Hot paths minimize state updates
- [ ] Pass only needed values to views (avoid large config objects)
- [ ] Large lists use `LazyVStack`/`LazyHStack`
- [ ] No object creation in `body`
- [ ] Heavy computation moved out of `body`
- [ ] Body kept simple and pure (no side effects)
- [ ] Derived state computed, not stored
- [ ] Use `Self._logChanges()` or `Self._printChanges()` to debug unexpected updates
- [ ] Equatable conformance for expensive views (when appropriate)
- [ ] Consider POD view wrappers for advanced optimization
- [ ] Consider using granular @Observable dependencies for list items (smaller observable units per row when it measurably reduces updates)
- [ ] Frequently-changing values not stored in the environment
- [ ] Sendable closures (Shape, visualEffect, Layout) capture values instead of accessing @MainActor state
- [ ] Persistent I/O and repeated JSON decode/encode stay off the main actor, with stale background snapshots guarded
- [ ] Untrusted row/title text is normalized and bounded before MainActor publication
- [ ] Exclusive selections are no-op on reselect and expensive loads use debounce, single-flight, cooperative cancellation, latest-wins, atomic snapshots, and cache invalidation
- [ ] Rapid-selection tests cover no-op, immediate intent, latest-only apply, and cache hit
- [ ] Performance comparisons replay the same cadence/window and include the final post-debounce content commit
- [ ] Accessibility probes are kept outside measured windows or identified as trace contamination
