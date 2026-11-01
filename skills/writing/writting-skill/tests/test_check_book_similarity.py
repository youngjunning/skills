from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "check_book_similarity.py"
SPEC = importlib.util.spec_from_file_location("check_book_similarity", SCRIPT)
assert SPEC and SPEC.loader
similarity = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = similarity
SPEC.loader.exec_module(similarity)


LONG_PARAGRAPH = (
    "这是一段专门用于查重测试的中文技术说明，它包含足够多的具体表达、执行边界和验证条件，"
    "能够稳定触发长段落比较，同时不会依赖任何真实书稿或外部受保护材料。"
    "检查结果还必须保留章节位置、匹配类型和人工复核证据。"
)


def write_manuscript(root: Path, files: dict[str, str]) -> Path:
    manuscript = root / "manuscript"
    manuscript.mkdir()
    for name, text in files.items():
        (manuscript / name).write_text(text, encoding="utf-8")
    return manuscript


def write_ledger(root: Path, source_text: str, *, logged_quote: bool = False) -> Path:
    (root / "source.txt").write_text(source_text, encoding="utf-8")
    uses = []
    if logged_quote:
        uses.append(
            {
                "source_id": "source-1",
                "kind": "quote",
                "manuscript_location": "chapter-01",
                "purpose": "Commentary",
                "excerpt": source_text,
                "attribution": "Test Source",
            }
        )
    ledger = {
        "schema_version": 1,
        "book": {"title": "Test Book"},
        "sources": [
            {
                "id": "source-1",
                "title": "Test Source",
                "source_text_path": "source.txt",
            }
        ],
        "uses": uses,
    }
    path = root / "copyright-ledger.json"
    path.write_text(json.dumps(ledger, ensure_ascii=False), encoding="utf-8")
    return path


class FakeSearchProvider:
    name = "fake"

    def search(self, query: str) -> list[similarity.WebResult]:
        return [
            similarity.WebResult(
                url="https://example.com/matching-page",
                title="Matching page",
                snippet=query.strip('"'),
            )
        ]


