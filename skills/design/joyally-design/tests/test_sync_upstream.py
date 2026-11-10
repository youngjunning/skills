"""Verify source sync updates clean files and preserves locally edited files."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile


SOURCE_SCRIPT = Path(__file__).resolve().parents[1] / "scripts/sync-upstream.py"


class SyncUpstreamTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "scripts").mkdir()
        (self.root / "references").mkdir()
        shutil.copy2(SOURCE_SCRIPT, self.root / "scripts/sync-upstream.py")
        self.target = self.root / "references/example.md"
        self.target.write_text("初始内容\n", encoding="utf-8")
        self.archive = self.root / "source.zip"
        self.pack("初始内容\n")
        initial = self.run_sync("--manifest")
        self.assertEqual(initial.returncode, 0, initial.stderr)
        (self.root / "UPSTREAM_SYNC.json").write_text(
            json.dumps(json.loads(initial.stdout), ensure_ascii=False), encoding="utf-8")

    def pack(self, content):
        with ZipFile(self.archive, "w") as bundle:
            bundle.writestr("source-design-kit/references/example.md", content)

    def run_sync(self, mode):
        return subprocess.run(
            [sys.executable, str(self.root / "scripts/sync-upstream.py"),
             str(self.archive), mode],
            capture_output=True, text=True, encoding="utf-8")

    def test_clean_update_then_conflict(self):
        self.pack("上游更新\n")
        self.assertIn("UPDATE references/example.md", self.run_sync("--check").stdout)
        applied = self.run_sync("--apply")
        self.assertEqual(applied.returncode, 0, applied.stderr)
        self.assertEqual(self.target.read_text(encoding="utf-8"), "上游更新\n")

        self.target.write_text("本地修改\n", encoding="utf-8")
        self.pack("上游再次更新\n")
        conflict = self.run_sync("--apply")
        self.assertEqual(conflict.returncode, 1)
        self.assertIn("REVIEW references/example.md", conflict.stdout)
        self.assertEqual(self.target.read_text(encoding="utf-8"), "本地修改\n")

    def test_skips_dsh_adapter_during_sync(self):
        self.pack("上游更新\n")
        with ZipFile(self.archive, "a") as bundle:
            bundle.writestr("source-design-kit/adapters/dsh/adapter.json", "{}")
            bundle.writestr("source-design-kit/adapters/dsh/new-rule.json", "{}")

        applied = self.run_sync("--apply")
        self.assertEqual(applied.returncode, 0, applied.stderr)
        self.assertEqual(self.target.read_text(encoding="utf-8"), "上游更新\n")
        self.assertFalse((self.root / "adapters/dsh").exists())
        manifest = json.loads((self.root / "UPSTREAM_SYNC.json").read_text(encoding="utf-8"))
        self.assertEqual(set(manifest["files"]), {"references/example.md"})


if __name__ == "__main__":
    unittest.main()
