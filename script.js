/**
 * ============================================================
 *  LEDGERLY — App Script
 *  Renders content from content.js and handles interactivity
 * ============================================================
 *
 *  CONTACT FORM:
 *  To receive form submissions, sign up for a free account at
 *  https://formspree.io, create a form, and replace the action
 *  URL on the <form> element in the submitForm() function below.
 *
 *  Or use Netlify Forms: add `netlify` attribute to <form> and
 *  set up redirects in your Netlify dashboard.
 * ============================================================
 */

/* ── Helpers ─────────────────────────────────────────────── */
const el  = id  => document.getElementById(id);
const set = (id, html) => { const e = el(id); if (e) e.innerHTML = html; };

function stars(n) {
  return '★'.repeat(n) + '☆'.repeat(5 - n);
}

/* ── Navigation ──────────────────────────────────────────── */
function renderNav() {
  const { nav, business } = SITE;

  set('nav-logo', business.name);
  set('footer-logo', business.name);

  // Desktop links
  el('nav-links').innerHTML = nav.links
    .map(l => `<a href="${l.href}">${l.label}</a>`)
    .join('');
  el('nav-cta').textContent = nav.cta.label;
  el('nav-cta').href        = nav.cta.href;

  // Mobile menu (same links + CTA)
  el('mobile-menu').innerHTML =
    nav.links.map(l => `<a href="${l.href}">${l.label}</a>`).join('') +
    `<a href="${nav.cta.href}" class="btn btn-primary">${nav.cta.label}</a>`;
}

/* ── Hero ────────────────────────────────────────────────── */
function renderHero() {
  const h = SITE.hero;
  set('hero-heading', h.heading);
  set('hero-sub', h.sub);

  set('hero-badges', h.badges
    .map(b => `<span class="badge">${b}</span>`)
    .join(''));

  set('hero-ctas',
    `<a href="${h.cta1.href}" class="btn btn-white">${h.cta1.label}</a>` +
    `<a href="${h.cta2.href}" class="btn btn-outline" style="border-color:rgba(255,255,255,.6);color:#fff">${h.cta2.label}</a>`
  );
}

/* ── Services ────────────────────────────────────────────── */
function renderServices() {
  const s = SITE.services;
  set('services-heading', s.heading);
  set('services-sub', s.sub);

  set('services-grid', s.items.map(item => `
    <article class="service-card">
      <div class="service-card__icon">${item.icon}</div>
      <h3>${item.title}</h3>
      <p>${item.desc}</p>
    </article>
  `).join(''));

  // Footer services list
  set('footer-services', s.items.slice(0, 6).map(item =>
    `<li><a href="#services">${item.title}</a></li>`
  ).join(''));
}

/* ── About ───────────────────────────────────────────────── */
function renderAbout() {
  const a = SITE.about;
  set('about-heading', a.heading);
  set('about-sub', a.sub);
  set('about-body', a.body);

  set('about-points', a.points.map(p => `
    <li class="about-point">
      <span class="about-point__icon">${p.icon}</span>
      <div>
        <h4>${p.title}</h4>
        <p>${p.desc}</p>
      </div>
    </li>
  `).join(''));
}

/* ── How It Works ────────────────────────────────────────── */
function renderHowItWorks() {
  const h = SITE.howItWorks;
  set('hiw-heading', h.heading);
  set('hiw-sub', h.sub);

  set('steps', h.steps.map(s => `
    <div class="step">
      <div class="step__num">${s.num}</div>
      <h3>${s.title}</h3>
      <p>${s.desc}</p>
    </div>
  `).join(''));
}

/* ── Reviews ─────────────────────────────────────────────── */
function renderReviews() {
  const r = SITE.reviews;
  set('reviews-heading', r.heading);
  set('reviews-sub', r.sub);

  set('reviews-grid', r.items.map(item => `
    <article class="review-card">
      <div class="review-card__stars">${stars(item.stars)}</div>
      <p class="review-card__text">"${item.text}"</p>
      <div class="review-card__author">
        <strong>${item.name}</strong>
        <span>${item.role}</span>
      </div>
    </article>
  `).join(''));
}

/* ── FAQ ─────────────────────────────────────────────────── */
function renderFaq() {
  const f = SITE.faq;
  set('faq-heading', f.heading);
  set('faq-sub', f.sub);

  set('faq-list', f.items.map((item, i) => `
    <li class="faq-item" id="faq-${i}">
      <button class="faq-item__q" aria-expanded="false" data-faq="${i}">
        ${item.q}
        <span class="arrow" aria-hidden="true"></span>
      </button>
      <div class="faq-item__a" id="faq-answer-${i}" role="region">
        <p>${item.a}</p>
      </div>
    </li>
  `).join(''));
}

