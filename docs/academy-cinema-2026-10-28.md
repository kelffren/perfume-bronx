# Khamrah cinematic pilot — 28 October 2026

## Release status: DRAFT, NOT APPROVED FOR MAIN

User explicitly requested licensed/owned product photography and no incomplete production releases. The existing external Khamrah image has no verified commercial license in the repository. See `docs/organic-growth-2026-10-26.md`. No permission is inferred from an HTTP 200 or public image URL. This iteration therefore remains on a review branch; it must not be described as deployed or as the completed 11-presentation redesign.

The hero currently contains an original CSS scent study explicitly labelled as an olfactory study, not a bottle rendering. This is a functioning draft art direction, but does not satisfy the user's product-photography requirement. `assets/academy-media.json` records the blocker. Supply an owned/licensed photograph of **Khamrah original**, its permission evidence, and a local path; then approve the manifest entry, regenerate and visually inspect the real photo before release. Do not use Qahwa or a generated imitation bottle. The renderer requires a real local asset and permission evidence when marked approved.

## Audit

Read AGENTS.md, FUNDAMENTOS.md, README.md, WORK-ORGANIC-GROWTH.md, SEO-LAUNCH.md, the mobile audit README and measured data (85 screens, tokens), Academy shared scripts/styles and presentation HTML. Opened the published Spanish Khamrah page in remote Chrome and inspected its actual screenshot.

Existing 11 bilingual decks have six slides each, with nearly identical composition. Khamrah repeats the same static pyramid three times; educational classes provide text but no lesson-specific exercises. The current mobile deck puts media before text without a differentiated scene system. Existing presentation navigation uses replaceState and offers no explicit reading mode. Remote product photos have no recorded commercial license. WhatsApp is still unconfigured in the storefront; this change preserves the product-guide inquiry path rather than inventing a number.

## Implemented in this pilot

- Seven authored ES/EN scenes: introduction, individually explorable notes, layered pyramid, natural-scroll evolution, Khamrah/Yara contrast, preference reasoning, contextual commercial close.
- Dark amber editorial composition, light note-study scene, original CSS cinnamon/date/vanilla studies, depth slabs, asymmetrical desktop layouts, reduced mobile density.
- Pyramid selection/reset with real buttons, aria-expanded and associated content. Depth is on pseudo-elements, preserving reliable pointer hit regions.
- Chapter links, keyboard arrows, swipe respecting vertical gestures, history Back/Forward, legacy `?slide=` links, full reading mode, reduced-motion media changes and manual motion control.
- Static HTML content and native details remain usable without JavaScript. Canonical/hreflang/JSON-LD/social metadata and sharing are preserved.
- Contextual product and comparison links; delivery wording follows FUNDAMENTOS. No unsupported performance, stock, authenticity or unconditional trial promises.
- Isolated `academy-cinema.css/js`; the other ten decks and storefront assets are unchanged.

## Sources

- https://lattafa.com/product/khamrah/ — checked 28 October 2026. Use its structured Fragrance Notes list (its prose description differs on one floral note). Educational descriptions are interpretations, not physical ingredient claims.
- https://lattafa.com/product/yara/ — checked 28 October 2026, comparison grounded in floral/tropical/vanilla notes.

## Verification

- `python scripts/check-organic.py`: PASS, 41 URLs, canonical, hreflang, H1, metadata, internal links, JSON-LD and inline JavaScript.
- `python scripts/test-indexnow.py`: PASS.
- `node --check assets/academy-cinema.js`: PASS.
- `python scripts/build-academy-cinema.py`: deterministic, ES/EN output identical on repeated generation.
- `scripts/test-academy-cinema.cjs`: PASS in local Chromium, ES/EN at 320×856, 384×856 and 1440×856; all seven scenes, no horizontal page overflow, pyramid mouse/keyboard/reset, note and preference disclosures, keyboard scene changes, browser Back, reading mode, live reduced-motion preference changes, legacy links, JavaScript-disabled reading, zero page errors.
- `scripts/test-organic.cjs`: PASS, existing 12 guide pages, unchanged store hero, cart inquiry, language, $55 bundle, carousel, URL sharing, no-JS catalogue, zero errors.
- Visual review found and fixed inherited white header, overflow-prone transformed pyramid hit regions and excessive mobile hero size.
- Normal Playwright browser downloads failed; used npm-distributed Chromium 153 through Playwright 1.62.1 for local testing. Remote Chrome was used for published-before inspection. No claim of physical iPhone Safari, WebKit, field CWV, or real WhatsApp sending.

## Next steps (in order)

1. Resolve Khamrah product-photo rights, inspect correct variant and responsive crop, rerun visual and accessibility QA, then release approved Khamrah to main and verify Pages deployment.
2. Apply the validated system to Yara and Asad with approved images and their own floral/dark art directions.
3. Author eight lesson-specific exercises and improve the Academy hub, then test all 22 pages. These are pending; no claim that shared CSS alone completes them.
