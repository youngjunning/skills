# Useful Site Builder

Use this reference during phase 4 to build the complete site experience: pages, interactive utility, technical SEO files, and ad placement structure. This is the phase that most directly determines whether the site passes AdSense review and earns organic traffic.

Do not finish this phase until every item in the completion gate is checked. A partially built site that proceeds to the audit is a wasted submission attempt.

---

## Inputs

Before building anything, load these artifacts produced by earlier phases:

- `outputs/niches.json` — read the `competitive_brief` for this site's entry (produced in phase 1). Used in Step 0.
- `outputs/<site-slug>/site-map.json` — the full page list and internal link map from phase 2. Every page in this file must be built.
- `outputs/<site-slug>/page-model.md` — the visual direction, token system, anchor choice, and page templates from phase 3. The build must match the design read, token system, and dial settings defined there. Do not deviate from the token system without documenting why.

---

## Step 0: Load the competitive brief

Before choosing a pattern or writing any page, read `competitive_brief` from this site's entry in `outputs/niches.json` (produced in phase 1). It is the differentiation baseline — the build's job is to be measurably better than the incumbents on the specific weaknesses recorded there.

Turn the brief into a checklist before building. Iterate **every entry in the array** and account for each one — Phase 4 is the last build phase before launch, so it is the backstop for all of them regardless of `acts_in_phase`. Route each entry by its token to decide *where* to verify:

- `acts_in_phase: "build"` — write down the concrete on-page requirement it imposes (e.g. "incumbent's top page has no worked examples → mine needs ≥ 3" or "incumbent's CWV is poor → hold LCP < 2.5s and ship a working tool they lack"), and fold it into the relevant page's content outline.
- `acts_in_phase: "keywords"` — confirm the missing sub-topic / page angle made it into the phase 2 cluster and exists as a real page in the site map. If it did not, add the page now.
- `acts_in_phase: "page_model"` — confirm the differentiating tool/asset is in the phase 3 page model and is actually being built. If it was dropped, build it now.
- **Any other value, or a missing/empty `acts_in_phase`** — do not skip it. Treat it as `build` (handle it on-page here), and correct the brief entry's token so the record is clean. An unrecognized token is a defect to fix, never a reason to drop the entry.

Every entry must end the phase in one of two states: **verified present and better than the incumbent**, or — only if genuinely out of scope — explicitly noted with a reason. An entry that is silently absent is a failed gate, not an acceptable omission.

If `competitive_brief` is empty or absent (e.g. the user skipped phase 1), note that the build has no differentiation baseline and apply the content-depth standards below as the floor. Do not invent competitor weaknesses — build to the standards instead.

---

## Site Patterns

Choose the pattern that best fits the niche. Do not default to a mini tool if a richer pattern serves the user better.

| Pattern | Best For | Primary Asset |
| --- | --- | --- |
| Tool site | calculators, converters, generators, checkers | working interactive tool with real output |
| Template library | resumes, emails, Notion pages, docs, prompts | copyable/downloadable templates with preview |
| Directory site | software, resources, datasets, services | curated list with filters and item detail pages |
| Comparison hub | SaaS alternatives, product choices, methods | comparison tables with decision criteria |
| Checklist hub | visa, moving, school, business setup | step-organized checklists with printable format |
| Tutorial hub | coding errors, Excel formulas, software workflows | step-by-step guides with prerequisites and troubleshooting |
| Hybrid site | niches with multiple intents | one primary utility + supporting clusters across types |

---

## Content Depth Standards

These are quality depth guidelines per page type. Google has no official word count minimum — "sufficient content" is the stated standard. The guidance below reflects what depth is typically needed to genuinely answer the user's question at each page type. A page that is thinner than these guidelines is almost always too shallow to satisfy users or earn ranking — but these are not AdSense policy numbers.

### Primary tool or resource page

The most important page on the site. It must:

- Provide a real, functional interactive experience — not a mockup.
- Show clear input controls with helpful labels and defaults.
- Produce a meaningful, specific output — not "your result is 42" without context.
- Include at least 3 worked examples showing different input scenarios.
- Explain the formula, algorithm, or curation logic — not just the result.
- State assumptions and edge cases explicitly.
- Link to at least 3 related supporting guides.
- Include a FAQ section with 5+ questions answered specifically (not generically).

