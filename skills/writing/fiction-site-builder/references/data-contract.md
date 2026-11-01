# Data Contract

## Purpose

This skill always generates real content — never mock data. If the user has no existing manuscript, run the writing phases first to produce actual chapters, then build the site.

Fiction projects use a filesystem-based directory structure (see below). The Next.js site reads those files directly at build time — no JSON intermediate, no pre-build scripts.

## Loader Strategy

| Scenario | Loader |
| --- | --- |
| Fiction writing directory co-located with Next.js project | **@content-collections** |

## Content Layer (@content-collections)

Use [`@content-collections`](https://www.content-collections.dev/) as the content layer. It hooks into `next dev` / `next build` automatically — drop files into `content/`, rebuild, done. No manual `fs` reads, no hand-written parsers. Chapters become fully-typed objects via auto-generated types.

**Install:**

```bash
pnpm add @content-collections/core@^0.15.2 @content-collections/next@^0.2.11
```

**Project layout:**

```
my-novel-site/
├── content/                      ← all fiction writing content
│   ├── {book-title}/             ← long-form book directory
│   │   ├── chapters/
│   │   │   ├── ch-001-the-beginning.md
│   │   │   └── ch-002-development.md
│   │   ├── outline/              ← writing internal, never read by content-collections
│   │   ├── world/                ← writing internal
│   │   └── tracking/             ← writing internal
│   └── short/                    ← short stories
│       └── {title}/
│           └── prose.md
├── public/
│   └── covers/                   ← cover images, flat structure: one file per book
│       └── {book-slug}.webp      ← served as /covers/{slug}.webp (lossy WebP q82)
├── content-collections.ts        ← collection definitions
├── src/
│   ├── lib/
│   │   └── site.ts                      ← site-level constants (see §Site Constants below)
│   ├── app/
│   │   ├── page.tsx                     ← home: book list
│   │   └── book/[slug]/
│   │       ├── page.tsx                 ← book detail + chapter list
│   │       └── chapter/[n]/
│   │           └── page.tsx             ← reader page with prev/next
└── tailwind.config.ts
```

**`content-collections.ts`:**

> **v0.15 breaking changes vs older docs:**
> - `schema` must be `z.object({...})`, NOT the old `z => ({...})` function form.
> - `content: z.string()` must be explicit in the schema — the field is not injected automatically.
> - `defineConfig` key is `content: [...]`, NOT `collections: [...]`.

```ts
import { defineCollection, defineConfig } from '@content-collections/core'
import { z } from 'zod'

const chapters = defineCollection({
  name: 'chapters',
  directory: 'content',
  include: '*/chapters/*.md',      // long-form: content/{book-title}/chapters/ch-NNN-{title}.md
  schema: z.object({               // z.object() — NOT z => ({})
    title: z.string().optional(),
    chapter: z.coerce.number().optional(),
    bookId: z.string().optional(),
    language: z.string().optional(),
    wordCount: z.coerce.number().optional(),
    publishedAt: z.string().optional(),
    status: z.enum(['published', 'draft']).default('published'),
    content: z.string(),           // required explicit field in v0.15
  }),
  transform: (doc) => {
    const [bookSlug] = doc._meta.path.split('/')
    const filename = doc._meta.fileName
    const orderMatch = filename.match(/ch-?0*(\d+)/)
    const order = doc.chapter ?? (orderMatch ? Number(orderMatch[1]) : 0)
    const rawTitle = filename
      .replace(/^ch-\d+-?/, '').replace(/\.md$/, '')
      .replace(/-/g, ' ').replace(/\b\w/g, (c: string) => c.toUpperCase())
    const title = doc.title ?? rawTitle
    return { ...doc, bookSlug, order, title }
  },
})

export default defineConfig({ content: [chapters] })  // "content", NOT "collections"
```

**`next.config.ts` (Next.js 16 + Turbopack):**

```ts
import { withContentCollections } from '@content-collections/next'
import path from 'path'
import type { NextConfig } from 'next'

const generated = path.resolve(process.cwd(), '.content-collections/generated/index.js')

const nextConfig: NextConfig = {
  output: 'export',
  images: { unoptimized: true },
  trailingSlash: true,
  turbopack: {
    resolveAlias: {
      'content-collections': './.content-collections/generated/index.js',  // relative — required
    },
  },
  webpack(config) {
    config.resolve.alias['content-collections'] = generated
    return config
  },
}

export default withContentCollections(nextConfig)
```

**Usage in pages (`app/book/[slug]/chapter/[n]/page.tsx`):**

```ts
import { notFound } from 'next/navigation'
import { allChapters } from 'content-collections'

// Generates one static page per chapter across all books
export async function generateStaticParams() {
  return allChapters.map(ch => ({
    slug: ch.bookSlug,
    n: String(ch.order),
  }))
}

// Resolve prev/next within the same book
// Next.js 15+: params is a Promise — must be async/await
export default async function ChapterPage({ params }: { params: Promise<{ slug: string; n: string }> }) {
  const { slug, n } = await params
  const bookChapters = allChapters
    .filter(ch => ch.bookSlug === slug)
    .sort((a, b) => a.order - b.order)
  const idx = bookChapters.findIndex(ch => String(ch.order) === n)
  if (idx === -1) notFound()
  const chapter = bookChapters[idx]
  const prev = bookChapters[idx - 1] ?? null
  const next = bookChapters[idx + 1] ?? null
  // ...render
}
```

- Writing internals (`outline/`, `world/`, `tracking/`, `teardowns/`) are excluded by the `include` glob — they never appear in generated types.
- Adding a new book: create `content/{book-title}/chapters/` and write chapters. `next build` picks them up automatically.
- Adding a new short story: create `content/short/{title}/prose.md`. No config change needed.
- Generated types live in `.content-collections/` — add to `.gitignore`.

## Site Constants (`src/lib/site.ts`)

Create `src/lib/site.ts` to centralize site-level constants. These values are used in at least three places (`layout.tsx`, `sitemap.ts`, `llms.txt/route.ts`) — defining them once prevents drift.

```ts
// src/lib/site.ts
export const SITE_NAME = 'Velvet Throne'
export const BASE_URL = 'https://velvet.fiction.example'
export const SITE_DESCRIPTION = 'romance, paranormal, billionaire, and sci-fi fiction for readers who crave intensity.'
export const SITE_LOCALE = 'en'
```

Rules:
- `BASE_URL` must match `metadataBase` in `layout.tsx` — they must be kept in sync.
- If no domain is assigned yet, use `'https://PLACEHOLDER.example.com'` and add a TODO (see SKILL.md §B4 — Domain).
- Import from `@/lib/site` in `sitemap.ts` and `src/app/llms.txt/route.ts` instead of repeating the URL string.

## Data Models

```ts
type Language = "en" | "es" | "ja" | "ko" | "zh";

type HeroStyle = "cinematic" | "gradient" | "atmospheric";
// cinematic: full-bleed cover image hero with text overlay (romance / thriller / paranormal)
// gradient: centered cover card with color gradient backdrop, heroColor sets the tint (fantasy / contemporary / colorful)
// atmospheric: blurred darkened cover bg behind a sharp floating cover card (literary / clean romance / prose-forward)

type BookStatus = "ongoing" | "completed";

type Book = {
  slug: string;
  title: string;
  author: string;
  tagline: string;           // 1-3 sentence hook — see tagline patterns in story-long-write.md
  description: string;       // back-cover copy, 4-6 sentences — follow drama hook formula in story-long-write.md §"Book Description & Tagline"
  genres: string[];
  cover: string;             // /covers/{slug}.webp — always flat path, always required at launch
  status: BookStatus;
  chapterCount: number;      // MUST equal the actual number of .md files in content/{slug}/chapters/
  heroStyle: HeroStyle;
  heroColor?: string;        // CSS color string, only used when heroStyle === "gradient"
  featured?: boolean;        // optional: pin to top of home page grid
};

type Volume = {
  id: string;
  bookId: string;
  order: number;
  title: string;
};

type Chapter = {
  id: string;
  bookId: string;
  volumeId?: string;       // optional arc/volume grouping
  order: number;
  title: string;
  language?: Language;     // per-chapter language (may differ from the book's language)
  sourcePath?: string;     // relative path to source .md file
  content: string;         // rendered body text (Markdown or HTML)
  wordCount?: number;
  publishedAt?: string;    // ISO 8601
  status?: "published" | "draft";
};

type ReadingProgress = {
  bookId: string;
  chapterId: string;
  scrollPercent: number;   // 0–1, position within the chapter
  updatedAt: string;       // ISO 8601
};

```

## Fiction Project Directory Structure

Long-form project:

```text
{book-title}/
├── world/
├── outline/
├── chapters/
│   ├── ch-001-{title}.md
│   └── ...
├── reference/
├── tracking/
│   ├── context.md
│   ├── threads.md
│   ├── timeline.md
│   └── character-status.md
└── resources/
```

Short-form project:

```text
short/{title}/
├── prose.md
├── beat-outline.md
└── teardowns/
```

## Field Mapping

```text
chapters/ch-001-{title}.md   →  Chapter { content, title, order }
short/{title}/prose.md        →  Book (one chapter, status: "completed")
outline/outline.md            →  internal only; not shown to readers
world/characters/*.md         →  internal only; optional public character page if user requests
tracking/*.md                 →  internal only
cover output                  →  Book.cover  (saved to public/covers/{slug}.webp, served as /covers/{slug}.webp — flat, not nested)
```

## Chapter Frontmatter Schema

Prefer this frontmatter in each chapter `.md`:

```md
---
title: "Chapter 1: The Night Ferry"
chapter: 1
bookId: night-ferry
language: en
wordCount: 3240
publishedAt: 2026-06-23
status: published
---

Chapter prose starts here.
```

Fields: `title` (string), `chapter` or `order` (number), `bookId` (string), `language` (Language), `wordCount` (number), `publishedAt` (ISO date string), `status` (`"published"` | `"draft"`).

## Rendering Rules

- Sanitize all Markdown/HTML before rendering user-provided content. Never render raw HTML from chapter files as trusted HTML without sanitization.
- Preserve paragraph breaks (`\n\n` → `<p>` tags or double line break).
- Do not render author notes (author-note blocks, typically prefixed with "Author's Note:" or similar) inside the main prose column unless requested.
- Exclude internal writing files from all reader-facing routes by default.
- Handle missing or empty `content` gracefully: show "This chapter has no content yet." instead of a blank page.

## Pagination and Loading

- Use `generateStaticParams` returning `{ slug, n }` pairs to pre-render every chapter of every book at build time. One static page per chapter, zero runtime filesystem reads.
- For client-side apps: fetch chapter content on demand when the reader enters the route.
- Do not load all chapter content into a single bundle. A book with 100 chapters should not load all 100 on the home page.
- Prefetch the next chapter's content when the reader reaches 80% scroll depth in the current chapter.
