# Qingshan Lake SwiftUI Design System

Use this bundled reference as the complete default visual specification for macOS work. It has no dependency on the host application, a repository-local palette, or external design documentation. If a project already defines stricter tokens or surface rules, preserve those as project-specific extensions.

## 1. Visual source and character

Derive the system from a misty lakeside landscape rather than a generic “Chinese ink painting” theme:

- Blue mist sky supplies cool atmospheric depth and low-contrast distance.
- Horizontal cloud belts soften boundaries between lake, hills, and controls.
- Lake teal provides restrained selection, focus, and progress accents.
- Deep cypress forest supplies text, dark surfaces, and structural contrast.
- Gray-blue hills support secondary surfaces without becoming generic gray chrome.
- Wet wood and bridge lamps provide rare human warmth.
- Duckweed green provides tiny signs of life, never a dominant theme.

The result should feel quiet, translucent, natural, and native to macOS. Reject tourism-poster imagery, cyber blue/purple, pure-black developer-tool styling, neon green, and large gold decoration.

## 2. Standalone SwiftUI tokens

If the target project has no equivalent shared palette, add one centrally and reuse it across all surfaces. Rename the type to match the project if needed, but preserve token meaning and approximate values.

```swift
import SwiftUI

enum QingshanLakePalette {
    // Text and structure
    static let primaryInk = Color(red: 0.06, green: 0.17, blue: 0.21)
    static let secondaryInk = Color(red: 0.24, green: 0.39, blue: 0.43).opacity(0.82)
    static let qingshanInk = Color(red: 0.12, green: 0.25, blue: 0.27)
    static let lakeBlue = Color(red: 0.26, green: 0.40, blue: 0.48)
    static let cypressDeep = Color(red: 0.07, green: 0.20, blue: 0.16)

    // Mist and atmosphere
    static let mistWhite = Color(red: 0.95, green: 0.97, blue: 0.95)
    static let warmMist = Color(red: 0.91, green: 0.87, blue: 0.76)
    static let blueMist = Color(red: 0.54, green: 0.68, blue: 0.82)
    static let cloudBelt = Color(red: 0.72, green: 0.80, blue: 0.86)
    static let lakeMist = Color(red: 0.52, green: 0.78, blue: 0.73)

    // Active states
    static let lakeTeal = Color(red: 0.18, green: 0.58, blue: 0.54)
    static let cypressGreen = Color(red: 0.18, green: 0.44, blue: 0.34)
    static let cypressFresh = Color(red: 0.28, green: 0.62, blue: 0.29)

    // Rare accents
    static let duckweedGreen = Color(red: 0.32, green: 0.68, blue: 0.10)
    static let reedSand = Color(red: 0.76, green: 0.68, blue: 0.46)
    static let dawnGold = Color(red: 0.84, green: 0.64, blue: 0.32)
    static let bridgeLamp = Color(red: 0.93, green: 0.70, blue: 0.42)
    static let wetWood = Color(red: 0.43, green: 0.20, blue: 0.10)
}
```

Use `lakeTeal` and `cypressGreen` for active controls. Use `primaryInk` and `secondaryInk` on light surfaces. Use `mistWhite` on sufficiently dark surfaces. Do not use `mistWhite` as light-surface body text. Use warm tokens for small status points, edge light, or exceptional states only.

## 3. Surface recipes

### Light application surface

- Base: `mistWhite` around 0.90–0.98 opacity.
- Atmosphere: low-opacity `blueMist`, `lakeMist`, or `cloudBelt` radial/linear gradients.
- Content text: `primaryInk`; supporting text: `secondaryInk`.
- Border: one-pixel `lakeTeal` or `lakeMist` around 0.12–0.28 opacity.
- Shadow: optional, cool and restrained; verify on a light desktop before keeping it.

### Dark application surface

- Base: layer `qingshanInk`, `cypressDeep`, and low-opacity `blueMist`; never use pure black as the designed surface.
- Primary text: `mistWhite`; secondary text: `mistWhite` at reduced opacity.
- Rows: lightweight translucent ink layers rather than thick nested cards.
- State accents: lake teal, cypress green, or a tiny bridge-lamp warmth.

### Navigation and control layer

- Use system material where it supports native behavior, then add a restrained mist/lake tint.
- Make selected state unmistakable with lake teal or cypress fill, shape, and text contrast.
- Keep unselected controls quiet but readable in deep-lake text.
- Avoid glass-on-glass. Content should be quieter than navigation.

### Content layer

- Prefer spacing, typography, and alignment over extra containers.
- Use mist-white translucent cards only when grouping is necessary.
- Avoid heavy borders, opaque white rectangles, and repeated nested rounded cards.

## 4. Control contract

| Control | Preserve | Qingshan Lake appearance | Reject |
|---|---|---|---|
| Primary action | `Button`, keyboard activation, VoiceOver label | lake-teal to cypress gradient or restrained lake-teal fill; mist-white label; continuous corner | bare `.borderedProminent`, system blue |
| Secondary action | `Button` semantics | mist-white translucent fill, lake-teal soft border, deep-lake text | generic gray bordered button |
| Segmented selection | exclusive selection, arrow/tab navigation, selected value | shared mist capsule; selected segment lake-teal/cypress; unselected deep-lake text | bare `.pickerStyle(.segmented)` |
| Toggle | `Toggle` value/role and accessibility | custom `ToggleStyle`; lake-teal selected state; visible custom focus | default switch or unstyled `.toggleStyle(.button)` |
| Text field/editor | native text editing, undo, selection, Services | plain control in mist fill; lake-teal focus stroke; restrained warm error stroke | default bezel or default blue focus ring |
| Menu/popover | menu semantics and keyboard behavior | styled trigger; custom Qingshan Lake popover when the visible body is product UI | default blue trigger or generic white feature popover |
| Sheet/alert | modal semantics, Escape/default action | mist/lake surface, styled close control, actions, and focus | default white sheet and blue primary action |
| Progress/loading | accessibility value and Reduce Motion | lake-teal/cypress progress and low-opacity mist pulse | perpetual decorative animation while idle |

