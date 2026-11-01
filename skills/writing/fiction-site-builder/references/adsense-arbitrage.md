# AdSense / AdX Arbitrage Playbook (Facebook Traffic)

Load this reference whenever the site's purpose is **paid-traffic monetization** — i.e. buying traffic on Facebook (Meta) ads and monetizing reading sessions with AdSense + AdX. This is the default business model for every site built by this skill (see AGENTS.md ad accounts). Apply it during Phase B1–B6 and at content/cover direction time.

> **One sentence:** the site is a machine that converts a Facebook click (cost) into multiple viewable ad impressions across a reading session (revenue). Everything below exists to widen that margin **without** getting the ad account or the AdSense account banned.

---

## 0. Profit model — what we are actually optimizing

```
Profit per visit = (viewable session RPM)  ×  (pageviews per session) / 1000  −  Facebook CPC  −  overhead
```

The build can move two of the three levers directly:

| Lever | Owner | Where this skill helps |
|---|---|---|
| Facebook CPC in | campaign / creative / targeting | keep landing page approvable (cheap, compliant) — see §1 |
| **Pageviews per session** | the site | chapter model, pagination, cliffhangers, prefetch — see §2 |
| **Viewable session RPM** | the site | ad layout, density, request coverage, viewability, refresh — see §3 |

A site is only profitable when `session RPM × PV/session` clears the CPC. Two below-average levers kill the margin even if the third is great. Treat layout and pageview depth as **revenue engineering**, not decoration.

---

## 1. Account-survival guardrails (READ FIRST — non-negotiable)

A banned Facebook ad account or a disabled AdSense account ends the business. These rules **override every aesthetic, allure, or CTR suggestion anywhere else in this skill.**

### 1.1 Content safety (Facebook + AdSense both scan the landing page)

§0 floor: per `cover-allure-elements.md §0` — no explicit content (nipples/genitals/sex acts). Suggestive allure fully allowed; push it. The site/ad creative is crawled by Meta and AdSense; cloaking is a permanent-ban offense.

### 1.2 No cloaking, no bridge/doorway pages

Showing FB's crawler one page and users another, or sending paid traffic to a thin redirect page, is detected and causes **permanent** account loss. The page the ad points to is the page users and crawlers both get.

### 1.3 Inventory-value rules (AdSense)

- Do **not** run more ad area than publisher content. Keep **ad pixels < 30% of content pixels** per screen.
- No low-value / replicated / auto-generated thin pages. **Every paginated screen must carry substantial original prose** (see §2.2) — pagination purely to multiply ad slots is a policy violation.
- Ads must not push content below the fold on mobile (FB low-quality + Google page-experience penalty).

### 1.4 No deceptive placement / no click encouragement

- Ads must never be styleable-mistakable for the "Next →" button, TOC, or nav. Keep a clear visual + spatial gap between any ad and the Next control.
- Never label, arrow, or arrange content to push ad clicks. No "click here", no images adjacent to ads that bait clicks.

### 1.5 Geographic IVT Protection (Mainland China)

Google AdX and AdSense are both blocked in mainland China. If CN IPs reach the site:

- Ad scripts load and attempt requests — none succeed.
- Google's IVT detector sees ad requests with zero ad interactions → raises IVT flags.
- Facebook Pixel fires PageView but conversion events never follow → FB algorithm penalizes the landing page as low-quality traffic.

**Action: block CN IPs at the edge.** See `geo.md` → Mainland China Policy for the Vercel
middleware implementation. This is not about excluding Chinese readers — the content is in
English/Spanish and the ad accounts depend on US/AU/UK/LATAM traffic. CN traffic is pure
liability with no revenue upside.

---

### 1.6 Consent + trust pages (AdSense approval + FB quality)

- A Google-certified **CMP / cookie-consent** is required to serve personalized ads in EEA/UK; without it demand drops to non-personalized only.
- Site MUST have: **Privacy Policy, Terms, About, Contact** (and a Cookie notice). AdSense approval fails and FB flags "low quality" without them. Link them in the footer of every page.

---

## 2. Pageviews per session — the #1 arbitrage lever

The chapter model already multiplies pageviews. Push it harder (within §1.3):

### 2.1 Forward momentum (already core to this skill)

- Cliffhanger chapter endings (Zeigarnik effect) — see `story-long-write.md` pacing. The unresolved loop is what makes the next pageview involuntary.
- Forward-only nav (no Previous), vivid Next button — see `reader-ux.md`.
- **Full-page navigation on chapter change** (`window.location.href`, not SPA) so AdSense/AdX reinitialize and count a fresh pageview with fresh impressions — already required in `reader-ux.md`.
- Prefetch the next chapter at ~80% scroll so the next pageview feels instant.

### 2.2 In-chapter pagination — not recommended

Splitting one chapter into sub-pages (`/chapter/3/p/1`, `/chapter/3/p/2`) creates URL-level confusion: the reader can't tell if they're on page 2 of a chapter or chapter 2 of a book. The disruption to reading flow causes more session drop-off than the extra pageview gains. **Do not implement in-chapter pagination.** Use §2.4 instead.

### 2.3 End-of-content continuation

- End of chapter → prominent Next button.
- End of book → "Continue with {next book}" / related-title cards to restart the loop instead of dead-ending.

### 2.4 Alternative session-depth levers (preferred — no UX disruption)

These techniques raise pageviews/session without breaking the reading experience.

**A. Next-chapter teaser below the "Next →" button**

After the chapter hook-out and the primary Next button, render the first 60–80 words of the next chapter in muted text, then a second "Continue reading →" link. The reader has already started reading before they realize they've decided to click. This is the single highest-impact single change for session depth on fiction sites.

```tsx
{next && (
  <div className="next-chapter-teaser">
    <p className="teaser-label">Next: {next.title}</p>
    <p className="teaser-text">{next.openingSnippet}</p>
    <a href={`/book/${slug}/chapter/${next.order}`} className="btn-next-sm">
      Continue reading →
    </a>
  </div>
)}
```

