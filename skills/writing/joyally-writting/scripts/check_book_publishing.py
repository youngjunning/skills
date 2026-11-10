#!/usr/bin/env python3
"""Deterministic preflight and evidence gate for publisher-facing books."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote, urlparse


EXIT_PASS = 0
EXIT_ERROR = 1
EXIT_BLOCK = 2
EXIT_NEEDS_REVIEW = 3

BLOCK = "BLOCK"
NEEDS_REVIEW = "NEEDS_REVIEW"

DEFAULT_COLLOQUIAL_TERMS = [
    "说白了",
    "搞定",
    "神器",
    "炸裂",
    "秒杀",
    "一把梭",
    "翻车",
    "跑偏",
    "你会发现",
    "看起来像",
    "真正执行时却",
]

REQUIRED_REVIEWS = (
    "copyedit",
    "citations",
    "figures_tables",
    "index",
    "appendices",
    "author_material",
    "rights",
    "rendered_artifact",
)

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)]+)\)")
PLACEHOLDER_RE = re.compile(
    r"(?:\bTODO\b|\bTBD\b|\bFIXME\b|\bXXX\b|\?\?\?|待补(?:充|写|图|表|证据)?|待确认|此处补)",
    re.IGNORECASE,
)
PRONOUN_LEAD_RE = re.compile(
    r"^\s*[（(【\[]?(我(?:们)?|你(?:们)?|他(?:们)?|她(?:们)?)(?=[，,：:、\s\u4e00-\u9fff])"
)


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    file: str | None = None
    line: int | None = None


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"evidence file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("evidence root must be a JSON object")
    return data


def manuscript_files(path: Path) -> tuple[Path, list[Path]]:
    path = path.resolve()
    if path.is_file():
        if path.suffix.lower() != ".md":
            raise ValueError("manuscript file must use the .md extension")
        return path.parent, [path]
    if not path.is_dir():
        raise ValueError(f"manuscript path does not exist: {path}")
    files = sorted(candidate for candidate in path.rglob("*.md") if candidate.is_file())
    if not files:
        raise ValueError(f"no Markdown files found under {path}")
    return path, files


def manuscript_sha256(root: Path, files: Iterable[Path]) -> str:
    digest = hashlib.sha256()
    for path in files:
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def iter_markdown_lines(path: Path) -> Iterable[tuple[int, str, bool]]:
    """Yield line number, text, and whether prose checks should inspect it."""
    in_fence = False
    fence_marker: str | None = None
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = None
            yield number, line, False
            continue
        inspect_prose = not in_fence and not stripped.startswith(">") and not line.startswith("    ")
        yield number, line, inspect_prose


def parse_link_target(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        return value[1 : value.index(">")]
    return value.split(maxsplit=1)[0] if value else ""


def is_external_target(target: str) -> bool:
    parsed = urlparse(target)
    return bool(parsed.scheme) or target.startswith("//") or target.startswith("#")


def normalized_heading(text: str) -> str:
    text = re.sub(r"^\s*(?:第[一二三四五六七八九十百]+[章节部分篇]\s*|\d+(?:[.．]\d+)*[.．、]?\s*)", "", text)
    return re.sub(r"[`*_]", "", text).strip().casefold()


def inspect_markdown(
    root: Path,
    files: list[Path],
    profile: dict[str, Any],
    findings: list[Finding],
) -> None:
    max_heading_depth = profile.get("max_heading_depth", 4)
    if not isinstance(max_heading_depth, int) or not 1 <= max_heading_depth <= 6:
        findings.append(Finding(BLOCK, "invalid_max_heading_depth", "max_heading_depth must be an integer from 1 to 6"))
        max_heading_depth = 6
    allow_jumps = bool(profile.get("allow_heading_level_skips", False))
    required_sections = profile.get("required_sections", [])
    if not isinstance(required_sections, list) or not all(isinstance(item, str) for item in required_sections):
        findings.append(Finding(BLOCK, "invalid_required_sections", "required_sections must be an array of strings"))
        required_sections = []
    extra_terms = profile.get("colloquial_terms", [])
    if not isinstance(extra_terms, list) or not all(isinstance(item, str) for item in extra_terms):
        findings.append(Finding(BLOCK, "invalid_colloquial_terms", "colloquial_terms must be an array of strings"))
        extra_terms = []
    colloquial_terms = list(dict.fromkeys(DEFAULT_COLLOQUIAL_TERMS + extra_terms))
    observed_headings: set[str] = set()

    for path in files:
        relative = path.relative_to(root).as_posix()
        previous_level: int | None = None
        for number, line, inspect_prose in iter_markdown_lines(path):
            stripped = line.strip()
            heading_match = HEADING_RE.match(stripped)
            if heading_match:
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()
                observed_headings.add(normalized_heading(title))
                if level > max_heading_depth:
                    findings.append(Finding(BLOCK, "heading_too_deep", f"heading level H{level} exceeds configured H{max_heading_depth}", relative, number))
                if previous_level is not None and level > previous_level + 1 and not allow_jumps:
                    findings.append(Finding(BLOCK, "heading_level_jump", f"heading jumps from H{previous_level} to H{level}", relative, number))
                previous_level = level

            if not inspect_prose:
                continue
            if PLACEHOLDER_RE.search(line):
                findings.append(Finding(BLOCK, "unresolved_placeholder", "unresolved placeholder remains in reader-facing prose", relative, number))
            matched_terms = [term for term in colloquial_terms if term and term in line]
            if matched_terms:
                findings.append(Finding(NEEDS_REVIEW, "colloquial_narration", f"review possible colloquial narration: {', '.join(matched_terms)}", relative, number))
            pronoun_match = PRONOUN_LEAD_RE.match(line)
            if pronoun_match:
                findings.append(Finding(NEEDS_REVIEW, "pronoun_led_framing", f"review sentence or paragraph led by personal pronoun: {pronoun_match.group(1)}", relative, number))

            for link_match in LINK_RE.finditer(line):
                is_image = bool(link_match.group(1))
                alt_or_label = link_match.group(2).strip()
                target = parse_link_target(link_match.group(3))
                if is_image and not alt_or_label:
                    findings.append(Finding(NEEDS_REVIEW, "empty_image_alt", "image has empty alt text", relative, number))
                if not target or is_external_target(target):
                    continue
                local_part = unquote(target.split("#", 1)[0].split("?", 1)[0])
                if not local_part:
                    continue
                resolved = (path.parent / local_part).resolve()
                if not resolved.is_file():
                    findings.append(Finding(BLOCK, "missing_local_asset", f"local link target does not exist: {target}", relative, number))

    for section in required_sections:
        if normalized_heading(section) not in observed_headings:
            findings.append(Finding(BLOCK, "missing_required_section", f"required section is missing: {section}"))


def validate_publisher_evidence(evidence: dict[str, Any], findings: list[Finding]) -> dict[str, Any]:
    publisher = evidence.get("publisher_requirements")
    if not isinstance(publisher, dict):
        findings.append(Finding(NEEDS_REVIEW, "missing_publisher_requirements", "publisher requirement evidence is missing"))
        return {}
    status = publisher.get("status")
    if status != "verified":
        findings.append(Finding(NEEDS_REVIEW, "publisher_requirements_not_verified", "publisher requirements are missing or provisional"))
    else:
        for field in ("source", "version", "verified_at", "reviewer"):
            if not str(publisher.get(field, "")).strip():
                findings.append(Finding(NEEDS_REVIEW, "incomplete_publisher_requirements", f"verified publisher requirements lack {field}"))
    return publisher


def validate_review_evidence(evidence: dict[str, Any], profile: dict[str, Any], findings: list[Finding]) -> None:
    reviews = evidence.get("reviews")
    if not isinstance(reviews, dict):
        findings.append(Finding(NEEDS_REVIEW, "missing_reviews", "manual review evidence is missing"))
        return

    for name in REQUIRED_REVIEWS:
        review = reviews.get(name)
        if not isinstance(review, dict):
            findings.append(Finding(NEEDS_REVIEW, "missing_review", f"required review evidence is missing: {name}"))
            continue
        status = review.get("status")
        if status == "pass":
            for field in ("reviewer", "date", "scope"):
                if not str(review.get(field, "")).strip():
                    findings.append(Finding(NEEDS_REVIEW, "incomplete_review", f"{name} review marked pass but lacks {field}"))
        elif status == "not_applicable":
            if not str(review.get("reason", "")).strip():
                findings.append(Finding(NEEDS_REVIEW, "unjustified_not_applicable", f"{name} review lacks a reason for not_applicable"))
        elif status == "block":
            findings.append(Finding(BLOCK, "manual_review_block", f"manual review is blocked: {name}"))
        else:
            findings.append(Finding(NEEDS_REVIEW, "manual_review_unresolved", f"manual review is not passed: {name}"))

    threshold = profile.get("max_error_rate_per_10000")
    if threshold is None and profile.get("jurisdiction") == "mainland-cn":
        threshold = 1.0
    if threshold is not None:
        if not isinstance(threshold, (int, float)) or threshold < 0:
            findings.append(Finding(BLOCK, "invalid_error_rate_threshold", "max_error_rate_per_10000 must be a non-negative number"))
            return
        copyedit = reviews.get("copyedit", {})
        rate = copyedit.get("error_rate_per_10000") if isinstance(copyedit, dict) else None
        if not isinstance(rate, (int, float)):
            findings.append(Finding(NEEDS_REVIEW, "missing_copyedit_error_rate", "copyedit review lacks a professional error rate"))
        elif rate > threshold:
            findings.append(Finding(BLOCK, "copyedit_error_rate_exceeded", f"copyedit error rate {rate}/10000 exceeds configured {threshold}/10000"))


def evidence_template(manuscript_hash: str) -> dict[str, Any]:
    empty_review = {"status": "needs_review", "reviewer": "", "date": "", "scope": ""}
    return {
        "schema_version": 1,
        "manuscript_sha256": manuscript_hash,
        "publisher_requirements": {
            "status": "provisional",
            "publisher": "",
            "imprint": "",
            "edition": "",
            "mediums": [],
            "source": "",
            "version": "",
            "verified_at": "",
            "reviewer": "",
        },
        "profile": {
            "jurisdiction": "mainland-cn",
            "max_heading_depth": 4,
            "allow_heading_level_skips": False,
            "required_sections": [],
            "colloquial_terms": [],
            "max_error_rate_per_10000": 1.0,
        },
        "reviews": {name: dict(empty_review) for name in REQUIRED_REVIEWS},
    }


def result_status(findings: list[Finding]) -> tuple[str, int]:
    if any(item.severity == BLOCK for item in findings):
        return BLOCK, EXIT_BLOCK
    if any(item.severity == NEEDS_REVIEW for item in findings):
        return NEEDS_REVIEW, EXIT_NEEDS_REVIEW
    return "PASS", EXIT_PASS


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path, help="Markdown file or directory")
    parser.add_argument("--evidence", type=Path, help="publishing evidence JSON")
    parser.add_argument("--report", type=Path, help="write JSON report")
    parser.add_argument("--write-template", type=Path, help="write an evidence template and exit")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        root, files = manuscript_files(args.manuscript)
        digest = manuscript_sha256(root, files)
        if args.write_template:
            write_json(args.write_template, evidence_template(digest))
            print(f"WROTE {args.write_template}")
            return EXIT_PASS
        if not args.evidence:
            raise ValueError("--evidence is required unless --write-template is used")

        evidence = load_json(args.evidence)
        findings: list[Finding] = []
        bound_hash = evidence.get("manuscript_sha256")
        if not bound_hash:
            findings.append(Finding(NEEDS_REVIEW, "missing_manuscript_hash", "evidence is not bound to a manuscript hash"))
        elif bound_hash != digest:
            findings.append(Finding(BLOCK, "manuscript_hash_mismatch", "evidence belongs to a different manuscript version"))

        profile = evidence.get("profile")
        if not isinstance(profile, dict):
            findings.append(Finding(BLOCK, "invalid_profile", "profile must be a JSON object"))
            profile = {}
        validate_publisher_evidence(evidence, findings)
        inspect_markdown(root, files, profile, findings)
        validate_review_evidence(evidence, profile, findings)
        status, exit_code = result_status(findings)
        report = {
            "status": status,
            "manuscript_sha256": digest,
            "files": [path.relative_to(root).as_posix() for path in files],
            "summary": {
                "block": sum(item.severity == BLOCK for item in findings),
                "needs_review": sum(item.severity == NEEDS_REVIEW for item in findings),
            },
            "findings": [asdict(item) for item in findings],
        }
        if args.report:
            write_json(args.report, report)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return exit_code
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
