(function(){
var SNAP=@@SNAP@@,FEEDS=@@FEEDS@@,SUBJ=@@SUBJ@@,PG=@@PG@@;
var items=SNAP.slice(),live=false,tried=false,F={s:'',c:'',off:false,q:''},seen='';
try{seen=localStorage.getItem('ca26-news-seen')||'';}catch(e){}
function lg(){return document.documentElement.lang==='nl'?'nl':'en';}
function L(en,nl){return lg()==='nl'?nl:en;}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function safe(u){return /^https?:\/\//i.test(u||'')?u:'#';}
function fdate(d){var m=/^(\d{4})-(\d\d)-(\d\d)$/.exec(d||'');if(!m)return d||'';try{return new Date(+m[1],+m[2]-1,+m[3]).toLocaleDateString(lg()==='nl'?'nl-BE':'en-GB',{day:'numeric',month:'short',year:'numeric'});}catch(e){return d;}}

var TRIG='trig_01Ny3on9sf9yEF9WGoJxDR2k',CC='Claude Code Remote',COOL=600000,FK='ca26-news-fetch';
var mcpNS=null,perms=null,busy=false,unavail=false,msg='',msgErr=false,cdT=null,cdOverride=0;
var KINDS=[['Official','Official sources','Officiële bronnen'],['News media','News media','Nieuwsmedia'],['Specialist media','Specialist media','Gespecialiseerde media'],['Research','Research','Onderzoek']];
var CTRY={'Belgium':'België','Netherlands':'Nederland','Germany':'Duitsland','France':'Frankrijk','United Kingdom':'Verenigd Koninkrijk','United States':'Verenigde Staten','Europe':'Europa','European Union':'Europese Unie','Luxembourg':'Luxemburg','Spain':'Spanje','Italy':'Italië','Poland':'Polen','Sweden':'Zweden','Denmark':'Denemarken','Norway':'Noorwegen','Estonia':'Estland','Ukraine':'Oekraïne','Switzerland':'Zwitserland','Austria':'Oostenrijk','Ireland':'Ierland'};
function ctry(c){if(!c)return L('International','Internationaal');if(lg()==='nl'){if(CTRY[c])return CTRY[c];if(window.cdUI)return window.cdUI.ctry(c);}return c;}
function pgn(k){return window.cdUI&&lg()==='nl'?window.cdUI.pageName(k,'nl'):PG[k];}
function stTag(s){if(s==='working')return ['ok',L('Read daily','Dagelijks gelezen')];if(s==='needs-domain')return ['wait',L('Not yet reachable','Nog niet bereikbaar')];if(s==='site-blocks')return ['wait',L('Site blocks automatic reading','Site blokkeert automatisch lezen')];if(s==='no-feed-found')return ['wait',L('Feed address not found','Feedadres niet gevonden')];return ['wait',esc(s||'')];}
function feedRow(f){var t=stTag(f.status),nm=lg()==='nl'&&f.name_nl?f.name_nl:f.name;
  return '<li><span class="nw-fn">'+(f.site?'<a href="'+esc(safe(f.site))+'" target="_blank" rel="noopener noreferrer">'+esc(nm)+'</a>':esc(nm))+'</span><span class="nw-fc">'+esc(ctry(f.country))+'</span>'+(f.browser?'<span class="nw-pill of">'+L('Also live in the saved file','Ook live in het opgeslagen bestand')+'</span>':'')+(f.cited?'<span class="nw-pill">'+L('Cited in this file','Geciteerd in dit dossier')+'</span>':'')+'<span class="nw-st '+t[0]+'">'+t[1]+'</span></li>';}
function feedsCard(){
  var fs=(FEEDS||[]).filter(function(f){return f&&f.name;}),known=KINDS.map(function(k){return k[0];});
  var groups=KINDS.map(function(k){return {k:k[0],l:L(k[1],k[2])};});
  fs.forEach(function(f){if(known.indexOf(f.kind)<0&&!groups.some(function(g){return g.k===f.kind;}))groups.push({k:f.kind,l:f.kind||L('Other','Overig')});});
  var n=fs.filter(function(f){return f.status==='working';}).length;
  var h='<details class="nw-help" id="nw-feeds"><summary>'+L('Where the news comes from','Waar het nieuws vandaan komt')+' ('+fs.length+')</summary><div class="nw-helpbody">';
  h+='<p><b>'+n+' '+L('feeds read every morning, plus web searches.','feeds worden elke ochtend gelezen, plus zoekopdrachten op het web.')+'</b></p>';
  h+='<p>'+L('A Claude task reads these feeds every morning at 06:47 Brussels time and adds the items it has checked to this page. Posts on X or other social media are not used.','Een Claude-taak leest deze feeds elke ochtend om 06:47 Belgische tijd en zet de gecontroleerde berichten op deze pagina. Berichten op X of andere sociale media worden niet gebruikt.')+'</p>';
  groups.forEach(function(g){var r=fs.filter(function(f){return (f.kind||'')===g.k;});if(!r.length)return;
    r.sort(function(a,b){var x=a.country==='Belgium'?0:1,y=b.country==='Belgium'?0:1;return x-y||String(a.name).localeCompare(String(b.name));});
    h+='<h4 class="nw-fh">'+esc(g.l)+'</h4><ul class="nw-fl">'+r.map(feedRow).join('')+'</ul>';});
  if(!fs.length)h+='<p class="small">'+L('No feeds listed yet.','Nog geen feeds vermeld.')+'</p>';
  return h+'</div></details>';
}
function lastStart(){var v=0;try{v=+localStorage.getItem(FK)||0;}catch(e){}return Math.max(v,cdOverride);}
function cdLeft(){var t=lastStart();return t?Math.max(0,t+COOL-Date.now()):0;}
function btnState(){
  var box=document.getElementById('nw-fetch');if(!box)return;
  if(!mcpNS){if(location.protocol==='file:'){box.hidden=false;box.innerHTML='<a class="nw-fbtn nw-fopen" href="https://claude.ai/artifact/1TUsEzWWR2P9biSw9tQt82#news" target="_blank" rel="noopener noreferrer">'+L("Fetch today's news in the online app","Nieuws van vandaag ophalen in de online app")+'</a><span class="nw-fmsg">'+L('The fetch button works only in the online app on claude.ai (it needs your Claude login). This saved file shows the news as of its last update, plus the live headlines below.','De ophaalknop werkt alleen in de online app op claude.ai (hij heeft uw Claude-login nodig). Dit opgeslagen bestand toont het nieuws van de laatste update, plus de live koppen hieronder.')+'</span>';}else box.hidden=true;return;}
  box.hidden=false;var b=document.getElementById('nw-fbtn'),st=document.getElementById('nw-fmsg');if(!b||!st)return;
  var cd=cdLeft(),text=msg,err=msgErr;
  if(unavail){b.disabled=true;text=L('Only the owner can start a fetch','Alleen de eigenaar kan ophalen');err=false;}
  else if(busy){b.disabled=true;text=L('Starting…','Bezig met starten…');err=false;}
  else if(cd>0){b.disabled=true;if(!err)text=L('Started — new items appear here in about 2–5 minutes','Gestart — nieuwe berichten verschijnen hier over ongeveer 2–5 minuten');}
  else b.disabled=false;
  st.textContent=text;st.className='nw-fmsg'+(err?' err':'');
  clearTimeout(cdT);if(cd>0&&!unavail)cdT=setTimeout(function(){msg='';msgErr=false;btnState();},cd+50);
}
function failMsg(e){var c=e&&e.code;
  if(c==='blocked_by_policy'||c==='not_granted'){unavail=true;return ['',false];}
  if(c==='not_in_manifest'||c==='approval_required'||c==='consent_required')return [L('Not allowed yet. The connector needs your permission to start a fetch; try again and choose Allow.','Nog niet toegestaan. De connector heeft uw toestemming nodig om op te halen; probeer opnieuw en kies Toestaan.'),true];
  if(c==='needs_reauth')return [L('Reconnect "Claude Code Remote" in claude.ai Settings → Connectors, then try again.','Verbind "Claude Code Remote" opnieuw via claude.ai Instellingen → Connectors en probeer dan opnieuw.'),true];
  if(c==='server_not_connected'||c==='selection_required'||c==='server_not_found')return [L('The "Claude Code Remote" connector is not available. Add it in claude.ai Settings → Connectors.','De connector "Claude Code Remote" is niet beschikbaar. Voeg hem toe via claude.ai Instellingen → Connectors.'),true];
  if(c==='tool_error')return [L('The connector refused the request. Nothing was started.','De connector weigerde het verzoek. Er is niets gestart.'),true];
  if(e&&e.retryable)return [L('The connector did not answer. A fetch may or may not have started; wait a minute, then try again.','De connector antwoordde niet. Mogelijk is het ophalen wel of niet gestart; wacht even en probeer opnieuw.'),true];
  return [L('Could not start the fetch. Please try again later.','Ophalen starten is niet gelukt. Probeer het later opnieuw.'),true];
}
function startFetch(){
  if(busy||unavail||!mcpNS||cdLeft()>0)return;
  busy=true;msg='';msgErr=false;btnState();
  var pr=perms&&perms.request?Promise.resolve().then(function(){return perms.request(['mcp:'+CC]);}).catch(function(){return null;}):Promise.resolve(null);
  pr.then(function(res){
    if(res&&res['mcp:'+CC]==='denied')throw {code:'approval_required'};
    return mcpNS.listTools(CC);
  }).then(function(r){
    var sv=((r&&r.servers)||[]).filter(function(s){return s.server===CC;})[0];
    if(!sv||!(sv.tools||[]).some(function(t){return t.name==='fire_trigger';}))throw {code:'blocked_by_policy'};
    return mcpNS.callTool(CC,'fire_trigger',{trigger_id:TRIG,text:'On-demand run from the News reader button: look for news from today (and since the last items) only.'});
  }).then(function(){
    cdOverride=Date.now();try{localStorage.setItem(FK,String(cdOverride));}catch(e){}
    busy=false;msg='';msgErr=false;btnState();
  },function(e){
    busy=false;var f=failMsg(e);msg=f[0];msgErr=f[1];btnState();
  });
}
function match(it){if(F.s&&(it.s||[]).indexOf(F.s)<0)return false;if(F.c&&it.c!==F.c)return false;if(F.off&&!it.off)return false;if(F.q){var t=((it.t||'')+' '+(it.sum||'')+' '+(it.sum_nl||'')+' '+(it.src||'')+' '+(it.c||'')).toLowerCase();if(t.indexOf(F.q)<0)return false;}return true;}
function card(it){
  var h='<div class="nw-it"><div class="nw-meta"><b>'+esc(fdate(it.d))+'</b>'+(it.c?'<span>'+esc(ctry(it.c))+'</span>':'')+'<span>'+esc(it.src||'')+(it.stype?' · '+esc(it.stype):'')+'</span>';
  if(it.added&&it.added>seen&&seen)h+='<span class="nw-pill new">'+L('NEW','NIEUW')+'</span>';
  h+=it.off?'<span class="nw-pill of">'+L('Official source','Officiële bron')+'</span>':'<span class="nw-pill un">'+(it.kind==='x'?L('Post on X, not verified by us','Bericht op X, niet door ons geverifieerd'):L('News, not yet verified by us','Nieuws, nog niet door ons geverifieerd'))+'</span>';
  h+='</div><h4><a href="'+esc(safe(it.url))+'" target="_blank" rel="noopener noreferrer">'+esc(it.t||'')+'</a></h4><p>'+esc(lg()==='nl'&&it.sum_nl?it.sum_nl:(it.sum||''))+'</p><div class="nw-meta" style="margin-top:7px">';
  (it.s||[]).forEach(function(k){if(SUBJ[k])h+='<span class="nw-pill">'+esc(SUBJ[k][lg()==='nl'?1:0])+'</span>';});
  if(it.rel&&PG[it.rel])h+='<a href="#'+esc(it.rel)+'">'+L('In this file: ','In dit dossier: ')+esc(pgn(it.rel))+'</a>';
  return h+'</div></div>';
}
function list(){
  var box=document.getElementById('nw-list');if(!box)return;
  var v=items.filter(match).sort(function(a,b){return (b.d||'').localeCompare(a.d||'');});
  var n=v.filter(function(i){return i.kind!=='x';}),x=v.filter(function(i){return i.kind==='x';});
  box.innerHTML=n.length?n.map(card).join(''):'<div class="u-empty nw-empty" role="status"><p>'+L('Nothing matches these filters.','Niets gevonden met deze filters.')+'</p><button type="button" class="u-reset" id="nw-reset">'+L('Reset filters','Filters herstellen')+'</button></div>';
  document.getElementById('nw-x').innerHTML=x.length?x.map(card).join(''):'<p class="small">'+L('No posts yet. Posts on X cannot be read automatically from here. A post is added by hand, and only as a lead: it stays marked "not verified" until a second source confirms it.','Nog geen berichten. Berichten op X kunnen van hieruit niet automatisch gelezen worden. Een bericht wordt met de hand toegevoegd, en alleen als aanwijzing: het blijft "niet geverifieerd" tot een tweede bron het bevestigt.')+'</p>';
  var last=items.reduce(function(m,i){return (i.added||'')>m?i.added:m;},'');
  document.getElementById('nw-state').textContent=n.length+' '+L('news items','nieuwsberichten')+(x.length?' · '+x.length+' '+L('posts on X','berichten op X'):'')+' · '+L('last refresh: ','laatste verversing: ')+fdate(last)+' · '+(live?L('live from the database','live uit de database'):L('saved copy (the live list is in the online app)','bewaarde kopie (de live lijst staat in de online app)'));
  if(last&&last>seen){setTimeout(function(){try{localStorage.setItem('ca26-news-seen',last);}catch(e){}},8000);}
}

/* ---- Live headlines: read in the visitor's browser, never stored, never inserted as HTML ---- */
var LV={state:'idle',res:null,at:null,rows:[],ok:0,total:0,failed:[],busy:false};
var LKW=['cyber','hack','ransomware','data leak','datalek','fuite de données','ddos','drone','drones','sabotage','arson','brandstichting','incendie criminel','cable','câble','kabel','pipeline','pijpleiding','gaspijpleiding','jamming','gps','spy','spion','espion','espionage','spionage','disinformation','desinformatie','désinformation','election interference','chat control','nis2','phishing','malware','breach','cyberaanval','cyberattaque','cyberangriff'];
var LKW_WHOLE={'gps':1,'spy':1,'drone':1};
/* 'hybrid' counts only in a security sense: hybrid threat/attack/warfare ..., hybride dreiging/aanval/oorlog(voering) ..., menaces hybrides, guerre hybride */
var LHYB=/(^|[^a-zà-öø-ÿ0-9])(?:hybrid[ -](?:threats?|attacks?|warfare|war|wars|campaigns?|operations?|interference|sabotage|activit(?:y|ies)|tactics|incidents?|actors?|measures|conflict)|hybride[ -](?:dreigingen|dreiging|aanvallen|aanval|oorlogvoering|oorlog|acties|actie|operaties|sabotage|campagnes?|inmenging)|menaces? hybrides?|guerres? hybrides?|attaques? hybrides?|hybrid(?:e)?[ -]?bedreigingen)(?![a-zà-öø-ÿ0-9])/i;
/* phrases that make a topic word harmless: breach of contract, cable car, pipeline of talent, spy film, drone music ... they are cut out before the topic words are looked up */
var LNEG=new RegExp('(?:breach(?:es|ed)? of (?:contract|contracts|duty|trust|promise|etiquette|the peace|covenant|warranty|agreement|rules|copyright|privilege|fiduciary)|(?:contract|copyright|trademark|patent|warranty) breach(?:es)?|cable[ -](?:cars?|tv|television|news|channels?|networks?|bills?|compan(?:y|ies)|providers?|subscribers?|knit|knitted|sweaters?|stitch|stitches|ties?|stayed)|kabel(?:baan|banen|televisie|krant|jauw|jauwen)\\w*|(?:sales|talent|product|project|deal|investment|development|clinical|drug|pharma|innovation|recruitment|hiring|leadership|housing|legislative|film|content|order|renewable|energy project) pipelines?|pipelines? of (?:talent|projects?|deals?|drugs?|candidates|ideas)|spy[ -](?:films?|movies?|novels?|thrillers?|series|dramas?|comed(?:y|ies)|games?|fiction|stor(?:y|ies)|kids|x family|shots?|cams?)|(?:film|movie|tv|thriller)s? spy|drone[ -](?:music|metal|doom|albums?|bands?|tracks?|ambient|shows?|light shows?|photograph\\w*|racing|racer|racers?|footage of (?:the )?(?:wedding|concert|festival))|(?:light|firework) drone shows?|gps[ -](?:watch(?:es)?|tracker|trackers|navigation|navigator|route|app|apps)|life ?hacks?|hackathons?|hackney|kitchen hacks?|cyber ?(?:monday|week|truck|punk|sale|sales|deals?)|cybertruck|cyberpunk)','gi');

var LEU=['europe','european','europa','europese','europees','eu','nato','europol','enisa','austria','austrian','oostenrijk','oostenrijks','belgium','belgian','belgië','belgisch','bulgaria','bulgarian','bulgarije','bulgaars','croatia','croatian','kroatië','kroatisch','cyprus','cypriot','czechia','czech','tsjechië','tsjechisch','denmark','danish','denemarken','deens','estonia','estonian','estland','estisch','finland','finnish','fins','france','french','frankrijk','frans','germany','german','duitsland','duits','greece','greek','griekenland','grieks','hungary','hungarian','hongarije','hongaars','ireland','irish','ierland','iers','italy','italian','italië','italiaans','latvia','latvian','letland','lets','lithuania','lithuanian','litouwen','litouws','luxembourg','luxemburg','malta','maltese','netherlands','dutch','nederland','nederlands','poland','polish','polen','pools','portugal','portuguese','portugees','romania','romanian','roemenië','roemeens','slovakia','slovak','slowakije','slovenia','slovenian','slovenië','sloveens','spain','spanish','spanje','spaans','sweden','swedish','zweden','zweeds','norway','norwegian','noorwegen','noors','iceland','icelandic','ijsland','ijslands','switzerland','swiss','zwitserland','zwitsers','liechtenstein'];
var LCH='a-zà-öø-ÿ0-9';
function lre(words){return new RegExp('(^|[^'+LCH+'])(?:'+words.join('|')+')(?:s|en)?(?![' +LCH+'])','i');}
var LRE_EU=lre(LEU);
function lkw(t){
  /* topic words: prefix match for long words (hack -> hackers, kabel -> kabels), whole word for short ones */
  var s=String(t).toLowerCase().replace(LNEG,' '),i;
  if(LHYB.test(s))return true;
  for(i=0;i<LKW.length;i++){var w=LKW[i],p=s.indexOf(w);while(p>=0){var b=p===0||!new RegExp('['+LCH+']').test(s.charAt(p-1)),e=s.charAt(p+w.length);
    if(b&&(!LKW_WHOLE[w]||!e||!new RegExp('['+LCH+']').test(e)))return true;p=s.indexOf(w,p+1);}}
  return false;}
function leu(t){return LRE_EU.test(t);}
function ltxt(s){try{var d=new DOMParser().parseFromString(String(s||''),'text/html');return (d.body.textContent||'').replace(/\s+/g,' ').trim();}catch(e){return '';}}
function lkid(n,names){var r=null,c=n.children,i;for(i=0;i<c.length&&!r;i++){if(names.indexOf(c[i].localName)>=0){var v=c[i];r=v;}}return r;}
function lparse(xml,f){
  var d=new DOMParser().parseFromString(xml,'text/xml');if(d.getElementsByTagName('parsererror').length)throw new Error('xml');
  var out=[],ns=d.getElementsByTagName('item');if(!ns.length)ns=d.getElementsByTagName('entry');
  for(var i=0;i<ns.length;i++){var n=ns[i],t=lkid(n,['title']),ln=null,c=n.children,k;
    for(k=0;k<c.length;k++){if(c[k].localName==='link'){var h=c[k].getAttribute('href'),rl=c[k].getAttribute('rel');
      if(h){if(!ln||rl==='alternate'||!rl)ln=h;}else if(!ln&&c[k].textContent.trim())ln=c[k].textContent.trim();}}
    if(!ln){var g=lkid(n,['guid']);if(g&&/^https?:\/\//i.test(g.textContent.trim()))ln=g.textContent.trim();}
    var dt=lkid(n,['pubdate','pubDate','published','updated','date']),ds=lkid(n,['description','summary','encoded','content']);
    var ts=dt?Date.parse(dt.textContent.trim()):NaN;
    if(!t||!ln||isNaN(ts)||!/^https?:\/\//i.test(ln.trim()))continue;
    out.push({t:ltxt(t.textContent),u:ln.trim(),ts:ts,s:ds?ltxt(ds.textContent):'',f:f});}
  return out;}
function lfetch(f){
  var ac=typeof AbortController==='function'?new AbortController():null,tm=null;
  var to=new Promise(function(_,rej){tm=setTimeout(function(){try{if(ac)ac.abort();}catch(e){}rej(new Error('timeout'));},12000);});
  var rq=fetch(f.url,ac?{cache:'no-store',signal:ac.signal}:{cache:'no-store'}).then(function(r){if(!r.ok)throw new Error('http');return r.text();}).then(function(x){return lparse(x,f);});
  return Promise.race([rq,to]).then(function(v){clearTimeout(tm);return v;},function(e){clearTimeout(tm);throw e;});}
function lload(){
  if(LV.busy)return;LV.busy=true;LV.state='loading';liveRender();
  var fs=(FEEDS||[]).filter(function(f){return f&&f.browser&&f.url;});LV.total=fs.length;
  var jobs=fs.map(function(f){var p;try{p=lfetch(f);}catch(e){p=Promise.reject(e);}return p.then(function(r){return {f:f,r:r};},function(){return {f:f,r:null};});});
  Promise.all(jobs).then(function(all){
    var now=Date.now(),seenU={},rows=[],ok=0,failed=[];
    all.forEach(function(a){if(!a.r){failed.push(a.f);return;}ok++;
      a.r.forEach(function(it){
        if(now-it.ts>72*3600000||it.ts-now>24*3600000)return;
        var txt=it.t+' '+it.s;if(!lkw(txt))return;
        if(!a.f.country&&!leu(txt))return;
        if(seenU[it.u])return;seenU[it.u]=1;rows.push(it);});});
    rows.sort(function(x,y){return y.ts-x.ts;});
    LV.ok=ok;LV.failed=failed;LV.all=rows.length;LV.rows=rows.slice(0,30);LV.at=new Date();LV.state=ok?'done':'fail';LV.busy=false;liveRender();
  }).catch(function(){LV.state='fail';LV.ok=0;LV.busy=false;liveRender();});
}
function ldt(ts){try{return new Date(ts).toLocaleString(lg()==='nl'?'nl-BE':'en-GB',{day:'numeric',month:'short',hour:'2-digit',minute:'2-digit'});}catch(e){return '';}}
function liveRender(){
  var el=document.getElementById('nw-live');if(!el)return;
  if(LV.state==='fail'){el.className='nw-live nw-live-off';el.innerHTML='<p class="nw-live-none">'+L('Live headlines work in the saved file opened in your browser.','Live koppen werken in het opgeslagen bestand, geopend in uw browser.')+'</p>';return;}
  el.className='nw-live';
  var tag=L("Publisher's headline, not checked by us","Kop van de uitgever, niet door ons gecontroleerd"),h='<div class="nw-live-h"><h3>'+L('Live headlines from '+LV.total+' feeds','Live koppen uit '+LV.total+' feeds')+'</h3><span class="nw-pill un">'+tag+'</span><button type="button" id="nw-live-re" class="nw-live-re"'+(LV.busy?' disabled':'')+'>'+L('Reload','Opnieuw laden')+'</button></div>';
  h+='<p class="nw-live-sub">'+L('Read by your browser straight from the publishers, just now. Last 72 hours, on the subjects of this file. Nothing is stored here and none of it has been checked.','Door uw browser rechtstreeks bij de uitgevers gelezen, zonet. Laatste 72 uur, over de onderwerpen van dit dossier. Er wordt niets bewaard en niets is gecontroleerd.')+'</p>';
  if(LV.state==='loading'||LV.state==='idle'){el.innerHTML=h+'<p class="nw-state" role="status">'+L('Reading the feeds…','De feeds worden gelezen…')+'</p>';return;}
  var st=L('Read just now from '+LV.ok+' of '+LV.total+' feeds · '+LV.all+' headlines on our topics','Zonet gelezen uit '+LV.ok+' van '+LV.total+' feeds · '+LV.all+' koppen over onze onderwerpen');
  if(LV.at)st+=' ('+LV.at.toLocaleTimeString(lg()==='nl'?'nl-BE':'en-GB',{hour:'2-digit',minute:'2-digit'})+')';
  if(LV.failed.length)st+=' · '+L('Not reachable: ','Niet bereikbaar: ')+LV.failed.map(function(f){return lg()==='nl'&&f.name_nl?f.name_nl:f.name;}).join(', ');
  h+='<div class="nw-state" role="status">'+esc(st)+'</div><div class="nw-live-list">';
  if(!LV.rows.length)h+='<p class="small">'+L('No headline in the last 72 hours matched our topics.','Geen kop van de laatste 72 uur kwam overeen met onze onderwerpen.')+'</p>';
  LV.rows.forEach(function(r,ri){if(!LV.more&&ri>=8)return;var nm=lg()==='nl'&&r.f.name_nl?r.f.name_nl:r.f.name,s=r.s.length>200?r.s.slice(0,199).replace(/\s+\S*$/,'')+'…':r.s;
    h+='<div class="nw-lr"><div class="nw-meta"><b>'+esc(ldt(r.ts))+'</b><span>'+esc(nm)+'</span><span class="nw-pill un">'+L("Publisher's headline, not checked by us","Kop van de uitgever, niet door ons gecontroleerd")+'</span></div><a href="'+esc(safe(r.u))+'" target="_blank" rel="noopener noreferrer">'+esc(r.t)+'</a>'+(s?'<div class="nw-ls">'+esc(s)+'</div>':'')+'</div>';});
  h+='</div>';
  if(LV.rows.length>8)h+='<button type="button" id="nw-live-more" class="u-reset nw-live-more" aria-expanded="'+(LV.more?'true':'false')+'">'+(LV.more?L('Show fewer','Toon minder'):L('Show more ('+(LV.rows.length-8)+')','Toon meer ('+(LV.rows.length-8)+')'))+'</button>';
  el.innerHTML=h;
}
document.addEventListener('click',function(e){var t=e.target&&e.target.closest?e.target.closest('#nw-live-re'):null;if(t)lload();});
function shell(el){
  var cs={};items.forEach(function(i){if(i.c)cs[i.c]=1;});
  var h='<h2>'+L('News reader','Nieuwslezer')+'</h2><div class="nw-fetch" id="nw-fetch" hidden><button type="button" id="nw-fbtn" class="nw-fbtn">'+L("Fetch today's news","Nieuws van vandaag ophalen")+'</button><span class="nw-fmsg" id="nw-fmsg" role="status" aria-live="polite"></span></div><p class="sub">'+L('Fresh news on the subjects of this file, refreshed once a day. Every item links to its source.','Vers nieuws over de onderwerpen van dit dossier, één keer per dag ververst. Elk bericht linkt naar de bron.')+'</p>';
  h+='<div class="plainbox"><div class="pb-h">'+L('In plain words','In gewone woorden')+'</div><p>'+L('This page is a reading list, not a list of facts. An item here means "a news outlet reported this". It only becomes part of the file, with a label such as Confirmed or Suspected, after it has been checked and written into one of the subject pages. Until then it carries the amber label "not yet verified by us".','Deze pagina is een leeslijst, geen lijst van feiten. Een bericht hier betekent "een nieuwsmedium meldde dit". Het wordt pas deel van het dossier, met een label zoals Bevestigd of Vermoed, nadat het gecontroleerd is en op een onderwerppagina staat. Tot dan draagt het het amberkleurige label "nog niet door ons geverifieerd".')+'</p></div>';
  h+=feedsCard();
  h+='<section id="nw-live" class="nw-live"></section>';
  h+='<div class="nw-f"><select id="nw-s" aria-label="'+L('Subject','Onderwerp')+'"><option value="">'+L('All subjects','Alle onderwerpen')+'</option>'+Object.keys(SUBJ).map(function(k){return '<option value="'+k+'"'+(F.s===k?' selected':'')+'>'+esc(SUBJ[k][lg()==='nl'?1:0])+'</option>';}).join('')+'</select>';
  h+='<select id="nw-c" aria-label="'+L('Country','Land')+'"><option value="">'+L('All countries','Alle landen')+'</option>'+Object.keys(cs).sort().map(function(c){return '<option value="'+esc(c)+'"'+(F.c===c?' selected':'')+'>'+esc(ctry(c))+'</option>';}).join('')+'</select>';
  h+='<input type="search" id="nw-q" aria-label="'+L('Search the news','Zoek in het nieuws')+'" placeholder="'+L('Search the news','Zoek in het nieuws')+'" value="'+esc(F.q)+'"><label class="ck"><input type="checkbox" id="nw-off"'+(F.off?' checked':'')+'> '+L('Official sources only','Alleen officiële bronnen')+'</label></div>';
  h+='<div class="nw-state" id="nw-state"></div><div class="nw-grid"><div id="nw-list"></div><aside class="nw-side"><h3>'+L('Posts on X','Berichten op X')+'</h3><div id="nw-x"></div></aside></div>';
  el.innerHTML=h;el.dataset.sig=lg()+'|'+Object.keys(cs).length;list();btnState();liveRender();if(LV.state==='idle'&&!LV.busy)lload();
}
function tick(){var el=document.getElementById('dyn-news');if(!el)return;var cs={};items.forEach(function(i){if(i.c)cs[i.c]=1;});var sig=lg()+'|'+Object.keys(cs).length;if(el.dataset.sig!==sig)shell(el);}
document.addEventListener('click',function(e){var t=e.target&&e.target.closest?e.target.closest('#nw-fbtn'):null;if(t)startFetch();
  var r=e.target&&e.target.closest?e.target.closest('#nw-reset'):null;
  if(r){F.s='';F.c='';F.off=false;F.q='';var a=document.getElementById('nw-s'),b=document.getElementById('nw-c'),c=document.getElementById('nw-q'),d=document.getElementById('nw-off');if(a)a.value='';if(b)b.value='';if(c)c.value='';if(d)d.checked=false;list();}
  var m=e.target&&e.target.closest?e.target.closest('#nw-live-more'):null;
  if(m){LV.more=!LV.more;liveRender();}});
document.addEventListener('change',function(e){var t=e.target;if(t.id==='nw-s'){F.s=t.value;list();}else if(t.id==='nw-c'){F.c=t.value;list();}else if(t.id==='nw-off'){F.off=t.checked;list();}});
document.addEventListener('input',function(e){if(e.target.id==='nw-q'){F.q=e.target.value.trim().toLowerCase();list();}});
window.addEventListener('hashchange',function(){setTimeout(tick,0);});document.addEventListener('DOMContentLoaded',tick);setInterval(tick,600);
(function(){var w=window.claude;if(!w||!w.use)return;
  try{w.use('mcp').then(function(m){mcpNS=m||null;btnState();},function(){});}catch(e){}
  try{w.use('permissions').then(function(p){perms=p||null;},function(){});}catch(e){}})();
(function connect(){if(tried)return;tried=true;var w=window.claude;if(!w||!w.use)return;
  w.use('db').then(function(db){if(!db)return;try{db.collection('news').onSnapshot(function(snap){var a=snap.docs.map(function(d){var v=d.data()||{};v.id=d.id;return v;});if(a.length){items=a;live=true;}list();tick();},function(){});}catch(e){}});})();
})();
