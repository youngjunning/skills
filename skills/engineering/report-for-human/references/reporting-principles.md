# Reporting Principles: Public-Source Synthesis

Use this reference when adapting a report for leadership, auditing the reporting style, or explaining why the skill makes a reporting decision. Ordinary engineering handoffs can follow `SKILL.md` without loading this file.

## Evidence boundary

The sources below are public, first-party statements about company values, leadership, goal setting, operations, or written decision practices. They do **not** establish one canonical internal reporting template for any company. The reporting rules are a cross-company synthesis: each rule is an engineering inference from a stated operating principle, not a claim that every team inside that company reports in the same way.

## What each company contributes

| Public principle | Reporting strength to retain | Do not overgeneralize |
| --- | --- | --- |
| **Tencent:** “Value for Users, Tech for Good”; integrity, proactivity, collaboration, and creativity | Start from user value; surface cross-team dependencies; report proactively and honestly | These values do not prove a Tencent-wide document format |
| **Alibaba:** customers first, trust, change, ownership, and “today’s best performance is tomorrow’s baseline” | Tie results to customer value; be straightforward; name the owner; compare with a baseline and state the next measurable bar | Do not turn cultural slogans into forced headings or demand endless scope expansion |
| **ByteDance:** be candid and clear; avoid managing up; use facts rather than assumptions or emotion; seek first-hand data and real impact | State bad news directly; remove jargon and flattering narration; separate fact from inference; prioritize real impact over activity | Directness does not justify rudeness, missing context, or unverified certainty |
| **Microsoft:** create clarity, generate energy, deliver success; growth mindset, customer obsession, and One Microsoft | Make the decision and success condition clear; preserve learning; report contribution and shared dependencies, not only individual output | A learning mindset does not weaken accountability or delivery gates |
| **Google:** OKRs for setting and tracking goals; SRE postmortems for learning from failure | Report target and measurable result; state impact; use blameless root-cause analysis and owned action items | OKRs are not required for every small report; blameless does not mean actionless |
| **Tesla:** first-principles problem solving, extreme scale, vertical integration, and repeated real-world deployment | Identify the governing constraint; challenge inherited assumptions; report the whole delivery chain and real-world verification | Urgency does not justify skipping safety, quality, evidence, or authorization |
| **Amazon:** customer obsession, ownership, Dive Deep, Deliver Results, narrative memos, and working backwards | Start from customer outcome; give a complete causal narrative; reconcile metrics with anecdotes; preserve enough detail for “why” questions | Six pages is a maximum for a particular practice, not a target length for routine updates |

## Integrated reporting model

### Decision layer

The top of the report should let a busy reader answer:

1. What target or customer problem mattered?
2. What result changed, by how much, and with what confidence?
3. What state is the work actually in?
4. What needs a decision, mitigation, or owner now?

### Evidence layer

Support the decision layer with:

- baseline, target, actual result, scope, time window, and method;
- behavior or artifact changes and intentionally unchanged scope;
- first-hand tests, observations, raw measurements, commits, artifacts, or URLs;
- root cause, contributing conditions, and alternative explanations where relevant;
- lifecycle state and rollback or reversibility boundaries.

### Action layer

Turn unresolved facts into explicit control points:

- todo plus completion condition;
- risk plus cause, impact, likelihood when known, and mitigation;
- blocker plus blocked step and unblock condition;
- decision request plus recommendation, alternatives, tradeoff, owner, and real deadline when known.

## Anti-patterns

- **Tool narration:** “我会用 report-for-human 做一次影响评估……” describes the reporter, not the result.
- **Activity theater:** “完成 12 项工作、召开 3 次会议” says nothing about target attainment or impact.
- **Managing up:** positive results are prominent while misses, caveats, or unverified gates are buried.
- **Metric theater:** a number has no baseline, target, denominator, time window, or decision consequence.
- **Status inflation:** local, built, committed, pushed, deployed, and production-verified states are blurred.
- **Template compliance:** empty headings and repeated “无” make a report longer without improving a decision.
- **Blame narrative:** an individual is named as the cause while system conditions, controls, and prevention are omitted.
- **Unowned next step:** “后续持续关注” has no action, owner, completion condition, or trigger.

## Primary public sources

- Tencent, [Value for Users, Tech for Good](https://www.tencent.com/value-for-users-tech-for-good/)
- Alibaba Group, [Alibaba Unveils Six New Company Values for the Digital Era](https://www.alibabagroup.com/en-US/document-1491212036011458560)
- ByteDance, [Company and ByteStyles](https://www.bytedance.com/en/)
- Microsoft, [Code Book](https://news.microsoft.com/codebook/)
- Google, [Let’s Make Work Better](https://blog.google/company-news/outreach-and-initiatives/small-business/lets-make-work-better/)
- Google SRE, [Postmortem Culture: Learning from Failure](https://sre.google/resources/book-update/postmortem-culture/)
- Tesla, [About Us](https://www.tesla.com/about)
- Amazon, [Leadership Principles](https://www.aboutamazon.com/about-us/leadership-principles)
- Amazon, [2024 Letter to Shareholders](https://www.aboutamazon.com/news/company-news/amazon-ceo-andy-jassy-2024-letter-to-shareholders)

Recheck live sources before making time-sensitive claims about current company practices. Preserve this boundary even if secondary articles assert a more specific internal convention.
