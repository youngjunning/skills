# Classic adventure cel-anime style

Use this preset when the user requests a `全职猎人` / `Hunter x Hunter`-like direction. The user calibrated this preset with late-1990s anime key visuals and selected `assets/identity-references/adventure-team-ensemble.png` as the persistent series reference. The target is classic cel-animation adventure artwork, not paper manga, cross-hatching or glossy modern anime.

The franchise phrase is a routing alias. Translate it into the reusable visual traits below before any outbound image prompt.

Attach the bundled ensemble reference to every generation made through this preset. Enter this preset only when the current request explicitly asks for this anime direction or explicitly asks to preserve the ensemble. A recurring AI Browser/FiaOS topic alone does not select it. If the user supplies a newer identity reference, route to `references/image-edit.md` and let the newer explicit reference win. The franchise name still stays out of the outbound prompt.

## Compliance boundary

- Do not send the franchise title, creator name, studio name, existing character names, powers, story locations, title logo, Japanese subtitle treatment, copyright line, or recognizable key-visual composition to an image model.
- The bundled asset is the user-selected persistent reference. Do not reproduce its logo, printed text, copyright line, numbered badges, exact pose, or photographic/key-visual composition in the output.
- When the current request explicitly selects this ensemble, preserve the four-person identities: black-and-green spiky-haired boy in green, white-haired boy in white and blue-violet, blond bob-haired youth in blue with red trim, and tall black-haired man with round glasses. Preserve count, faces, hair silhouettes, costume color blocks, relative ages/heights, and team relationship; vary only the task pose, props, setting, and placement required by the diagram.
- For architecture, timeline, process, or knowledge-map work, render labels, nodes, arrows, dates, and relationships deterministically. The generated layer supplies atmosphere and identity-locked character staging only.

## Visual signature

### Line and rendering

- Clean dark outlines with confident, mostly uniform contour weight; use slightly heavier exterior silhouettes and lighter interior facial or clothing lines.
- Flat cel colors with one hard-edged shadow step and occasional small highlight. Avoid painterly gradients, airbrushed rendering, 3D volume, heavy texture, screentone, or visible cross-hatching.
- Faces use simplified noses and mouths, large clear eyes with one or two controlled highlights, readable eyebrows, and expressions that remain legible at article width.
- Hair is designed as a strong graphic silhouette: angular spikes, compact bobs, or simple swept masses. Every original character should be distinguishable in silhouette.
- Background detail is simplified into large readable shapes. Texture may appear in maps, stone, sky, grass, architecture, or clouds, but must not muddy the characters or diagram overlay.

### Palette

- Use bright, decisive local colors: leaf green, cobalt or navy blue, clean white, warm yellow, and restrained red-orange accents.
- Skin tones remain warm and natural; shadows are slightly cooler or darker versions of the base color.
- Keep one dominant environment palette per image: parchment brown for historical maps, blue and green for open-air adventure, or stone gray and muted gold for formal task settings.
- Avoid neon cyberpunk, pastel kawaii wash, monochrome manga pages, muddy sepia over the whole image, and modern cinematic teal-orange grading.

### Ensemble composition

- Use the bundled four-person ensemble only after this preset has been explicitly selected; never add it merely because people might help explain the subject.
- Stage the group asymmetrically while preserving all four identities: one foreground lead, one or two midground specialists, and the taller figure behind. Preserve clean overlaps and distinct silhouettes.
- Give each person a task-relevant pose or prop. A team investigating a system should point, inspect, hold a map, operate a control, compare evidence, or verify a result rather than simply pose.
- Mix energetic and composed expressions inside the same group. The visual energy comes from contrast between curiosity, concentration, confidence, and caution.
- Crop from low angle, eye level, or a slightly elevated expedition view. Do not repeat the exact character placement of any source key visual.

### Task and costume adaptation

- Preserve the bundled identities and signature costume color blocks. Task adaptation may change pose, held objects, facial focus, and scene staging, but not substitute generic professionals or redesign the four characters.
- For FiaOS, use generic browser/workflow props and keep logos, numbered badges, fishing rods, title treatments, and copyright copy out of the generated image.
- For formal platform scenes, keep the same characters while using restrained navy, forest green, ivory, and amber in the surrounding environment and deterministic overlay.

