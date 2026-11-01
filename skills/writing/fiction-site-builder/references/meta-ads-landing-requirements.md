# Meta Ads Landing Page Requirements (Arbitrage Fiction Sites)

Load this reference during **Phase B4** (trust pages / compliance wiring) when the site will receive paid Facebook/Meta traffic. It supplements `adsense-arbitrage.md` (the profit-model and ad-layout reference) with Meta-specific policy, detection, and account-survival rules.

> **Relationship to `adsense-arbitrage.md`:** that file owns ad layout, session RPM engineering, and AdSense/AdX compliance. This file owns everything that is specific to Meta as the traffic source: account health, content policy distinctions, landing page quality scoring, cloaking rules, domain setup, Pixel/CAPI architecture, and ban causes.

---

## 0. What Meta actually checks

Meta's crawl stack deploys multiple bots against landing page URLs:

| Bot | User-Agent | Purpose |
|---|---|---|
| Link preview | `facebookexternalhit` | Fetches `og:` tags for ad card / link preview |
| Ad review | `Meta-ExternalAds` | Checks landing page matches ad creative; content policy scan |
| AI quality | `Meta-ExternalFetcher` | Quality assessment (may ignore `robots.txt`) |
| AI search | `Meta-WebIndexer` | Separate from ads; lower priority |

**robots.txt rule:** always allow `facebookexternalhit`:

```
User-agent: facebookexternalhit
Allow: /
```

Blocking it breaks link previews and can interfere with ad review. Allow all Meta bots to crawl all public pages — they must see the same content as real users.

---

## 1. Content policy — prohibited vs. restricted

Meta's policy distinguishes **prohibited** (no targeting workaround exists) from **restricted** (allowed only with 18+ audience targeting and approval).

### 1.1 Absolutely prohibited — instant creative rejection or ban

- Exposed genitals or nipples — including when covered only by a digital overlay
- Sex acts or simulated sex acts
- Gestures signifying sex acts
- Pornographic copy: words like `erotic`, `explicit`, `xxx`, `porn` in ad text trigger NLP rejection even without prohibited imagery

### 1.2 Restricted (18+ targeting, may require account-level approval)

- Images focused on groin, buttocks, or female breasts as the primary subject
- People in "sexually suggestive poses, revealing clothing, or stripping"
- "Sexually touching or moving commonly sexualized body parts"

**For romance fiction covers:** suggestive poses, deep cleavage, figure-forward bodies, off-shoulder, proximity / almost-kiss, sheer fabric, muscular torsos — these fall in the **restricted** zone, not the prohibited zone. They are runnable under 18+ targeting without explicit approval in most markets. The line is crossed when the image depicts the body parts listed above as the primary subject in isolation.

**Practical safe words in ad copy:** "steamy", "forbidden", "obsessed", "dark", "possessive", "enemies to lovers" — fine. "Explicit", "erotic", "sensual scenes", "erotica" — trigger NLP rejection.

**Image style note:** illustrated / painted covers pass automated review more easily than photographic covers with the same exposure level. When generating covers for ad creatives, the illustrated art style reduces false-positive rejections from Meta's image classifier.

### 1.3 Arbitrage as a business model

Meta's policy documents do not mention "arbitrage" or "traffic farming" as prohibited practices. The business model itself is not banned. Enforcement is applied via quality metrics and deceptive-content policies, not a blanket arbitrage rule.

---

## 2. Ad copy ↔ landing page consistency

Meta policy (Advertising Standards): *"The products and services promoted in an ad must match those promoted on the landing page."* The ad review process explicitly includes the landing page, not just the creative.

### 2.1 What is required to match

- The **nature of the product**: if the ad implies fiction reading, the landing page must be a fiction reading experience — not a signup wall, not a storefront for a different product, not a thin redirect.
- **Specific claims in ad copy**: if the ad says "read the most addictive romance of 2025", the landing page should be a romance chapter. If the ad quotes a specific line from chapter 1, that line should exist on the page.
- **Tone and content type**: an ad with dark-romance tension should land on content that delivers dark-romance tension, not a cozy contemporary chapter.

