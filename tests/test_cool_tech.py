import unittest
from html.parser import HTMLParser
from pathlib import Path


class IndexParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.projects = []
        self.roll = []
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'article' and 'project' in (attrs.get('class') or '').split():
            self.projects.append(attrs)
        if tag == 'li' and 'data-k' in attrs:
            self.roll.append(attrs['data-k'])
        if tag == 'a':
            self.links.append(attrs.get('href'))
        if tag == 'img':
            self.images.append(attrs.get('src'))


class CoolTechIndexTest(unittest.TestCase):
    def test_cool_tech_is_a_project_with_a_roll_call_link_and_screenshot(self):
        root = Path(__file__).resolve().parents[1]
        parser = IndexParser()
        parser.feed((root / 'index.html').read_text(encoding='utf-8'))
        projects = [p for p in parser.projects if p.get('data-k') == 'cool-tech']
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0].get('data-url'), 'https://priestkos-cool-tech.pages.dev/')
        self.assertEqual(parser.roll.count('cool-tech'), 1)
        self.assertIn('https://priestkos-cool-tech.pages.dev/', parser.links)
        self.assertIn('https://github.com/priestkos/cool-tech', parser.links)
        self.assertIn('shots/cool-tech.jpg', parser.images)
        self.assertTrue((root / 'shots/cool-tech.jpg').is_file())
        self.assertEqual(len(parser.projects), len(parser.roll))


if __name__ == '__main__':
    unittest.main()
