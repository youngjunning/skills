# Niche Opportunity Researcher

Use this reference during phase 1 to find niches with real search demand, concrete user utility, and a clear path through AdSense policy review.

## The Opportunity Formula

Before looking at any niche, anchor every evaluation to this formula:

**Website opportunity = search demand × low competition × real value you can build × monetizable × sustainable to update and distribute**

All five factors multiply — a zero in any one factor kills the opportunity regardless of how strong the others are. Do not start with "what should I write?" Start with: **which type of person has a stable recurring problem? How do they search for it? Are current results satisfying them? Can you do it better?**

---

## GEO and Target Market

AdSense RPM varies 5–10× across markets. Decide the target market before evaluating any niche — a niche earning $4 RPM in the US may earn $0.40 in a lower-tier market.

### GEO tiers by expected RPM

| Tier | Markets | Expected AdSense RPM |
| --- | --- | --- |
| **High** | US, CA, UK, AU, NZ, IE | $2–8+ |
| **Moderate** | DE, FR, NL, SG, JP, SE, NO, CH | $1–3 |
| **Low** | Most of Asia, Latin America, Eastern Europe, Africa | <$1 |

Default: English, United States. The US has the highest combination of search volume, CPC, and advertiser density.

### What GEO affects in every downstream phase

- **Keywords**: Volume, CPC, and KD all differ by country. Run keyword research in the target market's Google. A US KD of 25 may be a UK KD of 10 for the same query.
- **Content**: Match geo conventions — currency (USD vs GBP), date format (MM/DD vs DD/MM), units (imperial vs metric), legal context (HIPAA vs GDPR), and local colloquialisms.
- **Technical**: Set `<html lang="">` correctly. Use ccTLD (`.co.uk`, `.ca`) or hreflang when targeting a specific country.
- **Traffic quality**: AdSense evaluates geo-match between content and visitors. Geo-mismatched traffic depresses RPM. A US-targeted site with primarily UK visitors earns lower ad fill rates.

Record `geo_rpm_tier` in each niche entry in `niches.json` (see Output schema below). This makes the expected monetization ceiling explicit and feeds the `adsense_safety` score.

---

## Inputs

- Target language and country or market (e.g. `en-us`, `en-gb`, `en-au`)
- Batch size
- Preferred monetization path (usually AdSense)
- Exclusions (user-stated or policy-mandated)

---

## Step 1: Find Candidates

Generate more candidates than you need — at least 3x the final batch size — before scoring any of them.

### Where to search

**Observe recurring questions:**
- Reddit: search `r/[niche] site:reddit.com` for recurring how-to questions, tool requests, and "is there a site that..." posts
- Quora, Stack Overflow, AnswerThePublic, AlsoAsked — look for questions with no great existing answer
- Hacker News "Ask HN" posts — surfaces tool gaps engineers notice

**Find search volume signals:**
- Google autocomplete — type a seed keyword and read the suggestions; each suggestion is a real search pattern
- Google "People also ask" and "Related searches" — adjacent intents worth their own pages
- Google Trends — confirms demand isn't declining; compare candidates on the same chart
- Ahrefs free keyword explorer or Semrush free tier — estimate keyword difficulty and volume

**Find tool and template gaps:**
- Product Hunt — tools with strong upvotes but no SEO presence are a gap signal
- Chrome Web Store and App Store — browser extensions that solve a problem often have no web equivalent
- SERP analysis — search the seed keyword and check whether the current top results are thin articles, outdated tools, or behind paywalls; a gap is a weak incumbent, not just low domain rating

**Mine communities in the niche:**
- Facebook Groups, Discord servers, subreddits — watch what members ask about repeatedly
- Job boards (Indeed, LinkedIn) — job postings that mention a common tool reveal professional demand

### Candidate types to prefer

Prefer niches where a small site can provide concrete, self-contained utility:

- calculators (financial, health, unit conversion, estimation)
- generators (text, templates, codes, plans)
- converters and formatters
- checklist libraries organized by scenario
- template libraries with copyable content
- comparison tables and decision guides
- troubleshooting guides organized by error message or symptom
- directory listings with filtering

