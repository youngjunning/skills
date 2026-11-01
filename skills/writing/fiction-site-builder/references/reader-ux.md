# Reader UX

## Reading First Principles

The reader is the product. Optimize for long sessions, low fatigue, and fast return to the current chapter. Every interaction in the reader must serve the reading act or stay out of the way.

**Ease of reading over visual precision.** If a choice makes prose harder to track, it is wrong regardless of how it looks in a screenshot. The chapter page must feel as effortless to read as a well-formatted paperback — generous body size, ample line-height, neutral background, no chrome competing for attention.

## Required Reader Controls

The default reader ships with a focused set of controls. Add font size, density, or reading progress indicator only when the brief explicitly asks for them. Every chapter keeps a compact table-of-contents icon in the fixed top header; the bottom nav also keeps the chapter-list control for chapter 2 and later. Both controls hard-navigate to the book detail page's `#toc` anchor.

| Control | Requirement | Notes |
| --- | --- | --- |
| Next chapter | Required | Inline CTA in the content flow at the end of chapter text (see **End-of-Chapter Navigation** below). No Previous button — TOC handles backward navigation. |
| Table of contents | Required on every chapter | The fixed top header shows a compact chapter-list icon on every chapter. Chapter 2 and later also keep the bottom-bar chapter list button; both hard-navigate to `/book/{slug}#toc`. |
| Book cover header | Required | Small cover thumbnail in the reader header above the chapter title; omit if no cover image exists |
| End-of-chapter prompt | Required | Inline "Next chapter →" CTA at the very bottom of chapter text. Use **`my-10`** (symmetric 40px) margin — never asymmetric `mt-16 mb-6`. |
| Keyboard prev/next | Required on desktop | `←` / `→` arrow keys |
| Error / empty states | Required | See Error States section |
| Dark mode toggle | Required | DaisyUI `data-theme` swap; persists in `localStorage` |
| Resume last chapter | Required | Store last visited chapter slug in `localStorage`; restore on home/detail page |
| Tap zones (mobile) | Recommended | Left/right 15% tap zones for prev/next |

## Top Reader Header

Always fixed (`position: fixed; top: 0`), `height: 56px`, `bg-base-100/95 backdrop-blur-sm`, `border-b border-base-300`.

**Layout — left: site logo | center: book + chapter title | right: theme toggle**

```
[ site logo ]   [ Book Title (xs, muted)    ]   [ ≡ ]  [ ☽ ]
                [ Ch. 1 - Chapter Title (sm)]
```

- **Left slot — site logo** (`h-8 w-auto`): always render the site logo as a link to `/`, including chapter 1. Never use a static logo, back arrow (`<`), or book cover thumbnail.
- **Center slot** — two-line text block: book title in `11px` muted, chapter title in `13px` medium. Truncate both.
- **Right slot** — dark mode toggle only. Use `btn btn-ghost btn-sm btn-circle`.

No back arrow (`<`) anywhere in the header. The site logo is always the home link (`/`) on every chapter.

Add `padding-top: 56px` (or `pt-14`) to the chapter content wrapper so it clears the fixed header.

---

## Paid-Traffic Chapter 1 Landing Page (Velvet Pattern)

When Meta/Facebook ads land directly on chapter 1, use the Velvet chapter-landing pattern. This pattern is optimized for cold social readers: confirm the book identity immediately, move into prose quickly, keep ads viewable without blocking the first reading decision, and make the next-chapter action visually unavoidable.

### Chapter 1 distraction lock

Chapter 1 landing pages are not normal reader pages. They must remove every non-essential navigation affordance so the reader has one obvious path: continue reading.

- Hide the normal site navigation bar on chapter 1 landing pages. A minimal fixed reader header may remain with static logo, book/chapter identity, and theme toggle only.
- Hide side menus, drawer triggers, and back buttons on chapter 1 landing pages.
- Keep the compact table-of-contents action on chapter 1; readers must be able to return to the book catalog without scrolling through the chapter.
- Do not render recommendation grids before or after the prose on chapter 1 landing pages.
- Do not add secondary buttons or text links that compete with `Next chapter →`.
- Always keep the site logo for brand recognition and make it the home link on chapter 1 as well as later chapters.

### Chapter 1 cover lead

