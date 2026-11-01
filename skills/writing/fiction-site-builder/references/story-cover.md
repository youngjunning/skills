# Story Cover

Load this reference when the user asks to generate a novel cover (/story-cover, cover generation), or when A2 of the pipeline is entered. **Also load `references/facebook-ads.md` alongside this file — every cover is a Facebook ad creative and must pass the scroll-stop standards in Step 1.7.** For romance/drama covers, also load `references/cover-genre-playbook.md` and use its reference-derived CTR pattern blocks when the title, synopsis, or ad angle matches.

**Execution principle: invoke tools directly. Never surface a "please run X" prompt to the user mid-phase. Call the image generation tool, write the file, log the result — then move on.**

## Contents

- A2 entry, modes, and batch discovery
- Character visual sheet and genre routing
- Batch composition and visible-person cap
- Traffic-cover conflict direction
- Prompt construction and generation cascade
- Post-processing, exposure audit, and visual QA

## Cover Generation Contract

Treat these as acceptance criteria, not optional style advice:

### Project non-negotiable Facebook cover law

Every production fiction cover is a Facebook traffic creative for a primary audience aged 40–65. The following rules are hard gates. A cover that misses any one of them is rejected and regenerated or redesigned before publication:

- **Exactly three discernible adults:** show three and only three clearly readable adult people. No crowd, background faces, extra guests, silhouettes that read as additional people, or ambiguous fourth figure. Gender may be any combination.
- **One visibly crying or wronged person:** at least one of the three must be unmistakably crying, tearful, pleading, humiliated, betrayed, or visibly treated unfairly. The emotion must survive a 160px mobile thumbnail.
- **Strong emotional contrast:** the three people must carry different, opposing reactions—such as grief versus guilt versus accusation, panic versus fury versus disbelief, or resignation versus triumph versus fear. Neutral posing, matching smiles, harmonious group portraits, and three people merely looking at the camera fail.
- **40–65 readability:** use large faces, large high-contrast title typography, familiar real-world settings, clear hands and props, and a simple visual hierarchy. The scene must be understood in one glance by an older Facebook reader without relying on small decorative details.
- **One immediate conflict and one proof signal:** freeze a public rupture, betrayal, accusation, interruption, or status reversal and include one large, legible proof object (document, phone, recorder, ring, photograph, envelope, ledger, or similar).
- **No promise of guaranteed CTR:** “high-click” is a design target, not a claim. Final performance must be validated through real Facebook CTR/CPC testing and controlled creative variants.

### Mandatory cover checkpoints

Every generated cover or Facebook hook-card must pass all four checkpoints. Do not approve a prompt, raw image, overlay, or final asset by intuition alone:

| Checkpoint | Required inspection | Hard failure |
|---|---|---|
| **C0 — prompt** | Confirm exactly three adult roles, one crying/wronged role, contrasting reactions, one proof object, one frozen incident, and an image-only composition with no copy. | Vague “dramatic couple,” generic mood, crowd, no concrete consequence, or any requested text inside the image. |
| **C1 — raw art** | View the complete uncropped image at actual output size. Count every discernible person and verify faces, hands, proof object, available-light coherence, and clean negative space. The raw image must contain no title, author, hook, logo, watermark, UI, or readable lettering. | Fewer/more than three people, neutral faces, hidden proof object, pasted lighting, black mud, white fog, cropped action, or any generated text/lettering. |
| **C2 — image-only asset** | Keep the production image as pure artwork. Do not ask the image model to render title, author, hook, subtitle, genre chip, logo, watermark, signage, document text, or decorative lettering. If a site or ad placement needs copy, add it outside the image through deterministic UI/HTML/CSS in a separate layer. | Any visible generated words, gibberish, fake typography, browser/fullscreen notice, platform watermark, channel name, or copied UI chrome. |
| **C3 — thumbnail card** | Render the image-only asset at 160px wide and inspect it as a Facebook feed image on a phone-sized viewport. Recount the three people, identify the crying/wronged face, read the emotional contrast, and recognize the proof object. | Any visible generated text, the story cannot be paraphrased in one breath, any face merges into background, or the proof object becomes decorative noise. |

The C0–C3 audit applies to **every image in a batch**, not only the first or best-looking variant. Record failures and regenerate or redesign the individual image; never let a passing sibling hide a failed asset.

1. **Normal exposure by default:** use mid-key, scene-appropriate lighting. Keep natural skin tones, readable shadow detail, controlled highlights, and local contrast. A requested white or bright palette is valid, but must retain texture and midtone contrast rather than becoming washed out.
2. **One frozen scandal:** show a specific irreversible moment—an accusation, exposed proof, ceremony interruption, betrayal caught, rescue collision, or public humiliation. A cast lineup is not a scene.
3. **Exactly three people:** the project law above replaces the generic 3–4-person range. Use three clearly differentiated adults for ensemble conflict and never exceed or fall below three without an explicit user exception.
4. **Exaggerated reaction chain:** every visible face needs a different story role and readable emotion; at least one person must be crying or visibly wronged, and the emotional contrast must be obvious at thumbnail size. Reject neutral model posing.
5. **One thumbnail-readable proof object:** make the document, scan, ring, photograph, phone, recorder, ledger, envelope, token, or other evidence large enough to understand at 160px wide.
6. **40–65 audience readability:** prefer large type, high contrast, familiar relationship stakes, and uncluttered framing over fine-art subtlety or atmosphere-first composition.
7. **Generate image-only art:** do not generate or composite any title, author, hook, subtitle, logo, genre chip, watermark, UI, signage, or readable lettering into the production image. Keep the canvas clean; any required copy belongs outside the raster asset in the consuming page or ad placement.
8. **No prestige drift:** do not use elegant/editorial/subtle/movie-poster direction unless the user explicitly asks for it. Traffic covers should feel like a high-conflict short-drama freeze-frame, not luxury key art.
9. **Inspect the final card, not only the source image:** overlays, title bands, UI chips, and image crops are part of the cover. Reject collisions, duplicated labels, covered faces, black mud, white fog, extra people, weak crying/wronged emotion, or unreadable proof objects.

**Instruction precedence:** the user's explicit direction and supplied visual references come first; this contract comes second; genre pattern blocks and allure guidance come after it. A genre template must never override the visible-person cap, frozen-conflict requirement, normal-exposure default, or final-card QA. When instructions conflict, preserve story clarity and conflict—not glamour, darkness, skin exposure, or cinematic atmosphere.

## A2 Entry Check

**MANDATORY — run this bash command before anything else. Do not skip it. Do not assume the result.**

```bash
[ -n "$APIYI_API_KEY" ] && echo "API_PATH=apiyi" || echo "API_PATH=skip"
```

**If the output is `API_PATH=apiyi` → you MUST use the apiyi curl path below.**

If the output is `API_PATH=skip` → print the warning below, then **skip cover generation for this book and continue the pipeline** (no SVG fallback — leave the cover to be filled in later):
```
\033[33m⚠ WARNING: APIYI_API_KEY is not set. Skipping cover generation (no SVG fallback).\033[0m
\033[33m  Covers require apiyi. Get an API key at:\033[0m
\033[33m  https://api.apiyi.com/register/?aff_code=ijv5\033[0m
\033[33m  Then set: export APIYI_API_KEY="your-key"\033[0m
```

The apiyi path writes the raw PNG to a temporary file (e.g. `/tmp/cover_{book-slug}_v1.png`). That PNG is converted to the final flat WebP and deleted immediately. No subfolders are created under `public/covers/`. When the key is missing, no file is produced — do not block the pipeline; the book launches without a cover and the slot is flagged for a later pass.

## Modes

| Mode | When to use | What it generates |
|---|---|---|
| **Batch** | Initial site launch — all books written, Pre-Build Gate pending | Covers for every book in `content/` |
| **Single-book** | Adding one new book to an existing site | Cover for one book only (logo/favicon already exist) |

**Default to Batch mode at initial launch.** The Pre-Launch Gate requires covers for all ≥3 books. Single-book mode is for incremental updates only.

---

## Batch Mode (initial launch)

### B1 — Discover all books

List every directory in `content/` that is NOT `content/short/` — short stories do not get standalone covers.

```bash
CONTENT_DIR="${CONTENT_DIR:-./content}"
BOOKS=()
for d in "$CONTENT_DIR"/*/; do
  [ -d "$d" ] && [ "$(basename "$d")" != "short" ] && BOOKS+=("$(basename "$d")")
done
printf 'Found %d books:\n' "${#BOOKS[@]}"
printf '  %s\n' "${BOOKS[@]}"
```

