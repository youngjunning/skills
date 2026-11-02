# Adapting an existing HTML report

Use this path when a report renderer, HTML framework, or finished report already exists. The goal is a Joyally Design visual adapter, not a replacement report framework.

## Preserve first

Before editing, inventory and preserve:

- heading hierarchy and document landmarks;
- existing metadata; add `<meta name="viewport" content="width=device-width, initial-scale=1">` when the report lacks a responsive viewport declaration;
- IDs, anchor targets, deep links, and table-of-contents behavior;
- data attributes, hydration roots, event handlers, and export hooks;
- finding severity, evidence references, timestamps, task/session identifiers, and source URLs;
- loading, empty, partial, failure, retry, and print/export behavior;
- sanitization and escaping boundaries for report content.

## Map the framework to semantic regions

Map existing selectors to these roles without renaming the DOM unless the existing structure cannot express the role:

| Report role | Joyally Design selector or token | Treatment |
| --- | --- | --- |
| Document canvas | `.joyally-report`, `--bg` | Mist-white field with atmosphere at the perimeter |
| Main readable surface | `--surface` | Opaque enough for long text |
| Report identity | `.report-header` | Owner or series, title, concise scope, metadata |
| Decision summary | `.report-summary` | Strongest non-hero region; conclusion before detail |
| Finding | `.report-finding` | Left severity rail, explicit priority text, restrained shadow |
| Evidence | `.report-evidence` | Opaque table, screenshot, trace, or link region |
| Navigation | `.report-nav` | Quiet sticky navigation only for long reports |
| Supporting metadata | `--text-3` | Visible but below findings and evidence |

If the framework already exposes its own tokens, add an adapter stylesheet that aliases them to Joyally Design/Pakco semantic tokens. Prefer this over replacing every literal selector:

```css
.joyally-report {
  --report-canvas: var(--bg);
  --report-surface: var(--surface);
  --report-text: var(--text-1);
  --report-muted: var(--text-2);
  --report-primary: var(--accent);
  --report-border: var(--border);
}
```

Scope overrides under `.joyally-report` so embedded reports do not restyle their host application. Load the Joyally Design theme after the report framework's base stylesheet unless the framework requires a documented layer order.

## Composition rules

- Keep a readable content measure. Evidence tables may expand wider than prose.
- Use natural scrolling and content-driven section heights. Do not turn report sections into slides.
- Use one strong summary surface, then flatter content sections. Avoid a dashboard grid of equal cards.
- Keep evidence next to the finding it supports. Do not move screenshots into a decorative gallery detached from the conclusion.
- Use atmosphere in the header and outer canvas. Use opaque surfaces behind tables, code, logs, and long descriptions.
- On narrow screens, move navigation into normal flow and allow evidence tables to scroll horizontally without hiding meaning.
- In print, remove sticky navigation and atmosphere, preserve URLs where useful, and avoid splitting a finding from its first evidence block.

## Acceptance

1. Compare the same report before and after at desktop and narrow widths.
2. Confirm the narrow browser reports the requested CSS viewport width rather than the legacy 980px layout viewport.
3. Follow every internal anchor and evidence link.
4. Exercise long titles, long findings, empty evidence, broken media fallback, and the highest supported finding count.
5. Print or export to PDF and inspect page breaks, clipped tables, contrast, and URLs.
6. Confirm that visual adaptation did not change report data, sorting, severity, or interaction behavior.
