# GEO Reference — Generative Engine Optimization for Fiction Sites

Load this reference when a site goes live or when asked about AI search discoverability. It covers what actually moves the needle for fiction reading sites in AI-powered search (ChatGPT, Perplexity, Google AI Overviews, Claude, Copilot), what the evidence base looks like, and what is speculation.

---

## The Honest Starting Point

Fiction reading sites are structurally disadvantaged for AI citation. Entertainment queries trigger Google AI Overviews at under 3% — the lowest rate across all tracked categories (source: Ahrefs 1.46B SERP study; confirmed independently by Semrush and AliceLabs). No fiction reading platform appears in any published AI citation dataset. Wattpad gets 106M monthly visits but zero documented AI citations. Goodreads appears occasionally as a source for *informational queries about books*, not as a reading destination.

**What AI systems do cite:** informational content about books — genre guides, book recommendations, author backgrounds, "books like X" lists, character and trope explanations. The chapter reader pages will not be cited. This is a structural constraint, not an optimization gap.

The GEO opportunity for these sites is narrow but real: build the *metadata layer* (book detail pages, author pages, genre landing pages) to the standards AI engines prefer. That layer can get cited. The fiction prose itself will not.

---

## 1. AI Crawler Taxonomy

Understanding which bot does what determines robots.txt strategy. Training crawlers and retrieval crawlers are entirely separate systems — blocking one does not affect the other.

### Known crawlers by company

| Company | Training Bot | Search/Retrieval Bot | User-Triggered |
|---|---|---|---|
| OpenAI | `GPTBot/1.3` | `OAI-SearchBot/1.3` | `ChatGPT-User/1.0` |
| Anthropic | `ClaudeBot` / `anthropic-ai` | `Claude-SearchBot` | `Claude-User` |
| Perplexity | (dual-use) | `PerplexityBot` | `Perplexity-User` |
| Google | `Google-Extended` (training only) | Standard `Googlebot` | — |
| Apple | `Applebot-Extended` (training only) | `Applebot` | — |
| Meta | `meta-externalagent/1.1` | — | — |
| ByteDance | `Bytespider` | — | — |

**Critical nuance — Google:** `Google-Extended` controls only Gemini training and Vertex AI Grounding. It has zero effect on Google AI Overviews. AI Overviews use the standard Googlebot. Blocking `Google-Extended` while expecting it to suppress AI Overviews is a documented misconception.

**Critical nuance — Perplexity:** Cloudflare's August 2025 report confirmed Perplexity operates undeclared stealth crawlers that rotate user-agents and IPs to bypass robots.txt. `Perplexity-User` is also documented to ignore robots.txt. Blocking PerplexityBot is an incomplete defense.

**Compliance data** (arXiv 2505.21733, 2025): `ClaudeBot` — 100% path-level compliance. `GPTBot` — 100% full-disallow compliance but only 30.5% path-level. `Bytespider` — 0% path-level compliance (treat as uncontrollable).

### Recommended robots.ts for these sites

```ts
// src/app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      // Allow all legitimate crawlers by default
      { userAgent: '*', allow: '/' },

      // Block training crawlers only — does not affect AI search citations
      // (BuzzStream 4M-citation study: 88.2% of blocked sites still get cited)
      { userAgent: 'GPTBot', disallow: '/' },
      { userAgent: 'ClaudeBot', disallow: '/' },
      { userAgent: 'anthropic-ai', disallow: '/' },
      { userAgent: 'Google-Extended', disallow: '/' },
      { userAgent: 'Applebot-Extended', disallow: '/' },
      { userAgent: 'meta-externalagent', disallow: '/' },
      { userAgent: 'Bytespider', disallow: '/' }, // 0% compliance but declare anyway

      // Explicitly allow retrieval bots (these drive actual AI citation)
      { userAgent: 'OAI-SearchBot', allow: '/' },
      { userAgent: 'Claude-SearchBot', allow: '/' },
      { userAgent: 'PerplexityBot', allow: '/' },
    ],
    sitemap: 'https://your-domain.com/sitemap.xml',
  }
}
```

