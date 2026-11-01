#!/usr/bin/env python3
"""Deterministic similarity gate for book manuscripts.

The local scan detects repeated manuscript passages and exact or near overlap
with comparison texts recorded in a copyright ledger. Web discovery is opt-in
through a SearchProvider and produces review candidates, not legal conclusions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Callable, Iterable, Protocol


TEXT_SUFFIXES = {".md", ".markdown", ".txt"}
CLEARABLE_DECISIONS = {"false-positive", "intentional", "resolved"}


@dataclass(frozen=True)
class Paragraph:
    location: str
    text: str
    normalized: str


@dataclass(frozen=True)
class WebResult:
    url: str
    title: str
    snippet: str


class SearchProvider(Protocol):
    name: str

    def search(self, query: str) -> list[WebResult]: ...


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    context: dict[str, Any] = field(default_factory=dict)
    decision: dict[str, Any] | None = None

    @property
    def finding_id(self) -> str:
        payload = json.dumps(
            {"code": self.code, "context": self.context},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(payload.encode()).hexdigest()[:20]

    def as_dict(self) -> dict[str, Any]:
        result = {
            "id": self.finding_id,
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "context": self.context,
        }
        if self.decision is not None:
            result["decision"] = self.decision
        return result


class BraveSearchProvider:
    name = "brave"
    endpoint = "https://api.search.brave.com/res/v1/web/search"

    def __init__(
        self,
        api_key: str,
        *,
        opener: Callable[..., Any] = urllib.request.urlopen,
        timeout: int = 20,
    ) -> None:
        if not api_key.strip():
            raise ValueError("Brave Search API key is empty")
        self.api_key = api_key
        self.opener = opener
        self.timeout = timeout

    def search(self, query: str) -> list[WebResult]:
        parameters = urllib.parse.urlencode(
            {
                "q": query[:400],
                "count": 10,
                "safesearch": "moderate",
            }
        )
        request = urllib.request.Request(
            f"{self.endpoint}?{parameters}",
            headers={
                "Accept": "application/json",
                "User-Agent": "writting-skill-similarity-gate/1",
                "X-Subscription-Token": self.api_key,
            },
        )
        with self.opener(request, timeout=self.timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
        raw_results = payload.get("web", {}).get("results", [])
        results: list[WebResult] = []
        for raw in raw_results:
            if not isinstance(raw, dict) or not isinstance(raw.get("url"), str):
                continue
            results.append(
                WebResult(
                    url=raw["url"],
                    title=str(raw.get("title", "")),
                    snippet=str(raw.get("description", "")),
                )
            )
        return results


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    return "".join(ch for ch in text if ch.isalnum() or "\u3400" <= ch <= "\u9fff")


def clean_markdown(text: str) -> str:
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<https?://[^>]+>", "", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"^\s{0,3}(?:[-*+] |\d+[.)] |> )", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_~]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def manuscript_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path] if path.suffix.lower() in TEXT_SUFFIXES else []
    if path.is_dir():
        return sorted(
            item
            for item in path.rglob("*")
            if item.is_file() and item.suffix.lower() in TEXT_SUFFIXES
        )
    return []


def extract_paragraphs(path: Path, root: Path, min_chars: int) -> list[Paragraph]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    relative = path.relative_to(root).as_posix() if path != root else path.name
    paragraphs: list[Paragraph] = []
    buffer: list[str] = []
    start_line = 1
    in_fence = False
    in_frontmatter = bool(lines and lines[0].strip() == "---")

    def flush() -> None:
        nonlocal buffer
        if not buffer:
            return
        cleaned = clean_markdown("\n".join(buffer))
        normalized = normalize_text(cleaned)
        if len(normalized) >= min_chars:
            paragraphs.append(Paragraph(f"{relative}:{start_line}", cleaned, normalized))
        buffer = []

    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if in_frontmatter:
            if index > 1 and stripped == "---":
                in_frontmatter = False
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        structural = (
            not stripped
            or stripped.startswith("#")
            or bool(re.fullmatch(r"\|?\s*:?-{3,}.*", stripped))
            or (stripped.startswith("|") and stripped.endswith("|"))
            or bool(re.fullmatch(r"!\[[^\]]*\]\([^)]+\)", stripped))
        )
        if structural:
            flush()
            continue
        if not buffer:
            start_line = index
        buffer.append(line)
    flush()
    return paragraphs


def load_manuscript(path: Path, min_chars: int) -> tuple[list[Path], list[Paragraph]]:
    files = manuscript_files(path)
    root = path if path.is_dir() else path.parent
    paragraphs: list[Paragraph] = []
    for item in files:
        paragraphs.extend(extract_paragraphs(item, root, min_chars))
    return files, paragraphs


def shingles(text: str, size: int = 5) -> set[str]:
    if len(text) <= size:
        return {text} if text else set()
    return {text[index : index + size] for index in range(len(text) - size + 1)}


def similarity_scores(left: str, right: str) -> tuple[float, float]:
    sequence = SequenceMatcher(None, left, right, autojunk=False).ratio()
    left_shingles = shingles(left)
    right_shingles = shingles(right)
    union = left_shingles | right_shingles
    jaccard = len(left_shingles & right_shingles) / len(union) if union else 0.0
    return sequence, jaccard


def simhash(text: str) -> int:
    tokens = shingles(text, 4)
    weights = [0] * 64
    for token in tokens:
        digest = int.from_bytes(hashlib.sha256(token.encode()).digest()[:8], "big")
        for bit in range(64):
            weights[bit] += 1 if digest & (1 << bit) else -1
    result = 0
    for bit, weight in enumerate(weights):
        if weight >= 0:
            result |= 1 << bit
    return result


def band_keys(value: int) -> tuple[tuple[int, int], ...]:
    return tuple((band, (value >> (band * 8)) & 0xFF) for band in range(8))


def windows(text: str, size: int) -> Iterable[str]:
    for index in range(max(0, len(text) - size + 1)):
        yield text[index : index + size]


def candidate_pairs(paragraphs: list[Paragraph]) -> Iterable[tuple[int, int]]:
    buckets: dict[tuple[int, int], list[int]] = {}
    seen: set[tuple[int, int]] = set()
    for index, paragraph in enumerate(paragraphs):
        for key in band_keys(simhash(paragraph.normalized)):
            for previous in buckets.get(key, []):
                pair = (previous, index)
                if pair not in seen:
                    seen.add(pair)
                    yield pair
            buckets.setdefault(key, []).append(index)


def manuscript_findings(
    paragraphs: list[Paragraph],
    near_threshold: float,
    finding_limit: int,
) -> list[Finding]:
    findings: list[Finding] = []
    exact_groups: dict[str, list[Paragraph]] = {}
    for paragraph in paragraphs:
        exact_groups.setdefault(paragraph.normalized, []).append(paragraph)
    for group in exact_groups.values():
        if len(group) < 2:
            continue
        findings.append(
            Finding(
                "review",
                "manuscript-exact-duplicate",
                "A long passage is repeated inside the manuscript",
                {
                    "locations": [item.location for item in group],
                    "excerpt": group[0].text[:240],
                },
            )
        )
        if len(findings) >= finding_limit:
            return findings

    exact_pairs = {
        tuple(sorted((group[0].location, item.location)))
        for group in exact_groups.values()
        if len(group) > 1
        for item in group[1:]
    }
    for left_index, right_index in candidate_pairs(paragraphs):
        left = paragraphs[left_index]
        right = paragraphs[right_index]
        if left.normalized == right.normalized:
            continue
        location_pair = tuple(sorted((left.location, right.location)))
        if location_pair in exact_pairs:
            continue
        sequence, jaccard = similarity_scores(left.normalized, right.normalized)
        if sequence < near_threshold or jaccard < max(0.50, near_threshold - 0.25):
            continue
        findings.append(
            Finding(
                "review",
                "manuscript-near-duplicate",
                "Two manuscript passages are highly similar",
                {
                    "locations": [left.location, right.location],
                    "sequence_ratio": round(sequence, 4),
                    "shingle_jaccard": round(jaccard, 4),
                    "left_excerpt": left.text[:200],
                    "right_excerpt": right.text[:200],
                },
            )
        )
        if len(findings) >= finding_limit:
            break
    return findings


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def logged_excerpts(ledger: dict[str, Any], source_id: str) -> list[str]:
    excerpts: list[str] = []
    for use in ledger.get("uses", []):
        if not isinstance(use, dict) or use.get("source_id") != source_id:
            continue
        if use.get("kind") not in {"quote", "reproduce", "adapt", "translate"}:
            continue
        excerpt = use.get("excerpt")
        if isinstance(excerpt, str) and normalize_text(excerpt):
            excerpts.append(normalize_text(excerpt))
    return excerpts


def covered_by_logged_use(text: str, excerpts: list[str]) -> bool:
    return any(text in excerpt for excerpt in excerpts)


def source_findings(
    paragraphs: list[Paragraph],
    ledger_path: Path,
    source_exact_chars: int,
    source_near_threshold: float,
    finding_limit: int,
) -> list[Finding]:
    ledger = read_json(ledger_path)
    findings: list[Finding] = []
    for source in ledger.get("sources", []):
        if not isinstance(source, dict) or not isinstance(source.get("source_text_path"), str):
            continue
        source_id = str(source.get("id", "unknown-source"))
        source_path = (ledger_path.parent / source["source_text_path"]).resolve()
        if not source_path.is_file():
            findings.append(
                Finding(
                    "block",
                    "source-text-missing",
                    "A ledger comparison text is missing",
                    {"source_id": source_id, "path": source["source_text_path"]},
                )
            )
            continue
        raw_source = source_path.read_text(encoding="utf-8", errors="replace")
        normalized_source = normalize_text(raw_source)
        exact_source_windows = set(windows(normalized_source, source_exact_chars))
        source_blocks = [
            normalize_text(clean_markdown(block))
            for block in re.split(r"\n\s*\n", raw_source)
        ]
        source_blocks = [block for block in source_blocks if len(block) >= 40]
        block_buckets: dict[tuple[int, int], list[str]] = {}
        for block in source_blocks:
            for key in band_keys(simhash(block)):
                block_buckets.setdefault(key, []).append(block)
        excerpts = logged_excerpts(ledger, source_id)

        for paragraph in paragraphs:
            exact_match = next(
                (
                    chunk
                    for chunk in windows(paragraph.normalized, source_exact_chars)
                    if chunk in exact_source_windows
                    and not covered_by_logged_use(chunk, excerpts)
                ),
                None,
            )
            if exact_match is not None:
                findings.append(
                    Finding(
                        "block",
                        "unlogged-source-overlap",
                        "A manuscript passage exactly overlaps a ledger comparison source without a logged use",
                        {
                            "source_id": source_id,
                            "manuscript_location": paragraph.location,
                            "matched_normalized_text": exact_match,
                            "excerpt": paragraph.text[:240],
                        },
                    )
                )
                if len(findings) >= finding_limit:
                    return findings
                continue

            comparison_text = paragraph.normalized
            for excerpt in excerpts:
                comparison_text = comparison_text.replace(excerpt, "")
            if len(comparison_text) < 40:
                continue

            candidates: set[str] = set()
            for key in band_keys(simhash(comparison_text)):
                candidates.update(block_buckets.get(key, []))
            best: tuple[float, float, str] | None = None
            for block in candidates:
                sequence, jaccard = similarity_scores(comparison_text, block)
                if sequence < source_near_threshold or jaccard < max(
                    0.45, source_near_threshold - 0.30
                ):
                    continue
                if best is None or sequence > best[0]:
                    best = (sequence, jaccard, block)
            if best is not None:
                findings.append(
                    Finding(
                        "review",
                        "near-source-overlap",
                        "A manuscript passage is highly similar to a ledger comparison source",
                        {
                            "source_id": source_id,
                            "manuscript_location": paragraph.location,
                            "sequence_ratio": round(best[0], 4),
                            "shingle_jaccard": round(best[1], 4),
                            "manuscript_excerpt": paragraph.text[:200],
                            "source_excerpt": best[2][:200],
                        },
                    )
                )
                if len(findings) >= finding_limit:
                    return findings
    return findings


def sentence_candidates(paragraph: Paragraph) -> Iterable[str]:
    sentences = re.split(r"(?<=[。！？!?])\s+|(?<=[。！？!?])", paragraph.text)
    for sentence in sentences:
        sentence = sentence.strip()
        normalized = normalize_text(sentence)
        words = re.findall(r"[^\W_]+", sentence, flags=re.UNICODE)
        if len(normalized) >= 36 or len(words) >= 10:
            yield sentence[:220]


def distinctive_phrases(
    paragraphs: list[Paragraph],
    max_queries: int,
) -> list[tuple[str, str]]:
    ranked: list[tuple[float, str, str]] = []
    seen: set[str] = set()
    for paragraph in paragraphs:
        candidates = list(sentence_candidates(paragraph))
        if not candidates:
            candidates = [paragraph.text[:160]]
        for phrase in candidates:
            normalized = normalize_text(phrase)
            if len(normalized) < 36 or normalized in seen:
                continue
            seen.add(normalized)
            diversity = len(set(normalized)) / len(normalized)
            score = min(len(normalized), 140) + diversity * 40
            ranked.append((score, paragraph.location, phrase))
    ranked.sort(key=lambda item: (-item[0], item[1], item[2]))
    return [(location, phrase) for _, location, phrase in ranked[:max_queries]]


def domain_excluded(url: str, excluded_domains: list[str]) -> bool:
    hostname = (urllib.parse.urlparse(url).hostname or "").lower()
    return any(hostname == domain or hostname.endswith(f".{domain}") for domain in excluded_domains)


def web_findings(
    paragraphs: list[Paragraph],
    provider: SearchProvider | None,
    require_web: bool,
    max_queries: int,
    excluded_domains: list[str],
) -> tuple[list[Finding], list[dict[str, Any]]]:
    if provider is None:
        if require_web:
            return (
                [
                    Finding(
                        "block",
                        "web-provider-required",
                        "The release gate requires a web search provider",
                    )
                ],
                [],
            )
        return [], []

    phrases = distinctive_phrases(paragraphs, max_queries)
    if require_web and not phrases:
        return (
            [
                Finding(
                    "block",
                    "web-query-empty",
                    "No sufficiently distinctive manuscript phrase was available for the required web scan",
                )
            ],
            [],
        )

    findings: list[Finding] = []
    queries: list[dict[str, Any]] = []
    for location, phrase in phrases:
        query = f'"{phrase}"'
        try:
            results = provider.search(query)
        except Exception as error:  # provider boundary: preserve a bounded report
            findings.append(
                Finding(
                    "block" if require_web else "review",
                    "web-search-failed",
                    "A web similarity query failed",
                    {
                        "provider": provider.name,
                        "manuscript_location": location,
                        "query": query,
                        "error": f"{type(error).__name__}: {error}",
                    },
                )
            )
            continue
        kept = [result for result in results if not domain_excluded(result.url, excluded_domains)]
        queries.append(
            {
                "provider": provider.name,
                "manuscript_location": location,
                "query": query,
                "result_count": len(kept),
            }
        )
        for result in kept:
            findings.append(
                Finding(
                    "review",
                    "web-match-candidate",
                    "A distinctive manuscript phrase returned a web result that needs human disposition",
                    {
                        "provider": provider.name,
                        "manuscript_location": location,
                        "query": query,
                        "url": result.url,
                        "title": result.title,
                        "snippet": result.snippet,
                    },
                )
            )
    return findings, queries


def valid_decision(raw: Any) -> bool:
    if not isinstance(raw, dict) or raw.get("status") not in CLEARABLE_DECISIONS:
        return False
    if not all(isinstance(raw.get(key), str) and raw[key].strip() for key in ("reviewer", "date", "evidence")):
        return False
    try:
        date.fromisoformat(raw["date"])
    except ValueError:
        return False
    return True


def apply_decisions(findings: list[Finding], decisions_path: Path | None) -> list[Finding]:
    if decisions_path is None:
        return findings
    payload = read_json(decisions_path)
    if payload.get("schema_version") != 1 or not isinstance(payload.get("decisions"), list):
        findings.append(
            Finding(
                "block",
                "decisions-invalid",
                "Similarity decisions must use schema_version 1 and a decisions list",
                {"path": str(decisions_path)},
            )
        )
        return findings
    decisions: dict[str, dict[str, Any]] = {}
    for raw in payload["decisions"]:
        if not isinstance(raw, dict) or not isinstance(raw.get("finding_id"), str):
            findings.append(
                Finding(
                    "block",
                    "decision-invalid",
                    "A similarity decision lacks a finding_id",
                    {"path": str(decisions_path)},
                )
            )
            continue
        if not valid_decision(raw):
            findings.append(
                Finding(
                    "block",
                    "decision-invalid",
                    "A similarity decision lacks a valid status, reviewer, date, or evidence",
                    {"finding_id": raw["finding_id"]},
                )
            )
            continue
        decisions[raw["finding_id"]] = raw

    for finding in findings:
        decision = decisions.get(finding.finding_id)
        if finding.severity != "review" or decision is None:
            continue
        finding.severity = "info"
        finding.decision = {
            key: decision[key]
            for key in ("status", "reviewer", "date", "evidence")
        }
    return findings


def report_status(findings: list[Finding]) -> str:
    if any(finding.severity == "block" for finding in findings):
        return "BLOCK"
    if any(finding.severity == "review" for finding in findings):
        return "NEEDS_REVIEW"
    return "PASS"


def manuscript_hash(files: list[Path], manuscript_path: Path) -> str:
    digest = hashlib.sha256()
    root = manuscript_path if manuscript_path.is_dir() else manuscript_path.parent
    for path in files:
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def scan_similarity(
    manuscript_path: Path,
    *,
    ledger_path: Path | None = None,
    provider: SearchProvider | None = None,
    require_web: bool = False,
    decisions_path: Path | None = None,
    min_chars: int = 80,
    near_threshold: float = 0.88,
    source_near_threshold: float = 0.84,
    source_exact_chars: int = 50,
    max_web_queries: int = 20,
    exclude_domains: list[str] | None = None,
    finding_limit: int = 200,
) -> dict[str, Any]:
    if min_chars < 20:
        raise ValueError("min_chars must be at least 20")
    if not 0.0 < near_threshold <= 1.0:
        raise ValueError("near_threshold must be greater than 0 and at most 1")
    if not 0.0 < source_near_threshold <= 1.0:
        raise ValueError("source_near_threshold must be greater than 0 and at most 1")
    if source_exact_chars < 20:
        raise ValueError("source_exact_chars must be at least 20")
    if max_web_queries < 0:
        raise ValueError("max_web_queries cannot be negative")
    if finding_limit < 1:
        raise ValueError("finding_limit must be positive")
    files, paragraphs = load_manuscript(manuscript_path, min_chars)
    if not files:
        raise ValueError(f"No supported manuscript files found at {manuscript_path}")
    findings: list[Finding] = []
    if not paragraphs:
        findings.append(
            Finding(
                "block",
                "no-comparable-prose",
                "The manuscript contains no prose block long enough for the configured similarity scan",
                {"min_chars": min_chars},
            )
        )
    else:
        findings.extend(manuscript_findings(paragraphs, near_threshold, finding_limit))
    if ledger_path is not None:
        findings.extend(
            source_findings(
                paragraphs,
                ledger_path,
                source_exact_chars,
                source_near_threshold,
                max(0, finding_limit - len(findings)),
            )
        )
    web_matches, queries = web_findings(
        paragraphs,
        provider,
        require_web,
        max_web_queries,
        [domain.lower().strip() for domain in (exclude_domains or []) if domain.strip()],
    )
    findings.extend(web_matches)
    apply_decisions(findings, decisions_path)
    status = report_status(findings)
    counts = {
        severity: sum(1 for finding in findings if finding.severity == severity)
        for severity in ("block", "review", "info")
    }
    return {
        "schema_version": 1,
        "status": status,
        "checked_at": date.today().isoformat(),
        "manuscript": {
            "path": str(manuscript_path),
            "sha256": manuscript_hash(files, manuscript_path),
            "file_count": len(files),
            "paragraph_count": len(paragraphs),
        },
        "thresholds": {
            "min_chars": min_chars,
            "near_threshold": near_threshold,
            "source_exact_chars": source_exact_chars,
            "source_near_threshold": source_near_threshold,
        },
        "web": {
            "provider": provider.name if provider is not None else "none",
            "required": require_web,
            "query_count": len(queries),
            "queries": queries,
        },
        "counts": counts,
        "findings": [finding.as_dict() for finding in findings],
        "limitations": [
            "Similarity findings require context and rights review; they do not decide plagiarism or infringement.",
            "The web provider returns discovery candidates and does not prove absence when no result is found.",
        ],
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("manuscript", type=Path)
    result.add_argument("--ledger", type=Path)
    result.add_argument("--report", type=Path)
    result.add_argument("--decisions", type=Path)
    result.add_argument("--web-provider", choices=("none", "brave"), default="none")
    result.add_argument("--require-web", action="store_true")
    result.add_argument("--brave-api-key-env", default="BRAVE_SEARCH_API_KEY")
    result.add_argument("--max-web-queries", type=int, default=20)
    result.add_argument("--exclude-domain", action="append", default=[])
    result.add_argument("--min-chars", type=int, default=80)
    result.add_argument("--near-threshold", type=float, default=0.88)
    result.add_argument("--source-near-threshold", type=float, default=0.84)
    result.add_argument("--source-exact-chars", type=int, default=50)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    provider: SearchProvider | None = None
    if args.web_provider == "brave":
        api_key = os.environ.get(args.brave_api_key_env, "")
        if not api_key:
            print(
                f"Missing Brave Search API key in environment variable {args.brave_api_key_env}",
                file=sys.stderr,
            )
            return 1
        provider = BraveSearchProvider(api_key)
    try:
        report = scan_similarity(
            args.manuscript,
            ledger_path=args.ledger,
            provider=provider,
            require_web=args.require_web,
            decisions_path=args.decisions,
            min_chars=args.min_chars,
            near_threshold=args.near_threshold,
            source_exact_chars=args.source_exact_chars,
            source_near_threshold=args.source_near_threshold,
            max_web_queries=args.max_web_queries,
            exclude_domains=args.exclude_domain,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Similarity check failed: {error}", file=sys.stderr)
        return 1
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(
        f"{report['status']}: {report['counts']['block']} block, "
        f"{report['counts']['review']} review, {report['counts']['info']} info"
    )
    return {"PASS": 0, "BLOCK": 2, "NEEDS_REVIEW": 3}[report["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
