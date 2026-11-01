# Fiction Niche Researcher

## When to Run This

Run this reference **once per book**, not once per site. A site can have multiple books, each with its own niche research.

**Multi-book sites:** When generating multiple books for the same site, run this independently for each book. Selecting the same genre cluster as another book on the site is acceptable — genre repetition is allowed and expected. Optimize each book for demand independently; do not coordinate genres or try to maximize variety across the site.

Load and run whenever:
- Starting a new book (first book on a new site, or adding a book to an existing site)
- `outputs/{site-slug}/{book-slug}/niche-research.json` does not exist
- The user has NOT already stated the genre, tropes, and story premise explicitly

Skip (read the existing JSON instead) when:
- `outputs/{site-slug}/{book-slug}/niche-research.json` already exists for this book
- The user has stated the genre and premise — document them in `tracking/context.md` directly and proceed

---

Use this reference to pick a genre × trope combination with real reader demand, a differentiated story angle, and a clear path to social traffic and AdSense approval.

## The Opportunity Formula

**Fiction opportunity = reader demand × trope freshness × producibility × monetization safety × distribution fit**

All five factors multiply — a zero in any one factor kills the opportunity. Do not start with "what should I write?" Start with: **which reader has a craving that existing stories aren't fully satisfying? What trope combination gives them that hit? Can you write it well? Will the traffic convert to ad revenue?**

---

## Platform & Language Targeting

Fiction traffic is platform-driven, not search-driven. Pick your distribution channel before evaluating any genre — the same story can succeed on TikTok BookTok and fail on Wattpad because the format expectations differ.

### Platform tiers by expected traffic profile

| Platform | Dominant audience | Content format | Traffic type |
| --- | --- | --- | --- |
| **TikTok BookTok (EN)** | F 18–34, US/UK/AU | Short clips, quotes, trope tags | Viral, spiky, social |
| **Pinterest (EN)** | F 25–44, US | Aesthetic boards, cover art, quote cards | Evergreen, steady |
| **Reddit r/RomanceBooks, r/Fantasy, r/horrorlit, r/mysterybooks, r/scifibooks** | Varies by genre | Community recs, discussion threads | Referral, high intent |
| **Wattpad** | F 13–25, global | Long serialized reads | Organic, loyal |
| **Webnovel / Fizzo** | M+F 18–30, SEA/CN | Fast-paced chapters, power fantasy | In-app only, hard to funnel externally |
| **Facebook Groups (romance, horror, mystery, dark fantasy)** | F 30–50, US | Group posts, share-fests | Referral, high-volume |
| **Taiwan / zh-TW search and social** | F 18–44, Taiwan / Hong Kong / overseas Traditional Chinese readers | SEO book lists, Facebook posts, LINE sharing, Dcard/PTT discussions | Search + social referral |

Default target: **English, US-dominant**. Platform selection depends on genre — romance/drama leans TikTok BookTok + Pinterest + Facebook groups; mystery/thriller leans Reddit + Goodreads; horror/fantasy leans Reddit + Discord community + Pinterest. Pick the platform where your genre's readers already gather; highest ad RPM comes from matching audience intent to advertiser vertical.

For `zh-TW` sites, the default demand path is **SEO book-list landing pages + Facebook/LINE sharing**, not a direct clone of US BookTok behavior. Treat search phrases such as `繁體中文言情小說推薦`, `言情小說線上看`, and `完結言情小說推薦` as the primary organic entry points, then use book pages and chapter cliffhangers to drive session depth.

### What platform choice affects downstream

- **Cover design:** BookTok favors cinematic two-person drama covers. Pinterest favors aesthetic/mood boards. Wattpad favors illustrated character art.
- **Chapter length:** TikTok funnel → short punchy chapters (1 500–2 500 words). Wattpad organic → longer chapters (3 000–5 000 words).
- **Update cadence:** Serialized platforms (Wattpad, Webnovel) reward frequent updates. H5 sites for social traffic can launch complete.
- **Content tone:** BookTok skews toward dramatic, emotionally intense tropes with a strong "hook sentence." Reddit skews toward well-crafted prose and originality signals.