Render a minimal cover lead only on chapter 1, after the top ad and before the chapter title and prose:

- Show the book cover at `220px` wide on mobile and `260px` at `sm` and above, centered in the reader column with a `2:3` aspect ratio.
- Show only the book title below the cover. Do not add author, tagline, synopsis, genre chips, chapter count, labels, badges, or an in-page CTA.
- Keep the cover and title in normal document flow with compact spacing. Do not wrap them in a bordered identity card or a two-column metadata layout.
- The chapter heading remains separate below the cover lead and keeps the localized chapter number/title treatment.
- Use `priority` for the chapter 1 cover when the image component supports it because the cover is above the fold.
- The simplified lead applies to every reader site, including sites that do not receive paid traffic yet, so existing sites and generated output stay consistent.

#### Ultra-narrow book-detail heroes

Book-detail hero variants that place a `96px` cover beside genres, title, teaser, and CTA must switch to a single column below `360px`. Center the cover above a full-width content block, allow genre chips to wrap, and keep the CTA full width. Never preserve a two-column hero when the remaining text column is narrower than about `200px`.

### Five-slot chapter ad layout

For an AdX site configured with five chapter units, every chapter uses the same five-slot layout. This removes chapter-specific inventory drift and guarantees that each GPT div ID appears exactly once:

- Show the top ad before the chapter 1 cover lead. On later chapters it remains before the chapter title/prose.
- Split prose into four parts at roughly 25% / 50% / 75%.
- Render q1 after part 1, q2 after part 2, and q3 after part 3 on every chapter, including chapter 1.
- Render q5 after chapter navigation so the final ad sits below the TOC/Next button row.
- The complete order is `q4 top → chapter 1 cover lead (chapter 1 only) → chapter title → prose part 1 → q1 → prose part 2 → q2 → prose part 3 → q3 → prose part 4 → completion sentinel → chapter navigation → q5 bottom`. Do not reuse any unit ID in a sticky component.
- If a legacy site has fewer than five chapter units, move its existing final unit below chapter navigation; do not invent or duplicate a unit ID merely to match the five-slot example.
- The first real prose block must still appear quickly after the top ad and chapter 1 identity lead; no login wall, no modal, no interstitial.

### Reader flow and controls

- Chapter title header follows the top ad. For chapter 1, left-align the chapter header; later chapters can be centered.
- Keep `id="chapter-start"` and `scroll-mt-20` on the first prose wrapper for stable deep links below the fixed header.
- End-of-prose sentinel: add `<div id="chapter-content-end" />` before nav/recommendations so `ChapterCompleted` fires at the real prose ending.
- Bottom nav is in content flow, not a fixed bar. Chapter 1 renders only the vivid Continue/Next button at full width. Chapter 2 onward renders TOC + Continue/Next.
- Button sizing: min-height `64px`; chapter 1 uses one full-width column. From chapter 2 onward use a grid ratio around `minmax(88px, 0.58fr) minmax(160px, 1.42fr)` when Next exists.
- Continue button copy should show both action and next chapter context, for example `Continue` + `Ch. 2: {nextTitle}`.
- The Continue button should use the site's primary hot color and a subtle glow/active scale (`active:scale-[0.96]`). It must visually dominate TOC.

### Retention after the final chapter

- Show the 3-book `Keep reading` recommendation grid **only after the final chapter** (`next === null`).
- Intermediate chapters must end with the Next/Continue action and no cross-book recommendations; competing covers interrupt the current-book pageview chain.
- Use covers + short titles; link with `HardLink` so ad-bearing routes hard reload and ad slots reinitialize.
- Link final-chapter recommendations to the next book's detail page for context, or directly to `/book/{slug}/chapter/1` only when the business goal explicitly prioritizes immediate cross-book continuation.
- Never add recommendations on chapter 1 or any chapter that still has a next chapter.

### Bottom whitespace trap

The Velvet landing-page fix exposed a recurring layout bug: short pages can show a large blank block after the footer or after the chapter recommendation grid when the page shell forces viewport height.

