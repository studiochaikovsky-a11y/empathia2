import { makeToken } from './_token.js';

export function onRequestOptions() {
  return new Response(null, { status: 204 });
}

export async function onRequestPost({ request, env }) {
  let body;
  try { body = await request.json(); }
  catch { return json({ ok: false, error: 'bad request' }, 400); }

  if (!env.CRM_PASSWORD) return json({ ok: false, error: 'not configured' }, 503);
  if (body.password !== env.CRM_PASSWORD) return json({ ok: false, error: 'wrong password' }, 401);

  const token = await makeToken(env.CRM_PASSWORD);
  return json({ ok: true, token });
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
