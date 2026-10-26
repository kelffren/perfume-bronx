"""Notify participating search engines after deployment, only for changed canonical pages.
Dry-run by default. No Google submission or indexing/ranking guarantee.
"""
import argparse, json, subprocess, time, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://kelffren.github.io/perfume-bronx/'
NS = '{http://www.sitemaps.org/schemas/sitemap/0.9}'

def changed_urls(since):
    names = subprocess.check_output(['git', 'diff', '--name-only', since, 'HEAD'], cwd=ROOT, text=True).splitlines()
    urls = [n.text for n in ET.parse(ROOT / 'sitemap.xml').iter(NS + 'loc')]
    return [u for u in urls if u.startswith(BASE) and u[len(BASE):] + 'index.html' in names]

def payload(urls):
    key = (ROOT / 'indexnow-key.txt').read_text().strip()
    assert len(key) == 32 and all(c in '0123456789abcdef' for c in key)
    assert all(u.startswith(BASE) and not urlsplit(u).query for u in urls)
    return {'host': urlsplit(BASE).netloc, 'key': key, 'keyLocation': BASE + 'indexnow-key.txt', 'urlList': urls}

def wait_for_publication(urls, seconds):
    deadline = time.monotonic() + seconds
    pending = list(urls)
    while pending:
        for url in pending[:]:
            expected = (ROOT / (url[len(BASE):] + 'index.html')).read_bytes()
            try:
                request = urllib.request.Request(url + '?indexnow_check=' + str(time.time_ns()), headers={'Cache-Control': 'no-cache'})
                with urllib.request.urlopen(request, timeout=15) as response:
                    if response.read() == expected:
                        pending.remove(url)
            except OSError:
                pass
        if not pending:
            return
        if time.monotonic() >= deadline:
            raise RuntimeError('Deployment not verified; no notification sent: ' + ', '.join(pending))
        print(f'Waiting for published content: {len(pending)} pages', flush=True)
        time.sleep(10)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--since', default='HEAD^')
    parser.add_argument('--submit', action='store_true')
    parser.add_argument('--wait-seconds', type=int, default=180)
    args = parser.parse_args()
    urls = changed_urls(args.since)
    if not urls:
        print('No changed canonical pages; nothing submitted.')
        return
    data = payload(urls)
    if not args.submit:
        print(json.dumps({'mode': 'dry-run', 'urls': urls}, indent=2))
        return
    wait_for_publication(urls, args.wait_seconds)
    # Prevent notifying before the ownership file is actually published.
    with urllib.request.urlopen(data['keyLocation'], timeout=30) as response:
        assert response.read().decode().strip() == data['key'], 'Published key mismatch'
    request = urllib.request.Request('https://api.indexnow.org/indexnow',
        data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(request, timeout=30) as response:
        assert response.status in (200, 202), response.status
        print(f'IndexNow HTTP {response.status}: {len(urls)} URLs received; indexing is NOT confirmed.')

if __name__ == '__main__':
    main()
