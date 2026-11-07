# Image Edit (图生图 / img2img)

Use when the user provides an existing image and wants a faithful variation: refine, upscale-with-redraw, style-preserving cleanup, pose change on the same character, or any "不要大改形象 / 保持原样但更精致" request.

Key insight: text-to-image regeneration ALWAYS drifts the character design, no matter how detailed the prompt. When the user says the character/subject must stay the same, use the **edits endpoint** with the original image as reference — never regenerate from text alone.

## Reference-role contract

Classify each supplied image before editing:

- **Edit target:** the image whose pixels or composition will change.
- **Identity reference:** the authoritative subject appearance. Requests such as “人物形象要保留”, “参考一样”, “保持这个人物”, “只改文字”, or “不要换角色” make the supplied image an identity reference even when it also supplies a visual style.
- **Style reference:** supplies only general line, palette, lighting, texture, or era cues; subject identity may be original.

Identity preservation outranks style translation. Lock the referenced face, hair silhouette, costume and color blocks, body proportions, pose, expression, character count, relative placement, task props, and overlap order unless the user explicitly allows one of them to change. Do not substitute a newly generated “similar” character.

If an identity reference mentioned by the user is unavailable as a local path or usable conversation image, stop and ask for reattachment. Do not use memory, a textual description, a low-resolution screenshot, or a previous model-generated approximation as the identity source.

When the edit target is a poster, timeline, architecture diagram, knowledge map, or other layered visual and the requested change affects only text or diagram semantics:

1. Keep the approved character/background raster as a locked layer.
2. Edit the native HTML/CSS/SVG/text overlay deterministically when available.
3. Re-render and compare the locked region with the approved source before final encoding.
4. Use the image edits endpoint only when the requested pixel change cannot be isolated with the native source.

Do not spend an image API call on a text-only correction when deterministic overlay editing can preserve identity exactly.

Load first:
- `references/generation.md`
- `references/prompt-compliance.md`
- `references/post-process.md`

---

## Endpoint

`POST https://api.apiyi.com/v1/images/edits` — multipart form (NOT JSON). Load the model setup from `references/generation.md` first; editing uses the same Sunburst model and high quality as generation:

```bash
curl -s --max-time 300 "https://api.apiyi.com/v1/images/edits" \
  -H "Authorization: Bearer $APIYI_API_KEY" \
  -F "model=$MODEL_GPT" \
  -F "quality=$QUALITY_GPT" \
  -F "image=@input.png" \
  -F "prompt=$PROMPT" \
  -F "size=1280x1280"
```

Response is the same shape as generations: `data[0].b64_json` or `data[0].url`. Reuse the same Python extraction block from `gen_image_apiyi` in `references/generation.md`.

Notes:
- `image` accepts PNG with alpha; small inputs (e.g. 96px pixel art) work fine.
- Requested `size` is approximate — actual output may differ (e.g. 1254×1254 for 1024×1024 request). Always measure the real output.
- The model usually bakes a background (white or checkerboard) even when asked for transparency. Plan for background removal in post-processing — ask for "plain solid white background" in the prompt to make removal trivial, rather than fighting for real alpha.

---

## Prompt Template (faithful refinement)

The prompt must both describe the invariants explicitly AND forbid the common drift directions:

```text
Faithfully redraw this exact same <subject> at higher fidelity.
Keep the IDENTICAL character design: <enumerate concrete invariants — body shape,
proportions, eyes, palette hex, pose, style era>.
Keep the <style> and the cute/kawaii feeling — do NOT make it realistic,
do NOT add gradients or extra shading detail, do NOT change proportions.
Only <the single allowed change, e.g. "make the pixel edges slightly cleaner">.
Plain solid white background, no text, no border.
```

Enumerating invariants matters: "keep it the same" alone still drifts; listing "same blocky square body, same two ear tufts, same big round dot eyes, same warm amber-orange palette" holds the design.

### Direct eye-contact edits

Read `references/eye-gaze-edit.md` for the complete eye-part terminology, pupil-only workflow, locked-raster recovery rules, and QA/metadata contract. In particular, the black central region is the pupil, the colored region is the iris, and white dots are catchlights; never move the entire iris when the user asks to move the black region.

Do not rely on `look at the viewer`, `front-facing`, `centered eyes`, or `symmetrical pupils` alone. Models can satisfy those phrases while placing both pupils high inside the irises, producing an upward gaze. Use an anatomical position contract:

```text
Change only the gaze. Keep the head facing the camera. In each eye, place the dark
pupil body at the horizontal and vertical center of its colored iris, with balanced
iris clearance above and below and matching normalized pupil positions in both eyes.
Both visual axes converge on the camera lens. The white catchlights remain reflections
and do not define gaze. Do not place the pupils in the upper third of the irises. No
upward gaze, side glance, eye roll, looking past the viewer, or off-camera focus.
```

Run the shared `Direct-gaze hard gate` in `SKILL.md` after generation. A centered face, symmetric eye outlines, or similar catchlights are insufficient evidence. Inspect the dark pupil body inside each iris at 4× or greater before marking the edit as passed.

