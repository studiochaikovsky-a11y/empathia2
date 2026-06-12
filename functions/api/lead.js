// Cloudflare Pages Function: receives form submissions from the site
// and forwards them to Telegram and email (Web3Forms).
// Secrets are configured in Cloudflare Pages → Settings → Environment variables:
//   TELEGRAM_BOT_TOKEN  — token from @BotFather
//   TELEGRAM_CHAT_ID    — chat id that should receive the lead
//   WEB3FORMS_KEY       — access key from web3forms.com (sends email)

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
  };

  if (!lead.name && !lead.phone && !lead.email) {
    return json({ ok: false, error: 'empty' }, 400);
  }

  const lines = [
    '🌴 Новая заявка с сайта Empathia Village',
    '',
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
      fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: env.TELEGRAM_CHAT_ID, text }),
      }).then((r) => r.ok)
    );
  }

  if (env.WEB3FORMS_KEY) {
    tasks.push(
      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          access_key: env.WEB3FORMS_KEY,
          subject: 'Новая заявка — Empathia Village',
          from_name: 'Empathia Village Website',
          name: lead.name,
          phone: lead.phone,
          email: lead.email || undefined,
          interest: lead.interest,
          message: text,
        }),
      }).then((r) => r.ok)
    );
  }

  if (tasks.length === 0) {
    // Channels not configured yet — accept the lead so the visitor
    // still sees a success message, but report it in the response.
    return json({ ok: false, error: 'not configured' }, 503);
  }

  const results = await Promise.allSettled(tasks);
  const delivered = results.some((r) => r.status === 'fulfilled' && r.value === true);

  return json({ ok: delivered }, delivered ? 200 : 502);
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
