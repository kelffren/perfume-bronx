/* Share only the canonical URL: never cart data, personal details or query strings. */
(() => {
  const button = document.querySelector('.share-button');
  const canonical = document.querySelector('link[rel="canonical"]');
  if (!button || !canonical) return;
  const status = document.getElementById('share-status');
  const es = document.documentElement.lang === 'es';
  const copy = async () => {
    if (!navigator.clipboard?.writeText) {
      status.textContent = es ? 'Mantén pulsado el enlace de abajo para copiarlo.' : 'Press and hold the link below to copy it.';
      return;
    }
    try {
      await navigator.clipboard.writeText(canonical.href);
      status.textContent = es ? 'Enlace copiado.' : 'Link copied.';
    } catch {
      status.textContent = es ? 'Puedes copiar el enlace de abajo.' : 'You can copy the link below.';
    }
  };
  button.hidden = false;
  button.addEventListener('click', async () => {
    button.disabled = true;
    status.textContent = '';
    try {
      if (navigator.share) {
        try { await navigator.share({title: document.title, url: canonical.href}); }
        catch (error) { if (error.name !== 'AbortError') await copy(); }
      } else await copy();
    } finally { button.disabled = false; }
  });
})();
