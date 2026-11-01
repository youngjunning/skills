# Design System Planning

Use this reference before building any new UI or major redesign. Do the design plan first — do not skip to code.

---

## Step 0 — Design Read (Read the Room First)

Before any palette, font, or layout decision, state a one-line design read:

**"Reading this as: \<genre> fiction for \<audience>, with a \<vibe> language, leaning toward \<aesthetic family>."**

Examples:
- *"Reading this as: serialized web novel for mobile readers, with a clean modern language, leaning toward strong cover grid + restrained reader chrome."*
- *"Reading this as: literary short story collection for desktop readers, with a quiet editorial language, leaning toward typographic hierarchy + minimal UI chrome."*
- *"Reading this as: fantasy serial for CJK readers, with an atmospheric language, leaning toward warm amber palette + system CJK stack."*

If the brief is ambiguous, ask **one** clarifying question. If you can infer from genre, content language, or audience, declare the design read and proceed.

**Anti-default discipline:** Do not default to cream + terracotta + giant serif. Do not default to near-black + neon accent. Do not default to Inter everywhere. These are the LLM defaults for reading apps. Reach past them based on the design read.

---

## Step 1 — Fiction Dials

After the design read, set three dials. Every layout, motion, and density decision is gated by these.

| Dial | Range | Meaning |
| --- | --- | --- |
| `DESIGN_VARIANCE` | 1–10 | 1 = perfectly symmetrical, 10 = artsy chaos |
| `MOTION_INTENSITY` | 1–10 | 1 = static, 10 = cinematic physics |
| `VISUAL_DENSITY` | 1–10 | 1 = art gallery / airy, 10 = cockpit / packed |

**Fiction presets by page type:**

| Page | VARIANCE | MOTION | DENSITY | Rationale |
| --- | --- | --- | --- | --- |
| Reader page | 3–4 | 1–2 | 2–3 | Reading comfort overrides everything. No animation in the prose column. |
| Home / discovery | 6–7 | 3–4 | 3–4 | Enough visual energy to sell the genre; restrained enough to feel like a reading product. |
| Book detail | 5–6 | 2–3 | 3–4 | Genre atmosphere in cover and description; calm catalog. |

**Genre dial adjustments:**

| Genre | VARIANCE | MOTION | DENSITY |
| --- | --- | --- | --- |
| Literary / short story | 4–5 | 1–2 | 2–3 |
| Serialized web novel | 6–7 | 3–4 | 3–5 |
| Light novel / manga | 6–8 | 3–5 | 3–4 |
| Romance | 5–6 | 2–3 | 2–3 |
| Fantasy / historical | 5–6 | 2–3 | 2–3 |
| Thriller / mystery | 5–7 | 2–4 | 3–4 |

**Hard override:** The reader page MOTION dial is always capped at 2. No scroll animations, no entrance transitions, no infinite loops on the prose surface. Discovery pages may use motion; the reader page does not.

---

## Step 2 — Design Plan

Before writing any markup, decide the following and record them as `outputs/<site-slug>/design-brief.md`:

1. **Purpose** — What reading job does this site solve? (Serialized fiction discovery, CJK light novel reading, English short story collection, Spanish romance serial, etc.)
2. **Audience** — Casual web novel reader, serialized fiction subscriber, literary reader, language-learner, manga/manhwa crossover reader, etc.
3. **Tone** — Choose exactly one:
   - Refined editorial (calm, typographic, restrained)
   - Quiet literary (warm paper, minimal chrome)
   - Premium serialized fiction (strong cover grid, genre-forward)
   - Modern manga / light-novel adjacent (structured, character-art-friendly)
   - Warm personal library (bookshelf feel, cozy)
4. **Palette** — Define a theme for DaisyUI using 4–6 named token roles:
   - `base-100`: page background
   - `base-content`: body text
   - `muted`: secondary text and borders
   - `accent`: single genre-aware highlight
   - (optional) `base-200` / `base-300`: subtle surface variation for cards, navigation
