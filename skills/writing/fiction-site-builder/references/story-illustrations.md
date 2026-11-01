# Story Illustrations

Reference for Phase A2.5 — in-chapter illustration generation. Load only when the user explicitly requests illustrations in the current turn.

Default business rule: do not generate chapter illustrations automatically. Full pipeline, new-book creation, site build, cover refresh, and traffic-creative work all skip A2.5 unless the user explicitly says to generate illustrations.

**Execution principle: act autonomously. Do not surface "please run X" to the user. Identify peak scenes, insert markers, generate images, write files — then report what was produced.**

---

## What Illustrations Are (and Are Not)

**In-chapter illustrations** are full-width images embedded inside the chapter reader at the single highest-tension moment of a chapter. Romance illustrations use T3 or T4 tier — more intense than a standard cover (never used as ad creatives) but without the no-fabric extremity of T5. Non-romance books use the genre routing below instead of the allure-tier framework.

| Covers (A2) | Illustrations (A2.5) |
|---|---|
| T2 or T3 (randomly assigned per cover) | Romance: T3 or T4 (randomly assigned per illustration); non-romance: genre-routed |
| Hero image on book-detail and home pages | Embedded inside the chapter reader only |
| Scanned by ad-review crawlers | Never surfaced as an ad creative or meta-image |
| `public/covers/` | `public/illustrations/` |
| One per book | exactly 5 per book |

**T5 is never used for illustrations.** T5's no-fabric dorsal composition is too sparse as an inline scene image — it reads as a standalone art piece, not as a chapter moment. T3 and T4 produce more scene-grounded, immersive results.

**Romance tier assignment per illustration:** randomly pick T3 or T4 independently for each illustration in the book. This produces variety across the novel — some peak moments are charged-but-clothed (T3), others are post-decision (T4). Do not use the same tier for all illustrations in a book.

---

## §0 Floor Remains Absolute

§0 applies to illustrations — see `cover-allure-elements.md §0`. Tier does not relax the floor.

---

## Budget: Exactly 5 Illustrations Per Book

Place illustrations at the **highest-stakes dramatic peaks** of the novel — exactly 5 per book, no more. Cost of generation is real; every slot must earn it.

**Never add a 6th illustration.** If a scene doesn't earn a slot, leave that slot empty rather than adding a 6th mediocre image. 5 well-placed illustrations outperform 7 scattered ones.

---

## Genre Routing

The illustration framework differs by genre. Before selecting scenes, run the **Genre Allure Routing** table in `cover-allure-elements.md`.

**Default Allure Genres** and qualifying **Conditional Allure Genres** use the allure-tier system below (T3/T4) — peak scenes are intimacy, claim, temptation, possession, forbidden attraction, or relationship point-of-no-return scenes. Prompts use `cover-allure-elements.md` assembly blocks.

Qualifying examples include romance, Contemporary/Billionaire/Mafia Romance, Paranormal/Shifter/Vampire/Demon/Monster Romance, Romantasy/Fae/Fantasy Romance, Gothic Romance, Historical/Regency Romance, Sports Romance, Dark Academia Romance, and romance-coded thriller/fantasy/sci-fi subgenres.

**Non-allure genres** use the genre-specific sections at the bottom of this file instead of the T3/T4 system:
- Mystery / Cosy Mystery / Literary Thriller → §Genre: Mystery
- Horror → §Genre: Horror
- Fantasy without central adult attraction → §Genre: Fantasy
- Sci-Fi / Dystopian without central adult attraction → §Genre: Sci-Fi
- Contemporary Drama / Family Drama / Medical Drama without romance as the hook → §Genre: Drama

For non-allure genres: the §0 floor still applies (no explicit sexual content), but the allure-tier framework, T3/T4 assembly blocks, and all risqué-allure guidance do not apply. Skip §Peak Scene Selection through §Prompt Construction and go directly to the relevant genre section.

---

## Peak Scene Selection (Romance)

Read `content/{book-slug}/outline/outline.md` and `content/{book-slug}/tracking/context.md` to identify candidate scenes. Use these criteria:

### Placement rule — 5 primary slots

Illustrations must be **evenly distributed** across the novel. For a book with N chapters, divide into 5 equal zones and target exactly one illustration per zone. Stop at 5 — never exceed it.

| Slot | Target range | What to look for |
|---|---|---|
| **S1 — Opening hook** | chapters 2 – ⌊N×0.2⌋ | First charged encounter; first moment of undeniable attraction; the scene that hooks the reader to the relationship |
| **S2 — Rising tension** | chapters ⌊N×0.2⌋+1 – ⌊N×0.4⌋ | First deliberate touch; the moment the leads stop pretending; early push-pull moment |
| **S3 — Midpoint shift** | chapters ⌊N×0.4⌋+1 – ⌊N×0.6⌋ | Emotional turning point; a confession or betrayal that resets the relationship; the moment the protagonist stops fighting |
| **S4 — Late tension** | chapters ⌊N×0.6⌋+1 – ⌊N×0.8⌋ | Intimacy escalates; a secret revealed through closeness; near-climax; the decision point |
| **S5 — Climax** | chapters ⌊N×0.8⌋+1 – N−1 | The scene readers came for; point of no return; final surrender |

**Never place two illustrations within 3 chapters of each other.** If no qualifying scene exists in a slot, leave that slot empty — do not add a scene that doesn't earn it, and do not replace the empty slot with a 6th illustration elsewhere.

### Qualifying peak types (one per slot)

| Peak type | Description | Example moment |
|---|---|---|
| **Breaking point** | The scene where the protagonist's resistance finally collapses — emotional surrender | "She stopped pretending she didn't want this" |
| **First consummation** | First physical union between leads — regardless of how explicit the prose is | The moment they cross from tension to action |
| **Point of no return** | A decision that changes both characters irrevocably | A confession, a choice, a truth revealed through intimacy |
| **Climactic peak** | The highest-tension scene in the book — the scene readers came for | Final confrontation that resolves into surrender |

### Disqualifying conditions (skip the scene)

