# Cover Styles

Reference for `story-cover.md`. Genre-to-visual-style mapping for cover image generation prompts.

## Traffic-Fiction Default: Melodrama Over Prestige

For paid-traffic fiction, the cover must look like the decisive frame of a high-conflict short drama, not a prestige book jacket or movie poster. This rule overrides softer or more polished examples elsewhere in this file unless the user explicitly requests a literary, atmospheric, or restrained treatment.

**Required visual hierarchy:**

1. **Conflict:** freeze a concrete betrayal, exposure, rejection, interruption, humiliation, confrontation, or reversal. Show visual proof such as a marriage certificate, pregnancy test, torn contract, ring, child, rival, slap aftermath, hospital report, or kneeling ex.
2. **Expression:** make the emotional roles legible at thumbnail size. Use widened eyes, open-mouth shock, furious accusation, crying disbelief, jealous panic, smug triumph, or visible guilt. Calm model faces and subtle longing are not enough.
3. **Relationship complexity:** prefer 3–4 figures when the premise contains an ex, rival, child, parent, fiancé, witness, or betrayer. Four discernible people is the hard maximum; never turn the full cast into a crowd. Use gaze, pointing hands, grabbing, blocking, separation, and foreground/background hierarchy to show who wants whom, who betrayed whom, and who holds power.
4. **Lighting coherence:** choose one believable location-light family and one shadow direction. Lighting supports the conflict but must never make actors look individually keyed, waxy, or pasted into the set.

**Hard bans for the default traffic-fiction route:**

- No prestige, premium, tasteful, understated, editorial, or awards-season mood as the main selling point.
- No movie-poster composition built around atmosphere, heroic posing, skyline scale, or cinematic emptiness.
- No beautiful couple portrait, near-kiss, warm embrace, forehead touch, mutual gaze, or two attractive people merely standing together.
- No polished billionaire, royal, or elite-family group photo where everyone looks composed and harmonious.
- No more than 4 discernible people, including background witnesses, mourners, guards, teammates, children, or rivals. Imply larger groups through setting and proof objects instead of readable extra figures.
- No generic luxury penthouse, gala, manor, sports field, moon, or car unless a visible relationship conflict is happening inside the scene.
- Do not use `cinematic`, `elegant`, `luxury`, or `romantic` as standalone direction. If retained as rendering vocabulary, immediately subordinate it to a named scandal, conflict action, and exaggerated reaction.

**Pass test:** at 160px wide and with the title hidden, a viewer should be able to describe the scandal in one sentence and assign at least three emotional roles, such as “the wife caught her husband with the pregnant mistress while his mother protects them.” If not, redesign the tableau.

## Site-Level Style Decision

**Before generating any covers, determine the site's primary visual register.** All books on the same site use the same render style — do not mix styles across books unless the site explicitly mixes genres (e.g. a general fiction platform).

| Site theme | Visual register | When to use |
|---|---|---|
| **Cinematic Drama** | AI film-still quality, photorealistic real actors, high contrast, emotion-first composition | Site hosts Urban Drama / Contemporary Romance / Thriller / Historical Court Drama content — contemporary or historical drama where characters feel human and real |
| **Dark Fantasy Illustration** | Hyperrealistic 3D render, deep indigo, plum, stone, or daylight atmospheric background, gold/silver metallic typography, epic world elements | Site hosts Cultivation Fantasy / Dark Fantasy / Sci-Fi content — power systems, fantasy worlds, sci-fi; palette remains user-selectable |
| **British Literary** | Painterly period photography or fine-art editorial, warm muted tones and compositional restraint — understated rather than dramatic | Site hosts Regency / Historical / Cosy Mystery / Gothic / Literary Thriller — British-flavoured, period-grounded, atmosphere-first rather than power-first |
| **Emotional Drama** | Desaturated editorial photography, cold-warm contrast, threshold and outsider framing — quiet emotional weight rather than kinetic drama | Site hosts Family Drama / Secret Identity / Medical Drama / Grief Fiction — contemporary emotional fiction where the visual subject is an interior state, not an action |

Determine which register fits the site during **B2 (Design Identity)** and record it in the design-system notes. All A2 cover generation for that site uses the same register.

