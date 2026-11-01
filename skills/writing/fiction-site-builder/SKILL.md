---
name: fiction-site-builder
description: write fiction and build the reading site end-to-end. use when the user asks to write a novel or short story (long-form novel, short-form story, write chapters, continue writing, story setup, import a manuscript, review prose, remove AI flavor), or asks for a mobile-first fiction reading site, web novel H5, work list/detail/catalog/reader pages, markdown chapters, multilingual reading sites in english/spanish/korean, or a simple fiction site for social traffic campaigns. do not use for creator dashboards, ranking systems, bookshelf platforms, or reader community features unless the user explicitly asks for those.
---

# Fiction Arbitrage Builder

## The Model

```
Profit = (viewable session RPM × pageviews/session / 1000) − Facebook CPC
          ↑ Lever 3 (L3)        ↑ Lever 2 (L2)               ↑ Lever 1 (L1)
```

This skill builds a **Facebook paid-traffic → AdSense/AdX display-ad arbitrage** business. Buy a click on Meta for $X, monetize a multi-pageview reading session for $X + margin. Every decision — what to write, which genre, what image to generate, how to lay out ads — is a revenue decision traceable back to one of the three levers above.

The skill uses **fiction** as the delivery vehicle. Why fiction specifically:
- Romance and paranormal readers have some of the highest display CPMs on the internet
- The chapter model is a natural pageview chain — each chapter = one ad-loaded page
- Emotionally-driven cliffhanger content has higher average session depth than news or listicles
- Trust pages (About, Privacy, Terms) are a standard fiction site pattern — no user friction
- Organic SEO compounds over time, scaling the business beyond paid traffic dependency

## Three Revenue Levers

| Lever | Controls | Key references |
|---|---|---|
| **L1 — FB CPC** | Cover scroll-stop CTR, tagline hook quality, ad account survival | `facebook-ads.md` · `cover-allure-elements.md` · `story-cover.md` · `cover-styles.md` · `cover-genre-playbook.md` · `meta-ads-landing-requirements.md` |
| **L2 — pageviews/session** | Chapter count, cliffhanger endings, ch1 cold-traffic hook (200-word first-screen bait) | `story-long-write.md` · `reader-ux.md` · `story-review.md` · `story-deslop.md` |
| **L3 — viewable RPM** | Ad layout, placement depth, LCP < 2.5s, full-page reload on chapter nav, ad slot sizing | `adsense-arbitrage.md` · `performance.md` |

Ad density cap: ~3–4 units per 1,000 words, ad area ≤ 30% of content area. See `adsense-arbitrage.md` for the full arbitrage model.

---

## Operating Principles

- **Every chapter must end on a cliffhanger.** This is not a style preference — it is the mechanism that makes the next pageview happen. A chapter that resolves cleanly ends the session. See `story-long-write.md`.
- **Suspense is not a Chapter 1-only rule.** Every scene, every chapter opening, and every hook-out should leave one meaningful question unanswered. Chapter 1 gets the strongest cold-traffic bait, but later chapters still need tension, withheld information, and forward pull.
- **Ensemble causality is mandatory.** Long-form books use 6–8 active named characters, at least 4 recurring plot actors, three interacting storylines, and no more than 30% lead-only chapters. Supporting characters must pursue goals and change the leads' options; names and passive confidants do not count.
- **Escalation must change the situation.** Every 2–3 chapters produces an irreversible consequence and every 5–6 chapters a major reversal. A withheld answer or interrupted conversation is a hook-out technique, not a substitute for plot movement.
- **Plot volatility and relationship complexity are defaults.** Long-form fiction should feel tortuous and eventful: alliances shift, secrets collide, apparent victories create larger costs, and personal relationships interfere with external goals. Do not write a smooth two-lead progression with decorative side characters. Every major turn should alter at least two relationships or force one character to choose between conflicting loyalties.
- **Long-form novels must exceed 200 chapters.** A publishable novel must contain at least 201 chapter files. Short-form stories remain the only exception; never pad a short story into a novel to satisfy this threshold.
- **Do not make everything romance.** Treat `romance` as a primary genre only when the love relationship is the story's main conflict and resolution engine. Kidnapping, mafia, bullying, revenge, crime, legal, horror, thriller, dark academia, family, medical, fantasy, and sci-fi premises keep their own primary taxonomy when those external conflicts drive the plot; a relationship subplot does not justify adding `Romance` to the book genres, collection name, route slug, SEO keyword, article title, cover label, or promotional copy. For multi-book batches and collection pages, deliberately mix primary genres and audit reader-facing copy for unnecessary `romance` repetition before build.
- **The cover is an ad creative first, a book cover second.** Design and generate to stop the scroll in 0.3 seconds. For traffic fiction, default to a **normally exposed, high-readability melodramatic short-drama thumbnail**: a frozen scandal, an active accusation or interruption, visible proof, exaggerated shock/panic/guilt/fury, and a complicated 3–4-person relationship tableau. Use no more than 4 discernible people. Ban `premium`, `prestige`, `editorial`, `elegant`, `sophisticated`, `subtle emotion`, `restrained expression`, `calm power`, and atmosphere-first movie-poster direction from traffic-cover prompts unless the user explicitly requests that aesthetic. Neutral model poses, everyone looking away, beautiful couple portraits, romantic embraces, and polished family groups are hard failures. See `story-cover.md`, `cover-allure-elements.md`, and `facebook-ads.md`.
- **Avoid exposure extremes.** Dangerous subject matter does not prescribe a dark palette, and a bright palette must not become blown highlights, white fog, washed-out skin, or a near-opaque pale lower third. Default to mid-key exposure with natural skin tones, readable shadow detail, controlled highlights, and local contrast. Follow any user-specified palette first; white, ivory, silver, pale blue, daylight, and other bright palettes are valid. Preserve a supplied reference image's luminance and whitespace as first-class composition features. Apply the exposure gates in `story-cover.md` before accepting any cover.
- **Landing page = Chapter 1, not the homepage.** Facebook ads link directly to ch1. The ch1 hook is the first pageview; if it doesn't grab in 200 words, the session ends at 1.
- **The chapter page is the product.** Every other page is a path to it.
- **Mobile first — not mobile only.** Social traffic is 90% mobile. 390px must work perfectly; desktop must still get a purposeful layout.
- Prefer the simplest tech choice that meets the brief. Complexity needs a reason.
- Fixed good typography beats user-adjustable bad typography.
- Content language determines layout, font, and line-flow decisions.
- **Writing language is a first-class routing decision.** Before A1, select exactly one prose profile: `references/writing-english-fiction.md` for English chapters or `references/writing-chinese-fiction.md` for Chinese chapters. Do not draft in one profile and translate into the other, do not apply Chinese serial defaults to English prose, and do not treat either profile as a mere localization pass. Shared plot engineering (causality, ensemble action, evidence, reversals, and hook-outs) remains shared; prose rhythm, scene density, emotional expression, chapter packaging, and copy QA are language-specific. Other languages require their own guide or an explicit user-provided brief; never silently fall back to the English profile.
- Realistic content only. Never ship placeholder text to readers.
- Load only the references needed for the current task phase.