Depth guideline: 800+ words of body content outside the interactive element is typically needed to cover worked examples, edge cases, and FAQ at the depth users expect. Shorter pages are usually shallow.

### Supporting guide pages

Each guide must address exactly one search intent. It must:

- Answer the primary keyword question in the first paragraph.
- Use a clear H2/H3 heading hierarchy covering distinct sub-topics.
- Include at least one fully worked example (numbers, steps, or output).
- Include a "common mistakes" or "when this doesn't apply" section.
- Link back to the primary tool page and to 2–3 related guides.
- End with a clear next action for the reader.

Depth guideline: 700+ words is typically needed to cover a topic at the depth users expect. Shorter guides are usually thin; longer is appropriate for complex topics.

### Template pages

Each template page must:

- Display the complete, ready-to-use template — not a screenshot, not a locked preview.
- Provide a one-click copy button or direct download.
- Explain when to use this template (use case, audience, scenario).
- Include at least one completed example showing real content filled in.
- List customization notes: what to change, what not to.
- State common mistakes when using this template type.
- Link to the category page and to 2–3 related templates.

### Directory and comparison pages

Each item listing or comparison page must:

- Use real, verifiable information — no fabricated data points.
- Apply consistent fields across all items (price, features, pros, cons, best-for).
- State the evaluation criteria and how they were applied.
- Avoid pretending to have tested or used products unless evidence is provided.
- Link to the official source for each listed item.

---

## Ad Placement Structure

Build the ad placement structure into every page template from the start. Do not treat ads as an afterthought.

### Before AdSense approval

Add the AdSense auto-ads script to the `<head>` of every page immediately — this is required for Google to verify site ownership during the review process. Do not add manually placed ad units before approval. Auto-ads will not show until the account is approved; the script presence is what matters for the review.

```html
<!-- AdSense verification script — add to <head> before submission -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXX"
     crossorigin="anonymous"></script>
```

Replace `ca-pub-XXXXXXXXXX` with the actual publisher ID. Mark it as a placeholder if the user has not provided one yet.

### Ad placement rules (post-approval)

Follow these placement rules to maximize revenue without triggering policy violations:

| Placement | Rule |
| --- | --- |
| Above the fold | Ads must not occupy more than 30% of the visible viewport on any screen size. Primary content must be visible without scrolling. |
| Below the hero | Place the first ad unit after the primary tool output or after the first 200 words of body content — not before. |
| Within long content | One ad unit every 500–800 words in long-form guides. Never between two consecutive ad units without content in between. |
| Sidebar | Acceptable on desktop only. Must not overlap with the main content column on mobile. |
| After the primary tool | Place one ad unit below the tool result area, after the user has received their output. Do not place ads above the tool inputs where they block the primary experience. |
| Footer | Acceptable. One unit maximum. |
| Between navigation elements | Never. Ads placed inside or immediately adjacent to navigation links risk invalid clicks. |
| Inline with interactive elements | Never. Ads mixed into calculator inputs, template download buttons, or checklist checkboxes are a policy violation. |

### Ad slot placeholders in page templates

During the build phase, mark every intended ad slot with a clear comment so it is easy to activate post-approval:

```html
<!-- AD SLOT: below-tool-result — 728x90 leaderboard desktop / 320x50 mobile -->
<!-- activate after AdSense approval with correct ad unit code -->
```

---

## Technical SEO Implementation

Build all of these into the project during phase 4. Do not leave them for the audit phase.

### sitemap.xml

Generate dynamically or statically. Must include every indexable page with its `<lastmod>` date.

For Next.js, use `next-sitemap`:
```bash
yarn add next-sitemap
```

```js
// next-sitemap.config.js
module.exports = {
  siteUrl: 'https://your-domain.com',
  generateRobotsTxt: true,
  exclude: ['/api/*', '/admin/*'],
}
```

For Astro, enable the built-in sitemap:
```js
// astro.config.mjs
import sitemap from '@astrojs/sitemap';
export default defineConfig({
  site: 'https://your-domain.com',
  integrations: [sitemap()],
});
```

### robots.txt

```txt
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/

Sitemap: https://your-domain.com/sitemap.xml
```

### llms.txt

`llms.txt` is a plain-text file at the site root that tells AI crawlers (Perplexity, ChatGPT, Google AI Overview) which pages exist and how to understand the site. It is the AI-crawler equivalent of `robots.txt` — it does not block crawlers but guides what they should read and how they should describe the site.

