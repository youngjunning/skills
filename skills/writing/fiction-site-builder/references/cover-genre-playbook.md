# Cover Genre Playbook

> **Traffic-cover override:** many legacy templates below use words such as `cinematic`, `luxury`, `elegant`, `poster`, `near-kiss`, polished couple staging, rim light, or warm-key/cool-fill separation. For paid-traffic fiction, treat those words, compositions, and mixed-light formulas as deprecated unless the user explicitly requests them. Replace them with the anti-premium and lighting-coherence gates in `story-cover.md`: handheld wide-angle phone/cheap-TV freeze-frame, one believable available-light family, matte skin, cramped ordinary set, imperfect faces, active physical conflict, and evidence toward the lens. A movie poster, beautiful couple, wealthy-family group photo, or separately lit/pasted-looking cast is a hard failure regardless of genre.

Full prompt templates for each genre. Load during A2 (cover generation) only — not needed for A2.5 (illustrations).

Reference: `cover-allure-elements.md` for allure tiers, fabric ranking, poses, and exposure tiers.

---

### Reference-Derived CTR Pattern Blocks

Use these blocks when the book title, synopsis, or ad angle matches the pattern. They are extracted from high-CTR romance ad/cover references and normalized into reusable prompt language. Do not mention the reference images in the final prompt; use the pattern directly.

#### Threshold Rejection / Discarded Heir / Family Exile
```
Facebook fiction social-ad creative, story-first short-drama freeze-frame, portrait 2:3.
EXACTLY THREE clearly discernible adults and no other people. Put the wronged protagonist large in the foreground, visibly crying or carrying unmistakable hurt, humiliation, or pleading restraint. Place the two opposing adults together in a warmly lit doorway, estate entrance, courthouse steps, hospital lobby, or other threshold that makes the power structure legible. One antagonist should point, dismiss, block, or deliver the public rejection; the second should react with cold satisfaction, guilt, panic, or sudden fear. The three faces must show strong emotional contrast, not a coordinated pose.
Add one physical abandonment or proof signal in the foreground: a black refuse bag, suitcase, eviction envelope, broken ring, torn photograph, sealed letter, legal folder, medical file, or similar object. The object must be large enough to read at a 160px thumbnail and must explain what has just happened without exposition.
The subtext: they threw her away at the door, but the person they rejected is about to become the person they fear. Make the exit, doorway, steps, rain, or discarded belongings visible so the protagonist's next move is implied.
Use one believable available-light family, warm interior versus cool exterior contrast, ordinary imperfect adult faces, matte skin, and a slightly wide phone-camera or low-budget television freeze-frame. Avoid glossy prestige lighting, empty cinematic atmosphere, crowd scenes, generic mansion portraits, and neutral expressions.
Keep the entire raster asset as clean, image-only artwork. Do not generate or composite the title, author, hook, subtitle, logo, genre chip, watermark, UI, signage, or readable lettering into the image. Any Facebook hook copy belongs in the ad/page layer outside the image.
```

#### Facebook Hook-Card / Story-Beat Freeze-Frame
```
Facebook fiction social-ad creative, vertical short-drama hook card, portrait 9:16 or 2:3.
This is a story beat, not a prestige book jacket: freeze the exact second before or after a life-changing reveal. Use exactly THREE adult people and no crowd. One person must be visibly crying, humiliated, pleading, wronged, or emotionally abandoned; the other two must create a sharp emotional counterpoint through panic, guilt, accusation, indifference, seduction, triumph, or fear. Make the relationship geometry obvious through height, distance, a blocked exit, a bed, a certificate, a ring, a contract, a phone, a hospital chair, or a pointing/reaching hand.
Use one large physical proof or consequence object in the foreground: marriage certificate, legal document, hospital file, recorder, suitcase, broken ring, medical bill, envelope, or discarded belongings. The object must read as an object at 160px, even if its small text is not legible.
Use ordinary melodramatic settings—wedding altar, mansion entrance, bedroom, hospital room, courthouse, dining room, or rainy doorstep—with one coherent available-light family. Slight softness, phone-camera imperfection, and short-drama still quality are acceptable; glossy luxury-poster polish, empty atmosphere, and generic smiling couples are not.
The image itself contains no hook copy. If a separate ad/page layer later adds a hook, keep it consequence-led, short, high-contrast, and outside faces, hands, and the proof object. Never put browser/fullscreen notices, platform watermarks, channel names, or copied UI chrome into the image.
The winning read should be paraphrasable in one breath: “She was forced to marry him while he was unconscious,” “Her father sold her to pay a debt,” “He betrayed her, so she married his uncle,” or “They threw her out, then feared what she became.”
```

#### Gothic Funeral Bride / Buried Bride
```
Romance novel cover, cinematic photorealistic gothic bridal thriller atmosphere.
FRAMING: portrait 2:3, medium-full shot from knees to crown, bride center-dominant, male figure behind her.
TWO characters plus funeral environment. Bride in elaborate white lace wedding gown, bare embroidered back visible, pearl buttons down the spine, sheer veil trailing behind; she turns over her shoulder toward the viewer with wide controlled eyes and parted lips, the expression of a woman standing inside the lie everyone else believes.
Male figure behind her in black formal coat or investigator's dark suit, face half in shadow, close enough to claim the frame but not touching; his expression is severe, protective, and suspicious.
Background: gothic church interior, coffin or casket with white lilies at left or lower frame, black-clad mourners blurred in the back, tall stained-glass window casting cold blue and violet light, white roses on dark stone.
The subtext: they buried the bride, but she is standing beside the man who was meant to find her body.
Color palette: ivory lace, deep charcoal, cold blue stained glass, muted crimson rose accents.
Lighting: cold window backlight on veil and lace, small warm candlelight on her cheekbone, deep shadow behind him.
Title large in ornate gothic serif across lower third; author small at bottom. Photorealistic editorial photography, no watermark.
```