**Why this configuration:** Blocking training crawlers has no measurable effect on AI citation rates (documented across three independent studies totaling 6.4M citations). It does reduce server load — ClaudeBot's crawl-to-referral ratio is approximately 38,000:1. The retrieval bots (`OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`) drive actual real-time citations and must be allowed.

---

## 2. Entity Optimization

### The master variable

LLM entity recall is driven by **pretraining document frequency** more than any other factor. Peer-reviewed research (Kandpal et al., ICML 2023; FACT-Bench 2024) shows 60–94% of cross-model variance in entity recall is explained by how many documents in the training corpus mention that entity. GPT-4 scores ~45% accuracy on well-documented entities vs. ~10% on obscure ones. This gap cannot be closed by any single optimization — interventions below are multiplicative on a small base for unknown authors.

Practical implication: a self-published author with 50 web mentions is architecturally at a disadvantage compared to a traditionally published author with 50,000. No schema markup or page structure compensates for this gap. The interventions that do help are those that *generate more mentions across the web*.

### Wikidata entries (highest-leverage, lowest barrier)

Wikidata is the most actionable entity signal for new/indie fiction brands:
- No editorial notability requirement (unlike Wikipedia)
- Brands and authors can create entries directly (no COI restrictions for factual data)
- Refreshes every two weeks — faster than any LLM training cycle
- Feeds the Wikidata → Google Knowledge Graph → LLM training chain
- Hybrid AI systems (ChatGPT browsing, Perplexity, Google AI Overviews) query Wikidata at inference time for entity disambiguation

**Create Wikidata entries for:** each author pen name, each site brand. Minimum properties: `instance of`, `name`, `occupation`, `genre`, `official website`, `Goodreads author ID`.

### Wikipedia (high value, high barrier)

Wikipedia's influence on AI entity recall is disproportionate because:
1. LLM training pipelines oversample it (2–5% raw, higher with repetition multipliers)
2. It is used as a quality classifier for filtering Common Crawl even when excluded from direct training
3. A Wikipedia article generates downstream citations from news, academic papers, and blogs that independently enter training corpora

**Barrier:** Wikipedia's notability criteria (WP:NOTABILITY) require significant independent coverage in reliable published sources. Most indie fiction authors and new fiction brands will not qualify. Pursue Wikipedia only when genuine editorial notability is met with pre-existing press coverage. Do not create promotional articles — they will be deleted and the attempt logged.

**Hallucination risk without a Wikipedia anchor:** Documented case (Beutler Ink, tabletop RPG property) — when ChatGPT could not find a Wikipedia anchor, it fabricated a fake Kickstarter campaign, invented development dates, and generated non-existent citations. This is the most concrete evidence for why Wikipedia matters for creative properties.

### ISNI registration

Register an ISNI (International Standard Name Identifier) for each author at isni.org. ISNI feeds into VIAF (Virtual International Authority File) → Wikidata → Google Knowledge Graph. Low effort, durable, free. Takes 4–8 weeks to propagate.

### Co-occurrence structure matters

Research (NeurIPS 2024 Spotlight, arXiv 2409.14057) shows that LLMs encode co-occurrence statistics in middle transformer layers but true factual associations in lower layers. Co-occurrence knowledge does not generalize to reasoning beyond simple QA.

**Practical implication:** Writing "Author X, who wrote Book Y, known for Z genre" encodes a **relational triple** in the lower (generalizable) layers — not just proximity co-occurrence. Author bios, book descriptions, and About pages should use explicit relational language: `[Author name] writes [genre] fiction, known for [specific trope], author of [book title] published in [year]`.

---

## 3. Structured Data — What Actually Helps

### The honest evidence picture

The largest controlled experiment (Ahrefs, 1,885 pages, 2025–2026) found adding JSON-LD schema produced:
- Google AI Mode: +2.4% (statistical noise)
- ChatGPT: +2.2% (statistical noise)
- Google AI Overviews: −4.6% (slightly negative, marginally significant)

