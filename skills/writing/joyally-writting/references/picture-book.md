# Picture books — Book mode

`joyally-writting` owns story, page planning, exact copy, typography, print-template adaptation, review and final delivery. Designate `joyally-image` as the raster illustration provider, following its generation and editing instructions. It returns artwork and metadata; this writing workflow determines the story, count and edition contract.

Explicitly separate total images from interior pages. 20 images including front and back covers means 1 front cover + 18 interiors + 1 back cover. When counts change, remove or merge redundant beats while preserving required learning outcomes, renumber visible folios and filenames, and rebuild the package. Reuse approved art for ordering and text-only changes.

For short private family picture books, use page-level planning and reader-level factual review. Engineering-code and public-release gates apply only when the edition requires them; an AI topic alone does not make a preschool picture book a technical textbook.

## Illustration handoff and templates

Pass approved copy, scene/action, camera, visible evidence, references with roles, quiet text surface and protected objects to `joyally-image`. Review returned illustrations and request bounded repairs there; exact lettering and package acceptance stay here.

Record cover and interior geometry independently: upload canvas, trim, bleed, safe area and binding groove can differ. Match template ratios without stretching subjects. Screenshot measurements are estimates, not certified millimetres. Extend expendable scenery to the boundary while keeping text, faces, hands and story evidence within safety and binding clearances. Review objects as well as text bounds. Distinguish source pixels from export DPI; local guides do not prove printer acceptance. Label cover placement according to the actual template, and exclude guides from print-image packages.

Use for complete illustrated stories, recurring-character sequences, and page repairs. A cover, manuscript, contact sheet, or partial batch does not fulfill a complete book request.

## Establish the edition

Inspect available manuscript and artwork. Record audience, story/learning goal, exact page count including cover and recap, single-page versus spread dimensions, language, lettering preference, and deliverable format. Apply the latest user correction across planning, prompts, rendering, and packaging. A request for 20 separate images means 20 finished page files, not a 20-panel collage. Use the available writing skill for prose.

Separate rewrite invariants (cast, appearance, medium, palette) from changes (plot, dialogue, sequence). Classify references as identity, style, prop, or edit target. Missing required references block dependent illustration, not independent manuscript work. Do not invent replacement characters and claim continuity.

## Plan pages with observable differences

Maintain one authoritative page manifest. Each page records exact copy, narrative purpose, scene/action, focal subject, shot size, camera angle, composition, emotional beat, visible evidence, references with roles, and output paths. Include a text region in normalized coordinates and the natural surface behind it, such as sky, wall, floor, or blanket. The renderer reads this same copy; avoid alternate hardcoded text hidden in export scripts.

Give the protagonist a question or wish, an attempt, a change, and a response. Map each required educational outcome to visible evidence and the recap. Keep one main idea per page; deliberate read-aloud repetition is compatible with changing action and images.

Before generation, compare adjacent pages and the full sequence. Review three consecutive pages sharing the same shot size, angle, and composition. Change focal subject, action, distance, or viewpoint when the sequence stalls. Record the narrative reason for intentional repetition; a different sentence over the same family-at-table scene is not a new illustration. Scene variation need not mean changing rooms or inventing plot events.

Useful transitions include a room-establishing wide shot, an over-shoulder experiment, an overhead comparison, a detail revealing the mistake, and a reaction close-up. Choose them for the story, not a fixed camera quota. Object-only pages need not include the whole cast.

For AI introductions, distinguish human creation, learning from examples, prediction on an unseen example, error, and human checking. Labelled pictures illustrate one training method, not all AI. A device may contain AI; it is not synonymous with AI. A screen face is an interface, not a creature. Ear shape alone does not determine an animal. Conversational correction need not retrain a deployed model. Avoid promises of magic, consciousness, or automatic truth.

## Preserve identity without copying composition

Create a compact reference set from inspected material: individual character appearance, clothing, recurring prop design, palette and medium. A neutral character sheet or isolated identity view usually constrains composition less than a finished family cover. Keep private photos in the local book project, not the public skill repository.

Attach only references relevant to that page. Specify which attributes each controls. Use the authoritative identity reference repeatedly rather than chaining every new page into the next. A prop reveal may also reference the approved earlier prop image. Whole-page references must permit new poses and camera; if the model clones their arrangement, switch to individual identity/prop references and regenerate the affected page.