If fewer than 3 books are found, log a warning and continue with whatever books exist. Cover generation is not blocked by the book count — missing covers can be retried later.

### B2 — Resolve pen name (no prompt)

Read the pen name from project files in this order — do not ask the user:

1. Any `content/{book}/world/worldbuilding.md` → first "Author" line
2. Any `content/{book}/tracking/context.md` → first "Pen name" line
3. `src/lib/books.ts` → first book's `author` field (only exists after B4 site build)

Note: `src/lib/books.ts` is generated during B4 and will not exist when A2 runs. Try it last, not first.

If the pen name cannot be found in any of these files, substitute `"The Author"` as a placeholder and log a warning. Never stop the batch to ask.

### B3 — Generate covers

**MANDATORY — generate all covers in parallel.** Never loop books sequentially. Launch one background process per book (`gen_cover_apiyi ... &`), then `wait` for all to finish. For each book:
1. Read `content/{book-title}/world/worldbuilding.md` to extract genre and tone.
2. Run genre detection (Step 1.5 below) to select cover style.
3. Roll the cover tier (T2 or T3, per the Female figure rule) and build the cover prompt (Step 2 below) substituting the book's title, genre, and characters.
4. Run Step 3 (apiyi cascade: gpt → doubao → nano).
5. Verify the output file exists.
6. Log: `✓ {book-title} — cover saved` or `⚠ {book-title} — cover skipped: {reason}`.

```bash
# parallel batch — one process per book, then wait
for BOOK in "${BOOKS[@]}"; do
  ( mkdir -p public/covers; build_and_generate_cover "$BOOK" ) > "/tmp/cover_$BOOK.log" 2>&1 &
done
wait
rm -f /tmp/cover_*.log
```

### Batch completion checklist

- [ ] Covers exist for as many books as possible.
- [ ] Any failed/skipped covers are logged with the book title and error reason.

Missing covers are not a hard blocker for site build — the site can use CSS placeholders during development. Re-run A2 later if needed. Site logo and favicon are generated in B2 (Design Identity) — do not block on them here.

---

## Single-book mode

Use for adding one book to an already-launched site. Skip logo and favicon steps — they already exist.

## Generation Method

**apiyi path (preferred):** `curl` to `https://api.apiyi.com/v1/images/generations` with model `gpt-image-2-all`. Response `b64_json` already includes `data:image/png;base64,` prefix — strip it before decoding. See Step 3 and `references/apiyi.md` for full API reference.

**No SVG fallback.** When `APIYI_API_KEY` is not set, skip cover generation for the book (print the warning, continue the pipeline) — never write a styled SVG cover.

## Environment Variables

| Variable | Required | Notes |
|---|---|---|
| `APIYI_API_KEY` | No | API key for `api.apiyi.com`. If unset, cover generation is **skipped** (no SVG fallback) — the pipeline continues and the cover slot is filled later. Get one at https://api.apiyi.com/register/?aff_code=ijv5 |
| `BOOK_DIR` | Yes | Output directory, e.g. `./public/covers/{book-title}` |

## Step 1 — Resolve required info (no prompt)

Must have before proceeding: **book title**, **author pen name**, **BOOK_DIR**.

Derive all three from project files:
- **Book title**: directory name under `content/`
- **Pen name**: see B2 resolution order above (worldbuilding → context → books.ts → placeholder)
- **BOOK_DIR**: not used — covers are written as flat files: `public/covers/{book-slug}.webp` and `public/covers/{book-slug}.json`
- **Temporary PNG**: `/tmp/cover_{book-slug}_v1.png` (deleted after WebP conversion)
- **Cover cast list**: read `content/{book-slug}/world/characters/` and the outline/context files to identify the protagonist plus at most 3 premise-defining supporting characters. Rank by relevance to the frozen cover conflict; do not carry the full story ensemble into the image. This cast list is mandatory input to Step 2.

Do not ask the user. Do not fabricate values that cannot be derived.

### Step 1.1 — Character Visual Sheet (canonical, required)

**Before building any prompt**, resolve the character visual sheet for this book. Also load `references/facebook-ads.md` — the Signature and Figure fields must produce scroll-stopping images, not just accurate descriptions.

1. **Check for existing sheet:** `content/{book-slug}/world/character-visuals.md`
   - If it exists → read it and use the descriptors verbatim in the prompt.
   - If it does not exist → derive from `world/worldbuilding.md` + chapters 1–3, then **write** it now.

2. **Format of `character-visuals.md`:**

```markdown
# Character Visual Sheet — {book-title}

## Female Lead
- Ethnicity: [derive from worldbuilding/synopsis — e.g. "Latina woman, olive skin" / "Black woman, deep brown skin" / "Caucasian woman, light skin" — match the character's stated or implied background]
- Hair: [color, length, style — e.g. "dark auburn waves to mid-back"]
- Eyes: [color — e.g. "pale green eyes"]
- Figure: [body type — use the Female figure rule phrasing]
- Signature: [1–2 FB scroll-stop visual markers: expression (parted lips / wide eyes catching something off-frame / suppressed tears), implied story (clutching something / half-turned away / caught mid-movement), or physical detail that implies narrative tension]

## Male Lead
- Ethnicity: [derive from worldbuilding/synopsis — match the character's stated or implied background]
- Hair: [color, length — e.g. "dark brown, short-cropped"]
- Eyes: [color]
- Build: [e.g. "tall, broad-shouldered, lean muscular"]
- Signature: [1–2 FB scroll-stop visual markers: dominant stance / world signal (suit at dawn / holographic edge / tactical gear) / implied power that creates a question in the viewer's mind]
```

3. **Rules:**
   - Every character prompt MUST include the exact phrasing from this sheet (copy-paste, not paraphrase).
   - The sheet is shared by A2 (covers) and A2.5 (illustrations) — once written, never regenerated unless the book's worldbuilding explicitly contradicts it.
   - Ethnicity is derived from the novel's worldbuilding/synopsis — there is no global default; write what fits the character.
   - **Signature fields must serve FB scroll-stop signal #2 (implied story) and #1 (expression)**. A Signature like "always looks a little underdressed for the room" is good — it implies narrative tension. A Signature like "blue eyes" is not a Signature, it belongs in Eyes.
   - **Always render all characters as real humans — regardless of their in-story nature.** If a character is an AI, hologram, ghost, demon, vampire, fae, or any non-human entity, depict them as a real human on the cover. The cover is an ad creative, not a literal story illustration. Non-human visual elements (glowing projections, CGI beings, supernatural creatures) destroy photorealism and kill Facebook CTR. Translate the character's personality and role into a real human's appearance, posture, and expression instead.

Cover ratio: **2:3 portrait**. Generate at `848x1280` (1K Fast tier — sufficient for all UI display sizes, fastest generation). No resize step needed.

## Step 1.5 — Determine visual register and genre

