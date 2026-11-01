# Facebook Ads — Fiction Site Traffic Playbook

Load this reference when the user asks about Facebook advertising, ad copy, taglines for promotion, cover image requirements for ads, or campaign setup for fiction sites.

---

## Beginner's Wiki — Facebook Ads Concepts

Everything a first-time advertiser needs to know before running a single dollar. Read this section before anything else.

---

### Facebook Pixel — what it is and why it matters

**What it is:** A small piece of JavaScript code you paste into your website's `<head>`. Once installed, it sends an event to Facebook every time someone visits a page, clicks something, or takes an action (like reading a chapter).

**What it does for you:** Facebook uses this data to:
1. Know who visited your site — so it can find more people just like them (Lookalike Audiences)
2. Track whether someone who saw your ad actually came to your site (attribution)
3. Optimize delivery toward people who are most likely to do what you want (read, click, stay)

**Without a Pixel:** You are flying blind. Facebook shows your ad to whoever its guess says is right. With a Pixel, it learns from real visitor behavior and improves targeting automatically over time.

**Example project configuration:** The Pixel ID is set in `fictions/AGENTS.md` under `facebook_pixel`. All sites in this project share Pixel `YOUR_PIXEL_ID`. The code is injected in `src/app/layout.tsx`. Two events fire automatically: `PageView` on every page load.

**One critical rule:** The Pixel must fire *before* any ad spend. Run at least 500–1,000 organic pageviews through the site first so the Pixel has baseline data. Cold Pixels (zero events) make the algorithm guess randomly.

---

### Campaign Structure — the three-level hierarchy

Every Facebook ad lives inside a three-level hierarchy. Confusing these levels is the most common beginner mistake.

```
Campaign
  └── Ad Set (one or more)
        └── Ad (one or more)
```

| Level | What you control | Analogy |
|---|---|---|
| **Campaign** | Objective (what you want users to do) | The purpose of the whole campaign |
| **Ad Set** | Budget, audience, schedule, placements | Who sees it, when, and how much you spend |
| **Ad** | The image + copy the user actually sees | The creative itself |

**Campaign objective for fiction sites:** Start with **Traffic** objective. Once the Pixel has fired ≥ 500 `ViewContent` events (chapter opens), switch the objective to **Engagement — ViewContent** so Facebook optimizes toward readers who actually open chapters, not just people who click ads. Do not use raw `PageView` as the optimization event — it fires on landing even for instant bounces and teaches the algorithm to find clickers, not readers.

**One Campaign, multiple Ad Sets:** Run 2–3 Ad Sets with different audiences under one Campaign. Facebook will automatically shift budget toward the best-performing one if you use CBO (see below).

---

### Budget Types — CBO vs ABO

**ABO (Ad Set Budget Optimization):** You set a fixed daily budget on each Ad Set individually. If you have 3 Ad Sets at $10/day each, you spend $30/day total regardless of which one performs.

**CBO (Campaign Budget Optimization):** You set one budget at the Campaign level. Facebook automatically shifts spend toward whichever Ad Set is performing best that day.

**For beginners: start with CBO.** It reduces the number of decisions you have to make and lets Facebook's algorithm do the optimization work. Set $20–50/day at the Campaign level and let it run for at least 3–5 days before drawing conclusions.

---

### Audiences — the three types

**Core Audience (Interest Targeting):** You manually pick demographics, interests, and behaviors. Example: Women 25–45 in the US who follow "Kindle Unlimited" or "romance novels." This is where beginners start.

**Custom Audience:** Built from your own data — people who visited your site (via Pixel), people on your email list, or people who watched your video. Requires existing traffic. Not useful until you have at least 1,000 Pixel events.

**Lookalike Audience:** Facebook finds new people who look statistically similar to your Custom Audience. Example: "Find me 1 million people similar to the 500 who read more than 3 chapters on my site." This is the most powerful targeting type — but requires a Custom Audience as its source first.

**Practical order for fiction sites:**
1. Start with Core Audience (interest targeting: romance readers, Kindle, specific sub-genres)
2. After 2–4 weeks and 1,000+ Pixel events: create a Custom Audience of site visitors
3. After Custom Audience has 500+ people: create a 1% Lookalike Audience