---

## Content-to-Site Promise

This skill delivers a Next.js-blog-style experience:

1. Novel files live in `content/` inside the Next.js project root.
2. `next dev` / `next build` picks them up automatically — no scripts, no JSON generation.
3. Adding a new book = create `content/{book-title}/chapters/` and write chapters. Rebuild. Done.

All writing phase outputs MUST be saved to the correct path under `content/` from the project root. `@content-collections` reads `content/` at build time and generates typed collections automatically.

---

## Build Pipeline

All work starts with Phase 0. After that, Track A (content, serves L1 + L2) and Track B (site, serves L2 + L3) run in parallel.

### Phase 0 — Infra Setup

Reference: `references/story-setup.md`
Output: directory structure, naming conventions, GitHub private repo, submodule registration. Skip if the project directory already exists.

**`.npmrc` — MANDATORY first file (create before `pnpm install`):**

The dev machine uses a corporate npm registry. Without `.npmrc`, `pnpm install` bakes internal tarball URLs into `pnpm-lock.yaml` — Vercel CI cannot reach them and the build fails with `ERR_SOCKET_TIMEOUT`.

```bash
echo "registry=https://registry.npmjs.org" > .npmrc
```

If the site already exists and `pnpm-lock.yaml` contains `registry.corp.example` URLs, fix it:

```bash
echo "registry=https://registry.npmjs.org" > .npmrc
rm pnpm-lock.yaml
pnpm install --registry https://registry.npmjs.org
# Verify that lockfile tarball URLs are reachable from the deployment environment.
```

If internal URLs persist after reinstall: `sed -i '' 's|https://registry.corp.example/|https://registry.npmjs.org/|g' pnpm-lock.yaml`

Commit both `.npmrc` and the updated `pnpm-lock.yaml`.

**GitHub + Submodule setup (run once per new site):**

```bash
# 1. Initial commit inside the new site directory
git add -A && git commit -m "feat: initial commit"

# 2. Create private GitHub repo and push (account: zisheng-ai)
gh repo create zisheng-ai/{site-name} --private --source=. --remote=origin --push

# 3. Register as submodule in the fictions parent repo
git -C <parent-workspace> submodule add --force \
  https://github.com/zisheng-ai/{site-name}.git {site-name}

# 4. Commit the submodule entry in the parent repo
git -C <parent-workspace> add .gitmodules {site-name}
git -C <parent-workspace> commit -m "feat: add {site-name} as submodule"
git -C <parent-workspace> push
```

Replace `{site-name}` with the actual project directory name (kebab-case). Skip this block if the site already has a remote configured.

---

### Track A — Content (L1 + L2)

Starts after Phase 0. Runs in parallel with Track B.

| Phase | Name | Lever | Reference | Output |
| --- | --- | --- | --- | --- |
| A0 | Demand Validation | L1 + L2 | `fiction-niche-researcher.md` | `outputs/{site-slug}/{book-slug}/niche-research.json` |
| A1 | Session-Depth Writing | L2 | see modes below + `facebook-ads.md` (taglines & hook copy) | chapters, outline, world, tracking |
| A2 | Ad Creative | L1 | `story-cover.md` + `cover-styles.md` + `facebook-ads.md` | `public/covers/{book-title}.webp` + `public/covers/{book-title}.json` |
| A2.5 | Scroll-Depth Anchors | L3 | `story-illustrations.md` + `cover-allure-elements.md` | `public/illustrations/{book-slug}/ch-{NNN}.webp` (exactly 5 per book) |
| A3 | Bounce-Rate Reduction | L2 | `story-review.md` + `story-deslop.md` | full-manuscript deslop completed and recorded |
| A3.5 | Opening Conversion Gate | L2 | `story-long-write.md` + `story-review.md` | Chapters 1–3 pass conversion QA in `tracking/quality-gates.md` |

A0 runs once per book (not once per site). Required for each new book unless the user has explicitly stated the genre, tropes, and premise. A0's `differentiation_angle` and `competitive_brief` feed directly into A1's story brief.

**A1 modes — pick exactly one per session:**

- **Long-form:** `references/story-long-write.md` + the selected writing-language profile → `chapters/ch-NNN-{title}.md` + `tracking/`
- **Short-form:** `references/story-short-write.md` → `prose.md`, `setup.md`, `beat-outline.md`
- **Import:** `references/story-import.md` → split chapters, reconstructed `world/`, `outline/`, `tracking/`

**A2.5 rules:**
- **Default: skip illustrations.** Do not generate chapter illustrations in full pipeline runs, new-book runs, site builds, refreshes, or traffic-creative updates.
- A2.5 runs only when the user explicitly asks for illustrations in the current turn ("Add illustrations" / "Generate illustrations" / "生成插图"). Do not infer it from "full pipeline", "build the site", "rewrite creatives", or "improve prompts".
- Never on short-form stories (no chapter files to illustrate).
- If explicitly requested, romance illustrations use T3 or T4, randomly assigned per illustration. Never T1, T2, or T5 for romance. Non-romance books follow the genre routing in `story-illustrations.md` instead of the allure-tier system.
- If explicitly requested, generate at most 5 illustrations per book, placed at the highest-stakes peaks (see `story-illustrations.md` for slot distribution). Never exceed 5 — cost constraint.
- A2.5 is not a Pre-Launch Gate. A site can launch with zero illustrations.

A3 runs automatically after A1 completes for every long-form book. Do not skip or prompt — full-manuscript deslop is a required quality pass, not optional. Record the completed chapter range and Gate A–G result in `tracking/quality-gates.md`. Skip only for short-form stories or on explicit user opt-out.

A3.5 runs automatically after A3 for every long-form book. Re-read the post-deslop versions of Chapters 1–3 and apply the conversion gate in `story-long-write.md`; do not rely on the outline, an earlier draft, or a generic review statement. Any failing chapter must be structurally rewritten, deslop-checked again, and re-audited until it passes. A cover, article, build, commit, or publication does not prove this gate. The auditable proof is a dated PASS record in `tracking/quality-gates.md`.

| A4 | Traffic Articles | L1 | `seo.md` § 15 | `articles/{slug}.md` + `public/covers/articles/{slug}.webp` |

