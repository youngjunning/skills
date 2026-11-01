# AdSense Readiness Auditor

Use this reference during phase 7 — after the site has been live for 2–4 weeks — before recommending AdSense submission. The two goals are: (1) pass the review on the first attempt, (2) maintain account health after approval.

Do not recommend submission unless every blocking item passes. "Needs revision" is always better than a rejected or suspended account.

---

## Submission Timing

Confirm the site meets these preconditions before running the audit:

- The site has been live on the **final domain** for at least **2–4 weeks**.
- Google Search Console shows at least **15 indexed pages**. (GSC can lag real crawl coverage by a few days — if the site has 15+ live pages but only 12 are indexed, use the URL Inspection tool to request indexing for the unindexed pages and wait a few more days before submitting. Do not submit with fewer than 10 indexed pages under any circumstances.)
- GSC shows **some impressions** (even low ones). This proves the site is real to Google before you apply.
- All pages load on **HTTPS**. HTTP is an instant rejection.
- The Google account being used for AdSense has **no existing policy violations**.

If any precondition is not met, note it in the report and do not recommend submission yet.

---

## Audit Checklist

### 1. Content Quality (blocking if failed)

#### 1a. Google AdSense policy requirements

The following checks reflect explicit language from Google's official AdSense approval page (support.google.com/adsense/answer/81904). Failing any of them is a policy violation, not just a quality concern.

| Check | Pass Criteria |
| --- | --- |
| Site fully launched | The site is complete and live — not under construction, not a template shell. Google explicitly rejects sites that are still being built at application time. |
| Content is primarily text | Pages must be primarily text-based, not mainly images, videos, Flash, or animations. Visual content can supplement text but must not replace it. |
| Complete sentences and paragraphs | Pages must contain complete sentences and paragraphs — not only headlines, subheadings, bullet lists, or navigation menus. |
| No auto-generated pages | No page is auto-generated or contains little to no original content. Google explicitly names this as a rejection cause. |
| Affiliate content is minor or adds original value | If the site contains affiliate links or affiliate content, it represents a minor portion of the overall site or adds substantial original value beyond what the linked product page already provides. Google explicitly flags affiliate-heavy thin sites as a rejection reason. |

#### 1b. Internal quality gates

The following checks are not stated requirements in Google's official policy but reflect the practical standards that distinguish approvable sites from those that fail on "low value content." Google's stated standard is "sufficient content" — the thresholds below represent what that means in practice.

| Check | Pass Criteria |
| --- | --- |
| Sufficient page count | Enough complete, indexable pages that the site clearly serves its stated purpose. 15+ pages is the practical safe threshold; fewer than 10 is almost always insufficient. Google has no official minimum number. |
| Primary experience works | Main tool, calculator, template library, directory, or checklist functions correctly and produces real output. |
| No placeholder content | Zero "Lorem ipsum", "Coming soon", or blank sections on published pages. |
| No thin pages | No page consists only of headings, bullet lists, or undifferentiated text without original information or analysis. |
| No copied content | Content is original — not scraped, spun, or mirrored from other sites. |
| No fabricated claims | No invented statistics, fake examples, or unverifiable facts. |
| Supporting pages are distinct | No two pages are near-identical with only a keyword swapped. |

### 2. Trust and Identity Pages (blocking if any are missing)

These are required by AdSense policy. Missing any will cause rejection.