Avoid:
- Topics too broad for a small site to own (e.g., "fitness")
- Topics that require proprietary data you cannot produce
- Topics where the useful content is already locked behind free tools with strong brand moats (e.g., "YouTube thumbnail downloader" — saturated, low CPM)
- Topics dependent on scraped third-party listings without a curation layer
- Pure affiliate aggregators where the original content adds no value beyond a thin product roundup and outbound links. Google's AdSense policy states affiliate content must be a minor part of the site unless it adds substantial original value — sites that exist primarily to funnel affiliate clicks are a common rejection trigger.

---

## Step 2: Validate Search Demand

Before scoring, confirm there is real search demand for each candidate. A niche with no search signal is not viable regardless of how useful the site could be.

### Three-signal demand check

All three must pass:

1. **Google autocomplete** — the seed keyword appears as an autocomplete suggestion (not just a longer phrase you invented).
2. **At least one existing result in the top 5** that has clear engagement — comments, backlinks, or a high word count on the topic. This proves the market exists.
3. **Supporting keyword set** — you can name at least 10 supporting page topics, each with its own search intent. A niche with only 1–2 keyword angles cannot support a site. Phase 2 requires a firm minimum of 10 supporting pages; this check ensures the niche can sustain that before any build work begins.

Reject candidates that fail any of these three checks.

### Keyword metrics: five dimensions

For each candidate that passes the three-signal check, assess the keyword space on these five dimensions:

| Dimension | What to measure | Tool |
| --- | --- | --- |
| **Search Volume** | Monthly searches for the primary keyword | Google Keyword Planner (free), Ahrefs, Semrush |
| **Keyword Difficulty (KD)** | Ranking difficulty 0–100 | Ahrefs KD, Semrush KD — for new sites, target ≤ 30 on supporting pages |
| **CPC** | Advertiser cost per click | Google Keyword Planner — higher CPC = higher advertiser demand = higher CPM after AdSense approval |
| **SERP Quality** | How good are the current top 10 results? | Manual search — see signals below |
| **Long-tail Depth** | Can this expand into 20+ page topics? | Autocomplete, PAA, Semrush related keywords |

**Volume guidance:** Too low (<200/mo for the primary keyword) means no traffic ceiling. Too high (>50k/mo for a new site) usually means entrenched competitors. Sweet spot for a new AdSense site: 1k–20k/mo for the primary keyword, with dozens of long-tail variations.

**CPC as a CPM proxy:** AdSense RPM in a niche roughly correlates with CPC in that niche. CPC > $1 suggests real advertiser competition. CPC < $0.20 suggests thin advertiser demand even if approval is straightforward.

### Free tool workflow

Use this sequence — stop when you have enough signal:

1. **Google autocomplete** — type the seed keyword, read suggestions. Each suggestion is a real recurring search.
2. **People Also Ask** — shows question-form long-tail keywords worth their own FAQ pages.
3. **Related Searches** — at the bottom of the SERP, shows adjacent keyword clusters.
4. **Google Keyword Planner** (free with any Google Ads account) — search volume ranges, CPC, related keyword ideas.
5. **Google Trends** — confirm the trend is stable or rising. Compare 2–3 candidates on the same chart to pick the strongest.
6. **Ahrefs free Keyword Explorer or Semrush free tier** — KD score, top pages, and related keywords. Use the free daily queries strategically for final candidate selection.

### SERP quality signals: when to compete

Search the primary keyword. Look at the top 10 results. These signals indicate a gap worth entering:

**Green signals (proceed):**
- Forum threads, Reddit posts, or Quora answers in the top 5 — these rank because nothing better exists
- Content from 2–4 years ago with no recent updates
- Pages with poor UX: walls of text, no interactive element, slow load
- No dedicated tool page — only articles trying to explain something a calculator or generator would handle better
- Thin content: pages under 500 words ranking for a query that deserves depth

