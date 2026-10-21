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
- [ ] **QA de conversión móvil:** verificar botones individuales desde $25–$35, packs de 2 por $55, animación sutil solo del CTA principal y accesibilidad `prefers-reduced-motion`; comprobar que el acceso flotante no tape controles.

Al cerrar cada pendiente, marcar `[x]` y anotar fecha y evidencia de la prueba.