If the site mixes genres, default to the **Traffic-Fiction Melodrama** hierarchy above for realism-leaning titles and **Dark Fantasy Illustration** for genre-fantasy titles, but keep color palettes harmonized across covers so the homepage grid feels cohesive.

---

## Visual Style Standard

Both registers target **photorealistic or hyperrealistic 3D render quality** — not painted, not anime, not watercolor. The reference aesthetic is:

- **Mobile Short-Drama Conflict** (Urban Drama / Contemporary / Thriller / Historical Court Drama): low-budget live-action freeze-frame quality. Use handheld wide-angle framing, one coherent available-light family, cramped locations, overlapping gestures, and imperfect faces. Think: the loudest frame from a vertical web drama, never a movie poster or cast photo. Do not equate low budget with direct flash, hard LED glare, mixed blue/orange keys, or dead-black backgrounds.
- **Dark Fantasy Illustration** (Cultivation Fantasy / Dark Fantasy / Sci-Fi): Hyperrealistic 3D render, user-selected atmospheric background (deep indigo, plum, stone, ivory, or daylight are all valid), character in detailed fantasy or sci-fi attire, coherent lighting. Gold/silver/chrome metallic typography is large and dominant in the lower 35% of the frame.
- **British Literary** (Regency / Historical / Cosy Mystery / Gothic / Literary Thriller): Painterly period photography or fine-art editorial quality. Warm cream, muted sage, deep burgundy or charcoal palettes depending on sub-genre. Atmosphere and period detail are the primary subjects; characters are composed and restrained rather than dramatic. Think: BBC period drama production still, literary fiction hardcover jacket.
- **Emotional Conflict** (Family Drama / Secret Identity / Medical Drama / Grief Fiction): ordinary-location documentary immediacy. Use a hospital corridor, dining table, registry counter, or cramped apartment with broad ceiling/window light, visible paperwork, and one relationship rupture in progress. Zero editorial polish, zero formal family arrangement.

**Shared quality keywords (include in every prompt):**
`photorealistic, ultra-detailed, coherent available light, matte natural skin, exaggerated facial expressions, high-conflict relationship tableau, professional traffic-fiction cover, thumbnail-legible staging`

Avoid generic `cinematic lighting`, `shallow depth of field`, and `dramatic atmosphere` unless the prompt already names the scandal, every character's role, and their visible reaction. Background blur must not hide witnesses, rivals, or relationship evidence.

---

## Composition Templates

Pick the template that best matches the book's core tension. These mirror the reference visual language.