`openingSnippet` = first 2 sentences of the next chapter (strip markdown, plain text, truncate to ~80 words). Compute it at build time in `books.ts` or the content-collections schema. Cut at the last word before the 80-word mark — never in the middle of a sentence.

**B. Chapter position counter in the reader header**

Show `Chapter 3 / 22` in the sticky header. A reader who sees they are 13% through a 22-chapter story is psychologically further from the exit than one who has no frame. This is free: it adds no new components, just text.

**C. End-of-book restart loop**

After the final chapter's hook-out, instead of a dead end, render 2–3 related books (same tone, similar tropes, different title) with cover + first line + "Start reading →". This is the highest-leverage cross-book retention moment: the reader is emotionally warm and has just finished a story, making them more open to starting another than they will be at any other point.

Implementation: in the book-detail page's `BelowFold`, add a `RelatedBooks` component that takes `books.filter(b => b.slug !== currentSlug).slice(0, 3)` and renders them as a row of cards. No recommendation algorithm needed — any 3 books from the same site work. The emotional warmth from finishing does the heavy lifting.

**D. Chapter title list as teaser inventory**

Chapter titles that create forward curiosity ("The Night He Came Back", "What the Contract Didn't Cover") pull readers from the TOC into chapters they might not have arrived at naturally. When the reader scans the chapter list and sees an intriguing title for chapter 7, they read chapter 5 and 6 faster to get there — compressing the session and deepening engagement. This is a writing standard, not a code change (see story-long-write.md §Title Craft).

**Target: ≥ 2.5–4 pageviews per session.** Below ~2 the arbitrage rarely clears CPC.

---

## 3. Ad layout, density & viewability — the RPM lever

Map the AGENTS.md inventory (AdX `q1–q5` via `AdSlot`, AdSense slots 1–5 via `AdsenseSlot`) onto these positions. Layout structure matters more than raw ad count — moving a unit to a better slot can double its CPM; adding a 6th+ unit usually cannibalizes the others.

### 3.1 Placement map

| Position | Viewability | Notes |
|---|---|---|
| Pre-content (above all text, just below header) | **< 30%** | **Avoid.** Paid-traffic users start scrolling immediately — this unit exits the viewport before the 1-second viewability threshold. Moving this slot into content can double its Active View score. |
| After `contentParts[0]` (~20% into content) | 70–90% | **First slot.** Reader has invested ~2 min and is still engaged. Use the normal immediate-mount slot component for both AdSense and AdX. |
| In-content, every N paragraphs after the first break | 65–85% | the workhorse — inside the natural reading path |
| End-of-chapter (after the inline Next/TOC controls) | high | catches the post-navigation pause; keep clear separation so the ad cannot be mistaken for a control (§1.4) |
| Mobile sticky **nav bar** (bottom, `position: fixed`) | — | Nav-only: TOC + Next buttons. No ads in sticky bar. `StickyNav` component; `<main>` uses `pb-sticky-ad` (`calc(82px + env(safe-area-inset-bottom))`). |
| Desktop sticky **side-rail** | high | uses empty side space; never a static sidebar (low viewability) |

### 3.1.1 Per-page loading rule (AdSense and AdX)

**Rule: every configured ad slot requests on component mount. Do not add a custom `IntersectionObserver`, `priority` prop, or viewport-margin lazy branch to either `AdsenseSlot` or `AdSlot`.**

This is the current fill-rate / revenue-per-session default: requesting the complete configured inventory gives every eligible slot a chance to match, avoids observer and scroll-timing failure modes, and keeps the implementation simple. It can reduce Active View for later slots, so judge the strategy with **revenue per session, request coverage, fill/match rate, and Active View together** rather than optimizing one metric in isolation.

```tsx
<AdsenseSlot slot="..." />  {/* immediate on mount */}
<AdsenseSlot slot="..." />  {/* immediate on mount */}
```

**AdX sites**: keep `googletag.setConfig({ singleRequest: true, collapseDiv: "ON_NO_FILL" })`, but do not overstate what it guarantees. Single Request Architecture batches the slots that have already been defined when the first `display()` call executes. Independently mounted React components that each call `defineSlot()` and `display()` immediately improve request coverage, but they do not guarantee that every page slot joins one network request. If deterministic SRA batching becomes a requirement, centralize slot registration so all slots are defined before the first display; treat that as a separate architecture change.

### 3.2 Density ceiling (compliance + diminishing returns)

- **≤ 3–4 ad units per 1,000 words** of chapter content.
- **Ad pixels < 30% of content pixels** per screen (FB + AdSense inventory-value).
- RPM typically peaks around 5 units; beyond that each added unit adds ~2–4% and erodes engagement + page-experience. Cutting the weakest slot often **raises** total RPM.
- **Configured five-slot AdX layout:** when a site has q1–q5 assigned to chapter inventory, render exactly five unique units on every chapter: q4 at the top, q1/q2/q3 after the first three content quarters, and q5 below chapter navigation. There is no chapter 1 exception.
- When adding AdX to an existing reader, replace the chapter rendering sequence as one unit. Do not incrementally append q1–q3 after the prose or copy a legacy same-name `AdSlot` component from another site; use the immediate-mount AdX component in §8.6 and implement the complete five-slot sequence in the same change.
- Never reuse q5 inside a sticky component when it already appears at the bottom of the content flow; duplicate GPT div IDs break slot initialization.
- If a legacy AdX or AdSense reader has fewer configured chapter units, place its existing final unit below chapter navigation instead of adding an unconfigured slot.
- This fixed inventory is an explicit site strategy. Keep the density and ad-area checks above visible as an operational warning, especially for chapters below roughly 1,250 words.
- Avoid a fourth mid-content unit; it sits too close to q5 and adds clutter without meaningful RPM lift.

### 3.3 CLS protection (Core Web Vitals = cheaper FB traffic + SEO)