Compose prompts in this order:

1. Page-specific action and visible evidence, focal object, and interaction.
2. Camera distance, angle, subject scale/placement, and natural space for text.
3. Applicable character and prop invariants; hands and occlusion when necessary.
4. Shared medium/palette, reference roles, and scene-specific exclusions.

Keep the scene prominent. A long repeated family description can dominate a short scene instruction. Do not add all relatives to every prompt merely because their photos are available.

## Validate pilot pages before the batch

Generate and typeset two or three representative pages before the remaining batch: different cameras, the longest text, and a detail or difficult interaction. An existing accepted page can count. Inspect these finished pages together for identity, composition diversity, visible evidence, and lettering.

This is an agent QA step, not an automatic request for user approval. Continue under existing authorization once it passes. If the pilot repeats a composition or lacks text space, repair references/prompt/layout before multiplying the defect across the book.

Use `joyally-image`'s timeout, response-safety, cascade, and metadata rules. API success means an image exists, not that it satisfies the page. Record semantic failures separately from transport failures. Retry rejected pages with the observed defect named, retaining accepted pages. After two targeted repairs still fail, pause the affected batch and revise the reference/layout strategy; do not substitute an old page or mark the failed one accepted.

## Put lettering on the illustrated scene

Default to full-page art with exact Chinese copy typeset onto natural quiet surfaces inside the picture. Deterministic text rendering is compatible with integrated illustration. A sidebar, solid caption strip, separate card, or reduced image beside text is used only when requested or established by the accepted layout.

Generate text-free scene art, then render editable copy with an installed suitable font. An explicit request for model-rendered lettering overrides this default, but every glyph still needs inspection. The cover title needs its own hierarchy and placement; do not treat it as ordinary body copy.

Text regions vary with composition. Avoid reserving the same empty third of every page. Inspect returned art: requested quiet space does not prove it exists. Keep copy clear of faces, hands, key objects, and evidence such as plush seams. Record protected rectangles after inspection, and measure actual rendered glyph bounds including outline/shadow.

When copy does not fit, reflow within clear space, move it to another natural surface, simplify without changing meaning, or regenerate the scene. Preserve the agreed minimum type size. Heavy outlines, opaque panels, or progressively smaller fonts do not substitute for readable layout. Check contrast and reading order at intended physical size; bounding boxes alone cannot judge them.

Keep page size and pixel size distinct: pixels = cm / 2.54 × export DPI; PDF points = cm / 2.54 × 72. For example, 28.5 × 20.6 cm is 2850 × 2060 pixels at 254 DPI. Record native generation resolution separately: upscaling does not create native print detail. Match aspect ratio before generation, preserve proportions, and inspect crops for lost content. Use publisher-specific bleed/gutter requirements when provided; do not assume a trim-sized PDF is press-ready.

## Review, repair, and deliver

Inspect every finished page at full resolution and intended reading size, plus a whole-book contact sheet for visual rhythm. Check identity, props, anatomy, text/image agreement, exact copy, contrast, overlap, and continuity. A toy-versus-animal reveal must show the relevant difference. Do not change a required fact to excuse incorrect art.

Run [scripts/validate_picture_book.py](../scripts/validate_picture_book.py) with the manifest in [picture-book-validation.md](picture-book-validation.md). It catches wrong counts/order, missing files, wrong pixel dimensions, repeated decoded source art, recorded text-bound violations, and missing per-page review. It cannot identify people, read image text, or prove visual quality. Similar-but-not-identical compositions require visual comparison even when this checker passes.

Mark a page reviewed only after inspecting its final composite. Bind review to the file SHA-256; rerendering invalidates that review. Retain concise findings and rejected versions separately. Geometry uses measured rendered bounds and observed protected regions, not the prompt's wished-for layout.

Export from the accepted manifest only. Verify image count/order, readability, ZIP members, and actual PDF page size/count when producing a PDF. Independently render opening, middle, ending, longest-copy and repaired PDF pages. Separate generated art, composed pages, and visually reviewed output in the handoff; include per-image metadata as a linked manifest. Preserve prior editions.

For upstream mechanisms and tradeoffs, consult [picture-book-sources.md](picture-book-sources.md). Those projects are references, not dependencies or substitutes for local acceptance.
