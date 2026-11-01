# iPhone and iPad

Use this reference for SwiftUI/UIKit mobile apps. Adapt the language to touch, safe areas, Dynamic Type, and compact widths instead of shrinking the desktop composition.

## Platform contract

- Respect safe areas, Dynamic Island, camera housing, Home indicator, navigation bars, tab bars, keyboards, and sheets.
- Use system navigation and controls where possible. Preserve swipe-back, scroll behavior, text editing, VoiceOver, Switch Control, and Full Keyboard Access.
- Support Dynamic Type and content reflow. Do not pin critical labels to one line or encode layout in fixed heights.
- Apple lists 44×44pt as the default iOS/iPadOS control target and 28×28pt as the minimum; use 44×44pt for primary and frequent actions.

## Qingshan Design application

- Use mist-white canvas and opaque readable content surfaces by default. Reserve glass for navigation, transient controls, media overlays, or visually rich backgrounds.
- Keep lake teal as the interaction accent, but use the strong role for button fills carrying small white labels.
- Use cypress success and clay error with icons or labels, never color alone.
- Let large artwork or atmosphere bleed to safe-area edges; keep text and controls inside readable guides.
- On compact widths, collapse columns before reducing typography or touch targets.

## Navigation recipes

- **Phone:** one primary column; bottom tab or hierarchical navigation; filters become sheets, menus, or horizontal controls.
- **Tablet:** use split views or list-detail when content benefits from persistent context; do not simply center a narrow phone screen.
- **Modal:** use sheets for focused tasks, preserve dismissal expectations, and keep destructive confirmation explicit.

## Accessibility and motion

- Verify light, dark, Increased Contrast, Differentiate Without Color, Reduced Transparency, and Reduced Motion.
- Replace parallax, large scaling, and depth travel with a fade or static equivalent under Reduced Motion.
- Support text enlargement to 200% without losing content or actions.
- Audit outdoors/bright light as well as a dim environment; translucent colors can lose hierarchy in both.

## Official sources

- [Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
- [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility/)
- [Color](https://developer.apple.com/design/human-interface-guidelines/color)
- [Motion](https://developer.apple.com/design/human-interface-guidelines/motion)
- [Materials](https://developer.apple.com/design/human-interface-guidelines/materials)
