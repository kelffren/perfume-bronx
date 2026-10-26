import importlib.util
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('indexnow','scripts/notify-indexnow.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with patch.object(m.subprocess,'check_output',return_value='es/products/yara/index.html\nREADME.md\nlegacy/index-v0.html\nassets/share.js\n'):
 assert m.changed_urls('HEAD^')==[m.BASE+'es/products/yara/']
with patch.object(m.subprocess,'check_output',return_value='README.md\n'):
 assert m.changed_urls('HEAD^')==[]
for urls in [['https://example.com/'],[m.BASE+'?name=private']]:
 try:m.payload(urls)
 except AssertionError:pass
 else:raise AssertionError('Out-of-scope URL accepted')
data=m.payload([m.BASE+'en/'])
assert data['keyLocation']==m.BASE+'indexnow-key.txt'
assert data['host']=='kelffren.github.io'
print('PASS: changed canonical pages only, no legacy/docs, host/path scope, no query strings')
