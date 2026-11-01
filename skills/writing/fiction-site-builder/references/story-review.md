# Story Review

Load this reference when the user asks for a review, audit, or quality check of written chapters or a complete manuscript.

## Purpose

Find structural, character, prose, and consistency problems and give actionable revision instructions. The mandate is to find problems — not to validate what works.

## Review Modes

| Mode | When | Scope |
| --- | --- | --- |
| `full` | User explicitly asks for a deep audit | Structure + character + prose + consistency |
| `lean` | Default for pipeline use; fast turnaround | Structure + consistency only |
| `solo` | Single-pass; no sub-agents | All dimensions, inline execution |

Default to `lean` when running as part of the fiction-site-builder pipeline. Use `full` only when the user asks for it. If no agents are deployed or the environment doesn't support sub-agents, fall back to `solo` automatically and note the fallback in the report.

## Report Header (always output verbatim)

```
Requested Mode: full | lean | solo
Effective Mode: full | lean | solo
Fallback: none | missing agents -> solo | agent tool unavailable -> solo
```

## Review Dimensions

**Before reviewing:** load the relevant genre file — `genre-romance.md`, `genre-mystery.md`, `genre-horror.md`, `genre-fantasy.md`, `genre-scifi.md`, or `genre-drama.md`. The genre file's escalation register (Heat Level / Dread Register / Terror Register / Wonder Register / Hope Arc / Emotional Tension Register) is needed to audit whether genre-specific pacing is progressing correctly across chapters.

### 1. Structure Audit

- Does each chapter have a hook, escalation, turn, and hook-out?
- Run the mandatory First-Three-Chapter Conversion Gate from `story-long-write.md` whenever Chapters 1–3 are in scope. Report every row as PASS or FAIL; do not replace this with a general statement that the opening has hooks.
- Hard-fail Chapter 1 unless its first sentence contains active conflict, contradiction, abnormality, or a decision already in motion; a setting line, weather line, or retrospective setup does not pass.
- Hard-fail Chapter 1 unless one on-page event within the first 500 words overturns the protagonist's ordinary situation and changes her available options.
- Audit Chapter 1's foreground payloads: retain only the present dilemma, one abnormal detail, and one unresolved question. Move all other background into pressured dialogue or consequential action; explanatory interior-history blocks fail even when the facts are relevant.
- Audit Chapter 1's middle in rolling 200-word windows. Fail any window with more than 2 new memory burdens (new names, institutions, document types, acronyms, or specialized system concepts), and fail any system fact that does not cause visible action within the next 2 paragraphs.
- Hard-fail Chapter 1's final line unless it lands on a high-risk choice, a cognition-changing clue, or an opponent action already underway. Mood, summary, generalized resolve, and a question that changes no options do not pass.
- Do Chapters 1–2 deliver the advertised primary conflict? Require romantic charge only when romance is a primary promise; do not downgrade identity, family, legal, medical, crime, horror, or revenge openings for prioritizing their external engine.
- Does the chapter end with forward pull (reader wants next chapter)?
- Are any chapters filler — nothing changes from beginning to end?
- Is the arc pacing consistent, or does the middle sag?
- Are all planted foreshadows tracked and resolved (or intentionally open)?
- Does the book run at least three interacting storylines (core arc, external crisis, supporting-character agenda), each with its own goal, opposition, midpoint reversal, and endgame consequence?
- Does every chapter materially change goal, leverage, information, allegiance, deadline, safety, reputation, or access?
- Does every chapter's attempted solution create a local complication or reversal instead of succeeding cleanly?
- Does every major turn alter at least 2 relationship edges, or alter one relationship while materially damaging another storyline?
- Is there an irreversible consequence every 2–3 chapters and a major reversal every 5–6 chapters?
- Does the book use at least 4 distinct reversal mechanisms instead of recycling misunderstandings or withheld secrets?
- **Genre register check:** is the genre's escalation register (from the genre file) advancing correctly? Romance: heat level climbing toward the peak scene. Mystery: dread register building through investigation arc. Horror: terror register escalating from unease → dread → terror → horror. Fantasy: wonder register expanding as the world reveals itself. Sci-Fi: hope arc moving from compliant despair toward earned possibility. Drama: emotional tension register advancing E1 → E2 → E3 → E4 → E5 (surface normal → cracks showing → partial truth out → confrontation → earned reckoning).

Flag: chapters with no turn, chapters that end on summary/reflection, back-to-back low-stakes chapters, genre register stalling or resetting without narrative cause, dialogue-only cliffhangers with no material change, storyline lanes that never collide, and reversals that merely reveal information without changing anyone's options.

**Suspense integrity flags** (apply to mystery, thriller, gothic; check during structure audit):

