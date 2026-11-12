import unittest
from datetime import datetime
from pathlib import Path

from test_cool_tech import IndexParser

ROOT = Path(__file__).resolve().parents[1]


def parse():
    parser = IndexParser()
    parser.feed((ROOT / 'index.html').read_text(encoding='utf-8'))
    return parser


class ProjectsTest(unittest.TestCase):
    def test_every_project_has_roll_item_and_shot(self):
        parser = parse()
        keys = [p['data-k'] for p in parser.projects]
        self.assertEqual(sorted(keys), sorted(parser.roll))  # 1:1, the ping callback needs it
        for k in keys:
            self.assertEqual(parser.roll.count(k), 1, k)
            self.assertIn(f'shots/{k}.jpg', parser.images)
            self.assertTrue((ROOT / 'shots' / f'{k}.jpg').is_file(), k)

    def test_project_data_attrs_valid(self):
        for p in parse().projects:
            self.assertTrue(p['data-url'].startswith('https://'), p['data-k'])
            datetime.fromisoformat(p['data-push'])  # raises if not ISO-8601


if __name__ == '__main__':
    unittest.main()
