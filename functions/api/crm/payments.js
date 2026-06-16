export async function onRequestPost({ request, env }) {
  let data;
  try { data = await request.json(); }
  catch { return json({ ok: false, error: 'bad request' }, 400); }

  const c = v => String(v ?? '').trim().slice(0, 500);
  if (!data.client_id || !c(data.milestone)) {
    return json({ ok: false, error: 'client_id and milestone required' }, 400);
  }

  // place new milestone after the current last one by default
  const last = await env.DB.prepare(
    'SELECT COALESCE(MAX(sort_order), -1) AS n FROM payments WHERE client_id = ?'
  ).bind(data.client_id).first();

  const payment = await env.DB.prepare(
    `INSERT INTO payments (client_id, milestone, amount, currency, due_date, status, sort_order)
     VALUES (?, ?, ?, ?, ?, ?, ?) RETURNING *`
  ).bind(
    data.client_id,
    c(data.milestone),
    Number(data.amount) || 0,
    c(data.currency) || 'USD',
    c(data.due_date) || null,
    c(data.status) || 'pending',
    (last?.n ?? -1) + 1,
  ).first();

  return json({ ok: true, payment });
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
