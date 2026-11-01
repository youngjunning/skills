---
name: macos-app-develop
description: Design, implement, review, refactor, debug, and profile native macOS applications with SwiftUI or AppKit using a bundled Qingshan Lake visual system. Use for macOS windows, panels, sheets, popovers, menus, sidebars, toolbars, controls, focus, accessibility, state management, view composition, lists, localization, animation, performance, Instruments traces, Sequoia/Tahoe compatibility, or making an app feel like a polished Mac citizen without relying on project-local design documentation.
---

# macOS App Development

Build a good Mac citizen whose SwiftUI implementation is correct, efficient, accessible, and visually coherent. Apply the bundled Qingshan Lake direction as an implementation contract unless the user explicitly chooses another visual system.

## Operating rules

1. Preserve native macOS behavior: menus, keyboard access, focus, window management, text editing, Services, VoiceOver, and control roles.
2. Do not confuse native behavior with default appearance. Keep control semantics while applying the product's palette, surfaces, focus treatment, and states.
3. Read `references/latest-apis.md` before SwiftUI implementation or review. Confirm macOS availability; do not infer it from an iOS version number.
4. Prefer SwiftUI for new UI. Bridge to AppKit only for capabilities SwiftUI cannot provide, and keep the bridge narrow.
5. Separate business logic from view rendering without imposing a named architecture.
6. Gate APIs newer than the repository deployment target with `#available` and provide a real fallback.
7. Treat performance findings as evidence-driven. Profile before invasive optimization.

## Workflow

### 1. Establish platform and product constraints

- Read repository instructions, deployment target, shared design tokens, and existing components.
- Identify the app archetype, window model, primary commands, data ownership, and accessibility path.
- Read `references/qingshan-lake-swiftui.md` before changing any visible surface. It is self-contained and does not require repository-local design files.
- If the repository also contains a Qingshan Lake document or shared palette, treat it as a project-specific extension and preserve its stricter rules.
- Read the actual deployment target. Do not introduce unguarded APIs from a newer macOS release, including Liquid Glass.

### 2. Route the task

Read every reference relevant to the task:

| Topic | Reference |
|---|---|
| Native macOS design and release rubric | `references/macos-design-guide.md` |
| Qingshan Lake controls and visual audit | `references/qingshan-lake-swiftui.md` |
| Modern and deprecated APIs | `references/latest-apis.md`, `references/soft-deprecation.md` |
| State management and data flow | `references/state-management.md` |
| View composition, invalidation, and UI responsiveness | `references/view-structure.md`, `references/performance-patterns.md` |
| Lists, `ForEach`, and identity | `references/list-patterns.md` |
| Layout and scrolling | `references/layout-best-practices.md`, `references/scroll-patterns.md` |
| Sheets and navigation | `references/sheet-navigation-patterns.md` |
| Focus and keyboard interaction | `references/focus-patterns.md` |
| Accessibility | `references/accessibility-patterns.md` |
| Animation | `references/animation-basics.md`, `references/animation-transitions.md`, `references/animation-advanced.md` |
| macOS scenes, windows, and views | `references/macos-scenes.md`, `references/macos-window-styling.md`, `references/macos-views.md` |
| Text and localization | `references/text-patterns.md`, `references/localization.md` |
| Images | `references/image-optimization.md` |
| Charts | `references/charts.md`, `references/charts-accessibility.md` |
| Previews | `references/previews.md` |
| Liquid Glass | `references/liquid-glass.md` |
| Instruments capture and analysis | `references/trace-recording.md`, `references/trace-analysis.md` |

### 3. Implement or review

For existing code:

- Read the complete changed flow, not only the visible view body.
- For interaction lag, trace the exact path from input intent through data loading, state publication, view invalidation, layout, and render. Do not infer that the visible feature owns the lag, and do not delete or simplify product behavior before evidence identifies it as causal.
- Treat every agent-, file-, or network-derived string as untrusted layout input. `lineLimit`, clipping, and truncation mode only change visible output; bound and normalize the actual string before it reaches SwiftUI, CoreText, or Accessibility.
- Check API availability, ownership of state, identity stability, invalidation breadth, main-actor blocking work, focus, localization, accessibility, and all presentation surfaces.
- Avoid unrelated migrations. Never introduce a newly soft-deprecated API.

