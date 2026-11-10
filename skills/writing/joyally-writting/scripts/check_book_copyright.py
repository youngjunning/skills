#!/usr/bin/env python3
"""Conservative evidence gate for book copyright records.

This checker validates a JSON rights ledger and scans a manuscript for unlogged
exact overlap with local source texts. It cannot determine legal infringement or
replace qualified legal review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Iterable


PUBLIC_INTENTS = {"public-noncommercial", "commercial"}
RIGHTS_BASES = {
    "owned",
    "licensed",
    "public-domain",
    "open-license",
    "statutory-exception",
    "facts-ideas-only",
    "unknown",
}
USE_KINDS = {
    "reference",
    "facts-ideas",
    "quote",
    "paraphrase",
    "reproduce",
    "adapt",
    "translate",
}
EXPRESSIVE_USE_KINDS = {"quote", "paraphrase", "reproduce", "adapt", "translate"}
REPOSITORY_LICENSE_STATUSES = {
    "open-license",
    "multiple",
    "custom",
    "none",
    "unclear",
}
REPOSITORY_MATERIAL_TYPES = {
    "code",
    "documentation",
    "image",
    "diagram",
    "screenshot",
    "dataset",
    "model",
    "generated-output",
    "logo-trademark",
}
NON_CODE_MATERIAL_TYPES = REPOSITORY_MATERIAL_TYPES - {"code"}
TEXT_SUFFIXES = {".md", ".markdown", ".txt"}


TEMPLATE: dict[str, Any] = {
    "schema_version": 1,
    "book": {
        "title": "REPLACE_ME",
        "author": "俊宁",
        "publication_intent": "private-draft",
        "jurisdictions": ["CN"],
        "originality_declaration": False,
    },
    "sources": [],
    "uses": [],
    "reviews": {
        "distinctive_phrase_search": {
            "status": "pending",
            "reviewer": "",
            "date": "",
            "evidence": "",
        },
        "copyright_review": {
            "status": "pending",
            "reviewer": "",
            "date": "",
            "evidence": "",
        },
        "open_source_license_review": {
            "status": "pending",
            "reviewer": "",
            "date": "",
            "evidence": "",
        },
    },
}


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    context: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "context": self.context,
        }


def add(
    findings: list[Finding],
    severity: str,
    code: str,
    message: str,
    **context: Any,
) -> None:
    findings.append(Finding(severity, code, message, context))


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require_text(
    obj: dict[str, Any],
    key: str,
    findings: list[Finding],
    location: str,
) -> None:
    if not nonempty(obj.get(key)):
        add(findings, "block", "missing-field", f"Missing {location}.{key}")


def nonempty_string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(nonempty(item) for item in value)


def is_github_locator(value: Any) -> bool:
    if not nonempty(value):
        return False
    return bool(
        re.match(
            r"^https?://(?:www\.)?(?:github\.com|raw\.githubusercontent\.com)/",
            value.strip(),
            flags=re.IGNORECASE,
        )
    )


def is_http_locator(value: Any) -> bool:
    return nonempty(value) and bool(re.match(r"^https?://[^/]+/", value.strip()))


def valid_commit_sha(value: Any) -> bool:
    return nonempty(value) and bool(re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", value.strip()))


def path_is_in_scope(path: str, scopes: list[str]) -> bool:
    normalized_path = path.strip().lstrip("./")
    for raw_scope in scopes:
        scope = raw_scope.strip()
        if scope in {".", "./", "*"}:
            return True
        normalized_scope = scope.lstrip("./").rstrip("/")
        if normalized_path == normalized_scope or normalized_path.startswith(f"{normalized_scope}/"):
            return True
    return False


def validate_repository_source(
    source: dict[str, Any],
    source_id: str,
    location: str,
    source_uses: list[dict[str, Any]],
    findings: list[Finding],
    release_mode: bool,
) -> None:
    expressive_use = any(use.get("kind") in EXPRESSIVE_USE_KINDS for use in source_uses)
    if expressive_use:
        require_text(source, "repository_url", findings, location)
    repository_url = source.get("repository_url") or source.get("locator")
    if not is_http_locator(repository_url):
        add(
            findings,
            "block",
            "repository-url",
            f"Source {source_id} needs a canonical repository URL",
        )

    commit_sha = source.get("commit_sha")
    if not expressive_use:
        if nonempty(commit_sha) and not valid_commit_sha(commit_sha):
            add(
                findings,
                "block",
                "repository-commit",
                f"Source {source_id} has an invalid optional commit SHA",
            )
        elif valid_commit_sha(commit_sha) and commit_sha.lower() not in str(source.get("locator", "")).lower():
            add(
                findings,
                "block",
                "mutable-repository-locator",
                f"Source {source_id} records a commit but its locator is not pinned to it",
            )
        return

    require_text(source, "commit_sha", findings, location)
    require_text(source, "license_status", findings, location)
    if not valid_commit_sha(commit_sha):
        add(
            findings,
            "block",
            "repository-commit",
            f"Source {source_id} needs a full 40- or 64-character commit SHA",
        )
    elif commit_sha.lower() not in str(source.get("locator", "")).lower():
        add(
            findings,
            "block",
            "mutable-repository-locator",
            f"Source {source_id} locator is not pinned to its recorded commit",
        )

    path_scope = source.get("path_scope")
    if not nonempty_string_list(path_scope):
        add(
            findings,
            "block",
            "repository-path-scope",
            f"Source {source_id} needs a non-empty path_scope",
        )

    license_status = source.get("license_status")
    if license_status not in REPOSITORY_LICENSE_STATUSES:
        add(
            findings,
            "block",
            "repository-license-status",
            f"Source {source_id} has an invalid license_status",
        )

    basis = source.get("rights_basis")
    if license_status in {"none", "unclear"} and basis not in {"facts-ideas-only", "unknown"}:
        add(
            findings,
            "block",
            "repository-license-mismatch",
            f"Source {source_id} cannot claim reusable expression with {license_status} license status",
        )
    if license_status in {"open-license", "multiple", "custom"}:
        require_text(source, "license_expression", findings, location)
        if not nonempty_string_list(source.get("license_evidence")):
            add(
                findings,
                "block",
                "repository-license-evidence",
                f"Source {source_id} needs path-scoped license evidence",
            )
        expression = str(source.get("license_expression", "")).upper()
        if expression in {"NONE", "NOASSERTION"}:
            add(
                findings,
                "block",
                "repository-license-expression",
                f"Source {source_id} has no usable license expression",
            )

    review = source.get("license_review")
    validate_review(f"{source_id}.license_review", review, findings, release_mode)
    if isinstance(review, dict) and not isinstance(review.get("obligations"), list):
        add(
            findings,
            "block" if release_mode else "review",
            "repository-obligations-missing",
            f"Source {source_id} license review must record an obligations list",
        )
    elif isinstance(review, dict) and not all(nonempty(item) for item in review.get("obligations", [])):
        add(
            findings,
            "block",
            "repository-obligations-invalid",
            f"Source {source_id} license obligations must be non-empty strings",
        )


def validate_repository_use(
    use: dict[str, Any],
    source: dict[str, Any],
    location: str,
    findings: list[Finding],
    release_mode: bool,
) -> None:
    kind = use.get("kind")
    if kind not in EXPRESSIVE_USE_KINDS:
        permalink = use.get("source_permalink")
        commit_sha = source.get("commit_sha")
        if nonempty(permalink) and valid_commit_sha(commit_sha):
            if commit_sha.lower() not in permalink.lower():
                add(
                    findings,
                    "block",
                    "mutable-source-permalink",
                    f"{location} source_permalink is not pinned to the recorded commit",
                )
        return

    for key in ("material_type", "source_path", "source_permalink"):
        require_text(use, key, findings, location)

    material_type = use.get("material_type")
    if material_type not in REPOSITORY_MATERIAL_TYPES:
        add(findings, "block", "repository-material-type", f"Invalid material_type in {location}")

    source_path = use.get("source_path")
    scopes = source.get("path_scope")
    if nonempty(source_path) and nonempty_string_list(scopes) and not path_is_in_scope(source_path, scopes):
        add(
            findings,
            "block",
            "repository-use-out-of-scope",
            f"{location} source_path is outside the cleared path_scope",
        )

    permalink = use.get("source_permalink")
    commit_sha = source.get("commit_sha")
    if nonempty(permalink) and valid_commit_sha(commit_sha):
        if commit_sha.lower() not in permalink.lower():
            add(
                findings,
                "block",
                "mutable-source-permalink",
                f"{location} source_permalink is not pinned to the recorded commit",
            )

    require_text(use, "attribution", findings, location)
    if kind == "adapt" and use.get("modified") is not True:
        add(findings, "block", "adaptation-not-marked", f"{location} must mark modified as true")

    review = source.get("license_review")
    obligations = review.get("obligations", []) if isinstance(review, dict) else []
    compliance = use.get("compliance_evidence")
    if obligations and not isinstance(compliance, dict):
        add(
            findings,
            "block" if release_mode else "review",
            "repository-compliance-missing",
            f"{location} lacks compliance_evidence for repository license obligations",
        )
    elif isinstance(compliance, dict):
        for obligation in obligations:
            if nonempty(obligation) and not nonempty(compliance.get(obligation)):
                add(
                    findings,
                    "block" if release_mode else "review",
                    "repository-obligation-unsatisfied",
                    f"{location} lacks evidence for obligation {obligation}",
                )

    if material_type in NON_CODE_MATERIAL_TYPES:
        require_text(use, "material_rights_evidence", findings, location)
    if material_type == "logo-trademark":
        validate_review(
            f"{location}.trademark_review",
            use.get("trademark_review"),
            findings,
            release_mode,
        )


def manuscript_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path] if path.suffix.lower() in TEXT_SUFFIXES else []
    if path.is_dir():
        return sorted(
            p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES
        )
    return []


def read_texts(paths: Iterable[Path]) -> str:
    parts: list[str] = []
    for path in paths:
        parts.append(path.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


def normalize_chars(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    return "".join(ch for ch in text if ch.isalnum() or "\u3400" <= ch <= "\u9fff")


def normalize_words(text: str) -> list[str]:
    text = unicodedata.normalize("NFKC", text).lower()
    return re.findall(r"[^\W_]+", text, flags=re.UNICODE)


def contains_cjk(text: str) -> bool:
    return any("\u3400" <= ch <= "\u9fff" for ch in text)


def windows(sequence: Any, size: int) -> Iterable[Any]:
    for index in range(0, max(0, len(sequence) - size + 1)):
        yield sequence[index : index + size]


def logged_quote_sets(uses: list[dict[str, Any]], source_id: str) -> tuple[list[str], list[str]]:
    char_quotes: list[str] = []
    word_quotes: list[str] = []
    for use in uses:
        if use.get("source_id") != source_id or use.get("kind") != "quote":
            continue
        excerpt = use.get("excerpt")
        if nonempty(excerpt):
            char_quotes.append(normalize_chars(excerpt))
            word_quotes.append(" ".join(normalize_words(excerpt)))
    return char_quotes, word_quotes


def overlap_findings(
    manuscript: str,
    source_text: str,
    source_id: str,
    uses: list[dict[str, Any]],
    char_threshold: int,
    word_threshold: int,
    limit: int = 5,
) -> list[str]:
    char_quotes, word_quotes = logged_quote_sets(uses, source_id)
    matches: list[str] = []

    if contains_cjk(source_text) or contains_cjk(manuscript):
        manuscript_chars = normalize_chars(manuscript)
        source_chars = normalize_chars(source_text)
        if len(manuscript_chars) >= char_threshold and len(source_chars) >= char_threshold:
            source_windows = set(windows(source_chars, char_threshold))
            seen: set[str] = set()
            for chunk in windows(manuscript_chars, char_threshold):
                if chunk in source_windows and chunk not in seen:
                    seen.add(chunk)
                    if not any(chunk in quote for quote in char_quotes):
                        matches.append(chunk)
                        if len(matches) >= limit:
                            return matches

    manuscript_words = normalize_words(manuscript)
    source_words = normalize_words(source_text)
    if len(manuscript_words) >= word_threshold and len(source_words) >= word_threshold:
        source_windows = {tuple(chunk) for chunk in windows(source_words, word_threshold)}
        seen_words: set[tuple[str, ...]] = set()
        for chunk_list in windows(manuscript_words, word_threshold):
            chunk = tuple(chunk_list)
            if chunk in source_windows and chunk not in seen_words:
                seen_words.add(chunk)
                phrase = " ".join(chunk)
                if not any(phrase in quote for quote in word_quotes):
                    matches.append(phrase)
                    if len(matches) >= limit:
                        return matches
    return matches


def validate_review(
    name: str,
    review: Any,
    findings: list[Finding],
    release_mode: bool,
) -> None:
    severity = "block" if release_mode else "review"
    if not isinstance(review, dict) or review.get("status") != "passed":
        add(findings, severity, "review-not-passed", f"Review {name} has not passed")
        return
    for key in ("reviewer", "date", "evidence"):
        if not nonempty(review.get(key)):
            add(findings, severity, "review-evidence-missing", f"Review {name} lacks {key}")


def validate_ledger(
    ledger: dict[str, Any],
    ledger_path: Path,
    manuscript: str,
    char_threshold: int,
    word_threshold: int,
) -> list[Finding]:
    findings: list[Finding] = []
    if ledger.get("schema_version") != 1:
        add(findings, "block", "schema-version", "schema_version must equal 1")

    book = ledger.get("book")
    if not isinstance(book, dict):
        add(findings, "block", "missing-book", "Ledger must contain a book object")
        book = {}
    for key in ("title", "author", "publication_intent"):
        require_text(book, key, findings, "book")
    jurisdictions = book.get("jurisdictions")
    if not isinstance(jurisdictions, list) or not jurisdictions or not all(nonempty(x) for x in jurisdictions):
        add(findings, "block", "jurisdictions", "book.jurisdictions must be a non-empty string list")
    if book.get("originality_declaration") is not True:
        add(findings, "block", "originality-declaration", "Originality declaration must be true")

    intent = book.get("publication_intent")
    release_mode = intent in PUBLIC_INTENTS
    sources = ledger.get("sources")
    uses = ledger.get("uses")
    reviews = ledger.get("reviews")
    if not isinstance(sources, list):
        add(findings, "block", "sources-type", "sources must be a list")
        sources = []
    if not isinstance(uses, list):
        add(findings, "block", "uses-type", "uses must be a list")
        uses = []
    if not isinstance(reviews, dict):
        reviews = {}

    source_uses_by_id: dict[str, list[dict[str, Any]]] = {}
    for raw_use in uses:
        if isinstance(raw_use, dict) and nonempty(raw_use.get("source_id")):
            source_uses_by_id.setdefault(raw_use["source_id"], []).append(raw_use)

    source_map: dict[str, dict[str, Any]] = {}
    repository_source_ids: set[str] = set()
    repository_expressive_source_ids: set[str] = set()
    for index, raw_source in enumerate(sources):
        location = f"sources[{index}]"
        if not isinstance(raw_source, dict):
            add(findings, "block", "source-type", f"{location} must be an object")
            continue
        source = raw_source
        for key in ("id", "title", "creator", "locator", "rights_basis", "rights_status", "proof"):
            require_text(source, key, findings, location)
        source_id = source.get("id")
        if not nonempty(source_id):
            continue
        if source_id in source_map:
            add(findings, "block", "duplicate-source", f"Duplicate source id {source_id}")
        source_map[source_id] = source

        basis = source.get("rights_basis")
        if basis not in RIGHTS_BASES:
            add(findings, "block", "rights-basis", f"Invalid rights basis for {source_id}")
        if basis == "unknown":
            add(findings, "block", "unknown-rights", f"Source {source_id} has unknown rights")
        if source.get("rights_status") != "cleared":
            add(findings, "block", "rights-not-cleared", f"Source {source_id} is not cleared")

        allowed = source.get("allowed_uses")
        if basis not in {"facts-ideas-only", "unknown"} and (
            not isinstance(allowed, list) or not allowed
        ):
            add(findings, "block", "allowed-uses", f"Source {source_id} needs allowed_uses")
        if basis in {"licensed", "open-license"} and not (
            nonempty(source.get("license")) or nonempty(source.get("license_expression"))
        ):
            add(findings, "block", "license-missing", f"Source {source_id} needs exact license terms")
        if basis == "public-domain":
            if not nonempty(source.get("public_domain_reason")):
                add(findings, "block", "public-domain-reason", f"Source {source_id} needs public_domain_reason")
            pd_jurisdictions = source.get("jurisdictions")
            if not isinstance(pd_jurisdictions, list) or not pd_jurisdictions:
                add(findings, "block", "public-domain-jurisdiction", f"Source {source_id} needs jurisdictions")
        if basis == "statutory-exception" and not nonempty(source.get("legal_basis")):
            add(findings, "block", "legal-basis", f"Source {source_id} needs legal_basis")

        repository_source = source.get("source_type") == "software-repository"
        if is_github_locator(source.get("locator")) and not repository_source:
            repository_source = True
        if repository_source:
            repository_source_ids.add(source_id)
            source_uses = source_uses_by_id.get(source_id, [])
            if any(use.get("kind") in EXPRESSIVE_USE_KINDS for use in source_uses):
                repository_expressive_source_ids.add(source_id)
            validate_repository_source(
                source,
                source_id,
                location,
                source_uses,
                findings,
                release_mode,
            )

    for index, raw_use in enumerate(uses):
        location = f"uses[{index}]"
        if not isinstance(raw_use, dict):
            add(findings, "block", "use-type", f"{location} must be an object")
            continue
        use = raw_use
        for key in ("source_id", "kind", "manuscript_location", "purpose"):
            require_text(use, key, findings, location)
        source_id = use.get("source_id")
        kind = use.get("kind")
        if kind not in USE_KINDS:
            add(findings, "block", "use-kind", f"Invalid use kind in {location}")
        source = source_map.get(source_id)
        if source is None:
            add(findings, "block", "unknown-source-id", f"{location} refers to unknown source {source_id}")
            continue
        basis = source.get("rights_basis")
        allowed = source.get("allowed_uses", [])
        if basis == "facts-ideas-only" and kind not in {"facts-ideas", "reference"}:
            add(findings, "block", "facts-only-overreach", f"{location} exceeds facts-ideas-only basis")
        elif isinstance(allowed, list) and allowed and kind not in allowed:
            add(findings, "block", "use-not-permitted", f"{location} kind {kind} is not permitted")
        if kind == "quote":
            require_text(use, "excerpt", findings, location)
            require_text(use, "attribution", findings, location)
        if kind in {"adapt", "translate", "reproduce"} and basis in {
            "facts-ideas-only",
            "statutory-exception",
            "unknown",
        }:
            add(findings, "block", "derivative-rights", f"{location} lacks express derivative rights")
        if source_id in repository_source_ids:
            validate_repository_use(use, source, location, findings, release_mode)

    for source_id, source in source_map.items():
        source_text_path = source.get("source_text_path")
        expressive_uses = [
            use
            for use in uses
            if isinstance(use, dict)
            and use.get("source_id") == source_id
            and use.get("kind") in EXPRESSIVE_USE_KINDS
        ]
        if expressive_uses and not nonempty(source_text_path):
            add(
                findings,
                "block" if release_mode else "review",
                "comparison-text-missing",
                f"Source {source_id} has expressive uses but no lawful local comparison text",
            )
            continue
        if not nonempty(source_text_path):
            continue
        resolved = (ledger_path.parent / source_text_path).resolve()
        if not resolved.is_file():
            add(findings, "block", "source-text-missing", f"Local source text missing for {source_id}", path=str(resolved))
            continue
        source_text = resolved.read_text(encoding="utf-8", errors="replace")
        matches = overlap_findings(
            manuscript,
            source_text,
            source_id,
            [u for u in uses if isinstance(u, dict)],
            char_threshold,
            word_threshold,
        )
        for match in matches:
            add(
                findings,
                "block",
                "unlogged-overlap",
                f"Unlogged exact overlap with source {source_id}",
                excerpt=match,
            )

    validate_review(
        "distinctive_phrase_search",
        reviews.get("distinctive_phrase_search"),
        findings,
        release_mode,
    )
    validate_review(
        "copyright_review",
        reviews.get("copyright_review"),
        findings,
        release_mode,
    )
    if repository_expressive_source_ids:
        validate_review(
            "open_source_license_review",
            reviews.get("open_source_license_review"),
            findings,
            release_mode,
        )
    return findings


def report_status(findings: list[Finding]) -> str:
    if any(item.severity == "block" for item in findings):
        return "BLOCK"
    if any(item.severity == "review" for item in findings):
        return "NEEDS_REVIEW"
    return "PASS"


def build_report(
    status: str,
    manuscript_path: Path,
    ledger_path: Path,
    manuscript: str,
    findings: list[Finding],
) -> dict[str, Any]:
    return {
        "status": status,
        "checked_at": date.today().isoformat(),
        "manuscript_path": str(manuscript_path.resolve()),
        "manuscript_sha256": hashlib.sha256(manuscript.encode("utf-8")).hexdigest(),
        "ledger_path": str(ledger_path.resolve()),
        "finding_counts": {
            "block": sum(item.severity == "block" for item in findings),
            "review": sum(item.severity == "review" for item in findings),
        },
        "findings": [item.as_dict() for item in findings],
        "limitations": [
            "Exact-overlap checks cover only local source_text_path files in the ledger.",
            "Repository checks validate recorded evidence and obligations, not every file or license interpretation in the upstream project.",
            "A PASS records process evidence; it is not a legal opinion or non-infringement guarantee.",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", nargs="?", type=Path)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--write-template", type=Path)
    parser.add_argument("--min-match-chars", type=int, default=50)
    parser.add_argument("--min-match-words", type=int, default=14)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.write_template:
        path: Path = args.write_template
        if path.exists():
            print(f"Refusing to overwrite existing file: {path}", file=sys.stderr)
            return 1
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(TEMPLATE, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote ledger template: {path}")
        return 0

    if args.manuscript is None or args.ledger is None:
        print("manuscript and --ledger are required", file=sys.stderr)
        return 1
    if args.min_match_chars < 20 or args.min_match_words < 6:
        print("Similarity thresholds are too low for useful exact-match review", file=sys.stderr)
        return 1

    files = manuscript_files(args.manuscript)
    if not files:
        print(f"No Markdown or text manuscript files found: {args.manuscript}", file=sys.stderr)
        return 1
    try:
        ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot read ledger: {exc}", file=sys.stderr)
        return 1
    if not isinstance(ledger, dict):
        print("Ledger root must be a JSON object", file=sys.stderr)
        return 1

    manuscript = read_texts(files)
    findings = validate_ledger(
        ledger,
        args.ledger,
        manuscript,
        args.min_match_chars,
        args.min_match_words,
    )
    status = report_status(findings)
    report = build_report(status, args.manuscript, args.ledger, manuscript, findings)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return {"PASS": 0, "BLOCK": 2, "NEEDS_REVIEW": 3}[status]


if __name__ == "__main__":
    raise SystemExit(main())