Record `primary_platform` in `niche-research.json`.

---

## Step 1: Find Genre × Trope Candidates

Generate at least 3× more candidates than you need before scoring any.

### Where to find demand signals

**Social platforms (highest signal for fiction):**
- TikTok: search `#[genre/trope]` — check total views and recency of top videos. Views >50M on a genre tag = proven demand. Examples: `#darkromance`, `#mysterythriller`, `#horrorreads`, `#epicfantasy`, `#dystopianfiction`.
- Pinterest: search the genre or trope as a phrase — pin volume and board freshness signal sustained interest.
- Reddit: `r/RomanceBooks`, `r/fantasyromance`, `r/horrorlit`, `r/scifi`, `r/Fantasy`, `r/ifyoulikeblank` — search the trope and read what readers say they can't find enough of. "Does anyone know more books like X?" is a gap signal.
- Facebook groups: search your genre keywords — group size and post frequency indicate audience depth. Examples: "romance books," "horror fiction fans," "fantasy book club."
- Taiwan / Traditional Chinese: search Google Taiwan, Dcard, PTT, Facebook groups, LINE Today-style article surfaces, and bookstore/category language from Readmoo/Kobo/博客來. Look for exact Traditional Chinese phrase patterns, not Simplified Chinese volume. Capture whether readers say `言情小說`, `愛情小說`, `羅曼史`, `古風`, `仙俠`, `豪門`, `重生`, or `宮廷`.

**Fiction platforms:**
- Wattpad trending list by genre — what's rising this week vs. last month.
- Webnovel/GoodNovel hot list — fast-rising titles signal demand.
- Amazon Kindle Unlimited bestsellers by genre — the commercial market lags social trends by 3–6 months; use as confirmation, not discovery.

**Community signals:**
- Reddit AMA threads and "what tropes do you want MORE of" posts.
- GoodReads "Readers Also Enjoyed" chains on a trending title — adjacent tropes.
- BookTok comment sections: "PLEASE write more of this" = unmet demand.

### Candidate types to prefer

Each genre has its own community, demand signals, and trope language. Pick the genre that fits the **target site's tone** (see `AGENTS.md` site table) first, then find the best trope angle within that genre.

| Genre | Hot trope / angle combinations | Primary platform signal |
| --- | --- | --- |
| **Romance — Dark / Mafia** | Enemies to lovers + forced proximity + possessive hero; morally grey captor | `#darkromance` 15B+ TikTok views |
| **Romance — Paranormal** | Alpha werewolf + fated mates + rejected mate arc | `#wolfromance` `#materomance` |
| **Romance — Contemporary** | Cold CEO + contract marriage; rivals to lovers; small-town second chance | `#ceoromance` `#sportsromance` |
| **Romance — Historical / Regency** | Forbidden match across class lines; scandal + reputation at stake; enemies in ballrooms | `#regencyromance` `#historicalromance` Pinterest + Facebook Groups |
| **Mystery — Cosy** | Amateur detective + closed setting + recurring cast of suspects; village crime + outsider protagonist | `#cozymystery` `#cozymysterybooks` Reddit `r/cozynoir` |
| **Mystery — Literary / Gothic Thriller** | Unreliable narrator + hidden identity + psychological unravelling; ancestral estate secret | `#gothicfiction` `#literarythriller` `#psychologicalthriller` |
| **Thriller / Suspense** | Ticking clock + hidden past + wrong-place-wrong-time; witness protection + second life | `#thrillerbooks` `#suspensereads` Reddit `r/thrillermystery` |
| **Horror — Haunted / Folk** | Isolated location + unreliable senses + escalating dread; folk ritual + outsider who breaks the rules | `#horrorreads` `#folkhorror` Reddit `r/horrorlit` |
| **Horror — Psychological / Domestic** | Ordinary setting turned threatening; gaslighting + confined relationship; grief that won't stay buried | `#psychologicalhorror` `#domesticthriller` TikTok + Reddit |
| **Epic / Dark Fantasy** | Chosen burden + political intrigue + magic cost; fae court + mortal bargain; empire in collapse | `#epicfantasy` `#darkfantasy` Reddit `r/Fantasy` |
| **Fantasy — Paranormal / Urban** | Supernatural investigator + hidden world beneath the ordinary; reluctant chosen one in a modern city | `#urbanfantasy` `#paranormalfiction` TikTok + Pinterest |
| **Sci-Fi — Dystopian** | Resistance cell + surveillance state + one person who sees the truth; memory erasure + identity recovery | `#dystopian` `#dystopianfiction` Reddit `r/scifi` |
| **Sci-Fi — Speculative / First Contact** | Humanity's first encounter with the non-human; technology that changes what it means to be alive | `#sciencefiction` `#scifi` Reddit `r/scifi` `r/printSF` |
| **Contemporary Drama** | Secret child / hidden lineage + family reckoning; second-chance reunion after an old wrong; grief and inheritance | `#familydrama` `#emotionalfiction` `#secretbaby` Pinterest + Facebook Groups |
| **Medical Drama** | Deathbed revelation + caregiver relationship; hospital diagnosis that forces family truth; donor / recipient identity | `#medicaldrama` `#hospitalstory` TikTok + Pinterest emotional content |

