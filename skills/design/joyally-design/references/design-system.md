# Joyally Design: design system and bundled preset

Joyally Design supplies a cross-platform method for hierarchy, semantic tokens, component behavior, and evidence-rich reports. Chinese-inspired, landscape, and fashion-led aesthetics may coexist or be combined for a product. The documented [landscape direction](visual-language.md) includes Qingshan Lake, West Lake, Suzhou Gardens, Lingering Garden, Maldives, and [Alpine Snow Mountains](alpine-snow-mountains.md) as equal scene themes. The bundled [tokens](../assets/joyally-design.tokens.json) and [HTML theme](../assets/joyally-html-theme.css) currently implement a Qingshan Lake preset; other themes and directions need their own mapping while retaining semantic roles and validation. Another brand may provide its own token values and theme. Ant Design, Material 3, Radix Primitives, shadcn/ui, Tailwind CSS, and Magic UI each contribute a bounded implementation strength.

## Design character

Choose the report's visual character from the product brief, brand assets, and reading context. The following cues describe Joyally's own visual identity. Landscape cues are abstract responsibilities rather than literal scenery.

| Visual cue | Report responsibility |
| --- | --- |
| Mist-white field | Canvas, breathing room, and quiet material |
| Lake teal | Primary action, selection, focus, and progress |
| Cypress green | Success, recovery, and validated capability |
| Gray-blue structure | Secondary text, boundaries, inactive state, and metadata |
| Deep lake ink | Primary text, conclusions, and evidence |
| Dawn gold and clay | Warning and error signals used sparingly |
| Sparse particles or gradients | Peripheral identity around the header, never behind evidence |

### 青山湖四季参考与统一映射

Inspect landscape references and their provenance before selecting the theme palette. 青山湖以春夏秋冬各 5 张授权实拍为收集目标；已核实与待补的数量见[参考目录](../assets/references/qingshan-lake/README.md)。

Use spring's new green, summer's fuller cypress canopy, autumn's copper foliage and winter's cool mist as cues within one theme. Keep the large application canvas warm mist-white; use lake color, reflected sparkle, duckweed, cloud mist and low sun as local supporting details. Text, tables and evidence stay on opaque reading surfaces.

Empty work surfaces may use visible but soft neutral gray-white mist at their edges. Build it from overlapping, uneven patches with slow motion, keep it away from text and controls, and stop the motion for reduced-motion preferences. Mist must not recolor the canvas or appear as a repeated geometric band.

| Source cue | Token direction | UI use |
| --- | --- | --- |
| Shadowed cypress and matcha green | `#4E7159` / `#52795A` family | Primary actions, links, focus, navigation and Chat selection |
| Red and yellow cypress foliage | `#C86848` / `#D89848` sampled highlights; `#A7472D` / `#96620F` readable status text | Foliage artwork, error and warning feedback |
| Low sun and water sparkle | Small localized highlights | Never a page-wide color wash |
| Warm mist-white paper | `#F7F3EB` / `#FCFAF4` | Canvas, cards, readable content surfaces |

Primary actions use the theme's deep cypress green; selected navigation, Chat rows and other active controls use a quiet green fill with dark text. Red cypress is reserved for error and destructive feedback, yellow cypress for warning, each paired with an icon or label. Keep these semantic colors off large interactive surfaces; success remains green and the rest of the interface stays quiet.

Status colors keep the same meaning in every mode: use cypress red `#A7472D` for error text and icons with `#FBEAE2` / `#D9A28E` for the light fill and border; use cypress yellow's darker readable tone `#96620F` for warning text and icons with `#FFF2D9` / `#E5B663` for the fill and border. The brighter sampled foliage colors are source hues, not small-text colors.

The result should remain recognizably Joyally Design without requiring a 产品专属 logo, character, product screenshot, literal lake image, or scenic poster composition.

## Style and mood

Style and mood are peer-level design decisions, but they answer different questions:

