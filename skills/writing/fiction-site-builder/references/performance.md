# Performance

## Core Web Vitals Targets

Slow page loads lose readers before the first chapter. Fiction reading sites have no tolerance for sluggish chapter transitions.

| Metric | Target | Notes |
| --- | --- | --- |
| LCP | < 2.5s | Largest contentful paint at the 75th percentile of real users (Google "good" threshold; > 4s is "poor"). On a fiction site the LCP element is usually the first cover image or the chapter's opening heading. |
| INP | < 200ms | Reader controls (theme switch, font size) must be instant |
| CLS | < 0.1 | Font loading and image loading must not cause visible layout shifts |
| TTFB | < 600ms | For server-rendered routes; SSG from Vercel edge CDN targets < 100ms |

### Verification strategy

**Default (fast, unattended):**
- Build the site (`pnpm run build`).
- Check the build output for warnings about large JS bundles or unoptimized images.
- Run automated smoke tests with `curl` against the started server (see `qa-checklist.md`).
- Verify cover images are WebP (lossy q82) and comfortably under 300KB (q82 typically lands ~50–60KB).

**Deep audit (only when user explicitly asks):**
- Test on simulated mobile (Moto G4 equivalent) at Slow 3G in Chrome DevTools Lighthouse. Do not test only on fast desktop connections.

Do not block the pipeline on a full Lighthouse run by default.

---

## LCP — Largest Contentful Paint

### What is the LCP element on a fiction site

| Page | LCP element | Notes |
|---|---|---|
| Home / catalog | First visible book cover `<img>` | Usually the top-left cover in a grid |
| Book detail | Hero cover `<img>` | Larger display size than grid |
| Chapter reader | `<h1>` chapter heading | No image involved — fast HTML delivery is the lever |

On chapter reader pages, image optimization does not affect LCP. SSG + CDN delivery is the only LCP lever there.

### `next/image` priority and preload

**Next.js ≤15:** Use the `priority` prop. It injects `<link rel="preload" as="image" imagesrcset="..." imagesizes="...">` in `<head>`, triggering the browser's preload scanner before the `<img>` element is parsed in the body. This is what makes the difference on SSG where the image is always rendered below the initial scan position.

```jsx
// Apply only to the first visible cover — the one that will be the LCP element
<Image
  src={books[0].cover}
  width={160}
  height={240}
  sizes="(max-width: 480px) 160px, 200px"
  priority   // injects <link rel="preload"> in <head>
  alt={books[0].title}
/>
```

**Next.js 16+:** `priority` is deprecated. Use `fetchPriority="high"` + `loading="eager"` instead. Do not combine `preload` and `fetchPriority` — the docs warn against this.

```jsx
// Next.js 16+
<Image
  src={books[0].cover}
  fetchPriority="high"
  loading="eager"
  width={160}
  height={240}
  sizes="(max-width: 480px) 160px, 200px"
  alt={books[0].title}
/>
```

Apply to **only the first visible cover** (the LCP candidate). Every other cover should use the default `loading="lazy"`.

### `sizes` prop is mandatory

Without `sizes`, Next.js assumes the image is 100vw wide and generates an oversized srcset. With correct `sizes`, the browser picks the smallest adequate variant. Omitting `sizes` on a 160px cover causes the browser to download a 1200px image on mobile.

```jsx
// Cover grid — 2 columns on mobile, 3-4 on desktop
<Image
  src={book.cover}
  width={160}
  height={240}
  sizes="(max-width: 480px) calc(50vw - 24px), (max-width: 768px) 160px, 200px"
  loading="lazy"
  alt={book.title}
/>

// Hero cover on book detail page
<Image
  src={book.cover}
  width={180}
  height={270}
  sizes="(max-width: 768px) 180px, 220px"
  priority
  alt={book.title}
/>
```

### SSG advantage for LCP

SSG pages are served from Vercel's edge CDN with TTFB < 100ms globally. `LCPAttribution.timeToFirstByte` is a direct LCP sub-component — SSG eliminates server compute latency entirely. For a fiction site, always prefer SSG (`generateStaticParams` + default output) over SSR.

---

## INP — Interaction to Next Paint

INP measures responsiveness: every tap, click, and keypress. Target < 200ms. The primary INP killers on ad-monetized fiction sites are long tasks from third-party scripts during page load.

### INP breakdown

INP = input delay + processing duration + presentation delay

- **Input delay**: Time waiting for long tasks (ad scripts) to finish before event handlers run. Dominant on page load.
- **Processing duration**: Time running your event handlers. Dominant post-load.
- **Presentation delay**: Layout/paint after handlers complete.

### Breaking up long tasks with `scheduler.yield()`

Ad scripts (GPT.js, AdSense) create long tasks (> 50ms) during initialization that block the main thread. When a user taps during this window, the interaction is queued — this is input delay.

Use `scheduler.yield()` to break ad initialization into yielding chunks:

```javascript
// scheduler.yield() is Chrome 129+, Firefox 142+. Polyfill for Safari:
function yieldToMain() {
  if (globalThis.scheduler?.yield) return scheduler.yield();
  return new Promise(resolve => setTimeout(resolve, 0));
}

// Break ad initialization into yielding steps
async function initAdSlot(slotId, sizes, divId) {
  const slot = googletag.defineSlot(slotId, sizes, divId);
  await yieldToMain(); // yield — user input can now be handled
  slot.addService(googletag.pubads());
  await yieldToMain();
  googletag.display(divId);
}
```

