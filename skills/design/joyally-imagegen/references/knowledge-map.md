# Structured Knowledge Map

Use for domain knowledge graphs, architecture overviews, lifecycle maps, responsibility boundaries, dependency graphs, and other explanatory visuals where exact terminology and relationships matter.

This workflow delivers static images. Apply the entrypoint's diagram ownership rule before starting: follow an explicit Skill choice, otherwise route interactive deliverables to Joyally Design / Archify. Visual styling from Joyally Design does not change this workflow's ownership or turn an image request into an interactive page. The HTML/SVG below is a precise drawing source for image export, not an additional user-facing website.

Load first:

- `references/generation.md`
- `references/prompt-compliance.md`
- `references/post-process.md`

## Core rule

Split semantics from atmosphere:

1. Model the domain in text before drawing.
2. Use the image model only for a restrained, text-free backdrop.
3. Render every node, edge, arrow direction, label, legend, and status with deterministic HTML/CSS/SVG.
4. Verify graph meaning separately from visual polish.

Never ask the image model to render a knowledge graph directly. It may invent nodes, reverse arrows, merge lifecycle states, or corrupt Chinese labels.

## Illustration density gate

Do not treat “avoid decorative visuals” as “minimize diagrams.” For a long technical article, count semantic visualization opportunities before drawing. Create a diagram whenever the reader must understand one of these relationships:

- three or more ordered build, release, verification, or update steps;
- two or more branches, channels, runtimes, ownership boundaries, or trust paths;
- dependency propagation, containment, state transition, rollback, or fan-out/fan-in;
- a comparison whose meaning depends on position, direction, or grouping;
- a lifecycle summary spanning several modules.

Use text/code blocks only for executable commands, configuration, literal paths, short file inventories, and examples that readers should copy. Never leave an ASCII/TXT diagram in the final article. Treat `text`/ASCII diagrams as content-model drafts that must become deterministic graphics before publication.

For an article longer than about 2,000 Chinese characters, perform a full illustration-opportunity audit. There is no numeric maximum. Merge adjacent opportunities into one figure only when they answer the same reader question; do not force unrelated lifecycles into a dense poster just to reduce image count.

### Anti-crowding gate

Treat whitespace as part of the information architecture, not leftover canvas. Before styling:

#### Horizontal breathing-room gate

For left-to-right architecture diagrams, budget horizontal whitespace before assigning card widths. Passing a generic rectangle-overlap check is not enough.

- On a logical `1600x900` canvas, reserve at least `96px` on both outer sides. Inside a grouped boundary, reserve at least `64px` left/right padding between the border and the first/last semantic node; the boundary stroke is not a routing gutter.
- Keep at least `96px` between primary sibling columns. When one column contains stacked alternatives, treat the whole branch column as one block and reserve at least `120px` routing gutters on both sides so fan-out and fan-in connectors have their own air.
- At most about `62%` of the usable canvas width should be occupied by semantic cards in a five-step horizontal flow. Reserve at least `24%` for connectors, labels, and routing gutters; keep the remainder as outer and boundary breathing room. If the budget does not fit, widen the canvas, shorten copy, or move secondary detail to another figure. Do not shrink type, card padding, or arrow clearances.
- Keep edge labels in the routing gutter rather than centered over a short shaft. Require at least `24px` from the nearest card and `16px` from every connector or marker. A label that visually bridges two cards collapses the gutter and fails review.
- A large ownership/group boundary may not wrap the flow so tightly that it reads as another card. Prefer open columns or increase the boundary padding. Keep at least `40px` between branch cards vertically and at least `56px` between the branch block and the boundary header copy.
- Inspect a `900x506` preview and require the horizontal gaps to remain visibly open: primary column gutters should still read as roughly `45px` or more, and branch-side routing gutters as roughly `68px` or more. If adjacent cards read as one continuous block before their labels are read, the figure fails even when the full-resolution geometry passes.
- For a formal horizontal architecture figure with four or more semantic columns, use the spacious validator override as the minimum starting point: `--min-gap 96 --edge-clearance 24 --marker-clearance 24 --arrow-join-tolerance 2 --arrow-tangent-tolerance 8 --label-clearance 12 --connector-label-clearance 20`. Increase the canvas or restructure the graph when this preset cannot pass.