| Dimension | Answers | Examples |
| --- | --- | --- |
| Style | How does the interface look and behave? | Contemporary Chinese cues, celadon-glaze material, glass material, compact density, restrained motion |
| Mood / 意境 | What feeling, spatial distance, and narrative temperature should the interface leave? | Quiet distance, understated warmth, light time-worn texture, clear and youthful calm |

For the bundled lake-landscape preset, the mood / 意境 is a quiet, youthful sense of distance and time. Its references may include the cool object-focus and spacious composition associated with *青花瓷*, and the restrained seasonal/time feeling associated with *东风破*. Use those as high-level atmosphere references only: do not quote lyrics, reproduce song copy, or imitate a musical work. For any brand, `mood` means emotional atmosphere plus spatial distance, temporal feeling, and narrative restraint. Derive it from the product brief and express it through pacing, contrast, section rhythm, imagery selection, and visual silence; it never overrides hierarchy, readability, accessibility, or evidence.

## Reference system matrix

Joyally Design uses a multi-reference approach. Each reference system contributes a bounded capability; none is treated as the complete brand or as a reason to add another visual theme.

| Reference | Adopted responsibility | Joyally Design translation |
| --- | --- | --- |
| Ant Design | Token derivation, component tokens, enterprise information density, feedback states | `Seed → Map → Alias → Component`, compact workbench defaults |
| Material 3 | Semantic roles, tonal surface relationships, state layers, motion and accessibility | Clear state layers and appropriate tonal contrast on the chosen surfaces |
| Radix Primitives | Keyboard behavior, focus management, WAI-ARIA patterns, overlay logic | Shared primitives must remain operable before styling is applied |
| shadcn/ui | Open component source, composition, predictable local APIs | Components stay editable in `components/ui` and use explicit variants |
| Tailwind CSS | Theme variables and utility composition | Alias tokens exposed through `@theme`; utilities express layout |
| Magic UI | React Web 默认组件来源，提供可复用展示组件与部分交互 | 从 registry 按需安装并映射项目 tokens；动效保持可降级 |
| Joyally Design | Own visual identity and cultural expression | Choose or combine aesthetic directions for Joyally-branded surfaces; derive another product's visual values from its brand |

This matrix is a division of responsibilities, not a request to install every library. The project should keep one semantic token vocabulary and one component contract while borrowing proven solutions where each reference is strongest.

## Contemporary Chinese expression in the bundled preset

中国传统文化只作为可转译的视觉语汇，不限定单一朝代；排除清代典型审美、服饰、宫廷纹样与相关符号，不做清代历史复原。现代清晰度、年轻感和产品可用性优先，传统线索必须经过轻量、当代的设计转译。

Use traditional Chinese references as selective visual cues inside a modern, youthful product grammar rather than as a decorative or retro theme:

| Cultural cue | Modern UI translation | Boundary |
| --- | --- | --- |
| Ink and stone | Deep ink text, quiet gray-blue structure, evidence hierarchy | Never use near-black for every label or border |
| Celadon and lake water | Primary action, selection, focus, and progress | Keep controls readable and do not turn the whole surface green |
| Cinnabar seal | Critical marker, destructive confirmation, or one key emphasis | Rare, semantic, and always paired with text or icon |
| Xuan paper and mist | Canvas, empty state, and low-contrast surface | No texture beneath dense evidence or forms |
| Deliberate留白 | Content measure, alignment, and deliberate section rhythm | Do not create oversized empty hero blocks |
| Seal, inkstone, bamboo, scroll, bronze mirror, mountain-water outline | Topic-relevant illustration or branded icon subject | Use only when the subject explains the object; functional icons keep stable geometry |

Typography follows the same rule: modern sans-serif carries body copy and controls; a restrained Song-style serif is limited to a display title, report cover, or small kicker. Do not use faux-ancient fonts for navigation, tables, or operational text.

## Token architecture

Use the shared `Seed → Map → Alias → Component` mapping, informed by Ant Design's token model and Material 3's semantic roles. The bundled `semantic` group is the project's Alias-token representation. Components consume Alias roles rather than scenic names or copied hex values.

