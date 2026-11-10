#!/usr/bin/env python3
"""Record and verify official Wanfang similarity-report evidence for a manuscript.

This adapter deliberately does not automate Wanfang submission: the official
Detection Service API is contract-gated and has no public request schema. It
binds a lawfully obtained official report to an exact manuscript version and a
named authenticity review so the book release gate can retain verifiable
domestic-check evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse


TEXT_SUFFIXES = {".md", ".markdown", ".txt"}
OFFICIAL_SERVICE_URL = "https://jc.wanfangdata.com.cn/"
OFFICIAL_HOSTS = {
    "check.wanfangdata.com.cn",
    "jc.wanfangdata.com.cn",
    "truth.wanfangdata.com.cn",
}


@dataclass
class Finding:
    code: str
    message: str
    context: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {"code": self.code, "message": self.message, "context": self.context}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def valid_iso_date(value: Any) -> bool:
    if not nonempty(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def manuscript_sha256(path: Path) -> tuple[str, int]:
    files = manuscript_files(path)
    if not files:
        raise ValueError(f"No supported manuscript files found at {path}")
    content = "\n".join(
        item.read_text(encoding="utf-8", errors="replace") for item in files
    )
    return hashlib.sha256(content.encode("utf-8")).hexdigest(), len(files)


def official_url(value: Any) -> bool:
    if not nonempty(value):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and (parsed.hostname or "").lower() in OFFICIAL_HOSTS


def resolve_artifact(record_path: Path, raw_path: Any) -> Path | None:
    if not nonempty(raw_path):
        return None
    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        path = record_path.parent / path
    return path.resolve()


def validate_evidence(
    record: dict[str, Any],
    record_path: Path,
    manuscript_path: Path,
) -> list[Finding]:
    findings: list[Finding] = []
    if record.get("schema_version") != 1:
        findings.append(Finding("schema-version", "schema_version must equal 1"))
    if record.get("provider") != "wanfang":
        findings.append(Finding("provider", "provider must equal wanfang"))
    if not official_url(record.get("service_url")):
        findings.append(Finding("service-url", "service_url must use an official Wanfang host"))
    if not nonempty(record.get("report_id")):
        findings.append(Finding("report-id", "report_id is required"))
    if not valid_iso_date(record.get("checked_at")):
        findings.append(Finding("checked-at", "checked_at must be an ISO date"))

    similarity = record.get("overall_similarity_percent")
    if not isinstance(similarity, (int, float)) or isinstance(similarity, bool) or not 0 <= similarity <= 100:
        findings.append(
            Finding("overall-similarity", "overall_similarity_percent must be between 0 and 100")
        )

    try:
        current_manuscript_hash, current_file_count = manuscript_sha256(manuscript_path)
    except (OSError, ValueError) as error:
        findings.append(Finding("manuscript", str(error)))
    else:
        manuscript = record.get("manuscript")
        if not isinstance(manuscript, dict):
            findings.append(Finding("manuscript-record", "manuscript evidence is required"))
        else:
            if manuscript.get("sha256") != current_manuscript_hash:
                findings.append(
                    Finding(
                        "manuscript-hash-mismatch",
                        "The Wanfang evidence covers a different manuscript version",
                        {"expected": manuscript.get("sha256"), "actual": current_manuscript_hash},
                    )
                )
            if manuscript.get("file_count") != current_file_count:
                findings.append(
                    Finding(
                        "manuscript-file-count",
                        "The recorded manuscript file count does not match",
                        {"expected": manuscript.get("file_count"), "actual": current_file_count},
                    )
                )

    source_report = record.get("source_report")
    if not isinstance(source_report, dict):
        findings.append(Finding("source-report", "source_report evidence is required"))
    else:
        artifact = resolve_artifact(record_path, source_report.get("path"))
        if artifact is None or not artifact.is_file():
            findings.append(
                Finding("source-report-missing", "The retained official Wanfang report is missing")
            )
        elif source_report.get("sha256") != sha256_file(artifact):
            findings.append(
                Finding(
                    "source-report-hash-mismatch",
                    "The retained Wanfang report has changed since it was recorded",
                )
            )

    review = record.get("authenticity_review")
    if not isinstance(review, dict) or review.get("status") != "verified":
        findings.append(
            Finding("authenticity-not-verified", "Official-report authenticity has not been verified")
        )
    else:
        for key in ("reviewer", "date", "evidence"):
            if not nonempty(review.get(key)):
                findings.append(
                    Finding("review-evidence-missing", f"authenticity_review lacks {key}")
                )
        if not valid_iso_date(review.get("date")):
            findings.append(Finding("review-date", "authenticity_review.date must be an ISO date"))
        if not official_url(review.get("verification_url")):
            findings.append(
                Finding(
                    "verification-url",
                    "verification_url must use an official Wanfang verification host",
                )
            )
    return findings


def build_evidence(args: argparse.Namespace) -> dict[str, Any]:
    report_file = args.report_file.expanduser().resolve()
    if not report_file.is_file():
        raise ValueError(f"Wanfang report file not found: {report_file}")
    manuscript_hash, file_count = manuscript_sha256(args.manuscript)
    return {
        "schema_version": 1,
        "provider": "wanfang",
        "service_url": OFFICIAL_SERVICE_URL,
        "report_id": args.report_id,
        "checked_at": args.checked_at,
        "overall_similarity_percent": args.overall_similarity,
        "manuscript": {
            "path": str(args.manuscript.expanduser().resolve()),
            "sha256": manuscript_hash,
            "file_count": file_count,
        },
        "source_report": {
            "path": str(report_file),
            "sha256": sha256_file(report_file),
        },
        "authenticity_review": {
            "status": "verified",
            "reviewer": args.reviewer,
            "date": args.review_date,
            "verification_url": args.verification_url,
            "evidence": args.verification_evidence,
        },
        "limitations": [
            "The aggregate percentage is review evidence, not a plagiarism or copyright verdict.",
            "This record verifies retained artifacts and a named authenticity review; it does not call a private Wanfang API.",
        ],
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def print_result(findings: Iterable[Finding]) -> int:
    items = list(findings)
    status = "PASS" if not items else "BLOCK"
    print(f"{status}: {len(items)} evidence finding(s)")
    for item in items:
        print(f"- {item.code}: {item.message}", file=sys.stderr)
    return 0 if not items else 2


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)

    record = commands.add_parser("record", help="Bind an official Wanfang report to a manuscript")
    record.add_argument("manuscript", type=Path)
    record.add_argument("--report-file", type=Path, required=True)
    record.add_argument("--report-id", required=True)
    record.add_argument("--checked-at", required=True)
    record.add_argument("--overall-similarity", type=float, required=True)
    record.add_argument("--reviewer", required=True)
    record.add_argument("--review-date", default=date.today().isoformat())
    record.add_argument("--verification-url", required=True)
    record.add_argument("--verification-evidence", required=True)
    record.add_argument("--output", type=Path, required=True)

    verify = commands.add_parser("verify", help="Verify retained Wanfang evidence")
    verify.add_argument("manuscript", type=Path)
    verify.add_argument("--evidence", type=Path, required=True)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "record":
        try:
            record = build_evidence(args)
            findings = validate_evidence(record, args.output.resolve(), args.manuscript)
        except (OSError, ValueError) as error:
            print(f"Wanfang evidence failed: {error}", file=sys.stderr)
            return 1
        if findings:
            return print_result(findings)
        write_json(args.output, record)
        return print_result([])

    try:
        record = json.loads(args.evidence.read_text(encoding="utf-8"))
        if not isinstance(record, dict):
            raise ValueError("Evidence root must be a JSON object")
        findings = validate_evidence(record, args.evidence.resolve(), args.manuscript)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Wanfang evidence failed: {error}", file=sys.stderr)
        return 1
    return print_result(findings)


if __name__ == "__main__":
    raise SystemExit(main())