| Template | When to use | Description |
|---|---|---|
| **Power Inversion** | Urban Drama / Contemporary Romance revenge, humiliation, domination arcs | **TWO characters.** One standing figure (powerful, cold, composed) looks down at a kneeling/crying/bound figure. Third character optional as witness. Setting: luxury interior, parking garage, ballroom. |
| **Intimate Tension** | Contemporary Romance / Urban Drama romance, billionaire arcs | **TWO characters.** Two figures in close proximity — woman wrapped in white bed sheet with bare shoulders and legs visible to mid-thigh, clutching sheet to chest, expression of shock or conflict; man in open-collar shirt at rest on rumpled bed watching her. Luxury penthouse bedroom, floor-to-ceiling cityscape windows. Foreground props: champagne flute, scattered luxury items (jewelry, lipstick). |
| **Rain Shelter** | Thriller / Contemporary Romance romance, protection arcs | **TWO characters.** Two figures on a wet night street, one holding a black umbrella over the other. The protected figure looks downcast; the protector looks stern or conflicted. City lights reflect on the wet pavement. Setting can be European street or neon city. |
| **Grand Humiliation** | Contemporary Romance / Urban Drama gala/elite society arcs | **TWO characters.** Glamorous dominant figure in deep-V plunging neckline floor-length gown (thigh-high slit, jeweled décolletage, red lips, chandelier jewels) stands elevated or turns away in contempt while a male figure kneels or collapses crying at her feet. Grand ballroom setting: chandeliers, champagne tower, roses; use at most 1 additional readable witness and imply the wider audience through flash bulbs or cropped raised phones. |
| **Lone Hero** | Cultivation Fantasy / Sci-Fi / Historical War Epic | **ONE character.** Single powerful protagonist fills center-left frame, facing slightly away from camera. Epic world behind: ruined city + energy portal (sci-fi), snowy mountains + dark castle (fantasy), cloud sea + ancient pagodas (cultivation). Title in large metallic font occupies lower 35% of frame. |
| **Duo Confrontation** | Dark Fantasy / Historical Court Drama romance + power | **TWO characters.** Two characters pressed together — powerful male behind or beside protected female. Dark dramatic background. Matching detailed costumes. Both look into distance or at camera with intensity. |
| **Manor Portrait** | Regency / Historical Mystery | **ONE character.** Female figure in period dress (empire waist or Victorian) at estate exterior or formal garden; grand manor or gothic house behind her; soft atmospheric mist or golden afternoon light. Expression composed but with tension in the eyes. |
| **The Parlour Secret** | Cosy Mystery / Historical Mystery | **ONE character + props.** Woman at writing desk or armchair; period tea service visible; sealed letter, medicine bottle, or hidden key prominent in foreground; expression knowing or alarmed; warm afternoon window light or candlelight. |
| **Moors at Dusk** | Gothic / Gothic Romance | **ONE character / landscape dominant.** Solitary female silhouette small against windswept moors, ruined abbey battlements, or cliff edge; dramatic sky (storm clouds, pale moon, rolling fog); figure is emotionally isolated against scale of landscape. |
| **Cold Evidence** | Literary Thriller | **ONE character + object.** Subject holds or faces a single charged object (sealed document, decoded letter, photograph, key); near-minimalist background; chiaroscuro; expression unreadable or calculating. |
| **The Threshold** | Family Drama / Medical Drama / Secret Identity | **ONE character.** Figure stands at a doorway, corridor end, or entrance — not yet inside, not outside either. Hospital entrance, family home doorstep, the door of a room she is not supposed to enter. Expression carries the weight of what is on the other side. Desaturated exterior, warm interior light visible through the frame. |
| **Witnessed Distance** | Grief Fiction / Family Drama | **TWO characters** who are not connecting. Both in frame but not touching, not making eye contact — each looking at something the other cannot see or share. The space between them is the visual subject. Muted palette; natural light; no drama of pose. |
| **Gothic Funeral Bride** | Gothic bridal thriller, fake death, buried bride, hidden identity, romance | **TWO characters + coffin/funeral signal.** Bride in white lace gown half-turned over her bare embroidered back; dark male figure behind or beside her. Gothic church, coffin, lilies, mourners, stained glass. Title large in lower third. |
| **City Reclaimed Trio** | Rejected husband / ex-spouse revenge / billionaire return arcs; especially landscape social ads | **THREE characters.** Central male in rain-soaked suit dominates the frame, city skyline behind him; two women flank him as regret and rival claim. Use luxury car, neon rain, corporate towers, bold thumbnail-legible typography. |
| **Royal Claim Family Portrait** | Ownership / ward / age-gap / inheritance / royal or billionaire family drama | **THREE characters.** Adult couple in formal wear at center, child or heir below/between them, palace/estate/garden behind. The relationship triangle is the hook; composition must make inheritance, claim, and power visible. |
| **Desk Deal Near-Kiss** | Boss romance, secret deal, office contract, billionaire boss | **TWO characters.** Office or executive interior; man in suit leans down over woman in fitted blazer/dress; faces almost touching, her hand on his chest or lapel. Title can use script over lower half. |
| **Diaspora City Embrace** | Multicultural contemporary romance, mistake pregnancy, second chance, ordinary people with high emotion | **TWO characters.** Warm city or riverside background; couple in close embrace, eyes closed or almost closed, saturated statement dress on female lead. Emotional warmth beats luxury power. |
| **Rival Cheer Captain Poster** | Sports romance, rival schools, cheerleader/captain, YA-adult college sports | **TWO characters + sports scoreboard.** Cheerleader and team captain in uniforms in foreground; scoreboard and rival athlete in background; bright team colors, handwritten/marker-style title, sticker-like captions. Keep characters adult-coded. |
| **Military Skyline Shield** | Military boss, protector romance, shielded heroine, security romance | **TWO characters.** Male in dress uniform or tactical-formal hybrid stands protectively behind/over heroine against city skyline. Her expression is wary; his posture is controlled. Use medals, rank insignia, night skyline. |
| **Moonlit Wolfless Mate** | Shifter, alpha, rejected mate, wolfless mate | **TWO characters.** Couple in close profile under full moon; pale/white-haired heroine, dark male alpha behind or beside her, wolf silhouette or gothic forest/castle signal. Cold blue moonlight and silver typography. |
| **Ex-Wife Regret Close-Up** | Ex-wife return, no love left, divorce regret, second chance | **TWO characters.** Tight warm close-up; eyes closed or downcast, faces nearly touching, amber-gold background. Low environment detail; emotion and title own the thumbnail. |

