(function () {
  'use strict';
  var d = document;

  // mobile menu
  var toggle = d.querySelector('.nav-toggle');
  var menu = d.getElementById('mobile-menu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      d.body.style.overflow = open ? 'hidden' : '';
    });
    menu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { menu.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); d.body.style.overflow = ''; }
    });
  }

  // dropdown (touch + keyboard)
  d.querySelectorAll('.dd-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      var p = b.parentElement, o = p.classList.toggle('open');
      b.setAttribute('aria-expanded', o ? 'true' : 'false');
    });
  });
  d.addEventListener('click', function (e) {
    if (!e.target.closest('.dd')) d.querySelectorAll('.dd.open').forEach(function (x) { x.classList.remove('open'); });
  });
  d.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') d.querySelectorAll('.dd.open').forEach(function (x) { x.classList.remove('open'); });
  });

  // reveal on scroll
  var els = d.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    els.forEach(function (el) { io.observe(el); });
  } else { els.forEach(function (el) { el.classList.add('in'); }); }

  // live invitation demo
  var form = d.getElementById('demo-form');
  if (form) {
    var $ = function (id) { return d.getElementById(id); };
    var sync = function () {
      var kind = $('demo-kind').value;
      var name = $('demo-name').value.trim() || 'Sofia';
      var date = $('demo-date').value;
      var place = $('demo-place').value.trim();
      var labels = { birthday: "Birthday of", wedding: "The wedding of", baby: "Baby shower for", quince: "Quinceañera of", corporate: "You're invited to" };
      $('pv-kicker').textContent = labels[kind] || 'You are invited';
      $('pv-title').textContent = name;
      var when = 'Saturday, Oct 19';
      if (date) {
        var p = date.split('-');
        var dt = new Date(+p[0], +p[1] - 1, +p[2]);
        when = dt.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });
      }
      $('pv-when').textContent = when + (place ? ' · ' + place : '');
      var wrap = $('demo-phone');
      wrap.className = 'phone theme-' + ({ birthday: 'pink', wedding: 'gold', baby: 'blue', quince: 'pink', corporate: 'green' }[kind] || 'pink');
    };
    form.addEventListener('input', sync);
    form.addEventListener('submit', function (e) { e.preventDefault(); });
    sync();
  }

  // template filter
  var chips = d.querySelectorAll('[data-filter]');
  if (chips.length) {
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
        var f = c.getAttribute('data-filter');
        d.querySelectorAll('[data-cat]').forEach(function (t) {
          var show = f === 'all' || t.getAttribute('data-cat').split(' ').indexOf(f) > -1;
          t.style.display = show ? '' : 'none';
        });
      });
    });
  }

  var y = d.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