#### Rejected Husband Owns the City / Urban Revenge Landscape
```
Romance social ad creative or book cover, cinematic rain-soaked billionaire revenge poster.
FORMAT: landscape 16:9 for ad creative, portrait 2:3 for book cover.
THREE characters. Central male dominates the composition in a black suit and loosened white shirt, rain-wet hair, jacket open, standing in front of a neon night city skyline and luxury black car. His expression is cold certainty — the man they threw away now owns the city.
Left female figure: former wife or regret figure in sleek evening dress, turned partly away, face tense with realization. Right female figure: new rival claim or woman who believed in him, closer to his side, watching him with intensity.
Background: dense skyscrapers, fictional corporate signage, wet street reflections, dark luxury car, rain streaks catching blue and gold neon.
Add thumbnail-legible design: bold serif or condensed sans title in upper left; optional bottom icon row with short trope labels such as rejected husband, billionaire revenge, betrayal and regret.
Color palette: black, steel blue, neon gold, rain silver, white shirt highlight.
Lighting: city neon rim light on his shoulders and jaw, secondary women in partial shadow, skyline sharp enough to read at mobile size.
```

#### Royal Claim Family Drama / Owned and Claimed
```
Romance novel cover, opulent estate family-drama atmosphere.
FRAMING: portrait 2:3, full-body or three-quarter shot, palace or grand estate behind.
THREE characters. Adult couple in formal evening wear stand close at center: man in black tuxedo leaning down with protective possession, woman in deep red fitted gown with neckline and jewelry catching warm light. A child or heir stands below or between them in formal suit, looking directly at the viewer, making inheritance and claim instantly visible.
The female lead's expression: composed but emotionally trapped between duty and desire. The male lead's expression: controlled possession, forehead nearly touching hers. The child's expression: solemn witness.
Background: baroque palace facade, rose garden, gold sunset, red roses in foreground.
The subtext: one claim began when she was powerless; the second one came when she understood what power meant.
Color palette: deep red gown, black tuxedo, warm gold architecture, dark green garden, rose accents.
Lighting: golden-hour backlight around the couple, warm light on faces, background slightly magical but still photorealistic.
Title large in elegant gold serif/script mix across lower center; author beneath.
```

#### Secret Deal With My Billionaire Boss / Office Near-Kiss
```
Romance novel cover, cinematic photorealistic office romance, secret contract tension.
FRAMING: portrait 2:3, medium shot from waist to crown, faces and upper bodies readable.
TWO characters in executive office interior. Male lead in black suit and white shirt leans down over female lead with one hand braced near her, the other near her waist or lapel; his expression is controlled hunger under corporate restraint. Female lead in fitted blazer or sleek dress leans up toward him, one hand on his chest, lips parted, eyes half-closed but conflicted.
Faces almost touching — a near-kiss, not a kiss. The physical gap is the story.
Background: glass office blinds, city lights, desk edge, contract papers or pen barely visible in foreground.
The subtext: the deal was supposed to be professional until the room got too small.
Color palette: charcoal suit, ivory skin highlights, warm amber office light, cool blue city reflection.
Lighting: warm key light on faces, cool rim light from window blinds, shallow depth of field.
Title in script + bold serif combination across lower half; author small beneath.
```

#### Multicultural Mistake / Warm City Embrace
```
Romance novel cover, warm multicultural contemporary drama atmosphere.
FRAMING: portrait 2:3, medium close-up from chest to crown, couple centered.
TWO characters. Black woman in vivid red dress or blouse, hair in elegant updo or natural style, eyes closed with guarded tenderness; male lead in dark shirt or suit, forehead and nose close to hers, eyes lowered, one hand at her back or shoulder.
Their bodies are close but the emotion is regret and tenderness, not dominance.
Background: warm city riverfront or old city skyline at sunset, soft bokeh, amber sky.
The subtext: the mistake should not have happened, but it changed everything.
Color palette: saturated red dress, warm amber sky, dark suit, bronze and deep brown skin tones.
Lighting: sunset rim light around profiles, soft warm fill on faces, high emotional warmth.
Title at top or lower third in strong serif, key word in red if typography is included; author small at bottom.
```

#### Rival Cheer Captain / Bright Sports Poster
```
Romance novel cover, bright competitive sports romance poster, adult college or pro-sports energy.
FRAMING: portrait 2:3, full-body or medium-full shot, both figures readable.
TWO main adult characters plus rivalry background. Female lead in cheer or dance-team uniform, pom-poms or team colors visible, leaning toward male captain; male lead in basketball/football jersey with captain marker, tall and athletic, one arm around her waist or close behind her. Both read as 21+ adults.
Background: scoreboard with close score and final seconds, arena lights, rival player or opposing team figure in background looking on, crowd blur.
The subtext: rival teams, public stakes, private surrender.
Color palette: hot pink or team red accent, navy/white uniform blocks, bright arena light.
Lighting: glossy arena lights, energetic high-key contrast, confetti or scoreboard glow.
Typography: handwritten marker-style title with stickers, hearts, underlines, arrows, and small caption callouts; keep all text large enough for mobile thumbnail.
Safety: no high-school coding, no minor-looking faces, no school uniforms; adult college/pro visual language only.
```

#### Military Skyline Shield / Ruthless Protector Boss
```
Romance novel cover, cinematic military protector romance, night skyline drama.
FRAMING: portrait 2:3, medium shot from hip to crown.
TWO characters. Male lead in dark dress uniform or tactical-formal jacket with subtle rank insignia and medals, standing behind or beside heroine, body angled protectively over her shoulder. His expression: stern, disciplined, ruthless toward the world outside the frame. Female lead in dark dress or coat, hair wind-tossed, looking toward the viewer with wary vulnerability.
Background: high-rise window or rooftop with iconic night skyline, city lights blurred, military insignia or security badge catching light.
The subtext: she became the mission he was not supposed to want.
Color palette: black uniform, gold insignia, cool blue city lights, warm skin highlights.
Lighting: cool skyline rim light, warm key on her face, hard highlight on his jaw and medals.
Title in elegant script for the emotional word plus bold serif/sans for military/boss words.
```

#### Wolfless Mate / Moonlit Alpha Shifter
```
Romance novel cover, cinematic photorealistic paranormal shifter atmosphere.
FRAMING: portrait 2:3, tight medium shot from chest to crown, couple large in frame.
TWO characters. Pale or white-haired heroine in grey cloak or fitted dress, exposed throat and collarbone, expression torn between fear and longing. Dark-haired alpha male in black coat or open-collar shirt stands close behind or beside her, face near her temple or cheek, expression controlled and possessive.
Background: full moon huge behind them, gothic forest or castle silhouette, faint wolf silhouette or shadow in the distance.
The subtext: the pack called her wolfless; the alpha recognized something they could not see.
Color palette: cold blue moonlight, silver hair, black coat, pale skin highlights.
Lighting: moon rim light on hair and jaw, soft cold fill on faces, deep blue-black background.
Title in silver fantasy serif with faint glow; author at bottom.
```

