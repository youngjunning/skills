# SEO Reference

Load this reference during Phase B4/B5 and before any site goes live. It consolidates everything search engines and social platforms need to crawl, index, and preview the site correctly.

## Required Files

Create all of these in every site. They are not optional.

| File | Location | Purpose |
|---|---|---|
| `sitemap.ts` | `src/app/sitemap.ts` | Generates `/sitemap.xml` for all static, book, and chapter URLs |
| `robots.ts` | `src/app/robots.ts` | Generates `/robots.txt` allowing all crawlers and pointing to the sitemap |
| `metadata` export | `src/app/layout.tsx` | Site-wide title template, description, `metadataBase`, OG fallback |
| `openGraph` + `twitter` | `book/[slug]/page.tsx` and `book/[slug]/chapter/[n]/page.tsx` | Per-book / per-chapter social previews |
| JSON-LD | `src/app/layout.tsx` (home), book detail pages, chapter pages | Structured data: `WebSite`, `Book`, `BreadcrumbList`, `WebPage` |

## 1. Sitemap

Use Next.js App Router's built-in metadata route. No third-party package.

```ts
// src/app/sitemap.ts
import { MetadataRoute } from 'next'
import { books } from '@/lib/books'
import { allChapters } from 'content-collections'

export default function sitemap(): MetadataRoute.Sitemap {
  const base = 'https://your-domain.com'

  const staticPages: MetadataRoute.Sitemap = [
    { url: base + '/', changeFrequency: 'weekly', priority: 1.0, lastModified: new Date() },
    { url: base + '/about/', changeFrequency: 'yearly', priority: 0.3 },
    { url: base + '/contact/', changeFrequency: 'yearly', priority: 0.3 },
    { url: base + '/privacy/', changeFrequency: 'yearly', priority: 0.2 },
    { url: base + '/terms/', changeFrequency: 'yearly', priority: 0.2 },
  ]

  const bookPages: MetadataRoute.Sitemap = books.flatMap(book => {
    const chapters = allChapters
      .filter(ch => ch.bookSlug === book.slug && ch.status === 'published')
      .sort((a, b) => a.order - b.order)

    return [
      {
        url: `${base}/book/${book.slug}/`,
        changeFrequency: 'weekly' as const,
        priority: 0.8,
        lastModified: new Date(), // rebuild date = freshness signal when chapters are added
      },
      ...chapters.map(ch => ({
        url: `${base}/book/${book.slug}/chapter/${ch.order}/`,
        changeFrequency: 'monthly' as const,
        priority: 0.6,
      })),
    ]
  })

  return [...staticPages, ...bookPages]
}
```

Rules:
- All URLs must end with `/` when the site uses `trailingSlash: true` in `next.config.js`. Mismatches between sitemap URLs and canonical tags cause soft duplicate signals.
- Generate chapter URLs from actual published chapter documents (`allChapters` filtered by `status === 'published'`), not from `book.chapterCount`. `chapterCount` can drift and produce sitemap URLs that 404.
- Run `pnpm build` and verify `/out/sitemap.xml` contains every expected URL before deploying.
- Set `lastModified: new Date()` on book detail pages, not chapter pages. Chapter content does not change; the book page logically changes each time a chapter is added.

## 2. Robots

```ts
// src/app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: '*', allow: '/' },
    ],
    sitemap: 'https://your-domain.com/sitemap.xml',
  }
}
```

No need to disallow `/_next/` in a static export — those files don't exist on the same origin when hosted on a CDN. But never add `Disallow: /` or block any page that has indexable content.

## 3. Root Metadata

```ts
// src/app/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  metadataBase: new URL('https://your-domain.com'), // REQUIRED — omitting this poisons all OG image and canonical URLs with localhost:3000
  title: {
    default: 'Your Site Name — Free Romance Novels Online',
    template: '%s | Your Site Name',
  },
  description: 'Short, keyword-rich description. Lead with the genre and a reader benefit. Under 155 characters.',
  openGraph: {
    siteName: 'Your Site Name',
    type: 'website',
    locale: 'en_US', // use es_ES for Spanish sites
    images: [
      {
        url: '/og-default.png', // absolute path; metadataBase prepends the domain
        width: 1200,
        height: 630,
        alt: 'Your Site Name — romance novels',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
  },
  alternates: {
    canonical: './', // resolves relative to each page's own URL via metadataBase — do not hardcode absolute paths here
  },
}
```

Notes:
- `metadataBase` must be the real live domain, not a staging URL. The most common production bug is forgetting this — every `og:image` and canonical URL in the rendered HTML will point to `localhost:3000`.
- `alternates.canonical: './'` makes every page self-canonicalize. This is correct for SSG: Next.js resolves it against the page's own path.
- `locale` must match the site's actual language (`en_US`, `es_ES`, etc.).
- The OG default image should be 1200×630 (standard social sharing ratio), distinct from book covers (848×1280).
- Site description: lead with the genre and a reader value proposition. Example: `"romance and paranormal novels — read free chapters online. New releases weekly."` Aim for 130–155 characters.

