# Keyword Cluster Planner

Use this reference during phase 2 to turn a selected niche into a site map and SEO foundation. The output drives both organic traffic and AdSense approval — a properly structured site with clear intent signals ranks faster and passes review more easily.

---

## Keyword Strategy for New Sites

New sites have no domain authority. Targeting broad, high-competition keywords first wastes effort and produces no traffic. Follow this priority order:

1. **Long-tail, low-competition keywords first** — specific queries (4–6 words) with clear intent and few strong competitors. These are the pages that will rank and bring the first organic visitors.
2. **Mid-tail supporting cluster** — once the primary tool or resource is live, surrounding it with related how-to guides, example pages, and FAQ pages builds topical authority.
3. **Head term last** — the homepage targets the broadest keyword in the niche. It will rank after the supporting pages build authority.

Use keyword difficulty estimates from Ahrefs (free tier), Semrush, or Google's keyword planner. For a brand-new site, prefer keywords with difficulty ≤ 30.

**GEO-specific research:** Run keyword research in the target market's Google, not the global index. Volume, CPC, and competition differ significantly by country. Set the country filter in Ahrefs or Semrush to the target market before pulling any data.

- For US: no geo modifier usually needed — Google.com defaults to US intent.
- For UK: check whether the query is geo-implicit ("tax calculator" already targets UK tax on google.co.uk) or needs an explicit modifier ("uk tax calculator").
- For CA/AU: same check — add the country modifier only where search intent genuinely differs by country.
- Avoid appending a geo modifier to every keyword — it produces thin near-duplicate pages and only helps when the user's intent is explicitly country-specific.

---

## Keyword Type Classification

Before building the site map, classify keywords by type. This drives page structure, content depth requirements, and internal linking logic.

| Type | Examples | Search intent | Best page format |
| --- | --- | --- | --- |
| **Tool keywords** | "hourly rate calculator", "JSON formatter", "prompt generator" | Do — user wants to use something | Interactive tool page |
| **Template keywords** | "invoice template", "email template for job offer", "notion project tracker" | Get — user wants a ready-made asset | Copyable/downloadable template page |
| **Tutorial keywords** | "how to calculate freelance rate", "how to fix CORS error in Next.js" | Learn — user wants step-by-step guidance | How-to guide with numbered steps |
| **Comparison keywords** | "Notion vs Obsidian", "best tools for freelancers", "X alternatives" | Decide — user is choosing between options | Comparison page with criteria and verdict |
| **Question keywords** | "what should I charge as a freelancer?", "is X free?" | Understand — user wants a quick answer | FAQ entry or short answer page with schema |

Every site should have a mix. Tool + template keywords drive the primary asset. Tutorial + question keywords drive the supporting pages. Comparison keywords target users in a decision phase with higher advertiser CPC.

---

## Required Page Clusters

Build the site map in this order, because each layer supports the next:

### 1. Primary tool or resource page

The main interactive experience. This is the page that gives the site its reason to exist. It must:
- Target the highest-intent keyword in the niche (e.g., "freelance hourly rate calculator")
- Produce a real, useful output — not just display information
- Be the most-linked-to page across the rest of the site

### 2. Supporting pages (minimum 10, targeting distinct intents)

Each supporting page must satisfy a different search query. Prefer these content types because they rank well and satisfy both users and Google:

| Type | Example | Why it works |
| --- | --- | --- |
| How-to guide | "how to calculate hourly rate as a freelancer" | Informational intent, ranks for long-tail |
| Formula or explainer | "freelance rate formula explained" | Topical authority, supports the tool |
| Example page | "hourly rate examples by industry" | High relevance, linkable |
| Comparison page | "hourly vs project-based pricing" | Decision intent, longer dwell time |
| Common mistakes | "freelance pricing mistakes to avoid" | Strong long-tail, low competition |
| FAQ cluster | "what should I charge as a freelancer?" | Featured snippet candidate |
| Niche variant | "hourly rate for freelance designers" | Specific audience, low competition |
| Edge case | "how to price rush projects" | Addresses real user need |

Do not create pages that differ only by a swapped location name, skill name, or adjective unless the page has genuinely distinct data or logic behind it.

### 3. FAQ pages or sections

Target "People Also Ask" style questions — 3–5 word queries that appear in Google's PAA box. These are featured snippet opportunities that drive clicks even without a top-3 ranking.

