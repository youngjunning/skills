# Copyright gate for books

Use this gate whenever a book task uses third-party text, code, public repositories, images, tables, diagrams, characters, settings, translations, adaptations, substantial summaries, private manuscripts, or style references. Run it again before any public, commercial, publisher-facing, or platform upload. For GitHub or other source-available software, also load [open-source-book-sources.md](open-source-book-sources.md). For duplicate, overlap, near-paraphrase, or web-provenance checks, load [similarity-gate.md](similarity-gate.md).

This is a conservative production gate, not legal advice. It creates evidence, blocks obvious risks, and routes ambiguous legal questions to qualified review. It must never claim that a similarity scan proves originality or that a citation alone creates permission.

## Governing principles

- Copyright protects original expression, not facts, ideas, systems, methods, titles, or short phrases; the boundary between idea and expression still requires judgment.
- Translation, adaptation, reproduction, and compilation can implicate separate exclusive rights. Ownership of a copy, access to a text, or an online source does not grant those rights.
- Public-domain status is jurisdiction-, edition-, translation-, illustration-, and date-specific. A public-domain original can have a protected modern translation or annotated edition.
- Quotation exceptions are purpose- and amount-sensitive. In China, appropriate quotation for introduction, commentary, or explanation must identify the author and work and must not impair normal use or unreasonably harm the right holder's interests.
- Attribution is mandatory when the license or exception requires it, but attribution does not cure missing permission.
- A request to imitate a living or copyrighted author's style may be converted into high-level craft traits; do not copy signature phrases, passages, characters, world details, or a close substitute for the source work.
- Public repository access, GitHub fork rights, and an “open source” label do not by themselves license copied code or documentation. Project references and independently expressed facts or ideas remain separate from expressive reuse; require exact license, commit, path scope, and distribution obligations only for the latter.

## Source classification

Classify every source before it enters the drafting pipeline:

| Basis | Required evidence | Allowed default |
| --- | --- | --- |
| `owned` | Authorship or assignment proof and scope | Uses within the documented ownership scope |
| `licensed` | License or written permission, parties, territory, term, media, permitted uses | Only explicitly granted uses |
| `public-domain` | Jurisdiction, edition, author dates/publication facts, and authoritative evidence | Uses of that verified edition in that jurisdiction |
| `open-license` | Exact license/version, source, notice, modification and attribution terms | Uses the license permits after satisfying conditions |
| `statutory-exception` | Jurisdiction, legal basis, purpose, amount, attribution, market-effect analysis, reviewer | Only the reviewed use; never a blanket source clearance |
| `facts-ideas-only` | Source locator and a note separating facts/ideas from protected expression | Independent expression of verified facts or ideas |
| `unknown` | None or conflicting evidence | No derivative drafting or publish-ready use |

Search-engine snippets, retailer previews, pirated copies, model memory, “found online”, and an author's death without term analysis are not rights evidence.

## Three blocking checkpoints

### Gate A: intake

Before ingesting source material for drafting:

1. Identify the exact work, edition, creator, translator, illustrator, publisher, and locator where relevant.
2. Record intended uses: facts, reference, quotation, paraphrase, reproduction, adaptation, or translation.
3. Classify the rights basis and attach evidence.
4. Reject or quarantine `unknown`, leaked, DRM-circumvented, confidential, or apparently pirated material.
5. For adaptation or translation, require express permission or verified public-domain/open-license scope before producing chapter-length derivative prose.
6. For quoted, copied, adapted, screenshotted, vendored, or distributed repository material, pin a full commit SHA; inspect root and nested licenses, file headers, `NOTICE`, third-party code, submodules, documentation, assets, data, models, and trademark policies; split different rights scopes into separate source records. A reference-only project mention needs only proportionate source and version evidence.

The agent may help build an original alternative from unprotected ideas or facts, but it must not use an uncleared source as a hidden manuscript.

### Gate B: chapter

Before accepting a chapter:

- every quotation and close paraphrase has a source-use record, location, purpose, amount, and attribution;
- every expressive use has a lawfully obtained local comparison text; use only the relevant source portion when retaining a full copy is not permitted;
- quoted material is no more than needed for the stated purpose;
- facts and ideas have been independently expressed rather than syntax-swapped;
- protected tables, diagrams, poems, lyrics, letters, photographs, screenshots, and illustrations are separately cleared;
- repository code, documentation, examples, screenshots, generated output, datasets, models, logos, and companion downloads are cleared according to their own scope rather than the repository badge;
- no character, setting, plot sequence, example, or distinctive structure functions as an undisclosed adaptation;
- the local overlap scan has no unlogged matches above the configured threshold;
- repeated or near-duplicate passages inside the manuscript have a named editorial disposition;
- the chapter's source and rights delta has been written back to the ledger.

If a source is used only for research, the resulting prose must still be independently organized and expressed.

### Gate C: release

Before public or commercial delivery:

