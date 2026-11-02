# Validation

## Shared acceptance gate

Do not claim completion from source inspection or a successful build alone.

1. Render the real app or page with representative content.
2. Check primary workflow, empty, loading, error, success, disabled, focused, pressed, and selected states.
3. Verify the smallest and largest supported window/viewport plus one intermediate state.
4. Test long text and localization expansion.
5. Test keyboard or hardware-key navigation where supported.
6. Inspect with VoiceOver, TalkBack, or browser accessibility tools as appropriate.
7. Enable Reduced Motion, Reduced Transparency or opaque fallback, Increased Contrast, and Differentiate Without Color/forced colors where available.
8. Check light and dark appearances when supported.
9. Verify foreground/background contrast from computed or runtime colors, not only source hex values.
10. Inspect performance while atmosphere is idle, offscreen, and backgrounded.

## Style gate

- The screen expresses the product's own brand without relying on a literal scenic image.
- Primary action, navigation, and status are immediately legible.
- Atmospheric effects never sit between users and dense content.
- Color, imagery, and material choices follow the chosen brand and content.
- Decorative patterns serve hierarchy and meaning rather than filling empty space.
- Custom styling preserves the platform's semantics and input behavior.

## Token gate

Run:

```bash
python3 scripts/validate-native-tokens.py
```

The script validates required roles, hex syntax, token references, and declared WCAG contrast pairs in `assets/joyally-native.tokens.json`.

## Handoff evidence

Report these states independently:

- design contract written;
- source implemented;
- static validation passed;
- build/test passed;
- real UI inspected;
- device/platform accessibility inspected;
- committed and pushed;
- deployed;
- production verified.
