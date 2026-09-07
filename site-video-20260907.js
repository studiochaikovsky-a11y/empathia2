(function () {
  'use strict';
  document.querySelectorAll('[data-construction-video]').forEach(function (video) {
    var launch = video.querySelector('[data-video-launch]');
    if (!launch) return;
    launch.addEventListener('click', function (event) {
      // Modified clicks retain the normal link behaviour.
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      var frame = document.createElement('iframe');
      var lang = (document.documentElement.lang || 'en').split('-')[0];
      frame.title = launch.getAttribute('aria-label');
      frame.src = 'https://www.youtube-nocookie.com/embed/jVrAEEEGNJw?autoplay=1&playsinline=1&rel=0&hl=' + encodeURIComponent(lang);
      frame.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen';
      frame.allowFullscreen = true;
      frame.referrerPolicy = 'strict-origin-when-cross-origin';
      video.querySelector('.ev-video-frame').replaceChildren(frame);
      frame.focus();
    }, { once: false });
  });
})();
