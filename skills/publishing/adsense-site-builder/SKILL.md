---
name: adsense-site-builder
description: builds and audits adsense-ready niche websites from idea to launch. use when asked to create one or many websites for adsense approval or monetization, including niche validation, keyword planning, site architecture, useful page or tool creation, trust pages, technical seo, adsense readiness review, and safe initial traffic plans without invalid traffic tactics.
---

# AdSense Site Builder

## Two Core Goals

Every decision in this pipeline serves exactly two goals:

**Goal 1 — Pass AdSense review on the first submission.**
The site must have: real working utility, sufficient original text-primary content with complete sentences (15+ complete pages is the practical safe threshold — Google has no stated minimum but "sufficient content" is the requirement), a Privacy Policy that explicitly names Google AdSense and its cookies, a working About and Contact page, HTTPS, a submitted sitemap, pages indexed in Google Search Console, and no policy violations. These are not optional. Missing any single one causes rejection.

**Goal 2 — Earn compounding organic search traffic.**
The same site, targeting low-competition long-tail keywords, with correct on-page SEO, schema markup, and an internal link architecture that builds topical authority over time. Organic traffic is how the site makes AdSense revenue after approval — and it is the only traffic source AdSense considers high-quality.

These goals are not in tension. The qualities that pass AdSense — real utility, original content, clear identity, technical correctness, real users — are identical to the signals that earn organic ranking. Build for real users first. Both goals follow.

## Operating Principles

- Real user utility is the only moat. A site a user would bookmark, share, or return to will pass review and rank. A site that exists only for keywords will fail both.
- Prefer interactive tools, template libraries, directories, comparison hubs, checklists, and tutorial hubs over generic article farms.
- Never recommend traffic exchanges, bot traffic, paid traffic packages, forced ad interactions, or thin AI-generated pages.
- Keep every output inspectable: write assumptions, inputs, quality gates, and next steps into project files.
- Do not mark a site ready until it has real utility, complete trust pages, technical SEO basics, and a safe launch plan.
- The readiness audit is a hard gate, not a formality. Do not advance to submission if the audit returns "not ready" or "needs revision" without resolving the issues first.

## Site Building Pipeline

Run these phases in order unless the user explicitly starts from an existing artifact.

| Phase | Load Reference | Required Output | Timing |
| --- | --- | --- | --- |
| 1. niche validation | `references/niche-opportunity-researcher.md` | `outputs/niches.json` | before building |
| 2. keyword and SEO planning | `references/keyword-cluster-planner.md` | `outputs/<site>/site-map.json` + `outputs/<site>/site-brief.md` (initialized) | before building |
| 3. page model and visual design | `references/programmatic-seo-architect.md` | `outputs/<site>/page-model.md` | before building |
| 4. site build + trust pages | `references/useful-site-builder.md` | working site files + trust pages + technical SEO files | build |
| 5. pre-launch distribution plan | `references/distribution-launcher.md` | `outputs/<site>/launch-plan.md` | **before go-live** |
| 6. go-live + GSC setup | `references/go-live.md` | site live, GSC registered, sitemap submitted | launch day |
| 7. AdSense readiness audit | `references/adsense-readiness-auditor.md` | `outputs/<site>/adsense-readiness-report.md` | **2–4 weeks post-launch** |
| 8. search growth loop | `references/gsc-growth-loop.md` | monthly query report + content update log | monthly, post-approval |

**Phase sequencing rationale:**
- Trust pages are built in phase 4 alongside content pages — they are part of the site, not a separate step. Separating them created a hidden dependency where phase 4 could "complete" without the site being launchable.
- Phase 5 (distribution plan) must be complete *before* go-live so the first 2–4 weeks of traffic are guided from day one. Preparing the plan after launch means the highest-leverage early period is wasted.
- Phase 6 (go-live) executes the distribution plan immediately.
- Phase 7 (audit) requires 2–4 weeks of real GSC data — indexing, impressions, crawl coverage. Run it only after that window passes. Do not submit AdSense the same day the site launches.

## Phase Execution Protocol

Execute phases one at a time. Track progress with the best mechanism available in the current environment:

**If `TaskCreate` / `TaskUpdate` are available** (Claude Code): use them. Create all 8 phase tasks at session start (`pending`), flip to `in_progress` when entering a phase, `completed` when done. Use `TaskGet` on re-entry to restore state.

**If those tools are not available** (other agents / API): print a compact text progress block at each phase boundary instead:

```
[ AdSense Site Builder — Phase 3 / 8 ]
✓ 1 Niche  ✓ 2 Keywords  ▶ 3 Page Model  ○ 4 Build  ○ 5 Distribution
○ 6 Go-live  ○ 7 Audit (2–4 wks post-launch)  ○ 8 Growth Loop (monthly)
```

