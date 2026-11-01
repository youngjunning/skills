# QA Checklist

Run this checklist before any final delivery. For unattended execution, automate every check that can be automated; screenshots are captured programmatically and only surfaced when a check fails.

## Pre-Launch Gate

Run these checks before go-live. These are **not** blockers for development preview.

- [ ] `content/` has ≥ 3 book directories (initial site launch).
- [ ] Each long-form novel has at least 201 chapter files in `content/{book-title}/chapters/`. Smaller development previews are not launch-ready; short-form stories are classified separately.
- [ ] Each chapter is ≥ 1,200 words — no stub content.
- [ ] `outline/outline.md` exists and contains a real arc outline (not empty or stub-only).
- [ ] `world/worldbuilding.md` exists and describes the world, genre, and tone.
- [ ] `tracking/context.md` exists and reflects the last written chapter.
- [ ] Cover image generated for each book: `public/covers/{book-title}.webp` (flat path, no subfolders).
- [ ] Site logos generated: `public/logo-light.png` and `public/logo-dark.png` (apiyi). No SVG fallback — if skipped, flagged for a later pass.
- [ ] Favicon generated: `public/favicon-32x32.png` (apiyi). No SVG fallback — if skipped, flagged for a later pass.

If any launch asset is missing, attempt to generate it automatically (A2 covers / B2 logo and favicon). Only if generation fails, log the missing asset and continue; do not stop the pipeline.

## Automated Verification (run without user input)

Run the build and start the production server, then verify routes programmatically. The stack is fixed to Next.js (see `tech-stack.md`). Package manager is pnpm.

```bash
set -e

# Build
pnpm run build

# Start server in background and capture its port
pnpm run start > /tmp/fiction-server.log 2>&1 &
SERVER_PID=$!

# Wait for server to be ready; extract the port it bound to
PORT=""
for i in $(seq 1 30); do
  PORT=$(grep -oE 'http://localhost:[0-9]+' /tmp/fiction-server.log | head -1 | cut -d: -f3)
  [ -n "$PORT" ] && break
  sleep 1
done
[ -z "$PORT" ] && PORT=3000

# Pick the first book slug from content/
BOOK_SLUG=$(find content -maxdepth 2 -type d -name chapters | head -1 | xargs dirname | xargs basename)
[ -z "$BOOK_SLUG" ] && { echo "ERROR: no book found in content/"; kill $SERVER_PID; exit 1; }

BASE="http://localhost:${PORT}"
FAIL=0

check() {
  local name="$1"
  shift
  if "$@"; then
    echo "✓ $name"
  else
    echo "✗ $name"
    FAIL=1
  fi
}

# Route smoke tests (curl -sf already silences progress; no > /dev/null so check() can print ✓/✗)
check "home responds" curl -sf "${BASE}/"
check "book detail responds" curl -sf "${BASE}/book/${BOOK_SLUG}/"
check "chapter reader responds" curl -sf "${BASE}/book/${BOOK_SLUG}/chapter/1/"

# Content checks
check "chapter content renders" sh -c "curl -s '${BASE}/book/${BOOK_SLUG}/chapter/1/' | grep -q '<p>'"
check "next/finish link present" sh -c "curl -s '${BASE}/book/${BOOK_SLUG}/chapter/1/' | grep -qE 'Next chapter|Finish'"

kill $SERVER_PID

if [ "$FAIL" -ne 0 ]; then
  echo "ERROR: QA automated checks failed."
  exit 1
fi

echo "QA automated checks passed."
```

If the project uses `output: 'export'` (static export), replace the server start with serving the `dist/` or `out/` folder and point curl at that URL.

- [ ] Build completes without errors.
- [ ] TypeScript passes with no errors (`tsc --noEmit`) if applicable.
- [ ] All required pages respond with HTTP 200.
- [ ] Chapter content renders (`<p>` tags present).
- [ ] Navigation links present on reader (next chapter / finish).
- [ ] No `console.error` output in normal use.

## Visual QA (automated capture, human review only on failure)

