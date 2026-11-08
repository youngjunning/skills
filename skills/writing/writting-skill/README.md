# Writting Skill

A general-purpose Codex writing skill for Chinese and English prose. Persistent publishing work has two top-level modes: **Blog** and **Book**.

It activates when the user asks for a writing deliverable, continuation, rewrite, polish, or editorial review. Natural requests such as “写一篇文章” are sufficient. Routine coding, explanations, progress replies, incidental documentation updates, automatic maintenance, and questions about the skill do not activate its writing workflow.

**Blog mode** covers blog posts, technical articles, ATA, tutorials, product or project introductions, and opinion essays. It owns single-article structure, current-product evidence, and publication checks.

Its **Comic article** shape owns prose, fact checks, sources, and page integration. `better-imagegen` owns the comic production, including storyboard, cast, scene art, lettering, layout, and visual review. Its [小界 and 小南 roster](../../design/better-imagegen/references/comic-characters.md) includes portable portrait and full-body references. See [Comic articles](references/comic-articles.md).

**Book mode** covers books, ebooks, handbooks, manuscripts, chapter planning, and cross-chapter revision. It keeps a durable book contract, chapter map, evidence or story state, and cross-chapter review cadence. Its AI technical-book profile adds minimally qualified reader design, executable examples, reproducible experiments, version snapshots, and operational boundaries.

Its [Picture book](references/picture-book.md) workflow owns the story, exact copy, page count including requested covers, typography, print templates, validation and separate-image delivery. `better-imagegen` is the designated illustration and image-edit provider. Cover and interior templates are recorded independently; changing the page count also updates visible folios and packaged filenames.

Proposals, reports, technical documentation, product copy, speeches, and short copy continue to use the shared writing workflow; they are utility deliverables rather than a third publishing mode. All paths start from audience, purpose, evidence, and structure, test reasoning when needed, apply an optional named voice profile, and review clarity and natural wording.

The first bundled profile is **紫升风格**, distilled from the author's public writing on `blog.zisheng.pro`. The profile system is extensible: each future voice lives in its own reference and is selected explicitly rather than becoming a global default.

Public or commercial manuscripts must pass separate similarity and copyright gates backed by a source-rights ledger, local exact and near-overlap scans, targeted web or publisher-approved external checks, and named human review.

When a book's technical方案 refers to open-source projects, the gate distinguishes ordinary citation, independent architectural explanation, dependency use, and actual expressive reuse. Only copied, adapted, screenshotted, vendored, or distributed material escalates to exact-commit, path-scoped License obligations; a project mention does not turn the book into a derivative work.

## Install

Clone this repository into your Codex skills directory:

```bash
npx skills add youngjunning/skills --skill writting-skill -g
```

Restart Codex if the skill does not appear immediately.

## Use Blog mode

Create a new technical article:

```text
使用 $writting-skill 写一篇技术博客。先明确读者和核心判断，再基于提供的资料成稿并完成事实、结构和文风检查。
```

Apply the bundled 紫升风格 profile:

```text
使用 $writting-skill，以紫升风格重构这篇技术文章。保留事实和第一人称经历，
先修正论证，再强化“真实问题 → 工程机制 → 判断框架”的推进方式。
```

## Use Comic articles

For a comic article, stay in Blog mode:

```text
使用 $writting-skill 写一篇漫画拆解文章。先核验原理并完成正文，
将漫画的分镜、人物、对白、排版与验收交给 better-imagegen，最后把成品放回文章对应位置。
```

## Use Book mode

Start or continue a book in the author's voice:

```text
使用 $writting-skill 写这本书。加载紫升风格，先建立 book contract、章节依赖和版权台账，
逐章维护事实与连续性；任何公开或商业交付都必须通过 copyright gate。
```

Plan an AI technical book:

```text
使用 $writting-skill 规划一本面向前端工程师的 Agent 工程书。采用紫升风格，明确最小合格读者、
持续项目主线、可运行代码、实验复现和版本快照；研究只能吸收方法，不能复制受保护表达。
```

Reference open-source projects in a technical book:

```text
使用 $writting-skill 写这本原创技术书，其中部分方案参考开源项目。项目引用和独立方案讲解只记录来源与版本；
只有复制或改写代码、README、图、截图，或者随书分发第三方代码时，才核验 commit、路径级 License、
NOTICE 和 Copyleft obligations，并在公开交付前运行 open_source_license_review。
```