### US/UK women 25–60 portfolio routing

Use this pool when the user asks for a broad English-language collection for women 25–60. This is an audience portfolio, not a “50+” shelf and not a synonym for romance. Rotate protagonist ages and life pressures across the range instead of making every lead middle-aged or using age as the hook.

| Lane | Reader promise | Primary-genre routing | Required differentiation |
| --- | --- | --- | --- |
| **Restart romantic comedy** | Desire and humor return while the protagonist rebuilds a material part of her life | `genre-romance.md` only when the relationship drives the climax; otherwise contemporary drama with a romance subplot | External goal survives removal of the love interest; no “still desirable” framing |
| **Mature-amateur / silver-sleuth cozy** | A socially observant woman uses prior work, memory, and community access to solve a fair-play puzzle | `genre-mystery.md` | Experience creates access but not infallibility; no graphic violence or sexless-oracle stereotype |
| **Women’s literary reinvention** | A woman confronts the life she postponed and makes a costly structural choice | `genre-drama.md` | Work, money, housing, care, authorship, or family governance changes; replacement romance cannot be the sole reward |
| **Romantasy** | Magic, danger, court struggle, and intimacy increase one another's cost | `genre-fantasy.md` when the quest, war, court, or magical victory condition controls the ending; `genre-romance.md` only when the relationship is the main resolution engine | The heroine changes the political or magical outcome; forbidden love cannot replace a world-level objective |
| **Psychological / domestic suspense** | The protagonist tests her own perception against a home, town, institution, or narrator that cannot be trusted | `genre-mystery.md`; add `genre-small-town-corruption.md` or `genre-stalking-control.md` when that external system is primary | Page-turning uncertainty plus verifiable physical clues; do not reduce suspense to generalized anxiety |
| **Shifter / werewolf / supernatural bond** | Protection, loyalty, bodily transformation, and a claimed or destined bond collide with choice | `genre-romance.md` only when the bond relationship resolves the book; otherwise paranormal fantasy or horror | Protection must have limits and costs; fate creates pressure, never automatic consent or completed intimacy |
| **Billionaire / power-reversal comeback** | A woman excluded from power returns with evidence, ownership, expertise, or public leverage | Workplace, family, inheritance, or revenge drama by default; use `genre-romance.md` only when the couple conflict controls the climax | Her leverage must change the institution; a wealthy partner cannot buy the victory for her |

Portfolio rules:

- A collection may carry all seven lanes when its umbrella promise is female agency, reinvention, curiosity, or power. Keep each book's actual primary genre in metadata, SEO, cover labels, and article targets.
- Do not append `Romance` to cozy mystery, psychological suspense, women’s fiction, or power-reversal drama because a relationship subplot exists.
- Vary the protagonist ages, household structures, work positions, economic constraints, and appetite. “Women 25–60” should widen the available lives, not flatten them into one demographic persona.
- Validate each lane against current A0 demand evidence. Market-size figures, percentages, bestseller claims, and screenshots age quickly and must not be copied into the skill as permanent facts.
- For an initial three-book batch, prefer three different primary engines. A strong default is restart romantic comedy, mature-amateur cozy mystery, and women’s literary reinvention; use the other four lanes for expansion after independent demand validation.