## 4. Book and Chapter Metadata

### Book Detail Page

```ts
// src/app/book/[slug]/page.tsx
import type { Metadata } from 'next'
import { getBook } from '@/lib/books'

export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const book = getBook(params.slug)
  if (!book) return {}

  return {
    title: book.title,
    description: book.description.slice(0, 155),
    keywords: [book.title, book.author, ...book.genres, 'read online', 'free chapters'],
    openGraph: {
      title: book.title,
      description: book.description.slice(0, 155),
      type: 'book',
      images: [{ url: book.cover, width: 848, height: 1280, alt: `${book.title} — ${book.genres[0]} novel cover` }],
    },
    twitter: { card: 'summary_large_image' },
    alternates: { canonical: './' },
  }
}
```

### Chapter Page

```ts
// src/app/book/[slug]/chapter/[n]/page.tsx
export async function generateMetadata({ params }: { params: { slug: string; n: string } }): Promise<Metadata> {
  const book = getBook(params.slug)
  const chapterNum = parseInt(params.n, 10)
  const chapter = getChapter(book?.slug, chapterNum)
  if (!book || !chapter) return {}

  // Extract first 1–2 sentences of the chapter's prose as the description.
  // This avoids near-duplicate meta description signals across all chapter pages.
  // Never reuse the book blurb verbatim on every chapter page.
  const chapterExcerpt = extractFirstSentences(chapter.content, 155)

  return {
    title: `${chapter.title} — ${book.title}`,
    description: chapterExcerpt,
    keywords: [book.title, chapter.title, ...book.genres, `chapter ${chapterNum}`, 'read online'],
    openGraph: {
      title: `${chapter.title} — ${book.title}`,
      description: chapterExcerpt,
      type: 'article',
      images: [{ url: book.cover, width: 848, height: 1280, alt: `${book.title} — ${book.genres[0]} novel cover` }],
    },
    twitter: { card: 'summary_large_image' },
    alternates: { canonical: './' },
  }
}
```

`extractFirstSentences` helper — put in `src/lib/text.ts`:

```ts
export function extractFirstSentences(markdown: string, maxLen: number): string {
  // Strip markdown syntax, then take up to maxLen characters ending at a sentence boundary
  const plain = markdown
    .replace(/#{1,6}\s+/g, '')
    .replace(/[*_`~>\[\]()]/g, '')
    .replace(/\n+/g, ' ')
    .trim()
  if (plain.length <= maxLen) return plain
  const cut = plain.slice(0, maxLen)
  const lastPeriod = Math.max(cut.lastIndexOf('. '), cut.lastIndexOf('! '), cut.lastIndexOf('? '))
  return lastPeriod > 80 ? cut.slice(0, lastPeriod + 1) : cut.slice(0, maxLen - 1) + '…'
}
```

## 5. JSON-LD Structured Data

Use a shared server component to avoid repetition:

```tsx
// src/components/JsonLd.tsx
export function JsonLd({ data }: { data: Record<string, unknown> | Record<string, unknown>[] }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  )
}
```

### Home Page — `WebSite`

```tsx
// src/app/page.tsx (or layout.tsx)
import { JsonLd } from '@/components/JsonLd'

