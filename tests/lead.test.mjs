import test from 'node:test';
import assert from 'node:assert/strict';
import { onRequestPost } from '../functions/api/lead.js';

test('each website can send one isolated test to the sales mailbox only', async (t) => {
  const calls = [];
  t.mock.method(globalThis, 'fetch', async (_url, options) => {
    const envelope = JSON.parse(options.body);
    assert.match(envelope.signature, /^[0-9a-f]{64}$/);
    calls.push(JSON.parse(envelope.payload));
    return Response.json({code: 'sent'});
  });
  const env = {
    WEBSITE_REPLY_URL: 'https://script.google.com/macros/s/example/exec',
    WEBSITE_REPLY_KEY: 'fixture-key',
    DB: {prepare() { assert.fail('test must bypass the CRM'); }},
    TELEGRAM_BOT_TOKEN: 'fixture-token',
    TELEGRAM_CHAT_ID: 'fixture-chat',
  };

  for (const [domain, locale] of [['empathiavillage.ru', 'ru'], ['empathia-seychelles.com', 'en']]) {
    const response = await onRequestPost({
      request: new Request('https://empathia-seychelles.com/api/lead', {
        method: 'POST',
        headers: {Origin: 'https://' + domain},
        body: JSON.stringify({name: 'TEST Empathia Apps Script', phone: '0000000000', email: 'sales@empathia-seychelles.com'}),
      }),
      env,
    });
    const result = await response.json();
    assert.equal(result.ok, false);
    assert.equal(result.test, true);
    assert.equal(result.autoreply, 'sent');
    assert.match(result.lead_reference, new RegExp('^site:empathia-' + locale + ':[0-9]+$'));
  }
  assert.deepEqual(calls.map(({site, email, test}) => ({site, email, test})), [
    {site: 'empathiavillage.ru', email: 'sales@empathia-seychelles.com', test: true},
    {site: 'empathia-seychelles.com', email: 'sales@empathia-seychelles.com', test: true},
  ]);
});

async function submit({ telegramOk = true, emailOk = true, crmOk = true, source, origin, attribution } = {}) {
  const calls = [];let savedAttribution=null;
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, options) => {
    const body = JSON.parse(options.body);
    const channel = String(url).includes('telegram.org') ? 'telegram' : 'email';
    calls.push({ channel, body });
    if (channel === 'telegram') {
      return Response.json({ ok: telegramOk }, { status: telegramOk ? 200 : 500 });
    }
    return Response.json({ success: emailOk }, { status: emailOk ? 200 : 500 });
  };
  const env = {
    TELEGRAM_BOT_TOKEN: 'test-token',
    TELEGRAM_CHAT_ID: 'test-chat',
    WEB3FORMS_KEY: 'test-key',
    DB: {
      batch: async () => [],
      prepare(sql) {
        return {
          bind(...values) {
            if(sql.includes("INSERT INTO leads"))savedAttribution=JSON.parse(values.at(-1));
            return {
              run: async () => {
                if (!crmOk) throw new Error('test database outage');
                return {meta:{last_row_id:123}};
              },
            };
          },
        };
      },
    },
  };
  try {
    const response = await onRequestPost({
      request: new Request('https://example.test/api/lead', {
        method: 'POST',
        headers: origin ? {Origin:origin} : {},
        body: JSON.stringify({ attribution, source, phone: '+248 271 51 02', page: 'Contact' }),
      }),
      env,
    });
    return { response, result: await response.json(), calls, savedAttribution };
  } finally {
    globalThis.fetch = originalFetch;
  }
}

test('complete delivery succeeds without a warning', async () => {
  const { response, result, calls } = await submit();
  assert.equal(response.status, 200);
  assert.deepEqual(result.status, { telegram: 'ok', email: 'ok', crm: 'ok' });
  assert.equal(result.ok, true);
  assert.equal(calls.length, 2);
  assert.match(calls[0].body.text, /UACC-REF: site:empathia-en:123/);
  assert.match(calls[1].body.message, /UACC-REF: site:empathia-en:123/);
});

test('email failure warns through Telegram', async () => {
  const { result, calls } = await submit({ emailOk: false });
  assert.equal(result.ok, true);
  assert.equal(result.status.email, 'failed');
  assert.equal(calls.length, 3);
  assert.equal(calls[2].channel, 'telegram');
  assert.match(calls[2].body.text, /email: failed/);
});

test('Telegram failure warns through email', async () => {
  const { result, calls } = await submit({ telegramOk: false });
  assert.equal(result.ok, true);
  assert.equal(result.status.telegram, 'failed');
  assert.equal(calls.length, 3);
  assert.equal(calls[2].channel, 'email');
  assert.match(calls[2].body.message, /Telegram: failed/);
});

test('CRM failure warns through Telegram while keeping the delivered lead successful', async () => {
  const originalError = console.error;
  console.error = () => {};
  try {
    const { result, calls } = await submit({ crmOk: false });
    assert.equal(result.ok, true);
    assert.equal(result.status.crm, 'failed');
    assert.equal(calls.length, 3);
    assert.equal(calls[2].channel, 'telegram');
  } finally {
    console.error = originalError;
  }
});

test('two failed delivery channels do not report success', async () => {
  const originalError = console.error;
  console.error = () => {};
  try {
    const { result, calls } = await submit({ telegramOk: false, emailOk: false });
    assert.equal(result.ok, false);
    assert.equal(calls.length, 2);
  } finally {
    console.error = originalError;
  }
});

test('Russian forms carry a distinct site label, URL and receipt in both channels',async()=>{const {result,calls}=await submit({source:'empathiavillage.ru',origin:'https://empathiavillage.ru'});assert.equal(result.ok,true);assert.match(calls[0].body.text,/Эмпатия — русский сайт/);assert.match(calls[0].body.text,/Сайт: https:\/\/empathiavillage\.ru\//);assert.match(calls[0].body.text,/site:empathia-ru:123/);assert.match(calls[1].body.subject,/русский сайт/);assert.match(calls[1].body.message,/site:empathia-ru:123/);});
test('English origin controls classification even if payload claims Russian',async()=>{const {calls}=await submit({source:'empathiavillage.ru',origin:'https://empathia-seychelles.com'});assert.match(calls[0].body.text,/Эмпатия — английский сайт/);assert.match(calls[0].body.text,/site:empathia-en:123/);assert.match(calls[1].body.subject,/английский сайт/);});

test('durable receipt and sanitized attribution are saved with the enquiry',async()=>{const {result,savedAttribution,calls}=await submit({attribution:{gclid:'valid_click_123',utm_source:'google',utm_medium:'cpc',utm_campaign:'Villas',contactEmail:'must-not-pass',landing_page:'/contact'}});assert.equal(result.lead_reference,'site:empathia-en:123');assert.equal(savedAttribution.gclid,'valid_click_123');assert.equal(savedAttribution.contactEmail,undefined);assert.match(calls[0].body.text,/Google Ads/);assert(!calls[0].body.text.includes('valid_click_123'),'raw click IDs stay in private metadata');});