---

### Key Metrics — what each number means

| Metric | What it means | What's "good" for fiction |
|---|---|---|
| **CPM** (Cost Per Mille) | Cost per 1,000 impressions — how much to show your ad 1,000 times | $8–20 for the US; lower = your creative is being favored |
| **CTR** (Click-Through Rate) | % of people who saw the ad and clicked | ≥ 1.5% is solid; ≥ 3% is excellent for fiction |
| **CPC** (Cost Per Click) | How much you pay each time someone clicks | < $0.50 is the target for arbitrage to work |
| **Frequency** | Average number of times one person saw your ad | Keep below 3 in the first week; above 5 = audience fatigue |
| **ROAS** | Return on Ad Spend — revenue / ad spend | Fiction arbitrage target: ROAS > 1.5× (AdSense revenue vs. ad cost) |
| **Landing Page Views** | People who actually loaded your site (vs. just clicked) | Should be 70–80% of Link Clicks; lower = slow page load hurting you |

**The metric that matters most for this business model:** CPC. Your profit equation is:

```
Profit per click = (avg pageviews per session × RPM / 1000) − CPC
```

If your RPM is $8 and users average 4 pageviews, you earn $0.032 per pageview, or ~$0.128 per session. You need CPC < $0.12 to break even. Target CPC < $0.08 to profit.

---

### The Learning Phase — why you must not touch the ad for 7 days

When you launch a new Ad Set, Facebook enters a **Learning Phase**. It needs to show your ad to ~50 people who take your desired action before it knows who to target efficiently. During this phase:

- Performance will be unstable and often bad
- CPM and CPC will be higher than normal
- The algorithm is still guessing

**The rule:** Do not change your budget, audience, or ad creative during the Learning Phase. Any significant change resets the learning and you start over. Wait a minimum of 7 days and 50 optimization events before judging performance or making changes.

**"Learning Limited" warning:** If Facebook shows this label, your budget is too low or your audience is too small to collect enough events. Fix: increase the daily budget or broaden the audience.

---

### Ad Account vs. Business Manager vs. Page

These three things are different and beginners constantly confuse them.

| Thing | What it is | You need it for |
|---|---|---|
| **Facebook Page** | Your public-facing Facebook presence | Required to run ads at all |
| **Ad Account** | The billing account where your ads live | Running ads, setting budgets, holding your credit card |
| **Business Manager** | The container that holds your Pages and Ad Account | Managing multiple ad accounts or giving team members access |

**Practical setup:** Create one Business Manager → add your Page → create an Ad Account inside it → add your credit card to the Ad Account. Never run ads directly from a personal profile.

---

### What Gets Your Ad Account Banned

Facebook reviews landing pages, not just creatives. Your account can be restricted or permanently banned for:

| Violation | Example |
|---|---|
| **Misleading claims** | "Doctors hate this trick", fake endorsements, before/after comparisons |
| **Explicit sexual content** | Nipples, genitals, sex acts in the ad image or on the landing page |
| **Cloaking** | Showing Facebook reviewers a different page than what ad clickers see |
| **Missing trust pages** | No Privacy Policy, no Terms of Service, no About page |
| **Prohibited content categories** | Tobacco, weapons, MLM, payday loans — doesn't apply to fiction |

**For fiction sites specifically:** Suggestive covers (bare shoulders, implied intimacy) are fine. Explicit/pornographic imagery is not. The distinction: allure and tension = fine; exposed genitals or sex acts = account ban. See `references/cover-allure-elements.md` §0 for the exact line.

**If your account gets restricted:** Do not create a new account immediately — Facebook links accounts by payment method, IP, and device. First file a review appeal through Meta's support portal. Creating a second account while restricted = permanent ban.

---

### Attribution Window — what the numbers actually count

When Facebook says "this Campaign got 500 clicks," which 500? Attribution windows define how long after seeing your ad Facebook credits you a result.

**Default (recommended for fiction):** 7-day click, 1-day view
- "7-day click": if someone clicked your ad and visited your site within 7 days, it counts
- "1-day view": if someone only saw your ad (no click) and visited within 1 day, it also counts

