/* Progressive enhancement: semantic scenes and native disclosures work without JS. */
(() => {
  'use strict';
  const root = document.querySelector('[data-cinema]');
  if (!root) return;
  const scenes = [...root.querySelectorAll('.cinema-scene')];
  const links = [...root.querySelectorAll('.chapter-link')];
  const controls = root.querySelector('.cinema-controls');
  const prev = controls.querySelector('[data-prev]');
  const next = controls.querySelector('[data-next]');
  const motion = controls.querySelector('[data-motion]');
  const reading = controls.querySelector('[data-reading]');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let index = 0;
  let readAll = false;
  let animate = !reduced.matches;
  const fromURL = () => {
    const match = location.hash.match(/^#scene-(\d+)$/);
    const old = Number(new URL(location.href).searchParams.get('slide'));
    return match && Number(match[1])>=1 && Number(match[1])<=scenes.length ? Number(match[1])-1 : Number.isInteger(old) && old>=1 && old<=scenes.length ? old-1 : 0;
  };
  function setMotion() {
    root.classList.toggle('cinema-still', !animate || reduced.matches);
    motion.setAttribute('aria-pressed', String(animate && !reduced.matches));
  }
  function show(n, options = {}) {
    const before = index;
    index = Math.max(0, Math.min(scenes.length-1, n));
    root.style.setProperty('--direction', index < before ? '-18px' : '18px');
    scenes.forEach((scene, i) => {
      scene.classList.toggle('is-active', i === index);
      scene.inert = !readAll && i !== index;
      if (readAll) scene.removeAttribute('aria-hidden');
      else scene.setAttribute('aria-hidden', String(i !== index));
    });
    links.forEach((a,i) => i===index ? a.setAttribute('aria-current','step') : a.removeAttribute('aria-current'));
    prev.disabled = index === 0;
    next.disabled = index === scenes.length-1;
    controls.querySelector('[data-counter]').textContent = `${index+1} / ${scenes.length}`;
    controls.querySelector('.cinema-progress span').style.width = `${(index+1)/scenes.length*100}%`;
    if (options.history) {
      const url = new URL(location.href);
      url.searchParams.delete('slide');
      url.hash = scenes[index].id;
      history.pushState(null, '', url);
    }
    if (options.focus) {
      scenes[index].querySelector('h2').focus({preventScroll:true});
      scenes[index].scrollIntoView({block:'start',behavior:'instant'});
    }
  }
  root.classList.add('cinema-ready');
  controls.hidden = false;
  show(fromURL());
  setMotion();
  prev.addEventListener('click', () => show(index-1,{history:true,focus:true}));
  next.addEventListener('click', () => show(index+1,{history:true,focus:true}));
  root.addEventListener('click', event => {
    const a=event.target.closest('a[href^="#scene-"]');
    if (!a || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    show(Number(a.hash.split('-')[1])-1,{history:true,focus:true});
  });
  motion.addEventListener('click', () => {animate=!animate;setMotion();});
  reduced.addEventListener('change', () => {animate=!reduced.matches;setMotion();});
  reading.addEventListener('click', () => {
    readAll=!readAll;
    root.classList.toggle('cinema-reading',readAll);
    reading.setAttribute('aria-pressed',String(readAll));
    show(index,{focus:true});
  });
  root.addEventListener('keydown', event => {
    if (readAll || event.altKey || event.ctrlKey || event.metaKey || event.target.closest('input,select,textarea,summary,[data-tier],[data-reset]')) return;
    if (event.key==='ArrowRight' || event.key==='ArrowLeft') {
      event.preventDefault();
      show(index+(event.key==='ArrowRight'?1:-1),{history:true,focus:true});
    }
  });
  let touch = null;
  const stage=root.querySelector('.cinema-stage');
  stage.addEventListener('touchstart', event => {
    touch=null;
    if (readAll || event.touches.length!==1 || event.target.closest('a,button,summary,input,select')) return;
    touch={x:event.touches[0].clientX,y:event.touches[0].clientY};
  },{passive:true});
  stage.addEventListener('touchcancel', () => {touch=null;},{passive:true});
  stage.addEventListener('touchend', event => {
    if(!touch || !event.changedTouches.length)return;
    const dx=event.changedTouches[0].clientX-touch.x,dy=event.changedTouches[0].clientY-touch.y;
    touch=null;
    if(Math.abs(dx)>70 && Math.abs(dx)>Math.abs(dy)*1.8)show(index+(dx<0?1:-1),{history:true,focus:true});
  },{passive:true});
  window.addEventListener('popstate', () => show(fromURL(),{focus:true}));
  window.addEventListener('hashchange', () => show(fromURL()));
  const tiers=[...root.querySelectorAll('[data-tier]')];
  const panels=[...root.querySelectorAll('.tier-reading')];
  const reset=root.querySelector('[data-reset]');
  function selectTier(selected) {
    tiers.forEach((button,i) => {
      const active=selected===null || selected===i;
      button.setAttribute('aria-expanded',String(active));
      button.classList.toggle('is-selected',selected===i);
      panels[i].hidden=!active;
    });
  }
  tiers.forEach((button,i)=>button.addEventListener('click',()=>selectTier(button.classList.contains('is-selected')?null:i)));
  if (reset) reset.hidden=false;
  if (reset) reset.addEventListener('click',()=>selectTier(null));
  // Observe natural scrolling only; never intercept the wheel or lock body scrolling.
  if ('IntersectionObserver' in window) {
    const observer=new IntersectionObserver(entries=>entries.forEach(e=>e.target.classList.toggle('is-near',e.isIntersecting)),{threshold:.65});
    root.querySelectorAll('.evolution-story article').forEach(el=>observer.observe(el));
  }
})();
