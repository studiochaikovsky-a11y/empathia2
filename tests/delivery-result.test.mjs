import test from 'node:test';
import assert from 'node:assert/strict';
import {deliveryResult} from '../functions/_lib/delivery-result.js';
test('email acceptance requires an explicit provider receipt',async()=>{
 assert.deepEqual(await deliveryResult(Response.json({success:true}),'email'),{ok:true,httpStatus:200,code:'accepted'});
 for(const body of [{},{success:false},{ok:true}])assert.equal((await deliveryResult(Response.json(body),'email')).ok,false);
 assert.deepEqual(await deliveryResult(new Response('<html>blocked</html>',{status:403}),'email'),{ok:false,httpStatus:403,code:'forbidden'});
});
test('diagnostic codes distinguish provider restrictions without retaining response content',async()=>{
 const r=await deliveryResult(Response.json({success:false,message:'Server side method is not allowed. key secret must never appear'},{status:403}),'email');
 assert.equal(r.code,'server_side_restricted');assert(!JSON.stringify(r).includes('secret'));
 assert.equal((await deliveryResult(Response.json({success:false,message:'Monthly submission limit reached'},{status:400}),'email')).code,'quota_exceeded');
 assert.equal((await deliveryResult(Response.json({ok:true}),'telegram')).ok,true);
});