**Why it matters for GEO:** Sites with a well-structured `llms.txt` are more likely to be cited correctly in AI answers. The file directly signals the site's purpose, the tool's name, and which pages are authoritative — the same information AI systems need to form accurate citations.

**Auto-generate from `site-map.json`:** Since the site map already lists every page with title, path, description, and intent, `llms.txt` can be generated mechanically at end of phase 4.

Format (write to `public/llms.txt` for Next.js, `static/llms.txt` for Astro):

```txt
# [Site Name]

> [One sentence: what the site does and who it's for.]

## Primary Tool

- [Tool Name](/path): [One sentence describing what the tool does and what output it produces.]

## Guides and Resources

- [Page Title](/path): [One sentence describing the page's topic and what the user learns or gets.]
- [Page Title](/path): [One sentence.]
...

## Reference Pages

- [FAQ](/faq): [One sentence.]
...

## About

- [About](/about): [One sentence about the site's purpose and who maintains it.]
- [Contact](/contact): Contact form for questions and feedback.
- [Privacy Policy](/privacy): Privacy policy covering data use and Google AdSense cookies.
```

**Generation rules:**
- One entry per indexable page. Exclude `/api/*`, `/admin/*`, and any `noindex` pages.
- Descriptions must be original — do not copy the meta description verbatim. Write from the AI citation perspective: "This page explains..." or "Use this tool to..."
- The `>` intro line (the site description) is the highest-weight signal — write it to match the site's primary keyword and purpose clearly.
- Group pages by cluster: primary tool first, then guides, then reference/FAQ, then trust pages. Order within each group by importance (most traffic expected → first).
- Optionally also generate `public/llms-full.txt` with the full text content of the 3–5 most important pages (primary tool page + top guides). This is especially valuable when the site has original data or worked examples that AI systems should quote directly.

### Fonts

Load any display or heading web font via `next/font` — never via a Google Fonts `<link>` tag in production.

`next/font` self-hosts font files alongside your deployment: no third-party requests at runtime, GDPR-compliant by default, and it applies a `size-adjust` on the fallback metric automatically — which is what actually holds CLS near zero during the swap. A bare `font-display: swap` does not prevent the text-shift; only a matching fallback metric does.

```ts
import { Geist } from 'next/font/google'

const geist = Geist({ subsets: ['latin'], variable: '--font-sans' })
```

**Rules:**
- **Body text:** prefer system font stacks (`system-ui`, `-apple-system`, `Georgia`, or equivalent). Zero load time, zero CLS, equally readable.
- **Display / headings:** one family maximum, loaded via `next/font`. Subset to the characters actually used (`subsets: ['latin']`).
- **CJK body:** never load a CJK web font for mobile body text. System stacks (Hiragino, Yu Gothic, Noto) are faster and equally correct. Load a custom CJK font lazily only if a user explicitly selects it.

### Images

- Always set `width` and `height` on every `<img>` (and on `next/image`). Unset dimensions cause CLS during load.
- Use `next/image` for all images in Next.js projects — it negotiates WebP/AVIF automatically, applies lazy loading by default, and reserves space to prevent CLS.
- Add `priority` prop to the first above-the-fold image (home page hero or primary tool screenshot).
- Target under 150KB per hero or card image at display size. Compress before shipping.
- CSS placeholders (flat color, no heavy gradients) are acceptable when no real image is available — always set explicit dimensions.

### Canonical URLs

Every page must include a self-referencing canonical tag:

```html
<link rel="canonical" href="https://your-domain.com/exact-page-path" />
```

No trailing-slash variation. No query parameters in canonical URLs. Consistent throughout.

### Schema Markup Implementation

Implement schema for each page type. Use JSON-LD in the `<head>`.

**Tool / calculator page:**
```json
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Tool Name",
  "description": "What this tool does",
  "applicationCategory": "UtilitiesApplication",
  "operatingSystem": "Web",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }
}
```

**How-to guide:**
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to [do the thing]",
  "description": "A concise description",
  "step": [
    { "@type": "HowToStep", "name": "Step 1", "text": "Description" },
    { "@type": "HowToStep", "name": "Step 2", "text": "Description" }
  ]
}
```

**FAQ sections:**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Question text?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Answer text."
      }
    }
  ]
}
```

