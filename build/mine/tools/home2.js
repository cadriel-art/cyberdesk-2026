
/* ---------- home2: What's new from the live `updates` collection (online file) ---------- */
window.__homeUpd=function(list){
  try{
    var ul=document.getElementById('hm-new'); if(!ul||!list||!list.length)return;
    function e(x){return String(x==null?'':x).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
    function sh(t){t=String(t||'').trim();if(t.length<=190)return t;var c=t.slice(0,190),i=Math.max(c.lastIndexOf('. '),c.lastIndexOf('; '));return i>60?c.slice(0,i+1):c.slice(0,c.lastIndexOf(' '))+'…';}
    function L(a,b){return '<span class="hl hl-en">'+e(a)+'</span><span class="hl hl-nl">'+e(b)+'</span>';}
    ul.innerHTML=list.slice(0,3).map(function(u){
      return '<li class="hm-upd"><div class="hm-when">'+e(u.date||'')+(u.tag?' · '+L(u.tag,({'New':'Nieuw','Check':'Controle','Attribution':'Toeschrijving','New incidents':'Nieuwe incidenten','Correction':'Correctie'})[u.tag]||u.tag):'')+'</div><b>'+L(u.title,u.title_nl||u.title)+'</b><p>'+L(sh(u.body),sh(u.body_nl||u.body))+'</p></li>';
    }).join('');
  }catch(x){}
};
