# Book writing

Use this reference for fiction and nonfiction books, novels, memoirs, handbooks, ebooks, multi-chapter tutorials, and substantial manuscript revision. It extends the shared writing and voice rules in `SKILL.md`; it does not create a separate house style.

Before using third-party material or calling a manuscript publish-ready, also read [copyright-gate.md](copyright-gate.md). For publisher-facing work, a print or ebook edition, public or commercial release, or any publish-ready claim, also read [publishing-requirements.md](publishing-requirements.md).

## Route by book type

| Type | Primary contract | Main failure mode |
| --- | --- | --- |
| Picture book / 绘本 | Page-level story, exact copy, illustration briefs, cover-inclusive count and print geometry; follow [picture-book.md](picture-book.md), using `joyally-image` for images | Repeated scenes, lost learning outcomes, tiny text, clipped important objects, incorrect page totals |
| Nonfiction or technical | Reader problem, thesis, evidence map, chapter promise, usable outcome | Repetition, unsupported authority, chapter-as-article fragmentation |
| Fiction | Story promise, character desire, causality, viewpoint, world rules, reveal boundaries | Continuity drift, inert chapters, implausible knowledge or agency |
| Memoir or narrative nonfiction | Lived truth, memory limits, privacy boundaries, documentary support, narrative arc | Invented certainty, composite people presented as literal, privacy harm |
| Handbook or reference | Task taxonomy, lookup paths, stable terminology, examples, coverage boundaries | Forced linear reading, duplicated rules, stale facts |
| AI technical book | Minimally qualified reader, concept-to-artifact progression, reproducible evidence, version horizon | Runnable-looking but broken code, benchmark theater, rapid factual drift |
| Adaptation or translation | Rights scope, source edition, permitted transformation, attribution, fidelity policy | Unauthorized derivative work or false public-domain assumption |

If a book mixes types, name one primary contract and list the secondary contracts. Do not let a narrative device weaken factual standards in nonfiction.

For an AI technical book, also load [ai-technical-book.md](ai-technical-book.md). Its executable-code, experiment, version-drift, and technical-review gates extend rather than replace this workflow. For a short children's picture book, use the picture-book page manifest instead of chapter machinery, and the child's read-aloud register instead of a technical author's voice. An AI subject does not by itself require the technical-book profile.

## Book contract

Record the minimum durable contract before drafting several chapters:

- working title and one-sentence reader promise;
- intended reader, their starting state, and the change the book should produce;
- book type, scope, exclusions, target length, delivery format, and publication intent;
- central thesis or story promise and what would count as breaking it;
- voice profile and source corpus; for the author's own book, load [style-zisheng.md](style-zisheng.md) by default unless he selects another voice;
- factual standard, citation style, uncertainty policy, privacy boundary, and copyright jurisdictions;
- publisher, imprint, edition and medium when known; governing style sheet, manuscript template, editor instructions, and unresolved production requirements;
- chapter unit, review cadence, and definition of publish-ready.

Keep this contract short enough to reload. Mark unresolved choices explicitly; do not hide them inside prose.

## Persistent project shape

Use a persistent structure when the work spans sessions or more than a few chapters. Adapt existing project conventions instead of forcing these filenames:

```text
book-root/
├── book.md                       # contract, reader promise, thesis or story promise
├── outline.md                    # chapter map and dependencies
├── state.md                      # terminology, facts/canon, open loops, promises
├── sources/
│   ├── copyright-ledger.json     # rights and use records
│   └── research/                 # source notes; full source text only when lawful and needed
├── manuscript/                   # canonical chapters
├── reviews/                      # continuity, fact, reader, similarity, and copyright reports
└── output/                       # compiled delivery artifacts
```

The manuscript is authoritative for what the reader has actually seen. If a summary or state file conflicts with the canonical prose, verify the prose, correct the state, and record any downstream impact.

## Progressive context

Do not load a whole book by default. Expand context only when the task requires it:

1. **Task:** the exact chapter, scene, revision, or review request.
2. **Hard constraints:** book contract, local project rules, copyright ledger, voice profile.
3. **Near field:** current chapter, adjacent chapters, directly linked research or canon.
4. **Active state:** terminology, timeline, character or claim state, open loops, reader promises.
5. **Far structure:** relevant outline slice, arc, part, or dependency map.
6. **Cold text:** distant chapters and unused research, excluded until a concrete dependency appears.

Read full prose, not summaries, when judging rhythm, dialogue, ambiguity, emotional progression, exact claims, quotation use, or style fidelity.

## Outline and chapter contracts

The outline is a dependency map, not a list of topics. Every chapter must have a distinct job and a reason to appear at that point.

Record for each chapter:

