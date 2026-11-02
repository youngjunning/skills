from pathlib import Path
import json
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'skills/design/joyally-design'


class ReportRuntimeTests(unittest.TestCase):
    def run_command(self, *args):
        result = subprocess.run(list(args), capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return result

    def test_report_and_deck_are_portable_and_overwrite_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            for mode in ['report', 'deck']:
                target = Path(directory) / mode
                generator = str(ROOT / 'scripts/new-joyally-html.mjs')
                self.run_command('node', generator, mode, str(target), '--title', 'Example <safe>')
                report = json.loads(self.run_command('node', str(ROOT / 'scripts/validate-joyally-html.mjs'), str(target / 'index.html')).stdout)
                self.assertEqual(report['errors'], [])
                self.assertIn('Example &lt;safe&gt;', (target / 'index.html').read_text())
                original = (target / 'index.html').read_bytes()
                retry = subprocess.run(['node', generator, mode, str(target)], capture_output=True)
                self.assertNotEqual(retry.returncode, 0)
                self.assertEqual((target / 'index.html').read_bytes(), original)

    def test_diagram_runtime_delivers_from_bundled_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'diagram.html'
            result = self.run_command('node', str(ROOT / 'scripts/joyally-archify.mjs'), 'deliver', 'workflow', str(ROOT / 'examples/archify-minimal.workflow.json'), str(output), '--json')
            self.assertTrue(json.loads(result.stdout)['ok'])
            self.assertIn('<svg', output.read_text())
            self.assertGreater(output.stat().st_size, 1000)


if __name__ == '__main__':
    unittest.main()
