from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json, subprocess, tempfile, xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];BASE='https://kelffren.github.io/perfume-bronx/'
class Doc(HTMLParser):
 def __init__(self,s):super().__init__();self.tags=[];self.scripts=[];self.active=False;self.feed(s)
 def handle_starttag(self,t,a):
  a=dict(a);self.tags.append((t,a))
  if t=='script':self.active=not a.get('src');self.scripts.append([a.get('type'),''])
 def handle_data(self,s):
  if self.active:self.scripts[-1][1]+=s
 def handle_endtag(self,t):
  if t=='script':self.active=False
 def find(self,t,**kw):return [a for tag,a in self.tags if tag==t and all(a.get(k)==v for k,v in kw.items())]
def resolve(u):
 u=urlsplit(u)
 if u.netloc and u.netloc!='kelffren.github.io':return None
 p=u.path.removeprefix('/perfume-bronx/');return R/p/('index.html' if not Path(p).suffix else '')
urls=[n.text for n in ET.parse(R/'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert urls and len(urls)==len(set(urls))
assert all(u.startswith(BASE) and not urlsplit(u).query and not urlsplit(u).fragment for u in urls)
for url in urls:
 f=resolve(url);assert f.is_file();d=Doc(f.read_text());assert len(d.find('h1'))==1;assert d.find('link',rel='canonical')==[{'rel':'canonical','href':url}];assert len(d.find('meta',name='description'))==1
 for meta in d.find('meta'):
  if meta.get('name','').lower() in ('robots','googlebot'):
   assert 'noindex' not in meta.get('content','').lower(),url
 for tag in ('script','link'):
  for asset in d.find(tag):
   target=asset.get('src') if tag=='script' else (asset.get('href') if asset.get('rel')=='stylesheet' else None)
   if target and target.startswith('/perfume-bronx/'):
    assert resolve(target).is_file(),target
 if url!=BASE:
  for name in ('twitter:title','twitter:description','twitter:image'):
   assert len(d.find('meta',name=name))==1,(url,name)
  assert len(d.find('button',**{'class':'btn share-button'}))==1,url
 for typ,src in d.scripts:
  if typ=='application/ld+json':json.loads(src);assert 'aggregateRating' not in src and 'InStock' not in src
  elif src:
   with tempfile.NamedTemporaryFile(suffix='.js',mode='w') as t:t.write(src);t.flush();subprocess.run(['node','--check',t.name],check=True)
 if url==BASE:continue
 for a in d.find('a'):
  if a['href'].startswith('#'):continue
  f=resolve(a['href'])
  if f:assert f.is_file(),a
 alts=d.find('link',rel='alternate');assert {a['hreflang'] for a in alts}=={'en','es','x-default'}
 for a in alts:assert any(x['href']==url for x in Doc(resolve(a['href']).read_text()).find('link',rel='alternate'))
print(f'PASS: {len(urls)} URLs, H1, canonicals, metadata, reciprocal languages, links, JSON-LD and JS syntax')
