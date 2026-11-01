# Product Surface

## Default Product

Build a reader-facing fiction product. The core job is: find a work, open it, and read comfortably. Keep the product intentionally small by default.

Do not show creator tooling, AI writing workflows, prompt panels, analysis reports, "powered by" labels, or any feature that a reader would not understand or want. These are disqualifying if they appear without an explicit request.

## Required Information Architecture

A complete lightweight fiction H5 template has exactly these pages:

### Home / Work List
- Site title and optional tagline (1 line).
- Book grid or list: cover, title, author, genre tag(s), status badge, latest chapter or update date.
- "Continue reading" card at the top if reading progress exists for any book (nice-to-have but strongly recommended).
- No ranking, trending, categories, or recommendation algorithms by default.

### Book Detail
- Cover image (or CSS placeholder).
- Title, author, genre tags, status (Ongoing / Completed / Hiatus).
- Synopsis (2–5 sentences or a `<details>` expand for longer).
- Stats row: word count, chapter count, last updated.
- Primary action: "Start reading" (first chapter) or "Continue reading" (last read chapter).
- Chapter catalog below the detail — or a scrollable drawer triggered by a button.

### Chapter Catalog
- Ordered list of chapters with chapter number and title.
- Volume / arc group headers when available (bold or uppercase divider label).
- Current chapter highlighted.
- "Locked" state only if user explicitly requests a paywall UI.
- Accessible from the book detail page and from inside the reader.

### Reader
- Chapter title at the top.
- Chapter body prose.
- Progress indicator (scroll rail).
- Navigation: previous chapter, next chapter — accessible at top and bottom, or via tap zones.
- Settings trigger: font size, line height, theme.
- Catalog trigger: slide-in drawer with chapter list.
- End-of-chapter prompt: "Next: [Next Chapter Title]" with a tap/click target.

## URL Structure

```
/                          # home / work list
/book/[slug]               # book detail
/book/[slug]/chapters      # chapter catalog (optional separate page)
/book/[slug]/chapter/[n]  # reader
```

For static builds, use this structure as file paths:
```
index.html
book/[slug]/index.html
book/[slug]/chapter/[n]/index.html
```

Avoid query-string-based routing for primary navigation — it breaks deep-linking and browser history.

## Navigation Patterns

Mobile:
- Top bar: back navigation, current context label. Minimal. No hamburger menu on the reader page.
- Bottom bar on reader: previous chapter / progress label / next chapter.
- Chapter catalog: full-height or half-height bottom sheet, swipe-to-dismiss.
- Reader settings: bottom sheet, swipe-to-dismiss.

Desktop:
- Horizontal nav bar. No bottom bar.
- Reader: optional fixed left sidebar for chapter catalog (visible at ≥ 1024px).
- Reader settings: inline panel or floating popover to the right of the reading column.

Back navigation:
- Reader → Book detail (or catalog).
- Book detail → Home.
- Catalog → Book detail.

## Empty States

| State | Message |
| --- | --- |
| No books on home | "No titles yet. Check back soon." |
| No chapters in a book | "No chapters published yet. Check back soon." |
| Chapter not found | "This chapter isn't available yet." + link to catalog |
| Reading progress cleared | (silent — just show "Start reading") |
| Load error | "Couldn't load this chapter. Try refreshing." |

Empty states must always include a navigation affordance — never a dead end.

## Nice-to-Have Modules

Add these only when the brief asks or when they clearly add reader value:

- Continue reading card (strongly recommended even without explicit request).
- Recently updated feed on the home page.
- Simple language switcher for multilingual sites.
- Search (only if there are more than ~10 books).
- Offline reading hint for PWA builds.

## Optional SEO Extension: Articles

Add an `articles/` section when the user explicitly asks for SEO articles or a blog-style content hub. This is a traffic-acquisition feature — not part of the core reader product.

### When to add
- User asks for SEO articles, reading guides, or "story spotlight" pages
- Existing traffic is already flowing and needs supporting long-form content to capture more search intent

### Structure
```
articles/               ← markdown source files
  {slug}.md             ← one file per article

src/app/articles/
  page.tsx              ← article list page (/articles)
  [slug]/page.tsx       ← article detail page (/articles/{slug})
```

### Frontmatter schema
```yaml
---
title: "Long-form SEO headline"
slug: kebab-case-slug
target: genre-keyword-phrase   # e.g. paranormal-vampire-romance
books: [slug-a, slug-b]        # optional: explicit book slugs for sidebar
cta_url: https://site.domain   # ignored in template — CTA links to /book/{slug}
---
```

