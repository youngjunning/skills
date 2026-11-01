# Android

Use this reference for Jetpack Compose and Material 3 apps. Preserve Material roles, adaptive navigation, edge-to-edge insets, and TalkBack semantics.

## Platform contract

- Use Material 3 color roles and matched foreground/container pairs. Do not mix `primaryContainer` with an unrelated foreground role.
- Keep Material components and Compose semantics unless a custom component is necessary.
- Give interactive composables at least 48×48dp touch targets. Avoid overlapping expanded targets.
- Adapt by window size and posture at runtime. Treat phones, tablets, foldables, split screen, and desktop windowing as layout states, not device-name branches.
- Handle edge-to-edge system bars, cutouts, caption bars, navigation mode, and IME insets.

## Qingshan Design application

- Map lake teal to `primary`, deep lake ink to `onSurface`, mist to `surface`, cypress to success-compatible custom roles, and clay to error-compatible roles.
- Supply tonal containers and `on-*` colors; do not insert raw scenic colors directly into Material components.
- Dynamic Color is a product decision. When enabled, let the user's palette own primary UI and retain Qingshan Lake through illustration, shape, motion, and optional branded surfaces. When brand consistency is required, use the bundled static scheme and document that decision.
- Keep ripple, pressed, focus, selected, disabled, and TalkBack state behavior even when visual styling changes.

## Adaptive recipes

- **Compact:** single column, bottom navigation or compact navigation, filters in sheets.
- **Medium:** navigation rail or adaptive pane; list-detail when it reduces context switching.
- **Expanded:** persistent navigation and multi-pane content with controlled line length.
- Replace columns with panes before shrinking labels or touch targets.

## Accessibility and motion

- Ensure custom Canvas content has explicit Compose semantics or an accessible alternative.
- Test font scaling, display scaling, TalkBack traversal, keyboard/D-pad focus, high contrast text where available, dark theme, and gesture navigation.
- Disable decorative loops and parallax when the system requests reduced motion or when the surface is not visible.

## Official sources

- [Material Design 3 in Compose](https://developer.android.com/develop/ui/compose/designsystems/material3)
- [Build adaptive apps](https://developer.android.com/develop/ui/compose/build-adaptive-apps)
- [Set up edge-to-edge](https://developer.android.com/develop/ui/compose/system/setup-e2e)
- [Accessibility in Compose](https://developer.android.com/develop/ui/compose/accessibility)
- [Compose accessibility API defaults](https://developer.android.com/develop/ui/compose/accessibility/api-defaults)
