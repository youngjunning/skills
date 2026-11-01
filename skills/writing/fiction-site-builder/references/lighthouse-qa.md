# Lighthouse QA

Reference for Phase B6 — automated quality assurance with Lighthouse. Load when the build is ready and the user wants performance verification, or when B6 runs.

## When to Run

Run Lighthouse **after** `pnpm build` succeeds and the site is reachable (local `pnpm start` on `out/`, or a deployed preview URL). Do not run Lighthouse against a cold CDN — warm the cache first if testing production.

## Minimum Thresholds

A build must meet these scores before go-live. A single failed run is not enough to block — run 3 times and take the median.

| Metric | Minimum median score |
|--------|----------------------|
| Performance | 75 |
| Accessibility | 90 |
| Best Practices | 80 |
| SEO | 95 |

If Performance is below 75, investigate the top 3 audits before shipping.

## How to Run

### Option A — Local static server (recommended for pre-deploy QA)

```bash
cd /path/to/site
pnpm build
npx serve@latest out -l 3000 &
SERVER_PID=$!
npx lighthouse http://localhost:3000/ \
  --output=json \
  --output-path=./lighthouse-report-$(date +%Y%m%dT%H%M%S).json \
  --chrome-flags="--headless --no-sandbox"
kill $SERVER_PID
```

### Option B — Deployed URL

```bash
npx lighthouse https://example.com/ \
  --output=json \
  --output-path=./lighthouse-report-$(date +%Y%m%dT%H%M%S).json \
  --chrome-flags="--headless --no-sandbox"
```

### Run three times and summarize

```bash
URL="http://localhost:3000/"
for i in 1 2 3; do
  npx lighthouse "$URL" --output=json --output-path=./lh-$i.json --chrome-flags="--headless --no-sandbox" > /dev/null 2>&1
done
```

## What to Check

After each run, inspect these audits first:

1. **Performance**
   - `largest-contentful-paint` — should be < 2.5 s
   - `total-blocking-time` — should be < 200 ms
   - `speed-index` — should be < 4.0 s
   - `render-blocking-insight` — minimize render-blocking resources
   - `image-delivery-insight` — ensure cover/illustration sizes match display sizes
   - `total-byte-weight` — keep under 2 MB if possible

2. **Accessibility**
   - `color-contrast` — fix any failing elements
   - `heading-order` — ensure logical heading hierarchy
   - `image-alt` — all images have alt text

3. **Best Practices**
   - `errors-in-console` — zero console errors from site code (ads/third-party blockers may still report; separate those)
   - `inspector-issues` — no security warnings

4. **SEO**
   - `document-title`, `meta-description`, `hreflang`, `canonical` — all present and correct

## Common Issues and Fixes

| Issue | Typical cause | Fix |
|-------|---------------|-----|
| High TTFB (> 800 ms) | CDN cache cold or origin slow | Warm cache; check CDN cache headers; move origin closer to users |
| Large LCP image | Cover loaded at full size for small card | Add `srcset` with 400w and 848w variants; preload first cover |
| Render-blocking CSS | External CSS in `<head>` | Preload CSS with `rel="preload" as="style"`; inline critical CSS if needed |
| Unused JavaScript | Next.js runtime + ads | Accept baseline; do not load non-critical scripts above the fold |
| Google Fonts flash | Missing `display=swap` | Add `display=swap` to font URL |
| Console errors | Ad blocker / extensions | Verify site code has no errors; ignore ad-block related failures |

## Reporting

Save the JSON report to `lighthouse/` in the site repository. Keep the last 3 reports for trend comparison. Summarize:

- Median scores across 3 runs
- Top 3 slowest resources
- Any accessibility or best-practice failures
- Whether the build passes the go-live threshold

## Failure Handling

If a build fails Lighthouse QA:

1. Fix site code issues first (images, preload, fonts, contrast, headings).
2. Re-run 3 times and re-check median.
3. If scores are still low due to CDN/third-party latency, document the blocker and decide whether to delay launch.
4. Do not ship a build with Performance < 60 or Accessibility < 90.
