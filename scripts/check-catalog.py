"""Validate central catalogue integrity and its storefront projection."""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
data=json.loads((R/'data/catalog.json').read_text(encoding='utf-8'))
items=data['products']
assert len(items)==3 and {p['id'] for p in items}=={'yara','khamrah','asad'}
for p in items:
 assert p['name'].startswith('Lattafa ') and isinstance(p['price'],(int,float)) and p['price']>=0
 assert p['availability'] in ('unknown','in_stock','out_of_stock')
 assert p['price_status'] in ('site_displayed_unconfirmed','verified')
 assert all(p.get(k) for k in ('es','en','image','image_source','manufacturer_url'))
 assert all(p['notes'][l].get(k) for l in ('es','en') for k in ('top','heart','base'))
 assert p['tags']
html=(R/'index.html').read_text(encoding='utf-8')
match=re.search(r'const catalog=\[(.*?)\];\nconst bundles=',html,re.S)
assert match,'Missing storefront catalogue'
for p in items:
 assert 'id:"'+p['id']+'"' in match.group(1)
 assert 'price:'+str(p['price']) in match.group(1)
assert "fetch('/perfume-bronx/data/catalog.json')" in (R/'assets/scent-match.js').read_text(encoding='utf-8')
print('Central catalogue validated: 3 products, bilingual notes, storefront and Scent Match')
