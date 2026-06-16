export async function onRequestGet({ params, env }) {
  const [client, payments, notes] = await Promise.all([
    env.DB.prepare('SELECT * FROM clients WHERE id = ?').bind(params.id).first(),
    env.DB.prepare('SELECT * FROM payments WHERE client_id = ? ORDER BY sort_order ASC, id ASC')
      .bind(params.id).all(),
    env.DB.prepare('SELECT * FROM client_notes WHERE client_id = ? ORDER BY created_at DESC')
      .bind(params.id).all(),
  ]);
  if (!client) return json({ ok: false, error: 'not found' }, 404);
  return json({ ok: true, client, payments: payments.results, notes: notes.results });
}

export async function onRequestPatch({ params, request, env }) {
  let data;
  try { data = await request.json(); }
  catch { return json({ ok: false, error: 'bad request' }, 400); }

  const allowed = ['name', 'phone', 'email', 'villa', 'plot', 'price', 'currency', 'contract_date', 'agent', 'status'];
  const sets = [];
  const vals = [];

  for (const f of allowed) {
    if (data[f] !== undefined) { sets.push(`${f} = ?`); vals.push(data[f]); }
  }
  if (!sets.length) return json({ ok: false, error: 'nothing to update' }, 400);

  vals.push(params.id);
  await env.DB.prepare(`UPDATE clients SET ${sets.join(', ')} WHERE id = ?`).bind(...vals).run();
  const client = await env.DB.prepare('SELECT * FROM clients WHERE id = ?').bind(params.id).first();
  return json({ ok: true, client });
}

export async function onRequestDelete({ params, env }) {
  await env.DB.prepare('DELETE FROM clients WHERE id = ?').bind(params.id).run();
  return json({ ok: true });
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