**`scheduler.yield()` advantage over `setTimeout(fn, 0)`:** Continuation is prioritized over fresh tasks from the same source — your ad code picks up where it left off rather than going to the back of the task queue.

**`isInputPending()` is no longer recommended** — superseded by `scheduler.yield()`.

### Batch long jobs in 50ms chunks

```javascript
async function runJobs(jobs) {
  let lastYield = performance.now();
  for (const job of jobs) {
    job();
    if (performance.now() - lastYield > 50) {
      await yieldToMain();
      lastYield = performance.now();
    }
  }
}
```

### Reader UI controls (theme toggle, font size)

Theme toggle and font size are pure CSS state changes — they must not trigger React re-renders that cascade into ad slot re-renders.

- **Theme toggle**: swap `data-theme` attribute on `<html>`. CSS-only, zero JS reflow.
- **Font size**: swap a CSS custom property or `data-font-size` attribute. Same principle.
- **Memo isolation**: wrap `<AdSlot>` components in `React.memo` so reader UI state changes don't cause ad slot re-renders.

```tsx
const AdSlot = React.memo(function AdSlot({ slotId }: { slotId: string }) {
  // ... ad setup
});
```

### GPT request timing for the current fill strategy

Do not set `disableInitialLoad` or gate GPT refresh behind viewport entry. The current revenue default requests every configured slot on component mount so request coverage and fill are not dependent on scroll timing. Keep GPT asynchronous and reserve slot dimensions to control the LCP/CLS cost:

```javascript
googletag.cmd.push(() => {
  googletag.setConfig({
    singleRequest: true,
  });
  googletag.pubads().setForceSafeFrame(true);
  googletag.enableServices();
});
```

`singleRequest` batches only slots defined before the first `display()` call. Immediate per-component registration improves request coverage but does not guarantee deterministic one-request SRA batching; centralize all slot definitions before the first display only when that architecture is explicitly required.

---

## CLS — Cumulative Layout Shift

### Ad slots are the #1 CLS source

GPT/AdSense slots render as zero-height divs by default. When the ad creative loads, it pushes surrounding content — this is layout shift. The fix is always to reserve space before the ad loads.

**Always use `min-height` (not `height`) on ad containers:**

```css
/* Correct — reserves smallest configured size, expands for larger ads */
#div-gpt-ad-q1,
#div-gpt-ad-q2,
#div-gpt-ad-q3,
#div-gpt-ad-q4 {
  min-width: 250px;
  min-height: 250px; /* smallest size in the slot's size array */
}
```

**Never use fixed `height`** — it crops larger ads. `min-height` reserves the smallest configured size and gracefully expands.

**Never use JavaScript to reserve space** — JS-driven reservations run after layout, which may already have happened, causing a shift.

### q5 slot sizing

q5 uses standard display sizes `[[336,280],[300,250],[250,250]]` — same `minWidth: 250, minHeight: 250` reservation as q1–q4. No special CLS handling needed.

### Ad request coverage and CLS

Do not add GPT `lazyLoad` margins or a component-level `IntersectionObserver` under the current fill strategy. Request every configured slot on mount and reserve its width/min-height before the request. If a later controlled experiment reintroduces lazy loading, evaluate revenue per session, request coverage, fill/match rate, Active View, and CLS together; do not ship it from an isolated Lighthouse result.

### Font swap CLS

`font-display: swap` alone does **not** prevent layout shift — the swap from fallback to web font still moves text. To hold CLS near zero:

- Use `next/font` — it applies a `size-adjust` / `ascent-override` fallback metric automatically, making the fallback font match the web font's line metrics before the swap.
- Do not claim `swap` "fixes" CLS. It only prevents FOIT (invisible text). CLS from the swap still occurs unless fallback metrics are matched.

### Images and CLS

Always set `width` and `height` on every `<Image>` — the browser reserves the correct aspect-ratio space in the layout before the image loads. Missing dimensions cause a height-from-zero shift when the image arrives.

---

## Third-Party Script Loading Strategies

### `next/script` strategy reference

| Strategy | Timing | Use case |
|---|---|---|
| `beforeInteractive` | Before hydration | Critical polyfills only — never use for ads |
| `afterInteractive` | After hydration (default) | GPT.js, AdSense, Facebook Pixel |
| `lazyOnload` | Browser idle (`requestIdleCallback`) | Low-priority tracking, non-revenue analytics |
| `worker` | Web Worker via Partytown | **App Router: NOT SUPPORTED** |

**`worker` strategy does not work with App Router.** It only works with Pages Router. Do not attempt Partytown integration with App Router fiction sites.

### Recommended strategy per script

```tsx
import Script from 'next/script'

// GPT.js — afterInteractive: must load after hydration, ad slots need the DOM
<Script
  id="gpt"
  src="https://securepubads.g.doubleclick.net/tag/js/gpt.js"
  strategy="afterInteractive"
  crossOrigin="anonymous"
/>

// GPT initialization — inline script after the library
<Script id="gpt-init" strategy="afterInteractive">
  {`
    window.googletag = window.googletag || {cmd: []};
    googletag.cmd.push(function() {
      googletag.setConfig({singleRequest: true});
      googletag.pubads().setForceSafeFrame(true);
      googletag.enableServices();
    });
  `}
</Script>

// AdSense — afterInteractive
<Script
  id="adsense"
  src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXX"
  strategy="afterInteractive"
  crossOrigin="anonymous"
/>

// Facebook Pixel — afterInteractive
<Script id="facebook-pixel" strategy="afterInteractive">
  {`
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', 'PIXEL_ID');
    fbq('track', 'PageView');
  `}
</Script>
```