When a native style cannot express the contract, retain the native control type and implement a project `ButtonStyle`, `ToggleStyle`, `TextFieldStyle`, or `PickerStyle`. Build a custom interaction primitive only when necessary, then restore keyboard behavior, focus, accessibility value, and hit target explicitly.

### Sidebar exclusive selection

`NavigationSplitView` with `List(selection:)` can keep drawing the system accent highlight even when the surrounding surface uses a custom palette. Do not treat `.tint(lakeTeal)` as the finished style. For a product-themed sidebar:

- Keep `NavigationSplitView` and native `Button` semantics, but render each destination as a custom full-width row in a `ScrollView`/`VStack` when system selection chrome cannot satisfy the visual contract.
- Give the selected row a restrained `lakeTeal` to `cypressGreen` fill, `mistWhite` label, continuous shape, and one-pixel same-shape stroke. Keep unselected rows clear; use a low-opacity `lakeMist` hover fill.
- Make pressed state slightly darker or smaller, and draw a lake-teal focus stroke. Do not allow the focus ring or selected fill to fall back to blue.
- Preserve Up/Down keyboard movement with `onMoveCommand`, move focus with selection, and make reselecting the current destination a no-op.
- Add `.isSelected` for accessibility. Under Differentiate Without Color, add a checkmark, leading marker, or another non-color cue.
- Verify selected, unselected, hover, pressed, focused, Increased Contrast, Reduced Transparency, keyboard, and VoiceOver states in the real app. A static screenshot of the selected row is not sufficient acceptance.

Minimal structure:

```swift
@State private var selection: Destination = .overview
@FocusState private var focused: Destination?

ScrollView {
    VStack(spacing: 6) {
        ForEach(Destination.allCases) { destination in
            Button {
                guard selection != destination else { return }
                selection = destination
            } label: {
                Label(destination.title, systemImage: destination.symbol)
                    .frame(maxWidth: .infinity, minHeight: 44, alignment: .leading)
            }
            .buttonStyle(QingshanSidebarButtonStyle(
                isSelected: selection == destination,
                isFocused: focused == destination
            ))
            .focused($focused, equals: destination)
            .accessibilityAddTraits(selection == destination ? .isSelected : [])
        }
    }
}
.onMoveCommand { direction in
    moveSelection(direction) // Clamp bounds, update selection and focus, no-op at the edge.
}
```

## 5. Required states

Every reusable control must define or inherit:

- idle
- hover
- pressed
- selected/on
- focused
- disabled
- loading, when applicable
- error, when applicable
- Increased Contrast
- Reduced Transparency
- Reduced Motion

Use shape, stroke, icon, or label changes in addition to color. Keep visible controls at least 36 pt and important click targets at least 44×44 pt where the surface allows it.

## 6. Composition and transparent windows

For translucent rounded surfaces, keep modifier order stable:

```text
content
→ material/background and restrained tint
→ clipShape with a continuous rounded shape
→ one-pixel stroke
→ optional visually verified shadow
→ external transparent padding required by that shadow
```

For transparent `NSPanel` or `NSWindow`:

- Give the SwiftUI root the shared continuous corner and matching clip.
- Give `NSHostingView` a clear layer background, matching `cornerRadius`, `.continuous` corner curve, and `masksToBounds = true`.
- Set the window to non-opaque with a clear background.
- Do not use AppKit's rectangular default shadow as the visible boundary.
- Verify all four corners on a light background; checking only the center is insufficient.

## 7. Focus and accessibility

- Remove the default focus effect only after adding a custom visible focus stroke.
- Keep focus discoverable during keyboard navigation and Increased Contrast.
- Keep labels meaningful without relying on artwork or color.
- Respect `accessibilityReduceMotion` and `accessibilityReduceTransparency`.
- Preserve native text behavior by styling the editor container instead of rebuilding text editing.
- Do not encode state by color alone.

## 8. Audit before handoff

Search the Swift source root, regardless of project layout:

```bash
rg -n "pickerStyle\(\.segmented\)|buttonStyle\(\.borderedProminent\)|toggleStyle\(\.button\)|TextField\(|TextEditor\(|\.sheet\(|\.alert\(|Menu\(" . --glob '*.swift'
```

Treat matches as an audit list, not a ban on native APIs. For each match, verify Qingshan Lake styling and complete state treatment.

Then verify:

1. Light desktop: no white rectangular backing, clipped shadow, hard gray border, or system blue.
2. Keyboard-only path: every primary action and selection works; custom focus is visible.
3. VoiceOver: labels, selected values, toggle values, and progress values are announced.
4. Reduced Motion/Transparency and Increased Contrast remain readable and operable.
5. Resizing and long localized strings do not clip or overlap.
6. Sheets, alerts, popovers, context menus, toasts, debug/test UI, loading, empty, disabled, and error states follow the same system.

Do not report a surface complete until these checks pass.