Use a headless browser or screenshot tool if available (e.g. Playwright, Puppeteer). If none is installed, skip screenshot capture and rely on the curl smoke tests above. Do not present screenshots to the user unless an automated check fails.

### Required viewports

| Viewport | Page |
| --- | --- |
| 390 × 844 | Home / work list |
| 390 × 844 | Book detail |
| 390 × 844 | Reader (default theme) |
| 375 × 667 | Reader (small screen) |
| 1366 × 900 | Home / work list |
| 1366 × 900 | Reader |

### Automated inspections

For each captured screenshot, run programmatic checks where possible:

- Text clipping: assert no `scrollWidth > clientWidth` on body text elements.
- Touch targets: assert interactive elements are ≥ 44×44px.
- Contrast: assert body text and metadata meet WCAG AA (4.5:1) using computed styles.
- Image loading: assert cover images have naturalWidth > 0.

If all automated checks pass, mark the section complete without user review. If a check fails, show only the failing screenshot and a concise description of the problem.

## Theme Checks

Automate with headless browser:

- [ ] Toggle theme and verify `data-theme` attribute updates.
- [ ] Read computed colors and assert contrast ≥ 4.5:1 for body and metadata.
- [ ] No pure `#fff` or `#000` background in any default theme.
- [ ] Theme preference persists after reload (`localStorage` value preserved).

## Reader Controls

Automate with headless browser:

- [ ] Next chapter link navigates to the next chapter.
- [ ] Dark mode toggle switches themes and persists.
- [ ] Reading position is saved and restored on return.

## Multilingual Checks

For each target language:

- [ ] `<html lang="xx">` is set correctly.
- [ ] Reader body uses the correct language font stack.
- [ ] No garbled CJK characters.

## Accessibility Checks

Run `axe-core` or equivalent programmatically:

- [ ] No interactive `<div>` or `<span>` without keyboard role.
- [ ] Icon-only buttons have `aria-label`.
- [ ] Focus outlines visible on keyboard-navigable elements.
- [ ] `user-scalable=no` is not present.

## Content and Copy Checks

Automated grep over build output:

- [ ] No "lorem ipsum", "Coming soon", "TODO", "[BOOK TITLE]" on rendered pages.
- [ ] Imported chapters have no accidental code blocks caused by leading spaces or tabs.
- [ ] Imported chapters do not show excessive vertical gaps: consecutive blank lines are limited to one between paragraphs.
- [ ] No reader-visible copy mentions AI, Markdown, parser, prompt, or skill.
- [ ] Logos exist: `public/logo-light.png` and `public/logo-dark.png` (apiyi). No SVG fallback.
- [ ] Favicon exists: `public/favicon-32x32.png` (apiyi). No SVG fallback.
- [ ] End-of-chapter and end-of-book states render correctly.

## Performance Spot Check

- [ ] Initial JS bundle is below 200KB gzipped.
- [ ] No uncompressed image over 200KB on the home page.
- [ ] No external font CDN requests on the reader page unless explicitly required.

## Monetization & Ad-Policy Checks (paid-traffic arbitrage)

Run for every monetized FB-traffic site. See `references/adsense-arbitrage.md`. Account survival depends on these.

**Content compliance (Facebook + AdSense scan the landing page):**

- [ ] No cover, hero image, or imagery is outright explicit / pornographic — no exposed genitals or nipples, sex acts, or graphic nudity (suggestive allure is allowed; see `cover-allure-elements.md` §0).
- [ ] No "click here", arrows, or images placed to bait ad clicks; no content encourages clicking ads.

**Trust pages (AdSense approval + FB quality):**

- [ ] `/privacy`, `/terms`, `/about`, `/contact` pages exist and respond 200.
- [ ] All four are linked in the footer of every page.
- [ ] Privacy Policy mentions cookies, Google/AdSense + third-party vendors, and (if used) the Meta Pixel.
- [ ] Cookie-consent / Google-certified CMP banner is present.

**Ad layout & Core Web Vitals:**