**Revenue trade-off:** `lazyOnload` delays ad requests, which reduces ad fill and revenue. For display ad monetization, use `afterInteractive` for GPT/AdSense. Mitigate the INP/TBT cost with `scheduler.yield()` in your ad initialization code (see INP section).

### `@next/third-parties` for GTM/GA4

For Google Analytics and GTM, prefer the Chrome Aurora / Vercel maintained package over raw `next/script`:

```bash
pnpm add @next/third-parties
```

```tsx
import { GoogleTagManager, GoogleAnalytics } from '@next/third-parties/google'

// In layout.tsx
<GoogleTagManager gtmId="GTM-XXXXX" />
<GoogleAnalytics gaId="G-XXXXX" />
```

This does not yet cover GPT.js or AdSense — use `next/script` directly for those.

---

## Images

Book covers are the heaviest assets on the home and detail pages.

- Target < 80KB per cover at display size (typically 160×240px on mobile).
- Always set `width` and `height` on `<Image>` to prevent CLS during load.
- Use `loading="lazy"` for all below-fold covers on the home page.
- Use `priority` (or `fetchPriority="high"` + `loading="eager"` on Next.js 16+) on the first visible cover only.
- Ship covers and illustrations as lossy WebP — no `<picture>`/JPEG fallback needed (WebP is supported by every modern browser).
- CSS cover placeholders are acceptable when no image is provided. They must use flat color or subtle texture, not heavy gradients or box shadows.

### Cover compression (B5 step)

AI-generated covers are PNG and typically 400–800 KB. Convert to lossy **WebP q82** — this consistently brings covers to ~50–60 KB with no visible loss at display size. Prefer `cwebp`, fall back to Pillow:

```bash
mkdir -p public/covers
for f in public/covers/*.png; do
  [ -f "$f" ] || continue
  slug="$(basename "$f" .png)"
  out="public/covers/${slug}.webp"
  if command -v cwebp &>/dev/null; then
    cwebp -quiet -q 82 "$f" -o "$out"
  else
    python3 -c "from PIL import Image; im=Image.open('$f'); im.save('$out','webp',quality=82,method=6)"
  fi
  rm -f "$f"
done
```

**Never use lossless WebP** — on photographic covers it is ~3× larger than the source PNG. After conversion, ensure all `cover` paths in `src/lib/books.ts` use `.webp` and rebuild.

### `placeholder="blur"` for progressive loading

For covers loaded from static paths (not static imports), generate a tiny blurDataURL at build time:

```typescript
// Generate a 10×15px base64 WebP — ~20 bytes, sufficient for a blur placeholder
import sharp from 'sharp'

async function genBlur(coverAbsPath: string): Promise<string> {
  const buf = await sharp(coverAbsPath)
    .resize(10)
    .webp({ quality: 40 })
    .toBuffer()
  return `data:image/webp;base64,${buf.toString('base64')}`
}
```

Store the blurDataURL in `books.ts` alongside the cover path and pass it to `<Image>`:

```tsx
<Image
  src={book.cover}
  placeholder="blur"
  blurDataURL={book.blurDataURL}
  width={160}
  height={240}
  sizes="(max-width: 480px) calc(50vw - 24px), 160px"
  loading="lazy"
  alt={book.title}
/>
```

**Do not use a large blurDataURL** (e.g., full-res base64 of the original image). A 50KB blurDataURL is inlined into HTML and hurts more than no placeholder.

### AVIF vs WebP

Next.js on Vercel automatically serves AVIF (25–70% smaller than JPEG/PNG) when the browser supports it, then WebP, then original. This is handled transparently by the Image Optimization API when deploying to Vercel without `output: 'export'`. No code change required.

For static export (pre-built images), stick with the cwebp WebP pipeline — AVIF encoding is 5–10× slower and the savings at cover display sizes are less significant.

### Static export image limitation

When using `output: 'export'`, the Next.js Image Optimization API (`/_next/image`) does not exist — it requires a server. Two options:

**Option 1 — `unoptimized: true` (recommended):** Pass pre-built WebP files through without re-processing. Works correctly with the cwebp build pipeline.

```javascript
// next.config.js — for static hosts (GitHub Pages, Cloudflare Pages static, etc.)
module.exports = {
  output: 'export',
  trailingSlash: true,
  images: { unoptimized: true },
}
```

**Option 2 — `next-image-export-optimizer`:** Generates responsive srcset variants and blurDataURL at build time. Automates the manual cwebp step but adds setup complexity.

**For Vercel deployment (not static export):** Do NOT set `output: 'export'` and do NOT set `unoptimized: true`. Let the Image Optimization API handle format conversion and responsive serving. Recommended `next.config.js` for Vercel:

```javascript
module.exports = {
  // No output: 'export' — Vercel handles image optimization automatically
  images: {
    formats: ['image/avif', 'image/webp'],
  },
}
```

---

## Fonts

- Prefer system font stacks for body text. Do not load a web font for body reading — system stacks render faster and are often better for CJK.
- On Next.js, load any display font (titles, logo) via `next/font` instead of a CDN `<link>`. `next/font` self-hosts Google Fonts as static assets served from your own deployment domain — the browser never requests Google at runtime, so no `preconnect` is needed and there is no third-party dependency or GDPR exposure. A failed font download fails the build rather than silently falling back to the Google CDN.
- `font-display: swap` alone does **not** prevent layout shift — the swap from fallback to web font still moves text and counts against CLS. To actually hold CLS near zero, use `next/font` (it applies a size-adjusted fallback metric automatically) or define a fallback with matching `size-adjust`/`ascent-override`. Do not claim swap "fixes" CLS.
- Subset any loaded font to the characters actually used (Latin, CJK range as appropriate). `next/font` with `subsets: ['latin']` handles this.
- Never load a CJK web font for body text on mobile. The system stack (Hiragino, Yu Mincho, Noto) is always faster and equally good.
- If a custom reader font is offered as a setting, load it lazily only when the reader selects it.