#### Ex-Wife Regret / No Love Left Close-Up
```
Romance novel cover, warm amber second-chance regret atmosphere.
FRAMING: portrait 2:3, tight crop from upper chest to crown, faces large and emotional.
TWO characters. Male lead in dark shirt or suit, forehead almost touching female lead, eyes down or closed, jaw tense with regret. Female lead with blonde or light hair or story-accurate hair, eyes closed or downcast, expression exhausted from loving someone too long.
No smiling, no wedding-photo energy. This is grief, regret, and a final chance.
Background: warm blurred interior or chandelier bokeh, minimal props, emotional faces dominate.
The subtext: he came back after she had already taught herself not to need him.
Color palette: amber gold, deep brown shadow, cream skin highlights, dark suit contrast.
Lighting: soft warm key across their faces, shallow depth of field, background nearly abstract.
Title large across lower third in bold serif with one script/emotional word; author beneath.
```

---

### Genre-Specific Prompt Formulas

### Contemporary Relationship-Pressure Cover Selector

Use this selector before choosing a billionaire, contract-marriage, divorce, or second-chance prompt. The cover must show a story event and an agency signal, rather than a generic possessive pose.

| Core promise | Focal composition | Mandatory proof of agency | Avoid |
|---|---|---|---|
| Contract / marriage bargain | Two adults separated by a document, key, ring, or deadline object; charged distance rather than contact | Both can leave the frame; the heroine controls or contests one material term | Generic penthouse embrace with no visible bargain |
| Marriage deterioration | One protagonist foregrounded with an interrupted domestic ritual; partner distant or absent | Her next action, packed item, message, or doorway makes choice visible | Wedding-photo warmth, mutual longing without a rupture |
| Divorce / public reversal | Heroine faces viewer at the institution where power changes; former partner registers the change | Proof object, professional role, witness, or open route of exit | Luxury makeover as the only evidence of power |
| Reconciliation after harm | Physical distance remains; the person seeking repair is visually lower in access or outside her space | Her posture and environment make refusal credible | Grabbing, blocking, ownership poses, or a forced near-kiss |

If a relationship-pressure cover needs an intimacy cue, use eye-line, distance, or a hand paused short of contact. Never use physical control to communicate passion. Keep the scene's evidence object legible at mobile size, and pair it with copy that asks what the object changes rather than restating what it is.

#### romance / Billionaire Romance
```
Romance novel cover, cinematic photorealistic quality, luxury atmosphere with strong contrast.
FRAMING: full-body shot, both figures visible from feet to crown, three-quarter angle facing viewer.
TWO characters. Powerful man in charcoal suit with shirt fully open revealing his
defined chest, one hand gripping the woman's jaw from below tilting her face up to his,
his other hand gripping her bare lower back pulling her hips flush against him from the front.
Both figures face the viewer — full torsos, legs, and clothing visible in frame.
His expression: cold, absolute, the expression of a man accustomed to getting exactly
what he wants and currently deciding whether to take it — controlled hunger, dangerous patience.
Woman in a floor-length backless gown — extreme décolletage plunging to the sternum,
thigh-high slit baring the full leg, her voluptuous hourglass figure against his suit;
her fingers clutching his lapel — not to pull him closer, not to push him away, the ambiguity
is the story; lips parted and trembling, eyes half-closed, expression of someone losing an
argument she made with herself three months ago.
Faces one centimeter apart. The moment before everything changes.
Background: luxury penthouse, floor-to-ceiling city lights at night, the entire city below.
Color palette: charcoal, midnight black, ivory skin, single amber candlelight slash.
Lighting: single hard side light carving her bare legs and his jaw out of darkness.
Title '{title}' in elegant silver serif at top. Author '{author}' at bottom.
Portrait 2:3, photorealistic, ultra-detailed, no watermark.
```

#### Paranormal / Shifter Romance
```
Romance novel cover, cinematic photorealistic quality, dark paranormal atmosphere.
FRAMING: full-body shot, both figures visible from feet to crown, three-quarter angle facing viewer.
TWO characters. Man with powerful bare muscular torso — shirt completely removed,
defined abs and chest catching moonlight — standing beside woman, his body pressed
against her side, one forearm low across her abdomen pulling her into him, his other
hand at the side of her jaw — steadying, not directing. Both figures at three-quarter
angle toward the viewer — both faces toward the camera, neither looking at the other.
His bare chest and abs visible, her voluptuous figure from feet to crown.
His expression: absolute cold possession, eyes glowing amber, jaw tight —
looking at the camera, not at her. Her expression: fierce surrender, eyes forward
toward the viewer.
Woman in a torn flowing ivory dress — one shoulder completely bare, neckline
plunging to the sternum, fabric clinging to and slipping from her voluptuous hourglass
figure; lips parted and trembling, eyes wide with the expression of someone who knows
this is dangerous and cannot make herself stop.
One hand gripping his forearm — fingers pressing in, knuckles white — not pulling
away, holding on. A glowing silver wolf tattoo on her wrist visible in the moonlight.
The emotional subtext: she is losing a fight she started against herself.
Background: moonlit forest clearing, full moon through ancient oak trees, silver-blue
mist pooling at ground level — both full figures visible against the mist.
Color palette: cold silver moonlight, deep forest black-green, warm amber from his eyes, ivory skin.
Lighting: cold silver rim light from the side sculpting both figures, warm amber glow from his eyes.
Title '{title}' in weathered silver fantasy serif with faint glow. Author '{author}' at bottom.
Portrait 2:3, photorealistic, ultra-detailed, no watermark, text inside central safe area inner 85%.
```

#### Vampire Romance
```
Romance novel cover, cinematic photorealistic quality, gothic romance atmosphere.
FRAMING: medium-to-full-body shot, both figures from hip to crown facing viewer at three-quarter angle.
TWO characters. Man in dark Victorian coat, pale aristocratic face, standing beside woman
at a slight angle — his face turned toward her neck from the side closest to the viewer,
lips grazing her exposed throat. Her head tilts away from him — toward the camera —
so her face is visible to the viewer: eyes closed, lips parted in complete overwhelmed surrender.
His profile is visible at the edge, cold absolute possession; her full face catches the candlelight.
One hand gripping her hair at the root, the other splayed possessively across her bare stomach
pulling her against him — both his hand and her exposed midriff visible to the viewer.
Woman in deep burgundy gown with extreme plunging neckline — one shoulder slipped,
fabric barely clinging to her voluptuous figure, back arched so her chest lifts toward the light,
fingers pressing into his forearm — not pulling away, anchoring herself.
Both figures from hip to crown clearly in frame — her dress, his coat, her bare shoulders and chest.
The emotional subtext: she came here to fight and forgot why the moment he touched her.
Background: candlelit gothic stone chamber, scattered rose petals on cold floor, centuries of silence.
A single stained-glass window above casts fractured violet and red light.
Color palette: deep burgundy, ivory skin, black, warm gold candlelight, fractured violet.
Lighting: warm candlelight on her throat and exposed chest, violet from stained glass catching her shoulder.
Title '{title}' in gothic elegant serif. Author '{author}' at bottom.
Portrait 2:3, photorealistic, ultra-detailed, no watermark.
```

