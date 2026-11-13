---
name: joyally-spotlight
description: During UI automation, archive key real screenshots privately for later writing; find, redact, and verify product screenshots or demos before sharing.
---

# Joyally Spotlight

Turn an actual product flow into a screenshot or recording that lets a viewer understand what the product does. The result can stand alone or be used in any presentation, document, page, or message. Interface implementation belongs to the product's design and engineering workflow; prose belongs to the writing workflow.

## Choose the deliverable

- **Product screenshot:** show the product state or detail the viewer needs to understand. Capture the whole relevant UI first, then crop to keep context and text readable.
- **Interaction recording:** show a task from input through visible result. Capture the real UI and preserve the sequence of actions.
- **Edited demo video:** choose one representative task and the steps needed to show its result. Set the aspect ratio, duration, and playback format for the intended viewing surface; add captions, a loop, or a final CTA when useful. A useful sequence is starting state → user action → visible system response → result. Keep controls legible at the displayed size. Trim waiting time without changing the order or inventing an outcome; label simulated data and accelerated playback.

Record the product version or environment, capture date, demonstrated task, and the observed result. Mark simulated data and edited demonstrations. A polished reconstruction must be labeled as such; do not present generated UI as a live screenshot.

## Archive key automation screenshots

During browser or app automation, save a screenshot when a meaningful state is visible: the initial state needed to explain the task, a consequential choice or approval screen, the result after the action, or a failure that explains a change of course. Capture each distinct key state once; ordinary clicks, loading spinners, and repeated unchanged pages do not need copies. Use the automation tool's supported screenshot export and save the actual observed pixels. If the tool cannot export a local image, report that gap rather than describing a screenshot as archived.

Before saving, frame the relevant UI and avoid credential entry, access keys, tokens, personal messages, or unrelated desktop content. The archive is **private source material**, not a publication-ready asset. Save it under `~/.joyally/spotlight` with the project, task, step, environment, and observed outcome. The helper keeps the original image bytes, a SHA-256 hash, and searchable metadata in date folders; directories are owner-only and files are owner-readable. It does not upload, commit, or automatically declare the image safe to share.

```bash
python3 scripts/archive.py save --input /path/to/capture.png --project "project" --task "task" --step "visible result" --environment pre --outcome success
python3 scripts/archive.py find --project "project" --query "result" --verify
```

Use `--outcome before|success|failure|pending` to describe only what the screenshot proves. Add `--url` only when the URL has no credential or sensitive query string. When writing later, search the archive by project, task, keyword, or `--since YYYY-MM-DD`; `--json` returns metadata for scripts. Open the retrieved image and apply the privacy gate below before placing it in an article. Do not treat an earlier screenshot as proof of the current live state.

When importing an older screenshot, pass its known original date with `--captured-at YYYY-MM-DD`; otherwise the helper uses the current time as both capture and archive time. The metadata keeps `captured_at` and `archived_at` separate.

## Capture and privacy gate

1. Prefer a demo account or fixture data that contains no real customer, employee, account, or credential values. Inspect the entire capture surface, including browser chrome, tabs, notifications, menus, hover states, autocomplete, URLs, cursor tooltips, and the surrounding desktop.
2. Capture locally into a private staging directory or the private archive above. Do not upload or commit raw captures. Review the source against what the result is meant to show; choose a crop or shot list that keeps the flow understandable.
3. Automatically scan every still and recording frame with available OCR or vision. For a short recording, extract all frames (for example, `ffmpeg -i demo.mp4 -vsync 0 private-frames/%06d.png`) and scan each; sampling is useful for planning but does not pass the privacy gate. On macOS, `swift scripts/scan_macos.swift <image>` emits candidate mask rectangles without printing recognized text. Add masks for sensitive fields OCR misses: names, faces, avatars, account IDs, internal URLs, tokens, secrets, cookies, messages, personal data, and any source-specific restrictions. For moving UI, cover the full time interval and every position where the data appears.
4. Save reviewed mask coordinates in a local JSON manifest and apply them with [`scripts/redact_media.py`](scripts/redact_media.py). Cover every sensitive pixel with a **constant, fully opaque RGB color**. The default is quiet gray `#E9EDF1`; choose another fixed color that suits the surrounding interface when needed. A mask replaces its entire rectangular area, including the corners. Crop first and cover only the necessary fields, with enough padding for antialiasing and nearby text; avoid large blocks across labels or controls. Keep the screenshot caption clear that private information was covered. The helper rejects mosaic and alpha colors because blur, pixels, transparency, and generated repairs do not guarantee removal.
5. Inspect the exported image at original resolution. Check every mask edge, any repeated value elsewhere in the frame, browser chrome, and the surrounding desktop. For video, inspect all frames or intervals containing sensitive regions plus the beginning, end, transitions, and hover/menu states. Run OCR again on the output and verify that no unmasked values remain. If coverage is uncertain, widen the mask, replace the source with safe demo data, or withhold sharing. Never label an unchecked export “automatically sanitized.”
6. Validate technical delivery: dimensions, legibility, video playback, duration, and any requested loop, captions, alt text, poster frame, or placement. The helper removes source audio; add only reviewed narration or music afterward. Keep the raw file private; share only the reviewed export. Record what was masked and that the exported bytes were checked.

Image generation may create decorative illustrations or clearly labeled mockups. For evidence screenshots, use pixel-preserving crop and opaque masks: generative edits can silently change visible text, URLs, counts, or controls. Keep raw captures and manifests out of published artifacts. The exported file contains newly encoded pixels and no source metadata; verify the actual output rather than relying on the rendering command alone.

## Helper usage

The helpers use pixel coordinates in the source image or video. `scan_macos.swift` detects likely text secrets and emits a starting manifest; it does not detect every identity or visual secret. Review and add regions before rendering.

```bash
swift scripts/scan_macos.swift capture.png > masks.json
python3 scripts/redact_media.py --input capture.png --output capture-redacted.png --masks masks.json
python3 scripts/redact_media.py --input demo.mp4 --output demo-redacted.mp4 --masks video-masks.json
```

The Python renderer requires Pillow for still images and FFmpeg/FFprobe for recordings. A region has `x`, `y`, `width`, `height`, `mode: "solid"`, and optional opaque `color: "#RRGGBB"`; video regions can also set `start` and `end` in seconds. Omit times to cover the full clip. The renderer rejects invalid bounds, mosaic, and alpha colors, and writes output without source metadata. Its completed run proves only that specified regions were overwritten; the visual and OCR review above remains required.

For example, `{"regions":[{"x":120,"y":44,"width":180,"height":36,"mode":"solid","color":"#E9EDF1"}]}` irreversibly covers a sensitive value at that location. A full-duration video mask uses the same region without `start` or `end`. Candidate OCR output is a starting manifest; merge overlapping regions and widen them before rendering. For high-risk exports, verify with two synthetic inputs that differ only inside the covered area: their exported pixels must be identical.