**Why this matters:** If you compare Facebook's reported clicks to your Google Analytics sessions, they will never match. Facebook counts views; Analytics counts sessions with different cookies. Expect a 20–40% gap. Neither is wrong — they measure different things.

---

### Creative Fatigue — when to refresh your ads

**Creative fatigue** happens when the same people see your ad too many times and stop responding. Signs:
- CTR drops more than 30% from week 1 to week 2
- Frequency above 4 with no new audience expansion
- CPM rising week-over-week with stable targeting

**Fix:** Create 2–3 ad variations (different tagline, same image; or different image, same copy) and run them simultaneously. Facebook will automatically favor the one with better engagement.

**Rule of thumb for fiction:** Refresh creative every 3–4 weeks for ongoing Campaigns. For a new site launch, prepare at least 3 image + copy variants before spending.

---

## What Makes Fiction Ads Work on Facebook

Fiction readers on Facebook are not searching — they are scrolling. The ad has 0.3 seconds to interrupt the feed. Everything below is built around that constraint.

**The two-asset model:** Every Facebook ad for a fiction site needs exactly two things working together:
1. **Tagline** — the copy that hooks in the first 8 words
2. **Cover image** — the visual that stops the scroll before the copy is read

Both must tell the same implied story. A shocking image with bland copy fails. Great copy with a stock-photo cover fails. They amplify each other.

---

## Tagline Standards (Facebook Copy)

> **Full tagline authority lives in `references/tagline-formula.md`.** Load that file for all tagline writing, bulk optimization, formula selection, and the 5-formula playbook (A–E). This section is a pointer only.

### Summary of what's in tagline-formula.md

- **Creative intensity line** — Facebook mainly reviews image/video creatives; text can carry darker implication while avoiding blunt sexual description or false promises
- **8 psychological trigger formulas** (A–H): Forbidden Identity, Curiosity Gap, Reader Manifesto, Power Reversal, Cliffhanger Micro-Copy, Catastrophe → Impossible Consequence, Betrayal → Status Reversal, Intimacy → Identity Collision
- **Formula selection by genre** — which formula wins for billionaire vs. fae vs. fake dating vs. space opera
- **Universal writing rules** — first-8-words test, final-line rule, sentence rhythm, power words
- **Click-driven rewrite method** — 5-step bulk optimization pass
- **Consistency rules** — no repeated openers, one proof object per tagline, story-delivery check
- **Quick publish checklist**

### One-paragraph rule for engineers

The tagline is not a book description. It is the 2–4 short sentences that make a scroller think *"I need to know what happens next"* before they realize they've already tapped. Structure: `[Concrete incident] → [reversal of power or identity] → [irreversible consequence] → [one unresolved detail that forces the click]`. Paid-feed copy normally runs 25–55 words; book-card copy is 8–12. Ends unresolved. First 8 words carry the incident. See tagline-formula.md for everything else.

---

## Cover Image Standards (Facebook Creative)

See `references/story-cover.md` Step 1.7 for the full technical spec. Summary here for ad context:

### Project non-negotiable cover law

All fiction covers in this project are built for Facebook cold traffic and a primary reader audience aged 40–65. The cover must show **exactly three discernible adults**, with **at least one person visibly crying or visibly wronged**, and a **strong emotional contrast** among the three reactions. Gender is unrestricted. The scene must also contain one large, thumbnail-readable proof object and one instantly readable conflict. Use large high-contrast typography, familiar settings, clear faces and hands, and uncluttered framing for older mobile readers. Any crowd, fourth person, neutral group portrait, weak emotion, or tiny proof object is a hard failure.

This law is a design gate, not a guarantee of performance. Validate actual CTR and CPC with controlled Facebook creative tests after launch.

### Five scroll-stop signals

| Signal | What it does |
|---|---|
| **Expression** | One unmistakable emotion on the female lead's face — shocked, longing, torn, furious. Never neutral. |
| **Depth composition** | Female lead large in foreground (65% of frame), male lead smaller in background. Creates "what happened between them?" instantly. |
| **Implied story** | Viewer constructs a 3-word premise in 0.3 seconds: "morning after scandal", "forbidden attraction exposed", "dangerous obsession discovered". |
| **World signal** | One background element identifies the story world without the title: city penthouse = billionaire; candlelit manor = Regency; neon rain = cyberpunk. |
| **Partial reveal** | Bare shoulders + clutched sheet > full exposure. Suggestion generates more CTR than explicit. Better Facebook delivery too. |

