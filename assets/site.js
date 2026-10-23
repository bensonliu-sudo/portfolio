(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // nav background after scrolling
  const nav = document.getElementById('nav');
  const onScroll = () => nav.classList.toggle('scrolled', scrollY > 30);
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
