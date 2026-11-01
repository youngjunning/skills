# Go-Live Setup

Use this reference on **launch day** (phase 6). Execute this setup and the Day 1 actions from `outputs/<site-slug>/launch-plan.md` at the same time — they are the same event.

Do not go live until phase 4 (site build + trust pages) and phase 5 (distribution plan) are both complete.

---

## Google Search Console

1. Add the site as a property in Google Search Console using the domain verification method (preferred) or the HTML tag method.
2. Submit `sitemap.xml` immediately after the site goes live.
3. Use the URL Inspection tool to request indexing for the homepage and primary tool page.
4. Wait 2–4 weeks before running the AdSense readiness audit. Phase 7 requires real GSC impressions and indexed pages before it can return a meaningful verdict.

## Google Analytics (optional but recommended)

Add GA4 to track real user engagement metrics (session duration, return visitors, tool completion events). These signals confirm real user behavior to Google and help identify which pages need improvement.

If GA was not set up during the build phase, add it now before the site goes live so the full post-launch period has engagement data.

---

## Launch Day Checklist

- [ ] Site is live on the final domain (not a staging URL).
- [ ] HTTPS is active on all pages. No mixed-content warnings.
- [ ] `sitemap.xml` submitted to Google Search Console.
- [ ] Homepage and primary tool page requested for indexing via GSC URL Inspection.
- [ ] GA4 tracking active (if included in plan).
- [ ] Day 1 action from `outputs/<site-slug>/launch-plan.md` executed: Product Hunt listing, community post, or directory submission — whichever is first in the plan.