---

## Genre Detection Keywords

| Keywords in title | Genre | Style tag |
|---|---|---|
| cultivat / sect / dao / qi / immortal / ascend / spirit realm / xianxia / clan / celestial | Cultivation Fantasy | `hyperrealistic 3D cultivation fantasy, dark misty atmosphere, divine golden light` |
| CEO / billionaire / revenge / empire / tycoon / steel / enemies / forbidden / office / heir | Urban Drama | `cinematic photorealistic urban drama, film still quality, high contrast` |
| palace / imperial / dynasty / court / throne / queen / crown / emperor / concubine / majesty | Historical Court Drama | `hyperrealistic historical court drama, rich imperial colors, candlelight` |
| arranged / contract / marriage / secretly / pretend / fake / fake-dating / forbidden / always / forever | Contemporary Romance | `cinematic photorealistic modern romance, soft luxury atmosphere, warm glow` |
| detective / murder / missing / suspect / truth / shadows / case / killer / silent / dark / lies | Thriller | `dark cinematic thriller, noir rainy atmosphere, chiaroscuro lighting` |
| space / mech / cyber / apocalypse / system / evolution / android / orbital / future / neon | Sci-Fi | `photorealistic sci-fi composite, dark blue black palette, glowing energy, futuristic cityscape` |
| dragon / realm / lord / elf / arcane / magic / shadow / prophecy / fae / chosen / blood / fallen | Dark Fantasy | `hyperrealistic dark fantasy 3D render, user-selected indigo, plum, stone, ivory, or daylight background, gold silver metallic elements` |
| war / army / general / battle / soldier / medieval / crusade / knight / siege / conquer | Historical War Epic | `cinematic historical war epic, dramatic battlefield lighting, iron and fire` |
| ghost / haunted / demon / curse / ritual / possession / spirit / necromancer / eldritch / horror | Horror | `dark horror atmosphere, eerie green glow, cinematic supernatural tension` |
| isekai / reincarnated / another world / hero / quest / level / guild / academy / otome | Isekai / Slice of Life | `vibrant anime-adjacent illustration, bright colors, expressive characters` |
| regency / viscount / viscountess / ton / debutante / season / dowager / duchy / courtship / beau monde / london season | Regency | `painterly regency period photography, warm candlelight and garden light, empire-waist period dress, fine-art editorial` |
| vicar / village / manor / poison / cosy / cozy / spinster / gossip / parlour / drawing room / whodunit / clue / suspect | Cosy Mystery | `warm british editorial photography, afternoon window light, period prop detail, understated atmosphere` |
| moors / abbey / gothic / haunted / sealed / ruin / curse / governess / dark manor / secret room / spectre | Gothic | `dark atmospheric gothic photography, windswept moors, cold moonlight, fog and shadow, painterly composition` |
| spy / barrister / espionage / crown / cold war / traitor / diplomat / classified / whitehall / decoded / cipher / double agent | Literary Thriller | `cold literary thriller editorial, stark chiaroscuro, single charged object, controlled and spare atmosphere` |
| hospital / secret / hidden / daughter / mother / father / family / grief / inheritance / lineage / identity / belong / illegitimate / donor / sibling / reunion / deathbed | Emotional Drama | `desaturated editorial photography, cold-warm contrast, threshold composition, quiet emotional weight, no allure` |
| bride / buried / coffin / funeral / grave / casket / fake death / hidden identity / widow / veil | Gothic Bridal Thriller | `cinematic gothic bridal thriller, white lace against black funeral atmosphere, coffin and stained glass signal` |
| husband / threw away / runs this town / owns this city / rejected husband / discarded husband / ex-husband / revenge return | Rejected Spouse Revenge | `cinematic rain-soaked urban revenge poster, dominant male center, neon city skyline, bold thumbnail typography` |
| owned / claimed / ward / heir / guardian / inheritance / at 18 / at 28 / blessing / palace estate | Royal Claim Family Drama | `opulent estate family-drama romance, formal couple plus heir, roses and palace architecture` |
| secret deal / deal with my boss / billionaire boss / boss / office affair / contract with boss | Boss Deal Romance | `cinematic office romance near-kiss, executive interior, suit and blazer power tension` |
| mistake / should not happen / second chance / pregnancy / family secret / diaspora | Multicultural Contemporary Romance | `warm multicultural contemporary romance, emotional embrace, city river sunset, saturated dress` |
| captain / cheer / rivals / game / team / jersey / quarterback / cheerleader / scoreboard | Sports Romance | `bright competitive sports romance poster, team uniforms, scoreboard, handwritten title energy` |
| military boss / shielded / ruthless military / protector / commander / uniform / bodyguard | Military Protector Romance | `cinematic military protector romance, dress uniform, city skyline, guarded heroine` |
| alpha / wolfless / mate / rejected mate / shifter / pack / wolf / moon | Paranormal / Shifter Romance | `moonlit alpha shifter romance, full moon, cold blue forest, close couple tension` |
| ex-wife / no love / hubby / husband regret / divorce / left for you | Ex-Spouse Regret Romance | `warm amber close-up second-chance romance, faces nearly touching, grief and longing` |