**Rules (apply in both modes):**
- One phase per response turn. Never advance to the next phase without an explicit user confirmation.
- Load the phase's reference file only when entering that phase — not before.
- If a phase is skipped, mark it done with a note explaining why, then pause.
- On re-entry, restore or reprint current state before proceeding.
- Phases 7 and 8 have external timing dependencies. When completing Phase 6, remind the user: Phase 7 requires 2–4 weeks of real GSC data; Phase 8 runs monthly post-approval.

## Default Batch Workflow

When the user asks to create multiple sites:

1. Ask only for missing hard constraints: target language, country/market, preferred tech stack, and batch size. Default: English, United States, static Next.js or Astro, 3 sites.
2. Generate at least 3× more niche candidates than the final batch size before scoring any.
3. Score and select the strongest candidates. Choose the right site pattern for each.
4. For each site, run the full pipeline and produce all artifacts.
5. Stop or revise when any phase fails a quality gate. Never lower the bar silently.

## Quality Gates

A site is not ready to submit for AdSense if any of these are true:

**Content:**
- Fewer than 15 complete, indexable pages with distinct original content. (Google's official standard is "sufficient content" with no stated minimum — 15 is the practical safe threshold; fewer than 10 is almost always insufficient.)
- Content is primarily images, videos, or animations rather than text. Google's policy explicitly requires text-primary content.
- Any page contains only headlines and bullet points without complete sentences and paragraphs. Google's policy explicitly requires complete sentences.
- Any page consists of auto-generated content or content with no original information.
- The primary tool, calculator, or interactive experience does not work or produces no useful output.
- Any placeholder text ("Lorem ipsum", "Coming soon") exists on published pages.
- Affiliate content makes up the majority of the site without adding substantial original value beyond the linked product pages.

**Trust:**
- Privacy Policy is missing, or does not explicitly mention Google AdSense, the DoubleClick cookie, and the Google Ads Settings opt-out link.
- About page is missing.
- Contact page is missing or non-functional.

**Technical:**
- Site is on HTTP. HTTPS is required.
- sitemap.xml does not exist or is not submitted to Google Search Console.
- Pages are not indexed in GSC, or GSC shows zero impressions.
- Title tags exceed 60 characters or are missing.
- Schema markup is absent from the primary tool and FAQ pages.
- `<html lang>` attribute is missing or set to the wrong locale.
- Any interactive touch target (button, link) is below 44×44px on mobile.
- Core Web Vitals: LCP target < 2.5s ("Good"); fails if LCP > 4s on mobile (Google "Poor" threshold).
- Site ships with the default Next.js favicon or a missing logo asset.

**Safety:**
- Any banned category content (adult, gambling, weapons, drugs, hate, piracy) exists anywhere.
- The launch plan recommends traffic exchanges, bots, or incentivized clicks.
- The readiness audit returned "not ready" or "needs revision" and issues were not resolved.

## Output Contract

```txt
<project-root>/
  README.md               ← operations guide, generated at end of phase 4
  public/
    llms.txt              ← AI crawler index, generated from site-map.json at end of phase 4
    llms-full.txt         ← optional: full text of 3–5 key pages for AI citation
outputs/
  niches.json
  <site-slug>/
    site-brief.md
    site-map.json
    page-model.md
    adsense-readiness-report.md
    launch-plan.md
    gsc-report.md         ← added by phase 8, monthly post-approval
```

For actual web projects, follow the user's repository structure. Keep `outputs/<site-slug>/` as the planning and audit record regardless.

## Reference Loading

Load references only when entering that phase. Do not preload.

- `niche-opportunity-researcher.md` — find and validate the niche.
- `keyword-cluster-planner.md` — build the site map and SEO foundation.
- `programmatic-seo-architect.md` — define page templates and visual direction. Applies to all site types, not only programmatic ones.
- `useful-site-builder.md` — build the site, trust and identity pages, all technical SEO files, and ad placement structure.
- `distribution-launcher.md` — create the organic-first traffic plan **before go-live** so it executes from day one.
- `go-live.md` — execute on launch day: submit sitemap, set up GSC, run Day 1 distribution action.
- `adsense-readiness-auditor.md` — run the audit **2–4 weeks after go-live**, when GSC has real impression data.
- `gsc-growth-loop.md` — run the monthly content iteration loop after AdSense approval.

## Safe Traffic Rule

Organic search, community answers, directories, newsletters, short educational demos, and Pinterest for visual niches are the only channels worth recommending before AdSense approval. Small paid search tests are acceptable after GSC shows real query intent. Never recommend traffic packages, bots, automated browsing, click incentives, or anything that inflates impressions or clicks artificially.
