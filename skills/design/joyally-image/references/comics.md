# Comics: sequential art production

Use for a comic page, strip, vertical webtoon, knowledge comic, storyboard, or repair of one of these. This skill owns the entire comic: narrative beats, panel design, art, lettering, composition, export, and visual review. When the comic appears in an article, `joyally-writting` supplies the article's verified claims and places the finished pages; it does not direct panels or letter them. A standalone comic needs no article.

This workflow adapts the analysis → storyboard → cast → prompts → page review → targeted repair cycle from [baoyu-comic](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-comic) ([MIT License](https://github.com/JimLiu/baoyu-skills/blob/main/LICENSE), Copyright © 2026 Jim Liu). It keeps this skill's image backend and editable lettering. The sequential-design criteria are grounded in the linked creator and editor sources in [the research note](../../../../research/comic-sequential-design.md).

## 1. Set the comic contract

Record the reader, format (page, strip, or vertical scroll), reading direction, scene's before/after change, technical or narrative facts, cast, target display width, and destination asset conventions. For a knowledge comic, separate observed product behavior from illustrative scenes. Choose page and panel count from the action; no fixed six-panel layout or repeated two-panel template.

Choose characters in this order: user-provided cast, destination project's approved cast, local `~/.config/joyally-image/comic-characters.md` override, then the bundled [小界和小南 roster](comic-characters.md) **only when those characters suit the requested comic**. Do not add them to an unrelated comic by default. Read the manifest and inspect the relevant reference images before drawing. Preserve identity across panels while changing pose, expression, camera, and staging as the story requires.

## 2. Thumbnail the whole page before rendering

Make a compact storyboard beside the editable assets. One row per panel must state: panel ID and reading order; what changes since the previous panel; visible action/evidence; shot size and point of view; characters and positions; exact dialogue/caption/SFX; bubble position and speaker tail; continuity notes; fact source when relevant. Sketch the page or scroll segment at thumbnail size so the reading path, dominant panel, gutters, and balloon order are apparent before generating detailed art.

Every panel must add a new observation, action, reaction, or consequence. Vary framing to show the actual mechanism: an establishing view, hand or interface detail, consequence, and character reaction may each be appropriate. Do not fill a page with characters in the same pose explaining an unseen event. Keep screen direction, props, and task state consistent across adjacent panels; a deliberate jump needs a visual cue.

For example, a mistaken same-name button can progress as: two matching buttons on different rows → finger selects the wrong row and the wrong item changes → character checks the row label → new selection changes the intended item. Four meaningful beats can fit a page; four portraits with four captions do not depict that change.

## 3. Draw and compose as one sequence

Use `generation.md` and `prompt-compliance.md` for the configured model, API, metadata, and retries. Use `image-edit.md` to repair an existing panel or preserve an approved character. Panel-level generation is preferred when identity, action, or one failed cell needs a targeted fix; a whole-page generation is acceptable only if individual panels remain reviewable and the final result passes the same lettering and continuity gates. Generate a representative panel/page first and inspect it before scaling a batch.

Each prompt specifies the panel's *new* visible event, camera, relevant reference-image roles, character positions, recurring setting/props, and space reserved for balloons. Keep the world and large visual anchors stable. Generate clean art without baked-in technical text by default. Exact dialogue, commands, labels, and bubble tails are added as editable layers after art generation. Do not paste the same portrait or full-scene illustration into several panels as a substitute for redrawing the action.

Compose panels into an intentional page or scroll sequence. A page uses an unambiguous eye path and size contrast to control emphasis; a vertical webtoon uses viewport-sized beats and spacing to control reveal and pause. In both, adjacent panels must be visually and causally connected. The final output cannot be a stack of independent illustration cards.

## 4. Letter inside the comic

Place speech and thought balloons, captions, and sound effects in the storyboard before final art. Add exact copy as editable typography within the associated panel or a clearly connected borderless beat. A balloon tail must identify its speaker; the order of balloons must follow the reading path. Keep faces, hands, objects, and visible evidence clear. Use captions only where pictures cannot carry necessary context, and keep article prose outside the comic as prose.

Deterministic lettering is allowed and preferred for Chinese text, commands, and factual labels. It should behave as comic lettering: shaped balloons, tails, integrated placement, breathing room, and varied emphasis when the story calls for it. A rectangular row labeled with a character's name under one illustration is a transcript, not an integrated balloon. Repair lettering in its editable layer; if a balloon cannot fit, change the panel composition or reduce copy without losing the fact.

## 5. Accept or repair the final page

Inspect the finished composite at full resolution, whole-page thumbnail, actual article width, and narrow phone width. Read it in the chosen direction without the surrounding article. Confirm that panel order, action/state change, character identity, scene geography, speaker tails, exact text, and factual labels all survive. Cover the captions and ask whether the visible action still conveys the key event; some information may require words, but the plot must not exist only in a text block.

For panels where a character touches a screen, paper, tool, or another character, zoom into every contact point before acceptance. Trace each arm through wrist and fingers, count fingers when visible, and check that the object's edge and the hand obey one consistent front-to-back order. Reject hands that emerge from a display, pass through a solid object, or lose their visible connection to the arm. If the interaction fails, simplify the staged action to a physically clear one (for example, a hand on a laptop touchpad), repair that panel with the approved image as reference, then inspect the contact point again in both source art and final composite.

**Reject** a title + one scene illustration + separate dialogue rows or conclusion box as a comic page. Also reject repeated talking-head panels, disconnected postcard scenes, ambiguous reading order, bubbles without clear speakers, clipped text, or a mobile page whose lettering only works when zoomed. Classify such an output as an illustrated article/card and redraw the relevant panels before calling it a comic.

Keep the storyboard, panel source art, editable layout/lettering, exact copy, references and versions, generation metadata, review notes, and final exports together under the destination's asset convention. For a repair, change the failed panel/layout only when unaffected pages are already approved. Report what was visually inspected; API success and a valid image file are not comic acceptance.