- Keep one semantic question per figure. If an overview also needs implementation detail, create an overview plus one or more detail figures.
- Prefer 3–4 parallel reader lanes with 3–4 compact nodes each. Split the figure when a column needs more than four stacked cards, a card needs more than one title plus two short fact lines, or routing requires edges to pass through content.
- Never make fonts smaller, reduce line-height, remove padding, or use fixed-height clipping to force the content onto one canvas.
- On a logical `1600x900` canvas, use at least `24px` between cards, `18px` internal card padding, `18px` body text, and dedicated `40px` or wider edge-routing gutters. For a horizontal stage/timeline figure with 3–5 large cards, raise the routing gutter to at least `80px`, keep the line body at least `20px` from card borders, keep the rendered arrow tip at least another `20px` from the target card's border and shadow, and leave at least `8px` between an edge label and the nearest card. The target clearance is measured from the arrow tip, not the shaft endpoint. Put edges above card shadows but below text and labels so markers remain visible without crossing content. Use fewer words or another figure when these budgets do not fit.
- For a three-column architecture figure, default to `72px` or more outer margins and `100–120px` routing gutters between card columns on a logical `1600x900` canvas. Keep ordinary connector shafts around `56–80px` and arrowheads around `8–10px`; arrows are secondary relationship cues, not the visual subject. If the arrows or cards dominate the page, reduce card width and copy before reducing gutters, font size, or outer margins.
- Treat every canvas edge, lane rail, divider, and card boundary as protected geometry. Keep all text, arrows, arrowheads, shadows, accents, and decorative marks visibly inside their intended region; never use clipping or `overflow: hidden` to conceal an overrun. Annotate a decorative rule with `data-layout-divider`; keep it at least `16px` away from every semantic card so it cannot read as an accidental cross-node connector. Leave at least `24px` of outer canvas safety margin on a logical `1600x900` canvas unless the layout grammar requires a larger margin.
- Treat title bands, backing plaques, legends, and every other visible text container as real boxes, not decorative haze. On a logical `1600x900` canvas, keep at least `18px` internal padding on every opaque or visibly bounded side; never use zero padding on the first-glyph side. Inspect the glyph silhouette against the visible backing edge at full size and at the `900x506` preview, because a CSS box can remain inside the canvas while its text still looks clipped or stuck to the edge.
- Wrap every card's complete copy in one `data-layout-text` group and declare its owner with `data-node-ref="node-id"`. Run the rendered validator with `--text-node-clearance 18`; unannotated loose `<text>` elements inside cards are not acceptable because the gate cannot prove their glyphs remain inside the card. If a heading needs more room, widen the card or shorten the copy instead of letting the last glyph share the border or routing gutter.
- Keep a grouped-container border visually separate from the figure title band. Annotate the subtitle or other copy above the border with `data-boundary-ref` / `data-boundary-side="above"`, annotate the top border with `data-layout-boundary`, and require at least `24px` rendered clearance. A container border must not read as an underline, strike-through, or protruding rule from the title area.
- A routing gutter must explain itself. When an owner/lane card precedes a first process card, show the source-to-first-node connector across that gutter; an unexplained blank strip that makes the sequence look disconnected fails the layout review even when no rectangles overlap.
- Give each node exactly one job. Replace paragraphs with a canonical noun/title and one outcome or constraint line; move explanation back into the article.
- Reject a layout when cards technically do not overlap but still look compressed at the `900x506` preview. Four clean rows are better than six crowded stacks.

### Layered diagrams: spacing, arrow shafts, and copy containment

For vertically stacked responsibility/layer diagrams, start with **80–112px inter-card gutters**, **24px copy padding**, and a side rail wide enough for the longest rendered label plus padding on both sides. These values are logical canvas units, not export-scale pixels. Increase canvas height before shrinking labels or squeezing gutters. At the actual article width, retain at least about 24px of visible connector shaft; a triangle alone is not a readable connector.

Use the formal preset with `--min-gap 80 --text-node-clearance 24 --min-edge-length 56 --max-marker-size 12`. Reserve source/target clearance in addition to the shaft and arrowhead when calculating the gutter. Route feedback connectors in their own gutter with a full final segment; they must not run along a card border or through any unrelated card or text.

