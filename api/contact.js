// Contact form endpoint: validates the message and forwards it to Web3Forms, which emails the site owner.
// The Web3Forms access key lives only in the Vercel environment, never in the page.
const KEY_NAMES = ['WEB3FORMS_ACCESS_KEY', 'WEB3FORMS_KEY', 'WEB3FORM_ACCESS_KEY', 'WEB3FORM_KEY', 'WEB3_FORMS_KEY', 'ACCESS_KEY', 'FORM_ACCESS_KEY'];
const ALLOWED_ORIGIN = /^https:\/\/(bingchengliu\.com|www\.bingchengliu\.com|portfolio[a-z0-9-]*\.vercel\.app)$/;

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ success: false, message: 'Method not allowed' });
  const origin = req.headers.origin || '';
  if (origin && !ALLOWED_ORIGIN.test(origin)) return res.status(403).json({ success: false, message: 'Forbidden' });

  const keyName = KEY_NAMES.find((k) => process.env[k]);
  if (!keyName) return res.status(500).json({ success: false, message: 'Form is not configured' });

  const b = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  if (b.botcheck) return res.status(200).json({ success: true });   // honeypot: pretend success, send nothing
  const name = String(b.name || '').trim().slice(0, 100);
  const email = String(b.email || '').trim().slice(0, 200);
  const company = String(b.company || '').trim().slice(0, 120);
  const message = String(b.message || '').trim().slice(0, 4000);
  if (!name || !message || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ success: false, message: 'Please fill in your name, a valid email and a message.' });
  }

  try {
    const r = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ access_key: process.env[keyName], subject: 'New message from bingchengliu.com', from_name: 'bingchengliu.com',
        name, email, replyto: email, company: company || '-', message }),
    });
    const out = await r.json().catch(() => ({}));
    if (r.ok && out.success) return res.status(200).json({ success: true });
    return res.status(502).json({ success: false, message: 'Delivery failed', upstream: out.message || r.status });
  } catch (e) {
    return res.status(502).json({ success: false, message: 'Delivery failed' });
  }
};
