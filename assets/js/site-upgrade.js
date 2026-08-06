(function () {
  'use strict';

  const TEXT = {
    en: {
      required: 'Please enter your name and a WhatsApp number or email address.',
      sending: 'Sending…',
      button: 'Send Price List',
      success: 'Thank you. Our advisor will contact you shortly and send the current price list and available plots.',
      error: 'The form could not be sent. Please try again or contact us on WhatsApp.'
    },
    fr: {
      required: 'Veuillez saisir votre nom et un numéro WhatsApp ou une adresse e-mail.',
      sending: 'Envoi…',
      button: 'Recevoir les prix',
      success: 'Merci. Notre conseiller vous contactera prochainement avec les prix actuels et les terrains disponibles.',
      error: 'Le formulaire n’a pas pu être envoyé. Réessayez ou contactez-nous sur WhatsApp.'
    },
    ar: {
      required: 'يرجى إدخال الاسم ورقم واتساب أو البريد الإلكتروني.',
      sending: 'جارٍ الإرسال…',
      button: 'إرسال قائمة الأسعار',
      success: 'شكرًا لك. سيتواصل معك مستشارنا قريبًا ويرسل قائمة الأسعار الحالية والأراضي المتاحة.',
      error: 'تعذر إرسال النموذج. يرجى المحاولة مرة أخرى أو التواصل معنا عبر واتساب.'
    }
  };

  function locale() {
    const lang = (document.documentElement.lang || 'en').toLowerCase();
    return lang.startsWith('fr') ? 'fr' : lang.startsWith('ar') ? 'ar' : 'en';
  }

  function tracking() {
    const params = new URLSearchParams(location.search);
    ['utm_source', 'utm_medium', 'utm_campaign'].forEach(function (key) {
      if (params.get(key)) sessionStorage.setItem(key, params.get(key));
    });
    return {
      utm_source: sessionStorage.getItem('utm_source') || '',
      utm_medium: sessionStorage.getItem('utm_medium') || '',
      utm_campaign: sessionStorage.getItem('utm_campaign') || ''
    };
  }

  function initNav() {
    const nav = document.getElementById('nav');
    if (!nav) return;
    function sync() { nav.classList.toggle('solid', window.scrollY > 48); }
    sync();
    window.addEventListener('scroll', sync, { passive: true });
  }

  function initLightbox() {
    const box = document.getElementById('upgrade-lightbox');
    if (!box) return;
    const image = box.querySelector('img');
    const close = box.querySelector('.upgrade-lightbox-close');
    let opener = null;

    function shut() {
      box.classList.remove('open');
      box.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      if (opener) opener.focus();
    }

    document.querySelectorAll('[data-lightbox]').forEach(function (button) {
      button.addEventListener('click', function () {
        const source = button.querySelector('img');
        if (!source) return;
        opener = button;
        image.src = source.currentSrc || source.src;
        image.alt = source.alt || '';
        box.classList.add('open');
        box.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        close.focus();
      });
    });

    close.addEventListener('click', shut);
    box.addEventListener('click', function (event) { if (event.target === box) shut(); });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && box.classList.contains('open')) shut();
    });
  }

  function initForms() {
    const t = TEXT[locale()];
    document.querySelectorAll('[data-lead-form]').forEach(function (form) {
      const name = form.querySelector('[name="name"]');
      const contact = form.querySelector('[name="contact"]');
      const interest = form.querySelector('[name="interest"]');
      const button = form.querySelector('button[type="submit"]');
      const status = form.querySelector('[role="status"]');
      let sending = false;

      function message(type, text) {
        status.className = 'upgrade-form-status ' + type;
        status.textContent = text;
        status.hidden = !text;
      }

      form.addEventListener('submit', async function (event) {
        event.preventDefault();
        if (sending) return;
        const nameValue = name.value.trim();
        const contactValue = contact.value.trim();
        if (!nameValue || !contactValue) {
          message('error', t.required);
          (!nameValue ? name : contact).focus();
          return;
        }

        sending = true;
        button.disabled = true;
        button.textContent = t.sending;
        message('', '');
        const isEmail = contactValue.indexOf('@') !== -1;
        const payload = Object.assign({
          name: nameValue,
          email: isEmail ? contactValue : '',
          phone: isEmail ? '' : contactValue,
          interest: interest ? interest.value : '',
          page: document.title
        }, tracking());

        try {
          const response = await fetch('/api/lead', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          const result = await response.json();
          if (!response.ok || result.ok !== true) throw new Error('Delivery failed');
          form.reset();
          message('success', t.success);
        } catch (error) {
          message('error', t.error);
        } finally {
          sending = false;
          button.disabled = false;
          button.textContent = t.button;
        }
      });
    });
  }

  function initVillaStructuredData() {
    const holder = document.querySelector('[data-villa-detail]');
    if (!holder || !window.EmpathiaData) return;
    const key = holder.getAttribute('data-villa-detail');
    const villa = window.EmpathiaData.villas[key];
    if (!villa) return;
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.text = JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'Offer',
      price: String(villa.price),
      priceCurrency: 'USD',
      url: 'https://empathia-seychelles.com/' + villa.page.replace('.html', ''),
      itemOffered: {
        '@type': 'SingleFamilyResidence',
        name: villa.name,
        numberOfBedrooms: villa.bedrooms,
        numberOfRooms: villa.bedrooms,
        numberOfFloors: villa.floors,
        floorSize: { '@type': 'QuantitativeValue', value: villa.area, unitText: 'm²' },
        additionalProperty: [
          { '@type': 'PropertyValue', name: 'Plot size from', value: villa.plot + ' m²' },
          { '@type': 'PropertyValue', name: 'Ownership', value: 'Freehold, subject to applicable approvals' }
        ]
      }
    });
    document.head.appendChild(script);
  }

  function init() {
    tracking();
    initNav();
    initLightbox();
    initForms();
    initVillaStructuredData();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
