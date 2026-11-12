# Third-party components and adapted guidance

The report theme, generators and integration guidance are maintained in this skill. Bundled libraries retain their original licenses and are not claimed as original skills.

1. Pakco HTML: https://github.com/pakco77/pakco-html, MIT, copyright 2026 lewis. The bundled subset contains the base stylesheet, deck runtime and animation stylesheet, pinned to `8cefc6b6b68d85a1484e066c47ae571b75d0d4e1`. Its complete license is `runtime/html/LICENSE`.
2. Archify: https://github.com/tt-a1i/archify, Apache-2.0 (current upstream runtime; historical MIT portions retain `LICENSE-MIT`), copyright 2026 tt-a1i (Archify), copyright 2025 Cocoon AI. Runtime provenance, version, notices and additional asset terms are retained in `runtime/diagram/UPSTREAM.json`, `LICENSE`, `LICENSE-MIT`, `NOTICE` and `THIRD_PARTY_NOTICES.md`.

Private product artwork, deployment adapters and historical installation or acceptance evidence are not distributed.

The reference screenshots in `assets/references/qingshan-lake/` were supplied by the user from videos. They retain subtitles and player edges, are provided for design observation only, and are excluded from Joyally Design's PolyForm license. The repository does not claim ownership of the original footage.

Local Archify modification: `assets/template.html` and `explainer/reader.css` use Joyally semantic colors for all viewer and reader styles, both themes, chrome and print. Palette mappings are maintained in Joyally's `assets/joyally-design.tokens.json`; the upstream renderer geometry and licenses are retained. See `runtime/diagram/UPSTREAM.json` for provenance and validation.

## Design quality guidance

`references/design-quality.md` includes adapted guidance under Apache-2.0. The pinned source commit and adaptation details are recorded in `legal/quality-guidance/UPSTREAM.json`; the required upstream license and notice remain in `legal/quality-guidance/LICENSE` and `legal/quality-guidance/NOTICE.md`.

Modified for Joyally Design: condensed and translated the review, audit, refinement and task-selection methods; made aesthetic rules conditional on the product and platform; replaced CLI, hooks, detector, snapshot storage and agent orchestration requirements with Joyally's existing validation workflow. The upstream notice is preserved as required by its license; its iOS and Android derivative reference files are not included.