- Every ad slot wrapper reserves explicit `min-height` / `aspect-ratio` matching the largest expected creative **before** it loads. (AGENTS.md `AdSlot` min sizes already do this for q1–q4; keep it.)
- A jumping layout when an ad loads tanks CLS, raises bounce, and raises effective CPC.

### 3.4 Viewability & refresh

- Target **viewability ≥ 70%** (advertisers bid markedly higher; 40%→70% ≈ +30% RPM). Don't chase 95% at the cost of fill rate.
- Refresh ads only when the unit is **in the viewport** and after **≥ 30s active dwell**. Sticky/anchor units are the safe place to refresh because they stay viewable.
- Never refresh on a hidden tab or an off-screen unit.

**Critical: first in-content ad placement rule.**
The single biggest viewability lever inside chapter prose is WHERE the first in-content ad slot (q1 for AdX / slot 1 for AdSense) appears. This is separate from a configured top unit such as q4, which renders before the chapter 1 cover lead. Two failure modes:

1. **Pre-content placement (worst):** q1 above all prose → user starts scrolling immediately, ad exits viewport in < 1s. Active View score < 30%. This was the historical default; do not repeat it.
2. **Deep-content placement (bad):** first ad at 50%+ of chapter → only readers who finish more than half ever see it. Active View 30–50% on paid traffic.

Rule: place the **first** ad after `contentParts[0]` — the first ~20% of paragraphs (min 3, max 5 paragraphs). At this depth the reader has invested ~2 minutes and is still engaged — first-ad viewability should reach 70–90% vs < 30% pre-content.

Configured five-slot AdX layout: `q4 top → chapter 1 cover lead (chapter 1 only) → chapter title → part[0] → q1 → part[1] → q2 → part[2] → q3 → part[3] → sentinel → chapter nav → q5 bottom`.

AdSense layout (2-part): `part[0] → slot1 → part[1] → slot2`.
AdSense layout (3-part): `part[0] → slot1 → part[1] → slot2 → part[2]`.

Diagnostic signal: if AdX viewability is below 60% and match rate is ≥ 95%, the problem is almost always first-slot placement depth, not fill. Fix the slot position before investigating any other cause.

---

## 4. Facebook side — tracking & landing

### 4.1 Tracking

- **Browser Pixel is the baseline; CAPI is an additive option.** Pixel alone loses signal to iOS/ad-blockers, while CAPI can recover part of it. Never replace or short-circuit the working browser Pixel while adding CAPI. When both send the same event, deduplicate them with the same event ID. Only an explicitly scoped consent migration may gate browser delivery.
- If the site uses App Router / `next/link`, add a client-side route tracker that fires `fbq('track', 'PageView')` only after a genuine pathname change. Initialize `previousPathname` from the current pathname. In an unconditional design, never fire from the tracker's initial mount or a consent-state update because layout owns the first hard-load `PageView`. In an opt-in design, the consent handler sends one current-page `PageView` only on the transition from not-consented to consented; the route effect still handles genuine later path changes only.
- Events to fire: `PageView`, `ViewContent` (chapter open), `ScrollDepth25` / `ChapterRead50` / `ScrollDepth75` (scroll milestones), `ChapterCompleted` (IntersectionObserver on `#chapter-content-end` sentinel — not scroll ratio), and `TimeOnPage20s` / `TimeOnPage30` (20s / 30s setTimeout, independent of scroll) as engaged-session signals. Both dwell events must run inside `ChapterPixel` with identical chapter-only scope, payload, event name, and cleanup behavior; do not implement one in a route-wide tracker.
- Keep every custom event unprefixed across sites. Multiple sites using one Pixel intentionally contribute to the same event stream; use the page URL/domain rule or an event payload field when a report or custom conversion must distinguish a site. Standard events (`PageView`, `ViewContent`) remain unprefixed too.
- Next-chapter controls should fire `fbq('trackCustom', 'NextChapterClick', payload)` before hard navigation. Preserve normal browser behavior for modified clicks, then delay `window.location.href` by about 100–150ms so the Pixel request has time to leave the page.
- Optimize the FB campaign toward the **engaged/value event**, not raw landing PageView — that is what trains delivery toward profitable readers.
- UTM-tag every campaign; keep `campaign → landing chapter` mapping for ROAS attribution.

#### 4.1.1 Production Pixel regression contract

This contract comes from a production regression: replacing the fixed `layout.tsx` bootstrap with a consent-aware client wrapper left fresh visitors without `fbq`; the shared helper then suppressed `PageView`, `ViewContent`, reading-depth, dwell, and next-chapter events together. Removing the CAPI transport did not restore the browser Pixel because initialization had already moved behind the new gate.

Before editing Pixel, CAPI, consent, cookies, or route analytics on an existing site, capture these invariants from the code and preserve them unless the user explicitly requests a migration:

- the real Pixel ID in `fbq('init', ...)` and, for an unconditional design, the matching `noscript` URL;
- who owns the first `PageView` (normally the layout bootstrap);
- whether each navigation path is a hard document load or a true SPA pathname change;
- every browser event emitter (`ChapterPixel`, `HardLink`, route tracker, and any helper);
- current consent behavior for fresh, accepted, rejected, and returning visitors;
- exact event names. Standard and custom event names remain unprefixed across every site; do not reintroduce a site prefix during unrelated work.

Implementation constraints:

1. Keep one stable browser bootstrap or loader in `layout.tsx`. In the default unconditional design, load `fbevents.js`, initialize the real Pixel ID once, send one hard-load `PageView`, and retain a matching `noscript` fallback. In an explicitly approved opt-in design, define the loader inline but do not request `connect.facebook.net`, initialize `fbq`, send events, preconnect, or render a `noscript` tracking image before consent. Returning accepted visitors initialize and send one `PageView` from layout; fresh acceptance initializes and sends one current-page `PageView` from the consent handler.
2. CAPI must be additive. A CAPI timeout, missing endpoint, consent helper, or transport error must not prevent the browser `fbq` call. Removing CAPI must not remove or rewrite browser initialization.
3. Do not move an existing live bootstrap behind `useEffect`, `localStorage`, or a consent-change event as part of an unrelated refactor. If consent behavior must change for a jurisdiction, make it a separate high-risk migration and use the consent-state matrix below.
4. `ChapterPixel` owns chapter events. `HardLink` owns click-before-hard-navigation events. The route tracker owns only genuine SPA path changes. Do not let two owners send the same event instance.