| Page | Required Content |
| --- | --- |
| **Privacy Policy** | Must explicitly state: (1) the site uses Google AdSense to serve ads; (2) Google uses cookies, including the DoubleClick cookie; (3) users can opt out via [Google's Ads Settings](https://adssettings.google.com). Must also disclose any other data collection. Link from every page footer. |
| **About** | States who runs the site and what it helps users do. No fake biographies, fabricated credentials, or fake company claims. |
| **Contact** | A working email address or functional contact form. Must be reachable by Google reviewers. |
| **Terms of Use** | Covers acceptable use, disclaimers, and limitations of liability. Required whenever the site is interactive or offers tools. |

### 3. Technical Requirements (blocking if failed)

| Check | Pass Criteria |
| --- | --- |
| HTTPS | All pages load on HTTPS. No mixed-content warnings. |
| Mobile responsive | Site renders correctly at 375px viewport. No horizontal scroll. |
| No broken navigation | All primary nav links resolve. Zero 404s in the main navigation. |
| sitemap.xml | Exists at `/sitemap.xml` and submitted to Google Search Console. |
| robots.txt | Exists at `/robots.txt`. Does not block Googlebot from key pages. |
| Page speed | LCP under 4s on mobile (verify with PageSpeed Insights). |
| No intrusive pop-ups | No full-screen overlays blocking content on page load before user interaction. |
| No auto-play media | No video or audio that auto-plays without user action. |
| AdSense auto-ads script in `<head>` | The `pagead2.googlesyndication.com` script is present in the `<head>` of every page with the correct `ca-pub-XXXXXXXX` publisher ID. Google uses this to verify site ownership during review. |

### 4. AdSense Policy Compliance (blocking if any violation present)

| Check | Pass Criteria |
| --- | --- |
| No banned category content | No adult, gambling, weapons, drugs, hate, hacking, or piracy content anywhere on the site |
| YMYL pages have disclaimers | Health, legal, financial content includes "consult a professional" and does not make specific diagnoses, legal advice, or investment recommendations |
| No hidden text or cloaking | Visible content matches what Googlebot sees |
| No excessive outbound links | No link farms or pages primarily consisting of outbound links to low-quality sites |
| Ad placement preview | Ads will not appear before primary content, will not occupy more than 30% of the viewport, and will not surround content on all sides |

### 5. User Experience

| Check | Pass Criteria |
| --- | --- |
| Clear site purpose | A new visitor understands what the site does within 5 seconds |
| Primary utility above the fold | Users do not scroll past ads or unrelated content to reach the main tool or content |
| Readable typography | Body text ≥ 16px. Sufficient contrast (WCAG AA). |
| Internal linking present | Pages link to related content. No orphan pages. |

### 6. Competitive Differentiation (advisory — not blocking for AdSense, but affects long-term ranking)

If `competitive_brief` is present in `outputs/niches.json`, verify that the site actually beat the incumbents on the documented weaknesses. This is not an AdSense policy requirement, but a site that fails its own differentiation baseline will plateau in organic search shortly after approval.

| Check | Pass Criteria |
| --- | --- |
| All `competitive_brief` entries were addressed | Phase 4's completion gate confirmed each entry was handled. No entry was silently dropped. |
| Build actions are visible on the live site | For each `beat_action` recorded in the brief, the corresponding improvement is live and verifiable on the real site. |
| Site is measurably better than incumbents | The differentiating element (tool, depth, CWV, freshness, free access) exists and works on the live site. |

### 7. Traffic Quality Pre-Check

| Check | Pass Criteria |
| --- | --- |
| No invalid traffic sources | Launch plan uses only organic search, legitimate communities, and real paid acquisition |
| No incentivized traffic | No traffic exchanges, bots, autosurf, or click incentives — now or planned |
| No self-click risk | Site owner and team will not click ads, will not ask others to click ads |

---

## Scoring

- **Ready** — all blocking items pass. Submit.
- **Needs revision** — one or more non-blocking issues fail. Fix before submitting.
- **Not ready** — any blocking item fails. List each with a concrete fix.

Blocking items (any failure = do not submit):
- Privacy Policy missing or does not mention Google AdSense and cookies
- About page missing
- Contact page missing or non-functional
- Primary experience broken or unfinished
- Site on HTTP
- Insufficient page count (Google's standard is "sufficient content" — fewer than 10 complete, indexable pages is almost always insufficient; 15+ is the practical safe threshold)
- Content is primarily images/videos, not text — or pages contain only headlines without complete sentences
- Site not indexed in Google Search Console, or GSC shows zero impressions (no impressions means Google has not yet registered the site as real — wait until impressions appear before submitting)
- Any banned category content present

---

## Output

Write `outputs/<site-slug>/adsense-readiness-report.md`:

```md
# AdSense Readiness Report

## Verdict
ready | needs revision | not ready

## Submission Preconditions
- Site age on final domain: [X weeks]
- Indexed pages in GSC: [count]
- GSC impressions present: yes | no
- HTTPS: yes | no
- AdSense account clean: yes | no | unknown

## Audit Results

### 1. Content Quality
| Check | Result | Notes |
| --- | --- | --- |

### 2. Trust and Identity Pages
| Page | Result | Notes |
| --- | --- | --- |

### 3. Technical Requirements
| Check | Result | Notes |
| --- | --- | --- |

### 4. AdSense Policy Compliance
| Check | Result | Notes |
| --- | --- | --- |

### 5. User Experience
| Check | Result | Notes |
| --- | --- | --- |

### 6. Competitive Differentiation
| Check | Result | Notes |
| --- | --- | --- |

### 7. Traffic Quality Pre-Check
| Check | Result | Notes |
| --- | --- | --- |

## Blocking Issues
[Each failing blocking item with a specific fix]

## Recommended Fixes (Non-Blocking)
[Each non-blocking issue with a specific fix]

## Submission Recommendation
[Submit now / Fix X first / Do not submit — state clearly]
```
