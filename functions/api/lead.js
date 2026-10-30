// Cloudflare Pages Function: receives form submissions from the site
// and forwards them to Telegram and email (Web3Forms).
// Secrets are configured in Cloudflare Pages → Settings → Environment variables:
//   TELEGRAM_BOT_TOKEN  — token from @BotFather
//   TELEGRAM_CHAT_ID    — chat id that should receive the lead
//   WEB3FORMS_KEY       — access key from web3forms.com (sends email)

// Preflight for cross-origin form posts from approved campaign or language pages.
export function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export async function onRequestPost({ request, env }) {
  let data;
  try {
    data = await request.json();
  } catch {
    return json({ ok: false, error: 'bad request' }, 400);
  }

  const clean = (v) => String(v || '').slice(0, 500).trim();
  const lead = {
    name: clean(data.name),
    phone: clean(data.phone),
    email: clean(data.email),
    interest: clean(data.interest),
    message: clean(data.message),
    page: clean(data.page),
    utm_source: clean(data.utm_source),
    utm_medium: clean(data.utm_medium),
    utm_campaign: clean(data.utm_campaign),
  };

  const phoneDigits = lead.phone.replace(/\D/g, '');
  if (phoneDigits.length < 7) {
    return json({ ok: false, error: 'phone_required' }, 400);
  }

  const status = { telegram: 'not configured', email: 'not configured', crm: 'not configured' };
  let leadReference='';
  // Save first so all delivery channels carry the same durable receipt number.
  let dbPromise = Promise.resolve();
  if (env.DB) {
    const src = clean(data.source) || 'empathia-seychelles.com';
    const interest = lead.interest;
    const type = interest.toLowerCase().includes('agent') || lead.page.includes('agent')
      ? 'agent' : 'client';
    dbPromise = Promise.resolve().then(() => env.DB.prepare(
      `INSERT INTO leads (source, name, phone, email, interest, message, page, type, utm_source, utm_medium, utm_campaign)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    ).bind(src, lead.name, lead.phone, lead.email, interest, lead.message, lead.page, type,
        lead.utm_source, lead.utm_medium, lead.utm_campaign)
      .run()).then((result) => { status.crm = 'ok'; const id=Number(result?.meta?.last_row_id); if(Number.isSafeInteger(id)&&id>0) leadReference=`site:empathia-en:${id}`; })
      .catch(e => { console.error('CRM D1 insert failed:', e); status.crm = 'failed'; });
  }

  await dbPromise;

  const lines = [
    '🌴 Новая заявка с сайта Empathia Village',
    '',
    leadReference && `UACC-REF: ${leadReference}`,
    lead.name && `Имя: ${lead.name}`,
    lead.phone && `Телефон: ${lead.phone}`,
    lead.email && `Email: ${lead.email}`,
    lead.interest && `Интерес: ${lead.interest}`,
    lead.message && `Сообщение: ${lead.message}`,
    '',
    lead.page && `Страница: ${lead.page}`,
  ].filter(Boolean);
  const text = lines.join('\n');

  const tasks = [];

  if (env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) {
    tasks.push(
      fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN.trim()}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: env.TELEGRAM_CHAT_ID.trim(), text }),
      })
        .then(async (r) => {
          const body = await r.json().catch(() => ({}));
          const ok = r.ok && body.ok !== false;
          status.telegram = ok ? 'ok' : 'failed';
          return ok;
        })
        .catch((e) => { console.error('Lead Telegram delivery failed:', e); status.telegram = 'failed'; return false; })
    );
  }

  if (env.WEB3FORMS_KEY) {
    tasks.push(
      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          access_key: env.WEB3FORMS_KEY.trim(),
          subject: 'Новая заявка — Empathia Village',
          from_name: 'Empathia Village Website',
          name: lead.name || 'Website visitor',
          phone: lead.phone,
          ...(lead.email ? { email: lead.email } : {}),
          message: text,
        }),
      })
        .then(async (r) => {
          const body = await r.json().catch(() => ({}));
          const ok = r.ok && body.success !== false;
          status.email = ok ? 'ok' : 'failed';
          return ok;
        })
        .catch((e) => { console.error('Lead email delivery failed:', e); status.email = 'failed'; return false; })
    );
  }


  if (tasks.length === 0) {
    await dbPromise;
    return json({ ok: false, error: 'not configured' }, 503);
  }

  const [results] = await Promise.all([Promise.allSettled(tasks), dbPromise]);
  const delivered = results.some((r) => r.status === 'fulfilled' && r.value === true);

  if (Object.values(status).some(value => value !== 'ok')) {
    const warning = [
      '⚠️ Empathia: заявка доставлена не во все каналы',
      `Telegram: ${status.telegram}; email: ${status.email}; CRM: ${status.crm}`,
      `Страница: ${lead.page || 'не указана'}; телефон оканчивается на ${lead.phone.slice(-4)}`,
      'Проверьте заявку в доступном канале и восстановите сбойный.'
    ].join('\n');
    try {
      if (status.telegram === 'ok') {
        const response = await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN.trim()}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ chat_id: env.TELEGRAM_CHAT_ID.trim(), text: warning }),
        });
        if (!response.ok || (await response.json().catch(() => ({}))).ok === false) {
          throw new Error('Telegram warning delivery failed');
        }
      } else if (status.email === 'ok') {
        const response = await fetch('https://api.web3forms.com/submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            access_key: env.WEB3FORMS_KEY.trim(),
            subject: 'Проверьте доставку заявки — Empathia Village',
            from_name: 'Empathia Village Website',
            message: warning,
          }),
        });
        if (!response.ok || (await response.json().catch(() => ({}))).success === false) {
          throw new Error('Email warning delivery failed');
        }
      } else {
        console.error('Lead delivery failed with no working warning channel:', status);
      }
    } catch (error) {
      console.error('Lead warning delivery failed:', error);
    }
  }

  // Always 200 so Cloudflare doesn't replace the JSON body with its
  // generic 5xx error page; the client checks the `ok` field.
  return json({ ok: delivered, status });
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS },
  });
}