- reader or story question entering the chapter;
- chapter promise or mission;
- required prior knowledge and dependencies;
- evidence, example, scene, conflict, or mechanism that earns the chapter;
- entry state and exit state;
- new terms, facts, characters, claims, reveals, or open loops;
- deliberate callback or setup;
- rights-sensitive source material and required attribution;
- verification and revision status.

For nonfiction, require a claim-evidence-warrant-action chain where the genre needs one. For fiction, require a legible pressure-choice-action-consequence change without forcing every scene into the same beat sheet.

## Chapter cycle

### 1. Preflight

- Reload the book contract, chapter contract, voice profile, active state, and relevant copyright records.
- Read the previous chapter and the next planned interface; expand farther only for a named dependency.
- Resolve facts, canon, viewpoint knowledge, quotation scope, and source permissions before prose makes them expensive to unwind.

### 2. Draft

- Deliver the chapter's promised change; do not write a long article that happens to share a book title.
- Give abstractions a mechanism, scene, example, artifact, source, or consequence.
- Preserve the author's voice without copying a reference author's distinctive expression.
- Make callbacks useful to the current chapter instead of recapping earlier material.
- End at a genuine transition, implication, decision, discovery, or pressure point; not every chapter needs a cliffhanger.

### 3. Local edit

Review in this order so later polish is not wasted:

1. chapter mission and structural necessity;
2. factual or canonical correctness;
3. causality, argument, viewpoint, and continuity;
4. examples, scenes, dialogue, and transitions;
5. voice, rhythm, clarity, and AI-flavor;
6. citations, attribution, quotation, and copyright evidence.

### 4. State write-back

After accepted edits, update only facts that became true in the canonical manuscript:

- terminology and definitions;
- claims and evidence status;
- character, relationship, location, possession, knowledge, and timeline state;
- setups, callbacks, unresolved questions, and promised payoffs;
- privacy decisions, permissions, quotations, and source-use records;
- changes that invalidate later chapters or outline assumptions.

Do not allow state files to invent prose that has not been written.

## Review cadence

Use the lightest cadence that catches cascading errors:

- every chapter: mission, local continuity, facts/canon, voice, copyright delta;
- after the first three chapters: reader promise, chapter differentiation, voice calibration;
- at each part or arc boundary: structure, terminology, timeline, open loops, evidence distribution;
- before compilation: full-manuscript repetition and near-duplicate scan, contradiction, promise/payoff, citation, privacy, and copyright review;
- after compilation: rendered navigation, headings, notes, bibliography, image rights, front/back matter, and metadata.

Never describe a chapter count, outline, partial batch, or compiled file as a finished book unless the requested manuscript and acceptance checks actually exist.

## Book-level review

Run separate passes; one generic "polish" pass is not enough:

| Pass | Questions |
| --- | --- |
| Promise | Does the book deliver what its title, introduction, and structure promise? |
| Architecture | Is each chapter necessary, distinct, ordered correctly, and proportionate? |
| Continuity | Do terminology, facts, timeline, characters, examples, and callbacks remain stable? |
| Evidence or canon | Can every load-bearing claim or story rule be traced and reconciled? |
| Reader | Where will the target reader become lost, unconvinced, bored, or unable to act? |
| Voice | Does the book sound like one author across chapters without repeated mannerisms? |
| Publishing apparatus | Do heading levels, notes, citations, bibliography, figures, tables, cross-references, index, appendices, author introduction, and front/back matter follow the governing publisher requirements? |
| Copyright and privacy | Are all third-party materials, quotations, adaptations, images, and personal disclosures cleared? |

Report findings with location, severity, evidence, consequence, and a bounded revision. Do not silently rewrite the whole manuscript when the user asked for review.

## Delivery state

For a substantial book task, maintain these fields in the project state or requested delivery report. Do not append them as a default writing summary:

- 书稿阶段：构思 | 书约 | 大纲 | 初稿 | 结构修订 | 文本精修 | 全书审阅 | 编译交付
- 连续性：checked scope, unresolved contradictions, and state files updated
- 出版编校：`PASS` | `NEEDS_REVIEW` | `BLOCK` with governing style sheet or provisional scheme, checked artifact, and unresolved finding count
- 查重门禁：`PASS` | `NEEDS_REVIEW` | `BLOCK` with manuscript hash, report path, provider scope, and unresolved finding count
- 版权门禁：`PASS` | `NEEDS_REVIEW` | `BLOCK` with ledger path, checker result, and unresolved item count

Only `PASS` across the applicable continuity, publishing-apparatus, similarity, and copyright gates can support “publish-ready”, “可出版”, or equivalent language. Surface unresolved or blocking states when they affect the requested handoff.
