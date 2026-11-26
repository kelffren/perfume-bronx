const CONFIG = { whatsapp: "" };
window.OudContact?.ready.then(() => {
  if (window.OudContact.isReady())
    CONFIG.whatsapp =
      window.OudContact.url("").match(/wa\.me\/(\d+)/)?.[1] || "";
});
// Local, privacy-minimal funnel diagnostics. Counts stay on this visitor's device.
function trackFunnel(event) {
  try {
    const key = "oud-funnel-local-v1";
    const data = JSON.parse(localStorage.getItem(key) || "{}");
    data[event] = (data[event] || 0) + 1;
    localStorage.setItem(key, JSON.stringify(data));
  } catch {}
  try {
    if (typeof window.oudAnalytics === "function") window.oudAnalytics(event);
  } catch {}
}
// Optional privacy-minded aggregate analytics; configure domain in README when ready.
window.oudAnalytics = function (event) {
  if (typeof window.plausible === "function") window.plausible(event);
};
// Phase 1/5: privacy-minimal session and conversion diagnostics (no personal data).
// A WhatsApp handoff is NOT a confirmed order or sale.
(function () {
  const key = "oud-session-v1";
  let session;
  try {
    session = JSON.parse(sessionStorage.getItem(key) || "null");
    if (
      !session ||
      !session.started ||
      Date.now() - session.started > 30 * 60 * 1000
    ) {
      session = {
        started: Date.now(),
        id: Math.random().toString(36).slice(2),
      };
      sessionStorage.setItem(key, JSON.stringify(session));
      trackFunnel("session_started");
    }
  } catch {
    trackFunnel("session_started");
  }
  document.addEventListener(
    "click",
    function (e) {
      const target = e.target.closest(
        'a[href*="wa.me/"],a[href*="api.whatsapp.com/"]',
      );
      if (target) trackFunnel("whatsapp_link_clicked");
    },
    { capture: true },
  );
  window.addEventListener("pageshow", function (e) {
    if (e.persisted) trackFunnel("page_restored");
  });
})();