1. Validate the complete rights ledger and run both the deterministic similarity checker and copyright checker against the same manuscript version.
2. Search the web for several long, distinctive phrases from each high-risk or source-heavy chapter. In an interactive Codex task, use the available built-in web search capability without adding a separate service. For standalone CLI or CI, use `check_book_similarity.py --web-provider brave --require-web`. For a mainland-China publication, use the [Wanfang adapter](wanfang-similarity.md) unless the publisher mandates another platform. Record queries or provider, date, URLs, manuscript hash, report hash, reviewer, and dispositions.
3. Review high-similarity findings against the actual source, context, license, and logged quotation. Do not approve or reject a manuscript from an aggregate percentage alone.
4. Verify bibliography, endnotes, credit lines, license notices, image credits, and permissions against the compiled artifact.
5. Confirm title, cover, subtitle, series name, and marketing copy do not create separate trademark, publicity, privacy, or passing-off risks.
6. Require a named final reviewer and dated evidence. A qualified legal reviewer is required for an unresolved exception claim, orphan work, disputed ownership, high-risk commercial adaptation, or material jurisdiction conflict.
7. If expressive repository material or bundled third-party code is used, verify a named open-source license review across the printed book, ebook, sample chapters, companion repository, downloadable archives, and marketing assets.

`NEEDS_REVIEW` is blocking at this checkpoint. Only `PASS` permits a publish-ready claim.

## Automatic block conditions

Return `BLOCK` when any of these is present:

- source, edition, creator, translator, or rights holder cannot be identified where identification is necessary;
- rights basis is `unknown`, pending, expired, contradictory, or supported only by assertion;
- requested use exceeds the recorded license, territory, term, media, or permitted action;
- chapter-length translation, adaptation, abridgment, continuation, fan sequel, or reproduction lacks express authority or verified public-domain scope;
- quotation or distinctive expression is unlogged, unattributed, excessive, decorative, or substitutes for the source;
- the user asks to remove attribution, conceal the source, evade detection, or continue after a failed rights check;
- a local or web similarity check finds unexplained overlap;
- release review, evidence, or required qualified legal review is missing.
- a GitHub-derived expressive use lacks an exact commit, path-level license evidence, obligation compliance, or separate non-code/trademark review where applicable.

Do not downgrade a block because the output is AI-generated, rewritten, free, educational, internal, attributed, or not yet monetized. Those facts can affect analysis but are not blanket permission.

## Needs-review conditions

Return `NEEDS_REVIEW` for a non-release draft when material can be isolated but one of these remains unresolved:

- reliance on fair use, fair dealing, or another statutory exception;
- uncertain public-domain term, foreign publication history, restored rights, or modern derivative edition;
- open-license compatibility, share-alike, no-derivatives, or attribution ambiguity;
- a close paraphrase, distinctive sequence, or substantial qualitative taking that exact-match tools cannot settle;
- memoir privacy, confidential correspondence, interview releases, composite characters, or third-party allegations;
- title, cover, image, table, or quotation permissions that are not required for the current text draft but are required for release.

Keep the affected material out of the release artifact until resolved.

## Ledger and checker

Run the similarity gate first:

```bash
python scripts/check_book_similarity.py manuscript/ \
  --ledger sources/copyright-ledger.json \
  --report reviews/similarity-report.json
```

For an interactive Codex task, perform the targeted discovery with the built-in web search capability and retain its evidence. For standalone automation, add `--web-provider brave --require-web` and retain named decisions in `reviews/similarity-decisions.json`. For a Wanfang-backed domestic release, also record and verify `reviews/wanfang-evidence.json` with `check_wanfang_similarity.py`. See [similarity-gate.md](similarity-gate.md) for provider, privacy, threshold, and disposition rules.

Then run the rights gate.

Create the template with:

```bash
python scripts/check_book_copyright.py --write-template sources/copyright-ledger.json
```

Run the gate with:

```bash
python scripts/check_book_copyright.py manuscript/ \
  --ledger sources/copyright-ledger.json \
  --report reviews/copyright-report.json
```

The copyright checker validates required evidence, use permissions, quotation records, final reviews, and exact overlap against lawfully obtained local comparison texts listed in the ledger. The similarity checker adds internal exact and near duplicates, near-source overlap, optional automated web discovery, and named dispositions. Codex built-in web discovery is recorded separately because the standalone script cannot invoke a conversation tool. A public or commercial manuscript cannot pass with a quotation, paraphrase, reproduction, adaptation, or translation whose comparison text is unavailable. Both tools use the same status contract:

- exit `0`: `PASS`;
- exit `2`: `BLOCK`;
- exit `3`: `NEEDS_REVIEW` for an unresolved review finding;
- exit `1`: invalid input or execution error.

Neither checker can discover every source or decide substantial similarity. The release gate therefore also requires targeted web or publisher-approved external checks and named human review.

## Decision record

For each gate run, retain:

- manuscript hash or version/commit;
- ledger path and report path;
- publication intent and jurisdictions;
- source counts by rights basis;
- quotations, adaptations, translations, reproductions, and exceptions reviewed;
- local-overlap and web-search findings with dispositions;
- reviewer, date, remaining conditions, and final status.

Never report `PASS` for a later manuscript version using an earlier report without re-running the gate.
