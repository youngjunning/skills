# Pakco HTML integration

## Boundary

The bundled Pakco HTML subset supplies local layout and webpage primitives. Joyally Design supplies the report theme and content hierarchy.

- Upstream: `https://github.com/pakco77/pakco-html`
- License: MIT
- Verified upstream commit: `8cefc6b6b68d85a1484e066c47ae571b75d0d4e1` on 2026-09-09
- Bundled compatibility surface: `assets/base.css`, optional deck-only `assets/runtime.js` and `assets/animations/animations.css`, webpage primitives, semantic CSS tokens, `.deck`, `.slide`, `.notes`, and hash navigation

The compatible upstream capability is bundled under `vendor/pakco-html/`; consumers do not need another Pakco installation, another Skill, or network access. For HTML reports, use the local webpage primitives documented here. Consult individual bundled references only when their specific implementation detail is needed:

- webpage mode for vertically scrolling reading artifacts;
- layouts for complex report sections;
- render guidance for visual proof;
- deck runtime only when the user explicitly requests slides or a roadshow.

## Generated artifacts

`new-joyally-html.mjs report` creates a portable directory:

```text
<report>/
├── index.html
└── pakco/
    ├── LICENSE
    ├── base.css
    └── joyally-theme.css
```

The generated report carries only the Pakco files it uses. It uses natural browser scrolling, Joyally Design's report shell, print styles, and local system-font fallbacks; it does not request web fonts. Adapt an existing report framework in place when it already has a stronger schema or renderer; the starter is a reference implementation, not a required data model.

`new-joyally-html.mjs deck` remains available as a secondary, explicitly requested path. It additionally copies local runtime and animation assets; it does not fetch or install Pakco.

## Authoring rules

- Start from the Joyally Design report shell and Pakco webpage primitives. Do not import an unrelated Pakco theme and recolor it afterward.
- Use semantic tokens in report content. Add a new Joyally Design token only when existing roles cannot express the meaning.
- Keep report-specific atmosphere in `joyally-theme.css` or a scoped report-local stylesheet loaded after it. Keep bundled Pakco base files unmodified.
- Preserve natural scrolling, headings, landmarks, anchors, evidence links, and print behavior.
- Keep external media or CDN availability separate from local report correctness. Provide a visible fallback for critical media.
- Render representative report regions and inspect desktop, narrow-screen, and print output. Static validation alone does not prove visual acceptance.

## Updating upstream

When the user explicitly requests a Pakco update, fetch the official repository into a temporary directory and refresh only `vendor/pakco-html/assets`, `templates`, `references`, `scripts/render.sh`, `LICENSE`, and `UPSTREAM_SKILL.md`. Record the resolved commit, regenerate temporary report and deck artifacts, run the validator, and visually compare representative pages. Update the verified commit in this reference only after compatibility is confirmed.
