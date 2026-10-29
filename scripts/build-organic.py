"""Build twelve curated EN/ES pages; run with Python 3, no dependencies.
Manufacturer notes verified at lattafa.com/product/{yara,khamrah,asad}/ on 2026-10-25.
Prices and stock intentionally omitted until merchant confirmation.
"""
import json,re
from pathlib import Path
from html import escape as e
R=Path(__file__).resolve().parents[1]
BASE='https://kelffren.github.io/perfume-bronx/'
PREFIX='/perfume-bronx/'
# Single source of truth for storefront products. Keep the synchronous inline array
# for GitHub Pages and the existing cart; regenerate it from structured JSON.
CATALOG=json.loads((R/'data/catalog.json').read_text(encoding='utf-8'))
assert CATALOG['version']==1 and len(CATALOG['products'])>=3
products=CATALOG['products']
assert len({p['id'] for p in products})==len(products)
for product in products:
 assert product['id'] and product['name'] and product['price']>=0
 assert product['availability'] in ('unknown','in_stock','out_of_stock')
assert {p['id'] for p in products}=={'yara','khamrah','asad'}, 'Current cart/bundles support exactly three products'
storefront=[{key:p[key] for key in ('id','name','price','es','en')} | {'image':p['image'],'source':p['image_source']} for p in products]
index_path=R/'index.html'
raw_home=index_path.read_text(encoding='utf-8')
def js_obj(obj):
 return '{'+','.join(k+':'+json.dumps(v,ensure_ascii=False,separators=(',',':')) for k,v in obj.items())+'}'
pattern=r'const catalog=\[\{id:"yara".*?\}\];\nconst bundles='
replacement='const catalog=['+','.join(js_obj(p) for p in storefront)+'];\nconst bundles='
new_home,count=re.subn(pattern,lambda _:replacement,raw_home,count=1,flags=re.S)
if count!=1:raise ValueError('Storefront catalogue anchor not found; refusing to change cart')
if new_home!=raw_home:index_path.write_text(new_home,encoding='utf-8')
home=new_home
photos={p['id']:p['image'] for p in products}
DATA={
 'yara':{
 'es':['Vainilla · Floral · Tropical','Mandarina, heliotropo y orquídea','Acordes tropicales y gourmand','Vainilla, sándalo y almizcle','Empieza por Yara si buscas una combinación floral y dulce. Pregunta por el original: compartir nombre con otras versiones no significa compartir aroma.','Si prefieres evitar el dulzor, compara antes de elegir. Describe un perfume que te guste y uno que no; esa información ayuda más que pedir simplemente «el mejor».'],
 'en':['Vanilla · Floral · Tropical','Tangerine, heliotrope and orchid','Tropical and gourmand accords','Vanilla, sandalwood and musk','Start with Yara if you want a floral and sweet combination. Ask for the original: sharing a name with other versions does not mean sharing a scent.','If you avoid sweet accords, compare before choosing. Name one fragrance you enjoy and one you dislike; that is more useful than simply asking for “the best.”']},
 'khamrah':{
 'es':['Canela · Dátiles · Vainilla','Bergamota, canela y nuez moscada','Acorde de dátiles, praliné y flores','Vainilla, tonka, maderas ambaradas y resinas','Explora Khamrah si te atraen las especias con dulzor. Piensa en si quieres ese tipo de aroma para tu rutina o para una ocasión concreta.','Si buscas un perfume principalmente cítrico y ligero, no elijas solo por la popularidad del nombre. Compara el perfil y, cuando puedas, pruébalo antes de comprar un frasco.'],
 'en':['Cinnamon · Dates · Vanilla','Bergamot, cinnamon and nutmeg','Date accord, praline and florals','Vanilla, tonka, amber woods and resins','Explore Khamrah if you enjoy spice with sweetness. Consider whether you want that scent profile for your routine or a particular occasion.','If you want a primarily light citrus fragrance, do not choose by the popularity of the name alone. Compare the profile and, where possible, try it before buying a bottle.']},
 'asad':{
 'es':['Pimienta · Café · Ámbar','Pimienta negra, piña y tabaco','Café, iris y pachulí','Ámbar, vainilla, maderas secas y resinas','Explora Asad si buscas especias y un fondo ambarado. Explica si quieres llevarlo en espacios compartidos o en salidas; tu contexto importa tanto como las notas.','Si no disfrutas las especias o el tabaco en una descripción olfativa, compara con Yara y Khamrah. Una referencia a otro perfume no garantiza que te guste este.'],
 'en':['Pepper · Coffee · Amber','Black pepper, pineapple and tobacco','Coffee, iris and patchouli','Amber, vanilla, dry woods and resins','Explore Asad if you want spice and an amber base. Say whether you plan to wear it in shared spaces or on outings; context matters alongside notes.','If you do not enjoy spice or tobacco in a scent description, compare Yara and Khamrah. A comparison with another perfume does not guarantee you will like this one.']}}
