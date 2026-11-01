# React Native

Use this reference for React Native and Expo apps targeting iOS and Android. Share semantic tokens and product structure, but keep platform interaction, sizing, accessibility, and system-surface behavior distinct.

## Architecture contract

- Use one typed semantic theme such as [assets/QingshanTheme.ts](../assets/QingshanTheme.ts). Components consume roles like `background`, `surface`, `text`, and `primaryAction`, not scenic seed colors.
- Use `useWindowDimensions()` so layout and `fontScale` update with rotation, split screen, foldables, and resized windows. Do not cache initial screen dimensions.
- Treat `compact` as up to 599 logical pixels, `medium` as 600–839, and `expanded` as 840 or more by default. Let large `fontScale`, content constraints, or the product's existing grid override these suggestions.
- Use platform checks for real behavior differences, not for duplicating entire screens.
- Keep navigation, modals, gestures, keyboard avoidance, Back behavior, VoiceOver, and TalkBack aligned with the host platform.
- React Native's core `SafeAreaView` is deprecated; use the safe-area solution already adopted by the project, such as `react-native-safe-area-context`.
- `useWindowDimensions()` handles resized foldable windows, but it does not expose a physical hinge or fold bounds. Avoid critical content near the center by default; use an established native module or platform adapter when exact hinge avoidance is a requirement, and report that boundary explicitly.

## Qingshan Design application

- Use an opaque mist canvas and readable surfaces by default. Native blur is optional and must have an opaque fallback; do not assume CSS `backdrop-filter` exists.
- Use `#286B66` for primary action fills with white labels. Keep the brighter lake teal for charts, focus, progress, and atmosphere.
- Use `PlatformColor` or the project's native semantic-color bridge when system adaptation is required. Do not replace matched foreground/container pairs independently.
- The bundled TypeScript theme supports a static Qingshan Lake brand palette only; it does not implement Android Dynamic Color. Use the static theme as the fallback on both platforms.
- If a product explicitly requires Dynamic Color, add a separate typed adapter backed by a maintained native bridge. Map matched Material roles together — including `primary/onPrimary/primaryContainer/onPrimaryContainer`, `secondary/onSecondary/secondaryContainer/onSecondaryContainer`, `background/onBackground`, `surface/onSurface/surfaceVariant/onSurfaceVariant`, `outline`, and `error/onError/errorContainer/onErrorContainer` — then test the computed scheme. Never replace only `primary`, and never imply that [assets/QingshanTheme.ts](../assets/QingshanTheme.ts) provides this capability.
- Keep `Pressable` states for pressed, hovered, and focused input when supported. Use `hitSlop` carefully; adjacent targets must not overlap.

## Layout and target sizes

- **iPhone/iPad:** design primary and frequent targets at least 44×44 points and respect Dynamic Type expectations.
- **Android:** design touch targets at least 48×48dp and preserve Material state semantics.
- **Compact:** one column; move filters or secondary controls to a sheet or modal.
- **Medium/expanded:** introduce list-detail or supporting panes when they reduce navigation; do not stretch body text across the full width.
- Use `FlatList`/`SectionList` for long collections and keep translucent effects outside repeated list rows.
- If large `fontScale` makes a multi-pane layout cramped, step down one layout class even when the width breakpoint permits more columns.

## Accessibility and motion

- Provide `accessibilityRole`, `accessibilityLabel`, `accessibilityState`, and value semantics for custom controls.
- For progress or charts, provide `accessibilityValue` and a text alternative. For example, expose `accessibilityValue={{ min: 0, max: 6, now: 4, text: '4 of 6 complete' }}` rather than an unlabeled decorative ring.
- Verify that grouping with `accessible` does not hide actionable children from VoiceOver or TalkBack.
- Query and subscribe through `AccessibilityInfo` for screen-reader state and `reduceMotionChanged`. iOS also exposes reduced transparency; Android exposes high-text-contrast state.
- Under Reduce Motion, stop travel, parallax, decorative loops, and animated blur. Prefer a static state or short cross-fade where supported.
- Announce important asynchronous success or error changes when visual focus does not make them obvious.

Centralize effect preferences instead of querying them in every screen:

```tsx
function useReducedEffects() {
  const [reduceMotion, setReduceMotion] = React.useState(false);

  React.useEffect(() => {
    AccessibilityInfo.isReduceMotionEnabled().then(setReduceMotion);
    const subscription = AccessibilityInfo.addEventListener(
      'reduceMotionChanged',
      setReduceMotion,
    );
    return () => subscription.remove();
  }, []);

  return { reduceMotion };
}
```

Extend the provider with iOS reduced-transparency and Android high-text-contrast checks when those settings affect the implemented surfaces. Also pause atmospheric work when the app is backgrounded or the surface is offscreen.

## Verification

- Test at least one current iPhone size, one small Android phone, one large/text-scaled state, and one tablet or foldable/resized window when supported.
- Check light/dark appearance, 200% text or large font scale, keyboard/IME, orientation, VoiceOver, TalkBack, Reduced Motion, and offline/loading/error states.
- Profile JS/UI thread behavior while gradients, blur, lists, and animation are active. Pause decorative work when offscreen or backgrounded.

## Official sources

- [React Native Accessibility](https://reactnative.dev/docs/accessibility)
- [AccessibilityInfo](https://reactnative.dev/docs/accessibilityinfo)
- [Dimensions](https://reactnative.dev/docs/dimensions)
- [Appearance](https://reactnative.dev/docs/appearance)
- [Pressable](https://reactnative.dev/docs/pressable)
- [SafeAreaView deprecation notice](https://reactnative.dev/docs/safeareaview)