### 2.2 What is allowed

| Ad behavior | Verdict |
|---|---|
| Suspense hook ("What secret did she discover?") → lands on chapter 1 | Compliant — normal creative expression |
| Quoting a tense passage → lands on that chapter | Compliant |
| "Read free" in ad copy → chapter is genuinely free to read | Compliant |
| Generic genre hook → lands on any book of that genre | Compliant |

### 2.3 What triggers rejection or ban

| Ad behavior | Verdict |
|---|---|
| Ad implies specific content (e.g., a specific character scenario) → landing page shows different content | Bait-and-switch — violation |
| "Based on true events" for fiction | Misleading — violation |
| Countdown timer or urgency claim that is fake | Deceptive — violation |
| Ad promises a price/freebie → landing page has paywall | Bait-and-switch — violation |
| "Comment 'yes' to get chapter 2" in paid ad copy | Gray area — avoid |

**Landing chapter must match the ad creative's implied promise.** If the ad creative features Book A's cover, land on Book A's chapter 1 — not Book B's. Mismatched OG images (the Facebook link preview showing a different cover than the landing page) also trigger inconsistency flags.

---

## 3. Landing page quality scoring

Meta replaced the single "Relevance Score" with three **Ad Relevance Diagnostics** in 2019:

| Diagnostic | What it measures |
|---|---|
| **Quality Ranking** | Perceived quality vs. ads competing for the same audience |
| **Engagement Rate Ranking** | Expected engagement rate vs. similar ads |
| **Conversion Rate Ranking** | Expected conversion rate vs. ads with the same optimization goal |

Five tiers per diagnostic: `Above Average` → `Average` → `Below Average (Bottom 35%)` → `Below Average (Bottom 20%)` → `Below Average (Bottom 10%)`.

Landing page experience primarily drives **Quality Ranking** and **Conversion Rate Ranking** through post-click signals: bounce rate, dwell time, and conversion completion rate.

### 3.1 What degrades quality ranking — official Meta list

Meta has explicitly named the following as landing page low-quality signals (source: Meta Business News, "Reducing Low-Quality Ads"):

- **Interstitial ads** or pop-ups that appear before the user reaches the content — this is a direct rejection trigger, not just a ranking penalty
- **Disproportionate ad-to-content ratio** — when display ads crowd out the main content; no specific unit count is given, the standard is qualitative
- **Slow page load** — especially on mobile
- **Misleading or sensational headlines** (clickbait on the landing page itself)
- **Ad-to-landing-page mismatch** (covered in §2 above)

**Account-level cascade:** when multiple ads in the same account are flagged for low landing page quality, Meta degrades delivery for all ads in that account, not just the flagged ones. Landing page quality is an account health signal, not just a per-creative signal.

### 3.2 Quantified impact (practitioner data, not Meta-official)

| Quality signal change | Observed CPC/CPM effect |
|---|---|
| Below Average → Average | 20–50% CPM/CPC reduction |
| Bottom 20% quality ranking | CPM can double vs. average |
| +1 second mobile load time | ~7% increase in cost per result |

These numbers are practitioner aggregates, not Meta's published figures. Use as directional guidance.

### 3.3 What the landing page must deliver for good ranking

- Content begins immediately without gating (no login wall, no pre-content interstitial)
- Ad density is not disproportionate — reader reaches prose within the first screenful on mobile; see `adsense-arbitrage.md §3.2` for density caps
- Real, original prose — not thin placeholder or auto-generated filler
- Mobile experience matches desktop experience (no mobile-only pop-ups, no mobile-only redirects)

### 3.4 Typography requirements for paid traffic landing pages

Social traffic audiences have shorter attention spans than organic search readers. Typography must minimise friction in the first 5 seconds.

