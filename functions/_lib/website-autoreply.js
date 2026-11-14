const salesEmail = 'sales@empathia-seychelles.com';
const contactPaths = new Set(['/contact', '/contact/', '/contact.html']);
const contactPages = new Set(['Contact', 'RU Контакты']);
const testName = 'TEST Empathia Apps Script';
const validEmail = /^[a-z0-9_+%-]+(?:\.[a-z0-9_+%-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}$/i;

export function websiteReplyMode(request, lead, site, env) {
  const origin = request.headers.get('Origin');
  if (origin !== site.url.slice(0, -1) && origin !== 'https://www.' + site.domain) return null;
  if (lead.name === testName && lead.email.toLowerCase() === salesEmail) return 'test';
  if (!env.WEBSITE_REPLY_URL || !env.WEBSITE_REPLY_KEY) return null;
  if (env.WEBSITE_REPLY_MODE !== 'live' || lead.email.length > 254 || !validEmail.test(lead.email) ||
      lead.interest.toLowerCase().includes('agent') || lead.page.toLowerCase().includes('agent')) return null;
  // The two main contact forms share this handler. Keep other call sites out of the mailing workflow.
  if (!contactPages.has(lead.page)) {
    const referer = request.headers.get('Referer');
    if (!referer || !contactPaths.has(URL.parse(referer)?.pathname)) return null;
  }
  return 'live';
}

export async function deliverWebsiteReply({lead, site, reference, mode, env}) {
  const endpoint = String(env.WEBSITE_REPLY_URL).trim();
  if (!/^https:\/\/script\.google\.com\/(?:a\/macros\/[a-z0-9.-]+\/|macros\/)s\/[a-z0-9_-]+\/exec$/i.test(endpoint)) {
    return {ok: false, httpStatus: null, code: 'invalid_endpoint'};
  }
  const encoder = new TextEncoder();
  const timestamp = Date.now();
  const test = mode === 'test';
  const payload = JSON.stringify({site: site.domain, reference, email: test ? salesEmail : lead.email, test});
  const key = await crypto.subtle.importKey(
    'raw', encoder.encode(env.WEBSITE_REPLY_KEY.trim()), {name: 'HMAC', hash: 'SHA-256'}, false, ['sign'],
  );
  const digest = await crypto.subtle.sign('HMAC', key, encoder.encode(timestamp + '.' + payload));
  const signature = Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, '0')).join('');
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({timestamp, payload, signature}),
    signal: AbortSignal.timeout(20000),
  });
  const code = (await response.json().catch(() => null))?.code;
  const accepted = response.ok && code === 'sent';
  const known = ['sent', 'duplicate', 'invalid', 'disabled', 'limit', 'busy', 'uncertain'];
  return {ok: accepted, httpStatus: response.status, code: known.includes(code) ? code : 'provider_error'};
}
