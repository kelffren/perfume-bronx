(() => {
  const hero = document.querySelector('#home');
  const video = document.querySelector('#heroVideo');
  const control = document.querySelector('#heroPlayback');
  if (!hero || !video || !control) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let visible = true;
  let userPaused = false;
  let optedIn = false;
  const updateControl = () => {
    const es = document.documentElement.lang !== 'en';
    const label = video.paused ? (es ? 'Reproducir video' : 'Play video') : (es ? 'Pausar video' : 'Pause video');
    control.textContent = video.paused ? '▶' : 'Ⅱ';
    control.setAttribute('aria-label', label);
    control.title = label;
  };
  const allowed = () => optedIn || (!reduced.matches && !navigator.connection?.saveData);
  const play = () => {
    if (!visible || document.hidden || userPaused || !allowed()) return;
    if (!video.getAttribute('src')) video.src = video.dataset.src;
    video.muted = true;
    video.play().catch(updateControl);
  };
  control.hidden = false;
  control.addEventListener('click', () => {
    if (video.paused) { userPaused = false; optedIn = true; play(); }
    else { userPaused = true; video.pause(); }
  });
  video.addEventListener('playing', () => { hero.classList.add('is-playing', 'has-played'); updateControl(); });
  video.addEventListener('pause', () => { hero.classList.remove('is-playing'); updateControl(); });
  video.addEventListener('error', () => { hero.classList.remove('is-playing', 'has-played'); control.hidden = true; });
  document.addEventListener('visibilitychange', () => document.hidden ? video.pause() : play());
  reduced.addEventListener('change', () => { optedIn = false; if (reduced.matches) video.pause(); else play(); });
  new MutationObserver(updateControl).observe(document.documentElement, {attributes:true, attributeFilter:['lang']});
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; if (visible) play(); else video.pause(); }, {threshold:0}).observe(hero);
  }
  updateControl();
  play();
})();

// A single 20 CSS pixel nudge. Browser toolbar collapse is
// browser-controlled: never chase it with larger scrolls or repeated attempts.
(() => {
  const mobile = matchMedia('(max-width: 720px) and (pointer: coarse)');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const navigation = performance.getEntriesByType('navigation')[0];
  const reloading = navigation?.type === 'reload';
  if (!mobile.matches || reduced.matches || navigator.standalone ||
      matchMedia('(display-mode: standalone)').matches ||
      navigation?.type === 'back_forward' ||
      (!reloading && (location.hash || window.scrollY !== 0))) return;

  const listeners = new AbortController();
  const cancel = () => { clearTimeout(timer); listeners.abort(); };
  let timer;
  const schedule = () => { timer = setTimeout(() => {
    listeners.abort();
    if (!mobile.matches || reduced.matches || document.hidden ||
        (!reloading && (location.hash || window.scrollY !== 0)) || document.body.classList.contains('lock') ||
        document.querySelector('.menu.open,.langmenu.open')) return;
    // Override the site's smooth anchor scrolling for this imperceptible nudge.
    const root = document.documentElement;
    const previous = root.style.scrollBehavior;
    root.style.scrollBehavior = 'auto';
    window.scrollTo({top: window.scrollY + 20, left: window.scrollX, behavior: 'instant'});
    root.style.scrollBehavior = previous;
  }, 350); };
  // Let reload scroll restoration finish before applying the relative 20px nudge.
  if (document.readyState === 'complete') schedule();
  else window.addEventListener('pageshow', schedule, {once: true, signal: listeners.signal});
  // Visitor input always wins; browser restoration on reload is not user input.
  const events = ['touchstart', 'pointerdown', 'wheel', 'keydown', 'pagehide'];
  if (!reloading) events.push('scroll');
  for (const event of events) {
    window.addEventListener(event, cancel, {passive: true, signal: listeners.signal});
  }
})();