**Red signals (avoid or be very selective):**
- Established brands (Wikipedia, government sites, large media) in positions 1–3 with exact-match content
- Multiple well-funded SaaS products with free tools that already solve the problem
- Content from the last 6 months that is high-quality and interactive
- Keyword is so specific that the top result already perfectly satisfies it

### Competitor analysis

For the top 2–3 existing sites in the niche, run this assessment:

| Signal | Tool | What you're looking for |
| --- | --- | --- |
| Estimated traffic and sources | Similarweb (free tier) | Is the site growing? Does it rely on organic search or paid traffic? |
| Top pages by traffic | Ahrefs free / Semrush free | Which pages drive their traffic? Are those pages replicable or improvable? |
| Keyword gaps | Semrush Keyword Gap | Keywords the competitors rank for that you could target with better content |
| Technical quality | PageSpeed Insights | Are their Core Web Vitals poor? A fast, well-structured site can outrank a slow incumbent. |
| Content depth | Manual review | Do their top pages actually answer the user's question, or do they skirt around it? |

Note: third-party traffic estimates are directional, not exact. Use them to understand *which sites are winning* and *why*, not to get precise visitor counts.

### Capture the competitive brief (carry this forward to the build)

The assessment above is wasted if it only feeds a go/no-go decision. Convert it into a **competitive brief** that the build phases consume directly. For each of the top 2–3 incumbents, record the specific weakness you observed and the concrete action that beats it. Every weakness must map to an action — a weakness with no action is just an observation.

Map each weakness to the phase that acts on it. Use exactly one of these `acts_in_phase` tokens — they are a closed set the build phase matches on literally, so do not invent new values or use prose like "Phase 4":

| Weakness type | Beat-it action | `acts_in_phase` |
| --- | --- | --- |
| Thin / shallow top page | Set a higher content-depth target for that page type; cover the sub-questions they skip | `build` |
| Missing sub-topics / keyword gaps | Add the missing supporting-page angles to the cluster | `keywords` |
| No interactive tool, only prose | Choose a tool/template primary asset that does the job better | `page_model` |
| Poor Core Web Vitals / slow | Hold the performance budget so the site is measurably faster | `build` |
| Outdated (2–4 yr old) content | Cover current data, recent changes, and the year explicitly | `build` |
| Paywalled / sign-up-gated | Keep the equivalent value free and immediately usable | `build` |

`acts_in_phase` is always one of `keywords` (acted on in phase 2), `page_model` (phase 3), or `build` (phase 4). Whichever phase it names, phase 4's completion gate is the final backstop that verifies the weakness was actually addressed — so an entry never silently drops even if an earlier phase missed it.

Write the brief into `outputs/niches.json` as `competitive_brief` (schema below). If a niche is selected, this brief is the differentiation baseline the build is measured against — not optional flavor.

---

## Step 3: AdSense Policy Safety Assessment

This is the most important gate. A niche that cannot pass AdSense review is disqualified regardless of traffic potential.

### Explicitly banned by AdSense policy

Do not proceed with any niche in these categories:

| Category | Examples |
| --- | --- |
| Adult / sexually explicit | Pornography, escort listings, explicit personal ads |
| Gambling | Online casinos, poker, sports betting, lottery ticket sales |
| Weapons | Firearm sales, ammunition, tactical weapons, silencers |
| Drugs / controlled substances | Recreational drugs, drug buying guides, paraphernalia |
| Tobacco / vaping | Cigarette sales, e-cigarette promotion |
| Hacking / malware | Cracking tools, exploit kits, account takeover guides |
| Counterfeit goods | Replica products, fake documents, piracy |
| Violent or hateful content | Graphic violence, hate groups, harassment tools |
| Copyright infringement | Pirated software, unlicensed streaming, download sites for copyrighted content |

### High-risk categories (harder approval, lower CPM, higher ongoing scrutiny)

These are not banned, but they require extra care. Google applies additional scrutiny and some advertisers exclude these topics. Build into a safer niche unless the utility angle is clearly informational and non-advisory.