Required acceptance matrix after any Pixel-adjacent change:

| Scenario | Required observation |
|---|---|
| Fresh chapter hard load | Unconditional policy: `fbevents.js`, one initialization, one `PageView`, one `ViewContent`. Opt-in policy: no Meta request or event before a choice. |
| Hard next-chapter navigation | The click event leaves before navigation; the new document produces exactly one new `PageView` and one `ViewContent` |
| True SPA pathname change, if supported | Route tracker produces exactly one `PageView`; initial mount produces none |
| 25% / 50% / 75% / prose-end / 20s / 30s | Each configured browser event fires once with its unprefixed event name and chapter payload |
| CAPI unavailable or removed | Browser events above still fire; no helper returns early merely because the server transport is absent |
| Consent migration only | Fresh pre-consent and reload-after-reject make zero Meta requests/events; accept immediately creates one initialization, one current-page `PageView`, and one chapter `ViewContent`; reload-after-accept produces the same once-only events without duplicate initialization |

Use Meta Pixel Helper or Events Manager Test Events on a real chapter page. Inspect network/event counts across at least one hard next-chapter transition. A build, type-check, static HTML string, or source grep is supporting evidence only.

### 4.2 Landing page choice

- Land on a **strong hook chapter** (often chapter 1, or the highest-tension opening) — not the home page. The faster a reader is inside prose, the more pageviews follow.
- Landing page must: LCP < 2.5s on mid-range Android/4G, have footer trust links (§1.5), no pre-content interstitial, no deceptive pop-ups (FB "disruptive" + Google Better-Ads). A bottom anchor ad is fine; a full-screen interstitial before content is not.

### 4.3 Pixel event implementation — chapter page

Add this client component and drop it into every chapter page. It fires six events that cover the full optimization funnel described in §4.1 and in `facebook-ads.md §Pixel Event Hierarchy`.

```tsx
// src/components/ChapterPixel.tsx
'use client'
import { useEffect, useRef } from 'react'

interface Props {
  chapterTitle: string
  chapterOrder: number
  bookSlug: string
}

export function ChapterPixel({ chapterTitle, chapterOrder, bookSlug }: Props) {
  const fired25 = useRef(false)
  const fired50 = useRef(false)
  const fired75 = useRef(false)
  const firedCompleted = useRef(false)
  const firedDwell20 = useRef(false)
  const firedDwell30 = useRef(false)

  useEffect(() => {
    // ViewContent on chapter open — fires once, on mount
    window.fbq?.('track', 'ViewContent', {
      content_type: 'chapter',
      content_name: chapterTitle,
      content_ids: [`${bookSlug}-ch${chapterOrder}`],
    })

    const payload = { content_name: chapterTitle, chapter_order: chapterOrder }

    // TimeOnPage20s and TimeOnPage30 share the same chapter-only scope and payload.
    const dwell20Timer = setTimeout(() => {
      if (!firedDwell20.current) {
        firedDwell20.current = true
        window.fbq?.('trackCustom', 'TimeOnPage20s', payload)
      }
    }, 20000)

    const dwell30Timer = setTimeout(() => {
      if (!firedDwell30.current) {
        firedDwell30.current = true
        window.fbq?.('trackCustom', 'TimeOnPage30', payload)
      }
    }, 30000)

    // Scroll milestones
    const onScroll = () => {
      const ratio = window.scrollY / (document.body.scrollHeight - window.innerHeight)
      if (!fired25.current && ratio >= 0.25) {
        fired25.current = true
        window.fbq?.('trackCustom', 'ScrollDepth25', { content_name: chapterTitle, chapter_order: chapterOrder })
      }
      if (!fired50.current && ratio >= 0.5) {
        fired50.current = true
        window.fbq?.('trackCustom', 'ChapterRead50', { content_name: chapterTitle, chapter_order: chapterOrder })
      }
      if (!fired75.current && ratio >= 0.75) {
        fired75.current = true
        window.fbq?.('trackCustom', 'ScrollDepth75', { content_name: chapterTitle, chapter_order: chapterOrder })
      }
    }

    // ChapterCompleted — IntersectionObserver on #chapter-content-end sentinel
    // Cannot use scroll ratio: document.body.scrollHeight includes the recommendation
    // area below prose, so ratio ≥ 0.9 fires while the reader is still in that area.
    let io: IntersectionObserver | null = null
    const sentinel = document.getElementById('chapter-content-end')
    if (sentinel) {
      io = new IntersectionObserver(
        (entries) => {
          if (entries[0].isIntersecting && !firedCompleted.current) {
            firedCompleted.current = true
            window.fbq?.('trackCustom', 'ChapterCompleted', {
              content_name: chapterTitle,
              chapter_order: chapterOrder,
            })
          }
        },
        { threshold: 0.1 }
      )
      io.observe(sentinel)
    }

    window.addEventListener('scroll', onScroll, { passive: true })
    return () => {
      clearTimeout(dwell20Timer)
      clearTimeout(dwell30Timer)
      window.removeEventListener('scroll', onScroll)
      io?.disconnect()
    }
  }, [chapterTitle, chapterOrder, bookSlug])

  return null
}
```

Do not attach arbitrary `value` / `currency` fields to reading events. `ViewContent` has no monetary value by default, and invented values pollute value and ROAS reporting. When the business intentionally values a chapter open by expected advertising revenue, calculate it as `chapter page RPM / 1000` and use the site's actual ISO 4217 currency. For example, a measured or explicitly assumed `¥20` chapter Page RPM maps to `value: 0.02, currency: 'CNY'`. If no measured Page RPM exists but value reporting is required, `0.02 CNY` is an acceptable temporary baseline only when the assumption is recorded and revisited; otherwise omit both fields.

