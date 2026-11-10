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
                generator = str(ROOT / 'scripts/design-engine.mjs')
                self.run_command('node', generator, mode, str(target), '--title', 'Example <safe>')
                report = json.loads(self.run_command('node', str(ROOT / 'scripts/validate-joyally-html.mjs'), str(target / 'index.html')).stdout)
                self.assertEqual(report['errors'], [])
                self.assertIn('<title>Example &lt;safe&gt; · Joyally Design</title>', (target / 'index.html').read_text())
                self.assertTrue((target / 'joyally-design/LICENSE').is_file())
                original = (target / 'index.html').read_bytes()
                retry = subprocess.run(['node', generator, mode, str(target)], capture_output=True)
                self.assertNotEqual(retry.returncode, 0)
                self.assertEqual((target / 'index.html').read_bytes(), original)

    def test_diagram_runtime_delivers_from_bundled_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'diagram.html'
            result = self.run_command('node', str(ROOT / 'scripts/design-engine.mjs'), 'diagram', 'deliver', 'workflow', str(ROOT / 'examples/archify-minimal.workflow.json'), str(output), '--json')
            self.assertTrue(json.loads(result.stdout)['ok'])
            html = output.read_text()
            self.assertIn('<svg', html)
            self.assertIn('<meta name="generator" content="Joyally Design">', html)
            self.assertNotIn('<a class="diagram-guide-credit"', html)
            self.assertGreater(output.stat().st_size, 1000)

    def test_report_disclosure_clips_hover_fill_inside_rounded_border(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'report'
            self.run_command('node', str(ROOT / 'scripts/new-joyally-html.mjs'), 'report', str(target))
            html = (target / 'index.html').read_text()
            css = (target / 'joyally-design/joyally-theme.css').read_text()
            self.assertIn('<details class="report-disclosure">', html)
            disclosure = css.split('.joyally-report .report-disclosure {', 1)[1].split('}', 1)[0]
            self.assertIn('overflow: hidden;', disclosure)
            self.assertIn('border-radius: var(--radius-sm);', disclosure)
            self.assertIn('.joyally-report .report-disclosure > summary:hover', css)
            self.assertIn('.joyally-report .report-disclosure > summary:focus-visible', css)


if __name__ == '__main__':
    unittest.main()
