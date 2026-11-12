# Article cover gate

Use this reference for every persistent reader-facing article, blog post, ATA, tutorial, product introduction, opinion essay, or technical analysis handled in Blog mode.

## Ownership

`joyally-writting` owns the cover decision: what promise the cover should make, which identity and facts it must preserve, where it appears, whether an existing cover remains valid, and what evidence proves it is deliverable. An image-generation skill or tool may create the pixels, but it does not decide the article's thesis or publication state.

## Hard requirement

Every persistent article must have exactly one explicit cover before it is publish-ready.

- A cover is the article's entry visual. It conveys subject, tone, product identity, user scene, or central tension before the reader enters the detailed argument.
- An architecture diagram, flowchart, knowledge map, lifecycle map, dependency graph, table, dashboard screenshot, code screenshot, or dense UI screenshot is an explanatory figure. It must stay inside the article and cannot serve as the cover.
- A technical article may use the same visual language for its cover and diagrams, but the cover must remain scene-led or identity-led rather than diagram-led.
- A draft without a usable cover may still be handed off as a draft, but publication must remain blocked and the missing cover must be reported explicitly.

## Reuse before regeneration

Do not regenerate a cover mechanically on every edit.

Reuse the current cover when it still matches the title, central judgment, product identity, audience, and publication format, and when its local or remote asset can be verified. Regenerate or replace it when the article's promise changed, the cover represents an obsolete product state, the asset is missing, or the existing image is actually an inline diagram being used as a substitute.

## Cover brief

Write this compact brief before generation or selection:

```text
Article:
Reader:
Central promise:
Visible subject or scene:
Required identity references:
Visual language:
Composition and safe area:
Text policy:
Target surface and aspect ratio:
Local asset path:
Remote/publication requirement:
```

The brief should earn one clear visual idea. Do not combine product scene, architecture overview, package graph, roadmap, metrics, and team portrait into one poster.

## Valid cover directions

Choose the smallest direction that matches the article:

- **Product scene:** the user or operator encounters the product in a recognizable working moment.
- **Identity-led project visual:** a stable project character, object, environment, or product silhouette carries the subject.
- **Conceptual editorial scene:** one concrete visual metaphor expresses the article's tension without pretending to be system architecture.
- **Typographic cover:** restrained title treatment over an atmospheric or identity-led visual when the publication surface needs baked-in copy.

Avoid generic AI glows, floating dashboard cards, illegible pseudo-UI, decorative code, or a collage of every section in the article.

## Generation handoff

Use [visual-routing.md](visual-routing.md) to distinguish a cover from an explanatory figure and to route mixed artwork plus semantic content. The cover-specific requirements below still apply.

When a new cover is required, use the image-generation capability available in the current environment. If `joyally-image` is available, route scene-led covers through its cover/portrait reference and text-heavy covers through its text-poster reference. Do not route a cover through the knowledge-map or architecture-diagram reference.

Pass the cover brief and every required identity reference to the image workflow. Identity preservation outranks stylistic reinterpretation. Keep exact title text out of the raster model when deterministic overlay is available.

## Placement

Follow the publication surface's existing convention:

- If frontmatter or a CMS has a dedicated cover field, bind the cover there.
- If Markdown is the publication source without a cover field, place the cover as the first reader-facing image before the first major `##` section, normally after the short opening.
- Keep architecture diagrams and other evidence images at the sections whose claims they explain.
- Record one canonical local source asset. When the target surface requires a remote URL, upload and verify that URL separately; a local file does not prove publication.

## Acceptance gate

Before calling the article publish-ready, verify:

1. exactly one image is designated as the cover;
2. the cover is not an architecture diagram or another explanatory figure;
3. the image matches the article title, central promise, audience, and current product state;
4. required people, characters, products, and brand identities are preserved from authoritative references;
5. title-safe space, crop, contrast, resolution, file type, and size fit the target surface;
6. the local asset exists and renders from the article's final location;
7. any required uploaded URL returns the expected image content type;
8. repository change, asset upload, article publication, and live-page readback are reported as separate states.

Report unresolved identity, rights, asset, upload, or publication issues only when they materially affect the requested delivery or publication state.
