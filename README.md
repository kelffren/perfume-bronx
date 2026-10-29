# perfume-bronx
Página de aterrizaje con filtro de calificación para perfumes árabes en el Bronx. Prototipo V0.

## ⚠️ Regla para cualquier agente o desarrollador

Antes de crear, diseñar o modificar la página, **lee obligatoriamente** la auditoría de referencia en
[`docs/kelodiamonds-mobile-audit/`](docs/kelodiamonds-mobile-audit/README.md).

Esa carpeta documenta cómo vamos a construir la página: pantallas móviles (384×856) con capturas, colores, tipografías, botones, espaciados y qué hace cada elemento al tocarlo (`README.md` + `data.json`). Úsala como guía de diseño y estructura; no la ignores ni la sustituyas sin aprobación de Kelffren.

## Dirección del proyecto

Antes de tomar decisiones comerciales, diseñar funcionalidades o cambiar el embudo de ventas, lee **[FUNDAMENTOS.md](FUNDAMENTOS.md)**. Es el documento vivo de objetivos, oferta, posicionamiento, experiencia de usuario, métricas, hipótesis y fases del proyecto. La auditoría de Kelo Diamonds sigue siendo la referencia de interfaz; FUNDAMENTOS define **para qué** construimos y cómo medimos el éxito.

## 📋 Pendientes de configuración — completar cuando estén disponibles

**Regla permanente:** Si falta un dato (teléfono, imagen, precio, enlace, credencial o texto), implementar con un placeholder explícito, no inventar valores ni bloquear el resto del trabajo. Registrar aquí qué falta, dónde configurarlo y cómo verificarlo. No afirmar que una integración está operativa hasta probarla.

- [ ] **WhatsApp Business:** introducir el número real con código de país, solo dígitos, en `CONFIG.whatsapp` de `index.html` (actualmente vacío). Verificar que los botones de pedidos, ayuda y el futuro acceso flotante abran el chat correcto. Nunca reutilizar automáticamente el teléfono de otro negocio.
- [ ] **Fotografías del recomendador:** comprobar todos los perfumes del catálogo, asociar a cada SKU una fotografía verificable del frasco correcto, optimizada para móvil, y documentar cuáles falten. No inventar fotografías de productos reales ni declarar 40/40 hasta verificarlo.
- [ ] **Catálogo del recomendador:** actualmente hay 12 fragancias configuradas, no 40. Faltan 28 fichas reales con nombre, notas, precio de referencia y foto verificada. No inventar inventario ni precios. Las fotos verificadas de Yara, Khamrah y Asad se muestran en resultados; faltan las otras 9 fotografías de las 12 fichas actuales. Comprobar también permisos y estabilidad de imágenes alojadas en sitios externos.\n- [ ] **QA de conversión móvil:** verificar botones individuales desde $25–$35, packs de 2 por $55, animación sutil solo del CTA principal y accesibilidad `prefers-reduced-motion`; comprobar que el acceso flotante no tape controles.

Al cerrar cada pendiente, marcar `[x]` y anotar fecha y evidencia de la prueba.

## Cambios implementados — 21 octubre 2026
- Hero: botón principal a perfumes individuales desde $25, segundo botón al test y enlace discreto a paquetes de $55.
- Animación de respiración solo en el CTA principal, desactivada con `prefers-reduced-motion`.
- Ayuda flotante de WhatsApp con texto bilingüe y número tomado de `CONFIG.whatsapp`; **no se abrirá un chat real hasta configurar el teléfono**.
- Recomendador: fotografías asociadas a Yara, Khamrah y Asad; los otros productos mantienen aviso explícito de fotografía pendiente.
- **Pendiente de validación real:** comprobar funcionamiento en iPhone, enlaces, ausencia de superposiciones y carga de imágenes. Estos cambios no prueban aumento de ventas: medir clics y pedidos antes/después.

## Próximo sprint — embudo medible (21 octubre 2026)

**Implementado en código:** contadores locales de clics al Hero (perfumes, test y packs), selección de perfume, selección de pack, intento de envío de pedido, apertura intentada de WhatsApp y falta de número. Se almacenan únicamente en `localStorage` del navegador del visitante, sin datos personales ni envío a servidor. Son diagnósticos locales, **no analítica agregada del negocio ni ventas confirmadas**. Se pueden inspeccionar en la consola del navegador con `JSON.parse(localStorage.getItem("oud-funnel-local-v1") || "{}")`.

**Pendientes siguientes:**
- [ ] Configurar un servicio de analítica agregado respetuoso con privacidad y consentimiento aplicable; no confundir clic con pedido ni pedido con venta.
- [ ] Medir el embudo real: sesiones → clic Hero → test iniciado/completado → selección → WhatsApp → venta confirmada (esta última requiere registro manual o CRM).
- [ ] Auditar en iPhone Safari, Chrome Android, redes lentas, navegación por teclado y movimiento reducido; documentar pruebas reales y errores.
- [ ] Conseguir imágenes verificadas de las 9 fragancias del recomendador sin foto; después ampliar 12 → 40 con fichas verificadas, sin asumir stock.
- [ ] A/B test solo cuando exista suficiente tráfico; cambiar una variable cada vez y comparar conversiones, no solo clics.