This applies equally to edits of an existing SVG. Annotate **every** node, connector, arrowhead, and visible text group, including side rails and implementation notes. A static rectangle-only pass, or a report with zero checked edges/copy groups, does not establish that the diagram fits. Run the rendered strict gate after fonts load; then inspect the full export and a preview scaled to the actual article width. If text overflows, widen or wrap the label; never hide it with clipping or reduce the semantic font merely to pass.

### Article asset-completeness gate

Maintain a figure manifest while producing a technical article:

```text
Figure ID | reader question | local asset | article placement | uploaded URL | HTTP/content-type | live-rendered
```

Before handoff:

1. Reconcile planned, generated, inserted, and uploaded figure counts. No generated figure may remain unplaced without an explicit reason.
2. When the publication surface requires remote assets, require zero unresolved local image references and one immutable remote URL per inserted figure.
3. Fetch every remote URL and verify a successful status plus the expected image content type. Asset upload is not article publication.
4. Verify the rendered article separately. Do not infer page visibility from a local Markdown rewrite or a successful CDN response.
5. Report local, inserted, uploaded, published, and live-rendered states separately.

## 1. Build the content model

Write a compact graph specification before layout:

```text
Purpose: what the reader should understand or decide
Reader: expected domain knowledge
Entities: canonical nouns only
Relations: source -> target | verb phrase
States: lifecycle states that must remain distinct
Boundaries: ownership, process, trust, or deployment boundaries
Legend: what color, shape, line style, and arrow style mean
Evidence: source files or facts behind load-bearing labels
```

Apply these constraints:

- Keep one canvas to roughly 8–18 primary nodes. Split the graphic when more nodes are required.
- Give every edge a verb or short relationship label; an unlabeled line is ambiguous.
- Use one dominant reading direction: left-to-right for pipelines, top-to-bottom for hierarchy.
- Keep secondary relationships visually quieter than the primary flow.
- Show state distinctions explicitly. For example, `built`, `signed`, `uploaded`, `deployed`, and `live-verified` must not collapse into one "released" node.
- Distinguish artifact containment (`contains`), transformation (`builds`), trust (`verifies`), and delivery (`updates`) with different line styles or colors.

## 2. Choose a layout grammar

Pick the smallest grammar that explains the domain:

| Relationship | Layout |
|---|---|
| Ordered lifecycle or build pipeline | Horizontal stages with directional arrows |
| Components owned by different runtimes or teams | Vertical swimlanes or bounded columns |
| One source affecting many consumers | Hub-and-spoke |
| Containment and nested ownership | Grouped containers with solid borders |
| Trust or control plane over a delivery flow | Main pipeline plus a narrow trust rail |
| Several exact mappings | Matrix or table instead of a graph |
| Historical evolution expressed as a river | Literal main river with tributaries, confluences, bends, and bank milestones |

Prefer a 16:9 logical canvas at `1600x900`, rendered at 2x DPR to `3200x1800`. Reserve about 10% for title/summary, 78% for the graph, and 12% for legend or lifecycle caveats.

For a genuinely edgeless matrix, comparison, or status board, declare the root as `data-layout-kind="matrix|comparison|status-board"`. The validator then requires semantic nodes and owned text but does not invent a `data-layout-edge` requirement. Do not use this escape hatch for a lifecycle, dependency, transition, or delivery figure whose meaning actually depends on direction.

### Historical-river grammar

When the request says `历史长河`, `演进长河`, `发展长河`, or `evolution river`, the metaphor is a semantic requirement:

- Make one continuous, visibly wider main river the chronological spine. It must dominate the composition at full size and at the `900x506` preview.
- Show each major branch as a narrower tributary with an organic river path. Tributaries may begin at different times, split, run independently, and merge at explicit confluences that match the history.
- Draw confluences as natural water geometry: a tributary approaches at an acute downstream angle, widens slightly at the mouth, and terminates inside the receiving channel. The receiving river remains visually continuous through the merge.
- Never draw a tributary as a constant-width translucent tube laid over the main stream. Reject perpendicular crossings, double shorelines across an open river mouth, branch strokes continuing past the receiving channel, and opacity overlaps that read as stacked pipes.
- Express time through the river's flow direction and label the source/present ends. For a maintained timeline whose newest state must appear first in the article, place the present at the top or upper-right while preserving an unmistakable upstream-to-downstream reading cue.
- Place dates and milestones as bank inscriptions, stones, docks, settlements, bends, or confluence markers. Small backing plaques are allowed for legibility, but repeated equal-sized cards must not become the primary silhouette.
- Keep tributary names next to their own watercourse. Do not turn branches into swimlanes, boxed columns, or parallel card rows.
- Use deterministic SVG/HTML for river paths, confluence geometry, dates, names, and direction cues. The generated backdrop supplies landscape atmosphere only and must not invent semantic waterways.
- If the figure first reads as an architecture diagram, roadmap, or row of cards rather than a river system, reject it even when every label is correct.