<JsonLd data={{
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: 'Your Site Name',
  url: 'https://your-domain.com',
  inLanguage: 'en',
  // Only include SearchAction if your site has actual search functionality
  // potentialAction: {
  //   '@type': 'SearchAction',
  //   target: 'https://your-domain.com/?q={search_term_string}',
  //   'query-input': 'required name=search_term_string',
  // },
}} />
```

### Book Detail Page — `Book` + `BreadcrumbList`

Note: Google's Book Actions rich result was discontinued in 2023–2024. The `Book` schema type is still valid and used by Bing and for semantic enrichment, but it no longer triggers dedicated Google rich results. Include it regardless — it costs nothing and helps other engines.

```tsx
// src/app/book/[slug]/page.tsx
<JsonLd data={[
  {
    '@context': 'https://schema.org',
    '@type': 'Book',
    name: book.title,
    author: { '@type': 'Person', name: book.author },
    description: book.description,
    image: `https://your-domain.com${book.cover}`,
    url: `https://your-domain.com/book/${book.slug}/`,
    genre: book.genres.join(', '),
    inLanguage: 'en', // or 'es' for Spanish sites
    datePublished: book.publishedAt, // ISO 8601, e.g. '2024-09-01'
    // Omit: isbn (not applicable for web fiction), bookFormat (not meaningful for serialized web content), numberOfPages
  },
  {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://your-domain.com/' },
      { '@type': 'ListItem', position: 2, name: book.title, item: `https://your-domain.com/book/${book.slug}/` },
    ],
  },
]} />
```

### Chapter Page — `WebPage` + `BreadcrumbList`

```tsx
// src/app/book/[slug]/chapter/[n]/page.tsx
<JsonLd data={[
  {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name: `${chapter.title} — ${book.title}`,
    description: chapterExcerpt,
    url: `https://your-domain.com/book/${book.slug}/chapter/${chapterNum}/`,
    inLanguage: 'en',
    isPartOf: {
      '@type': 'Book',
      name: book.title,
      url: `https://your-domain.com/book/${book.slug}/`,
    },
  },
  {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://your-domain.com/' },
      { '@type': 'ListItem', position: 2, name: book.title, item: `https://your-domain.com/book/${book.slug}/` },
      { '@type': 'ListItem', position: 3, name: chapter.title, item: `https://your-domain.com/book/${book.slug}/chapter/${chapterNum}/` },
    ],
  },
]} />
```

## 6. Canonical URL Strategy (SSG Static Export)

With `output: 'export'` + `trailingSlash: true`, Next.js writes each page as `[path]/index.html`. The canonical tag using `alternates: { canonical: './' }` in metadata is the correct approach — Next.js resolves it against `metadataBase` + the page's own path, producing an absolute URL with trailing slash.

**The two most common canonical bugs in static export:**

1. **Missing `metadataBase`**: Every canonical and OG image URL in the rendered HTML will say `http://localhost:3000/...`. This is silent — no build error, no warning. Check your `/out/book/[slug]/index.html` and grep for `localhost` to catch this.

2. **Trailing slash mismatch**: The sitemap, canonical tags, and served URLs must all agree. If `trailingSlash: true` is set, all three must use trailing slashes. Crawlers that see `/book/slug/` in the sitemap but `/book/slug` in the canonical treat them as separate pages.

**What NOT to do:**
- Do not hardcode absolute canonical strings in `generateMetadata` like `https://your-domain.com/book/${book.slug}/`. If the domain changes (staging, preview deploys), every page has the wrong canonical. Use `'./'` and let `metadataBase` do the work.
- Do not set `metadataBase` to a staging URL in production builds. Use an environment variable: `metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL ?? 'https://your-domain.com')`.

## 7. Internal Linking Strategy

The link hierarchy is: **Home → Book List → Book Detail → Chapter 1 → Chapter 2 → … → Chapter N**. Every link in this chain must be a crawlable `<a href>` tag, not a JS-only button.

### Home Page
- Every book card links to `/book/[slug]/`. Use the book title as anchor text — not "Read Now" or "Click Here".
- Recommended anchor text pattern: `{book.title}` or `{book.title} — {genres[0]}`.

### Book Detail Page
- "Start Reading" CTA links to `/book/[slug]/chapter/1/` — this is the most important internal link on the site for distributing link equity into the chapter set.
- Chapter list renders all chapters as individual `<a>` links. Anchor text: `Chapter ${n}: ${chapter.title}` — not just `Chapter ${n}`.
- "You May Also Like" section: show 2–3 books from the same genre with linked book titles. This creates cross-book internal links and distributes PageRank across the catalog.

### Chapter Page
- Header/breadcrumb: `← {book.title}` link back to the book detail page. This is the primary back-reference from chapter to book.
- Bottom navigation: "← Chapter N-1 title" and "Chapter N+1 title →" as `<a>` links. Chapter 1 has no Previous; last chapter has no Next.
- These chapter nav links are how Googlebot discovers the full chapter sequence — `rel=next/prev` was dropped by Google in 2019 and has no replacement. Crawlable in-page links are the correct mechanism.
- End-of-chapter CTA: after the last chapter, link to the book detail page of a related title ("Continue Reading: {Related Book Title}"). This keeps readers on the site and creates cross-book links.

## 8. Image SEO

### next/image in Static Export

Static export requires either `images: { unoptimized: true }` in `next.config.js` or a custom image loader (Cloudflare Images, Imgix, etc.). Without this, `next/image` optimization endpoints don't exist and the build silently serves broken image URLs on some configurations.

```js
// next.config.js
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true, // required for pure static export without a CDN image optimizer
  },
}
```

If using Cloudflare Pages or a CDN with image optimization, wire up a custom loader instead and remove `unoptimized: true`.

### Alt Text

Alt text is a ranking signal for Google Images. Romance readers frequently discover books via image search.

- Book cover: `alt={`${book.title} — ${book.genres[0]} novel cover`}`
- Chapter illustration: `alt={`${book.title} Chapter ${chapterNum} — ${chapter.title}`}`
- Site logo: `alt="[Site Name] logo"`
- Never leave `alt` empty on content images. Use `alt=""` only for purely decorative images.

### Image Performance (CLS and LCP)