---

## Title Font Style by Genre

| Genre | Title font keywords |
|---|---|
| Cultivation Fantasy | `large bold golden embossed calligraphy with metallic glow, ornate separator lines above and below` |
| Urban Drama | `bold modern sans-serif in silver-white with subtle metallic sheen, clean layout` |
| Historical Court Drama | `elegant golden traditional serif, ornate red-gold border frame` |
| Contemporary Romance | `soft white rounded serif, warm glow, tagline in small italic below` |
| Thriller | `stark white or blood-red condensed sans, sharp and cold` |
| Sci-Fi | `chrome metallic condensed sans-serif, electric blue edge glow, large and aggressive` |
| Dark Fantasy | `large gold embossed fantasy serif with glow halo, tagline text above and below in small spaced serif` |
| Historical War Epic | `heavy stone-carved serif in deep red-gold` |
| Horror | `eerie dripping gothic in sickly green-black` |
| Isekai / Slice of Life | `colorful cartoon outlined bubbly font with star accents` |
| Regency | `elegant italic serif in warm ivory or antique gold, fine decorative hairline rule above and below, period-formal` |
| Cosy Mystery | `warm antiqued serif in deep burgundy or forest green, subtle decorative flourish, approachable but precise` |
| Gothic | `tall condensed serif in pale silver or faded white, slightly irregular letterpress texture, eerie elegance` |
| Literary Thriller | `stark modern serif in cold white or deep charcoal, minimal ornament, compressed letter-spacing` |
| Emotional Drama | `clean quiet sans-serif or refined text-weight serif in muted white or pale grey, no ornament, generous tracking, understated` |

---

## Author Name Style by Genre

| Genre | Author name keywords |
|---|---|
| Cultivation Fantasy | `small refined white serif, faint golden glow, flanked by cloud-scroll ornaments, thin gold horizontal line` |
| Urban Drama | `small clean white modern sans, subtle drop shadow, thin silver divider` |
| Historical Court Drama | `small elegant dark red traditional text, thin golden rectangular border` |
| Contemporary Romance | `small soft white serif, tiny heart or petal motif, light sparkle` |
| Thriller | `small pale grey, near-hidden in shadows, thin cracked line underneath` |
| Sci-Fi | `small crisp white monospace, cyan scanline overlay, geometric bracket flanks` |
| Dark Fantasy | `small bronze medieval script, decorative shield or crest shape` |
| Historical War Epic | `small dignified white serif, double red horizontal line` |
| Horror | `small faded grey-green, slightly tilted, dripping ink line above` |
| Isekai / Slice of Life | `small playful rounded white, pastel outline, star decorations` |
| Regency | `small refined italic serif in cream-gold, thin double hairline rule, period-restrained` |
| Cosy Mystery | `small neat roman serif in muted sage or burgundy, tiny botanical or magnifying glass motif, warm and precise` |
| Gothic | `small faded pale-grey serif, slightly irregular baseline, thin shadow underline` |
| Literary Thriller | `small clean modern serif in cool grey, no ornament, cold and authoritative` |
| Emotional Drama | `small quiet roman or sans in pale grey, no ornament, low contrast against background, honest and undemonstrative` |

