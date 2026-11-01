# Similarity gate for books

Use this gate for book 查重、重复段落检查、来源重合检查、疑似近似改写排查，and the similarity portion of a public or commercial release review. It complements [copyright-gate.md](copyright-gate.md); similarity is evidence for editorial and rights review, not a legal conclusion.

## What the gate measures

Keep four questions separate:

1. **Internal repetition:** does the manuscript repeat the same or nearly the same long passage across chapters?
2. **Known-source overlap:** does the manuscript overlap comparison text recorded in the copyright ledger without a corresponding quotation or reuse record?
3. **Unknown web provenance:** do distinctive manuscript phrases lead to existing web pages that require review?
4. **Rights disposition:** is a match an allowed quotation, intentional callback, false positive, original public sample, licensed reuse, or unresolved copying risk?

Do not collapse these questions into one percentage. A low aggregate score can hide one material copied passage; a high score can be caused by bibliography, quoted text, standard terminology, or the author's own public sample.

## Default local scan

Run the local scan without external services:

```bash
python scripts/check_book_similarity.py manuscript/ \
  --ledger sources/copyright-ledger.json \
  --report reviews/similarity-report.json
```

The checker:

- extracts prose blocks from Markdown and text files while excluding frontmatter, headings, fenced code, standalone images, and Markdown tables;
- detects exact long-passage repetition across the manuscript;
- detects near duplicates with SimHash candidate generation, character-shingle Jaccard similarity, and sequence similarity;
- compares manuscript paragraphs with lawful local comparison texts referenced by `source_text_path` in the copyright ledger, including partial exact overlap through a 50-character sliding window;
- excludes expressive uses whose excerpt is already logged as `quote`, `reproduce`, `adapt`, or `translate`;
- emits a manuscript content hash, thresholds, exact locations, excerpts, scores, findings, and limitations in JSON.

Default thresholds are conservative starting points, not universal definitions of substantial similarity:

- minimum normalized paragraph length: `80` characters;
- known-source exact overlap window: `50` normalized characters;
- manuscript near-duplicate sequence threshold: `0.88`;
- known-source near-overlap sequence threshold: `0.84`.

Lower a threshold only for a named review purpose and record the value in the retained report. Do not tune thresholds merely to obtain `PASS`.

## Codex web discovery by default

Local comparison can only find sources present in the ledger. In an interactive Codex task, use the current session's built-in web search capability to discover unknown public web candidates. This path needs no separate API key or similarity service.

1. Extract several long, distinctive phrases from every high-risk or source-heavy chapter. Exclude quotations, code, generic definitions, headings, and sensitive text.
2. Search each phrase as an exact or tightly constrained query with the built-in web search tool.
3. Open plausible results and compare the manuscript passage with the source in context.
4. Record query, manuscript location, search date, result URL, relevant snippet or comparison note, disposition, reviewer, and manuscript hash in `reviews/distinctive-phrase-search.json` or the ledger's review evidence.
5. Treat every plausible result as a candidate for human review. A hit does not prove copying, and no hit does not prove originality.

Send only selected distinctive phrases, never the whole manuscript. Do not search confidential, embargoed, private-client, or unpublished sensitive text without authorization. Built-in tool availability can vary by Codex session and environment; if it is unavailable, do not claim the discovery step passed. Use the unattended adapter below, use a publisher-accepted service, or return `NEEDS_REVIEW`.

## Unattended CLI or CI discovery

The standalone Python checker cannot invoke the web tool belonging to the current Codex conversation. For deterministic CLI, CI, scheduled, or unattended runs, configure the optional Brave Search adapter:

```bash
export BRAVE_SEARCH_API_KEY="REPLACE_ME"
python scripts/check_book_similarity.py manuscript/ \
  --ledger sources/copyright-ledger.json \
  --web-provider brave \
  --require-web \
  --exclude-domain zisheng.pro \
  --report reviews/similarity-report.json
```

The checker sends only selected distinctive phrases, not the whole manuscript. It records the query, manuscript location, result URL, title, and snippet. A result is `web-match-candidate` and requires human disposition.