- Chapter is still building tension — the peak hasn't landed yet
- Scene is plot-focused (fight, reveal, travel) without intimacy **[Romance only — for other genres, plot-focused scenes ARE the qualifying scenes; see §Genre Routing]**
- Scene has already been illustrated in this book (no two illustrations within 2 chapters of each other)
- Fewer than 3 chapters remain after this scene (end-of-book illustrations feel anticlimactic)

---

## Marker Placement

Once you select a peak scene, insert the marker **immediately before the peak line** inside the chapter `.md` file:

```markdown
She had been trying to say something rational, something that would stop this, but every
word dissolved before it reached her mouth.

<!-- ILLUSTRATION -->

He reached for her then, and she stopped pretending.
```

**One marker per chapter. Maximum one marker per 2 consecutive chapters.**

The site renderer splits chapter content on this marker and renders `IllustrationBlock` at that position.

---

## File Convention

```
public/
  illustrations/
    {book-slug}/
      ch-{NNN}.webp     # e.g. ch-007.webp — matches chapter file ch-007-*
      ch-{NNN}.json     # metadata: model, size, prompt (all in one file)
```

- `{book-slug}` matches the `content/{book-slug}/` directory name
- `{NNN}` is the zero-padded chapter number from the chapter filename (`ch-007-title.md` → `ch-007.webp`)
- Always shipped as lossy **WebP q72**, always a single file per illustrated chapter (the PNG straight from the model is the intermediate; the WebP is the deliverable)
- JSON format matches cover convention: `{"model": "...", "size": "...", "prompt": "..."}`
- Write the JSON immediately after saving the PNG — never use a separate `.prompt.txt` file

---

## Prompt Construction (Romance)

