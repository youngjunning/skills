# GSC Growth Loop

Use this reference during phase 8 — after AdSense is approved. Run this loop monthly to grow organic search traffic using real data from Google Search Console.

The organic growth loop is what converts a site that passed AdSense review into a site that earns consistent revenue. A site that stops improving after launch will plateau and eventually decline as competitors improve. This loop prevents that.

---

## Why This Loop Exists

Google's Helpful Content Update (HCU) was permanently merged into the core ranking algorithm in March 2024. It is no longer a one-time event — content quality now continuously affects search visibility as a persistent ranking signal. Sites that stop improving after launch will plateau and eventually decline as the algorithm reassesses them alongside improving competitors.

Running the GSC loop monthly:

- Finds queries where the site already appears but ranks too low to get clicks (positions 8–20).
- Identifies real user language that the site's content doesn't yet match.
- Discovers new page opportunities the original site map missed.
- Catches pages with declining performance before they drop off the first page.

---

## Monthly Loop: Four Steps

### Step 1: Pull the Data

In Google Search Console → Performance → Search results:

- Set date range: last 28 days vs. previous 28 days.
- Export: queries, pages, countries, devices.

Look at three views:

**View A — Position 8–20 queries (quick wins)**
Filter: Average position 8–20, at least 50 impressions. These pages are on the edge of page one. A small content improvement often moves them into positions 1–7 where click-through rate is 5–10× higher.

**View B — High impression, low CTR (title/description problems)**
Filter: impressions > 100, CTR < 2%. The page is appearing in results but users are not clicking. The title tag or meta description is not matching what users want to see.

**View C — Queries with no matching page (content gaps)**
Look for queries driving traffic to the homepage or primary tool page that would be better served by a dedicated page. These are real, proven search demands the site is not fully addressing.

### Step 2: Prioritize Actions

Rank opportunities by impact:

| Priority | Signal | Action |
| --- | --- | --- |
| 1 | Position 8–20, ≥ 50 impressions | Improve the existing page to move into top 7 |
| 2 | High impression, CTR < 2% | Rewrite title tag and meta description to match search intent |
| 3 | Query with no matching page, ≥ 30 impressions | Build a new supporting page targeting that query |
| 4 | Page with declining clicks month-over-month | Audit for content freshness, add examples, update outdated info |

Do not try to address all opportunities at once. Pick the top 3–5 per month.

### Step 3: Make the Changes

**Improving an underperforming page (position 8–20):**

1. Search the target query yourself. Read the top 3 results. What do they have that the site's page lacks?
2. Add a section, example, or data point that directly addresses the gap.
3. Make sure the primary keyword appears in the H1, the first paragraph, and at least one H2.
4. Add or improve the FAQ section with questions that appear in the "People Also Ask" box for this query.
5. Improve internal links to this page from 2–3 related pages.
6. Update the `dateModified` in the page's schema markup.

**Rewriting a title tag / meta description:**

1. The title must make the page's unique value obvious in 50–60 characters.
2. The meta description must explain what the user gets and why this page is worth clicking, in 150–160 characters.
3. Do not keyword-stuff. Write for the user, not the crawler.
4. After updating, use GSC URL Inspection to request re-crawl.

**Building a new page for a content gap:**

1. Treat it exactly like a new supporting page from phase 2 — distinct intent, correct keyword, required sections, schema markup, internal links.
2. Add the new URL to sitemap.xml.
3. Request indexing via GSC URL Inspection.
4. Link to the new page from the primary tool page and from at least 2 existing supporting pages.

### Step 4: Measure and Document

After making changes, track each improvement over the next 28 days:

- Did the page move from position 8–20 into position 1–7?
- Did the rewritten title improve CTR from < 2% to > 3%?
- Did the new page get indexed and start generating impressions within 14 days?

Document results in `outputs/<site-slug>/gsc-report.md`. This record drives future loop iterations.

---

## Signals That Indicate Healthy Organic Growth

| Metric | Healthy Trend |
| --- | --- |
| Organic impressions | Growing month-over-month as new pages index |
| Organic clicks | Growing; click growth should lag impressions by 4–8 weeks |
| Average CTR | 3–8% for informational queries; 1–3% for branded/navigational |
| Average position | Gradually improving for target keywords over 3–6 months |
| Indexed pages | All pages in sitemap are indexed; no "Discovered - currently not indexed" issues |
| New queries | Site appears for new long-tail queries it was not targeting — topical authority signal |

