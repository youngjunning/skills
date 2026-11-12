---
name: joyally-spotlight
description: Capture and prepare real product screenshots, UI recordings, and interaction demos for presentation or explanation. Redact private UI data with reproducible masks and verify the exported image or video before sharing.
---

# Joyally Spotlight

Turn an actual product flow into a screenshot or recording that lets a viewer understand what the product does. The result can stand alone or be used in any presentation, document, page, or message. Interface implementation belongs to the product's design and engineering workflow; prose belongs to the writing workflow.

## Choose the deliverable

- **Product screenshot:** show the product state or detail the viewer needs to understand. Capture the whole relevant UI first, then crop to keep context and text readable.
- **Interaction recording:** show a task from input through visible result. Capture the real UI and preserve the sequence of actions.
- **Edited demo video:** choose one representative task and the steps needed to show its result. Set the aspect ratio, duration, and playback format for the intended viewing surface; add captions, a loop, or a final CTA when useful. A useful sequence is starting state → user action → visible system response → result. Keep controls legible at the displayed size. Trim waiting time without changing the order or inventing an outcome; label simulated data and accelerated playback.

Record the product version or environment, capture date, demonstrated task, and the observed result. Mark simulated data and edited demonstrations. A polished reconstruction must be labeled as such; do not present generated UI as a live screenshot.

## Capture and privacy gate

1. Prefer a demo account or fixture data that contains no real customer, employee, account, or credential values. Inspect the entire capture surface, including browser chrome, tabs, notifications, menus, hover states, autocomplete, URLs, cursor tooltips, and the surrounding desktop.
2. Capture locally into a private staging directory. Do not upload or commit raw captures. Review the source against what the result is meant to show; choose a crop or shot list that keeps the flow understandable.
3. Automatically scan every still and recording frame with available OCR or vision. For a short recording, extract all frames (for example, `ffmpeg -i demo.mp4 -vsync 0 private-frames/%06d.png`) and scan each; sampling is useful for planning but does not pass the privacy gate. On macOS, `swift scripts/scan_macos.swift <image>` emits candidate mask rectangles without printing recognized text. Add masks for sensitive fields OCR misses: names, faces, avatars, account IDs, internal URLs, tokens, secrets, cookies, messages, personal data, and any source-specific restrictions. For moving UI, cover the full time interval and every position where the data appears.
4. Save the final mask coordinates in a local JSON manifest and apply them with [`scripts/redact_media.py`](scripts/redact_media.py). Use opaque cover for credentials, authentication material, and data that could be reconstructed. Use mosaic for faces or contextual details when retaining the shape helps explain the UI. A blurred or mosaic secret is not considered hidden.
5. Inspect the exported image at original resolution. For video, inspect the beginning, end, transitions, hover/menu states, and all frames or intervals containing sensitive regions. Run OCR again on representative output frames and verify that no unmasked values remain. If detection or coverage is uncertain, widen the mask, replace the source with safe demo data, or withhold sharing. Never label an unchecked export “automatically sanitized.”
6. Validate technical delivery: dimensions, legibility, video playback, duration, and any requested loop, captions, alt text, poster frame, or placement. The helper removes source audio; add only reviewed narration or music afterward. Keep the raw file private; share only the reviewed export. Record what was masked and that the exported bytes were checked.

Image generation may create decorative illustrations or clearly labeled mockups. For evidence screenshots, use pixel-preserving crop and masks: generative edits can silently change visible text, URLs, counts, or controls. If the available tool can only regenerate the UI, label the result an edited illustration and keep the factual evidence in text or an unaltered, safely cropped capture.

## Helper usage

The helpers use pixel coordinates in the source image or video. `scan_macos.swift` detects likely text secrets and emits a starting manifest; it does not detect every identity or visual secret. Review and add regions before rendering.

```bash
swift scripts/scan_macos.swift capture.png > masks.json
python3 scripts/redact_media.py --input capture.png --output capture-redacted.png --masks masks.json
python3 scripts/redact_media.py --input demo.mp4 --output demo-redacted.mp4 --masks video-masks.json
```

The Python renderer requires Pillow for still images and FFmpeg/FFprobe for recordings. A region has `x`, `y`, `width`, `height`, and `mode` (`solid` or `mosaic`); video regions can also set `start` and `end` in seconds. Omit times to cover the full clip. The renderer rejects invalid bounds and writes output without source metadata. Its completed run proves only that specified regions were masked; the visual and OCR review above remains required.

For example, `{"regions":[{"x":120,"y":44,"width":180,"height":36,"mode":"solid"}]}` covers a sensitive value at that location. A full-duration video mask uses the same region without `start` or `end`. Candidate OCR output is a starting manifest; merge overlapping regions and widen them before rendering.