## Structured-diagram adaptation

When this style is combined with `references/knowledge-map.md`:

- Keep the semantic question primary. Timeline, architecture, or workflow structure must still be readable without the character art.
- Generate a text-free cel-animation background with large clean color fields and low detail beneath diagram lanes.
- Put the identity-locked four-person ensemble or its task-relevant subset at the outer edge, in reserved gutters, or behind a low-opacity veil. When the user requires all four identities, all four must remain visible. They must not overlap labels, cards, arrows, or protected boundaries.
- Use card outlines and arrow strokes that echo the clean anime contour language. Prefer cream or white cards, dark navy/forest outlines, flat green/blue fills, and one amber confirmation color.
- A historical timeline may use a river, route, map, or stepping-stone metaphor, but dates and causal sequence remain deterministic overlays.
- An architecture diagram may place the bundled team inspecting layers, while the actual component boundaries remain geometric and exact.
- A process diagram may use a relay or expedition-route rhythm, while confirmation and readback branches remain explicit.

## Prompt recipe

```text
Use the bundled four-person ensemble image as the identity reference. Create a new late-1990s adventure cel-animation editorial background for <article section>. Preserve exactly the same four identities, facial silhouettes, hair shapes, costume color blocks, relative ages/heights, and team relationship; vary only <task pose, props, setting, and reserved placement>. Clean dark anime outlines, strong graphic silhouettes, flat saturated cel colors, one hard-edged shadow step, large expressive eyes, simplified facial features, asymmetrical ensemble staging, bright leaf-green/cobalt/navy/ivory palette with restrained red-orange or amber accents, simplified readable environment, low-detail protected lanes for deterministic diagram overlay, safe margins. Do not reproduce the reference logo, printed text, numbered badges, exact pose, or key-visual composition. No title logo, no text, no letters, no numbers, no copyright line, no watermark, no brand marks.
```

For a text-free backdrop, explicitly name every lane or region that must stay visually quiet. Do not ask the image model to draw nodes, dates, arrows, labels, or flowchart semantics.

## Series consistency

- Keep the same four identities, outline weight, eye construction, hair silhouettes, costume color blocks, cel-shadow rule, saturation, and ensemble relationship across a set.
- Change setting and task posture across images: expedition/history, architecture inspection, and operational workflow should not reuse one poster layout.
- Keep confirmation and human judgment amber across technical figures; reserve red for blocked, failed, or irreversible actions.
- Use exact text only in the deterministic overlay.

## QA gate

Reject or regenerate when any of these is true:

- any of the four required identities is missing, duplicated, merged, replaced by a generic person, or materially changed in face, hair, costume color blocks, relative age/height, or team relationship;
- the output reproduces the reference logo, printed text, copyright line, numbered badges, exact pose, or source-key-visual layout;
- the result looks like monochrome manga, paper-and-ink sketching, screentone, watercolor, photorealism, glossy modern anime, or 3D game art;
- every character is standing frontally with the same expression and no task relationship;
- gradients or texture replace the flat cel-color structure;
- the background competes with diagram labels or protected lanes;
- text, pseudo-text, logo-like marks, copyright lines, watermarks, cropped extremities, or edge contact remain;
- the architecture, timeline, or process cannot be understood without guessing through the decorative layer.

For identity-preserving edits, also apply the identity QA gate in `references/image-edit.md`: any unrequested change to face, hair, costume, proportions, count, required placement, props, or ensemble order is a failure.

## Calibration basis

Recalibrated on 2026-08-21 from four user-supplied late-1990s anime key visuals. The reusable findings were:

- confident dark outlines and flat cel colors;
- large expressive eyes and simplified facial construction;
- saturated green, blue, white, yellow, and red-orange local colors;
- asymmetrical four-person ensemble staging with clean silhouette separation;
- adventure-map, open-sky/grass, task-prop, and formal stone-interior settings;
- costumes changing with the task while the character-rendering grammar remains stable.

The user-selected persistent ensemble reference is bundled at `assets/identity-references/adventure-team-ensemble.png` and must be attached to every generation routed through this preset.