- Always set explicit `width` and `height` on `next/image`. This reserves layout space and prevents Cumulative Layout Shift (CLS).
- Book cover on the book detail page is almost always the Largest Contentful Paint (LCP) element. Set `priority={true}` on it — this adds a `<link rel="preload">` in the document head. Without this, the cover loads lazily and LCP on mobile typically exceeds 3s.
- Target cover file size: under 150 KB after compression. Oversized covers are the single most common LCP killer on mobile. PNG from the cover generation pipeline can be 500 KB+; convert to WebP or compress the PNG before deploying.
- Hero/banner images on the home page: set `priority={true}` on the first visible image only.

### OG Images

The `og:image` URL must be absolute. Verify this in the rendered HTML source — OG crawlers (Facebook, Twitter) do not follow `metadataBase` resolution; they need a fully qualified URL. If `metadataBase` is set correctly and the image path starts with `/`, Next.js handles this automatically. Grep `/out/` for `og:image` and confirm every value starts with `https://`.

## 9. Mobile SEO and Core Web Vitals

Google uses mobile-first indexing. The mobile rendering is what gets ranked.

### Core Web Vitals Thresholds (as of March 2024)

| Metric | Good | Needs Improvement | Poor |
|---|---|---|---|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5–4.0s | > 4.0s |
| INP (Interaction to Next Paint) | ≤ 200ms | 200–500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1–0.25 | > 0.25 |

INP replaced FID (First Input Delay) as a Core Web Vital on March 12, 2024. FID only measured the first interaction; INP measures the worst interaction latency throughout the page lifetime.

### LCP — Book Cover is the Target

The book cover on the detail page is the LCP element. Attack it on two fronts:
1. `priority={true}` on the `<Image>` component → preload tag in `<head>`
2. Compress the cover file. Use WebP or aggressively compressed JPEG/PNG. Target < 100 KB.

### INP — Ad Scripts are the Risk

Ad scripts (GPT, AdSense) run on the main thread and are the primary INP risk on these sites. Mitigation:
- Load `AdSlot` / `AdsenseSlot` as client components. They should mount after the page content is interactive.
- Do not load ad scripts in the `<head>` with `strategy="beforeInteractive"`. Use `strategy="afterInteractive"` (Next.js Script) or `strategy="lazyOnload"` for non-critical ads.
- Chapter navigation (`← Previous` / `Next →`) should be plain `<a>` links, not buttons with `onClick` handlers that do client-side routing with heavy re-renders.

### CLS — Reserve Space for Ads

Ads are the most common source of CLS on these sites. Every `AdSlot` component must have a container `div` with a fixed minimum height matching the smallest possible ad size:

```tsx
// Correct — space is reserved before the ad loads
<div style={{ minHeight: '250px', minWidth: '250px' }}>
  <AdSlot position="q1" />
</div>
```

All ad slots (q1–q5) use standard display sizes; `AdSlot` already reserves `minWidth: 250, minHeight: 250` before creative loads.

### Preconnect for Third-Party Origins

Put these in `layout.tsx` `<head>` before any script tags:

```tsx
<link rel="preconnect" href="https://securepubads.g.doubleclick.net" />
<link rel="preconnect" href="https://pagead2.googlesyndication.com" />
<link rel="preconnect" href="https://connect.facebook.net" />
<link rel="dns-prefetch" href="https://securepubads.g.doubleclick.net" />
```

### Font Strategy

Limit custom fonts to two font families maximum. Use `font-display: swap` (Next.js `next/font` applies this by default). Avoid loading large variable font files above the fold on mobile.

### Viewport Meta

Next.js App Router automatically outputs `<meta name="viewport" content="width=device-width, initial-scale=1">` — do not override it. Do not set `user-scalable=no`; it hurts accessibility and is a mobile usability signal Google tracks.

## 10. Thin Content and Duplicate Content Strategy

### What is NOT a problem

Chapter pages contain 1,000–1,800 words of original prose. This is not thin content — Google's thin-content threshold is around 300 words; fiction chapters are well above it. Google indexes long-form fiction chapters and can rank individual chapters for long-tail search queries like `"romance enemies to lovers chapter 3 read online"`.

### What IS a problem

1. **Identical meta descriptions across all chapter pages.** If every chapter page uses `book.description.slice(0, 160)` as its meta description, every chapter page in the set looks near-duplicate to the crawler. Fix: use `extractFirstSentences(chapter.content, 155)` (see Section 4). The first paragraph of each chapter is unique.

2. **Identical `<title>` tag structure with no differentiator.** `Chapter 1 | Book Title | Site Name` vs `Chapter 2 | Book Title | Site Name` are fine — the chapter number differentiates them. Avoid stripping the chapter title entirely.

3. **Same story text on two different sites.** This is prohibited by `fictions/AGENTS.md`. Cross-site duplicate content from the same network of sites is a significant ranking penalty risk. Different language versions (English on velvet-throne, Spanish adaptation on fuego-eterno) are acceptable — they are distinct language content.

