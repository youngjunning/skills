# macOS

Use this reference for SwiftUI/AppKit windows, menu bar surfaces, settings, dashboards, panels, and popovers.

## Platform contract

- Keep windows resizable and useful at minimum, typical, and wide sizes.
- Use the Mac's larger canvas for comfortable information density and fewer nested levels.
- Preserve menu commands, keyboard shortcuts, focus movement, pointer hover, secondary click, and VoiceOver.
- Prefer native `Button`, `Toggle`, `TextField`, `Menu`, `Table`, `NavigationSplitView`, sheet, and alert semantics. Style them through project styles before rebuilding interaction primitives.
- Keep frequent actions reachable without forcing repeated modality.

## Qingshan Design application

- Use native material where it expresses a real hierarchy boundary, then add a restrained mist or lake tint.
- Treat material as semantic structure, not a color picker. Provide an opaque fallback for Reduced Transparency.
- Keep sidebars quieter than content; make selection unmistakable with fill, label contrast, focus, and a non-color cue when requested.
- On light desktops, inspect all translucent window edges and shadows. A visually acceptable center does not prove correct corners.
- For transparent `NSPanel` or `NSWindow`, align the SwiftUI clip, hosting-view layer corner, and window background. Do not rely on a rectangular system shadow as the visible boundary.

## Controls and sizing

- Apple lists 28×28pt as the default macOS control size and 20×20pt as the minimum. Use larger targets for primary actions and dense custom controls when space allows.
- Keep body text near platform defaults; support user text and contrast preferences.
- Never remove the default focus treatment without supplying a visible custom focus indicator.
- Test selected, hover, pressed, focused, disabled, loading, error, Increased Contrast, Differentiate Without Color, Reduced Motion, and Reduced Transparency.

## Layout recipes

- **Dashboard:** stable sidebar, title/toolbar, filters, content table or chart, status strip. Use spacing before cards.
- **Settings:** native grouping, direct labels, restrained surfaces, predictable tab/keyboard order.
- **Menu bar/popover:** compact hierarchy, no decorative background motion, immediate state and one obvious next action.
- **Floating panel:** one visual boundary, high contrast over arbitrary desktops, safe edge/corner rendering.

## Official sources

- [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos/)
- [Materials](https://developer.apple.com/design/human-interface-guidelines/materials)
- [Windows](https://developer.apple.com/design/human-interface-guidelines/windows)
- [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility/)
