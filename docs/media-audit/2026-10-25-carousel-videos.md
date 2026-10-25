# Auditoría de videos del carrusel — 25 octubre 2026

## Resultado de publicación
**0 de 3 videos aprobados. Integración NO completada.**
Investigación y auditoría realizadas como dos funciones consecutivas por el mismo asistente; no se presenta esto como revisión humana independiente.
Rama solicitada: `main`. Archivo inspeccionado: `index.html`, blob `5b8355de6cf7c1412b0b9f00089511049381cc36`.
Este informe no modifica fotografías, estilos, catálogo, temporizador ni URLs de reproducción. Los tres campos de `productVideos` siguen vacíos.

## Informe por perfume

| Perfume | Fuente candidata encontrada | Evidencia disponible de coincidencia | Licencia comercial | MP4 autorizado | Veredicto del auditor |
|---|---|---|---|---|---|
| Lattafa Yara Pink original | [iSpot: Play by Play: Interview](https://www.ispot.tv/ad/6moZ/lattafa-perfumes-play-by-play-interview), anuncio catalogado de 20 s, 11 junio 2024 | El catálogo identifica Lattafa Perfumes Yara. No se inspeccionaron fotogramas: el nombre en metadatos no demuestra botella rosa ni variante exacta. | No verificada; no se obtuvo permiso para descargar, editar o alojar en Oud Bronx. | Ninguno | PENDIENTE. No publicar. |
| Lattafa Khamrah original | [YouTube: Khamrah by Lattafa Perfumes](https://www.youtube.com/watch?v=VNbE9sd_2Wk), Dollars & Scents, 22 septiembre 2022 | Título y descripción identifican Khamrah; es una reseña de primeras impresiones, no un anuncio oficial verificado. No se inspeccionaron fotogramas. | No verificada; no se encontró autorización aplicable a esta reutilización. | Ninguno | NO APROBADO. Candidato secundario, poco adecuado como publicidad visual. |
| Lattafa Asad original negro | [Vimeo: Lattafa Asad - 100ml](https://vimeo.com/1011105255); alternativa [iSpot: Play by Play](https://www.ispot.tv/ad/6iBu/lattafa-perfumes-play-by-play), 20 s, 10 junio 2024 | Vimeo aporta el título; iSpot identifica el producto Asad. No se inspeccionaron botella, nombre ni presentación en fotogramas. | No verificada para ninguno de los dos candidatos. | Ninguno | PENDIENTE. No publicar. |

**Resultado de pruebas para cada uno de los tres:** no hubo reproducción de un archivo aprobado; codec, tamaño, dimensiones, duración real, hash, transición, fin de video y rendimiento quedan sin comprobar. Ninguno pasó QA de Safari en iPhone. El commit que añade este documento es documental, no una integración de medios.

## Fuentes revisadas y descartes
- [Lattafa: Khamrah](https://lattafa.com/product/khamrah/): referencia oficial del producto original 100 ml. Su ficha no constituye permiso para reutilizar videos.
- [Lattafa: términos](https://lattafa.com/terms-conditions/): se consultaron sus términos. No se identificó allí una licencia expresa que autorice a Oud Bronx a descargar y republicar estas piezas. La cláusula sobre derechos de Lattafa respecto de materiales subidos a su web no es una concesión equivalente a terceros.
- [Lattafa: consultas de distribución](https://lattafa.com/distributor-enquiries/): canal encontrado para consultar disponibilidad de materiales y permiso. No se envió formulario ni mensaje.
- [Lattafa USA](https://www.lattafa-usa.com/): fuente comercial de marca encontrada. No se obtuvo un paquete de prensa ni MP4 con autorización aplicable.
- [Vimeo: Khamrah Dukhan / Belvish](https://vimeo.com/1084528811): descartado por variante explícitamente diferente en el título; no es Khamrah original.
- [YouTube: Khamrah Waha](https://www.youtube.com/watch?v=y2zxlRitzJo): descartado por variante diferente en el título.
- [YouTube: Khamrah Qahwa](https://www.youtube.com/watch?v=FxjHqB53jD8): descartado por variante diferente en título y descripción.
- [Vimeo: Lattafa Perfumes Tvc | Film-1](https://vimeo.com/1019935411): título demasiado general; no permite asignar variante. No aprobado.

Una página pública, un código iframe, una miniatura o un botón de descarga no se registran como prueba suficiente de autorización comercial para autoalojar un MP4.

## Límites de verificación observados
- La consulta textual de iSpot devolvió 403; el buscador aportó metadatos de los anuncios, no una inspección visual.
- La consulta textual de Vimeo solo devolvió contenido mínimo. Se intentó abrir el video de Asad en el navegador para inspeccionar fotogramas.
- La revisión automática rechazó esa apertura por límite de uso del navegador. No fue un rechazo manual del usuario ni una determinación sobre la seguridad del video. No se ejecutó la navegación ni se intentó eludir la restricción.
- No hubo acceso a un iPhone físico con Safari. No se debe confundir Chrome con viewport móvil o WebKit automatizado con Safari real.
- No se han confirmado permisos, comprado licencias ni contactado titulares. No existe evidencia de que estos videos sean libres de uso.

## Auditoría estática del carrusel existente
Confirmado por lectura de código, **no por prueba de navegador**:
1. `productVideos={khamrah:"",yara:"",asad:""}`: ningún video de producto configurado.
2. `schedule()` programa `startProductVideo` a 23000 ms cuando el carrusel está visible y no hay pausa por foco, hover, detalle expandido, pestaña oculta o movimiento reducido.
3. Si no existe URL, pasa al siguiente perfume. Las fotos se conservan.
4. El elemento de video se crea con `muted playsinline preload="none"`; su `src` se asigna al iniciar.
5. `onended` avanza al siguiente; errores y rechazo de `play()` también avanzan.
6. Al salir de pantalla o esconder la pestaña se detiene y descarga el video activo.

Riesgos detectados por inspección para resolver y probar antes de activar archivos:
- La promesa de `play()` no valida que siga vigente la tarjeta. Si se navega mientras está pendiente, su resolución/rechazo puede afectar la tarjeta o navegación posterior.
- `stopVideo()` no elimina los manejadores `onended/onerror` antes de quitar `src` y llamar `load()`.
- `schedule()` no comprueba si hay video activo. Un evento de salida de hover o foco puede programar un segundo inicio durante reproducción.
- No hay timeout explícito de carga/buffering; una carga que no termina ni emite error puede detener el avance.
- Hover/foco solo cancelan el temporizador; no pausan necesariamente el video ya iniciado.
- La condición `:hover` requiere prueba táctil: un estado hover persistente puede impedir reanudar el temporizador en móvil.
- Cada reprogramación reinicia los 23 segundos, no acumula tiempo visible. Debe acordarse y probarse este comportamiento al reingresar al carrusel.
No se modificó código de reproducción sin poder ejecutar la validación visual requerida.

Hallazgo ajeno al video pero relevante para QA: `CONFIG.whatsapp` sigue vacío. No se puede declarar verificado el envío al chat comercial correcto.

## Requisitos para aprobar cada archivo
- Identificar al titular/licenciante y conservar autorización aplicable a Oud Bronx: uso comercial web, descarga, autoalojamiento, silenciamiento, compresión y recorte si se necesitan; alcance territorial y duración.
- Recibir el archivo original autorizado o una descarga oficial acompañada de esos derechos. No colocar URLs de páginas YouTube/Vimeo en `video.src`.
- Inspeccionar inicio, mitad, final y todos los cambios de producto. Registrar timestamps y capturas:
  - Yara: botella rosa del Yara original, nombre Yara y marca Lattafa; excluir Moi, Tous, Candy y Elixir.
  - Khamrah: presentación del original con etiqueta legible; excluir Qahwa, Dukhan y Waha. No identificar solo por silueta compartida.
  - Asad: presentación negra del original con nombre legible; excluir Zanzibar, Bourbon y Elixir.
- Registrar origen, permiso, archivo, SHA-256, codec, dimensiones, duración, bytes, fecha y decisión de auditor.
- Preparar derivado móvil H.264 en MP4, formato de píxel yuv420p y faststart; sin pista de audio si el permiso lo permite. Elegir resolución/bitrate tras medir, sin ampliar innecesariamente.
- Mantener la fotografía actual como estado inicial y fallback. Activar solo tras aprobar todas las comprobaciones.

## Matriz de pruebas pendiente (ninguna marcada como pasada)
| Caso | Criterio |
|---|---|
| Inicio de tarjeta | Foto visible durante los primeros 23 s; ningún MP4 de producto solicitado antes de su activación. |
| Reproducción | Un solo video activo, silenciado, inline, sin reemplazar el elemento de foto. |
| Final | Avanza exactamente una tarjeta; comienza una nueva espera de 23 s. |
| Controles | Anterior/siguiente, swipe, pestañas HOT/GEMS, revelar y pedido responden durante carga y reproducción. |
| Carreras asíncronas | Cambiar tarjeta durante play pendiente no genera saltos tardíos ni reproduce una tarjeta oculta. |
| Error/autoplay denegado | Foto visible y controles operativos; el carrusel no queda bloqueado. |
| Visibilidad | Salir de pantalla, ocultar pestaña y volver no dejan videos ocultos activos ni temporizadores duplicados. |
| Accesibilidad | Movimiento reducido, teclado y foco no provocan avance inesperado. |
| Safari iPhone | Probar dispositivo/versiones registrados, modo normal y bajo consumo, datos móviles y red lenta. |
| Rendimiento/transición | Medir bytes, solicitudes, carga/buffering y estabilidad visual; revisar recortes de frasco y etiquetas. |
| Conversión | Selección y pedido conservan producto/cantidad; WhatsApp requiere número real configurado. |

## Próximas acciones
1. Obtener permiso y archivos del titular o material propio del usuario con derechos confirmados.
2. Completar inspección de fotogramas y correcciones de reproducción con pruebas automatizadas y visuales.
3. Solo entonces configurar videos aprobados, verificar Safari real y publicar commit de integración con evidencia.

Para localizar el commit documental: historial de este archivo en GitHub. No se inserta un SHA futuro inventado dentro del propio documento.
