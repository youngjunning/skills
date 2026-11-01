# Paid-Traffic Landing Page Requirements

Use this reference when a chapter page is the destination URL for Meta/Facebook paid traffic. It is operational, not policy-only: the goal is lower cost per result by improving landing-page quality, completed-read rate, and next-chapter clicks while preserving ad revenue.

## 1. Default Landing URL

- Use `/book/{slug}/chapter/1/` as the default ad destination.
- The ad creative cover, book title, genre promise, and quoted hook must match the landing chapter.
- Avoid nonessential query strings in the ad URL. Standard `utm_*` parameters are fine.
- Do not gate, redirect, cloak, or vary content for Meta crawlers.

## 2. Chapter 1 Content

Chapter 1 is both story opening and conversion page.

- Target length: **1,100-1,600 words**.
- If chapter 1 exceeds ~1,700 words, split at the strongest unresolved beat and move the second half to chapter 2.
- First paragraph must state or strongly imply the central commercial hook: debt, forced proximity, secret, power imbalance, forbidden desire, danger, or impossible choice.
- First 300-500 words must answer: who is in trouble, what they want, who has power over the outcome, and why the reader should keep going.
- End chapter 1 on a hard hook-out, not a soft emotional resolution.

## 3. First Screen

The reader should immediately understand the book and the conflict.

- Show a compact book cover + title + author + 1-2 genre chips above the chapter title.
- Keep the book tagline visible, but cap it to a few lines.
- Remove duplicate rendered headings. If Markdown starts with `# Chapter 1: ...`, strip it before rendering prose because the page already renders `<h1>`.
- Clean display titles so UI does not show `Chapter 1: Chapter 1: Title`.

## 3.1 Distraction Lock

Chapter 1 is a conversion page, not a browse page. Remove every competing action until the reader has started the story.

- Hide the top navigation bar on chapter 1 landing pages.
- Hide side menus, drawer triggers, and back buttons on chapter 1 landing pages.
- Do not render the table of contents on chapter 1 landing pages.
- Do not render book recommendations on chapter 1 landing pages before or after the prose.
- The only meaningful action on the page should be the primary next-chapter CTA after the prose.
- If the implementation needs a logo for brand presence, it must be static and non-interactive on chapter 1.

## 4. Ad Density

Use a different density rule for chapter 1 than for later chapters.

- **Chapter 1:** exactly **3 ads** for normal 1,100-1,600 word landers:
  - one top ad before prose
  - one in-content ad after the first content segment
  - one in-content ad after the second content segment
- Skip the later q3 / third mid-content slot on chapter 1 unless chapter 1 is over ~2,000 words.
- **Other chapters:** use **4-5 ads** depending on length and sticky/anchor inventory.
- Never add popups, prestitials, interstitials, or anything that appears before content loads.

## 5. Tracking Events

The landing page should train Meta toward readers, not raw clickers.

- Fire `PageView` globally.
- Fire chapter `ViewContent` on chapter load.
- Fire `TimeOnPage30` after 30 seconds.
- Fire `ChapterRead50` around 50% scroll.
- Fire `ChapterCompleted` when the chapter-end sentinel enters viewport, before recommendations.
- Fire `NextChapterClick` on the chapter 2 CTA.

Use `ChapterCompleted` and/or `NextChapterClick` as quality signals when evaluating campaigns. Raw landing-page views alone are too noisy.

Whenever a dashboard, checklist, or Meta setup guide lists conversion or optimization events, include `NextChapterClick` together with `ChapterRead50`, `ChapterCompleted`, and `TimeOnPage30`. It is the cleanest continuation-intent signal after a chapter-1 ad click.

## 6. SEO And Preview

- Add canonical metadata for chapter pages.
- Sitemap chapter URLs must come from actual published chapter documents, not stale `book.chapterCount`.
- OG title/description/image must match the advertised book.
- The cover image should be compressed enough for mobile LCP; target under 100-150 KB.

## 7. QA Checklist

Before pushing or deploying a paid-traffic lander:

- [ ] Chapter 1 word count is 1,100-1,600, or there is a specific reason it is not.
- [ ] Built HTML has exactly 3 GPT/AdSense slots on chapter 1.
- [ ] Built HTML has no duplicate chapter title.
- [ ] First paragraph contains the campaign hook.
- [ ] Chapter 1 has no visible nav bar, side menu, back button, TOC, or recommendation grid.
- [ ] Chapter-end sentinel exists before nav/recommendations.
- [ ] Next-chapter CTA is visible, specific, and tracks `NextChapterClick`.
- [ ] Canonical URL and sitemap URL use the same trailing-slash format.
