# Story & Copy Deslop

Load this reference when removing AI flavor from prose — fiction chapters, traffic articles, taglines, synopses, or site copy.

Run deslop periodically on full books:
- After finishing all chapters of a new book, following the write and review passes.
- During bulk maintenance of existing books.

For every new long-form book, deslop is a publication gate rather than an optional cleanup step. Run it across the full manuscript before the final First-Three-Chapter Conversion Gate, record coverage in `tracking/quality-gates.md`, and rerun it on any opening chapter changed by the conversion audit. Do not advance to traffic articles, build, commit, or publication until both A3 and A3.5 are recorded as PASS.

## Content Type Router

| Content | Gates to run | Notes |
|---------|-------------|-------|
| Fiction chapters | All 7 Gates + Three-Pass Method | Full pipeline |
| Traffic articles | A, B, C (passive + vague), G, H + Article Quick Checks | No E/F (no dialogue/endings) |
| Taglines / synopses | A (adverbs + jargon), B (binary contrasts + throat-clearing), G (false agency), H (stakes inflation + concept labels) | Minimal pass, surgical |
| Meta descriptions | B (throat-clearing), G (false agency), Article Quick Checks | <155 chars, one active sentence |

---

## Core Philosophy

AI flavor is not a grammar error — it is a style problem: over-polished, symmetrical, over-explained. The goal is to pull text from over-crafted back toward specific, natural, readable. Change the minimum amount to shift the character of the passage.

**Never delete entire paragraphs.** Plot function, foreshadow, character reveals, and tension hooks must survive. If a passage is bad, rewrite it — don't erase it.

For copy (articles, taglines): same principle — minimum effective change. Don't rewrite voice, rewrite violations.

---

## Detection: The 7 Gates + Gate H

Run the applicable gates based on content type (see router above) and severity (see Severity Levels below).

| Gate | Problem | Signal |
|------|---------|--------|
| A | Banned words / high-frequency clichés / adverbs / jargon | Fiction: "something flickered in his eyes" "he drew a deep breath"; Copy: adverbs (-ly), filler phrases ("At its core"), business jargon, AI vocabulary tells |
| B | Template sentence patterns | negation-then-reversal, binary contrasts, consecutive parallel ≥3, throat-clearing openers, dramatic fragmentation, meta-commentary, self-posed Q&A, anaphora, superficial analyses |
| C | Telling not showing / passive voice / vague declaratives | "he felt" / "X was created" / "The implications are significant" |
| D | Uniform rhythm / paragraph length / formatting | Every paragraph 4–6 sentences, identical beat; bold-first bullets; em dashes; listicle-as-prose |
| E | Flat dialogue tags *(fiction only)* | "said/asked/smiled" on nearly every line |
| F | Moral summary endings *(fiction only)* | Last paragraph summarizes or moralizes what just happened |
| G | Narrator intrusion / false agency / narrator-from-a-distance / vague attributions | "What she didn't know was..." / "the decision emerges" / "Nobody designed this." / "Experts argue..." |
| H | Composition & tone tropes *(articles + copy)* | False vulnerability, grandiose stakes, invented concept labels, fractal summaries, dead metaphor, one-point dilution |

---

## Severity Levels

*(Fiction chapters — for copy, run gates directly without severity scoring)*

| Level | Quantity signal | Gates to run |
|-------|-----------------|-------------|
| Mild | ≤5 banned words/1,000 chars, no consecutive 3+ templates | A + B |
| Moderate | 6–15 banned words/1,000 chars, or 3+ consecutive templates | A + B + C + D + G |
| Severe | >15 banned words/1,000 chars, or 4+ of the 7 Gates flagged | All 7 Gates + targeted rewrites |

Deletion cap by severity: Mild ≤15%, Moderate ≤25%, Severe ≤35% of the passage. Mark anything borderline `[NEEDS REVIEW]` rather than deleting.

---

## Structural Anchors — Never Touch

These elements must survive every deslop pass unchanged:

| Element | Why |
|---------|-----|
| Frontmatter fields (`title`, `chapter`, `bookId`, `language`, `status`) | Build system and URL routing depend on these |
| Chapter H1 heading (the first `# ` line after frontmatter) | Reader UI renders this as chapter title |
| `<!-- ILLUSTRATION -->` markers | Illustration injection point — moving breaks layout |
| Internal links (`href="/book/..."`) | Any path change breaks navigation |
| File names (`ch-NNN-slug.md`) | Static params generated from filenames |

