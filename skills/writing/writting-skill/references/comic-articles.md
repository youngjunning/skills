# Comic articles

Use this Blog article shape for 漫画文章、漫画拆解 and scene-led technical explainers. The deliverable is a complete article with embedded comic pages, a distinct cover, sources, and maintainable visual assets. Let the subject determine page count and panel layout.

For revisions, change only the requested prose, panels, lettering, or cast. Reuse approved unaffected pages and the cover; article-level acceptance does not require regenerating them. An image-only repair request remains scoped to that repair.

## Establish the argument before the panels

Read the destination's article and asset conventions. Identify the reader's question, central explanation, factual sources, version, and illustrative versus observed behavior. Draft enough prose to establish the argument, then map its scenes; finish and review both together. An image batch alone does not fulfill an article request.

For each panel record the learning point, task state, speaker, visible action or evidence, camera/composition, exact dialogue or command, and supporting source. Keep this compact table or scene list beside the editable article assets. Put factual anchors and uncertainty in prose as well as dialogue. Characters explain or demonstrate a system; their dialogue does not establish the real system's ownership or capabilities.

Choose scenes that show causes and consequences: a changed observation, an action, an observable result, or a failure and recovery. Match panel detail to the explanation. Use screenshots only as observed product evidence and label generated interfaces and example outputs as illustrations.

## Resolve the character roster

Use a user-supplied roster first, then the destination project's configured roster. An optional `~/.config/writting-skill/comic-characters.md` can supply local overrides. Otherwise use the bundled [小界 and 小南 roster](comic-characters.md) and its relative image references; no local configuration or external project checkout is required. Use this cast by default for comic articles unless the user or destination specifies another cast.

Each entry identifies the character, its authoritative identity document and inspected reference images, stable appearance markers, and intended narrative role. Read the linked identity document at execution time so a new approved design replaces obsolete versions. Keep one authoritative identity source rather than copying image sets into every skill or article.

Inspect relevant references before using them. Preserve face, hairstyle, iris color, clothing palette, accessories, and illustration language; let pose, expression, camera, gesture, and environment follow the scene. Use the roster's approved cast by default when applicable; panels can feature one character, several, or an object alone.

New scenes redraw the characters in context. A portrait reference constrains identity, not a repeated bust pose or composition. Do not repeatedly paste the same avatar into panels. When repairing an existing approved panel, edit the requested character or region and protect the accepted surrounding artwork; identity preservation does not require copying unchanged portrait pixels into new scenes.

The bundled cast and reference art are included under the user's explicit distribution request. Keep any additional private roster, local paths, internal URLs, and source history out of public skill distribution. A local override does not itself grant permission to publish its private characters.

## Generate artwork through better-imagegen

Read the available better-imagegen Skill before image work. It owns API calls, credentials, model selection, timeout and fallback behavior, prompt compliance, response handling, and generation metadata. This workflow does not duplicate those instructions or invoke a different generator as a shortcut.

Pass a page- or panel-specific brief with the visible action, camera, character identity references and their roles, scene-specific props, and space for lettering. Use its image-edit route when preserving existing character designs. For a continuous multi-page scene sequence, consult its picture-book guidance for recurring-character and composition QA without importing print-book packaging requirements into a web article.

Keep the scene instruction prominent. Reuse authoritative identity references rather than repeatedly chaining each new output as the next reference. Avoid identity details that make two characters visually converge. Their silhouette and large clothing colors should remain distinct at article reading size.

Finish a representative page or panel before scaling the batch. Inspect identity, action, visual evidence, and text room. This is an agent QA step; already authorized scope and approved cast do not need another confirmation. Repair the observed defect before generating the remaining pages.

## Typeset and integrate

Default to generated scene art with editable, deterministic dialogue, captions, technical labels, and commands. Fit lettering into the scene or speech bubbles and keep technical callouts readable. Honor an explicit request for model-rendered text, then inspect every glyph. Use deterministic diagram authoring for exact arrows or relationships when needed, following [visual-routing.md](visual-routing.md).

Check the final composite, not only the scene image: text must match the mechanism, commands must remain executable examples, bubble tails must identify the speaker, and faces, hands, props, and evidence must remain legible. Reflow lettering or revise the scene when it does not fit; preserve useful reading size.

Place comic pages near the prose they explain. Include the practical commands, sources, tradeoffs, and result-validation criteria required by the subject. The distinct cover follows [article-cover.md](article-cover.md); an internal page is not automatically a cover. Keep the article useful when a reader needs to copy a command or follow a source link.

## Joint acceptance and maintenance

Inspect every finished page at full resolution and the article's actual reading width, including a narrow viewport when the destination supports it. Review the whole sequence for varied actions and composition, consistent character identity, factual continuity, page order, text clarity, and clipping. Compare eyes, hair, outfit colors, accessories, and speaker attribution across pages.

Keep editable layouts, source art, exact copy, generation metadata, current identity versions, and final exports in the destination's prescribed locations. Use its existing image format, size budget, upload/readback, and publication rules; tool API success is not visual acceptance. Re-exporting invalidates the affected page's visual review.

For later character redesigns, update the selected canonical identity first. For the bundled cast, update its character manifest, reference art, and roster together; for a project override, follow that project's maintenance rules. Audit the affected current comic pages and cover together; retain historical evidence as historical. Report article, images, local review, commit, push, and deployment at their observed states. Do not start image generation merely to test this writing reference during skill maintenance.