5. **Type system** — Define three roles:
   - Display: for site title, book titles, chapter headings
   - Reader body: for prose — must be a highly readable serif or CJK system stack
   - UI/utility: for navigation, controls, metadata — system sans-serif
6. **Layout concept** — How do discovery, book detail, and reader layouts differ between H5 and desktop?
7. **Signature element** — One memorable detail connected to reading, books, chapters, or genre (see below).

**Two-pass process:** First, brainstorm the design plan in thinking. Then review it against the design read — if any part reads like the generic default you would produce for any similar genre, revise that part and say what changed. Only after confirming the relative uniqueness of the plan should you write code.

---

## Signature Element Rules

Spend all the distinctiveness in one place. A good signature element improves reader orientation, mood, or recognition — not decoration. Take one real aesthetic risk you can justify.

Examples that work:
- **Atmospheric detail hero** (web novel / romance / thriller): blurred, darkened, saturated cover fills the hero zone behind the crisp floating cover. See `ui-components.md` Book Detail Hero for implementation. This is the minimum quality bar for web novel builds.
- A chapter progress rail styled as a bookmark ribbon or page-edge marker.
- Book cover cards with a genre badge overlaid on the cover image (dark pill, top-right).
- A reader settings panel that slides in as a "reading lamp" side drawer.
- A "continue reading" card with a short chapter excerpt and a chapter-number marker.
- Desktop reader with a restrained antiquarian left margin rule (visual only, no interaction needed).
- Genre-specific cover accent systems (warm amber for romance, slate for thriller, moss for literary fiction).

Examples that fail:
- A decorative particle animation anywhere on the reader page.
- A split-panel hero with a large illustration above the book catalog.
- A typewriter animation on chapter titles.
- A floating "AI" badge or creation-process callout anywhere.
- Multiple signature elements. One is the rule.

If the signature element does not improve orientation or reading mood, remove it. Chanel's rule applies: before shipping, remove one decorative element you added.

---

## Genre-Specific Visual Direction

| Genre | Tone | Palette cue | Typography cue | Avoid |
| --- | --- | --- | --- | --- |
| Literary fiction | Quiet editorial | Warm paper, slate ink | Old-style serif display, comfortable body serif | Flashy gradients, web-novel genre tropes |
| Serialized web novel | Modern, energetic | Strong cover grid, one saturated accent | Clean sans display, readable body serif | Literary pretension, tiny cover cards |
| Light novel / manga | Character-forward | White or light base, single accent | Bold gothic display, system CJK body | Heavy drop shadows, overly dark backgrounds |
| Romance | Warm, personal | Dusty rose, warm sand, or mauve accent | Rounded serif or italic display face | Cool/corporate palettes |
| Fantasy / historical | Atmospheric | Warm amber, parchment, or deep navy | Humanist serif display, generous line height | Neon or high-saturation accents |
| Thriller / mystery | Taut, focused | Near-black base, single cold accent | High-contrast sans display, tight body | Warm/cozy palettes |
| Short story collection | Calm editorial | High contrast, minimal or no accent | Strong typographic hierarchy, no cover grid needed | Cover-grid layouts when there are no covers |

---

## Palette Guidance

Default to calm. The reader page inherits these tokens.

- `--base`: warm off-white (`#f9f6f1`), soft paper (`#faf8f4`), or light neutral (`#f8f8f6`). Never `#ffffff`.
- `--ink`: near-black (`#1a1814`), warm dark (`#1c1916`), or deep slate. Never `#000000`.
- `--muted`: warm gray for metadata, borders, placeholders. WCAG AA compliant against `--base`.
- `--accent`: one restrained color that fits the genre. Used 1–2 times per page. Never used as a background.
- `--night-base`: deep warm neutral (`#141210`) or cool dark (`#121416`). Never `#000000`.
- `--night-ink`: soft off-white (`#e8e4de`) or warm light. Never `#ffffff`.
- Sepia: `--sepia-base: #f2ead8`, `--sepia-ink: #3d3220`.

