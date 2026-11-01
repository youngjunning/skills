# Programmatic SEO Architect

Use this reference during phase 3 for all site types. The visual design and page model sections apply universally — not only to niches with repeated page patterns.

## Goal

Design page models that are scalable without becoming thin or duplicated. A programmatic page must have a reason to exist beyond keyword variation.

Page models also define the visual direction for the site. Use the brief-inference discipline from taste-skill and the brainstorm-plan-critique process from frontend-design-skill so AdSense niche sites look intentional, trustworthy, and useful — not like another generic AI content farm.

## Required Page Model Fields

For every template, define:

- Page purpose
- Search intent
- Data fields
- Unique computation or transformation
- Required examples
- Required caveats
- Internal links
- Schema markup opportunities
- Thin-content risk
- Minimum completion criteria

## Anti-Thin Rules

Reject a template if:

- The only difference between pages is a title or keyword.
- The page has no unique input, output, example, comparison, or data point.
- It cannot answer why a user would prefer this page over a generic article.
- It depends on unverifiable generated facts.

---

## Visual Design Direction

Before generating page models, lock a visual direction. AdSense sites must feel credible and readable first. Follow this process in order.

### Step 1: Read the Brief

Infer the right visual direction from:

- **Site type** — tool site, template library, directory, comparison hub, checklist hub, tutorial hub, hybrid.
- **Audience** — general consumer, professionals, students, parents, small-business owners.
- **Vibe words** the user used — "clean", "modern", "playful", "serious", "minimal", "premium", "friendly".
- **Trust constraints** — finance, health, legal, and education niches must look conservative and accessible; avoid experimental aesthetics.
- **Existing assets** — logo, colors, photography, or brand guidelines.
- **Quiet constraints** — YMYL niches, public-sector audiences, regulated industries. These override aesthetic preference.

Output a one-line **Design Read** before modeling pages:

> Reading this as: [site type] for [audience], with a [vibe] language, leaning toward [design system or aesthetic family].

Example:

> Reading this as: tool site for freelancers, with a clean/minimal language, leaning toward Tailwind utilities + Geist + restrained motion.

If the brief is ambiguous on one axis, ask exactly one clarifying question. If you can confidently infer from context, do not ask — declare the read and proceed.

### Step 2: Anti-Default Discipline

LLMs jump to the same three looks regardless of the brief. Do not reach for these defaults:

