"""Render the eight bilingual lessons with authored exercises and original diagrams."""
from pathlib import Path
import json,re,html
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'scripts/academy-lessons.json').read_text())
# Each exercise contrasts a concrete decision, rather than awarding points.
EX={
'authenticity':{
 'word':['Evidencia','Evidence'],
 'concepts':[['Procedencia','Vendedor y documentación de compra.','Origin','Seller and purchase documentation.'],['Presentación','Misma variante, tamaño y mercado.','Presentation','The same variant, size and market.'],['Verificación','Sigue el procedimiento oficial de la marca.','Verification','Follow the brand’s official verification procedure.']],
 'compare':['Tiene QR: es original.','La presencia del QR no basta. Comprueba el destino y sigue las instrucciones del fabricante.','It has a QR: it is genuine.','A QR alone is not enough. Check the destination and follow the manufacturer’s instructions.'],
 'question':['¿Un código QR demuestra por sí solo que un perfume es original?','Does a QR code alone prove a perfume is genuine?'],
 'answers':[['Sí, basta con que abra una página.','Revisa esa conclusión: un QR puede dirigir a una página que imita otra. Empieza en la web oficial de la marca.','Yes, as long as it opens a page.','Reconsider: a QR can lead to a look-alike page. Start on the brand’s official website.'],['No; hay que verificar el sistema y la procedencia.','Correcto. El código es parte de un proceso, no una garantía por su mera presencia. Conserva las pruebas de compra y consulta al fabricante si hay dudas.','No; verify the system and the source.','Correct. A code is part of a process, not a guarantee merely because it exists. Keep proof of purchase and ask the maker if uncertain.']],
 'checks':[['Identificar vendedor','Identify the seller'],['Confirmar variante y tamaño','Confirm variant and size'],['Consultar instrucciones oficiales','Read official instructions']],
 'source':['https://lattafa.com/spot-a-fake/','Lattafa — Product verification'],'next':'notes'},
'notes':{
 'word':['Evolución','Evolution'],
 'concepts':[['Salida','La primera impresión del aroma.','Top','The opening impression of the scent.'],['Corazón','El carácter que emerge después.','Heart','The character emerging afterwards.'],['Fondo','Las facetas asociadas a etapas posteriores.','Base','Facets associated with later stages.']],
 'compare':['La pirámide es una receta.','Es un mapa descriptivo: una nota no identifica por sí sola un ingrediente químico.','The pyramid is a recipe.','It is a descriptive map: a note does not by itself identify a chemical ingredient.'],
 'question':['Lattafa sitúa la vainilla de Khamrah en…','Lattafa places vanilla in Khamrah’s…'],
 'answers':[['La salida.','Vuelve a mirar la fuente: la salida enumera bergamota, canela y nuez moscada.','The top.','Check the source again: the top lists bergamot, cinnamon and nutmeg.'],['El fondo.','Correcto. La vainilla forma parte del fondo publicado. Eso no fija un minuto de aparición ni un número de horas.','The base.','Correct. Vanilla is part of the published base. That does not fix an arrival time or a number of hours.']],
 'checks':[['Reconocer una nota que disfruto','Identify a note I enjoy'],['Comparar las tres etapas','Compare the three stages'],['Distinguir descripción de fórmula','Distinguish description from formula']],
 'source':['https://lattafa.com/product/khamrah/','Lattafa — Khamrah'],'next':'concentration'},
'concentration':{
 'word':['Proporción','Proportion'],
 'concepts':[['EDT','Una denominación de concentración.','EDT','A concentration descriptor.'],['EDP','No garantiza una duración fija.','EDP','Not a fixed wear-time guarantee.'],['Extrait','No significa automáticamente que encaje mejor contigo.','Extrait','Not automatically a better fit for you.']],
 'compare':['EDP siempre dura más que EDT.','Compara productos concretos: la denominación no sustituye la fórmula ni una prueba de uso.','EDP always lasts longer than EDT.','Compare specific products: the label does not replace the formula or a wear test.'],
 'question':['Dos frascos dicen EDP. ¿Tienen necesariamente la misma concentración exacta?','Two bottles say EDP. Must they have the exact same concentration?'],
 'answers':[['Sí: EDP fija un porcentaje universal.','No. IFRA explica que estas denominaciones no tienen una definición internacional única de concentración.','Yes: EDP fixes a universal percentage.','No. IFRA explains that these descriptors have no single international concentration definition.'],['No: la etiqueta no da un porcentaje exacto universal.','Correcto. Consulta la información del fabricante y compara el aroma, sin convertir la sigla en una promesa.','No: the label gives no universal exact percentage.','Correct. Consult the maker’s information and compare the scent without turning initials into a promise.']],
 'checks':[['Leer la denominación','Read the descriptor'],['Consultar el producto exacto','Check the exact product'],['Elegir por aroma y uso','Choose by scent and use']],
 'source':['https://ifrafragrance.org/using-the-standards','IFRA — Using the Standards'],'next':'longevity'},
'longevity':{
 'word':['Contexto','Context'],
 'concepts':[['Fórmula','Compara el perfume concreto.','Formula','Compare the specific fragrance.'],['Aplicación','Anota cómo lo utilizaste.','Application','Note how you used it.'],['Percepción','Lo que tú percibes puede cambiar.','Perception','What you perceive can change.']],
 'compare':['Si yo ya no lo noto, ha desaparecido.','Esa observación no basta para medirlo. Compara en condiciones parecidas y evita conclusiones por una sola percepción.','If I no longer notice it, it is gone.','That observation alone does not measure it. Compare under similar conditions rather than relying on one impression.'],
 'question':['¿Qué comparación ayuda más a evaluar dos perfumes?','Which comparison helps more when evaluating two fragrances?'],
 'answers':[['Uno en papel y otro en piel, en días diferentes.','Cambias varias condiciones a la vez. Será difícil atribuir la diferencia al perfume.','One on paper and another on skin, on different days.','Several conditions change at once. It becomes hard to attribute the difference to the fragrance.'],['Anotar soporte, aplicación y entorno para comparar condiciones parecidas.','Correcto. No es un ensayo de laboratorio, pero una comparación consistente aporta más que una cifra de horas sin contexto.','Record surface, application and surroundings to compare similar conditions.','Correct. It is not a laboratory trial, but a consistent comparison helps more than an hours claim without context.']],
 'checks':[['Anotar el perfume y soporte','Record fragrance and surface'],['Anotar aplicación y entorno','Record application and surroundings'],['Evitar prometer horas a otras personas','Avoid promising hours to others']],
 'source':None,'next':'care'},
'oud':{
 'word':['Carácter','Character'],
 'concepts':[['Materia','Oud natural: una materia aromática.','Material','Natural oud: an aromatic material.'],['Acorde','Una composición puede evocar una impresión de oud.','Accord','A composition can evoke an oud impression.'],['Nombre','El nombre comercial no revela la fórmula.','Name','The product name does not disclose the formula.']],
 'compare':['Si es un perfume árabe, contiene oud.','El origen o estilo comercial no sustituye la descripción del producto. Revisa sus notas y la información del fabricante.','If it is an Arabian fragrance, it contains oud.','Origin or marketing style does not replace product information. Check its notes and the maker’s description.'],
 'question':['Ves “oud” en el nombre. ¿Qué puedes concluir?','You see “oud” in the name. What can you conclude?'],
 'answers':[['Contiene necesariamente oud natural en una cantidad conocida.','El nombre por sí solo no informa del origen ni del porcentaje de los materiales.','It necessarily contains a known amount of natural oud.','The name alone gives neither the origin nor percentage of the materials.'],['Necesito más información para saber qué representa ese nombre.','Correcto. Distingue el nombre, la descripción olfativa y la información documentada sobre materiales.','I need more information about what the name represents.','Correct. Distinguish the name, scent description and documented material information.']],
 'checks':[['Leer las notas','Read the notes'],['Distinguir acorde de materia','Distinguish accord from material'],['Preguntar si la composición no está clara','Ask when the composition is unclear']],
 'source':None,'next':'notes'},
'care':{
 'word':['Cuidado','Care'],
 'concepts':[['Aplicación','Empieza de forma moderada.','Application','Start moderately.'],['Entorno','Respeta el espacio compartido.','Surroundings','Respect shared spaces.'],['Conservación','Evita calor y luz directa.','Storage','Avoid heat and direct sunlight.']],
 'compare':['Más pulverizaciones siempre es mejor.','Ajusta la aplicación al lugar y a cómo se percibe. Más cantidad no equivale a una mejor experiencia.','More sprays are always better.','Adjust application to the setting and perception. More does not equal a better experience.'],
 'question':['¿Dónde guardarías el frasco cuando no lo usas?','Where would you keep the bottle when not using it?'],
 'answers':[['En el coche al sol.','Revisa la elección: el calor y la luz directa no son buenas condiciones de conservación.','In a car in sunlight.','Reconsider: heat and direct sunlight are not good storage conditions.'],['En un lugar protegido del calor y de la luz directa.','Correcto. Sigue también las indicaciones de conservación del fabricante.','In a place protected from heat and direct sunlight.','Correct. Follow the manufacturer’s storage instructions too.']],
 'checks':[['Leer indicaciones del fabricante','Read the maker’s instructions'],['Elegir un lugar protegido','Choose a protected location'],['Ajustar aplicación al entorno','Adjust application to the setting']],
 'source':None,'next':'occasions'},
'occasions':{
 'word':['Presencia','Presence'],
 'concepts':[['Espacio','Cerrado o al aire libre.','Space','Enclosed or outdoors.'],['Compañía','Ten en cuenta a otras personas.','Company','Consider other people.'],['Preferencia','Tu gusto sigue siendo importante.','Preference','Your taste still matters.']],
 'compare':['Un perfume nocturno no se puede usar de día.','La ocasión orienta; no impone una regla. Considera el entorno, tu preferencia y la cantidad aplicada.','An evening fragrance cannot be worn by day.','Occasion is guidance, not a rule. Consider surroundings, preference and application.'],
 'question':['Vas a una reunión en una sala pequeña. ¿Qué decisión tiene más sentido?','You are attending a meeting in a small room. Which decision makes more sense?'],
 'answers':[['Aplicar mucho para que todos lo noten.','En un espacio compartido conviene considerar el confort de los demás, no buscar máxima presencia.','Apply heavily so everyone notices.','In shared space, consider others’ comfort rather than maximum presence.'],['Empezar de forma moderada y respetar las normas del lugar.','Correcto. Si el lugar pide evitar fragancias, respeta esa indicación.','Start moderately and follow the venue’s rules.','Correct. If the place asks for no fragrance, respect that guidance.']],
 'checks':[['Considerar el espacio','Consider the space'],['Revisar normas del lugar','Check venue rules'],['Elegir aplicación moderada','Choose moderate application']],
 'source':None,'next':'gifts'},
'gifts':{
 'word':['Afinidad','Affinity'],
 'concepts':[['Gusto','Qué aromas disfruta esa persona.','Taste','Which scents the person enjoys.'],['Contexto','Cuándo le gustaría utilizarlo.','Context','When they would like to wear it.'],['Elección','Confirmar variante y condiciones.','Choice','Confirm variant and conditions.']],
 'compare':['El más popular será el regalo perfecto.','La popularidad no revela el gusto de quien lo recibe. Un perfume que ya disfruta aporta una pista más útil.','The most popular will be the perfect gift.','Popularity does not reveal the recipient’s taste. A fragrance they already enjoy gives a more useful clue.'],
 'question':['No conoces sus gustos. ¿Qué pregunta harías primero?','You do not know their tastes. What would you ask first?'],
 'answers':[['¿Cuál es el más vendido?','Puede dar contexto comercial, pero no describe los gustos de esa persona.','Which one sells the most?','It may offer sales context, but it does not describe this person’s tastes.'],['¿Qué perfume usa y qué le gusta de él?','Correcto. Ese punto de partida permite comparar perfiles y evitar elegir solo por fama o envase.','What fragrance do they wear, and what do they like about it?','Correct. That starting point helps compare profiles and avoids choosing only by fame or packaging.']],
 'checks':[['Conocer un aroma que disfruta','Identify a scent they enjoy'],['Definir presupuesto','Set a budget'],['Confirmar presentación y condiciones','Confirm presentation and terms']],
 'source':None,'next':'occasions'}
}
for key,langs in D.items():
 ex=EX[key]
 for lang,data in langs.items():
  es=lang=='es';a=0 if es else 1
  def t(s,e):return s if es else e
  def esc(s):return html.escape(s)
  base=f'/perfume-bronx/{lang}/academy/'
  f=R/lang/'academy'/key/'index.html'
  head=f.read_text().split('</head>')[0]
  head=re.sub(r'<link rel="stylesheet" href="/perfume-bronx/assets/academy-(?:deck|cinema|lessons).css">','',head)
  head+='<link rel="stylesheet" href="/perfume-bronx/assets/academy-cinema.css"><link rel="stylesheet" href="/perfume-bronx/assets/academy-lessons.css"></head>'
  concepts=[(x[0],x[1]) if es else (x[2],x[3]) for x in ex['concepts']]
  chapters=t(['Idea','Contraste','Conceptos','Práctica','Decisión','Aplicar'],['Idea','Contrast','Concepts','Practice','Decision','Apply'])
  art=[]
  art.append('<div class="concept-atlas"><span class="atlas-name">'+esc(ex['word'][a])+'</span><ol>'+''.join('<li><span>'+str(i+1).zfill(2)+'</span>'+esc(name)+'</li>' for i,(name,_) in enumerate(concepts))+'</ol></div>')
  contrast=ex['compare'];claim,explain=(contrast[0],contrast[1]) if es else (contrast[2],contrast[3])
  art.append('<div class="before-after"><div><small>'+t('LA SUPOSICIÓN','THE ASSUMPTION')+'</small><p>'+esc(claim)+'</p></div><details><summary>'+t('Revisar la idea ↗','Reconsider the idea ↗')+'</summary><p>'+esc(explain)+'</p></details></div>')
  art.append('<div class="concept-stack">'+''.join('<details><summary><span>'+str(i+1).zfill(2)+'</span><strong>'+esc(name)+'</strong><span aria-hidden="true">+</span></summary><p>'+esc(desc)+'</p></details>' for i,(name,desc) in enumerate(concepts))+'</div>')
  checks='<fieldset class="lesson-checklist"><legend>'+t('Haz tu propia comprobación','Make your own check')+'</legend>'+''.join('<label><input type="checkbox"><span>'+esc(x[a])+'</span></label>' for x in ex['checks'])+'<p>'+t('Tus selecciones permanecen solo en esta página. No se envían ni se guardan.','Your selections stay on this page. They are not sent or saved.')+'</p></fieldset>'
  art.append(checks)
  answers=[(x[0],x[1]) if es else (x[2],x[3]) for x in ex['answers']]
  art.append('<div class="lesson-exercise"><h3>'+esc(ex['question'][a])+'</h3>'+''.join('<details class="choice" data-exercise-answer="'+str(i)+'"><summary>'+esc(answer)+'<span aria-hidden="true">↗</span></summary><p>'+esc(feedback)+'</p></details>' for i,(answer,feedback) in enumerate(answers))+'</div>')
  art.append('<div class="takeaway"><small>'+t('TU SIGUIENTE PASO','YOUR NEXT STEP')+'</small><ol>'+''.join('<li>'+esc(x[a])+'</li>' for x in ex['checks'])+'</ol><a class="cinema-link" href="'+base+ex['next']+'/">'+t('Seguir aprendiendo ↗','Keep learning ↗')+'</a></div>')
  scenes=[]
  for i,scene in enumerate(data['scenes']):
   actions='' if i<5 else '<div class="lesson-actions"><a class="cinema-link" href="/perfume-bronx/'+lang+'/compare/yara-khamrah-asad/">'+t('Comparar perfiles ↗','Compare profiles ↗')+'</a><a class="cinema-link" href="/perfume-bronx/'+lang+'/bronx-delivery/">'+t('Consultar entrega y posibilidad de prueba','Ask about delivery and trying a fragrance')+'</a></div>'
   scenes.append(f'<section id="scene-{i+1}" class="cinema-scene lesson-layout-{i+1}" aria-labelledby="title-{i+1}"><div class="scene-copy"><p class="eyebrow">{i+1:02d} / 06 — {chapters[i]}</p><h2 id="title-{i+1}" tabindex="-1">{scene["title"]}</h2><p>{scene["text"]}</p>{actions}</div>{art[i]}</section>')
  nav='<nav class="chapter-nav" aria-label="'+t('Escenas','Scenes')+'">'+''.join(f'<a class="chapter-link" href="#scene-{i+1}"><span>{i+1:02d}</span> {name}</a>' for i,name in enumerate(chapters))+'</nav>'
  controls='<nav class="cinema-controls" hidden aria-label="'+t('Controles de la presentación','Presentation controls')+'"><button type="button" data-prev aria-label="'+t('Escena anterior','Previous scene')+'">←</button><span data-counter role="status" aria-live="polite"></span><div class="cinema-progress" aria-hidden="true"><span></span></div><button type="button" data-next aria-label="'+t('Escena siguiente','Next scene')+'">→</button><button type="button" data-motion aria-pressed="true">'+t('Movimiento','Motion')+'</button><button type="button" data-reading aria-pressed="false">'+t('Leer todo','Read all')+'</button></nav>'
  source='' if not ex['source'] else '<p>'+t('Fuente de referencia: ','Reference source: ')+f'<a href="{ex["source"][0]}">{ex["source"][1]}</a>.</p>'
  f.write_text(head+'<body class="academy-cinema cinema-lesson"><a class="skip" href="#content">'+t('Saltar al contenido','Skip to content')+'</a><main id="content" class="cinema-shell" data-cinema="'+key+'"><header class="cinema-header"><a class="cinema-brand" href="'+base+'">OUD BRONX <span>ACADEMY</span></a><a class="language-link" href="/perfume-bronx/'+('en' if es else 'es')+'/academy/'+key+'/">'+t('English','Español')+'</a></header><div class="cinema-intro"><p class="eyebrow">'+t('EL ARTE DE ELEGIR · CLASE INTERACTIVA','THE ART OF CHOOSING · INTERACTIVE LESSON')+'</p><h1>'+data['title']+'</h1></div>'+nav+'<div class="cinema-stage">'+''.join(scenes)+'</div>'+controls+'<footer class="cinema-footer">'+source+'<p>'+t('Ejercicios orientativos de OUD BRONX. Sin puntuaciones ni recomendaciones de compra automáticas.','Educational exercises by OUD BRONX. No scores or automatic buying recommendations.')+'</p><a class="cinema-link" href="'+base+'">'+t('← Volver a la Academia','← Back to Academy')+'</a><button type="button" class="btn share-button" hidden>'+t('Compartir','Share')+'</button><p id="share-status" role="status" aria-live="polite"></p></footer></main><script src="/perfume-bronx/assets/share.js" defer></script><script src="/perfume-bronx/assets/academy-cinema.js" defer></script></body></html>\n')
print('Built eight bilingual interactive lessons')