#### Fantasy Romance / Dark Fae
```
Romance novel cover, cinematic fantasy photorealistic quality, dark ethereal atmosphere.
FRAMING: medium-to-full-body shot, both figures from hip to crown, three-quarter angle facing viewer.
TWO characters. Fae male in dark armor or black robes with silver detail, inhumanly beautiful
pointed features, his hand at the side of her jaw — steadying, not directing — both faces
at three-quarter angle toward the viewer, both looking toward the camera, the charged gap
between their faces one inch apart but neither breaking to look at the other.
Both figures face the viewer — clothing and figures readable from hip to crown.
His expression: cold ancient amusement and absolute want, looking at the camera —
the expression of someone who has never been told no and finds it unexpectedly interesting.
Woman in sheer silver flowing gown with deep plunging neckline, bare shoulders, bare midriff —
fabric billowing from wind that doesn't exist, her hair unbound with tiny flowers woven in;
her hand pressed flat against his armored chest — the gesture could be stopping him or
steadying herself — her own expression a war: the part of her that knows better and the part
of her that is already gone.
Magical light pulses between their faces in the charged space — her human warmth, his fae cold —
a visible current of power exchange.
The subtext: she bargained for something else entirely. She didn't read the fine print.
Background: moonlit ancient fae ruins, crumbling carved stone arches, silver-violet magical mist
pooling at ground level, bioluminescent flowers growing from the cracks.
Color palette: deep midnight violet, silver, ivory complexion, black armor, bioluminescent teal accents.
Lighting: silver magical glow from the charged space between their faces, full moonlight from above.
Title '{title}' in silver fantasy script with faint magical glow. Author '{author}' at bottom.
Portrait 2:3, photorealistic, ultra-detailed, no watermark.
```

#### Mafia / Cartel / Organized Crime Romance
```
Romance novel cover, cinematic photorealistic quality, high-contrast thriller romance.
FRAMING: full-body shot, both figures visible from feet to crown, three-quarter angle facing viewer.
TWO characters, but the frame must read like a frozen scene from a television episode, not a posed fashion shot.
Show a specific moment in the story: she has just realized something dangerous, or is about to run, or has just been caught.
Man in sharp charcoal suit reaching toward her or stepping into her path — not caressing pose, but action. His expression: controlled danger, the split second before he decides whether to protect, stop, or claim.
Woman in a sleek fitted dress or coat-dress with movement in the fabric — coat flaring, hair blown back, body half-turned as if she is mid-step. Her expression must carry alarm, defiance, or shocked recognition.
The subtext: the room has changed in the last second and both of them know it.
Background: a luxury rooftop, street-level confrontation, or penthouse interior with a visible threat cue — open car door, shattered glass, flashing headlights, a phone lit up with bad news, or another figure just out of focus.
Color palette: charcoal, ivory, deep emerald or red, muted gold, one vivid accent from a hazard source.
Lighting: clean cinematic key light with enough brightness to read faces and motion clearly.
Composition note: make the scene feel like a story beat, with tension, interruption, and immediate consequence visible at thumbnail size.
Title '{title}' in bold condensed serif. Author '{author}' at bottom.
Portrait 2:3, photorealistic, ultra-detailed, no watermark.
```

#### Contemporary Romance (Fake Dating / Marriage of Convenience)
```
Romance novel cover, cinematic photorealistic quality, intimate contemporary atmosphere.
FRAMING: medium shot, both figures from hip to crown facing viewer — NOT a face-only crop.
TWO characters. Man in casual open-collar shirt or rolled-sleeve button-down,
bodies pressed together, his hand cradling her bare jaw tilting her face up to his,
faces close — noses nearly grazing, eyes barely open.
Her hand pressed flat to his chest over his heart — she can feel his pulse.
The held breath of the moment before they stop pretending.
His expression: guarded and already lost — a man who agreed to a deal and did not expect to mean it.
Her expression: surrender under protest — brows furrowed slightly, lips parted.
She is wearing a silk slip dress with one strap slipped, bare shoulder visible, waist and hips in frame;
his open shirt showing his chest — skin to skin in a moment that was supposed to be business.
Medium shot from hip to crown so both figures' bodies are in frame — dress, slipped strap,
his open chest — NOT cropped to faces alone.
The subtext: the contract said sixty days. She stopped counting at fourteen.
Background: warm golden interior — a luxury hotel room, rain-streaked window, city
lights soft and blurred, unmade bed in peripheral.
Color palette: warm amber, ivory skin, soft cream shadows, champagne gold.
Lighting: golden hour through rain-streaked glass, soft diffused warm glow.
Title '{title}' in warm elegant serif. Author '{author}' at bottom.
Portrait 2:3, photorealistic, ultra-detailed, no watermark.
```

#### Sports Romance
```
Romance novel cover, cinematic photorealistic quality, charged competitive atmosphere.
FRAMING: full-body shot, both figures from feet to crown, three-quarter angle facing the viewer.
TWO characters both at three-quarter angle facing the viewer — NOT in side profile facing each other — both bodies fully readable.
He bare chest or fitted athletic shirt torn open, muscular torso and abs fully visible —
sweat-sheened, still running warm from competition. He looks toward her with controlled intensity,
jaw tight, not letting himself look away, his gaze cutting toward her but his body angled to camera.
His expression: defiance + desire — he's been told she's off-limits and cannot find a reason
that still makes sense. Eyes dark, decision already made.
She at three-quarter angle toward the viewer, in fitted athletic wear — sports bra, high-waist leggings,
bare midriff fully exposed, voluptuous figure forward — chin raised, her gaze forward;
her hand gripping his jersey or forearm. Full body visible — her athletic figure from feet to crown,
his bare torso, both fully in frame.
Background: golden-hour empty stadium tunnel, dramatic light shafts from above cutting through dust.
Color palette: warm amber and deep gold, deep shadow, team colors as accent on her wear.
Lighting: directional golden light sculpting his bare torso and her bare midriff, both catching every beam.
Title '{title}' in bold condensed athletic serif. Author '{author}' at bottom.
Portrait 2:3, photorealistic, ultra-detailed, no watermark.
```