### Taiwan / zh-TW serial-fiction niche pool

Use this pool when the target site language is `zh-TW` or the user asks for Taiwan-facing Traditional Chinese fiction. Choose the primary taxonomy from the climax and victory condition; relationship presence alone does not make a book romance.

| Niche | Hook pattern | SEO phrase examples | Notes |
| --- | --- | --- | --- |
| **Modern contract marriage / wealthy family pressure** | A practical agreement hides an old debt, family secret, or legal trap | `豪門契約婚姻小說`, `現代言情小說推薦`, `契約婚姻言情` | Prefer `豪門` / `契約婚姻`; avoid Simplified-style `霸总文` in UI copy. |
| **Rebirth revenge / palace power** | The heroine dies wronged, returns before the turning point, and uses memory to reverse the court game | `重生復仇宮廷言情小說`, `古風言情小說推薦`, `宮廷權謀言情` | Works well for readers who want agency and payback, not only romance. |
| **Xianxia doomed bond / demon lord vow** | Love interest is the key to sealing or destroying the heroine's fate | `仙俠虐戀小說`, `玄幻言情推薦`, `魔尊言情小說` | Keep terminology readable for Taiwan users; explain the emotional dilemma early. |
| **Family inheritance / hidden identity** | A will, adoption record, or old scandal rewrites the heroine's status | `家族秘密言情小說`, `身世之謎小說`, `現代愛情小說推薦` | Good for broader audiences and lower policy risk. |
| **Small-town second chance / healing romance** | Old lovers meet after a family obligation or local crisis | `療癒系愛情小說`, `小鎮愛情小說`, `第二次愛情小說` | Lower heat, safer for trust-building content and evergreen SEO. |
| **Engagement betrayal / staged compromise** | A relative stages a room, photo, or accusation, but the target preserves provenance and exposes the family transaction | `婚約陷害小說`, `豪門家族鬥爭`, `女性復仇小說` | Primary: domestic thriller / family abuse. Do not eroticize drugging or inability to consent. |
| **Secret child / custody return** | An injured mother returns with a child and refuses to surrender custody or her rebuilt life | `萌寶家庭小說`, `豪門撫養權小說`, `女性成長小說` | Primary: family drama / custody conflict. Reconciliation is optional. |
| **Practical flash marriage / period burden** | A family or housing crisis forces a quick marriage; the underestimated bride has a scarce skill | `閃婚家庭小說`, `年代家庭故事`, `逆境翻身小說` | Primary: period family drama unless the relationship controls the climax. |
| **Traded bride / exchange marriage** | Relatives trade the protagonist for debt, another marriage, land, or supplies; the transaction document becomes evidence | `換親小說`, `家族交易小說`, `逆境翻身故事` | Primary: survival drama / family persecution. Load `genre-taiwan-serial-fiction.md`. |
| **Ancestor awakening / rewritten legend** | A powerful woman wakes in a degraded identity and discovers descendants or history were manipulated | `古風玄幻小說`, `老祖宗甦醒小說`, `身分翻轉小說` | Primary: fantasy / identity revenge. Restore a public record, not only a bond. |

For the first `zh-TW` site launch, three books can intentionally cover three different primary genres. Create a broad `繁體中文小說推薦` article first; create `言情小說` articles only for books whose actual primary engine is romance.

Prefer combinations where:
- At least two tropes or tension angles overlap (readers search the intersection, not just one)
- There is a visible reader community around the combination (subreddit, hashtag, Facebook group)
- There is a clear escalating arc you can structure as chapter-ending hooks

Avoid:
- Single-angle stories with no combination (low differentiation)
- Sub-genres where the top titles have 100M+ Wattpad reads (too saturated to break through organically)
- Stories that require deep proprietary world-building before the first hook — if you can't open in medias res in chapter 1, reconsider scope

