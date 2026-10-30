// Store only bounded diagnostic codes, never provider response bodies or keys.
export async function deliveryResult(response,channel){
  const body=await response.json().catch(()=>null);
  const ok=response.ok&&(channel==='email'?body?.success===true:body?.ok===true);
  const message=String(body?.message||body?.error||'');
  let code=ok?'accepted':response.status===429?'rate_limited':response.status>=500?'provider_unavailable':response.status===403?'forbidden':response.status===401?'unauthorized':!body?'invalid_response':'rejected';
  if(!ok&&/access.?key|api.?key/i.test(message)&&/invalid|missing|required|not found/i.test(message))code='invalid_key';
  else if(!ok&&/monthly|quota|submission limit/i.test(message))code='quota_exceeded';
  else if(!ok&&/server.?side|method.{0,15}not allowed/i.test(message))code='server_side_restricted';
  else if(!ok&&/blocked|suppress|bounce/i.test(message))code='delivery_blocked';
  return {ok,httpStatus:response.status,code};
}
