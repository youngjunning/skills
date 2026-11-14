# Third-party components and adapted guidance

The report theme, generators and integration guidance are maintained in this skill. Bundled libraries retain their original licenses and are not claimed as original skills.

1. Pakco HTML presentation assets: https://github.com/pakco77/pakco-html, MIT, copyright 2026 lewis. Only the deck foundation, playback runtime, 27 CSS animations and 20 Canvas FX modules are adapted from upstream; webpage mode, style picker, social cards and the 36 upstream themes are excluded. Joyally Design maintains its own presentation source model, layouts, scenario starters, six theme mappings, gallery and PNG/PDF export. The bundled license is `assets/presentation/LICENSE`. Reports use independent Joyally CSS and do not bundle these assets.
2. Archify: https://github.com/tt-a1i/archify, Apache-2.0 (current upstream runtime; historical MIT portions retain `LICENSE-MIT`), copyright 2026 tt-a1i (Archify), copyright 2025 Cocoon AI. Runtime provenance, version, notices and additional asset terms are retained in `runtime/diagram/UPSTREAM.json`, `LICENSE`, `LICENSE-MIT`, `NOTICE` and `THIRD_PARTY_NOTICES.md`.

Private product artwork, deployment adapters and historical installation or acceptance evidence are not distributed.

The reference screenshots in `assets/references/qingshan-lake/` were supplied by the user from videos. They retain subtitles and player edges, are provided for design observation only, and are excluded from Joyally Design's PolyForm license. The repository does not claim ownership of the original footage.

Local Archify modification: `assets/template.html` and `explainer/reader.css` use Joyally semantic colors for all viewer and reader styles, both themes, chrome and print. Palette mappings are maintained in Joyally's `assets/joyally-design.tokens.json`; the upstream renderer geometry and licenses are retained. See `runtime/diagram/UPSTREAM.json` for provenance and validation.

## Design quality guidance

`references/design-quality.md` includes adapted guidance under Apache-2.0. The pinned source commit and adaptation details are recorded in `legal/quality-guidance/UPSTREAM.json`; the required upstream license and notice remain in `legal/quality-guidance/LICENSE` and `legal/quality-guidance/NOTICE.md`.

Modified for Joyally Design: condensed and translated the review, audit, refinement and task-selection methods; made aesthetic rules conditional on the product and platform; replaced CLI, hooks, detector, snapshot storage and agent orchestration requirements with Joyally's existing validation workflow. The upstream notice is preserved as required by its license; its iOS and Android derivative reference files are not included.

## Hallmark

The tier names, selected default-pattern checks and before/kept preservation concept in `references/quality-gates.md` were inspired by Hallmark, https://github.com/nutlope/hallmark, MIT, copyright 2026 Hallmark contributors. Joyally Design independently implements the browser rules, explainable exception format and DOM contract comparison; it does not bundle Hallmark themes or page assets. The pinned source commit and scope are recorded in `legal/hallmark/UPSTREAM.json`, with the upstream license and adaptation notice alongside it.