**Rule**: deslop operates only on prose body lines. It never modifies frontmatter, headings, markers, links, or filenames — even if those contain AI-flavored phrasing.

---

## Gate A — Banned Words / Adverbs / Jargon

### Fiction clichés

| AI-flavored phrase | Natural alternative |
|--------------------|---------------------|
| he drew a deep breath | his chest rose / delete |
| something flickered in his eyes | he looked away / narrowed his eyes |
| the corner of his mouth curved | he smiled — it didn't reach his eyes / he laughed |
| as if / as though / as though woven from | plain comparison or literal description |
| couldn't help but | direct action verb |
| slowly opened his mouth | just use dialogue / action-then-dialogue |
| something in his/her chest | name the specific physical sensation or delete |
| exhale/inhale like [simile] | delete the action tag entirely, go to dialogue or next beat |

### Adverbs — kill on sight

No -ly words. No softeners, no intensifiers, no hedges.

Offenders: really, just, literally, genuinely, honestly, simply, actually, deeply, truly, fundamentally, inherently, inevitably, interestingly, importantly, crucially, quietly, certainly, arguably, remarkably, notably, surprisingly.

**"Quietly" as magic adverb:** AI reaches for "quietly" to convey subtle importance — "quietly orchestrating workflows", "a quiet intelligence behind it." It's not actually subtle; it's decorative. Delete.

### AI vocabulary tells

Words overrepresented in AI-generated text. Flag on sight.

| Word | Why | Replace with |
|------|-----|--------------|
| delve | no human writes "let's delve" | examine, look at, explore |
| tapestry | lazy metaphor for anything complex | mix, combination, range |
| nuanced | used instead of being nuanced | complex, specific |
| certainly | hedging that sounds confident | rewrite with evidence, or cut |
| curated | overused for "selected" | selected, chosen, collected |
| foster | bureaucratic verb | build, create, encourage |
| ecosystem | grandiose replacement for "community" or "system" | system, field, community |
| paradigm | sounds academic, means nothing specific | model, approach |
| synergy | never use | cooperation, combined effect |
| framework | overused | structure, approach |

**False ranges:** "From X to Y" constructions where X and Y aren't on a real spectrum — "from startups to enterprises," "from innovation to cultural transformation." They list examples, not a range. State the examples directly.

### The "serves as" dodge

AI replaces "is" with pompous alternatives. Use the simple verb.

| Avoid | Use instead |
|-------|-------------|
| serves as | is |
| stands as | is |
| marks (when meaning "is") | is |
| represents (when meaning "is") | is |

### Business jargon → plain language