---

## Genre Visual Details

### Cultivation Fantasy
- **Render style:** Hyperrealistic 3D dark fantasy render. Character fills 60% of frame, atmospheric world behind.
- **Colors:** Deep black → cold blue gradient base; gold and teal accent; divine white light beams
- **Characters:** Male — long tied or loose hair, sword or artifact held up, flowing dark robes with gold trim. Female — translucent fairy dress, glowing spiritual beast companion, lotus motif.
- **Background:** Vast cloud sea, sacred snow-capped mountains, ancient glowing pagodas, spiritual energy vortex
- **Lighting:** `divine golden light rays breaking through storm clouds, mystical mist, spiritual energy glow radiating from artifact`
- **Composition:** Lone Hero template; title in large gold in lower 35%

### Urban Drama
- **Render style:** Cinematic photorealistic. Film still quality — characters look like real actors in a directed scene.
- **Colors:** Deep grey + cool blue base; warm amber/gold accent for luxury interiors; neon color for night streets
- **Characters:** Power dynamic compositions dominate. Male — tailored suit, sharp jawline, cold or dominant expression. Female — designer clothes or disheveled vulnerability.
- **Background:** Luxury penthouse interior, underground parking, corporate lobby, rainy city streets, gala ballroom
- **Lighting:** `dramatic chiaroscuro, harsh overhead light for power scenes, golden sunset for luxury interiors, neon reflections on wet streets`
- **Composition:** Power Inversion / Intimate Tension / Grand Humiliation templates

### Historical Court Drama
- **Render style:** Hyperrealistic period drama photography. Rich fabric textures, intricate costume detail.
- **Colors:** Imperial red + gold + deep ink black; jade green and imperial yellow accents
- **Characters:** Female — full elaborate court dress, phoenix crown, heavy ornate makeup, hair with gold hairpins. Male — emperor robes or general armor.
- **Background:** Grand palace halls, red-wall courtyards, silk curtains, golden lantern rows, cherry blossom garden
- **Lighting:** `warm golden candle and lantern glow, silk fabric shimmering, shafts of light through palace lattice`
- **Composition:** Duo Confrontation template; female in foreground, imperial setting dominant

### Contemporary Romance
- **Render style:** Cinematic photorealistic. Warm film grain quality, dreamy atmosphere.
- **Colors:** Warm cream + blush pink + soft gold; rainy blue-grey for dramatic variants
- **Characters:** Couple — emotional tension is the subject. Female often vulnerable (white bed sheet clutched to chest, bare shoulders and thighs exposed; or wet, disheveled). Male in open-collar shirt, at rest or looming, watching her. Foreground props: champagne flute, scattered jewelry, luxury items on glass table.
- **Background:** Luxury penthouse bedroom with floor-to-ceiling city skyline windows (golden sunset preferred); or rainy street
- **Lighting:** `golden sunset pouring through panoramic windows, warm rim light on her bare shoulders, cool shadow on the man behind`
- **Composition:** Intimate Tension template (white sheet variant at highest intensity) / Rain Shelter template

### Thriller
- **Render style:** Cinematic dark photography. Stark, high-contrast, emotionally cold.
- **Colors:** Near-black + deep charcoal + cold blue; single accent in blood red or pale yellow
- **Characters:** Silhouette or partial reveal; calm/stone-faced expression. Rain Shelter composition is common — power gap between protector and protected.
- **Background:** Rain-slicked cobblestone streets, European stone buildings, alleys, foggy bridges, or daylight streets as requested
- **Lighting:** `dramatic chiaroscuro, single hard overhead light or street lamp, rain-slicked surface reflections`
- **Composition:** Rain Shelter template with cold power-gap energy

