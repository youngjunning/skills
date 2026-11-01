# Story Short Write

Load this reference when the user asks to write a short story or flash fiction.

**Genre-specific short form guidance** is in the relevant genre file — `genre-romance.md` (Romance Heat Level short form), `genre-mystery.md` (Mystery & Suspense short form), `genre-horror.md` (Short Form Horror), `genre-fantasy.md` (Short Form Fantasy), `genre-scifi.md` (Short Form Sci-Fi & Dystopian), `genre-drama.md` (Short Form Drama). Load the relevant genre file alongside this reference.

## Niche Research Input

Before writing a new short story, check `outputs/{site-slug}/{book-slug}/niche-research.json`:

- **Exists** → read `differentiation_angle`, `selected_tropes`, and `adsense_policy.high_risk_notes`. Anchor the emotional hook and twist to these.
- **Does not exist + user gave explicit genre/premise** → proceed directly.
- **Does not exist + no explicit brief** → run `fiction-niche-researcher.md` first, then return here.

## Core Principles

1. **Emotion before story**: Lock the target reader emotion before plotting. All structure serves that emotion.
2. **One twist, total commitment**: Every line of setup exists for the twist. No sub-plots, no world-building.
3. **Every sentence earns its place**: If a sentence doesn't advance plot, build toward the twist, or raise emotion — cut it.
4. **Opening 3 sentences are everything**: Hook or lose the reader. Ending creates shareability.
5. **Default first-person**: First-person narration creates the strongest reader identification in web fiction.

## Emotion Targets

Pick one before starting. The entire story structure flows from this choice.

| Target emotion | Best for | Difficulty | Market heat |
| --- | --- | --- | --- |
| Lingering regret | Romance, missed connection | Medium | High |
| Twist shock | Suspense, identity reversal | Hard | High |
| Cathartic release | Face-slapping, reversal of fortune | Easy | Medium |
| Healing warmth | Growth, family, friendship | Medium | Medium |
| Creeping dread | Psychological, suspense | Hard | Low-Medium |
| Resonant emotion | Realist, workplace, marriage | Medium | High |

## Writing Process

### Step 1: Lock the emotion and framework

Answer before writing any prose:

```
Target emotion: {choose one from the table above}
One-line premise: {protagonist + predicament + reversal + emotional landing}
Core twist: {one sentence}
Opening hook: {first 3 sentences — must contain suspense or conflict}
Closing echo: {final sentence — must have resonance or impact}
```

Save as `content/short/{story-title}/setup.md` from the project root.

### Step 2: Beat outline

Write a beat-level outline with section markers. Target 6–12 beats for 8,000–20,000 characters.

```md
### 1. Hook — {action/conflict that hooks immediately}
### 2. Setup — {introduce character situation, raise stakes}
### 3. Misdirection 1 — {first misdirection or setup detail}
### 4. Misdirection 2 — {second misdirection, tighten tension}
### 5. False resolution — {appears to resolve, but raises new question}
### 6. Twist — {the twist, from a single unambiguous moment}
### 7. Resonance — {emotional landing, last image or line}
```

For genre-specific beat structures (mystery investigation, horror, fantasy portal fiction, sci-fi/dystopian), load the relevant genre file.

Save as `content/short/{story-title}/beat-outline.md` from the project root.

### Step 3: Write prose

Write full prose section by section following the beat outline. Save all to `content/short/{story-title}/prose.md` from the project root.

Prose formatting:
- Adjacent paragraphs: blank line between them (`\n\n`). CommonMark collapses a single `\n` into a space — do not use single newlines between paragraphs.
- Dialogue: half-width double quotes `""`
- Section markers: `### 1.` / `### 2.` — consistent throughout
- No `……` or `——` — rewrite as action, short sentence, or line break

## Short Story Quality Checks

- Hook (first 3 sentences): contains a question, conflict, or unusual detail?
- Twist: arrives from setup, not from nowhere?
- Ending: has one image or line that lingers?
- No consecutive 3+ sentences with identical syntactic structure.
- Total word count: 8,000–20,000 characters for a self-contained short story.

## After Story Completion → Cover Generation (automatic, no prompt)

When the story passes quality checks, **immediately load `story-cover.md` and generate the cover** — do not ask the user whether to proceed. This is always the next step.

## Reference Book Integration

If the user has a reference book to emulate:

1. Read `{story-title}/reference/{book-title}/teardown.md` and `techniques.md`.
2. Extract: twist positioning, pacing of misdirection, sentence-level technique.
3. Add a brief "Reference Summary" section at the bottom of `setup.md`.
4. During Step 3, pull 1–2 specific techniques per section from the summary — do not copy, emulate.

If no reference exists, use the genre emotion table to select a structural template before writing.