## Entrega parcial de sprint — 21 octubre 2026
- [x] Añadido gancho `window.oudAnalytics(event)` a `trackFunnel`, preparado para enviar eventos a un proveedor si se configura.
- [ ] **Plausible (placeholder desactivado):** crear y verificar cuenta/sitio de analítica, confirmar dominio definitivo, revisar privacidad y consentimiento aplicable y habilitar script. El dominio de GitHub Pages puede requerir configuración de sitio/ruta según el proveedor. Hasta entonces, **no existe panel global activo**. No insertar credenciales privadas en GitHub Pages.
- [ ] **Fotos:** identificadas fuentes oficiales para Club de Nuit Intense Man, Club de Nuit Woman, Afnan 9PM y Turathi Blue. Falta obtener archivos de imagen permitidos, optimizarlos y validar visualmente que correspondan al frasco/variante exactos antes de añadirlos. No se han publicado fotos nuevas de estos cuatro.
- [ ] **Pruebas de navegador:** ejecución visual remota pendiente; no afirmar compatibilidad iOS/Android sin captura y recorrido funcional.
- [ ] **Ventas reales:** registrar manualmente cierre, producto, importe, margen y canal, o conectar un CRM. Ningún evento de clic representa una venta.

## Embudo simplificado — 25 octubre 2026

Implementado:
- Selección directa desde el carrusel; detalles del aroma disponibles en un botón separado. Se conserva la secuencia existente de foto/video.
- Test de tres preguntas (aromas, ocasión, intensidad), con selección múltiple y una recomendación principal más dos alternativas. Los productos fuera del catálogo siguen siendo consultas de disponibilidad.
- Datos personales plegados y opcionales. Mensaje de pedido con productos, cantidades, subtotal y condiciones de entrega; se omiten campos vacíos.
- Oferta complementaria al seleccionar un frasco. Los tres pares distintos del catálogo aplican automáticamente el paquete de $55. Dos frascos iguales y cantidades superiores conservan sus precios individuales; no se amplía una promoción sin definirla.
- Entradas para anuncios: `?product=yara`, `?product=khamrah`, `?product=asad`. Enfocan la tarjeta correspondiente sin añadir productos automáticamente. También se admiten anclas `#perfume-yara`, `#perfume-khamrah`, `#perfume-asad`.
- Eventos locales y gancho de analítica para selección complementaria, test y entrada de producto. No equivalen a ventas ni a un panel agregado.

Validación: comprobación de sintaxis y pruebas DOM con jsdom: catálogo, selección/cantidades, nueve combinaciones de dos frascos, descuentos, mensajes sin datos personales, compra desde carrusel, detalles, test de tres preguntas, traducción de controles ES/EN y entrada directa. Sin errores de script en estos recorridos.

Limitación: no se completó validación visual ni Safari real; la descarga del navegador de prueba falló. No se afirma compatibilidad visual comprobada. WhatsApp continúa pendiente porque `CONFIG.whatsapp` está vacío. No se añadieron reseñas, pruebas de autenticidad ni promesas de entrega/pago sin documentación real. Analítica global, atribución de ventas y seguimiento autorizado siguen pendientes.

## Organic growth — 26 October 2026
Twelve curated EN/ES pages in `es/` and `en/`, generated by `scripts/build-organic.py`. Regenerate and run `scripts/check-organic.py` and `scripts/test-organic.cjs` before publishing. Guide inquiry links add `intent=inquiry`; ordinary advertising product links retain their focus-only behavior. `organic_product_inquiry` is a local diagnostic event, not a verified conversation or sale. WhatsApp remains unconfigured. See [execution log](docs/organic-growth-2026-10-26.md) for evidence, blockers and next priorities.

## Technical discovery — 26 October 2026
Guides support native sharing/copying of clean canonical links. GitHub Actions checks generated SEO files and notifies IndexNow after successful Pages deployment. See [implementation, verification and blockers](docs/seo-discovery-2026-10-26.md). IndexNow receipt is not confirmed indexing; Search Console, aggregated analytics and the actual business WhatsApp number remain pending.

## Khamrah cinematic pilot — draft, 28 October 2026
A bilingual seven-scene implementation is prepared in `scripts/build-academy-cinema.py`, with isolated `assets/academy-cinema.css/js` and Playwright coverage in `scripts/test-academy-cinema.cjs`. See [audit, QA and release blocker](docs/academy-cinema-2026-10-28.md). Product photography is gated by `assets/academy-media.json`; a commercial license or owned-photo evidence is required before this pilot is approved for main. The remaining ten presentations have not been redesigned in this iteration.

## Academy extension — 29 October 2026
The draft now covers all 11 bilingual presentations and both Academy directories (24 pages), with lesson-specific exercises and separate Yara/Asad art directions. See [current implementation and QA log](docs/academy-cinema-2026-10-29.md). This supersedes the pilot-only scope above; production release still requires approved photographs for the three exact product variants. Build all four Academy generators in the documented order and run both Academy browser suites before merging.
