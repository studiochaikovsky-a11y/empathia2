export async function onRequestPost({ request, env }) {
  let data;
  try { data = await request.json(); }
  catch { return json({ ok: false, error: 'bad request' }, 400); }

  if (!data.client_id || !String(data.text || '').trim()) {
    return json({ ok: false, error: 'client_id and text required' }, 400);
  }

  const note = await env.DB.prepare(
    'INSERT INTO client_notes (client_id, text) VALUES (?, ?) RETURNING *'
  ).bind(data.client_id, String(data.text).trim()).first();

  return json({ ok: true, note });
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