- Do not wrap homepage or reader routes in `min-h-screen` / `min-h-dvh` plus `flex flex-col` / `flex-1` unless there is a real sticky-footer requirement.
- Chapter pages should end at the real content flow: prose → sentinel → nav → recommendations. The page root should usually be `bg-base-100`, not `min-h-screen bg-base-100`.
- Home/list pages with a small catalog should not use `main.flex-1` to push the footer down; let the footer follow content naturally.
- Do not fix this by listening to GPT `slotRenderEnded` and hiding ad wrappers. For AdX/GAM, empty slots are handled by `googletag.setConfig({ singleRequest: true, collapseDiv: "ON_NO_FILL" })`; manual wrapper hiding can interfere with GPT lifecycle and Active View reasoning.
- If a no-fill ad still reserves space in screenshots where third-party scripts are blocked, treat that as a local preview artifact unless it reproduces with GPT loaded in production.

### Quality gates

- Fails if the top ad is not followed directly by the chapter 1 cover/title identity lead before the chapter heading and prose.
- Fails if the chapter 1 cover lead contains metadata or copy other than the book title.
- Fails if the chapter 1 cover is rendered as a small thumbnail instead of the `220px` mobile / `260px` larger-screen lead image.
- Fails if a modal, paywall, cookie wall, or interstitial appears before prose.
- Fails if any chapter renders fewer or more than the configured five unique slots.
- Fails if the final configured chapter ad appears above the chapter-navigation buttons.
- Fails if generated production HTML for Chapter 1, an ordinary chapter, and the final chapter does not contain exactly one element for each configured GPT div ID in strict q4 → q1 → q2 → q3 → q5 DOM order.
- Fails if the next action is a muted text link or smaller than TOC.
- Fails if the landing chapter uses SPA navigation for next chapter.
- Fails if chapter 1 shows a normal site nav bar, clickable logo, side menu, back button, TOC, or recommendation grid.
- Fails if homepage/footer or chapter recommendations are followed by a viewport-sized blank area caused by `min-h-screen` / `flex-1` page shells.

---

## End-of-Chapter Navigation

**No fixed bottom navigation bar.** The bottom viewport is reserved for the sticky anchor ad (AdX sites use `StickyAnchorAd` / q4; AdSense sites leave the bottom clear per policy). Navigation lives in two places:

1. **Top header** — right slot keeps a compact TOC icon followed by the theme toggle. The icon hard-navigates to `/book/{slug}#toc`. The bottom nav keeps its TOC button from chapter 2 onward. No drawer, no modal.
2. **Content flow** — inline "Next chapter →" CTA and cross-book recommendation grid appear at the end of chapter text, in the natural scroll path.

```tsx
{/* Inline next-chapter CTA — at bottom of prose */}
{next && (
  <div className="my-10 border border-base-300 rounded-2xl text-center px-8 py-10">
    <p className="text-xs text-base-content/40 uppercase tracking-widest mb-5">Continue reading</p>
    <HardLink
      href={`/book/${slug}/chapter/${next.order}`}
      className="inline-flex items-center gap-2 text-xl font-bold text-primary hover:text-primary/80 transition-colors"
    >
      Next chapter →
    </HardLink>
  </div>
)}
```

No "Previous" button anywhere. Fiction reading is a forward-only experience — the TOC handles backward navigation.

**Bottom padding — account for sticky anchor ad (AdX only):**

AdX chapter pages must add enough bottom padding so the last content line is not hidden behind the sticky q4 ad (min 250px height):

```css
/* AdX sites */
.pb-sticky-ad {
  padding-bottom: calc(280px + env(safe-area-inset-bottom));
}

/* AdSense sites — no sticky ad, just safe-area clearance */
.pb-safe-reader {
  padding-bottom: calc(24px + env(safe-area-inset-bottom));
}
```

**Next button — psychology-driven design:**

The "Next chapter →" inline CTA must trigger an almost involuntary desire to tap. Use a vivid, saturated warm color — hot pink (`#E91E8C` range), coral, or electric magenta when rendered as a full button. Never use the site's calm brand color here; this button needs contrast-driven urgency.

