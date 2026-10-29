# Academy extension — 29 October 2026

## Implemented, still on a draft review branch

All eleven bilingual presentations and both Academy directories now use the cinematic system: 24 pages in total. Khamrah remains the reference pilot; Yara Pink uses a rose palette and floral/tropical studies, while Asad uses graphite, pepper/coffee/amber studies and its own published notes. Three product decks each contain seven scenes. Eight educational decks each contain six scenes with specific exercises, explanatory feedback, concept disclosures and local checklists. No points, fake prizes or fabricated customer claims.

The home directory now prioritizes the three profiles and eight lessons. It preserves Coverflow, scent quiz, comparison inputs, dictionary, delivery conditions and FAQ in crawlable HTML. Secondary topics use native disclosures and open when following their existing anchors. Product/lesson links remain ordinary navigable links. Product photos from third-party stores are not reused in these redesigned pages.

## Production blocker — unchanged

This is **not deployed to main**. The user's required hero photographs for Khamrah original, Yara Pink and Asad original have no documented ownership/license. Original CSS scent studies are explicitly labelled and are not product photographs or fake bottles. Populate `assets/academy-media.json` with an approved local photo and rights evidence for each variant, rebuild and visually inspect before release. No user permission to reuse those external photos is inferred from earlier repository use. The user explicitly requested no incomplete production release.

## Files and reproducibility

- Shared system: `assets/academy-cinema.css`, `assets/academy-cinema.js`.
- Art directions: `assets/academy-products.css`, `assets/academy-lessons.css`, `assets/academy-hub.css/js`.
- Build order: `build-academy-cinema.py`, `build-academy-products.py`, `build-academy-lessons.py`, `build-academy-hub.py` in `scripts/`.
- Original six-scene educational copy preserved in `scripts/academy-lessons.json`; authored exercises live in the lesson generator.
- Existing `scripts/build-organic.py` does not overwrite Academy pages.
- Browser checks: `scripts/test-academy-cinema.cjs`, `scripts/test-academy-all.cjs`, and the existing store regression.

## Verification and corrections

- Local Chromium: all 24 pages at 384×856 and 1440×856; each scene, 3 product pyramids/reset, 8 lesson exercises/checklists, Coverflow, quiz, comparison selection, anchored disclosures and no-JS reading. No horizontal page overflow, missing local resources or page errors.
- Khamrah pilot previously passed at 320, 384 and 1440, including browser Back, keyboard, reduced-motion changes and old slide query parameters.
- Deterministic generation: repeated runs of all four generators leave all 24 pages unchanged.
- Structural SEO: 41 sitemap URLs pass metadata, language reciprocity, H1, internal links and structured-data parsing.
- The earlier CI failure was a browser-process crash in the pre-existing storefront test when creating another context with `--single-process`/`--no-zygote`. Replaced those host-specific flags with normal Chromium processes; both CI jobs then passed for commit cc6775879ab5d1e0217d6a722ab42be45e6591a5.
- Expanded CI now includes Chromium and WebKit for the complete Academy. Its final results must be checked on the latest remote commit before claiming success. WebKit is not a physical iPhone Safari test.
- Reviewed real mobile screenshots for Yara, Asad, authenticity and notes, plus the Academy directory. Screenshots are saved in `docs/academy-cinema/screenshots/`.
- The storefront, its cart, catalogue prices and WhatsApp configuration were not modified. Existing inquiry links are used; a real WhatsApp conversation is not claimed.

## Editorial evidence

- Khamrah: https://lattafa.com/product/khamrah/
- Yara: https://lattafa.com/product/yara/
- Asad: https://lattafa.com/product/asad/ (structured notes used; user reviews on that page sometimes mention other variants and are NOT reused).
- Authenticity: https://lattafa.com/spot-a-fake/
- Concentration terminology: https://ifrafragrance.org/using-the-standards — descriptors have no universal exact concentration definition.

Exercises use illustrative choices, not independent product tests. No fixed wear hours or definitive authentication from a photo/QR alone is asserted.
