# Story Long Write

Load this reference when the user asks to write, continue, or revise long-form novel chapters.

**Before writing:** load the relevant broad genre file alongside this reference — `genre-romance.md`, `genre-mystery.md`, `genre-horror.md`, `genre-fantasy.md`, `genre-scifi.md`, or `genre-drama.md`. If the premise uses a pressure genre listed in `SKILL.md` (family captivity, workplace persecution, medical conspiracy, digital blackmail, and related systems), load that dedicated guide too. The broad file controls emotional and scene technique; the pressure-genre guide controls the power system, evidence chain, escalation, public reversal, and safety boundary.

## Niche Research Input

Before writing the first chapter of a new book, check `outputs/{site-slug}/{book-slug}/niche-research.json`:

- **Exists** → read `differentiation_angle`, `selected_tropes`, `competitive_brief[].beat_action`, and `producibility` (target chapters, words per chapter, intensity_level). These constrain the story brief.
- **Does not exist + user gave explicit genre/tropes/premise** → proceed directly; document them in `tracking/context.md`.
- **Does not exist + no explicit brief** → run `fiction-niche-researcher.md` first, then return here.

Continuing an existing book (adding chapters): skip this gate.

## Writing Language Routing (mandatory before outline expansion)

Select the prose profile from the **chapter language**, not the operator's language or the site's default UI language:

- English chapter (`language: en`, `en-GB`, or another English locale) → load `writing-english-fiction.md`.
- Chinese chapter (`language: zh-CN`, `zh-TW`, or another Chinese locale) → load `writing-chinese-fiction.md`; for `zh-TW`, also load `internationalization.md`.
- Any other language → use a dedicated language guide when available, or obtain an explicit brief. Never use the English profile as an unmarked substitute.

Record the chosen profile, locale, and reader market in `tracking/context.md`. Build the outline in that profile from the start. Translating an English draft into Chinese, or a Chinese draft into English, does not satisfy A1: it must be rewritten for the target profile and pass that profile's review checks.

## Chapter Length Gate

For English serial fiction, target **1,200–1,800 words per chapter**. Treat **1,800 words as the normal upper limit**. Any chapter above 1,800 words requires an explicit pacing review; any chapter above **3,200 words must be split or compressed before publication**. Split at a real scene turn, decision, consequence, or hook-out, not at an arbitrary sentence. Preserve causal actions, evidence, relationship changes, reversals, and the hook-out when compressing. Short epilogues, interludes, and narrow transition chapters may fall below the target range only when their narrative function is complete.

## Core Principles

1. **Emotion-first**: Every chapter has one primary emotional goal. Name it before writing a word.
2. **Validated patterns**: If a reference book exists in `reference/`, extract its technique before inventing new structure.
3. **Modular assembly**: Each chapter = hook + escalation + turn + hook-out. Each beat has a proven formula.
4. **Load only what's needed**: Before writing, read only the files relevant to this chapter's conflict and characters. Never load the full book.
5. **Ensemble causality**: Supporting characters must pursue independent goals and change the plot through action. A name in worldbuilding or a confidant who only listens does not count as an active character.
6. **Multi-thread escalation**: Every book runs at least three interacting storylines. Romantic tension alone cannot carry the middle of the book.

## Scene-Level Drama — The Click Standard

Every scene must pass the same test as the cover image: **tension + question + desire, all three present**. Every scene must deliver at least two of the three simultaneously. Which two (or three) depends on the genre — see the relevant genre file for the genre-specific Click Standard.

### The One-Paragraph Test

Read the opening paragraph of every scene. Ask: *does the reader feel something in the first three sentences?* If the answer is only "I understand where we are" — the scene starts too early. Cut to the moment tension is already present.

---

### Named Emotion Requirement

**Banned:** generic emotional states — "she felt nervous", "he was angry", "she was confused", "he seemed interested". These communicate the emotion's name, not the experience of it.

**Required:** emotions with internal contradiction — the character feels one thing and does or says or wants something else. Name the specific state before writing the scene.

**Genre-specific named states are in the relevant genre file.** Load `genre-romance.md`, `genre-mystery.md`, `genre-horror.md`, `genre-fantasy.md`, or `genre-scifi.md` for the complete table for your genre.

Universal examples (apply to any genre):

| Named state | Internal contradiction | How it reads on the page |
|-------------|----------------------|--------------------------|
| **Shock recognition** | She understands something that changes the frame; the understanding is complete before she can speak | Goes still; what she was about to do or say dies before it happens; one physical detail only |
| **Performed calm** | She is not calm; she is performing calm for a specific person in the room | Voice measured; choices deliberate; the reader sees the effort the other character doesn't |
| **Deferred grief** | Something has been lost; she knows; she cannot stop moving long enough to feel it | Acts with unusual efficiency; the grief leaks through one small wrong detail in her behavior |

Use the named state as the scene's emotional throughline. Every action, beat of dialogue, and internal observation should be filtered through it.

---

### Environmental Drama — Setting Amplifies Emotion

The setting is not backdrop. It is a second character that pushes the primary emotion forward. Before writing any scene, ask: *does this location make the stakes harder or easier?*

**Genre-specific environment types are in the relevant genre file.** Load the genre file for environments mapped to your genre's emotional beats.

Universal principle: if the setting could be swapped with any other location without changing the scene — change the setting.

| Emotional beat | Universal environment choice | What it adds |
|---------------|------------------------------|--------------|
| Forced proximity | Enclosed space with no easy exit (elevator, car, small room) | No escape; whatever is between them must be dealt with here |
| Power imbalance | The antagonist's space, not the protagonist's | She is on his territory; the power imbalance is architectural |
| Aftermath | Her familiar space, now contaminated by what happened | The ordinary world is no longer neutral |

---

### Contrast — The Scene's Composition

High-contrast moments are read more slowly and remembered longer. Build at least two of these into any pivotal scene:

- **Control vs. chaos** — one character's composure against the other's fracture
- **Public face / private reality** — what they show the room vs. what the reader knows
- **What is said / what is meant** — dialogue that runs parallel to the subtext, not identical to it
- **The ordinary detail / the extraordinary stakes** — mundane action (pouring a drink, adjusting a cuff) against the weight of what is actually happening
- **Speed: slow body / fast mind** — physical movement slows to micro-beats while internal monologue accelerates

---

**Genre-specific scene techniques** are in the relevant genre file. Load `genre-romance.md` for regression/villainess/creature-fixation techniques; `genre-mystery.md` for clue architecture, investigation pacing, gothic atmosphere, and Regency social constraint; `genre-horror.md` for reveal architecture, monster problem, and terror pacing; `genre-fantasy.md` for council scenes, battle chapters, cost scenes, and world-building economy; `genre-scifi.md` for inciting violation, compliance scenes, scale reveals, and resistance cell dynamics.

---

## Chapter Hook-Out Framework — The Next Button

The hook-out is the most commercially important sentence in any chapter. It is the only sentence the reader evaluates before deciding whether to stay. Every chapter must end on forward pull, never on resolution.

**Core rule:** end mid-tension, not mid-resolution. The reader should feel like the chapter ended one beat too early — which means they must click Next to get the beat they were promised.

**Forbidden endings (rewrite flag — any of these = the chapter fails the hook-out gate):**
- Summary sentences: "It had been a long day." / "She had a lot to think about."
- Emotional generalization: "She felt hopeful for the first time in months." / "He finally felt at peace."
- Scene-closing clichés: "She closed her eyes and let herself breathe." / "She fell into a dreamless sleep."
- Perfect resolution: "Everything was going to be fine." / "She let it go."
- Going to sleep / waking up as the chapter's final beat
- Any sentence that begins with "She/He finally…" and then resolves

---

### The 10 Hook-Out Techniques

Pick the one technique per chapter that fits the emotional beat. Do not use the same technique twice in a row.

#### 1. Mid-Motion Cut
Cut inside an action, not at its completion. The reader's own momentum carries them to the next chapter.

**When:** Any chapter where something physical is about to happen. Best for early-arc chapters.

