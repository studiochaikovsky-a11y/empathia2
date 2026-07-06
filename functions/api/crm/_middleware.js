import { makeToken } from './_token.js';

function corsHeaders(request, env) {
  const origin = request.headers.get('Origin') || '';
  const allowed = (env.CRM_ALLOWED_ORIGIN || origin || '*')
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
  const allowOrigin = !origin || allowed.includes('*') || allowed.includes(origin)
    ? (origin || allowed[0] || '*')
    : 'null';

  return {
    'Access-Control-Allow-Origin': allowOrigin,
    'Access-Control-Allow-Methods': 'GET, POST, PATCH, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Vary': 'Origin',
  };
}

export async function onRequest({ request, next, env }) {
  const cors = corsHeaders(request, env);

  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: cors });
  }

  const url = new URL(request.url);

  // Auth endpoint bypasses token check
  if (url.pathname === '/api/crm/auth') {
    return addCors(await next(), cors);
  }

  if (!env.CRM_PASSWORD) {
    return err('CRM not configured — set CRM_PASSWORD env var', 503, cors);
  }

  const bearer = request.headers.get('Authorization') || '';
  const token = bearer.startsWith('Bearer ') ? bearer.slice(7) : '';
  const expected = await makeToken(env.CRM_PASSWORD);

  if (token !== expected) return err('unauthorized', 401, cors);

  return addCors(await next(), cors);
}

function err(msg, status, cors) {
  return new Response(JSON.stringify({ ok: false, error: msg }), {
    status,
    headers: { 'Content-Type': 'application/json', ...cors },
  });
}

function addCors(res, cors) {
  const h = new Headers(res.headers);
  for (const [k, v] of Object.entries(cors)) h.set(k, v);
  return new Response(res.body, { status: res.status, headers: h });
}