/* ── Contact ─────────────────────────────────────────────── */
function renderContact() {
  const { contact, business } = SITE;

  set('contact-heading', contact.heading);
  set('contact-sub', contact.sub);

  // Details
  el('contact-phone').textContent = business.phone;
  el('contact-phone').href        = `tel:${business.phone.replace(/\s/g, '')}`;
  el('contact-email').textContent = business.email;
  el('contact-email').href        = `mailto:${business.email}`;
  set('contact-hours',    business.hours);
  set('contact-location', business.location);

  // Form fields
  set('form-fields', contact.formFields.map(f => {
    const required = f.required ? 'required' : '';
    const ph       = f.placeholder ? `placeholder="${f.placeholder}"` : '';
    const field    = f.type === 'textarea'
      ? `<textarea id="${f.name}" name="${f.name}" ${required} rows="4"></textarea>`
      : `<input type="${f.type}" id="${f.name}" name="${f.name}" ${required} ${ph} />`;
    return `
      <div class="form-group">
        <label for="${f.name}">${f.label}${f.required ? ' <span style="color:var(--clr-500)">*</span>' : ''}</label>
        ${field}
      </div>`;
  }).join(''));

  set('form-submit', contact.submitLabel);

  // Footer contact
  set('footer-contact', `
    <li><a href="tel:${business.phone.replace(/\s/g, '')}">${business.phone}</a></li>
    <li><a href="mailto:${business.email}">${business.email}</a></li>
    <li>${business.hours}</li>
  `);
}

/* ── Footer ──────────────────────────────────────────────── */
function renderFooter() {
  const { footer, nav } = SITE;

  set('footer-tagline', footer.tagline);
  set('footer-copy',    footer.copy);

  set('footer-nav', nav.links
    .map(l => `<li><a href="${l.href}">${l.label}</a></li>`)
    .join(''));
}

/* ── FAQ Accordion ───────────────────────────────────────── */
function initFaqAccordion() {
  document.querySelectorAll('.faq-item__q').forEach(btn => {
    btn.addEventListener('click', () => {
      const item     = btn.closest('.faq-item');
      const isOpen   = item.classList.contains('open');
      // Close all
      document.querySelectorAll('.faq-item').forEach(i => {
        i.classList.remove('open');
        i.querySelector('.faq-item__q').setAttribute('aria-expanded', 'false');
      });
      // Open clicked (if wasn't open)
      if (!isOpen) {
        item.classList.add('open');
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });
}

/* ── Mobile Hamburger ────────────────────────────────────── */
function initHamburger() {
  const btn   = el('hamburger');
  const menu  = el('mobile-menu');

  btn.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });

  // Close when a link is clicked
  menu.addEventListener('click', e => {
    if (e.target.tagName === 'A') {
      menu.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
    }
  });
}

/* ── Contact Form Submit ─────────────────────────────────── */
function initForm() {
  const form = el('contact-form');

  form.addEventListener('submit', async e => {
    e.preventDefault();

    const btn = el('form-submit');
    btn.textContent = 'Sending…';
    btn.disabled    = true;

    /*
     * TO ENABLE REAL SUBMISSIONS:
     * 1. Go to https://formspree.io and create a free form
     * 2. Replace 'YOUR_FORMSPREE_ID' below with your form ID
     *    e.g. https://formspree.io/f/abcdefgh
     *
     * OR for Netlify: add `netlify` attribute to <form> in index.html
     * and remove this JS handler entirely.
     */
    const FORMSPREE_URL = ''; // e.g. 'https://formspree.io/f/YOUR_ID'

    if (FORMSPREE_URL) {
      try {
        const data = new FormData(form);
        const res  = await fetch(FORMSPREE_URL, {
          method:  'POST',
          body:    data,
          headers: { Accept: 'application/json' },
        });
        if (res.ok) {
          showFormSuccess();
        } else {
          btn.textContent = SITE.contact.submitLabel;
          btn.disabled    = false;
          alert('Something went wrong. Please try emailing us directly.');
        }
      } catch {
        btn.textContent = SITE.contact.submitLabel;
        btn.disabled    = false;
        alert('Could not send message. Please email us directly.');
      }
    } else {
      // Placeholder behaviour until form service is connected
      setTimeout(showFormSuccess, 600);
    }
  });
}

function showFormSuccess() {
  el('contact-form').style.display   = 'none';
  el('form-success').style.display   = 'block';
}

/* ── Sticky nav shadow ───────────────────────────────────── */
function initScrollEffects() {
  const nav = el('nav');
  window.addEventListener('scroll', () => {
    nav.style.boxShadow = window.scrollY > 10
      ? '0 4px 20px rgba(13,148,136,.15)'
      : '';
  }, { passive: true });
}

/* ── Boot ────────────────────────────────────────────────── */
function boot() {
  renderNav();
  renderHero();
  renderServices();
  renderAbout();
  renderHowItWorks();
  renderReviews();
  renderFaq();
  renderContact();
  renderFooter();

  // Interactivity
  initFaqAccordion();
  initHamburger();
  initForm();
  initScrollEffects();
}

document.addEventListener('DOMContentLoaded', boot);
