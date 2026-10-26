# SEO discovery and sharing — 26 October 2026

## Implemented
- Twelve EN/ES guides now offer native sharing with clipboard/manual-link fallback. Shared URLs are canonical and exclude query strings, cart data and personal details. Cancellation is quiet. No third-party tracking is added.
- Complete Twitter title/description/image tags and Open Graph image descriptions per guide. Existing catalogue photographs retained; no new media rights asserted.
- IndexNow notifier and public ownership file scoped to `/perfume-bronx/`. Only changed HTML pages currently in the sitemap are submitted after a successful GitHub Pages deployment; documentation-only changes submit nothing. Dry run by default; `--submit` explicitly sends. HTTP 200/202 means receipt, not indexing, rankings or Google notification. Removed URLs are not submitted by this version; add deletion support if removing pages.
- SEO checks on PRs and main pushes: generation consistency, canonical URLs, unique URLs/H1, language reciprocity, internal links, local script/CSS existence, no noindex on sitemap pages, structured-data and JS syntax, share metadata and scoped IndexNow tests. Checks report failures; branch protection is not configured by this change and deployment is not gated on these checks.
- Main storefront/cart code is unchanged by this batch. Concurrent main cart changes preserved.

## Validation
- Structural checks pass for 13 canonical URLs.
- Chromium 384px/1440px: all twelve guides have no horizontal overflow; unchanged homepage screenshot relative to checkout baseline; guide inquiry selects product and language, missing WhatsApp message visible, $55 bundle, carousel, normal advertising landing, invalid query handling and no-JavaScript catalogue pass.
- Sharing tests: clean canonical URL, cancellation, clipboard success, clipboard refusal, re-enabled button; no uncaught errors. Screenshot reviewed; deterministic browser test blocks external fonts/photos, so this is layout/behavior evidence, not a live-image or physical Safari test.
- IndexNow unit checks cover changed-page selection, exclusions and host/query scope. Production acceptance is only established by the deployment workflow output, not by local dry runs.

## Sources
- https://www.indexnow.org/documentation — path-scoped ownership and 200/202 receipt semantics.
- https://developers.google.com/search/docs/appearance/google-images — image discovery and responsive images.
- https://support.google.com/merchants/answer/12160471 — Merchant Center purchase requirements.
- https://support.google.com/business/answer/13763036 — Business Profile eligibility.

## Blockers / next three priorities
1. Configure the verified business WhatsApp number (still empty). Verify Search Console ownership for the URL-prefix property `https://kelffren.github.io/perfume-bronx/`, submit `sitemap.xml`, inspect indexation. No verified account token or GA4 measurement ID has been supplied; no aggregated analytics is active.
2. Obtain merchant-owned/authorized product photographs. Optimize responsive local assets after verifying variant and permission. No assumption that remote catalogue photos may be republished.
3. Confirm prices, inventory, payment and delivery/returns policies before implementing a transactional checkout and Merchant Center feed. WhatsApp consultation alone is not a complete Merchant Center purchase flow. Confirm in-person business operation before Google Business Profile setup. No fabricated address or reviews.

## Reproduce
`python scripts/build-organic.py`
`python scripts/check-organic.py`
`python scripts/test-indexnow.py`
`node --check assets/share.js`
`BASELINE_REF=<pre-change-commit> CHROMIUM_EXECUTABLE_PATH=<chrome> node scripts/test-organic.cjs`
`python scripts/notify-indexnow.py --since <previous-deployed-commit>` (dry run)

For multi-commit manual releases, provide the previous deployed commit with `--since`; the automatic workflow compares to the first parent of the deployed commit. The usual merge-PR deployment covers that PR's changes. Do not bulk-resubmit unchanged pages. No background process outside GitHub events is created.
