import { makeToken } from './_token.js';

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PATCH, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

export async function onRequest({ request, next, env }) {
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: CORS });
  }

  const url = new URL(request.url);

  // Auth endpoint bypasses token check
  if (url.pathname === '/api/crm/auth') {
    return addCors(await next());
  }

  if (!env.CRM_PASSWORD) {
    return err('CRM not configured — set CRM_PASSWORD env var', 503);
  }

  const bearer = request.headers.get('Authorization') || '';
  const token = bearer.startsWith('Bearer ') ? bearer.slice(7) : '';
  const expected = await makeToken(env.CRM_PASSWORD);

  if (token !== expected) return err('unauthorized', 401);

  return addCors(await next());
}

function err(msg, status) {
  return new Response(JSON.stringify({ ok: false, error: msg }), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS },
  });
}

function addCors(res) {
  const h = new Headers(res.headers);
  for (const [k, v] of Object.entries(CORS)) h.set(k, v);
  return new Response(res.body, { status: res.status, headers: h });
}