**Color Consistency Lock:** Once an accent color is chosen, it is used on the whole site. A warm-toned reader site does not suddenly get a blue chapter-nav CTA. Pick one accent, lock it, audit every component before shipping.

**Page Theme Lock:** The site has one theme (light, dark, or system). Sections do not flip between modes. The only exception is the reader page offering light / dark themes as a user preference, controlled by DaisyUI `data-theme` — not section-level overrides. Add sepia only when explicitly requested.

Avoid:
- Cream + terracotta + giant serif as a default for every brief — this is the LLM default for reading apps.
- Neon + near-black as a default "dark reading" treatment.
- Multiple accent colors. One accent per palette, used sparingly.
- Any pure `#000` / `#fff` in any theme.
- AI-purple gradients, glowing orbs, or frosted glass panels on the reader surface.

---

## Typography Guidance

Reader body typography matters more than display typography. Get body right before touching anything else.

**Display type:** System fonts only — no external font dependencies of any kind. Do not use `next/font/google`, `@fontsource`, or any self-hosted font packages. Good system serif choices for display: `Baskerville, "Palatino Linotype", Palatino, Georgia, serif` (dark/literary tone) or `Georgia, "Times New Roman", serif` (neutral). Avoid `Fraunces` and `Instrument Serif` — they are LLM default display serifs, deployed without thought. The site logo and headings must be legible and on-brand using the system font fallback chain alone.

**Reader body:** Use the system sans-serif stack for all scripts — zero load latency and native feel on every platform. `--font-reader: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`. Do not use serif system stacks (`Georgia`, `Times`) or self-hosted serif fonts for body prose — they increase perceived reading friction for social traffic audiences. The body face must hold up at 19px mobile with 1.8 line height for 500+ words at a time.

**UI/utility text:** `system-ui` stack for all controls, labels, and navigation. Never use display or body fonts for controls.

**Font choice discipline:**
- `Inter` is discouraged as the default UI font. Pick `Geist`, `Outfit`, or `system-ui` first.
- Never use decorative, handwritten, or novelty display fonts for chapter prose.
- Never apply letter-spacing to body or CJK text. Use it only on uppercase UI labels, sparingly.
- Serif is appropriate for literary/romance/fantasy reader bodies. For thriller, modern web-novel, or manga, a highly readable sans body may be more on-genre.
- If italic is used in display type with descenders (`y g j p q`), use `leading-[1.1]` minimum and add `pb-1` reserve on the wrapper.

**Typography carries personality.** The type treatment should be a memorable part of the design identity — not a neutral delivery vehicle for the content.

---

## Site Logo and Favicon

Never use placeholder text, generic emoji, or external icon libraries. Always generate real assets for launch.

### Entry check

**MANDATORY — run this bash command first. Do not skip it. Do not assume the result.**

```bash
[ -n "$APIYI_API_KEY" ] && echo "API_PATH=apiyi" || echo "API_PATH=skip"
```

**If the output is `API_PATH=apiyi` → you MUST use the apiyi curl path below.**

If the output is `API_PATH=skip` → print the warning below, then **skip logo/favicon generation and continue** (no SVG fallback — a dev placeholder holds the slot until a later pass):
```
\033[33m⚠ WARNING: APIYI_API_KEY is not set. Skipping logo/favicon generation (no SVG fallback).\033[0m
\033[33m  Assets require apiyi. Get an API key at:\033[0m
\033[33m  https://api.apiyi.com/register/?aff_code=ijv5\033[0m
\033[33m  Then set: export APIYI_API_KEY="your-key"\033[0m
```

### Two-variant logo system

Each site ships **two logo files** for automatic light/dark theme switching:

| File | Theme | Background | Use |
|---|---|---|---|
| `public/logo-light.png` | Light mode | White / plain | Visible on light backgrounds |
| `public/logo-dark.png` | Dark mode | Solid pure black, full square | Visible on dark backgrounds |

**Critical: never bake border-radius into the image.** Both files must be perfect squares with straight edges to all four corners. CSS controls `border-radius` at render time.

### Prompt rules

**logo-light prompt template:**
```
Flat vector logo icon: {genre-appropriate motif, e.g. "crescent moon embracing an open book"}.
{Motif color description — use the site's primary palette}.
Clean bold outlines, centered composition, white background, no rounded corners, square canvas.
```

**logo-dark prompt template:**
```
Flat vector logo icon: {same motif}.
{Bright/gold version of motif colors for dark background readability}.
Clean bold outlines, centered composition.
Solid pure black background filling the entire square canvas to all four edges. No rounded corners. Square edges only.
```

### apiyi path (APIYI_API_KEY is set)

Generate logo-light, logo-dark, and favicon via `doubao-seedream-5-0-260128`, falling through to `gpt-image-2-all` on failure. Do **not** use `nano-banana-pro` for logo/favicon. Logo requests are `1920x1920`; favicon requests are `1024x1024`. **Launch all as background processes then `wait`.**

```bash
mkdir -p public

gen_asset_apiyi() {
  local prompt="$1" out="$2" size="$3"
  local pj; pj=$(printf '%s' "$prompt" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read().strip()))')
  for model in "doubao-seedream-5-0-260128" "gpt-image-2-all"; do
    curl -s --max-time 300 https://api.apiyi.com/v1/images/generations \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $APIYI_API_KEY" \
      -d "{\"model\":\"$model\",\"prompt\":$pj,\"size\":\"$size\"}" \
    | OUT="$out" python3 -c "
import sys, json, base64, os, urllib.request
out = os.environ['OUT']
raw = sys.stdin.read()
if not raw.strip(): sys.exit(1)
data = json.loads(raw)
if 'error' in data or not data.get('data'): sys.exit(2)
item = data['data'][0]
if item.get('b64_json'):
    b = item['b64_json']; b = b.split(',',1)[1] if ',' in b else b
    open(out,'wb').write(base64.b64decode(b))
elif item.get('url'):
    urllib.request.urlretrieve(item['url'], out)
else: sys.exit(3)
" && return 0
  done
  return 1
}

# Fill in site-specific prompts before running
LOGO_LIGHT_PROMPT="{flat vector motif, colored, white background, square canvas, no rounded corners}"
LOGO_DARK_PROMPT="{flat vector motif, bright colors, solid pure black background edge-to-edge, square edges, no rounded corners}"
FAVICON_PROMPT="{same motif, ultra-simplified, high contrast, no text, readable at 32px}"

gen_asset_apiyi "$LOGO_LIGHT_PROMPT" public/logo-light_raw.png "1920x1920" && echo "logo-light saved" &
gen_asset_apiyi "$LOGO_DARK_PROMPT"  public/logo-dark_raw.png  "1920x1920" && echo "logo-dark saved"  &
gen_asset_apiyi "$FAVICON_PROMPT"    public/favicon_raw.png    "1024x1024" && echo "favicon saved"    &
wait

resize() { local src="$1" dst="$2" s="$3"
  [ -f "$src" ] && { ffmpeg -i "$src" -vf scale=${s}:${s} "$dst" -y 2>/dev/null \
    || sips -z $s $s "$src" --out "$dst"; }; }

resize public/logo-light_raw.png public/logo-light.png 512
resize public/logo-dark_raw.png  public/logo-dark.png  512
resize public/favicon_raw.png    public/favicon-32x32.png  256
resize public/favicon_raw.png    public/apple-touch-icon.png 180

command -v pngquant >/dev/null 2>&1 && for f in public/logo-light.png public/logo-dark.png public/favicon-32x32.png public/apple-touch-icon.png; do
  [ -f "$f" ] && pngquant --force --quality=80-95 --speed 1 --ext .png --skip-if-larger "$f" || true
done

rm -f public/logo-light_raw.png public/logo-dark_raw.png public/favicon_raw.png
```

