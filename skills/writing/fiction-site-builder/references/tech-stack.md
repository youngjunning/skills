# Tech Stack Decision

## Stack

Always use **Next.js 16 + Tailwind CSS 4 + DaisyUI 5 + @content-collections**. No exceptions. Pin these versions:

| Package | Version |
| --- | --- |
| `next` | `^16` |
| `tailwindcss` | `^4` |
| `@tailwindcss/postcss` | `^4` |
| `daisyui` | `^5` |
| `@content-collections/core` | `^0.15.2` |
| `@content-collections/next` | `^0.2.11` |

- App Router + `output: 'export'` for static hosting.
- Fiction content is managed by `@content-collections`. Define collections in `content-collections.ts` → import fully-typed `allChapters` / `allShortStories` directly in pages. No manual `fs` reads, no hand-written parsers.
- Adding new content = drop files into `content/`, run `next build`. Zero config change.

## Breaking Changes vs Next.js 14

### params is a Promise (Next.js 15+)

In Next.js 15+, route `params` is a `Promise` — accessing `params.slug` synchronously returns `undefined` and causes a silent `notFound()`. Every dynamic page component and `generateMetadata` must be `async` and `await params`.

```ts
// WRONG — causes 404 on all dynamic routes
type Props = { params: { slug: string } }
export default function Page({ params }: Props) {
  const book = getBook(params.slug)  // params.slug is undefined
}

// CORRECT
type Props = { params: Promise<{ slug: string }> }
export default async function Page({ params }: Props) {
  const { slug } = await params
  const book = getBook(slug)
}
```

Apply this pattern to every file under `app/book/[slug]/` and `app/book/[slug]/chapter/[n]/` — both the default export and `generateMetadata`.

After destructuring, use **only** the local variable throughout the entire component, including JSX. Never reference `params.slug` or `params.n` after the `await` line — they are still `Promise` objects, not strings.

```ts
// WRONG — mixes awaited slug with raw params in JSX
const { slug } = await params
return <a href={`/book/${params.slug}`}>...</a>  // params.slug is a Promise, not a string

// CORRECT
const { slug } = await params
return <a href={`/book/${slug}`}>...</a>
```

### Turbopack is the default bundler (Next.js 16)

`next dev` runs Turbopack by default. Webpack `resolveAlias` does NOT apply to Turbopack. Add `turbopack.resolveAlias` alongside `webpack`:

```ts
// next.config.ts
import path from 'path'
const generated = path.resolve(process.cwd(), '.content-collections/generated/index.js')
const nextConfig = {
  turbopack: {
    resolveAlias: {
      'content-collections': './.content-collections/generated/index.js',  // relative path
    },
  },
  webpack(config) {
    config.resolve.alias['content-collections'] = generated  // absolute path ok for webpack
    return config
  },
}
```

Note: Turbopack `resolveAlias` requires a **relative** path (starting with `./`). An absolute path is treated as a server-relative URL and fails silently.

### DaisyUI 5 CSS variable names

DaisyUI 5 renamed all CSS variables. Never use the old shorthand names:

| Old (DaisyUI 4) | New (DaisyUI 5) |
| --- | --- |
| `oklch(var(--bc))` | `var(--color-base-content)` |
| `oklch(var(--p))` | `var(--color-primary)` |
| `oklch(var(--b1))` | `var(--color-base-100)` |

Always use the full `--color-*` prefix.

## Styling

**Tailwind CSS 4 + DaisyUI 5 — required, not optional.**

Use DaisyUI components (`btn`, `drawer`, `badge`, `card`, etc.) as the first choice for any interactive or structured UI element. Only write custom Tailwind utility classes when DaisyUI has no matching component. Never reach for custom CSS where a DaisyUI component exists.

- Tailwind 4 uses CSS-based config. No `tailwind.config.js/ts` for theme tokens — define themes in `globals.css` via `@plugin "daisyui/theme"`.
- PostCSS: use `@tailwindcss/postcss` instead of the old `tailwindcss` plugin. Remove `autoprefixer` (Tailwind 4 handles vendor prefixes).
- Reader themes use DaisyUI's `data-theme` attribute on `<html>`.
- Do not use the DaisyUI `aura` effect component on navigation buttons. It creates white padding artifacts (`padding: 2px` in `.aura`) and `display: inline-block` that conflict with flex layouts. The vivid `btn-primary` fill on the Next button is sufficient without any glow wrapper.
- Do not layer a separate CSS custom property system on top of DaisyUI tokens — use `--color-base-100`, `--color-primary`, etc. directly.
- Never use inline styles for design decisions.