| Avoid | Use instead |
|-------|-------------|
| Navigate (challenges) | Handle, address |
| Unpack (analysis) | Explain, examine |
| Lean into | Accept, embrace |
| Landscape (context) | Situation, field |
| Game-changer | Replace with the specific impact |
| Deep dive | Analysis, examination |
| Moving forward | Next, from now |
| Circle back | Return to, revisit |
| Understands the assignment | Replace with the actual premise |
| Leverage (verb) | Use |
| Utilize | Use |
| Robust | Strong, solid |
| Streamline | Simplify |
| Harness | Use, apply |
| Double down | Commit, increase |
| Take a step back | Reconsider |
| On the same page | Aligned, agreed |
| Unpack | Explain |
| Holistic | Complete, full |
| Cutting-edge | New, recent |
| Groundbreaking | New, first |
| Transformative | Significant (if it's actually significant) |

### Paired adjectives with "yet" / "and"

"Simple yet powerful", "elegant and robust", "lightweight but comprehensive." Pick the stronger adjective. Drop the pairing.

### Scare quotes

Quotation marks used for irony or emphasis around ordinary words — not actual quotations. "The tool 'seamlessly' integrates..." Choose a better word and drop the quotes.

### Internet clichés

Phrases that were once online-native, now overused by AI as if they're still fresh.

| Cut | Replace with |
|-----|-------------|
| "you can't unsee it" | say what you now see |
| "hits different" | say how it differs |
| "rent-free" | say it occupies your attention |
| "chef's kiss" | say what makes it right |
| "the quiet part out loud" | say what was implied |
| "let that sink in" | delete |
| "say it louder for the people in the back" | delete |
| "I'm here for it" | delete or commit to a specific opinion |

---

## Gate B — Template Sentence Patterns

Gate B structural patterns appear in ~2/3 of AI-generated chapters and are more endemic than Gate A word-level clichés. Scan for these first.

### 1. Negation-reversal / Binary contrasts (most common — ~65% of chapters)

The writer states what something is NOT before stating what it IS. State Y directly. Drop the negation entirely.

```
Flagged:  "Not defensive. Flat."
Flagged:  "No X. No Y. Just Z."
Flagged:  "Not because X. Because Y."
Flagged:  "[X] isn't the problem. [Y] is."
Flagged:  "The answer isn't X. It's Y."
Flagged:  "not X, it's Y" / "isn't X, it's Y"
Flagged:  "not just X but also Y"
Flagged:  "It feels like X. It's actually Y."
Flagged:  "The question isn't X. It's Y."
Flagged:  "It's not this. It's that."
Flagged:  "stops being X and starts being Y"
Flagged:  "doesn't mean X, but actually Y"
Flagged:  "less about X, more about Y"
Rewrite:  Collapse into one direct statement.
Example:  "Not defensive. Flat." → "Flat."
Example:  "No grief, no shock. Just calculation." → "Pure calculation."
Example:  "The tension isn't whether they'll fall. It's whether she'll understand." → "The question is whether she'll understand."
```

### 2. Consecutive same-structure sentences (≥3 in a row)

Any subject-verb pattern repeated three or more consecutive times, regardless of vocabulary variation.

```
Flagged:  She'd done this. She'd seen that. She'd known better.
Flagged:  He left. He came back. He said nothing.
Flagged:  Then she stood. Then she turned. Then she opened the door.
Fix:      Vary the third sentence's structure — subordinate clause, question, or restructure.
```

### 3. Passive reflection blocks ("had always") *(fiction)*

```
Flagged:  "She had always found silence uncomfortable."
Fix:      Cut "had always" and put the character into an active moment that shows the same trait.
Example:  → "The silence went on long enough that she started counting floor tiles."
```

### 4. Throat-clearing openers *(copy)*

Remove these; state the content directly.

```
Flagged:  "Here's the thing:" / "Here's what [X]" / "Here's why [X]"
Flagged:  "The uncomfortable truth is" / "The real [X] is"
Flagged:  "It turns out" / "Let me be clear" / "The truth is,"
Flagged:  "I'm going to be honest" / "Can we talk about"
Flagged:  "If you've been looking for X" / "If you came here for X but"
Flagged:  "Here's the kicker" / "Here's where it gets interesting"
Flagged:  "Here's what most people miss" / "Here's the deal"
Flagged:  "I'll say it again:" / "Here's what I find interesting"
Flagged:  "The truth is simple" / "History is unambiguous on this point"
Flagged:  "We're excited to announce..." / "I'm thrilled to share..."
Flagged:  "Look:" / "So here's what happened:"
Fix:      State the point. Cut everything before it.
```

### 4a. Pedagogical hand-holding *(copy)*

AI defaults to teacher mode and assumes the reader needs hand-holding. Cut these.

```
Flagged:  "Let's break this down" / "Let's unpack this" / "Let's explore"
Flagged:  "Let's dive in" / "Let's delve into"
Flagged:  "Think of it as..." / "Think of it like..."
Flagged:  "Imagine a world where..."
Flagged:  "Whether you're X or Y..." (false inclusivity; pick the actual audience)
Fix:      Delete. Start with the substance.
```

### 5. Dramatic fragmentation

Sentence fragments for emphasis read as manufactured profundity.

```
Flagged:  "[Noun]. That's it. That's the [thing]."
Flagged:  "The mark. The debt. The clause." (three separate fragments)
Flagged:  "This unlocks something. [Word]."
Flagged:  "X. And Y. And Z." (staccato drama)
Flagged:  "He published this. Openly. In a book." (fragment stacking)
Flagged:  "Platforms do." (orphaned fragment as punchline)
Fix:      Complete sentences, or combine: "The mark, the debt, the clause."
```

### 6. Meta-commentary *(copy)*

Remove self-referential asides. Let the piece move.

```
Flagged:  "The rest of this essay explains..."
Flagged:  "Let me walk you through..." / "In this section, we'll..."
Flagged:  "But that's another post"
Flagged:  "As we discussed above..." / "As mentioned earlier..."
Fix:      Delete. Start the next point.
```

### 7. Rhetorical setups

```
Flagged:  "What if [reframe]?" answered immediately
Flagged:  "Think about it:" / "Here's what I mean:"
Fix:      Make the point. Let readers draw conclusions.
```

### 8. Self-posed rhetorical Q&A *(copy — highest priority after type 1)*

The model asks a question nobody was asking, then answers it immediately for dramatic effect.

```
Flagged:  "The result? Devastating."
Flagged:  "The worst part? Nobody saw it coming."
Flagged:  "The scary part? This attack vector is perfect."
Flagged:  "And that's okay." (unnecessary permission-granting)
Fix:      Merge into a direct statement. "The result was devastating."
```

### 9. Anaphora abuse *(copy)*

Repeating the same sentence opening multiple times in quick succession.

```
Flagged:  "They assume that users will pay... They assume that developers will build... They assume that..."
Flagged:  "They could expose... They could offer... They could provide... They could create..."
Fix:      Vary openings. Combine related points into single sentences.
```

### 10. Superficial participle analysis

Tacking a present participle phrase onto a sentence to inject shallow significance. The -ing phrase adds the appearance of analysis without the content.

```
Flagged:  "contributing to the region's rich cultural heritage"
Flagged:  "highlighting its enduring importance"
Flagged:  "reflecting broader trends in the industry"
Flagged:  "underscoring its role as a dynamic hub"
Fix:      Cut the phrase entirely, or rewrite as a specific claim.
```

### 11. Repetitive "you" sentence starters *(copy)*

```
Flagged:  3+ consecutive sentences beginning with "You"
Fix:      Vary sentence structure — lead with the action, result, or situation.
```

---

## Gate C — Telling / Passive Voice / Vague Declaratives

### Telling not showing *(fiction)*

```
Flagged:  "he felt" / "she realized" / "emotion surged inside her"
Fix:      Ground in body action. "His hands shook." not "He was terrified."
```

### Passive voice *(all content)*

Every sentence needs a subject doing something. Passive voice hides the actor.

```
Flagged:  "X was created" → Name who created it.
Flagged:  "It is believed that" → Name who believes it.
Flagged:  "The decision was reached" → Name who decided.
Flagged:  "Mistakes were made" → Name who made them.
```

### Vague declaratives *(copy)*

Sentences that announce importance without naming the specific thing.

```
Flagged:  "The reasons are structural"
Flagged:  "The implications are significant"
Flagged:  "The stakes are high"
Fix:      Name the specific thing. If you can't, cut the sentence.
```

---

## Gate D — Uniform Rhythm / Paragraph Length / Formatting *(fiction + articles)*

| Natural | AI-flavored |
|---------|-------------|
| 1–3 sentences; occasional 1-sentence standalone | 4–6 sentences, uniform |
| Mix of short and long | Metronomic |
| Two-item lists | Three-item lists as default |
| Paragraphs ending differently | Every paragraph ends punchily |
| No em dashes | Em dashes everywhere |

**Em dash rule:** Remove all em dashes. Use a comma, period, or restructure the sentence.

**Three-item list rule:** Two items beat three. One item beats two when the point is singular.

**Sentence length uniformity check:** Four or more consecutive sentences all within 30% of their mean word count is an AI pattern. Real writing varies. Mix short and long; a 3-word sentence after a complex one creates rhythm.

**Bold-first bullets:** Every bullet starting with a bolded phrase is an AI formatting tell — almost no human writes lists this way by hand. In prose: write the key point into the sentence. In actual lists: keep the bolded keyword only if it's genuinely a label, not decoration.

**Unicode decoration:** → arrows, → bullets, decorative symbols (→, ◆, ★) in body prose. Use plain punctuation. "Input → Processing → Output" should be "input, processing, then output" or just a plain list.

**Listicle in trench coat:** Numbered paragraphs dressed as prose — "The first wall is... The second wall is... The third wall is..." That's a list. Either write genuine prose (combine points, develop them) or make it an explicit list. Don't disguise one as the other.

**Exclamation mark clusters:** More than one exclamation mark per paragraph, or more than three in the full document. Cut all but the one that matters most.

---

## Gate E — Flat Dialogue Tags *(fiction only)*

| Natural web fiction | AI-flavored text |
|--------------------|-----------------|
| 60%+ tagless, action-attributed | Nearly every line tagged |
| Varied beats | "said/asked/smiled" on every line |

---

## Gate F — Moral Summary Endings *(fiction only)*

Last paragraph summarizes or moralizes what just happened. Cut it. End on action or dialogue.

---

## Gate G — Narrator Intrusion / False Agency / Narrator-from-a-Distance / Vague Attributions

### Narrator intrusion *(fiction)*

```
Flagged:  "What she didn't know was..."
Flagged:  "The reason he ... was because..."
Flagged:  Evaluative aside that steps outside character POV
Fix:      Stay in POV. Show the character's perception only.
```

### False agency *(all content)*

Inanimate things doing human verbs. Name the actual human actor.

```
Flagged:  "the decision emerges" → Someone decided.
Flagged:  "the culture shifts" → People changed behavior.
Flagged:  "the data tells us" → Readers who finished chapter 1 are more likely to...
Flagged:  "the debt stopped being the point" → She stopped caring about the debt.
Flagged:  "the market rewards" → Buyers pay for...
Flagged:  "a complaint becomes a fix" → The team fixed it.
Fix:      Name the human. If no specific person fits, use "you."
```

### Narrator-from-a-distance *(all content)*

Put the reader in the room, not above it.

```
Flagged:  "Nobody designed this." → "You don't sit down one day and decide to..."
Flagged:  "There's a specific kind of story that..." → Name the story directly.
Flagged:  "There is a specific pleasure in..." → State what happens in the story.
Flagged:  "People tend to..." → "You tend to..."
Flagged:  "This happens because..." → Name who did it and when.
```

### Vague attributions *(copy)*

Claiming authority without naming the source.

```
Flagged:  "Experts argue that..."
Flagged:  "Industry reports suggest..."
Flagged:  "Observers have cited..."
Flagged:  "Studies show..." (with no study named)
Fix:      Name the expert, study, or person. If you can't, cut the claim.
```

### Sentence starters to avoid *(copy)*

```
Flagged:  Sentences starting with What, When, Where, Which, Who, Why, How
Fix:      Lead with the subject or verb.
Example:  "What makes this hard is..." → "The constraint is [specific thing]."
```

---

## Gate H — Composition & Tone Tropes *(articles + copy)*

These operate at the level of the full piece, not individual sentences. Run Gate H after Gates A–G when reviewing articles, essays, or copy.

### False vulnerability

Performative self-awareness inserted to disarm skepticism — "I know this seems obvious, but..." / "I'll be the first to admit..." / "And yes, since we're being honest..." AI uses this to sound human. It reads as manipulation because real vulnerability is specific and uncomfortable; AI vulnerability is polished and risk-free.

Fix: Remove. State the point.

### Grandiose stakes inflation

Treating a narrow topic as civilization-defining. "This will fundamentally reshape how we think about everything." / "We're at a crossroads." / "will define the next era of computing."

Fix: Scope the claim to what the evidence supports.

### Invented concept labels

Naming a phenomenon with a compound neologism used as if it's an established term: "the supervision paradox," "the acceleration trap," "workload creep." The label is invented on the spot to sound incisive. Multiple such labels in the same piece is a strong AI signal.

Fix: Describe the phenomenon in plain language. If the label is genuinely useful, define it explicitly.

### Fractal summaries

"What I'm going to tell you; what I'm telling you; what I just told you" — applied at every level. Every subsection gets a summary. Every section gets a summary. The piece itself gets a summary. All structure, no content.

Fix: One summary per piece, at the end. Open sections with a point, not a preview of the point.

### Dead metaphor

A single metaphor introduced early and then beaten through every subsequent paragraph. "The model is a toolbox" → tools, hammer, wrench, workshop, craftsmanship, blueprint — for 1,500 words.

Fix: Use the metaphor once or twice. Then switch to literal language.

### Historical analogy stacking

Rapid-fire historical examples or company names stacked to build false authority without developing any of them. "Apple didn't build Uber. Facebook didn't build Spotify. Stripe didn't build Shopify..." / "Like the printing press. Like the internet. Like the industrial revolution."

Fix: Develop one analogy fully. Cut the others.

### One-point dilution

A single argument restated in different words across thousands of words. Each section rephrases the thesis with a different metaphor but adds nothing new. An 800-word argument padded to 4,000 words.

Fix: Find the one sharpest formulation. Cut everything that rephrases it rather than advancing it.

### "Despite its challenges..." formula

Acknowledging downsides with a dismissive clause before pivoting to enthusiasm: "Despite its challenges, X represents..." / "While there are concerns, Y offers..." AI uses this as a balance-seeking reflex that dismisses every objection without engaging it.

Fix: Either engage the challenges seriously or drop the acknowledgment.

### Signposted conclusion

"In conclusion..." / "To sum up..." / "In summary..." as a conclusion opener. Competent writing doesn't announce itself. The reader can feel when it's ending.

Fix: Cut the signpost. Start with the actual final point.

### Triple-value lists

Three abstract virtues listed in "X, Y, and Z" form with no specifics: "excellence, collaboration, and innovation." Sounds principled, says nothing.

Fix: Pick the one that matters and say something specific about it.

### Uncontracted forms as stiffness signal *(copy)*

Consistent use of "it is", "do not", "is not", "we are", "they have" with zero contractions anywhere. Real writing uses contractions.

Flag if: 2+ uncontracted forms exist and no contractions appear anywhere in the text.

Fix: "It is" → "it's", "do not" → "don't", "we are" → "we're".

---

## Natural Writing Benchmarks *(fiction chapters)*

| Dimension | Natural web fiction | AI-flavored text |
|-----------|--------------------|--------------------|
| Paragraph length | 1–3 sentences; occasional 1-sentence standalone | 4–6 sentences, uniform |
| Dialogue tags | 60%+ tagless, action-attributed | Nearly every line tagged |
| Emotion | Body action ("his hands shook") | Direct statement ("he was terrified") |
| Simile | Everyday ("like a dog guarding its bowl") | Literary ("like crystalline ice") |
| Filler words | Colloquial ("God", "damn", "ugh") | Almost none |
| Detail | Specific, concrete | Vague and thorough |
| Parallel structure | At most 1–2, never 3+ consecutive | 3–5 in a row is standard |
| Endings | Action or dialogue | Summary or uplift |

---

## High-Frequency Patterns *(Gate B priority — validated across 33 ch-001 files)*

Gate B structural patterns appear in ~2/3 of AI-generated chapters and are more endemic than Gate A word-level clichés. Scan for these first.

See Gate B section above for full pattern list. Negation-reversal is present in ~65% of chapters and is the highest-priority scan target.

---

## Quick Replacement Reference *(fiction)*

| AI-flavored phrase | Natural alternative |
|--------------------|---------------------|
| Not X. Y. / Not X. Just Y. | collapse into one direct statement |
| No X. No Y. Just Z. | collapse into one direct statement |
| had always [verb]ed | cut to an active scene beat that shows the trait |
| he drew a deep breath | his chest rose / delete |
| something flickered in his eyes | he looked away / narrowed his eyes |
| the corner of his mouth curved | he smiled — it didn't reach his eyes / he laughed |
| as if / as though | plain comparison or literal description |
| couldn't help but | direct action verb |
| something in his/her chest | name the specific physical sensation or delete |
| exhale/inhale like [simile] | delete the action tag, go to dialogue or next beat |

---

## Article Quick Checks *(run before delivering any article, tagline, or copy block)*

- Any adverbs? Kill them.
- Any passive voice? Find the actor, make them the subject.
- Inanimate thing doing a human verb? Name the person.
- Sentence starts with a Wh- word? Restructure it.
- Any "here's what/this/that" throat-clearing? Cut to the point.
- Any "not X, it's Y" contrasts? State Y directly.
- Self-posed question ("The result? Devastating.")? Merge into a statement.
- Three consecutive sentences match length? Break one.
- Paragraph ends with punchy one-liner? Vary it.
- Em dash anywhere? Remove it.
- Vague declarative ("The implications are significant")? Name the specific thing.
- Meta-joiners ("The rest of this article...")? Delete.
- Pull-quote energy ("X. That's it. That's the thing.")? Rewrite as a complete sentence.
- "Serves as" or "stands as"? Replace with "is."
- Any pedagogical hand-holding ("Let's break this down", "Think of it as...")? Delete.
- Bold-first bullets? Restructure as sentences or unlabeled list items.
- Any invented concept label (neologism not defined in context)? Replace with plain description.
- Any vague attribution ("Experts argue...")? Name the source or cut.
- Any "Despite its challenges..." or "In conclusion..."? Rewrite.
- Single metaphor used more than 3 times? Vary or cut.

---

## Scoring *(copy — rate 1–10 on each)*

| Dimension | Question |
|-----------|----------|
| Directness | Statements or announcements? |
| Rhythm | Varied or metronomic? |
| Trust | Respects reader intelligence? |
| Authenticity | Sounds human? |
| Density | Anything cuttable? |
| Originality | Any dead metaphor, analogy stacking, or invented labels? |

Below 42/60: revise.

---

## Copy Application Notes

### Traffic articles (`articles/`)

- Lead with the conflict or hook — no setup paragraphs explaining what the article covers.
- Every paragraph earns its place. If cutting it doesn't break the argument, cut it.
- Short paragraphs win on mobile. 1–3 sentences, then break.
- The reader came from a Facebook ad about a book — reward that expectation fast.

### Book taglines

- No adverbs, no em dashes, no binary contrasts.
- 8–12 words max. Every word must do work.
- End on unresolved tension — never on a summary or conclusion.

### Book synopses (description field in `books.ts`)

- Lead with the conflict, not the setup.
- Introduce the protagonist and the obstacle in sentence 1–2.
- No throat-clearing ("In a world where..." / "Meet [Name], a woman who...").
- 3–5 sentences total. End on what's at stake, not a summary.

### Meta descriptions

- ≤155 characters.
- State what the book/article is about in one active sentence.
- Include the genre signal or emotional hook.
- No "Click here to read" / "Find out what happens."

---

## Triage Pass *(fiction chapters — run before any rewriting)*

Before touching a single chapter, do a fast read-only scan of all chapters and output a severity table:

```
| Chapter | Banned words/1k | Consecutive templates | Gates triggered | Severity |
|---------|-----------------|----------------------|-----------------|---------|
| ch-001  | 4               | 1                    | A               | mild    |
| ch-002  | 11              | 3                    | A B C           | moderate|
...
```

Rules:
- Scan by reading each chapter once — do not rewrite anything yet.
- Assign severity (mild / moderate / severe) per the Detection table above.
- Chapters with **zero** banned words and no Gate triggers: mark `clean` — **skip entirely**, do not process.
- Group results: clean (skip) → mild (Pass 1 only) → moderate (Pass 1+2) → severe (all 3 passes).

This triage pass typically saves 30–50% of total tokens on a full book by skipping clean chapters and limiting mild chapters to one pass.

---

## Three-Pass Method *(fiction chapters)*

Execution order:
1. Run the triage pass first and output the severity table.
2. Process chapters by severity group: clean chapters are skipped, mild get Pass 1, moderate get Pass 1+2, severe get all three passes plus targeted rewrites.
3. Output a De-Slop Report after each processed chapter.

- **Pass 1 — Deabstract**: Gates A, C (abstract emotion), D (uniform rhythm), G (narrator intrusion)
- **Pass 2 — Deliteralize**: Gates A (literary register), B (sentence templates)
- **Pass 3 — Restore natural voice**: Gates D (short/long rhythm mix), E (dialogue differentiation), F (ending de-moralization), add sensory detail

| Severity | Passes |
|----------|--------|
| Clean | skip |
| Mild | Pass 1 |
| Moderate | Pass 1 + Pass 2 |
| Severe | All 3 + targeted rewrites |

---

## Whitelist

If the project root contains `.deslop-whitelist`, skip flagging any phrase that appears there. Format: one entry per line, `#` for comments. Use for world-building terms, character nicknames, or intentional stylistic choices that happen to match banned patterns.

---

## Deslop Report Format

```
## De-Slop Report

Content type: {fiction chapter / article / tagline / synopsis}
AI flavor level: {mild / moderate / severe}  [fiction only]
Gates applied: {A B C ...}
Deletion rate: {X%}

### Change Log
| Location | Gate | Original | Revised | Note |
|----------|------|----------|---------|------|

### [NEEDS REVIEW]
{Any passages marked for human review rather than auto-rewrite}
```