A4 runs automatically after A3.5 for every new long-form book. Do not skip or prompt — every new book needs a traffic article. Skip only for short-form stories or on explicit user opt-out.

**A4 routing — run on every new book:**

1. Identify the new book's primary genre keyword (from A0 `niche-research.json` or the book's `target` field in frontmatter).
   - Use the actual plot engine, not a relationship subplot. Do not append `romance` by default to genre keywords, article slugs, titles, or targets.
2. Check existing articles in `articles/`: is there already a SEO list article targeting this genre keyword?
   - **Yes → update**: rewrite the article's opening section and move the new book to `books[0]`. Keep existing books as `books[1–n]`. Regenerate the article cover only if the visual concept has changed substantially. Commit the updated file.
   - **No → create**: write a new SEO list article with the new book as `books[0]` and 2–3 existing same-genre books as `books[1–n]`. Generate a new article cover.
3. Additionally, if the book's premise or hook is strong enough for social traffic, also write a short-form traffic article (引流短篇) targeting the same book. Use judgment — not every book needs one.

See `seo.md` § 15.0 for the full article-book relationship model.

**A4 modes — pick one per article:**

- **SEO list article (default):** `1200–1800` words, keyword-targeted title, prose-style book list, no `cta_url` field, ends with plain-text CTA. New book is always `books[0]`. See `seo.md` § 15.1.
- **Short-form traffic article (引流短篇):** `300–500` words, hook-driven title in 2-sentence format, 2–3 books each getting one punchy premise-pitch section separated by `---`, inline CTA links to specific `/book/{slug}` (not external homepage). See `seo.md` § 15.2.

After writing, generate article cover: landscape `1280×720` GPT Image 2, stored at `public/covers/articles/{slug}.webp`. Add `cover: /covers/articles/{slug}.webp` to frontmatter. Ensure `/articles` is linked from the homepage/footer navigation and any shared footer nav before committing. Run deslop Gates A/B/C/G + Article Quick Checks on both article types before committing.

A4 also runs as a standalone step when the user requests articles directly ("write articles", "引流文章", "SEO article", "short-form article").

---

### Track B — Site (L2 + L3)

Starts after Phase 0. Runs in parallel with Track A.

**Before starting B1, read the reference site that matches this site's ad network:**

| Ad network | Reference site | Path |
|---|---|---|
| configured AdX | velvet-throne | `<parent-workspace>/velvet-throne/` |
| configured AdSense | midnight-fable | `<parent-workspace>/midnight-fable/` |
| none / unknown | velvet-throne | `<parent-workspace>/velvet-throne/` |

Read at minimum: `next.config.ts`, `vercel.json`, `src/app/layout.tsx` (non-ad parts). Copy config structure and patterns verbatim — this avoids stale config and Next.js export drift. **Dependency versions should always be the latest** — do not copy pinned versions from `package.json`; run `pnpm add` with no version pin to get the newest release. Ad components (`AdSlot` / `AdsenseSlot`) are defined in `references/adsense-arbitrage.md` and should not be copied from the reference site.

| Phase | Name | Lever | Reference | Output |
| --- | --- | --- | --- | --- |
| B1 | Stack | — | `tech-stack.md` | chosen stack with one-line rationale |
| B2 | Design Identity | — | `design-system.md` | tone, palette, type system, `public/logo-light.png`, `public/logo-dark.png`, `public/favicon-32x32.png` |
| B3 | Data Layer | — | `data-contract.md` | content-collections schema |
| B4 | Monetization Build | L1 compliance + L2 + L3 | `ui-components.md` + `reader-ux.md` + `adsense-arbitrage.md` + `seo.md` + `meta-ads-landing-requirements.md` | working site with ad slots, FB Pixel, trust pages, sitemap |
| B5 | RPM Optimization | L3 | `performance.md` + `adsense-arbitrage.md` | Core Web Vitals targets met, ad CLS/lazy-load tuned |
| B6 | Arbitrage Readiness QA | all | `qa-checklist.md` + `lighthouse-qa.md` | Lighthouse scores meet thresholds, monetization gates pass |

B1 → B2 → B3 → B4 are sequential. B5 and B6 run in parallel against the same build — run `pnpm run build` once, then check both.

**B4 gate:** at least one book with ≥ 10 chapters must exist before starting B4. B1–B3 may run while writing is still in progress.

### B4 — Domain (optional)

During B4, check the parent project `fictions/AGENTS.md` site table for the domain assigned to this site.

- **If domain is specified**: use it in `metadataBase`, `sitemap.ts`, and `src/lib/site.ts`.
- **If no domain is specified**: set `metadataBase: new URL('https://PLACEHOLDER.example.com')` and record a TODO:
  ```
  - [ ] 配置正式域名（当前 metadataBase 为占位地址，需在 layout.tsx / src/lib/site.ts / sitemap.ts 同步更新）
  ```

### B4 — Google Ads (optional)

During B4, check the parent project `fictions/AGENTS.md` site table for the ad account assigned to this site (either configured AdX or configured AdSense).

- **If an ad account is specified**: wire up the full ad stack — GPT/AdSense script in `<head>`, `AdSlot` / `AdsenseSlot` components in pages, and follow `references/adsense-arbitrage.md` for slot placement and density rules.
- **If no ad account is specified**: skip all ad code entirely — no GPT script, no AdSense script, no slot components. Record a TODO:
  ```
  - [ ] 配置广告账号（当前无广告代码，待确定账号类型后接入 AdX 或 AdSense）
  ```

Do not add placeholder ad markup or commented-out ad code — leave the pages clean.

### B4 — Facebook Pixel (optional)

During B4, check the parent project `fictions/AGENTS.md` for a `facebook_pixel.id` configuration. This step is **optional** — if the parent project does not specify a Pixel ID, skip the code change and only record it in `TODO.md`.