#### Accidental Marriage / Woke Up Wed (Contemporary)
```
Romance novel cover, cinematic photorealistic quality, charged morning-after atmosphere.
FRAMING: medium shot, both figures from hip to crown, both facing toward the viewer.
TWO characters. Man in rumpled dress shirt with two buttons open, sleeves half-rolled —
facing toward the viewer and toward her, expression unreadable, controlled intensity.
His expression: shocked recognition — the expression of a man who woke up to a consequence
he cannot undo and is deciding whether he wants to.
Woman sitting on the edge of the luxury hotel bed facing the viewer, wrapped in a white sheet
clutched to her chest — bare shoulders and legs from mid-thigh down fully visible, hair disheveled,
last night's makeup slightly smudged; holding up a marriage certificate with one hand,
expression of raw vulnerability — lips parted, eyes wide.
Both figures in medium shot, full torsos and faces readable, seated her / standing him
both oriented toward camera.
Two champagne flutes on the nightstand. One overturned. Scattered rose petals.
Background: floor-to-ceiling luxury hotel penthouse windows, golden morning city skyline.
Color palette: ivory white sheet, warm golden morning light, charcoal gray of his shirt.
Lighting: golden sunrise through panoramic windows, warm rim light on her bare shoulders.
Title '{title}' in warm contemporary serif. Author '{author}' at bottom.
Portrait 2:3, photorealistic, ultra-detailed, no watermark.
```

#### Revenge Return / Secret Children (Family Drama Romance)
```
Romance novel cover, cinematic photorealistic quality, high-stakes emotional drama atmosphere.
FRAMING: full-body shot, primary figure from feet to crown, facing the viewer.
TWO characters — or ONE if drama context calls for it. Primary: woman in elegant power dress
or tailored suit, standing straight facing the viewer, chin raised — returned from exile and
dressed like a reckoning. Her full figure visible — dress, heels, the posture of someone
who rebuilt herself into something they cannot stop.
Her expression: cold possession of her own narrative — jaw set, a ghost of a smile
that contains six years of planning. Eyes facing the viewer.
Optional secondary character: the man from her past, to her side facing slightly away
or toward her with stunned recognition — he is seeing someone he thought he knew.
His hand half-raised toward her, caught between reaching and not daring.
If children are visible: a child's hand in hers at the edge of frame — not the
subject, but the subtext: proof of everything they tried to erase.
The subtext: they erased her name. She came back as a headline.
Background: grand family estate entrance or a glass-and-marble corporate lobby.
The doors are open because she walked in, not because she was invited.
Color palette: deep cold teal or steel blue dress, ivory marble, warm amber interior light.
Lighting: cold overcast light catching her full figure from crown to feet — she is the center.
Title '{title}' in sharp contemporary serif — clean lines, authority. Author '{author}' at bottom.
Portrait 2:3, photorealistic, ultra-detailed, no watermark.
```

#### Hidden Heiress Divorce Revenge / Proof at the Gala
```
Romance novel cover, cinematic photorealistic corporate-family revenge drama, opulent gala at the instant power changes hands.
FRAMING: portrait 2:3, medium-full shot, heroine standing center-dominant; ensemble conflict readable behind and around her.
FOUR adult characters. Heroine in a deep wine, emerald, or ivory evening gown, composed and upright, holding one thumbnail-legible proof object: a black-gold founder seal, signed share register, trust amendment, audit ledger, or board proxy. Her hand and the object are sharply lit. Her expression is controlled agency after a finalized exit—not seduction, victimhood, or smugness.
Former husband lower or off-center, formally dressed, facing the evidence rather than touching her; his expression shows recognition and accountability, not ownership. A family conspirator and status rival stand on opposite sides behind him, visibly reacting in different ways so the opposition reads as a network rather than one jealous woman. Optional auditor, lawyer, or board chair may replace the rival when institutional authentication is the stronger story beat.
Background: chandelier-lit hotel ballroom, shareholder gala, or estate reception with blurred witnesses, press cameras, and a board display or corporate crest. Include a subtle divorce-finality cue such as a sealed document folder or removed wedding ring near the proof object; no kneeling proposal pose.
The subtext: they erased her name, finalized her divorce, and invited her back as a nobody. The document in her hand decides who controls the company before midnight.
Color palette: burgundy or emerald, black formalwear, warm chandelier gold, one cold white spotlight on the proof object.
Lighting: warm gala ambience with a clean hard key on her face, hand, and evidence; former husband one stop darker; conspirators separated by rim light.
Composition priority: heroine first, proof object second, ensemble reactions third. Do not reduce the reversal to jewelry, a luxury car, or a glamorous makeover.
Safety: all characters clearly adult; no intoxication, bedroom framing, coercive contact, sexualized humiliation, or reconciliation-as-possession imagery.
Title '{title}' in elegant high-contrast serif across upper third; author '{author}' at bottom.
Portrait 2:3, photorealistic, ultra-detailed, no watermark.
```

#### Romantasy (Romance-Fantasy Fusion)
```
Romance novel cover, semi-realistic illustrated or hyperrealistic 3D render style — NOT photographic
realism, NOT anime. TWO characters.
Female lead center-left: fantasy battle leathers or an asymmetric gown with one armored leg exposed,
deep jewel-tone fabric (midnight blue, blood red, or deep emerald), one hand gripping a glowing
rune-etched sword or trailing warm golden magic from her palm.
Her expression: defiance bleeding into something she has not named yet — jaw set, eyes on him,
body half-turned as if she started to leave and changed her mind.
Male figure right of center: dark plate armor with silver-edged sigils or heavy royal robes over
a broad frame, expression controlled but with one detail that breaks the control — a hand reaching
toward her that stops just short of contact.
One dominant symbolic object occupies the vertical center between them: a serpent coiling upward,
a dragon skull at frame edge, a crown of bone, or a crystal key.
The charged space between their bodies emits an ethereal magical glow — her light warm gold,
his cold blue or silver — the two tones bleeding together at the midpoint, neither winning.
The subtext: she was trained to destroy him. She did not expect the glow to appear when they
stood this close.
Background: suggestion of a fantasy environment (carved stone arch, ruined citadel, fae forest
silhouette) in soft focus — it frames without competing.
Color palette: deep purple or midnight blue base with blood red or emerald accent,
bioluminescent or candlelight lighting on faces, cold silver on his armor.
Lighting: ethereal magical glow from the space between them as primary source,
cold moonlight rim from above, deep shadow filling the rest.
Title '{title}' in whimsical script font, large, top third of frame.
Author '{author}' in bold condensed secondary font below title.
Portrait 2:3, ultra-detailed, no watermark, single dominant mobile-legible element (the magical glow).
```

