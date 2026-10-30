# Oud Bronx Knowledge Engine — roadmap
Updated: 2026-10-29. Statuses require evidence, not assumptions.

| ID | Priority | Work | Status | Dependencies / acceptance | Next action |
|---|---|---|---|---|---|
| KE-001 | P0 | Bilingual calculators + troubleshooting | IMPLEMENTADA | Pages, links, sitemap, JS, automated tests | Confirm CI and production URLs before marking VERIFIED |
| KE-002 | P0 | Scent Match | PENDIENTE | Verified scent-reference dataset; no unproven dupes | Model sources and build accessible finder |
| KE-003 | P0 | Fragrance encyclopedia | PENDIENTE | Verified notes and citations | Publish first useful bilingual note guides |
| KE-004 | P0 | Gift finder | PENDIENTE | Existing catalogue and real pricing | Reuse recommendation model |
| KE-005 | P0 | Central catalogue | PENDIENTE | Preserve cart, pricing and photos | Extract structured source of truth |
| KE-006 | P1 | Decant and price calculators | IMPLEMENTADA | Basic calculator on tools pages | Extend comparisons with verified prices |
| KE-007 | P1 | Seasonal/occasion finder | PENDIENTE | Documented scent families | Implement filters |
| KE-008 | P1 | Label dictionary | PENDIENTE | Official manufacturer sources | Research and publish |
| KE-009 | P1 | Editorial rankings | PENDIENTE | Explicit methodology | Publish curated comparisons |
| KE-010 | P1 | Product FAQs | PENDIENTE | Verified manufacturer facts | Add per-product FAQ |
| KE-011 | P1 | Bronx local SEO | BLOQUEADA | Confirm coverage and fulfillment terms | Verify real service |
| KE-012 | P1 | Ask Oud Bronx | PENDIENTE | Static search first; backend for submissions | Build searchable answer index |
| KE-013 | P2 | Multimedia | BLOQUEADA | Licensed assets | Collect authorized media |
| KE-014 | P0 | Internal links | EN PROGRESO | Generator must preserve links | Expand cross-links and nav |
| KE-015 | P0 | Premium mobile UI | EN PROGRESO | Respect design audit | Browser/mobile QA |
| KE-016 | P0 | Analytics | BLOQUEADA | Consent, provider, business confirmation | Verify setup |
| KE-017 | P0 | Automated QA | EN PROGRESO | Existing organic CI | Add interaction tests |
| KE-018 | P0 | Publication | EN PROGRESO | Green CI and verified GitHub Pages | Merge only after tests |

Next three: (1) verify KE-001 CI/deployment, (2) build KE-002 with sourced comparisons, (3) centralize catalogue KE-005.

## KE-002 progress — 2026-10-29
Bilingual Scent Match MVP built for three documented Lattafa profiles with accessible search and family filters, indexed routes and crawlable fallback cards. Status IMPLEMENTADA; CI, deployment and live interaction verification remain pending. Next: expand verified data and create distinct editorial comparisons, not unsupported dupes.

## KE-005 — central catalogue, 2026-10-29
Status: IMPLEMENTADA (pending CI and public verification). Source `data/catalog.json` holds the three current store products, displayed-but-unconfirmed prices, explicit unknown stock, bilingual manufacturer-note metadata, imagery provenance and tags. `scripts/build-organic.py` regenerates the existing synchronous storefront array without changing cart/bundle interfaces; Scent Match reads the same JSON. CI checks catalogue consistency. Acceptance: CI green, storefront cart and Scent Match browser verified. Next: expand only with confirmed SKU details and licensed imagery.

## KE-004 — Gift Finder (2026-10-29)
Status: IMPLEMENTADA, pending CI/public verification. Bilingual `/es/gift-finder/` and `/en/gift-finder/` with accessible budget, scent family, and gift-mood filters. Data loaded from `data/catalog.json` (Yara, Khamrah, Asad). Displayed prices are unverified, stock unknown; static crawlable product guide fallback and manufacturer links. Next: verify live mobile interaction and ensure navigation discoverability.
