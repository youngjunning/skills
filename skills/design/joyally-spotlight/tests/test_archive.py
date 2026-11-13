import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "archive.py"


class ArchiveTest(unittest.TestCase):
    def run_archive(self, root, *args, ok=True):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), *args],
            capture_output=True, text=True,
        )
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result

    def test_save_and_find_private_screenshot(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "spotlight"
            image = base / "source.png"
            Image.new("RGB", (64, 32), "white").save(image)
            saved = json.loads(self.run_archive(
                root, "save", "--input", str(image), "--project", "sample-app",
                "--task", "storage setup", "--step", "预发写读删通过",
                "--environment", "pre", "--outcome", "success",
                "--captured-at", "2026-11-12",
            ).stdout)
            target = Path(saved["image"])
            self.assertIn("预发写读删通过", target.name)
            self.assertEqual(target.read_bytes(), image.read_bytes())
            self.assertEqual(saved["width"], 64)
            self.assertEqual(saved["height"], 32)
            self.assertIn("archived_at", saved)
            self.assertEqual(saved["captured_at"], "2026-11-12")
            self.assertEqual(os.stat(root).st_mode & 0o777, 0o700)
            self.assertEqual(os.stat(target).st_mode & 0o777, 0o600)
            self.assertEqual(os.stat(target.with_suffix(".json")).st_mode & 0o777, 0o600)
            found = json.loads(self.run_archive(root, "find", "--project", "sample", "--query", "写读删", "--verify", "--json").stdout)
            self.assertEqual([item["image"] for item in found], [str(target)])
            self.assertEqual(json.loads(self.run_archive(root, "find", "--since", "2026-11-13", "--json").stdout), [])
            self.assertEqual(json.loads(self.run_archive(root, "find", "--task", "ACL", "--json").stdout), [])

    def test_rejects_invalid_image_and_symlink_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            invalid = base / "capture.png"
            invalid.write_text("not a screenshot")
            result = self.run_archive(
                base / "archive", "save", "--input", str(invalid),
                "--project", "test", "--task", "task", "--step", "result",
                "--outcome", "success", ok=False,
            )
            self.assertIn("cannot identify image", result.stderr)
            archive = base / "archive"
            archive.symlink_to(base / "elsewhere", target_is_directory=True)
            image = base / "source.png"
            Image.new("RGB", (8, 8), "white").save(image)
            result = self.run_archive(
                archive, "save", "--input", str(image),
                "--project", "test", "--task", "task", "--step", "result",
                "--outcome", "success", ok=False,
            )
            self.assertIn("must not be a symlink", result.stderr)

    def test_rejects_sensitive_url_query(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            image = base / "source.png"
            Image.new("RGB", (8, 8), "white").save(image)
            result = self.run_archive(
                base / "archive", "save", "--input", str(image),
                "--project", "test", "--task", "task", "--step", "result",
                "--outcome", "success", "--url", "https://example.com/page?token=secret",
                ok=False,
            )
            self.assertIn("must omit query and fragment", result.stderr)


if __name__ == "__main__":
    unittest.main()
