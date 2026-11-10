import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

SLUGS = {
    'spark-flame-zinc-beam', 'daisy-pilot-horizon-bay', 'lotus-comet-cap-fair',
    'quiet-quartz-amber-willow', 'earth-cherry-sage-reef', 'blend-spark-prism-stone',
    'clear-zenith-leaf-quiet', 'gold-charm-wolf-sapphire', 'eagle-zenith-sand-ruby',
    'otter-green-daisy-arrow', 'raven-fleet-hazel-eagle', 'storm-gold-trail-winter',
}


class AppsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_list = False
        self.items = []
        self.counts = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'ol' and attrs.get('id') == 'applist':
            self.in_list = True
        elif self.in_list and tag == 'li':
            self.items.append({'kind': attrs['data-kind']})
        elif self.in_list and tag == 'a':
            self.items[-1]['url'] = attrs['href'].rstrip('/')
        elif tag == 'button' and 'data-kind' in attrs:
            self.counts[attrs['data-kind']] = None
            self.button = attrs['data-kind']
        elif tag == 'span' and getattr(self, 'button', None):
            self.read_count = True

    def handle_data(self, data):
        if getattr(self, 'read_count', False) and data.strip().isdigit():
            self.counts[self.button] = int(data.strip())

    def handle_endtag(self, tag):
        if tag == 'ol' and self.in_list:
            self.in_list = False
        elif tag == 'button':
            self.button = None
        elif tag == 'span':
            self.read_count = False


class GrokAppsTest(unittest.TestCase):
    def test_new_urls_and_filter_counts(self):
        parser = AppsParser()
        parser.feed((Path(__file__).resolve().parents[1] / 'index.html').read_text())
        urls = [item['url'] for item in parser.items]
        for slug in SLUGS:
            self.assertEqual(urls.count(f'https://{slug}.grok.me'), 1, slug)
        counts = Counter(item['kind'] for item in parser.items)
        counts['all'] = len(parser.items)
        self.assertEqual(parser.counts, counts)


if __name__ == '__main__':
    unittest.main()