### Design language and appearance layers

Design language and runtime appearance are related but not interchangeable. 青山湖从四季参考中提炼一套固定主题映射：

| Layer | Axis | Values | Owns | Does not own |
| --- | --- | --- | --- | --- |
| Design language | `style` | `contemporary-chinese-cues` | Visual grammar: form, cultural references, typography, icon treatment, and motion restraint | Current luminance |
| Design language | `mood` | `quiet-youthful-distance` (baseline) | 意境：emotional atmosphere, spatial distance, temporal feeling, and narrative restraint | Semantic state meaning or task hierarchy |
| Appearance | `mode` | `light` / `dark` | Luminance, contrast, foreground/background pairing, and elevated-surface behavior | Theme identity or surface texture |
| Implementation preset | `material` | `celadon-glaze` / `glass` (extensible) | Surface treatment, translucency, border, highlight, and shadow expression | Semantic meaning, content hierarchy, or state color |

The four seasons are reference categories, not selectable token sets. Their observed colors and structures resolve into one Alias and Component contract. Shared dimensions, typography, interaction states, accessibility, and density stay single-source. The default is `mode=light`, `material=celadon-glaze`.

The executable appearance contract lives in `joyally-design.tokens.json.appearanceContract`:

- `themeTokens` contains the semantic color slots supplied by the 青山湖 theme.
- `materialTokens` contains surface alpha, quiet-border alpha, blur and fallback behavior for each material. `celadon-glaze` is the more opaque, glaze-like surface; `glass` is more translucent and is restricted to perimeter/orientation surfaces.
- `materialRules` is a hard boundary: `surfaceRoles` names material-bearing chrome and opaque reading areas; transparency is forbidden behind evidence/table/code/log/long text, and `semanticColorsUnaffected` must remain `true`.

When changing theme tokens or material, update the JSON first and run `python3 .codex/skills/joyally-design/scripts/validate-joyally-tokens.py`. Do not add a CSS selector or page-local variable without a corresponding contract entry. If a browser cannot support `backdrop-filter`, or the user requests reduced transparency, remove the effect and use the declared opaque fallback; do not lower text contrast to preserve the material.

### Element coverage and material boundaries

Material support is a coverage contract, not a single panel style. The theme supplies the canvas, foliage palette, semantic colors, and selected-state meaning. Material changes only the optical treatment of surfaces: alpha, blur, border, highlight, and shadow. Both materials derive their subtle tint from the theme; switching material preserves success, warning, error and focus colors. Every shared surface must choose one of the following roles before implementation:

| Element group | 青瓷釉 (`celadon-glaze`) | 玻璃拟态 (`glass`) | Required fallback and checks |
| --- | --- | --- | --- |
| App shell and outer header | Opaque, lightly theme-tinted glaze with a soft fired edge | Translucent perimeter with blur, bright edge, and lifted shadow | Page canvas keeps the same theme color in both materials; keep labels readable |
| Sidebar, navigation item, tab, selected conversation item, interactive skill card | Solid glaze and inset edge | Translucent tile or shell, visible specular edge and blur | Selected state keeps its theme-derived tint and geometry in both materials; apply treatment to highlighted items even when inactive |
| Page frame and supporting panel | Solid outer frame with a quiet glaze gradient | Translucent outer frame that reveals the theme canvas | The table or document inside stays opaque; audit page-specific CSS that may cover the shared frame rule |
| Toolbar shell, filters, compact controls | Opaque or near-opaque glaze | Glass on surrounding chrome; editable controls stay opaque | Preserve 32–36px control height and visible focus, hover, pressed, disabled states |
| Primary and outline actions | Keep the theme's semantic action color, add a thin glazed highlight and inset fired edge; outline actions use an opaque tinted surface | Keep the same action meaning with a quieter specular edge; outline actions may use translucent chrome | Check default, hover, pressed, focus, disabled and reduced-transparency states; the material must not change success or danger semantics |
| Card shell, Chat status tile, Chat document header and footer | One solid glazed shell with a single visible edge | One translucent shell with blur and specular edge | Keep the document body opaque; avoid nested preview rectangles or multiple competing material layers |
| Dialogs, popovers, drawers | Solid readable surface | Glass may appear on the outer chrome; reading and form areas stay opaque | Keep overlay contrast, Escape/focus behavior, and an opaque fallback |
| Tables, form fields, editors, composer input, Chat document body, logs, code, long text, screenshots, evidence | Always `surfaceStrong` and opaque | Always `surfaceStrong` and opaque | Local scrolling is preferred to shrinking text; semantic severity needs text/icon/shape |
| Empty, loading, error, success states | Use the same surface role as the parent and explicit semantic colors | Glass can frame the state but cannot reduce message contrast | Keep final layout footprint during loading; provide recovery for errors |
| Input, editor, composer | Opaque enough to distinguish editable area from its shell | Glass may surround but not replace the editable surface | Focus ring and placeholder contrast must remain visible in both materials |