| Pitfall | Signal | Fix direction |
|---------|--------|---------------|
| Logic holes | The solution requires information not available to the protagonist at the time of deduction; timeline contradictions | Trace the deduction chain; ensure every inference is supported by a planted clue |
| Mid-section drag | Consecutive chapters where the investigation makes no net progress; reader learns nothing new | Cut or compress; every chapter must either open a new thread or close a false one |
| Character-as-tool | Supporting characters exist only to deliver clues and have no independent motivation | Give each supporting character a reason to be in the scene that is not "to help the protagonist" |
| Twist without setup | The reveal introduces information not available to the reader before the final act | Audit planted foreshadows in `tracking/threads.md`; add at minimum two independent setups |
| Abrupt ending | The resolution arrives before the reader has processed the final reversal; emotional payoff is skipped | Add one scene between the reveal and the close that shows the protagonist — and at least one other character — reckon with what the truth means |
| Expertise gap | Investigative method is technically incorrect (forensics, legal procedure, period-accurate agency) | Verify against genre standard; the reader's suspension of disbelief breaks at domain errors |
| Emotional absence | The mystery is solved but the reader does not feel anything at the reveal | The victim must be known before they are gone; the antagonist must be understood before they are caught |
| Foreshadow orphans | A detail was planted but never paid off; or a payoff arrives with no planted setup | Cross-reference `tracking/threads.md`; every planted element must resolve; every reveal must have a planted ancestor |

### 2. Character Audit

- Does the book have 6–8 active named characters, with at least 4 repeatedly affecting the main plot?
- Do recurring supporting characters appear in at least 3 chapters and cause a material plot change in at least 2?
- Are lead-only chapters no more than 30% of the book?
- Does every rolling block of 3 chapters beginning with Chapter 2 contain at least 2 chapters with 3 or more active scene participants?
- Does at least one supporting-character decision every 2 chapters change access, information, safety, reputation, resources, or allegiance?
- Do supporting characters interact without either lead present at least twice?
- Does each supporting character have an independent goal, leverage/resource, conflict action, and alignment path?
- Does every active character have at least 3 consequential relationship edges, including hidden friction/debt and a conflicting loyalty?
- Do at least 3 relationships change state twice, rather than remaining fixed around the central couple?
- Does each major character have a consistent voice in dialogue?
- Are character motivations coherent across scenes?
- Does any character act against established personality without earned cause?
- Is the protagonist's change arc progressing?

Flag: dialogue that could be spoken by any character interchangeably, unmotivated decisions, characters who disappear mid-arc, passive confidants, one-use messengers, disposable jealousy devices, named characters who never change the plot, and scenes padded with background extras to fake an ensemble.

### 3. Prose Audit

Run the Gate A–G scan from `references/story-deslop.md`. Report:

- Overall AI flavor severity (Mild / Moderate / Severe)
- Top 3 recurring patterns
- Worst 2–3 passages (location + problem + suggested fix)

Do not rewrite prose in a review — that is `/story-deslop`'s job. Point to specific lines and describe the fix.

### 4. Consistency Audit

- Are character names, appearance, and traits consistent across chapters?
- Are setting details (geography, distances, time-of-day) internally coherent?
- Does the timeline hold? Check `tracking/timeline.md` if available.
- Are open threads from `tracking/threads.md` accounted for?

Flag: name variants, contradictory descriptions, timeline breaks, unresolved foreshadows that appear forgotten.

## Report Format

```md
## Review Report

Requested Mode: {mode}
Effective Mode: {mode}
Fallback: {reason or "none"}
Scope: {chapters N–M or "full manuscript"}

---

### Structure
{Problems found, with chapter numbers. Actionable fix per problem.}

### Opening Conversion (Chapters 1–3)
Chapter 1: {row-by-row PASS/FAIL plus exact evidence, including middle-density and action-translation rows}
Chapter 2: {row-by-row PASS/FAIL plus exact evidence}
Chapter 3: {row-by-row PASS/FAIL plus exact evidence}
Overall: {PASS/FAIL; a single hard failure makes the overall result FAIL}

### Character
Active cast: {N; pass/fail against 6–8 floor}
Lead-only chapters: {N}/{total} ({percentage}; pass/fail against 30% cap)
Ensemble-window failures: {rolling 3-chapter ranges}
Supporting-character causality: {appearance/action failures}
{Other problems found. Quote the offending dialogue or beat if possible.}

### Prose
AI Flavor: {Mild / Moderate / Severe}
Top patterns: {list}
Worst passages: {location + problem + fix direction}

### Consistency
{Problems found. Quote conflicting details if possible.}

---

### Priority Actions
1. {Highest-impact fix}
2. {Second fix}
3. {Third fix}

### Passed
{What is working well — brief, 3–5 items max.}
```

## What Review Does Not Do

- Does not rewrite prose (use `/story-deslop`)
- Does not generate new content
- Does not validate the story concept — only the execution

## Context Files to Read Before Reviewing

Read only the files relevant to the review scope:

```
Required (if they exist):
  tracking/threads.md                    — to check unresolved threads
  tracking/timeline.md                   — to check timeline coherence
  tracking/character-status.md           — to check character consistency

Load only if needed:
  world/characters/{character-name}.md   — if character voice/behavior is in question
  outline/outline.md                     — if structural pacing is in question
  reference/{book-title}/teardown.md     — if comparing against reference book standard
```