---

## Chapter Content Loading

- Never bundle all chapter text into the initial HTML or JS payload.
- For static builds: generate one HTML file or JSON file per chapter and navigate between them.
- For SPA/Next.js: lazy-load chapter content when entering the reader route. Do not prefetch every chapter at book-detail load time.
- Prefetch only the next chapter when the reader reaches 80% of the current chapter.
- Avoid loading the full book catalog on a chapter reader page.

### Next.js App Router prefetch behavior

Chapter navigation is the hot path; lean on the framework's native prefetching rather than rolling your own.

- **Statically rendered chapter routes** (the `generateStaticParams` + SSG path this skill recommends) are fully prefetched by `<Link>` when they enter the viewport, and cached client-side for ~5 minutes by default. This is what makes prev/next feel instant — no extra code needed.
- **Dynamically rendered chapter routes** are *not* prefetched at all unless a `loading.js` boundary exists, in which case only the shell up to that boundary is prefetched. If your reader must be dynamic, add a `loading.tsx` so the layout/skeleton still prefetches. Prefer SSG to avoid this entirely.
- **Sibling navigation** (chapter N → N+1) reuses the shared parent layout and only fetches the changed leaf segment. Keep the reader chrome (header, nav, settings) in a parent `layout.tsx` so it is not re-fetched on every page turn.
- Next.js maintains a prioritized prefetch queue: links in the viewport first, then links showing hover/touch intent, and links scrolled off-screen are discarded rather than queued forever. A book-detail page with hundreds of chapter links therefore will not thrash the network — but still avoid rendering a 1000-link catalog without virtualization.

### Scroll-triggered prefetch at 80% (implementation)

For the next chapter, trigger `router.prefetch()` when the reader reaches 80% of the current chapter content using `IntersectionObserver`:

```tsx
// src/components/ScrollPrefetch.tsx
'use client'
import { useRouter } from 'next/navigation'
import { useEffect, useRef } from 'react'

interface Props {
  nextChapterHref: string | null
}

export function ScrollPrefetch({ nextChapterHref }: Props) {
  const router = useRouter()
  const sentinelRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const sentinel = sentinelRef.current
    if (!sentinel || !nextChapterHref) return

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          router.prefetch(nextChapterHref)
          observer.disconnect() // prefetch once, stop watching
        }
      },
      { threshold: 0 }
    )
    observer.observe(sentinel)
    return () => observer.disconnect()
  }, [nextChapterHref, router])

  // Placed at 80% of the chapter content container (container must be position: relative)
  return (
    <div
      ref={sentinelRef}
      style={{ position: 'absolute', top: '80%', height: 1 }}
      aria-hidden="true"
    />
  )
}
```

Place `<ScrollPrefetch nextChapterHref={nextHref} />` inside the chapter content container.

### Disable prefetch on large chapter lists

If a book detail page shows all 50+ chapter links, prevent viewport-triggered prefetch from hitting the network for all of them simultaneously:

```tsx
// In the chapter list — disable auto-prefetch; hover intent will still trigger it
<Link href={chapterHref} prefetch={false}>
  {chapterTitle}
</Link>
```

### Side-effect isolation during prefetch

Do not put analytics events (pageview tracking, scroll depth) directly in page/layout components — they fire during prefetch, not just on actual navigation. Wrap them in `useEffect` inside a client component so they only run in the browser after the route actually renders.

---

## JavaScript Bundle

### App Router code splitting model

React Server Components (RSC) are automatically excluded from the browser JS bundle — they never ship JavaScript to the client. Only `'use client'` components are included. This means a chapter reader page with the navigation in RSC and only the theme toggle as a client component has a very small initial JS footprint.

**Bundle size targets:**

| Budget | Threshold | Notes |
|---|---|---|
| Initial JS | < 150KB gzipped | Good; web.dev recommendation for 4G/3G mobile |
| Initial JS | < 200KB gzipped | Maximum acceptable |
| Total page weight | < 600KB | HTML + CSS + images + initial JS |
| Third-party scripts | ≤ 5 resources | GPT, AdSense, Pixel, Vercel SI, GA = 5 |

### Bundle analyzer setup

```bash
pnpm add -D @next/bundle-analyzer
```

```javascript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})
module.exports = withBundleAnalyzer({ /* existing config */ })
```

```bash
ANALYZE=true pnpm build
# Opens client.html, edge.html, nodejs.html — inspect the treemap for bloat
```

### Dynamic imports for non-critical client components

```tsx
import dynamic from 'next/dynamic'

// Reader settings panel — only needed when user opens it
const ReaderSettings = dynamic(() => import('./ReaderSettings'), {
  ssr: false,  // excludes from SSR bundle; creates a separate JS chunk
  loading: () => <div className="h-32 animate-pulse bg-base-200 rounded" />,
})
```

`ssr: false` creates a separate JS chunk that only downloads when the component first renders, not on initial page load.

### Common bundle bloat sources

