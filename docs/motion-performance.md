# Motion and interaction refinement — 2026-10-18

Preserves the Kelo Diamonds reference palette, fonts, section structure and pill controls. The user requested Apple-inspired maturity and fluidity, not an Apple visual clone.

## Research

- Apple Motion HIG: https://developer.apple.com/design/human-interface-guidelines/motion
  Motion should explain state, provide feedback and preserve orientation.
- Apple accessibility: https://developer.apple.com/help/app-store-connect/manage-app-accessibility/reduced-motion-evaluation-criteria
  Respect reduced motion; avoid unnecessary depth and perpetual movement.
- WebKit: https://webkit.org/blog/10266/web-animations-in-safari-13-1/
  Browser-managed CSS/Web Animations integrate with rendering and can use acceleration.

## Applied decisions

- Shared 120/240/360/600 ms timings using the existing cubic-bezier(.22,1,.36,1). These are project choices, not claimed universal Apple timings.
- Press feedback is immediate and subtle; hover effects only run for fine pointers.
- Mobile order panel slides vertically; desktop remains a lateral drawer. Reversing the CSS transition handles rapid open/close without timer races.
- Closed panel, navigation and floating CTA cannot receive focus. Background becomes inert during a modal. Closing restores focus and scroll position.
- Floating CTA appears after the hero passes the header, not just because the catalog is outside the viewport.
- Reveal uses transform and opacity only, below the fold, once; content defaults to visible without animation support. Reduced-motion changes are respected during the session.
- Removed continuously floating hero decoration, animated shadows and hover rotations. No new runtime dependencies or scroll listeners.
- Two CDN images request 720px rather than 1024/1445px. Actual network savings depend on CDN responses; not measured. Existing dimensions, lazy loading and async decoding retained.

## Verification and limits

JavaScript syntax checked. Browser testing attempted but initially blocked by missing Playwright browser binaries. No FPS, Core Web Vitals or real-iPhone claims can be made without measurement. Remote product photography is still an external dependency. WhatsApp number remains empty in CONFIG and must be confirmed before live orders.

Recommended device acceptance: 384×856 and desktop; open/close panel rapidly, change quantities, switch languages, keyboard Tab/Escape, return scroll position, reduced motion, image failures and successful WhatsApp handoff with a verified number. Target LCP <=2.5s, INP <=200ms and CLS <=0.1 are future measurement criteria, not results.
