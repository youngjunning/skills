# Joyally image

**A general-purpose GPT Image 2.6 AI image generation Skill** — usable from any Agent runtime that supports `SKILL.md`, or by reusing its scripts directly. Powered by [apiyi](https://api.apiyi.com/register/?aff_code=ijv5), using only GPT Image 2.6 at high quality through an OpenAI-compatible image API.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-blueviolet)](#)
[![apiyi](https://img.shields.io/badge/Powered_by-apiyi-orange)](https://api.apiyi.com/register/?aff_code=ijv5)

[English](#) · [中文](README.zh-CN.md)

---

## What It Does

Describe the request naturally in any Agent that has this Skill enabled:

```
Generate a cinematic portrait of a woman in a Tokyo street at night
Make a square logo for my app, dark theme, minimalist
Create 8 product images in parallel for my store
Make a RunCat-style menu bar sprite loop of a tiny robot running
Create a Codex-compatible pet: a plush lake otter with all 16 look directions
Create a Mac dynamic wallpaper of a deep-sea coral reef, with Light/Dark mode variants
Turn this technical article's architecture, dependency, and update-flow text blocks into real diagrams
Create a knowledge comic with connected panels, in-panel speech balloons, and phone-width review
```

The skill routes each image type to the right workflow, uses GPT Image 2.6 at high quality, post-processes output, and saves files to `~/Pictures/better-imagegen/`. Its [comic workflow](references/comics.md) owns storyboards, panel art, lettering, layout, and page review; the bundled [小界、小萌、小南 character references](references/comic-characters.md) include fullbody, halfbody, and avatar images for reuse when the story calls for them.

It also applies a prompt compliance layer before generation: prompts are normalized away from platform logos, exact in-image text, explicit content, graphic violence, and living-artist imitation so routine creative requests are less likely to be rejected accidentally.

---

## Model

| Model | Role | Notes |
|-------|------|-------|
| `gpt-image-2.6-sunburst` | Only model for generation and editing | Explicit `quality=high`; at most one same-model retry, then stop and report the error. Verification scope is in `references/apiyi.md`. |

**GPT size presets (16:9 tier):**

| Tier | Size |
|------|------|
| 1K   | 1280×720 |
| 2K   | 2048×1152 |
| 4K   | 3840×2160 |

Full model specifications and size constraints are in `references/apiyi.md`.

---

## Use Cases

| Request | Model | Output |
|---------|--------------|--------|
| Comic / knowledge comic | GPT Image 2.6 panel art + editable lettering and layout | Sequential page or vertical strip with storyboard, sources, and review notes |
| Knowledge map / architecture / lifecycle diagram | GPT backdrop + deterministic HTML/CSS/SVG | 3200×1800 PNG + WebP + layout-gate report |
| Portrait / illustration | GPT Image 2.6 | `.webp` q78, ≤ 300 KB |
| Logo / favicon | GPT Image 2.6 | `.png` (pngquant), ≤ 100 KB |
| Mac static wallpaper (4K) | GPT Image 2.6 | `wallpaper.png` (lossless PNG) |
| Mac dynamic wallpaper | GPT Image 2.6 per frame | `wallpaper-apr.heic` (2-frame, Light/Dark) |
| Sprite loop | GPT Image 2.6 | numbered PNG frames + `preview.gif` |
| Codex v2 pet | GPT Image 2.6 | 8×11 spritesheet + `pet.json` + QA artifacts |
| Batch (N images) | GPT Image 2.6 per image | N × `.webp`, generated in parallel |

---

## Technical Diagrams and Illustration Density

For structured knowledge maps, architecture diagrams, dependency graphs, build pipelines, release flows, and updater state machines, the image model generates only a restrained text-free backdrop. Every node, edge, arrow, label, legend, and lifecycle state is rendered deterministically with HTML/CSS/SVG so technical terminology and directionality stay exact.

Long technical articles get an illustration-opportunity audit before delivery. There is no maximum image count: a diagram is preferred whenever readers must understand three or more ordered steps, branches, ownership or runtime boundaries, dependency propagation, state transitions, rollback, or cross-module lifecycle differences. ASCII/TXT diagrams are content-model drafts, not final article assets. Executable commands, configuration, literal paths, and short copyable inventories remain code blocks.

Every deterministic diagram must pass the rendered-DOM layout gate before export or publication:

```bash
node scripts/validate_diagram_layout.mjs /absolute/path/diagram.html \
  --width 1600 --height 900 --min-gap 24 --boundary-clearance 16
```

The gate launches headless Chrome after fonts load and rejects overlapping cards, insufficient gutters, labels intersecting cards, edge paths crossing unrelated nodes, arrow markers crowding card borders or shadows, text touching or crossing a divider/rail, clipped text, canvas overflow, and missing layout annotations. Mark protected lines with `data-layout-boundary`, and mark nearby text groups with `data-layout-text`, `data-boundary-ref`, and `data-boundary-side`. For a horizontal stage diagram, add `--min-gap 80 --edge-clearance 20 --marker-clearance 20 --label-clearance 8 --min-edge-length 56 --max-marker-size 16`. Numeric success is followed by full-resolution and reduced-preview visual QA for layouts that technically do not overlap but still feel cramped.

---

## Mac Dynamic Wallpaper

Generates a 2-frame HEIC with `apple_desktop:apr` metadata — macOS switches frames automatically when Light/Dark mode is toggled in System Settings.

```
Make a dynamic wallpaper of mountains beneath a midnight starry sky
Make a dynamic wallpaper — underwater coral reef, day and night
```

**Requirements:** `"$BETTER_IMAGEGEN_PYTHON" -m pip install pillow-heif` (installed into the project `.venv`; bundles libheif, no Homebrew needed)

**Output:** `~/Pictures/better-imagegen/dynamic-wallpaper/wallpaper-apr.heic`

> macOS Sonoma note: time-based (h24) HEIC wallpapers no longer work — Apple migrated that format to a private `.madesktop` system. Light/Dark (apr) works fully.

---

## Sprite Loop

Use for RunCat-like frame animations, menu-bar status mascots, loading loops, and tiny app animations. The skill generates a sprite sheet, splits it into numbered PNG frames, writes `manifest.json`, and opens `preview.gif`.

**Output:** `~/Pictures/better-imagegen/sprite-loop/{name}/`

## Codex-Compatible Pets (Optional Target Format)

This is an optional adapter in the general pet-asset workflow, not a restriction on the skill. For Codex, it produces a `1536×2288` 8×11 v2 spritesheet, a `pet.json` with `spriteVersionNumber: 2`, 16 continuous look directions, and contact-sheet, motion, direction, chroma, and validation QA artifacts. It never auto-installs into any runtime directory; user-controlled installation and in-app verification remain outside the skill.

**Output:** `~/Pictures/better-imagegen/codex-pet/{pet-id}/`

---

## Output Convention

| Asset | Format | Location |
|-------|--------|----------|
| Cover / illustration | Lossy WebP q78 | `~/Pictures/better-imagegen/{name}.webp` |
| Mac static wallpaper | Lossless PNG | `~/Pictures/better-imagegen/wallpaper.png` |
| Mac dynamic wallpaper | 2-frame HEIC | `~/Pictures/better-imagegen/dynamic-wallpaper/wallpaper-apr.heic` |
| Sprite loop | PNG frames + preview GIF | `~/Pictures/better-imagegen/sprite-loop/{name}/` |
| Codex v2 pet | spritesheet + `pet.json` + QA artifacts | `~/Pictures/better-imagegen/codex-pet/{pet-id}/` |
| Logo | PNG (pngquant) | project-local |
| Metadata | JSON | alongside each image |

Intermediate PNGs are written to `/tmp/` and cleaned up after packaging.

---

## Setup

**1. Get an API key**

Register at [apiyi.com](https://api.apiyi.com/register/?aff_code=ijv5) — new accounts get free credits.

**2. Export the key**
```bash
export APIYI_API_KEY="your-key-here"
# Add to ~/.zshrc to persist across sessions
```

**3. Install it in your Agent's skill directory**
```bash
# Use the location and loading convention for your Agent runtime.
npx skills add youngjunning/skills --skill joyally-image -g
```

**4. Install the core local dependency**

Run the following command from the installed `joyally-image` directory shown by the installer:

```bash
eval "$(./scripts/ensure_venv.sh)"
# Dependencies are installed into this project's .venv, never global Python.
```

**5. (Dynamic wallpaper only)**
```bash
"$BETTER_IMAGEGEN_PYTHON" -m pip install pillow-heif
```

---

## File Structure

```
SKILL.md                      ← skill entry point & trigger rules
references/
  apiyi.md                    ← API auth, model specs, size constraints, error codes
  generation.md               ← API key check, model aliases, gen_image_apiyi, metadata helpers
  prompt-compliance.md        ← prompt normalization and rejection retry policy
  post-process.md             ← WebP conversion, resize, PNG compression
  portrait.md                 ← portraits, covers, banners, general single images
  knowledge-map.md            ← exact diagrams, illustration-density audit, mandatory layout gate
  high-allure.md              ← suggestive romance/editorial images
  logo-icon.md                ← transparent logos, icons, favicons, cutouts
  static-wallpaper.md         ← static wallpaper PNG pipeline
  dynamic-wallpaper.md        ← Mac dynamic wallpaper: generation + HEIC packaging
  sprite-loop.md              ← RunCat-like frame animation assets
  codex-pet.md                ← Codex v2 pets: 8×11 atlas, direction semantics, QA
scripts/
  validate_diagram_layout.mjs ← rendered-DOM overlap, gutter, edge-crossing, overflow gate
  test_validate_diagram_layout.mjs ← positive and negative regression cases
```

---

## License

MIT — see [LICENSE](LICENSE).