Historical-river QA adds four release gates: the main stream is visually wider than every tributary; every tributary visibly connects to or branches from the correct stream; every confluence opens into the receiving channel without a crossing stroke or shoreline barrier; and the river topology remains understandable before reading any label.

## 3. Generate a backdrop

Use `1280x720`. Unless the user named another style, resolve Light or Dark through `qingshan-lake-style.md`; default to Light for technical documents and ATA. Keep the center low-detail so lines and small labels remain readable.

Light default:

```text
Wide abstract technical-systems backdrop in Qingshan Lake light visual language. Warm mist-white canvas, subtle pale lake haze, restrained lake-teal and cypress-green topology only around the outer edges, distant gray-blue hill layering, rare soft dawn-gold accent. Center and all content lanes stay clean, calm, low-contrast, and empty for a precise diagram overlay. no text, no letters, no numbers, no watermark, no logos, no icons, no cards, no arrows, no flowchart, no central subject.
```

Dark alternative:

```text
Wide abstract technical-systems backdrop in Qingshan Lake dark visual language. Deep-lake ink canvas instead of pure black, layered dark-water and cypress tones, restrained lake-teal mist and gray-blue contours only around the outer edges, rare dawn-gold edge light. Center and all content lanes stay clean, calm, low-contrast, and empty for a precise diagram overlay. no neon cyberpunk, no text, no letters, no numbers, no watermark, no logos, no icons, no cards, no arrows, no flowchart, no central subject.
```

```bash
PROMPT="Wide abstract technical-systems backdrop in Qingshan Lake light visual language. Warm mist-white canvas, subtle pale lake haze, restrained lake-teal and cypress-green topology only around the outer edges, distant gray-blue hill layering, rare soft dawn-gold accent. Center and all content lanes stay clean, calm, low-contrast, and empty for a precise diagram overlay. no text, no letters, no numbers, no watermark, no logos, no icons, no cards, no arrows, no flowchart, no central subject, no humanoid figure. Wide 16:9."
OUTPUT_PATH="/tmp/knowledge_map_bg.png"
if   GEN_LOG=$(gen_image_apiyi "$MODEL_GPT"    "1280x720" "$OUTPUT_PATH"); then MODEL_USED="$MODEL_GPT";    SIZE="1280x720"
else echo "KNOWLEDGE_MAP_BACKDROP_GENERATION_FAILED"; exit 1
fi
GENERATION_MS=$(printf '%s\n' "$GEN_LOG" | awk -F: '/^ELAPSED_MS:/{v=$2} END{print v+0}')
RESPONSE_FORMAT=$(printf '%s\n' "$GEN_LOG" | awk -F: '/^RESPONSE_FORMAT:/{v=$2} END{print v}')
```

Preview the backdrop before compositing. Reject it if the center contains pseudo-text, diagram-like shapes, bright focal objects, or high-frequency texture.

## 4. Render deterministic semantics

Use HTML/CSS for containers and typography, plus inline SVG for edges and arrowheads.