**Article / guide pages:**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Page title",
  "datePublished": "2025-01-01",
  "dateModified": "2025-01-01",
  "author": { "@type": "Organization", "name": "Site Name" }
}
```

### Internal Links

Every page must link outward and receive links. Build this from the site-map.json link map.

- Primary tool page: links to 3+ supporting guides.
- Every supporting guide: links back to the primary tool + 2–3 related guides.
- Homepage: links to primary tool, at least 3 guides, and the FAQ page.
- No orphan pages — every page must be reachable from at least one other page.

---

## Core Web Vitals

These affect both organic ranking and AdSense ad performance. Implement from the start; do not retrofit.

| Metric | Target | Implementation |
| --- | --- | --- |
| LCP (Largest Contentful Paint) | < 2.5s | Server-render hero content. Preload the LCP image with `<link rel="preload">`. Avoid lazy-loading the hero image. |
| CLS (Cumulative Layout Shift) | < 0.1 | Specify `width` and `height` on every `<img>`. Reserve space for ad slots with `min-height`. Avoid inserting content above existing content after load. |
| INP (Interaction to Next Paint) | < 200ms | Minimize client-side JavaScript on initial load. Defer non-critical scripts. Run heavy calculations in a Web Worker if they take > 50ms. |

For AdSense specifically: ad units that inject late cause CLS. Reserve the ad slot space before the ad loads:

```css
.ad-slot {
  min-height: 90px; /* leaderboard */
  background: transparent;
}
```

---

## Pattern-Specific Build Requirements

### Tool sites

- All input fields have labels (not just placeholders).
- Form submits without page reload. Results update in place.
- Every edge case produces a meaningful message, not a blank result or NaN.
- The calculation or generation logic is explained below the tool with real examples.
- Include a "How to use this tool" section with step-by-step instructions.
- Test at minimum: zero inputs, extreme inputs, typical inputs, and at least one error case.

### Template libraries

- Templates are copyable with a single click (Clipboard API).
- Each template has a preview mode that shows it filled in with realistic sample data.
- Category pages list all templates with a short description and link to each.
- Download option (TXT or DOCX) for templates longer than 200 words.

### Directory sites

- Inclusion criteria are published on the site (not hidden in the About page).
- Filters work without page reload.
- Each item page has a consistent field set: name, description, URL, category, last verified date.
- Mark data that may be outdated with a "last verified" date.

### Comparison hubs

- Evaluation criteria are stated explicitly before the comparison table.
- Tables render correctly on mobile (horizontal scroll or collapsed layout, not broken columns).
- Each comparison concludes with a "best for" recommendation, not just a neutral data dump.
- Caveats section: note what this comparison does not cover.

### Checklist hubs

- Checklists are printable (CSS print styles) and copyable as plain text.
- Items are organized by phase or deadline, not alphabetically.
- Each item has a short rationale (why this step matters).
- Provide a "download as PDF" or "copy to clipboard" action for each checklist.

### Tutorial hubs

- Every tutorial states prerequisites at the top.
- Steps are numbered. Each step is atomic (one action per step).
- Every tutorial has an "expected result" section showing what success looks like.
- Common errors section with each error message and its fix.
- A "next steps" section linking to the next logical tutorial in the sequence.

---

## GEO (Generative Engine Optimization)

AI-powered search interfaces (Google AI Overviews, Perplexity, ChatGPT) increasingly answer queries directly, reducing clicks to organic results. Build content to be cited by these systems — not just ranked by traditional search.

### Content structure for AI citation

- **Lead with a direct answer.** The first paragraph of every supporting page should answer the primary question in 1–3 sentences. AI systems quote the most direct, unambiguous phrasing they find.
- **Use original data, examples, and computations.** AI systems prefer to cite sources that provide something they cannot generate themselves: real numbers, worked examples with specific inputs and outputs, current-year data, and first-hand observations. Generic summaries are never cited.
- **Structured definitions.** If a page introduces a term, define it clearly in the first sentence: "X is [definition]." This format is directly quotable by AI answers.
- **FAQ schema on every supporting page.** FAQ content is the highest-leverage GEO investment: it surfaces in Google's "People Also Ask" boxes AND is structured for AI to parse and quote. Every page should end with 3–5 specific, answered questions.
- **Cite sources within the content.** Pages that reference external authoritative sources (government data, academic studies, official documentation) are treated as more trustworthy by AI systems. Link out to sources you reference.

### The tool moat

Interactive tools are the strongest GEO defense. AI systems can describe how to use a calculator but cannot *be* a calculator — users who need their specific result must still visit the page. Every site in this skill has a primary tool for exactly this reason.

For tool pages specifically:
- The tool itself is the citation target. AI answers will say "use [site name]'s [tool name] to calculate this." Ensure the tool name is consistently stated on the page.
- Worked examples (with real inputs and outputs) are cited more than generic descriptions. Include at least 3 examples with distinct scenarios.

### GEO-vulnerable content to monitor

Flag these page types as at-risk after launch and watch their impressions in GSC:
- Simple definition pages ("what is X")
- Pages where the primary keyword already shows a fully-resolving AI Overview
- Short FAQ pages without original data

If impressions collapse on a GEO-vulnerable page within 3–6 months, the page needs either a tool angle, original data, or consolidation into a deeper resource.

---

## Site Identity Assets

Generate favicon and logo before writing any page component so they embed from day one.

Priority order:
1. **Codex** — provide: site name, niche, one-sentence purpose, accent color from the phase 3 token system, design anchor. Preferred.
2. **Claude native image generation** — if Codex is unavailable.
3. **SVG placeholder** — label clearly and note in the completion gate.

**Output paths:**
- Logo: `public/logo.svg` — inline SVG or `<img src="/logo.svg">` in the header. Fallback: site name as styled text in the token system typeface and accent color.
- Favicon source: `public/favicon-32x32.png` (32×32 PNG) — also convert to `public/favicon.ico`.
- Apple touch icon: `public/apple-touch-icon.png` (180×180).

Wire up in `src/app/layout.tsx` via Next.js metadata:

```ts
export const metadata: Metadata = {
  icons: {
    icon: '/favicon-32x32.png',
    apple: '/apple-touch-icon.png',
  },
}
```

Do not ship with a browser-default blank favicon or a missing logo — both signal an incomplete site to Google reviewers.

---

## Trust and Identity Pages

Build these pages as part of the site in phase 4. All are required for AdSense approval and must be linked from the global footer of every page. The completion gate below confirms they exist before the distribution plan (phase 5) begins.

### Privacy Policy (AdSense hard requirement)

The most critical trust page for AdSense approval. Must explicitly state:

1. The site uses **Google AdSense** to display advertisements.
2. Google uses **cookies** (including the DoubleClick cookie) to serve ads based on user visits.
3. Users can opt out of personalized advertising via **[Google's Ads Settings](https://adssettings.google.com)**.
4. What other data the site collects (email submissions, analytics, session data).
5. Whether the site uses **Google Analytics** or other tracking tools.
6. A link to the **Google Privacy Policy** at `https://policies.google.com/privacy`.

