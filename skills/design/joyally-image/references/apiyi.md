# APIyi — API Reference

Unified image API using only `gpt-image-2.6-sunburst` with explicit `quality=high` for generation and editing. Keep both settings unchanged during retries.

- **Docs:** https://docs.apiyi.com/
- **Provider model guide:** https://help.apiyi.com/chatgpt-images-2-6-gif-reference-flare-sunburst.html
- **Sign up:** https://api.apiyi.com/register/?aff_code=ijv5
- **Base URL:** `https://api.apiyi.com/v1`

## Authentication

`APIYI_API_KEY` is the required bearer token. JSON generation requests use `Content-Type: application/json`; edits use multipart form data.

## GPT Image 2.6 Sunburst

`MODEL_GPT` and `QUALITY_GPT` in `references/generation.md` are the shared settings for both endpoints.

- **Provider model ID:** `gpt-image-2.6-sunburst`.
- **Verified 2026-11-07:** generation with `quality=high` and `size=1280x720` returned a decodable image at exactly 1280×720 in 37.57 seconds. Editing with the same quality and `size=1280x1280` returned exactly 1280×1280 in 43.96 seconds. Both returned `b64_json`; the edit preserved the reference scene while adding the requested scarf.
- **Evidence limits:** these smoke tests establish accepted parameters and working endpoints, not long-term uptime, quality superiority, or a full size matrix.
- **Sizes:** use type-specific request defaults, measure actual dimensions, and handle explicit unsupported-size errors. The previous 2.5 preset table is not a verified 2.6 contract.
- **Unverified in this integration:** native animated GIF, SVG, mask/markup inpainting, the full size matrix, batch parameters and pricing. Verify before using or quoting them; do not copy 2.5 pricing or constraints.
- **Timeout:** use at least 300 seconds. Wait for a confirmed error or timeout before retrying.

### Generation

```bash
curl -s --max-time 300 "https://api.apiyi.com/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $APIYI_API_KEY" \
  -d "{\"model\":\"$MODEL_GPT\",\"quality\":\"$QUALITY_GPT\",\"prompt\":\"A ceramic owl beside a paper boat\",\"size\":\"1280x720\"}" \
  -o /tmp/apiyi-image-response.json
```

Use `gen_image_apiyi` from `references/generation.md` for response decoding and metadata. Never print the raw base64 response.

### Editing

Use `POST /v1/images/edits` with multipart fields `model=$MODEL_GPT`, `quality=$QUALITY_GPT`, `image=@reference.png`, `prompt` and `size`. See `references/image-edit.md` for the complete identity-preserving workflow.

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| `429` | Rate limit | Honor Retry-After or back off, retry once |
| `5xx` | Provider/server failure | Keep prompt, model and quality unchanged; retry once. Do not infer a safety rejection or billing outcome from HTTP status alone. |
| Timeout | Exceeded `--max-time` | Increase to 360 s, retry once; then stop and report the failure |
| `error.message` contains `invalid_prompt` / `safety` / `rejected` | Content safety refusal | For permitted content, correct the prompt and retry once; if it still fails, stop and report the refusal |

Allow at most one same-model retry per image request across all failure categories. Preserve the original asset when editing fails.
