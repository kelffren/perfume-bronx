"""Apply the seven-scene cinema system to Yara Pink and Asad original.
Khamrah is built first. All product photos remain gated by media provenance.
"""
from pathlib import Path
import re,json,html
R=Path(__file__).resolve().parents[1]
MEDIA=json.loads((R/'assets/academy-media.json').read_text())
PRODUCTS={
 'yara':{
 'name':'Yara','variant':'Pink',
 'tag':['FLORAL & DULCE','FLORAL & SWEET'],
 'title':['Una faceta floral.<br>Un fondo dulce.','A floral facet.<br>A sweet base.'],
 'intro':['Mandarina, flores y notas tropicales se encuentran con vainilla, sándalo y almizcle. Conoce el perfil publicado de Yara Pink.','Tangerine, flowers and tropical notes meet vanilla, sandalwood and musk. Explore the published profile of Yara Pink.'],
 'motto':['Flores. Trópico. Vainilla.','Flowers. Tropics. Vanilla.'],
 'notes':[['Orquídea','Una referencia floral en la salida.','Orchid','A floral reference in the opening.','flower'],['Acorde tropical','Una impresión aromática, no una lista de frutas concretas.','Tropical accord','A scent impression, not a list of specific fruits.','tropical'],['Vainilla','Una faceta dulce en el fondo del perfume.','Vanilla','A sweet facet in the fragrance base.','vanilla']],
 'tiers':[['Mandarina · heliotropo · orquídea','Tangerine · heliotrope · orchid'],['Notas tropicales · acorde gourmand','Tropical notes · gourmand accord'],['Vainilla · sándalo · almizcle','Vanilla · sandalwood · musk']],
 'evolution':[['La apertura combina referencias cítricas y florales.','The opening combines citrus and floral references.'],['El corazón aporta facetas tropicales y gourmand.','The heart brings tropical and gourmand facets.'],['El fondo reúne vainilla, sándalo y almizcle.','The base brings together vanilla, sandalwood and musk.']],
 'compare_title':['Dos direcciones<br>para el dulzor.','Two directions<br>for sweetness.'],
 'profile':['Dulzor<br>floral','Floral<br>sweetness'],
 'question':['¿Qué faceta despierta tu curiosidad?','Which facet sparks your curiosity?'],
 'answers':[['Flores y notas tropicales','Explora Yara Pink: estas facetas aparecen en sus notas publicadas. Pruébalo cuando sea posible para conocer tu propia impresión.','Flowers and tropical notes','Explore Yara Pink: these facets appear in its published notes. Try it when possible to form your own impression.'],['Especias con dulzor','Compara Khamrah: su canela, dátiles y praliné ofrecen otro punto de partida dulce.','Spice with sweetness','Compare Khamrah: cinnamon, dates and praline offer a different sweet starting point.'],['Quiero comparar primero','Revisa ambos perfiles. Compartir vainilla no hace que huelan igual ni que ambos encajen contigo.','I want to compare first','Review both profiles. Sharing vanilla does not make them smell alike or guarantee both will suit you.']],
 'variant_note':['Confirma Yara Pink, la presentación rosa original. No asumas que las otras variantes de Yara tienen el mismo perfil.','Confirm Yara Pink, the original pink presentation. Do not assume other Yara variants have the same profile.']},
 'asad':{
 'name':'Asad','variant':'Original',
 'tag':['ESPECIAS & ÁMBAR','SPICE & AMBER'],
 'title':['El contraste<br>tiene carácter.','Contrast<br>has character.'],
 'intro':['Pimienta negra y tabaco. Un corazón con café, iris y pachulí. Una base ambarada y amaderada. Explora Asad original.','Black pepper and tobacco. A heart with coffee, iris and patchouli. An amber and woody base. Explore original Asad.'],
 'motto':['Pimienta. Café. Ámbar.','Pepper. Coffee. Amber.'],
 'notes':[['Pimienta negra','Una referencia especiada en la primera impresión.','Black pepper','A spicy reference in the opening impression.','pepper'],['Café','Una nota del corazón; no describe un ingrediente alimentario dentro del frasco.','Coffee','A heart note; not a claim about a food ingredient inside the bottle.','coffee'],['Ámbar','Una referencia cálida en una base con maderas y resinas.','Amber','A warm reference in a base with woods and resins.','amber']],
 'tiers':[['Pimienta negra · piña · tabaco','Black pepper · pineapple · tobacco'],['Café · iris · pachulí','Coffee · iris · patchouli'],['Ámbar · vainilla · maderas secas · benjuí · ládano','Amber · vanilla · dry woods · benzoin · labdanum']],
 'evolution':[['La primera impresión reúne pimienta negra, piña y tabaco.','The opening brings together black pepper, pineapple and tobacco.'],['El corazón incorpora café, iris y pachulí.','The heart includes coffee, iris and patchouli.'],['La base combina ámbar, vainilla, maderas secas y resinas.','The base combines amber, vanilla, dry woods and resins.']],
 'compare_title':['Especias.<br>Dos lecturas.','Spice.<br>Two interpretations.'],
 'profile':['Especias<br>y ámbar','Spice<br>and amber'],
 'question':['¿Qué contraste prefieres explorar?','Which contrast would you like to explore?'],
 'answers':[['Pimienta, café y maderas','Explora Asad original: esas referencias aparecen en sus notas publicadas. La experiencia real depende de tu percepción.','Pepper, coffee and woods','Explore original Asad: those references appear in its published notes. The actual experience depends on your perception.'],['Canela, dátiles y praliné','Compara Khamrah para explorar otra combinación de especias y dulzor.','Cinnamon, dates and praline','Compare Khamrah to explore another combination of spice and sweetness.'],['No lo sé todavía','Compara las notas y consulta si es posible probarlos antes de decidir. No elijas únicamente por popularidad.','I am not sure yet','Compare the notes and ask whether trying them is possible before deciding. Do not choose only by popularity.']],
 'variant_note':['Confirma Asad original, la presentación negra. Asad Zanzibar y otras variantes no son este mismo perfume.','Confirm original Asad, the black presentation. Asad Zanzibar and other variants are not the same fragrance.']}
}
for key,d in PRODUCTS.items():
 for lang in ['es','en']:
  es=lang=='es';idx=0 if es else 1
  def t(a,b):return a if es else b
  def e(s):return html.escape(s)
  f=R/lang/'academy'/key/'index.html'
  head=f.read_text().split('</head>')[0]
  head=re.sub(r'<link rel="stylesheet" href="/perfume-bronx/assets/academy-(?:deck|cinema|products).css">','',head)
  head+='<link rel="stylesheet" href="/perfume-bronx/assets/academy-cinema.css"><link rel="stylesheet" href="/perfume-bronx/assets/academy-products.css"></head>'
  original=(R/lang/'academy/khamrah/index.html').read_text().split('</head>')[1]
  body=original.replace('data-cinema="khamrah"',f'data-cinema="{key}"').replace('class="academy-cinema"',f'class="academy-cinema theme-{key}"').replace('/academy/khamrah/','/academy/'+key+'/')
  body=re.sub(r'<div class="cinema-intro">.*?</div>',f'<div class="cinema-intro"><p class="eyebrow">'+t('EL ATELIER DEL AROMA','THE SCENT ATELIER')+f'</p><h1>{d["name"]} <em>{d["variant"]}</em></h1><p>LATTAFA · {d["tag"][idx]}</p></div>',body,count=1)
  scenes=re.findall(r'<section id="scene-\d".*?</section>',body)
  def replace_scene(i,s):
   global body
   body=body.replace(scenes[i],s,1)
  s=scenes[0].replace(t('La calidez<br>tiene capas.','Warmth<br>has layers.'),d['title'][idx])
  s=re.sub(r'(<h2.*?</h2>)<p>.*?</p>',lambda m:m[1]+'<p>'+d['intro'][idx]+'</p>',s,count=1)
  s=s.replace('KHAMRAH',d['name'].upper()).replace(t('Especias. Dulzor. Calidez.','Spice. Sweetness. Warmth.'),d['motto'][idx])
  m=MEDIA[key]
  if m.get('approved'):
   if not m.get('rights_evidence') or not m.get('path') or not (R/m['path']).is_file():raise ValueError('Approved media needs local file and rights evidence')
   s=re.sub(r'<figure.*?</figure>',f'<figure class="product-stage"><img src="/perfume-bronx/{e(m["path"])}" alt="Lattafa {d["name"]} {d["variant"]}" width="720" height="900" fetchpriority="high"></figure>',s,count=1)
  replace_scene(0,s)
  cards=''
  for i,n in enumerate(d['notes']):
   name,desc=(n[0],n[1]) if es else (n[2],n[3])
   cards+=f'<details class="note-study"><summary><span class="note-drawing drawing-{n[4]}" aria-hidden="true"></span><span><small>0{i+1}</small><strong>{e(name)}</strong><span class="note-hint">'+t('Explorar +','Explore +')+f'</span></span></summary><p>{e(desc)}</p></details>'
  replace_scene(1,re.sub(r'<div class="note-gallery">.*</div></section>',lambda m:'<div class="note-gallery">'+cards+'</div></section>',scenes[1]))
  s=scenes[2]
  for i in range(3):
   s=re.sub(r'(<div id="tier-'+str(i)+r'".*?<h3>.*?</h3>)<p>.*?</p><p class="tier-explain">.*?</p>',lambda m:m[1]+f'<p>{e(d["tiers"][i][idx])}</p><p class="tier-explain">{e(d["evolution"][i][idx])}</p>',s,count=1)
  replace_scene(2,s)
  s=scenes[3];articles=re.findall(r'<article>.*?</article>',s)
  for i,article in enumerate(articles):s=s.replace(article,re.sub(r'<p>.*?</p>',lambda m:'<p>'+e(d['evolution'][i][idx])+'</p>',article))
  replace_scene(3,s)
  s=scenes[4]
  s=re.sub(r'(<h2[^>]*>).*?(</h2>)',lambda m:m[1]+d['compare_title'][idx]+m[2],s,count=1)
  pairs=f'<div class="contrast-pair"><article><small>01 / {d["name"].upper()}</small><h3>{d["profile"][idx]}</h3><p>{e(d["motto"][idx])}</p><span class="profile-line" aria-hidden="true"></span></article><article><small>02 / KHAMRAH</small><h3>'+t('Dulzor<br>especiado','Spiced<br>sweetness')+'</h3><p>'+t('Canela · dátiles · praliné','Cinnamon · dates · praline')+'</p><span class="profile-line" aria-hidden="true"></span></article></div>'
  s=re.sub(r'<div class="contrast-pair">.*</div></section>',lambda m:pairs+'</section>',s)
  replace_scene(4,s)
  quiz='<div class="preference-lab"><h3>'+e(d['question'][idx])+'</h3>'
  for a in d['answers']:
   title,desc=(a[0],a[1]) if es else (a[2],a[3])
   quiz+='<details class="choice"><summary>'+e(title)+'<span aria-hidden="true">↗</span></summary><p>'+e(desc)+'</p></details>'
  quiz+='</div>'
  replace_scene(5,re.sub(r'<div class="preference-lab">.*</div></section>',lambda m:quiz+'</section>',scenes[5]))
  s=scenes[6].replace('/products/khamrah/','/products/'+key+'/').replace(t('Consultar Khamrah','Ask about Khamrah'),t('Consultar ','Ask about ')+d['name'])
  s=re.sub(r'(<div class="closing-card">.*?<h3>.*?</h3>)<p>.*?</p>',lambda m:m[1]+'<p>'+e(d['variant_note'][idx])+'</p>',s)
  replace_scene(6,s)
  body=re.sub(r'(<footer class="cinema-footer">)<p>.*?</p>',lambda m:m[1]+'<p>'+t('Notas: ','Notes: ')+f'<a href="https://lattafa.com/product/{key}/">Lattafa {d["name"]}</a> · <a href="https://lattafa.com/product/khamrah/">Lattafa Khamrah</a>. '+t('Interpretación educativa. No es una prueba independiente.','Educational interpretation. Not an independent wear test.')+'</p>',body,count=1)
  f.write_text(head+body)
print('Built seven-scene Yara Pink and Asad ES/EN drafts')
