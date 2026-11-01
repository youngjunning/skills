# Referencing open-source projects in technical books

Use this reference when an original technical book discusses a solution that refers to, compares with, uses, quotes, modifies, screenshots, or ships material from an open-source project. The project is supporting technical evidence, not the book's source manuscript. This workflow extends [copyright-gate.md](copyright-gate.md); it does not replace the exact license text or qualified legal review.

## Core boundary

Publicly readable is not the same as licensed for reuse. GitHub permits viewing and forking public repositories through GitHub's service, but a repository without an applicable license remains under default copyright rules. Treat `public`, `forkable`, `popular`, `educational`, and `open source` as different claims. This matters only when protected material is reused; it does not prevent the author from citing a project, describing verified facts, comparing architectures, or independently explaining unprotected ideas.

For Level 3 expressive reuse, do not clear an entire repository from the badge shown by GitHub. Resolve rights at the exact commit and path used because a repository can contain:

- code under the root software license;
- documentation under a different content license;
- examples, generated files, vendored dependencies, submodules, or copied snippets under separate licenses;
- screenshots, icons, fonts, diagrams, datasets, model weights, prompts, and media outside the code license;
- names and logos governed by trademark policies rather than the software license.

For Level 3, one ledger source record must describe one coherent rights scope. Split a repository into multiple source records when directories or files have different owners, licenses, or obligations.

## Classify the intended use

| Book use | Default treatment |
| --- | --- |
| Explain an algorithm, architecture, API behavior, or engineering decision in original language | `facts-ideas`; cite the project and relevant version or date; use an exact commit only when the claim depends on inspected implementation details |
| Link to a repository, compare projects, or recommend further reading | `reference`; no code-license compliance record is required unless protected material is reproduced |
| Use the project as an ordinary package, tool, runtime, or external dependency | Record the dependency and tested version; escalate only if the delivery bundles its files, modifies it, or copies its implementation into the book or companion code |
| Print a code excerpt verbatim | `quote` or `reproduce`; verify license or statutory exception, amount, notices, attribution, and book/ebook distribution obligations |
| Rewrite or simplify repository code while retaining its expressive implementation | `adapt`; treat it as a derivative use and satisfy the source license |
| Independently implement the same unprotected idea | `facts-ideas`; keep evidence showing independent organization and expression, and do not syntax-swap the source |
| Reproduce README prose, documentation, diagrams, tables, or screenshots | Classify the specific material separately; never assume the software license covers it |
| Show program output | Check whether the output contains protected program text, art, UI assets, sample data, or trademarks; the code license alone may not decide output rights |
| Use a project name or logo in the title, cover, or marketing | Run a separate trademark and non-endorsement review; an open-source license normally does not grant trademark rights |
| Ship runnable companion code copied or adapted from the repository | Treat the companion as a distribution artifact with its own complete `LICENSE`, notices, source-availability, modification, and copyleft review |

Prefer explaining verified mechanisms and creating an original minimal implementation. This reduces license coupling but does not permit disguised paraphrase or reimplementation of protected expression.

## Escalate by actual use

### Level 1: reference or ideas

Use for project mentions, comparisons, architectural inspiration, verified behavior, API descriptions, and independently written方案:

- record project name, canonical URL, relevant release/version/date, and the claim it supports;
- use a full commit only when the claim depends on a particular implementation detail;
- write the explanation and diagrams independently;
- classify the use as `reference` or `facts-ideas`;
- do not require a repository license review merely because the project is cited.

A source-visible project without a License can still be cited and analyzed. It cannot supply copied or adapted expression by default.

### Level 2: dependency use

Use when the book's original demo or companion project calls an open-source library, CLI, server, framework, or model runtime without copying its source:

- record the package/project, resolved version, official locator, tested role, and detected license;
- distinguish normal dependency installation from bundling third-party files into a downloadable artifact;
- do not treat API calls, execution, or package-manager installation alone as code copied into the manuscript;
- run distribution obligations when the companion artifact vendors, bundles, modifies, or redistributes the dependency.

### Level 3: expressive reuse or distribution

Run the full repository License gate when the book or its delivery quotes, reproduces, adapts, translates, screenshots, vendors, or distributes repository material.

## Full repository intake

Before Level 3 use:

1. Record the canonical repository URL and a full commit SHA. Never use only `main`, `master`, `latest`, a mutable release page, or an unpinned web snippet as release evidence.
2. Record commit permalinks for every quoted or adapted file, including path and line or symbol location.
3. Inspect root and nested `LICENSE`, `COPYING`, `NOTICE`, `README`, file headers, SPDX identifiers, `THIRD_PARTY*`, vendored directories, submodules, generated assets, and package metadata.
4. Record the exact SPDX license expression when standard identifiers apply. Preserve `AND`, `OR`, `WITH`, `-only`, and `-or-later`; they are not interchangeable.
5. Define `path_scope`: the exact files or directory prefix proved to be governed by that record. A root license badge is supporting evidence, not automatic proof for every asset.
6. Record copyright holders and notices that must survive reproduction.
7. Derive the obligations for the actual book use and publication format. Record a named reviewer, date, evidence, and every applicable obligation.
8. Obtain a lawful local comparison copy for any quotation, paraphrase, reproduction, or adaptation so the overlap checker can distinguish logged use from accidental copying.

Re-run intake after changing the commit, path, edition, format, or intended use.

## License-family decision guide

This table is a routing aid, not a substitute for the license text:

| Situation | Conservative book rule |
| --- | --- |
| No license, missing scope, custom terms, or unclear owner | Use only independently expressed facts/ideas and references; block copied or adapted expression until permission or reviewed exception exists |
| MIT, BSD, ISC, or another permissive software license | Commercial use may be permitted, but preserve the required copyright and license notices wherever covered code is distributed |
| Apache-2.0 | Preserve the license and applicable attribution; propagate required `NOTICE` material, mark modifications where required, and keep patent and trademark boundaries visible |
| GPL or AGPL | Do not assume a commercial book is prohibited; instead review whether the printed excerpt, ebook, downloads, and companion code form a covered distribution and satisfy license-copy, source, and copyleft obligations. Small statutory-exception snippets require jurisdiction-specific review |
| LGPL, MPL, EPL, or file/library-scoped copyleft | Review the exact boundary and modified files. Do not generalize “weak copyleft” into blanket permission |
| CC, GFDL, or another documentation/content license | Apply it to the covered prose, figures, or media, not automatically to code. Check attribution, ShareAlike, NoDerivatives, invariant sections, and format requirements |
| Dual or multiple license | Preserve the exact `OR` or `AND` expression and record which permitted option is selected; do not silently choose the least restrictive label |
| Dataset, model, weights, benchmark, or generated asset terms | Create a separate source record; software licensing does not automatically cover these artifacts or personal-data and acceptable-use constraints |

If copyleft compatibility, statutory exception, custom terms, or scope remains disputed, return `NEEDS_REVIEW` for drafts and `BLOCK` for public or commercial release.

## Ledger fields

For Level 1 reference or facts/ideas, a lightweight source and use record is enough:

```json
{
  "source": {
    "id": "project-reference",
    "source_type": "software-repository",
    "title": "Example Project",
    "creator": "Example maintainers",
    "locator": "https://github.com/owner/repo",
    "repository_url": "https://github.com/owner/repo",
    "rights_basis": "facts-ideas-only",
    "rights_status": "cleared",
    "proof": "Used only as a cited technical reference; no protected material reused"
  },
  "use": {
    "source_id": "project-reference",
    "kind": "facts-ideas",
    "manuscript_location": "chapter-04/方案对比",
    "purpose": "Support an independently written architecture comparison"
  }
}
```

For Level 3 expressive reuse, add the full record:

```json
{
  "id": "repo-example-src",
  "source_type": "software-repository",
  "title": "Example repository source files",
  "creator": "Named copyright holders",
  "locator": "https://github.com/owner/repo/tree/FULL_COMMIT_SHA/src",
  "repository_url": "https://github.com/owner/repo",
  "commit_sha": "FULL_COMMIT_SHA",
  "path_scope": ["src/"],
  "rights_basis": "open-license",
  "rights_status": "cleared",
  "proof": "LICENSE and file headers inspected at the recorded commit",
  "license": "Apache License 2.0",
  "license_status": "open-license",
  "license_expression": "Apache-2.0",
  "license_evidence": ["commit permalink to LICENSE", "commit permalink to NOTICE"],
  "allowed_uses": ["reference", "facts-ideas", "quote", "reproduce", "adapt"],
  "license_review": {
    "status": "passed",
    "reviewer": "NAME",
    "date": "YYYY-MM-DD",
    "evidence": "Scope and distribution formats reviewed",
    "obligations": ["attribution", "license-copy", "notice", "change-notice"]
  },
  "source_text_path": "research/repo-example-src.txt"
}
```

Every expressive use of that source must add:

```json
{
  "source_id": "repo-example-src",
  "kind": "adapt",
  "material_type": "code",
  "source_path": "src/example.py",
  "source_permalink": "https://github.com/owner/repo/blob/FULL_COMMIT_SHA/src/example.py#L10-L32",
  "manuscript_location": "chapter-04/example-02",
  "purpose": "Teach the retry state transition",
  "attribution": "Project and copyright-holder credit",
  "modified": true,
  "compliance_evidence": {
    "attribution": "Appendix A and code caption",
    "license-copy": "companion/THIRD_PARTY_LICENSES/Apache-2.0.txt",
    "notice": "companion/NOTICE",
    "change-notice": "caption and source header mark this as modified"
  }
}
```

For non-code expressive material, add `material_rights_evidence` proving that the relevant license or permission covers that exact documentation, image, diagram, screenshot, dataset, model, output, or logo. For `logo-trademark`, also add a passed `trademark_review` with reviewer, date, and evidence.

## Chapter and release gates

Before accepting a chapter:

- every project-derived claim points to the relevant project version, date, or inspected commit at the precision the claim requires;
- every expressive use has an exact source path, commit permalink, attribution, comparison text, and satisfied-obligation evidence;
- adapted code is visibly marked and remains within the proved license scope;
- examples described as original were independently designed rather than mechanically renamed from the source;
- screenshots, diagrams, documentation, datasets, models, outputs, and marks have separate scope evidence.

Before release:

1. Run the normal deterministic copyright checker.
2. If Level 3 material or bundled third-party code exists, run a named `open_source_license_review` across print, ebook, sample chapters, marketing images, downloadable archives, and companion repositories.
3. For Level 3 materials and bundled code, generate a third-party inventory from the ledger and compare it with the compiled book and shipped files.
4. For those materials, verify attribution, copyright notices, full license texts, `NOTICE`, modification notices, source links or offers, ShareAlike or copyleft deliverables, and trademark disclaimers in the actual output.
5. Check that implementation-specific GitHub evidence and every expressive-use permalink are pinned to the recorded commit.

Ordinary Level 1 references do not turn the entire book into a derivative work and do not require the book to adopt the project's software license. Do not call the book publish-ready if Level 3 manuscript material or bundled companion artifacts fail license compliance. Report manuscript, code companion, notices, and trademark review as separate states.