The current Sunburst integration has not verified mask-based inpainting. Do not invent a mask-based guarantee, and do not locally translate a generic circular/elliptical pupil patch in a flattened antialiased mascot image; those approaches can leave visible seams or overwrite eyelids, sclera, muzzle, fur, or feathers. After the permitted edit and one same-model correction fail, preserve the source. Only route to a fresh generation when the user has prioritized correct gaze over exact identity continuity, and record that tradeoff in metadata.

For multi-character references, enumerate invariants per character and then lock ensemble invariants: character count, left-to-right order, foreground/background depth, overlaps, gaze direction, and task interaction. A result that preserves the style but changes one person is an identity failure.

---

## Batch: animation frames / multi-image edits

For frame sequences (e.g. a 6-frame menu bar sprite), edit each source frame in a parallel background process, one edits call per frame. Describe that frame's pose in its prompt so the model doesn't "correct" the pose toward a neutral one:

```bash
POSES=("wings fully tucked down" "wings slightly lifted" "wings at mid height" \
       "wings fully spread upward" "wings coming back down" "wings almost tucked")
for i in 0 1 2 3 4 5; do
  ( curl ... -F "image=@$SRC_DIR/frame-$i.png" \
      -F "prompt=... same wing pose as the input image (${POSES[$((i+1))]}) ..." \
      ... ) &
done
wait
```

Caveat: independently edited frames have slight frame-to-frame jitter (eye shape, outline width). At menu-bar size (~22px) this is invisible or reads as natural blinking. If jitter is unacceptable, fall back to the sprite-sheet flow in `references/sprite-loop.md` (better inter-frame consistency, worse fidelity to the original design).

---

## Post-processing pipeline

1. **Background removal** — use `"$BETTER_IMAGEGEN_PYTHON" scripts/ensure_transparent.py input.png output.png`. It handles solid black, white, gray, or tinted backgrounds by sampling the four corners and only clearing matching edge-connected pixels. Use `--edge-mode pixel` for pixel art; use the default soft mode for hair, fur, feathers, fringe, glass, smoke, or antialiased art. Do not use the older near-white-only flood fill for transparency-critical output.

```python
from PIL import Image
from collections import deque

def remove_bg(im):
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    def is_bg(p):
        r, g, b, a = p
        return a == 0 or (r > 200 and g > 200 and b > 200 and abs(r-g) < 18 and abs(g-b) < 18)
    seen = [[False]*w for _ in range(h)]
    q = deque()
    for x in range(w):
        for y in (0, h-1):
            if is_bg(px[x, y]) and not seen[y][x]:
                seen[y][x] = True; q.append((x, y))
    for y in range(h):
        for x in (0, w-1):
            if is_bg(px[x, y]) and not seen[y][x]:
                seen[y][x] = True; q.append((x, y))
    while q:
        x, y = q.popleft()
        px[x, y] = (0, 0, 0, 0)
        for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and is_bg(px[nx, ny]):
                seen[ny][nx] = True; q.append((nx, ny))
    return im
```

2. **Crop + center** — `im.crop(im.getbbox())`, then paste centered on a square transparent canvas with ~12% margin (`side = int(max(im.size) * 1.12)`), matching typical icon padding.

3. **Resize** — LANCZOS down to the delivery size (blocks are large after AI redraw, so LANCZOS stays crisp; NEAREST is only for integer-scaling true pixel sources).

4. **Verify alpha** — the script must print `TRANSPARENCY_OK`; additionally preserve its non-zero exit as a hard generation failure. Never deliver an asset merely because its file format supports alpha.
5. **Visual matte QA** — composite a 4× preview over white, black, and checkerboard backgrounds. Inspect fine strands and high-contrast contours for clipping, dark/light halos, matte-color contamination, and excessive feathering. Regenerate against a more contrasting matte when cleanup would require erasing subject-colored pixels.

5. For frame sequences, also emit a `preview.gif` (`duration=100, loop=0, disposal=2`) so the user can eyeball loop smoothness.

Deliver PNG with alpha (not WebP) when the asset is an icon/sprite; write metadata JSON per `references/generation.md`.

## Identity QA gate

Inspect the reference and result side by side at full resolution and intended display size. Reject the result when any locked character changes face shape, eye construction, hair silhouette or color, costume silhouette or color blocks, body proportions, pose, expression, props, placement, overlap order, or count.

For deterministic overlay edits, compare the locked raster region before lossy export and require exact equality. After WebP/JPEG encoding, confirm that any pixel differences are compression-only and produce no visible subject drift. Record the reference path or conversation-image role, locked regions, allowed change, and QA result in metadata.

---

## When NOT to use edits

- Brand-new asset with no source image → generations endpoint (type-specific reference).
- Frame-to-frame consistency matters more than fidelity to an existing design → `references/sprite-loop.md` sprite sheet.
- Pure mechanical upscale where zero design change is acceptable → no API at all; integer-scale locally with PIL `Image.NEAREST`. Offer this first when the user says the image must not change AT ALL — it's free and instant. Only escalate to edits when the user wants "同样的形象但更精致" (same design, slightly refined).
