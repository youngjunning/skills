from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "check_book_copyright.py"
SPEC = importlib.util.spec_from_file_location("check_book_copyright", SCRIPT)
assert SPEC and SPEC.loader
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)


def passed_reviews() -> dict:
    return {
        "distinctive_phrase_search": {
            "status": "passed",
            "reviewer": "the author",
            "date": "2026-08-19",
            "evidence": "Exact phrase queries recorded in the review notes.",
        },
        "copyright_review": {
            "status": "passed",
            "reviewer": "the author",
            "date": "2026-08-19",
            "evidence": "Rights ledger and compiled manuscript reviewed.",
        },
        "open_source_license_review": {
            "status": "passed",
            "reviewer": "the author",
            "date": "2026-08-19",
            "evidence": "Repository scope, licenses, notices, and delivery formats reviewed.",
        },
    }


def base_ledger(intent: str = "commercial") -> dict:
    return {
        "schema_version": 1,
        "book": {
            "title": "Test Book",
            "author": "俊宁",
            "publication_intent": intent,
            "jurisdictions": ["CN"],
            "originality_declaration": True,
        },
        "sources": [],
        "uses": [],
        "reviews": passed_reviews(),
    }


def repository_source(commit: str, source_text_path: str | None = None) -> dict:
    source = {
        "id": "repo-source",
        "source_type": "software-repository",
        "title": "Example repository source files",
        "creator": "Example Authors",
        "locator": f"https://github.com/example/project/tree/{commit}/src",
        "repository_url": "https://github.com/example/project",
        "commit_sha": commit,
        "path_scope": ["src/"],
        "rights_basis": "open-license",
        "rights_status": "cleared",
        "proof": "LICENSE and source headers inspected at the recorded commit.",
        "license": "MIT License",
        "license_status": "open-license",
        "license_expression": "MIT",
        "license_evidence": [
            f"https://github.com/example/project/blob/{commit}/LICENSE"
        ],
        "allowed_uses": ["reference", "facts-ideas", "quote", "reproduce", "adapt"],
        "license_review": {
            "status": "passed",
            "reviewer": "the author",
            "date": "2026-08-19",
            "evidence": "MIT scope and book distribution reviewed.",
            "obligations": ["attribution", "license-copy"],
        },
    }
    if source_text_path is not None:
        source["source_text_path"] = source_text_path
    return source


def repository_quote(commit: str, excerpt: str) -> dict:
    return {
        "source_id": "repo-source",
        "kind": "quote",
        "material_type": "code",
        "source_path": "src/example.py",
        "source_permalink": f"https://github.com/example/project/blob/{commit}/src/example.py#L1-L4",
        "manuscript_location": "chapter-04/example-01",
        "purpose": "Explain a state transition.",
        "excerpt": excerpt,
        "attribution": "Example Project contributors",
        "compliance_evidence": {
            "attribution": "Code caption and third-party inventory.",
            "license-copy": "companion/THIRD_PARTY_LICENSES/MIT.txt",
        },
    }


def repository_reference_source() -> dict:
    return {
        "id": "repo-reference",
        "title": "Example Project",
        "creator": "Example maintainers",
        "locator": "https://github.com/example/project",
        "rights_basis": "facts-ideas-only",
        "rights_status": "cleared",
        "proof": "Referenced for facts and ideas only; no protected material reused.",
    }