### Reference-derived hook-card pattern — luxury-room emotional triangle

Use this as a reusable **story-card composition**, not as a fixed cast, wardrobe, or plot. It is derived from the supplied luxury-penthouse reference: the image works because the viewer can decode a relationship hierarchy, a public emotional collapse, and a third-person complication in one glance. Adapt the roles to the book's actual premise; never add a third person merely to imitate the pattern.

#### 1. Relationship structure

| Layer | Visual role | What the viewer should understand immediately |
|---|---|---|
| Foreground focal | The wronged, pleading, betrayed, or publicly rejected protagonist | She has just lost safety, status, love, or bargaining power |
| Central power figure | The person who controls the decision, relationship, money, contract, or doorway | He or she can change the protagonist's life with one gesture |
| Close ally / rival / witness | A third adult attached to one side or positioned behind the power figure | Someone else wants the central figure, knows the truth, or has just discovered the betrayal |

Preferred high-click variant: make the foreground pair or central relationship unmistakable, then place the third adult behind or just outside that bond with a visibly shocked, jealous, guilty, or horrified reaction. The third person must have a distinct story role, not a decorative face.

#### 2. Physical action and height hierarchy

- Use one standing figure, one lower-positioned or kneeling wronged figure, and one attached or separated witness when the premise supports a status reversal.
- Give every person a concrete action: holding a lapel or wrist for support, reaching toward a document, clutching an envelope, turning away, blocking a doorway, recoiling, or staring at the couple.
- Use eye-lines to establish the triangle: the wronged protagonist looks up or toward the person who can answer her; the power figure looks down or away; the third person looks at the relationship they fear losing.
- Keep the protagonist's agency visible through the proof object, an attempted exit, a refused signature, a hand pulling free, or a decision-ready posture. Do not make helplessness a sensual pose.
- No running, walking, motion blur, symmetrical lineup, equal spacing, neutral expressions, or three people posing for a wealth portrait.

#### 3. Scene and world signal

For billionaire, inheritance, contract, marriage, and high-society betrayal cards, use a **luxury room that contains evidence of the plot**:

```text
lavish Manhattan penthouse salon or private signing room,
floor-to-ceiling windows with a recognizable city skyline at night,
grand crystal chandelier, warm lamps, velvet seating,
polished marble floor or conference table, rich curtains,
brass or gold architectural details, a quiet private bar,
expensive old-money decor with enough ordinary objects to feel lived-in
```

The room must explain why these people have power and why the confrontation is private. Avoid an empty lobby, generic mansion, featureless studio, or luxury background that contributes no plot information.

#### 4. Proof object and story trigger

Place one large, simple proof object in the foreground or between the characters:

| Premise | Proof object |
|---|---|
| Debt / contract bargain | Blank legal folder, open agreement, envelope, fountain pen |
| Marriage betrayal | Ring box, loose ring, unsigned certificate, torn photograph |
| Inheritance / family power | Will folder, sealed letter, key, trust box, share ledger |
| Medical / identity reveal | Medical file, scan envelope, test result folder |
| Public rejection | Suitcase, eviction envelope, broken keepsake, discarded gift |

The object should read by shape and placement at 160px. It must remain blank or abstract inside the raster asset: no generated contract wording, signage, fake logos, author name, title, or pseudo-writing.

#### 5. Warm luxury lighting and palette

Use one coherent warm-light family when the card promises intimacy, wealth, or a private emotional reckoning:

```text
warm golden chandelier light, honey and champagne highlights,
ivory furnishings, polished brass, amber lamps, muted rose or deep red accent,
soft city lights beyond the windows, natural skin texture and readable shadow detail
```

Warm does not mean muddy. Keep faces, hands, proof object, and the relationship geometry readable. Do not stack unrelated blue/orange keys, crush the room into black, or wash the lower third into white. If the user explicitly requests a white, silver, or daylight palette, preserve the same scene hierarchy with that palette instead.

#### 6. Camera, crop, and depth