### Sci-Fi
- **Render style:** Photorealistic composite / dark digital painting. Gritty and cinematic.
- **Colors:** Deep blue-black base; electric blue / cyan / purple energy glow; chrome silver
- **Characters:** Male in tactical armor or mech suit, back or side profile, one knee up on a ledge. Expression: steely, determined.
- **Background:** Futuristic cityscape from high above; energy portal / dimensional rift in sky; floating structures, neon corporate towers, crashed ships
- **Lighting:** `electric blue energy glow from portal above, city neon light from below, rim light on armor edges`
- **Composition:** Lone Hero template (back-to-viewer); title in large chrome lower 40%
- **Tagline:** Small serif text at very bottom: short punchy lines referencing the system/power concept

### Dark Fantasy
- **Render style:** Hyperrealistic dark fantasy 3D render. User-selected atmospheric background with coherent broad lighting on characters.
- **Colors:** Near-black base; deep navy/charcoal atmosphere; gold, silver, and burgundy accent
- **Characters:** Male protagonist in dark ornate robes/armor with gold detailing; female in matching dark dress with crown or tiara. Together or side-by-side.
- **Background:** Snow-covered mountains and gothic castle with glowing windows; stormy clouded sky; falling snow or embers
- **Lighting:** `moody dramatic backlight from glowing castle, falling snow catching light, gold trim on costumes catching a rim light`
- **Composition:** Duo Confrontation template (upper 65%); large gold title lower 35%; tagline text top and bottom in small spaced serif
- **Typography note:** Title is the most visually prominent element after characters. Two-line title common: first line smaller, second line very large.

### Historical War Epic
- **Render style:** Cinematic historical epic photography. Textured, weighty, grand scale.
- **Colors:** Iron grey + deep red + earth yellow; amber fire glow accent
- **Characters:** General in battle-worn armor, sword or spear, commanding posture. Army or battlefield context.
- **Background:** Battlefield panorama, fortress walls at dusk, beacon fire towers, war smoke
- **Lighting:** `dramatic sunset over battlefield, beacon fire glow, smoke-filled sky, armor glinting in dying light`
- **Composition:** Lone Hero (general facing battlefield) or Duo Confrontation (rivals)

### Horror
- **Render style:** Dark atmospheric photography with supernatural compositing.
- **Colors:** Ink black + sickly green + dark red; faded paper yellow accent
- **Characters:** Ordinary person (fearful) contrasted with supernatural presence (ghost, demon). Hunter in ritual attire optional.
- **Background:** Cemetery, crumbling ancient temple, alley with paper lanterns, coffin-lined passage; time of day follows the requested palette
- **Lighting:** `eerie green ghost glow, flickering yellow candlelight, cold moonlight, shadows swallowing periphery`
- **Composition:** Lone figure at center, supernatural threat looming from darkness behind

### Isekai / Slice of Life
- **Render style:** High-quality anime illustration style — bright, clean linework, expressive faces.
- **Colors:** Bright multi-color; star / petal / sparkle accents; pastel or vivid depending on tone
- **Characters:** Cute protagonist; cat ears, wings, fantasy school uniform, chibi options
- **Background:** Fantasy isekai world, sparkling academy, starry night sky
- **Lighting:** `magical particle sparkles, soft luminous backlighting, vivid colored light`
- **Composition:** Character facing forward, friendly expression, colorful background

### Regency
- **Render style:** Painterly period photography / fine-art editorial. Warm, texturally rich, compositionally restrained.
- **Colors:** Warm cream, blush, cornflower blue, soft sage; ivory and antique gold accent; muted saturation throughout
- **Characters:** Female in empire-waist gown with gloves, upswept hair, composed expression with underlying tension. Male in Regency coat and cravat, formal posture.
- **Background:** Country estate exterior, formal garden, candlelit ballroom, London drawing room, Vauxhall Gardens at dusk
- **Lighting:** `warm afternoon sunlight through tall sash windows, soft golden candlelight for interiors, dappled garden light for exteriors, overcast English sky`
- **Composition:** Manor Portrait (female alone with estate behind) or Duo Confrontation (social tension between the pair, period costumes matching)

### Cosy Mystery
- **Render style:** Warm British editorial photography. High detail on period props and domestic atmosphere. Interior-focused.
- **Colors:** Warm amber, sage green, cream, deep burgundy; muted and autumnal rather than vivid; fireplace and afternoon light palette
- **Characters:** Female amateur detective — composed, perceptive expression, period-appropriate dress (Victorian or Edwardian). Charged prop in foreground (letter, poison bottle, hidden key, cryptic note).
- **Background:** Cottage parlour, manor library, vicarage garden, village tea room, stone-walled church interior
- **Lighting:** `warm afternoon window light, low fireplace glow, soft fog outside mullioned windows, overcast garden light`
- **Composition:** Parlour Secret template — interior scene with prominent prop and knowing expression; or single figure on misty village lane

