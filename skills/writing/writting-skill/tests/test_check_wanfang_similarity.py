from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "check_wanfang_similarity.py"
SPEC = importlib.util.spec_from_file_location("check_wanfang_similarity", SCRIPT)
assert SPEC and SPEC.loader
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)


class WanfangEvidenceTests(unittest.TestCase):
    def create_record(self, root: Path) -> tuple[Path, Path, Path, dict]:
        manuscript = root / "manuscript.md"
        report = root / "wanfang-report.pdf"
        evidence = root / "wanfang-evidence.json"
        manuscript.write_text("这是需要绑定万方检测报告的原创技术书稿。", encoding="utf-8")
        report.write_bytes(b"synthetic official report fixture")
        args = Namespace(
            manuscript=manuscript,
            report_file=report,
            report_id="WF-20260819-TEST",
            checked_at="2026-08-19",
            overall_similarity=8.6,
            reviewer="the author",
            review_date="2026-08-19",
            verification_url="https://truth.wanfangdata.com.cn/",
            verification_evidence="Report ID checked on the official verification page.",
        )
        record = gate.build_evidence(args)
        evidence.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
        return manuscript, report, evidence, record

    def test_valid_official_report_evidence_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            manuscript, _, evidence, record = self.create_record(Path(raw_dir))
            findings = gate.validate_evidence(record, evidence, manuscript)
        self.assertEqual(findings, [])

    def test_changed_manuscript_blocks_old_report(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            manuscript, _, evidence, record = self.create_record(Path(raw_dir))
            manuscript.write_text("书稿已经发生修改，旧报告不再覆盖当前版本。", encoding="utf-8")
            findings = gate.validate_evidence(record, evidence, manuscript)
        self.assertTrue(any(item.code == "manuscript-hash-mismatch" for item in findings))

    def test_changed_report_artifact_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            manuscript, report, evidence, record = self.create_record(Path(raw_dir))
            report.write_bytes(b"changed report")
            findings = gate.validate_evidence(record, evidence, manuscript)
        self.assertTrue(any(item.code == "source-report-hash-mismatch" for item in findings))

    def test_non_official_verification_url_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            manuscript, _, evidence, record = self.create_record(Path(raw_dir))
            record["authenticity_review"]["verification_url"] = "https://wanfang.example/report"
            findings = gate.validate_evidence(record, evidence, manuscript)
        self.assertTrue(any(item.code == "verification-url" for item in findings))


if __name__ == "__main__":
    unittest.main()