### Relationship-Pressure Brief (Contemporary Romance Only)

For billionaire, contract marriage, divorce, second-chance, or marriage-in-crisis candidates, a trope label is not a sufficient demand brief. Record the commercial pressure system that makes the relationship legible before the reader knows the characters.

- **Material collision:** the concrete thing both leads need and cannot obtain alone (home, inheritance, business vote, custody, reputation, family obligation, or deadline).
- **Visible relationship breach:** the opening proof that an old promise, public image, or practical arrangement has failed.
- **Heroine agency:** the resource, expertise, evidence, exit option, or constituency that prevents the story from becoming a rescue fantasy.
- **Irreplaceable emotional contrast:** the domestic ritual, object, place, or obligation that can recur with a changed meaning as the relationship changes.
- **Accountability outcome:** whether the ending is a new courtship, a renegotiated partnership, or permanent separation; reconciliation cannot be assumed from the trope.

Reject a candidate if its only pitch is a rich or possessive man. Select it only when the heroine has a non-romantic objective and the relationship creates a distinct cost to achieving it. Route stories whose climax is institutional exposure, inheritance recovery, or corporate reversal to their actual primary genre; do not label them romance merely because the central antagonist is an ex-husband or CEO.

---

## Step 1.5: Site Tone Gate (mandatory — run BEFORE Step 2)

**Before evaluating any candidate, read the target site's entry in `fictions/AGENTS.md`.** Every candidate must clear this gate or be dropped immediately:

1. **Tone match** — the candidate's core emotion (dark intensity, wholesome/cosy, literary, Spanish heat, etc.) must match the site's declared tone. No exceptions. A "heartwarming small-town" story does not belong on velvet-throne no matter how high its demand score.
2. **No topic overlap with sister sites** — if the parent project has multiple sites on the same root domain, the candidate must not replicate the core topic of another site. Check the site isolation table in `fictions/AGENTS.md`. Reject any candidate that would compete with a sister site on the same domain.
3. **Language match** — the story language must match the site's declared language (`en`, `es`, `en-GB`, `zh-TW`). Do not write English content for a Spanish or Traditional Chinese site, and do not write Simplified Chinese for a `zh-TW` site.

Reject candidates that fail any gate. Do not score them. Do not bring them back.

---

## Step 2: Validate Reader Demand

Before scoring, confirm the genre × trope combo has real reader demand **with recent (last 3 months) trending signals**.

### Four-signal demand check (all four must pass)

1. **Social proof** — at least one TikTok hashtag related to this trope has >10M total views, OR a Reddit thread about this trope has >200 upvotes in the last 6 months.
2. **Existing successful titles** — you can name at least 3 titles (any platform) in this exact trope combo with confirmed readership (Wattpad reads >500K, KU bestseller, or BookTok viral). This proves the market exists and readers return to the sub-genre.
3. **Reader appetite gap** — community evidence (Reddit comments, BookTok comments, Facebook posts) that readers want MORE of this trope. Absence of complaints about oversaturation.
4. **Recency gate (MANDATORY)** — demand must be active in the **last 3 months**. Evidence required: TikTok videos on this trope/genre tag published in the last 3 months with >100K views each, OR a BookTok trend/audio currently circulating, OR a Reddit "what to read" thread from the last 3 months with 50+ upvotes recommending this sub-genre. **Flat or declining genres fail this gate even if they have historically large audiences.** A genre that was huge 18 months ago but hasn't surfaced in recent discussions must be treated as fading demand.

Reject candidates that fail any of these four checks.

### Demand dimensions