Illustration prompts differ from cover prompts in three ways:
1. No title, author, or text overlay instructions
2. Replace "book cover" framing with "intimate scene illustration" framing
3. Include scene-specific context (location, body position, emotional beat from the actual prose) — but **not** the literal wardrobe; garment state always comes from the tier (see mistake #2 below)

> ### ⚠️ The narrative event is the point — do not write a generic "emotional" scene
>
> An illustration at T3/T4 must first be a **readable dramatic tableau**: irreversible event, visual proof, distinct reaction, and clear hierarchy. Use skin/garment exposure only when it intensifies that exact event. A plot-faithful but visually modest frame is valid if it has stronger story legibility than a generic intimate pose. The single hard limit is the **§0 floor** (no visible nipples/areola/genitals, no sex acts).
>
> Three mistakes that produced tame output in the past (all banned):
> 1. **Writing a tier *label* instead of pulling the tier *block*.** `T4 intensity: a deliberate first kiss, deeper emotional intimacy` is NOT a T4 prompt — it describes a feeling, not an image. You MUST copy the actual T3/T4 assembly block (clothing-state + skin-zones + fabric-behavior vocabulary) from `cover-allure-elements.md`.
> 2. **Letting the prose's literal costume win.** If the prose says she wears an "oversized sweater" or "practical layered clothing," that does **not** carry into the image. The tier's clothing-state spec **replaces** the literal costume — re-cast the garment to the tier (rain-soaked clinging silk, fallen panels, nominal drape) with a plausible in-scene reason. Keep the *location, body position, and emotional beat* from the prose; re-dress the characters to the tier.
> 3. **Adding suppressive negatives.** Never write `fully clothed`, `no nudity`, `modest`, `tasteful`, or `no explicit content` into an illustration prompt. The only constraint is the §0 floor, expressed the §0 way (covered by fabric edge / shadow / body position) — never as a blanket "clothed" instruction, which collapses the image to ~T0.

### Step 1 — Randomly assign tier and pull the assembly block

For each romance illustration, randomly pick **T3 or T4**. Do not use the same tier for every illustration in a single book.

**Copy the corresponding assembly block from `cover-allure-elements.md` verbatim as the spine of the prompt** — do not paraphrase it into a one-line "intensity" description:

- **T3 assembly block** (garment failing — torn/wet/clinging, charged anticipation, surrender-imminent; apply the validated techniques: fabric departure, two-panel deep V, body arch + barely-containing, rim light on silhouette)
- **T4 assembly block** (clothing has left, one nominal drape remains, maximum skin zones, post-decision emotional register)

**Never use T5 for illustrations.** **Never downgrade the block's clothing/skin language to fit the prose's literal wardrobe — re-dress the scene to the tier (see mistake #2 above).**

### Step 2 — Add character anchors from `character-visuals.md` (canonical source)

**Read `content/{book-slug}/world/character-visuals.md`** — this is the canonical visual sheet written during A2 (cover generation). If it does not exist, generate it now using the same Step 1.1 procedure in `story-cover.md`, then write it before continuing.

Copy the descriptors **verbatim** from the sheet into the prompt — do not paraphrase:
```
{female-lead: Ethnicity phrase, Hair phrase, Eyes phrase, Signature phrase from character-visuals.md}
{male-lead: Ethnicity phrase, Hair phrase, Build phrase, Signature phrase from character-visuals.md}
```

Keep this to 3–4 keywords per character — copy the exact wording, not a summary. Consistent phrasing across cover and all illustrations is what produces visual continuity. Never re-derive or re-describe characters from scratch.

**Hard rule:** one novel's illustrations must look like the same cast as its cover. Do not change a character's race, age band, hair color, hair length, body type, facial structure, or signature status marker between cover and illustration. If the cover shows a major supporting character, that character's illustration appearances must preserve the same visual identity. A beautiful but different-looking lead is a failed illustration.

### Step 3 — Add scene-specific context

Replace the generic cover environment with the chapter's actual setting:
```
{location from prose: e.g. "rain-soaked apartment, single lamp on the floor"}
{specific body position or gesture from the prose that triggered the marker placement}
```

**Narrative-tableau requirement:** Treat the illustration as a frozen short-drama frame. Include one irreversible beat, one visible proof object or social witness, and one readable reaction. Examples: the wedding stops around an impossible condition; she reads the document while he stands behind her; an ex sees her leave with someone new; a family member realizes who her ally is. Do not render an attractive couple merely standing in a beautiful room — the still must make viewers infer what happened immediately before and fear what follows.

For romance tableau scenes, also pull a distinct performance beat for each visible character from `cover-allure-elements.md` §"Performance Direction". Explicitly state face direction, hand action, and relative height/position; "emotional" or "dramatic" alone is not enough for a model to direct the scene.

### Step 4 — Add illustration framing

Append at the end:
```
cinematic drama still, prestige streaming series cinematography, film-still from a high-budget production, real human skin and hair and faces, NO anime, NO cartoon, NO illustration, NO digital painting, NO CGI, intimate scene, warm cinematic palette, no text, no title, no watermark
```

### Complete example (T4)

```
white silk sheet corner barely draped across her hip — entire bare back from nape to the curve of her spine,
long bare legs from hip to foot, her shoulder at his jaw. His bare chest her only backdrop, skin to skin
from shoulder to hip, no fabric between them anywhere. Ultra-tight crop: skin fills the frame, background
gone to warm amber abstraction. Single candle the only light source.
Her expression: not surrender but arrival — eyes closed, the look of someone who stopped fighting and found
it was right. His: certain, possessive, the question was always already answered.
[female-lead: black hair loose, almond eyes, warm skin tone]
[male-lead: broad shoulders, sharp jaw, dark hair, lit from one side]
Scene: luxury hotel suite after midnight, single bedside lamp, city lights blurred beyond the window.
She had reached for his hand to push him away and found herself pulling him closer instead.
intimate scene illustration, painterly warm palette, soft editorial romance art, no text, no title, no watermark
```

---

## Generation — A2.5 Execution Steps

### A2.5-1: Select peak scenes

For each book being illustrated:
1. Read `content/{book-slug}/outline/outline.md`
2. Read `content/{book-slug}/tracking/context.md`
3. Identify 1–3 chapters meeting the peak criteria above
4. Record: chapter filename, the exact prose line immediately after which the marker goes

### A2.5-2: Insert markers

For each selected chapter, insert `<!-- ILLUSTRATION -->` at the correct position. Commit the chapter files after all markers are inserted.

### A2.5-3: Generate images

Use inline curl — same pattern as cover generation (`story-cover.md`). **Do NOT use `/tmp/gen_cover_model.py`** — that script is for model capability testing only (`tests/image-model-tests/`), never for production asset generation.

```bash
gen_illus_apiyi() {
  local model="$1" size="$2" output_path="$3"
  local prompt_json
  prompt_json=$(printf '%s' "$PROMPT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))')
  curl -s --max-time 300 https://api.apiyi.com/v1/images/generations \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $APIYI_API_KEY" \
    -d "{\"model\":\"$model\",\"prompt\":$prompt_json,\"size\":\"$size\"}" \
  | OUTPUT_PATH="$output_path" python3 -c "
import sys, json, base64, os, urllib.request
output_path = os.environ['OUTPUT_PATH']
raw = sys.stdin.read()
if not raw.strip(): print('ERROR: empty response'); sys.exit(1)
data = json.loads(raw)
if 'error' in data:
    msg = data['error']['message'] if isinstance(data['error'], dict) else str(data['error'])
    print('API_ERROR:' + msg); sys.exit(2)
if not data.get('data'): print('SOFT_REJECT'); sys.exit(2)
item = data['data'][0]
if item.get('b64_json'):
    b64 = item['b64_json']
    if ',' in b64: b64 = b64.split(',', 1)[1]
    with open(output_path, 'wb') as f: f.write(base64.b64decode(b64))
elif item.get('url'):
    urllib.request.urlretrieve(item['url'], output_path)
else:
    print('UNKNOWN_FORMAT'); sys.exit(3)
print('SAVED:' + str(os.path.getsize(output_path)))
"
}
```

**Model routing for illustrations (final target: ~664×996 display, file ≤ 300 KB):**

| Tier | Primary | Fallback |
|---|---|---|
| T3 | `gpt-image-2-all` `848x1280` | `gpt-image-2-all` `848x1280` → retry once → `doubao-seedream-5-0-260128` `1664x2496` |
| T4 | `gpt-image-2-all` `848x1280` | `gpt-image-2-all` `848x1280` → retry once → `doubao-seedream-5-0-260128` `1664x2496` |

- gpt-image-2-all: **preferred primary**. 848×1280 output. Stricter content filter (hard-rejects T3/T4 fabric-failure language); when rejected, soften prompt and retry once before falling back.
- doubao-seedream-5-0-260128: fallback when gpt-image-2-all fails twice. Requires 1664×2496 pixel floor; stochastic rejection → retry once; stamps `AI生成` watermark → crop bottom ~7% post-generation.
- On second rejection: soften prompt per `cover-allure-elements.md` safe-wording rules, then use nano as blank-prevention.
- nano: silently downgrades T3+ to ~T1 — use as-is (blank-prevention only).

**Run all illustrations in parallel** — one background process per illustration across all books, then a single `wait`:

```bash
OUTDIR="public/illustrations/{book-slug}"
mkdir -p "$OUTDIR"

(
  OUTPUT="$OUTDIR/ch-{NNN}.png"   # intermediate — post-process (A2.5-4) resizes then converts to ch-{NNN}.webp
  if   gen_illus_apiyi "gpt-image-2-all"            "848x1280"  "$OUTPUT"; then MODEL_USED="gpt-image-2-all"; SIZE="848x1280"
  elif gen_illus_apiyi "gpt-image-2-all"            "848x1280"  "$OUTPUT"; then MODEL_USED="gpt-image-2-all"; SIZE="848x1280"  # retry once
  elif gen_illus_apiyi "doubao-seedream-5-0-260128" "1664x2496" "$OUTPUT"; then MODEL_USED="doubao-seedream-5-0-260128"; SIZE="1664x2496"
  elif gen_illus_apiyi "nano-banana-pro"            "1024x1024" "$OUTPUT"; then MODEL_USED="nano-banana-pro"; SIZE="1024x1024"
  else echo "ALL_FAILED ch-{NNN}"; exit 0; fi
  # Write metadata JSON
  PROMPT_JSON=$(printf '%s' "$PROMPT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))')
  printf '{"model":"%s","size":"%s","prompt":%s}\n' "$MODEL_USED" "$SIZE" "$PROMPT_JSON" \
    > "$OUTDIR/ch-{NNN}.json"
) > /tmp/illus_{book-slug}_ch{NNN}.log 2>&1 &

# repeat for every chapter across every book...

wait
rm -f /tmp/illus_*.log
```

### A2.5-4: Post-process

**Target dimensions and file size:** every illustration should end at **664×996** (display 2:3), shipped as lossy **WebP q72**, ≤ 300 KB on disk. Resize/crop first with `sips` on the PNG, then convert the final PNG to WebP q72 (prefer `cwebp`, fall back to Pillow). The `.png` is the intermediate; the `.webp` is the deliverable.

```bash
# Resize/crop a PNG (in place) → final ch-{NNN}.webp at q72. Prefer cwebp; fall back to Pillow.
# If the WebP output is larger than the source PNG, discard it and keep the PNG renamed to .webp.
to_webp_illus() {
  local src="$1" dst="$2" q="${3:-72}"
  local before after
  before=$(stat -f%z "$src" 2>/dev/null || stat -c%s "$src")
  if command -v cwebp &>/dev/null; then
    cwebp -quiet -q "$q" "$src" -o "$dst"
  else
    python3 -c "from PIL import Image; im=Image.open('$src'); im.save('$dst','webp',quality=$q,method=6)"
  fi
  after=$(stat -f%z "$dst" 2>/dev/null || stat -c%s "$dst")
  if [ "$after" -ge "$before" ]; then
    rm -f "$dst"
    cp "$src" "$dst"
    echo "⚠ webp larger than src (${after}B ≥ ${before}B) — kept original"
  fi
}
```

**If model was `gpt-image-2-all`:** output is already 848×1280 PNG. Resize to 664×996, then convert:

```bash
sips -z 996 664 input.png --out input.png
to_webp_illus input.png "ch-${NNN}.webp" 78
```

**If model was `doubao-seedream-5-0-260128`:** crop watermark, resize, then convert:

```bash
# $w and $h are the original dimensions after download (usually 1664 x 2496 or close)
sips -c $((h * 93 / 100)) $w input.png --out input.png   # crop ~7% from bottom
sips -z 996 664 input.png --out input.png                 # resize to 664x996
to_webp_illus input.png "ch-${NNN}.webp" 78
```

**If model was `nano-banana-pro`:** crop square to 2:3, resize, then convert:

```bash
sips -c 1024 683 input.png --out input.png   # → 683×1024 (2:3), centered
sips -z 996 664 input.png --out input.png    # → 664×996
to_webp_illus input.png "ch-${NNN}.webp" 78
```

**Never use lossless WebP** — on photographic art it is larger than the source PNG. Always lossy q72.

**Verify and report**

After cropping/converting each file, check:
- Final `.webp` width is 664 px, height 996 px
- File size ≤ 300 KB
- Watermark is gone (doubao) — if still visible, increase bottom crop to ~10%
- Character continuity matches the cover: same lead(s), same major supporting character(s), same core hair/face/build/status markers. Reject and regenerate any illustration that swaps identities or makes the cast look unrelated to the cover.

If a file exceeds 300 KB, lower the WebP quality to ~72 and re-convert.

---

## Site Integration

When building the site (B4), implement `IllustrationBlock` and wire it into the chapter renderer.

### IllustrationBlock component

`IllustrationBlock` is a server component that checks file existence, then delegates rendering to `LightboxImage` (a client component). This composition keeps the server-side `existsSync` out of the client bundle while enabling interactive lightbox/download.

```tsx
// src/components/LightboxImage.tsx
'use client'

import { useState, useEffect, useCallback } from 'react'

interface Props {
  src: string
  alt: string
  width?: number
  height?: number
  className?: string
  style?: React.CSSProperties
  loading?: 'lazy' | 'eager'
}

export default function LightboxImage({ src, alt, width, height, className, style, loading = 'lazy' }: Props) {
  const [open, setOpen] = useState(false)
  const close = useCallback(() => setOpen(false), [])

  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') close() }
    document.addEventListener('keydown', onKey)
    document.body.style.overflow = 'hidden'
    return () => { document.removeEventListener('keydown', onKey); document.body.style.overflow = '' }
  }, [open, close])

  async function download() {
    try {
      const res = await fetch(src)
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = src.split('/').pop() ?? 'image.png'
      a.click()
      URL.revokeObjectURL(url)
    } catch { window.open(src, '_blank') }
  }

  return (
    <>
      <img src={src} alt={alt} width={width} height={height}
        className={`lb-trigger${className ? ` ${className}` : ''}`}
        style={style} loading={loading} onClick={() => setOpen(true)} />
      {open && (
        <div className="lb-overlay" onClick={e => { if (e.target === e.currentTarget) close() }}>
          <div className="lb-box">
            <div className="lb-toolbar">
              <button className="lb-btn" onClick={download} aria-label="Save image">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
              </button>
              <button className="lb-btn" onClick={close} aria-label="Close">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>
            <img src={src} alt={alt} className="lb-img" />
          </div>
        </div>
      )}
    </>
  )
}
```

```tsx
// src/components/IllustrationBlock.tsx
import { existsSync } from 'fs'
import { join } from 'path'
import LightboxImage from './LightboxImage'

interface Props {
  bookSlug: string
  chapterNum: string   // zero-padded: "007"
}

export default function IllustrationBlock({ bookSlug, chapterNum }: Props) {
  const filePath = join(process.cwd(), 'public', 'illustrations', bookSlug, `ch-${chapterNum}.webp`)
  if (!existsSync(filePath)) return null

  return (
    <figure className="illustration-block">
      <LightboxImage
        src={`/illustrations/${bookSlug}/ch-${chapterNum}.webp`}
        alt=""
        width={664}
        height={996}
        className="illustration-img"
      />
    </figure>
  )
}
```

```css
/* global styles */
.illustration-block {
  margin: 2.5rem 0;
  padding: 0 2rem;   /* horizontal padding — image never full-bleed */
  text-align: center;
}
.illustration-img {
  width: 100%;
  max-width: 400px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.18);
}

/* Lightbox */
.lb-trigger { cursor: zoom-in; }
.lb-overlay {
  position: fixed; inset: 0; z-index: 9999;
  background: rgba(0,0,0,.85);
  backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
  display: flex; align-items: center; justify-content: center;
  padding: 20px; animation: lb-in .2s ease;
}
@keyframes lb-in { from { opacity: 0 } to { opacity: 1 } }
.lb-box { display: flex; flex-direction: column; align-items: flex-end; gap: 10px; max-width: min(90vw, 800px); }
.lb-toolbar { display: flex; gap: 8px; }
.lb-btn {
  display: flex; align-items: center; justify-content: center;
  width: 36px; height: 36px; border-radius: 50%;
  background: rgba(255,255,255,.12); border: none; cursor: pointer; color: #fff; transition: background .15s;
}
.lb-btn:hover { background: rgba(255,255,255,.24); }
.lb-img {
  max-width: 100%; max-height: calc(90vh - 60px);
  border-radius: 10px; object-fit: contain;
  box-shadow: 0 24px 80px rgba(0,0,0,.6); animation: lb-scale-in .2s ease;
}
@keyframes lb-scale-in { from { transform: scale(.94); opacity: 0 } to { transform: scale(1); opacity: 1 } }
```

### Chapter renderer split

In the chapter page component, split chapter body on the marker and insert `IllustrationBlock` at the split point. The split must integrate with any existing ad-interleaving logic — the `before` half goes through the existing paragraph-split/ad loop; the `after` half renders as a single block after the illustration.

```tsx
// src/app/book/[slug]/chapter/[n]/page.tsx (integration pattern)
import IllustrationBlock from '@/components/IllustrationBlock'

// Inside the page component, before the JSX return:
const chapterNum = String(chapter.order).padStart(3, '0')
const ILLUSTRATION_MARKER = '<!-- ILLUSTRATION -->'
const hasIllustration = chapter.content.includes(ILLUSTRATION_MARKER)
const [mainContent, afterIllustration] = hasIllustration
  ? chapter.content.split(ILLUSTRATION_MARKER)
  : [chapter.content, '']
const contentParts = splitContent(mainContent)  // existing paragraph-split function

// In the JSX, after the existing content/ad block:
{hasIllustration && (
  <>
    <IllustrationBlock bookSlug={slug} chapterNum={chapterNum} />
    <div className="prose-reader">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{afterIllustration}</ReactMarkdown>
    </div>
  </>
)}
```

**IllustrationBlock uses `fs.existsSync` to guard rendering** — if the PNG doesn't exist on disk it returns `null`. This prevents broken images on chapters where generation failed.

---

## Scope-to-phase mapping additions

| User intent | Phases to run |
|---|---|
| "Add illustrations" / "Generate illustrations" | A2.5 only |
| "Add illustrations to [book]" | A2.5 for that book only |
| Full pipeline (new site) | Skip A2.5 by default |

A2.5 is **not a hard Pre-Launch Gate** — a site can launch with zero illustrations. In a full pipeline run, do not run A2.5 unless the user explicitly requests illustrations in the current turn.

---

## Genre: Mystery

### Peak Scene Selection (Mystery)

Use the same 6-slot distribution as romance (one illustration per sixth of the novel). Peak types differ entirely:

| Slot | Target range | What to look for |
|---|---|---|
| **S1 — Discovery** | chapters 1 – ⌊N×0.17⌋ | The protagonist first encounters the crime, wrong, or anomaly — the scene she cannot un-see |
| **S2 — Commitment** | chapters ⌊N×0.17⌋+1 – ⌊N×0.33⌋ | She commits to finding the truth; first active investigation; the moment she stops dismissing and starts pursuing |
| **S3 — False certainty** | chapters ⌊N×0.33⌋+1 – ⌊N×0.5⌋ | She believes she has the answer; peak of the wrong theory; before the collapse — she is alone with her conviction |
| **S4 — Impossible clue** | chapters ⌊N×0.5⌋+1 – ⌊N×0.67⌋ | The piece of evidence that cannot fit; the moment she holds something that breaks her theory — she doesn't yet know why |
| **S5 — Revelation** | chapters ⌊N×0.67⌋+1 – ⌊N×0.83⌋ | The connection made; she understands; the scene immediately after or during her deduction — the look of someone who now knows |
| **S6 — Confrontation** | chapters ⌊N×0.83⌋+1 – N−2 | Direct face-to-face with the culprit or consequence; the highest-tension scene in the investigation arc |

**Qualifying peak types (Mystery):**
| Peak type | Description |
|---|---|
| **The charged space** | Protagonist alone in a location with significant meaning — the crime scene, the victim's room, the sealed archive; the image is her and the space |
| **The weight of knowing** | She holds evidence or has just understood something; the image captures the knowledge on her face and in her posture |
| **The confrontation** | Direct face-to-face with the culprit, the suspect, or the person who holds the answer; maximum emotional tension between two characters |
| **The gothic moment** | A scene where the setting itself is the subject — she is small in a charged landscape (dark manor, misty moor, sealed room); atmosphere-first |

### Prompt Construction (Mystery)

No allure tiers. Mystery illustrations use **atmospheric drama intensity** instead:

| Level | Definition | When to use |
|---|---|---|
| **L1 — Charged atmosphere** | The setting is the subject; the character is present but the scene's weight comes from the location and its implications | S1, S4 |
| **L2 — Emotional weight** | The character's knowledge or emotion is the subject; the setting amplifies it; the image captures what she knows | S2, S3, S5 |
| **L3 — Direct tension** | Two characters in direct confrontation; the power balance is visible; maximum emotional charge between them | S6 |

**Step 1 — Select intensity level (L1/L2/L3) based on slot.**

**Step 2 — Add character anchors:** pull female lead description. For confrontation scenes, include antagonist physical description. Keep to expression + 2 physical details — posture and expression carry more than appearance in mystery illustrations.

**Step 3 — Add scene-specific context:**
```
{location: specific and period-appropriate — "Victorian drawing room, late afternoon light through lace curtains", "fog-bound cobblestone street, single gas lamp"}
{the object or evidence in the scene, if any}
{protagonist's posture and expression — the emotional register of the moment}
```

**Step 4 — Add genre framing:**
```
dramatic scene illustration, painterly chiaroscuro palette, period editorial atmosphere, single figure with emotional weight, no text, no title, no watermark
```

For gothic/atmospheric peak (L1): replace with:
```
gothic atmosphere illustration, dark editorial palette, figure small against charged landscape, mist and shadow, no text, no title, no watermark
```

**Complete example (S5 — Revelation, L2):**
```
Victorian study, late evening, single oil lamp on the writing desk casting warm amber light against deep shadow. Shelves of leather-bound ledgers behind her. She stands at the desk, one hand flat on an open letter, the other at her mouth — not shock but recognition, the look of someone who has just understood what she was looking at all along.
[female lead: dark upswept hair, sharp grey eyes, posture precise even in shock]
Scene: the letter is open; the evidence is there; she is the only one in the room.
dramatic scene illustration, painterly chiaroscuro palette, period editorial atmosphere, single figure with emotional weight, no text, no title, no watermark
```

---

## Genre: Horror

### Peak Scene Selection (Horror)

| Slot | Target range | What to look for |
|---|---|---|
| **S1 — First wrong thing** | chapters 1 – ⌊N×0.17⌋ | The anomaly she cannot explain away; the first undeniable evidence that something is wrong — she is alone in the space with it |
| **S2 — Confirmed threat** | chapters ⌊N×0.17⌋+1 – ⌊N×0.33⌋ | The threat is real and present; no longer deniable; the protagonist in direct proximity to the danger for the first time |
| **S3 — First cost** | chapters ⌊N×0.33⌋+1 – ⌊N×0.5⌋ | Someone or something is taken or harmed; the threat has demonstrated its power; the aftermath scene |
| **S4 — Isolation peak** | chapters ⌊N×0.5⌋+1 – ⌊N×0.67⌋ | Protagonist at maximum vulnerability — resources depleted, help cut off, alone; the scene before the final act |
| **S5 — Partial reveal** | chapters ⌊N×0.67⌋+1 – ⌊N×0.83⌋ | The nature of the threat becomes visible for the first time in a meaningful way; the character's face as she sees it |
| **S6 — Confrontation** | chapters ⌊N×0.83⌋+1 – N−2 | Direct confrontation with the threat; survival uncertain; the highest-tension scene in the horror arc |

**Qualifying peak types (Horror):**
| Peak type | Description |
|---|---|
| **The charged space** | The wrong place — the basement, the attic, the room that should be empty; the protagonist alone in it; the image is her and the space's wrongness |
| **The witness moment** | She has seen something; the image captures what seeing it has done to her face and body; the thing itself may be implied but not fully shown |
| **The threat proximity** | The threat is close — behind, above, implied in the frame's negative space; the character's body response to proximity |
| **The confrontation** | The protagonist facing the threat directly; maximum tension; survival in the balance |

### Prompt Construction (Horror)

No allure tiers. Horror illustrations use **fear intensity level**:

| Level | Definition | When to use |
|---|---|---|
| **F1 — Atmospheric dread** | The setting is wrong; the threat is implied or absent from frame; the image is the charged space | S1, S4 |
| **F2 — Witnessed fear** | The protagonist's face and body register what she has seen or heard; she is the subject; the threat is off-frame or implied | S2, S3, S5 |
| **F3 — Direct confrontation** | Threat is present in the frame, partially or fully; maximum tension; the protagonist and the threat in the same image | S6 |

**Step 1 — Select fear level (F1/F2/F3) based on slot.**

**Step 2 — Add character anchors:** protagonist physical description with emphasis on expression and posture — "wide eyes, one hand on the wall, body angled toward the exit." Keep the threat description vague at F1/F2 (implied by shadow, wrong angle, negative space); only partially describe at F3.

**Step 3 — Add scene-specific context:**
```
{location: specific and wrong — "basement stairwell, single bare bulb, walls close", "attic with covered furniture, moonlight through a broken pane"}
{what she has just seen or heard — stated as effect, not cause}
{her body position — where she is looking, what her hands are doing}
```

**Step 4 — Add genre framing:**
```
horror scene illustration, dark atmospheric palette, high contrast shadow, visceral emotional tension, figure in charged space, no text, no title, no watermark
```

For atmospheric/no-figure peak (F1): replace with:
```
horror atmosphere illustration, dark editorial palette, wrong space with implied presence, deep shadow and single light source, no text, no title, no watermark
```

**Complete example (S2 — Confirmed threat, F2):**
```
Old house hallway, night, single wall sconce at the far end casting yellow light. She stands in the middle of the hall, turned halfway toward the camera — not fleeing, not yet, stopped by something. Her eyes are open very wide. One hand is flat against the wallpaper. She has heard something that has made her stop.
[protagonist: pale, dark hair loose, wearing a heavy robe — it's the middle of the night]
The threat is not visible. The hall behind her is dark beyond the light's reach.
horror scene illustration, dark atmospheric palette, high contrast shadow, visceral emotional tension, figure in charged space, no text, no title, no watermark
```

---

## Genre: Fantasy

### Peak Scene Selection (Fantasy)

| Slot | Target range | What to look for |
|---|---|---|
| **S1 — Wonder encounter** | chapters 1 – ⌊N×0.17⌋ | The protagonist's first direct encounter with the impossible; the scene where the world reveals its scale to her for the first time |
| **S2 — Power in use** | chapters ⌊N×0.17⌋+1 – ⌊N×0.33⌋ | First significant use of power or magic with visible cost or consequence; the system in action at a high-stakes moment |
| **S3 — Alliance shift** | chapters ⌊N×0.33⌋+1 – ⌊N×0.5⌋ | A key relationship shifts irrevocably — alliance formed, betrayal revealed, loyalty declared; the emotional turning point of the character web |
| **S4 — Battle or confrontation** | chapters ⌊N×0.5⌋+1 – ⌊N×0.67⌋ | A major physical confrontation; the protagonist in the middle of the world's violence; the stakes made visible through action |
| **S5 — The cost** | chapters ⌊N×0.67⌋+1 – ⌊N×0.83⌋ | She pays the highest price yet — loss, sacrifice, the magic's bill due; the scene immediately after or during the cost |
| **S6 — Climax confrontation** | chapters ⌊N×0.83⌋+1 – N−2 | The final confrontation; the world's fate in the balance; the protagonist at the peak of what she is capable of |

**Qualifying peak types (Fantasy):**
| Peak type | Description |
|---|---|
| **The wonder moment** | She stands before something vast and impossible; the image is her small against the world's scale |
| **Power in action** | Magic or power visually manifested; the protagonist as its source or its target; the cost written on her body |
| **The battle beat** | A specific moment in combat — not the whole battle but one precise moment of maximum tension |
| **The sacrifice or cost** | What was given; what was lost; the aftermath of a choice that cannot be undone |

### Prompt Construction (Fantasy)

No allure tiers. Fantasy illustrations use **epic scale level**:

| Level | Definition | When to use |
|---|---|---|
| **E1 — Intimate scale** | Two or three figures; emotional and relational stakes; the world is background | S3, S5 |
| **E2 — Dramatic action** | One or two figures in direct action; power, magic, or combat as the visual subject | S2, S4 |
| **E3 — Epic scale** | The protagonist small against the world; the landscape or impossible thing is the subject | S1, S6 |

**Step 1 — Select scale level (E1/E2/E3) based on slot.**

**Step 2 — Add character anchors:** protagonist in period-appropriate fantasy attire; emphasize posture and visual drama over physical description. For battle or power scenes, include any visual manifestation of the power system (light, shadow, energy, symbol).

**Step 3 — Add scene-specific context:**
```
{location: the fantasy environment — "ruined fortress at the edge of a storm-lit cliff", "dark forest clearing, ancient stone circle, one shaft of cold moonlight"}
{the specific action or moment — "she stands at the summit, the army visible in the valley below", "she reaches toward the fragment and the air around it distorts"}
{the emotional register of the moment — triumph, grief, resolve, terror, wonder}
```

**Step 4 — Add genre framing:**
```
fantasy scene illustration, epic cinematic palette, dramatic lighting, atmospheric fantasy world, no text, no title, no watermark
```

Adjust by scale:
- E1 (intimate): `fantasy scene illustration, painterly warm palette, intimate emotional register, period fantasy setting, no text, no title, no watermark`
- E3 (epic scale): `epic fantasy illustration, vast cinematic scale, figure small against world, dramatic sky and landscape, no text, no title, no watermark`

**Complete example (S1 — Wonder encounter, E3):**
```
Ancient stone bridge spanning a chasm of mist, the far side lost in cloud. She stands at the midpoint of the bridge, very small against the scale — one hand on the worn parapet, her head tilted up at something enormous above the cloud line. The sky above is fractured: two moons visible through a rift in the cloud cover, one pale, one amber. She has never seen this before. Her posture is not fear — it is the specific stillness of someone whose understanding of the world has just changed.
[protagonist: practical travelling clothes, hair loose from a long journey, weathered pack visible]
epic fantasy illustration, vast cinematic scale, figure small against world, dramatic sky and impossible vista, no text, no title, no watermark
```

---

## Genre: Sci-Fi & Dystopian

### Peak Scene Selection (Sci-Fi / Dystopian)

| Slot | Target range | What to look for |
|---|---|---|
| **S1 — Inciting violation** | chapters 1 – ⌊N×0.17⌋ | The moment the system reveals its violence; the protagonist witnesses the thing she cannot un-see; she is changed by what she sees |
| **S2 — Commitment** | chapters ⌊N×0.17⌋+1 – ⌊N×0.33⌋ | She joins the resistance or takes the first act of defiance; the point of no safe return |
| **S3 — Scale reveal** | chapters ⌊N×0.33⌋+1 – ⌊N×0.5⌋ | She understands for the first time how large the problem is; alone with that understanding; the image of someone who now knows the scope |
| **S4 — Crisis** | chapters ⌊N×0.5⌋+1 – ⌊N×0.67⌋ | What she built is at risk; the system has found her; she is at maximum exposure and vulnerability |
| **S5 — Impossible choice** | chapters ⌊N×0.67⌋+1 – ⌊N×0.83⌋ | She faces the decision where both options cost something she cannot afford; the moment before she chooses |
| **S6 — Confrontation** | chapters ⌊N×0.83⌋+1 – N−2 | The final act of resistance or the direct confrontation with the system; the world's trajectory at stake |

**Qualifying peak types (Sci-Fi):**
| Peak type | Description |
|---|---|
| **The witness moment** | She sees the system's violence; the image is her face as she watches something she cannot deny |
| **The system made visible** | The architecture of the wrong world — the compliance checkpoint, the controlled space — with her inside it; the oppression is the visual subject |
| **The resistance act** | A moment of active defiance; the protagonist doing the thing she was told not to do |
| **The scale encounter** | She stands before the full scope of the premise — the vast infrastructure of the wrong world, the scale of what must be changed |

### Prompt Construction (Sci-Fi / Dystopian)

No allure tiers. Sci-fi illustrations use **stakes level**:

| Level | Definition | When to use |
|---|---|---|
| **K1 — Personal stakes** | The protagonist alone with her knowledge or her choice; interior emotional register externalized | S3, S5 |
| **K2 — Direct action** | She is doing something — resisting, witnessing, deciding; the action is the visual subject | S1, S2, S4 |
| **K3 — Systemic scale** | The system's scale is visible; she is human-scale against the world's machinery | S6 |

**Step 1 — Select stakes level (K1/K2/K3) based on slot.**

**Step 2 — Add character anchors:** protagonist in world-appropriate attire (utilitarian, system-assigned, or deliberately non-conforming); emphasize posture and expression. For systemic-scale scenes, the environment often carries more visual weight than the character.

**Step 3 — Add scene-specific context:**
```
{location: the speculative world's specific environment — "grey compliance hall, fluorescent ceiling, numbered booths", "rooftop above the city at night, the tower's signal beams visible across the skyline"}
{the specific action or moment — "she stands at the terminal, the file open, her hands not yet moving", "she is one face in a crowd all facing the same direction, the only one not looking where she should"}
{the emotional register — controlled fear, cold resolve, shock, determination, grief}
```

**Step 4 — Add genre framing:**
```
sci-fi scene illustration, stark cinematic palette, high contrast shadow and artificial light, human figure in systemic environment, no text, no title, no watermark
```

Adjust by scale:
- K1 (personal): `sci-fi scene illustration, cold editorial palette, intimate emotional register, controlled technological environment, no text, no title, no watermark`
- K3 (systemic): `dystopian scale illustration, stark cinematic palette, human-scale figure against vast system architecture, cold and overwhelming, no text, no title, no watermark`

**Complete example (S3 — Scale reveal, K1):**
```
Server room or archive, deep underground — rows of identical units extending beyond the visible frame. Cold white overhead light. She stands at the end of one row, a data tablet in her hand, looking up at the extent of what she is reading about. She has just understood how large this is. Her face is completely still — not shock, but the specific controlled expression of someone who has just stopped being surprised and started calculating.
[protagonist: standard-issue grey work uniform, hair back, the tablet glowing in her hands]
The room is vast. She is small in it. The data on the tablet is the point — but the room is the revelation.
sci-fi scene illustration, cold editorial palette, intimate emotional register within vast systemic space, artificial light and deep shadow, no text, no title, no watermark
```

---

## Genre: Contemporary Drama / Family Drama / Medical Drama

### Peak Scene Selection (Drama)

| Slot | Target range | What to look for |
|---|---|---|
| **S1 — The first crack** | chapters 1 – ⌊N×0.20⌋ | The moment the surface normal (E1) first shows a crack (E2); one character perceives something is wrong and does not name it; the image is a face at the edge of knowing |
| **S2 — The approach** | chapters ⌊N×0.20⌋+1 – ⌊N×0.40⌋ | She moves toward the thing she has been avoiding; the specific resistance visible on her face; a threshold moment before she commits |
| **S3 — Partial truth out** | chapters ⌊N×0.40⌋+1 – ⌊N×0.55⌋ | Something adjacent to the central secret is now in the open (E3); a relationship must reconfigure; the characters are recalibrating |
| **S4 — The witness moment** | chapters ⌊N×0.55⌋+1 – ⌊N×0.70⌋ | She sees something she was not meant to see; or she is in a space that demonstrates the gap between her claim and her acknowledged place |
| **S5 — Confrontation** | chapters ⌊N×0.70⌋+1 – ⌊N×0.85⌋ | The central concealment is directly in the room (E4); avoidance is no longer possible; the image is two characters in the same space with nowhere to go |
| **S6 — Earned reckoning** | chapters ⌊N×0.85⌋+1 – N | The truth is held by everyone it belongs to (E5); not necessarily reconciliation; the cost is acknowledged; the image is stillness after the reckoning |

**Qualifying peak types (Drama):**
| Peak type | Description |
|---|---|
| **The threshold** | Figure at a doorway or corridor — not inside, not outside; what is on the other side is the visual weight |
| **Witnessed distance** | Two characters in the same frame, not touching, not looking at each other; the space between them is the subject |
| **The unclaimed space** | She is in a room where she has a claim that is not acknowledged; the room demonstrates the gap |
| **The almost-said** | One character facing another; she has just not-said the true thing; the expression carries the weight of the withheld |

### Prompt Construction (Drama)

No allure tiers. Drama illustrations use **emotional register**:

| Level | Definition | When to use |
|---|---|---|
| **D1 — Interior, still** | The protagonist alone with a knowledge or a grief; the exterior is quiet; the interior state is the visual subject | S1, S2, S6 |
| **D2 — Relational pressure** | Two characters in the same space under emotional pressure; the composition captures the gap or the tension between them | S3, S4, S5 |
| **D3 — Institutional weight** | The setting carries the scene's pressure — hospital corridor, family home, the room that proves she doesn't belong; character is human-scale inside a charged environment | S1, S4 |

**Step 1 — Select register (D1/D2/D3) based on slot.**

**Step 2 — Zero allure:** no bare skin, no intimate contact, no romantic body language. Ordinary clothes. Stillness over gesture.

**Step 3 — Add scene-specific context:**
```
{location: "hospital corridor, evening — fluorescent overhead, window at the far end showing a dark sky", "family home hallway, morning — a coat she recognizes hanging by the door that she wasn't told about"}
{the specific moment — "she stands at the door of the room, her hand not yet on the handle", "they are both at the table, not eating, not talking, both looking at the third seat"}
{emotional register — quiet dread, still grief, the specific stillness of managed emotion, the expression of someone who has just understood something they cannot unknow}
```

**Step 4 — Add genre framing:**
```
editorial drama scene illustration, desaturated palette, cold-warm contrast, quiet emotional weight, observational composition, no allure, no text, no title, no watermark
```

Adjust by register:
- D1 (interior, still): `quiet literary scene illustration, muted palette, figure alone with interior weight, natural or institutional light, no text, no title, no watermark`
- D3 (institutional): `editorial drama illustration, institutional setting, human-scale figure in charged environment, cold fluorescent and warm distance, no text, no title, no watermark`

**Complete example (S4 — Witness moment, D3):**
```
Hospital corridor, evening. Fluorescent overhead light. She stands at the far end of the corridor — not at the door yet, not close enough for the number on the door to be readable. The corridor is empty except for her. She is holding nothing. Her coat is still on. She is looking at the door at the end of the corridor and she is not moving toward it.
[protagonist: practical coat, hair unstyled, flat shoes — no styling toward beauty; the clothes of someone who came directly from something else]
The corridor is long. She is small in it. The door is the entire point.
editorial drama scene illustration, desaturated institutional palette, cold overhead fluorescent with warm light visible under the door at the far end, quiet observational framing, no allure, no text, no title, no watermark
```

---

## Reference Loading

Only load this file when entering A2.5. It depends on:
- `cover-allure-elements.md` (T3 and T4 assembly blocks — must be loaded alongside this file)
- The book's `outline/outline.md` and `tracking/context.md`
- The book's `world/characters/` (for character anchors in the prompt)