**First: check the site-level visual register** (set during B2 design plan, or derive from the site's dominant content type):
- If the site is drama/romance-dominant → **Cinematic Drama** register for all covers
- If the site is fantasy/sci-fi-dominant → **Dark Fantasy Illustration** register for all covers
- Record the register and apply it consistently across all books on this site

**Then: detect per-book genre** by scanning the book title (and synopsis if available) against the keyword table in `references/cover-styles.md`.
- One match → use it
- Multiple matches → priority order: Cultivation Fantasy > Dark Fantasy > Historical > Thriller > Contemporary Romance > Urban Drama > Sci-Fi > Horror > Isekai
- No match → default to the site's primary genre

The genre determines composition template, color palette, character design, and typography style. The visual register determines render quality language (photorealistic film-still vs. hyperrealistic 3D render).

**If the detected title/synopsis matches a reference-derived CTR pattern** from `references/cover-genre-playbook.md`, use that pattern block as the base prompt and then substitute story-specific character descriptors from `character-visuals.md`. Pattern blocks override generic genre formulas because they encode a proven thumbnail read:

- Gothic Funeral Bride / Buried Bride
- Rejected Husband Owns the City / Urban Revenge Landscape
- Threshold Rejection / Discarded Heir / Family Exile
- Facebook Hook-Card / Story-Beat Freeze-Frame
- Royal Claim Family Drama / Owned and Claimed
- Secret Deal With My Billionaire Boss / Office Near-Kiss
- Multicultural Mistake / Warm City Embrace
- Rival Cheer Captain / Bright Sports Poster
- Military Skyline Shield / Ruthless Protector Boss
- Wolfless Mate / Moonlit Alpha Shifter
- Ex-Wife Regret / No Love Left Close-Up

**Allure applies to ALL genres — intensity varies by genre, never zero.** A cover with no physical magnetism, no skin, and no charged atmosphere is a failure regardless of genre. Load `references/cover-allure-elements.md` for vocabulary. Apply the tier matching your genre:

| Genre | Allure tier | What it looks like |
|-------|-------------|-------------------|
| Romance / romance / Contemporary Drama | **T2–T3 (mandatory, roll per cover)** | Deep neckline + bare back / torn garment + wet fabric. Maximum skin within §0 floor. See Female figure rule below. |
| WLW / Sapphic Romance | **T1–T2 (default T1, push T2 via satin fabric + décolletage)** | Luxury satin sleepwear open at collar, necklines falling naturally, warm skin tones as primary texture. Intimacy communicated through proximity and fabric, not explicit exposure. |
| BL / MM Romance | **T1 (charged proximity, no explicit content)** | Open collar, shirt undone one button, bare jaw and throat in warm light. Allure is entirely in the charged gap between figures — skin vocabulary is minimal but deliberate. |
| African Royalty / Multicultural Historical | **T1 (regal presence, not allure-forward)** | Traditional garments are the primary visual element. Allure lives in posture, composition authority, and the warm light catching fabric and jewelry. Bare chest (male figure only, in traditional context) is acceptable. |
| Gothic Bridal Thriller | **T1 (sensuality via contrast — bridal innocence against dark atmosphere)** | Backless lace wedding gown is the primary allure element. Bare back with intricate embroidery, visible décolletage at the front when she turns. The gothic atmosphere carries the mood; the lace carries the allure. |
| Domineering CEO / Rejected Spouse Revenge | **T1 (male-dominant physicality)** | Rain-soaked shirt that clings to chest and shoulders, jacket open, jaw and neck in high-contrast key light. Secondary female figures in evening wear at T1. The allure is power read through physicality. |
| Fantasy / Paranormal / Historical | **T1–T2 (default T1, push T2 when composition allows)** | Bare shoulder, off-shoulder gown, wind-pulled fabric revealing leg, armour gap, sheer sleeve. Physical contact between figures if Duo/Trio. |
| Mystery / Gothic Thriller / Literary Thriller | **T1 (atmospheric sensuality, not explicit)** | Figure silhouetted in revealing dress, collarbone and décolletage prominent, rain-soaked blouse, dishevelled hair, coat falling off one shoulder. Mood is dangerous + magnetic, not clinical. |
| Horror | **T1 (vulnerability, not allure — same skin vocabulary, different emotional register)** | Pale skin exposed at throat/shoulders, torn nightgown, soaked fabric, fear-posed body that is also visually magnetic. The exposure signals danger, not invitation. |
| Sci-Fi / Dystopian | **T1 (fit physique + utilitarian reveal)** | Form-fitting suit, cropped jacket, bare midriff under armour, short tactical garment. Physique is lean-athletic, not domestic-soft. |

A cover where the figure is fully clothed, covered from neck to ankle with no body-conscious framing is a quality gate failure for **every genre**. T1 is the absolute floor — apply it even for mystery and horror. Never go below T1.

- **Romance / Drama genres:** follow the full Female figure rule below (T2/T3 mandatory). Load `references/cover-allure-elements.md` Costume Elements, Poses, and English Romance Playbook. Pick the genre-specific prompt formula and follow the Escalation Strategy if the output looks tame.

## Step 1.6 — Batch Diversity Plan (batch mode only)

**Before generating any covers, assign each book a unique slot in a diversity grid.** Two covers on the same site must not share the same composition type AND pose. Log the plan before running the batch.

### Composition types — assign one per book, rotate across the batch

| Type | When to use | Character count |
|------|-------------|-----------------|
| **Solo** | Strong single-POV protagonist; atmospheric/thriller/horror/sci-fi; story doesn't require a second prominent character | 1 (protagonist only) |
| **Duo** | Two-character focus — both leads present; romance, drama, fantasy duo, detective pair, allies | 2 |
| **Trio** | Love triangle, rival over shoulder, court/pack dynamic with 3–4 key figures | 3–4 |
| **Environmental** | Thriller, mystery, horror — figure(s) small against a dramatic landscape/setting | 1–2, environment dominant |

### Status / Case Unlocked template

Use this as a **text-free image-only** composition for promotion-led covers about revenge, captivity, criminal power, rank changes, public exposure, or a protagonist entering a dangerous new status. Do not add a status label, title, author, hook, badge, logo, or any other copy to the raster image. The consuming page or ad system may supply those elements outside the image when required.

**Luminance preservation — mandatory:** match a supplied reference's exposure family—low-key, mid-key, or high-key—without exaggerating it. Follow an explicit user palette before any genre convention: a white, ivory, silver, pale-blue, or daylight cover is fully valid. Do not translate a bright reference into night, and do not translate a request for white into overexposed fog. Without a reference or explicit direction, use **mid-key normal exposure**. Warm ivory, pale stone, mist grey, and daylight glass are valid background colors, while skin and highlights must retain texture.

## Exposure Gate — Reject Dark Mud and White Fog

Apply these rules to every cover batch, especially crime, thriller, mafia, bullying, horror, and revenge:

- Dark subject matter is not a palette instruction. Do not add a dark or black palette unless the user explicitly requests it; do not let genre convention override a requested white, ivory, silver, pale-blue, or daylight palette.
- `Readable`, `daylight`, and `not dark` are not instructions to overexpose. Do not stack `bright`, `high-key`, `airy`, `white`, `glowing`, and `soft haze` in one prompt. Do not add global white veils or fog to solve typography.
- In a multi-cover batch, default at least half of the covers to mid-key normal exposure. Use low-key or high-key treatment only when the scene/reference earns it; adjacent cards may vary without occupying opposite extremes.
- Faces, proof objects, and the main conflict must remain readable at 160px wide without increasing screen brightness.
- Preserve highlight texture in white clothes, walls, sky, paper, and skin. If these merge into a flat white field, the cover is overexposed even when faces remain visible.
- Do not use text bands, title plates, text strokes, copy shadows, labels, badges, or gradients intended to support text inside the raster asset.
- When adapting a supplied reference, match its overall luminance and contrast direction, while removing all visible wording, lettering, logos, and UI.
- Audit the generated image as an image-only WebP. Any required copy is a separate consuming-layer concern, not part of cover generation.

Run an automated luminance check after final WebP export. The thresholds are deliberately broad; they catch extremes and do not replace visual QA:

```bash
python3 - "$COVER_PATH" <<'PY'
from PIL import Image
import sys
im = Image.open(sys.argv[1]).convert('RGB').resize((128, 192))
def luminance_values(region):
    return [(0.2126*r + 0.7152*g + 0.0722*b) / 255 for r, g, b in region.getdata()]
values = luminance_values(im)
mean = sum(values) / len(values)
dark_share = sum(v < 0.12 for v in values) / len(values)
bright_share = sum(v > 0.92 for v in values) / len(values)
middle = luminance_values(im.crop((0, 64, 128, 128)))
lower = luminance_values(im.crop((0, 128, 128, 192)))
middle_mean = sum(middle) / len(middle)
lower_mean = sum(lower) / len(lower)
lower_bright_share = sum(v > 0.92 for v in lower) / len(lower)
lower_lift = lower_mean - middle_mean
print(
    f"mean_luminance={mean:.3f} dark_pixel_share={dark_share:.3f} "
    f"bright_pixel_share={bright_share:.3f} lower_mean={lower_mean:.3f} "
    f"lower_bright_share={lower_bright_share:.3f} lower_lift={lower_lift:.3f}"
)
if mean < 0.18 or dark_share > 0.65:
    raise SystemExit("FAIL_DARK: regenerate, lift scene exposure, or reduce the black overlay")
if mean > 0.62 or bright_share > 0.45:
    raise SystemExit("FAIL_BRIGHT: regenerate, restore midtones, or reduce the white overlay")
if (lower_mean > 0.78 and lower_lift > 0.22) or lower_bright_share > 0.40:
    raise SystemExit("FAIL_LOWER_VEIL: reduce/remove the lower-third white overlay")
PY
```

If `FAIL_DARK`, remove stacked low-key terms, lift the scene to normal exposure, and remove opaque overlays. If `FAIL_BRIGHT`, remove stacked high-key/haze terms, restore midtone contrast, and remove white overlays. If `FAIL_LOWER_VEIL`, keep the source art and fix the deterministic composition layer first. The regional check exists because an opaque lower-third veil can look bad while the whole-image average still appears acceptable. Do not correct one extreme by forcing the opposite extreme. Then visually compare the full batch as a row and as rendered cards, not only one source cover at a time.

Operator quick reference:
- **Solo** means one character owns the cover. Use it when the protagonist's individual arc is stronger than the relationship dynamic, or when the genre benefits from a single iconic figure.
- **Duo** means two characters share the cover. Use it for romance, drama, fantasy pairs, detective pairs, or allies where the relationship is the selling hook.
- **Trio** means 3–4 figures create the tension. Use it for love triangles, rivals, courts, packs, factions, or group power dynamics; keep one clear focal pair or focal character.
- **Environmental** means the setting is the main drama. Figure(s) may appear, but atmosphere, danger, place, scale, or worldbuilding should dominate the read.

**Visible-person cap — MANDATORY:** never render more than 4 discernible people on one cover. Count every readable face or body, including children, rivals, witnesses, mourners, guards, teammates, and background figures. For ensemble relationship conflicts, prefer 3–4 clearly differentiated figures. Solo, Duo, and Environmental compositions remain valid when the premise is genuinely narrower. If the story has more than 4 relevant characters, keep the protagonist plus the top 2–3 characters needed to explain the frozen conflict; imply everyone else through proof objects, empty positions, cropped hands, architecture, or environmental signals. Do not create a readable crowd, court line, family gathering, army, or team behind the focal cast.

- **Duo cap: maximum 1 Duo cover per 3-book initial batch.** Larger batches may use up to 2 Duo covers per site, but must keep at least half the covers non-Duo (Solo, Trio, or Environmental).
- Do not assign the same type to more than 2 consecutive books.
- Every batch must include at least one Environmental cover.

### Camera framing — rotate across the batch

| Frame | Prompt fragment | Cap per site |
|-------|----------------|-------------|
| Full body (feet to crown) | `full-body shot, both figures visible head to toe` | No cap |
| Medium (hip to crown) | `medium shot, from hip to crown` | No cap |
| Close-up / intimate crop | `tight crop on faces and upper chest` | ≤2 per site |
| Side-profile body + face forward | `pure side-profile body, face turned toward viewer` | ≤2 per site |

- No more than 2 covers per site may use the same framing.

### Pose — rotate through the full Poses table

- Assign each book a pose from `cover-allure-elements.md` Poses table.
- **No pose may repeat for 2 consecutive books** in the same batch.
- From-behind poses (marked ▲) cap at **2 per site** (not "1 in 3" — the cap is a count, not a ratio).
- Solo covers: pick any solo-friendly pose: Solo power pose, Solo atmospheric, Downcast gaze, Billowing skirt, Rain-soaked.

### Color palette / environment — vary across the batch

No two books on the same site should share the same dominant palette. Assign from:
`warm amber candlelight` · `cold silver moonlight` · `neon rain street` · `golden morning light` · `moody luxury penthouse` · `moody gothic stone` · `coastal golden-hour` · `stark high-contrast black-and-white accent`


## Step 1.7 — Facebook Ad Scroll-Stop Standards

Every cover is also a Facebook ad creative. Apply these standards inside Step 2 — they are not optional and override "aesthetically nice" defaults.

**Evidence weighting:** Treat `cover-allure-elements.md` §"Narrative Tableau Library" and §"Performance Direction" as the highest-priority specification. A cover that makes forced marriage, public rejection, medical proof, hidden status, or late regret legible wins over a more attractive but generic intimate pose. When this conflicts with an allure-tier default, keep the event and lower the allure.

**The 0.3-second test (mandatory gate):** A viewer scrolling their feed at full speed must feel something in under 0.3 seconds — not just notice an attractive person. If the image would read as a fashion photo or stock portrait, it fails the test. Rewrite the prompt.

### Traffic-cover style lock — normal exposure, no prestige fallback

Unless the user explicitly asks for an elegant or cinematic cover, traffic fiction uses **normally exposed dog-blood short-drama conflict**, not premium editorial restraint. `Normal exposure` means believable scene light, natural skin, retained highlight texture, readable midtones, and enough contrast to separate people from the setting.

#### Anti-premium production-value gate

Darkening a polished ensemble does not make it a traffic cover. Reject any result that still reads as a movie poster, streaming key art, beauty campaign, romantic couple portrait, or wealthy-family publicity photo. For traffic covers, production value should feel deliberately immediate and inexpensive:

- Prefer a handheld phone-camera or cheap local-TV freeze-frame: 24–28mm wide view, slightly crooked eye level, awkward close crop, overlapping bodies, and evidence pushed toward the lens.
- Use one coherent source family that belongs to the location: neutral office ceiling panels, a warm hotel corridor fixture, overcast outdoor daylight, or soft tungsten on a modest costume-drama set. A weak on-axis fill may lift eyes, but it must not create a second visible light direction. Low budget means simple location light—not direct phone flash, hard LED glare, or random mixed color temperatures. Avoid sculpted rim light, beauty key light, bokeh, elegant chiaroscuro, and teal/orange separation.
- Use cramped ordinary locations and visibly practical props: a standard hotel room, crowded office, apartment dining room, hospital corridor, registry desk, small hearing room, worn wedding jeep, or modest costume-drama set. Do not establish scale through mansion facades, palace vistas, skyline panoramas, giant moonlight, or epic ruins.
- Preserve imperfect realism: sweat, creased clothes, tired eyes, visible age, uneven hair, and unflattering but legible reactions. Keep skin matte and dimensional; reject waxy highlights, oily flash glare, beauty retouching, and actor-poster perfection.
- Every visible person must be caught doing something to another person or the evidence: pushing, grabbing, blocking, pointing, tearing, snatching, recoiling, or shouting. Four people standing in an arc is still a family group photo even when all four look surprised.
- Typography should resemble a mobile short-drama thumbnail: heavy block title, hard shadow or outline, one loud accent bar, and a compact proof hook. Avoid elegant serif, refined spacing, ornamental gold, and balanced theatrical-poster composition.

At final-card QA, ask: **could this image plausibly be a polished movie poster or wealthy-family cast photo?** If yes, reject it even if the plot and facial expressions are technically correct.

- **Required frozen action:** show an accusation, slap-down of evidence, ceremony interruption, caught betrayal, public exposure, rescue collision, or comparable irreversible moment. Characters must be doing something to one another; standing in a symmetrical lineup is not a scene.
- **Required reaction chain:** assign every visible person a distinct readable reaction such as wide-eyed shock, open-mouthed panic, finger-pointing accusation, tearful fury, guilty recoil, desperate grabbing, or stunned disbelief. At least 2 faces must be exaggerated; no visible face may be neutral without a plot-specific reason.
- **Required proof object:** make the document, scan, ring, child, phone, ledger, photograph, test result, or other scandal proof large enough to read as evidence at thumbnail size.
- **Normal readability:** choose a believable ballroom, hospital, courthouse, office, harbor, street, or home exposure. Faces must be readable, and white clothing and walls must retain texture. Use direct light plus controlled fill—not global haze, a white wash, or lifted shadows.
- **Prompt bans:** remove `premium`, `prestige`, `high-end editorial`, `fashion editorial`, `elegant`, `sophisticated`, `subtle`, `restrained expression`, `calm power`, `quiet intensity`, `moody cinematic`, `85mm prestige portrait`, and `atmosphere-first` unless the user explicitly requested them.
- **Composition bans:** reject a beautiful cast lineup, harmonious group portrait, everyone looking away, characters standing without interaction, symmetrical power tableau with neutral faces, or a generic couple centered like a wedding poster.

Before accepting a cover, state the frozen scandal in one sentence and label each visible person's action and emotion. If that cannot be done from the pixels without reading the title, regenerate it. Also name the dominant lighting condition in one phrase. If it requires more than one contradictory phrase—such as `warm faces plus blue rim plus flash`—or the only honest description is `very dark`, `washed out`, or `waxy flash`, reject it.

### Lighting-coherence gate

- Choose exactly one dominant color temperature and direction per scene. Background practicals may be visible, but they must belong to the same family and cannot paint separate blue/orange edges around people.
- All faces in the same plane must share believable exposure and shadow direction. Reject results where each actor appears individually keyed or pasted into the room.
- Preserve forehead, cheek, nose, paper, satin, and white-clothing texture. Small highlights are acceptable; clipped or greasy facial patches are not.
- Keep ambient background detail within roughly two stops of the faces. A readable face floating over a dead-black room is a failure.
- For ordinary interiors, prefer broad ceiling bounce or window diffusion over on-camera flash. For overcast exteriors, use sky diffusion only. For costume sets, use one broad warm overhead/front source and let practical lanterns remain background decoration, not additional keys.

### Prompt assembly — write observable direction

Build the prompt in this order. Use concrete nouns and actions; do not substitute aesthetic adjectives for staging.

```text
PURPOSE: traffic-fiction cover, photorealistic short-drama freeze-frame, normal mid-key exposure.
EVENT: [one irreversible scandal in a single sentence].
CAST: exactly [1–4] discernible adults; list each role, position, physical action, and distinct expression.
PROOF: [one large evidence object], held toward camera or placed in the focal plane.
SETTING: [one instantly recognizable story world], uncluttered enough for thumbnail reading.
LIGHT: one believable [daylight / warm interior / neutral ceiling fluorescent / overcast] source family and one shadow direction; matte natural skin; controlled highlights; background within two stops of faces; no flash glare, rim light, mixed color temperature, fog, or wash.
COMPOSITION: portrait 2:3, medium-wide or medium shot, triangular/asymmetric action, faces and proof unobstructed, clean top and lower text safe zones.
NEGATIVE: no text, no watermark, no crowd, no extra faces, no neutral posing, no fashion lineup, no romantic embrace, no prestige poster, no deep crushed shadows, no overexposure, no blown white clothing, no white haze.
```

Do not write mutually cancelling directions such as `bright high-key` plus `deep moody shadows`, or `clean minimal composition` plus a long list of background extras. If a prompt needs more drama, intensify the **event, gestures, and expressions** before changing exposure or adding people.

### Conflict staging patterns

Choose one pattern per cover and vary it across a batch:

| Pattern | Foreground action | Reaction chain | Proof object |
|---|---|---|---|
| Public accusation | protagonist thrusts evidence toward accused person | fury → guilty recoil → witness shock | contract, test, photograph |
| Ceremony interruption | intruder stops vows/award/announcement | outrage → panic → authority alarm | ledger, ring, sealed letter |
| Rescue collision | rescuer pulls victim from vehicle/doorway while another blocks them | fear → protective rage → exposed guilt | key, family seal, restraint |
| Institutional humiliation | target stands up against official or elite antagonist | defiance → accusation → stunned bystander | receipts, scholarship file, verdict |
| Identity exposed | protagonist displays proof while rival tries to seize it | resolve → panic → disbelief | certificate, badge, name record |

The evidence object supports the conflict; it must not introduce an extra readable face. Avoid photographs with a large portrait when the visible-person count is already at the cap.

### Five scroll-stop signals — bake all five into every cover prompt

**1. Expression drives everything.**
The female lead's face must carry one clear, intense emotion. Never neutral, never pleasant. Pick one and make it unmistakable:

| Emotion | Prompt fragment |
|---------|----------------|
| Shocked / startled | `wide eyes, lips parted in shock, clutching something to her chest` |
| Fearful + drawn-in | `wide eyes, slight tremor in the jaw, leaning back yet unable to look away` |
| Desperate longing | `heavy-lidded gaze, parted lips, soft anguish in the brow` |
| Cold fury | `jaw set, eyes burning with restrained fury, perfectly composed posture masking rage` |
| Torn — wanting + terrified | `eyes full of conflict, biting lower lip, body angled away but gaze pulled back` |

**2. Foreground/background depth composition (high priority for billionaire/romance).**
Place the female lead large in the foreground (occupying 60–70% of frame height), male lead smaller in the background. This creates three simultaneous questions in the viewer's mind: *What did she just find out? Who is he? What happens next?*

Prompt fragment: `female lead fills the foreground, male lead seated or standing behind her in the mid-ground, smaller, watching her`

Never center both characters at the same scale — that reads as a wedding photo, not a thriller.

**3. Implied-story read (3-word premise in 0.3 seconds).**
The image must communicate a 3-word story premise without any text. Target premises:
- "morning after scandal"
- "dangerous obsession discovered"
- "forbidden attraction exposed"
- "power shifted overnight"

Achieve this through environment + costume + expression together:
- Morning after: rumpled bedding, warm morning light, bare shoulders, man still present
- Dangerous obsession: she found something (document, phone, ring) — her expression reacts to it while he watches
- Forbidden attraction: extreme physical proximity despite one character clearly trying to create distance

**Narrative-tableau gate:** In addition to the 3-word premise, the frame must show a specific plot event with visible proof: a ceremony interrupted, a document/scan that changes the relationship, a public humiliation, a return to the estate, a rival at a gala, or an inheritance reveal. Pull one scaffold from `cover-allure-elements.md` §"Narrative Tableau Library" and state the event, proof object, and reaction in the final prompt. Do not ship a generic embrace, portrait, or glamorous couple pose.

**4. Wealth / world signal in the environment.**
One background element must instantly communicate the story's world. The viewer shouldn't need to read the title to know if it's a billionaire romance vs. a small-town romance vs. a dark paranormal.

| Story world | Environment signal |
|-------------|-------------------|
| Billionaire / romance | `floor-to-ceiling windows, city skyline at dawn, luxury penthouse suite` |
| Mafia / cartel | `dim marble-floored study, heavy drapes, a city visible through armored glass` |
| Military / action | `tactical vehicle interior, map-covered desk, desert light through a dusty window` |
| Paranormal / fae | `midnight forest, bioluminescent light, stone archway with moonlight beyond` |
| Historical / Regency | `candlelit drawing room, damask wallpaper, frost on the window beyond` |
| Sci-fi / dystopian | `neon-lit rain-soaked city below, glass and steel, cold blue cityscape light` |

**5. Partial-reveal over explicit — suggest more than it shows.**
Bare shoulders + clutched sheet outperforms full nudity for Facebook delivery (better CTR, lower rejection risk). The viewer's imagination does more work than the image needs to. Standard partial-reveal constructions:

- `bare shoulders, clutching white bedsheet or silk to her chest`
- `silk robe slipping off one shoulder, catching at the elbow`
- `wet blouse pressed against her figure, hair damp and dishevelled`
- `his jacket placed around her bare shoulders from behind`
- `one strap fallen, hand pressed to collarbone`

### Reference image — canonical T2 template (GPT-native, high-CTR Facebook ad, romance / billionaire)

**Use `gpt-image-2-all` for this template.** This is the GPT-native T2 composition — "morning-after scandal" scene. Produce a believable short-drama publicity photograph, not a polished fashion image or rendered poster.

**Key quality signal: specify a real camera + scene-appropriate lens.** Use `35mm f/4` for 3–4-person conflict so hands, evidence, and all faces remain readable; use `50mm f/2.8` for Solo/Duo. Avoid `85mm f/1.4` for ensembles because shallow focus and portrait compression encourage prestige posing and blur supporting reactions. Do not use `cinematic drama still` or `film-still` unless the user requests that treatment.

Use for any contemporary romance / billionaire cover at T2 tier:

```
photorealistic short-drama publicity photography, looks like a real on-location photograph,
shot on Canon EOS R5 with 50mm f/2.8 lens, natural skin texture with visible pores and real imperfections,
real hair strands with natural weight and movement, candid unposed capture,
NO CGI NO 3D render NO illustration NO painting NO anime NO cartoon NO digital art NO artwork,
luxury penthouse bedroom, floor-to-ceiling windows with city skyline at dawn, warm golden morning light,

female lead [ethnicity] [hair], late 20s, bare shoulders,
clutching white bedsheet to chest with both hands,
wide [eye color] eyes looking off-camera with shocked expression, lips slightly parted,
positioned large in foreground filling 65% of frame height, hair slightly dishevelled,

male lead [ethnicity] [hair], late 20s to mid-30s, casual [color] open-collar shirt with stubble,
seated on bed behind her, watching her with quiet intensity, positioned smaller in mid-ground, slightly soft-focus,

white linen bedding, warm amber morning light, shallow depth of field bokeh,
photorealistic candid drama photograph, no text, no watermark, 9:16 vertical
```

Substitute `[ethnicity]`, `[hair]`, `[eye color]` from the book's `character-visuals.md`.

---

## Step 2 — Build the text-free art prompt

Write the image-generation prompt in English and keep it **strictly text-free**. Do not create a title/author/hook/typography composition spec for the raster asset. The image prompt must explicitly forbid all readable text and branding.

```
[Genre style from cover-styles.md].
[Frozen scandal, cast actions/reactions, and proof object from Prompt assembly].
[genre style tags]. [character description]. [background description].
[color palette]. [lighting].
photorealistic short-drama publicity photography, looks like a real on-location photograph, shot on Canon EOS R5 with 35mm f/4 lens for ensemble scenes or 50mm f/2.8 for one to two people, natural skin texture with visible pores, all required faces in focus, real hair strands with natural movement, caught mid-action, NO CGI, NO 3D render, NO illustration, NO painting, NO anime, NO cartoon, NO digital art, NO artwork, portrait [ratio] ratio,
clean top and lower safe zones, no text, no letters, no logo, no watermark
```

Text handling: none inside the image. Do not ask the image model or cover compositor to render title, author, hook, subtitle, genre/status label, logo, watermark, signage, UI, or readable lettering. If a consuming page needs copy, it must render it outside the raster asset.

**Character count — use the composition type assigned in Step 1.6:**

| Composition type | Characters | Notes |
|---|---|---|
| **Solo** | 1 (protagonist) | Powerful solo poses: dramatic expression, environment-forward. Valid for any genre when the protagonist's arc stands alone. |
| **Duo** | 2 (two leads) | Two-character focus; romance, drama, fantasy duo, detective pair, or allies. Describe both explicitly. |
| **Trio** | 3–4 | Love triangle, rival figure, pack/court conflict. Keep a clear focal pairing; the third or fourth figure must have a distinct relationship role. |
| **Environmental** | 1–2, small against scene | Figure(s) partially subsumed by the dramatic environment. Best for thriller/mystery/gothic. |

For a Status / Case Unlocked cover, build a text-free image-only scene. Preserve the project hard cap of exactly 3 discernible adults.

**Genre defaults when Step 1.6 has not been run (single-book mode):**

Roll a random number 1–4 to pick composition. Romance bias: Duo at 1–2, Solo at 3, Trio or Environmental at 4.

| Genre | Composition pool (roll 1–4) |
|---|---|
| Urban Drama / Contemporary Romance / Historical Court Drama | 1–2 → Duo; 3 → Solo (protagonist only, strong atmospheric); 4 → Trio or Environmental |
| Dark Fantasy / Paranormal | 1 → Duo; 2–3 → Trio; 4 → Environmental |
| Thriller / Mystery | 1–2 → Environmental; 3 → Solo; 4 → Duo |
| Horror | 1–3 → Environmental or Solo; 4 → Duo (danger/threat) |
| Sci-Fi / Dystopian | 1–2 → Solo; 3 → Environmental; 4 → Duo |
| Cultivation Fantasy / War Epic | 1–2 → Solo; 3 → Trio; 4 → Environmental |
| Isekai / Slice of Life | 1 → Solo; 2–3 → Duo; 4 → Trio |

**Do not default to Duo.** Across any set of books on the same site, no more than 40% (rounded down) should be Duo. If the roll would produce a third Duo on a 5-book site, reroll once and take any non-Duo result.

**A third figure adds more tension than a clean two-person embrace** when the synopsis offers it. Keep one clear focal pairing; place the third figure to threaten or intrude (watching from behind, reaching between them, turned away in betrayal).

**Ethnicity — MANDATORY for all character descriptions:** Always derive ethnicity from the novel's worldbuilding and synopsis. Never default to any specific ethnicity. Never omit ethnicity entirely — Doubao defaults to East-Asian features without explicit guidance. Examples of correct phrasing:
- `Caucasian woman, Western European features, light skin`
- `Latina woman, olive skin, dark hair`
- `Black woman, deep brown skin, natural curls`
- Match exactly what the story says. If the worldbuilding is ambiguous, pick the most narratively fitting option and record it in `character-visuals.md`.

**Cover cast rule — MANDATORY:** the cover must show the protagonist and the book's major supporting character(s). A cover that only shows the protagonist is not acceptable when the story has a central love interest, antagonist, rival, partner, handler, court figure, pack alpha, vampire lord, AI counterpart, or other premise-defining secondary character. Use the smallest composition that includes the full required cast:
- 1 protagonist + 1 major counterpart → **Duo**.
- 1 protagonist + 2 major counterparts/rivals → **Trio**.
- Larger ensemble → protagonist and top 2–3 major supporting characters visible, with extras implied by setting only.

The hard maximum is 4 discernible people on the final cover. Never add generic extras to make the scene feel busy, and never include the full story ensemble when 3–4 roles communicate the conflict.

The diversity plan may vary pose, framing, palette, and environmental dominance, but it may not remove required characters. If Step 1.6 assigned Solo or Environmental and the cast list contains major supporting characters, upgrade the composition to Duo/Trio or use an Environmental composition with all required figures visible inside the scene. Do not accept a cover where a major supporting character is absent, hidden by crop, reduced to an unreadable silhouette, or replaced by a generic figure.

**Character identity persistence:** the prompt must include stable visual anchors for every required character — hair color/length, eye color or gaze quality, build, age range, signature clothing/status marker, and role in the power dynamic. These same anchors must be preserved for later illustrations.

**Figure rule — apply by genre:**

**Romance / romance / Contemporary Drama (T2–T4, roll per cover):**
The female character must be visually magnetic — impossible to scroll past. **Allure tier = randomly T2, T3, or T4, picked independently per cover** — roll once per book and bake that tier's assembly block from the Exposure Tiers table (`references/cover-allure-elements.md`) directly into the prompt. Required elements by tier. In this reference, **exposure** without a `T` number always means image luminance; `T2–T4` means allure/clothing tier.

| Element | T2 (Bold) | T3 (Maximum) | T4 (Limit) |
|---------|-----------|--------------|------------|
| **Clothing** | Deep neckline + bare back/midriff/high slit — two simultaneous revealing elements | Garment failing in multiple places: torn, slipped, soaked, or sheer — the garment is losing | Clothing has already left — one nominal draping element only (silk sheet corner, sheer panel, wisp of fabric) |
| **Skin** | Cleavage + one secondary zone | Three or more zones simultaneously (bare back, legs, midriff, shoulders, extreme neckline) | Every zone simultaneously except §0-protected; frame reads as total skin with a single covered point |
| **Figure** | `voluptuous hourglass figure, slim toned waist dramatically cinched, large full bust dramatically prominent, E-cup figure, long shapely legs` | Same figure — drop explicit `E-cup`, use visual-effect phrasing only | Same figure, described through what the drape reveals rather than the figure itself |
| **Model** | **gpt-image-2-all primary** (doubao fallback) — T2 is GPT's natural ceiling; direct it toward candid short-drama action | doubao primary (GPT hard-rejects T3 fabric-failure/soaked/torn language) | doubao primary only — **do not attempt gpt at T3 or T4** (hard rejection); nano as terminal fallback |

- Pose: use the pose assigned in Step 1.6 (batch) or pick freely from the Poses table (single-book). From-behind poses cap at 2 per site.
- Framing: state explicitly in every prompt. Never allow the model to default to a face-only crop.
A modest, fully-clothed, non-contact composition is a quality gate failure for romance/drama. Allure tier is stochastic — bake in higher-tier fragments, never accept a weak roll. Hard floor: no nipples, no genitals, no sex acts (§0 in `cover-allure-elements.md`). Everything above that floor: push it. The allure tier never authorizes overexposure or weakening the frozen conflict.

**Fantasy / Paranormal / Historical (T1–T2, physique-forward):**
Figure should read as powerful, magnetic, and physically present — not demure or neutral. Describe body type in genre-appropriate terms: `athletic and lithe`, `commanding presence, tall and broad-shouldered`, `ethereal beauty, slender and graceful`. Include at least one deliberate skin detail (bare shoulder, exposed collarbone, fitted bodice, wind-pulled skirt). Clothing should be atmospheric and body-conscious — flowing but structured, battle-worn but fitted.

**Mystery / Gothic Thriller / Horror (T1, atmosphere-dominant):**
Figure reads as striking and unsettling, not conventionally alluring. Describe posture, tension in the body, pale skin at throat or collarbone, dishevelled or soaked hair, a garment that conveys vulnerability or power (not both). The body is present and magnetic but the magnetism comes from the mood, not the exposure level. Never fully covered, featureless, or portrait-cropped to face only.

**Sci-Fi / Dystopian (T1, fit + utilitarian):**
Figure is lean-athletic, not domestic-soft. Form-fitting tactical or functional clothing. At least one skin-visible detail: bare forearms, cropped jacket, midriff gap under armour. Pose carries agency — not decorative. Never passive or posed-for-beauty.

**Drama rule — MANDATORY (see Drama Hook section in `cover-allure-elements.md`):** allure without drama is a fashion photo, not a book cover. Every prompt must include:
- A specific emotional expression from the Expression Rules table (never neutral/pleasant)
- A visible power dynamic between the central characters (and any added third figure)
- At least one environmental element that amplifies the emotional stakes
- The "one-second test": a viewer must feel something — not just notice someone attractive

Title font styles and author name styles are in `references/cover-styles.md` per genre.
Default composition: **full-body or medium shot** — both figures visible from hip to crown minimum. Close-up portrait (face and chest only) is a secondary variant, not the default. Pure scene (no figures) only for thriller/horror genres.

## Step 3 — Generate cover

Set the temporary output path and final asset paths before running:

```bash
COVER_TMP="/tmp/cover_${bookSlug}_v1.png"
WEBP_OUT="public/covers/${bookSlug}.webp"
JSON_OUT="public/covers/${bookSlug}.json"
mkdir -p "public/covers"
```

Use `COVER_TMP` as `OUTPUT_PATH` in the apiyi generator below.

### Model capability ranking (cascade order)

Four apiyi models are viable for covers. **GPT is primary** for T1/T2 — use on-location photography language, explicit actions, and reaction chains so the result reads as a real short-drama incident rather than a rendered or fashion image. The generator tries them **in this order** and falls through to the next on any failure:

| Rank | Model | Size | Response | Notes |
|---|---|---|---|---|
| 1 (primary, T1/T2) | `gpt-image-2-all` | `848x1280` | `b64_json` (PNG) | **Primary.** Use `Canon EOS R5, 35mm f/4` for 3–4-person conflicts so every face and hand stays readable; use `50mm f/2.8` for Solo/Duo. Ask for real skin, natural hair, caught-mid-action energy, and all required faces in focus. Clean output, no watermark. Max safe tier: T2. Hard-rejects T3/T4 fabric-failure, soaked-clinging, torn-garment language — skip it for T3/T4 covers. |
| 2 (fallback, T1/T2 only) | `gemini-3.1-flash-image-4k` | `1664x2496` | `b64_json` (raw, no prefix) | **Fallback when GPT fails/times out on T1/T2.** Free-form sizing, no watermark, true 4K. Not used for T3/T4 — its tolerance for fabric-failure/torn/soaked language is unverified and likely shares GPT's rejection behavior. |
| 3 (fallback) | `doubao-seedream-5-0-260128` | `1664x2496` | `url` (JPEG) | **Primary for T3/T4; fallback for T1/T2 when GPT and Gemini both fail.** Most permissive content filter. **Stamps an `AI生成` watermark in the bottom-right corner — must crop it (see post-process).** |
**nano-banana-pro — terminal blank-prevention fallback:**
- Silently downgrades T3+ prompts to ~T1 output; square 1024×1024 (wrong aspect ratio for covers — reframe to 2:3 after generation).
- Use only when gpt (×2) and doubao both fail.

### apiyi path

```bash
mkdir -p public/covers
PROMPT_JSON=$(printf '%s' "$PROMPT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))')

# Generic generator: handles both b64_json (PNG) and url (JPEG) responses.
# Returns 0 on success (file written), non-zero on any failure.
gen_cover_apiyi() {
  local model="$1" size="$2"
  SIZE="$size"
  curl -s --max-time 300 https://api.apiyi.com/v1/images/generations \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $APIYI_API_KEY" \
    -d "{\"model\":\"$model\",\"prompt\":$PROMPT_JSON,\"size\":\"$size\"}" \
  | OUTPUT_PATH="$OUTPUT_PATH" python3 -c "
import sys, json, base64, os, urllib.request
output_path = os.environ['OUTPUT_PATH']
raw = sys.stdin.read()
if not raw.strip():
    print('ERROR: empty response (timeout)'); sys.exit(1)
data = json.loads(raw)
if 'error' in data:
    msg = data['error']['message'] if isinstance(data['error'], dict) else str(data['error'])
    print('API_ERROR:' + msg); sys.exit(2)
if not data.get('data'): print('SOFT_REJECT: empty data array (model declined silently)'); sys.exit(2)
item = data['data'][0]
if item.get('b64_json'):
    b64 = item['b64_json']
    if ',' in b64: b64 = b64.split(',', 1)[1]
    with open(output_path, 'wb') as f: f.write(base64.b64decode(b64))
elif item.get('url'):
    urllib.request.urlretrieve(item['url'], output_path)
else:
    print('UNKNOWN_FORMAT:' + str(list(item.keys()))); sys.exit(3)
print('SAVED:' + str(os.path.getsize(output_path)))
"
}

# Capability cascade — GPT primary (cinematic drama still quality); gemini/doubao fallback
# GPT max safe tier: T2 (bare shoulders + concealing element). Skip GPT entirely for T3/T4 (hard rejection).
if   [ "$TIER" = "T3" ] || [ "$TIER" = "T4" ]; then
  # T3/T4: go straight to doubao (GPT and gemini both reject fabric-failure/torn/soaked language)
  gen_cover_apiyi "doubao-seedream-5-0-260128" "1664x2496" && MODEL_USED="doubao-seedream-5-0-260128" || \
  gen_cover_apiyi "doubao-seedream-5-0-260128" "1664x2496" && MODEL_USED="doubao-seedream-5-0-260128" || \
  gen_cover_apiyi "nano-banana-pro"            "1024x1024" && MODEL_USED="nano-banana-pro" || \
  { MODEL_USED=""; echo "ALL_MODELS_FAILED — skipping book"; }
else
  # T1/T2: GPT first (candid short-drama incident), gemini fallback (no watermark, true 4K), doubao last
  if   gen_cover_apiyi "gpt-image-2-all"            "848x1280";  then MODEL_USED="gpt-image-2-all"
  elif gen_cover_apiyi "gpt-image-2-all"            "848x1280";  then MODEL_USED="gpt-image-2-all"           # retry once
  elif gen_cover_apiyi "gemini-3.1-flash-image-4k"  "1664x2496"; then MODEL_USED="gemini-3.1-flash-image-4k"
  elif gen_cover_apiyi "doubao-seedream-5-0-260128" "1664x2496"; then MODEL_USED="doubao-seedream-5-0-260128"
  elif gen_cover_apiyi "nano-banana-pro"            "1024x1024"; then MODEL_USED="nano-banana-pro"
  else MODEL_USED=""; echo "ALL_MODELS_FAILED — skipping book"
  fi
fi
echo "MODEL_USED=$MODEL_USED"

# Save metadata JSON alongside the final WebP (flat path)
printf '{"model":"%s","size":"%s","prompt":%s}\n' \
  "$MODEL_USED" "$SIZE" \
  "$(printf '%s' "$PROMPT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))')" \
  > "$JSON_OUT"
```

**Post-process by model used (final target: ~848×1280 true 2:3 portrait; final WebP ≤ 300 KB):**
- `gpt-image-2-all` → already 848×1280 PNG; no resize needed. Final WebP conversion happens in Step 3.5.
- `gemini-3.1-flash-image-4k` → requested at `1664x2496` (2:3, no watermark); resize down to 848×1280:
  ```bash
  sips -z 1280 848 "$OUTPUT"                  # resize to 848x1280 (2:3)
  ```
- `doubao-seedream-5-0-260128` → crop the bottom-right `AI生成` watermark, then resize to 848 px wide (maintaining 2:3):
  ```bash
  sips -c 2321 1664 "$OUTPUT"                 # crop ~7% from bottom to clear watermark, output stays ~1664x2321
  sips -z 1280 848 "$OUTPUT"                  # resize to 848x1280 (2:3)
  ```
- `nano-banana-pro` → output is square 1024×1024; center-crop width to get 2:3, then resize up to 848×1280:
  ```bash
  sips -c 1024 683 "$OUTPUT"                  # crops to 683x1024 (2:3), centered
  sips -z 1280 848 "$OUTPUT"                  # resize to 848x1280
  ```
  Note: nano silently downgrades T3+ to ~T1 allure.

**Final format — flat WebP + JSON only (see Step 3.5):**
- Every shipped cover is lossy **WebP at quality 78**, served as `/covers/{slug}.webp`. This is the single delivery format — no JPEG, no PNG, no format branching, no subfolders.
- Metadata lives next to it as `/covers/{slug}.json`.
- The temporary `cover_v1.png` is deleted immediately after conversion; do not keep it in `public/`.

**If the whole cascade fails on content safety** (`API_ERROR` containing `invalid_prompt` / `safety` / `rejected` from the primary, and the fallbacks also reject): replace triggering terms in `$PROMPT` and re-run the cascade once:

| Replace | With |
|---|---|
| `bare back exposed` | `off-shoulder gown, collarbone catching the light` |
| `exposed breast`, `topless`, `naked`, `nude` | `off-shoulder`, `elegant neckline`, `décolletage` |
| `bodies pressed flush together` | `close proximity, charged tension` |
| `gripping her hip`, `hand on her bare hip` | `hand at her waist` |
| `wet transparent fabric`, `see-through wet` | `rain-soaked fabric, damp clothing` |
| `clinging to and outlining every curve` | `rain-soaked clothing pressed against her silhouette` |
| `lips pressed against` | `faces close, the moment before` |
| `erotic`, `sexual`, `explicit` | `alluring`, `intimate atmosphere`, `romantic tension` |

Re-run the full cascade once with the softened prompt. If every model (gpt → gemini → doubao ×2 → nano) still fails, **skip the book and continue the batch** — no SVG fallback.

On any other API error: log the response, skip this book, continue batch.

### Terminal fallback — nano (no SVG)

The cascade ends at `nano-banana-pro`. There is **no SVG fallback**:
- If `APIYI_API_KEY` is not set → skip the cover (warning + continue).
- If nano also fails → skip the book, log the reason, continue the batch.
- A nano result is usable as-is — reframe to 2:3 after generation.
- Never write a styled `.svg` cover.

### B3 batch flow

**Generate all books in parallel** — one background process per book, then `wait`. Build the prompt inline per book — do not pre-build a map:

```bash
mkdir -p public/covers
for bookSlug in "${BOOKS[@]}"; do
  (
    COVER_TMP="/tmp/cover_${bookSlug}_v1.png"
    WEBP_OUT="public/covers/${bookSlug}.webp"
    JSON_OUT="public/covers/${bookSlug}.json"
    # Steps 1.5 + 2: detect genre, roll T2/T3 tier, build PROMPT string for this book
    PROMPT="$(build_cover_prompt "$bookSlug")"  # inline per Step 2 template
    # Step 3: apiyi cascade (gpt → doubao → nano); skip on no key / total failure
    # Step 3.5: convert COVER_TMP → WEBP_OUT, write JSON_OUT, rm COVER_TMP
  ) > "/tmp/cover_${bookSlug}.log" 2>&1 &
done
wait
rm -f /tmp/cover_*.log
```

`build_cover_prompt` is not a real function — it represents executing Steps 1.5 and 2 inline for each book before the curl call.

## Step 3.5 — Convert the cover to WebP

Run immediately after Step 3, before quality check. Do not skip. This produces the final shipped assets: `public/covers/{book-slug}.webp` (flat path, lossy WebP q78) and `public/covers/{book-slug}.json`. The temporary `cover_v1.png` is deleted after conversion — it is not a deliverable.

```bash
# Convert one cover PNG → final flat WebP at q78. Prefer cwebp; fall back to Pillow.
to_webp_cover() {
  local src="$1" dst="$2" q="${3:-78}"
  if command -v cwebp &>/dev/null; then
    cwebp -quiet -q "$q" "$src" -o "$dst"
  else
    python3 -c "from PIL import Image; im=Image.open('$src'); im.save('$dst','webp',quality=$q,method=6)"
  fi
}

COVER_TMP="/tmp/cover_${bookSlug}_v1.png"
WEBP_OUT="public/covers/${bookSlug}.webp"
JSON_OUT="public/covers/${bookSlug}.json"
if [ -f "$COVER_TMP" ]; then
  if ! command -v cwebp &>/dev/null && ! python3 -c "import PIL" &>/dev/null; then
    brew install webp -q || echo "⚠ cwebp install failed — install webp or Pillow"
  fi
  BEFORE=$(stat -f%z "$COVER_TMP" 2>/dev/null || stat -c%s "$COVER_TMP")
  to_webp_cover "$COVER_TMP" "$WEBP_OUT" 78
  AFTER=$(stat -f%z "$WEBP_OUT" 2>/dev/null || stat -c%s "$WEBP_OUT")
  if [ "$AFTER" -ge "$BEFORE" ]; then
    # WebP larger than source — keep original, skip WebP
    rm -f "$WEBP_OUT"
    cp "$COVER_TMP" "$WEBP_OUT"
    echo "⚠ webp larger than src (${AFTER}B ≥ ${BEFORE}B) — kept original"
  else
    echo "✓ webp q78: ${BEFORE}B → ${AFTER}B (-$(( (BEFORE-AFTER)*100/BEFORE ))%)"
  fi
  rm -f "$COVER_TMP"   # remove the intermediate PNG; only WebP + JSON remain
fi
```

**Never use lossless WebP** (`cwebp -lossless` / `Image.save(..., lossless=True)`) — on photographic covers it is ~3× *larger* than the source PNG. Always lossy q78. WebP q78 brings AI covers to ~50–80 KB with no visible loss at display size (well under the ≤ 300 KB cap). If a cover is still > 300 KB after conversion, resize to 683×1024 and re-convert.

For **batch mode**, run this loop after all covers are generated:

```bash
for bookSlug in "${BOOKS[@]}"; do
  COVER_TMP="/tmp/cover_${bookSlug}_v1.png"
  WEBP_OUT="public/covers/${bookSlug}.webp"
  JSON_OUT="public/covers/${bookSlug}.json"
  # same to_webp_cover call as above with COVER_TMP / WEBP_OUT / JSON_OUT set per book
  # then: rm -f "$COVER_TMP"
done
```

---

## Step 4 — Quality check

| Check | Standard |
|---|---|
| Frozen conflict | Specific scandal is understandable without title or synopsis |
| Reaction chain | Every face has a distinct role/emotion; at least 2 are unmistakably exaggerated for ensemble drama |
| Proof object | Large and recognizable at 160px thumbnail width |
| Visible cast | 1–4 discernible people; ensemble conflicts normally use 3–4; count faces inside photos/screens too |
| Exposure | Normal mid-key by default; no crushed shadow mass, blown skin/whites, or global black/white veil |
| Image text | No generated or composited words, letters, logos, watermarks, UI, or readable signage anywhere in the raster asset |
| UI integration | No duplicate genre chip, collision, unintended crop, or overlay introduced by the card component |
| Genre match | Setting and conflict match the book's actual primary genre; do not label every story romance |
| Ratio correct | 2:3 portrait |

### Mandatory acceptance sequence

1. Verify file exists, decodes, is 2:3 portrait, and is ≤300 KB.
2. Run the exposure gate on the **final WebP**.
3. Render or inspect the cover at full size and at 160px width.
4. Inspect the actual site card at desktop and mobile breakpoints when the cover is already integrated.
5. Write a one-line QA record: `event | cast count | expressions | proof | exposure metrics | UI collisions`.

**Never mark a cover passed from dimensions alone.** Retry with a corrected prompt or corrected deterministic overlay based on the failed gate:

- Wrong/missing people, weak expressions, unclear event, or bad proof → regenerate the art.
- Correct art but dark/white veil or crop collision → fix the image-only composition; do not add a text layer.
- Text generated inside the art → regenerate text-free or inpaint/remove it; never accept or preserve it.
- Retry once per distinct failure mode. If it still fails, log the exact failed gate and exclude the cover from delivery rather than silently accepting it.

### Batch QA matrix

Before delivery, inspect the covers together in display order. Reject the batch when:

- every cover uses the same room, palette, gesture, or evidence object;
- every cover sits at the same exposure extreme;
- adjacent covers are visually interchangeable at 160px;
- any row reads as prestige movie posters instead of scandal scenes;
- any cover relies on a title to explain what is happening;
- the raster asset contains any image-baked label, title, hook, logo, watermark, or UI.

## Output Location

```
public/covers/{book-slug}.webp  ← cover image (lossy WebP q78), served as /covers/{book-slug}.webp
public/covers/{book-slug}.json  ← metadata: model, size, prompt
```

No subfolders are created under `public/covers/`. The temporary `cover_v1.png` is written to `/tmp/cover_{book-slug}_v1.png`, converted to WebP, and deleted in the same phase.

JSON format:
```json
{ "model": "gpt-image-2-all", "size": "848x1280", "prompt": "..." }
```

Served from `public/` — no CDN needed. The site builder reads `Book.cover` as `/covers/{book-slug}.webp`.

After generation, write the JSON alongside the WebP:
```bash
printf '{"model":"%s","size":"%s","prompt":%s}' \
  "$MODEL_USED" "$SIZE" \
  "$(printf '%s' "$PROMPT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))')" \
  > "public/covers/${bookSlug}.json"
```

Note: the old `cover_v1.prompt.txt` file is no longer used — prompt is stored in the JSON.

Site logo and favicon are **not** part of this phase. They are generated in B2 (Design Identity) via `references/design-system.md`.
