(function () {
  'use strict';

  var keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];

  function attribution() {
    var query = new URLSearchParams(location.search);
    var result = {};
    keys.forEach(function (key) {
      try {
        if (query.get(key)) sessionStorage.setItem(key, query.get(key));
        result[key] = sessionStorage.getItem(key) || '';
      } catch (error) {
        result[key] = '';
      }
    });
    return result;
  }

  function deliver(details) {
    var payload = JSON.stringify(details);
    try {
      if (navigator.sendBeacon) {
        navigator.sendBeacon('/api/event', new Blob([payload], { type: 'application/json' }));
        return;
      }
    } catch (error) {}
    fetch('/api/event', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: payload,
      keepalive: true
    }).catch(function () {});
  }

  window.evAttribution = attribution;
  window.evTrack = function (name, params) {
    var details = Object.assign({
      event: name,
      page: location.pathname,
      page_title: document.title
    }, attribution(), params || {});
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(details);
    deliver(details);
  };

  document.addEventListener('click', function (event) {
    var target = event.target.closest('a,button');
    if (!target) return;
    var href = target.getAttribute('href') || '';
    var label = (target.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 120);
    var named = target.getAttribute('data-track');
    if (named) window.evTrack(named, { label: label, href: href });
    else if (href.indexOf('wa.me') > -1) window.evTrack('whatsapp_click', { href: href, label: label });
    else if (/^tel:/i.test(href)) window.evTrack('phone_click', { href: href, label: label });
    else if (/\.pdf(?:$|\?)/i.test(href)) window.evTrack('brochure_download', { href: href, label: label });
    else if (href === '#contact' || /contact(?:\.html)?(?:#.*)?$/i.test(href)) window.evTrack('price_list_click', { href: href, label: label });
  });

  attribution();
})();
