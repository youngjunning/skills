# Joyally Design HTML reports

Use the bundled layouts, CSS tokens, and local assets to create portable HTML:

- Joyally's own natural scrolling report layout;
- layouts for complex report sections;
- render guidance for visual proof.

## Generated artifacts

`node scripts/design-engine.mjs report <output-dir>` creates a portable directory:

```text
<report>/
├── index.html
└── joyally-design/
    ├── report-base.css
    └── joyally-theme.css
```

The generated report uses Joyally's own CSS, natural scrolling, print styles, and system font fallbacks. Adapt an existing report in place when it already has a stronger schema or renderer.

`assets/report-demo.html` is a worked example with explicitly fictional ticket data. It shows how to replace the starter placeholders with a conclusion-led opening, measured comparisons, and evidence using only Joyally report styles.

The lake report uses an editorial hierarchy: a Song-style display title, a decisive conclusion surface, large measured values, crisp section rules, and quiet evidence tables. Keep the typographic contrast and section rhythm when adapting it; use the report's own content to choose which number or finding deserves emphasis. This is a Joyally report treatment, not a deck or a generic landing page.

## Authoring rules

- Start from the Joyally Design report shell and its local layout primitives.
- Put the report's actual takeaway and its most important measured value in the first screen. Use a short metric strip only when each figure has a clear unit, comparison baseline, and source; use a simple visual comparison when it helps readers see a real change.
- Use semantic tokens in report content. Add a new Joyally Design token only when existing roles cannot express the meaning.
- Keep report-specific styles in `joyally-theme.css` or a scoped report-local stylesheet loaded after it.
- Preserve natural scrolling, headings, landmarks, anchors, evidence links, and print behavior.
- Keep external media or CDN availability separate from local report correctness. Provide a visible fallback for critical media.
- Render representative report regions and inspect desktop, narrow-screen, and print output. Static validation alone does not prove visual acceptance.
