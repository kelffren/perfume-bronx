# OUD BRONX Commerce Lab — local/cloud switch

Open `/perfume-bronx/commerce/` after deploying. The default is **local**, using browser localStorage. Change the dropdown to cloud or use `?backend=local` / `?backend=cloud`. The chosen mode persists per browser.

**Important:** This is an isolated prototype, not a production checkout or a working SaaS. Local data is not shared across devices and may disappear when browser storage is cleared. Do not enter real customer personal data. Cloud mode intentionally fails closed until an authenticated API is configured using `window.OUD_COMMERCE_API_URL` before the module loads. No silent fallback, no invented server or credentials, no automatic migration. The existing storefront is unchanged.

Next: implement authenticated server-side order validation, row-level authorization, inventory transactions, migrations, backups, and integration tests before real orders. Never expose service-role keys in GitHub Pages.

## Persistent local SQLite mode
Run `python3 commerce/local-server.py` on your own computer, then select **SQLite local** in the Commerce Lab. The server binds only to 127.0.0.1:8765, and persists draft orders in `commerce/commerce-local.sqlite3`. Run `python3 commerce/test-local-server.py` for basic schema checks. To serve the UI locally run `python3 -m http.server 8000` from the repository root and open `http://localhost:8000/commerce/` (GitHub Pages absolute links to the storefront still point to the deployed site). Do not expose port 8765 publicly. This prototype does not implement authentication or payment processing.

## Local inventory editor (development only)

Start the server with an admin token (do not commit or share the token):

```sh
OUD_LOCAL_ADMIN_TOKEN="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')" python3 commerce/local-server.py
```

For repeated use, save the generated token in your local password manager and start the server with that same value. In a separate terminal run `python3 -m http.server 8000` from the repository root. Open `http://localhost:8000/commerce/admin.html`, select **SQLite local**, enter the exact token, and load the catalogue. The server persists price and stock updates in its SQLite database. This does not change public storefront prices.

The admin endpoint requires a configured token and a local browser Origin. Do not publish this server, expose port 8765, or store the token in frontend files. No customer data, payment data, or live inventory should be entered. Security hardening, end-to-end tests, and deployment review are required before real use.
