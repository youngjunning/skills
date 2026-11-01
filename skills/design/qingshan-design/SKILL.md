---
name: qingshan-design
description: Apply, implement, or audit the Qingshan Lake design language across macOS, iPhone/iPad, Android, React Native, web dashboards, and landing pages. Use when Codex is asked for 青山湖风格, Qingshan Lake or Jiangnan landscape glass UI, mist-and-lake visual systems, cross-platform design tokens, a restrained natural glass redesign, or consistency/accessibility review of an existing implementation.
---

# Qingshan Design

Translate a misty lakeside landscape into a quiet, native, low-noise product system. Preserve the target platform's interaction model; apply the visual language through semantic tokens, hierarchy, material, restrained motion, and explicit anti-patterns.

## Route the task

Always read [references/visual-system.md](references/visual-system.md) and [references/validation.md](references/validation.md). Then load only the target references:

| Target | Reference |
| --- | --- |
| macOS, SwiftUI, AppKit, menu bar, settings, floating panel | [references/macos.md](references/macos.md) |
| iPhone, iPad, iOS, UIKit, SwiftUI mobile | [references/ios.md](references/ios.md) |
| Android, Jetpack Compose, Material 3 | [references/android.md](references/android.md) |
| React Native, Expo, shared iOS/Android UI | [references/react-native.md](references/react-native.md) |
| Web app, dashboard, console, admin, data UI | [references/web-dashboard.md](references/web-dashboard.md) |
| Marketing site, product site, landing page | [references/web-landing-page.md](references/web-landing-page.md) |

For a cross-platform system, read every relevant platform reference and keep one semantic token vocabulary with platform-specific component recipes.

## Workflow

### 1. Recover the product before styling

- Read existing design tokens, shared components, route structure, accessibility utilities, and project instructions.
- Identify the primary workflow, information density, input method, screen/window behavior, and brand constraints.
- Preserve established platform-native navigation and interaction unless the user explicitly requests a structural redesign.
- Decide whether the requested surface is a productivity interface, content surface, transient control, or marketing narrative.

Do not start by replacing colors. The design language must change hierarchy, surfaces, states, and motion together.

### 2. Build the design contract

State the following before implementation:

1. **Visual source:** mist, lake, cypress forest, distant hills, wet wood, and rare dawn light.
2. **Primary hierarchy:** what users should notice first, second, and last.
3. **Semantic mapping:** canvas, surface, text, primary action, focus, success, warning, error, and decorative accent.
4. **Density:** compact, balanced, or narrative.
5. **Material strategy:** native system material, CSS translucency, opaque fallback, or no glass.
6. **Anti-patterns:** the concrete effects that must not appear.

Use [assets/qingshan.tokens.json](assets/qingshan.tokens.json) when the project has no stronger token source. Copy or adapt [assets/qingshan.css](assets/qingshan.css), [assets/QingshanPalette.swift](assets/QingshanPalette.swift), [assets/QingshanTheme.kt](assets/QingshanTheme.kt), or [assets/QingshanTheme.ts](assets/QingshanTheme.ts) only when their platform and framework match.

### 3. Apply the hierarchy in this order

1. Establish layout zones and reading path.
2. Map semantic colors and accessible foreground pairs.
3. Define surface depth, borders, and fallback behavior.
4. Style native controls without losing semantics, focus, keyboard, touch, or assistive-technology behavior.
5. Define loading, empty, error, success, disabled, selected, pressed, and focused states.
6. Add atmosphere and motion last.

Prefer spacing, alignment, type, and one clear action over another card or decorative effect.

### 4. Keep the language recognizable

Require all of these:

- mist-white or deep-lake canvas instead of pure white or pure black as the designed field;
- lake teal for primary action, focus, selection, or progress;
- cypress green for healthy, complete, or growing states;
- gray-blue hills and cloud belts for secondary hierarchy;
- continuous, restrained corner geometry;
- soft separation through spacing, translucent borders, or platform material;
- warm gold, clay, wet wood, wildlife, particles, and scenic imagery only as rare supporting accents.

Reject:

- tourism-poster backgrounds;
- generic blue-purple AI gradients;
- full neon, black developer-tool chrome, or large gold surfaces;
- glass-on-glass and nested rounded cards;
- low-contrast text placed directly on atmosphere;
- pills on every control;
- perpetual decorative animation;
- state communicated by color alone.

### 5. Validate the real surface

- Run [scripts/validate_tokens.py](scripts/validate_tokens.py) after changing the bundled token file or deriving a new token JSON with the same schema.
- Verify the implemented product at its real size and input mode, not only in source or a mockup.
- Exercise platform accessibility settings, compact and expanded layouts, long content, loading/error states, and reduced effects.
- For existing products, compare before/after screenshots on the same content and viewport.
- Report implementation, build, rendered UI, device/runtime, and production states separately.

## Output contract

For design or implementation work, deliver:

- the product and platform assumptions;
- the semantic token mapping;
- the surface/component/state decisions;
- the files or artifacts changed;
- the real UI and accessibility checks performed;
- any unverified device, window, browser, or production boundary.

For audit-only work, list each issue with its surface, violated rule, user impact, and smallest corrective action. Do not rewrite the product unless asked.

## Origin and naming

Qingshan Design is an independently authored design language inspired by the mist, water, cypress forests, hills, and boardwalk atmosphere of Qingshan Lake in Lin'an, Hangzhou. It is not an official design system of the scenic area or its operators.