For a new feature:

- Define owned versus injected state first.
- Define window, sheet, popover, menu, and keyboard-command behavior before styling.
- Extract meaningful subviews early enough to narrow dependencies and invalidation.
- Use `Button` for actions; use gestures only when location, count, or continuous input is required.
- Build self-contained previews with mock data and no live service or network dependency.

### 4. Verify

- Build and test according to repository instructions.
- Exercise keyboard-only and VoiceOver paths.
- Resize the window and test long localized strings.
- Check Reduced Motion, Reduced Transparency, and Increased Contrast.
- For visual work, inspect every changed state on a light background before handoff.
- For performance claims, attach trace evidence or clearly mark the claim as a hypothesis.

## Qingshan Lake visual contract

Treat Qingshan Lake as the default visual direction unless the user explicitly supplies another system.

Before editing UI:

1. Search for existing design tokens, surface metrics, and styled controls. If none exist, create a shared palette from the exact standalone tokens in `references/qingshan-lake-swiftui.md`.
2. Inventory every touched button, picker, toggle, text field, editor, focus ring, sheet, alert, popover, menu, context menu, toast, loading state, empty state, and error state.
3. Reuse shared styles before creating wrappers or new tokens.

### Hard gates

- Do not ship a bare `.segmented` picker, `.borderedProminent` button, default switch, default TextField bezel/focus ring, default white sheet, or default-blue selection.
- For a themed `NavigationSplitView` sidebar, do not rely on `List(selection:)`, app tint, or the system accent to express the selected state. Use the native-control custom-row recipe in `references/qingshan-lake-swiftui.md`, including hover, pressed, focus, keyboard movement, accessibility selection, and non-color differentiation.
- Use mist-white and lake-teal translucent layers, deep-lake/cypress text, continuous corners, and one-pixel soft borders. Reserve dawn gold for small status accents.
- Keep native semantics. Implement project `ButtonStyle`, `ToggleStyle`, `TextFieldStyle`, or `PickerStyle` before replacing a native interaction primitive.
- Style idle, hover, pressed, selected/on, focused, disabled, loading, error, Increased Contrast, Reduced Transparency, and Reduced Motion states.
- Use app-level lake-teal tint only as a safety net, never as the sole style.
- Avoid glass-on-glass and nested card chrome. Prefer layout, spacing, and typography for hierarchy.
- For transparent `NSPanel`/`NSWindow`, style both SwiftUI and AppKit boundaries. Do not rely on rectangular AppKit shadows or opaque hosting backgrounds.
- **Highlights belong to their host surface; they must never read as a second surface.** A static highlight must reuse the host's shape and clip boundary, be composited inside that boundary, and span the host deliberately. Do not attach an intrinsic-size `RoundedRectangle`/`Capsule` with a partial frame (for example a 10 pt `topLeading` overlay), or stack `screen`/`softLight` glows that create a second card. Prefer one restrained base gradient plus an optional same-shape 1 px stroke; reserve clipped shimmer for active progress only.

Decision test: **Would the interface still behave like a good Mac app with color removed, and would every visible state still express Qingshan Lake during interaction?** Both must be true.

## Mac citizen requirements

- Keep standard App/File/Edit/View/Window/Help menus when applicable.
- Put Settings in the App menu and support `⌘,`.
- Make primary commands keyboard reachable without overriding standard editing shortcuts.
- Make window resizing, minimize, zoom, fullscreen, and multi-window behavior appropriate to the app archetype.
- Use system text components to preserve selection, undo/redo, copy/paste, spell checking, and Services.
- Use SF Symbols for system concepts and provide accessibility labels for icon-only actions.
- Reserve Liquid Glass for navigation/control layers when explicitly requested and platform-gated; do not stack glass on content.

## SwiftUI correctness gates