The Brave adapter is opt-in and is not required for an interactive Codex run whose built-in web-search evidence was retained. Keep API keys in environment variables and out of the ledger, manuscript, report, Git history, and Skill files.

## Human dispositions

Review findings against the actual manuscript, source, rights ledger, and publication history. `block` findings cannot be waived by a disposition; fix the manuscript or rights record. A `review` finding can be cleared with a named, dated decision:

```json
{
  "schema_version": 1,
  "decisions": [
    {
      "finding_id": "COPY_FROM_REPORT",
      "status": "false-positive",
      "reviewer": "the author",
      "date": "YYYY-MM-DD",
      "evidence": "The result republishes this author's earlier approved sample; URL and publication date verified."
    }
  ]
}
```

Allowed decision statuses are:

- `false-positive`: the candidate is not a meaningful match;
- `intentional`: the internal repetition is deliberate and editorially justified;
- `resolved`: the manuscript, ledger, attribution, or permission evidence was corrected and rechecked.

Re-run with:

```bash
python scripts/check_book_similarity.py manuscript/ \
  --ledger sources/copyright-ledger.json \
  --web-provider brave \
  --require-web \
  --decisions reviews/similarity-decisions.json \
  --report reviews/similarity-report.json
```

Decisions must contain a reviewer, ISO date, and concrete evidence. The checker downgrades only matching `review` findings to `info`; an exact unlogged source overlap remains blocking until the source use is recorded or the text changes.

## Status and exit codes

| Status | Meaning | Exit |
| --- | --- | ---: |
| `PASS` | No unresolved block or review finding in the checked scope | `0` |
| `BLOCK` | Missing a specifically required CLI web provider, unlogged exact source overlap, missing comparison text, or invalid evidence | `2` |
| `NEEDS_REVIEW` | Near duplicate, near-source overlap, web candidate, or optional provider failure remains unresolved | `3` |
| execution error | Invalid path, JSON, arguments, credentials, or runtime input | `1` |

For public or commercial delivery, `NEEDS_REVIEW` is blocking. Preserve both the report and decisions beside the manuscript version they cover; a later manuscript hash requires a new scan.

## External similarity services

`SearchProvider` is the extension boundary for automated discovery outside the interactive Codex session. The bundled CLI implements only `BraveSearchProvider` because it can search exact phrases without uploading the complete manuscript. It is an automation adapter, not the default interactive path.

Wanfang is the default domestic report adapter for a Chinese-language book intended for publication in mainland China when the publisher accepts it. Follow [wanfang-similarity.md](wanfang-similarity.md) and use `check_wanfang_similarity.py` to bind the official report to the manuscript hash. A publisher-mandated platform overrides this default.

Copyleaks, Turnitin, 知网, 维普, or another publisher-designated platform should remain optional release adapters rather than default dependencies:

- confirm contract, data region, retention, deletion, indexing, confidentiality, and whether submissions enter a shared comparison corpus;
- retain the provider report, configuration, manuscript hash, date, and named reviewer;
- reference that evidence from `reviews.distinctive_phrase_search` in the copyright ledger;
- do not convert a provider's aggregate similarity percentage into an automatic copyright decision.

When the publisher mandates a named platform, its accepted report can satisfy the external-search requirement, but the local manuscript and known-source scan still runs. Do not upload a manuscript to multiple commercial services merely to chase a lower percentage.

## Release gate

Before calling a book publish-ready:

1. Local similarity report is `PASS` for the final manuscript hash.
2. Every known-source comparison text required by the copyright ledger was available.
3. Unknown-source discovery has reviewed evidence from Codex built-in web search or `--require-web` with named decisions.
4. For a mainland-China release using Wanfang, `check_wanfang_similarity.py verify` returns `PASS` for the final manuscript and retained report hashes; otherwise retain the publisher-mandated external report with equivalent evidence.
5. The copyright ledger's similarity review names the reviewer, date, report, queries or provider, and dispositions.
6. `check_book_copyright.py` also returns `PASS`.

Neither checker replaces editorial judgment, source verification, license compliance, or qualified legal review.
