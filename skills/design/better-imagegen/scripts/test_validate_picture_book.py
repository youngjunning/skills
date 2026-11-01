"""Regression checks for book-delivery failures using synthetic local images."""
import copy
import hashlib
from pathlib import Path
import tempfile
import unittest

from PIL import Image
from validate_picture_book import validate


class PictureBookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        Image.new('RGB', (100, 80), 'white').save(self.root / 'page.png')
        Image.new('RGB', (100, 80), 'green').save(self.root / 'art.png')
        self.page = dict(page=1, purpose='reveal', scene='hands hold toy',
                         focal_subject='toy', shot='detail', angle='overhead',
                         composition='upper right', evidence='visible seam',
                         layout='integrated', art='art.png', image='page.png',
                         text='玩具', text_region=[0.1, 0.7, 0.9, 0.9],
                         protected_boxes=[[0.2, 0.1, 0.8, 0.6]],
                         text_blocks=[dict(text='玩具', box=[0.2, 0.75, 0.6, 0.85])])
        self.page['review'] = dict.fromkeys(
            ('identity', 'anatomy', 'story_evidence', 'copy', 'readability', 'composition'), 'pass')
        self.page['review'].update(note='Synthetic test fixture, not a visual approval',
            image_sha256=hashlib.sha256((self.root / 'page.png').read_bytes()).hexdigest())
        self.book = dict(page_count=1, size_cm=[2.54, 2.032], dpi=100,
                         layout='integrated', safe_box=[0.05, 0.05, 0.95, 0.95], pages=[self.page])

    def errors(self):
        return '\n'.join(validate(self.book, self.root)['errors'])

    def test_valid_fixture(self):
        self.assertEqual(self.errors(), '')

    def test_count_and_order(self):
        self.book['page_count'] = 20
        self.page['page'] = 2
        self.assertIn('page count', self.errors())
        self.assertIn('page numbers', self.errors())

    def test_same_art_different_caption(self):
        p = copy.deepcopy(self.page)
        p.update(page=2, text='小猫', image='second.png')
        p['text_blocks'][0]['text'] = '小猫'
        Image.new('RGB', (100, 80), 'yellow').save(self.root / 'second.png')
        p['review']['image_sha256'] = hashlib.sha256((self.root / 'second.png').read_bytes()).hexdigest()
        self.book['pages'].append(p)
        self.book['page_count'] = 2
        self.assertIn('source art duplicates', self.errors())

    def test_text_protected_overlap(self):
        self.page['protected_boxes'] = [[0.3, 0.8, 0.7, 0.9]]
        self.assertIn('overlaps protected', self.errors())

    def test_text_overflow(self):
        self.page['text_blocks'][0]['box'] = [0.2, 0.8, 0.97, 0.99]
        self.assertIn('outside region or safe', self.errors())

    def test_text_blocks_overlap(self):
        self.page['text'] = '玩具猫'
        self.page['text_blocks'].append(dict(text='猫', box=[0.4, 0.75, 0.8, 0.85]))
        self.assertIn('text blocks overlap', self.errors())

    def test_copy_and_layout(self):
        self.page['text'] = '改动后的文字'
        self.page['layout'] = 'split'
        self.assertIn('rendered copy differs', self.errors())
        self.assertIn('layout differs', self.errors())

    def test_changed_export_invalidates_review(self):
        Image.new('RGB', (100, 80), 'black').save(self.root / 'page.png')
        self.assertIn('stale', self.errors())

    def test_missing_and_wrong_dimensions(self):
        Image.new('RGB', (80, 100), 'white').save(self.root / 'page.png')
        self.assertIn('pixels', self.errors())
        (self.root / 'art.png').unlink()
        self.assertIn('unreadable image', self.errors())

    def test_repeated_plan_warning(self):
        self.book['pages'] = [copy.deepcopy(self.page) for _ in range(3)]
        result = validate(self.book, self.root)
        self.assertEqual(len(result['warnings']), 1)


if __name__ == '__main__':
    unittest.main()
