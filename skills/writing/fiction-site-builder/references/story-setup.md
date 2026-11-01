# Story Setup

Load this reference when the user asks to set up a new writing project or initialize a fiction project directory.

## Niche Research Input

Before creating the project structure for a new book, check `outputs/{site-slug}/{book-slug}/niche-research.json`:

- **Exists** → read `selected_genre`, `selected_tropes`, `differentiation_angle`, and `producibility`. Record them in `tracking/context.md` as the story brief baseline.
- **Does not exist + user gave explicit genre/premise** → document them in `tracking/context.md` directly and proceed.
- **Does not exist + no explicit brief** → run `fiction-niche-researcher.md` first, then return here.

## Project Root Directory

Before creating any files, determine where the project lives:

- **Default**: create a new folder named after the site/project in the current working directory. Example: if the project is called "midnight-fable", create `./midnight-fable/` and work inside it.
- **Exception**: if the user explicitly says to use the current directory (e.g. "in this folder", "current directory", "here"), skip folder creation and treat `.` as the project root.

Never write files directly into the current directory unless the user explicitly requests it.

## Project Directory Structure

Long-form novel — place under `content/{book-title}/`:

```
content/{book-title}/
├── world/
│   ├── worldbuilding.md
│   ├── characters/
│   │   ├── {protagonist-name}.md
│   │   └── ...
│   └── map.md                 # optional
├── outline/
│   ├── outline.md             # full-book outline
│   └── arc-outlines/          # optional arc-level outlines
├── chapters/
│   ├── ch-001-{title}.md
│   ├── ch-002-{title}.md
│   └── ...
├── reference/
│   └── {reference-title}/
│       ├── teardown.md
│       ├── plot-beats.md
│       └── techniques.md
├── tracking/
│   ├── context.md             # running context for next chapter
│   ├── threads.md
│   ├── timeline.md
│   └── character-status.md
└── resources/                 # optional research
```

Short-form story — place under `content/short/{story-title}/`:

```
content/short/{story-title}/
├── setup.md                   # world + characters + emotion target
├── beat-outline.md            # beat-level outline
├── prose.md                   # all prose, single file
└── reference/                 # optional reference books
    └── {book-title}/
        ├── teardown.md
        └── techniques.md
```

## Naming Conventions

- Chapter files: `ch-NNN-{title}.md` — zero-padded to 3 digits minimum (`ch-001`, `ch-010`, `ch-100`)
- Chapter order: derived from filename sort — never rely on frontmatter order alone
- Book root: `content/{book-title}/` — use the book title as the directory name under `content/`
- Short stories: always under `content/short/{story-title}/`

## What the Site Reads vs. Ignores

| Directory | Reader sees it? |
| --- | --- |
| `chapters/ch-NNN-*.md` | Yes — chapter content |
| `public/covers/<book-title>.webp` | Yes — served as `/covers/<book-title>.webp` |
| `public/covers/<book-title>.json` | No — metadata for generation tracking only |
| `world/`, `outline/`, `tracking/`, `reference/`, `resources/` | Never — writing internals |

Never create routes or expose links to writing-internal directories.

## Initialization Checklist

**Before running any step below**, check whether the project already exists:

```bash
[ -f "content/*/world/worldbuilding.md" ] || ls content/*/world/worldbuilding.md 2>/dev/null
```

If `content/` already contains at least one book directory with non-empty files, **skip steps 1–6 entirely** and proceed directly to the writing phase. Re-running initialization on an existing project will overwrite `worldbuilding.md`, `outline.md`, and `tracking/context.md` with placeholder content, destroying the author's work.

When setting up a **new project** (no existing content):

1. Create the directory structure above with placeholder files.
2. Write a brief `world/worldbuilding.md` (3–5 bullet points: genre, setting, tone, core conflict).
3. Write `world/characters/{protagonist-name}.md` with role, motivation, voice notes.
4. Write `outline/outline.md` with a 10–30 beat arc outline.
5. Create `tracking/context.md` — starts empty; populated after each chapter.
6. Create `tracking/threads.md`, `tracking/timeline.md`, `tracking/character-status.md` — start empty.
7. If a reference book exists, run `/story-import` or manually create `reference/{book-title}/` files.

## .gitignore

Every site is its own git repo (registered as a submodule of the `fictions` parent). Write a `.gitignore` at the project root **before the initial commit** — build output, dependencies, generated collections, and local env must never be committed:

```gitignore
.next/
out/
node_modules/
.content-collections/
*.tsbuildinfo
.env.local
.DS_Store
```

- `.next/`, `out/` — Next.js build output
- `node_modules/` — dependencies (restored via `pnpm install`)
- `.content-collections/` — generated typed collections (rebuilt at `pnpm build`)
- `*.tsbuildinfo` — TypeScript incremental build cache
- `.env.local` — local secrets (e.g. `APIYI_API_KEY`); never commit
- `.DS_Store` — macOS Finder metadata

Chapter markdown under `content/` **is** committed — it is the source content, not build output.


## Writing Target

When building a fiction site from scratch, write **N books** in total, where N is the user-specified count (default 5 if not specified). Writing and site build run in parallel — site setup (stack, design, data) starts immediately after Phase 0 and does not wait for books to be written.

Each long-form novel must reach minimum content level before it can be included in the site build:
- At least 201 chapters per novel for launch (development preview may run with fewer while writing is in progress)
- ≥ 1,200 words per chapter

Run `/story-cover` to generate covers. This can run incrementally as books are completed, or in one batch before launch.

## Pre-Launch Gate

Verify all of the following before go-live:

- [ ] `content/` has ≥ 3 book directories.
- [ ] Each long-form novel has at least 201 chapters in `chapters/`. A smaller development preview is not launch-ready.
- [ ] Each chapter is ≥ 1,000 words (resolution chapters may be 1,000–1,400; other types target 1,200–1,800 — see Pacing Guidelines in `story-long-write.md`).
- [ ] `outline/outline.md` is non-empty for each book.
- [ ] `world/worldbuilding.md` is non-empty for each book.
- [ ] `tracking/context.md` populated for each book.
- [ ] Cover image generated for each book (A2): `public/covers/{book-title}.webp` for every book (flat path, no subfolders).
- [ ] Site logos generated (B2): `public/logo-light.png` and `public/logo-dark.png` (apiyi). No SVG fallback.
- [ ] Favicon generated (B2): `public/favicon-32x32.png` (apiyi). No SVG fallback.

These are launch requirements only — they do not block the development site build. Development preview may run without them.
