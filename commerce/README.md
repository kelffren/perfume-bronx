# OUD BRONX Commerce Lab — local/cloud switch

Open `/perfume-bronx/commerce/` after deploying. The default is **local**, using browser localStorage. Change the dropdown to cloud or use `?backend=local` / `?backend=cloud`. The chosen mode persists per browser.

**Important:** This is an isolated prototype, not a production checkout or a working SaaS. Local data is not shared across devices and may disappear when browser storage is cleared. Do not enter real customer personal data. Cloud mode intentionally fails closed until an authenticated API is configured using `window.OUD_COMMERCE_API_URL` before the module loads. No silent fallback, no invented server or credentials, no automatic migration. The existing storefront is unchanged.

Next: implement authenticated server-side order validation, row-level authorization, inventory transactions, migrations, backups, and integration tests before real orders. Never expose service-role keys in GitHub Pages.