`books:` is optional. If absent or empty, the page auto-matches related books by matching keywords from `target` against `books.ts` genres (falling back to the first 3 books in the list).

### content-collections config
Add to `content-collections.ts` alongside the existing `chapters` collection:
```ts
const articles = defineCollection({
  name: 'articles',
  directory: 'articles',
  include: '*.md',
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    target: z.string().optional(),
    books: z.array(z.string()).default([]),
    cta_url: z.string().optional(),
    content: z.string(),
  }),
})
// add `articles` to defineConfig({ content: [chapters, articles] })
```

### Article detail page layout (desktop)
Two-column: `lg:grid-cols-[1fr_300px]`
- **Main (left)**: H1 title → section 0 → q4 ad → sections 1–2 → q3 ad (if 4+ sections) → remaining sections → q5 ad → CTA box linking to primary book
- **Sidebar (right)**: q1 ad → "Stories in this article" book list (cover + title + author + "Read free →" linking to `/book/{slug}`) → q2 ad → "View all stories" link to `/`

### Content splitting
Split article markdown on `\n---\n` separators to insert ads between narrative sections. Strip the leading `# H1` line before splitting (page renders its own `<h1>`).

### CSS
No `@tailwindcss/typography`. Use a custom `.prose-article` class in `globals.css`:
```css
.prose-article { font-size: 16px; line-height: 1.75; color: oklch(var(--bc) / 0.82); }
.prose-article p { margin-bottom: 1em; }
.prose-article h2 { font-weight: 700; font-size: 1.2em; margin: 1.6em 0 0.5em; }
.prose-article strong { font-weight: 600; color: oklch(var(--bc)); }
.prose-article a { color: oklch(var(--p)); }
.prose-article hr { border-color: oklch(var(--bc) / 0.12); margin: 1.5em 0; }
```

### Sitemap
Add the article list page and all article pages to `sitemap.ts`:
```ts
import { allArticles } from 'content-collections'
// ...
const articlePages = [
  { url: `${BASE}/articles/`, priority: 0.6, changeFrequency: 'weekly' },
  ...allArticles.map(a => ({ url: `${BASE}/articles/${a.slug}/`, priority: 0.7, changeFrequency: 'monthly' })),
]
```

### Footer nav
Add `Articles` link before `About` in all pages that have a footer nav.

## Out-of-Scope By Default

Do not add any of these unless explicitly requested:

- Ranking, trending, or recommendation systems.
- Category or genre browse pages.
- Bookshelf or reading list management.
- Reading history log.
- Full-text search.
- Comments or social features.
- Payment, subscription, or chapter unlock.
- User accounts or login.
- Author dashboard or writing tools.
- Analytics dashboard.

## Content Tone

Site copy must feel editorial and calm:

- Use: "Start reading", "Continue reading", "Latest update", "Chapter list", "Reading progress", "Completed", "Ongoing", "Hiatus".
- Avoid: "AI generated", "one-click creation", "super explosive", "powered by", any marketing superlatives, any technical implementation terminology.
- Error messages: direct and helpful, not apologetic or technical.

## Desktop Adaptation

Desktop must use a different layout, not a stretched phone screen:

- Home/work list: wider grid (4–6 columns), `max-width: 1200px`, centered with generous padding.
- Book detail: 2-column layout at ≥ 768px — cover + info left, catalog right (or below).
- Reader: centered column, `max-width: 680px` for Latin, `max-width: 600px` for CJK. Side catalog at ≥ 1024px.
- Latin characters per line in the reader: 60–76 characters. Never allow the full viewport width.
- Navigation bar horizontal, not bottom-anchored.

## README

Every site ships with a `README.md` in Chinese containing:

1. **Header block** — domain, language, tone, ad account, deploy status
2. **书目** — table of all books (slug, title; fuego-eterno adds chapter count and illustration count)
3. **技术栈** — one-liner
4. **构建记录** — build log table (see below)
5. **开发** — local dev commands

### 构建记录 (Build Record)

Append a row every time a significant change is made to the site. Helps track which model built what and lets you compare output quality across models.

```markdown
## 构建记录

| 阶段 | 日期 | 模型 | Token 消耗 | 耗时 |
|------|------|------|-----------|------|
| 初始建站 | YYYY-MM-DD | Claude Sonnet 4.6 | — | — |

> 每次对站点做重大改动，在此追加一行：阶段名称、日期、使用模型、Token 消耗（如可查）、耗时（如可查）。
```

Typical stage names: `初始建站` / `内容补充` / `SEO / GEO 改造` / `Header 透明化 & 跨书推荐` / `广告接入` / `部署上线`.

Place `## 构建记录` **before** `## 开发`.