- Centered hero over a dark mesh/gradient background.
- AI-purple or blue-glow accent on neutral surfaces.
- Three equal feature cards as the primary layout.
- Generic glassmorphism everywhere.
- Inter + slate-900 as the font/color default.
- Warm cream (#F4F1EA range) + brass/clay accent + espresso near-black — the "artisan default" that makes every site invisible.

Before writing any code, state in the design plan what the LLM default would be for this brief and why you are doing something different.

### Step 3: Build a Token System

Before writing any page model, define a compact token system:

- **Color:** 4–6 named hex values. One accent, one surface, one text, one border, optional subtle and strong variants.
- **Type:** a display face + a body face. State the pairing reason in one sentence.
- **Layout:** a one-sentence layout concept. Use ASCII wireframes to compare options before committing.
- **Signature:** the single memorable element this site will be known for — a layout move, a typographic treatment, a data-driven component. State it explicitly.

Review the token system against the design read before writing any template. If any token reads as the generic default for a similar brief, revise it and say what you changed.

### Step 4: Pick a Design Anchor

Use one anchor per site. Do not hybridize. For AdSense niche sites, prefer anchors that prioritize readability, trust, and performance.

| Anchor | Best For | Key Tokens |
| --- | --- | --- |
| **Swiss** | utility tools, calculators, explainers | white/neutral surface, single sans typeface, one strong accent, visible grid lines |
| **Organic** | wellness, lifestyle, parenting, food | earth tones, rounded corners 16–32 px, humanist serif or warm sans, subtle grain |
| **Industrial** | devtools, finance, data-heavy sites | dark surface, monospace type, one semantic signal color, flat 1 px borders |
| **Lo-Fi** | creative templates, personal brands, tutorials | paper-yellow surface, mixed system fonts, slight rotation, halftone texture |

Avoid by default for AdSense sites:

- **Aurora / Chaotic Maximalism** — high motion and clashing colors hurt readability and ad performance.
- **Brutalist** — raw aesthetics undermine trust in YMYL niches.
- **Retro-Futuristic** — niche unless the topic genuinely calls for it.

### Step 5: Set the Dials

After choosing the anchor, set three dials. AdSense sites should default lower than marketing landers — readability and ad-friendliness matter more than visual ambition.

- **DESIGN_VARIANCE** — 1 = perfectly symmetric, 10 = experimental. Default **4–6** for AdSense sites.
- **MOTION_INTENSITY** — 1 = static, 10 = cinematic. Default **2–4**. Heavy motion slows perceived performance and distracts from content.
- **VISUAL_DENSITY** — 1 = airy gallery, 10 = packed dashboard. Default **3–5**. Leave room for ads without cramping content.

Adjust based on the design read:

| Signal | VARIANCE | MOTION | DENSITY |
| --- | --- | --- | --- |
| trust-first / YMYL / public-sector | 3–4 | 2–3 | 4–5 |
| clean tool / calculator / tutorial | 4–5 | 2–3 | 3–4 |
| lifestyle / creative / template library | 6–7 | 4–5 | 3–4 |
| directory / comparison hub | 5–6 | 2–3 | 4–5 |

### Step 6: Typography

- **Display / Headlines:** `text-4xl md:text-6xl tracking-tighter leading-none` as baseline.
- **Body:** `text-base leading-relaxed max-w-[65ch]`.
- **Sans choice:** avoid Inter as default. Prefer Geist, Outfit, Cabinet Grotesk, or Satoshi. Inter is acceptable only when the brief explicitly asks for a neutral/standard feel or the site is public-sector.
- **Serif:** very discouraged as default. Only use if the brand brief names a serif, or the niche is genuinely editorial/heritage AND you can articulate why. Specifically banned as defaults: Fraunces and Instrument Serif.
- **Italic descender clearance:** when italic display type contains descenders (y g j p q), use `leading-[1.1]` minimum and add `pb-1` reserve on the wrapper.
- **One typeface pairing per site.** Declare it in the token system and do not drift.

### Step 7: Color

- Max 1 accent color. Saturation < 80% by default.
- **The Lila Rule:** AI-purple / blue-glow is banned as default. Use neutral bases (Zinc / Slate / Stone) with high-contrast singular accents (Emerald, Electric Blue, Deep Rose, Burnt Orange).
- **Color Consistency Lock:** once an accent is chosen, it is used on the whole site. A warm-grey site does not get a blue CTA in one section. Pick one accent, lock it, audit every component.
- **One palette.** Do not fluctuate between warm and cool grays within the same site.

### Step 8: Content Discipline

Every string on screen must name real information or be clearly labeled sample data.

Forbidden:

- Fabricated personas, fake telemetry, or invented statistics.
- Filler labels like `SECURE OPERATOR AUTHENTICATION` or `// INTELLIGENCE LAYER`.
- Themed replacement of standard UI copy (`Authenticate Session` instead of `Next`).
- Unicode glyphs used as icons.
- AI-slop register: twee subcopy on serious surfaces, ornamental status strips, fake dashboard screenshots.
- Em-dash (`—`) anywhere visible to users — in headlines, body text, labels, CTAs, or captions. Use a hyphen (`-`) or restructure the sentence. Zero em-dashes is the rule.

Required:

- Real examples, real formulas, real listings, or real templates.
- Label sample data explicitly when real data is not available.
- Standard UI copy for standard actions.
- One label per intent across the entire site. If the CTA is "Get Started", it is "Get Started" everywhere — not "Get Started" in the hero and "Sign Up Free" in the footer.

Writing discipline: words are design material. Write from the user's side of the screen. Active voice. Name things by what users control, not how the system is built. Errors explain what happened and how to fix it — they do not apologize and they are never vague.

### Step 9: Layout Rules

Apply these hard rules to every page model. Failing any is broken work.

- **Hero fits the initial viewport.** Headline max 2 lines on desktop; subtext max 20 words and 3–4 lines; primary CTA visible without scroll.
- **Hero top padding cap.** Max `pt-24` at desktop.
- **Hero stack discipline.** Max 4 text elements: eyebrow OR brand strip (zero or one), headline, subtext, CTAs. No trust strips, no feature bullets, no pricing teasers inside the hero.
- **CTA clarity.** One label per intent across the page. Button text fits on one line at desktop. Contrast passes WCAG AA.
- **Eyebrow restraint.** Max 1 eyebrow per 3 sections. If section A has an eyebrow, the next 2 sections cannot. Count `uppercase tracking` instances — if count > ceil(sections / 3), it fails.
- **Split-header ban.** "Left big headline + right floating paragraph" as a section header is banned as default. Stack vertically: headline on top, body below, max-width 65ch.
- **Section-layout-repetition ban.** A layout family can appear at most once on the page. Use at least 4 different layout families on a page with 8 sections.
- **Zigzag alternation cap.** Max 2 consecutive image+text split sections. The 3rd in a row is a pre-flight fail.
- **Bento cell count rule.** A grid has exactly as many cells as it has content for. No blank tiles.
- **Bento background diversity.** At least 2–3 cells in any multi-cell grid need real visual variation: an image, a brand-appropriate gradient, a pattern, or a tinted background. All-white-on-white bento is AI default.
- **Mobile collapse explicit.** Declare the `< 768px` fallback for every multi-column layout in the same component.
- **Ad-friendly spacing.** Leave predictable whitespace for ad placements without breaking layout rhythm.

### Step 10: Asset Strategy

Every page needs real visual assets. Text-only pages read as thin or incomplete.

**Site identity assets (favicon, logo) — generate first, before any page component:**

Do not ship with a browser-default blank favicon. Priority order:

1. **Codex** — delegate with: site name, niche, one-sentence purpose, accent color from the token system, design anchor. Preferred — generates multiple variants and SVG output.
2. **Claude native image generation** — if Codex is unavailable.
3. **SVG placeholder** — label clearly (`<!-- TODO: replace with final favicon/logo -->`). Add to the phase 4 completion gate so it cannot be forgotten.

**Output paths:**
- Logo: `public/logo.svg` — SVG preferred. Fallback: site name as styled text in the token system typeface and accent color.
- Favicon source: `public/favicon-32x32.png` (32×32 PNG) — also convert to `public/favicon.ico`.
- Apple touch icon: `public/apple-touch-icon.png` (180×180).

Wire up in `src/app/layout.tsx` via Next.js metadata:

```ts
export const metadata: Metadata = {
  icons: {
    icon: '/favicon-32x32.png',
    apple: '/apple-touch-icon.png',
  },
}
```

**Page-level visual assets:**

1. **Generated images.** If an image-generation tool is available, create section-specific assets: hero photography, product shots, diagrams.
2. **Real photography or brand assets.** Use actual stock or provided URLs when available. Acceptable placeholder: `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}` — seed should describe the section.
3. **Placeholder slots.** If neither is possible, leave clearly labeled placeholders (`<!-- TODO: hero image 1600x1200 -->`) and tell the user what is missing.

Avoid:

- Hand-rolled SVG illustrations as default visuals.
- Div-based fake screenshots.
- Generic gradient blobs as the only hero visual.
- Text + gradient blob as a "hero" — it is a placeholder.

### Step 11: Technical Defaults

Unless the existing project demands otherwise:

- **Framework:** static Next.js or Astro.
- **Styling:** Tailwind CSS.
- **Fonts:** self-host via `next/font` or `@font-face` with `font-display: swap`. No Google Fonts `<link>` in production.
- **Icons:** one library per project (Phosphor, Tabler, or Radix). Standardize `strokeWidth`. Never hand-roll SVG icons.
- **Animation:** Motion (formerly Framer Motion). Import from `motion/react`. Use `useMotionValue` / `useTransform` for continuous pointer/scroll values — never `useState` for these.
- **Accessibility:** WCAG AA contrast for text and buttons, labels above inputs, focus rings, alt text on images, `min-h-[100dvh]` (not `h-screen`) for full-height sections.
- **Performance:** no layout-thrashing animation; isolate motion to leaf `'use client'` components.

---

## Output

Write `outputs/<site-slug>/page-model.md`:

```md
# Page Model

## Design Read
Reading this as: [site type] for [audience], with a [vibe] language, leaning toward [anchor / design system].

## Anti-Default Note
The LLM default for this brief would be: [describe it]. This design avoids it by: [state the deliberate choice].

## Token System
- Color: [4–6 named hex values]
- Type: [display face + body face, one-line pairing reason]
- Layout: [one-sentence concept]
- Signature: [the single memorable element]

## Dials
- DESIGN_VARIANCE: [value]
- MOTION_INTENSITY: [value]
- VISUAL_DENSITY: [value]

## Template: [Name]

- Purpose:
- Search intent:
- URL pattern:
- Data fields:
- Unique value per page:
- Required sections:
- Internal links:
- Schema:
- Thin-content risks:
- Completion gate:
```

Only approve templates that can create pages a real user would bookmark, share, or use to complete a task.

---

## Pre-Flight Check

Before moving to phase 4, verify:

- [ ] Design read is stated and matches the niche.
- [ ] Anti-default note is written — what the LLM default would be and why this deviates.
- [ ] Token system is defined: color, type, layout, signature.
- [ ] One anchor is chosen and no hybrid drift is planned.
- [ ] Dials are set and appropriate for AdSense readability.
- [ ] Typography uses a deliberate pairing; no default Inter; no unjustified serif.
- [ ] One accent color, locked across the whole site.
- [ ] Every template passes anti-thin rules.
- [ ] Every string in mocks is real information or clearly labeled sample/filler.
- [ ] Hero layout fits initial viewport, respects stack discipline, top padding ≤ pt-24.
- [ ] CTA labels are consistent, one label per intent, contrast-compliant.
- [ ] Eyebrow count ≤ ceil(sections / 3).
- [ ] No split-header pattern used as default.
- [ ] No 3+ consecutive zigzag sections.
- [ ] Bento cells match content count; no blank tiles; cells have visual diversity.
- [ ] Image strategy is defined; no fake-screenshot plans; placeholder slots labeled.
- [ ] Ad placements are accounted for without breaking layout.
- [ ] Mobile collapse declared per multi-column component.
- [ ] All `acts_in_phase: "page_model"` entries from `competitive_brief` in `outputs/niches.json` are addressed in at least one page template — the differentiating tool, asset, or feature exists in the page model and is planned for build. If an entry was missed here, note it and ensure phase 4 Step 0 catches it.
