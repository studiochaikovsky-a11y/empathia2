const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

export async function onRequestPost({ request, env }) {
  if (!env.DB) return json({ ok: true, stored: false });

  let data;
  try {
    data = await request.json();
  } catch {
    return json({ ok: false, error: 'bad_request' }, 400);
  }

  const clean = (value, limit = 300) => String(value || '').slice(0, limit).trim();
  const event = clean(data.event, 80);
  if (!/^[a-z0-9_:-]{2,80}$/i.test(event)) return json({ ok: false, error: 'bad_event' }, 400);

  await env.DB.prepare(
    `CREATE TABLE IF NOT EXISTS analytics_events (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      event TEXT NOT NULL,
      page TEXT DEFAULT '',
      page_title TEXT DEFAULT '',
      label TEXT DEFAULT '',
      href TEXT DEFAULT '',
      interest TEXT DEFAULT '',
      utm_source TEXT DEFAULT '',
      utm_medium TEXT DEFAULT '',
      utm_campaign TEXT DEFAULT '',
      created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )`
  ).run();

  await env.DB.prepare(
    `INSERT INTO analytics_events
      (event, page, page_title, label, href, interest, utm_source, utm_medium, utm_campaign)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`
  ).bind(
    event,
    clean(data.page),
    clean(data.page_title),
    clean(data.label),
    clean(data.href),
    clean(data.interest),
    clean(data.utm_source),
    clean(data.utm_medium),
    clean(data.utm_campaign)
  ).run();

  return json({ ok: true, stored: true });
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS },
  });
}
