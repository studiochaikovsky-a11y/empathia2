export function leadAttribution(data){
  const raw=data.attribution&&typeof data.attribution==='object'&&!Array.isArray(data.attribution)?data.attribution:data,out={};
  for(const key of ['gclid','gbraid','wbraid'])if(typeof raw[key]==='string'&&/^[A-Za-z0-9_-]{5,512}$/.test(raw[key]))out[key]=raw[key];
  for(const key of ['utm_source','utm_medium','utm_campaign','utm_content','utm_term','utm_id','campaign_id'])if(typeof raw[key]==='string'&&raw[key].trim()&&raw[key].length<=200&&!/[\u0000-\u001f]/.test(raw[key]))out[key]=raw[key].trim();
  if(typeof raw.captured_at==='string'&&raw.captured_at.length<=40&&Number.isFinite(Date.parse(raw.captured_at)))out.captured_at=new Date(raw.captured_at).toISOString();
  if(typeof raw.landing_page==='string'&&/^\/(?!\/)[^?#\s]*$/.test(raw.landing_page)&&raw.landing_page.length<=300)out.landing_page=raw.landing_page;
  return out;
}
