(function(){
  var keys=['utm_source','utm_medium','utm_campaign','utm_content','utm_term'];
  function attribution(){
    var query=new URLSearchParams(location.search);
    var result={};
    keys.forEach(function(key){
      try{if(query.get(key))sessionStorage.setItem(key,query.get(key));result[key]=sessionStorage.getItem(key)||'';}
      catch(error){result[key]='';}
    });
    return result;
  }
  window.evAttribution=attribution;
  window.evTrack=function(name,params){
    var details=Object.assign({page:location.pathname},attribution(),params||{});
    window.dataLayer=window.dataLayer||[];
    window.dataLayer.push(Object.assign({event:name},details));
  };
  document.addEventListener('click',function(event){
    var target=event.target.closest('a,button');
    if(!target)return;
    var href=target.getAttribute('href')||'';
    var named=target.getAttribute('data-track');
    if(named)window.evTrack(named,{label:(target.textContent||'').trim(),href:href});
    else if(href.indexOf('wa.me')>-1)window.evTrack('whatsapp_click',{href:href});
    else if(/\.pdf(?:$|\?)/i.test(href))window.evTrack('brochure_download',{href:href});
    else if(/^tel:/i.test(href))window.evTrack('phone_click',{href:href});
    else if(/^mailto:/i.test(href))window.evTrack('email_click',{href:href});
  });
  attribution();
})();