#### Regression Romance / Second-Chance Time Loop
```
Romance novel cover, cinematic quality, muted time-displaced atmosphere.
Primary composition: single dominant female figure OR double-exposure layered composition.
Foreground: the heroine as she is now — standing with deliberate stillness in contemporary tailored
power dress or period court gown, posture radiating cold possession of her own narrative.
Her expression: cold possession — not grief, not fear, the specific expression of a woman who
has already lived this scene and knows exactly how it ends. Jaw set, gaze forward, mouth with
the faint certainty of someone counting down.
Background ghost layer at 40% opacity: her past self in similar clothing but collapsed,
defeated, or mid-fall — the moment of original betrayal, soft and translucent behind her certainty.
Male figure: if present, turned away from camera or in soft focus at frame edge — his ignorance
of what she knows is communicated by his averted gaze. He is not the center.
One color break in the otherwise muted palette: blood red at the ghost layer's heart for the
original death or betrayal moment, deep sapphire at her hands or feet for the reset point.
The subtext: she died knowing exactly where it went wrong. She woke up with the map.
Color palette: muted gold and grey base, desaturated, both tones blending until the color break.
Matte quality — no neon, no high saturation. The palette communicates weight.
Lighting: cold ambient light on the foreground figure, soft warm diffuse on the ghost layer
behind — the past is warmer, the present colder and more certain.
Title '{title}' in elegant serif or calligraphic script, muted gold. Author '{author}' in clean grey beneath.
Portrait 2:3, ultra-detailed, no watermark.
```

#### Villainess Redemption / Reverse Isekai Romance
```
Romance novel cover, cinematic quality, opulent historical fantasy atmosphere.
Single female figure, center-dominant, filling two-thirds of vertical frame.
She wears elaborate historical fantasy court regalia: full ball gown with intricate beading,
lace overlay, or embroidered panels in deep emerald or burgundy with antique gold trim —
the dress of a condemned woman who chose to wear it anyway.
Her expression is the critical element — achieve precisely: knowing, slightly amused, composed.
NOT victimized. NOT action-heroine fierce. NOT tragic. She looks directly out of frame or
slightly past the viewer as if she sees something beyond the image. The slight curve of her mouth
and the steadiness of her gaze communicate one thing: she has read the ending and is not afraid of it.
Male figure optional; if present, secondary — partially visible at frame edge, facing slightly away,
unaware of what she knows.
The subtext: she woke up as the villainess. She has read this story. The script is about to change.
Background: imperial court interior or palace exterior, warm candlelight and antique gold,
architecturally detailed but soft focus — the figure reads first.
Color palette: deep emerald, burgundy, antique gold, warm cream at highlights. Rose gold overall
register — opulent and knowing, not suffering.
Lighting: warm candlelight from below catching the embroidery and her jaw, soft ambient court
light filling the background, nothing harsh — she is at home here.
Title '{title}' in calligraphic or fine-serif script, rose gold or cream, upper frame.
Author '{author}' in smaller matching serif below.
Portrait 2:3, ultra-detailed, no watermark.
```

#### Monster Romance / Interspecies Romance
```
Romance novel cover, cinematic quality, dark boundary-threshold atmosphere.
TWO figures. Non-human male occupies the larger vertical portion: massive, scaled or shadowed,
marked as non-human — but ONE detail is distinctly human and is the emotional pivot of the image:
a hand extended toward her, palm open, fingers slightly curled; OR a head tilted in attention,
ear angled toward the sound of her; OR eyes tracking her with an intensity no predator uses for prey.
His form is dark, muted, powerful. Bioluminescent accent color (teal, amber, or violet) emanates
from his markings, eyes, or form edges — single saturated color against the near-black,
drawing the eye to the one human gesture he is performing.
Human female figure: smaller in scale, placed close or just within his reach, wearing ordinary
or torn clothing — nothing elevated that equalizes the power scale.
Her expression: the exact moment she realizes she is the only safe person in his world.
Not fear. Not love yet. Recognition — the thing that frightens everything else has rearranged
itself for her specifically, and she has just understood this.
The subtext: everyone in the village knows what lives in the forest. No one comes back.
She is the first one they sent in who was not meant to survive.
Background: dark forest, ruins, or boundary threshold — near-black with organic texture,
bark or stone or collapsed archway, the boundary between the human world and his.
Color palette: near-black base, single bioluminescent accent (her choice — teal most common),
deep forest shadow, the warm skin tone of her face as the only human-warm element.
Lighting: bioluminescent accent from his markings as primary source on her face,
ambient dark engulfing everything else, her face the only warmth in the frame.
Title '{title}' in bold or brushstroke display font in the accent color. Author '{author}' in muted grey beneath.
Portrait 2:3, ultra-detailed, no watermark.
```

#### Dark Academia Romance
```
Romance novel cover, cinematic quality, candlelit institutional atmosphere.
TWO characters in chiaroscuro — one hard candle or oil lamp source carving both faces from
near-total shadow, warm amber light on cheekbones and brows, everything else falling into
deep burgundy-black.
Male figure: academic or institutional authority visible in clothing (waistcoat, open-collar dress
shirt, reading glasses pushed up, or society insignia at lapel), body angled toward her across
a table or in a doorway. His expression: barely-controlled want masked as intellectual contempt —
control that is visibly costing him something. He has not decided what to do with what he knows.
Female figure: her expression openly reads what his does not — she has found something out about
him, and she has not yet decided what to do with it. Not fear. The specific confidence of a woman
who holds information as currency.
Bodies angled toward each other, the charged gap between them is visible negative space —
deliberate and composed, the emotional argument of the image.
Secondary props in soft focus: a single raven on a windowsill, old paper or open book between
them on the table, one extinguished candle with smoke still rising, rain-streaked window
showing only darkness beyond.
The subtext: at this institution, every secret has a price. She just found out what his costs.
Color palette: deep burgundy, candlelight amber, aged parchment, near-black.
No neon, no digital brightness, nothing glossy. Matte finish.
Lighting: single candle as the only source — warm amber carving cheekbones and brows,
deep shadow filling everything else, the smoke of the extinguished candle catching the light.
Title '{title}' in aged serif or gothic letterpress, upper frame or across the gap between figures.
Author '{author}' in smaller matching serif.
Portrait 2:3, ultra-detailed, no watermark.
```