4. **Book detail page and Chapter 1 page with nearly identical content.** The book detail page description is the marketing blurb; the chapter 1 description should be the opening lines of chapter 1 prose. Keep them distinct.

### `noindex` Policy

- Chapter pages: do NOT add `noindex`. They are unique long-form content.
- `/about/`, `/contact/`, `/privacy/`, `/terms/`: do NOT add `noindex` unless truly templated. These pages contribute to topical trust signals.
- The only pages that should be `noindex` are pagination, tag/filter pages with thin derived content, or error pages — none of which exist in the current architecture.

## 11. Multilingual SEO and hreflang

This applies when the same story has versions on different language sites (e.g., English on `velvet.fiction.example`, Spanish adaptation on `fuego.fiction.example`). For pages with no cross-language equivalent, skip hreflang entirely.

### How it Works

hreflang tells Google which language/region variant a page targets and links equivalents together. The annotation must be **bidirectional**: if the English page declares the Spanish page as an alternate, the Spanish page must also declare the English page as an alternate. One-way annotation is ignored.

### Implementation in Next.js App Router

`alternates.languages` in `generateMetadata` works correctly with `output: 'export'`. Only the built-in i18n routing middleware is blocked in static export — the metadata API is unaffected. Use **absolute URLs** for cross-domain hreflang:

```ts
// src/app/book/[slug]/page.tsx (English site)
export async function generateMetadata({ params }): Promise<Metadata> {
  const book = getBook(params.slug)
  const esEquivalentSlug = book.translations?.es // only set if a Spanish version exists

  return {
    title: book.title,
    description: book.description.slice(0, 155),
    alternates: {
      canonical: './',
      ...(esEquivalentSlug && {
        languages: {
          'en': `https://velvet.fiction.example/book/${book.slug}/`,
          'es': `https://fuego.fiction.example/book/${esEquivalentSlug}/`,
          'x-default': `https://velvet.fiction.example/book/${book.slug}/`,
        },
      }),
    },
  }
}
```

The corresponding Spanish page must mirror this annotation with the `en` and `es` values swapped.

### Sitemap Alternates (Optional but Recommended)

Next.js 14+ supports `alternates.languages` in `sitemap.ts` entries. Use this for pages that have known cross-language pairs:

```ts
// src/app/sitemap.ts (English site)
const bookPages = books.flatMap(book => {
  const esSlug = book.translations?.es
  return [
    {
      url: `${base}/book/${book.slug}/`,
      changeFrequency: 'weekly' as const,
      priority: 0.8,
      lastModified: new Date(),
      ...(esSlug && {
        alternates: {
          languages: {
            en: `${base}/book/${book.slug}/`,
            es: `https://fuego.fiction.example/book/${esSlug}/`,
          },
        },
      }),
    },
    // chapter entries (no hreflang needed on individual chapters)
  ]
})
```

### Language Codes

| Site | `<html lang>` | OG `locale` | hreflang value |
|---|---|---|---|
| velvet-throne (EN) | `en` | `en_US` | `en` |
| midnight-fable (EN) | `en` | `en_US` | `en` |
| fuego-eterno (ES) | `es` | `es_ES` | `es` (use `es-419` only if explicitly targeting Latin America) |
| wildfire-reads (EN) | `en` | `en_US` | `en` |
| london-pages (EN-GB) | `en-GB` | `en_GB` | `en-GB` |

The `<html lang="...">` attribute is set in the root `layout.tsx`. Without it, Google infers the language from page content — fine in practice, but explicit is always better.

### `x-default` is Required

Every hreflang set must include an `x-default` entry pointing to the English (default) page. It tells Google which URL to show to users in regions/languages not covered by any explicit alternate.

## 12. Content Freshness Signals

Google's freshness algorithm ("Query Deserves Freshness") boosts recently updated content for volatile queries. Romance fiction search queries are not typically freshness-sensitive, but adding new chapters is a legitimate freshness signal that increases crawl frequency.

- Set `lastModified: new Date()` in `sitemap.ts` on **book detail pages** only, not chapter pages. The book detail page is rebuilt every time a new chapter ships, so the build date is a legitimate modification date.
- In the `Book` JSON-LD, include `datePublished` (original launch date) and `dateModified` (date of most recent chapter addition, ideally from `book.updatedAt`):

```ts
{
  '@type': 'Book',
  datePublished: book.publishedAt, // '2024-09-01'
  dateModified: book.updatedAt,    // '2025-06-15' — update this when chapters are added
}
```

- When adding new chapters: rebuild and redeploy. The sitemap automatically includes the new chapter URLs. Google will discover them on the next sitemap crawl (usually within 24–72 hours of sitemap submission ping).
- Consider showing a visible "Last Updated" date on the book detail page (not just in meta). Readers click more on recently updated titles in SERPs, improving CTR, which is a positive ranking signal.
- Do not set `changeFrequency: 'daily'` on everything. Googlebot treats this as a hint, not a command, but setting unrealistic frequencies erodes trust in the hint over time. Book pages: `weekly`. Chapter pages: `monthly`. Static/legal pages: `yearly`.

## 13. Post-Launch Checklist

- [ ] Submit `/sitemap.xml` to Google Search Console.
- [ ] Verify `/robots.txt` returns 200 and references the correct sitemap URL.
- [ ] Inspect a book page and a chapter page with Google's [Rich Results Test](https://search.google.com/test/rich-results). Expect BreadcrumbList and WebSite results; Book Actions are discontinued so don't chase that.
- [ ] Run PageSpeed Insights (mobile) on the home page and a chapter page. Target LCP < 2.5s, INP ≤ 200ms, CLS < 0.1.
- [ ] Inspect a book page with the [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) and the [Twitter Card Validator](https://cards-dev.twitter.com/validator).
- [ ] Grep `/out/` for `content="http://localhost` — any hit means `metadataBase` is wrong or missing.
- [ ] Grep `/out/` for `og:image` and confirm every value is an absolute `https://` URL.
- [ ] Confirm chapter pages have unique `<title>` tags (not all "Chapter N | Site Name" with identical N).
- [ ] Confirm chapter pages have unique `<meta name="description">` values (not the book blurb repeated on every chapter).
- [ ] Verify `<html lang="...">` is set correctly in each site's root `layout.tsx`.
- [ ] For multilingual pairs: verify hreflang annotations are bidirectional using the URL Inspection tool in Search Console for both the English and Spanish URLs.
- [ ] Verify no chapter page is accidentally set to `noindex`.
- [ ] Confirm chapter navigation (Previous / Next) renders as `<a>` tags in the built HTML (not JS-only).
- [ ] Confirm that `/out/` does not contain any `covers/*.json` or `illustrations/**/*.json` prompt files (should be blocked or excluded from the build).

