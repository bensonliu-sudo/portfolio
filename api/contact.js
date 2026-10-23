// Contact form configuration: hands the Web3Forms access key to the page.
// Web3Forms' free plan accepts submissions only from the visitor's browser (server-side use needs a paid plan),
// so the browser posts to Web3Forms itself. The key is public by design (it can only deliver to the owner's inbox);
// keeping it in the Vercel environment keeps it out of the repository and lets it be rotated without a code change.
const KEY_NAMES = ['WEB3_FORM', 'WEB3FORMS_ACCESS_KEY', 'WEB3FORMS_KEY', 'ACCESS_KEY'];

module.exports = (req, res) => {
  if (req.method !== 'GET') return res.status(405).json({ success: false, message: 'Method not allowed' });
  const keyName = KEY_NAMES.find((k) => process.env[k]);
  res.setHeader('Cache-Control', 'no-store');
  if (!keyName) return res.status(500).json({ success: false, message: 'Form is not configured' });
  return res.status(200).json({ success: true, key: process.env[keyName] });
};