| Property | Value | Rationale |
|---|---|---|
| Font family | System sans-serif stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, …`) | Zero load latency; native feel; no FOIT risk on mobile networks |
| Font size — mobile | 19px | Below 17px increases bounce; above 21px feels low-density |
| Font size — desktop | 20px | Slightly larger for wider viewport |
| Line height — mobile | 1.8 | Generous enough to track across lines; below 1.7 feels cramped |
| Line height — desktop | 1.85 | |
| Paragraph spacing | `margin-bottom: 1.1em` | Compact beat separation; 1.3em+ is blog-style and hurts scroll depth |
| Max line width | `max-width: 68ch` | Prevents eye-tracking fatigue on wide screens |
| Word break | `word-break: break-word` | Prevents long names/URLs breaking the container on mobile |
| Text rendering | `text-rendering: optimizeLegibility` | Better kerning with system fonts at body size |

These values are validated across 5 live sites (midnight-fable, velvet-throne, wildfire-reads, fuego-eterno, london-pages) for Facebook traffic arbitrage. Do not revert to serif body fonts — `Georgia`/`Times` stacks increase perceived reading friction for social audiences accustomed to sans-serif mobile UI.

---

## 4. Cloaking policy

### 4.1 Official definition

Meta's policy documents do not use the word "cloaking." Two policies cover it:

1. **Fraud, Scams and Deceptive Practices**: ads must not use deceptive or misleading practices
2. **Circumventing Systems**: prohibited to help anyone evade Meta's enforcement mechanisms

The operative definition: **showing Meta's review systems different content than real users see**.

### 4.2 Detection methods (as of 2024–2025)

Meta's detection has evolved past simple User-Agent blocking:

| Detection layer | Method |
|---|---|
| Residential IP crawlers | Meta routes audit traffic through residential proxies — the IP is indistinguishable from a real user; IP-based UA-detection cloaking is largely defeated |
| Mobile device simulation | Real or high-fidelity device fingerprints, not datacenter headers |
| ML classifiers | Pattern-match text, images, URL structure, and account behavior history |
| Behavioral anomaly detection | If post-click signals (bounce, dwell) diverge sharply from what the landing page would predict, Meta flags for human review |

**Consequence:** cloaking triggers the **Circumventing Systems** violation — permanent ban, near-zero appeal success rate.

### 4.3 What is NOT cloaking

| Behavior | Verdict |
|---|---|
| Geo-targeted ads showing different (but all compliant) content per country | Allowed |
| A/B testing two different landing pages (both fully compliant) | Allowed |
| Serving faster cached version to bots | Allowed (same content, different delivery) |
| Robots.txt `Disallow` on admin routes | Allowed (only public ad-destination URLs matter) |
| Using Next.js static export with CDN caching for fast delivery | Allowed |

The test: is there **intentional deception of the review system**? Varying content by audience is fine; hiding violations from Meta's crawler is not.

### 4.4 What this means for this stack

Next.js static export serves identical HTML to all crawlers and users — no server-side rendering branch that could accidentally serve different content to bots. This architecture is inherently cloaking-safe. Do not add any middleware, edge function, or redirect logic that serves different content based on User-Agent or IP range.

---

## 5. Page load speed

### 5.1 Meta's position

Meta confirms it considers page speed in News Feed algorithm ranking ("the person's current network connection and the general speed of the corresponding webpage") but publishes no specific LCP threshold for ads.

### 5.2 Practitioner-aggregated thresholds (directional, not Meta-official)

| Mobile LCP | Signal |
|---|---|
| < 2.5 s | Ideal — no bounce penalty |
| 2.5–3 s | Acceptable — minor conversion loss |
| > 3 s | Bounce rate penalty begins; CPM rises |
| > 5 s | Severe — delivery volume shrinks significantly |

The 3-second threshold aligns with Google's Core Web Vitals "Needs Improvement" boundary (LCP > 2.5 s). Meta's quality scoring likely uses similar benchmarks since ~75% of Facebook traffic is mobile.

### 5.3 What already helps (Next.js static export)

- Static HTML served from CDN edge — removes server render latency
- No database queries on the critical path

### 5.4 Additional requirements

- **`next/image`** for all covers and illustrations: automatic WebP/AVIF conversion, lazy loading, `sizes` attribute for responsive delivery
- **Brotli or Gzip** compression enabled on the hosting platform (Vercel: on by default; manual nginx: configure explicitly)
- **No render-blocking third-party scripts above the fold** — Google Ads GPT and AdSense scripts load with `async`; Meta Pixel loads with `strategy="afterInteractive"` via `next/script`
- **Above-fold ad unit** (`strategy="immediate"`) must use a pre-reserved placeholder to avoid layout shift while the ad loads — see `adsense-arbitrage.md §3.3`
- **Font loading**: use `next/font` with `display: swap`; avoid FOIT on mobile networks

### 5.5 Measurement

Test landing page speed from the perspective of a mid-range Android device on a 4G connection:
- Google PageSpeed Insights (mobile score, LCP column)
- WebPageTest with Moto G4 / LTE throttle profile
- Meta's own "Test Events" in 事件管理工具 shows page load timing

Target: **LCP < 2.5 s on mobile**, CLS < 0.1, FID/INP < 200 ms.

---

## 6. Domain setup and verification

### 6.1 Domain verification (required for iOS 14+ attribution)

Every domain that receives Facebook ad traffic must be verified in Meta Business Suite. Without it:
- Aggregated Event Measurement (AEM) cannot be configured
- The 8-event limit for iOS 14+ is not unlocked
- Learning phase resets repeatedly because conversion events can't be attributed

Steps:
1. Business Suite → Brand Safety → Domains → Add Domain
2. Choose verification method: DNS TXT record (recommended for static export — no HTML file needed), or `<meta>` tag in `<head>`
3. Verification propagates within 24–72 hours
4. Assign the Pixel linked to this domain

### 6.2 Domain age and reputation

Meta does not publish a domain-age signal for ad quality. What matters:

- **Domain history**: if a domain previously hosted violating content or was used in banned ad accounts, that history follows the domain. Freshly registered domains have no negative history — an advantage.
- **Domain/URL structure**: keep landing page URLs clean (`/book/slug/chapter/1`); avoid query strings like `?source=fbads&ref=tracking123` in the advertised URL (use UTM only in the `utm_*` parameters, which are allowed and standard).
- **TLD**: no evidence that `.com` vs. `.net` or other TLDs affects Meta ad review. `.com` has better user trust perception; use it when available.

### 6.3 Account warming timeline (new ad accounts)

A new Meta Business Manager + ad account starts with low spend limits and high CPMs until it establishes a history. Ramp slowly:

| Phase | Activity | Daily budget | Duration |
|---|---|---|---|
| Setup | Create BM, verify domain, add payment method, set up Pixel | — | Wait 48–72 h before first ad |
| Warm-up 1 | Page engagement or video view campaign | $5–10 | 3–5 days |
| Warm-up 2 | Traffic campaign (optimize for Landing Page Views) | $10–25 | 3–5 days |
| Conversion | Traffic/conversion campaign (ViewContent) | $25–50 | Until 50+ events/week |
| Scale | Increase budget 20–50% every 2–3 days | Ongoing |

Never jump daily budget by more than 2× in a single day. A jump from $10 to $500 in one day is a documented account-disable trigger.

---

## 7. Meta Pixel + Conversions API (CAPI) architecture

### 7.1 Pixel baseline and optional CAPI reinforcement

Pixel alone (browser-side) loses 30–60% of conversion events due to:
- iOS 14+ ATT opt-outs (Safari blocks third-party cookies + Intelligent Tracking Prevention)
- Ad blockers (uBlock, Brave, Firefox Enhanced Tracking Protection)
- Browser-level cookie restrictions (Chrome third-party cookie phase-out)

CAPI sends selected events server-side and can recover lost signal, but it is an additive transport, not a replacement for the browser Pixel. Launching with Pixel only is valid. Add CAPI only when the traffic volume, signal-loss evidence, and separate backend justify it.

Do not replace an existing layout bootstrap with a consent-aware client wrapper merely to introduce CAPI. A prior production change did exactly that: fresh visitors who had not clicked the banner never initialized `fbq`, and the shared helper consequently suppressed the full browser funnel. Preserve the existing browser path and consent semantics unless the user explicitly requests a consent migration. The full invariants and acceptance matrix live in `adsense-arbitrage.md §4.1.1`.

### 7.2 Event deduplication (required when running both)

Both Pixel and CAPI fire the same event for the same user action. Without deduplication, Meta counts them twice and trains the model on inflated data.

Deduplication requires:
1. Generate a unique `event_id` per event instance (UUID or hash of `user_id + timestamp + event_name`)
2. Send the **same `event_id`** in the Pixel call and the CAPI call for the same action
3. Meta deduplicates within a ~2-hour window — do not send CAPI events more than 2 hours after the browser event

Common mistakes:
- Browser generates `event_id = uuid_v4()` and CAPI generates a different `event_id` for the same user action → no deduplication, events doubled
- Server timezone mismatch pushes CAPI event outside the 2-hour window → both events counted

### 7.3 Events to implement (fiction reading arbitrage)

| Event | When to fire | AEM Priority | Notes |
|---|---|---|---|
| `PageView` | Every page load (auto via Pixel init) | 4 — lowest | Low intent; includes 3-second bounces. Good for cold-start data volume only. |
| `ViewContent` | Chapter page mount — reader enters chapter content | **3 — switch campaign optimization to this once ≥ 500 events** | Standard event, no custom conversion needed. Fire via `ChapterPixel` component on mount. |
| `ScrollDepth25` (custom) | 25% scroll | Funnel analysis only — do not add to AEM | Measures ch1 hook retention. Weak intent signal; not recommended as optimization target. |
| `ChapterRead50` (custom) | 50% scroll | **2 — strong optimization target** | Genuinely interested reader. Requires custom conversion in 事件管理工具 before AEM/campaign use. |
| `ScrollDepth75` (custom) | 75% scroll | Funnel analysis only — do not add to AEM | Mid-to-late retention diagnostic. Useful for content quality analysis; not for AEM. |
| `ChapterCompleted` (custom) | **90% scroll** (not 100% — footer/ads/recommendations below fold make 100% unreachable) | **1 — highest; best Lookalike seed** | Strongest intent signal. Train delivery toward deep readers. Requires custom conversion in 事件管理工具. |
| `NextChapter` (custom) | Reader navigates to next chapter | High | Clearest engaged-session signal; use for ROAS attribution if implemented. |

**Recommendation:** optimize campaigns toward `ViewContent` or `ChapterRead50`, not raw `PageView`. AEM event priority: `ChapterCompleted(1) > ChapterRead50(2) > ViewContent(3) > PageView(4)`.

**Implementation:** all scroll events live in `src/components/ChapterPixel.tsx` — a client component that fires `ViewContent` on mount and uses a single passive scroll listener with `useRef` guards to fire each depth event exactly once per page load.

Reading events have no monetary value by default. Do not send arbitrary placeholder `value` / `currency` parameters; they distort value and ROAS reporting. When the business intentionally values a chapter open by expected ad revenue, set `value` to measured chapter Page RPM / 1000 and use the site's actual ISO 4217 currency. A temporary `0.02 CNY` baseline is acceptable only when its implied `¥20` Page RPM assumption is recorded and scheduled for replacement with measured data; otherwise omit both fields.

### 7.4 CAPI implementation pattern (Next.js static export)

Static export means no Node.js server and no in-project `app/api/*/route.ts`. CAPI must be sent via a separate serverless/backend project, or skipped for MVP. Do not add API routes to the static export site.

The browser call happens independently and first. Posting the mirrored event to the external endpoint must be best-effort; endpoint absence, timeout, non-2xx response, or consent-helper state must never suppress the browser `fbq` call. Rollback of CAPI must remove only the server transport and its disclosure, not `layout.tsx` Pixel initialization or browser event emitters.

**Option A — Separate Vercel Edge Function project (recommended when CAPI is required)**

```ts
// Separate serverless project, not inside the static export site.
// app/api/capi/route.ts
export const runtime = 'edge'

export async function POST(req: Request) {
  const body = await req.json()
  const { event_name, event_id, event_time, user_data, custom_data, event_source_url } = body

  await fetch(
    `https://graph.facebook.com/v19.0/${process.env.PIXEL_ID}/events`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        data: [{
          event_name,
          event_id,           // must match client-side Pixel event_id
          event_time,         // Unix timestamp (seconds)
          action_source: 'website',
          event_source_url,
          user_data: {
            client_ip_address: req.headers.get('x-forwarded-for')?.split(',')[0],
            client_user_agent: req.headers.get('user-agent'),
            ...user_data,     // em (hashed email), fbc, fbp if available
          },
          custom_data,
        }],
        access_token: process.env.META_CAPI_TOKEN,
      }),
    }
  )
  return new Response('ok')
}
```

Client side fires the Pixel event and posts the same `event_id` to the external endpoint concurrently. Configure the external endpoint URL via project configuration; do not hardcode it into the skill template.

**Option B — Skip CAPI for MVP, add later**

CAPI is not required to launch. Launch with the verified browser Pixel, then add CAPI only when Events Manager shows material signal loss or traffic and spend justify the separate backend. Record the decision and re-run the regression contract when that threshold is reached.

### 7.5 Privacy policy disclosure (required for Pixel)

The privacy policy must explicitly state:
- The site uses Meta Pixel (name it: "Meta Pixel / Facebook Pixel")
- What data the Pixel collects (page visits, custom events)
- That collected data is used for targeted advertising on Meta platforms
- Link to Meta's own privacy policy / ad preferences

Without this disclosure, running Meta Pixel violates GDPR (EU) and CCPA (California). More practically, Meta's ad review can flag the landing page for inadequate privacy disclosure.

---

## 8. Trust pages — Meta-specific requirements

`adsense-arbitrage.md §5` lists the required pages. This section adds what Meta specifically needs in each.

### 8.1 Privacy Policy — required content

Meta's crawler checks that the privacy policy URL is reachable. Content requirements (Meta policy + GDPR/CCPA compliance):

- Data types collected: IP address, browser/device info, cookies, browsing behavior on the site
- Purpose: content delivery, analytics, **advertising and retargeting** — write this explicitly
- **Named third parties: "Meta Platforms, Inc. (Facebook)" as an advertising partner**
- **Explicit Meta Pixel disclosure**: "We use the Meta Pixel to measure ad performance and deliver targeted ads on Facebook and Instagram"
- User rights: access, correction, deletion, opt-out of targeted advertising
- Link to Meta's ad preferences: `https://www.facebook.com/ads/preferences`
- Cookie disclosure
- Contact for privacy inquiries
- GDPR lawful basis (if targeting EU): typically "legitimate interests" for analytics, "consent" for marketing cookies

### 8.2 About page

Must describe the site as a real editorial brand, not a thin shell. Include:
- What genre(s) the site covers
- Brief mission or editorial angle ("We publish romance and paranormal stories for readers who want intensity")
- The site/brand name used consistently with the ad account

### 8.3 Contact page

Must be reachable without login. A dedicated email address is sufficient (`contact@yourdomain.com`). Include DMCA / content removal process.

### 8.4 Cookie consent

Required for any EU/UK traffic. Without a Google-certified CMP:
- AdSense/AdX can only serve non-personalized ads to EU users (lower CPM)
- Meta Pixel cannot set cookies for EU users without consent (attribution degrades)

Use a suitable certified CMP and implement the policy required for the site's actual jurisdictions. On an existing live site, do not introduce a new Pixel gate as a side effect of CAPI, privacy-copy, or banner refactoring. Treat a change from unconditional initialization to consent-gated initialization as a separate high-risk migration requiring owner approval and browser acceptance in all five states: fresh pre-consent, accept, reject, reload after accept, and reload after reject. In a consent-gated design, acceptance must initialize the Pixel immediately and produce exactly one `PageView`; a returning accepted visitor must initialize on first load.

For an enforced opt-in design, the Reject state must block the Meta network path itself: no preconnect, `fbevents.js` request, `fbq('init')`, browser event, CAPI mirror, or `noscript` tracking image. Gate every emitter through the same stored decision; do not let direct scroll or click handlers bypass the shared helper.

---

## 9. What gets accounts banned (ranked by severity)

| Rank | Cause | Severity | Recovery |
|---|---|---|---|
| 1 | **Cloaking** | Permanent ban | Near-zero appeal success |
| 2 | **Creating a new account after being banned** | Permanent cascade ban on all related assets | None |
| 3 | **Reusing payment method / device fingerprint from banned account** | Meta tracks globally — new account gets banned | None |
| 4 | **Misleading or exaggerated claims** | Ad disable → account disable | Possible if root cause fixed |
| 5 | **Ad-to-landing-page mismatch** | Ad rejection → pattern → account review | Fixable |
| 6 | **Budget spike (e.g. $10/day → $2,000/day overnight)** | Account spend limit freeze | Usually reversible |
| 7 | **Multiple ad accounts in same BM with a violating account** | Chain disable across BM | Fixable if clean accounts are separated before violation |
| 8 | **Prohibited content in creative or landing page** | Ad rejection → account review | Fixable |
| 9 | **Payment method issues** (failed charge, mismatch, prepaid/virtual card) | Spend freeze | Fixable |
| 10 | **High Page Feedback Score** (users hiding / reporting ads) | Delivery degradation → eventual disable | Fixable via creative refresh |
| 11 | **Bot/invalid traffic on landing page** | Contaminates Pixel data, breaks learning | Fixable via traffic quality tools |
| 12 | **Copyright infringement** in creative (branded logos, copyrighted music in video) | Ad rejection → escalation | Fixable |

**Arbitrage-specific risks:**
- Buying "aged accounts" or "white-hat accounts" from third parties — if the account has hidden violations, new activity on a new IP triggers those dormant flags
- Running all funnels through one Business Manager — a single violating campaign can freeze the entire BM's ad accounts

### 9.1 Appeal process

If an account is disabled:
1. Business Settings → Account Quality — read the specific violation cited
2. Fix the underlying issue before appealing (appeal with the violation still present always fails)
3. Submit one detailed, professional appeal — explain the business model, show evidence of compliance. Repeat submissions are flagged by the system
4. Operate from your usual device and location (not a VPN, not a new machine)
5. Attach business legitimacy evidence: business registration, domain ownership, payment account match
6. Accounts with $1,000+ recent spend can escalate via Business Manager live chat

---

## 10. Build-time checklist (B4 phase)

Wire these during B4 (trust pages / compliance) before running any Meta campaigns:

**Domain & account setup**
- [ ] Domain verified in Meta Business Suite → Brand Safety → Domains
- [ ] Meta Pixel created and linked to verified domain
- [ ] Ad account warmed up before first conversion campaign (see §6.3)

**Landing page technical**
- [ ] `robots.txt` allows `facebookexternalhit` on all public routes
- [ ] `og:title`, `og:description`, `og:image` present in first 1 MB of HTML on every page
- [ ] `og:image` is the book cover (portrait 2:3) — matches the creative shown in the ad
- [ ] Mobile LCP < 2.5 s (test with PageSpeed Insights mobile)
- [ ] No interstitial or pop-up appears before chapter content loads
- [ ] No redirect chain between the ad's destination URL and the final landing page
- [ ] Meta Pixel fires `PageView` on every chapter load (via `layout.tsx`)
- [ ] `ChapterPixel` client component added to chapter page — fires `ViewContent` on mount + scroll depth events at 25% / 50% / 75% / 90%
- [ ] Pixel-adjacent changes pass `adsense-arbitrage.md §4.1.1`: fresh hard load, hard next chapter, any true SPA change, reading milestones, CAPI-unavailable fallback, and the consent-state matrix when consent behavior changed
- [ ] Custom conversions created in 事件管理工具: `ChapterRead50`, `ChapterCompleted`
- [ ] AEM configured: `ChapterCompleted(1) > ChapterRead50(2) > ViewContent(3) > PageView(4)`
- [ ] `.prose-reader` uses system sans-serif stack, ≥19px mobile, line-height 1.8, max-width 68ch, word-break break-word (see §3.4)

**Content consistency**
- [ ] Ad creative's cover matches the book on the landing page
- [ ] Ad copy's implied genre/tone matches the landing chapter's content
- [ ] No specific claims in ad copy (price, character name, plot point) that the landing page does not deliver

**Trust pages** (see `adsense-arbitrage.md §5` for page structure)
- [ ] `/privacy` exists, is reachable without login, names Meta Pixel, names Google as ad partner, lists user rights
- [ ] `/terms`, `/about`, `/contact` exist and are footer-linked on every page
- [ ] Cookie consent behavior matches the approved jurisdiction policy; if gating is required, fresh/accept/reject/returning states were browser-tested without missing or duplicate initialization

**Cloaking safety**
- [ ] No middleware or edge logic serves different content based on User-Agent or IP range
- [ ] Next.js static export is confirmed — same HTML served to all crawlers and users
- [ ] No separate "crawler-friendly" page vs. "user page" distinction anywhere in the codebase

**Pixel / CAPI (when running campaigns)**
- [ ] Meta Pixel ID is real and matches the verified domain (no placeholder)
- [ ] Pixel `strategy="afterInteractive"` via `next/script` — does not block render
- [ ] Layout bootstrap still owns exactly one hard-load `PageView`; the route tracker skips initial mount and handles only genuine SPA pathname changes
- [ ] Browser `fbq` still sends when the CAPI endpoint is absent, fails, or is removed
- [ ] (If CAPI implemented) unique `event_id` generated per event, same ID sent by both Pixel and CAPI
- [ ] Privacy policy explicitly discloses Meta Pixel use
- [ ] Campaign optimization event is `ViewContent` or `NextChapter`, not `PageView`

---

## 11. OG tags — technical requirements

Meta's crawler fetches OG tags during ad review. Requirements:

- All tags must appear **within the first 1 MB of the HTML document** — pages that dynamically inject OG tags client-side (e.g., via `useEffect`) will have blank link previews and may fail ad review
- Next.js App Router `metadata` export generates OG tags server-side in the `<head>` — this is correct; do not move OG generation to client components
- `og:image` must be an absolute URL (not a relative path); `metadataBase` in `layout.tsx` ensures Next.js resolves relative paths to absolute URLs automatically
- Recommended `og:image` dimensions for Facebook link preview: **1200×630** (landscape) for news feed, or the book cover at **848×1280** (portrait) — both are accepted; portrait cover is already the correct asset
- `og:type` should be `article` on chapter pages and `book` on book detail pages

```tsx
// Chapter page — server component metadata
export function generateMetadata({ params }: Props): Metadata {
  const book = getBook(params.slug)
  const chapter = getChapter(params.slug, params.n)
  return {
    title: `${chapter.title} — ${book.title}`,
    description: `Read Chapter ${params.n} of ${book.title}.`,
    openGraph: {
      title: `${chapter.title} — ${book.title}`,
      description: `Read Chapter ${params.n} of ${book.title}.`,
      images: [{ url: book.cover, width: 848, height: 1280, alt: book.title }],
      type: 'article',
      siteName: 'Your Site Name',
    },
    twitter: { card: 'summary_large_image' },
  }
}
```

`metadataBase` set once in `layout.tsx` resolves all relative cover paths to absolute URLs across all pages — no per-page `metadataBase` needed.
