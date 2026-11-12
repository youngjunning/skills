# Joyally Design social cards

Create a 3:4 image card when the requested output is a social post cover, a carousel panel, or a shareable visual summary. Use the source material's claim and attribution. A card is one idea at one reading depth; split a longer argument into a sequence with page numbers.

## Styles

| Style | Best use | Joyally treatment |
| --- | --- | --- |
| `editorial` | Essays and product thinking | Song-style display title, warm paper, ink-colored type, a single lake-green rule |
| `swiss` | Technical points and measured updates | Strict left grid, large sans title, restrained accent |
| `poster` | Strong cover and final takeaway | Heavy title, bold lake color, bottom band; `insight` layout becomes a deep-lake payoff panel |

These styles adapt editorial typography, grid discipline, and cover-to-insight pacing to Joyally's lake palette. They do not import a third-party theme, logo, sample copy, or runtime.

Visual study: [pakco-html social-card previews](https://github.com/pakco77/pakco-html/blob/main/templates/style-picker.html). Joyally maintains the card CSS, generator, and export path independently.

## Generate and export

```bash
node scripts/design-engine.mjs social-card /tmp/social-cover \
  --style poster --layout cover --title "报告先讲结论" \
  --subtitle "把最重要的判断放在读者第一眼能看到的位置。" \
  --eyebrow "设计笔记" --credit "Joyally Design · 示例" --page 01 --total 02
node scripts/design-engine.mjs social-render /tmp/social-cover/index.html \
  --out /tmp/social-cover.png
```

Run `social-card` once per card. Use `--layout insight` for an inside panel, `--highlight` only for a supported figure or takeaway, and `--credit` for the actual author or source. Use `--brand` when the card belongs to a different product. The generated directory holds `index.html` and a local Joyally stylesheet. `social-render` exports a 2160 × 2880 PNG by default; `--scale 1` exports 1080 × 1440. It uses local Chrome, or `--chrome` / `CHROME_PATH` when Chrome is elsewhere.

Check the actual PNG before delivery: title wraps cleanly, no text clips, page numbers are consistent, attribution is correct, and important facts remain legible at phone size. Do not invent figures to fill a panel. If the material does not fit, shorten or split it without changing its meaning.
