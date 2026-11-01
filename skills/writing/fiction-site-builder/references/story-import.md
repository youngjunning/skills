# Story Import

Load this reference when the user wants to import an existing novel (partial or complete) into the standard project structure so it can be continued and published.

## Purpose

Reverse-engineer a user-provided manuscript into a complete writing project — `world/`, `outline/`, `chapters/`, `tracking/` — so that the story can be continued using `/story-long-write` or `/story-short-write`, and published using the fiction-site-builder pipeline.

The deliverable is a **writable project**, not just an analysis.

## Step 1: Confirm the Source

Ask the user:
1. Book title and source file path (or paste text directly)
2. Genre
3. Is the manuscript complete or partial? If partial, which chapter is the last?
4. Is the last chapter complete or a fragment?
5. Does the user want a full writable project (can continue writing) or just a structural analysis?

Auto-detect:
- Total chapter count and word count from the file
- Chapter delimiter format (e.g. `Chapter N`, `###`)
- Length classification (see below)

Confirm detections with the user before proceeding.

## Length Classification

| Signal | Long-form | Short-form |
| --- | --- | --- |
| Explicit chapter markers | Multiple discrete chapters | Single file or ≤3 chapters |
| Word count | >30,000 words | ≤30,000 words |
| User declaration | "long-form" / "novel" | "short-form" / "short story" |

User declaration overrides auto-detection. Confirm classification with the user.

## Step 2: Structural Analysis

### Long-form analysis

For each chapter (or sampled chapters for very long manuscripts):

1. Extract: chapter number, title, opening beat, closing beat, major events
2. Identify: recurring characters + their relationships
3. Map: foreshadows planted and resolved
4. Extract: world-building rules (geography, systems, factions)
5. Identify: the author's prose style signals (sentence length, dialogue density, rhythm patterns)

Output to:
```
{book-title}/reference/{book-title}/
├── teardown.md      — summary: arc structure, turning points, pacing
├── plot-beats.md    — beat-level chapter map
└── techniques.md    — prose technique, dialogue style, chapter hook patterns
```

### Short-form analysis

1. Identify the target emotion and the twist
2. Map setup beats and misdirection
3. Extract the hook sentence and the ending image
4. Identify prose techniques used

Output to `{story-title}/reference/{book-title}/` with same three files.

## Step 3: Build the Writing Project

After analysis, construct the writable project.

### Long-form project structure

```
content/{book-title}/
├── world/
│   ├── worldbuilding.md          — extracted from the manuscript
│   └── characters/{character-name}.md  — one file per major character
├── outline/
│   └── outline.md            — reconstructed arc outline (beat-level, chapter-referenced)
├── chapters/
│   ├── ch-001-{title}.md    — split from source, zero-padded
│   └── ...
├── reference/{book-title}/   — from Step 2 analysis
├── tracking/
│   ├── context.md           — last chapter's ending + open threads
│   ├── threads.md           — all open foreshadows with chapter references
│   ├── timeline.md          — inferred chronology
│   └── character-status.md  — character state at the end of the imported manuscript
└── resources/               # optional research files
```

### Short-form project structure

```
content/short/{story-title}/
├── setup.md               — emotion target + characters + world notes
├── beat-outline.md        — beat outline of the imported story
├── prose.md               — full prose
└── reference/{book-title}/  — from Step 2 analysis
```

## Chapter Splitting Rules (Long-form)

When the source is a single file with chapter markers:

1. Split on the chapter delimiter (detect from first occurrence)
2. Name each file `ch-NNN-{title}.md` — zero-pad to 3 digits minimum
3. Strip chapter headers from prose body (the filename carries the number)
4. Add frontmatter if chapter title is available:
   ```md
   ---
   title: "{chapter-title}"
   chapter: N
   ---
   ```
5. Preserve wording, punctuation, and paragraph boundaries during splitting, but normalize transport formatting before writing Markdown:
   - remove ASCII spaces, tabs, and full-width spaces accidentally used as paragraph indentation;
   - collapse any run of 2 or more consecutive blank lines to exactly 1 blank line;
   - never leave a body line indented by 4+ spaces, because Markdown will render it as a code block;
   - keep exactly one blank line between prose paragraphs and no blank-line padding at the start or end of the body.
6. Do not rewrite prose content during splitting — import as-is apart from the mechanical whitespace normalization above; deslop separately.
7. After splitting, run the language-specific chapter-length gate before publication. For English serial fiction, target 1,200–1,800 words, treat 1,800 as the normal upper limit, and split or compress every chapter above 3,200 words. Import preservation does not exempt a source chapter from this review; use a real scene turn, decision, consequence, or hook-out as the split point and preserve the causal chain.

### Duplicate Chapter File Cleanup

When `content/{book}/chapters/` contains multiple files mapping to the same chapter number, for example two files both starting with `ch-005`, keep only one.

Resolution priority:
1. Keep the file with more words; delete the shorter one.
2. If word counts are equal, keep the file whose frontmatter `chapter:` field matches the filename number, for example `chapter: 5` should not appear in `ch-003-xxx.md`.
3. If both are equal, keep the file with more complete content or a more descriptive title.

Detection command:

```bash
book="book-slug"
ls content/$book/chapters/ | sed 's/\(ch-[0-9]*\).*/\1/' | sort | uniq -d
```

For each duplicate pair, run `wc -w` on both files and delete the shorter version. No confirmation needed before deletion; the user reviews all changes via `git status` at wrap-up.

## Tracking File Reconstruction

`tracking/context.md` — write the last chapter's final beat and identify 2–3 open threads the next chapter must address.

`tracking/threads.md` — list all foreshadows found during analysis: what was planted, where, whether resolved.

`tracking/timeline.md` — reconstruct key timeline points (character ages, story days elapsed, seasonal markers).

`tracking/character-status.md` — for each major character: current location, emotional state, key relationships as of the last imported chapter.

## Post-Import Checklist

- [ ] All chapter files named with correct zero-padded numbers
- [ ] Body indentation is normalized: no accidental Markdown code blocks from leading whitespace
- [ ] Consecutive blank lines are collapsed to one, including after frontmatter and before chapter navigation
- [ ] A sample of early, middle, and final chapters renders as normal paragraphs with expected reading density
- [ ] `world/worldbuilding.md` contains enough to orient a writer continuing the story
- [ ] `outline/outline.md` shows where the story is and what is planned next
- [ ] `tracking/context.md` is ready to hand off to `/story-long-write`
- [ ] `tracking/threads.md` captures all unresolved threads
- [ ] Analysis assets in `reference/` (not deleted — they feed future writing decisions)

## What Import Does Not Do

- Does not edit or improve the imported prose (use `/story-deslop`)
- Does not review quality (use `/story-review`)
- Does not generate new chapters
- Does not modify the original source file
