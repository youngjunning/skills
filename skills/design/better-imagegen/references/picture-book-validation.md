# Picture-book manifest and deterministic validation

Use the skill's Pillow virtual environment:

```bash
"$BETTER_IMAGEGEN_PYTHON" "$SKILL_DIR/scripts/validate_picture_book.py" /path/to/book/manifest.json
```

Exit 1 means a structural, file, geometry, or recorded-review failure. Warnings flag planned repetition for inspection; they are not similarity judgments. The checker neither generates nor approves pictures. Do not fill `pass` automatically to obtain a successful exit.

The manifest is the authoritative copy and export plan. Retain additional generation metadata, references and draft status alongside these fields. This abbreviated one-page example shows the validation contract; the pending review intentionally prevents final acceptance:

```json
{
  "page_count": 1,
  "size_cm": [28.5, 20.6],
  "dpi": 254,
  "layout": "integrated",
  "safe_box": [0.04, 0.04, 0.96, 0.96],
  "pages": [{
    "page": 1,
    "purpose": "Reveal the toy's fabric seam",
    "scene": "A child gently pinches the stuffed animal",
    "focal_subject": "Fabric seam and child's hands",
    "shot": "detail",
    "angle": "slightly overhead",
    "composition": "toy upper right; blanket lower left",
    "evidence": "Stitched belly and soft stuffing are visible",
    "layout": "integrated",
    "art": "art/01.png",
    "image": "pages/01.jpg",
    "text": "原来，这是毛绒玩具呀！",
    "text_region": [0.06, 0.75, 0.85, 0.90],
    "text_surface": "pale blanket continuing the scene",
    "protected_boxes": [[0.50, 0.15, 0.90, 0.68]],
    "text_blocks": [{
      "text": "原来，这是毛绒玩具呀！",
      "box": [0.07, 0.78, 0.70, 0.85]
    }],
    "review": {
      "image_sha256": "",
      "identity": "pending",
      "anatomy": "pending",
      "story_evidence": "pending",
      "copy": "pending",
      "readability": "pending",
      "composition": "pending",
      "note": ""
    }
  }]
}
```

All rectangles are `[left, top, right, bottom]`, normalized to the final page, origin top-left. `text_blocks` contains measured ink bounds from rendering, including effects; preserve exact text/newlines so concatenation equals `text`. Protected rectangles come from inspecting the image after crop/scale. Empty protected regions may be legitimate on an object-free page but require visual judgment. Choose safe margins for the edition; the example is not a printer specification.

Keep `layout` aligned with the requested edition. `integrated` means continuous scene art under the lettering; `split` means an explicitly chosen separate text area. The checker compares declared layouts but cannot detect a mislabeled sidebar in pixels. Likewise, measured boxes do not prove contrast or glyph correctness. Review final pages directly.

Store SHA-256 of the finished image only after actual review. Each of the six review fields must be `pass`, and `note` should identify concrete checks/findings. Export changes require a fresh visual review and hash. `repetition_reason` can document deliberate camera repetition; `reuse_reason` permits intentionally repeated artwork, only when compatible with the user's request. Never use these fields to bypass a request for distinct images.

Compare decoded source-art pixels rather than final pages so different captions cannot hide reused illustrations. This catches exact duplication only. Inspect the contact sheet for near-duplicates and review individual pages for scene/identity drift. PDF geometry, ZIP contents, and actual reading-size quality remain separate export checks.
