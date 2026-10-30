from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
base = 'https://kelffren.github.io/perfume-bronx/'
ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'

class Parser(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.links = []
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href')
            if href:
                self.links.append(href)

def path_of(url):
    parsed = urlsplit(url)
    if parsed.netloc and parsed.netloc != 'kelffren.github.io':
        return None
    if not parsed.path.startswith('/perfume-bronx/'):
        return None
    return parsed.path.removeprefix('/perfume-bronx/').rstrip('/')

def file_of(path):
    p = root / path
    return p if p.suffix else p / 'index.html'

urls = [n.text for n in ET.parse(root / 'sitemap.xml').iter(ns + 'loc')]
pages = {path_of(url) for url in urls}
errors = []
if len(pages) != len(urls) or None in pages:
    errors.append('Duplicate or external sitemap URLs')
edges = {}
for page in sorted(pages - {None}):
    f = file_of(page)
    if not f.is_file():
        errors.append('Missing sitemap page: ' + page)
        continue
    edges[page] = set()
    for href in Parser(f.read_text(encoding='utf-8')).links:
        dest = path_of(href)
        if dest is not None:
            if not file_of(dest).is_file():
                errors.append('Broken link: ' + page + ' -> ' + dest)
            else:
                edges[page].add(dest)
reachable = {''}
pending = ['']
while pending:
    for dest in edges.get(pending.pop(), ()):
        if dest in pages and dest not in reachable:
            reachable.add(dest)
            pending.append(dest)
for page in sorted(pages - reachable - {None}):
    errors.append('Orphaned from homepage: ' + page)
for lang, slugs in [('es', ('vainilla','especiados','ambarados')), ('en', ('vanilla','spicy','amber'))]:
    hub = lang
    for slug in slugs:
        dest = lang + '/notes/' + slug
        if dest not in edges.get(hub, set()):
            errors.append('Missing note hub link: ' + dest)
    if lang + '/compare' not in edges.get(hub, set()):
        errors.append('Missing comparator hub link: ' + lang)
print('Pages:', len(pages), 'Reachable:', len(reachable))
for error in errors:
    print('FAIL:', error)
if errors:
    raise SystemExit(1)
print('PASS: Internal links and discovery')