```css
/* globals.css — Tailwind 4 + DaisyUI 5 setup */
@import "tailwindcss";
@plugin "daisyui" {
  themes: my-light --default, my-dark --prefersdark, aura;
}

@plugin "daisyui/theme" {
  name: "my-light";
  default: true;
  color-scheme: light;
  --color-primary: #ec4b9b;       /* generated per-site — see Color Palette below */
  --color-primary-content: #ffffff;
  --color-base-100: #FFF5FB;
  /* ... other tokens */
}
```

## Color Palette

**Philosophy: vibrant, hormonal, alive.**

Fiction sites target readers who tap out of boredom — the color palette must feel youthful, energetic, and emotionally charged. Think hot pink, electric violet, vivid coral, burning orange. Never muted, never corporate, never default cream + terracotta.

**Rules:**
- `--color-primary` must have high saturation (HSL S ≥ 80%) and mid-to-high lightness (L 45–65% in light theme). Warm hues (pink, magenta, coral, orange) or vivid cool hues (electric violet, indigo) both work. No burgundy, no slate, no olive.
- `--color-primary-content` is `#ffffff` for any primary darker than L=65%; otherwise `#1a0a12`.
- `--color-base-100` in light theme: very light tint of the primary hue (not plain white, not beige). E.g. if primary is hot pink → `#FFF5FB`.
- Dark theme `--color-primary`: lighten the light-theme primary by ~20% L so it reads well on dark backgrounds.

**Generate a unique palette per site** — do not reuse the same colors across sites. Each time you build a new site, pick a primary from this palette of starting hues and vary it based on genre mood:

| Genre | Hue direction | Example primary (light) |
| --- | --- | --- |
| Urban Drama / Contemporary Romance | Hot pink → magenta | `#ec4b9b`, `#e91e8c`, `#d946ef` |
| Historical / Dark Fantasy | Warm coral → rose | `#f43f5e`, `#fb7185`, `#e879a0` |
| Cultivation Fantasy | Electric violet → indigo | `#8b5cf6`, `#7c3aed`, `#6366f1` |
| Thriller / Horror | Deep violet → crimson | `#9333ea`, `#dc2626`, `#be185d` |
| Sci-Fi | Electric cyan → indigo | `#06b6d4`, `#3b82f6`, `#6366f1` |

Vary lightness and exact hue by ±10% each time — two romance sites should look visually distinct even if both use hot pink family.

## Fonts

**Use system font stack only. No webfonts, no `@fontsource`, no Google Fonts.**

System fonts load instantly, cover all target language characters out of the box, and add zero bytes to the bundle. The visual difference from a webfont is negligible compared to the reliability and bundle-size gains.

Define one variable in `globals.css` and apply it to `body`:

```css
:root {
  --font-ui: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial,
             "Hiragino Sans", "Yu Gothic UI", "Malgun Gothic", sans-serif;
}
body {
  font-family: var(--font-ui);
}
```

Do not add `@fontsource/*` dependencies. Do not import any font CSS in `layout.tsx`. Do not define `--font-display` or `--font-body` — use font-weight and letter-spacing to establish hierarchy:

- Headings / titles: `font-extrabold tracking-tight` (`font-weight: 800`, `letter-spacing: -0.02em`)
- Chapter title: `text-2xl sm:text-3xl font-extrabold tracking-tight`
- Body prose: `font-size: 19px` (mobile) → `20px` (sm+), `line-height: 1.8` → `1.85`, `margin-bottom: 1.1em`, `max-width: 68ch`, `word-break: break-word`, `text-rendering: optimizeLegibility`

## TypeScript

- Always use TypeScript. Use the data models in `references/data-contract.md` as the type baseline.

## State Management

- Reader preferences (font size, theme, density): `localStorage` for prototypes, user settings API for real products.
- Reading progress: `localStorage` for prototypes, durable backend for real products.
- Do not add Redux, Zustand, Jotai, or any state library. React state is sufficient.

## Deployment

| Mode | Default deployment target |
| --- | --- |
| Next.js export | Vercel, Netlify, Cloudflare Pages |
| Next.js SSR | Vercel |
| Docker/VPS | Only if user specifies |

Do not set up CI/CD or deployment pipelines unless the user asks. Describe the deploy target in the output but leave execution to the user.