| Dimension | What to measure | Where to check |
| --- | --- | --- |
| **Trope tag views** | Total TikTok views on primary trope hashtag | TikTok hashtag search |
| **Recent activity** | TikTok videos posted in last 3 months on this trope hashtag — count and view velocity | TikTok, filter by recency |
| **Community depth** | Active subreddit or Facebook group dedicated to this sub-genre | Reddit, Facebook Groups |
| **Title density** | How many existing titles in this exact combo? Sparse (<20 active titles) = gap; saturated (>500) = harder entry | Wattpad search, Amazon KU filter |
| **Trend direction** | Is demand rising, flat, or falling? Rising required. | Google Trends (trope as phrase, 3-month window), TikTok video recency |
| **Emotional hook strength** | Can the premise be stated in one sentence that triggers a strong emotional reaction? | Gut check + test against 5 similar titles |

### Competitive landscape check

For the top 3–5 existing titles in your target genre × trope combo:

| Signal | What to look for |
| --- | --- |
| Chapter count and update frequency | Serialized? Complete? Cliffhanger density? |
| Reader comments | What are readers praising? What are they asking for that the story doesn't give them? |
| Cover and title conventions | What visual/naming patterns does this sub-genre use? You need to fit in before you can stand out. |
| Prose style | Is the market's standard first-person present or third-person past? How short are the chapters? |
| Weakness to exploit | Thin world-building, weak protagonist agency, slow pacing, abrupt ending, unresolved tension — pick one weakness to beat |

Record one `differentiation_angle` per candidate: the specific thing your story does that the top titles don't. This feeds the story brief in A1.

---

## Step 3: Content Producibility Assessment

A niche you can't write well at speed is not viable regardless of demand.

| Factor | Assessment question |
| --- | --- |
| **Genre fluency** | Have you read (or is Claude trained on) enough titles in this sub-genre to replicate the emotional beats, pacing, and dialogue register? |
| **World complexity** | How much world-building is required before the first chapter? Contemporary = zero. Paranormal = light. Epic fantasy = heavy. |
| **Chapter structure** | Does this genre follow recognizable chapter patterns? Romance: meeting → tension → almost-moment → cliffhanger. Mystery: discovery → investigation → red herring → revelation. Horror: normalcy → unease → escalation → confrontation. Predictable genre structure = easier to produce at volume. |
| **Content intensity** | Romance: steamy / closed-door at peak = AdSense-safe default; explicit = policy risk. Horror: graphic violence → AdSense-safe if not gratuitous. All genres: no explicit sex, no graphic content sexualizing minors. See Step 4 for full policy rules. |
| **Target chapter count** | Can the story be told in 15–20 chapters at 1 500–2 000 words each? If yes, it's producible in one session. If it needs 50+ chapters, plan for serialized delivery. |

Score producibility 1–5. Below 3 = reject unless you have a specific reason to proceed.

---

## Step 4: AdSense Policy Safety Assessment

Fiction sites can be approved for AdSense. Most genre fiction qualifies. A small set of content types does not.

### Disqualified content (hard rejection)

| Content type | Why disqualified |
| --- | --- |
| Sexually explicit / pornographic prose | AdSense explicit content policy — regardless of whether it's labeled "fiction" |
| Content sexualizing minors (even implied) | Hard banned, no exceptions |
| Graphic torture / gore as primary content | Violent content policy |
| Real-person fiction in defamatory or sexual framing | Legal and policy risk |
| Content that glorifies violence against real groups | Hate content policy |

### High-risk (proceed with care)

| Content type | Risk | Safer angle |
| --- | --- | --- |
| romance with non-consent elements | Can trigger content flags | Frame as "morally complex," keep explicit force off-page; focus on emotional complexity |
| Mafia / crime fiction with detailed criminal methods | Can read as instructional | Keep methods vague; focus on emotional/relational stakes |
| Vampire / supernatural with graphic blood scenes | Borderline violence | Keep blood atmospheric, not gratuitous |
| Reverse harem / polyamory | Generally fine for AdSense; some ad networks flag | Proceed; just avoid explicit scenes |

**For romance genres:** Default to steamy but not explicit — sexual tension, implied scenes, fade-to-black or closed-door at the peak intimate moment. Readers understand; AdSense approves.

**For non-romance genres (mystery, horror, fantasy, sci-fi):** Sexual content is not the primary risk. Watch for graphic violence, torture, or body horror as the primary content — atmospheric tension is fine, sustained gore is not.

### Advertiser demand by fiction genre

