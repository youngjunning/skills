# Publishing requirements for books

Use this reference for publisher-facing manuscripts, print or ebook editions, public or commercial Book releases, and any request to make a book publish-ready. It governs editorial apparatus and production consistency; it does not replace factual, technical, similarity, copyright, legal, or rendered-artifact review.

## Source-of-truth order

Resolve requirements in this order:

1. signed publishing contract and current publisher or imprint style sheet;
2. editor instructions, manuscript template, house examples, and edition-specific production notes;
3. the target output's technical specification for print, PDF, EPUB, DOCX, or another delivery format;
4. a named external citation or editorial standard only when the publisher adopts it or no higher-priority rule exists;
5. a documented provisional scheme for drafting when no publisher requirement is available.

Do not assume that one publisher, journal, academic style, national standard, or previous edition applies to another. Record the source, version, date, medium, and any editor-approved exception. A provisional scheme can keep a manuscript internally consistent, but the publishing-apparatus status remains `NEEDS_REVIEW` until the actual publisher requirements are applied.

### Mainland-China baseline

For a book published in mainland China, verify the current publisher requirements and applicable law or standards at the time of the edition. As of 2026-08-27, the minimum baseline includes:

- the National Press and Publication Administration's [《图书质量管理规定》](https://www.nppa.gov.cn/xxgk/fdzdgknr/zcfg_210/bmgz_213/202112/t20211208_442149.html), which treats content, copyediting, design, and printing as separate quality dimensions and sets the qualifying copyediting error-rate ceiling at `1/10000`;
- [CY/T 266—2023《图书编校质量差错判定和计算方法》](https://www.nppa.gov.cn/xxfb/tzgs/202306/t20230630_718503.html), effective since 2023-08-01, for current industry error classification and calculation;
- [GB/T 7714—2025《信息与文献 参考文献著录规则》](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14), current since 2026-07-01, when the publisher or book type adopts the national bibliographic-reference standard; do not continue treating the superseded 2015 edition as current;
- [GB/T 15834—2011《标点符号用法》](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=22EA6D162E4110E752259661E1A0D0A8) and [GB/T 15835—2011《出版物上数字用法》](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=F5DAC3377DA99C8D78AE66735B6359C7), both currently listed as active;
- [GB/T 7713.2—2022《学术论文编写规则》](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=0B963916637B8F34B295FCF4A51A1BE5) only when the artifact is an academic paper or the publisher explicitly adopts it; it is not a generic replacement for a book's house style.

These are a baseline, not a complete publisher specification. Check current versions rather than freezing this dated snapshot into a later edition. Do not claim formal compliance from a text lint alone: the regulated error rate depends on professional error classification and the final laid-out book.

## Gate sequence

Keep development, editing, and production passes separate:

1. **Developmental readiness:** stabilize reader promise, architecture, chapter jobs, evidence plan, and major omissions before layout work.
2. **Substantive and technical edit:** verify facts, logic, terminology, examples, code, equations, figures, and domain correctness.
3. **Copyedit:** apply the governing language, punctuation, numeral, citation, note, heading, caption, and style rules without changing meaning.
4. **Citation and rights review:** validate source metadata, inspect whether each source supports the associated claim, check updates or retractions, and clear permissions separately.
5. **Proofread and production preflight:** inspect the stable laid-out artifact for text, numbering, cross-reference, page, font, image, color, metadata, and export defects.
6. **Final proof:** re-run navigation, generated lists, index locators, links, and production checks after the last pagination or ebook reflow.

Do not use copyediting or layout to conceal an unresolved structural problem. Do not treat a clean source manuscript as proof that the compiled artifact is clean.

## Editorial style record

Before a full manuscript pass, record the fields that affect the work:

- publisher, imprint, edition, language, territory, and print or digital formats;
- manuscript template, style-sheet version and date, named editor instructions, and approved exceptions;
- chapter and heading hierarchy, numbering depth, table-of-contents depth, and unnumbered front/back-matter rules;
- note system, in-text citation system, bibliography style, quotation treatment, and locator requirements;
- numbering and caption rules for figures, tables, equations, examples, listings, boxes, exercises, and appendices;
- cross-reference syntax, glossary, abbreviation list, index scope, and page-proof workflow;
- author-introduction, contributor-credit, portrait, affiliation, contact, and disclosure requirements;
- source-file, asset, font, image resolution, color, accessibility, filename, and delivery-package requirements.

Keep these decisions in the book contract or a compact editorial-style file that can be reloaded. Do not distribute them across chat history or infer them from a rendered sample when a written rule exists.

## Heading hierarchy and navigation

- Map each semantic level to one publisher style and use it consistently. Do not skip a level, use bold body text as a hidden heading, or change numbering depth for visual convenience.
- Keep chapter, part, section, subsection, front matter, back matter, and unnumbered headings distinct. Follow publisher rules for punctuation, capitalization, spacing, numbering, and table-of-contents inclusion.
- Preserve stable heading identifiers or bookmarks when the toolchain supports them. Regenerate the table of contents and navigation after structural edits; do not hand-maintain page numbers that can drift.
- Flag excessive depth. A fourth or fifth heading level often indicates that the structure needs consolidation, but the publisher's permitted depth remains authoritative.

## Notes, citations, quotations, and bibliography

- Use exactly one governing note and citation scheme unless the publisher explicitly defines exceptions. Keep footnotes, endnotes, author-date citations, numeric citations, and explanatory notes in their assigned roles.
- Give every load-bearing factual, historical, empirical, or attributed claim a source at the precision the style requires. Include page, section, chapter, timestamp, version, DOI, URL, access date, edition, translator, or repository revision when material to locating or evaluating the claim.
- Ensure every in-text citation and note resolves to a complete bibliography entry, and every bibliography entry is cited or intentionally retained under publisher rules. Detect missing, orphaned, duplicated, and inconsistent records.
- Preserve exact quotation text, delimit quotations correctly, identify omissions or additions, and record the locator. A close paraphrase still needs attribution when the underlying idea or sequence belongs to a source.
- Prefer primary, canonical, or current official sources for technical and factual claims. Label secondary synthesis, vendor claims, author observations, and author inferences accurately.
- Keep citation compliance separate from permission. A correctly formatted reference does not clear copyright, privacy, trademark, or license obligations; the copyright gate remains blocking.
- Validate metadata and claim support separately. Crossref metadata search or its REST API can help resolve DOI, title, author, date, and publication metadata; DOI resolution alone does not show that the source supports the manuscript claim. For scholarly sources, also check corrections, updates, expressions of concern, and retractions through the publisher record, Crossmark when available, and another authoritative status source required by the field.
- For load-bearing claims, maintain a compact evidence mapping with manuscript location, claim, citation key, exact source locator, support type, verification date, and disposition. A bibliography without claim-level traceability cannot prove that citations are relevant.

## Figures, tables, equations, examples, and listings

- Follow the publisher's numbering scope, such as continuous book-level numbering or chapter-based numbering. Maintain separate sequences for each object type unless instructed otherwise.
- Refer to every numbered object from the body with a stable cross-reference. Place the object near its first meaningful callout when the template permits; never rely on “上图”“下表” when pagination or reflow can change.
- Require the complete caption, title or takeaway, units, legend, abbreviations, source or credit line, rights status, and modification disclosure that apply to the object.
- Keep editable source files and publication-grade exports. Verify resolution, dimensions, color mode, fonts, line weights, grayscale legibility, and alt text against the target medium.
- Generate computed tables, charts, and values from the same maintained source when practical. Re-run cross-references after insertion, deletion, reordering, translation, or layout changes.

## Index, glossary, and appendices

- Treat the index as a reader-navigation artifact, not a keyword dump or duplicate table of contents. Establish scope and entry policy early, then generate and edit locators from the final paginated proof. Re-run it after any reflow.
- Normalize preferred terms, aliases, names, products, acronyms, and cross-references such as `see` or `see also` according to the publisher style. Merge trivial variants and add subentries only when they help retrieval.
- Keep the glossary limited to terms the intended reader must look up. Definitions must match the manuscript's actual usage and terminology state.
- Put supporting material in appendices only when it is useful but would interrupt the main reading path. Give each appendix a distinct purpose, label and title; cite it from the body; apply the same source, rights, numbering, and cross-reference standards as the main text.
- Do not use appendices to hide missing reasoning, unreviewed source dumps, stale code, or material that belongs in the companion repository.

## Author introduction and contributor material

Load [technical-book-author-bio.md](technical-book-author-bio.md) for a technical-book author introduction. Apply the publisher's required length, grammatical person, ordering, placement, affiliations, links, portrait and credit specifications, contributor-role labels, and disclosure limits. Verify every credential and project relationship; remove promotional adjectives that add no evidence.

## Language and copyediting gate

For nonfiction narration, require rigorous, accurate, plain written language:

- use stable terms, concrete actors, precise verbs, bounded claims, and explicit conditions;
- reduce recoverable personal pronouns and replace vague third-person reference with the responsible role, team, product, or system;
- remove narrator-added colloquial expressions, chatty transitions, hype, empty significance claims, vague authority, anthropomorphism, and rhetorical decoration;
- preserve natural language inside faithful prompts, dialogue, quotations, interview responses, and UI copy when the artifact itself is evidence; keep the surrounding explanation in the publication register;
- do not make the text obscure merely to sound formal. Prefer plain standard written Chinese over bureaucratic wording or unnecessary nominalization.

Copyediting must not silently change technical meaning, numerical precision, quotation text, legal wording, code, identifiers, or the strength of evidence.

## Acceptance gate

Before calling a manuscript publisher-ready or publish-ready:

1. identify the governing requirements and bind the review to the exact manuscript or artifact version;
2. validate heading hierarchy, navigation, notes, citations, bibliography, quotations, numbered objects, captions, callouts, cross-references, glossary, index, appendices, author material, and front/back matter;
3. run link, reference, asset, terminology, placeholder, and rights checks;
4. compile or render every target format and inspect representative front matter, dense body pages, figures and tables, notes, bibliography, index, appendices, and author material;
5. re-run generated navigation, numbering, cross-references, and index locators after final pagination or reflow;
6. record reviewer, date, governing style source, checked artifact hash or version, unresolved finding count, and status.

Use the repository checker for deterministic preflight and evidence binding:

```bash
python scripts/check_book_publishing.py manuscript/ \
  --write-template reviews/publishing-evidence.json

python scripts/check_book_publishing.py manuscript/ \
  --evidence reviews/publishing-evidence.json \
  --report reviews/publishing-report.json
```

The checker can verify heading jumps and configured depth, required sections, local links and images, empty image alt text, unresolved placeholders, likely colloquial narration, pronoun-led framing, manuscript hashes, publisher-requirement evidence, manual-review evidence, and a configured copyediting error-rate ceiling. Findings about colloquial wording and pronouns are review candidates because Markdown alone cannot always distinguish narration from inline quotation. The checker cannot decide factual correctness, citation support, professional error counts, copyright permission, index quality, layout quality, or publisher acceptance.

Return `NEEDS_REVIEW` when publisher requirements are missing or provisional, final pagination is unavailable for the index, or an editor decision is still required. Return `BLOCK` when the target artifact has broken hierarchy, unresolved citations, missing references, stale numbering, broken cross-references, unreviewed figures, invalid index locators, missing required author material, unresolved rights, or production defects. Only `PASS` supports an unconditional publish-ready claim.