### Theme-switching CSS

Add to `src/app/globals.css`:
```css
/* Logo theme switching */
.logo-dark { display: none; }
[data-theme$="-dark"] .logo-light { display: none; }
[data-theme$="-dark"] .logo-dark  { display: block; }
```

### Nav markup

In the site header/nav, render both images together:
```tsx
<img src="/logo-light.png" alt="site logo" width={32} height={32} className="logo-light rounded-lg" />
<img src="/logo-dark.png"  alt="site logo" width={32} height={32} className="logo-dark  rounded-lg" />
```

`rounded-lg` (or whatever radius fits the design) is applied via CSS — **never baked into the PNG**.

Wire up icons in `src/app/layout.tsx`:
```ts
export const metadata: Metadata = {
  icons: {
    icon: '/favicon-32x32.png',
    apple: '/apple-touch-icon.png',
  },
}
```

### No SVG fallback

There is **no SVG fallback** for logo/favicon. When `APIYI_API_KEY` is unset, or both models fail, **skip the asset and continue** — a dev placeholder holds the slot until a later generation pass. Never write `public/logo.svg`, `public/favicon.svg`, or `public/logo.png` as a fallback.

**Never ship a launched site with the default Next.js favicon or a missing logo** — but a skipped asset does not block the build; it is flagged for a follow-up pass.

---

## Typography Scale

```css
:root {
  /* size */
  --text-xs:   12px;   /* word count, metadata */
  --text-sm:   14px;   /* chapter nav labels, tags */
  --text-base: 17px;   /* reader body default (mobile) */
  --text-lg:   19px;   /* reader body large step */
  --text-xl:   22px;   /* chapter title */
  --text-2xl:  28px;   /* book title on detail page */
  --text-3xl:  36px;   /* site title / display */

  /* line height */
  --leading-tight:  1.4;
  --leading-reader: 1.75;  /* reader body default */
  --leading-loose:  2.0;   /* reader large line height */
  --leading-cjk:    1.9;   /* CJK default */
}
```

---

## Dark Mode Protocol

The reader page requires a dark mode toggle as a user-controlled preference, not OS-based switching. Discovery pages should support system dark mode via `prefers-color-scheme`.

The default implementation provides **light and dark** themes via DaisyUI. Add a third **sepia** theme only when the brief explicitly asks for it.

**Token strategy:** Use DaisyUI theme tokens (`base-100`, `base-content`, `accent`, etc.) for all color decisions. Swap the full theme under a `[data-theme]` attribute on `<html>` or the reader wrapper. Do not use Tailwind `dark:` classes for reader themes — they cannot handle three-way switching.

```js
// tailwind.config.js
plugins: [require('daisyui')],
daisyui: {
  themes: [
    { light: { 'base-100': '#f9f6f1', 'base-content': '#1a1814' } },
    { dark:  { 'base-100': '#141210', 'base-content': '#e8e4de' } },
  ],
}
```

**Contrast mandate:** WCAG AA minimum for body text (4.5:1) across all enabled themes. Test each theme before shipping. Do not ship a theme you have only seen in one mode.

**No pure extremes:** Off-black and off-white only. `#000000` and `#ffffff` kill depth and are banned in all themes.

---

## Motion Guidance

**Reader page:** No animations. No scroll effects. No entrance transitions. No infinite loops. Only permitted motion: theme-switch CSS transition (200ms), chapter-nav hover state (CSS only), settings panel slide-in (CSS only). Any JavaScript animation library is forbidden on the reader page.