- **Lodash without tree-shaking**: import `{ debounce }` from `lodash-es`, not `import _ from 'lodash'`
- **Moment.js**: replace with `date-fns` or native `Intl.DateTimeFormat`
- **Heavy icon libraries**: import individual SVGs, not an entire icon pack
- **DaisyUI**: CSS-only at runtime (zero JS), but Tailwind `content` config must be correct for purging
- **React runtime**: ~45KB gzipped — unavoidable; accept it as the baseline
- Defer any script that is not needed for first paint
- Do not load analytics, chat widgets, or ad scripts on a prototype unless the user explicitly asks

---

## CSS

- Inline critical above-the-fold CSS (reader background, font size, body text color).
- Tailwind: configure `content` paths correctly to eliminate unused utility classes.
- Reader theme switching must use DaisyUI `data-theme` value updates, not class-swap-triggered reflows.
- Avoid layout-triggering animations (avoid animating `width`, `height`, `top`, `left`). Use `transform` and `opacity` only.

---

## Caching

### Static asset cache headers

```json
// vercel.json — covers and illustrations are content-addressed, cache 1 year
{
  "headers": [
    {
      "source": "/(covers|illustrations)/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }]
    },
    {
      "source": "/_next/static/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }]
    }
  ]
}
```

### HTML page cache

```
Cache-Control: public, max-age=3600, stale-while-revalidate=86400
```

SSG HTML files are safe to cache for 1 hour (3600s) with a 24-hour stale-while-revalidate window. Vercel sets this automatically for SSG pages.

### Client-side prefetch cache

Next.js App Router caches prefetched pages client-side for ~5 minutes. Chapter navigation reuses this cache — no network request on prev/next within a 5-minute reading session.

---

## Real User Monitoring

### web-vitals library

```bash
pnpm add web-vitals
```

Use the attribution build to get element-level debug data:

```typescript
// src/lib/vitals.ts
import { onCLS, onINP, onLCP } from 'web-vitals/attribution'

function sendVital(metric: Parameters<Parameters<typeof onLCP>[0]>[0]) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating,  // 'good' | 'needs-improvement' | 'poor'
    delta: metric.delta,
    id: metric.id,
    attribution: metric.attribution,
    page: location.pathname,
  })
  // sendBeacon is non-blocking — fires on page hide without delaying navigation
  navigator.sendBeacon('/api/vitals', body)
}

export function initVitals() {
  onLCP(sendVital)
  onINP(sendVital)
  onCLS(sendVital)
}
```

### Key attribution fields for fiction site debugging

| Metric | Useful attribution fields | What they reveal |
|---|---|---|
| LCP | `target`, `url`, `timeToFirstByte`, `resourceLoadDelay`, `resourceLoadDuration`, `elementRenderDelay` | Which cover image is slow; is it TTFB or image fetch? |
| INP | `inputDelay`, `processingDuration`, `presentationDelay`, `interactionTarget`, `longAnimationFrameEntries` | Which element caused poor INP; is it ad scripts (input delay) or handler code (processing)? |
| CLS | `largestShiftTarget`, `largestShiftValue` | Which element shifted; usually an ad slot div |

If `interactionTarget` for a poor INP interaction points to an ad slot div → fix: `scheduler.yield()` in ad initialization. If it points to a chapter navigation button → fix: reduce React re-renders in the reader.

### Vercel Speed Insights vs. web-vitals library

| | Vercel Speed Insights | web-vitals library |
|---|---|---|
| Setup | Zero-config component | Custom reporting endpoint |
| Data | p75 per route in Vercel dashboard | Full distribution + attribution |
| GDPR | No cookies, no cross-site | No cookies, no cross-site |
| Use for | Trend monitoring, regression alerts | Root-cause investigation |

Use both: Speed Insights for monitoring, web-vitals for debugging regressions.

---

## Performance Budgets & CI Enforcement

### Lighthouse CI

```bash
pnpm add -D @lhci/cli
```

**`lighthouserc.js`** at the project root:

```javascript
module.exports = {
  ci: {
    collect: {
      staticDistDir: './out',  // for output: 'export' sites
      // For Vercel deployment: use startServerCommand + url instead
      numberOfRuns: 3,         // median of 3 runs for stable scores
    },
    assert: {
      assertions: {
        'categories:performance':          ['error', { minScore: 0.8 }],
        'largest-contentful-paint':        ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift':         ['error', { maxNumericValue: 0.1 }],
        'interaction-to-next-paint':       ['warn',  { maxNumericValue: 200 }],
        'total-blocking-time':             ['warn',  { maxNumericValue: 300 }],
        'first-contentful-paint':          ['warn',  { maxNumericValue: 1800 }],
      },
    },
    upload: { target: 'temporary-public-storage' },
  },
}
```

**GitHub Actions workflow:**

```yaml
name: Lighthouse CI
on: [push, pull_request]
jobs:
  lhci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: pnpm install && pnpm build
      - run: pnpm dlx @lhci/cli autorun
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
```

### Bundle size CI with `size-limit`

```bash
pnpm add -D @size-limit/preset-app size-limit
```

```json
// package.json
"size-limit": [
  { "path": ".next/static/chunks/main-*.js", "limit": "50 KB", "gzip": true },
  { "path": ".next/static/chunks/pages/_app-*.js", "limit": "80 KB", "gzip": true }
],
"scripts": {
  "size": "size-limit"
}
```

Add `pnpm size` to the CI pipeline after the build step. Fails the build if a PR inflates a chunk past budget.

---

## Offline / PWA

Implement a Service Worker only if the user asks for PWA or offline reading support.

