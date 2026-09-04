/* Interaction enhancement only: navigation content is rendered in every HTML page. */
(function () {
  'use strict';
  var header = document.getElementById('site-header');
  if (!header) return;
  var toggle = header.querySelector('.ev-menu-toggle');
  var panel = header.querySelector('.ev-panel');
  var groups = Array.from(header.querySelectorAll('.ev-group'));
  var compact = window.matchMedia('(max-width: 1439px)');
  var oldOverflow = '';
  header.classList.add('ev-enhanced');

  function closeGroups(except) {
    groups.forEach(function (group) { if (group !== except) group.open = false; });
  }
  function setMenu(open, returnFocus) {
    var wasOpen = header.classList.contains('is-menu-open');
    if (open && !wasOpen) oldOverflow = document.body.style.overflow;
    header.classList.toggle('is-menu-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    if (open) document.body.style.overflow = 'hidden';
    else if (wasOpen) document.body.style.overflow = oldOverflow;
    if (!open) closeGroups();
    if (returnFocus) toggle.focus();
  }
  toggle.addEventListener('click', function () {
    var open = !header.classList.contains('is-menu-open');
    setMenu(open, false);
    if (open) panel.querySelector('a, summary').focus();
  });
  groups.forEach(function (group) {
    // Native details supplies keyboard and touch support even without JavaScript.
    group.querySelector('summary').addEventListener('click', function () { if (!group.open) closeGroups(group); });
  });
  document.addEventListener('click', function (event) {
    if (!header.contains(event.target)) setMenu(false, false);
  });
  header.addEventListener('click', function (event) {
    if (event.target.closest('a')) setMenu(false, false);
  });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
      var expanded = groups.find(function (group) { return group.open; });
      if (expanded) { expanded.open = false; expanded.querySelector('summary').focus(); }
      else if (header.classList.contains('is-menu-open')) setMenu(false, true);
    }
    if (event.key !== 'Tab' || !compact.matches || !header.classList.contains('is-menu-open')) return;
    var focusable = Array.from(header.querySelectorAll('a, button, summary')).filter(function (el) { return el.getClientRects().length; });
    var first = focusable[0], last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  });
  header.addEventListener('focusout', function () {
    setTimeout(function () { if (!header.contains(document.activeElement)) closeGroups(); }, 0);
  });
  compact.addEventListener('change', function () {
    var focusInside = panel.contains(document.activeElement);
    setMenu(false, compact.matches && focusInside);
  });

  // Preserve the existing quick-contact action on pages where the old mobile
  // script created it. The legacy script still supplies its marketing helpers.
  if (!document.querySelector('.upgrade-mobile-cta, .mobile-sticky-cta')) {
    var cta = document.createElement('div');
    cta.className = 'mobile-sticky-cta';
    cta.setAttribute('aria-label', header.dataset.contactLabel);
    var price = header.querySelector('.ev-price').cloneNode(true);
    price.removeAttribute('class');
    var wa = document.createElement('a');
    wa.href = 'https://wa.me/2482715102'; wa.target = '_blank'; wa.rel = 'noopener'; wa.textContent = 'WhatsApp';
    cta.append(price, wa);
    document.body.appendChild(cta);
  }
})();
