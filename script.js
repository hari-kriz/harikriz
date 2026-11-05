(function () {
  var toggle = document.getElementById('navToggle');
  var links = document.getElementById('navLinks');

  function closeMenu() {
    if (!links.classList.contains('is-open')) return;
    links.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.textContent = 'Menu';
  }

  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.textContent = open ? 'Close' : 'Menu';
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') closeMenu();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });
  }

  // Highlight the section in view in the navigation.
  if ('IntersectionObserver' in window && links) {
    var navFor = {};
    links.querySelectorAll('a[href^="#"]').forEach(function (a) { navFor[a.getAttribute('href').slice(1)] = a; });
    var sections = Object.keys(navFor).map(function (id) { return document.getElementById(id); }).filter(Boolean);
    var current = null;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        if (current) { current.classList.remove('is-active'); current.removeAttribute('aria-current'); }
        current = navFor[en.target.id];
        if (current) { current.classList.add('is-active'); current.setAttribute('aria-current', 'true'); }
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    sections.forEach(function (s) { io.observe(s); });
  }

  // Local time in Bengaluru, next to the contact status.
  var clock = document.getElementById('localTime');
  if (clock) {
    var fmt = new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Asia/Kolkata' });
    var tick = function () { clock.textContent = ', ' + fmt.format(new Date()) + ' IST'; };
    tick();
    setInterval(tick, 30000);
  }
})();