Generate the full text. Do not link to an external generator and assume it is complete.

### About

States who runs the site (person, team, or project — no fake credentials), what the site helps users do, why it was built, and when it launched or was last updated. If the owner has not provided identity details, use a transparent brand or project identity and mark all placeholders clearly for the owner to fill in before submission.

### Contact

Provide at minimum one of: a working email address or a functional contact form. The contact path must work when tested — Google reviewers will test it. Do not use a non-functional placeholder.

### Terms of Use

Required whenever the site includes interactive tools, calculators, or outputs users act on. Must cover: acceptable use, a disclaimer that tool outputs are informational only and not professional advice, limitations of liability, and a DMCA or content removal policy if the site hosts user-generated content.

### Content rules for all trust pages

- Written in plain language — not unread legal boilerplate.
- No fabricated credentials or unverifiable authority claims.
- Hosted on the same domain (not a subdomain or externally hosted page).
- Not blocked by `robots.txt` or tagged `noindex`.
- Linked from the global footer on every page.

After building, add the status to `outputs/<site-slug>/site-brief.md`:

```md
## Trust Pages

- Privacy Policy: done | needs AdSense/cookie language | needs legal review
- About: done | needs owner details
- Contact: done | needs working email or form endpoint
- Terms of Use: done | not applicable | needs review

## AdSense Privacy Policy Checklist
- [ ] Mentions Google AdSense by name
- [ ] Mentions cookies / DoubleClick cookie
- [ ] Links to Google Ads Settings opt-out
- [ ] Links to Google Privacy Policy
- [ ] Covers other data collection (analytics, forms)
- [ ] Linked from every page footer
```

---

## Completion Gate

