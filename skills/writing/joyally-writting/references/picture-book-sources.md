# Open-source references for picture-book production

Reviewed 2026-11-01. These are selected mechanisms, not end-to-end quality claims. No upstream code, templates, artwork, or model weights are bundled.

| Source | Inspected evidence | Applied decision |
| --- | --- | --- |
| [weaiw/storybook-generator-skill](https://github.com/weaiw/storybook-generator-skill/tree/72d30ecd51d12986738db6d4f40d79cd7fa6358a) | `references/character-continuity.md`, `prompt-workflow.md`, `qa-checklist.md`; MIT | Separate recurring attributes from page action; require visible evidence for text; inspect pilot pages; repair rejected pages individually. |
| [KalminX/storybook_generator](https://github.com/KalminX/storybook_generator/tree/c4943b9230109938725de98e87bdc66cad3cad9e) | `src/generation/character_bible.py`, `image_generator.py`, `src/rendering/pdf_renderer.py` | Separate character data, scene prompt, provider call, and rendering. Keep authoritative copy outside image generation and verify decoded images. No repository license file was found in this snapshot; code is inspected conceptually, not copied. |
| [HVision-NKU/StoryDiffusion](https://github.com/HVision-NKU/StoryDiffusion), [paper](https://arxiv.org/abs/2405.01434) | Official README and research description of consistent self-attention; repository identifies Apache-2.0 | Sequence identity consistency is separate from per-page storytelling. This model-internal method is not exposed by the current hosted API; attaching references does not implement StoryDiffusion. |

The first two projects also offer fixed caption/split layouts. Those defaults do not satisfy integrated scene lettering. Earlier-illustration conditioning can copy camera arrangement as well as identity, so this skill uses role-scoped references and inspects variation in pilot pages. These are local adaptations, not claims that upstream guarantees either behavior.

The observed local failure combined repeated full-cover references with generic camera-variation instructions and a renderer placing prose outside the art. The earlier skill allowed a separate text band and lacked concrete variation checks. The revised workflow constrains generation and composition and reviews finished pages rather than API success alone.