Treat these violations as bugs:

- Keep `@State` and `@FocusState` properties `private`.
- Use `@Binding` only when a child modifies parent-owned state.
- Never mark an injected value as `@State` or `@StateObject`.
- Use `@StateObject` for view-owned `ObservableObject` and `@ObservedObject` for injected objects.
- For new Observation code, use `@State` with `@Observable`; use `@Bindable` when an injected observable needs bindings.
- Give every `ForEach` stable identity that outlives the view and is not derived from mutable content. Do not use indices or offsets as identity.
- Keep a constant number of views per `ForEach` element; keep `List` rows unary.
- Do not store closures in custom `@Environment` or `@FocusedValue` keys.
- Keep custom `@Entry` defaults stable; do not create `Model()`, `Date()`, or `UUID()` as a default expression.
- Always use `.animation(_:value:)` with an explicit value.
- Make reselecting the active tab, segment, sidebar destination, or equivalent exclusive selection a no-op. Before assigning selection or invoking selection-coupled work, guard `newSelection != currentSelection`; a repeated click must not republish state, restart animation, reload data, rebuild a window/view hierarchy, or trigger navigation side effects.
- When an exclusive selection triggers persistent reads or expensive preparation, follow the selector-driven snapshot pattern in `references/performance-patterns.md`: publish lightweight selection intent immediately, coalesce the burst, serialize loading, reject stale results, and publish one immutable content snapshot. Cancellation without cooperative checks is not sufficient for synchronous SQLite, filesystem, decode, or repository work.
- Do not redundantly write `@FocusState` from tap handlers attached to `.focusable()` controls.
- Gate newer APIs and implement fallbacks that compile against the minimum deployment target.
- Import Charts in files that use chart types.
- Keep previews deterministic and independent from production services.

## Instruments workflows

### Record a trace

Read `references/trace-recording.md`, determine whether to attach, launch, or record the host Mac, then use:

```bash
python3 "${SKILL_DIR}/scripts/record_trace.py" --list-devices
python3 "${SKILL_DIR}/scripts/record_trace.py" \
  --device "<name|udid>" --attach "<AppName>" \
  --stop-file /tmp/stop-trace --output ~/Desktop/session.trace
```

When the user finishes exercising the app, create the stop file and wait for trace finalization. Do not treat an iOS Simulator as equivalent to the host Mac; consult the reference's template decision table.

### Analyze a trace

Read `references/trace-analysis.md`. Resolve a requested time window with logs or signposts before the main analysis, then run:

```bash
python3 "${SKILL_DIR}/scripts/analyze_trace.py" \
  --trace <path> --json-only --top 10 [--window START_MS:END_MS]
```

Use `--fanin-for "<view name>"` to identify invalidation sources. Report main-thread coverage, hot symbols, overlapping view updates, cause-graph edges, and timestamps before recommending a fix. Edit code only when requested.

For before/after performance claims, replay the same interaction cadence and analyze the same logical window. Include the final content commit after any debounce, then compare hitch count, total and worst hitch duration, app-update/render narratives, and main-thread sampled work. Accessibility tree capture can itself stall the target app; if stacks contain `CopyAppKitUIElementAttributeValueNoCatch`, `_AXUIElement*`, or SwiftUI accessibility resolvers, re-record with input-only automation and no tree snapshot inside the measured window. Reject a speculative or cosmetic optimization when the trace does not improve; remove profiling hooks and restore the user's installed app before handoff.

## Definition of done

- Native menu, keyboard, focus, text, accessibility, and window behavior remain intact.
- State ownership and list identity pass the SwiftUI correctness gates.
- New APIs match the deployment target or have tested fallbacks.
- The changed product contains no unstyled system-blue controls, generic white transient surfaces, unrelated gray chrome, or rectangular transparent-window artifacts.
- Every changed interaction state follows Qingshan Lake and remains distinguishable without color alone.
- Reduced Motion/Transparency, Increased Contrast, localization, and resize paths remain usable.
- Build/tests pass, or the exact blocker and unverified scope are reported.