**Discovery pages:** Motion is allowed when `MOTION_INTENSITY > 2` and the brief reads energetic (web novel, manga). Use Motion (`motion/react`) for scroll-reveal on cover grids and book cards. Use spring physics — no linear easing.

**Motion must be motivated.** Before adding any animation, ask: what does this communicate? Valid: hierarchy, storytelling, feedback, state change. Invalid: "it looked cool." Every animation needs a one-sentence justification.

**Reduced motion is mandatory.** Wrap all motion above intensity 2 in `prefers-reduced-motion` or `useReducedMotion()`. Infinite loops, scroll effects, and entrance transitions collapse to static under reduced motion.

**Forbidden patterns:**
- `window.addEventListener('scroll', ...)` — use Motion's `useScroll()` or IntersectionObserver.
- `useState` for continuous values (mouse position, scroll progress) — use `useMotionValue`.
- Typewriter animation on chapter titles. Particle effects on the reader surface. Parallax inside the prose column.

---

## AI-Tells Banned in Fiction UI

These are the patterns LLMs default to for reading-adjacent products. Avoid them unless the brief explicitly asks.

**Visual:**
- Gradient orbs, glowing blobs, frosted glass panels on the reader surface.
- Three equal feature cards in a row on the discovery page.
- Drop shadows heavier than `0 1px 4px rgba(0,0,0,0.08)`.
- Corner-radius inconsistency (pill buttons in a sharp-card layout).

**Typography:**
- `Inter` as the default body font without a reason.
- `Fraunces` or `Instrument Serif` as display fonts — the two most-reached-for LLM serif defaults.
- Decorative `letter-spacing` on body text.
- Mixed font families in chapter prose.

**Content and copy:**
- Em-dash (`—`) anywhere — headlines, body, attribution, labels, buttons, captions. Use a regular hyphen (`-`) or restructure the sentence. Zero em-dashes is the rule, not a guideline.
- "Jane Doe" / "John Smith" as author names. Use contextually appropriate, believable names.
- Section-numbering eyebrows (`001 · Chapters`, `02 / Catalog`) — name sections plainly.
- Generic placeholder text in chapter content. Fiction sites must have real prose before shipping.
- Any reader-visible copy mentioning AI, Markdown, parser, prompt, skill, or generation.

**Layout:**
- Discovery page that is just a stretched phone screen on desktop.
- Navigation that wraps to two lines at desktop viewport.
- Empty bento cells — N items means N cells, no blank tiles.
- Scrollcue labels (`Scroll ↓`, `Scroll to explore`) — readers know what scroll is.

---

## Interface Copy Rules

Copy must feel editorial and reader-side. Words in an interface are design material — bring the same intentionality to copy that you bring to spacing and color.

Write from the reader's side of the screen. Name things by what readers control and recognize, never by how the system is built. Describe what something does in plain terms. Use active voice. A control says exactly what happens when used.

| Avoid | Use instead |
| --- | --- |
| "Submit" | "Continue reading" |
| "Content management" | "Chapter list" |
| "Operation successful" | "Added to shelf" |
| "No data" | "No books yet. Add a title to start reading." |
| "AI generated" | (never say this) |
| "Powered by AI" | (never say this) |
| "Markdown" | (never say this) |
| "Loading..." | "Loading chapter…" or a skeleton screen |

Empty states must tell the reader what to do next, not just that a data structure is empty. Error messages explain what went wrong and how to fix it — they do not apologize.

Keep one copy register per site. Do not mix editorial prose, technical labels, and marketing punch in the same composition.

**Copy self-audit before shipping:** Re-read every visible string. Flag anything grammatically broken, unclear in referent, or that sounds like an LLM trying to sound thoughtful ("elegant nothing" phrases, mock-poetic micro-meta, passive-aggressive humility). Rewrite every flagged string. Boring-but-clear beats cute-but-wrong.

---

## Self-Critique Before Build