Add the sentinel element at the end of the chapter prose (before the recommendation/nav section):

```tsx
{/* Marks the true end of prose — ChapterPixel's IntersectionObserver targets this */}
<div id="chapter-content-end" aria-hidden="true" />
```

In the chapter page Server Component:

```tsx
// src/app/book/[slug]/chapter/[order]/page.tsx
import { ChapterPixel } from '@/components/ChapterPixel'

export default function ChapterPage({ params }) {
  const chapter = getChapter(params.slug, params.order)
  return (
    <>
      <ChapterPixel
        chapterTitle={chapter.title}
        chapterOrder={chapter.order}
        bookSlug={params.slug}
      />
      {/* chapter content */}
    </>
  )
}
```

**Ad Set conversion event priority (广告组转化事件 — Ads Manager → Ad Set → Performance goal → Conversion event):**

Select the highest-quality event that has accumulated ≥ 50 events/week. Upgrade as volume grows:

| Priority | Event | Signal quality |
|---|---|---|
| 1 | `ChapterCompleted` (custom) | Reader finished prose — highest intent |
| 2 | `ChapterRead50` (custom) | Reader reached midpoint — proven engagement |
| 3 | `TimeOnPage30` (custom) | 30s dwell — time-dimension engagement, good for short chapters |
| 4 | `ViewContent` (standard) | Chapter opened — lowest, but broadest volume |
| 5 | `PageView` | Any page — fallback only |

Note: custom events (`ChapterCompleted`, `ChapterRead50`, `TimeOnPage30`, `NextChapterClick`) must be wrapped as Custom Conversions in Events Manager before they can be selected as Ad Set optimization targets — see `facebook-ads.md §Step 1.2`. Record this manual setup in `TODO.md`.

Use `ViewContent` as the campaign optimization target to start. Upgrade to `ChapterRead50` once it accumulates ≥ 50 events/week — it signals actual readers, not page-loaders.

---

## 5. Required trust pages (build in B4)

Add these routes/pages to every monetized site — they are gating requirements, not optional:

- `/privacy` — Privacy Policy (mentions cookies, AdSense/Google & third-party vendors, Meta Pixel, data use)
- `/terms` — Terms of Use
- `/about` — About (a real description of the site/brand)
- `/contact` — Contact (a reachable address — either a dedicated email or a reference to the domain WHOIS contact for DMCA/content requests; a page must exist)
- Cookie-consent banner wired to a Google-certified CMP
- Footer on every page links all of the above.

Without these, AdSense approval fails and Facebook flags the domain as low quality.

---

## 6. KPIs & iteration

Track and optimize:

| Metric | Target / note |
|---|---|
| Session RPM (viewable) | the headline revenue number |
| Pageviews / session | ≥ 2.5–4 |
| Ad viewability | ≥ 70% |
| CLS / LCP | CLS < 0.1, LCP < 2.5s (cheaper FB delivery + SEO) |
| Facebook CPC | the cost side — drive down via creative/targeting |
| **ROAS** = ad revenue ÷ FB spend | must be > 1 with margin; the whole game |

- Change layout via **50/50 A/B** (AdSense Experiments or a feature flag), run **≥ 14–21 days** to cover weekly + seasonal cycles, roll out only if RPM lift > 5% **with no engagement degradation**.
- Re-test placements every 6–12 months — demand and behavior drift; set-and-forget loses 8–15% RPM over two years.

---

## 7. Build-time checklist (wire into B4–B6)

- [ ] Covers, hero images, titles, synopses contain no outright explicit/pornographic content (§1.1); suggestive allure is fine.
- [ ] Privacy / Terms / About / Contact pages exist and are footer-linked on every route (§5).
- [ ] Google-certified CMP / cookie consent wired (§1.5).
- [ ] Every ad slot reserves explicit size (no CLS) (§3.3).
- [ ] Every configured AdSense and AdX unit requests on component mount; no ad component contains a custom `IntersectionObserver`, `priority` prop, or viewport-margin lazy branch (§3.1.1, §8.6).
- [ ] Ad components from §8.6 are used unchanged; every slot reserves explicit width/height before its immediate request (no CLS).
- [ ] Ad density ≤ 3–4 / 1,000 words and ad-pixels < 30% of content (§1.3, §3.2).
- [ ] No ad is mistakable for the Next/TOC control; clear gap maintained (§1.4).
- [ ] Chapter change does a full reload so ads reinit and a fresh pageview counts (§2.1).
- [ ] (If used) in-chapter pagination keeps each page content-rich and compliant (§2.2).
- [ ] *(Optional — add when running FB campaigns)* Meta Pixel installed (§8.1).
- [ ] Landing chapter LCP < 2.5s, no interstitial before content (§4.2).
- [ ] `og:image` set on all chapter and book detail pages; `metadataBase` set in root layout (§4 impl).
- [ ] End-of-last-chapter shows cross-book recommendation grid, not a dead-end link (§2.3 impl).
- [ ] `<link rel="prefetch">` added for next chapter URL on every chapter page (§2.1 impl).
- [ ] After the production build, inspect generated HTML for Chapter 1, one ordinary chapter, and the final chapter. Each configured GPT div ID must appear exactly once as an element, and their DOM positions must strictly increase in the order q4 → q1 → q2 → q3 → q5. Source inspection alone does not pass this gate.

---

## 8. Implementation patterns (Next.js App Router + static export)

### 8.1 Meta Pixel — `layout.tsx` *(add when running FB campaigns)*

Fires `PageView` on every full-reload chapter navigation automatically. Only add this when you have a real Pixel ID — do not add placeholder env vars to the build. On an existing live site, preserve this bootstrap and its current consent behavior unless an explicit consent migration is in scope; see §4.1.1.

Hardcode `metadataBase` with the real domain (no env var needed):