class SimilarityGateTests(unittest.TestCase):
    def test_unrelated_manuscript_passes_local_scan(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manuscript = write_manuscript(
                root,
                {
                    "chapter-01.md": LONG_PARAGRAPH,
                    "chapter-02.md": (
                        "另一章讨论完全不同的工程问题：如何记录模型版本、运行环境、成本和失败恢复。"
                        "这段内容在用词、结构和结论上都与前一章不同，并且同样满足最小长度要求。"
                    ),
                },
            )
            report = similarity.scan_similarity(manuscript)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["findings"], [])

    def test_manuscript_without_comparable_prose_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manuscript = write_manuscript(root, {"chapter-01.md": "# 标题\n\n太短。"})
            report = similarity.scan_similarity(manuscript)
        self.assertEqual(report["status"], "BLOCK")
        self.assertTrue(
            any(item["code"] == "no-comparable-prose" for item in report["findings"])
        )

    def test_invalid_threshold_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manuscript = write_manuscript(root, {"chapter-01.md": LONG_PARAGRAPH})
            with self.assertRaisesRegex(ValueError, "near_threshold"):
                similarity.scan_similarity(manuscript, near_threshold=1.1)

    def test_exact_cross_chapter_duplicate_needs_review(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manuscript = write_manuscript(
                root,
                {
                    "chapter-01.md": LONG_PARAGRAPH,
                    "chapter-02.md": LONG_PARAGRAPH,
                },
            )
            report = similarity.scan_similarity(manuscript)
        self.assertEqual(report["status"], "NEEDS_REVIEW")
        self.assertTrue(
            any(item["code"] == "manuscript-exact-duplicate" for item in report["findings"])
        )

    def test_near_cross_chapter_duplicate_needs_review(self) -> None:
        changed = LONG_PARAGRAPH.replace("执行边界", "运行边界").replace("稳定触发", "可靠触发")
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manuscript = write_manuscript(
                root,
                {
                    "chapter-01.md": LONG_PARAGRAPH,
                    "chapter-02.md": changed,
                },
            )
            report = similarity.scan_similarity(manuscript, near_threshold=0.84)
        self.assertEqual(report["status"], "NEEDS_REVIEW")
        self.assertTrue(
            any(item["code"] == "manuscript-near-duplicate" for item in report["findings"])
        )

    def test_unlogged_exact_source_overlap_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manuscript = write_manuscript(root, {"chapter-01.md": LONG_PARAGRAPH})
            ledger = write_ledger(root, LONG_PARAGRAPH)
            report = similarity.scan_similarity(manuscript, ledger_path=ledger)
        self.assertEqual(report["status"], "BLOCK")
        self.assertTrue(
            any(item["code"] == "unlogged-source-overlap" for item in report["findings"])
        )

    def test_partial_exact_source_overlap_blocks(self) -> None:
        copied = LONG_PARAGRAPH[10:75]
        manuscript_text = "这段开头是作者自己的说明，用于建立上下文和读者问题。" + copied + "这段结尾也是作者新增的判断。"
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manuscript = write_manuscript(root, {"chapter-01.md": manuscript_text})
            ledger = write_ledger(root, LONG_PARAGRAPH)
            report = similarity.scan_similarity(manuscript, ledger_path=ledger)
        self.assertEqual(report["status"], "BLOCK")
        self.assertTrue(
            any(item["code"] == "unlogged-source-overlap" for item in report["findings"])
        )

    def test_logged_quote_is_excluded_from_source_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manuscript = write_manuscript(root, {"chapter-01.md": LONG_PARAGRAPH})
            ledger = write_ledger(root, LONG_PARAGRAPH, logged_quote=True)
            report = similarity.scan_similarity(manuscript, ledger_path=ledger)
        self.assertEqual(report["status"], "PASS")

    def test_logged_quote_inside_commentary_is_not_reported_as_near_overlap(self) -> None:
        manuscript_text = (
            "下面这段 quotation 用来解释一个具体判断，引用前后的评论都是作者独立撰写的内容。"
            + LONG_PARAGRAPH
            + "引用到此结束；接下来只讨论该判断在当前系统约束下为什么成立。"
        )
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manuscript = write_manuscript(root, {"chapter-01.md": manuscript_text})
            ledger = write_ledger(root, LONG_PARAGRAPH, logged_quote=True)
            report = similarity.scan_similarity(manuscript, ledger_path=ledger)
        self.assertEqual(report["status"], "PASS")

    def test_near_source_overlap_needs_review(self) -> None:
        changed = "新增".join(
            LONG_PARAGRAPH[index : index + 24]
            for index in range(0, len(LONG_PARAGRAPH), 24)
        )
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manuscript = write_manuscript(root, {"chapter-01.md": changed})
            ledger = write_ledger(root, LONG_PARAGRAPH)
            report = similarity.scan_similarity(
                manuscript,
                ledger_path=ledger,
                source_near_threshold=0.80,
            )
        self.assertEqual(report["status"], "NEEDS_REVIEW")
        self.assertTrue(
            any(item["code"] == "near-source-overlap" for item in report["findings"])
        )

    def test_required_web_scan_without_provider_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manuscript = write_manuscript(root, {"chapter-01.md": LONG_PARAGRAPH})
            report = similarity.scan_similarity(manuscript, require_web=True)
        self.assertEqual(report["status"], "BLOCK")
        self.assertTrue(
            any(item["code"] == "web-provider-required" for item in report["findings"])
        )

    def test_web_match_candidate_can_be_cleared_by_named_decision(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manuscript = write_manuscript(root, {"chapter-01.md": LONG_PARAGRAPH})
            first = similarity.scan_similarity(
                manuscript,
                provider=FakeSearchProvider(),
                require_web=True,
                max_web_queries=1,
            )
            self.assertEqual(first["status"], "NEEDS_REVIEW")
            candidate = next(
                item for item in first["findings"] if item["code"] == "web-match-candidate"
            )
            decisions = root / "similarity-decisions.json"
            decisions.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "decisions": [
                            {
                                "finding_id": candidate["id"],
                                "status": "false-positive",
                                "reviewer": "the author",
                                "date": "2026-08-19",
                                "evidence": "The result quotes this book's own public sample.",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            cleared = similarity.scan_similarity(
                manuscript,
                provider=FakeSearchProvider(),
                require_web=True,
                max_web_queries=1,
                decisions_path=decisions,
            )
        self.assertEqual(cleared["status"], "PASS")
        cleared_candidate = next(
            item for item in cleared["findings"] if item["code"] == "web-match-candidate"
        )
        self.assertEqual(cleared_candidate["severity"], "info")
        self.assertEqual(cleared_candidate["decision"]["reviewer"], "the author")

    def test_brave_provider_parses_web_results(self) -> None:
        payload = json.dumps(
            {
                "web": {
                    "results": [
                        {
                            "url": "https://example.com/article",
                            "title": "Article",
                            "description": "Matching text",
                        }
                    ]
                }
            }
        ).encode()

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return None

            def read(self) -> bytes:
                return payload

        def opener(_request, timeout: int):
            self.assertEqual(timeout, 20)
            return Response()

        provider = similarity.BraveSearchProvider("secret", opener=opener)
        results = provider.search('"distinctive phrase"')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].url, "https://example.com/article")

    def test_cli_writes_json_report(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            manuscript = write_manuscript(root, {"chapter-01.md": LONG_PARAGRAPH})
            report_path = root / "reviews" / "similarity-report.json"
            exit_code = similarity.main(
                [str(manuscript), "--report", str(report_path)]
            )
            report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(exit_code, 0)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["manuscript"]["file_count"], 1)


if __name__ == "__main__":
    unittest.main()