- **If configured**: add the Facebook Pixel base code to `src/app/layout.tsx` `<head>` using `next/script` with `strategy="afterInteractive"`. Use the exact Pixel ID from `fictions/AGENTS.md`. Also wire the `ChapterPixel` component (see `references/adsense-arbitrage.md §4.3`) into `src/app/book/[slug]/chapter/[n]/page.tsx` — this fires `ViewContent` on mount, `ScrollDepth25` / `ChapterRead50` / `ScrollDepth75` at scroll milestones, `ChapterCompleted` via IntersectionObserver on `#chapter-content-end` sentinel, and `TimeOnPage20s` / `TimeOnPage30` after 20 / 30 seconds. Both dwell events must use the same chapter-only scope, payload, name, and lifecycle. These are the L1 optimization signals for Lookalike Audience building.
  - Treat the existing browser Pixel as a production contract. A CAPI, cookie-banner, analytics-helper, or route-tracking change must not remove the stable layout bootstrap/loader, move initialization ownership into a React effect, or make browser `fbq` delivery depend on a CAPI endpoint. Preserve the current site's consent semantics unless the user explicitly scopes a consent migration. For an explicit opt-in migration, keep a stable inline loader in `layout.tsx`, gate every Meta emitter with the same stored decision, and test pre-consent, accept, reject, returning-accepted, and returning-rejected states separately.
  - Before changing an existing Pixel path, record its Pixel ID, `layout.tsx` bootstrap, any `noscript` ID, navigation model, event emitters, consent behavior, and exact custom-event names. Afterward run the regression matrix in `references/adsense-arbitrage.md §4.1.1`; a successful build or source grep alone does not prove that events fire.
  - Custom event names MUST be unprefixed and shared across sites: `ChapterRead50`, `ChapterCompleted`, `TimeOnPage30`, `NextChapterClick`, and the other established event names. Never add a directory, subdomain, or abbreviated site prefix. Keep Meta standard events (`PageView`, `ViewContent`) unprefixed too. Use page URL/domain rules or event payloads for site-level reporting under a shared Pixel.
  - Add a TODO for manual Meta Events Manager setup: create Custom Conversions / Ad Set conversion events for `ChapterRead50`, `ChapterCompleted`, `TimeOnPage30`, and `NextChapterClick`. Code can emit the events, but selecting them as optimization targets requires this manual backend setup.
  - If the site uses `next/link` or any App Router client navigation, also add a lightweight route tracker that fires `fbq('track', 'PageView')` on pathname changes after the initial render. A single bootstrap `PageView` in layout is not enough for SPA-style navigation.
- **If not configured**: do not add any Pixel code. Record in the site's `TODO.md`:
  ```
  - [ ] 配置 Facebook Pixel（项目 AGENTS.md 未指定 Pixel ID）
  - [ ] 接入 ChapterPixel 组件（ViewContent + ChapterRead50 + ChapterCompleted + TimeOnPage30 事件）
  ```

This Pixel setup is **project-level** and must not be hardcoded into the skill template.

Optional phases (load only when the brief requires):
- `references/internationalization.md` — when target language is not the build default
- `references/writing-english-fiction.md` — required for English fiction writing and English-language prose review
- `references/writing-chinese-fiction.md` — required for Simplified or Traditional Chinese fiction writing and Chinese-language prose review; pair with `internationalization.md` for `zh-TW`
- `references/product-surface.md` — when IA or URL structure needs formal documentation

---

### Parallel-safe pairs

| What | Notes |
| --- | --- |
| Track A + Track B | Both start after Phase 0; fully independent |
| Multiple books in A1 | All books run concurrently |
| Chapters within a book (A1) | Expand outline first → parallel chapters → continuity pass |
| Covers across books (A2) | Batch all books in one round, not one-at-a-time |
| Illustrations across books (A2.5) | All books in parallel — one Agent call per book |
| Illustrations within a book (A2.5) | All peak chapters (up to 5) in parallel — background processes |
| B2 + B3 | Design tokens and data schema are independent |
| B5 + B6 | Share one `pnpm run build` — do not run two concurrent builds |

### Post-Build Deliverables (required after B6)

After B6 passes, generate two files before closing the session:

**`README.md`** — site reference card for this repo, written in **Chinese (中文)**:
- 域名、语言、调性、广告账号等头部信息
- 书目表：slug、书名、章节数、插图数
- 技术栈一句话
- 开发命令（`pnpm dev`、`pnpm build`）

**`TODO.md`** — outstanding work for this site, written in **Chinese (中文)**:
- 部署状态（未部署 / 已上线 + 域名）
- 每本书的章节缺口：列出少于 201 章的长篇小说及缺多少章；短篇故事单独标记
- 缺少插图的书
- `books.ts` 里的 `chapterCount` 与实际文件数不一致的地方
- 广告和分析工具中尚未完成的项，包括：
  - Google Analytics 4 (GA4): add the `G-XXXXXXXX` tag to `layout.tsx` when the measurement ID is available.
  - Google Search Console (GSC): verify the live domain and submit `/sitemap.xml` after deployment.
  - Meta Events Manager: create Custom Conversions / Ad Set conversion events for unprefixed custom events (`ChapterRead50`, `ChapterCompleted`, `TimeOnPage30`, `NextChapterClick`).

Both files must be written in **Chinese**. If the site is a new build, start with the expected state (all chapters to write, not yet deployed). If the site is updated, reflect the current delta.

### Per-Site `AGENTS.md`

If a site directory contains an `AGENTS.md` file, read it before starting site work. It may contain project-specific conventions that override this skill's defaults (e.g., a non-standard Next.js version or local build rules). Treat its instructions as site-specific addenda to `SKILL.md`.

### Pre-Launch Gate (Arbitrage Readiness)

All of the following must be true before go-live (after B6 passes):

| Check | Required location |
| --- | --- |
| ≥ 3 book directories | `content/{book-title}/` |
| Each long-form book has **at least 201 chapters**; chapter counts do not need to be unique across books within the same site | `content/{book-title}/chapters/` |
| Each chapter meets its type target (see Pacing Guidelines in `story-long-write.md`); word counts must vary naturally across chapters — never identical | A1 output |
| `outline/outline.md` exists and non-empty | A1 output |
| `world/worldbuilding.md` exists and non-empty | A1 output |
| `tracking/context.md` exists | A1 output |
| 6–8 active named characters; ≥ 4 recurring plot actors | `world/worldbuilding.md` + outline cast fields |
| Three interacting storylines with goals, opposition, midpoint reversals, and endgame consequences | `world/worldbuilding.md` `Storyline Matrix` + `outline/outline.md` |
| Lead-only chapters ≤ 30%; ensemble and supporting-character action cadence pass | `outline/outline.md` cast/conflict fields + A3 review |
| Cover image for every book (L1 gate) | `public/covers/{book-title}.webp` |
| Ad slots wired and sized (L3 gate) | `src/app/book/[slug]/chapter/[n]/page.tsx` |
| Built Chapter 1, ordinary chapter, and final chapter each contain one q4/q1/q2/q3/q5 element in that DOM order | generated production HTML |
| FB Pixel base code + ChapterPixel (L1 gate) | `src/app/layout.tsx` + chapter page |
| Trust pages present and footer-linked (account survival) | `/privacy`, `/terms`, `/about`, `/contact` |

If any book is missing a cover at launch time, run A2 immediately — do not prompt the user.

If a full pipeline run reaches launch with no illustrations generated for its long-form books, do not run A2.5 unless the user explicitly requested illustrations in the current turn.

### Scope-to-phase mapping

