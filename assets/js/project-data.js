(function () {
  'use strict';

  const DATA = {
    project: {
      name: 'Empathia Village',
      plots: 30,
      availabilityShownOnMasterplan: true,
      adjacentPlotsCanBeCombined: true,
      plotMin: 600,
      plotMax: 2000,
      ownership: 'Freehold ownership, subject to applicable approvals',
      location: 'Baie Lazare, Mahé, Seychelles',
      setting: 'Between Four Seasons Resort Seychelles and Kempinski Seychelles Resort',
      beachTime: '2 minutes',
      airportTime: '30 minutes by car',
      constructionStatus: 'Construction underway',
      constructionStage: 'Phase I foundation works are underway',
      constructionUpdated: 'June 2026',
      estateCompletionYear: 2030,
      developer: 'Kensington Construction & Development',
      developerExperience: 'Over 30 years of international experience',
      licenseClass: 'Class I Building Contractor',
      licenseNumber: '322704',
      licenseValidThrough: 2028,
      agentCommissionFromPercent: 3,
      contactEmail: 'info@empathia-seychelles.com',
      contactPhone: '+248 271 51 02',
      whatsapp: 'https://wa.me/2482715102'
    },
    villas: {
      jane: {
        slug: 'jane',
        name: 'Villa Jane',
        price: 990000,
        area: 140,
        plot: 600,
        bedrooms: 2,
        floors: 1,
        image: 'assets/images/villas/jane/villa-jane-card.webp',
        hero: 'assets/images/villas/jane/villa-jane-il.webp',
        plan: 'assets/images/villas/jane/villa-jane-sheet.webp',
        page: 'villa-jane.html',
        description: 'A refined single-storey residence with panoramic glazing, two bedrooms, a private pool and an effortless indoor-outdoor plan.',
        descriptions: {
          fr: 'Une résidence raffinée de plain-pied avec vitrage panoramique, deux chambres, piscine privée et espaces ouverts sur l’extérieur.',
          ar: 'فيلا راقية من طابق واحد بزجاج بانورامي وغرفتي نوم ومسبح خاص وتصميم منفتح على المساحات الخارجية.'
        }
      },
      anna: {
        slug: 'anna',
        name: 'Villa Anna',
        price: 1500000,
        area: 240,
        plot: 600,
        bedrooms: 3,
        floors: 2,
        image: 'assets/images/villas/anna/villa-anna-card.webp',
        hero: 'assets/images/villas/anna/villa-anna-il.webp',
        plan: 'assets/images/villas/anna/villa-anna-sheet.webp',
        page: 'villa-anna.html',
        description: 'An elegant two-storey villa with generous living spaces, panoramic glazing, a private pool and a sun terrace.',
        descriptions: {
          fr: 'Une élégante villa sur deux niveaux avec de généreux espaces, vitrage panoramique, piscine privée et terrasse ensoleillée.',
          ar: 'فيلا أنيقة من طابقين بمساحات واسعة وزجاج بانورامي ومسبح خاص وتراس شمسي.'
        }
      },
      georgette: {
        slug: 'georgette',
        name: 'Villa Georgette',
        price: 2100000,
        area: 350,
        plot: 1500,
        bedrooms: 4,
        floors: 3,
        image: 'assets/images/villas/georgette/villa-georgette-card.webp',
        hero: 'assets/images/villas/georgette/villa-georgette-il.webp',
        plan: 'assets/images/villas/georgette/villa-georgette-sheet.webp',
        page: 'villa-georgette.html',
        description: 'The signature three-storey villa with four bedrooms, panoramic terraces, a private pool and elevated Indian Ocean views.',
        descriptions: {
          fr: 'La villa signature sur trois niveaux avec quatre chambres, terrasses panoramiques, piscine privée et vue sur l’océan Indien.',
          ar: 'الفيلا الرئيسية من ثلاثة طوابق، بأربع غرف نوم وتراسات بانورامية ومسبح خاص وإطلالات مرتفعة على المحيط الهندي.'
        }
      }
    },
    legal: {
      residence: 'Residency support is available. Eligibility is subject to approval by the relevant Seychelles authorities.',
      rental: 'Rental rates and occupancy figures are indicative only and are not guaranteed.',
      pricing: 'Prices and availability are confirmed individually and do not constitute a public offer.'
    }
  };

  const COPY = {
    en: {
      from: 'From', area: 'House', plot: 'Plot', bedrooms: 'Bedrooms', floors: 'Floors',
      view: 'View Villa', request: 'Request Details', residence: 'Residence'
    },
    fr: {
      from: 'À partir de', area: 'Maison', plot: 'Terrain', bedrooms: 'Chambres', floors: 'Niveaux',
      view: 'Voir la villa', request: 'Recevoir les détails', residence: 'Résidence'
    },
    ar: {
      from: 'ابتداءً من', area: 'مساحة المنزل', plot: 'مساحة الأرض', bedrooms: 'غرف النوم', floors: 'الطوابق',
      view: 'عرض الفيلا', request: 'طلب التفاصيل', residence: 'فيلا'
    }
  };

  function locale() {
    const lang = (document.documentElement.lang || 'en').toLowerCase();
    return lang.startsWith('fr') ? 'fr' : lang.startsWith('ar') ? 'ar' : 'en';
  }

  function money(value) {
    return '$' + Number(value).toLocaleString('en-US');
  }

  function rootPrefix() {
    return location.pathname.indexOf('/fr/') !== -1 || location.pathname.indexOf('/ar/') !== -1 ? '../' : '';
  }

  function villaCard(villa, lang) {
    const c = COPY[lang];
    const prefix = rootPrefix();
    return '<article class="upgrade-villa-card">' +
      '<a class="upgrade-villa-image" href="' + prefix + villa.page + '">' +
        '<img src="' + prefix + villa.image + '" alt="' + villa.name + ' at Empathia Village in Baie Lazare" loading="lazy" decoding="async" width="1254" height="1254">' +
      '</a>' +
      '<div class="upgrade-villa-copy">' +
        '<p class="upgrade-kicker">' + c.residence + '</p>' +
        '<h3>' + villa.name + '</h3>' +
        '<p class="upgrade-villa-price">' + c.from + ' ' + money(villa.price) + '</p>' +
        '<dl class="upgrade-specs">' +
          '<div><dt>' + c.area + '</dt><dd>' + villa.area + ' m²+</dd></div>' +
          '<div><dt>' + c.plot + '</dt><dd>' + villa.plot.toLocaleString('en-US') + ' m²+</dd></div>' +
          '<div><dt>' + c.bedrooms + '</dt><dd>' + villa.bedrooms + '</dd></div>' +
          '<div><dt>' + c.floors + '</dt><dd>' + villa.floors + '</dd></div>' +
        '</dl>' +
        '<p class="upgrade-villa-description">' + (villa.descriptions && villa.descriptions[lang] ? villa.descriptions[lang] : villa.description) + '</p>' +
        '<div class="upgrade-card-actions">' +
          '<a class="upgrade-link" href="' + prefix + villa.page + '">' + c.view + '</a>' +
          '<a class="upgrade-link upgrade-link-muted" href="#contact" data-interest="' + villa.name + '">' + c.request + '</a>' +
        '</div>' +
      '</div>' +
    '</article>';
  }

  function renderCards() {
    const lang = locale();
    const html = Object.keys(DATA.villas).map(function (key) {
      return villaCard(DATA.villas[key], lang);
    }).join('');
    document.querySelectorAll('[data-villa-grid]').forEach(function (grid) {
      grid.innerHTML = html;
    });
  }

  function renderVillaDetail() {
    const target = document.querySelector('[data-villa-detail]');
    if (!target) return;
    const key = target.getAttribute('data-villa-detail');
    const villa = DATA.villas[key];
    if (!villa) return;
    const nodes = document.querySelectorAll('[data-villa-field]');
    nodes.forEach(function (node) {
      const field = node.getAttribute('data-villa-field');
      if (field === 'price') node.textContent = money(villa.price);
      else if (field === 'area') node.textContent = villa.area + ' m²+';
      else if (field === 'plot') node.textContent = villa.plot.toLocaleString('en-US') + ' m²+';
      else if (field === 'floors') node.textContent = villa.floors;
      else node.textContent = villa[field] || '';
    });
  }

  function bindInterests() {
    document.querySelectorAll('[data-interest]').forEach(function (link) {
      link.addEventListener('click', function () {
        const field = document.getElementById('lead-interest');
        if (field) field.value = link.getAttribute('data-interest');
      });
    });
  }

  function fixLegacyData() {
    document.querySelectorAll('a, button').forEach(function (node) {
      if (node.childElementCount === 0 && node.textContent.trim() === 'Residencies') node.textContent = 'Residences';
    });

    const georgette = document.getElementById('georgette');
    if (georgette) {
      georgette.querySelectorAll('.res-feat').forEach(function (node) {
        node.textContent = node.textContent.replace('Two floors', 'Three floors');
      });
      georgette.querySelectorAll('.body').forEach(function (node) {
        node.textContent = node.textContent.replace('two-storey', 'three-storey');
      });
    }

    if (document.body.classList.contains('pricing-page')) {
      const panel = document.getElementById('p-georgette');
      if (panel) {
        panel.querySelectorAll('*').forEach(function (node) {
          if (node.childElementCount === 0) {
            node.textContent = node.textContent.replace('Two Storeys', 'Three Storeys').replace('two-storey', 'three-storey').replace('Two floors', 'Three floors');
          }
        });
      }
    }
  }

  function renderLegacyVillaSources() {
    const cardOrder = ['jane', 'anna', 'georgette'];
    document.querySelectorAll('.res-card').forEach(function (card, index) {
      const villa = DATA.villas[cardOrder[index]];
      if (!villa) return;
      const price = card.querySelector('.res-card-price');
      const meta = card.querySelector('.res-card-meta');
      if (price) price.textContent = 'From ' + money(villa.price);
      if (meta) meta.textContent = villa.bedrooms + ' bedrooms · ' + villa.floors + ' ' + (villa.floors === 1 ? 'floor' : 'floors') + ' · from ' + villa.area + ' m² · plot from ' + villa.plot.toLocaleString('en-US') + ' m²';
      card.href = villa.page;
    });

    cardOrder.forEach(function (key) {
      const villa = DATA.villas[key];
      const section = document.getElementById(key);
      if (section) {
        const price = section.querySelector('.res-price');
        const note = section.querySelector('.res-price-note');
        const specs = section.querySelector('.res-specs');
        const description = section.querySelector('.body');
        if (price) price.textContent = 'From ' + money(villa.price);
        if (note) note.textContent = 'Plot from ' + villa.plot.toLocaleString('en-US') + ' m² · Not a public offer';
        if (specs) specs.innerHTML =
          '<div class="res-spec"><div class="res-spec-v">from ' + villa.area + '</div><div class="res-spec-k">m² Area</div></div>' +
          '<div class="res-spec"><div class="res-spec-v">' + villa.bedrooms + '</div><div class="res-spec-k">Bedrooms</div></div>' +
          '<div class="res-spec"><div class="res-spec-v">' + villa.floors + '</div><div class="res-spec-k">Floors</div></div>' +
          '<div class="res-spec"><div class="res-spec-v">from ' + villa.plot.toLocaleString('en-US') + '</div><div class="res-spec-k">m² Plot</div></div>';
        if (description) description.textContent = villa.description + ' Individual adaptations are available subject to technical review and an agreed specification.';
      }

      const panel = document.getElementById('p-' + key);
      if (panel && panel.classList.contains('villa-panel')) {
        const type = panel.querySelector('.villa-type');
        const specs = panel.querySelector('.villa-specs');
        const price = panel.querySelector('.villa-price');
        const note = panel.querySelector('.villa-price-note');
        const description = panel.querySelector('.villa-desc');
        if (type) type.textContent = villa.floors + ' ' + (villa.floors === 1 ? 'Floor' : 'Floors') + ' · Private Pool';
        if (specs) specs.innerHTML =
          '<div class="vs"><div class="vs-n">from ' + villa.area + '</div><div class="vs-l">m² Area</div></div>' +
          '<div class="vs"><div class="vs-n">' + villa.bedrooms + '</div><div class="vs-l">Bedrooms</div></div>' +
          '<div class="vs"><div class="vs-n">' + villa.floors + '</div><div class="vs-l">Floors</div></div>' +
          '<div class="vs"><div class="vs-n">from ' + villa.plot.toLocaleString('en-US') + '</div><div class="vs-l">m² Plot</div></div>';
        if (price) price.textContent = 'from ' + money(villa.price);
        if (note) note.textContent = 'Starting price · Plot from ' + villa.plot.toLocaleString('en-US') + ' m² · Not a public offer';
        if (description) description.textContent = villa.description;
      }
    });
  }

  window.EmpathiaData = DATA;
  window.EmpathiaMoney = money;

  function init() {
    renderCards();
    renderVillaDetail();
    renderLegacyVillaSources();
    bindInterests();
    fixLegacyData();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
