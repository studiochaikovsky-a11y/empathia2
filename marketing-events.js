(function () {
  'use strict';

  var keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];

  var clickKeys=['gclid','gbraid','wbraid'];
  var campaignKeys=keys.concat(['utm_id','campaign_id']);
  var attributionKey='empathia.ad-attribution.v1';
  var memoryAttribution=null,lastQuery=null;
  function leadAttribution(){
    var query=new URLSearchParams(location.search),now=Date.now(),saved=memoryAttribution;
    if(!saved)try{saved=JSON.parse(localStorage.getItem(attributionKey)||'null');}catch(error){}
    if(!saved||!Number.isFinite(Date.parse(saved.captured_at))||now-Date.parse(saved.captured_at)>30*86400000||Date.parse(saved.captured_at)>now+300000)saved={};
    var fresh={};
    clickKeys.forEach(function(key){var v=query.get(key)||'';if(/^[A-Za-z0-9_-]{5,512}$/.test(v))fresh[key]=v;});
    campaignKeys.forEach(function(key){var v=query.get(key)||'';if(v&&v.length<=200&&!/[\u0000-\u001f]/.test(v))fresh[key]=v;});
    if(Object.keys(fresh).length&&lastQuery!==location.search){
      // A new campaign replaces the previous touch; old Google click IDs must not
      // leak into a later non-Google campaign. Direct page navigation preserves it.
      saved=Object.assign(fresh,{captured_at:new Date(now).toISOString(),landing_page:location.pathname});
      try{localStorage.setItem(attributionKey,JSON.stringify(saved));}catch(error){}
    }
    lastQuery=location.search;memoryAttribution=saved;
    return Object.assign({},saved);
  }
  function attribution(){var a=leadAttribution(),out={};keys.forEach(function(key){out[key]=a[key]||'';});return out;}
  window.evLeadAttribution=leadAttribution;

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

  var reportedReceipts=Object.create(null);
  window.evTrackLeadSuccess = function (params) {
    if(location.hostname!=='empathia-seychelles.com'&&location.hostname!=='www.empathia-seychelles.com')return;
    var receipt=params&&params.lead_reference;
    if(!/^site:empathia-(en|ru):[1-9]\d*$/.test(receipt||''))return;
    if(reportedReceipts[receipt])return;reportedReceipts[receipt]=true;
    try { window.evTrack('lead_submit_success', params); } catch (error) {}
    if (typeof window.gtag === 'function') {
      // Called only after /api/lead confirms delivery. Never send form values
      // (name, phone, email, free text) to Google Analytics.
      if (location.hostname === 'empathia-seychelles.com' || location.hostname === 'www.empathia-seychelles.com') {
        window.gtag('event', 'generate_lead', {
          send_to: 'G-3G2W4S48YP',
          method: 'website_form',
          form_id: /^\/contact(?:\.html)?\/?$/.test(location.pathname) ? 'contact' : 'enquiry'
        });
      }
      window.gtag('event', 'conversion', {
        send_to: 'AW-18528545143/7NAqCKzfqqQdEPfSjINF',
        transaction_id: receipt
      });
    }
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