Why this works: bright saturated warm colors activate dopamine anticipation. Combined with the unresolved story tension (Zeigarnik effect — the reader's brain cannot rest on an open narrative loop), the button becomes the path of least resistance. The reader taps before consciously deciding to.

**TOC button — hard navigation, no drawer:**

The top-header and bottom-bar TOC buttons must use a hard navigation (`window.location.href` or a plain anchor) to `/book/{slug}#toc`. Do NOT implement a `TOCDrawer`, bottom sheet, or any modal overlay.

```tsx
<a
  href={`/book/${bookSlug}#toc`}
  onClick={(e) => { e.preventDefault(); window.location.href = `/book/${bookSlug}#toc` }}
  className="flex items-center justify-center w-8 h-8 rounded-full hover:bg-base-200 transition-colors shrink-0"
  aria-label="Chapter list"
>
  {/* list icon SVG */}
</a>
```

The book detail page must place `id="toc"` on the first book-detail ad wrapper immediately before the chapter list, not on the chapter-list section itself. This is deliberate: when readers tap the bottom-nav TOC button from a chapter, the detail page first shows the high-viewability ad, then the chapter list directly below it. Add `scroll-margin-top: 64px` to account for the fixed header.

**Book detail hero + first ad:**

Every book-detail hero style must keep the first display ad visible in the first mobile viewport. The hero can be cinematic, compact/gradient, atmospheric, or another site-specific variant, but it must not consume the whole first screen before an ad appears.

- Place the first book-detail ad immediately after the hero block, before synopsis/tagline/update metadata. Do not bury it below long copy.
- On the 390px × 844px mobile viewport, the first ad slot must be visible without scrolling; ideally its top starts within the lower half of the first screen.
- Keep detail-page hero height capped by content, not by `100vh` / full-screen marketing sections. Full-bleed is allowed only when it still leaves room for the first ad.
- The `#toc` anchor belongs on the first detail-page ad wrapper immediately before the chapter list. This makes TOC navigation expose the ad before the list without adding an interstitial.
- If a hero variant cannot satisfy this, shrink the cover, reduce vertical padding, or move supporting metadata below the first ad. Do not remove the ad.

**Quality gate failure if not met:**

- Next button uses a muted, dark, or low-saturation color.
- Next button is same width or narrower than TOC.
- "Previous" button appears anywhere in the reader nav.
- On mobile ≤ 640px: maintain 60px height minimum.
- Book detail hero pushes the first display ad below the first mobile viewport.

## Cross-Book Recommendation Grid

Show a 3-book recommendation grid on **every chapter** — the moment a reader finishes any chapter is the highest-intent moment for cross-promotion. Render it after the next-chapter nav on mid-book chapters, and after the "You've finished" message on the last chapter.

**Mid-book chapters** (`next` exists) — insert after the next-chapter nav block:

```tsx
{/* Cross-book recommendations */}
{next && (
  <div className="mt-10 pt-8 border-t border-base-300">
    <p className="text-xs text-base-content/40 uppercase tracking-widest text-center mb-6">You might also like</p>
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

**Last chapter** (`!next`) — use a more conclusive heading:

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

Rules:
- Links go to `/book/${b.slug}/chapter/1` so the reader starts immediately; arbitrage flows convert better when the next click lands in the reader, not on a detail page.
- Filter out the current book (`b.slug !== slug`). Take first 3 from remaining.
- **Use `HardLink` for cross-book grid links.** The chapter reader carries in-content ad slots; a client-side `<Link>` transition would skip ad reinitialization and reduce impressions. Only pages that carry no ad slots may use `next/link` for internal navigation.
- For Spanish sites, use "También te puede gustar" instead of "You might also like".

## Optional Enhancements

Add only when explicitly requested:

| Control | Notes |
| --- | --- |
| Font size | ≥ 4 steps (e.g. 14/16/18/20px) |
| Line height / density | ≥ 2 options: "Compact" and "Comfortable" |
| Theme | Light / Sepia / Dark via DaisyUI themes |
| Reading progress | Visible but not distracting |
| Resume scroll position | Per-chapter scroll restoration |
| Immersive mode | Chrome-hidden reading mode |

## Never Add Without Explicit Request

These features add UI complexity and distract from reading. Omit by default:

- Favorites / bookmarks
- Social sharing buttons
- Comment sections
- User accounts / login
- Bookshelf or reading list management
- Search
- Ranking or recommendation widgets
- Payment or chapter-lock UI

## Default Typography

Use conservative defaults. Readers should not need to adjust settings to find a comfortable starting point.

- **Font:** system fonts only — no external dependencies. Set `--font-reader` in `:root` to `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`. Do not use `Georgia`/serif stacks for prose — they add perceived reading friction for social traffic audiences. Do not use `next/font/google`, `@fontsource`, or any font package of any kind — they add build-time or runtime dependencies and can fail in restricted network environments. The system font stack is the final answer for both body and display text.
- **Prose size:** `19px` mobile → `20px` sm+.
- **Line height:** `1.8` mobile → `1.85` sm+.
- **Paragraph spacing:** `margin-bottom: 1.1em`.

```css
.prose-reader {
  font-size: 19px;
  line-height: 1.8;
  max-width: 68ch;
  margin: 0 auto;
  word-break: break-word;
  text-rendering: optimizeLegibility;
}
@media (min-width: 640px) { .prose-reader { font-size: 20px; line-height: 1.85; } }
```
- Latin line-height: 1.8–1.85 (compact but trackable — optimised for social traffic landing pages).
- Japanese/Korean line-height: 1.75–1.9.
- Paragraph spacing: `1em` top margin between paragraphs. Enough to separate beats without the double-spaced blog-style gap.
- Max line length: 32–38em for Latin prose; narrower for CJK (28–34em) to avoid very long line scanning.

## Chapter Page `<title>` Format

The HTML `<title>` on chapter pages is critical for SEO and social share quality. Use:

```
Chapter {n}: {chapter.title} | {book.title}
```

With the layout's `template: '%s | {Site Name}'`, the final browser title becomes:

```
Chapter 3: The Dark Bargain | Crimson Crown | Velvet Throne
```

**Rules:**
- Include the chapter number — search engines surface it in snippets; readers scanning results can orient immediately.
- Use `|` as separator (not `-` or `—`) for both the `title` and the `template`.
- Keep the `openGraph.title` shorter: `${chapter.title} — ${book.title}` (no chapter number; social cards show a thumbnail, not a search snippet).
- Spanish sites: `Capítulo ${n}: ${chapter.title} | ${book.title}`.

```ts
// generateMetadata
title: `Chapter ${n}: ${chapter.title} | ${book.title}`,
// openGraph
openGraph: { title: `${chapter.title} — ${book.title}`, ... }
```

## Layout

- Mobile horizontal padding: 18–22px.
- The sticky anchor ad (AdX only, `position: fixed; bottom: 0`) must not cover body text — use `.pb-sticky-ad` on the `<main>` wrapper. AdSense sites use `.pb-safe-reader`.
- Chapter title: visible at the top but not oversized. `--text-xl` or smaller.
- Reader background: off-white, paper tone, or deep neutral dark. Never pure `#fff` or `#000` in any theme.
- Do not use full-bleed background images behind prose.

## Immersive Mode

If implementing an immersive (chrome-hidden) reading mode:
- Trigger: tap the center of the screen, or scroll past a threshold.
- On hide: animate the top bar and bottom bar out smoothly (200ms, `transform: translateY`).
- On show: single tap or scroll-up restores chrome.
- Progress indicator may remain visible in immersive mode as a thin rail, not a full bar.
- Never hide previous/next controls entirely in immersive mode — they must be accessible with a single tap.

## Theme Implementation

Use DaisyUI's `data-theme` attribute on `<html>` to switch themes. The default reader provides **light and dark**. Add **sepia** only when the brief explicitly asks for it.

```js
// tailwind.config.js
plugins: [require('daisyui')],
daisyui: {
  themes: [
    {
      light: {
        'base-100': '#f9f6f1',
        'base-content': '#1a1814',
      },
    },
    {
      dark: {
        'base-100': '#141210',
        'base-content': '#e8e4de',
      },
    },
  ],
}
```

- Theme change must be instant — no transition delay that makes the UI feel unresponsive.
- Theme preference must persist in `localStorage`.
- Respect `prefers-color-scheme: dark` as the initial default if no saved preference exists.

## Font Size Implementation

Use only when the brief explicitly asks for font size control.

```js
const SIZES = [14, 16, 18, 20, 22]; // px
let current = 2; // default index

function applySize(index) {
  document.documentElement.style.setProperty('--reader-size', SIZES[index] + 'px');
  localStorage.setItem('reader-font-size', index);
}
```

- Font size changes must reflow gracefully without layout breakage.
- Line height should scale proportionally with font size.
- Save preference per reader (not per book).

## Scroll and Navigation

- Default: vertical scroll for H5. Horizontal paging is an optional mode, not the default.
- End-of-chapter: show a clear "Next chapter" prompt at the bottom of content — do not rely on navigation bars alone.
- Resume: on entering a chapter, restore scroll position from `localStorage` if available.
- Chapter transitions: force a full browser reload so AdSense reinitializes and the browser shows its native loading progress bar. Do NOT use `<Link>` from `next/link` or `router.push()` — Next.js App Router intercepts same-origin clicks after hydration and performs SPA navigation even on plain `<a>` tags. The only reliable override is `e.preventDefault()` + `window.location.href`:

  ```tsx
  <a
    href={`/book/${bookSlug}/chapter/${nextChapter}`}
    onClick={(e) => {
      e.preventDefault()
      window.location.href = `/book/${bookSlug}/chapter/${nextChapter}`
    }}
  >
    Next →
  </a>
  ```

  A plain `<a href>` without the `onClick` override is NOT sufficient in Next.js App Router — the framework hydration intercepts it for SPA routing.

  **When to use `HardLink` vs. `next/link`:**
  - **Any navigation that leaves an ad-bearing page** (home with ad slots, book detail, chapter reader): use `HardLink` / `window.location.href` so ad slots reinitialize and each destination counts as a fresh pageview.
  - **Chapter reader navigation** (Next →, prev/next tap zones, keyboard shortcuts): force a full reload with `window.location.href` so ad slots reinitialize.
  - **Ad-free pages only** (about, contact, privacy, terms, cookie policy, /dashboard): `next/link` with prefetch is acceptable for internal navigation because there are no ad slots to reinitialize.

## Gestures and Tap Zones (Mobile)

- Left-edge tap (15% width): previous chapter.
- Right-edge tap (15% width): next chapter.
- Center tap: toggle chrome visibility (if implementing immersive mode).
- These zones must not conflict with text selection.
- Swipe left/right for chapter navigation is acceptable as an enhancement, not a requirement.

## Keyboard Shortcuts (Desktop)

- `ArrowLeft` / `ArrowRight` or `←` / `→`: previous / next chapter.
- `F` or `Esc`: toggle immersive mode.
- These shortcuts must not conflict with browser defaults.
- Include a one-time tooltip hint for first-time desktop visitors.

## Interaction Rules

- All settings changes (theme, font size, density) apply instantly with no delay when those controls are present.
- Preserve reader preferences in `localStorage` for prototypes; in a server-side user account for real products.
- Preserve reading position in `localStorage` for prototypes; durable backend for real products.
- Reader controls must be reachable with one thumb on mobile.
- Do not require login before basic reading unless the user explicitly asks for a gated product.
- Display ads are expected on monetized sites (the default arbitrage model — see `references/adsense-arbitrage.md`): place the first AdSense/AdX slot **after** `contentParts[0]` (not before all content — pre-content ads have near-zero viewability on paid traffic), then interleave remaining slots within the reading flow. AdX sites add a `StickyAnchorAd` (q4, `position: fixed; bottom: 0`) for high-viewability anchor impressions. AdSense sites omit the sticky anchor (Google AdSense policy prohibits fixed-position manual units). Keep each slot's size reserved (no CLS), never let an ad be mistakable for navigation, and never push chapter content below the fold. Pop-ups and pre-content interstitials remain forbidden.

## Accessibility

- Use `<button>` for all interactive controls, not clickable `<div>` or `<span>`.
- Maintain WCAG AA contrast (4.5:1) for body text and controls in all enabled themes.
- Ensure visible `:focus` states on all keyboard-navigable controls.
- Do not disable browser pinch-to-zoom (`user-scalable=no` is forbidden).
- Avoid motion or animations on the reading surface itself. Restrict motion to chrome transitions.
- Use `aria-label` on icon-only controls (prev/next arrows, settings gear).
- Chapter content should be wrapped in `<article>` with an appropriate `aria-label`.

## Empty and Error States

- Chapter not found: "This chapter isn't available yet." with a link back to the catalog.
- Load failure: "Couldn't load this chapter. Try refreshing or check your connection."
- End of book: "You've finished [Book Title]." with a link to the book detail page.
- No chapters yet: "No chapters published yet. Check back soon."

Never show a raw error object or stack trace to the reader.
