import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_book_publishing.py"


class PublishingGateTests(unittest.TestCase):
    def run_gate(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def write_clean_manuscript(self, directory: Path) -> Path:
        manuscript = directory / "manuscript"
        manuscript.mkdir()
        (manuscript / "chapter-01.md").write_text(
            "# 第一章 浏览器任务链路\n\n该任务由浏览器系统协同执行。\n\n## 1.1 执行边界\n\n运行时保存审计记录。\n",
            encoding="utf-8",
        )
        return manuscript

    def completed_evidence(self, template_path: Path) -> dict:
        evidence = json.loads(template_path.read_text(encoding="utf-8"))
        evidence["publisher_requirements"].update(
            {
                "status": "verified",
                "publisher": "示例出版社",
                "source": "publisher-style-sheet.pdf",
                "version": "2026-08",
                "verified_at": "2026-08-27",
                "reviewer": "editor",
            }
        )
        for name, review in evidence["reviews"].items():
            review.update(
                {
                    "status": "pass",
                    "reviewer": "editor",
                    "date": "2026-08-27",
                    "scope": name,
                }
            )
        evidence["reviews"]["copyedit"]["error_rate_per_10000"] = 0.2
        return evidence

    def test_clean_verified_manuscript_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manuscript = self.write_clean_manuscript(root)
            template = root / "evidence.json"
            self.assertEqual(self.run_gate(str(manuscript), "--write-template", str(template)).returncode, 0)
            evidence = self.completed_evidence(template)
            template.write_text(json.dumps(evidence, ensure_ascii=False), encoding="utf-8")

            result = self.run_gate(str(manuscript), "--evidence", str(template))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "PASS")

    def test_template_is_needs_review(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manuscript = self.write_clean_manuscript(root)
            template = root / "evidence.json"
            self.run_gate(str(manuscript), "--write-template", str(template))

            result = self.run_gate(str(manuscript), "--evidence", str(template))

            self.assertEqual(result.returncode, 3)
            self.assertEqual(json.loads(result.stdout)["status"], "NEEDS_REVIEW")

    def test_hash_mismatch_and_heading_jump_block(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manuscript = self.write_clean_manuscript(root)
            template = root / "evidence.json"
            self.run_gate(str(manuscript), "--write-template", str(template))
            evidence = self.completed_evidence(template)
            template.write_text(json.dumps(evidence, ensure_ascii=False), encoding="utf-8")
            (manuscript / "chapter-01.md").write_text(
                "# 第一章\n\n### 跳级标题\n\n正文。\n",
                encoding="utf-8",
            )

            result = self.run_gate(str(manuscript), "--evidence", str(template))
            report = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            codes = {item["code"] for item in report["findings"]}
            self.assertIn("manuscript_hash_mismatch", codes)
            self.assertIn("heading_level_jump", codes)

    def test_broken_asset_and_placeholder_block(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manuscript = root / "chapter.md"
            manuscript.write_text(
                "# 标题\n\nTODO：补图。\n\n![架构图](images/missing.png)\n",
                encoding="utf-8",
            )
            template = root / "evidence.json"
            self.run_gate(str(manuscript), "--write-template", str(template))
            evidence = self.completed_evidence(template)
            template.write_text(json.dumps(evidence, ensure_ascii=False), encoding="utf-8")

            result = self.run_gate(str(manuscript), "--evidence", str(template))
            report = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            codes = {item["code"] for item in report["findings"]}
            self.assertIn("unresolved_placeholder", codes)
            self.assertIn("missing_local_asset", codes)

    def test_colloquial_narration_is_reviewed_but_blockquote_prompt_is_ignored(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manuscript = root / "chapter.md"
            manuscript.write_text(
                "# 标题\n\n这句话看起来像一个 prompt。\n\n> 先让我确认，再提交申请。\n",
                encoding="utf-8",
            )
            template = root / "evidence.json"
            self.run_gate(str(manuscript), "--write-template", str(template))
            evidence = self.completed_evidence(template)
            template.write_text(json.dumps(evidence, ensure_ascii=False), encoding="utf-8")

            result = self.run_gate(str(manuscript), "--evidence", str(template))
            report = json.loads(result.stdout)

            self.assertEqual(result.returncode, 3)
            colloquial = [item for item in report["findings"] if item["code"] == "colloquial_narration"]
            self.assertEqual(len(colloquial), 1)
            self.assertEqual(colloquial[0]["line"], 3)

    def test_pronoun_led_narration_is_reviewed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manuscript = root / "chapter.md"
            manuscript.write_text(
                "# 标题\n\n我认为该方案更稳定。\n\n> 我需要先确认采购申请。\n",
                encoding="utf-8",
            )
            template = root / "evidence.json"
            self.run_gate(str(manuscript), "--write-template", str(template))
            evidence = self.completed_evidence(template)
            template.write_text(json.dumps(evidence, ensure_ascii=False), encoding="utf-8")

            result = self.run_gate(str(manuscript), "--evidence", str(template))
            report = json.loads(result.stdout)

            self.assertEqual(result.returncode, 3)
            pronouns = [item for item in report["findings"] if item["code"] == "pronoun_led_framing"]
            self.assertEqual(len(pronouns), 1)
            self.assertEqual(pronouns[0]["line"], 3)

    def test_mainland_china_error_rate_above_limit_blocks(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manuscript = self.write_clean_manuscript(root)
            template = root / "evidence.json"
            self.run_gate(str(manuscript), "--write-template", str(template))
            evidence = self.completed_evidence(template)
            evidence["reviews"]["copyedit"]["error_rate_per_10000"] = 1.1
            template.write_text(json.dumps(evidence, ensure_ascii=False), encoding="utf-8")

            result = self.run_gate(str(manuscript), "--evidence", str(template))
            report = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            codes = {item["code"] for item in report["findings"]}
            self.assertIn("copyedit_error_rate_exceeded", codes)


if __name__ == "__main__":
    unittest.main()
