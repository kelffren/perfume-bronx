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