When implementing:
- Cache the site shell (HTML, CSS, core JS) on install.
- Cache visited chapters on fetch, using a cache-first strategy for chapter content.
- Cache the home page and last-visited book detail.
- Show an offline fallback page for uncached routes.
- Do not cache chapter content speculatively (pre-cache the whole book) unless the user asks — it wastes mobile data.

---

## Vercel Deployment Checklist

Five standards every fiction site deployed to Vercel must satisfy before going live.

### 1. sitemap.ts + robots.ts

Use Next.js App Router's native metadata route files — no third-party package needed.

Place both files directly under `src/app/`:

**`src/app/sitemap.ts`** — imports the books array, generates URLs for every book detail page and every chapter page. All URLs end with `/` (matches `trailingSlash: true` in next.config):

```ts
import { MetadataRoute } from 'next'
import { books } from '@/lib/books'

export default function sitemap(): MetadataRoute.Sitemap {
  const base = 'https://your-domain.com'
  const staticPages: MetadataRoute.Sitemap = [
    { url: base + '/', changeFrequency: 'weekly', priority: 1.0 },
    { url: base + '/about/', changeFrequency: 'yearly', priority: 0.3 },
    { url: base + '/privacy/', changeFrequency: 'yearly', priority: 0.2 },
    { url: base + '/terms/', changeFrequency: 'yearly', priority: 0.2 },
    { url: base + '/contact/', changeFrequency: 'yearly', priority: 0.2 },
  ]
  const bookPages: MetadataRoute.Sitemap = books.flatMap(book => [
    { url: `${base}/book/${book.slug}/`, changeFrequency: 'weekly' as const, priority: 0.8 },
    ...Array.from({ length: book.chapterCount }, (_, i) => ({
      url: `${base}/book/${book.slug}/chapter/${i + 1}/`,
      changeFrequency: 'monthly' as const,
      priority: 0.6,
    })),
  ])
  return [...staticPages, ...bookPages]
}
```

**`src/app/robots.ts`** — points search engines at `/sitemap.xml`:

```ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: '*', allow: '/' },
    sitemap: 'https://your-domain.com/sitemap.xml',
  }
}
```

Both files are automatically served at `/sitemap.xml` and `/robots.txt` by the framework — no `next.config` change required.

### 2. vercel.json Cache Headers + Security

**`vercel.json`** at the project root:

```json
{
  "headers": [
    {
      "source": "/(covers|illustrations)/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ],
  "rewrites": [
    { "source": "/covers/:file.json", "destination": "/___blocked___" },
    { "source": "/illustrations/:book/:file.json", "destination": "/___blocked___" }
  ]
}
```

**Cache headers**: covers and illustrations are content-addressed and never change after upload — one combined pattern caches both at the CDN edge for one year, eliminating origin bandwidth on repeat visits.

**Rewrites (security)**: each image generation also produces a `.json` sidecar that contains the full AI prompt. Rewriting `.json` requests to a non-existent path causes Vercel to return a natural 404, blocking prompt exposure without affecting image delivery. The two patterns cover the flat cover structure (`/covers/{slug}.json`) and the nested illustration structure (`/illustrations/{book}/{file}.json`).

### 3. CookieBanner

Each site needs its own cookie-consent banner with a site-specific localStorage key so consent state is isolated per domain. Choose the variant based on the site's primary market:

| Variant | When to use | Key format |
|---------|-------------|------------|
| **Basic** | Non-EU/UK markets (US, LatAm, etc.) — Reject + Accept buttons | `{prefix}-cookie-consent` |
| **GDPR** | EU / UK markets — Accept All / Reject All / Manage categories | `{prefix}-cookie-consent-v2` |

Key prefix convention: two-letter abbreviation of the site slug (e.g. `vt` for velvet-throne, `mf` for midnight-fable, `fe` for fuego-eterno, `lp` for london-pages, `wr` for wildfire-reads).

The banner is the preference surface, not the enforcement mechanism. Every analytics or advertising tag must explicitly consume the stored choice. Do not ship Reject / Accept controls that only dismiss the banner while tracking continues.

- A notice-only design must not label its action as Reject or claim that tracking stops.
- An enforced Meta opt-in design must not preconnect to Meta, request `fbevents.js`, initialize `fbq`, emit events, or render a `noscript` tracking image before consent. Accept initializes immediately and sends one current-page `PageView`; reject and returning-rejected states send nothing.
- Google ad personalization remains a separate CMP concern. Rejecting Meta measurement does not automatically disable AdX/AdSense; the banner copy must name the exact category it controls.
- Store the choice and dispatch a site-specific consent-change event so Pixel, route, and chapter-event owners update from one source of truth. All event helpers must re-check the stored choice before sending.

---

**Variant A — Basic** (non-EU/UK markets):

Adapt text to the site language. English template: `"{Site Name} uses cookies to personalise content and ads."` Spanish template: `"{Nombre} utiliza cookies para personalizar contenido y anuncios."`

Provide both **Reject** and **Accept** buttons. Rejecting Meta measurement may still allow non-personalized ads, but it must block Meta initialization and events when the banner promises Meta opt-in.