- Portrait 2:3; use a slightly wide 35mm-equivalent view for three-person conflict so the room, hands, and skyline remain legible.
- Put the emotional focal person or pair in the foreground at roughly 55–70% of frame height; keep the shocked witness or rival smaller but fully readable in the mid-ground.
- Reserve a clean, textured upper band for later title treatment, but do not create a blank veil or add typography to the raster image.
- Use real depth: foreground hands and proof object, mid-ground faces and relationship action, background chandelier/windows/wealth signal. Shallow blur must never erase the third person's reaction.

#### 7. Ready-to-adapt prompt block

```text
Facebook fiction hook-card, photorealistic short-drama freeze-frame, portrait 2:3.
Exactly three mature adults and no other people. [WRONGED PROTAGONIST] occupies the
foreground in a lower or pleading position, visibly [emotion], holding [proof object].
[POWER FIGURE] stands at the center and controls [decision / document / doorway],
looking [down / away / toward the couple] with [emotion]. [THIRD ROLE] is placed
close to one side or separated behind them, visibly [shock / jealousy / guilt / fear],
so the relationship triangle is instantly legible. Every person has a concrete action;
no lineup, no neutral pose, no running, no motion blur.

Set the event in [luxury room or familiar setting] with [world signal]. Use one
coherent [warm golden / daylight / cool overcast] lighting family, readable faces and
hands, a large thumbnail-legible proof object, and clear foreground/mid-ground/background
depth. Image only: no text, letters, signage, logos, watermark, UI, or pseudo-writing.
```

**Card QA sentence:** before approval, summarize the frame in one breath: “She is [doing what] while [power figure] [does what], and [third role] reacts because [unanswered consequence].” If that sentence cannot be written from the pixels alone, the card is a mood board, not a high-click story hook.

### High-performing composition template (billionaire / romance)

Extracted from a proven high-CTR Facebook creative:

```
photorealistic cinematic photograph, luxury penthouse bedroom,
floor-to-ceiling windows with city skyline at dawn, warm golden morning light,

female lead [ethnicity + hair], late 20s, bare shoulders,
clutching white bedsheet to chest, wide eyes looking off-camera with shocked expression,
lips slightly parted, positioned large in foreground filling 65% of frame height,

male lead [ethnicity + hair], late 20s–mid-30s, casual open-collar shirt,
seated on bed behind her, watching her with quiet intensity,
positioned smaller in mid-ground,

white linen bedding, warm amber morning light, soft bokeh depth of field,
cinematic depth of field, romance novel cover composition, photorealistic, 8k
```

### Image + copy pairing rule

The image and tagline must imply the same scene without repeating each other.

| If the image shows | The tagline should imply |
|---|---|
| Woman clutching sheet, man watching from bed | What she just discovered, not the morning itself |
| Two people in charged proximity | What neither of them is saying |
| Woman alone with a document / object | What that object reveals that changes everything |
| Man behind her, she doesn't see him yet | What he already knows that she doesn't |

### Relationship-Pressure Creative Brief (Billionaire / Contract / Divorce)

For contemporary relationship-pressure fiction, the creative must sell the **broken arrangement**, not merely a beautiful or exposed couple. Before generating a cover or feed unit, choose one readable dramatic fact and make the copy imply its consequence:

| Story promise | Image evidence | Copy should withhold |
|---|---|---|
| Contract becoming personal | A signed page, ring box, keycard, or calendar between the leads | Which rule was broken and who will pay for it |
| Marriage in decay | One lead alone with a domestic object or an unkept ritual in frame | The specific absence or betrayal the object proves |
| Divorce / power reversal | The heroine upright at a boardroom, courthouse, family entrance, or doorway; the ex reacts | What evidence or decision made her return possible |
| Second-chance accountability | Visible distance, regret, and an unobstructed exit for the heroine | Whether repair will be accepted, not whether he wants her |

Do not depict coercive restraint, document seizure, trapped-body poses, intoxication, or a powerless heroine as sensual shorthand. If the premise involves control, show the protagonist's agency, exit, proof, or refusal in the frame. The ad's implied scene must be delivered in Chapters 1–2; a contract, ritual breach, or proof object shown in the creative cannot be deferred into vague setup.

---

## Campaign Setup Notes

### Audience targeting angles for romance fiction

