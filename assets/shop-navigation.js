(() => {
  const connection = navigator.connection;
  if (connection?.saveData || /2g/.test(connection?.effectiveType || ""))
    return;
  const prefetched = new Set();
  function anticipate(event) {
    const link = event.target.closest?.("a[href]");
    if (
      !link ||
      link.origin !== location.origin ||
      !/\/products\/(yara|asad|khamrah)\/$/.test(link.pathname) ||
      prefetched.has(link.href)
    )
      return;
    prefetched.add(link.href);
    const hint = document.createElement("link");
    hint.rel = "prefetch";
    hint.as = "document";
    hint.href = link.href;
    document.head.append(hint);
  }
  document.addEventListener("pointerover", anticipate, { passive: true });
  document.addEventListener("focusin", anticipate);
})();