```tsx
'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'

const CONSENT_KEY = '{prefix}-cookie-consent'
const CONSENT_EVENT = '{prefix}-consent-change'

export default function CookieBanner() {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    try {
      if (!localStorage.getItem(CONSENT_KEY)) setVisible(true)
    } catch { setVisible(true) }
  }, [])

  if (!visible) return null

  function accept() {
    try { localStorage.setItem(CONSENT_KEY, '1') } catch {}
    window.dispatchEvent(new CustomEvent(CONSENT_EVENT, { detail: '1' }))
    setVisible(false)
  }

  function reject() {
    try { localStorage.setItem(CONSENT_KEY, '0') } catch {}
    window.dispatchEvent(new CustomEvent(CONSENT_EVENT, { detail: '0' }))
    setVisible(false)
  }

  return (
    <div className="fixed bottom-0 left-0 right-0 z-[9999] bg-base-200 border-t border-base-300 shadow-lg px-4 py-3 flex flex-col sm:flex-row items-center gap-3">
      <p className="text-sm text-base-content flex-1 text-center sm:text-left">
        {/* EN: "{Site Name} uses cookies to personalise content and ads." */}
        {/* ES: "{Nombre} utiliza cookies para personalizar contenido y anuncios." */}
        {'{Site Name}'} uses cookies to personalise content and ads.{' '}
        <Link href="/privacy" className="underline hover:text-primary">Learn more</Link>
      </p>
      <div className="flex items-center gap-2 shrink-0">
        <button
          onClick={reject}
          className="px-4 py-2 rounded text-sm font-medium border border-base-300 hover:border-primary hover:text-primary transition-colors"
        >
          {/* EN: Reject  ES: Rechazar */}
          Reject
        </button>
        <button
          onClick={accept}
          className="bg-primary text-primary-content px-4 py-2 rounded text-sm font-medium hover:opacity-90 transition-opacity"
        >
          {/* EN: Accept  ES: Aceptar */}
          Accept
        </button>
      </div>
    </div>
  )
}
```

---

**Variant B — GDPR** (EU / UK markets):

Three-button layout (Accept All / Reject All / Manage) with a category panel. Stores structured JSON so categories can be read later. The `v2` suffix in the key intentionally invalidates any legacy `v1` consent stored by an older Basic banner on the same domain.

```tsx
'use client'
import { useEffect, useState } from 'react'

type ConsentData = { analytics: boolean; advertising: boolean }

const KEY = '{prefix}-cookie-consent-v2'

function saveConsent(c: ConsentData) {
  try { localStorage.setItem(KEY, JSON.stringify(c)) } catch {}
  window.dispatchEvent(new CustomEvent('{prefix}-consent-change', { detail: c }))
}

export default function CookieBanner() {
  const [visible, setVisible] = useState(false)
  const [managing, setManaging] = useState(false)
  const [analytics, setAnalytics] = useState(false)
  const [advertising, setAdvertising] = useState(false)

  useEffect(() => {
    try {
      if (!localStorage.getItem(KEY)) setVisible(true)
    } catch { setVisible(true) }
  }, [])

  if (!visible) return null

  return (
    <div className="fixed bottom-0 left-0 right-0 z-[9999] bg-base-200 border-t border-base-300 shadow-lg">
      {!managing ? (
        <div className="max-w-4xl mx-auto px-4 py-4 flex flex-col sm:flex-row items-start sm:items-center gap-4">
          <p className="text-sm text-base-content/80 flex-1">
            {'{Site Name}'} uses cookies to personalise content and advertisements, and to analyse our traffic.{' '}
            <a href="/privacy" className="text-primary underline hover:opacity-80">Privacy Policy</a>
          </p>
          <div className="flex items-center gap-2 flex-shrink-0 flex-wrap">
            <button onClick={() => setManaging(true)}
              className="px-4 h-9 rounded-lg border border-base-300 text-sm text-base-content/70 font-medium hover:border-primary hover:text-primary transition-colors">
              Manage
            </button>
            <button onClick={() => { saveConsent({ analytics: false, advertising: false }); setVisible(false) }}
              className="px-4 h-9 rounded-lg border border-base-300 bg-base-100 text-sm text-base-content font-semibold hover:bg-base-300 transition-colors">
              Reject All
            </button>
            <button onClick={() => { saveConsent({ analytics: true, advertising: true }); setVisible(false) }}
              className="px-5 h-9 rounded-lg bg-primary text-primary-content text-sm font-semibold hover:opacity-90 transition-opacity">
              Accept All
            </button>
          </div>
        </div>
      ) : (
        <div className="max-w-4xl mx-auto px-4 py-4 flex flex-col gap-4">
          <p className="text-sm font-semibold text-base-content">Cookie Preferences</p>
          <div className="flex flex-col divide-y divide-base-300">
            <div className="flex items-center justify-between gap-4 py-3">
              <div>
                <p className="text-sm font-medium text-base-content">Necessary</p>
                <p className="text-xs text-base-content/60 mt-0.5">Required for the site to function. Always active.</p>
              </div>
              <span className="text-xs text-base-content/40 flex-shrink-0">Always on</span>
            </div>
            <div className="flex items-center justify-between gap-4 py-3">
              <div>
                <p className="text-sm font-medium text-base-content">Analytics</p>
                <p className="text-xs text-base-content/60 mt-0.5">Helps us understand how visitors use the site.</p>
              </div>
              <input type="checkbox" checked={analytics} onChange={e => setAnalytics(e.target.checked)}
                className="checkbox checkbox-primary checkbox-sm flex-shrink-0" />
            </div>
            <div className="flex items-center justify-between gap-4 py-3">
              <div>
                <p className="text-sm font-medium text-base-content">Advertising</p>
                <p className="text-xs text-base-content/60 mt-0.5">Enables personalised ads. Declining shows non-personalised ads only.</p>
              </div>
              <input type="checkbox" checked={advertising} onChange={e => setAdvertising(e.target.checked)}
                className="checkbox checkbox-primary checkbox-sm flex-shrink-0" />
            </div>
          </div>
          <div className="flex justify-end gap-2">
            <button onClick={() => setManaging(false)}
              className="px-4 h-9 rounded-lg border border-base-300 text-sm text-base-content/70">Back</button>
            <button onClick={() => { saveConsent({ analytics, advertising }); setVisible(false) }}
              className="px-5 h-9 rounded-lg bg-primary text-primary-content text-sm font-semibold hover:opacity-90 transition-opacity">
              Save Preferences
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
```