The migration order is shell → navigation and emphasis markers → page frames → controls → cards and overlays → opaque reading surfaces → state variants. Audit both materials on the same page and mode at desktop and narrow widths, then repeat with `prefers-reduced-transparency` or an equivalent low-transparency setting. Include at least one selected navigation tile, a page frame with a table, and a Chat document card with header, body, and footer. Compare computed background alpha, blur, border, and shadow as well as screenshots; a changed border alone is not a perceptible material switch. A material is complete only when all groups have an explicit treatment, a fallback, and a contrast check; a page that styles only its hero or main card is incomplete.

For contrast checks, read the computed text color and its effective background in the rendered page, including the theme canvas beneath translucent chrome. Compare normal text and its background against the token contract's 4.5:1 minimum; run the bundled token validator for the declared semantic pairs. Repeat after reduced transparency removes blur and replaces translucent surfaces with opaque fills. Check focus and selected states for a visible shape, edge, or text cue in addition to color, and inspect long text, table cells, form fields, and evidence against their own opaque backgrounds.

In a material picker, show one swatch per material. Each swatch is one surface with its own theme-derived color and optical treatment. A second inner rectangle reads as another layer or an unrelated preview and hides the actual difference.

In product language, call `celadon-glaze` **青瓷釉** or a **surface material**, not a “celadon base.” “Texture” or “质感” describes the visual result; it is not the token axis.

| Report meaning | Semantic role | Typical use |
| --- | --- | --- |
| Document canvas | `background` | Page background and outer breathing room |
| Reading surface | `surface`, `surfaceStrong` | Prose, findings, evidence, tables, code |
| Quiet grouping | `surfaceMuted`, `primarySubtle` | Metadata, scope, filters, supporting context |
| Primary text | `text` | Conclusions, headings, evidence |
| Supporting text | `textSecondary`, `textTertiary` | Metadata and annotations |
| Current decision or action | `primary`, `primaryAction` | Links, focus, active navigation, CTA |
| Validated outcome | `success` | Complete or verified state |
| Attention and risk | `warning`, `error` | Explicit severity with text/icon support |

The bundled 青山湖 palette anchors are cypress green primary `#397A46`, primary action `#275A34`, leaf green `#4F8D50`, text `#253C2D`, and warm mist-white background `#F7F5F0`. Copper foliage and cool mist remain local accents; lake mist `#85C7BA` can mark atmosphere without covering reading surfaces.

## Report hierarchy

1. Use one strong summary surface near the top.
2. Let findings and evidence form the main reading rhythm.
3. Keep recommendations visibly tied to the finding or decision they address.
4. Make metadata quieter but still readable.
5. Prefer natural document sections over a grid of equal cards.
6. Let evidence tables exceed the prose measure when necessary, with local horizontal scrolling on narrow screens.

## Density and geometry

Use an 8px rhythm with 4px micro gaps. For reading-oriented HTML reports:

