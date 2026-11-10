# Third-party components and adapted guidance

The report theme, generators and integration guidance are maintained in this skill. Bundled libraries retain their original licenses and are not claimed as original skills.

1. Pakco HTML: https://github.com/pakco77/pakco-html, MIT, copyright 2026 lewis. The bundled subset contains the base stylesheet, deck runtime and animation stylesheet. Its complete license is `vendor/pakco-html/LICENSE`.
2. Archify: https://github.com/tt-a1i/archify, Apache-2.0 (current upstream runtime; historical MIT portions retain `LICENSE-MIT`), copyright 2026 tt-a1i (Archify), copyright 2025 Cocoon AI. Runtime provenance, version, notices and additional asset terms are retained in `vendor/archify/UPSTREAM.json`, `LICENSE`, `LICENSE-MIT`, `NOTICE` and `THIRD_PARTY_NOTICES.md`.

Private product artwork, deployment adapters and historical installation or acceptance evidence are not distributed.

Local Archify modification: `assets/template.html` and `explainer/reader.css` use Joyally semantic colors for all viewer and reader styles, both themes, chrome and print. Palette mappings are maintained in Joyally's `assets/joyally-design.tokens.json`; the upstream renderer geometry and licenses are retained. See `vendor/archify/UPSTREAM.json` for provenance and validation.

## Impeccable design guidance

`references/design-quality.md` and its routing in `SKILL.md` adapt design guidance from [pbakaus/impeccable](https://github.com/pbakaus/impeccable), licensed under Apache-2.0. Original attribution: Impeccable contributors. The pinned source commit, selected source files and adaptation details are recorded in `vendor/impeccable/UPSTREAM.json`; the complete upstream license and notice are retained as `vendor/impeccable/LICENSE` and `vendor/impeccable/NOTICE.md`.

Modified for Joyally Design: condensed and translated the review, audit, refinement and task-selection methods; made aesthetic rules conditional on the product and platform; replaced CLI, hooks, detector, snapshot storage and agent orchestration requirements with Joyally's existing validation workflow. This is adapted guidance, not a bundled or installed Impeccable runtime. The upstream notice is preserved for attribution; its iOS and Android derivative reference files are not included.

## oil-ui-pro process reference

`references/design-workflow.md` was independently written for Joyally Design after reviewing a user-provided `oil-ui-pro` 0.33.3 archive by [oil-oil](https://github.com/oil-oil). `references/oil-ui-pro-integration.md` now routes Joyally Design to a separately installed package at runtime, covering its task methods and original tools. The external package remains in its own installation and is not part of this MIT repository. No upstream code, assets, templates, or substantial prose is bundled; the source archive did not include a redistribution license. This integration does not claim ownership of oil-ui-pro.