## 13.1 Traditional Chinese / Taiwan SEO Notes

Use these notes when the site language is `zh-TW` or the user asks for Taiwan-facing fiction traffic.

- Lead with natural Traditional Chinese search phrases: `繁體中文言情小說推薦`, `言情小說線上看`, `完結言情小說推薦`, then add genre phrases such as `豪門契約婚姻小說`, `重生復仇宮廷言情小說`, `仙俠虐戀小說`.
- Avoid Simplified Chinese keyword stuffing. A `zh-TW` page that says `网文`, `霸总文`, `女频`, or `爽文` reads off-market for Taiwan readers unless the article is explicitly discussing Mainland web novel categories.
- For a new site with only three books across different sub-genres, create one broad book-list article first. Example title pattern: `繁體中文言情小說推薦：3 本完結書單，從契約婚姻到重生復仇`.
- The article should describe why each book fits a reader mood, not just list tropes. Taiwan search traffic often arrives through recommendation intent, so the copy must answer "which one should I read first?"
- Use `books:` frontmatter to pin the recommended order. Put the strongest commercial hook first, then related books.
- Add `/articles` to the homepage footer once any article exists. Search visitors who land on the homepage need a visible path back into the SEO content hub.
- Article cover: use a 16:9 landscape visual (`1280×720`) with no text. For mixed-genre lists, combine three visual zones rather than forcing one genre signal.
- CTA should be plain and low-friction: `從第一章開始讀，無需註冊。` Avoid hard-sell wording.

## 14. Common Mistakes

- **Forgetting `metadataBase`:** Every `og:image`, canonical, and `alternates.languages` URL in the rendered HTML will be `http://localhost:3000/...`. No build error. Silent production failure. Always check by grepping the built `/out/` files.
- **Reusing the book blurb as description on every chapter page:** Creates near-duplicate meta description signals across the entire chapter set. Use the chapter's own opening prose (see `extractFirstSentences` in Section 4).
- **Leaving alt empty on cover images:** Google Images is a meaningful discovery channel for romance fiction. Every cover needs a descriptive alt text.
- **Not setting `priority={true}` on the above-fold cover image:** The book cover is always the LCP element on the detail page. Without `priority`, it loads lazily and LCP exceeds 4s on mobile 4G. This is the easiest LCP win available.
- **No `min-height` on ad containers:** Ad slots that render after page load cause CLS. Reserve the space with a fixed `minHeight` equal to the ad's smallest possible dimension.
- **Serving the prompt JSON:** Block or exclude `/covers/*.json` and `/illustrations/**/*.json` from the deployed output so generation prompts are not public.
- **Wrong chapter count:** `sitemap.ts` and `chapterCount` in `books.ts` must stay in sync with the actual file count. Derive `chapterCount` from the filesystem at build time to prevent drift.
- **Trailing slash mismatch:** If `trailingSlash: true` is set in `next.config.js`, the sitemap, canonical tags, and all internal `<a>` links must use trailing slashes. Inconsistency causes crawlers to treat trailing-slash and non-trailing-slash URLs as separate pages, splitting link equity.
- **One-way hreflang annotation:** If the English page declares the Spanish alternate but the Spanish page does not reciprocate, Google ignores both annotations entirely.
- **Publishing the same story text on two sites:** Google will pick one version to rank and may demote the other site. This also violates the uniqueness rule in `fictions/AGENTS.md`. Different language adaptations are acceptable; same-language duplicate text is not.
- **Setting `<html lang="en">` on Spanish sites:** Copy-pasting the English site's `layout.tsx` leaves the wrong `lang` attribute. Set it correctly: `<html lang="es">` for fuego-eterno.
- **Using `strategy="beforeInteractive"` for ad scripts:** Ad scripts must not block page interactivity. Use `strategy="afterInteractive"` at the earliest.
- **Overly optimistic `changeFrequency`:** Setting `daily` everywhere inflates crawler expectations and reduces the hint's credibility over time. Use accurate frequencies.

