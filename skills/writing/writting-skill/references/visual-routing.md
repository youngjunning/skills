# Visual routing for articles and books

Choose by the information the reader must recover, then choose the output format. The deciding question is whether an incorrect label, relationship, arrow, or state would change the explanation. Interactivity and file extension are secondary: an exported WebP architecture diagram still needs deterministic semantic authoring.

## Selection

| Reader need | Default owner | What stays deterministic |
| --- | --- | --- |
| Components, ownership boundaries, deployment topology, dependencies | Archify `architecture` | Nodes, containment, edges, labels, evidence |
| Ordered steps, branches, parallel work, recovery paths | Archify `workflow` | Ordering, conditions, joins, failure routes |
| API calls, participants, asynchronous messages, returns | Archify `sequence` | Participants, message order, direction, sync/async meaning |
| Data pipelines, lineage, transformations | Archify `dataflow` | Sources, sinks, transformations, data movement |
| States, events, lifecycle transitions | Archify `lifecycle` | State distinctions, transition conditions, terminal states |
| Scene-led or identity-led cover, editorial illustration, atmosphere, portrait, texture | better-imagegen | Exact titles, figures, identifiers, or captions added outside the raster model when needed |
| Comic article with recurring characters, scene actions, and dialogue | better-imagegen, with [comic-articles.md](comic-articles.md) owning the article/storyboard | Dialogue, commands, facts, reading order, and any explanatory relationships |
| Statistical charts, scientific plots, numeric comparisons | Standard plotting tools | Data, scales, axes, units, uncertainty, legends |
| Lookup, specifications, small comparisons | Markdown or document table | Values and column meanings; an image is often unnecessary |
| Current product behavior or an observed failure | Real screenshot or recording | Provenance and any annotations; identify a mockup as illustrative |

Read the selected skill before producing the asset. Discover the actual available Archify entrypoint, including a project-owned Joyally Design integration when required by that project. Do not hardcode a repository path into this reusable skill. Tool mechanics, schemas, validation commands, styling, and upload procedures remain owned by their respective skills and destination repository.

## Archify boundary

Use Archify when the figure's contribution is an exact relationship covered by one of its five diagram types. Model the entities and relations from evidence first; render and validate them with the selected schema. Keep the editable specification beside the delivered asset when the destination calls for maintainable source.

For an article, use a readable static export inline and provide the interactive HTML as an optional companion when useful. An HTML-only delivery is insufficient for a renderer that strips iframes. Validate the exported figure as well as the interactive artifact; inspect text and arrows at the article's actual reading width. Preserve required relationship labels instead of deleting them to make a layout pass.

A domain taxonomy, annotated illustration, geographic map, or unusual knowledge layout may not fit Archify. Use a deterministic SVG/HTML or specialist renderer when its grammar expresses the subject more accurately. Do not force every labeled visual into a component diagram. A simple relationship may be clearer as one sentence or a table.

## better-imagegen boundary

Use better-imagegen when the contribution is appearance, scene, identity, mood, or a raster asset. Follow the cover brief and acceptance requirements in `article-cover.md` for article covers. Keep covers distinct from explanatory figures.

Its `knowledge-map` workflow also uses deterministic HTML/CSS/SVG for semantics; the image model supplies only an optional text-free backdrop. The presence of that workflow is not a reason to route every architecture request through image generation. Prefer Archify for a supported node-and-edge diagram; use the custom deterministic path when the needed layout is unsupported or the user explicitly selects it.

For a mixed figure, generate only the visual layer that benefits from generation. Render exact labels, numbers, arrows, UI annotations, and state distinctions separately, then check the composite. Skip the generated background when it adds no explanatory value. Existing vector diagrams should normally be edited in their source format.

## Mixed examples

| Request | Route and acceptance |
| --- | --- |
| “写 AnyUse 架构文章，配封面和架构图” | better-imagegen creates a cover; Archify creates the component/ownership diagram; verify them independently |
| “把白板草图整理成框架图” | Recover the intended topology, mark ambiguous handwriting, then use Archify when its grammar fits; do not rasterize the handwriting as evidence of a confirmed design |
| “做一张静态 PNG 的请求时序图” | Archify `sequence`, then static export; PNG does not change the semantic owner |
| “知识体系画成河流或山脉，术语必须准确” | Custom deterministic semantic labels over optional better-imagegen scenery; use real coordinates and a legend only if they carry meaning |
| “对比三种执行器的成功率和 P95” | Verified measurements in a table or plotting tool; neither a generated chart nor an architecture diagram supplies evidence |
| “保持这张插画的人物，换背景” | Image-edit workflow with the identity reference; preserve identity rather than rebuilding it as diagram nodes |
| “只改现有 SVG 的一个节点名称” | Edit the existing vector source and revalidate references/layout; image generation is unnecessary |

## Handoff check

1. Each figure answers one named reader question and is placed near the claim it explains. Add another figure when it reduces a real reading burden, without a fixed count or a diagram quota.
2. Compare node names, relationships, ordering, states, numbers, and uncertainty with the source independently of visual polish. A generated backdrop cannot establish a system fact.
3. Inspect the final composite or static export at reading size for legibility, clipping, crossings, and missing fonts. A valid source specification is not proof of a readable export.
4. Keep editable source, exported asset, uploaded asset, article rendering, and publication status separate. Use the destination's existing upload and readback contract only when authorized.
5. If a preferred tool is unavailable, preserve the semantic contract with an available deterministic renderer or keep the affected figure explicitly unfinished. Never silently substitute a plausible raster picture for a verified diagram.

## Basis and maintenance

Routing reviewed on 2026-10-27 against the available Archify 2.17 skill (`architecture`, `workflow`, `sequence`, `dataflow`, `lifecycle`), better-imagegen's `portrait`, `text-poster`, and `knowledge-map` references, and this skill's cover contract. This is a writing-layer selection rule, not a fork of those tool manuals; consult their current instructions for generation and validation.