---

Import and render `<CookieBanner />` at the end of `<body>` in `src/app/layout.tsx`:

```tsx
import CookieBanner from '@/components/CookieBanner'
// ...
<body>
  {children}
  <CookieBanner />
</body>
```

### 4. OG Image

Three-layer requirement. Every layer must be covered before launch:

| Layer | Where | Image | URL form |
|---|---|---|---|
| **Homepage** | `layout.tsx` openGraph | `logo-light.png` (512×512) | Absolute (`https://`) |
| **Book detail** | `book/[slug]/page.tsx` generateMetadata | `book.cover` (848×1280) | Relative OK — resolved by `metadataBase` |
| **Chapter** | `book/[slug]/chapter/[n]/page.tsx` generateMetadata | `book.cover` (848×1280) | Relative OK — resolved by `metadataBase` |

**`metadataBase` is the key**: set it once in `layout.tsx` with the real domain, and all relative OG image URLs in child pages resolve to absolute automatically. No `siteUrl` env var needed.

**`src/app/layout.tsx`** — homepage fallback (logo-light, absolute URL):

```ts
export const metadata: Metadata = {
  metadataBase: new URL('https://your-domain.com'),  // hardcode real domain
  openGraph: {
    siteName: 'Your Site Name',
    type: 'website',
    images: [{ url: 'https://your-domain.com/logo-light.png', width: 512, height: 512, alt: 'Your Site Name' }],
  },
}
```

**`src/app/book/[slug]/page.tsx`** and **`src/app/book/[slug]/chapter/[n]/page.tsx`** — book cover (relative path resolved by metadataBase):

```ts
openGraph: {
  title: book.title,
  description: book.description,
  images: [{ url: book.cover, width: 848, height: 1280, alt: book.title }],
  type: 'book',  // or 'article' for chapter pages
  siteName: 'Your Site Name',
},
twitter: { card: 'summary_large_image' },
```

**Chapter page without explicit OG image** is acceptable — Next.js falls back to the root layout's `logo-light.png`. But setting `book.cover` on chapter pages is preferred for better FB/Twitter previews.

Rules:
- `logo-light.png` must exist at `public/logo-light.png`. Dimensions: 512×512 minimum, square is safe for all platforms.
- `book.cover` is `/covers/{slug}.webp` — a relative path. With `metadataBase` set, Next.js outputs an absolute URL in the built HTML. Verify by grepping `og:image` in `out/` after build.
- The book cover (portrait 2:3, 848×1280) doubles as the FB link preview for book and chapter pages — no separate OG image asset needed.

### 5. Speed Insights + Analytics

Vercel Analytics tracks page views and visitor trends. It is GDPR-friendly (no cookies, no cross-site tracking) and complements GA4 rather than replace it. Vercel Speed Insights is reserved for the primary paid-traffic test site (`midnight-fable`) because adding a domain to a Vercel project for Speed Insights can incur billing on non-Pro plans. New sites should wire Analytics only unless the user explicitly asks for Speed Insights.

**Install Analytics only (default):**

```bash
pnpm add @vercel/analytics
```

**`src/app/layout.tsx`** — import and render `Analytics` inside `<body>`:

```tsx
import { Analytics } from '@vercel/analytics/react'
// ...
<body>
  {children}
  <CookieBanner />
  <Analytics />
</body>
```

The component injects a minimal script that runs after the page is interactive — it does not block first paint or affect LCP.

**Speed Insights (optional, only when explicitly requested):**

If the user asks for Speed Insights on a specific site, install and import it separately:

```bash
pnpm add @vercel/speed-insights
```

```tsx
import { SpeedInsights } from '@vercel/speed-insights/next'
// ...
<body>
  {children}
  <CookieBanner />
  <SpeedInsights />
  <Analytics />
</body>
```

---

## Pitfall: Internal npm Registry in pnpm Lockfile

If the development machine has a corporate or internal npm registry set as the global pnpm registry (e.g. `registry.corp.example`), pnpm bakes the registry's tarball URLs into `pnpm-lock.yaml`. Vercel's CI cannot reach an internal network and the build fails with `ERR_SOCKET_TIMEOUT` when fetching packages.

**Symptom**: Vercel build log shows errors like:
```
WARN GET https://registry.corp.example/@vercel/analytics/-/analytics-x.x.x.tgz
ERR_SOCKET_TIMEOUT ... Socket timeout
Error: Command "pnpm install" exited with 1
```

**Fix**: add a project-level `.npmrc` at the site root to override the global registry, then regenerate the lockfile:

```ini
# .npmrc
registry=https://registry.npmjs.org
```

```bash
rm pnpm-lock.yaml
pnpm install --registry https://registry.npmjs.org
```

The `--registry` flag is required because pnpm's own global config (`pnpm config set registry`) takes precedence over `.npmrc`; passing it on the CLI overrides everything. Commit both `.npmrc` and the regenerated `pnpm-lock.yaml`. The lockfile should contain only `integrity` hashes, not `tarball` URLs pointing to the internal host.