| Element | Default |
| --- | --- |
| Body | 14–16px, line-height 1.65–1.8 |
| Supporting text | 12–13px |
| Page title | 28–40px on desktop, responsive on narrow screens |
| Section title | 18–24px |
| Control height | 32–36px; 40px only for a primary action |
| Dense radius | 6–12px |
| Narrative surface radius | 12–20px |
| Component gap | 8–16px |
| Section gap | 24–48px |
| Prose measure | roughly 68–78 characters |

Hierarchy comes from alignment, spacing, typography, opacity, and one clear emphasis—not from nesting cards.

## Material

1. Begin with an opaque, readable surface.
2. Use transparency only when background context improves orientation or identity.
3. Keep tables, logs, code, screenshots, and long descriptions more opaque than navigation or atmosphere.
4. Use one material boundary per hierarchy level, one-pixel quiet borders, and broad cool shadows.
5. Provide an opaque fallback for unsupported or reduced transparency.
6. Keep warm colors rare and local.

## Motion and atmosphere

1. Use 120–220ms for interactive transitions and up to roughly 600ms for a one-time report-header reveal.
2. Animate state or spatial continuity, not decoration for its own sake.
3. Pause ambient animation when hidden or offscreen.
4. Under Reduced Motion, remove travel, scale, parallax, and continuous movement or replace them with a short fade.
5. Keep particles and gradients outside dense reading and evidence regions.
6. Ambient mist uses a few neutral, soft-edged banks with clearly perceptible slow drift; avoid stacking so many stationary gradients that motion disappears into a gray wash. Keep the reading surface clear.

## Responsive, accessibility, and print

1. Preserve semantic HTML, landmarks, native controls, logical keyboard order, and visible focus. Use `<p>` for prose only; compact previews, metadata, labels, and tags use `<div>`/`<span>` so global paragraph margins cannot distort row geometry.
2. Target WCAG 2.2 AA: 4.5:1 for normal text and 3:1 for large text or non-text UI.
3. Move sticky navigation into document flow on narrow screens.
4. Let wide evidence tables scroll locally without hiding labels or meaning.
5. Support `prefers-reduced-motion`, `prefers-contrast`, and `forced-colors` where the host permits it.
6. In print, remove sticky behavior and atmosphere, reveal useful URLs, preserve contrast, and avoid splitting a finding from its first evidence block.

## Validation

1. Run the bundled token validator after theme or material token changes.
2. Render representative content at desktop and narrow widths.
3. Exercise long titles, long findings, empty evidence, broken-media fallback, focus, error, retry, and success states present in the report.
4. Follow internal anchors and evidence links.
5. Inspect print or PDF output for page breaks, clipped tables, contrast, and URLs.
6. Compare the same content before and after when adapting an existing report.

## Internal web surface rules

The following rules express lake-landscape's visual discipline in Joyally Design's React/web and report surfaces:

1. Establish layout zones and reading order before adding atmosphere or animation.
2. Use opaque readable surfaces for tables, logs, evidence, and long descriptions; reserve translucency for perimeter atmosphere and orientation.
3. Use compact professional density for dashboards: 8px rhythm, 12–16px component padding, 20–24px section gaps, and 32–40px controls.
4. Support wide, medium, and narrow states explicitly: keep stable sidebars on wide screens, collapse secondary panes at medium widths, and move filters or wide evidence into local scrolling containers on narrow screens.
5. Treat focus, selected, loading, empty, error, success, disabled, reduced motion, reduced transparency, increased contrast, and forced colors as component states rather than afterthoughts.
6. Reject tourism-poster scenery, blue-purple AI gradients, full neon, glass-on-glass nesting, perpetual decorative motion, and color-only state communication.

## Provenance

The token layers and component discipline follow a composed reference-system model, with each reference contributing only where it is strongest. The quiet landscape abstraction and contemporary Chinese visual cues belong to the bundled lake-landscape preset. Other products can retain the same semantic and accessibility contract while deriving their own visual language from their brand and audience.