Before advancing to phase 5 (pre-launch distribution plan), verify all of the following:

**Content:**
- [ ] Primary tool or resource works correctly. Tested with at least 3 input scenarios including an edge case.
- [ ] Every entry in `competitive_brief` is accounted for — count the entries, not the tokens. Each is verified present and better than the incumbent on the relevant page, or explicitly noted as out of scope with a reason (or the brief was empty). Entries with an unknown/missing `acts_in_phase` were handled as `build`, not skipped. No entry is silently absent. The site beats the incumbents, not just matches them.
- [ ] All 15+ pages are complete. No placeholder text.
- [ ] Every page meets the content depth standard for its type.
- [ ] No page exists only to target a keyword without adding value for the user.
- [ ] Every page has a distinct H1, title tag (50–60 chars), and meta description (150–160 chars).

**Technical SEO:**
- [ ] sitemap.xml generated and includes all indexable pages.
- [ ] robots.txt present at root and correct.
- [ ] Canonical URLs on every page.
- [ ] Schema markup implemented for the primary tool page, all FAQ sections, and all how-to guides.
- [ ] Internal link map fully implemented. No orphan pages.
- [ ] Alt text on all images.

**Performance:**
- [ ] LCP < 2.5s on mobile (verify with PageSpeed Insights or Lighthouse).
- [ ] CLS < 0.1 (no layout shifts from ad slots or late-loading images).
- [ ] No layout-thrashing JavaScript on page load.

**Ad structure:**
- [ ] AdSense auto-ads script added to `<head>` of every page.
- [ ] Ad slot placeholders marked in page templates with comments.
- [ ] No ads placed above primary content or inside interactive elements.
- [ ] Ad slot CSS reserves minimum height to prevent CLS.

**Mobile:**
- [ ] Site renders correctly at 375px viewport.
- [ ] No horizontal scroll on any page.
- [ ] Touch targets (buttons, links) are at least 44×44px.
- [ ] Font size ≥ 16px for body text.

**Trust pages:**
- [ ] Privacy Policy is live and passes the AdSense checklist: names Google AdSense, mentions the DoubleClick cookie, links to Google Ads Settings opt-out, links to the Google Privacy Policy, covers any other data collection.
- [ ] About page is live. No fabricated credentials or unverifiable claims.
- [ ] Contact page is live with a working email or functional form endpoint — tested, not a placeholder.
- [ ] Terms of Use is live for any site with interactive tools or user-actionable outputs.
- [ ] All trust pages are linked from the global footer on every page.
- [ ] No trust page is blocked by `robots.txt` or tagged `noindex`.
- [ ] `outputs/<site-slug>/site-brief.md` trust pages section is complete.

**Site identity:**
- [ ] Favicon and Apple touch icon are in place (not browser-default blank).
- [ ] Logo or site name mark is in the header and matches the token system.

**Technical SEO files:**
- [ ] `public/llms.txt` (or `static/llms.txt`) generated from `site-map.json` — every indexable page listed with a one-sentence description, grouped by cluster (primary tool → guides → reference → trust pages).
- [ ] `llms.txt` intro line (`>`) accurately describes the site purpose in one sentence matching the primary keyword.
- [ ] `sitemap.xml` includes every indexable page.
- [ ] `robots.txt` allows Googlebot; disallows `/api/` and `/admin/`.

**Project README:**
- [ ] `README.md` generated in the project root using the Operations Guide template below.

---

## Project README — Operations Guide Template

Generate `README.md` in the project root at the end of phase 4. Fill in the site-specific values. This file is the single reference point for every post-launch operational task.

````md
# [Site Name] — Operations Guide

## Site Overview