| Genre | Expected AdSense RPM | Reason |
| --- | --- | --- |
| Romance (all sub-genres) | Moderate–High | Female 18–45 audience; beauty, fashion, relationship product advertisers |
| Paranormal / Fantasy Romance | Moderate | Broad demographic; entertainment product advertisers |
| romance / Mafia | Moderate | Some advertiser exclusions due to content tone; partially offset by high session time |
| Cosy Mystery / Thriller | Moderate | Book, streaming, and home product advertisers |
| Horror | Low–Moderate | Niche audience; some advertiser avoidance of dark content |
| Fantasy / Sci-Fi | Low–Moderate | Narrower audience; entertainment and tech advertiser crossover |
| Literary Fiction | Low | Small audience; low commercial advertiser interest |
| Contemporary Drama / Family Drama | Moderate | Female 25–50; family, home, lifestyle advertisers; high session time from emotionally engaged readers |
| Medical Drama | Low–Moderate | Broad demographic (F 25–55); healthcare, insurance, wellness advertisers; emotionally sticky content |

---

## Step 5: Score Candidates

Score each candidate 1–5 on all five dimensions. Select only candidates averaging ≥ 3.5 with no dimension below 2.

| Dimension | Meaning |
| --- | --- |
| `reader_demand` | Active community, growing hashtag views, confirmed existing readership |
| `trope_freshness` | The specific combination feels distinctive within the sub-genre |
| `producibility` | Can be written well at target chapter count within a single session |
| `differentiation` | Clear one-line angle that beats the top 3 incumbents on at least one axis |
| `adsense_safety` | Content is policy-safe; no explicit material; advertiser-friendly audience |

`adsense_safety` is a hard gate: any candidate scoring below 3 is rejected regardless of other scores.

---

## Book Title & Slug — SEO Strategy

The book title becomes the URL slug (`/book/{slug}/`) and the primary `<title>` tag. A title that is both emotionally compelling and search-friendly outperforms a purely creative title for social traffic and organic discovery.

**Rules:**
- Include at least one genre-signal word in the title or subtitle when possible — readers scan for these in social feeds and search results. Examples: "Dark", "Alpha", "Devil", "Crown", "Cartel", "Veil", "Forbidden".
- The slug is auto-derived from the title (lowercase, hyphens). Avoid titles with special characters, numbers-as-symbols, or non-Latin characters that degrade URL readability.
- Avoid generic titles that are already saturated on Wattpad / Amazon KU (e.g. "His Obsession", "The CEO's Secret") — these attract no differentiated search intent and lose social pattern-matching against existing titles.
- A good title can be read as a micro-teaser: "The Cartel's Bride", "Iron Veil", "Protocol Zero" — each implies a world and a conflict in 2–4 words.
- For contemporary relationship-pressure stories, title the **rupture or contested role**, not the hero's generic status. Prefer a role plus breach, proof, consequence, or changed term; avoid interchangeable possessives such as "His Billionaire Obsession." The title must still distinguish this book if the CEO, wedding, or contract is removed from the thumbnail.

Record `suggested_title` and `suggested_slug` in `niche-research.json`.

For candidates covered by Relationship-Pressure Brief, also record:

```json
"relationship_pressure_brief": {
  "material_collision": "...",
  "visible_breach": "...",
  "heroine_agency": "...",
  "recurring_emotional_anchor": "...",
  "accountability_outcome": "new courtship | renegotiated partnership | permanent separation"
}
```

---

## Output

Write `outputs/{site-slug}/{book-slug}/niche-research.json`.

**Example (romance):**