```tsx
export const metadata: Metadata = {
  metadataBase: new URL('https://yoursite.com'),  // hardcode — no env var
  // ...
}
```

Then add the Pixel script in `<head>` when the campaign goes live:

```tsx
<script
  dangerouslySetInnerHTML={{
    __html: `!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','YOUR_PIXEL_ID');fbq('track','PageView');`,
  }}
/>
<noscript>
  <img
    height="1"
    width="1"
    style={{ display: 'none' }}
    src="https://www.facebook.com/tr?id=YOUR_PIXEL_ID&ev=PageView&noscript=1"
    alt=""
  />
</noscript>
```

The ID in `fbq('init', ...)` and the `noscript` URL must be identical. Do not replace this browser path with a CAPI-only helper.

The snippet above is the default unconditional policy. When the site has an explicitly approved Meta opt-in policy, use the gated loader contract in §4.1.1 instead: no Meta preconnect, script request, `fbq('init')`, event, or `noscript` tracking image before consent. Do not implement the gate as a client wrapper that leaves downstream emitters without a stable initializer.

### 8.2 OG image — three layers required

Set `metadataBase` once in `layout.tsx` — all relative OG image paths in child pages resolve to absolute automatically. No `siteUrl` env var needed.

**Layer 1 — Homepage (`layout.tsx`):** logo as fallback for any page without a specific OG image:
```ts
metadataBase: new URL('https://yoursite.com'),
openGraph: {
  siteName: 'Your Site Name',
  type: 'website',
  images: [{ url: 'https://yoursite.com/logo-light.png', width: 512, height: 512, alt: 'Your Site Name' }],
},
```

**Layer 2 — Book detail page (`book/[slug]/page.tsx`):**
```ts
openGraph: {
  title: book.title,
  description: book.description,
  images: [{ url: book.cover, width: 848, height: 1280, alt: book.title }],  // relative path OK, metadataBase resolves it
  type: 'book',
  siteName: 'Your Site Name',
},
twitter: { card: 'summary_large_image' },
```

**Layer 3 — Chapter page (`book/[slug]/chapter/[n]/page.tsx`):**
```ts
openGraph: {
  title: `${chapter.title} — ${book.title}`,
  description: `Read Chapter ${n} of ${book.title} by ${book.author}.`,
  images: [{ url: book.cover, width: 848, height: 1280, alt: book.title }],  // same cover as book page
  type: 'article',
  siteName: 'Your Site Name',
},
twitter: { card: 'summary_large_image' },
```

The book cover (portrait 2:3, 848×1280) doubles as the FB link preview for book and chapter pages — no separate OG asset needed. Chapter page may omit `images` and fall back to the layout logo, but setting `book.cover` is preferred. See `references/performance.md` §4 for the full requirements table.

### 8.3 Next-chapter prefetch — chapter `page.tsx`

```tsx
return (
  <>
    {next && <link rel="prefetch" href={`/book/${slug}/chapter/${next.order}`} />}
    <div className="min-h-screen bg-base-100">
      ...
    </div>
  </>
)
```

Next.js App Router hoists `<link rel="prefetch">` from Server Components into `<head>` automatically.

### 8.4 Cross-book recommendation at end of book

Replace the dead-end "Back to book page" with a 3-book grid. Import `books` (already used in `generateStaticParams`) and filter out the current book:

```tsx
{!next && (
  <div className="my-10 border border-base-300 rounded-2xl px-6 py-10">
    <p className="text-base font-semibold text-base-content text-center mb-1">
      You&apos;ve finished <em>{book.title}</em>.
    </p>
    <p className="text-xs text-base-content/40 uppercase tracking-widest text-center mb-8">Keep reading</p>
    <div className="grid grid-cols-3 gap-4">
      {books.filter(b => b.slug !== slug).slice(0, 3).map(b => (
        <HardLink key={b.slug} href={`/book/${b.slug}/chapter/1`} className="flex flex-col items-center gap-2 group">
          <div className="w-full rounded-lg overflow-hidden shadow-md" style={{ aspectRatio: '2/3' }}>
            <img src={b.cover} alt={b.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
          </div>
          <span className="text-[11px] font-semibold text-center text-base-content group-hover:text-primary transition-colors line-clamp-2 leading-tight">
            {b.title}
          </span>
        </HardLink>
      ))}
    </div>
  </div>
)}
```

Link directly to chapter 1 of each book — not the book detail page — to minimize the click-to-reading funnel.

### 8.5 Trust pages — minimal viable set

Each trust page follows the same shell: site header `<Link href="/">← Site Name</Link>` + content + footer with trust nav links. Footer pattern:

```tsx
<footer className="border-t border-base-300 mt-16">
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-3">
    <p className="text-[13px] text-base-content/40">&copy; {new Date().getFullYear()} Site Name</p>
    <nav className="flex gap-5">
      <Link href="/about" className="text-[13px] text-base-content/40 hover:text-base-content/70 transition-colors">About</Link>
      <Link href="/privacy" className="text-[13px] text-base-content/40 hover:text-base-content/70 transition-colors">Privacy</Link>
      <Link href="/terms" className="text-[13px] text-base-content/40 hover:text-base-content/70 transition-colors">Terms</Link>
      <Link href="/contact" className="text-[13px] text-base-content/40 hover:text-base-content/70 transition-colors">Contact</Link>
    </nav>
  </div>
</footer>
```

Privacy Policy must explicitly name: the ad network (Google AdSense or Google Ad Manager), cookies, and user rights. Add Meta Pixel mention only if Pixel is actually installed. Terms must state: fiction content, 18+ audience, no reproduction. Contact page must exist and be reachable — a dedicated email is fine, but for independently-operated sites a note directing DMCA requests to the domain WHOIS contact is acceptable.

### 8.6 Ad components

#### AdX / GAM — `AdSlot.tsx`

Mount immediately on render — no `IntersectionObserver` or `priority` branch. Keep `singleRequest`, but remember that independently mounted components do not guarantee deterministic one-request batching; guaranteed SRA requires defining every slot before the first `display()` call.

```tsx
'use client'

import { useEffect } from 'react'

type Props = {
  path: string
  id: string
  sizes: [number, number][]
  className?: string
}

declare global {
  interface Window {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    googletag: any
  }
}

export default function AdSlot({ path, id, sizes, className = '' }: Props) {
  useEffect(() => {
    window.googletag = window.googletag || { cmd: [] }
    window.googletag.cmd.push(() => {
      const slot = window.googletag.defineSlot(path, sizes, id)
      if (!slot) return
      slot.addService(window.googletag.pubads())
      window.googletag.display(id)
    })
    return () => {
      window.googletag?.cmd.push(() => {
        const slot = window.googletag.pubads().getSlots()
          .find((s: { getSlotElementId: () => string }) => s.getSlotElementId() === id)
        if (slot) window.googletag.destroySlots([slot])
      })
    }
  }, [path, id]) // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className={`flex justify-center my-6 ${className}`}>
      <div id={id} style={{ minWidth: 250, minHeight: 250 }} />
    </div>
  )
}
```

Placement mapping — split every chapter into four parts and render the configured five unique AdX units:

```tsx
function splitContent(content: string): [string, string, string, string] {
  const paras = content.split(/\n{2,}/).filter(p => p.trim())
  if (paras.length === 0) return ['', '', '', '']
  const c1 = Math.max(1, Math.round(paras.length * 0.25))
  const c2 = Math.max(c1 + 1, Math.round(paras.length * 0.5))
  const c3 = Math.max(c2 + 1, Math.round(paras.length * 0.75))
  return [
    paras.slice(0, c1).join('\n\n'),
    paras.slice(c1, c2).join('\n\n'),
    paras.slice(c2, c3).join('\n\n'),
    paras.slice(c3).join('\n\n'),
  ]
}