Facebook algorithm reads the tagline + image together to find the audience. Writing for the reader, not for the algorithm, produces better auto-targeting.

**Primary audiences that convert for fiction sites:**
- Women 25–45 interested in romance novels, Kindle Unlimited, BookTok, Wattpad
- Lookalike audiences from email list (if available)
- Interest: specific romance sub-genres (paranormal romance, romance, historical romance)

**Do not target broadly by "reading" interest** — the creative (image + tagline) does the targeting. A romance cover with the right tagline will self-select the right audience more precisely than interest layers.

### Ad format recommendations

| Format | When to use |
|---|---|
| Single image | Fastest to test; use the book cover + tagline in the ad copy |
| Carousel | Multiple books from the same site; each card = one book cover + short tagline |
| Video (slideshow) | Animate the cover with Ken Burns effect + tagline appearing word by word — high engagement for romance |

### Copy structure for the full ad unit

```
[Tagline — 25–40 words, follows the rules above]

[CTA line — 1 sentence, tells them exactly what to click]
Example: "Read Chapter 1 free →" or "Start reading now — no sign-up required."

[URL — the book's chapter 1 or the site homepage]
```

Keep the copy above the "See more" fold. The tagline is the entire body — no additional paragraphs.

### High-performing composition template 2 — three-character power hierarchy (romance / mafia / cartel)

Extracted from a proven high-CTR Facebook creative. Outperforms two-character compositions because the viewer must decode three relationships simultaneously — that cognitive load keeps them on the image longer.

```
photorealistic cinematic photograph, underground parking garage,
concrete pillars, luxury black SUV in background,
dramatic low ambient lighting, dark moody atmosphere,

three-character power dynamic composition:

antagonist: [ethnicity + hair] woman, sleek hair pulled back tight,
wearing sharp [color] business suit,
pointing finger down aggressively at woman on the ground,
cold authoritative expression, standing tall, commanding,

protagonist: young woman, long [hair] disheveled,
wearing [color] casual clothing, kneeling on concrete floor,
looking up with frightened defeated expression, visibly distressed,

ally or rival: [ethnicity + hair] woman, wearing [color] fitted outfit,
kneeling beside protagonist in protective stance,
reaching toward her, expression of fierce concern,

cinematic thriller composition, three-way female power hierarchy,
dark mafia-romance atmosphere, photorealistic, 8k
```

**Why three-character compositions outperform on Facebook:**

| Three-character advantage | Why it works |
|---|---|
| Viewer must decode three relationships | Longer dwell time before the scroll continues |
| Physical height hierarchy (standing vs. kneeling) | Power dynamic is legible in under 0.1 seconds |
| Ambiguous third character | "Is she friend or enemy?" forces a click |
| No male characters required | Female power conflict hooks romance audiences directly |
| Accusation gesture (pointing finger) | Single most visceral confrontation signal — instantly raises "what did she do?" |

**3-word implied story:** "betrayal costs everything" / "she paid the price" / "two sides, one woman"

### Story-first threshold freeze-frame

When the ad angle is family rejection, adoption, inheritance, marriage expulsion, public humiliation, or a protagonist being thrown out, use the `Threshold Rejection / Discarded Heir / Family Exile` pattern from `cover-genre-playbook.md`. The winning read is not an attractive estate or a sad portrait; it is a three-person event that can be paraphrased in one breath: **“They threw her out—and now they are afraid of what she will become.”**

- Keep exactly three adults: wronged/crying protagonist in the foreground, two opposing adults at a doorway or threshold.
- Show one abandonment/proof object—suitcase, refuse bag, torn photo, legal folder, sealed letter, ring, or medical file—large enough for a mobile thumbnail.
- Use visible height, distance, pointing, dismissal, or a blocked doorway to show the power relationship without needing exposition.
- Reserve space for one short consequence-led hook. For the 40–65 audience, large yellow or warm-cream type with a dark outline may be used when it remains legible and does not cover faces or the proof object.
- Keep the background ordinary and readable: an estate entrance, family home, courthouse, hospital, or rainy threshold is stronger than an empty luxury set.

---

### What to A/B test first

