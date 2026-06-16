const PAGE_SIZE = 20;

export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const status = url.searchParams.get('status') || '';
  const villa  = url.searchParams.get('villa')  || '';
  const search = url.searchParams.get('search') || '';
  const page   = Math.max(1, parseInt(url.searchParams.get('page') || '1', 10));

  let where = 'WHERE 1=1';
  const params = [];

  if (status) { where += ' AND status = ?'; params.push(status); }
  if (villa)  { where += ' AND villa = ?';   params.push(villa); }
  if (search) {
    where += ' AND (name LIKE ? OR email LIKE ? OR phone LIKE ? OR plot LIKE ?)';
    const s = `%${search}%`;
    params.push(s, s, s, s);
  }

  const [countRow, rows] = await Promise.all([
    env.DB.prepare(`SELECT COUNT(*) AS n FROM clients ${where}`)
      .bind(...params).first(),
    env.DB.prepare(
      `SELECT c.*,
        (SELECT COALESCE(SUM(amount), 0) FROM payments WHERE client_id = c.id AND status = 'paid') AS paid_total,
        (SELECT MIN(due_date) FROM payments WHERE client_id = c.id AND status = 'pending') AS next_due
       FROM clients c ${where} ORDER BY created_at DESC LIMIT ? OFFSET ?`
    ).bind(...params, PAGE_SIZE, (page - 1) * PAGE_SIZE).all(),
  ]);

  const total = countRow?.n ?? 0;
  return json({
    ok: true,
    clients: rows.results,
    total,
    page,
    pages: Math.max(1, Math.ceil(total / PAGE_SIZE)),
  });
}

export async function onRequestPost({ request, env }) {
  let data;
  try { data = await request.json(); }
  catch { return json({ ok: false, error: 'bad request' }, 400); }

  const c = v => String(v ?? '').trim().slice(0, 500);
  if (!c(data.name)) return json({ ok: false, error: 'name required' }, 400);

  const price = Number(data.price) || 0;

  const client = await env.DB.prepare(
    `INSERT INTO clients (lead_id, name, phone, email, villa, plot, price, currency, contract_date, agent, status)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING *`
  ).bind(
    data.lead_id || null,
    c(data.name), c(data.phone), c(data.email),
    c(data.villa), c(data.plot),
    price, c(data.currency) || 'USD',
    c(data.contract_date) || null,
    c(data.agent),
    c(data.status) || 'active',
  ).first();

  // Optional: create the payment plan rows in the same request
  if (Array.isArray(data.milestones) && data.milestones.length) {
    const stmts = data.milestones.map((m, i) =>
      env.DB.prepare(
        `INSERT INTO payments (client_id, milestone, amount, currency, due_date, status, sort_order)
         VALUES (?, ?, ?, ?, ?, ?, ?)`
      ).bind(
        client.id,
        c(m.milestone) || `Stage ${i + 1}`,
        Number(m.amount) || 0,
        c(m.currency) || c(data.currency) || 'USD',
        c(m.due_date) || null,
        c(m.status) || 'pending',
        i,
      )
    );
    await env.DB.batch(stmts);
  }

  return json({ ok: true, client });
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
