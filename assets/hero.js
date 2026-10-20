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