1. **Tagline variant** (same image, two different taglines) — fastest signal on which hook wins
2. **Opening line** (same tagline structure, different first 8 words) — tests the scroll-stop moment
3. **Image composition** (same book, different scene: morning-after vs. discovery moment vs. confrontation)

Never test image AND copy simultaneously in early rounds — isolate the variable.

---

### Pixel Event Hierarchy

The `ChapterPixel` component (`src/components/ChapterPixel.tsx`) fires these events per chapter page, giving Facebook a full reading-depth funnel:

| Event | Trigger | Type | Optimization value |
|---|---|---|---|
| `ViewContent` | Chapter page mount (chapter opened) | Standard | High — confirms reader entered content |
| `ScrollDepth25` | 25% scroll | Custom | Low — reference only, not an optimization target |
| `ChapterRead50` | 50% scroll | Custom | Highest — half-chapter read, strongest real-reader signal |
| `ScrollDepth75` | 75% scroll | Custom | Reference only |
| `ChapterCompleted` | Chapter-end sentinel enters viewport (IntersectionObserver on `#chapter-content-end`) | Custom | High — chapter finished |
| `TimeOnPage20s` | 20 seconds on chapter page (setTimeout, independent of scroll) | Custom | Medium — early dwell signal |
| `TimeOnPage30` | 30 seconds on page (setTimeout, independent of scroll) | Custom | High — time-dimension engagement; fills the gap for short chapters |

`PageView` fires on every page load including instant bounces — do not use it as an optimization target.

---

### Meta Ads Setup — Phased Campaign Configuration (2026)

> **Note (2026):** Optimization events are selected at the Ad Set level in Ads Manager. Events Manager is only used to verify events and create custom conversions.

Two separate tools, distinct roles:

| Tool | URL | Purpose |
|---|---|---|
| **Events Manager** | eventsmanager.facebook.com/events_manager2 | Verify Pixel events, create custom conversions |
| **Ads Manager** | adsmanager.facebook.com/adsmanager/manage/campaigns | Create campaigns, set optimization objectives |

---

#### Step 1: Events Manager — Verify Events + Create Custom Conversions

**1.1 Verify events are arriving**

1. Go to Events Manager → select your Pixel (or Dataset — Meta is migrating Pixels to "Dataset" view, same thing)
2. Open the **Test Events** tab → enter your site URL
3. Open a chapter page in the browser, confirm these events appear:
   - `PageView` — on page load
   - `ViewContent` — on chapter mount (with `content_type: "chapter"`)
4. Scroll down the chapter page, confirm: `ScrollDepth25` → `ChapterRead50` → `ScrollDepth75` → `ChapterCompleted`
5. Stay on the chapter page without scrolling for ~30s, confirm: `TimeOnPage30`
6. Events firing at expected moments = instrumentation correct

**1.2 Create custom conversions (custom events must be wrapped before they can be used as optimization targets)**

`ChapterRead50` and `ChapterCompleted` are custom events — they cannot be selected directly in an Ad Set. Wrap them as custom conversions first:

1. Events Manager → **Custom conversions** → **Create custom conversion**
2. Configure `ChapterRead50`: Name = "Read Chapter 50%", Data source = your Pixel, Rule: event = `ChapterRead50`, Category = "View Content" → Save
3. Same process for `ChapterCompleted` → Name = "Chapter Completed"
4. Same process for `TimeOnPage30` → Name = "30s On Page" → Category = "View Content"
5. These three custom conversions now appear in the Ads Manager Ad Set optimization event dropdown

---

#### Step 2: Ads Manager — Phased Campaign Creation

> **Key constraint: Meta does not allow changing the objective of an existing Campaign.** Switching from Traffic to Conversions requires creating a new Campaign — you cannot edit the existing one.

**Phase 1: Launch (Ad Set < 50 ViewContent events/week)**

Goal: accumulate Pixel data so the algorithm has enough signal.