- [ ] Every ad slot reserves explicit `min-height` / `aspect-ratio` before load — assert CLS < 0.1.
- [ ] Every configured AdSense and AdX slot requests on component mount; ad components contain no custom `IntersectionObserver`, `priority`, or viewport-margin lazy branch.
- [ ] Ad density ≤ ~3–4 units / 1,000 words and ad area < ~30% of content area per screen.
- [ ] No ad is visually/spatially mistakable for the Next or TOC control (clear gap maintained).
- [ ] Ads do not push chapter content below the fold on mobile (390×844).
- [ ] No pop-up or pre-content interstitial before the chapter renders.

**Pageview depth & tracking:**

- [ ] Chapter navigation does a full reload (`window.location.href`) so ads reinitialize and a fresh pageview counts.
- [ ] Meta Pixel fires `PageView` on load, `ViewContent` on chapter mount, unprefixed custom events (`ScrollDepth25`, `ChapterRead50`, `ScrollDepth75`) at the correct scroll ratios, `ChapterCompleted` when `#chapter-content-end` sentinel enters viewport, and `TimeOnPage30` after 30 seconds.
- [ ] `ViewContent` omits `value` / `currency` unless an explicit chapter-value model exists. When present, value equals measured chapter Page RPM / 1000; a temporary `0.02 CNY` baseline records its implied `¥20` Page RPM assumption.
- [ ] On a fresh chapter hard load, the layout bootstrap initializes the configured Pixel and emits exactly one `PageView`; `RouteAnalyticsTracker` emits nothing on initial mount or consent-state changes.
- [ ] One hard next-chapter transition produces exactly one click event before navigation, then exactly one new `PageView` and one `ViewContent` in the new document.
- [ ] CAPI failure/removal does not suppress browser events. If consent behavior changed, fresh pre-consent, accept, reject, reload-after-accept, and reload-after-reject all match the approved policy without duplicate initialization.
- [ ] Pixel-adjacent changes were verified with Meta Pixel Helper or Events Manager Test Events on a real chapter page; build/source checks alone are not marked as runtime acceptance.
- [ ] Landing chapter LCP < 2.5s on mid-range Android/4G.

## Post-Pipeline TODO.md

After B6 passes, generate `TODO.md` in the project root listing every post-launch task that cannot be automated. Create this file automatically — do not prompt the user.

**Required sections:**

```markdown
# TODO — Post-launch manual checklist

## Deployment
- [ ] Deploy to CDN (Vercel / Cloudflare Pages) — publish the `out/` directory
- [ ] Bind custom domain, configure DNS

## Ads
- [ ] Select which ad account to use for this site (reuse existing account or apply for a new one)
- [ ] Confirm AdSense slots (ca-pub-XXXXXXXX) serving after deployment
- [ ] Confirm AdX slots (/XXXXXXXXX) serving after deployment — omit if AdX not wired
- [ ] Confirm the correct CookieBanner variant is used for this site's market (see `references/performance.md §3`):
  - **Basic** (non-EU/UK — US, LatAm, etc.): single Accept button, localStorage flag. Default for most sites.
  - **GDPR** (EU / UK markets): Accept All / Reject All / Manage with category breakdown (Analytics + Advertising). Use when the primary audience is in the EU or UK. Both variants are UI-only — they record preference but do not gate ad loading.

## Analytics
- [ ] Add Google Analytics 4 (GA4) script (G-XXXXXXXX) to layout.tsx
- [ ] Register site in Google Search Console, submit sitemap

## Content expansion
- [ ] Add Open Graph images per book for social sharing
- [ ] Plan next batch of chapters or new books
```

Fill in the actual publisher IDs and ad-network paths from the project's AGENTS.md. Only include sections relevant to what was actually built (e.g. omit the AdX row if AdX was not wired up).

**Important:** Ad accounts are shared across sites — do NOT include a "apply for / submit for review" step. The accounts already exist; the only post-launch action is confirming the slots serve correctly after the new domain goes live.
