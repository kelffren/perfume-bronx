"""Recompose both Academy directories; preserve existing tools and crawlable explanations."""
from pathlib import Path
import re,json
R=Path(__file__).resolve().parents[1]
lessons=json.loads((R/'scripts/academy-lessons.json').read_text())
for lang in ['es','en']:
 es=lang=='es'
 def t(a,b):return a if es else b
 f=R/lang/'academy/index.html';s=f.read_text()
 if 'academy-hub.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="/perfume-bronx/assets/academy-hub.css"></head>')
 s=s.replace('<body>','<body class="academy-hub">')
 intro='<div class="intro hub-intro"><p class="eyebrow">OUD BRONX ACADEMY</p><h1>'+t('El arte de<br>elegir tu aroma.','The art of<br>finding your scent.')+'</h1><p class="lead">'+t('Tres perfumes. Ocho clases. Aprende a reconocer lo que te gusta y a preguntar lo que importa.','Three fragrances. Eight lessons. Learn to recognise what you enjoy and ask what matters.')+'</p><a class="hub-start" href="#presentations">'+t('Explorar los perfumes ↗','Explore the fragrances ↗')+'</a><a class="hub-secondary" href="#lessons">'+t('Elegir una clase','Choose a lesson')+'</a></div>'
 # Capture tools from the current or already-generated page; generation remains repeatable.
 showcase=re.search(r'<section class="academy-showcase".*?</section>',s).group(0)
 showcase=re.sub(r'<img[^>]*>', '',showcase)
 showcase=showcase.replace(' id="presentations"','')
 for key,name,label in [('yara','Yara Pink',t('FLORAL · TROPICAL','FLORAL · TROPICAL')),('khamrah','Khamrah',t('ESPECIAS · DULZOR','SPICE · SWEETNESS')),('asad','Asad',t('ESPECIAS · ÁMBAR','SPICE · AMBER'))]:
  pattern=r'(<article class="coverflow-card" data-perfume="'+key+r'">)(?:<div class="hub-profile".*?</div>)?'
  showcase=re.sub(pattern,lambda m:m[1]+'<div class="hub-profile" aria-hidden="true"><span>'+label+'</span><strong>'+name+'</strong><i></i></div>',showcase)
 showcase=showcase.replace('class="academy-showcase"','class="academy-showcase" id="presentations"')
 showcase=re.sub(r'<h2>.*?</h2>',lambda m:'<h2>'+t('Tres perfiles.<br>Tu punto de partida.','Three profiles.<br>Your starting point.')+'</h2>',showcase,count=1)
 directory='<section class="hub-lessons" id="lessons"><p class="eyebrow">'+t('APRENDER PARA ELEGIR','LEARN TO CHOOSE')+'</p><h2>'+t('Un criterio nuevo<br>en cada clase.','A fresh insight<br>in every lesson.')+'</h2><div class="lesson-directory">'
 for i,key in enumerate(['notes','authenticity','concentration','longevity','oud','care','occasions','gifts']):
  directory+=f'<a href="/perfume-bronx/{lang}/academy/{key}/"><span>{i+1:02d}</span><strong>{lessons[key][lang]["title"]}</strong><small>'+t('Explorar + practicar','Explore + practise')+'</small><b aria-hidden="true">↗</b></a>'
 directory+='</div></section>'
 start=s.index('<main class="wrap">');end=s.index('<nav class="academy-jump"',start)
 old=s[start:end]
 # Preserve the functional comparison tool (checkboxes/columns).
 comparison=next((x for x in re.findall(r'<section\b.*?</section>',old) if 'data-compare-check' in x),'')
 s=s[:start]+'<main class="wrap">'+intro+showcase+directory+comparison+s[end:]
 # Fix a pre-existing fragment of answer without its question.
 s=s.replace('<h2>Autenticidad y compra segura</h2><p>No.', '<h2>Autenticidad y compra segura</h2><p>¿Un QR basta para demostrar autenticidad? No.')
 # Preserve old anchor content while making secondary topics intentional disclosures.
 for key in ['dictionary','auth','gifts','local','wear','season','video','questions']:
  pat=r'<section class="reading" id="'+key+r'"><h2>(.*?)</h2>(.*?)</section>'
  s=re.sub(pat,lambda m:f'<details class="hub-topic" id="{key}"><summary>{m[1]}<span aria-hidden="true">+</span></summary><div>{m[2]}</div></details>',s)
 if 'academy-hub.js' not in s:s=s.replace('</body>','<script src="/perfume-bronx/assets/academy-hub.js" defer></script></body>')
 # The existing guide links labelled Academy incorrectly pointed to the general language hub.
 s=s.replace(f'href="/perfume-bronx/{lang}/">Academia',f'href="/perfume-bronx/{lang}/academy/">Academia')
 f.write_text(s)
print('Built bilingual Academy directory and preserved existing tools')
