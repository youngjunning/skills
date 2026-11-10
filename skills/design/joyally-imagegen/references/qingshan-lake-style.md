# Qingshan Lake default image style

Use this as the default visual language when the user has not named another style. It translates mist, lake water, cypress forest, distant hills, wet wood, and rare dawn light into palette, hierarchy, material, atmosphere, and whitespace. It is landscape distillation, not literal landscape illustration.

## Mode selection

Choose exactly one mode before writing the image prompt or deterministic semantic layer:

| Context | Mode |
| --- | --- |
| Internal ATA, technical article, knowledge map, architecture diagram, report, unspecified canvas | `light` |
| Existing dark product surface, night scene, dark wallpaper, user asks for black/dark | `dark` |
| Existing artifact with an established theme | Match the artifact |
| User names another style | Do not apply Qingshan Lake; follow the requested style |

“Black” means deep-lake ink, never pure black. “White” means warm mist-white, never a sterile pure-white field.

For ATA and technical-article covers, Qingshan Lake Light is the default unless the current request names another style. This remains true for recurring FiaOS and AI Browser articles. A previous cover, repository theme, or series history does not authorize carrying forward anime characters or any identity reference. Add people only when the current request explicitly asks for them.

## Optional Zisheng character element

Qingshan Lake is a visual language, not a character or identity requirement. Do not add 紫升 merely because Qingshan Lake Light or Dark is selected.

Only when the user explicitly asks to include or preserve Zisheng, use both bundled identity references:

- `../assets/identity-references/zisheng-avatar.png` is authoritative for face shape, warm brown eyes, eyebrows, short upward-spiked black hair and friendly confident expression.
- `../assets/identity-references/zisheng-full-body.png` is authoritative for adult body proportion, relaxed three-quarter stance, signature deep-purple oversized hoodie, dark tapered pants and teal-accent sneakers.

Render the author as an adult age 25+. Preserve the purple hoodie as an identity exception to the Qingshan Lake palette; apply lake teal, cypress green, gray-blue and dawn gold to the environment and secondary accents instead of recoloring the character.

- For scene-led covers, portraits and illustrations, attach both files as identity references and keep the face, hair, outfit silhouette, adult proportion and expression stable.
- For architecture diagrams, knowledge maps and text-heavy posters, use `zisheng-full-body.png` as a locked deterministic layer in a reserved perimeter or title zone. It must not cover nodes, labels, arrows, rails or evidence.
- For a close crop, keep the avatar as the face authority even when the full-body image supplies costume and body pose.
- If a functional contract cannot contain a character without becoming invalid—for example a standalone transparent logo mark or a strict sprite grid—preserve the functional contract and omit the character unless the user explicitly changes that contract.

Reject outputs that merely add a generic anime person, change the purple hoodie, make the author childlike, replace the face, or use the character as an unlabeled diagram node.

## Shared character

Require:

- quiet, natural, precise, low-noise composition;
- generous breathing room and layered atmospheric depth;
- lake teal for the main focal relationship or action;
- cypress green for healthy, complete, or growing states;
- gray-blue hill tones for secondary structure;
- warm dawn gold, clay, wood, wildlife, particles, and scenic motifs only as rare accents;
- soft borders, continuous geometry, and restrained translucency when the asset contains surfaces;

Reject:

- literal tourism-poster scenery unless the user explicitly requests a landscape;
- pure white or pure black designed canvases;
- generic blue-purple AI gradients, neon cyberpunk chrome, or large gold fields;
- glass-on-glass, nested rounded-card mazes, pills on every label, and heavy glow;
- decorative card-edge bars, including full-height side strips, short rules above titles, and pseudo-tabs attached to rounded cards;
- decorative atmosphere between the reader and technical content;
- low-contrast text, state communicated by color alone, or texture that competes with labels.

## Light mode

### Palette