---

## Signals That Indicate Problems

Act on these immediately:

| Signal | Likely Cause | Action |
| --- | --- | --- |
| Sudden drop in clicks on a specific page | Google update, competitor improvement, content freshness, or AI Overview displacement | Check the SERP for that page's keyword — if an AI Overview now appears, see GEO section below |
| "Discovered - currently not indexed" in GSC | Google crawled the page but chose not to index it — thin content likely | Improve content depth and request re-indexing |
| High impressions, near-zero clicks | Page ranking for irrelevant queries, title mismatch, or AI Overview absorbing intent | Check queries driving impressions; if an AI Overview is present, optimize to be cited in it |
| Core Web Vitals failing in GSC | Performance regression, likely from a new dependency or image | Run PageSpeed Insights and fix the regressing metric |
| AdSense invalid traffic warning | Traffic source quality issue | Audit traffic sources; remove any non-organic channel that may be sending low-quality visits |

---

## GEO (Generative Engine Optimization) — Monthly AI Overview Audit

AI Overviews expand over time — a keyword without an AI Overview today may have one in 3 months. Run this check monthly alongside the standard GSC loop.

### Step 1: Identify AI Overview exposure

For every page with a month-over-month click decline greater than 20%:
1. Search the page's primary keyword in an incognito window.
2. Check whether a Google AI Overview now appears above organic results.
3. If yes — is the site being cited in the Overview? Check the Overview's source links.

### Step 2: Respond by signal

| AI Overview status | Action |
| --- | --- |
| No AI Overview | Drop is from another cause — investigate ranking, CWV, or content freshness |
| Overview present, site is cited | The citation is driving brand impressions even if organic clicks fell. Maintain the content quality that earned the citation. |
| Overview present, site is NOT cited | Optimize for citation: add a clear 1–3 sentence answer at the top of the page, add or improve FAQ schema, include original data or examples AI would prefer to attribute |
| Overview fully resolves the query, no citation possible | Accept organic CTR loss. Mitigate by: adding an interactive tool to the page (forces a visit), shifting SEO weight to tool-angle keywords for this topic |

### Step 3: GEO-proof new content

When building new pages in the monthly growth loop (View C — content gaps):
- Check if the target query shows an AI Overview before writing the page.
- If it does: lead with a direct quotable answer, include original worked examples, add FAQ schema.
- If it does not: build normally, but monitor for AI Overview appearance at the next monthly check.

### What GEO cannot take

Protect investment here — AI systems cannot displace:
- Interactive tools that produce user-specific results
- Template libraries where users need the actual copyable asset
- Directories with real, verified, current listings
- Original research, proprietary data, or first-hand tested content

If the site's primary asset is a tool, GEO risk is structurally low. Supporting content may lose clicks to AI Overviews but the tool page is protected.

---

## Ad Performance Optimization (post-approval)

Once AdSense is live, use the AdSense dashboard alongside GSC to optimize:

- **Auto-ads vs. manual placements:** Auto-ads are easier to start with. After 60 days, compare RPM on pages where you add manual placements in high-intent positions (below the tool result, after the first body paragraph) versus auto-ads-only pages.
- **Page RPM by page type:** Tool pages typically earn higher RPM than guide pages because users are in an active research/decision mode. Invest more in improving tool pages first.
- **Avoid over-monetization:** If ads cause CLS, reduce loading speed, or dominate the viewport on mobile, they will hurt organic ranking — which hurts long-term revenue more than a marginal ad placement gain.

---

## Output

Update `outputs/<site-slug>/gsc-report.md` monthly:

```md
# GSC Growth Report — [Month YYYY]

## Summary
- Total clicks this month: [X] (vs [X] last month)
- Total impressions: [X]
- Average CTR: [X%]
- Average position: [X]

## Quick Win Opportunities (position 8–20)
| Page | Query | Position | Impressions | Action Taken |
| --- | --- | --- | --- | --- |

## Title/Description Fixes (high impression, low CTR)
| Page | Query | Impressions | CTR | Change Made |
| --- | --- | --- | --- | --- |

## New Pages Built This Month
| Page | Target Query | Indexed? | Early Impressions |
| --- | --- | --- | --- |

## Declining Pages
| Page | Clicks Δ | Likely Cause | Action |
| --- | --- | --- | --- |

## Next Month Priorities
1.
2.
3.
```