- Use `PingFang SC`, `Inter`, `-apple-system`, `sans-serif` for Chinese technical diagrams.
- Give each semantic category one accent color. Do not use color as the only distinction; pair it with a heading, shape, or line style.
- Put SVG edges behind cards and labels. Use explicit `viewBox="0 0 1600 900"` coordinates.
- Model arrows as semantic source-to-target relations. Put the source in `data-from`, the target in `data-to`, declare `data-flow="down|up|left|right"`, and place exactly one arrowhead at `marker-end`. Never choose arrow direction from visual symmetry or layer order alone.
- Start and end every connector in the dedicated gutter outside the source and target boxes. Align vertical connectors within both cards' horizontal projection, and horizontal connectors within both cards' vertical projection; do not run a connector through a card center merely to make the columns look continuous.
- Treat the shaft endpoint and arrow tip as different coordinates. For an explicit right-pointing triangle whose base is at `x=460` and tip is at `x=470`, end the shaft at `x=460`, not `x=470`. Apply the equivalent rule for left/up/down arrows, keep the shaft centerline aligned with the arrowhead center, and let the arrowhead inherit the connector's computed stroke color.
- Align the arrowhead with the connector's actual terminal tangent. For a curved connector, prefer an SVG marker with `orient="auto"`; set the marker reference point on the arrow base (`refX` at the base, not the tip) and center `refY` on the shaft. If an explicit arrowhead is used, rotate it to the same tangent or choose the final control point so the curve enters a short terminal segment tangent-continuously. Do not attach a vertical triangle to a diagonal curve or hide a sharp curve-to-shaft kink behind a few axis-aligned pixels; explicit arrows allow at most `8°` of deviation at `1600x900`.
- Use solid arrows for transformation or delivery, dashed arrows for optional paths, and dotted lines for trust/verification.
- Use short edge labels on dark translucent pills so labels do not disappear into the backdrop.
- Keep node text to a title, one role line, and at most three compact facts.
- Avoid emoji for formal knowledge maps; use simple CSS or SVG glyphs when an icon materially aids scanning.

Composite through the same CDP validator used by the geometry gate. This avoids stale screenshots and guarantees that the captured pixels are the layout that passed validation:

```bash
node "$SKILL_DIR/scripts/validate_diagram_layout.mjs" /absolute/path/knowledge-map.html \
  --width 1600 --height 900 --scale 2 \
  --screenshot /tmp/knowledge_map_final.png
```

Do not reuse an existing screenshot path as evidence unless this command exits zero and rewrites it in the current run.

If headless Chrome cannot start reliably, or the figure does not need HTML-only layout features, use a pure SVG semantic layer instead. Keep every card as an axis-aligned `rect`, every primary connector as a straight `M/L/H/V` path, and draw the arrowhead as an explicit target-end path annotated with `data-arrow-for`; do not rely on SVG `marker-end` because native macOS rasterizers may omit markers. Validate before rasterization:

```bash
"$BETTER_IMAGEGEN_PYTHON" "$SKILL_DIR/scripts/validate_svg_layout.py" /absolute/path/diagram.svg \
  --min-gap 48 --edge-clearance 12 --arrow-clearance 12 --arrow-join-tolerance 2 --arrow-tangent-tolerance 8 --arrow-shaft-tolerance 0.25 --label-clearance 8 --divider-node-clearance 16
sips -s format png /absolute/path/diagram.svg --out /tmp/knowledge_map_final.png
```

Prefer Chrome for Testing from an installed Playwright cache over the user's interactive Chrome. On macOS, remove an inherited `MallocNanoZone` from the renderer environment. Always use a unique profile and terminate the headless renderer after validation or export; orphaned renderers are a failed gate.

## 5. Verification gates

Check in this order:

1. **Semantic coverage:** every required entity and relationship appears once with the canonical name.
2. **Directionality:** every arrow points from the real source to the real target.
3. **Boundary integrity:** build, signing, upload, deployment, update, and live verification are not visually merged.
4. **Typography:** exact Chinese/English text, no clipping, no overlap, no font fallback boxes.
5. **Legibility:** titles readable at 25% preview; node facts readable at 50% preview.
6. **Visual hierarchy:** the intended primary flow is visible before secondary rails and notes.
7. **Edge quality:** no arrow crosses a node; minimize crossings and label collisions.

### Diagram layout gate

Treat connector placement as a release-blocking visual gate for ATA diagrams:

- Route progression connectors through a dedicated lane above the card content. For staircase layouts, keep each arrowhead above the downstream card; do not center connectors between card bodies.
- Keep the complete shaft and rendered marker outside every node, text, label, shadow, title, and footer bounding box. Require at least 16 px visual clearance from the downstream card and at least 16 px between every label and the nearest connector shaft or rendered marker. Do not route a connector behind a label and count the hidden segment as clearance.
- Do not add decorative card-edge bars. Full-height vertical strips beside owner/lane cards, short horizontal rules above card titles, and pseudo-tabs attached to card borders are forbidden even when they fit numerically: they carry no relationship or state, compete with copy, and often read as clipped or broken geometry at preview size.
- Express hierarchy or state with the card surface, border tint, typography, a labeled badge, or a compact semantic icon. A non-bar accent is allowed only when it carries explicit meaning; annotate it with `data-layout-accent="<unique-id>"` and `data-for-node="<owner-node-id>"`, keep at least `12px` from the card border and `8px` from owned copy, and explain its meaning in the legend or label.
- Treat rails, dividers, lane separators, trust boundaries, and ownership boundaries as protected geometry. No title, description, badge, or footer may touch or cross one. Annotate the boundary and the nearby copy, then require at least 16 px rendered clearance on the declared side. Wrapping a long label onto two lines is preferable to moving the divider or shrinking the font.
- Place the arrowhead at the downstream end and verify its direction, full silhouette, and endpoint clearance after rasterization; checking the SVG path alone is insufficient.
- For explicit arrowheads, the connector shaft must terminate at the arrowhead base with no visible gap, remain centered on the arrowhead, and never continue through the triangle toward its tip. Use a maximum `2px` join tolerance at `1600x900`, and require the arrowhead fill to match the connector stroke. A shaft ending at the triangle tip, a floating arrowhead, a vertically shifted join, or a mismatched arrow color is release-blocking.
- The final shaft tangent must point along the arrowhead axis. Reject a curved path whose last segment approaches the arrow base diagonally while the arrowhead points vertically or horizontally; require at most `8°` tangent deviation.
- Prefer `stroke-linecap: butt` for explicit-arrow and marker-ended connectors. If `round` or `square` caps are required, account for the half-stroke cap extension when placing the arrowhead base or marker reference point. A line visible past the arrowhead tip, even by a few raster pixels, is release-blocking.
- Render both the lossless PNG and delivery WebP, inspect both at the final aspect ratio, and fail the gate if any connector crosses a content region, appears detached from the intended sequence, or becomes ambiguous against the background.
- Inspect the raster boundary itself: reject text, shadows, arrowheads, accents, or decorative forms that touch or appear cut by the outer canvas, a lane rail, a divider, or another card. A clipped element hidden by the SVG/HTML viewport is still a failure.
- Record the connector routing rule and measured clearances in the generation metadata. Do not publish or replace the ATA CDN asset until this gate passes.

Inspect both the full-resolution result and a `900x506` preview. A visually attractive graph with one incorrect edge fails.

Run a final crowding review in addition to correctness: scan every card at full size for text touching borders, adjacent cards for less than one visual gutter, labels for edge collisions, and the preview for any region that reads as a solid block of text. If the reviewer must zoom in or trace around another card to follow the primary path, split or simplify the figure.

Also inspect the complete raster for accidental tiling or repeated quadrants after screenshot and resize. A renderer can produce a correctly sized file whose page is repeated several times; geometry checks may still pass because they inspect only one DOM. Reject any repeated title, card grid, background quadrant, or clipped page tile before encoding or publication.

### Mandatory geometric layout gate

Mark every semantic card, edge, and edge label in the deterministic HTML:

```html
<article data-layout-node="server">...</article>
<div data-layout-text="server-copy" data-node-ref="server">...</div>
<path data-layout-edge="extension-to-server" data-from="extension" data-to="server" data-flow="down" marker-end="url(#arrow)" ... />
<g data-layout-label="extension-to-server-label" data-edge-ref="extension-to-server">...</g>
<aside data-layout-text="layer-rail" data-boundary-ref="layer-divider" data-boundary-side="left">...</aside>
<span data-layout-boundary="layer-divider">...</span>
<span data-layout-divider="footer-divider">...</span>
<h1 data-layout-text="figure-title" data-layout-role="title">...</h1>
```

The strict contract is complete only when:

- every node, edge, label, text group, boundary, divider, accent, and explicit arrow has a non-empty unique semantic ID within its kind;
- every node owns one annotated copy group through `data-node-ref`;
- every edge declares `data-from`, `data-to`, and `data-flow`, and both endpoints resolve to nodes;
- every edge label declares `data-edge-ref`, every accent declares `data-for-node`, and every explicit arrow declares `data-arrow-for`;
- standalone copy uses `data-layout-role="title|subtitle|legend|note|footer"`; loose visible text outside `data-layout-text` or `data-layout-label` is forbidden;
- semantic elements have non-zero rendered bounds and remain inside the configured canvas safe area.