| Role | Value |
| --- | --- |
| Canvas | `#F4F6F1` |
| Surface | `#FBFCFA` |
| Surface muted | `#E8EEEA` |
| Primary text | `#183B40` |
| Secondary text | `#4D676B` |
| Lake teal | `#2E948A` |
| Strong teal | `#286B66` |
| Teal container | `#DCEFEB` |
| Cypress / success | `#356439` |
| Dawn / warning | `#7A5B1E` |
| Clay / error | `#8E493E` |
| Border | `#D4DFDC` |

### Backdrop prompt fragment

```text
Qingshan Lake light visual language: warm mist-white canvas, translucent pale lake haze, restrained lake-teal and cypress-green traces, distant gray-blue hill layering around the outer edges, rare soft dawn-gold accent, quiet natural precision, generous clean center and breathing room, subtle paper and water depth, no literal scenic poster.
```

For text-heavy or structured graphics, keep the center low-detail and put decorative topology only at the perimeter.

## Dark mode

### Palette

| Role | Value |
| --- | --- |
| Canvas | `#0F2B36` |
| Surface | `#183B40` |
| Elevated surface | `#234B50` |
| Primary text | `#F2F7F2` |
| Secondary text | `#B8CCDB` |
| Lake teal | `#85C7BA` |
| Strong teal | `#62B3A6` |
| Teal container | `#244F50` |
| Cypress / success | `#8DBB82` |
| Dawn / warning | `#D6A352` |
| Clay / error | `#D58B7D` |
| Border | `#365D62` |

### Backdrop prompt fragment

```text
Qingshan Lake dark visual language: deep-lake ink canvas instead of pure black, layered dark-water and cypress silhouettes, restrained lake-teal mist and gray-blue distant-hill contours at the outer edges, rare dawn-gold edge light, quiet natural depth, generous clean center, low-noise premium technical atmosphere, no neon cyberpunk and no literal scenic poster.
```

Dark mode must retain readable mist-white content surfaces and should not become a black developer-console theme.

## Adapt by asset type

- **Knowledge map / architecture diagram:** use the selected token set for deterministic HTML/CSS/SVG and keep one semantic question per figure. Use image generation only for a restrained text-free backdrop. If the user explicitly requests Zisheng, composite the approved full-body cutout as a locked perimeter layer and validate that it does not reduce graph clearance or legibility.
- **Cover / poster:** use mist, water depth, hills, cypress, and dawn light as composition and palette. Preserve a large quiet region for exact overlay text.
- **Portrait / illustration:** apply the palette through environment, wardrobe accents, lighting, and depth; do not add UI cards or force a lake into the scene.
- **Logo / transparent icon:** preserve the transparent-background contract. Apply teal/cypress/dawn colors only to the isolated mark; never add a scenic canvas or app tile.
- **macOS icon:** apply the palette to the source art, then follow the native squircle/iconset workflow.
- **Wallpaper:** literal landscape cues are allowed, but keep them restrained and avoid tourism-poster saturation.
- **Sprite / Codex pet:** character identity, frame grid, directions, and alpha rules take precedence; use Qingshan Lake only as a color/material guide.
- **Image edit:** preserve the referenced image’s identity and composition. Apply Qingshan Lake only when the requested edit includes restyling.

## Deterministic diagram tokens

Use `assets/qingshan-lake-image.tokens.json` as the machine-readable source for Light/Dark diagram layers. Maintain at least 24 px card gaps on a 1600×900 canvas, one readable surface per hierarchy boundary, and rare warm accents.

## Verification

Run the deterministic token gate after changing the bundled palette:

```bash
python3 scripts/validate_qingshan_lake_tokens.py
```

Check both modes for:

1. no pure-white or pure-black field;
2. exact foreground contrast on every semantic surface;
3. teal as the main accent and warm colors below roughly 5% of the composition;
4. no generic blue-purple AI gradient or neon glow;
5. atmosphere staying outside the primary reading path;
6. full-resolution and thumbnail legibility for structured assets.
