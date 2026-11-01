import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('link_skills', Path(__file__).resolve().parents[1] / 'scripts/link-skills.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class LinkSkillsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        self.source = self.base / 'source'
        self.source.mkdir()
        (self.source / 'SKILL.md').write_text('test fixture')
        self.dest = self.base / 'agent'
        self.backups = self.base / 'backups'

    def install(self, **kwargs):
        return module.install([('sample', self.source)], self.dest, backup_root=self.backups, **kwargs)

    def test_dry_run_does_not_create_destination(self):
        self.assertEqual(self.install(dry_run=True), [('sample', 'link')])
        self.assertFalse(self.dest.exists())

    def test_install_is_idempotent(self):
        self.install()
        self.assertEqual((self.dest / 'sample').resolve(), self.source)
        self.assertEqual(self.install(), [('sample', 'unchanged')])

    def test_conflict_stops_before_any_mutation(self):
        self.dest.mkdir()
        (self.dest / 'sample').mkdir()
        with self.assertRaises(ValueError):
            module.install([('first', self.source), ('sample', self.source)], self.dest)
        self.assertFalse((self.dest / 'first').exists())
        self.assertFalse(self.backups.exists())

    def test_replace_preserves_existing_contents(self):
        old = self.dest / 'sample'
        old.mkdir(parents=True)
        (old / 'custom.txt').write_text('keep my changes')
        self.install(replace=True)
        self.assertTrue(old.is_symlink())
        backup = next(self.backups.glob('*/sample/custom.txt'))
        self.assertEqual(backup.read_text(), 'keep my changes')

    def test_dangling_link_is_preserved_in_backup(self):
        self.dest.mkdir()
        (self.dest / 'sample').symlink_to(self.base / 'missing')
        self.install(replace=True)
        backup = next(self.backups.glob('*/sample'))
        self.assertTrue(backup.is_symlink())
        self.assertEqual(backup.readlink(), self.base / 'missing')

    def test_destination_inside_source_checkout_is_rejected(self):
        with self.assertRaises(ValueError):
            module.install([('sample', self.source)], module.ROOT / 'skills', dry_run=True)


if __name__ == '__main__':
    unittest.main()