---

## 15. Articles (`articles/` directory)

Articles are SEO landing pages that drive L1 traffic into books. They live in `articles/` alongside book content and are rendered at `/articles/{slug}/`. Two types exist; choose one per article session.

### 15.0 — Article-Book Relationship

Every new long-form book triggers A4 automatically. Articles and book pages target different query layers:

- **Book pages** (`/book/{slug}`) rank for long-tail queries — title, character names, specific plot keywords.
- **Articles** (`/articles/{slug}`) rank for genre-category queries — "best romance books", "fae romance online" — and drive cold traffic to multiple books at once.

**Routing logic (run each time a new book is added):**

| Condition | Action |
|---|---|
| Existing SEO article targets the same genre keyword | Move new book to `books[0]`; keep existing books as `books[1–n]`; rewrite opening section; regenerate cover only if concept changed substantially |
| No existing article for this genre keyword | Create a new SEO list article; new book = `books[0]`; fill `books[1–2]` with existing same-genre books |
| Book has a strong social hook (specific premise, unusual dynamic) | Also create a short-form traffic article (§ 15.2) — use judgment, not every book needs one |

**New book is always `books[0]`** in any article it anchors — it gets the primary CTA button and the longest prose section. Existing books are supporting context.

**Genre keyword matching:** use the book's `target` field (from frontmatter) or A0's top keyword. One SEO article per genre keyword per site — do not create two articles with the same `target`. If an update would make the article exceed 5 books, drop the weakest-performing one.

---

### 15.1 — SEO List Article

**Purpose:** rank for broad keyword queries (`"best romance books"`, `"fae romance books"`). Drives cold traffic from search.

**Word count:** 1200–1800 words.

**Frontmatter schema (content-collections):**

```yaml
---
title: "Best romance Books to Read Online (Dark, Obsessive, and Free)"
slug: "best-dark-romance-books"          # matches filename, no spaces
publishedAt: "YYYY-MM-DD"
description: "130–155 char meta description leading with genre + value prop."
target: "best romance books"        # the keyword this article targets
books:                                   # slugs from books.ts — drives sidebar + primary CTA
  - the-ceos-obsession
  - the-devils-debt
cover: /covers/articles/{slug}.webp      # landscape hero image — see § 15.3
---
```

**Content structure:**

1. Opening paragraph: define the genre distinction (what readers are actually looking for — not the surface description).
2. Per-book sections, each 150–250 words, separated by `---`. Bold the book title on first mention. Describe the specific premise + power dynamic, not generic praise.
3. Final section: "where to read" paragraph ending with plain-text CTA: `Start reading free at Velvet Throne — no account required.` (no markdown link — the page template adds the CTA button).

**No `cta_url` field.** The page template generates the primary CTA button from `books[0]`.

---

### 15.2 — Short-Form Traffic Article (引流短篇)

**Purpose:** social traffic (Facebook/Reddit/organic). Hook-driven. Sends readers directly to specific books.

**Word count:** 300–500 words.

**Title format:** 2-sentence hook. Specific detail + consequence. Example: *"He Created the Position Two Years Before She Applied. She Found the Proof in a Drawer She Wasn't Supposed to Open."*

**Frontmatter schema:**

```yaml
---
title: "Hook sentence one. Hook sentence two."
slug: hook-sentence-slug
target: genre-keyword-for-seo            # e.g. billionaire-dark-romance
books: [primary-slug, second-slug, third-slug]   # inline array, max 3
cta_url: https://{site-domain}           # kept for reference; not rendered by template
cover: /covers/articles/{slug}.webp
---
```

**Content structure:**