### 4. Homepage

Targets the broadest keyword in the niche. Summarizes the site's value and links to every major cluster. It will rank last — do not count on it for early traffic.

---

## GEO (Generative Engine Optimization) — AI Overview Check

Before finalizing any page, search its primary keyword and check whether Google displays an AI Overview above organic results.

| Signal | Implication | Action |
| --- | --- | --- |
| No AI Overview | Safer for organic CTR | Proceed as planned |
| AI Overview present, partial answer | Content could be cited by AI | Optimize to appear *in* the Overview: clear answer in the first paragraph, FAQ schema, original data cited |
| AI Overview fully resolves the query | Organic CTR may be near zero | Deprioritize or replace with a tool-angle that AI cannot replicate |

**Rule:** if more than half of the supporting page keywords trigger fully-resolving AI Overviews, the cluster is over-weighted on informational content. Shift toward tool-keyword variants (e.g. "hourly rate calculator" beats "how to calculate hourly rate") — interactive tools are not displaceable by AI answers.

Mark each page in `site-map.json` with `"ai_overview": true | false` after checking the live SERP for its primary keyword.

---

## Page Selection Rules

- Each page must satisfy a **distinct search intent** that differs from every other page.
- Each page must have a reason a user would land on it directly from a search — not only via internal navigation.
- Mark pages that require **fresh external data** (pricing, statistics, dates) so the build phase can decide how to handle them.
- If the map cannot reach 10 meaningful supporting pages, return to phase 1 and choose a different niche.

---

## On-Page SEO Requirements

Every page in the site map must include these SEO fields. Define them during planning so the build phase generates them correctly.

| Field | Requirement |
| --- | --- |
| `<title>` | 50–60 characters. Include the primary keyword near the front. Do not truncate. |
| `meta description` | 150–160 characters. Describes the page's unique value. Includes a call to action. |
| `H1` | One per page. Matches or closely mirrors the `<title>`. |
| `H2` / `H3` | Organize the content hierarchy. Each H2 should map to a distinct sub-topic or question. |
| `alt` text | Every image has descriptive alt text. No "image1.jpg" or empty alt on informational images. |
| Canonical URL | Self-referencing canonical on every page. Prevents duplicate content issues. |
| `lang` attribute | Set on the `<html>` element to match the site's primary language. |

---

## Technical SEO Checklist

These apply to the entire site, not individual pages. Deliver all of them as part of phase 2 planning so the build phase implements them by default.

- **`sitemap.xml`** — list every indexable page. Submit to Google Search Console immediately after launch.
- **`robots.txt`** — allow Googlebot. Disallow `/admin`, `/api`, and any non-public paths.
- **Canonical URLs** — consistent URL structure, no trailing slash variation, no duplicate content from query parameters.
- **Internal linking map** — every supporting page links back to the primary tool. The primary tool links to at least 3 supporting guides. No orphan pages.
- **HTTPS** — required. No mixed content.
- **Core Web Vitals** — LCP < 2.5s, CLS < 0.1, INP < 200ms target. Static Next.js or Astro with server-rendered HTML achieves this by default.
- **Mobile-first** — all layouts declared for ≥ 375px viewport.
- **Schema markup** — assign schema types per page template (see below).

---

## Schema Markup Map

Assign schema types during planning. Implement during the build phase.

| Page type | Schema type | Key fields |
| --- | --- | --- |
| Tool / calculator | `SoftwareApplication` or `WebApplication` | `name`, `description`, `applicationCategory`, `offers` |
| How-to guide | `HowTo` | `name`, `step[]` with `name` and `text` |
| FAQ page | `FAQPage` | `mainEntity[]` with `Question` and `acceptedAnswer` |
| Comparison page | `Article` | `headline`, `author`, `datePublished`, `dateModified` |
| Template download | `CreativeWork` | `name`, `description`, `fileFormat` |
| Directory listing | `ItemList` | `itemListElement[]` |
| Homepage | `WebSite` + `SiteNavigationElement` | `name`, `url`, `potentialAction` for site search if available |

---

## Output

Write `outputs/<site-slug>/site-map.json`:

