export function leadSource(request,data){
  let host='';try{host=new URL(request.headers.get('Origin')||'').hostname.toLowerCase().replace(/^www\./,'');}catch{}
  const supported=['empathiavillage.ru','empathia-seychelles.com'];
  const domain=supported.includes(host)?host:data.source==='empathiavillage.ru'?'empathiavillage.ru':'empathia-seychelles.com';
  const ru=domain==='empathiavillage.ru';
  return {domain,refPrefix:ru?'site:empathia-ru:':'site:empathia-en:',label:ru?'Эмпатия — русский сайт':'Эмпатия — английский сайт',url:ru?'https://empathiavillage.ru/':'https://empathia-seychelles.com/'};
}
