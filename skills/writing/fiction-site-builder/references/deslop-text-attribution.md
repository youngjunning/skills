> [MERGED] All rules from this skill have been integrated into `story-deslop.md`. Load `story-deslop.md` for runtime use — this file is attribution only.

---

# Attribution: deslop-text

**Source:** https://github.com/adamdunkels/deslop-text  
**Author:** Adam Dunkels  
**License:** (not specified — open source project)  
**Merged:** 2026-07-05  
**Merged into:** `story-deslop.md`

## Merge mapping

| deslop-text warning sign | Merged into |
|---|---|
| W9 — Paired adjectives with "yet"/"and" ("Simple yet powerful") | Gate A (new subsection) |
| W13 — Scare quotes (quotes for irony/emphasis, not actual quotations) | Gate A (new subsection) |
| W16 — "Whether you're X or Y" false inclusivity | Gate B type 4a (pedagogical hand-holding) |
| W19 — Repetitive "You" sentence starters (3+ consecutive) | Gate B type 11 (new) |
| W24 — Triple-value lists (three abstract virtues with no specifics) | Gate H (new subsection) |
| W26 — Uncontracted forms as stiffness signal | Gate H (new subsection) |
| W28 — Repetitive word use (local clustering + document saturation) | Implied in Gate D; noted in Article Quick Checks scoring |
| W29 — Sentence length uniformity (4+ sentences within 30% of mean) | Gate D (quantified version of existing rule) |
| W31 — Repeated thematic points (same idea restated multiple ways) | Gate H one-point dilution (merged with tropes.md concept) |
| W32 — Internet clichés ("hits different", "rent-free", "chef's kiss") | Gate A (new subsection) |
| W4 caveat — Exception for "Question? Answer." pairs | Gate B type 7 (rhetorical setups); exception noted |

## What was NOT merged (and why)

| Warning sign | Reason |
|---|---|
| W22 — Hashtag blocks | Not relevant; our articles don't append hashtags |
| W23 — Emoji as emphasis (rocket, fire, sparkle) | Not relevant; our articles don't use decorative emoji |
| W27 — Typographic quotes (curly vs straight) | Build pipeline handles encoding; not an authoring concern |
| W30 — Heading emoji (## 🚀 Getting Started) | Not relevant to our article or fiction format |
| W15 — "Excited to announce..." | Already covered in Gate B type 4 throat-clearing |
| W1, W2, W3, W5, W6, W7, W8, W10, W11, W17, W21, W25 | Already covered in existing Gates before this merge |

## When to re-check upstream

If adamdunkels/deslop-text adds new warning signs beyond W32, check for patterns not already in Gates A–H.

## Key distinctions from skill-deslop

deslop-text is more precise about thresholds:
- Em dashes: "one per document is fine; 3+ is a pattern" (our rule is stricter: remove all in copy)
- Rhetorical questions: "more than one per 500 words" — flag threshold
- Sentence length uniformity: specifically "4+ consecutive sentences within 30% of mean"
- Repetitive word: local (3+ in a paragraph) OR document (8+ per 2000 words)

These quantified thresholds have been incorporated into Gate D.

## Original 32 warning signs (summary)

**High severity:** W1 (filler phrases), W2 ("not X, it is Y"), W5 (marketing language), W6 (generic openings), W9 (paired adjectives), W15 (excited-to-announce), W16 (whether you're X or Y), W17 (faux-conversational pivots), W21 (corporate clichés), W24 (triple-value lists)

**Medium severity:** W3 (em-dashes), W4 (rhetorical questions), W7 (passive voice), W8 (hedging), W10 (meta-references), W11 (mechanical transitions), W12 (bold emphasis), W13 (scare quotes), W14 (section-end summaries), W18 (exclamation clusters), W19 (repetitive "You"), W22 (hashtags), W23 (emoji), W25 (corporate slang), W26 (uncontracted forms), W30 (heading emoji), W32 (internet clichés)

**Low severity:** W20 ("very"), W27 (typographic quotes), W28 (repetitive words), W29 (sentence length uniformity), W31 (repeated thematic points)