```json
{
  "site_slug": "example-calculator",
  "keyword_strategy": "long-tail first — target difficulty ≤ 30 keywords for supporting pages; homepage targets head term after authority builds",
  "homepage": {
    "path": "/",
    "primary_keyword": "example calculator",
    "title_tag": "Example Calculator — [Benefit] in Seconds",
    "meta_description": "Calculate [X] instantly with our free tool. [Unique value]. Try it now.",
    "intent": "find and use the primary tool",
    "schema": "WebSite"
  },
  "tool_pages": [
    {
      "path": "/calculator",
      "primary_keyword": "example calculator",
      "title_tag": "Example Calculator: [Primary Benefit]",
      "meta_description": "Free [example] calculator. Enter [inputs] and get [output] instantly.",
      "intent": "perform the calculation",
      "inputs": ["input one", "input two"],
      "output": "result description",
      "schema": "WebApplication",
      "difficulty_estimate": "medium",
      "ai_overview": false
    }
  ],
  "supporting_pages": [
    {
      "path": "/guide/example-formula",
      "primary_keyword": "example formula",
      "title_tag": "Example Formula Explained: How to Calculate [X]",
      "meta_description": "Learn the [example] formula with step-by-step examples. Includes edge cases and worked examples.",
      "intent": "understand the formula",
      "content_type": "how-to guide",
      "unique_value": "worked examples and edge cases",
      "schema": "HowTo",
      "difficulty_estimate": "low",
      "ai_overview": false,
      "internal_links_to": ["/calculator"]
    }
  ],
  "faq": [
    {
      "path": "/faq",
      "questions": [
        {
          "question": "common question?",
          "answer_angle": "short direct answer with caveats",
          "paa_candidate": true
        }
      ],
      "schema": "FAQPage"
    }
  ],
  "internal_link_map": {
    "primary_tool_links_to": ["/guide/example-formula"],
    "all_supporting_pages_link_to": ["/calculator"]
  },
  "technical_seo": {
    "sitemap": true,
    "robots_txt": true,
    "canonical_strategy": "self-referencing on every page",
    "schema_types_used": ["WebSite", "WebApplication", "HowTo", "FAQPage"]
  }
}
```

If the map cannot reach 10 meaningful supporting pages, return to phase 1 and choose a better niche.

**Start small principle:** Launch with 15–20 high-quality pages, not 100 thin ones. 15 is the practical safe threshold for AdSense approval — fewer than 10 is almost always insufficient. Google rewards depth and engagement. A site with 15 complete, useful pages that users actually finish reading will rank faster and pass AdSense review more reliably than a site with 200 shallow pages that users bounce from in 8 seconds. Scale page count only after the first pages show real GSC impressions and user engagement.

---

## Completion Gate

Before advancing to phase 3, verify all of the following:

- [ ] `outputs/<site-slug>/site-map.json` is written and complete.
- [ ] The primary tool or resource page is defined with a clear keyword, intent, and schema type.
- [ ] At least 10 supporting pages are defined, each with a **distinct search intent** that differs from every other page.
- [ ] Total planned indexable pages (tool + supporting + FAQ + homepage) reaches **at least 11**, knowing that phase 5 will add 4 trust pages (Privacy Policy, About, Contact, Terms of Use) to reach the 15-page safe threshold. If the niche cannot support 11 content pages here, it cannot safely pass AdSense review — return to phase 1 and choose a different niche.
- [ ] Every page has a defined title tag (50–60 chars), meta description (150–160 chars), H1, schema type, and internal link target.
- [ ] No two pages differ only by a swapped keyword, location name, or adjective without distinct data or logic.
- [ ] All `acts_in_phase: "keywords"` entries from `competitive_brief` in `outputs/niches.json` are accounted for — the missing sub-topics or page angles are either present in the site map or explicitly ruled out with a reason.
- [ ] Internal link map ensures no orphan pages.
- [ ] Every page in `site-map.json` has `ai_overview` set to `true` or `false` — checked against the live SERP for its primary keyword. Pages with `ai_overview: true` have a note on the GEO strategy (optimize for citation, shift to tool-angle, or accept and monitor).
- [ ] If more than half of supporting pages have `ai_overview: true`, the cluster has been rebalanced toward tool-keyword variants to reduce AI displacement risk.
- [ ] `outputs/<site-slug>/site-brief.md` is initialized with: site name, one-sentence purpose, target audience, primary keyword strategy, and a link to this site-map.json. Subsequent phases will append to this file.