#### Urban Romantasy / Contemporary Paranormal Revival
```
Romance novel cover, cinematic photorealistic quality, contemporary-with-wrong-detail atmosphere.
TWO characters. Contemporary interior or urban threshold — apartment hallway, coffee shop corner,
building lobby at night — with city skyline or rain-streaked window visible in background,
muted and dark, the ordinary world continuing behind them.
Male figure in contemporary clothing (dark coat, simple shirt, nothing elevated) but with ONE
inhuman detail found after the face: iris color slightly wrong — too pale, too gold, too flat;
OR canine teeth one millimeter too long; OR posture too still, the stillness of something that
stopped needing to perform restfulness centuries ago; OR a shadow that does not match his position.
His body language: ancient certainty — he is not anxious; he has survived everything and the
experience has made him very still.
Female figure in completely ordinary contemporary clothing (jeans, work clothes, Tuesday in a
modern city) beside him. Her expression: raw vulnerability — the precise moment of understanding
that something is not right about this person she thought she knew. She is not afraid yet.
She is recalibrating.
The subtext: she thought the city's worst problem was her rent. Then he admitted he had been
alive since 1347. She did not leave.
Color palette by subspecies: cool blue-grey and silver for vampire or immortal; warm amber and
rust for shifter; deep forest green and charcoal for fae-urban. City window provides one note
of familiar indifferent light — life continuing outside while something ancient stands in frame.
Lighting: ambient city glow from the window as cool fill, single interior lamp as warm key
on his inhuman detail and her face, deep shadow filling the rest.
Title '{title}' in semi-bold contemporary sans-serif with one typographic anomaly — a slightly
different weight on one letter, or a ligature that reads as marginally inhuman.
Author '{author}' in clean standard sans beneath.
Portrait 2:3, photorealistic, ultra-detailed, no watermark.
```

#### Gothic Bridal Thriller (Fake Death / Hidden Identity Romance)
```
Romance novel cover, cinematic photorealistic quality, gothic thriller atmosphere — the intersection of bridal innocence and death.
FRAMING: full-body shot, both primary figures from feet to crown, bride center-dominant.
TWO characters. Bride in elaborate floor-length lace wedding gown — backless with intricate floral embroidery, seed-pearl buttons down the spine, sheer veil trailing to the floor; body half-turned so the full ornate lace back is the primary visual, face turning back over her shoulder — the look of someone who knows exactly who is watching and has decided what to do about it.
Her expression: composed intelligence with something unreadable beneath — not grief, not fear, the specific expression of a woman who staged her own ending and is watching the consequences unfold from inside them.
Male figure beside or slightly behind her: tall, dark suit, law enforcement badge visible at belt or chest (detective or investigator), jaw set, expression of controlled disbelief — the man tasked with finding the dead woman, currently standing beside her. His eyes search her face for the lie that should be there. He has not found it yet.
Background: gothic cathedral interior, a funeral in progress — mourners in black with umbrellas dimly visible in the background, a coffin draped in white lilies placed at center aisle. Stained glass window casting fractured violet and crimson light across cold stone floor. Crimson and ivory roses scattered at ground level.
The subtext: everyone in this room believes she is in that casket. She is standing at her own funeral in her wedding dress, and she brought him with her.
Color palette: ivory lace, deep charcoal black, crimson rose petals, fractured violet and amber from stained glass, cold stone grey.
Lighting: stained glass window as primary color source — fractured violet and crimson light falling through the composition from above; cold candelabra light catching the lace embroidery; deep shadow filling the cathedral behind.
Title '{title}' in ornate gothic serif with fine flourish details, aged gold or deep ivory. Author '{author}' in smaller matching serif beneath.
Portrait 2:3, photorealistic, ultra-detailed, no watermark.
```

#### WLW / Sapphic Romance (F/F Intimate)
```
Romance novel cover, editorial photography aesthetic, intimate luxury boudoir atmosphere — two women, warm amber candlelight, no male figures present.
TWO female characters, diverse pairing strongly encouraged — different ethnicities and hair textures create visual richness and wider audience resonance. Both women in matching luxury satin sleepwear or robes in a deep jewel tone — amethyst, deep mauve, champagne, or deep rose — fabric catching the candlelight and shimmering liquidly against their skin. Both seated on a bed or chaise, bodies close, leaning naturally toward each other.
Their expressions: the specific softness of having stopped pretending — not performing for anyone, not holding anything back tonight. One figure's head tilted toward the other's shoulder or cheekbone, eyes half-closed. The other gazing at her with the expression of someone who knows exactly what this is and has decided not to question it.
One delicate detail per figure: a pendant resting against décolletage, an earring catching candlelight, a curl against a bare shoulder — small tactile details that communicate intimacy without explicit content.
Allure note: satin fabric is load-bearing here. Shirt open just enough, necklines naturally falling, the fabric draping to communicate warmth. T1 minimum; push to T2 if satin décolletage reads cleanly.
Background: luxury bedroom interior — warm amber from a bedside lamp and candles, soft white or ivory bedding, roses or peonies in soft focus in background. No harsh lines. Everything communicates warmth, safety, and chosen intimacy.
The subtext: this started as a secret. At some point it became the realest thing in the room.
Color palette: deep jewel-tone satin (amethyst, mauve, or champagne), warm amber candlelight, ivory bedding, warm skin tones in caramel and deep brown, gold jewelry accents.
Lighting: single warm bedside lamp as key light catching the satin fabric and their faces, candles as warm fill, soft diffuse wrap — no harsh shadows. The lighting communicates safety and warmth, not drama.
Title '{title}' in elegant feminine script or slim clean serif, warm rose gold or champagne. Author '{author}' in matching weight beneath.
Portrait 2:3, photorealistic, ultra-detailed, no watermark.
```