class CopyrightGateTests(unittest.TestCase):
    def test_original_release_can_pass(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            ledger_path = root / "copyright-ledger.json"
            findings = gate.validate_ledger(
                base_ledger(), ledger_path, "这是独立创作的测试书稿。", 50, 14
            )
        self.assertEqual(gate.report_status(findings), "PASS")

    def test_unknown_rights_block(self) -> None:
        ledger = base_ledger()
        ledger["sources"] = [
            {
                "id": "unknown-source",
                "title": "Unknown",
                "creator": "Unknown",
                "locator": "https://example.invalid/source",
                "rights_basis": "unknown",
                "rights_status": "pending",
                "proof": "No proof",
            }
        ]
        findings = gate.validate_ledger(
            ledger, Path("copyright-ledger.json"), "测试书稿。", 50, 14
        )
        self.assertEqual(gate.report_status(findings), "BLOCK")
        self.assertTrue(any(item.code == "unknown-rights" for item in findings))

    def test_unlogged_source_overlap_blocks(self) -> None:
        repeated = "这是一段具有明显表达特征并且应该被版权检查器识别出来的中文测试材料，" * 3
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            source_path = root / "source.txt"
            source_path.write_text(repeated, encoding="utf-8")
            ledger = base_ledger()
            ledger["sources"] = [
                {
                    "id": "public-source",
                    "title": "Public Source",
                    "creator": "Test Author",
                    "locator": "https://example.invalid/public-source",
                    "rights_basis": "public-domain",
                    "rights_status": "cleared",
                    "proof": "Authoritative public-domain record",
                    "public_domain_reason": "Term expired for this edition",
                    "jurisdictions": ["CN"],
                    "allowed_uses": ["quote", "reference"],
                    "source_text_path": "source.txt",
                }
            ]
            findings = gate.validate_ledger(
                ledger, root / "copyright-ledger.json", repeated, 50, 14
            )
        self.assertEqual(gate.report_status(findings), "BLOCK")
        self.assertTrue(any(item.code == "unlogged-overlap" for item in findings))

    def test_logged_quote_is_excluded_from_overlap_block(self) -> None:
        excerpt = "This deliberately distinctive quotation contains enough words for the exact overlap scanner to find it and verify its ledger record."
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            source_path = root / "source.txt"
            source_path.write_text(excerpt, encoding="utf-8")
            ledger = base_ledger()
            ledger["sources"] = [
                {
                    "id": "licensed-source",
                    "title": "Licensed Source",
                    "creator": "Test Author",
                    "locator": "https://example.invalid/licensed-source",
                    "rights_basis": "licensed",
                    "rights_status": "cleared",
                    "proof": "Signed permission record",
                    "license": "Written permission for quotation",
                    "allowed_uses": ["quote"],
                    "source_text_path": "source.txt",
                }
            ]
            ledger["uses"] = [
                {
                    "source_id": "licensed-source",
                    "kind": "quote",
                    "manuscript_location": "chapter-01",
                    "purpose": "Commentary",
                    "excerpt": excerpt,
                    "attribution": "Test Author, Licensed Source",
                }
            ]
            findings = gate.validate_ledger(
                ledger, root / "copyright-ledger.json", excerpt, 50, 14
            )
        self.assertEqual(gate.report_status(findings), "PASS")

    def test_release_quote_without_comparison_text_blocks(self) -> None:
        ledger = base_ledger()
        ledger["sources"] = [
            {
                "id": "licensed-source",
                "title": "Licensed Source",
                "creator": "Test Author",
                "locator": "https://example.invalid/licensed-source",
                "rights_basis": "licensed",
                "rights_status": "cleared",
                "proof": "Signed permission record",
                "license": "Written permission for quotation",
                "allowed_uses": ["quote"],
            }
        ]
        ledger["uses"] = [
            {
                "source_id": "licensed-source",
                "kind": "quote",
                "manuscript_location": "chapter-01",
                "purpose": "Commentary",
                "excerpt": "A short licensed quotation.",
                "attribution": "Test Author, Licensed Source",
            }
        ]
        findings = gate.validate_ledger(
            ledger, Path("copyright-ledger.json"), "A short licensed quotation.", 50, 14
        )
        self.assertEqual(gate.report_status(findings), "BLOCK")
        self.assertTrue(any(item.code == "comparison-text-missing" for item in findings))

    def test_pending_review_is_non_release_review_state(self) -> None:
        ledger = base_ledger(intent="private-draft")
        ledger["reviews"]["copyright_review"]["status"] = "pending"
        findings = gate.validate_ledger(
            ledger, Path("copyright-ledger.json"), "Draft manuscript", 50, 14
        )
        self.assertEqual(gate.report_status(findings), "NEEDS_REVIEW")

    def test_public_github_repository_without_license_cannot_supply_code(self) -> None:
        commit = "a" * 40
        ledger = base_ledger()
        source = repository_source(commit)
        source.update(
            {
                "rights_basis": "facts-ideas-only",
                "license_status": "none",
                "license": "No license",
                "license_expression": "NONE",
                "license_evidence": [],
                "allowed_uses": ["reference", "facts-ideas"],
            }
        )
        ledger["sources"] = [source]
        use = repository_quote(commit, "def example(): return True")
        ledger["uses"] = [use]
        findings = gate.validate_ledger(
            ledger, Path("copyright-ledger.json"), use["excerpt"], 50, 14
        )
        self.assertEqual(gate.report_status(findings), "BLOCK")
        self.assertTrue(any(item.code == "facts-only-overreach" for item in findings))

    def test_repository_reference_does_not_require_commit_or_license_review(self) -> None:
        ledger = base_ledger()
        del ledger["reviews"]["open_source_license_review"]
        ledger["sources"] = [repository_reference_source()]
        ledger["uses"] = [
            {
                "source_id": "repo-reference",
                "kind": "facts-ideas",
                "manuscript_location": "chapter-02/architecture-comparison",
                "purpose": "Support an independently written comparison.",
            }
        ]
        findings = gate.validate_ledger(
            ledger, Path("copyright-ledger.json"), "Independent explanation.", 50, 14
        )
        self.assertEqual(gate.report_status(findings), "PASS")

    def test_expressive_repository_use_requires_full_commit(self) -> None:
        ledger = base_ledger()
        source = repository_source("abc123")
        ledger["sources"] = [source]
        ledger["uses"] = [repository_quote("abc123", "def example(): return True")]
        findings = gate.validate_ledger(
            ledger, Path("copyright-ledger.json"), "def example(): return True", 50, 14
        )
        self.assertEqual(gate.report_status(findings), "BLOCK")
        self.assertTrue(any(item.code == "repository-commit" for item in findings))

    def test_repository_use_requires_every_recorded_obligation(self) -> None:
        commit = "b" * 40
        excerpt = "def retry_request():\n    return request_with_backoff()"
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            (root / "source.txt").write_text(excerpt, encoding="utf-8")
            ledger = base_ledger()
            ledger["sources"] = [repository_source(commit, "source.txt")]
            use = repository_quote(commit, excerpt)
            del use["compliance_evidence"]["license-copy"]
            ledger["uses"] = [use]
            findings = gate.validate_ledger(
                ledger, root / "copyright-ledger.json", excerpt, 50, 14
            )
        self.assertEqual(gate.report_status(findings), "BLOCK")
        self.assertTrue(
            any(item.code == "repository-obligation-unsatisfied" for item in findings)
        )

    def test_compliant_commit_pinned_repository_quote_can_pass(self) -> None:
        commit = "c" * 40
        excerpt = "def retry_request():\n    return request_with_backoff()"
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            (root / "source.txt").write_text(excerpt, encoding="utf-8")
            ledger = base_ledger()
            ledger["sources"] = [repository_source(commit, "source.txt")]
            ledger["uses"] = [repository_quote(commit, excerpt)]
            findings = gate.validate_ledger(
                ledger, root / "copyright-ledger.json", excerpt, 50, 14
            )
        self.assertEqual(gate.report_status(findings), "PASS")

    def test_reference_only_use_does_not_trigger_path_scope_gate(self) -> None:
        commit = "d" * 40
        ledger = base_ledger()
        ledger["sources"] = [repository_source(commit)]
        ledger["uses"] = [
            {
                "source_id": "repo-source",
                "kind": "reference",
                "material_type": "documentation",
                "source_path": "docs/architecture.md",
                "source_permalink": f"https://github.com/example/project/blob/{commit}/docs/architecture.md",
                "manuscript_location": "chapter-02",
                "purpose": "Cite the documented architecture.",
            }
        ]
        findings = gate.validate_ledger(
            ledger, Path("copyright-ledger.json"), "Independent explanation.", 50, 14
        )
        self.assertEqual(gate.report_status(findings), "PASS")

    def test_repository_non_code_reproduction_needs_separate_rights_evidence(self) -> None:
        commit = "e" * 40
        excerpt = "A distinctive architecture diagram caption from the repository."
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            (root / "source.txt").write_text(excerpt, encoding="utf-8")
            source = repository_source(commit, "source.txt")
            source["path_scope"] = ["docs/"]
            ledger = base_ledger()
            ledger["sources"] = [source]
            use = repository_quote(commit, excerpt)
            use.update(
                {
                    "kind": "reproduce",
                    "material_type": "diagram",
                    "source_path": "docs/architecture.svg",
                    "source_permalink": f"https://github.com/example/project/blob/{commit}/docs/architecture.svg",
                }
            )
            ledger["uses"] = [use]
            findings = gate.validate_ledger(
                ledger, root / "copyright-ledger.json", excerpt, 50, 14
            )
        self.assertEqual(gate.report_status(findings), "BLOCK")
        self.assertTrue(
            any(
                item.code == "missing-field"
                and "material_rights_evidence" in item.message
                for item in findings
            )
        )


if __name__ == "__main__":
    unittest.main()
