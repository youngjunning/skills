# Technical Book Cover

Use this together with `references/text-poster.md` when the output is a technical, nonfiction, engineering, or business book cover. Generate the visual backdrop without text; render every title, subtitle, author name, edition, and publisher mark with HTML/CSS.

## Design contract

- Make the title the first thing readable at a 320 px-wide thumbnail. Subtitle, author, and context must be secondary.
- Use one focused visual metaphor for the subject. For an AI Browser book, a browser silhouette flowing into agent nodes communicates the thesis better than a dashboard, robot, or generic circuitry.
- Reserve a genuinely quiet title field. Do not put the hero object, bright glow, dense nodes, or fine detail behind the title.
- Match the book genre: restrained editorial typography, clear contrast, and one professional palette. Avoid neon cyberpunk, faux code, browser UI screenshots, and feature-card clutter unless the book itself is a UI catalogue.
- Keep all copy in safe margins. Never rely on cropping to hide an overflow.

## Default technical-book layout

Unless the publisher supplies a trim specification, use a 2:3 front cover:

```text
logical canvas: 1600 x 2400
Chrome DPR:    2
deliverable:   3200 x 4800 PNG + WebP
safe margin:   120 logical px minimum on each side
```

Use a small English/context kicker, a dominant title in the upper half, a concise subtitle below it, and author/edition information in the lower safe area. Keep any vertical side copy decorative and legible rather than necessary to identify the book.

## Backdrop prompt pattern

State the format, empty region, single metaphor, palette, and exclusions explicitly. For example:

```text
Portrait technical book cover backdrop, no text, no letters, no logos, no UI screenshot.
Deep-lake ink editorial canvas with restrained teal mist, gray-blue contours, and rare warm-gold edge light.
One elegant browser-window silhouette at the lower third dissolves into a small constellation of connected agent nodes.
Keep the upper half and left side quiet and dark for title typography; premium engineering nonfiction; readable at thumbnail size.
No neon cyberpunk, robots, humans, code, DNA, clutter, interface panels, or decorative labels.
```

Use `848x1280` for the generated portrait backdrop unless the selected model requires another supported size. Visually inspect it before compositing; regenerate when the title field is busy or the metaphor is unclear.

## Typography and composite

Use `PingFang SC` first for Chinese. Compose at the logical canvas size with a `file://` backdrop, then use Chrome at `--force-device-scale-factor=2`. Add a dark vignette or side shade behind text only when needed for contrast; do not dim the whole cover.

Before delivery, inspect both the full raster and a 320 px-wide thumbnail. Reject the cover if the title loses hierarchy, any text touches an edge, the author competes with the title, or a visual element makes the technical subject look like generic AI marketing.

## Deliverables

- Keep a full-resolution PNG for print review.
- Export WebP for repository pages; use q90 for text-heavy composition, then lower quality only until it remains legible and meets the applicable size budget.
- Write metadata for each deliverable, including model, requested and actual size, output format, file size, elapsed generation time, prompt, and post-processing steps.
- Report the image and print paths separately. A front-cover image is not a print-ready full wrap; spine, bleed, barcode, paper, and binding must wait for publisher specifications.