COPY={
 'es':{'store':'Tienda','guide':'Guía de perfumes','compare':'Yara vs Khamrah vs Asad: elige por aroma','local':'Perfumes árabes en el Bronx: guía de compra local','hub':'Guías de perfumes árabes para el Bronx','inquire':'Preparar consulta →','status':'Confirma precio actual, existencias, tamaño y entrega antes de pagar.','delivery':'Indica nombre completo del perfume, cantidad y ZIP. Confirma el total final y la franja de entrega. Una unidad tiene tarifa de entrega por confirmar; desde dos unidades, delivery gratis dentro de la cobertura confirmada.','disclaimer':'Las notas proceden del fabricante; las recomendaciones son interpretación editorial de OUD BRONX, no reseñas de clientes ni pruebas personales de uso. Consulta: 25 de octubre de 2026.','sources':'Fuentes y criterio editorial','notes':'Notas seleccionadas del fabricante','fit':'¿Encaja contigo?','before':'Antes de pedir en el Bronx','duration':'¿Cuánto dura?','duration_text':'No prometemos un número de horas. La piel, la aplicación y las condiciones influyen. No hemos realizado una prueba controlada de duración; elige por preferencias y no por una cifra sin verificar.','next':'Compara antes de elegir'},
 'en':{'store':'Store','guide':'Fragrance guide','compare':'Yara vs Khamrah vs Asad: choose by scent','local':'Arabian perfumes in the Bronx: local ordering guide','hub':'Arabian perfume guides for the Bronx','inquire':'Prepare inquiry →','status':'Confirm current price, stock, bottle size and delivery before paying.','delivery':'Share the full fragrance name, quantity and ZIP code. Confirm the final total and delivery window. Delivery for one bottle has a fee to confirm; free delivery starts at two bottles within confirmed service areas.','disclaimer':'Notes come from the manufacturer; recommendations are editorial interpretation by OUD BRONX, not customer reviews or personal wear tests. Checked October 25, 2026.','sources':'Sources and editorial approach','notes':'Selected manufacturer notes','fit':'Is it for you?','before':'Before ordering in the Bronx','duration':'How long does it last?','duration_text':'There is no guaranteed number of hours here. Skin, application and conditions affect the experience. We have not conducted a controlled wear test; choose by preferences rather than an unverified duration claim.','next':'Compare before choosing'}}
pages=[]
def path(lang,slug=''):return lang+'/'+(slug.strip('/')+'/' if slug else '')
def link(dest,text,cls=''):return f'<a class="{cls}" href="{e(PREFIX+dest)}">{e(text)}</a>'
def p(text):return '<p>'+e(text)+'</p>'
def section(title,body):return '<section class="reading"><h2>'+e(title)+'</h2>'+body+'</section>'
def cards(lang):return '<div class="cards">'+''.join('<article>'+link(path(lang,'products/'+k),'Lattafa '+k.title(),'card-title')+p(d[lang][0])+'</article>' for k,d in DATA.items())+'</div>'
def sources(lang,keys):return p(COPY[lang]['disclaimer'])+'<p>'+' · '.join(f'<a href="https://lattafa.com/product/{k}/">Lattafa {k.title()}</a>' for k in keys)+'</p>'
def shell(lang,slug,title,desc,body,key=None):
 dest=path(lang,slug);other=path('en' if lang=='es' else 'es',slug);c=COPY[lang];image=photos[key] if key else BASE+'assets/hero-poster.jpg'
 page={'@type':'WebPage','@id':BASE+dest+'#page','name':title,'url':BASE+dest,'description':desc,'inLanguage':lang}
 if key:page['mainEntity']={'@type':'Product','name':'Lattafa '+key.title(),'brand':{'@type':'Brand','name':'Lattafa'},'image':image,'description':DATA[key][lang][0],'url':BASE+dest}
 schema={'@context':'https://schema.org','@graph':[page,{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'OUD BRONX','item':BASE},{'@type':'ListItem','position':2,'name':title,'item':BASE+dest}]}]}
 html=f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | OUD BRONX</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{BASE+dest}">