A separate experiment placed data only in JSON-LD (not in visible body text) and tested across five AI platforms — all five extracted zero information. LLMs tokenize JSON-LD as formatted plain text; they do not semantically parse `@type` declarations. `@type: "FAQPage"` carries no more semantic weight than the words "this is an FAQ page."

**Where schema does have a positive effect:** Google AI Overviews, via an indirect mechanism. Schema improves traditional Google indexing and ranking → higher traditional rank → higher AI Overviews citation probability. The AI model itself is not parsing the schema; the benefit flows through the traditional index.

### Schema to implement (evidence-ranked)

**`Organization` + `sameAs` — implement on every site**

This is the highest-confidence schema for entity disambiguation. The `sameAs` array links site identity to external authority nodes (Wikidata, Crunchbase equivalent, social profiles), enabling the Google Knowledge Graph to resolve the site as a known entity. Without `sameAs`, the value is near-zero.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://velvet.fiction.example/#organization",
  "name": "Velvet Throne",
  "url": "https://velvet.fiction.example",
  "description": "romance, paranormal, and billionaire fiction.",
  "sameAs": [
    "https://www.wikidata.org/wiki/Q[entity-id]",
    "https://www.facebook.com/velvetthrone",
    "https://www.instagram.com/velvetthronereads"
  ]
}
```

**`Person` (author) — implement on every author page, complete version only**

A practitioner study found `Person` schema with only `name` + `jobTitle` (no `sameAs`) reduced citation rates by 18 percentage points vs. no schema — likely signaling low-quality implementation. Implement fully or not at all.

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://velvet.fiction.example/author/celine-voss/#person",
  "name": "Celine Voss",
  "jobTitle": "Romance Author",
  "knowsAbout": ["romance", "Paranormal Romance", "Billionaire Romance"],
  "sameAs": [
    "https://www.goodreads.com/author/show/[id]",
    "https://www.wikidata.org/wiki/Q[id]",
    "https://www.amazon.com/author/[id]"
  ]
}
```

**`Book` — implement on every book detail page**

Provides the `Book → Person → genre` relational triple that helps AI systems map author identity to creative output. All schema data must also appear in visible body text — LLMs extract from text, not from JSON-LD.

```json
{
  "@context": "https://schema.org",
  "@type": "Book",
  "@id": "https://velvet.fiction.example/book/shadow-lord/#book",
  "name": "Shadow Lord",
  "author": {
    "@type": "Person",
    "@id": "https://velvet.fiction.example/author/celine-voss/#person",
    "name": "Celine Voss"
  },
  "genre": ["romance", "Paranormal"],
  "inLanguage": "en",
  "datePublished": "2025-03",
  "description": "A 400-year-old vampire lord claims his fated mate in a world where...",
  "publisher": {
    "@type": "Organization",
    "@id": "https://velvet.fiction.example/#organization"
  }
}
```

Add `aggregateRating` if reader ratings are collected and displayed on the page.

**`FAQPage` — do not implement**

Google deprecated FAQPage rich results on May 7, 2026 (removed from Rich Results Test in June 2026). SE Ranking analysis found pages with FAQPage schema averaged 3.6 ChatGPT citations vs. 4.2 without (negative direction). The widely-cited "3.2x boost from FAQPage schema" has no traceable first-party source — it is citation-laundered marketing copy. Use FAQ content in visible text without the schema markup.

**`BreadcrumbList` — no AI citation evidence**

Useful for traditional SEO rich results. No study has isolated it as an AI citation variable. Keep it for traditional SEO; do not treat it as a GEO signal.

**`WebSite` + `SearchAction` — implement on root layout**

Enables sitelinks search box in traditional results, which is a brand visibility signal. Minimal cost to add.

---

## 4. Content Format Signals

### What AI systems actually cite

The Princeton GEO study (Aggarwal et al., KDD 2024, n=10,000 queries) — the strongest academic baseline — tested content modifications against AI citation rates. Top strategies:

