# Voice profile registry

Use named profiles to reproduce a stable set of writing decisions without copying an author's sentences or inventing their experience.

## Routing

| Request | Load |
| --- | --- |
| 紫升风格, 俊宁风格, `blog.zisheng.pro` house voice | [style-zisheng.md](style-zisheng.md) |
| 团队项目外宣、团队项目介绍、阶段成果对外表达、产品形态与工作方式说明 | [style-team-project-external.md](style-team-project-external.md) |
| 体系化技术长文、系统性知识梳理、原理/架构/工程实践文章、框架式技术文章 | [style-systematic-engineering.md](style-systematic-engineering.md) |

If no profile matches, preserve the source voice or use the general workflow. Do not approximate a named author from vague cultural stereotypes.

## Application order

1. Preserve facts, constraints, terminology, quotations, and the author's actual position.
2. Make the argument sound enough for its genre.
3. Apply the selected profile's viewpoint, structure, diction, rhythm, and ending behavior.
4. Run the AI-flavor gate so profile markers do not become repeated mannerisms.

Logic and facts outrank style. A profile may change how a qualified claim sounds; it may not remove the qualification.

## Adding another profile

Create one `references/style-<name>.md` file and add one routing row above. Keep references one level below `SKILL.md`.

Use this schema:

1. **Source and scope:** corpus, snapshot date, genres, and which material receives the most weight.
2. **Voice contract:** narrator position, reader relationship, confidence, and formality.
3. **Reasoning signature:** how the voice moves from observation to conclusion.
4. **Structure recipes:** common shapes by genre, not one mandatory outline.
5. **Diction and rhythm:** language mix, sentence and paragraph behavior, formatting.
6. **Opening and ending behavior:** how the voice enters and leaves a topic.
7. **Anti-mimicry rules:** phrases, biography, and habits that must not be fabricated or overused.
8. **Calibration checklist:** observable tests for whether the profile is present and natural.

Record corpus statistics as dated evidence, not timeless rules. Refresh a profile when the author's current work has materially changed.

## Blending profiles

Blend profiles only when the user explicitly asks. Name one dominant profile and list the borrowed traits from the secondary profile. Never average two voices into generic polished prose.
