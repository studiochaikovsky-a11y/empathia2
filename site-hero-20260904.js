(function () {
  'use strict';
  const hero = document.querySelector('[data-hero-slideshow]');
  if (!hero) return;
  const slides = Array.from(hero.querySelectorAll('.ev-hero-slide'));
  const controls = hero.querySelector('.ev-hero-controls');
  const play = controls.querySelector('[data-hero-play]');
  const caption = hero.querySelector('.ev-hero-caption');
  const compact = matchMedia('(max-width: 720px)');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const loads = new Map();
  let current = 0, timer = null, request = 0, paused = false, hovered = false, focused = false, visible = true;
  hero.classList.add('is-enhanced');

  function load(index) {
    if (loads.has(index)) return loads.get(index);
    const image = slides[index].querySelector('img');
    const loading = new Promise(resolve => {
      if (image.complete && image.naturalWidth) return resolve(true);
      image.addEventListener('load', () => resolve(true), { once: true });
      image.addEventListener('error', () => resolve(false), { once: true });
      if (image.dataset.src) { image.src = image.dataset.src; delete image.dataset.src; }
    });
    loads.set(index, loading);
    return loading;
  }
  function stopped() { return paused || compact.matches || reduced.matches || document.hidden || !visible || hovered || focused; }
  function sync() {
    clearTimeout(timer);
    hero.classList.toggle('is-suspended', stopped());
    hero.classList.toggle('is-user-paused', paused);
    controls.hidden = compact.matches;
    play.hidden = reduced.matches;
    play.setAttribute('aria-label', paused ? play.dataset.playLabel : play.dataset.pauseLabel);
    play.setAttribute('aria-pressed', String(paused));
    if (!stopped()) timer = setTimeout(() => show((current + 1) % slides.length), 8000);
  }
  async function show(index, manual = false) {
    clearTimeout(timer);
    if (compact.matches) return;
    const ticket = ++request;
    if (manual) { paused = true; sync(); }
    const loaded = await load(index);
    if (ticket !== request || compact.matches) return;
    if (!loaded) { paused = true; sync(); return; }
    if (!manual && stopped()) { sync(); return; }
    if (index !== current) {
      slides.forEach((slide, i) => {
        slide.classList.toggle('is-leaving', i === current);
        slide.classList.toggle('is-active', i === index);
        slide.setAttribute('aria-hidden', String(i !== index));
      });
      current = index;
      hero.querySelector('[data-hero-current]').textContent = String(index + 1).padStart(2, '0');
      caption.setAttribute('aria-live', manual ? 'polite' : 'off');
      caption.querySelector('strong').textContent = slides[index].dataset.title;
      caption.querySelector('span').textContent = slides[index].dataset.note;
    }
    sync();
  }
  controls.querySelector('[data-hero-prev]').addEventListener('click', () => show((current + slides.length - 1) % slides.length, true));
  controls.querySelector('[data-hero-next]').addEventListener('click', () => show((current + 1) % slides.length, true));
  play.addEventListener('click', () => { paused = !paused; sync(); });
  hero.addEventListener('mouseenter', () => { hovered = true; sync(); });
  hero.addEventListener('mouseleave', () => { hovered = false; sync(); });
  hero.addEventListener('focusin', () => { focused = true; sync(); });
  hero.addEventListener('focusout', () => { setTimeout(() => { focused = hero.contains(document.activeElement); sync(); }, 0); });
  document.addEventListener('visibilitychange', sync);
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting; sync(); }, { threshold: .1 }).observe(hero);
  reduced.addEventListener('change', sync);
  compact.addEventListener('change', () => {
    ++request;
    if (compact.matches) {
      current = 0;
      slides.forEach((slide, i) => { slide.classList.toggle('is-active', i === 0); slide.classList.remove('is-leaving'); slide.setAttribute('aria-hidden', String(i !== 0)); });
      hero.querySelector('[data-hero-current]').textContent = '01';
      caption.setAttribute('aria-live', 'off');
      caption.querySelector('strong').textContent = slides[0].dataset.title;
      caption.querySelector('span').textContent = slides[0].dataset.note;
    }
    sync();
  });
  // Only the first image is requested on mobile. Desktop prepares the next
  // image after the first has decoded, without competing with its initial load.
  load(0).then(() => {
    sync();
    if (!compact.matches && !reduced.matches) setTimeout(() => { if (!compact.matches) load(1); }, 1800);
  });
  sync();
})();