| Strategy | Measured lift | Platform tested |
|---|---|---|
| Add expert quotations with attribution | +27–41% | Bing / Perplexity-style RAG |
| Add specific statistics with attribution | +26–33% | Same |
| Cite authoritative sources inline | +25% average; +115% for rank-5 pages | Same |
| Keyword stuffing | **Worst strategy — negative effect** | All |
| Content padding (adding words without substance) | 0% | All |

From arXiv 2604.25707 (Citation Absorption Framework, 602 prompts, 21,143 citations), content types by citation absorption rate vs. baseline:

| Content type | Citation absorption vs. baseline |
|---|---|
| Statistics / definitions / comparisons | +55–62% |
| Comparison tables | +45% (table extraction rate 81% vs. prose 23%) |
| Q&A format content | −5.74% (counterintuitive — worse than baseline) |
| Narrative / prose | Baseline (lowest) |

### Self-contained sentences are cited; context-dependent ones are not

GhostCite (arXiv 2602.06718) documented that LLMs preferentially cite **atomic facts** — sentences that are semantically self-contained and do not require surrounding context. Sentences using cross-reference language ("as mentioned above," "as discussed earlier") lose citation eligibility because they fail the corroboration check across multiple sources.

For book descriptions, author bios, and genre pages: write in declarative, self-contained statements. "Celine Voss writes romance featuring morally grey vampire heroes and forced-proximity plots" is citable. "As discussed, her work features..." is not.

### Content length — word count is not the driver

Ahrefs analyzed 560,346 AI Overviews: word count correlation with citation rate = 0.04 (near-zero). 53.4% of cited pages are under 1,000 words. The difference between platforms:
- Google AI Overviews: favors ~600–1,500 words
- ChatGPT: longer comprehensive content performs better (2,900+ words)
- Perplexity: first 40–60 words are decisive (real-time RAG retrieval)

More content helps only when it adds more citable units (statistics, definitions, tables) — not when it adds padding.

### Position matters

44.2% of LLM citations come from the first 30% of a page (SparkToro, 2026). Answer-first structure is required: core description in the opening 40–60 words, not after setup paragraphs.

### Freshness weighting

Perplexity weights content published within 30 days at 3.2× the citation rate of older content (Discovered Labs). This makes newly published book detail pages and genre guides more likely to surface in Perplexity results immediately after publication.

---

## 5. E-E-A-T for Fiction Brands

### Realistic scope

Google's Quality Rater Guidelines (updated September 2025) explicitly apply a lower E-E-A-T bar to entertainment content than to YMYL (health/finance) content. Entertainment errors "don't have serious consequences." The standard is **honest intent and transparent authorship**, not subject-matter credentials.

The most important post-2024 shift: AI-generated content floods have made **transparent human authorship** the primary E-E-A-T signal for content sites. A real author name, a real bio photo, verifiable external presence — these differentiate human-created fiction from AI-generated bulk content in evaluator and algorithmic signals.

### Author pages

Every author on the site needs an individual page with:
- Real (pen) name and a genre-specific description
- Author photo consistent with external profiles
- `Person` schema (full implementation as above)
- Links to Goodreads author page, Amazon Author Central
- List of books on the site with publication dates

Danny Sullivan's caveat applies here: "Anyone can claim someone is an expert. That's meaningless." The bio page only works when it links to externally verifiable identity.

### About page and editorial transparency

The site needs an About page explaining:
- What the site is (reading platform, not author website)
- Content selection rationale and editorial tone
- Who is responsible for the content

This is a trust signal for quality raters and — indirectly — for AI systems trained on rater-influenced content.

### External brand mentions are the strongest AI citation signal

Ahrefs analyzed 75,000 brands across platforms and found:
- Brand mentions correlation with AI citation rate: **r = 0.664**
- Traditional backlinks correlation with AI citation rate: **r = 0.218**

Brand mentions (including nofollow links) outperform link equity at 3× the correlation strength. AirOps analysis of 21,311 AI brand mentions found 85% come from third-party pages, not the brand's own domain.

**For fiction sites:** Goodreads listings, BookBub profiles, mentions in romance review blogs (Smart Bitches Trashy Books, Dear Author), and reader discussions on Reddit all contribute to this signal — even though none of these send link equity.

