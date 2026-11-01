# Web dashboard

Use this reference for professional web apps, admin tools, data consoles, settings, and Agent workspaces.

## Information architecture

- Start from the real workflow: navigation, context, controls, feedback, result, and next action.
- Prefer stable sidebars, compact toolbars, filters, tables, charts, and status strips over a marketing-style hero.
- Use a balanced or compact density: 8px base, 12–16px card padding, 20–24px section gaps, 32–40px controls for pointer-first desktop UI.
- Collapse columns and relocate filters on narrow screens; never preserve a desktop grid by shrinking text below readable sizes.

## Qingshan Design application

- Build the page from low-noise canvas, readable surfaces, lake-teal interaction, cypress status, and gray-blue secondary hierarchy.
- Use CSS `backdrop-filter` only when content remains legible without it. Supply an opaque fallback.
- Keep tables and long-form content more opaque than navigation or transient overlays.
- Use atmosphere around empty/welcome areas, not behind dense tables or long text.
- Limit charts to one or two emphasized series; de-emphasize grids and axes without making them disappear.

## Web interaction contract

- Use semantic HTML and native controls before custom div-based interactions.
- Keep keyboard order logical and focus never obscured by sticky headers or overlays.
- Target WCAG 2.2 AA: 4.5:1 normal text, 3:1 large text and non-text UI, and at least 24×24 CSS px targets or sufficient spacing. Prefer 36–44px for important controls.
- Provide error text, icons, or shapes in addition to color.
- Use `prefers-reduced-motion`, `prefers-contrast`, `forced-colors`, and an opaque Reduced Transparency strategy where supported.

## Responsive states

- **Wide:** sidebar + primary content + optional inspector only when each pane stays useful.
- **Medium:** collapse the inspector or convert it to a drawer.
- **Narrow/touch:** single column, reachable controls, filter sheet, card/list alternative for tables when horizontal scrolling would hide meaning.

## Official sources

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [WCAG target size minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum)
- [WCAG focus appearance](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance)
- [Media Queries Level 5](https://www.w3.org/TR/mediaqueries-5/)
- [Responsive web design basics](https://web.dev/articles/responsive-web-design-basics)