1. Ads Manager → **Create**
2. **Campaign objective** → **Traffic**
3. Ad Set settings: **Performance goal** → **Maximize landing page views** (not "Link clicks" or "Impressions")
4. Audience: Core Audience (interest targeting: romance novels, Kindle Unlimited, BookTok)
5. Run until the Ad Set consistently produces ≥ 50 ViewContent events/week (reference: 500 cumulative events; Meta's threshold for exiting Learning Phase)

**Phase 2: Scale (Ad Set ≥ 50 ViewContent/week, reference: 500 cumulative)**

Goal: find people who resemble real readers, not just ad-clickers.

> **Cost trap — do not switch to Sales before Phase 1 is complete.**
> A Sales campaign competes in conversion auction pools (e-commerce, courses) where CPM is structurally higher. Switching too early produces ViewContent costs 5–10× higher than a Traffic campaign:
> - Traffic campaign (Phase 1): ~¥0.31 per landing page view
> - Sales campaign (Phase 2, premature): ~¥2.24 per ViewContent — 7× more expensive
>
> This destroys arbitrage margin. Run Phase 1 until ≥ 50 ViewContent/week is stable. If a Sales campaign is already running with costs this high, pause it immediately and redirect budget to the Traffic campaign.

> Cannot modify the existing Traffic Campaign — create a new Sales Campaign.

1. Ads Manager → **Create**
2. **Campaign objective** → **Sales**
3. **Conversion location** → **Website**
4. Confirm Pixel is linked
5. Ad Set settings: **Performance goal** → **Maximize number of conversions** → **Conversion event** → **View Content (ViewContent)**
   - If ViewContent is greyed out or shows a warning, < 50 events in the last 7 days — keep running Phase 1
6. Reuse Phase 1's audience, budget, and creatives
7. Phase 1 Campaign: pause to concentrate budget on the new campaign's Learning Phase, or run both in parallel for 1–2 weeks to compare ROAS

**Phase 3: Lookalike Audiences (Custom Audience ≥ 500 people)**

1. Ads Manager → **Audiences** → **Create audience** → **Custom Audience**
2. Source: Website → Event: ViewContent → Lookback: Last 180 days
3. After saving, create → **Lookalike Audience**, source = the ViewContent Custom Audience, ratio = 1%
4. Create a new Ad Set with this 1% Lookalike Audience, all other settings unchanged

**Phase 4 (optional): Upgrade to deep-reading events**

When the Ad Set consistently generates ≥ 50 `ChapterRead50` events/week (reference: 500 cumulative), create a new Sales Campaign and set the **Conversion event** to "Read Chapter 50%". This signal produces the highest-quality audience — Lookalike Audience ROAS typically runs 20–40% higher than ViewContent.

---

#### Local Verification (no Meta backend access needed)

Install **Meta Pixel Helper** from the Chrome Web Store (search "Meta Pixel Helper", choose the official Meta extension).

**Verification steps:**

1. Run `pnpm dev` in the site directory, open `http://localhost:3000`
2. Enable Meta Pixel Helper (icon appears in toolbar)
3. Open any chapter page (e.g. `http://localhost:3000/book/{slug}/chapter/1`)
4. Click the extension icon, confirm:
   - `PageView` — fires on load
   - `ViewContent` — fires with `content_type: "chapter"`
5. Scroll down the chapter page, confirm in order:
   - 25% → `ScrollDepth25`
   - 50% → `ChapterRead50`
   - 75% → `ScrollDepth75`
   - Scroll to chapter end (past main prose) → `ChapterCompleted` (IntersectionObserver on `#chapter-content-end` sentinel)

All present = instrumentation correct. Then do a live second-pass in Events Manager using the **Test Events** tab.

**Why not optimize for `PageView`?**

`PageView` fires the instant the page loads, including users who bounce in under 3 seconds. Optimizing for PageView teaches the algorithm to find people who click ads, not people who read fiction. CPM may drop, but ROAS will decline continuously. `ViewContent` confirms the reader opened chapter content. `ChapterRead50` confirms they read half a chapter — Lookalike Audiences built on this signal typically convert 20–40% better.

---

## Quick Reference: Tagline Checklist Before Publishing

See `references/tagline-formula.md` § "Quick checklist before publishing" for the full list. Summary:

- [ ] First 8 words: curiosity gap or emotional punch
- [ ] 25–40 words total
- [ ] One reversal of power or expectation
- [ ] Final line unresolved — no conclusion, no emotional wrap-up
- [ ] Image and tagline imply the same scene without repeating
- [ ] Cover passes the 0.3-second test