---

## 6. Content Types That Can Get Cited

These are the page types where AI citation is achievable. Rank them by investment priority.

### High potential (target these)

**Genre guide pages** — "What is romance?", "What is romantasy?", "romance vs. paranormal romance explained"
- Match informational query intent (the intent AI Overviews are designed for)
- Can include statistics, definitions, comparison tables
- Internal link target for all book pages sharing a genre
- 1,500–2,500 words, answer-first, table-of-contents structure

**Book list / recommendation pages** — "Best romance books 2025", "Books like Colleen Hoover", "Billionaire romance with enemies-to-lovers"
- Match "recommend me" query patterns that AI engines respond to
- Reddit (46.7% of Perplexity citations) surfaces book list discussions — this content competes for the same query
- Structure as a list with one self-contained description per book

**Author biography pages**
- AI engines cite author background when readers ask "Who is [author name]?"
- Requires external identity anchoring (Goodreads, Amazon, Wikidata) to avoid hallucination

**"Books similar to X" pages**
- Closest to a recommendation engine response
- Use read-alike framing in descriptions: "For readers who loved [comparable title] and enjoy [specific trope]..."

### Low potential (optimize for traditional SEO, not AI citation)

**Book detail pages (synopsis + chapter list)**
- Can appear in AI results if a reader searches the exact book title
- Implement schema, answer-first description, FAQ content in visible text
- Compete against Goodreads, Amazon, publisher sites which have higher entity weight

**Chapter reader pages**
- Will not be cited by AI systems
- Optimize for reader experience and traditional SEO long-tail (story content + keywords)
- Ensure static HTML rendering — most AI crawlers do not execute JavaScript

---

## 7. Internal Linking as Entity Relationship Signals

### What the evidence shows

Topical authority (how comprehensively a site covers a subject area) correlates with AI citation at r=0.41 (Ziptie.dev analysis). This is significantly stronger than domain authority (r²=0.032) or backlink count (r²=0.038). Pages with strong topical authority at rank 6–10 receive 2.3× more AI citations than rank-1 pages with weak topical authority.

Google's Content Warehouse API leak (2024) confirmed `siteFocus` and `siteRadius` signals that measure topic depth and breadth — these are upstream signals for AI Overviews.

### Practical structure for fiction sites

Build a bidirectional pillar-cluster structure around each genre:

```
Genre Landing Page (pillar)
  ├── linked FROM every book in that genre (cluster)
  ├── linked FROM "books like X" recommendation page (cluster)
  ├── linked FROM "what is [genre]" guide page (cluster)
  └── links TO all of the above
```

Each cluster page links back to the pillar. This signals to AI systems which page "owns" the genre topic. 88% of AI Overview responses cite three or more sources — a cluster of 10–15 tightly interlinked pages increases the probability that multiple pages from the same site appear in a single AI answer.

### Anchor text for AI context

AI engines process anchor text as semantic context within the crawled document (not as PageRank signal). Use descriptive anchor text that encodes the relationship: "romance novels featuring vampire heroes" rather than "click here" or even just "vampire romance."

---

## 8. Multilingual Considerations (fuego-eterno)

### Hreflang has near-zero effect on AI engines