| User intent | Phases to run |
| --- | --- |
| "Write a novel" / "Continue writing" / `/story-long-write` | 0 (skip if exists), A1 long-form, **A3 (automatic)**, **A3.5 (automatic)**, **A4 (automatic)** |
| "Write a short story" / `/story-short-write` | 0 (skip if exists), A1 short-form (A3 skipped, A4 skipped for short-form) |
| "Add one book to existing site" | A1 long-form (single book), A2 (single book), **A3**, **A3.5**, **A4 (automatic — update or create article)** |
| "Generate covers" / `/story-cover` | A2 only |
| "Add illustrations" / "Generate illustrations" | A2.5 only |
| "Import manuscript" / `/story-import` | A1 import only |
| "Review prose" / `/story-review` | A3; include A3.5 when Chapters 1–3 are in scope |
| "Build the site" / full pipeline | 0 → Track A + Track B in parallel; **A2.5 is skipped by default** |

**Book count default — 3 for initial site generation.** When building a new site from scratch, generate exactly **3 books** unless the user explicitly specifies a different count. For new sites: run A0 for all 3 in parallel, then A1 for all 3 in parallel. For existing sites, honor the user's requested count; if unspecified, add one book. Never exceed 5 books in a single session unless the user explicitly requests a larger batch. Select each book from validated demand, but maintain useful primary-genre variety across the batch. Never collapse distinct crime, thriller, horror, bullying, legal, family, medical, fantasy, or sci-fi premises into `romance` merely because they contain attraction or a couple.

For review and redesign tasks, start at the relevant phase and load only the references covering the failing areas.

---

## Environment Prerequisites

This skill works in Claude Code and Codex-style coding agents. Before doing anything else, verify that shell command execution and file editing are available:

```bash
echo "fiction-site-builder-ok"
```

If shell execution or file editing is unavailable, stop immediately and output:
```
ERROR: fiction-site-builder requires a coding-agent session with shell and file-edit access.
```

Read project instructions before site work:
- **Codex:** read `AGENTS.md` in the repo and target site directory if present.
- **Claude Code:** read `CLAUDE.md` in the repo and target site directory if present.
- If both exist, apply both; site-level instructions override repo-level defaults.

In Codex, follow the active sandbox and approval rules from `AGENTS.md`. If it says build commands or HTTP traffic must run outside the sandbox, request approval before running `pnpm build`, `next build`, `curl`, or equivalent verification commands.

**Cover image generation (A2):** Calls `https://api.apiyi.com/v1/images/generations` via curl. **Model cascade depends on allure tier** (see `story-cover.md` §Model capability ranking): T1/T2 → `gpt-image-2-all` (primary, hyperrealistic editorial photo quality) → `gpt-image-2-all` (retry) → `doubao-seedream-5-0-260128` → `nano-banana-pro`. T3/T4 → `doubao-seedream-5-0-260128` (primary, GPT hard-rejects fabric-failure/torn/soaked language) → `doubao-seedream-5-0-260128` (retry) → `nano-banana-pro`. Requires `APIYI_API_KEY` in the environment. **No SVG fallback** — if the key is not set, cover generation is skipped (warning + continue), and the slot is filled in a later pass. All covers in a batch are generated **in parallel**.

```bash
[ -n "$APIYI_API_KEY" ] && echo "apiyi path" || echo "skip (no SVG fallback)"
```

**Logo and favicon (B2):** Same `APIYI_API_KEY` check as A2. If set, generates PNG assets via `doubao-seedream-5-0-260128` → `gpt-image-2-all` fallback; if not set, yellow warning + **skip** (no SVG fallback). Do **not** use `nano-banana-pro` for logo/favicon.

Generate **three assets in parallel**:
- `public/logo-light.png` — square icon (no text, no wordmark) for light backgrounds, generate at 1920×1920 then resize to 512×512
- `public/logo-dark.png` — square icon (no text, no wordmark) for dark backgrounds, generate at 1920×1920 then resize to 512×512
- `public/favicon-32x32.png` — same icon style, works on any background, generate at 1024×1024 then resize to 256×256

**After generation, compress all three with pngquant** (quality 80–95, speed 1):
```bash
sips -z 512 512 public/logo-light.png --out public/logo-light.png
sips -z 512 512 public/logo-dark.png  --out public/logo-dark.png
sips -z 256 256 public/favicon-32x32.png --out public/favicon-32x32.png
pngquant --force --quality=80-95 --speed 1 --output public/logo-light.png public/logo-light.png
pngquant --force --quality=80-95 --speed 1 --output public/logo-dark.png  public/logo-dark.png
pngquant --force --quality=80-95 --speed 1 --output public/favicon-32x32.png public/favicon-32x32.png
```

Target sizes after compression: logo ≤ 100 KB, favicon ≤ 25 KB. Sites use static export (`output: 'export'`) so `next/image` optimization is unavailable — pre-compression is mandatory.

After generating the assets, add the following CSS to `src/app/globals.css` (theme switching, no JS required):
```css
/* Logo theme switching */
.logo-dark { display: none; }
[data-theme$="-dark"] .logo-light { display: none; }
[data-theme$="-dark"] .logo-dark { display: block; }
```

Create `src/components/SiteLogo.tsx`:
```tsx
export function SiteLogo({ className, alt }: { className?: string; alt?: string }) {
  const a = alt ?? 'SITE_NAME'
  return (
    <>
      <img src="/logo-light.png" alt={a} className={`logo-light${className ? ' ' + className : ''}`} />
      <img src="/logo-dark.png" alt={a} className={`logo-dark${className ? ' ' + className : ''}`} />
    </>
  )
}
```

Replace all `<img src="/logo.png" ...>` (and `<Image src="/logo.png" ...>`) in rendered UI with `<SiteLogo className="..." />`. Use `logo-light.png` as the homepage OG fallback image unless the project explicitly creates a separate social image. Remove any `filter: brightness(0) invert(1)` or similar filter hacks that were compensating for a single-logo approach.

---

## Phase Execution Protocol

Execute phases one at a time. Track progress with the best mechanism available in the current environment:

**If `TaskCreate` / `TaskUpdate` are available** (Claude Code): use them. Create tasks only for the phases that will actually run in this session. Do not create tasks for phases outside the current scope. Flip a task to `in_progress` when entering that phase and `completed` when done. Use `TaskGet` on re-entry to restore state.

**Phase naming convention:**
- Full pipeline: use phase IDs in task titles, e.g. "A2: Ad Creative", "B4: Monetization Build".
- Single-function triggers (`/story-cover`, `/story-import`, `/story-review`, etc.): use descriptive titles — "Cover Generation", "Manuscript Import", "Prose Review".

