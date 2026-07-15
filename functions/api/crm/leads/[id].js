export async function onRequestGet({ params, env }) {
  const [lead, notes] = await Promise.all([
    env.DB.prepare('SELECT * FROM leads WHERE id = ?').bind(params.id).first(),
    env.DB.prepare('SELECT * FROM notes WHERE lead_id = ? ORDER BY created_at DESC')
      .bind(params.id).all(),
  ]);
  if (!lead) return json({ ok: false, error: 'not found' }, 404);
  return json({ ok: true, lead, notes: notes.results });
}

export async function onRequestPatch({ params, request, env }) {
  await ensureLeadCountryColumn(env);
  let data;
  try { data = await request.json(); }
  catch { return json({ ok: false, error: 'bad request' }, 400); }

  const allowed = ['status', 'name', 'phone', 'email', 'interest', 'type', 'source', 'created_at', 'country'];
  const sets = [];
  const vals = [];

  for (const f of allowed) {
    if (data[f] !== undefined) { sets.push(`${f} = ?`); vals.push(data[f]); }
  }
  if (!sets.length) return json({ ok: false, error: 'nothing to update' }, 400);

  vals.push(params.id);
  await env.DB.prepare(`UPDATE leads SET ${sets.join(', ')} WHERE id = ?`).bind(...vals).run();
  const lead = await env.DB.prepare('SELECT * FROM leads WHERE id = ?').bind(params.id).first();
  return json({ ok: true, lead });
}

export async function onRequestDelete({ params, env }) {
  await env.DB.prepare('DELETE FROM leads WHERE id = ?').bind(params.id).run();
  return json({ ok: true });
}

async function ensureLeadCountryColumn(env) {
  try { await env.DB.prepare('ALTER TABLE leads ADD COLUMN country TEXT').run(); }
  catch (err) { if (!String(err?.message || err).includes('duplicate column')) throw err; }
}
function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
