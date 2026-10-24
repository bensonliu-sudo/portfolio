(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // nav background after scrolling
  // the nav takes the theme of whatever band is under it
  const nav = document.getElementById('nav');
  const darkBands = [...document.querySelectorAll('.theme-dark')].filter((el) => el !== nav);
  const onScroll = () => {
    nav.classList.toggle('scrolled', scrollY > 30);
    const y = 37;
    nav.classList.toggle('theme-dark', darkBands.some((el) => { const r = el.getBoundingClientRect(); return r.top <= y && r.bottom > y; }));
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // reveal on scroll + counters (final values are already in the HTML for no-JS readers)
  const fmt = (v, dec, sep) => sep ? Math.round(v).toLocaleString('en-US') : v.toFixed(dec);
  const count = (el) => {
    if (reduce) return;
    const end = parseFloat(el.dataset.count), dec = +(el.dataset.dec || 0), sep = !!el.dataset.sep, pre = el.dataset.prefix || '';
    const t0 = performance.now(), dur = 1600;
    const tick = (t) => { const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 4);
      el.textContent = pre + fmt(end * e, dec, sep); if (p < 1) requestAnimationFrame(tick); };
    requestAnimationFrame(tick);
  };
  const io = new IntersectionObserver((entries) => entries.forEach((en) => {
    if (!en.isIntersecting) return;
    en.target.classList.add('in');
    en.target.querySelectorAll('[data-count]').forEach(count);
    io.unobserve(en.target);
  }), { threshold: 0.18, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.rv').forEach((el) => io.observe(el));

  // walkthrough videos: play only while on screen
  if (!reduce) {
    const vo = new IntersectionObserver((entries) => entries.forEach((e) => { e.isIntersecting ? e.target.play().catch(() => {}) : e.target.pause(); }), { threshold: 0.35 });
    document.querySelectorAll('video[data-auto]').forEach((v) => vo.observe(v));
  }

  // contact form: the browser posts to Web3Forms (its free plan only accepts browser submissions);
  // the access key comes from /api/contact, which reads it from the Vercel environment
  const form = document.getElementById('contact-form');
  if (form) {
    const status = form.querySelector('.form-status'), button = form.querySelector('button');
    const say = (msg, cls) => { status.textContent = msg; status.className = 'form-status' + (cls ? ' ' + cls : ''); };
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!form.checkValidity()) { say('Please fill in your name, a valid email and a message.', 'err'); return; }
      const data = Object.fromEntries(new FormData(form));
      if (data.botcheck) return;
      button.disabled = true; say('Sending…');
      try {
        const cfg = await fetch('/api/contact', { cache: 'no-store' }).then((r) => r.json()).catch(() => ({}));
        if (!cfg.key) { say('The form is not available right now. Please try again later.', 'err'); button.disabled = false; return; }
        const res = await fetch('https://api.web3forms.com/submit', {
          method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ access_key: cfg.key, subject: 'New message from bingchengliu.com', from_name: 'bingchengliu.com',
            name: data.name.slice(0, 100), email: data.email.slice(0, 200), replyto: data.email.slice(0, 200),
            company: (data.company || '-').slice(0, 120), message: data.message.slice(0, 4000), botcheck: '' }),
        });
        const out = await res.json().catch(() => ({}));
        if (res.ok && out.success) { form.reset(); say('Thank you. Your message is on its way, and I will get back to you soon.', 'ok'); }
        else say('Something went wrong. Please try again in a moment.', 'err');
      } catch { say('Could not reach the server. Please check your connection and try again.', 'err'); }
      button.disabled = false;
    });
  }

  // ---------- return to where the reader left the homepage ----------
  try {
    if (location.pathname === '/' || location.pathname === '/index.html') {
      document.querySelectorAll('a[href^="/work/"]').forEach((a) => a.addEventListener('click', () => sessionStorage.setItem('homeY', String(scrollY))));
      if (sessionStorage.getItem('restoreHome')) {
        const y = sessionStorage.getItem('homeY');
        sessionStorage.removeItem('restoreHome');
        if (y !== null) requestAnimationFrame(() => scrollTo({ top: +y, behavior: 'instant' }));   // no saved spot: the #work anchor applies
      }
    }
    document.querySelectorAll('[data-home]').forEach((a) => a.addEventListener('click', (e) => {
      const ref = document.referrer ? new URL(document.referrer) : null;
      if (ref && ref.origin === location.origin && (ref.pathname === '/' || ref.pathname === '/index.html') && history.length > 1) { e.preventDefault(); history.back(); return; }
      sessionStorage.setItem('restoreHome', '1');
    }));
  } catch (_) { /* storage unavailable: plain links still work */ }

  // ---------- motion layer ----------
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  // scroll progress
  const bar = document.createElement('div'); bar.className = 'progress'; document.body.appendChild(bar);
  const prog = () => { const h = document.documentElement.scrollHeight - innerHeight; bar.style.transform = `scaleX(${h > 0 ? scrollY / h : 0})`; };
  addEventListener('scroll', prog, { passive: true }); prog();
  if (!reduce) {
    // headings rise word by word
    document.querySelectorAll('.sec-head h2, .cs-sec h2, .contact h2, .about h2, .next b').forEach((h) => {
      const walk = (node) => [...node.childNodes].forEach((n) => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach((w) => {
            if (!w.trim()) { frag.appendChild(document.createTextNode(w)); return; }
            const s = document.createElement('span'); s.className = 'wd'; s.textContent = w; frag.appendChild(s);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
      });
      walk(h); h.classList.add('split');
      h.querySelectorAll('.wd').forEach((w, i) => { w.style.transitionDelay = (i * 0.06) + 's'; });
      const o = new IntersectionObserver(([e]) => { if (e.isIntersecting) { h.classList.add('in'); o.disconnect(); } }, { threshold: 0.3 });
      o.observe(h);
    });
    // screenshots wipe in
    const wipes = [];
    document.querySelectorAll('.prow .frame, .block .shot, .cs-video .frame').forEach((f) => {
      // observe the container: a fully clipped element never reports as intersecting
      f.classList.remove('rv'); f.classList.add('wipe');
      if (f.closest('.prow')) f.classList.add(['wipe-c', 'wipe-s', 'wipe-d'][[...document.querySelectorAll('.prow')].indexOf(f.closest('.prow')) % 3]);
      wipes.push(f);
    });
    // trigger on the frame's own position (getBoundingClientRect ignores clip-path), so each video animates where the reader can see it
    const wipeCheck = () => {
      for (let i = wipes.length - 1; i >= 0; i--) {
        const r = wipes[i].getBoundingClientRect();
        if (r.top < innerHeight * 0.85 && r.bottom > 0) { wipes[i].classList.add('in'); wipes.splice(i, 1); }
      }
    };
    addEventListener('scroll', wipeCheck, { passive: true }); addEventListener('resize', wipeCheck); wipeCheck();
    // gentle parallax: frames drift against the text column
    const par = [...document.querySelectorAll('.prow .frame, .block .shot')];
    const para = () => par.forEach((el) => { const r = el.getBoundingClientRect(); const c = (r.top + r.height / 2 - innerHeight / 2) / innerHeight;
      el.style.translate = `0 ${(-c * 28).toFixed(1)}px`; });
    addEventListener('scroll', para, { passive: true }); para();
  }
  if (fine && !reduce) {
    // glass sheen follows the pointer; cards tilt toward it
    document.querySelectorAll('.prow, .card, .lesson, .step, .contact-form, .stat').forEach((el) => {
      el.classList.add('sheen');
      el.addEventListener('pointermove', (e) => { const r = el.getBoundingClientRect();
        el.style.setProperty('--sx', (e.clientX - r.left) + 'px'); el.style.setProperty('--sy', (e.clientY - r.top) + 'px'); });
    });
    document.querySelectorAll('.card, .lesson, .step').forEach((el) => {
      el.classList.add('tilt');
      el.addEventListener('pointermove', (e) => { const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = `perspective(900px) rotateX(${(-y * 6).toFixed(2)}deg) rotateY(${(x * 8).toFixed(2)}deg) translateY(-4px)`; });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });
    // magnetic buttons
    document.querySelectorAll('.btn, .more-link').forEach((el) => {
      el.classList.add('magnet');
      el.addEventListener('pointermove', (e) => { const r = el.getBoundingClientRect();
        el.style.transform = `translate(${((e.clientX - r.left - r.width / 2) * 0.25).toFixed(1)}px, ${((e.clientY - r.top - r.height / 2) * 0.35).toFixed(1)}px)`; });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });
  }

  // spotlight following the pointer on approach cards
  document.querySelectorAll('.step').forEach((el) => el.addEventListener('pointermove', (e) => {
    const r = el.getBoundingClientRect(); el.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%');
  }));

  // hero: flowing data lines
  const cv = document.getElementById('flow');
  if (!cv) return;
  const ctx = cv.getContext('2d');
  let W = 0, H = 0, lines = [], mouseY = 0.5, visible = true, t = 0, last = 0;
  const rnd = (a, b) => a + Math.random() * (b - a);
  const build = () => {
    const dpr = Math.min(2, devicePixelRatio || 1);
    W = cv.clientWidth; H = cv.clientHeight; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const n = W < 700 ? 16 : 30;
    lines = Array.from({ length: n }, (_, i) => ({
      y: H * (0.16 + 0.8 * i / (n - 1)), amp: rnd(14, 46), f1: rnd(0.0016, 0.0042), f2: rnd(0.006, 0.013), f3: rnd(0.018, 0.03),
      s1: rnd(0.12, 0.32), s2: rnd(0.25, 0.6), p: rnd(0, 1000), hot: i % 7 === 3, alpha: rnd(0.07, 0.2)
    }));
  };
  const yAt = (L, x, tt) => L.y + L.amp * (Math.sin(x * L.f1 + tt * L.s1 + L.p) * 0.65 + Math.sin(x * L.f2 - tt * L.s2 + L.p * 1.7) * 0.28 + Math.sin(x * L.f3 + tt * 0.9 + L.p) * 0.07) + (mouseY - 0.5) * 30 * (L.y / H);
  const draw = () => {
    ctx.clearRect(0, 0, W, H);
    ctx.strokeStyle = 'rgba(140,180,255,0.045)'; ctx.lineWidth = 1;
    for (let x = 0; x < W; x += 80) { ctx.beginPath(); ctx.moveTo(x + 0.5, 0); ctx.lineTo(x + 0.5, H); ctx.stroke(); }
    for (let y = 0; y < H; y += 80) { ctx.beginPath(); ctx.moveTo(0, y + 0.5); ctx.lineTo(W, y + 0.5); ctx.stroke(); }
    const step = W < 700 ? 10 : 7;
    for (const L of lines) {
      const a = L.hot ? 0.75 : L.alpha, g = ctx.createLinearGradient(0, 0, W, 0);
      g.addColorStop(0, 'rgba(91,140,255,0)'); g.addColorStop(0.45, `rgba(110,160,255,${a * 0.6})`); g.addColorStop(1, `rgba(150,200,255,${a})`);
      ctx.strokeStyle = g; ctx.lineWidth = L.hot ? 1.6 : 1; ctx.beginPath();
      for (let x = 0; x <= W + step; x += step) { const y = yAt(L, x, t); x ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
      ctx.stroke();
      if (L.hot) {
        const x = W * 0.86, y = yAt(L, x, t);
        ctx.fillStyle = 'rgba(160,205,255,0.95)'; ctx.beginPath(); ctx.arc(x, y, 3, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = 'rgba(140,194,255,0.16)'; ctx.beginPath(); ctx.arc(x, y, 10 + 4 * Math.sin(t * 3), 0, Math.PI * 2); ctx.fill();
      }
    }
  };
  const loop = (now) => { if (visible) { t += Math.min(0.05, (now - last) / 1000 || 0.016); draw(); } last = now; requestAnimationFrame(loop); };
  build(); draw();
  addEventListener('resize', () => { build(); draw(); });
  addEventListener('pointermove', (e) => { mouseY += ((e.clientY / innerHeight) - mouseY) * 0.08; }, { passive: true });
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(cv);
  if (!reduce) requestAnimationFrame(loop);
})();