**If those tools are not available** (other agents / API): print a compact text progress block only when a phase runs.

**Orchestration — use `Agent` for all delegation:**

Use the `Agent` tool for every delegation task, whether single or parallel. To run tasks concurrently, send multiple `Agent` tool calls in a single response — the runtime executes them in parallel automatically. Do not use `Workflow`.

| Situation | Use |
| --- | --- |
| Single chapter rewrite, single cover retry | One `Agent` call |
| A1 — multiple books in parallel | Multiple `Agent` calls in one response, one per book |
| A1 — chapters within a book | Expand outline first → multiple `Agent` calls in one response (one per chapter) → continuity pass |
| A2 — cover batch across all books | Multiple `Agent` calls in one response, one per book |
| A2.5 — illustrations across all books | Only if explicitly requested; multiple `Agent` calls in one response, one per book |
| Track A + Track B launched together | Two `Agent` calls in one response |
| B5 + B6 against the same build | Two `Agent` calls in one response |

**Model selection:**

**If the `Agent` tool is available** (Claude Code — guaranteed by the prerequisite check above): delegate all chapter writing. Never write fiction content directly in the main context. Never prompt the user to switch models manually.

**If the `Agent` tool is not available**: write chapters sequentially in the main context. Skip parallel multi-book and multi-chapter spawning; write one chapter at a time following the Single Chapter Writing Process in `story-long-write.md`. Note: this is a degraded mode — quality and speed are both reduced.

Track B phases carry no model override and inherit the session model regardless.

**Rules (apply in both modes):**
- **Within a phase: act autonomously.** Invoke all required tools (image generation, file writes, bash commands) without asking the user. Never surface a "please run X" prompt mid-phase — just do it.
- **Between phases: summarize and continue.** At each phase boundary, print a one-line summary of what was produced and move to the next phase. Do not wait for user confirmation unless the user explicitly says to pause.
- Parallel-safe phases may be executed in the same turn — announce both at the start and summarize both at the end.
- Sequential phases run back-to-back without pausing for confirmation.
- Load each phase's reference file only when entering that phase.
- If a phase is skipped, mark it done with a note explaining why, then continue.
- On re-entry, restore or reprint current state before proceeding.

---

## Reference Loading

Load references only when entering that phase. Do not preload all references at the start.

### L1 — Traffic Cost references

- **`facebook-ads.md`** — load during A1 for all tagline and hook copy writing (punchy 8-word opener, setup→reversal→unresolved tension, 25–40 words, final line always unresolved); during A2 for cover direction; during B4 for Pixel optimization event strategy. Do not load for pure chapter prose writing.
- **`cover-allure-elements.md`** — allure vocabulary and tier system (T1–T5): fabric ranking, face/hair/body tables, poses, exposure tiers. Load during A2 and A2.5.
- **`cover-genre-playbook.md`** — 15 genre-specific prompt templates (romance, Paranormal, Vampire, Fae, Mafia, Contemporary, Sports, Accidental Marriage, Revenge, Romantasy, Regression, Villainess, Monster, Dark Academia, Urban Paranormal). Load during A2 only — not needed for A2.5.
- **`story-cover.md`** — cover generation pipeline via apiyi cascade (T1/T2 → gpt-image-2-all; T3/T4 → doubao-seedream); all covers in parallel; no SVG fallback. Load during A2.
- **`cover-styles.md`** — genre-specific cover composition templates and visual style references. Load during A2.
- **`japan-market-visual-direction.md`** — Japanese-market casting and face-direction rules for female leads, male leads, and second male/rival roles. Load during A2 when the target locale is `ja-JP` or Japanese face references are supplied.
- **`meta-ads-landing-requirements.md`** — Meta/Facebook ad traffic landing page policy, account-survival rules, cloaking prohibition, trust pages (About/Privacy/Terms/Contact requirements), Pixel+CAPI architecture, B4 compliance checklist. Load during B4.

### L2 — Session Depth references

- **`story-long-write.md`** — long-form chapter writing pipeline, context handoff, pacing guidelines, mandatory cliffhanger techniques, scene-level suspense rules, chapter 1 cold-traffic hook structure (200-word beat checkpoints, line-1 bans, backstory cap). Load at A1 long-form.
- **Writing language profiles** — before writing a chapter, load exactly one: `writing-english-fiction.md` for English, or `writing-chinese-fiction.md` for Chinese. The language profile governs sentence rhythm, exposition compression, dialogue/subtext, emotional escalation, chapter titles, synopses, and language-specific review checks. It supplements rather than replaces the selected genre guide. Do not use one profile to judge the other.
- **Pressure-genre guides** — when the external conflict below is a primary story engine, load its dedicated guide alongside `story-long-write.md` and the broad genre file. These guides define the power system, evidence chain, escalation architecture, public reversal, safety boundaries, and genre-specific QA:

  | Story engine | Reference |
  |---|---|
  | Family abuse, illegitimacy, inheritance theft | `genre-family-abuse.md` |
  | Workplace persecution and industry blacklisting | `genre-workplace-persecution.md` |
  | Marital control, forced marriage, replacement bride | `genre-marital-control.md` |
  | Adult campus power and elite bullying | `genre-campus-power.md` |
  | Medical conspiracy, switched infants, false confinement | `genre-medical-conspiracy.md` |
  | Cult control and closed-community escape | `genre-cult-control.md` |
  | Wealthy-family captivity and erased identity | `genre-family-captivity.md` |
  | Trafficking, illegal adoption, stolen identity networks | `genre-trafficking-illegal-adoption.md` |
  | Stalking, surveillance, impersonation | `genre-stalking-control.md` |
  | Gang debt, hostage families, criminal succession | `genre-gang-debt.md` |
  | Wrongful conviction and corrupt justice | `genre-wrongful-conviction.md` |
  | Digital blackmail, deepfakes, networked humiliation | `genre-digital-blackmail.md` |
  | Entertainment-industry coercion and contract blacklisting | `genre-entertainment-coercion.md` |
  | Sports bullying, doping frames, match corruption | `genre-sports-bullying.md` |
  | Military and private-security control | `genre-military-security-control.md` |
  | Survival games and human hunts | `genre-survival-game.md` |
  | Small-town dynasties and covered disappearances | `genre-small-town-corruption.md` |
  | Revenge judgment and public reckoning | `genre-revenge-judgment.md` |
  | Taiwan `zh-TW` oppression-to-reversal serial fiction, including engagement frames, substitutes, secret children, traded brides, and ancestor awakening | `genre-taiwan-serial-fiction.md` |

  If two guides apply, designate one as the primary plot engine and use the second only for its relevant subsystem. Do not merge multiple guides into a premise that lacks a single clear victory condition.