<link rel="alternate" hreflang="es" href="{BASE+path('es',slug)}"><link rel="alternate" hreflang="en" href="{BASE+path('en',slug)}"><link rel="alternate" hreflang="x-default" href="{BASE+path('en',slug)}">
<meta property="og:type" content="website"><meta property="og:site_name" content="OUD BRONX"><meta property="og:locale" content="{lang}_US"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{BASE+dest}"><meta property="og:image" content="{e(image)}"><meta property="og:image:alt" content="{e(title)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{e(image)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet"><link rel="stylesheet" href="{PREFIX}assets/organic.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head>
<body><a class="skip" href="#content">{'Ir al contenido' if lang=='es' else 'Skip to content'}</a><header><nav class="wrap" aria-label="{'Navegación principal' if lang=='es' else 'Main navigation'}">{link('','OUD BRONX','brand')}<div>{link(path(lang),c['guide'])}{link(other,'English' if lang=='es' else 'Español')}</div></nav></header><main id="content"><div class="wrap breadcrumb">{link('',c['store'])} / {link(path(lang),c['guide'])}</div>{body}<section class="wrap reading share-tools" aria-label="{'Compartir' if lang=='es' else 'Share'}"><button type="button" class="btn share-button" hidden>{'Compartir esta guía' if lang=='es' else 'Share this guide'}</button><p class="small" role="status" aria-live="polite" id="share-status"></p><a class="share-url" href="{BASE+dest}">{'Enlace de esta guía' if lang=='es' else 'Link to this guide'}</a></section></main><script src="{PREFIX}assets/share.js" defer></script>
<footer class="wrap"><p class="brand">OUD BRONX</p><p>Bronx · New York</p><nav>{link(path(lang,'compare/yara-khamrah-asad'),c['compare'])}{link(path(lang,'bronx-delivery'),c['local'])}{link('',c['store'])}</nav><p class="small">© 2026 OUD BRONX</p></footer></body></html>'''
 f=R/dest/'index.html';f.parent.mkdir(parents=True,exist_ok=True);f.write_text(html);pages.append((dest,photos[key] if key else None))
for lang in COPY:
 en=lang=='en';c=COPY[lang]
 for key,d in DATA.items():
  info=d[lang];name='Lattafa '+key.title();title=name+(': notes and buying guide in the Bronx' if en else ': notas y guía de compra en el Bronx')
  desc=(f'Explore {name}: {info[0]}. Compare the original fragrance and prepare a local delivery inquiry.' if en else f'Conoce {name}: {info[0]}. Compara el perfume original y prepara tu consulta de entrega local.')
  body=f'<section class="wrap product"><figure><img src="{e(photos[key])}" width="512" height="512" alt="{name}" fetchpriority="high"><figcaption>'+('Reference image from the existing catalogue; actual packaging may differ.' if en else 'Imagen de referencia del catálogo; el empaque real puede variar.')+'</figcaption></figure><div><p class="eyebrow">LATTAFA · THE ORIGINAL EDIT</p><h1>'+name+'</h1><p class="lead">'+info[0]+'</p>'+p('Ask for the original version and confirm the bottle size before ordering.' if en else 'Consulta por la versión original y confirma el tamaño del frasco antes de pedir.')+'<p class="availability">'+c['status']+'</p>'+link('?product='+key+'&intent=inquiry&lang='+lang+'#collection',c['inquire'],'btn')+'<p class="small">'+('Continue to the store with this fragrance selected. No online payment.' if en else 'Continúa en la tienda con este perfume seleccionado. Sin pago online.')+'</p></div></section><div class="wrap">'
  body+=section(c['notes'],'<dl>'+''.join('<div><dt>'+a+'</dt><dd>'+e(b)+'</dd></div>' for a,b in zip(['Top','Heart','Base'] if en else ['Salida','Corazón','Fondo'],info[1:4]))+'</dl>'+p('These describe the scent, not the ingredient list.' if en else 'Describen el aroma, no la lista de ingredientes.'))
  body+=section(c['fit'],p(info[4])+p(info[5]))+section(c['before'],p(c['delivery']))+section(c['duration'],p(c['duration_text']))+section(c['sources'],sources(lang,[key]))+section(c['next'],cards(lang)+link(path(lang,'compare/yara-khamrah-asad'),c['compare']))+'</div>'
  body=body.replace('</div>',section('Comparador interactivo' if not en else 'Interactive comparison',link(path(lang,'compare'),'Comparar Yara, Khamrah y Asad' if not en else 'Compare Yara, Khamrah and Asad'))+'</div>',1)
  # Contextual links to reviewed note-family guides; no invented scent attributes.
  NOTE_LINKS={
   'es':{'yara':('vainilla',),'khamrah':('vainilla','especiados','ambarados'),'asad':('especiados','ambarados')},
   'en':{'yara':('vanilla',),'khamrah':('vanilla','spicy','amber'),'asad':('spicy','amber')}
  }
  NOTE_LABELS={'es':{'vainilla':'Perfumes árabes con vainilla','especiados':'Perfumes árabes especiados','ambarados':'Perfumes árabes ambarados'},'en':{'vanilla':'Arabian perfumes with vanilla','spicy':'Spicy Arabian perfumes','amber':'Amber Arabian perfumes'}}
  related=''.join('<li>'+link(path(lang,'notes/'+slug),NOTE_LABELS[lang][slug])+'</li>' for slug in NOTE_LINKS[lang][key])
  body+=section('Explora por notas olfativas' if not en else 'Explore by scent notes','<ul>'+related+'</ul>')
  shell(lang,'products/'+key,title,desc,body,key)
 title=c['compare'];desc='Compare three Lattafa originals by notes, preferences and buying questions.' if en else 'Compara tres originales de Lattafa según notas, preferencias y preguntas de compra.'
 body='<div class="wrap"><section class="intro"><p class="eyebrow">THE OUD BRONX GUIDE</p><h1>'+title+'</h1>'+p('Choose the scent direction first, then confirm the version and your delivered total. None is automatically best for everyone.' if en else 'Elige primero la dirección del aroma; después confirma la versión y el total con entrega. Ninguno es automáticamente el mejor para todos.')+'</section>'
 body+=section('A useful starting point' if en else 'Un punto de partida útil','<div class="table-scroll" tabindex="0" role="region" aria-label="'+e(title)+'"><table><caption>'+title+'</caption><thead><tr><th scope="col">Perfume</th><th scope="col">'+('Profile' if en else 'Perfil')+'</th><th scope="col">'+('Consider it if…' if en else 'Considéralo si…')+'</th></tr></thead><tbody>'+''.join('<tr><th scope="row">'+link(path(lang,'products/'+k),k.title())+'</th><td>'+d[lang][0]+'</td><td>'+d[lang][4]+'</td></tr>' for k,d in DATA.items())+'</tbody></table></div>')
 questions=['Do you prefer floral sweetness, spiced sweetness or peppery amber? Start with Yara, Khamrah or Asad respectively and compare the full notes.','Where will you wear it? Explain the setting and whether you prefer a discreet or noticeable presence. Notes alone do not establish projection.','Is it for you or a gift? Ask what the recipient already wears before choosing an unfamiliar fragrance.'] if en else ['¿Prefieres dulzor floral, dulzor especiado o ámbar con pimienta? Empieza por Yara, Khamrah o Asad, respectivamente, y compara las notas completas.','¿Dónde lo usarás? Explica el contexto y si buscas presencia discreta o perceptible. Las notas por sí solas no establecen la proyección.','¿Es para ti o para regalar? Averigua qué usa ya esa persona antes de elegir un aroma desconocido.']
 body+=section('Three questions to narrow the choice' if en else 'Tres preguntas para decidir','<ol>'+''.join('<li>'+e(x)+'</li>' for x in questions)+'</ol>')
 body+=section('What this guide does not claim' if en else 'Qué no afirma esta guía',p('This is not a wear test, sales ranking or guarantee of similarity to a designer fragrance. A shared note does not imply an identical formula. We do not assign invented longevity scores or customer ratings.' if en else 'No es una prueba de uso, un ranking de ventas ni una garantía de parecido con un perfume de diseñador. Compartir una nota no implica fórmulas idénticas. No asignamos puntuaciones de duración ni valoraciones inventadas.'))
 body+=section('Buying two fragrances' if en else 'Si eliges dos perfumes',p('Choose two scents you actually want rather than adding a bottle solely for delivery. Ask the store to confirm bundle eligibility, current price and your ZIP code before agreeing to an order.' if en else 'Elige dos aromas que realmente quieras, en vez de añadir un frasco solo por la entrega. Consulta combinaciones, precio actual y cobertura de tu ZIP antes de acordar un pedido.'))
 body+=section(c['next'],cards(lang))+section(c['sources'],sources(lang,DATA))+'</div>';shell(lang,'compare/yara-khamrah-asad',title,desc,body)
 title=c['local'];desc='Confirm your ZIP code, delivery cost and order details before paying.' if en else 'Confirma tu ZIP, el costo de entrega y los detalles del pedido antes de pagar.'
 body='<div class="wrap"><section class="intro"><p class="eyebrow">OUD BRONX · NEW YORK</p><h1>'+title+'</h1>'+p('A local order starts with knowing which bottle you want and the delivered total. Prepare these questions without committing to a purchase.' if en else 'Un pedido local empieza por saber qué frasco quieres y cuánto pagarás con la entrega. Prepara estas preguntas sin comprometerte a comprar.')+'</section>'
 body+=section('Confirm delivery before making plans' if en else 'Confirma la entrega antes de hacer planes',p('Send your ZIP code and quantity first. Bronx, Yonkers and Westchester are areas to ask about, not guaranteed coverage for every address. Do not assume same-day delivery or a fixed arrival time; wait for confirmation of availability, route and delivery window.' if en else 'Indica primero ZIP y cantidad. Bronx, Yonkers y Westchester son zonas por las que puedes consultar, no cobertura garantizada para todas las direcciones. No presupongas entrega el mismo día ni una hora fija; espera confirmación de disponibilidad, ruta y franja.'))+section('One bottle or two?' if en else '¿Uno o dos frascos?',p(c['delivery']))
 checklist=['Exact name and variant, bottle size and quantity.','Current stock and a photo of the actual bottle and packaging if you need to verify what you will receive.','Final total, delivery fee or free-delivery eligibility, and delivery window.','Payment method and how to report a problem. Confirm before paying; this page does not establish a returns policy.'] if en else ['Nombre y variante exactos, tamaño del frasco y cantidad.','Existencias actuales y foto del frasco y empaque reales si necesitas verificar qué recibirás.','Total final, tarifa o condiciones de entrega gratis y franja acordada.','Método de pago y cómo comunicar una incidencia. Confírmalo antes de pagar; esta página no establece una política de devoluciones.']
 body+=section('Pre-order checklist' if en else 'Lista antes de pedir','<ol>'+''.join('<li>'+e(x)+'</li>' for x in checklist)+'</ol>')+section(c['next'],cards(lang))
 body+=section(c['inquire'].replace(' →',''),p('An inquiry is not a paid order. Share a full address only when needed to arrange delivery.' if en else 'Una consulta no es un pedido pagado. Comparte la dirección completa solo cuando sea necesaria para coordinar la entrega.')+link('?lang='+lang+'#collection',c['store'],'btn'))+'</div>';shell(lang,'bronx-delivery',title,desc,body)
 title=c['hub'];desc='Explore Yara, Khamrah and Asad, compare notes and prepare your local order with OUD BRONX.' if en else 'Explora Yara, Khamrah y Asad, compara notas y prepara tu pedido local con OUD BRONX.'
 body='<div class="wrap"><section class="intro"><p class="eyebrow">THE OUD BRONX GUIDE</p><h1>'+title+'</h1>'+p(desc)+'</section>'+section('Meet the fragrances' if en else 'Conoce los perfumes',cards(lang))+section('Make an informed choice' if en else 'Elige con información','<div class="cards"><article>'+link(path(lang,'compare/yara-khamrah-asad'),c['compare'],'card-title')+'</article><article>'+link(path(lang,'bronx-delivery'),c['local'],'card-title')+'</article></div>')+'</div>';shell(lang,'',title,desc,body)
# Initial catalogue works without JS; enhanced buttons replace it when JS runs.
static=[]
for i,(k,d) in enumerate(DATA.items(),1):
 price=re.search(r'id:"'+k+r'",name:"[^"]+",price:(\d+)',home).group(1)
 static.append(f'<article class="tile"><div class="art product-photo"><img src="{e(photos[k])}" alt="Lattafa {k.title()}" loading="lazy" decoding="async" width="512" height="512"><small>Foto de referencia</small></div><div class="content"><div class="eyebrow">OUD BRONX · 0{i}</div><h3><a href="es/products/{k}/">Lattafa {k.title()}</a></h3><p class="muted">{d["es"][0]}</p><div class="price">${price}</div><a class="btn" href="es/products/{k}/">Ver notas y detalles →</a></div></article>')
fragment='<!-- organic-catalog:start -->'+''.join(static)+'<!-- organic-catalog:end -->'
if '<!-- organic-catalog:start -->' in home:home=re.sub(r'<!-- organic-catalog:start -->.*?<!-- organic-catalog:end -->',lambda m:fragment,home,flags=re.S)
else:home=home.replace('<div class="grid" id="products"></div>','<div class="grid" id="products">'+fragment+'</div>')
(R/'index.html').write_text(home)
xml=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',f'<url><loc>{BASE}</loc></url>']
for dest,image in pages:xml.append(f'<url><loc>{BASE+dest}</loc>'+(f'<image:image><image:loc>{e(image)}</image:loc></image:image>' if image else '')+'</url>')
(R/'sitemap.xml').write_text('\n'.join(xml+['</urlset>'])+'\n')
# Preserve and index independently authored editorial articles.
# Discover articles on disk rather than hard-coding a list. Each article is a
# reviewed static HTML file, never generated from a keyword-only template.
from html.parser import HTMLParser
class ArticleTitle(HTMLParser):
 def __init__(self):
  super().__init__();self.inside=False;self.title=''
 def handle_starttag(self,tag,attrs):
  if tag=='h1':self.inside=True
 def handle_endtag(self,tag):
  if tag=='h1':self.inside=False
 def handle_data(self,data):
  if self.inside:self.title+=data

article_urls=[]
for lang in ('es','en'):
 cards_html=[]
 for article in sorted((R/lang/'articles').glob('*/index.html')):
  parser=ArticleTitle();parser.feed(article.read_text(encoding='utf-8'))
  if not parser.title.strip():
   raise ValueError(f'Article missing H1: {article}')
  relative=article.parent.relative_to(R).as_posix()+'/'
  article_urls.append(BASE+relative)
  cards_html.append('<article>'+link(relative,parser.title.strip(),'card-title')+'</article>')
 if cards_html:
  hub=R/lang/'index.html'
  content=hub.read_text(encoding='utf-8')
  section_title='Tutoriales de perfumes' if lang=='es' else 'Perfume tutorials'
  section_html=section(section_title,'<div class="cards">'+''.join(cards_html)+'</div>')
  anchor='<section class="reading"><h2>'+('Elige con información' if lang=='es' else 'Make an informed choice')+'</h2>'
  if anchor not in content:raise ValueError(f'Missing guide hub anchor: {hub}')
  content=content.replace(anchor,section_html+anchor,1)
  hub.write_text(content,encoding='utf-8')
if article_urls:
 sitemap=R/'sitemap.xml'
 xml=sitemap.read_text(encoding='utf-8')
 xml=xml.replace('</urlset>',''.join('<url><loc>'+e(url)+'</loc></url>\n' for url in article_urls)+'</urlset>')
 sitemap.write_text(xml,encoding='utf-8')
# Preserve reviewed authenticity guides, which are authored independently of the catalogue generator.
for lang in ('es','en'):
 hub=R/lang/'index.html'
 content=hub.read_text(encoding='utf-8')
 slugs=('how-to-tell-if-perfume-is-original','verify-lattafa-perfume')
 labels=('Cómo saber si un perfume es original','Cómo verificar Lattafa con QR') if lang=='es' else ('How to tell if a perfume is authentic','How to verify Lattafa with QR')
 cards_html='<div class="cards">'+''.join('<article>'+link(lang+'/'+slug+'/',label,'card-title')+'</article>' for slug,label in zip(slugs,labels))+'</div>'
 section_html=section('Autenticidad de perfumes' if lang=='es' else 'Perfume authenticity',cards_html)
 content=content.replace('</main>',section_html+'</main>',1)
 hub.write_text(content,encoding='utf-8')
 for slug in slugs:
  guide=R/lang/slug/'index.html'
  if not guide.is_file():raise ValueError(f'Missing authenticity guide: {guide}')
  sitemap=R/'sitemap.xml'
  xml=sitemap.read_text(encoding='utf-8')
  url=BASE+lang+'/'+slug+'/'
  if '<loc>'+url+'</loc>' not in xml:xml=xml.replace('</urlset>','<url><loc>'+e(url)+'</loc></url>\n</urlset>')
  sitemap.write_text(xml,encoding='utf-8')
# Knowledge Engine tools are independently authored and must survive regeneration.
for lang in ('es','en'):
 guide=R/lang/'tools'/'index.html'
 if not guide.is_file():raise ValueError(f'Missing knowledge tools: {guide}')
 hub=R/lang/'index.html'
 html=hub.read_text(encoding='utf-8')
 label='Calculadoras y respuestas sobre perfumes' if lang=='es' else 'Perfume calculators and troubleshooting'
 link_html='<section class="reading"><h2>'+label+'</h2><p><a href="'+PREFIX+lang+'/tools/">'+label+'</a></p></section>'
 if PREFIX+lang+'/tools/' not in html:html=html.replace('</main>',link_html+'</main>',1)
 hub.write_text(html,encoding='utf-8')
 sitemap=R/'sitemap.xml'
 xml=sitemap.read_text(encoding='utf-8')
 url=BASE+lang+'/tools/'
 if '<loc>'+url+'</loc>' not in xml:xml=xml.replace('</urlset>','<url><loc>'+e(url)+'</loc></url>\n</urlset>')
 sitemap.write_text(xml,encoding='utf-8')
# Scent Match is independently authored; preserve its crawlable links and sitemap.
for lang in ('es','en'):
 guide=R/lang/'scent-match'/'index.html'
 if not guide.is_file():raise ValueError(f'Missing scent match page: {guide}')
 hub=R/lang/'index.html'
 html=hub.read_text(encoding='utf-8')
 label='Descubre perfumes por aroma' if lang=='es' else 'Find fragrances by scent'
 card='<section class="reading"><h2>'+label+'</h2><p><a href="'+PREFIX+lang+'/scent-match/">'+label+'</a></p></section>'
 if PREFIX+lang+'/scent-match/' not in html:html=html.replace('</main>',card+'</main>',1)
 hub.write_text(html,encoding='utf-8')
 sitemap=R/'sitemap.xml'
 xml=sitemap.read_text(encoding='utf-8')
 url=BASE+lang+'/scent-match/'
 if '<loc>'+url+'</loc>' not in xml:xml=xml.replace('</urlset>','<url><loc>'+e(url)+'</loc></url></urlset>')
 sitemap.write_text(xml,encoding='utf-8')
# Keep independently authored interactive comparison pages discoverable after regeneration.
for lang in ('es','en'):
 guide=R/lang/'compare'/'index.html'
 if not guide.is_file():raise ValueError(f'Missing interactive comparator: {guide}')
 hub=R/lang/'index.html'
 html=hub.read_text(encoding='utf-8')
 label='Comparador interactivo de perfumes' if lang=='es' else 'Interactive fragrance comparator'
 card=section(label,'<p>'+link(lang+'/compare/',label)+'</p>')
 if PREFIX+lang+'/compare/' not in html:html=html.replace('</main>',card+'</main>',1)
 hub.write_text(html,encoding='utf-8')
 sitemap=R/'sitemap.xml'
 xml=sitemap.read_text(encoding='utf-8')
 url=BASE+lang+'/compare/'
 if '<loc>'+url+'</loc>' not in xml:xml=xml.replace('</urlset>','<url><loc>'+e(url)+'</loc></url>\n</urlset>')
 sitemap.write_text(xml,encoding='utf-8')
# Preserve independently authored note-family landing pages and link from guide hubs.
NOTE_SLUGS={'es':('vainilla','especiados','ambarados'),'en':('vanilla','spicy','amber')}
for lang,slugs in NOTE_SLUGS.items():
 hub=R/lang/'index.html'
 html=hub.read_text(encoding='utf-8')
 labels={'es':('Perfumes con vainilla','Perfumes especiados','Perfumes ambarados'),'en':('Vanilla perfumes','Spicy perfumes','Amber perfumes')}[lang]
 cards_html='<div class="cards">'+''.join('<article>'+link(lang+'/notes/'+slug+'/',label,'card-title')+'</article>' for slug,label in zip(slugs,labels))+'</div>'
 section_html=section('Descubre perfumes por notas' if lang=='es' else 'Discover fragrances by notes',cards_html)
 if PREFIX+lang+'/notes/'+slugs[0]+'/' not in html:html=html.replace('</main>',section_html+'</main>',1)
 hub.write_text(html,encoding='utf-8')
 sitemap=R/'sitemap.xml'
 xml=sitemap.read_text(encoding='utf-8')
 for slug in slugs:
  guide=R/lang/'notes'/slug/'index.html'
  if not guide.is_file():raise ValueError(f'Missing note-family page: {guide}')
  url=BASE+lang+'/notes/'+slug+'/'
  if '<loc>'+url+'</loc>' not in xml:xml=xml.replace('</urlset>','<url><loc>'+e(url)+'</loc></url>\n</urlset>')
 sitemap.write_text(xml,encoding='utf-8')
# Authored fragrance-note encyclopedia: preserve distinct guides and hubs.
for lang in ('es','en'):
 hub=R/lang/'index.html'
 html=hub.read_text(encoding='utf-8')
 label='Enciclopedia de notas olfativas' if lang=='es' else 'Fragrance notes encyclopedia'
 card=section(label,'<p>'+link(lang+'/notes/',label)+'</p>')
 if PREFIX+lang+'/notes/' not in html:html=html.replace('</main>',card+'</main>',1)
 hub.write_text(html,encoding='utf-8')
 for page in sorted((R/lang/'notes').rglob('index.html')):
  slug=page.parent.relative_to(R).as_posix()+'/'
  sitemap=R/'sitemap.xml'
  xml=sitemap.read_text(encoding='utf-8')
  url=BASE+slug
  if '<loc>'+url+'</loc>' not in xml:xml=xml.replace('</urlset>','<url><loc>'+e(url)+'</loc></url>\\n</urlset>')
  sitemap.write_text(xml,encoding='utf-8')
# Academy landing pages are authored independently, so include them in the sitemap.
for lang in ('es','en'):
 academy=R/lang/'academy'/'index.html'
 if not academy.is_file():
  raise ValueError(f'Missing academy landing page: {academy}')
 sitemap=R/'sitemap.xml'
 xml=sitemap.read_text(encoding='utf-8')
 url=BASE+lang+'/academy/'
 if '<loc>'+url+'</loc>' not in xml:
  xml=xml.replace('</urlset>','<url><loc>'+e(url)+'</loc></url>\n</urlset>')
 sitemap.write_text(xml,encoding='utf-8')
# Preserve six reviewed bilingual Academy presentations in the generated sitemap.
for lang in ('es','en'):
 for perfume in ('yara','khamrah','asad','notes','authenticity','longevity','concentration','gifts','oud','care','occasions'):
  presentation=R/lang/'academy'/perfume/'index.html'
  if not presentation.is_file():
   raise ValueError(f'Missing Academy presentation: {presentation}')
  sitemap=R/'sitemap.xml'
  xml=sitemap.read_text(encoding='utf-8')
  url=BASE+lang+'/academy/'+perfume+'/'
  if '<loc>'+url+'</loc>' not in xml:
   xml=xml.replace('</urlset>','<url><loc>'+e(url)+'</loc></url>\n</urlset>')
  sitemap.write_text(xml,encoding='utf-8')
print(f'Built 12 curated pages and {len(article_urls)} editorial article URLs; sitemap includes {37+len(article_urls)} URLs.')