<AdSlot path="/YOUR_NETWORK_CODE/q4" id="ad-slot-4" sizes={[[336,280],[250,250],[300,250]]} />
<div className="prose-reader">{contentParts[0]}</div>
<AdSlot path="/YOUR_NETWORK_CODE/q1" id="ad-slot-1" sizes={[[250,250],[300,250],[336,280]]} />
<div className="prose-reader">{contentParts[1]}</div>
<AdSlot path="/YOUR_NETWORK_CODE/q2" id="ad-slot-2" sizes={[[250,250],[336,280],[300,250]]} />
<div className="prose-reader">{contentParts[2]}</div>
<AdSlot path="/YOUR_NETWORK_CODE/q3" id="ad-slot-3" sizes={[[250,250],[336,280],[300,250]]} />
<div className="prose-reader">{contentParts[3]}</div>
<div id="chapter-content-end" />
{/* Render the in-flow TOC / Next chapter controls here. */}
<AdSlot path="/YOUR_NETWORK_CODE/q5" id="ad-slot-5" sizes={[[336,280],[300,250],[250,250]]} />
```

#### Fixed navigation bar — `StickyNav.tsx`

Mount outside `<main>` as a sibling before `<div className="min-h-screen">`. The bar is always visible; `<main>` uses `className="pb-sticky-ad"` (CSS utility: `calc(82px + env(safe-area-inset-bottom))`) to prevent content hiding behind it.

All sites use a nav-only bar: TOC + Next buttons, no ads. q5 goes in the content flow below chapter navigation and must never be duplicated in the sticky bar.

```tsx
'use client'

type Props = { bookSlug: string; nextChapter: number | null }

const btnFont = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'

export default function StickyNav({ bookSlug, nextChapter }: Props) {
  return (
    <div
      className="fixed bottom-0 left-0 right-0 z-40 bg-base-100/60 backdrop-blur-md border-t border-base-300/40"
      style={{ paddingBottom: 'env(safe-area-inset-bottom)' }}
    >
      <div
        className="max-w-3xl mx-auto px-4 py-2"
        style={{
          display: 'grid',
          gap: '12px',
          gridTemplateColumns: nextChapter !== null
            ? 'minmax(96px, 0.75fr) minmax(136px, 1.12fr)'
            : '1fr',
        }}
      >
        <a
          href={`/book/${bookSlug}#toc`}
          onClick={(e) => { e.preventDefault(); window.location.href = `/book/${bookSlug}#toc` }}
          onTouchStart={() => {}}
          className="flex items-center justify-center gap-1.5 min-h-[44px] px-5 rounded-[14px] border-2 border-base-300 text-base-content font-extrabold text-[13px] tracking-tight hover:border-primary hover:text-primary active:scale-90 active:bg-base-300 transition-[transform,opacity,background-color,border-color] duration-75 select-none"
          style={{ fontFamily: btnFont }}
        >
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" className="shrink-0">
            <line x1="8" y1="6" x2="21" y2="6" /><line x1="8" y1="12" x2="21" y2="12" /><line x1="8" y1="18" x2="21" y2="18" />
            <line x1="3" y1="6" x2="3.01" y2="6" /><line x1="3" y1="12" x2="3.01" y2="12" /><line x1="3" y1="18" x2="3.01" y2="18" />
          </svg>
          <span>TOC</span>
        </a>
        {nextChapter !== null && (
          <a
            href={`/book/${bookSlug}/chapter/${nextChapter}`}
            onClick={(e) => { e.preventDefault(); window.location.href = `/book/${bookSlug}/chapter/${nextChapter}` }}
            onTouchStart={() => {}}
            className="flex items-center justify-center gap-1.5 min-h-[44px] px-5 rounded-[14px] bg-primary text-primary-content font-extrabold text-[15px] tracking-tight hover:opacity-90 active:scale-90 active:opacity-50 transition-[transform,opacity,background-color,border-color] duration-75 select-none"
            style={{ fontFamily: btnFont, boxShadow: '0 8px 18px rgba(236,75,155,.18)' }}
          >
            <span>Next</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" className="shrink-0">
              <path d="M9 18l6-6-6-6" />
            </svg>
          </a>
        )}
      </div>
    </div>
  )
}
```

**AdSense variant** — same nav strip, no ad section:

```tsx
'use client'