- **`story-short-write.md`** — short-form story pipeline, emotion-first structure. Load at A1 short-form.
- **`story-import.md`** — import and split an existing manuscript into project structure. Load at A1 import.
- **`story-review.md`** — multi-perspective structural and prose review. Load at A3.
- **`story-deslop.md`** — unified deslop framework covering fiction chapters (full 7 Gates + Three-Pass) and non-fiction copy (articles, taglines, synopses, meta descriptions — run Gates A/B/C/G + Article Quick Checks). Incorporates stop-slop (hardikpandya/stop-slop) rules merged into the Gate structure. Load at A3 for fiction; load when writing or reviewing any `articles/`, taglines, synopses, or site copy. AI prose increases bounce rate; deslopping is a revenue pass, not a style pass.
- **`reader-ux.md`** — chapter page UX requirements: next-chapter CTA height/color, TOC, no Previous button, dark mode, resume-last-chapter via localStorage. Load during B4. These are session-depth mechanics, not aesthetic preferences.

### L3 — Monetization Rate references

- **`adsense-arbitrage.md`** — **primary reference**: covers the full profit model, account-survival compliance (§1), session-depth mechanics (§2), ad layout and placement map (§3), Facebook tracking and Pixel events (§4), trust pages (§5), KPIs (§6), build checklist (§7), implementation patterns including full AdSlot / AdsenseSlot / StickyNav / ChapterPixel TSX (§8). Load whenever building, laying out ads, directing covers, or wiring Facebook tracking.
- **`performance.md`** — Core Web Vitals, loading strategy, image optimization. LCP < 2.5s is an L3 requirement — slow load kills active-view time and CPM. Load during B5.

### Cross-cutting references

- **`fiction-niche-researcher.md`** — A0 demand validation and competitive analysis; outputs `niche-research.json` that feeds A1 story brief and A2 cover direction. Includes Taiwan / `zh-TW` niche routing and a US/UK women 25–60 portfolio covering restart comedy, silver-sleuth cozy, women’s reinvention, Romantasy, psychological suspense, supernatural bonds, and power-reversal fiction without default romance labeling.
- **`seo.md`** — load during A0 for keyword demand validation; during A1 when writing book synopses (meta descriptions). Organic traffic scales the business beyond paid dependency. Includes Taiwan / Traditional Chinese book-list article patterns.
- **`geo.md`** — load during A0 and A1: book synopses as self-contained relational sentences (GEO evidence); author pen-name entity strategy. Load during B4: `llms.txt` generation, structured data, AI crawler robots.
- **`tech-stack.md`** — choose the implementation stack before writing any code (B1).
- **`design-system.md`** — design identity, typography, palette, logo/favicon generation (B2).
- **`data-contract.md`** — data models and `@content-collections` setup (B3).
- **`ui-components.md`** — visual and component quality floor during build (B4).
- **`qa-checklist.md`** — final automated QA and screenshot verification (B6; failures only).
- **`lighthouse-qa.md`** — Lighthouse performance/accessibility/SEO thresholds and runbook (B6).
- **`vercel-operations.md`** — Vercel project setup, custom domains, cache headers, deploy hooks, `output: export` pitfalls. Load when deploying or configuring hosting.
- **`product-surface.md`** — IA and URL structure (optional, load when needed).
- **`internationalization.md`** — language and font decisions for non-default target language (optional, load when needed). Required for `zh-TW` sites to apply Taiwan Traditional Chinese wording, UI labels, and article-hub rules.

---

## Quality Gates (Arbitrage Readiness)

Do not deliver a build if any of these are true.

**Monetization & account survival (highest priority — failing these ends the business):**
- Any cover, hero image, or imagery is outright explicit / pornographic — exposed genitals or nipples, sex acts, graphic nudity. Suggestive allure is fine; only hardcore content gets the ad account banned and AdSense disabled.
- Privacy Policy, Terms, About, or Contact page is missing or not footer-linked (AdSense approval + FB quality requirement).
- No cookie-consent / Google-certified CMP wired.
- An ad slot has no reserved size (causes CLS), or the above-the-fold ad is lazy-loaded (kills L3 viewability score).
- Ad density exceeds ~3–4 units / 1,000 words, or ad area exceeds ~30% of content area on any screen.
- An ad is visually/spatially mistakable for the Next/TOC control, or any layout encourages ad clicks.
- Chapter navigation is SPA (does not full-reload), so ads do not reinitialize and pageviews/impressions are undercounted — an L3 failure.
- A live site's Pixel initialization or consent semantics were changed without browser verification; `PageView` is missing or duplicated on a hard load; `ViewContent` is absent after tracking becomes active; or two owners send the same `PageView`. In an opt-in design, the consent handler may own the first `PageView` only when the layout intentionally withheld it before consent.

**Content completeness (L2 depth gates):**
- Any new long-form book lacks `tracking/quality-gates.md`, has an incomplete A3 deslop record, or has anything other than a final post-deslop PASS for the Chapters 1–3 conversion gate.
- Chapter 1 fails to create conflict or abnormality in its first sentence, overturn the protagonist's normal situation within the first 500 words, or end on a high-risk choice or cognition-changing clue.
- Chapter 1's middle asks a cold reader to retain more than 2 new names, institutions, document types, or specialized legal/commercial/medical concepts in any 200-word window; or explains a system fact without making a character act on it within the next 2 paragraphs.
- Chapter 2 resets or explains Chapter 1 instead of imposing a new material cost, choice, deadline, exposure, or loss within its first 500 words.
- By the end of Chapter 3, the opening crisis has not produced an irreversible consequence and a harder forward plan.
- Site launches with fewer than 3 books.
- Any long-form book has fewer than 201 chapters. Short-form stories are exempt and must be explicitly classified.
- Any chapter falls below its type's minimum (see Pacing Guidelines in `story-long-write.md`).
- All chapters in a book have the same word count — natural variation is required.
- `outline/outline.md` is missing or empty for any published book.
- `world/worldbuilding.md` is missing or empty for any published book.
- `world/worldbuilding.md` lacks a Supporting Cast, Relationship Web, or three-line Storyline Matrix.
- A book has fewer than 6 active named characters, fewer than 4 recurring plot actors, or uses background extras/passive confidants to satisfy the count.
- Lead-only chapters exceed 30%, any rolling 3-chapter block beginning with Chapter 2 lacks at least 2 ensemble chapters, or supporting characters never interact without the leads.
- The outline misses an irreversible consequence in any 3-chapter span or a major reversal in any 6-chapter span.
- Cover image is missing for any book in the reader at launch time. (Development preview may use CSS placeholders; final launch requires real covers.)

