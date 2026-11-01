# Native macOS design checks

Establish the app archetype, deployment target and existing design tokens. Use the product's own context and terminology; a visual style does not authorize changes to behavior or data.

1. Preserve standard menu placement, keyboard shortcuts, text editing, undo, Services and window commands. Keep focus and default/cancel actions predictable.
2. Use window, panel, popover and sheet roles according to the task. Define resize behavior, minimum readable width, restored state and multiple-window ownership.
3. Build hierarchy with spacing, typography and semantic surfaces. Keep primary work readable and distinguish navigation, supporting metadata and commands without nested decoration.
4. Apply the bundled Qingshan Lake guidance through shared semantic tokens. Cover selection, focus, hover, disabled, loading, empty and error states; preserve geometry during state changes.
5. Use native accessibility roles and labels, logical keyboard order, adequate contrast, reduced motion and transparency fallbacks. Color alone cannot convey severity or selection.
6. Check long localized strings, narrow windows, light/dark appearance, large content and empty data. A screenshot of the default state does not prove complete behavior.

Use current primary references for implementation details and availability:

1. Apple Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines/
2. SwiftUI: https://developer.apple.com/documentation/swiftui
3. AppKit: https://developer.apple.com/documentation/appkit
4. Accessibility: https://developer.apple.com/accessibility/

This guide is an original review checklist. It does not reproduce a third-party design manual.
