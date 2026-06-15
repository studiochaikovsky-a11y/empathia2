// Daily HMAC token — rotates every 24 h, invalidates on password change
export async function makeToken(password) {
  const key = await crypto.subtle.importKey(
    'raw', new TextEncoder().encode(password),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']
  );
  const day = Math.floor(Date.now() / 86_400_000);
  const sig = await crypto.subtle.sign(
    'HMAC', key, new TextEncoder().encode(`crm-${day}`)
  );
  return btoa(String.fromCharCode(...new Uint8Array(sig)));
}