**Reading product (L2 UX gates):**
- Chapter content contains lorem ipsum or generic placeholder text.
- Reader background is pure white (`#fff`) or pure black (`#000`), or a tinted hue that makes the page feel pink / rosy / flashy.
- Next chapter button is missing, broken, or below 60px height.
- Next button uses a muted or dark color instead of a vivid warm fill (hot pink / magenta / coral).
- A "Previous" button appears in the reader nav.
- Table of contents button is missing from the reader nav, or is unavailable on chapter 1.
- The site logo is not a home link (`/`) on any chapter page, including chapter 1.
- Chapter content fails to load or shows a blank page.

**Visual quality:**
- Loud gradients, fake glass panels, glowing orbs, or heavy drop shadows on any surface.
- Light theme `--color-base-100/200/300` tinted pink, rosy, or any vivid hue — use warm neutral tones only (ivory, linen, parchment: e.g. `#F9F7F3` / `#F0EBE3` / `#E4DDD4`).
- Body font is decorative, handwritten, or a novelty display face.
- Body text is below 17px on mobile or below 17px on desktop.
- Body text fails WCAG AA contrast (4.5:1) against the page background.
- Desktop is a stretched phone layout with no layout adaptation.

**Content and language:**
- `<html lang>` is missing or set to the wrong locale.
- Font stack does not include appropriate language fallbacks for the target language.
- Any reader-visible copy mentions AI, Markdown, parser, prompt, skill, or generation.
- Chinese chapters were drafted or reviewed with the English prose profile, or English chapters were drafted or reviewed with the Chinese prose profile. Record the selected profile in `tracking/context.md` and use its language-specific QA before marking A3 complete.

**Technical:**
- Build errors or console errors exist on page load.
- Routes do not work or data does not load.
- Any required page (home, book detail, reader) is missing.
- Initial JS bundle exceeds 200KB for a prototype.
- Cover images are not optimized (`next/image` or equivalent).
- `chapterCount` in `books.ts` does not equal the actual number of `.md` files in `content/{slug}/chapters/`. Always derive the count from the filesystem at build time or keep in sync manually — a stale value breaks chapter progress indicators and reader UX.
- `public/logo-light.png` or `public/logo-dark.png` is missing at launch time.
- Favicon is missing or is the default Next.js favicon at launch time.
- `SiteLogo` component is missing or any rendered `<img src="/logo.png">` reference remains.

---

## Non-Negotiables

- Writing internals (`outline/`, `world/`, `tracking/`, `reference/`, `resources/`, `teardowns/`) are never exposed in reader routes, reader-facing URLs, or site navigation. Build the site as if those directories do not exist.
- Reader-facing only by default: no AI labels, writing workflow panels, or "generated by" branding.
- Mobile is the primary target. Desktop must have its own layout logic — not a stretched phone screen.
- Required pages: home / book list, book detail with chapter list, chapter reader.
- Required reader controls: fixed top header with a compact TOC icon plus dark mode toggle; fixed/in-flow bottom bar with TOC (ghost) + Next → (vivid warm fill, min 60px height); no Previous button; both TOC controls hard-navigate to `/book/{slug}#toc`; resume-last-chapter via localStorage.
- Add font size control or reading progress indicator only when the brief explicitly asks for them.
- Do not add ranking, bookshelf, favorites/bookmarks, search, payment, comments, or account modules unless explicitly requested.
- Respect content language: set `lang`, use language-appropriate font stacks, handle CJK line flow.
- One deliberate visual signature per build — connected to reading, books, chapters, or genre.
- Monetized FB-traffic sites (the default): ship Privacy / Terms / About / Contact pages + cookie consent, and reserve size on every ad slot. Suggestive covers are allowed; avoid only outright explicit/pornographic imagery (see `references/cover-allure-elements.md` §0). Trust pages, ad-layout, and no-cloaking compliance still apply everywhere.

---

## Performance Baseline

Fast loading is an L3 revenue requirement for social traffic, not a UX preference.

- SSG (`generateStaticParams`) for all chapter and book routes. No runtime filesystem reads.
- Cover images: `next/image` with `priority` on above-the-fold images when covers exist; CSS placeholder when they don't.
- Chapter content: loaded per route, never bundled all-at-once.
- Prefetch next chapter at 80% scroll depth (simple `router.prefetch()` call).
- Initial JS bundle under 200KB.
- LCP target: under 2.5s on a mid-range Android device on 4G.

---

## Output Contract

```
<project>/
  README.md                     # site reference card (generated after B6)
  TODO.md                       # outstanding work (generated after B6)
  public/
    llms.txt                    # AI crawler manifest (generated during B4, see geo.md §9)
  content/                      # all writing outputs live here
    {book-title}/
      chapters/                 # ch-001-{title}.md, ch-002-{title}.md, ...
      world/                    # worldbuilding.md, characters/, map.md
      outline/                  # outline.md
      tracking/                 # context.md, threads.md, timeline.md
  src/app/
    page.tsx                    # home: book list
    book/[slug]/
      page.tsx                  # book detail: synopsis + chapter list
      chapter/[n]/
        page.tsx                # chapter reader: content + prev/next + ChapterPixel
  content-collections.ts        # collection schema definitions
  src/lib/
  src/components/
    BookCard.tsx
    ChapterNav.tsx
    ChapterPixel.tsx            # FB Pixel scroll events (L1 optimization signal)
    ThemeToggle.tsx             # DaisyUI data-theme switcher
    IllustrationBlock.tsx       # inline chapter illustration (A2.5, optional)
  public/
    covers/                     # cover images (A2) — flat: {slug}.webp per book (lossy WebP q82)
    illustrations/              # in-chapter illustrations (A2.5, optional)
      {book-slug}/
        ch-{NNN}.webp           # 0–5 per book, at peak dramatic moments (lossy WebP q78)
    logo-light.png              # logo for light mode — PNG via apiyi (B2); no SVG fallback
    logo-dark.png               # logo for dark mode — PNG via apiyi (B2); no SVG fallback
    favicon-32x32.png           # favicon (single, no light/dark) — PNG via apiyi (B2); no SVG fallback
```

Cover images (`public/covers/{slug}.webp` — flat, one file per book, lossy WebP q82) are generated in A2 via the apiyi cascade, all books in parallel. Logo and favicon follow the same pattern in B2 — PNG via apiyi (doubao → gpt-image-2-all), all three generated in parallel. **No SVG fallback** anywhere: if `APIYI_API_KEY` is unset or the cascade fails, the asset is skipped (warning + continue) and flagged for a later pass.

For a review or redesign task, the output is a findings report and patch set, not a full scaffold.

---

## Collaboration With Other Skills

The skills listed in **Merged Skills** below are already integrated — no separate installation needed. Use their capabilities directly.
