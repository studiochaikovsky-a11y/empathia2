(function () {
  'use strict';

  var plots = [
    { id: 'W4', area: 603.74, x: 24.7, y: 19 },
    { id: 'W3', area: 516.59, x: 32.5, y: 24 },
    { id: 'W2', area: 530.94, x: 38.0, y: 24 },
    { id: 'W1', area: 1471.51, x: 43.5, y: 24 },
    { id: 'W8', area: 1016.19, x: 24.8, y: 34 },
    { id: 'W7', area: 571.10, x: 32.7, y: 42 },
    { id: 'W6', area: 596.41, x: 38.5, y: 42 },
    { id: 'W5', area: 574.05, x: 44.5, y: 42 },
    { id: 'H11', area: 497.87, x: 48.4, y: 29 },
    { id: 'H12', area: 509.47, x: 53.3, y: 33 },
    { id: 'H9', area: 523.50, x: 59.0, y: 33 },
    { id: 'H10', area: 545.73, x: 59.0, y: 40 },
    { id: 'H8', area: null, x: 65.0, y: 40, status: 'sold' },
    { id: 'H7', area: 593.80, x: 69.0, y: 32 },
    { id: 'H6', area: null, x: 72.2, y: 41, status: 'sold' },
    { id: 'H4', area: 652.48, x: 74.6, y: 35 },
    { id: 'H5', area: 792.77, x: 77.0, y: 42 },
    { id: 'H1', area: 564.00, x: 86.1, y: 31 },
    { id: 'H2', area: 536.93, x: 86.1, y: 39 },
    { id: 'H3', area: 490.10, x: 84.2, y: 47 },
    { id: 'L10', area: 1901.74, x: 32.0, y: 48 },
    { id: 'L9', area: 1780.83, x: 32.0, y: 57 },
    { id: 'L8', area: 2217.67, x: 43.0, y: 62 },
    { id: 'L7', area: 2039.30, x: 49.0, y: 48 },
    { id: 'L6', area: 1991.15, x: 49.0, y: 63 },
    { id: 'L5', area: 2058.67, x: 55.0, y: 72 },
    { id: 'L4', area: 1560.16, x: 67.0, y: 59 },
    { id: 'L3', area: 1949.75, x: 67.0, y: 75 },
    { id: 'L2', area: 854.22, x: 75.0, y: 63, status: 'sold' },
    { id: 'L1', area: 2044.60, x: 73.0, y: 82, status: 'sold' }
  ];

  function moneyArea(value) {
    return value ? value.toLocaleString('en-US', { maximumFractionDigits: 2 }) + ' m²' : 'Confirmed in the current plot pack';
  }

  function init() {
    var root = document.querySelector('[data-interactive-masterplan]');
    if (!root) return;
    var canvas = root.querySelector('[data-masterplan-canvas]');
    var title = root.querySelector('[data-plot-title]');
    var status = root.querySelector('[data-plot-status]');
    var area = root.querySelector('[data-plot-area]');
    var note = root.querySelector('[data-plot-note]');
    var action = root.querySelector('[data-plot-action]');
    var list = root.querySelector('[data-plot-list]');
    var active = null;

    function select(plot, button) {
      if (active) active.classList.remove('is-active');
      active = button;
      if (active) active.classList.add('is-active');
      title.textContent = 'Plot ' + plot.id;
      status.textContent = plot.status === 'sold' ? 'Sold on the published masterplan' : 'Shown as on sale';
      status.className = 'upgrade-plot-status ' + (plot.status === 'sold' ? 'is-sold' : 'is-available');
      area.textContent = moneyArea(plot.area);
      note.textContent = plot.status === 'sold'
        ? 'Ask our advisor to compare neighbouring available plots with a similar position.'
        : 'Availability, exact surveyed area, suitable villa design and the option to combine adjacent plots are confirmed individually.';
      action.textContent = plot.status === 'sold' ? 'Explore available plots' : 'Request plot ' + plot.id;
      action.setAttribute('data-interest', plot.status === 'sold' ? 'Available plots' : 'Plot ' + plot.id);
      var interest = document.getElementById('lead-interest');
      if (interest) interest.value = action.getAttribute('data-interest');
      if (window.evTrack) window.evTrack('masterplan_plot_select', { interest: plot.id, plot_status: plot.status || 'available' });
    }

    plots.forEach(function (plot) {
      var marker = document.createElement('button');
      marker.type = 'button';
      marker.className = 'upgrade-plot-marker ' + (plot.status === 'sold' ? 'is-sold' : 'is-available');
      marker.style.left = plot.x + '%';
      marker.style.top = plot.y + '%';
      marker.textContent = plot.id;
      marker.setAttribute('aria-label', 'Plot ' + plot.id + ', ' + (plot.status === 'sold' ? 'sold' : 'shown as on sale'));
      marker.addEventListener('click', function () { select(plot, marker); });
      canvas.appendChild(marker);

      var chip = document.createElement('button');
      chip.type = 'button';
      chip.className = 'upgrade-plot-chip ' + (plot.status === 'sold' ? 'is-sold' : 'is-available');
      chip.textContent = plot.id;
      chip.addEventListener('click', function () { select(plot, marker); marker.scrollIntoView({ block: 'center', inline: 'center', behavior: 'smooth' }); });
      list.appendChild(chip);
    });

    action.addEventListener('click', function () {
      var interest = document.getElementById('lead-interest');
      if (interest) interest.value = action.getAttribute('data-interest') || 'Available plots';
    });

    select(plots[0], canvas.querySelector('.upgrade-plot-marker'));
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