1. Opening scene (4–8 lines): present tense, 3rd person, specific moment, cut before resolution. No character names repeated from the title.
2. `---`
3. Book pitch for `books[0]`: 2–4 sentences. Bold the title on first mention. Show what the reader is deciding, not what happens.
4. `---`
5. Book pitch for `books[1]`.
6. `---`
7. (Optional) Book pitch for `books[2]`.
8. `---`
9. Closing line (1 sentence, thematic link between all books).
10. Inline CTA — link to specific books, not the homepage:

```markdown
**[Start reading Primary Title](/book/primary-slug)** · [Second Title](/book/second-slug) · [Third Title](/book/third-slug)

*Free to read. No account required. All stories available now.*
```

**Never use an external absolute URL** (`https://velvet.fiction.example`) for the inline CTA — it triggers a full page reload and sends readers to the homepage instead of the book. Use internal paths (`/book/{slug}`).

---

### 15.3 — Article Cover Images

Every article needs a landscape cover for the hero image and OG share preview.

**Spec:**
- Format: WebP, q78
- Size: `1280×720` (GPT `1280x720` preset — exact match, no resize needed)
- Path: `public/covers/articles/{slug}.webp`
- Frontmatter field: `cover: /covers/articles/{slug}.webp`

**Generation (GPT Image 2 primary, nano fallback):**

```bash
PROMPT="[cinematic scene matching article topic]. Dark aesthetic, no text, no watermarks."
OUTPUT_PATH="/tmp/article_cover_${slug}.png"

if gen_image_apiyi "gpt-image-2-all" "1280x720" "$OUTPUT_PATH"; then
  to_webp "$OUTPUT_PATH" "$OUT_DIR/${slug}.webp" 78
  rm -f "$OUTPUT_PATH"
elif gen_image_apiyi "nano-banana-pro" "1024x1024" "$OUTPUT_PATH"; then
  sips -c 576 1024 "$OUTPUT_PATH" 2>/dev/null   # crop to 16:9
  sips -z 720 1280 "$OUTPUT_PATH" 2>/dev/null   # resize
  to_webp "$OUTPUT_PATH" "$OUT_DIR/${slug}.webp" 78
  rm -f "$OUTPUT_PATH"
fi
```

Run all article covers in parallel (one background process per article). See `references/generation.md` for the `gen_image_apiyi` and `to_webp` functions.

**Prompt guidelines by article type:**
- SEO list article: genre-defining scene (gothic library for dark academia, luxury penthouse for billionaire, space bridge for military sci-fi). Dark cinematic. No figures required.
- Short-form traffic article: key scene from the opening hook (lakefront estate at night, painting on a gothic wall, scattered classified documents). Match the article's specific atmosphere.

**OG metadata:** The article detail page must include the cover in OpenGraph metadata:

```ts
const ogImage = article.cover ? `${BASE_URL}${article.cover}` : undefined
openGraph: {
  ...(ogImage ? { images: [{ url: ogImage, width: 1280, height: 720 }] } : {}),
}
```

---

### 15.4 — Article Page Template Requirements

The `src/app/articles/[slug]/page.tsx` must implement:

1. **Hero image block** (if `article.cover` exists): `aspect-[16/9]` or `aspect-[2/1]` container, `object-cover`, `priority` loading.
2. **Section split:** `content.split(/\n\s*---\s*\n/)` after stripping the leading H1. Insert ad slots between sections.
3. **Primary CTA block:** `books[0]` → `/book/{slug}` link. Never use `cta_url` for navigation — it is metadata only.
4. **Sidebar:** related books with cover thumbnails linking to `/book/{slug}`.
5. **List page cover:** `src/app/articles/page.tsx` must give the landscape cover enough visual weight to communicate the article topic. Use a full-width `16:9` image above the text on mobile and at least `288×162px` beside the text from `sm` upward. The article-list content column should be at least `max-w-5xl`; do not use the old `96–128px` postage-stamp thumbnail pattern.

### 15.5 — Common Article Mistakes

- **Inline CTA links to the homepage:** `https://velvet.fiction.example` causes a full page reload and drops readers at the home page. Use `/book/{slug}` for every in-content book link.
- **Missing `cover` field after generation:** If `cover` is omitted from frontmatter, the hero image and OG preview are both missing. Always add the field immediately after generating the image.
- **`cta_url` used for navigation:** The page template ignores `cta_url`. It is retained in frontmatter for reference only. The primary CTA button always uses `books[0]`.
- **SEO article slug mismatch:** `slug` in frontmatter must match the filename exactly (no spaces, hyphens only). Content-collections uses the frontmatter `slug` for routing; a mismatch causes a 404.
- **Book slugs not in `books.ts`:** `getRelatedBooks()` silently drops unrecognized slugs. Cross-check every slug in `books:` against `src/lib/books.ts` before committing.
- **Short-form article too long:** Once prose for a book section exceeds ~200 words the piece reads like a chapter summary, not a hook. Cut to the premise and the moment — do not resolve it.