For the pure SVG fallback, use the same `data-layout-node`, `data-layout-edge`, `data-from`, `data-to`, `data-flow`, and `data-layout-label` attributes, plus one explicit arrowhead path carrying `data-arrow-for="edge-id"`. Put the copy near a divider in its own `<g data-layout-text="..." data-boundary-ref="..." data-boundary-side="left|right|above|below">`; do not put the boundary line inside that text group. Mark the line itself with `data-layout-boundary="..."`.

Before screenshot export or upload, run the formal architecture preset. Additional arguments override preset values when a figure has a documented exception:

```bash
node "$SKILL_DIR/scripts/validate_architecture_diagram.mjs" /absolute/path/diagram.html \
  --width 1600 --height 900 --scale 2 \
  --screenshot /absolute/path/diagram.png
```

The preset enables strict semantic annotations and the formal-book baseline: `48px` node gap, `18px` node-copy padding, `24px` boundary and canvas clearance, `16px` divider-to-node clearance, `16px` minimum semantic font size, `8px` label gap, `12px` edge/marker clearance, `2px` explicit-arrow join tolerance, `8°` terminal-tangent tolerance, `16px` connector-to-label clearance, `12px` accent inset, `8px` accent-to-owned-copy clearance, `48px` minimum edge length, `16px` maximum marker size, and zero edge crossings between unrelated relations.

For a horizontal stage/timeline figure with 3–5 large cards, use the stricter spaciousness gate:

```bash
node "$SKILL_DIR/scripts/validate_architecture_diagram.mjs" /absolute/path/diagram.html \
  --width 1600 --height 900 --min-gap 80 --edge-clearance 20 --marker-clearance 20 --arrow-join-tolerance 2 --arrow-tangent-tolerance 8 --label-clearance 8 \
  --connector-label-clearance 16 --accent-border-clearance 12 --accent-text-clearance 8 --divider-node-clearance 16 \
  --min-edge-length 56 --max-marker-size 16 --marker-shaft-tolerance 0.25 \
  --scale 2 --screenshot /absolute/path/diagram.png
```

Do not export or publish unless it exits zero. The gate launches headless Chrome, reads actual `getBoundingClientRect()` geometry after fonts load, and rejects:

- overlapping cards or cards closer than the required gutter;
- duplicate or empty semantic IDs, missing references, orphan labels/arrows/accents, edges without declared direction, nodes without annotated copy, and visible loose text outside the semantic contract;
- labels intersecting any card;
- labels touching or crowding one another;
- sampled SVG edge paths crossing a card other than their declared endpoints;
- annotated edges whose rendered start/end order contradicts `data-flow`, whose endpoint is not aligned with the declared source/target boundary, or whose arrowhead is not exclusively on the target end;
- when requested, edge paths approaching their endpoint cards more closely than the required clearance;
- when requested, a rendered arrow marker, including stroke allowance, approaching its source or target card more closely than the required visual clearance;
- when requested, edge labels approaching any card more closely than the required clearance;
- when requested, any connector shaft or rendered marker approaching a label more closely than the required clearance;
- annotated card accents approaching, covering, or protruding through their owning card border;
- annotated accents shaped like horizontal or vertical bars (aspect ratio `>= 4:1`);
- annotated card accents touching or crowding the text group owned by the same card;
- annotated decorative dividers touching or crossing a semantic card (`divider-node-clearance`);
- annotated semantic text approaching or crossing its referenced rail/divider/boundary on the declared side;
- annotated card copy approaching, touching, or crossing any side of its declared owning node;
- semantic copy below the minimum font size, zero-size semantic elements, or meaningful elements entering the outer canvas safety margin;
- crossings between unrelated edges beyond the explicitly permitted count;
- horizontal stage arrows shorter than the required visible routing span, or arrow markers large enough to visually consume the shaft;
- marker-ended or explicit-arrow connectors whose stroke cap extends past the rendered arrowhead tip (`marker-shaft-overrun`);
- explicit arrowheads whose shaft stops before the arrow base, overlaps through the arrow body, misses the arrowhead centerline, approaches on a tangent inconsistent with the arrow direction, or uses a different color (`arrow-shaft-gap`, `arrow-shaft-overlap`, `arrow-shaft-misaligned`, `arrow-tangent-misaligned`, `arrow-color-mismatch`);
- clipped or overflowing text, labels, and cards;
- clipped or overflowing headers, layer rails, footers, or other semantic copy annotated with `data-layout-text`;
- elements outside the logical canvas.

