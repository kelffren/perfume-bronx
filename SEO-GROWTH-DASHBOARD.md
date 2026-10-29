# SEO Growth Dashboard — measurement specification

Status: specification only. No Search Console, GA4 or Plausible access verified as of 2026-10-29.

| KPI | Definition | Source | Frequency |
|---|---|---|---|
| Organic impressions | Search result appearances | Google Search Console | Weekly |
| Organic clicks | Clicks from Google results | Google Search Console | Weekly |
| Organic CTR | Clicks / impressions | Google Search Console | Weekly |
| Indexed URLs | Google-reported indexed pages, not merely sitemap URLs | Search Console Page indexing | Weekly |
| Organic landing sessions | Sessions with organic search acquisition | Consented analytics | Weekly |
| Article-to-product | Product visits from guide pages / guide sessions | Consented analytics | Weekly |
| WhatsApp initiation | Outbound WhatsApp CTA clicks; **not** confirmed conversations | Consent-aware event tracking | Weekly |
| Confirmed paid orders | Orders delivered and paid | Manual ledger or CRM | Weekly |
| Customer acquisition cost | Attributed acquisition spend / paid customers | Ads and order ledger | Monthly |

## Implementation safeguards
- Do not claim visitor-level localStorage counters are aggregated analytics.
- Never put private keys, customer addresses or contact details in public GitHub files.
- Tag article-to-product and WhatsApp links only after reviewing privacy/consent requirements.
- Separate impressions, clicks, inquiries, confirmed orders and profit; do not count them interchangeably.
- Compare pages by search intent and baseline period, not only raw traffic.

## First operational checklist
- [ ] Confirm Search Console site ownership and query coverage.
- [ ] Submit the verified sitemap and inspect indexing diagnostics.
- [ ] Confirm an analytics provider and privacy configuration.
- [ ] Record a baseline of indexed pages, clicks, impressions and top queries.
- [ ] Record the actual business WhatsApp destination and test on mobile.
- [ ] Define a private paid-order ledger to close the attribution loop.
