const PAGE_SIZE = 20;

export async function onRequestGet({ request, env }) {
  await ensureLeadCountryColumn(env);
  const url = new URL(request.url);
  const status = url.searchParams.get('status') || '';
  const source = url.searchParams.get('source') || '';
  const search = url.searchParams.get('search') || '';
  const page   = Math.max(1, parseInt(url.searchParams.get('page') || '1', 10));

  let where = 'WHERE 1=1';
  const params = [];

  if (status) { where += ' AND status = ?'; params.push(status); }
  if (source) { where += ' AND source = ?'; params.push(source); }
  if (search) {
    where += ' AND (name LIKE ? OR email LIKE ? OR phone LIKE ? OR country LIKE ?)';
    const s = `%${search}%`;
    params.push(s, s, s, s);
  }

  const [countRow, rows] = await Promise.all([
    env.DB.prepare(`SELECT COUNT(*) AS n FROM leads ${where}`)
      .bind(...params).first(),
    env.DB.prepare(
      `SELECT * FROM leads ${where} ORDER BY created_at DESC LIMIT ? OFFSET ?`
    ).bind(...params, PAGE_SIZE, (page - 1) * PAGE_SIZE).all(),
  ]);

  const total = countRow?.n ?? 0;
  return json({
    ok: true,
    leads: rows.results,
    total,
    page,
    pages: Math.max(1, Math.ceil(total / PAGE_SIZE)),
  });
}

export async function onRequestPost({ request, env }) {
  await ensureLeadCountryColumn(env);
  let data;
  try { data = await request.json(); }
  catch { return json({ ok: false, error: 'bad request' }, 400); }

  const c = v => String(v || '').trim().slice(0, 500);
  if (!c(data.name) && !c(data.phone) && !c(data.email)) {
    return json({ ok: false, error: 'name, phone or email required' }, 400);
  }

  const interest = c(data.interest);
  const type = interest.toLowerCase().includes('агент') || c(data.page).includes('agent')
    ? 'agent' : 'client';

  const lead = await env.DB.prepare(
    `INSERT INTO leads (source, country, name, phone, email, interest, message, page, type)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING *`
  ).bind(
    c(data.source) || 'manual',
    c(data.country),
    c(data.name), c(data.phone), c(data.email),
    interest, c(data.message),
    c(data.page) || 'manual',
    type,
  ).first();

  return json({ ok: true, lead });
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