Before writing any markup, check:

- Does the design read match the genre and audience, or is it a generic reading-app default?
- Would this palette and layout work equally well on a finance dashboard? If yes, it is too generic — revise.
- Is the signature element connected to reading, books, chapters, or genre? If not, revise.
- Does anything on the reader page compete with comfortable prose reading? If yes, remove it.
- Does the desktop layout have its own logic, or is it just wider? If just wider, revise.
- Is the type system derived from the audience and genre, or from a generic design kit? If the latter, revise.
- Is there an em-dash (`—`) anywhere in the planned copy? Replace it now.

---

## Self-Critique After Build

After taking screenshots:

- Remove one decorative element that was added.
- Increase body text size or line height before adjusting any decorative details.
- Confirm the reader page is calmer and more focused than the home page.
- Confirm the first visible screen shows a usable reading product, not brand theater.
- Confirm no reader-visible copy mentions AI, tools, or implementation details.

---

## Pre-flight Checklist

Run every item before delivering. If any item fails, the output is not done.

**Design identity:**
- [ ] Design Read declared (one-line brief inference)?
- [ ] Dial values set and reasoned from the genre and brief?
- [ ] Signature element is exactly one, connected to reading?
- [ ] Palette is not the LLM default (cream + terracotta + giant serif)?
- [ ] Color Consistency Lock: one accent used identically across all pages?
- [ ] Page Theme Lock: no mid-page theme inversion between sections?

**Typography:**
- [ ] Display font is not `Fraunces` or `Instrument Serif` without explicit brand reason?
- [ ] Reader body is a high-readability serif or system CJK stack?
- [ ] Body text ≥ 17px mobile, ≥ 17px desktop?
- [ ] `letter-spacing` not applied to body or CJK text?
- [ ] Italic descender clearance: `leading-[1.1]` min + `pb-1` for display italic with `y g j p q`?

**Reader page:**
- [ ] No JavaScript animation library active on the reader page?
- [ ] No scroll effects, entrance transitions, or infinite loops in the prose column?
- [ ] Previous / next chapter navigation present and working?
- [ ] End-of-chapter "Next chapter" prompt visible at bottom of content?
- [ ] Reader background is not pure `#fff` or `#000`?
- [ ] Body text ≥ 17px mobile, contrast ≥ 4.5:1 against page background?
- [ ] Dark mode toggle present and persists in `localStorage`?
- [ ] Last visited chapter stored and surfaced on home/detail page?
- [ ] Light and dark themes implemented via DaisyUI `data-theme`? (required; verify WCAG AA for each)
- [ ] Sepia theme added only if the brief explicitly asks for it?

**Copy and content:**
- [ ] Zero em-dashes (`—` or `–`) anywhere visible to the reader?
- [ ] No reader-visible copy mentions AI, Markdown, prompt, or generation?
- [ ] No lorem ipsum or placeholder text in any chapter content?
- [ ] Copy self-audit passed: no grammatically broken or AI-hallucinated phrases?
- [ ] Empty states give the reader a next action, not just an error?

**Layout and structure:**
- [ ] Desktop is not a stretched phone layout — has its own layout logic?
- [ ] Navigation renders on one line at desktop, height ≤ 80px?
- [ ] No section-numbering eyebrows (`001 · Chapters`)?
- [ ] No scroll cue labels (`Scroll ↓`)?
- [ ] Required pages present: home / work list, book detail with chapter catalog, reader?

**Accessibility and performance:**
- [ ] WCAG AA (4.5:1) for body text in the default theme?
- [ ] `prefers-reduced-motion` respected for all motion above intensity 2?
- [ ] `<html lang>` set to the correct locale?
- [ ] Initial JS bundle under 200KB for a prototype?
- [ ] DaisyUI used for reader themes and UI components (not a separate CSS custom property token system)?
- [ ] Build errors and console errors absent on page load?