Treat the numeric gate as necessary but not sufficient. After it passes, still inspect the full image and `900x506` preview for visual crowding, ambiguous grouping, excessive empty zones, or a technically non-overlapping layout that still feels cramped. Prefer open columns and dedicated routing gutters over boxed swimlanes when lane borders add visual collisions.

For every owner/lane-to-flow transition, include the source-to-first-node connector in the annotated graph model. In the final raster, verify that it crosses the reserved routing gutter with a full shaft and target-end arrowhead; the gutter must not read as an accidental blank column.

For a pure SVG fallback, run both gates: the static path/card gate and the rendered-DOM gate. The latter is mandatory whenever copy sits near a divider because XML geometry alone does not know the final font metrics:

```bash
"$BETTER_IMAGEGEN_PYTHON" "$SKILL_DIR/scripts/validate_svg_layout.py" /absolute/path/diagram.svg \
  --min-gap 48 --edge-clearance 12 --arrow-clearance 12 --arrow-join-tolerance 2 --arrow-tangent-tolerance 8 --arrow-shaft-tolerance 0.25 --label-clearance 8 --divider-node-clearance 16
node "$SKILL_DIR/scripts/validate_architecture_diagram.mjs" /absolute/path/diagram.svg \
  --width 1600 --height 900 --scale 2 --screenshot /absolute/path/diagram.png
```

### Raster and editorial release gate

Automation cannot reliably judge all publication defects. After the strict gate passes, record and inspect both the lossless full-resolution raster and the intended-size preview:

- exact text and terminology, correct Chinese glyphs, no tofu/fallback boxes, consistent weights, and no synthetic bold distortion;
- readable hierarchy at `900x506`: title first, primary flow second, secondary implementation notes third;
- contrast against the final composited background, including translucent cards and delivery WebP compression;
- balanced density, deliberate whitespace, clear grouping, and no border that visually becomes an underline or protruding rule;
- no accidental tiling, stale screenshot reuse, missing arrowheads, raster seams, clipped shadows, or export-size/aspect-ratio drift;
- figure caption, source/rights ledger, local asset, inserted document, uploaded asset, and live-rendered state tracked separately when the publication workflow needs them.

Record the preset name, numeric overrides, validator counts, zero-error result, full-resolution review, intended-size review, output dimensions, and file hash or metadata path. A validator pass without both raster reviews is not a release pass.

## 6. Deliver

Keep PNG for presentations and WebP q90 for documentation:

```bash
DEST="${DEST:-$HOME/Pictures/better-imagegen/knowledge-map}"
mkdir -p "$DEST"
to_webp /tmp/knowledge_map_final.png "$DEST/knowledge-map.webp" 90
cp /tmp/knowledge_map_final.png "$DEST/knowledge-map.png"
POSTPROCESS_NOTE="deterministic HTML/CSS/SVG knowledge graph over $MODEL_USED text-free backdrop, Chrome 2x screenshot, WebP q90"
write_image_metadata "$DEST/knowledge-map.webp" "$DEST/knowledge-map.json" "$MODEL_USED" "$SIZE" "$GENERATION_MS" "$RESPONSE_FORMAT" "$POSTPROCESS_NOTE"
write_image_metadata "$DEST/knowledge-map.png" "$DEST/knowledge-map-print.json" "$MODEL_USED" "$SIZE" "$GENERATION_MS" "$RESPONSE_FORMAT" "$POSTPROCESS_NOTE"
print_image_summary "$DEST/knowledge-map.json" "$DEST/knowledge-map-print.json"
```

For repository documentation, copy the final files and metadata into the repository only after visual and semantic QA. Keep temporary HTML/backdrop files out of the repository unless the user explicitly wants editable design sources.