| Category | Risk | Safer angle |
| --- | --- | --- |
| Health / medical (YMYL) | Symptom checkers, treatment advice, diagnosis tools | General wellness calculators, BMI, hydration, sleep — avoid symptom → diagnosis flows |
| Legal | Legal advice, contract generation | Checklist guides ("what documents you need"), not "here is your contract" |
| Financial advice | Investment recommendations, loan structuring | Calculators (mortgage, tax estimate, savings) with clear "consult a professional" disclaimers |
| Cryptocurrency | Trading signals, ICO promotion | Technical explainers, fee calculators — avoid price prediction or investment framing |
| Political / news | Partisan commentary, election content | Avoid entirely unless purely factual (e.g., candidate comparison facts) |
| Dating / relationships | Matchmaking, personal ads | General relationship explainers are fine; matchmaking platforms are not |
| Alcohol | Cocktail recipes are borderline | Recipe-only is generally fine; spirits sales or bar directories are riskier |

### Advertiser safety scoring

Beyond policy compliance, assess how attractive the niche is to advertisers. Low advertiser demand means low CPM even after approval.

High advertiser demand (good CPM):
- B2B software, productivity tools, SaaS
- Finance (mortgages, insurance, personal finance calculators)
- Legal services (information only)
- Education and e-learning
- Home improvement, real estate
- Travel planning
- Career and HR tools

Moderate advertiser demand:
- General consumer tools (unit converters, generators)
- Food and cooking
- Hobbies and crafts
- Pet care (general, not veterinary)
- Parenting tools

Lower advertiser demand (thin CPM):
- Entertainment-only content without a decision or purchase adjacent
- Meme or humor sites
- Ultra-local content with no national advertisers

### Traffic quality risk

Some niches attract fraudulent or low-quality traffic patterns that can trigger AdSense policy violations even if the content is fine.

Flag and avoid:
- Niches where the dominant existing sites use traffic exchanges, bot networks, or incentivized visits — these patterns follow the niche
- Niches where the primary audience is other webmasters (e.g., SEO tool aggregators) — high ad-blind, low click-through
- Niches where the expected visit duration is under 10 seconds — low engagement → policy risk

---

## Step 4: Score Candidates

Score each candidate from 1 to 5 on all six dimensions. Only candidates averaging ≥ 3.5 with no dimension below 2 are worth selecting.

| Field | Meaning |
| --- | --- |
| `search_intent_strength` | Users have a clear, recurring problem and consistent search wording |
| `utility_potential` | The site can solve or transform something, not only summarize |
| `content_depth` | At least 10 supporting page angles, each with distinct intent |
| `competition_gap` | Existing top results are weak, thin, outdated, or behind paywalls |
| `adsense_safety` | Topic is policy-compliant, advertiser-safe, and has no traffic-quality red flags |
| `build_effort` | Lower effort relative to the expected output earns a higher score |

`adsense_safety` is a hard gate: any candidate scoring below 3 here is rejected regardless of other scores.

### GEO (Generative Engine Optimization) vulnerability assessment

Google AI Overviews, Perplexity, and ChatGPT can answer questions directly in the interface, reducing organic click-through rates on affected queries. Assess each niche for AI displacement risk before selecting it.

**Low vulnerability (prefer these):**
- Interactive tools, calculators, converters — AI cannot replicate the interaction; users must visit the site to get their specific result.
- Template libraries — users need the actual copyable asset, not a description of it.
- Directory and comparison hubs with current, verifiable data — AI answers go stale; a maintained directory stays authoritative.
- Niches requiring real computation with user-specific inputs.

**High vulnerability (proceed with caution):**
- Simple factual questions ("what is X", "how does Y work") — AI Overviews fully absorb these.
- Definition pages, glossaries, and explainers without original data or examples.
- FAQ content on generic topics — likely to appear verbatim in AI answers, leaving no reason to click.

