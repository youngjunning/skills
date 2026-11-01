# Distribution Launcher

Use this reference during **phase 5 — before go-live**. The distribution plan must be ready before the site launches so the first 2–4 weeks of organic activity are guided from day one. Those weeks are when Google first crawls and indexes the site; real engagement signals during that period carry outsized weight.

Do not create this plan after launch. A plan written after the fact describes what already happened, not what to do next.

The goal is **real users with genuine interest** — not raw pageview counts. AdSense evaluates traffic quality. Sites with high bounce rates, sub-10-second sessions, and zero return visits are at higher risk of rejection or policy violations after approval.

---

## Core Strategy for New Sites

New sites need a sequenced approach. Do not try every channel at once.

**Day 1 (go-live):** submit sitemap to GSC, request indexing for homepage and primary tool page, execute the first distribution action (Product Hunt launch or first community post).

**Week 1–2:** seed search indexing and establish presence in one relevant community. Prioritize channels that bring users who will actually use the tool.

**Week 3–4 (during GSC wait period):** build the first backlinks through directory submissions and genuine community participation. These weeks are also when to record the tool demo video.

**After AdSense approval (month 2+):** layer in content repurposing, Pinterest if relevant, and paid if appropriate.

---

## Safe Channels

### 1. Google Organic Search (primary long-term channel)

The only channel that compounds. Every action you take elsewhere should ultimately serve this.

Actions:
- Submit `sitemap.xml` to Google Search Console on launch day.
- Use the URL Inspection tool to request indexing for the primary tool page and homepage.
- Monitor GSC weekly: watch for crawl errors, coverage drops, and which queries are generating impressions.
- Update supporting pages as Google surfaces new query patterns in GSC.

Signals to watch: organic impressions, click-through rate by page, average position for target keywords.

### 2. Directory Submissions (fastest initial backlinks)

Submit to directories that accept new tools and sites. These are also real traffic sources:

| Directory | Best For | Notes |
| --- | --- | --- |
| Product Hunt | Any tool or productivity site | Schedule a launch; prepare a short description and screenshots |
| Indie Hackers | Developer tools, side projects | Post a "just launched" update, not a pure promotion |
| Hacker News "Show HN" | Developer, productivity, data tools | Only if the site is genuinely useful and not purely ad-monetized |
| AlternativeTo | Any site that competes with an existing tool | Add a listing and description |
| There's An AI For That / Futurepedia | AI-adjacent tools | Free listing |
| G2 / Capterra | B2B tools with a free tier | Create a vendor profile |
| Toolify / AI Tool directories | AI tools | Free listing |
| Niche-specific directories | Match the niche (e.g., recipe tools → recipe directories) | Search "[niche] + resource directory" to find them |

Do not submit to low-quality link farms or "1000 free directory submissions" services. One real directory is worth 100 spam directories.

### 3. Community Participation (first real users)

Do not post promotional links. Participate first, then mention the tool when it genuinely helps.

| Platform | Approach |
| --- | --- |
| Reddit | Find the 2–3 subreddits where the target audience is. Answer questions. When someone asks for a calculator or tool of this type, share the site. Do not post as an ad. |
| Quora | Search for questions that the site's content directly answers. Write a full answer first, then link to the tool or guide as a resource. |
| Facebook Groups | Same approach as Reddit. Join the group before posting. Contribute context before sharing a link. |
| Discord communities | Many niche communities have a `#resources` or `#tools` channel. Share there once, genuinely. |
| Stack Overflow / niche forums | Only when a question is directly answerable with the tool or content. |

One genuine community mention from a relevant subreddit brings better users than 100 from a general link-drop.

### 4. Pinterest (for template, checklist, and visual topics)

Effective for template libraries, checklist hubs, and tutorial hubs. Pinterest has its own search engine and drives sustained referral traffic.

Actions:
- Create one board per page cluster.
- Pin a clean image of the tool output, template preview, or checklist design for each major page.
- Pin descriptions include the target keyword and a link to the page.
- Consistency beats volume: 3 pins per week is better than 30 in one day.

### 5. YouTube Shorts or TikTok (for tool demos)

A 30-60 second screen recording showing the tool solving a real problem drives both brand awareness and direct visits. It also signals to Google that the site is a real product.

