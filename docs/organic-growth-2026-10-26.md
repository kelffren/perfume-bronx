# Organic growth — execution 25–26 October 2026

## Implemented
Twelve static bilingual pages: six product guides (Yara original/Pink, Khamrah original, Asad original), two comparisons, two local buying guides and two language hubs. Sitemap now contains thirteen URLs with six product-image references. Canonicals, reciprocal EN/ES/x-default, descriptions, social metadata, Product entities and breadcrumbs included. No fabricated stock, ratings or offers.

Homepage links and catalogue HTML allow discovery without JavaScript. Guide CTAs use `?product=yara&intent=inquiry&lang=es` to select one bottle in the existing drawer. Ordinary `?product=yara` advertising landings retain the newer main behavior: focus the product without opening the drawer. Missing WhatsApp errors become visible; failing optional analytics cannot interrupt ordering. Legacy copies are noindex.

Preserved main's simplified order form, automatic bundle pricing, complementary bottle suggestions, one-click carousel selection and new quiz logic from `057cb56`, and the media audit from `4b14527`. Original implementation: `8eec32d`; review and final integration: https://github.com/kelffren/perfume-bronx/pull/2 .

## Research and editorial evidence
Manufacturer notes checked on 25 October:
- https://lattafa.com/product/yara/
- https://lattafa.com/product/khamrah/
- https://lattafa.com/product/asad/

Recommendations are editorial interpretation, not personal wear tests. Search results contained relevant comparison pages (Perfume Primitive and Arabic Perfumery); this indicates comparison intent, not proven search volume. Our hypothesis: variant clarity, bilingual notes and a practical local-order checklist can attract qualified visitors. No rankings or revenue increases are claimed.

Implementation references:
- https://developers.google.com/search/docs/specialty/ecommerce/help-google-understand-your-ecommerce-site-structure
- https://developers.google.com/search/docs/specialty/international/localized-versions
- https://developers.google.com/search/docs/appearance/google-images

## Validation
Run `python scripts/build-organic.py`, `python scripts/check-organic.py`, then `node scripts/test-organic.cjs` with Playwright and a Chromium executable (optional `CHROMIUM_EXECUTABLE_PATH`). Tests validate all sitemap URLs, headings, canonical metadata, language reciprocity, internal links, JSON-LD and JS syntax. Browser checks cover 384/1440px layouts, original hero screenshot equality, product inquiries, language, bundle subtotal, carousel ordering, ad landings, invalid input, missing-number visibility and no-JS catalogue.

The previous version passed these checks on 25 October. Final integration results are recorded below after rerunning. No physical iPhone/Safari, Google Rich Results Test, real WhatsApp send or field Core Web Vitals result is claimed. Existing external images returned HTTP 200 on 25 October: Yara 148003 bytes, Khamrah 167068, Asad 32781. This is retrieval evidence, not a media license or guarantee of continued availability. Own photography remains preferable.

## Blockers and next three priorities
1. Configure verified OUD BRONX number in `CONFIG.whatsapp` (still empty), test real chat routing and confirm stock, sizes, prices and delivery coverage. Do not copy another business's phone. Local click counters are not confirmed conversations or sales.
2. Verify Search Console URL-prefix property, submit the sitemap and inspect representative URLs. No account access/token is available. The project's `/perfume-bronx/robots.txt` does not replace the host-root `/robots.txt`; do not assume the project file controls host crawling. Product data without offers/reviews does not establish product rich-result eligibility.
3. Obtain merchant-owned photos and genuine customer feedback with consent. Replace third-party images with responsive local assets once permission is established; add first-hand product details when actually tested.

## Legitimate referral and review workflow
No outreach has been sent and no partner is claimed. Qualify local beauty/barber businesses, Bronx lifestyle creators and fragrance editors by actual relevance and verified contact. Offer an original demonstration or comparison, not a paid-link exchange. Disclose payment/free-product relationships and leave the creator's opinion independent.

Draft outreach: “Hola, soy de OUD BRONX. Hemos preparado una guía bilingüe para elegir entre Yara, Khamrah y Asad y coordinar pedidos en el Bronx. ¿Te interesaría valorar una colaboración con una demostración real? Acordaríamos los detalles y declararíamos cualquier producto o pago recibido; tu opinión sería independiente.”

After genuine delivered orders, request feedback neutrally from all customers: “¿Cómo fue tu experiencia con el perfume y la entrega? ¿Qué te gustó y qué mejorarías? ¿Nos autorizas a publicar tus palabras y con qué nombre?” Keep verification and consent privately; never publish addresses, phone numbers or payment data. Do not filter out legitimate negative feedback. A public review form needs a real receiving service and moderation owner before activation.

Google Business Profile eligibility must be confirmed against https://support.google.com/business/answer/3038177 ; do not invent a storefront, address or online-only eligibility. Merchant Center setup is also pending confirmed merchant data and requirements. No external account was created or modified.

## Final integration validation — 26 October
Structural checks passed for all 13 sitemap URLs. Chromium checks passed for all 12 new pages at 384px and 1440px: identical hero screenshot to current main (`057cb56`), inquiry preselection, English preference, visible missing-WhatsApp feedback, $55 bundle, carousel ordering, normal advertising landings, invalid query rejection, no-JS catalogue and zero uncaught JavaScript errors.