Run the local book similarity gate without uploading the manuscript:

```bash
python scripts/check_book_similarity.py manuscript/ \
  --ledger sources/copyright-ledger.json \
  --report reviews/similarity-report.json
```

In an interactive Codex task, ask the Skill to run targeted web discovery directly. It uses the built-in web search capability available to the current session, so no separate search service or API key is required:

```text
使用 $writting-skill 对这本书执行出版前查重。先运行本地 similarity gate，再用 Codex 联网搜索每个高风险章节的特征句，
逐条打开候选来源并记录 query、URL、日期、稿件 hash、审阅人和处置结论。不要上传整本书，也不要把相似度百分比当成版权结论。
```

For standalone CLI, CI, scheduled, or unattended checks, enable the optional Brave Search adapter:

```bash
export BRAVE_SEARCH_API_KEY="REPLACE_ME"
python scripts/check_book_similarity.py manuscript/ \
  --ledger sources/copyright-ledger.json \
  --web-provider brave \
  --require-web \
  --report reviews/similarity-report.json
```

Review any candidates, write `reviews/similarity-decisions.json`, then rerun with `--decisions reviews/similarity-decisions.json`. The report keeps exact locations and evidence instead of treating one aggregate similarity percentage as a copyright verdict. The Python checker makes no network request unless a provider is selected; it cannot call the web tool belonging to a Codex conversation.

For a Chinese-language book intended for publication in mainland China, Wanfang is the default domestic report adapter unless the publisher mandates another platform. Submit through the [official Wanfang service](https://jc.wanfangdata.com.cn/), download the official report, verify its number at the [official authenticity page](https://truth.wanfangdata.com.cn/), then bind it to the manuscript:

```bash
python scripts/check_wanfang_similarity.py record manuscript/ \
  --report-file reviews/wanfang-official-report.pdf \
  --report-id "REPORT_ID_FROM_WANFANG" \
  --checked-at YYYY-MM-DD \
  --overall-similarity 0 \
  --reviewer "REVIEWER_NAME" \
  --verification-url "https://truth.wanfangdata.com.cn/" \
  --verification-evidence "Report number and document title matched." \
  --output reviews/wanfang-evidence.json

python scripts/check_wanfang_similarity.py verify manuscript/ \
  --evidence reviews/wanfang-evidence.json
```

The official Detection Service API is contract-gated and does not publish a request schema. This repository does not reverse-engineer it; direct submission automation can be added after an institution or publisher supplies the API contract and credentials.

## Shared utility tasks

Rewrite an existing proposal:

```text
Use $writting-skill to restructure this proposal. Preserve every fact,
technical term, caveat, and link, but make the decision and tradeoffs easier to find.
```

Run an audit without changing the source:

```text
使用 $writting-skill 审阅这份报告，列出事实、论证、结构、语气和 AI 味问题，先不要改正文。
```

## Workflow

The skill:

1. identifies the reader, purpose, format, and evidence;
2. protects factual and structural invariants;
3. builds or recovers the content and argument model;
4. checks premises, inference type, scope, causality, and counterexamples;
5. applies a requested voice profile and drafts or revises in the author's voice;
6. checks accuracy, logic, structure, voice-profile fidelity, and usability;
7. runs a final AI-flavor audit;
8. reports what changed and what still needs author judgment.

See [Blog writing](references/blog-writing.md) for article structure, product reality, and publication checks. See [Book writing](references/book-writing.md) for long-form planning, context, chapter cycles, and continuity. See [AI technical book writing](references/ai-technical-book.md) for reader progression, executable artifacts, evidence, version drift, and technical review. See [Similarity gate](references/similarity-gate.md) for local duplicate detection, known-source comparison, Codex web discovery, optional unattended automation, and named dispositions. See the [Wanfang adapter](references/wanfang-similarity.md) for domestic report submission boundaries, report verification, and hash-bound evidence. See [Referencing open-source projects](references/open-source-book-sources.md) for proportional project citation and the escalated License gate for expressive reuse. See [Copyright gate](references/copyright-gate.md) for the blocking source-rights and release workflow. See [Logic and argumentation](references/logic.md) for the claim model, inference types, causal checks, fallacy audit, and genre-specific guidance. See the [voice profile registry](references/styles.md) and [紫升风格](references/style-zisheng.md) for style routing and the first profile.

## License

MIT. See [LICENSE](LICENSE) and [provenance](references/attribution.md).