Actions:
- Record one demo per tool page.
- Mention the site URL in the first 5 seconds and in the description.
- Post on YouTube (discoverable via Google search) and optionally TikTok.
- Title and description should include the target keyword.

### 6. Newsletter or Creator Outreach

Find newsletters, blogs, or YouTube channels in the niche with audiences who would use the tool. Offer them:
- Free access or a preview
- A short description they can include in a roundup
- A genuine reason why their audience would find it useful

Do not buy newsletter placements that promise "1000 clicks guaranteed." Those are the same as traffic packages.

### 7. Paid Search (only after organic shows intent)

Small paid tests ($20–$50) on Google Search Ads are legitimate after GSC shows real queries with commercial or tool intent. Target the exact keywords the site is trying to rank for. The goal is to validate click-through rate before relying on organic position.

Do not run display ads or social ads before AdSense approval — the traffic quality from broad targeting is poor and risks invalid click patterns.

---

## Unsafe Channels

Reject all of these. They risk AdSense account suspension, not just low-quality traffic:

- Traffic packages promising guaranteed visits
- Bot visits or automated browsing
- Autosurf and traffic exchange networks (where you view others' sites to earn views)
- Incentivized clicks or click rings
- Popunder ad networks used to inflate impressions before AdSense approval
- Paid social ads targeting interest audiences with no search intent (they bounce immediately)
- Any tactic whose primary purpose is hitting a visit count rather than reaching users with genuine interest

---

## Metrics That Matter

These are the signals AdSense and Google organic both care about:

| Metric | What it means |
| --- | --- |
| Average session duration > 45s | Users are reading and using the tool |
| Pages per session > 1.5 | Internal links are working; users explore |
| Return visitor rate | The site has something worth coming back to |
| Tool completion rate | Users who start the tool actually finish it |
| Organic click-through rate | Title and meta description are matching search intent |
| Backlinks from real sites | The site has earned trust, not bought it |
| Zero-bounce on tool page | Users are engaging, not immediately leaving |

Metrics to ignore before AdSense approval: raw pageviews, social impressions, follower counts.

---

## 14-Day Launch Sequence

| Day | Action |
| --- | --- |
| 1 | Submit sitemap.xml to Google Search Console. Request indexing for homepage and primary tool page. |
| 2 | Submit to Product Hunt or Indie Hackers (whichever fits the niche). Prepare launch assets: description, screenshots, short demo video. |
| 3–5 | Find 3 relevant subreddits, Quora threads, or Discord communities. Read and participate before posting anything. |
| 6–7 | Post to AlternativeTo and 2–3 niche-specific directories. |
| 8–10 | Find one or two Quora questions the site content directly answers. Write full answers and include the tool link as a resource. |
| 11–12 | Record a 60-second screen demo of the primary tool. Post to YouTube Shorts with the target keyword in the title. |
| 13–14 | Check GSC for early impressions. Note which queries are surfacing. Identify 1–2 supporting pages that should be written or improved based on real query data. |

---

## Completion Gate

Before advancing to phase 6 (go-live), verify all of the following:

- [ ] `outputs/<site-slug>/launch-plan.md` is written and complete — not the generic template, but adapted to this specific niche and audience.
- [ ] The 14-Day Sequence is fully specified with concrete actions (not placeholders like "post somewhere relevant").
- [ ] Every channel listed is from the Safe Channels section. No unsafe channels are in the plan.
- [ ] All assets needed for Day 1 are either ready or explicitly listed as "to prepare before launch": Product Hunt description, screenshots, demo video script, community post draft.
- [ ] Metrics to watch are defined with target ranges for this niche (not just copied from the template).
- [ ] The plan does not rely on GA data if GA was not set up in phase 5 — revise metric tracking to use GSC data only if GA is absent.

---

## Output

Write `outputs/<site-slug>/launch-plan.md`:

```md
# Launch Plan

## Audience
[Who this site is for in one sentence]

## Positioning
[What makes this site worth using over the existing results]

## Channels

| Channel | Action | Asset Needed | Timeline | Expected Signal |
| --- | --- | --- | --- | --- |

## 14-Day Sequence
[Specific daily actions from the template above, adapted to this niche]

## Content Repurposing
[How the primary tool or content can be adapted for YouTube, Pinterest, or community posts]

## Metrics to Watch
[3–5 specific metrics with target ranges for this niche]

## Avoid
[Traffic tactics ruled out for this site and why]
```