| Field | Value |
| --- | --- |
| Niche | [one-line description] |
| Primary keyword | [keyword] |
| Target market | [e.g. en-us, en-gb] |
| Site URL | [https://your-domain.com] |
| Launch date | [YYYY-MM-DD — fill in on go-live] |

## Pipeline Status

| Phase | Status | Artifact |
| --- | --- | --- |
| 1. Niche validation | ✅ done | `outputs/niches.json` |
| 2. Keyword planning | ✅ done | `outputs/<site>/site-map.json` |
| 3. Page model | ✅ done | `outputs/<site>/page-model.md` |
| 4. Site build + trust pages | ✅ done | — |
| 5. Distribution plan | ⬜ todo | `outputs/<site>/launch-plan.md` |
| 6. Go-live | ⬜ todo | — |
| 7. AdSense audit | ⬜ todo | `outputs/<site>/adsense-readiness-report.md` |
| 8. Monthly growth loop | ⬜ ongoing | `outputs/<site>/gsc-report.md` |

---

## Phase 5 — Distribution Plan (before go-live)

See `outputs/<site>/launch-plan.md` for the full 14-day sequence.

**Safe channels:**
- Organic search (submit sitemap on launch day)
- Directory submissions: Product Hunt, Indie Hackers, AlternativeTo, niche directories
- Community participation: Reddit, Quora, Discord — answer first, link when genuinely helpful
- Pinterest (for template/checklist/visual niches): 3 pins/week, one board per page cluster
- YouTube Shorts: 60-second screen demo of the primary tool, keyword in title
- Newsletter/creator outreach: offer a preview to relevant newsletters in the niche

**Metrics to watch (weeks 1–4):**
- Average session duration > 45s
- Pages per session > 1.5
- Return visitor rate (growing)
- Tool completion rate (users who start the tool finish it)

**Never do this:**
- Traffic packages, bot visits, autosurf, traffic exchanges
- Incentivized clicks or click rings
- Paid display/social ads before AdSense approval
- Any tactic whose goal is hitting a visit count rather than reaching real users

---

## Phase 6 — Go-Live Day

- [ ] Site live on final domain (not staging)
- [ ] HTTPS active, no mixed-content warnings
- [ ] `sitemap.xml` submitted to Google Search Console
- [ ] Homepage + primary tool page requested for indexing via GSC URL Inspection
- [ ] GA4 tracking active (if included in plan)
- [ ] Day 1 action from `launch-plan.md` executed

---

## Phase 7 — AdSense Readiness Audit (2–4 weeks post-launch)

See `outputs/<site>/adsense-readiness-report.md` for the full checklist.

**Prerequisites before submitting:**
- Site live on final domain ≥ 2 weeks
- GSC shows ≥ 15 indexed pages
- GSC shows real impressions (not zero)
- All blocking items in the readiness report pass

**Run the audit before submitting.** A rejected account delays approval and raises scrutiny on resubmission.

---

## Phase 8 — Monthly Growth Loop

Update `outputs/<site>/gsc-report.md` each month.

**Monthly process:**
1. Open GSC → Performance → Search results. Set date: last 28 days vs previous 28 days.
2. **Quick wins** (position 8–20, ≥ 50 impressions): improve the page — add a section, example, or FAQ that the top 3 results have and the page lacks.
3. **Low CTR** (impressions > 100, CTR < 2%): rewrite the title tag and meta description to match actual search intent.
4. **Content gaps** (queries landing on the wrong page): build a dedicated supporting page for that query.
5. **Declining pages** (clicks falling month-over-month): audit against current top-3 results and update.
6. Pick top 3–5 actions. Do not try to fix everything at once.

**Healthy growth signals:**
- Organic impressions growing month-over-month
- Organic CTR: 3–8% for informational, 1–3% for navigational queries
- Average position gradually improving over 3–6 months
- New long-tail queries appearing (topical authority building)
- All sitemap pages indexed (no "Discovered — currently not indexed" issues)

**Problem signals — act immediately:**
- Sudden drop on a specific page → audit against current top-3, improve and re-index
- "Discovered — currently not indexed" → thin content likely, improve and re-request
- Core Web Vitals failing in GSC → run PageSpeed Insights, fix the regression

**Ad optimization (post-approval):**
- Start with auto-ads for the first 60 days.
- After 60 days: compare RPM on pages with manual placements (below tool result, after first body paragraph) vs auto-ads-only pages.
- Tool pages typically earn higher RPM than guide pages — prioritize their improvement.
- If ads cause CLS or dominate the mobile viewport, reduce placement density. Long-term organic ranking matters more than marginal ad placement gain.

---

## Key Metrics Reference

| Metric | Target | Source |
| --- | --- | --- |
| Session duration | > 45s | GA4 |
| Pages per session | > 1.5 | GA4 |
| Organic CTR | 3–8% (info) / 1–3% (nav) | GSC |
| Average position | improving monthly | GSC |
| LCP mobile | < 2.5s | PageSpeed Insights |
| CLS | < 0.1 | PageSpeed Insights |
| Indexed pages | 100% of sitemap | GSC Coverage |
````
