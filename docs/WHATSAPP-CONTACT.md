# Configuración centralizada de WhatsApp — OUD BRONX

**Único lugar para cambiar el número:** `data/contact.json`.

Valor inicial (solo ejemplo, NO se usa para enviar mensajes): `15550000000`.

Para activar el WhatsApp comercial, edita:

```json
"whatsapp": {
  "number": "1XXXXXXXXXX",
  "placeholder": "15550000000",
  "configured": true,
  "format": "E.164 digits only, 10–15 digits, no plus sign"
}
```

Sustituye `1XXXXXXXXXX` por tu número real de WhatsApp Business, con código de país, sin espacios, `+` ni guiones. El placeholder no activa enlaces de contacto. El catálogo y las herramientas consumen `assets/contact.js`, que lee este JSON. Los botones del recomendador incluyen producto, intención (para mí o regalo), y solicitud de confirmación de precio, disponibilidad y prueba antes de comprar. El carrito de la portada también consulta esta configuración antes de abrir WhatsApp.

Si falta número verificado, la herramienta permite copiar el mensaje y la tienda conserva su aviso de número sin configurar; **no se redirige a un número ficticio**. En GitHub Pages el archivo es público, por lo que nunca guardes secretos, tokens ni credenciales aquí.

Los eventos `oud:conversion-intent` indican intención de clic local, **no una venta confirmada**. Integración de analítica de conversiones y pruebas manuales Safari/WhatsApp pendientes.
