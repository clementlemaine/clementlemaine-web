(() => {
  const doc = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // --- rechargement : on repart toujours du haut de la page d'accueil
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  if (performance.getEntriesByType('navigation')[0]?.type === 'reload') {
    if (location.hash) history.replaceState(null, '', location.pathname + location.search);
    scrollTo({ top: 0, behavior: 'instant' });
    addEventListener('load', () => scrollTo({ top: 0, behavior: 'instant' }), { once: true });
  }

  requestAnimationFrame(() => setTimeout(() => {
    doc.classList.add('ready');
    $('.nav-wrap').classList.add('show');
  }, 80));

  // --- thème clair / sombre (aria-pressed : le bouton annonce s'il est en mode sombre)
  const themeBtn = $('.theme');
  const syncTheme = () => themeBtn.setAttribute('aria-pressed', String(doc.dataset.theme === 'dark'));
  syncTheme();
  themeBtn.addEventListener('click', () => {
    const dark = doc.dataset.theme !== 'dark';
    doc.dataset.theme = dark ? 'dark' : 'light';
    try { localStorage.setItem('cl-theme', doc.dataset.theme); } catch (_) {}
    syncTheme();
  });

  // --- email assemblé côté client
  $$('.mail').forEach(m => { const a = m.dataset.u + '@' + m.dataset.d; m.textContent = a; m.href = 'mailto:' + a; });

  // les pages légales s'arrêtent ici : pas de CV, de trajet ni d'animations
  if (!$('.cv-modal')) return;

  // --- aperçu du CV
  const modal = $('.cv-modal');
  $$('[data-open-cv]').forEach(b => b.addEventListener('click', () => modal.showModal()));
  $('[data-close]', modal).addEventListener('click', () => modal.close());
  modal.addEventListener('click', e => { if (e.target === modal) modal.close(); });
  // langue du CV : change l'aperçu et le PDF téléchargé
  const cvTabs = $$('[data-cv-lang]', modal);
  cvTabs.forEach(b => b.addEventListener('click', () => {
    cvTabs.forEach(x => x.toggleAttribute('aria-current', x === b));
    $('.cv-img', modal).src = `../cv/preview-${b.dataset.cvLang}.png`;
    $('.cv-pdf', modal).href = b.dataset.pdf;
  }));

  // --- aperçu mobile : le site dans un cadre de téléphone
  if (window.self !== window.top) doc.classList.add('in-frame');
  const phoneModal = $('.phone-modal');
  if (phoneModal) {
    const frame = $('iframe', phoneModal);
    const fit = () => phoneModal.style.setProperty('--s', Math.min(1, (innerHeight - 48) / 868, (innerWidth - 32) / 414));
    $('[data-phone]').addEventListener('click', () => {
      if (!frame.getAttribute('src')) frame.src = location.pathname;
      fit(); phoneModal.showModal();
    });
    $('[data-phone-close]', phoneModal).addEventListener('click', () => phoneModal.close());
    phoneModal.addEventListener('click', e => { if (e.target === phoneModal) phoneModal.close(); });
    addEventListener('resize', fit);
  }

  // --- QR code plein écran (aussi via l'adresse …/#qr)
  const qrModal = $('.qr-modal');
  $$('[data-open-qr]').forEach(b => b.addEventListener('click', () => qrModal.showModal()));
  $('[data-close]', qrModal).addEventListener('click', () => qrModal.close());
  qrModal.addEventListener('click', e => { if (e.target === qrModal) qrModal.close(); });
  if (location.hash === '#qr') qrModal.showModal();

  // --- apparitions
  const io = new IntersectionObserver(es => es.forEach(en => {
    if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
  }), { threshold: .2 });
  $$('[data-reveal]').forEach(el => io.observe(el));

  // --- reflet qui suit la souris sur les cartes
  if (matchMedia('(pointer: fine)').matches) {
    $$('.spot').forEach(el => el.addEventListener('mousemove', e => {
      const r = el.getBoundingClientRect();
      el.style.setProperty('--mx', `${e.clientX - r.left}px`);
      el.style.setProperty('--my', `${e.clientY - r.top}px`);
    }));
  }

  // --- cartes de langues : la première passe derrière, en boucle
  const cards = $$('.flyer');
  if (cards.length && !reduce) {
    let order = cards.slice();
    setInterval(() => {
      if (document.hidden) return;
      const top = order.shift();
      order.push(top);
      top.classList.add('deal');
      top.addEventListener('animationend', () => top.classList.remove('deal'), { once: true });
      order.forEach((c, i) => { c.classList.remove('p0', 'p1', 'p2'); c.classList.add('p' + i); });
    }, 2600);
  }

  // --- projets : l'invite s'écrit, s'envoie, puis passe à la suivante
  const prompt = $('.prompt');
  if (prompt && !reduce) {
    const texts = JSON.parse(prompt.dataset.prompts);
    const out = $('.prompt-t', prompt);
    const wait = ms => new Promise(r => setTimeout(r, ms));
    const run = async () => {
      for (let k = 0; ; k = (k + 1) % texts.length) {
        prompt.classList.remove('sent');
        for (let n = 0; n <= texts[k].length; n++) { out.textContent = texts[k].slice(0, n); await wait(32); }
        await wait(500); prompt.classList.add('sent');
        await wait(1500); out.textContent = '';
        await wait(350);
      }
    };
    out.textContent = '';
    new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { o.disconnect(); run(); } }, { threshold: .4 }).observe(prompt);
  }

  // --- refonte : la barre balaie toute seule l'avant et l'après ; on la prend en main en maintenant le clic
  const ba = $('.ba');
  if (ba) {
    const view = $('.ba-view', ba), imgs = $$('.ba-img', ba);
    let split = 100, target = 0, hold = 1200, scroll = 0, dir = 1, held = false, seen = false, last = 0;
    const paint = () => {
      ba.style.setProperty('--split', split + '%');
      ba.classList.toggle('is-new', split < 50);
      imgs.forEach(im => { im.style.transform = `translateY(${-scroll * Math.max(0, im.offsetHeight - view.clientHeight)}px)`; });
    };
    const tick = now => {
      const dt = Math.min(64, now - (last || now)); last = now;
      if (seen && !held && !document.hidden) {
        if (hold > 0) hold -= dt;
        else {
          const step = dt * .032;                                          // ~3 s pour traverser
          split += clamp(target - split, -step, step);
          if (split === target) { target = target ? 0 : 100; hold = 1400; }
        }
        scroll = clamp(scroll + dir * dt / 40000);                         // les pages défilent doucement
        if (scroll === 0 || scroll === 1) dir = -dir;
        paint();
      }
      requestAnimationFrame(tick);
    };
    const follow = e => { const r = view.getBoundingClientRect(); split = clamp((e.clientX - r.left) / r.width) * 100; paint(); };
    view.addEventListener('pointerdown', e => { held = true; view.setPointerCapture(e.pointerId); ba.classList.add('is-held'); follow(e); });
    view.addEventListener('pointermove', e => { if (held) follow(e); });
    const release = () => { if (!held) return; held = false; ba.classList.remove('is-held'); target = split < 50 ? 100 : 0; hold = 1800; };
    view.addEventListener('pointerup', release);
    view.addEventListener('pointercancel', release);
    imgs.forEach(im => im.addEventListener('load', paint));
    if (reduce) { split = 50; paint(); }
    else {
      new IntersectionObserver(es => { seen = es[0].isIntersecting; }, { threshold: .25 }).observe(ba);
      requestAnimationFrame(tick);
    }
  }

  // --- scroll : trajet, nav active
  const routeSec = $('.route-sec');
  const line = $('.route-line', routeSec);
  const plane = $('.plane', routeSec);
  const stops = $$('.stop', routeSec);
  const legs = $$('.leg', routeSec);
  const L = line.getTotalLength();
  line.style.strokeDasharray = L;
  // distance parcourue sur le tracé jusqu'à chaque escale (data-d = tracé jusqu'à elle)
  const svg = line.ownerSVGElement;
  const at = stops.map(g => {
    if (!g.dataset.d) return 0;
    const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    p.setAttribute('d', g.dataset.d);
    svg.appendChild(p);
    const len = p.getTotalLength();
    p.remove();
    return len;
  });
  const navLinks = $$('.nav-links a');
  const secs = navLinks.map(a => $(a.getAttribute('href')));
  let lastLeg = -1;
  const cue = $('.route-cue'), cueN = $('.route-cue-n'), cueDots = $$('.route-cue-dots i');
  // l'indicateur emmène à l'escale suivante (la position de scroll qui la fait apparaître)
  cue.addEventListener('click', () => {
    const next = Math.min(lastLeg + 1, stops.length - 1);
    const p = clamp((at[next] + 4) / L * .92);
    const top = routeSec.getBoundingClientRect().top + scrollY + p * (routeSec.offsetHeight - innerHeight);
    scrollTo({ top, behavior: reduce ? 'auto' : 'smooth' });
  });

  const progress = el => {
    const r = el.getBoundingClientRect();
    return clamp(-r.top / Math.max(1, el.offsetHeight - innerHeight));
  };

  const onScroll = () => {
    const d = reduce ? L : clamp(progress(routeSec) / .92) * L;
    line.style.strokeDashoffset = L - d;
    const p1 = line.getPointAtLength(Math.max(0, d)), p2 = line.getPointAtLength(Math.min(L, d + 1));
    const ang = Math.atan2(p2.y - p1.y, p2.x - p1.x) * 180 / Math.PI;
    plane.setAttribute('transform', `translate(${p1.x} ${p1.y}) rotate(${ang})`);
    plane.classList.toggle('done', d >= L - 1);
    let leg = 0;
    at.forEach((len, i) => { if (d >= len - 2) leg = i; });
    stops.forEach((g, i) => { g.classList.toggle('on', d >= at[i] - 2); g.classList.toggle('cur', i === leg); });
    if (leg !== lastLeg) {
      lastLeg = leg;
      legs.forEach((el, i) => el.classList.toggle('is-on', i === leg));
      cueN.textContent = cue.dataset.n.replace('{n}', leg + 1).replace('{total}', stops.length);
      cueDots.forEach((el, i) => { el.classList.toggle('on', i <= leg); el.classList.toggle('cur', i === leg); });
    }
    const rr = routeSec.getBoundingClientRect();
    const cueOn = rr.top < innerHeight * .6 && rr.bottom > innerHeight * 1.05 && leg < stops.length - 1;
    cue.classList.toggle('on', cueOn);
    doc.classList.toggle('cue-on', cueOn);

    doc.classList.toggle('past-hero', scrollY > innerHeight * .6);

    let cur = -1;
    secs.forEach((sec, i) => { if (sec && sec.getBoundingClientRect().top < innerHeight * .4) cur = i; });
    navLinks.forEach((a, i) => a.classList.toggle('on', i === cur));
  };
  let raf = 0;
  addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(() => { raf = 0; onScroll(); }); }, { passive: true });
  addEventListener('resize', onScroll);
  onScroll();
})();
