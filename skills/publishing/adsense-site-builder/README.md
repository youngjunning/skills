# AdSense Site Builder

AdSense Site Builder is a single-entry skill built around two core goals: **getting the site through AdSense's first review quickly**, and **earning compounding organic search traffic**.

Both goals are driven by the same build standard: real interactive utility, original content depth, correct technical SEO, and complete trust pages (Privacy Policy must explicitly name Google AdSense and its cookies). Build for real users and both goals follow naturally.

Suited for builders who want to create niche site assets with real search demand and real user value — not thin AI article farms or sites that rely on risky traffic tactics.

## Site Types You Can Build

This skill helps build the following categories of AdSense-ready niche sites:

| Site type | Use case | Examples |
| --- | --- | --- |
| Tool site | Calculators, generators, converters, validators | Salary calculator, JSON formatter, prompt generator |
| Template library | Copyable or downloadable reusable assets | Resume templates, email templates, Notion templates |
| Directory site | Curated lists with filter and comparison fields | AI tools directory, SaaS alternatives, resource lists |
| Comparison hub | Decision support and product/solution comparisons | X vs Y, best alternatives, best tool for a scenario |
| Checklist hub | Process-oriented topics with steps and timelines | Visa checklist, moving checklist, startup launch checklist |
| Tutorial hub | Step-by-step problem solving | Coding errors, Excel formulas, software workflows |
| Hybrid site | Niche covering multiple search intents | One core tool + guides, templates, and comparisons |

## How It Works

The skill runs the site build pipeline in phases:

1. **Validate the niche**: Mine candidates from Reddit, Google Autocomplete, AnswerThePublic, Product Hunt, and similar sources. Verify three demand signals (autocomplete confirmation + engagement on existing results + ≥10 supporting page angles). Filter through AdSense policy safety checks (banned categories, high-risk categories, advertiser demand tier, traffic quality risk).
2. **Plan keywords and SEO foundation**: Long-tail first (target KD ≤ 30 for new sites). Define title tag, meta description, and schema type for every page. Output site-map.json with an internal link map.
3. **Design the page model**: Read the brief → Design Read → token system → design anchor and three dials → anti-AI-default discipline → define non-thin page templates.
4. **Build the site**: Implement all pages and interactive features. Generate sitemap.xml, robots.txt, canonical tags, schema markup, internal link structure, and ad slot placeholders. Embed the AdSense auto-ads script in `<head>`. Meet Core Web Vitals targets (LCP < 2.5s, CLS < 0.1).
5. **Trust pages**: Create About, Contact, Privacy Policy (must name Google AdSense and its cookies), and Terms.
6. **Create the distribution plan (before go-live)**: Product Hunt, directory submissions, targeted community participation (contribute first, share second), YouTube Shorts demos, Pinterest (for template niches). 14-day day-by-day action plan. **Must be ready before launch** so day one executes immediately and the first 2–4 weeks of traffic are fully leveraged.
7. **Go live + GSC setup**: Deploy to production, execute day 1 of the distribution plan, register in GSC, submit sitemap, request indexing for the first batch of pages.
8. **AdSense readiness audit (2–4 weeks post-launch)**: Run after GSC has indexing and impression data. Check content quality, trust page completeness, technical requirements, policy compliance, and traffic quality. Output an audit report with a clear submission recommendation.
9. **GSC growth loop (monthly, post-approval)**: Find three opportunity types from GSC data — quick-win pages ranking 8–20, high-impression/low-CTR title problems, content gaps revealed by real queries. Improve each and document results.

The main workflow is in `SKILL.md`. Phase sub-modules are in `references/`.

```txt
adsense-site-builder/
  SKILL.md
  README.md
  agents/
    openai.yaml
  references/
    niche-opportunity-researcher.md      ← phase 1
    keyword-cluster-planner.md           ← phase 2
    programmatic-seo-architect.md        ← phase 3
    useful-site-builder.md               ← phase 4
    eeat-site-builder.md                 ← phase 5 (archived)
    distribution-launcher.md             ← phase 5 (create before go-live)
    go-live.md                           ← phase 6
    adsense-readiness-auditor.md         ← phase 7 (2–4 weeks post-launch)
    gsc-growth-loop.md                   ← phase 8 (monthly, post-approval)
```

## Installation

Install globally and select your Agent when prompted:

```bash
npx skills add youngjunning/skills --skill adsense-site-builder -g
```

For a project installation, omit `-g`:

```bash
npx skills add youngjunning/skills --skill adsense-site-builder
```

After installation, tell the agent to use `adsense-site-builder` in a new session.

For a shared checkout and local links, use the [repository installation guide](../../../README.md#安装). A Git submodule pins the complete repository, not a GitHub `tree/` URL.

## General Prompt Template

```txt
Use adsense-site-builder to build an AdSense-ready niche website.

Goal:
- Create a useful website with real search demand and real user value.

Market:
- Language: English
- Target country: United States

Requirements:
- Validate the niche before building.
- Choose the best site type for the niche.
- Build the site with a clear homepage, one primary useful experience, and at least 10 supporting pages.
- Add About, Contact, Privacy Policy, Terms, and author/editorial information where appropriate.
- Generate SEO metadata, sitemap, robots.txt, and internal links.
- Run an AdSense readiness audit.
- Create a safe initial traffic plan.

Constraints:
- Do not create a thin AI article site.
- Do not use copied, spun, or keyword-stuffed content.
- Do not recommend traffic packages, traffic exchanges, bots, incentivized clicks, or any invalid traffic tactic.
```

## Batch Site Build Prompt

```txt
Use adsense-site-builder to generate 3 AdSense-ready niche websites.

Market:
- Language: English
- Target country: United States

Process:
1. Generate at least 12 niche candidates.
2. Score them by search intent, utility potential, content depth, competition gap, AdSense safety, and build effort.
3. Select the best 3.
4. For each selected niche, choose the best site pattern: tool site, template library, directory, comparison hub, checklist hub, tutorial hub, or hybrid.
5. Build each site with one primary useful experience and at least 10 supporting pages.
6. Add trust pages.
7. Run technical SEO and AdSense readiness audits.
8. Create a 14-day safe launch plan for each site.

Output:
- Create one folder per site.
- Keep planning and audit files under outputs/<site-slug>/.
- Do not skip the readiness audit.
```

## Tool Site Prompt

```txt
Use adsense-site-builder to build a tool site.

Site type:
- Tool site

Niche:
- [describe the niche, for example: freelance hourly rate calculator]

Requirements:
- Validate search demand and user intent first.
- Build one working interactive tool with clear inputs, useful defaults, result output, examples, and edge-case handling.
- Explain the formula, assumptions, or generation logic.
- Create at least 10 supporting pages covering examples, use cases, common mistakes, comparisons, FAQs, and related calculations.
- Add About, Contact, Privacy Policy, Terms, and disclaimer text if needed.
- Generate SEO metadata, sitemap, robots.txt, and internal links.
- Run the AdSense readiness audit.
- Generate a safe launch plan.

Quality bar:
- The site must still be useful with ads disabled.
- Do not create pages that only exist to target keywords.
```

## Template Library Prompt

```txt
Use adsense-site-builder to build a template library site.

Site type:
- Template library

Niche:
- [describe the niche, for example: job application email templates]

Requirements:
- Validate the niche and identify high-intent template searches.
- Create a homepage, category pages, and individual template pages.
- Each template page must include preview, copyable template text, use case, customization notes, common mistakes, and related templates.
- Create at least 10 supporting pages explaining workflows, examples, and selection guidance.
- Add trust pages and clear ownership/contact information.
- Add SEO metadata, internal links, sitemap, and robots.txt.
- Run an AdSense readiness audit and create a safe launch plan.

Constraints:
- Do not generate generic filler templates.
- Do not claim legal, medical, financial, or professional authority unless verified.
```

## Directory Site Prompt

```txt
Use adsense-site-builder to build a curated directory site.

Site type:
- Directory site

Niche:
- [describe the niche, for example: free AI tools for teachers]

Requirements:
- Validate search demand and directory usefulness.
- Define clear inclusion criteria.
- Create directory listing pages with filters or sortable fields.
- Create item detail pages with consistent fields, use cases, pros, cons, pricing notes, and source links where appropriate.
- Create at least 10 supporting pages such as best-for guides, comparison pages, category explainers, and FAQs.
- Add About, Contact, Privacy Policy, Terms, and editorial criteria.
- Run SEO and AdSense readiness audits.
- Create a safe launch plan.

Constraints:
- Do not invent fake listings.
- Do not scrape or copy product descriptions.
- Clearly mark unknown or unverified information.
```

## Comparison Hub Prompt

```txt
Use adsense-site-builder to build a comparison hub.

Site type:
- Comparison hub

Niche:
- [describe the niche, for example: Notion vs Obsidian alternatives for students]

Requirements:
- Validate search demand around alternatives, comparisons, and best-for queries.
- Define fair comparison criteria.
- Create a homepage, comparison pages, alternative pages, and best-for pages.
- Each comparison page must include criteria, table, pros, cons, best-for recommendation, caveats, and related internal links.
- Create at least 10 supporting pages.
- Add trust pages and editorial methodology.
- Run SEO and AdSense readiness audits.
- Create a safe launch plan.

Constraints:
- Do not claim hands-on testing unless evidence is provided.
- Do not write fake reviews.
- Avoid affiliate-style over-optimization unless the user explicitly asks for affiliate monetization.
```

## Checklist Hub Prompt

```txt
Use adsense-site-builder to build a checklist hub.

Site type:
- Checklist hub

Niche:
- [describe the niche, for example: study abroad application checklist]

Requirements:
- Validate search demand and user scenarios.
- Create checklists organized by phase, deadline, user type, or situation.
- Each checklist page must include action items, timeline, required documents or inputs, common mistakes, and printable or copyable format.
- Create at least 10 supporting pages with guides, examples, FAQs, and edge cases.
- Add trust pages and disclaimers where official verification is needed.
- Run SEO and AdSense readiness audits.
- Create a safe launch plan.

Constraints:
- Do not present unofficial information as official.
- Mark items that users should verify with official sources.
```

## Tutorial Hub Prompt

```txt
Use adsense-site-builder to build a tutorial hub.

Site type:
- Tutorial hub

Niche:
- [describe the niche, for example: Excel formula troubleshooting]

Requirements:
- Validate search demand around errors, how-to queries, and examples.
- Create a homepage, tutorial categories, and step-by-step tutorial pages.
- Each tutorial must include prerequisites, steps, expected result, examples, troubleshooting, common errors, and related guides.
- Create at least 10 supporting pages.
- Add trust pages and clear editorial information.
- Add SEO metadata, internal links, sitemap, and robots.txt.
- Run an AdSense readiness audit and safe launch plan.

Constraints:
- Do not create vague tutorials.
- Every tutorial must solve a concrete user problem.
```

## Hybrid Site Prompt

```txt
Use adsense-site-builder to build a hybrid niche site.

Site type:
- Hybrid site

Niche:
- [describe the niche, for example: moving cost planning]

Primary experience:
- [tool, template library, directory, comparison hub, checklist hub, or tutorial hub]

Requirements:
- Validate the niche and identify multiple search intents.
- Build one primary useful experience.
- Add supporting pages across guides, templates, comparisons, checklists, FAQs, and examples where relevant.
- Create at least 10 supporting pages with distinct search intent.
- Add trust pages.
- Run SEO and AdSense readiness audits.
- Create a safe launch plan.

Quality bar:
- The site must feel like one coherent product, not a random collection of articles.
```

## Existing Site Audit Prompt

```txt
Use adsense-site-builder to audit an existing website for AdSense readiness.

Website/project:
- [URL or local project path]

Audit:
- Check site utility, content depth, originality, navigation, trust pages, mobile usability, technical SEO, indexability, AdSense risk, and traffic quality risk.
- Identify blocking issues before AdSense submission.
- Recommend concrete fixes.
- Create an updated safe launch plan.

Output:
- Write outputs/<site-slug>/adsense-readiness-report.md.
- Use a conservative verdict: ready, needs revision, or not ready.
```

## Safe Traffic Plan Prompt

```txt
Use adsense-site-builder to create a safe initial traffic plan for this niche website.

Site:
- [site name or path]

Requirements:
- Recommend only real user acquisition channels.
- Include organic search, community answers, directories, creator outreach, short educational videos, Pinterest if relevant, and small legitimate paid tests only if appropriate.
- Create a 14-day launch plan.
- Define metrics to watch: organic queries, returning users, tool completions, saves, comments, backlinks, and natural shares.

Do not recommend:
- Traffic packages
- Bot visits
- Autosurf or traffic exchange networks
- Incentivized clicks
- Popunder traffic for AdSense approval
- Any tactic intended to inflate ad impressions or clicks
```

## Notes

This skill does not guarantee AdSense approval. Its goal is to raise site quality, reduce low-value content risk, and avoid unsafe traffic tactics.

Always manually review generated content, legal pages, factual claims, and policy-sensitive topics before publishing.