**Mitigation (not a reason to reject, but factor in):**
- A high-vulnerability niche is still viable if the primary asset is a tool (low vulnerability) and the supporting content serves topical authority. The tool page earns clicks; the supporting pages build authority and are cited by AI.
- Add `geo_ai_vulnerability` to the niche record: `low | medium | high`.

Record this in `niches.json` (see Output schema).

---

## Output

Write `outputs/niches.json`:

```json
[
  {
    "slug": "example-calculator",
    "title": "Example Calculator",
    "market": "en-us",
    "user_problem": "What the user is trying to solve in one sentence",
    "primary_asset": "calculator | generator | checker | template library | directory | comparison hub | checklist hub | tutorial hub",
    "seed_keywords": ["keyword one", "keyword two"],
    "demand_validation": {
      "autocomplete_confirmed": true,
      "existing_results_engaged": true,
      "supporting_page_count": 12
    },
    "supporting_page_angles": ["angle one", "angle two"],
    "competitive_brief": [
      {
        "competitor": "incumbent-domain.com",
        "rank_position": 1,
        "weakness": "Top page is a 400-word article with no worked examples; data is from 2022",
        "weakness_type": "thin | missing_subtopics | no_tool | poor_cwv | outdated | paywalled",
        "beat_action": "Build a calculator with 3 worked examples and current-year data; target 800+ words of support",
        "acts_in_phase": "build"
      }
    ],
    "geo_rpm_tier": "high | moderate | low",
    "geo_ai_vulnerability": "low | medium | high",
    "adsense_policy_check": {
      "banned_category": false,
      "high_risk_category": false,
      "high_risk_notes": "",
      "advertiser_demand_tier": "high | moderate | low",
      "traffic_quality_risk": "none | low | medium | high"
    },
    "score": {
      "search_intent_strength": 4,
      "utility_potential": 5,
      "content_depth": 4,
      "competition_gap": 3,
      "adsense_safety": 5,
      "build_effort": 4
    },
    "risks": ["risk one"],
    "decision": "select | reject | needs research"
  }
]
```

**`competitive_brief` field note:** other fields above show `a | b | c` to list allowed values, but `acts_in_phase` is matched literally by the phase-4 build gate, so its written value must be a single token — exactly one of `keywords`, `page_model`, or `build` — never the pipe string itself and never prose like `"Phase 4"`. `weakness_type` is descriptive (not dispatched on), so a single value from its list is enough but a near-synonym will not break the gate. When in doubt about which phase acts on a weakness, use `build`: phase 4 is the backstop and will catch it.

### Decision rules

- **select** — passes demand validation, no banned or high-risk category flags, `adsense_safety` ≥ 3, average score ≥ 3.5, no dimension below 2.
- **reject** — banned category, `adsense_safety` < 3, fails demand validation, or average score < 3.0.
- **needs research** — potentially viable but missing data on one critical dimension; mark and note what to verify before building.

Select only candidates with strong utility potential, confirmed search demand, and a clear path through AdSense policy review.

---

## Completion Gate

Before advancing to phase 2, verify all of the following:

- [ ] `outputs/niches.json` is written and valid JSON.
- [ ] At least one niche has `decision: "select"`.
- [ ] Every selected niche: `adsense_safety ≥ 3`, average score ≥ 3.5, no single dimension below 2.
- [ ] Every selected niche has a `competitive_brief` array. If no clear incumbents were found, the array may be empty — but note that the build will have no differentiation baseline and will default to the content-depth standards in phase 4.
- [ ] Every `competitive_brief` entry has `acts_in_phase` set to a single token (`keywords`, `page_model`, or `build`), never a pipe string or prose.
- [ ] No selected niche is in a banned AdSense category.
- [ ] Every `needs research` candidate has a specific note on what must be verified before it can be promoted to `select`. Do not advance a `needs research` candidate to phase 2 without resolving the gap.
- [ ] Demand validation passes all three signals (autocomplete, existing engaged result, at least 10 supporting page angles each with distinct search intent) for every selected niche.