```json
{
  "site_slug": "velvet-throne",
  "primary_platform": "tiktok-booktok | pinterest | facebook-groups",
  "target_language": "en",
  "target_market": "en-us",
  "selected_genre": "romance",
  "selected_tropes": ["CEO / billionaire", "enemies to lovers", "forced proximity"],
  "demand_validation": {
    "social_signal": "TikTok #darkromance 15B+ views",
    "existing_titles_confirmed": ["Title A", "Title B", "Title C"],
    "community_gap_evidence": "Reddit r/RomanceBooks: 'Why is there no dark CEO romance where the female lead actually has leverage?'"
  },
  "competitive_brief": [
    {
      "title": "His Obsession",
      "platform": "Wattpad",
      "reads": "12M",
      "weakness": "FMC is passive; plot resolves via the hero rescuing her in every arc",
      "beat_action": "FMC holds real power in at least 2 out of 3 major turning points"
    }
  ],
  "differentiation_angle": "FMC is the CEO's legal adversary — she can destroy his company; he can't let her go",
  "producibility": {
    "genre_fluency": 5,
    "world_complexity": "contemporary — zero setup",
    "chapter_structure": "meeting → power struggle → almost-moment → cliffhanger",
    "intensity_level": "steamy / closed-door at explicit moments",
    "target_chapters": 18,
    "words_per_chapter": 1700
  },
  "adsense_policy": {
    "explicit_content": false,
    "high_risk_notes": "romance framing — keep force off-page, focus on tension and emotional stakes",
    "advertiser_demand_tier": "moderate"
  },
  "score": {
    "reader_demand": 5,
    "trope_freshness": 4,
    "producibility": 5,
    "differentiation": 4,
    "adsense_safety": 4
  },
  "decision": "select"
}
```

**Cosy Mystery example:**

```json
{
  "site_slug": "london-pages",
  "primary_platform": "pinterest | reddit | facebook-groups",
  "target_language": "en-GB",
  "target_market": "en-gb",
  "selected_genre": "Cosy Mystery",
  "selected_tropes": ["amateur sleuth", "small village", "found family", "recurring cast"],
  "demand_validation": {
    "social_signal": "TikTok #cozymystery 500M+ views; Reddit r/mysterybooks active community",
    "existing_titles_confirmed": ["The Thursday Murder Club", "Richard Osman village series", "A Flicker in the Dark"],
    "community_gap_evidence": "Reddit r/mysterybooks: 'Need more cosy mysteries with a quirky protagonist who isn't a professional detective'"
  },
  "competitive_brief": [
    {
      "title": "The Thursday Murder Club",
      "platform": "Amazon KU + Reddit",
      "reads": "Bestseller",
      "weakness": "Large ensemble cast is hard to track for new readers",
      "beat_action": "Tight 2-person duo as core sleuths — easier reader attachment"
    }
  ],
  "differentiation_angle": "A retired archivist discovers murder patterns hidden inside historical documents — each crime unlocks a secret from the village's past",
  "producibility": {
    "genre_fluency": 4,
    "world_complexity": "small English village — minimal setup, recurring locations",
    "chapter_structure": "discovery → investigation → red herring → clue reveal → confrontation",
    "intensity_level": "low — no explicit content, minimal on-page violence",
    "target_chapters": 20,
    "words_per_chapter": 1800
  },
  "adsense_policy": {
    "explicit_content": false,
    "high_risk_notes": "None — cosy mystery is the most AdSense-safe fiction genre",
    "advertiser_demand_tier": "moderate"
  },
  "score": {
    "reader_demand": 4,
    "trope_freshness": 4,
    "producibility": 4,
    "differentiation": 5,
    "adsense_safety": 5
  },
  "decision": "select"
}
```

The `decision` field accepts: `"select" | "reject" | "needs research"`

---

## Completion Gate

Before advancing to A1, verify all of the following:

- [ ] `outputs/{site-slug}/{book-slug}/niche-research.json` is written and valid JSON.
- [ ] `decision` is `"select"`.
- [ ] All three demand signals confirmed: social proof, existing titles, reader gap evidence.
- [ ] `differentiation_angle` is one specific sentence — not a vague claim like "better writing."
- [ ] `adsense_safety` score ≥ 3. No explicit content, no minors, no banned categories.
- [ ] Average score ≥ 3.5, no single dimension below 2.
- [ ] `competitive_brief` has at least one entry with a concrete `beat_action` that feeds the A1 story brief.
- [ ] `producibility.target_chapters` and `words_per_chapter` are set — A1 uses these as the writing target.
