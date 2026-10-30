import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';
const tracking=readFileSync(new URL('../marketing-events.js',import.meta.url),'utf8');
const contact=readFileSync(new URL('../contact.html',import.meta.url),'utf8');
const formScript=[...contact.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(s=>s.includes('async function submitForm()'));
function setup({ok=true,httpOk=true,hostname='empathia-seychelles.com'}={}){
  const events=[],internal=[],requests=[];const button={disabled:false,textContent:''};
  const fields=Object.fromEntries(['fn','fe','fp','fv','contact-status'].map(id=>[id,{value:'',validity:{valid:true},focus(){},hidden:true,textContent:'',className:''}]));fields.fn.value='Private name';fields.fe.value='private@example.test';fields.fp.value='+2481234567';
  const context={location:{hostname,pathname:'/contact',search:''},document:{title:'Contact',addEventListener(){},getElementById:id=>fields[id],querySelector:()=>button},navigator:{sendBeacon:(url,blob)=>{internal.push(url);return true;}},URLSearchParams,Blob,sessionStorage:{setItem(){},getItem(){return null;}},fetch:async(url,options)=>{requests.push(url);return {ok:httpOk,json:async()=>({ok})};}};
  context._utm=()=>({});context.window=context;context.addEventListener=()=>{};context.gtag=(...args)=>events.push(args);runInNewContext(tracking,context);runInNewContext(formScript,context);return {context,events,internal,requests,fields,button};
}
test('a delivered contact form records exactly one GA4 lead, separately from Ads',async()=>{
  const t=setup();await t.context.submitForm();assert.equal(t.requests.length,1);assert.equal(t.events.filter(e=>e[1]==='generate_lead').length,1);assert.equal(t.events.filter(e=>e[1]==='conversion').length,1);
  const lead=t.events.find(e=>e[1]==='generate_lead');assert.equal(lead[2].send_to,'G-3G2W4S48YP');assert.equal(lead[2].form_id,'contact');assert(!JSON.stringify(lead).includes('Private'));assert(!JSON.stringify(lead).includes('private@example'));assert(!JSON.stringify(lead).includes('+248'));
  await t.context.submitForm();assert.equal(t.events.filter(e=>e[1]==='generate_lead').length,1,'cleared form cannot generate another lead');
});
test('invalid fields, failed delivery and HTTP errors never count as leads',async()=>{
  for(const config of [{ok:false},{httpOk:false}]){const t=setup(config);await t.context.submitForm();assert.equal(t.events.length,0);}
  const t=setup();t.fields.fp.value='12';await t.context.submitForm();assert.equal(t.requests.length,0);assert.equal(t.events.length,0);
});
test('double clicks while delivery is pending send one request and one event',async()=>{
  const t=setup();let release;t.context.fetch=()=>new Promise(resolve=>{t.requests.push('/api/lead');release=()=>resolve({ok:true,json:async()=>({ok:true})});});const first=t.context.submitForm();await t.context.submitForm();assert.equal(t.requests.length,1);release();await first;assert.equal(t.events.filter(e=>e[1]==='generate_lead').length,1);
});
test('preview domains do not record GA4 leads; internal logging failure does not hide GA4 success',async()=>{
  const preview=setup({hostname:'preview.empathivillage.pages.dev'});await preview.context.submitForm();assert.equal(preview.events.filter(e=>e[1]==='generate_lead').length,0);
  const t=setup();t.context.evTrack=()=>{throw Error('blocked logger');};await t.context.submitForm();assert.equal(t.events.filter(e=>e[1]==='generate_lead').length,1);
});
test('built pages initialize GA4 once on the public domain and exclude preview traffic',()=>{
  const html=readFileSync(new URL('../dist/contact.html',import.meta.url),'utf8');assert(html.includes('marketing-events.js?v=20261030-ga4'));assert.equal((html.match(/gtag\('config', 'G-3G2W4S48YP'\)/g)||[]).length,1);
  const script=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(s=>s.includes("gtag('config', 'G-3G2W4S48YP')"));
  for(const hostname of ['empathia-seychelles.com','www.empathia-seychelles.com','preview.empathivillage.pages.dev','localhost']){const c={location:{hostname},window:{}};c.window=c;runInNewContext(script,c);const count=c.dataLayer.filter(a=>a[0]==='config'&&a[1]==='G-3G2W4S48YP').length;assert.equal(count,hostname.endsWith('empathia-seychelles.com')?1:0);}
});
