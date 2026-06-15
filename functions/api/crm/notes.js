export async function onRequestPost({ request, env }) {
  let data;
  try { data = await request.json(); }
  catch { return json({ ok: false, error: 'bad request' }, 400); }

  if (!data.lead_id || !String(data.text || '').trim()) {
    return json({ ok: false, error: 'lead_id and text required' }, 400);
  }

  const note = await env.DB.prepare(
    'INSERT INTO notes (lead_id, text) VALUES (?, ?) RETURNING *'
  ).bind(data.lead_id, String(data.text).trim()).first();

  return json({ ok: true, note });
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