**Formula:** Describe the action beginning. Cut before it completes. Never write what happens next.
> *She reached for the door handle. Her hand closed around cold metal.*

---

#### 2. Withheld Reaction
Something significant happens. The chapter ends before the protagonist reacts. The reader must know.

**When:** Revelation moments, confrontations, admissions. The event is the beat; the reaction is the next chapter's opening.

**Formula:** [The event / the thing said.] [One physical stillness detail.] END.
> *He said it. All of it. She stood very still.*

---

#### 3. Planted Bomb
The chapter appears to resolve. The final sentence retroactively recolors everything the reader just experienced.

**When:** Best at chapter midpoints in the arc — when the reader thinks they understand the situation and the narrative needs to destabilize.

**Formula:** [Resolution paragraph — the reader thinks it's over.] [Final 1-2 sentences that shatter the premise.]
> *She locked the apartment and didn't look back. Three floors below, someone had been watching her window for two hours.*

---

#### 4. Ticking Clock
A deadline that didn't exist in the opening paragraph appears in the final paragraph.

**When:** Any chapter where the stakes need to escalate. Especially effective after quiet intimacy chapters — the contrast between the warmth of the scene and the sudden time pressure is the hook.

**Formula:** [Closing action.] [New deadline, stated specifically — not vague.] [Character acknowledges she doesn't have enough time.]
> *The deal was done. Her phone buzzed once. Forty-eight hours, the message said. She understood, for the first time, that she had miscounted.*

---

#### 5. Decision at the Threshold
The character stands at the choice. The chapter ends before the decision is made.

**When:** Any chapter whose arc is a character being pushed toward a decision. End at the maximum pressure point, not after.

**Formula:** [Forces converge on the character.] [She knows what she has to do / what she's about to do.] [END before she does it — she does not move.]
> *She had the evidence. She had the exit. She had, finally, after seven months, the window. She did not move.*

---

#### 6. The Unanswered Line
The other character's dialogue or action is the chapter's final note. Their words are still in the air when the chapter ends. The protagonist does not get to respond.

**When:** Any chapter-ending exchange between two characters. Works in any genre — romance (the love interest's charged admission), mystery (the suspect's ambiguous denial), horror (the antagonist's threat), thriller (the ally's revelation). The reader is left holding the words, with no release.

**Formula:** [Exchange builds.] [Their final line — specific, charged, or ambiguous.] [Protagonist's response reduced to one physical detail only — no interior, no speech.]
> *"I'll be here when you decide," he said. She heard the door close. She did not look.*
> *"We both know what you found," the inspector said. The room went very quiet.*

---

#### 7. Overheard / Discovered Truth
The character learns something they weren't supposed to know. The chapter ends before they process it or act.

**When:** Mystery reveals, accidental discoveries, eavesdropped conversations. The discovery is the beat; the response is the hook.

**Formula:** [Discovery moment.] [The fact stated in one sentence, flat.] [Physical stillness — the body receiving what the mind hasn't processed yet.] END.
> *The file was open on his desk. Her name was in it — not as a contact, not as a reference. As the target.*

---

#### 8. False Resolution + Detonation
Appear to fully close the chapter's tension in the penultimate paragraph. Destroy it in the final two sentences.

**When:** Late-arc chapters, chapters after a major emotional win. Let the reader exhale — then pull the floor.

**Formula:** [Full resolution paragraph — sell it.] [Line break.] [Final 1-2 sentences that erase the resolution entirely.]
> *She'd handled it. She told herself that on the walk home, in the elevator, standing at the bathroom mirror.*
>
> *Her phone rang with a number she hadn't seen in two years.*

---

#### 9. Body's Unfinished Business
The physical tension between the pairing is at maximum. The chapter cuts on held breath, not on exhale.

**When:** Any chapter ending in unresolved physical proximity — romance (near-kiss, held breath), horror (hunter and hunted inches apart), thriller (confrontation that hasn't broken yet). The reader is physiologically pulled forward.

**Formula:** [Maximum proximity established.] [One precise physical detail: his hand, her breath, the distance between them.] [Neither moves.] [One environmental detail that underlines the silence.] END.
> *His hand was still at her jaw. She had not stepped back. Outside, the city was doing what cities do at 2 AM — making noise to cover everything that wasn't being said.*

---

#### 10. The Unanswered Question
One sharp, specific question — not rhetorical — that the reader cannot answer without clicking Next.

**When:** Chapters that end on character insight or partial revelation. The insight opens the question; the chapter ends with the question open.

**Formula:** [Chapter beat resolves.] [The question emerges from the resolution — voiced or as internal monologue.] [No answer. The chapter ends on the question itself.]
> *She got in the car. She put the key in the ignition. She sat there for a long time with one thought she couldn't dismiss: if he'd known all along, why had he said nothing?*

---

### Technique Selection by Chapter Position

| Position | Recommended techniques | Avoid |
|----------|----------------------|-------|
| Ch 1–4 (early) | Mid-Motion Cut, Ticking Clock, Overheard Truth, Planted Bomb | False Resolution (reader not invested enough), Body's Unfinished Business (too early for physical tension) |
| Ch 5–(N-3) (mid) | Withheld Reaction, Decision at Threshold, The Unanswered Line, Body's Unfinished Business, Unanswered Question | Mid-Motion Cut (loses impact when overused) |
| Last 3 chapters | False Resolution + Detonation, Planted Bomb, Decision at Threshold | Ticking Clock (too mechanical at the end), Unanswered Question if it's the final chapter |
| Final chapter | Allowed to resolve — but the last paragraph must still earn the close | Any forbidden ending from the list above |

---

### Hook-Out Rewrite Protocol (if an existing chapter fails the gate)

1. Read the chapter's final 3 paragraphs.
2. Identify the chapter's primary emotional turn (what changed from opening to close).
3. Ask: *what does the reader most want to know right now that this chapter hasn't answered?*
4. Select the technique that withholds exactly that answer.
5. Rewrite the final 1–3 paragraphs only. Do not touch the rest of the chapter.
6. Verify: the new ending must end the chapter one beat before the reader expected it to end.

---

## What to Read Before Each Chapter

```
Required:
  tracking/context.md                   — previous chapter ending + open threads
  outline/outline.md                    — this chapter's role in the arc (find by chapter number)

Load only if needed:
  world/characters/{character-name}.md  — only characters appearing in this chapter
  tracking/threads.md                   — only if this chapter resolves or plants a foreshadow
  reference/{book-title}/techniques.md  — only if a reference technique is needed
```

## Ensemble Plot & Cast Setup (required before any chapter writing)

Before expanding the outline or writing chapters, the world document must have a **Supporting Cast**, a **Relationship Web**, and a **Storyline Matrix**. A story with only two active characters produces flat scenes even when additional names exist in the world document.

**Active-character floor:** create **6–8 active named characters per book**, including the protagonist and primary love interest when present. At least **4 characters** must repeatedly affect the main plot through decisions, opposition, leverage, withheld information, resource control, or changes of allegiance. Background staff, unnamed witnesses, one-scene messengers, and passive confidants do not count toward the floor.

**Minimum cast requirements for `world/worldbuilding.md`:**

```markdown
## Supporting Cast

### [Name] — [Role archetype]
- Relationship to protagonist: [see genre table below]
- Independent goal: [what do they want even if the protagonist disappears?]
- Leverage / resource: [what can they grant, remove, expose, or destroy?]
- Conflict action: [what do they actively do that changes another character's options?]
- Alignment path: [ally / rival / uncertain, plus any planned shift]
- Function in story: [what tension, consequence, or information do they generate?]
- Distinct voice marker: [1 sentence — how they speak or behave differently from the leads]

### [Name] — [Role archetype]
...
```

**Required archetypes — pick at least 4 from your genre's table of 10:**

### Romance / Contemporary Drama
1. **Confidant** — best friend or sibling who receives the protagonist's confessions; absorbs exposition naturally; their reactions calibrate reader sympathy
2. **Romantic antagonist** — ex, rival suitor, or jealous third party who actively obstructs the central relationship
3. **Love triangle point** — a credible alternative romantic option; must be genuinely appealing, not obviously wrong
4. **Controlling authority figure** — parent, boss, or family member whose approval the protagonist needs or fears
5. **Matchmaker / orchestrator** — person who engineers proximity between the leads, knowingly or not
6. **Loyal ally with their own subplot** — friend or sibling with a romantic or personal arc running parallel; reinforces themes through contrast
7. **The messenger / witness** — someone who sees something they shouldn't, or delivers news that changes the stakes
8. **The work / world context character** — colleague, client, or professional contact who forces the leads into the same space on neutral ground
9. **Comic relief / grounding voice** — breaks tension without undercutting it; keeps the tone from becoming relentlessly serious
10. **The past made present** — someone from one lead's history who reveals a secret, complication, or wound the protagonist has kept hidden

For Hidden Heiress Divorce Revenge, ensure the selected cast collectively covers: a family conspirator, a corporate/legal gatekeeper, an independent witness or auditor, and an ally whose own stake can conflict with the heroine's. The romantic rival and ex-husband do not count as the entire opposition network.

### Fantasy / Paranormal
1. **Mentor / elder** — wizard, oracle, ancient being, or dying sovereign who holds knowledge the protagonist must earn; their power should be declining or limited
2. **Loyal companion / sidekick** — follows the hero without sharing their gift; reflects the arc back; can be killed to raise stakes
3. **Dark rival** — antagonist with mirrored power, opposing philosophy, or a claim on the same destiny
4. **Trickster / ambiguous ally** — helps and harms; true allegiance unclear until late; not evil, but not safe
5. **Council / court figure** — political power broker who forces the protagonist to navigate institutional constraint alongside magical threat
6. **The believer who is wrong** — someone whose faith in the old order or a false prophecy makes them dangerous despite good intentions
7. **The outsider / mundane anchor** — someone without magic or status who grounds the story in ordinary stakes and asks the questions the reader asks
8. **The defector from the other side** — an enemy who crosses over; brings secrets and distrust; may be a double agent
9. **The cost-bearer** — someone who pays the price of the protagonist's choices; their suffering personalizes the moral weight of power
10. **The keeper of the secret history** — archivist, scholar, or exile who knows what the official record erased; their knowledge arrives at exactly the wrong or right moment

### Mystery / Cosy Mystery / Gothic Thriller / Literary Thriller
1. **Red-herring suspect** — appears most guilty in the middle third; reader should genuinely believe them; their innocence must be earned, not announced
2. **Victim's inner circle** — friend, colleague, or lover who knew the victim best and reveals hidden motive by trying to protect someone or something
3. **Obstructive authority** — police, inspector, or institution that slows the protagonist; not incompetent — just working within different constraints
4. **The culprit** — must have a distinct voice, established presence, and at least one sympathetic trait before the reveal; their guilt must feel inevitable in retrospect
5. **The confidant / sounding board** — person the protagonist thinks through evidence with; voices the reader's doubts and pushes back on wild theories
6. **The informant / reluctant witness** — knows something but has a reason to stay silent; their silence is itself a clue
7. **The false ally** — appears to help; is concealing something (not necessarily guilt; could be shame, fear, or a separate secret)
8. **The prior victim** — someone who encountered the threat before the protagonist did and survived, escaped, or was silenced; their experience frames the protagonist's danger
9. **The community voice** — village gossip, pub regular, or local historian who holds the texture of a place and its grudges; provides colour and misdirection
10. **The character who changes the case** — late-arrival figure whose testimony, death, or disappearance forces the protagonist to restart from a new angle

### Horror
1. **Skeptic** — refuses to believe until forced to; their conversion is a structural beat; their disbelief makes the early dread feel earned
2. **First victim / cautionary figure** — establishes the threat's rules and reach before the protagonist is directly endangered
3. **Local expert / keeper** — historian, priest, old resident, or folkloric authority who holds the lore; their knowledge is partial and costs something to access
4. **Compromised ally** — possessed, coerced, mentally fracturing, or hiding their own infection; the protagonist cannot fully trust them
5. **The survivor from a prior cycle** — someone who lived through this before; traumatised, credible, and possibly unreliable
6. **The true believer / cultist** — someone who has chosen or been conditioned to serve the threat; their perspective makes the horror comprehensible without excusing it
7. **The protector who fails** — authority figure (parent, police, doctor) whose normal-world power is useless here; their failure marks the point of no return
8. **The innocent in danger** — child, dependent, or someone the protagonist is responsible for; their presence raises the cost of every decision
9. **The rationaliser** — insists on explaining everything away; useful for misdirection; must eventually be confronted with the inexplicable
10. **The one who knows and stays silent** — a character who understood the threat early and chose not to warn others; their silence is its own horror

### Sci-Fi / Dystopian
1. **Resistance cell member** — comrade with a distinct ideological angle, not just loyal; should disagree with the protagonist on method or priority
2. **True believer in the system** — enforcer or idealist who sees the protagonist as the villain; their logic should be coherent, not cartoonish
3. **Defector from the other side** — crossing over with secrets and earned distrust; their loyalty is perpetually in question
4. **Scientist / archivist with forbidden knowledge** — holds what the system erased; their knowledge creates the ethical dilemma at the story's core
5. **The compliant majority** — ordinary person who has accepted the system; their comfort makes the protagonist's resistance look irrational; their awakening (if it happens) is a turning point
6. **The handler / watcher** — regime figure assigned to monitor the protagonist; knows more than they reveal; may be an unlikely source of help
7. **The child of the system** — someone born after the change who has never known anything else; their innocence is both asset and vulnerability
8. **The black marketeer / information broker** — operates in the cracks between systems; helps for price, not principle; cannot be fully trusted
9. **The tech or protocol expert** — knows how the surveillance, the AI, or the infrastructure actually works; their knowledge is the protagonist's operational edge
10. **The ghost of the before** — someone who remembers the old world (or was shaped by it); their nostalgia is either wisdom or blindness, and the protagonist must determine which

### Historical / Regency
1. **Social gatekeeper** — hostess, matriarch, or gossip who controls reputation access; their approval or disapproval changes what is possible for the protagonist
2. **Rival or jealous peer** — same-class competitor with a different motive from the main antagonist; creates horizontal social pressure
3. **Confidant-servant or companion** — hears secrets by virtue of lower rank; sees the same events from a different vantage and provides corrective irony
4. **The reformer or outsider** — tradesman, foreigner, colonial subject, or political radical whose presence disrupts period social assumptions and forces the protagonist to examine their own position
5. **The family obligation** — sibling, ward, or dependent whose welfare the protagonist is responsible for; their needs constrain choices and create moral conflict
6. **The old scandal** — a person connected to a secret in the protagonist's or love interest's past; their reappearance destabilises the present
7. **The match-maker with an agenda** — parent, aunt, or sponsor engineering a marriage for reasons that may not align with the protagonist's interests
8. **The sympathetic enemy** — someone whose opposition is rooted in legitimate grievance, not malice; their conflict with the protagonist is the most interesting in the book
9. **The witness to the private self** — a character who has seen the protagonist outside their public role and holds that knowledge, whether as ally, threat, or complication
10. **The institution made human** — a character who embodies the period's dominant institution (the church, the law, the military, the court) and whose personal humanity complicates the protagonist's relationship to that power

After the cast list, add both planning artifacts:

```markdown
## Relationship Web

| Character A | Character B | Surface relationship | Hidden friction / debt / secret | Conflicting loyalty | Who currently has leverage? | Planned reversal |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... |

## Storyline Matrix

| Storyline | Driving character(s) | Concrete goal | Opposition | Midpoint reversal | Endgame collision |
|---|---|---|---|---|---|
| A — Core relationship / protagonist arc | ... | ... | ... | ... | ... |
| B — External crisis / power struggle | ... | ... | ... | ... | ... |
| C — Supporting-character agenda / betrayal | ... | ... | ... | ... | ... |
```

### Cast participation gates

- Every active character must have at least **3 consequential relationship edges** in the Relationship Web; at least one edge must contain hidden friction or debt, and at least one must contain a conflicting loyalty. A cast arranged as isolated satellites around the protagonist fails.
- At least **3 relationships** must change state twice during the book (for example ally → suspect → ally with conditions, spouse → enemy → reluctant co-conspirator). Attraction alone is not a state change.
- Each recurring supporting character appears in **at least 3 chapters** and causes a material plot change in at least **2** of them.
- At least **4 active characters** must still have unresolved goals at the midpoint. Do not collapse the book into the two leads after the opening act.
- No supporting character may exist only to receive exposition, approve the protagonist, deliver one clue, or create disposable jealousy. Give them an independent goal and a credible action when the leads are absent.
- Across the whole book, **lead-only chapters must be no more than 30%**. A lead-only chapter contains only the protagonist and primary love interest as active scene participants; background extras do not change this classification.
- Every rolling block of **3 chapters beginning with Chapter 2** must include at least **2 chapters with 3 or more active scene participants**. Chapter 1 retains its two-name introduction cap; expand the active cast from Chapter 2 onward.
- At least **one supporting-character decision every 2 chapters** must change access, information, safety, reputation, resources, or allegiance.
- Supporting characters must interact with one another without either lead present at least **twice per book**. These scenes prove the world has causality beyond the central couple.

### Multi-thread escalation gates

Run at least three interacting storylines throughout the book:

1. **A — Core relationship / protagonist arc:** attraction, trust, identity, or internal transformation.
2. **B — External crisis / power struggle:** investigation, family pressure, corporate threat, political contest, survival problem, war, or institutional constraint.
3. **C — Supporting-character agenda / betrayal:** a secondary character pursues a goal that can help, exploit, expose, or derail the leads.

Every storyline must have its own goal, opposition, midpoint reversal, and endgame consequence. At least once per act, one storyline must directly damage or complicate another. Do not write three parallel summaries that never collide.

### Escalation cadence

- Every chapter changes at least one of: goal, leverage, information, allegiance, deadline, safety, reputation, or access.
- Every chapter must contain a local complication or reversal: the attempted solution exposes a secret, strengthens an opponent, creates a witness, transfers leverage, splits an alliance, or forces an unwanted bargain. A chapter that merely completes the planned task fails even if its final line teases danger.
- Every major turn must alter at least **2 relationship edges**, or alter one relationship edge while materially damaging a separate storyline. Plot and relationship drama must compound rather than run in parallel.
- Every **2–3 chapters**, create an **irreversible consequence**: evidence becomes public, an alliance breaks, a resource is lost, a deadline locks, a secret reaches the wrong person, someone is injured/captured/removed, or a binding decision is made.
- Every **5–6 chapters**, deliver a **major reversal** that changes the reader's model of the conflict, transfers power, or forces a new plan.
- Across the book, use at least **4 different reversal mechanisms**: betrayal or allegiance shift; secret exposure; identity/status reversal; false victory with a larger cost; resource or custody transfer; public humiliation; forced alliance; presumed loss/return. Do not repeat the same misunderstanding or withheld-secret pattern.
- Never reset tension after a reveal. The next chapter begins from the new damaged state and introduces a harder choice; it does not restore the previous relationship arrangement.
- A cliffhanger that only withholds a spoken answer does not satisfy escalation by itself. The chapter must first produce a material change in the situation.

---

## Opening-First Writing (mandatory for new books)

Use this flow whenever writing a new long-form book. Do not draft the full book in parallel before the opening has proved it can convert cold traffic.

### Step 1 — Expand outline beats

Before spawning any agents, expand `outline/outline.md` so every chapter has a concrete beat entry:

```
Ch-NNN: [primary emotion] | cast: {active scene participants} | threads: {A/B/C advanced} | hook: {1-sentence} | conflict action: {who acts against whose goal} | complication: {why the attempted solution makes matters worse} | turn: {material change} | relationship shifts: {at least 2 edges, or 1 edge + 1 damaged storyline} | consequence: {reversible/irreversible} | hook-out: {open question}
```

All chapters must have this before any parallel writing starts. The beat entries replace `tracking/context.md` as the coordination signal during parallel writing.

### Step 2 — Write Chapters 1–3 as a sequential conversion batch

Write Chapter 1, then Chapter 2 from Chapter 1's actual final line, then Chapter 3 from Chapter 2's actual final line. Run the provisional First-Three-Chapter Conversion Gate below. Rewrite and recheck any failure before drafting Chapter 4 or later. This early gate prevents a structurally weak opening from being propagated across a completed manuscript.

Do not mark `tracking/quality-gates.md` final at this point. The recorded final PASS happens after A3 deslop, because prose cleanup can weaken, move, or accidentally explain away a hook.

### Step 3 — Draft Chapters 4+ in parallel

After Chapters 1–3 pass the provisional gate, spawn the remaining chapter agents concurrently. To avoid redundant file reads, read shared context once in the main context and pass it into each agent's prompt:

- **Read once, share with every agent:**
  - `world/worldbuilding.md`
  - Full expanded `outline/outline.md` (with beat entries for all chapters)
- **Read once, shard per agent:**
  - `world/characters/{character-name}.md` — only for characters appearing in that chapter
- **Coordination signal:** each agent receives the previous chapter's hook-out line from the outline beat.

Each agent writes Chapters 4+ to `content/{book-title}/chapters/ch-NNN-{title}.md` and returns its own hook-out line.

Use a **single batch Agent call** when the environment supports it (e.g. one Agent invocation carrying the remaining chapter list), otherwise spawn individual Agents per chapter. Chapters 4+ should be produced in parallel; Chapters 1–3 must not.

### Step 4 — Lightweight continuity pass

After all chapter agents complete, do a single sequential pass:
1. Read chapters in order; verify hook-out of chapter N matches the opening of chapter N+1.
2. Audit the outline's `cast`, `threads`, `conflict action`, and `consequence` fields. Verify the 30% lead-only cap, every rolling 3-chapter ensemble gate, supporting-character action cadence, 2–3 chapter irreversible cadence, and 5–6 chapter major-reversal cadence. Rewrite failing beats before prose cleanup.
3. **Word count check** — flag any chapter exceeding 1,800 words (1,500 for resolution chapters). For each flagged chapter: find the highest-tension cut point, split into two chapters, bump subsequent chapter numbers. Verify both parts meet the lower bound of ≥1,200 words:
   - If Part 1 < minimum, add details to Part 1.
   - If Part 2 < minimum, merge it back into Part 1 (do not save a skeleton).
   Update `outline/outline.md` with final chapter count. Then update `src/lib/books.ts` `chapterCount` for each book that underwent splits.
4. Fix only continuity and ensemble-plot breaks — do not rewrite prose for style.
5. Write `tracking/context.md` from the final chapter's ending.
6. Update `tracking/threads.md`, `tracking/timeline.md`, `tracking/character-status.md`.

Keep this pass minimal. Do not run a full quality rewrite here; that is A3.

### Step 5 — Final quality sequence

After all chapters exist, run these gates in order:

1. A3 full-manuscript deslop using `story-deslop.md`.
2. Re-read the final post-deslop Chapters 1–3 and run the First-Three-Chapter Conversion Gate.
3. Rewrite failures structurally, rerun deslop on the changed chapters, and repeat the conversion audit.
4. Create or update `tracking/quality-gates.md` only when both checks pass. A book may not advance to A4, build, commit, or publication with `FAIL`, `PARTIAL`, `TODO`, or an absent record.

### Multiple books in parallel

Spawn one top-level Agent per book. Pass only that book's `world/`, `outline/`, and character files so each agent starts with a minimal context. Books share no state and can complete in any order.

## Single Chapter Writing Process

Use this for adding one chapter to an existing book (incremental update only).

1. Read `tracking/context.md` — know the exact last beat.
2. Read the chapter's outline entry in `outline/outline.md`.
3. Name the chapter's **primary emotion** (tension / release / shock / ache / warmth).
4. Name the chapter's **turn**: what changes from start to end?
5. Name the **active cast**, the A/B/C storyline(s) advanced, and which character acts against another character's goal.
6. Write the **hook** (≤3 sentences): drop into motion, not setup.
7. Write the **escalation**: raise stakes through action/dialogue. No passive reflection blocks.
8. Write the **turn**: the moment that changes something — reveal, decision, or loss.
9. Write the **hook-out**: end mid-motion or on an open question. Never summarize.
10. **Length guidance** — treat word count as a pacing signal, not a hard gate:

   | Chapter type | Preferred range | Typical soft ceiling |
   |---|---|---|
   | Opening (ch 1) | 1,400–1,800 | 2,000 |
   | Escalation (ch 2–N-3) | 1,200–1,600 | 2,000 |
   | Climax (last 3) | 1,200–1,600 | 2,000 |
   | Resolution | 1,200–1,500 | 1,800 |

   If a chapter exceeds the soft ceiling without adding momentum, split at the strongest unresolved beat. The tail becomes the opening beat of the next chapter.
   If a chapter is far below preferred range and lacks scene value, add one concrete detail, scene action, or dialogue turn before saving.
   Adjust the outline accordingly.
   Do not pad with reflection or summary to hit a length target.

11. Save to `content/{book-title}/chapters/ch-NNN-{title}.md` from the project root, with correct zero-padded number.
12. **If split occurred in step 10:** update `src/lib/books.ts` — increment `chapterCount` by 1 for the book, and ensure all chapter filenames in `content/{book-title}/chapters/` match the final chapter numbering.
13. Update `tracking/context.md`: last beat + open threads + any foreshadow planted.
14. Update `tracking/threads.md` if foreshadow added or resolved.
15. Update `tracking/character-status.md` for any character changes, including goal, leverage, and alignment shifts.

## Chapter File Format

```md
---
title: "Chapter One: Night Crossing"
chapter: 1
---

Prose starts here — no leading blank line.
```

Frontmatter is optional but recommended. The site loader falls back to filename if `title` is absent.

Prose formatting rules:
- Adjacent paragraphs: blank line between them (`\n\n`). Within a paragraph, do not hard-wrap lines. (CommonMark renders a single `\n` as a space, collapsing all paragraphs into one block.)
- Dialogue quotes: half-width double quotes `""`
- No `……` or `——` in the prose product — rewrite as action, short sentence, or line break
- No chapter summaries or author notes inline

## Title Craft — Book & Chapter Titles

Titles are clickable surface area. A reader sees the book title before the cover loads, and scans the chapter list before committing to read. Both must do work, not just label.

### Book Titles

The book title appears on the home grid, the book detail hero, browser tabs, and every share card. It is the single most-repeated piece of text for the book. It must promise a specific emotional experience — not describe the plot.

**The bar:** a strong book title creates a question or a tension the reader wants resolved. "Convenient Husband" works because *convenient* and *husband* are in productive conflict. "The Garden" does not work as a book title — it describes a location, promises nothing.

| Pattern | Mechanism | Examples |
|---------|-----------|----------|
| **Possessive + charged noun** | Ownership implies a power dynamic | *The CEO's Obsession*, *The Devil's Debt* |
| **Oxymoron / productive conflict** | Two words that shouldn't sit together | *Convenient Husband*, *Borrowed Time*, *Cartel Prince* |
| **Loaded object as metaphor** | A concrete object that carries the whole theme | *Mark of the Moon*, *Iron Veil*, *Blood and Velvet* |
| **Stakes-in-two-words** | Names the irreversible thing | *Protocol Zero*, *Dead Frequency*, *The Last Crown* |
| **Threat/promise verb phrase** | Implies action already in motion | *Alpha Claimed*, *Dragon in Debt* |

**Banned book titles:**
- Pure location or object with no charge: *The Garden*, *The House*, *The Library*
- Character name alone (unless the name itself is iconic to the premise)
- Generic genre words: *Desire*, *Passion*, *Forbidden*, *Temptation* — these signal "every romance" and rank for nothing
- Abstract emotion nouns: *Longing*, *Yearning*, *Hope*

**Test:** say the title aloud, then ask "a story about what?" If the answer is fully contained in the title with no tension left, the title is flat. The title should make someone *ask* the question, not answer it.

### Chapter Titles

Chapter titles appear in the book detail chapter list — the reader scans them to gauge momentum before committing. A list of flat nouns ("The Arrival", "Names", "The Garden") reads as low-energy and kills scroll-through. A list of charged titles makes the reader want to read just to find out what each one means.

**Core rule:** a chapter title should be a small hook — it raises a question the chapter answers, or names a turn without giving it away. It must never spoil the chapter's turn.

| Technique | What it does | Examples |
|-----------|-------------|----------|
| **The loaded fragment** | A phrase pulled from the chapter's most charged line | *The Real Reason*, *What Stays*, *Speaking for Herself* |
| **The countdown / number** | A specific number that implies a clock or stakes | *Seven Days*, *Forty-Seven Steps*, *Twelve Marks* |
| **The withheld noun** | Names a thing without explaining it | *The Hackney Claim*, *Pack Recognition*, *The List* |
| **The quiet menace** | Innocuous words made ominous by the genre | *Documented*, *Something Permanent*, *Below Again* |
| **The line of dialogue** | A short charged quote from the chapter | *"I Know About the Mark"*, *"You Knew"* |

**Banned chapter titles:**
- Bare setting labels: *The Garden*, *The Hall*, *The Arrival*, *Night* — a place is not a hook
- Generic beats: *The Meeting*, *The Talk*, *The Decision* — names the function, not the tension
- Single flat nouns with no charge: *Names*, *Morning*, *Home*
- Titles that spoil the turn: if the chapter's twist is that he betrays her, do not title it *The Betrayal*

**Pattern across the chapter list:** vary the techniques down the list — don't title every chapter with a number, or every chapter with a fragment. The list itself should have rhythm. Escalate menace as the arc climbs: early chapters can be quieter, late-arc titles should feel heavier.

**Test:** read the full chapter list top to bottom as if it were a table of contents on the book detail page. Does it build? Does each title make you mildly curious? If three consecutive titles are flat nouns, rewrite them.

## Chapter Count Planning

**MANDATORY FIRST STEP — check existing counts before deciding anything:**

```bash
for d in content/*/chapters; do
  book=$(basename $(dirname "$d"))
  count=$(ls "$d"/*.md 2>/dev/null | wc -l | tr -d ' ')
  echo "$book: $count"
done
```

Run this command, read the output, and identify every long-form book below the 201-chapter minimum. Do not guess the current count — run the command before planning extensions.

**WARNING: Do NOT copy the chapter count from the reference site** (`velvet-throne/` or `midnight-fable/`). Those sites are borrowed for code/component structure only. Their chapter counts are irrelevant and must never be used as a default or template.

Plan a minimum of **201 chapters** for every long-form novel. The final count may be higher and should fit the story's scope; treat the count as story architecture, not filler:

> **Why 201+?** The business model is Facebook traffic arbitrage: every chapter is one pageview, and the profit equation is `RPM × pageviews/session − CPC`. A 201+ chapter novel creates a durable session-depth ceiling and supports multiple arcs. Do not fill chapters with padding; each chapter still needs a meaningful turn, consequence, or hook-out.

- A tight psychological thriller or revenge arc: 201+ chapters organized into short escalation arcs
- A paranormal/billionaire romance with full slow-burn arc: 201+ chapters with recurring relationship reversals
- A space opera, fae epic, or multi-POV dark fantasy: 201+ chapters with multiple major arcs

Existing long-form books with fewer than 201 chapters must be extended to at least 201 chapters before launch.

**Never default to a short 20–26 chapter plan.** If a long-form novel is planned below 201 chapters, stop and expand the arc architecture before writing.

Document the chosen count in `outline/outline.md` header before writing any beat entries.

## Pacing Guidelines

Word counts are targets, not uniform quotas. Let each chapter breathe according to its dramatic weight. Vary lengths across the book so readers feel the rhythm shift.

> **Facebook arbitrage note:** shorter chapters increase pageviews/session. A reader finishes a 1,200-word chapter in ~5 minutes and immediately clicks Next; a 2,500-word chapter takes ~12 minutes for the same single pageview. The cliffhanger hook-out is the #1 driver of next-pageview clicks — **never sacrifice the hook-out to add chapter count**. Use arc-level planning and natural word-count variation rather than padding.

| Chapter type | Word count range | Dialogue ratio | Action beats |
| --- | --- | --- | --- |
| Opening chapter | 1,400–1,800 | 20–30% | 3+ |
| Escalation chapter | 1,200–1,600 | 30–50% | 2–4 |
| Climax chapter | 1,200–1,600 | 15–25% | 4–6 |
| Resolution chapter | 1,000–1,400 | 20–40% | 1–2 |

## Chapter 1 — Cold-Traffic Hook Structure

Chapter 1 is the only chapter a Facebook ad click will ever guarantee. Every reader who arrives from a paid ad lands here first, knowing nothing — no character names, no story world, no emotional investment. The cold-traffic reader decides in the first 200 words whether to continue or hit Back.

This is a separate spec from the general "Single Chapter Writing Process." Apply it **only to ch-001**; other chapters follow the standard process.
The suspense rule itself is global: every later chapter still needs a scene-level question, withheld information, and a hook-out that makes the next page necessary.

### The cold-traffic contract

A warm reader (returning from organic search, book detail page, or recommendation) arrives with context. A cold-traffic reader arrives with one thing: the expectation set by the ad creative (the cover + tagline). Ch1 must immediately deliver on that expectation — the emotional register, the character type, the power dynamic — before it can ask for investment.

**Violation:** opening ch1 with backstory, worldbuilding, or a secondary character meeting the protagonist. These are legitimate techniques for chapters 4–8. In ch1 they signal to the cold reader "this isn't the story I came for" and cause a bounce.

### Chapter 1–2 premise-delivery gate (mandatory)

The first two chapters must deliver the concrete conflict promised by the ad creative. Romance charge is required only when romance is a primary promise; family, identity, legal, medical, workplace, crime, captivity, horror, and revenge stories must prioritize their own plot engine instead of inserting generic attraction.

**Priority rule:** the opening's observed-ad pattern outranks generic romance heat. Start with the specific short-drama event the creative promised — forced/strategic marriage, public rejection, debt ultimatum, evidence that changes a relationship, status reversal, or a return with leverage. Add consensual sensual tension inside that event; never substitute a generic intimate exchange for the actual crisis.

**Divorce-revenge opening rule (overrides the generic Chapter 1 sensual-delivery row below):** when the premise is Hidden Heiress Divorce Revenge, begin with the rupture, proof object, or agency decision—not an eroticized scene of intoxication, sleep, mistaken identity, drugging, coercion, or marital entitlement. The heroine must make a consequential choice within the first 500 words. If prior intimacy matters, establish adult capacity and mutual consent clearly, then move immediately to the accusation, public humiliation, evidence discovery, or finalized exit that drives the book. Chapter 1 may deliver relational charge through confrontation and broken trust; place any consensual new-romance proximity beat in Chapter 2 without displacing the external crisis.

| Chapter | Required delivery | On-page evidence |
|---|---|---|
| **Chapter 1** | The advertised confrontation within the first 500 words | A public rupture, proof object, coercive demand, status reversal, immediate danger, or other premise-defining event forces the protagonist to act. If romance is primary, include one consensual proximity/attention cue inside this event. |
| **Chapter 2** | Escalate or complicate the advertised conflict | Impose a new material cost, choice, deadline, exposure, or loss rather than explaining Chapter 1. If romance is primary, a voluntary touch, interrupted near-contact, private-room boundary, or third-party cost may carry the escalation. |

Write sensual story tension, never explicit content: use gaze, closing distance, an offered hand, a hand that stops short, a door closing, a shared room with a stated boundary, or the awareness of being watched. Every character is clearly adult; consent, reciprocity, and agency must be visible. Do not write sex acts, graphic anatomy, nudity, coercion framed as desire, or age-ambiguous characters.

**Failure conditions:** the advertised antagonist or conflict engine appears only after Chapter 2; Chapter 2 spends its first 500 words restating Chapter 1's reveal; Chapters 1–2 contain only worldbuilding or procedural explanation; or the only change is a withheld answer. Any failure requires restructuring before writing Chapter 4. For primary romance, also fail if the promised love interest has not appeared or all charge is non-consensual threat.

### First-Three-Chapter Conversion Gate (mandatory)

The opening is a three-pageview conversion funnel, not three setup chapters. Run this gate twice: provisionally before drafting Chapter 4, then finally on the post-deslop manuscript during A3.5.

#### Chapter 1: three-second conflict

- **First sentence:** contain conflict, contradiction, abnormality, or a decision already in motion. Naming the setting is not enough.
- **First 500 words:** produce one event that overturns the protagonist's normal situation. A threat or explanation without changed options does not count.
- **Information budget:** foreground only three payloads: the present dilemma, one abnormal detail, and one unresolved question. Carry other background through pressured dialogue or action; do not stop for an explanatory internal-history block.
- **Middle-density gate:** between the first identity/conflict proof and the final escalation, keep each 200-word window to at most 2 new memory burdens: a new named person, institution, document type, acronym, or specialized legal/commercial/medical concept. Existing focal-character names and concrete stake numbers do not count. If the reader needs an org chart, glossary, or procedural timeline to follow the scene, rewrite the middle.
- **Action translation:** make every abstract system fact change visible behavior within the next 2 paragraphs. Someone freezes a signature, grabs evidence, blocks security, changes sides, loses access, exposes a lie, or faces a deadline. Move facts with no immediate action to Chapter 2 or later.
- **Midpoint detonation:** the first key proof or discovery must trigger a larger family, legal, commercial, reputational, medical, or safety crisis. Evidence that merely confirms what the reader already knows is insufficient.
- **Final line:** land on a high-risk choice, a cognition-changing clue, or an opponent action already in motion. Mood, summary, and generalized resolve fail.

#### Identity-replacement variant

When another person is living under the protagonist's name or status:

1. Open in an important public setting where witnesses, cameras, officials, family, or money make denial costly.
2. Within the first 800 words, stage three distinct identity probes: one physical marker, one habitual behavior, and one private shared memory. Each probe must increase danger or shift a witness; do not present them as a static checklist.
3. After the first legal, biometric, financial, or archival proof appears, detonate a larger crisis that shows the dispute controls more than one person's name.
4. End with an unexpected action, declaration, or hidden proof that reveals the protagonist still holds leverage; cut on the resulting question, alarm, or cognition shift.
5. Do not explain backstory through interior monologue, describe identity through a mirror, or let dialogue settle the scene by simply announcing "this is fake." Make characters test, obstruct, expose, or act on the claim.

#### Chapter 1 middle: reduce concepts, increase events

The middle normally begins after the first 500-word overturn and ends when the final escalation starts. Its job is to convert curiosity into momentum, not teach the reader how the family, company, court, hospital, school, or criminal network works.

- Use plain functional labels on first mention: `passport record`, `court filing`, `trust vote`, `hospital order`, `board signature`. Save full institution names, statute names, document taxonomies, acronyms, dates, and procedural history for later chapters.
- Introduce one proof object at a time. Make a character attack, protect, misread, authenticate, or act on it before introducing another.
- Prefer `Adrian froze every signature` over an explanation of merger authorization; prefer `security chose whose order to obey` over a paragraph about authority.
- Keep at least one visible conflict action every 150–200 words: interruption, obstruction, evidence movement, public reaction, allegiance shift, deadline, or loss.
- Preserve only stakes the reader can feel immediately. Numbers such as `31%` or `$4 billion` are useful when a character reacts to them; they fail when followed by financial mechanics.
- Do not solve density by turning the chapter into a synopsis. Remove concepts, then replace some of the saved space with choices, reactions, reversals, and concrete interpersonal pressure. For five-ad chapter layouts, prefer roughly 1,250–1,500 words unless the site's ad-density rule requires more.

**Cold-reader retell test:** after reading Chapter 1 once, a reader should be able to say who is being erased, who benefits, what proof changed the room, and what new danger demands Chapter 2. If the retell depends on remembering company divisions, court names, medical chronology, document subclasses, or more than the core 3–4 people, the middle fails.

#### Chapters 2–3: no flat runway

| Gate | Chapter 2 | Chapter 3 |
|---|---|---|
| Opening consequence | Continue from Chapter 1's damaged state; do not reset location, power, or urgency for comfort | Begin under the cost created by Chapter 2 |
| First 500 words | Add a new material cost, choice, deadline, exposure, loss, or adversary action | Add a stronger reversal or evidence change; explanation alone fails |
| Mid-chapter turn | Make the attempted solution worsen another storyline or relationship | Force a plan change, alliance shift, public commitment, or resource transfer |
| Hook-out | Close on an immediate deadline, loss of access, dangerous bargain, or active countermove | Produce the opening arc's first irreversible consequence and a harder forward plan |

#### Hard-fail logic and record

- Grade each row `PASS` or `FAIL`; do not average away a failed first sentence, first-500 event, or hook-out.
- A hook must change options. Surprise, eloquent dialogue, chemistry, or an unanswered question without material change does not pass by itself.
- After any structural rewrite, rerun deslop on the changed chapter before regrading it.
- Save final proof in `tracking/quality-gates.md`:

```md
## Long-Form Quality Gates

Audit date: YYYY-MM-DD
Manuscript scope: Chapters 1–N

### A3 Deslop
Status: PASS
Coverage: Chapters 1–N, Gates A–G, Three-Pass routing complete

### A3.5 Opening Conversion
Status: PASS
Chapter 1: {first sentence / first 500 / information budget / middle density / action translation / midpoint / hook-out}
Chapter 2: {opening consequence / first 500 / midpoint / hook-out}
Chapter 3: {opening consequence / first 500 / midpoint / irreversible consequence}
Rewrites and rechecks: {none or exact chapters}
```

### Ch1 beat structure (200-word checkpoints)

| Words | Required beat | Purpose |
|---|---|---|
| 0–30 | Drop into motion — the protagonist is already doing something | Establishes POV and energy before the reader has time to disengage |
| 30–100 | One concrete detail that names the protagonist's world-defining problem | Gives the reader something to care about without explaining anything |
| 100–200 | Introduce the source of tension (person, situation, or object) | Sets the stakes; the reader must feel: "this is going wrong" |
| 200–400 | Establish what she wants and what's blocking her — in action, not narration | Emotional identification; reader must see themselves or someone they've read before |
| 400–700 | First unexpected turn — something changes that the protagonist did not expect | Proves the story will surprise; signals this is not a slow burn that earns nothing |
| 700–end | Escalate one more beat; land the hook-out on an unresolved reversal | Demands ch2; the reader should not be able to stop here |

### Specific rules for ch1 (do not apply to other chapters)

**Line 1 ban:** never open with weather, time of day, or a description of the setting. The first sentence must name or imply the protagonist and create immediate forward motion.

```
Banned: "The city lights shimmered below as Elena stood at the penthouse window."
Banned: "It had been three years since she last saw him."
Required: something that implies action, conflict, or a decision already in motion.
```

**Backstory cap:** ch1 may contain at most **two** sentences of backstory in the first 500 words. Backstory is permitted only when it creates irony (what she assumed vs. what is now true) — never to explain the world.

**Character introduction cap:** keep at most **two focal identities** in the first 200 words. A third named participant is allowed when the premise requires a claimant, impostor, and recognizer, but their relationship must be instantly legible. Introduce later witnesses only after the core conflict is clear. A crowd is useful when it raises the cost of denial; a roll call is a conversion killer.

**The Facebook Promise check:** before finalizing ch1, re-read the tagline from `src/lib/books.ts`. The emotional register of ch1's opening 200 words must match the register the tagline implied. If the tagline promises a charged, high-stakes encounter, ch1 must open in that register — not in a quiet or contemplative scene that delays the promised tension.

**Two-chapter promise check:** before shipping Chapter 2, verify that the specific confrontation, danger, proof, humiliation, or intimacy cue implied by the ad/tagline has appeared and escalated on-page. The reader must receive the promised scene, not a summary or a promise that it happens later.

**Dialogue timing:** first dialogue should appear before word 300. Dialogue signals that pressure exists between people and prevents the opening from becoming narrated setup.

### Ch1 word count target

Opening chapters target **1,400–1,800 words** (from the Pacing table). For cold-traffic arbitrage, aim for the lower half (1,400–1,500): a cold reader who finishes the chapter in under 7 minutes immediately clicks Next, which is a second pageview. A longer ch1 delays that click.

### The 200-word bail test

After writing ch1, read only the first 200 words. Ask: if someone arrived from a Facebook ad with nothing else to go on, would they feel something and want to know what happens next? If the answer is "they would understand the setting" — rewrite from word 1. Understanding is not feeling.

---

If chapter 1 exceeds ~1,700 words, prefer splitting at the strongest unresolved beat and making the second half chapter 2. Do not pad chapter 1 to satisfy old long-chapter instincts; a sharp 1,300-word opener with a hard hook-out is better for campaign learning than a slow 2,300-word opener.

## Context Handoff (`tracking/context.md` template)

```md
## Last Chapter Ending
{Final action or dialogue — 1–3 sentences}

## Next Chapter Start
{Which action or scene to continue from}

## Open Threads
- {foreshadow/suspense 1}
- {foreshadow/suspense 2}

## Target Emotion for Next Chapter
{tension / release / shock / lingering regret / warmth}
```

Always overwrite `context.md` after each chapter. Do not append history — the file is a rolling handoff.

## Quality Check Before Saving

- Hook: does it drop into motion? No weather, backstory, or setup.
- Turn: does something change? A chapter where nothing changes is a filler chapter.
- Hook-out: does it create forward pull? Reader must want the next chapter.
- No consecutive paragraphs with identical rhythm or length.
- No three consecutive sentences starting with the same subject.
- **Hook-out gate:** does the final sentence / final paragraph use one of the 10 named techniques from §"Chapter Hook-Out Framework"? Any forbidden ending (summary, emotional generalization, going to sleep, "finally…resolved") is a mandatory rewrite — do not ship the chapter until this passes.
- **One-paragraph test:** does the opening paragraph make the reader feel something in the first three sentences? If it only establishes setting or backstory, cut to the tension.
- **Named emotion check:** does every pivotal scene have a specific named emotional state (from the genre file's Named Emotion table)? Generic emotions ("nervous", "angry", "interested") are a rewrite flag.
- **Dynamic check:** is it clear who holds the power in this scene and who is off-balance? If all characters feel equally matched, the scene has no subtext.
- **Ensemble causality check:** does a character other than the lead pair pursue an independent goal or alter another character's options? If not, verify that this chapter fits within the 30% lead-only budget.
- **Thread collision check:** which of A/B/C advanced, and did one storyline complicate another when required by the act plan? A romantic conversation that changes no external condition is not enough.
- **Material-change check:** name the changed goal, leverage, information, allegiance, deadline, safety, reputation, or access. If none changed, the chapter is filler even if its dialogue is emotional.
- **Escalation-cadence check:** verify the outline still delivers an irreversible consequence every 2–3 chapters and a major reversal every 5–6 chapters. A withheld reply does not count as either.
- **Setting check:** does the location amplify the emotional stakes, or could it be any room? If it's interchangeable, change it.
- **Structural pattern check (Gate B — inline, do not defer):** before saving any chapter, do a 30-second scan for the two highest-frequency AI structural patterns:
  1. **Negation-reversal** — any sentence of the form "Not X. Y." or "No X. No Y. Just Z." → collapse to one direct statement.
  2. **Consecutive same-structure sentences ≥3** — any run of three or more sentences with the same subject-verb pattern (She'd…/She'd…/She'd…, He left./He turned./He said., Then she…/Then she…/Then she…) → vary the third sentence's structure.
  These two patterns appear in ~65% of AI-generated chapters and are the fastest fix with the highest reader-impact return. Fix them before saving; do not defer to A3.
- If other AI flavor is detected beyond the above two patterns, flag the chapter for the A3 deslop pass — do not run full deslop inline here. A3 (`references/story-deslop.md`) is loaded separately and runs after all chapters are written.

## Book Description & Tagline (Required — write before cover generation)

After chapters are complete, write the `tagline` and `description` fields for `src/lib/books.ts`. These appear on the book detail page and are the primary click trigger for every reader who arrives at the site. Apply the same hook standards as the cover: tension + question + desire, all three.

### Tagline (1–3 short sentences)

One sentence is ideal. Two is the maximum. It must reveal the core irony of the situation — what she came for vs. what she got, what was supposed to be simple vs. what it became.

**Banned:** genre labels ("enemies-to-lovers", "fated mates", "romance"), passive descriptions ("a story about"), vague emotional promises ("a journey of self-discovery").

**Patterns — pick the one that fits:**

| Pattern | Formula | Example |
|---------|---------|---------|
| **Action → consequence** | [what she did] → [the thing that happened because of it] | "She mapped his world. He had no defense against that." |
| **Intent + ironic reversal** | [what she came to do]. [what he did instead]. | "She came to end him. He made her the only person he trusted." |
| **Three escalating beats** | One [setup]. One [complication]. One [the real problem]. | "One qualifying spot. One fake relationship. One very real problem." |
| **Plan + role + failure** | [His plan]. [Her assigned role]. [Why the role failed]. | "He had a plan. She was supposed to be a variable. She was not a variable." |
| **She/He didn't expect** | [What she went in to do]. [What she didn't expect]. | "She crossed the Veil to complete a survey. She didn't expect to be claimed before she could cross back." |
| **Title-as-peak-state (fantasy / progression)** | Name the protagonist's achievement state or core power mechanic, not a thematic abstraction. | "Hundredfold Dominion", "The Last Cartographer of the Shattered Court", "Iron Sovereign" |

### Description (4–6 sentences)

Back-cover copy, not a plot summary. Each sentence has a job:

| Sentence | Job | What it must do |
|----------|-----|----------------|
| **1 — Protagonist state** | Who she is + why she's there | Names the character + the specific ordinary-world goal. Not "a woman who" — a person doing a specific thing. |
| **2 — The collision** | What went wrong when he entered | The inciting event in one sentence. What changed. "She didn't expect X." "X happened instead." |
| **3 — The exchange** | What each needs from the other | "[Character A] needs [X]. [Character B] needs [Y]." The transactional logic of the forced proximity or central conflict. |
| **4 — The third variable** | What neither planned for | This is the actual story. The thing the arrangement didn't account for. Must be specific, not vague. |
| **5 — Stakes (optional)** | What happens if they fail or succeed | Only include if it sharpens the hook. Cut if it reads like a plot outline. |
| **6 — The feeling (optional)** | The emotional impossibility in one image | One sentence that makes the reader feel the situation rather than understand it. |

**Genre-specific synopsis formulas** are in the relevant genre file. Load `genre-romance.md` for Formulas G/H/I (regression, villainess, monster romance); `genre-mystery.md` for Formula J; `genre-fantasy.md` for Formula K; `genre-scifi.md` for the sci-fi/dystopian formula; `genre-horror.md` for the horror formula.

---

### Self-Aware Genre Declaration (Fantasy / Sci-Fi / Progression — closing sentence only)

After 3–4 sentences of plot hook, close the synopsis for fantasy, sci-fi, or progression titles with one sentence that names the emotional register and genre promise explicitly. This sentence is for the recommendation algorithm and the reader's genre filter — it is not literary, it is pitch:

**Formula:** `This is a [genre adjective] [genre noun] about [emotional core 1], [emotional core 2], and [protagonist's transformation or peak state].`

**Example:** "This is a cinematic sci-fi progression saga about strategy, bloodline, and the birth of a monarch in ruins."

**Rule:** use ONLY as the final sentence, never as the opening. Do NOT use for romance titles — the hook sentence performs this function through emotional identification instead.

---

### Suspense Layer — The Information Gap (Required)

The description must **withhold** at least one piece of critical information. The reader should finish reading and immediately need to click — not because the story sounds good, but because there is a specific thing they don't know yet and cannot tolerate not knowing.

**The technique:** reveal that something exists, without revealing what it is or why it matters. The gap between "this thing exists" and "what this thing means" is the click trigger.

**Withheld-detail patterns:**

| Type | Formula | Example |
|------|---------|---------|
| **The counter-intuitive fact** | State a fact that demands explanation | "He fired her three times. She came back each time. On the fourth, he stopped trying." |
| **The incomplete revelation** | Something happened — the description doesn't say what | "She found the letter. Everything after that is his fault." |
| **The already-happened twist** | A consequence is named, not the cause | "By the time she understood what she'd agreed to, she was already in his city, in his life." |
| **The double secret** | Both characters are hiding the same category of thing | "She's been lying to him for six weeks. He's known for five." |
| **The unanswered question (explicit)** | End with a direct question the reader must click to answer | "The question she can't answer: which one of them is more dangerous?" |
| **The counter-expectation** | The setup happens, then one sentence undercuts it | "The wedding happens. That's not the problem." |
| **The withheld identity** | One character knows something about the other that the reader knows they know | "The man who bought her contract doesn't know she's the person who destroyed his company five years ago. She's counting on that." |

**Suspense check:** after writing the description, ask — *what specific thing does the reader not know that they now need to know?* If the answer is "nothing, it's all there" — add a withheld detail. If the answer is "the whole plot" (too vague) — make it specific. The withheld detail must be one sentence away from being revealed; the reader should feel they are *this close* to the answer.

**New tagline pattern — The Withheld Fact:**

| Pattern | Formula | Example |
|---------|---------|---------|
| **The withheld fact** | [Something happened]. [What it means is not said]. | "She found what he'd been hiding. She didn't tell him what she planned to do about it." |

---

**Quality check — one-second test:** if someone reads only the tagline and the first sentence of description, do they feel something and want to know more? If the answer is only "this sounds like a romance novel" — rewrite. The goal is "I need to know how this ends."

**Banned patterns:**
- Trope labels in reader-facing copy: `enemies-to-lovers`, `fake dating`, `fated mates`, `alpha male`
- Passive construction: "a story is told of...", "discover the world of..."
- Vague stakes: "everything they know will be tested", "nothing will ever be the same"
- Suspense that is too vague to be specific: "dark secrets", "hidden truth", "nothing is as it seems" — name the specific thing that is hidden, or don't mention it
- Placeholder description: do not ship a `description: ""` or `description: "Coming soon."`

### GEO Layer — AI-Citability (apply to Sentence 1 of every description)

The first sentence of `description` is used verbatim in `llms.txt` and as the page `<meta description>`. AI retrieval engines (Perplexity, ChatGPT, Claude web) cite the first sentence of structured content most frequently. Write Sentence 1 as a **self-contained relational triple** — Subject → Relationship → Object — that remains fully intelligible with no surrounding context:

**Formula:** `[Character A] [relationship dynamic] [Character B] — [the irreversible consequence].`

| Bad (context-dependent) | Good (self-contained) |
|-------------------------|----------------------|
| "She didn't expect this." | "A contract lawyer discovers her new client is the man who destroyed her firm — and he doesn't recognize her." |
| "Everything changed that night." | "A cartel bride fakes her own death to escape her arranged marriage; the cartel's enforcer is sent to retrieve her." |
| "Their worlds collide." | "A billionaire CEO hires his legal adversary as his temporary wife — she's the only one who can destroy him, and she knows it." |

This requirement does **not** change the hook writing standards above — the full description is still written for emotional impact. Only Sentence 1 must additionally satisfy the self-contained test.

---

## After All Chapters Written → Cover Generation (automatic, no prompt)

After the `tagline` and `description` are written and added to `src/lib/books.ts`, **immediately load `story-cover.md` and generate the cover** — do not ask whether to proceed. This is always the next step after the final chapter is saved.
