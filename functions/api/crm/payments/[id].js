export async function onRequestPatch({ params, request, env }) {
  let data;
  try { data = await request.json(); }
  catch { return json({ ok: false, error: 'bad request' }, 400); }

  const allowed = ['milestone', 'amount', 'currency', 'due_date', 'status', 'paid_date', 'sort_order'];
  const sets = [];
  const vals = [];

  // Marking a payment paid auto-stamps paid_date unless one was explicitly given
  if (data.status === 'paid' && !data.paid_date) {
    data.paid_date = new Date().toISOString().slice(0, 10);
  }
  if (data.status && data.status !== 'paid' && data.paid_date === undefined) {
    data.paid_date = null;
  }

  for (const f of allowed) {
    if (data[f] !== undefined) { sets.push(`${f} = ?`); vals.push(data[f]); }
  }
  if (!sets.length) return json({ ok: false, error: 'nothing to update' }, 400);

  vals.push(params.id);
  await env.DB.prepare(`UPDATE payments SET ${sets.join(', ')} WHERE id = ?`).bind(...vals).run();
  const payment = await env.DB.prepare('SELECT * FROM payments WHERE id = ?').bind(params.id).first();
  return json({ ok: true, payment });
}

export async function onRequestDelete({ params, env }) {
  await env.DB.prepare('DELETE FROM payments WHERE id = ?').bind(params.id).run();
  return json({ ok: true });
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
