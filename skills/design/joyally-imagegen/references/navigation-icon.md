# Navigation icon family

Use this reference for a set of product UI navigation icons: sidebar items, toolbar entries, agent roles, settings categories, or other repeated icons that must read as one visual family at 16–24px.

This is distinct from a logo or app icon. The deliverable is a small transparent source asset that sits directly beside a label; it must not contain an app tile, rounded container, scene, or decorative background.

## Design contract

1. Establish the slot before generating: default runtime size is `18px`, source size is `96×96 PNG`, and the subject should occupy roughly `72–84px` of the source canvas so it remains legible after downscaling.
2. Keep the family stable: one outline character, one restrained palette, one detail density, one optical weight, and one baseline. Use semantic silhouettes to differentiate icons; do not differentiate them with saturated backgrounds.
3. Prefer a muted lake-teal / gray-blue palette, low saturation, opaque subject pixels, and transparent outer pixels. Use no text, letters, checkerboard pattern, border, rounded rectangle, drop shadow outside the subject, or mockup frame.
4. Generate each icon from the same family prompt plus a short subject clause. Separate generation makes semantic silhouettes easier to control than asking for a multi-icon sheet.
5. Calibrate against the neighboring sidebar icons after generation. If the new family reads darker, blend the opaque pixels toward white and lower saturation before wiring it into the UI; do not compensate with a selected-state-only CSS color that changes the icon's optical weight.

If the user says the icon feels too small, first increase optical fill to roughly `88–92%` of the `96×96` source subject and then use a `20px` runtime slot when the row height permits it. Do not enlarge transparent padding or compensate with CSS cropping.

### Optional style variant: Chinese ink-wash

This is an optional family treatment, not the default navigation-icon style. Keep the base vector-like family when the user does not request a style. Activate this variant only when the user explicitly asks for 中国风、水墨、江南水墨、写意 or ink-wash navigation icons.

When the product direction calls for 中国风、水墨 or 江南 ink-wash, keep the same slot, optical scale, and transparency contract but switch the family treatment to:

1. Confident dark ink brush contours with restrained pressure variation and soft diffusion only along the subject strokes.
2. Pale celadon and gray-blue wash accents, with at most one small vermilion semantic accent (for example, a recording light or verification mark).
3. Traditional xieyi / shuimo character translated into a compact modern pictogram; do not add landscapes, mountains, calligraphy, Chinese characters, or decorative scenes.
4. Fully transparent pixels outside the silhouette. Do not render rice-paper texture, paper grain, haze, matte, or a rectangular wash behind the icon; these backgrounds often survive corner cleanup and become visible squares in the sidebar.
5. Add explicit small-size constraints: the semantic silhouette must remain recognizable at 18px, and varied brush edges must not dissolve the outline or erase the negative space.

### Chinese cultural motif selection

For the ink-wash variant, the subject itself should come from Chinese traditional culture; ink texture alone is not enough. Choose one recognizable traditional object or motif first, then adapt it to the product meaning. Do not use a generic Western pictogram and merely recolor it with ink.

| Product meaning | Preferred Chinese motif | Semantic adaptation |
|---|---|---|
| assistant home / conversation | 如意云纹、玉璧、团扇 | cloud or jade form with two restrained dots |
| skill library | 毛笔、砚台、竹简 | brush crossing a bamboo slip or jade bead |
| knowledge base | 线装书、竹卷、册页 | stitched book or scroll with a bookmark/seal |
| self evolution | 太极、阴阳鱼、云气、新芽 | taiji ring with flowing cloud ribbons and sprout |
| link exploration / recording | 皮影戏台、戏匣、朱砂灯 | shadow-theatre frame with a small red recording cue |
| experience inspection | 铜镜、玉环、如意纹 | bronze mirror or jade ring with a check seal |
| rule validation | 竹牌、木牍、官印、印谱 | tally tablet with compact marks and vermilion seal |
| reusable skills documentation | 竹卷、卷轴、玉结、朱印 | scroll tied with jade knot and seal |

The chosen object must remain legible at the runtime size, and the adaptation must not add literal Chinese characters, decorative calligraphy, landscapes, mountains, or a scenic background. Keep one motif family across the set: for example, bamboo/scroll/seal objects for document meanings and jade/cloud/taiji forms for agent meanings.

Use this style clause in the prompt:

```text
restrained Chinese ink-wash UI pictogram whose semantic silhouette comes from a recognizable Chinese traditional object or motif, xieyi shuimo brushwork, visible dry-brush bristles and wet-ink pooling only within the subject strokes, confident dark ink contour with subtle pressure variation, pale celadon and gray-blue wash accents, one restrained vermilion semantic accent, fully transparent outside the subject silhouette, no generic Western app pictogram, no paper texture or rectangular background, crisp semantic readability at 20px
```

## Prompt template

```text
A single isolated navigation UI icon: <semantic subject>.
Calm professional hand-drawn vector-like line art, compact centered silhouette,
deep lake teal ink outline with muted mist-teal and gray-blue accents, restrained
low saturation, subtle paper texture inside the subject only, consistent icon family,
crisp edges at 24px, no text, no letters.

Transparent-background source artwork. Isolated subject only. Preserve alpha channel.
No background layer. Avoid: black background, white background, solid square background,
checkerboard pattern, rounded rectangle container, app icon tile, mockup frame, border,
drop shadow outside the subject, canvas, backdrop, wallpaper, scene, watermark, brand marks.
```

Use GPT Image 2.6 with high quality for transparent icon art, then verify alpha and small-edge integrity.

## Post-processing

1. Decode the API response to a file; never put the base64 response in a shell variable or command argument.
2. Run `scripts/ensure_transparent.py` with edge-connected background removal and require transparent corners. This catches opaque white, black, and solid-color backgrounds.
3. Treat a checkerboard as baked pixels, not transparency. Inspect the full-resolution image and a 4× crop; reject any repeated light/dark grid outside the subject even when the four corners are transparent.
4. Alpha-crop the subject, add 6–8% optical padding, and resize to `96×96` PNG. Verify `sips -g hasAlpha`, dimensions, and file size after resizing. If the family is too dark, use deterministic post-processing such as color reduction, brightness lift, and a restrained white blend while preserving the alpha channel.
5. Keep runtime PNGs in the frontend asset directory and keep generation metadata in the repository asset archive. Metadata records the model, requested size, actual size, generation time, prompt, and post-processing.

## Integration and QA

1. Wire the generated PNG through the navigation config's `iconSrc`; do not use a CSS crop to compensate for a padded or checkerboard source.
2. Keep the runtime slot at the same width as neighboring icons (`18px` in the default sidebar, or `20px` when the user explicitly asks for a larger optical size). Check labels, selected state, collapsed sidebar, and narrow viewport.
3. Review each icon at source size, 4× enlargement, and actual runtime display size. Reject clipped strokes, opaque corners, unreadable details, inconsistent optical scale, or a visibly different saturation level.
4. Search for references to the old asset before deleting it. Remove obsolete checkerboard assets once the new assets are wired so they cannot be reused accidentally.
