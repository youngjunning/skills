# Portrait / Illustration

Use for portraits, editorial illustrations, book covers, banners, hero images, product-style visuals, and general single-image requests that do not need transparency, wallpaper packaging, or multi-frame output.

Load first:
- `references/generation.md`
- `references/prompt-compliance.md`
- `references/post-process.md`

---

## Defaults

| Field | Value |
|---|---|
| Output directory | `~/Pictures/better-imagegen/` |
| Final format | `.webp` |
| Quality | q78 |
| Primary size | `848x1280` |
| Model flow | GPT Image 2.6 |

Use user-requested aspect ratio when clear. Otherwise choose:
- Portrait / cover: `848x1280`
- Square social image: `1280x1280`
- Landscape / banner: `1280x720`

---

## Prompt Requirements

For ATA and technical-article covers, load `references/qingshan-lake-style.md` and default to Qingshan Lake Light. Do not infer people, anime styling, or a recurring identity ensemble from the subject, repository, or earlier series artwork; those require an explicit current request.

Normalize the outbound prompt through `references/prompt-compliance.md`, then write a complete scene prompt with:
- subject
- setting
- composition
- lighting
- camera or illustration style
- mood
- exclusions: `no text, no watermark, no logo unless requested`

For book covers or ad creatives, make the image scroll-stopping in 0.3 seconds: clear emotion, strong foreground subject, readable world signal.

---

## Pipeline

```bash
OUT_DIR="$HOME/Pictures/better-imagegen"
mkdir -p "$OUT_DIR"
OUTPUT_PATH="/tmp/image_output.png"
FINAL_PATH="$OUT_DIR/${OUTPUT_NAME:-image}.webp"

SIZE="${REQ_SIZE:-848x1280}"
if   GEN_LOG=$(gen_image_apiyi "$MODEL_GPT"    "$SIZE"      "$OUTPUT_PATH"); then MODEL_USED="$MODEL_GPT"
else echo "GPT_IMAGE_GENERATION_FAILED"; exit 1
fi

GENERATION_MS=$(printf '%s\n' "$GEN_LOG" | awk -F: '/^ELAPSED_MS:/{v=$2} END{print v+0}')
RESPONSE_FORMAT=$(printf '%s\n' "$GEN_LOG" | awk -F: '/^RESPONSE_FORMAT:/{v=$2} END{print v}')

POSTPROCESS_NOTE="direct webp q78"
to_webp "$OUTPUT_PATH" "$FINAL_PATH" 78
rm -f "$OUTPUT_PATH"
write_image_metadata "$FINAL_PATH" "${FINAL_PATH%.*}.json" "$MODEL_USED" "$SIZE" "$GENERATION_MS" "$RESPONSE_FORMAT" "$POSTPROCESS_NOTE"
print_image_summary "${FINAL_PATH%.*}.json"
open "$FINAL_PATH"
```