#### African Royalty Romance (Traditional Regalia / Royal Court)
```
Romance novel cover, regal portrait photography aesthetic, warm African royal atmosphere — traditional regalia, authentically African setting, no Western architectural elements.
COMPOSITION: seated-power portrait — primary female figure seated in a leopard-fur throne or carved wooden throne at frame center, male figure standing directly and closely behind her. Not dominating — flanking; his presence extending her power, not replacing it. Both figures from base of seat to crown fully in frame.
Female figure: African woman in traditional Southern or East African formal dress — ivory or white fabric with bold geometric border embroidery in primary colors (red, green, blue, gold), elaborate layered beaded collar necklace across chest and shoulders, matching beaded headpiece at crown. Her posture: upright, composed, the specific stillness of someone who has never needed to announce authority. Her expression: clear-eyed regal warmth — not cold, not deferential — the ease of someone who belongs exactly here.
Male figure: taller, bare muscular chest or draped in a leopard-skin or kente-cloth royal cloak, gold crown, gold chain necklace, traditional cuff or bracelet. His expression: protective certainty — eyes forward, his stance directly behind her communicates he stands here by choice and would stand nowhere else. One hand may rest at her shoulder — a claim, a partnership.
Secondary elements: carved wooden shield partially visible at frame edge, traditional patterned textiles or animal-hide seat covers, tribal or cultural artifacts in soft focus background.
Background: warm earthen-toned African interior — thatch, carved wood, animal hide, terracotta textures — or an open ceremonial space with warm golden ambient light. The setting must read as authentically African: no European architectural elements, no generic "throne room" clichés.
The subtext: her bloodline built this kingdom. He came to claim a throne and found she already wore it.
Color palette: rich warm earth tones — sienna, ochre, burnt orange, deep chocolate — with bold jewelry and embroidery accents in primary colors (red, green, gold beads). Warm diffuse golden light.
Lighting: warm ambient golden-hour or interior torch light — even, regal wrap across both figures. No harsh directional shadows. The lighting communicates warmth and permanence.
Title '{title}' in bold serif with gold ornamental dividers — geometric African motifs or crown symbol above and below. Author '{author}' in clean serif beneath.
Portrait 2:3, photorealistic, ultra-detailed, no watermark.
```

#### Domineering CEO / Rejected Spouse Revenge (Male Power Fantasy)
```
Romance novel cover or social ad creative, cinematic composite digital art, rain-soaked urban power atmosphere — the man they discarded returning as the city's apex predator.
FORMAT: portrait 2:3 for book cover; landscape 16:9 for social ad creative. For landscape: characters arranged horizontally, city skyline fills the full background width. For portrait: city towers compressed behind the stacked figures.
COMPOSITION — THREE figures for maximum narrative tension: central alpha male dominant, two women flanking (one left = the regret; one right = the rival claim). For solo focus: male figure alone against the cityscape, full body.
Central male figure: tall, dark business suit — jacket open or partially torn, white dress shirt rain-soaked and possibly stained (survival, not defeat), tie loosened, dark hair rain-wet, water dripping from jaw. Standing against the night cityscape with the body language of total command — chest open, feet planted, weight settled. His expression: cold absolute dominance with zero residual anger — the specific expression of a man who watched them underestimate him, made a plan, and waited. He has won. He knows it. He is not gloating.
His eyes look directly at the viewer or past them — the gaze of a man who owns the building the viewer is standing in.
Left female figure: evening wear or structured dress, body partially turned away — her expression is the grief of realizing what she threw away, expressed as stillness rather than tears.
Right female figure: closer to him, looking toward him with the intensity of someone who sees what she underestimated.
Background: rain-soaked night city — skyscrapers with fictional corporate signage, neon reflections in wet pavement, a luxury dark SUV at frame edge. Rain in visible streaks catching city neon. The city is not backdrop — it is his possession.
Color palette: black and gold — deep night, gold corporate signage, white-blue neon, rain-silver. High contrast. Secondary figures in deeper shadow.
Lighting: cool city neon rim light on his shoulders and rain-wet hair, key light from below catching his jaw and chest, rain streaks as secondary light, secondary figures darker.
Title in bold impact or condensed sans-serif, gold metallic with black outline, thumbnail-legible. Optional genre-tag icons at bottom: crown / ring / flame with short tagline phrases.
Portrait 2:3 or landscape 16:9, cinematic composite, photorealistic, ultra-detailed.
```

#### BL / MM Romance (Boys' Love / Male–Male Intimate)
```
Romance novel cover, cinematic photography or high-quality digital illustration, intimate charged atmosphere — two male leads, emotional tension, no female figures.
FRAMING: close-up or medium-close — both faces and upper torsos visible, bodies from chest to crown. The proximity is the composition; the charged space between them is the narrative engine.
TWO male characters, deliberately distinct in visual styling to create polarity:
Dominant figure: slightly taller or higher in frame, darker clothing (black or deep charcoal shirt or jacket), jaw set, body angled toward his partner with controlled deliberateness — the posture of a man who has made a decision. His expression: focused want that has not yet tipped into action — controlled, certain, unhurried.
Receiving figure: lighter or open-collar shirt, one or two buttons undone, body tilted toward the dominant figure but chin lifted slightly up and back — the posture of someone who knows what is about to happen and is not moving away. His expression: surrender that does not read as weakness — eyes half-closed, lips slightly parted.
The space between their faces is the critical element: foreheads almost touching, or lips separated by centimeters. No explicit content — the almost-contact carries the full charge.
Ethnicities: Asian, mixed, or ethnically ambiguous characters have strong audience resonance in this genre. Consistency within a series matters more than any specific ethnicity.
Background: city at night — Las Vegas neon, Tokyo blur, or dense urban night with warm bokeh — in soft focus through a window or directly behind. Bokeh circles of warm light, completely unfocused, communicating that the world outside has ceased to matter.
The subtext: they had one night and agreed it meant nothing. One of them lied.
Color palette: dark navy or charcoal base, warm amber or gold rim light from city glow, skin tones as the brightest elements. City creates warm halo behind without competing with faces.
Lighting: warm ambient city glow as soft rim light on hair and jaw, single warm key from one side catching the dominant figure's jaw and his partner's cheekbone, deep shadow in background. Intimate, close, warm.
Title '{title}' in clean modern serif — neither script-feminine nor impact-masculine — warm gold, rose gold, or clean white. Author '{author}' beneath.
Portrait 2:3, photorealistic or high-quality render, ultra-detailed, no watermark.
```