GSQI direct testing across ChatGPT, Perplexity, Gemini, Copilot, Claude found:
- ChatGPT: returns English URLs regardless of language preference
- Perplexity: frequently returns wrong-language URLs
- Gemini: requires follow-up prompts to return localized content
- Copilot: only engine that consistently respects language routing (inherits Bing's detection system)
- Claude: rarely returns source URLs at all

Implement hreflang correctly for traditional Google indexing — it still affects organic search rank, which indirectly influences AI citation. But do not expect it to drive AI-engine language routing.

### Bilingual content increases total AI visibility

Weglot study (n=1.3M citations, Google AI Overviews + ChatGPT): sites with both Spanish and English content received 327% more AI visibility on non-native queries than monolingual sites. Bilingual sites averaged 24% more total citations across all queries.

**For fuego-eterno:** Adding English-language meta-content (About page, category descriptions, author bios in both languages) will measurably increase AI citation totals. The Spanish fiction prose itself still won't be cited, but the informational wrapper pages can be.

### Perplexity's language behavior

Perplexity's internal query fan-out runs 43% of sub-queries in English even when the user's original query was in Spanish. English-language content on a Spanish-language site gets retrieved and feeds into Spanish-language answers. This is a documented system behavior, not speculation.

### Platform behavior by engine for Spanish content

| Engine | Spanish handling | Primary citation source | Note |
|---|---|---|---|
| ChatGPT | Strong English/US bias; under-crawls Spanish pages | Wikipedia (47.9%) | English content advantage |
| Perplexity | Real-time crawl; often wrong-language URLs | Reddit (46.7%) | Freshness matters (3.2× for <30 days) |
| Gemini | Best cross-language entity understanding | No single dominant source | Spanish Wikipedia + local TLD authority |
| Copilot | Best multilingual support | Bing index | Only engine where hreflang works |

Add `areaServed` and `knowsLanguage` to the site's `Organization` schema to explicitly signal the geographic and linguistic scope.

---

## 9. Brand Mention Monitoring

### Free tools

**Ahrefs AI Visibility Checker** (ahrefs.com/ai-visibility-checker) — free, no signup, covers 6 engines. Use for one-off snapshots before/after content launches.

**Rankshift** — 30-day free trial, no credit card required, covers 8 engines including Llama. Best option for multi-week monitoring during a launch.

**HubSpot AEO Grader** — free, covers 3 engines, good for page-level analysis.

### What monitoring reveals

All GEO monitoring tools share the same core mechanism: pre-set prompts → query AI engines periodically → parse returns for brand mentions, citation URLs, sentiment → trend report. The limitation: most tools query base LLM APIs without web browsing enabled, capturing parametric model knowledge rather than the RAG-augmented results users actually see. Evertune explicitly distinguishes these; most others do not.

Track these queries for each site:
- "[Site name] romance" / "[Site name] paranormal romance"
- "best [genre] reading sites"
- "[Book title] [Author name]"
- "read [book title] online free"

AI answers are non-deterministic — the same query may return different citations across runs. Tools compensate by sampling multiple runs. Treat trends over 4+ week periods, not individual query results.

---

## 10. What's Proven vs. What's Speculation

### Tier 1 — Peer-reviewed evidence

| Claim | Source |
|---|---|
| Statistics + quotations + source citations improve AI citation +26–41% | Princeton GEO, arXiv 2311.09735, KDD 2024 |
| Self-contained atomic sentences are cited; context-dependent sentences are not | GhostCite, arXiv 2602.06718 |
| Entity recall scales with training-data document frequency | Kandpal et al., arXiv 2211.08411, ICML 2023 |
| FACT-Bench 22pp gap between popular vs. obscure entities | arXiv 2404.16164, 2024 |
| Co-occurrence encodes in different layers than factual associations | NeurIPS 2024, arXiv 2409.14057 |
| Statistics/definitions/comparisons +55–62% citation absorption vs. prose | arXiv 2604.25707 |
| Tables: 81% extraction rate vs. 23% for prose | arXiv 2604.25707 |

### Tier 2 — Large-scale industry studies (data-backed, vendor incentives apply)

| Claim | Source |
|---|---|
| Brand mentions r=0.664, backlinks r=0.218 for AI citation correlation | Ahrefs, 75,000 brands |
| 85% of AI brand citations come from third-party pages | AirOps, 21,311 mentions |
| Entertainment queries <3% AI Overview trigger rate | Ahrefs + Semrush + AliceLabs (3 independent) |
| Blocking GPTBot: 88.2% of sites still get cited | BuzzStream, 4M citations |
| Bilingual sites +327% more AI visibility, +24% total citations | Weglot, 1.3M citations |
| Content freshness 3.2× citation rate boost for <30 days (Perplexity) | Discovered Labs |
| 44.2% of LLM citations from first 30% of page | SparkToro, 2026 |
| JSON-LD schema: near-zero effect on ChatGPT/Perplexity; indirect positive for Google AI Overviews | Ahrefs, 1,885-page RCT |
| Topical authority r=0.41 for AI citation; 2.3× advantage over higher-DA pages | Ziptie.dev |

### Tier 3 — Directional practitioner evidence (treat as "probably true, not proven")

| Claim | Caveat |
|---|---|
| Heading hierarchy (H1→H2→H3) improves AI extraction | Mechanism is sound; specific numbers (2.8x, +63%) come from a single agency study with undisclosed methodology |
| Organization schema with full sameAs: 2.3× Google AI Overview citations | Digital Applied, n=1,000; not peer-reviewed |
| Person schema with name+jobTitle only (no sameAs) reduces citations −18pp | Single practitioner study |
| Wikidata injection +272–348% entity Hit@10 | arXiv preprint, not yet peer-reviewed |
| Pillar-cluster internal linking improves AI topical authority | Directional support from Content Warehouse leak + practitioner consensus; no controlled test |

### Claims to reject (fabricated or debunked)

| Claim | Status |
|---|---|
| "FAQPage schema → 3.2× AI citation boost" | No first-party source exists. Citation-laundered marketing copy. |
| "JSON-LD schema improves AI citations by 44–89%" | No traceable primary source. Commercial vendor fabrication. |
| "Person schema → +40–80% ChatGPT/Claude citations" | Refuted by Ahrefs 1,885-page RCT (+2.2%, statistical noise) |
| "Blocking Google-Extended prevents AI Overviews" | False. AI Overviews use standard Googlebot. |
| "Hreflang guides AI engines to correct language URLs" | False for ChatGPT, Perplexity, Gemini, Claude. Only Copilot respects it. |
| "FAQPage schema" (as a structured data type) | Deprecated by Google May 7, 2026 |

---

## Mainland China Policy

**Rule: geo-block all mainland China IPs.** These sites target EN/ES markets; CN visitors
cannot load any monetization scripts (AdX/AdSense/Facebook Pixel are all blocked in mainland
China). A CN visit generates an ad request without a response — Google and Facebook classify
this pattern as potential Invalid Traffic (IVT). Sustained IVT signals risk account warnings
or bans. Blocking CN traffic at the edge eliminates the IVT surface entirely.

### Vercel Edge Middleware implementation

```ts
// middleware.ts — project root
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(req: NextRequest) {
  const country = req.geo?.country ?? req.headers.get('x-vercel-ip-country')
  if (country === 'CN') {
    return new NextResponse('Not available in your region.', { status: 451 })
  }
  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon).*)'],
}
```

`x-vercel-ip-country` is set by Vercel's edge automatically — no extra configuration needed.
For non-Vercel deployments, use Cloudflare's `CF-IPCountry` header instead.

### Organization schema: exclude CN explicitly

Set `areaServed` on the site's Organization schema to explicit target regions and exclude CN:

```json
{
  "@type": "Organization",
  "areaServed": ["US", "GB", "AU", "CA", "IE", "NZ"]
}
```

This gives Google Knowledge Graph and AI search engines an accurate geographic signal and
avoids CN traffic being treated as an intended audience.

---

## Quick Reference — Priority Actions by Site Type

### All sites (implement at launch)

1. Allow `OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot` in robots.ts
2. Implement `Organization` schema with full `sameAs` on root layout
3. Implement `Book` schema on every book detail page (data must also be in visible text)
4. Implement `Person` schema (full version with `sameAs`) on every author page
5. Create Wikidata entries for site brand and each author pen name
6. Create Goodreads author profiles and book listings
7. About page with editorial transparency

### After launch (content layer)

8. Build one genre guide page per genre (1,500–2,500 words, table-of-contents, comparison tables, answer-first)
9. Build "books like X" recommendation pages for each title
10. Establish bidirectional pillar-cluster internal linking between genre guides and book pages
11. Write book descriptions as self-contained relational triples, not promotional copy
12. Register ISNI for each author at isni.org

### Long-term entity building

13. Seek book review coverage from authoritative genre blogs (earned media = 85% of AI citations)
14. Build authentic Reddit presence in r/romancebooks, r/fantasyromance, r/suggestmeabook (Perplexity cites Reddit at 46.7%)
15. Pursue Wikipedia article only when editorial notability criteria are genuinely met

### For Spanish-language sites (fuego-eterno)

16. Add English-language versions of About, category, and author pages (+24% total AI citations per Weglot data)
17. Add `areaServed` and `knowsLanguage` to Organization schema
18. Build Spanish-Wikipedia entity presence (Gemini cites local-language authority sources for Spanish queries)
19. Implement per-country hreflang (`es-ES`/`es-MX`) for traditional Google indexing; do not expect AI-engine routing benefit

---

## 9. llms.txt

`llms.txt` is a draft standard (Jeremy Howard, fast.ai, 2024) analogous to `robots.txt`. It is a Markdown file served at `/llms.txt` that gives LLMs a structured, human-readable summary of the site — what it is, what content exists, and where to find it. The format was adopted quickly: Perplexity reads it, ChatGPT browsing reads it, Claude's web tool reads it. Cost: one static file, zero maintenance.

### Why it matters for fiction sites

The chapter reader pages will not be cited by AI engines. `llms.txt` lets you surface the *metadata layer* — site identity, book list, genre focus, author bios — in the format AI retrieval systems prefer: clean, unformatted, plain Markdown without nav bars, ads, or DOM noise.

### Format spec

```
# {Site Name}

> {One-sentence description of the site and its genre focus}

## Books

- [{Book Title}]({/book/slug}): {One-sentence synopsis, genre tags}
- ...

## About

{2–3 sentences: who publishes this, what readers will find here}

## Contact

{contact email or /contact page URL}
```

### Implementation (Next.js static export — Route Handler)

Use a Route Handler at `src/app/llms.txt/route.ts`. This is the same pattern as `sitemap.ts` / `robots.ts` — Next.js generates `out/llms.txt` at build time, reading live book data from `@/lib/books`. No manual file, no post-build script, zero maintenance.

```ts
// src/app/llms.txt/route.ts
import { books } from '@/lib/books'

export const dynamic = 'force-static'

const BASE = 'https://velvet.fiction.example'   // replace per site
const SITE_NAME = 'Velvet Throne'
const SITE_DESCRIPTION = 'romance, paranormal, and billionaire fiction for readers who want intensity on every page.'

export function GET() {
  const bookLines = books
    .map(b => {
      // first sentence of description only — keep each entry under 30 words
      const oneLiner = b.description.split(/\.|\n/)[0].trim()
      const tags = b.genres.join(', ')
      return `- [${b.title}](${BASE}/book/${b.slug}/): ${oneLiner}. ${tags}.`
    })
    .join('\n')

  const content = [
    `# ${SITE_NAME}`,
    '',
    `> ${SITE_DESCRIPTION}`,
    '',
    '## Books',
    '',
    bookLines,
    '',
    '## About',
    '',
    `${SITE_NAME} publishes ${books[0]?.genres?.[0] ?? 'romance'} fiction for adult readers. New chapters added weekly.`,
    '',
    '## Contact',
    '',
    `${BASE}/contact/`,
  ].join('\n')

  return new Response(content, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  })
}
```

Update `BASE`, `SITE_NAME`, and `SITE_DESCRIPTION` per site. Everything else derives from `books.ts` automatically.

### Rules

- Keep each book entry under 30 words — AI retrieval systems truncate long entries
- Use the first sentence of `book.description` as the one-liner — not promotional copy, not taglines
- Do not include chapter URLs — AI engines do not cite fiction prose, only metadata
- `llms.txt` is **not** a substitute for `robots.txt` — serve both
- For Spanish sites: write `llms.txt` in Spanish (primary language); add a separate `public/llms-en.txt` (static file is fine for the secondary version) in English to capture English-query AI citations (+24% cross-language citation uplift)
