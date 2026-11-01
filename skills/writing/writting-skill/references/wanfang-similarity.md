# Wanfang similarity adapter

Use this reference when a Chinese-language book is intended for publication in mainland China, the user asks for 国内查重 or 万方检测, or the publisher accepts a Wanfang report.

## Why Wanfang is the default domestic adapter

Wanfang's official similarity service explicitly covers publication and distribution scenarios, supports Chinese and English submissions, and compares against domestic journals, dissertations, conference papers, newspapers, patents, standards, laws and regulations, and academic web resources. It provides individual and institutional products, downloadable reports, and an official report-authenticity page.

This makes it a useful domestic complement to the local checker and Codex web discovery. It does not replace the publisher's required platform. If the publisher mandates CNKI, VIP, or another service, use that service and retain its accepted report instead.

Use only these official domains:

- personal service: `https://jc.wanfangdata.com.cn/`;
- institutional service: `https://check.wanfangdata.com.cn/`;
- report verification: `https://truth.wanfangdata.com.cn/`;
- contracted API gateway information: `https://cloud.wanfangdata.com.cn/`.

Do not submit manuscripts to lookalike domains, marketplace sellers, shared accounts, or unofficial resellers.

## Integration boundary

Wanfang advertises a unified API gateway with detection services, but the official request schema, authentication contract, retention terms, pricing, and credentials are not publicly documented. Do not reverse-engineer browser requests or invent API endpoints.

Until a publisher or institution supplies the contracted API documentation and credentials, use the supported report workflow:

1. Obtain authorization to upload the manuscript and confirm it contains no state secret, client secret, embargoed material, personal information, or other restricted data that the service is not approved to process.
2. Submit the exact compiled manuscript through an official Wanfang page. Prefer DOC or DOCX when the service recommends it; remove tracked changes and comments, and make references structurally identifiable.
3. Download the official report promptly. The personal service states that reports are retained for 30 days, so the release project must keep its own immutable copy.
4. Verify the report number and document title at the official authenticity page.
5. Bind the report artifact to the manuscript version with `check_wanfang_similarity.py record`.
6. Re-run `verify` immediately before the copyright gate. Any manuscript or report hash change invalidates the evidence.

## Record official evidence

```bash
python scripts/check_wanfang_similarity.py record manuscript/ \
  --report-file reviews/wanfang-official-report.pdf \
  --report-id "REPORT_ID_FROM_WANFANG" \
  --checked-at YYYY-MM-DD \
  --overall-similarity 0 \
  --reviewer "REVIEWER_NAME" \
  --verification-url "https://truth.wanfangdata.com.cn/" \
  --verification-evidence "Report number and document title matched on the official verification page." \
  --output reviews/wanfang-evidence.json
```

Use the actual overall similarity shown by Wanfang. The example value `0` is a placeholder, not a target or pass threshold.

The evidence record contains:

- Wanfang report number and detection date;
- manuscript path, file count, and SHA-256;
- retained official report path and SHA-256;
- overall similarity as report metadata, never as the release verdict;
- named authenticity reviewer, review date, official verification URL, and concrete evidence.

## Verify before release

```bash
python scripts/check_wanfang_similarity.py verify manuscript/ \
  --evidence reviews/wanfang-evidence.json
```

Exit codes:

- `0`: `PASS`, retained evidence still covers this manuscript and report artifact;
- `2`: `BLOCK`, evidence, hash, official domain, or authenticity review is invalid;
- `1`: invalid input or execution failure.

This `PASS` means only that the retained Wanfang evidence is internally valid. A named reviewer must still inspect the detailed matched passages and resolve quotation, attribution, license, false-positive, and close-paraphrase findings. The aggregate percentage never grants copyright clearance.

## Release routing

For a mainland-China public or commercial book release:

1. local manuscript and known-source scan must pass;
2. Codex distinctive-phrase web discovery must be reviewed;
3. Wanfang evidence verification must pass when Wanfang is the selected or publisher-accepted domestic provider;
4. every material Wanfang match must have a named disposition;
5. the rights ledger and copyright checker must pass for the same manuscript hash;
6. a publisher-mandated platform overrides this default and its report must be retained with equivalent evidence.

Do not upload the same unpublished manuscript to several providers merely to obtain a lower percentage.
