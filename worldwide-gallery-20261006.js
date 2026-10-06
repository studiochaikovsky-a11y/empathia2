(() => {
  const links = [...document.querySelectorAll('.worldwide-photo')];
  const viewer = document.querySelector('.worldwide-viewer');
  if (!links.length || !viewer || typeof viewer.showModal !== 'function') return;
  const image = viewer.querySelector('img');
  let active = 0;
  let opener;
  const show = (index) => {
    active = (index + links.length) % links.length;
    image.src = links[active].href;
    image.alt = links[active].querySelector('img').alt;
  };
  links.forEach((link, index) => link.addEventListener('click', (event) => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    opener = link;
    show(index);
    viewer.showModal();
    document.documentElement.classList.add('worldwide-viewer-open');
  }));
  viewer.querySelector('.worldwide-close').addEventListener('click', () => viewer.close());
  viewer.querySelector('.worldwide-prev').addEventListener('click', () => show(active - 1));
  viewer.querySelector('.worldwide-next').addEventListener('click', () => show(active + 1));
  viewer.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      show(active + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  viewer.addEventListener('click', (event) => { if (event.target === viewer) viewer.close(); });
  viewer.addEventListener('close', () => {
    document.documentElement.classList.remove('worldwide-viewer-open');
    opener?.focus({ preventScroll: true });
  });
})();