### Gothic
- **Render style:** Dark atmospheric photography with dramatic compositing. Atmosphere and landscape are the primary subjects.
- **Colors:** Near-black → deep indigo and forest green; pale moonsilver and fog; single accent of deep crimson or amber lantern glow
- **Characters:** Female figure in period dress, alone, small against the landscape. Expression fearful or quietly determined.
- **Background:** Windswept moors, ruined abbey, gothic manor silhouetted at night, fog-covered cemetery, dark cliff edge above churning sea
- **Lighting:** `cold moonlight breaking through storm clouds, single lantern glow in deep shadow, mist swallowing the middle distance, lightning suggestion in sky`
- **Composition:** Moors at Dusk — figure occupies lower quarter of frame; dramatic sky and landscape dominate the upper 65%; the solitude is architectural

### Literary Thriller
- **Render style:** Cold editorial photography. Controlled, spare, intelligent atmosphere. Period British or cold-war era.
- **Colors:** Deep charcoal, cold white, pale grey; single accent of aged paper yellow or deep red; desaturated throughout
- **Characters:** Protagonist (male or female) holding or facing a single charged object — classified document, decoded letter, photograph, key. Expression unreadable or calculating.
- **Background:** Whitehall corridor, study interior with papers, rain-slicked London street, classified archive room, train platform at night
- **Lighting:** `cold overhead office light, stark window backlight, single angled desk lamp in near-dark room, wet street lamp reflection`
- **Composition:** Cold Evidence template — figure and object in two-thirds of frame; spare background; title in cold condensed serif, authoritative

### Emotional Drama
- **Render style:** Desaturated editorial photography. Quiet, observational, restrained. The camera witnesses rather than directs. No heightened drama of pose or expression.
- **Colors:** Cool grey and muted warm tones; institutional whites and pale blues for exterior/hospital; amber and ochre lamp glow visible through glass or doorways; muted throughout — no saturated color
- **Characters:** One figure alone (preferred) or two figures at distance. Ordinary clothes — no styling toward beauty or power. Expression held still, not performed — the specific stillness of someone who is managing something. Zero allure; no bare skin, no intimate contact.
- **Background:** Hospital corridor or waiting room (clinical, impersonal); family home interior glimpsed through a window or door (warm but distant); an institutional setting where the character does not quite belong; a threshold space — the approach to a door, a parking lot, a waiting area
- **Lighting:** `cool diffuse hospital fluorescent with warm amber lamp glow visible in background, window light that doesn't quite reach the figure, morning light through glass that reveals rather than glamorizes`
- **Composition:** The Threshold template (solo figure at a doorway, cold exterior / warm interior contrast) or Witnessed Distance template (two figures in the same frame, not connecting, space between them is the subject); title in quiet text-weight serif, no ornament

---

## Prompt Quality Checklist

Before sending a prompt to the image API, verify:
- [ ] The frozen scandal or irreversible conflict can be stated in one sentence
- [ ] Every visible character has a distinct relationship role and exaggerated readable reaction
- [ ] A third or fourth figure is included when the premise has a rival, ex, child, parent, witness, or betrayer
- [ ] The cover contains no more than 4 discernible people; larger groups are implied rather than rendered as a readable crowd
- [ ] The image still communicates the relationship conflict at 160px wide with the title hidden
- [ ] No generic couple portrait, romantic embrace, near-kiss, harmonious luxury-family photo, or atmosphere-first movie-poster composition
- [ ] Render style keyword included (`photorealistic` or `hyperrealistic 3D render`)
- [ ] Color palette specified
- [ ] Lighting description included
- [ ] Composition template selected and described
- [ ] Title text placement described (lower 35–40% for fantasy/sci-fi; overlay for drama)
- [ ] `portrait orientation, 2:3 ratio, 1024x1536` specified
- [ ] `professional book cover, ultra-detailed, no watermark` included
- [ ] `keep text inside central safe area (inner 85%)` included
