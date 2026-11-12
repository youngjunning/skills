# Joyally Design HTML reports and presentations

Use the bundled layouts, CSS tokens, and local assets to create portable HTML:

- webpage mode for vertically scrolling reading artifacts;
- layouts for complex report sections;
- render guidance for visual proof;
- deck runtime only when the user explicitly requests slides or a roadshow.

## Generated artifacts

`node scripts/design-engine.mjs report <output-dir>` creates a portable directory:

```text
<report>/
├── index.html
└── joyally-design/
    ├── LICENSE
    ├── base.css
    └── joyally-theme.css
```

The generated report uses natural scrolling, print styles, and system font fallbacks. Adapt an existing report in place when it already has a stronger schema or renderer.

`node scripts/design-engine.mjs deck <output-dir>` adds local playback and animation assets for a three-slide starter. For a complete presentation, use a scenario or a JSON slide source as described in [演示文稿制作](presentations.md). Keep `.deck`, `.slide`, `.notes`, and hash navigation.

## Authoring rules

- Start from the Joyally Design report shell and its local layout primitives.
- Use semantic tokens in report content. Add a new Joyally Design token only when existing roles cannot express the meaning.
- Keep report-specific styles in `joyally-theme.css` or a scoped report-local stylesheet loaded after it.
- Preserve natural scrolling, headings, landmarks, anchors, evidence links, and print behavior.
- Keep external media or CDN availability separate from local report correctness. Provide a visible fallback for critical media.
- Render representative report regions and inspect desktop, narrow-screen, and print output. Static validation alone does not prove visual acceptance.