type Props = { bookSlug: string; nextChapter: number | null }

const btnFont = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'

export default function StickyNav({ bookSlug, nextChapter }: Props) {
  return (
    <div
      className="fixed bottom-0 left-0 right-0 z-40 bg-base-100/60 backdrop-blur-md border-t border-base-300/40"
      style={{ paddingBottom: 'env(safe-area-inset-bottom)' }}
    >
      <div
        className="max-w-3xl mx-auto px-4 py-2"
        style={{
          display: 'grid',
          gap: '12px',
          gridTemplateColumns: nextChapter !== null
            ? 'minmax(96px, 0.75fr) minmax(136px, 1.12fr)'
            : '1fr',
        }}
      >
        <a
          href={`/book/${bookSlug}#toc`}
          onClick={(e) => { e.preventDefault(); window.location.href = `/book/${bookSlug}#toc` }}
          onTouchStart={() => {}}
          className="flex items-center justify-center gap-1.5 min-h-[44px] px-5 rounded-[14px] border-2 border-base-300 text-base-content font-extrabold text-[13px] tracking-tight hover:border-primary hover:text-primary active:scale-90 active:bg-base-300 transition-[transform,opacity,background-color,border-color] duration-75 select-none"
          style={{ fontFamily: btnFont }}
        >
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" className="shrink-0">
            <line x1="8" y1="6" x2="21" y2="6" /><line x1="8" y1="12" x2="21" y2="12" /><line x1="8" y1="18" x2="21" y2="18" />
            <line x1="3" y1="6" x2="3.01" y2="6" /><line x1="3" y1="12" x2="3.01" y2="12" /><line x1="3" y1="18" x2="3.01" y2="18" />
          </svg>
          <span>TOC</span>
        </a>
        {nextChapter !== null && (
          <a
            href={`/book/${bookSlug}/chapter/${nextChapter}`}
            onClick={(e) => { e.preventDefault(); window.location.href = `/book/${bookSlug}/chapter/${nextChapter}` }}
            onTouchStart={() => {}}
            className="flex items-center justify-center gap-1.5 min-h-[44px] px-5 rounded-[14px] bg-primary text-primary-content font-extrabold text-[15px] tracking-tight hover:opacity-90 active:scale-90 active:opacity-50 transition-[transform,opacity,background-color,border-color] duration-75 select-none"
            style={{ fontFamily: btnFont, boxShadow: '0 8px 18px rgba(0,0,0,.12)' }}
          >
            <span>Next</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" className="shrink-0">
              <path d="M9 18l6-6-6-6" />
            </svg>
          </a>
        )}
      </div>
    </div>
  )
}
```

**iOS `:active` note**: iOS Safari does not fire `:active` on `<a>` without a touch listener. Add `onTouchStart={() => {}}` to every button/link that uses `active:` Tailwind classes. Use `transition-[transform,opacity,background-color,border-color] duration-75` (not `transition-all`) for 75ms response.

**Do NOT** add `<ins class="adsbygoogle">` or any AdSense slot inside a fixed/sticky container — AdSense policy violation.

#### AdSense — `AdsenseSlot.tsx`

The `<ins>` must expose a non-zero responsive width before `adsbygoogle.push({})` runs. Keep `width: '100%'` on the element; an empty `<ins>` inside a flex wrapper can otherwise collapse to `availableWidth=0`, preventing AdSense from selecting a creative size. Reserve at least 250px of height to protect CLS while the request resolves.

```tsx
'use client'

import { useEffect } from 'react'

declare global {
  interface Window {
    adsbygoogle: unknown[]
  }
}

type Props = {
  slot: string
  className?: string
}

export default function AdsenseSlot({ slot, className = '' }: Props) {
  useEffect(() => {
    try {
      window.adsbygoogle = window.adsbygoogle || []
      window.adsbygoogle.push({})
    } catch {
      // blocked by ad blocker
    }
  }, [slot])

  return (
    <div className={`flex justify-center my-6 overflow-hidden ${className}`}>
      <ins
        className="adsbygoogle"
        style={{ display: 'block', width: '100%', minHeight: 250 }}
        data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
        data-ad-slot={slot}
        data-ad-format="auto"
        data-full-width-responsive="true"
      />
    </div>
  )
}
```

### 8.7 Layout viewport and empty-div collapse

Export an explicit viewport in `app/layout.tsx` so mobile ad sizing and viewability measurement are correct:

```tsx
import type { Metadata, Viewport } from 'next'

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}
```

For AdX / Google Ad Manager sites, use GPT `setConfig` to collapse unfilled slots (no deprecated `pubads()` calls):

```tsx
<script
  dangerouslySetInnerHTML={{
    __html: `window.googletag=window.googletag||{cmd:[]};googletag.cmd.push(function(){googletag.setConfig({singleRequest:true,collapseDiv:"ON_NO_FILL"});googletag.enableServices();});`,
  }}
/>
```

This empty-slot collapse rule is for GPT / Google Ad Manager inventory, including AdX-backed sites. It is not an AdSense `<ins class="adsbygoogle">` feature, and must not be copied into AdSense implementations.

Hard pitfall: hiding empty `AdSlot` wrappers manually by listening to `slotRenderEnded` and setting `display:none` is a dumb implementation pattern, not an acceptable alternative. Active View and viewability measurement depend on GPT's slot lifecycle and visible ad pixels. Manual post-render DOM hiding makes measurement and layout behavior harder to reason about, and usually means the developer solved the wrong layer. Let GPT own the collapse decision through `collapseDiv:"ON_NO_FILL"` and keep each `AdSlot` reserving its normal size before render to avoid CLS.

### 8.8 Refresh rule (optional)

Only refresh ads when the unit is in the viewport and the tab has been active for ≥ 30 seconds. Sticky/anchor units are the safest refresh surface because they remain viewable. Do not refresh below-the-fold units.
