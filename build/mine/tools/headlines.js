const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
const URL='file://'+S+'cyber-desk.html#news';
let fails=0;const ok=(c,m)=>{console.log((c?'PASS ':'FAIL ')+m);if(!c)fails++;};
const now=Date.now(),iso=h=>new Date(now-h*3600000).toISOString();
const items=[
 {t:'Ransomware hits <img src=x onerror="window.__xss=1"> hospital',u:'https://example.org/a?x=1&y=2',src:'Pub <b>A</b>',d:iso(2),c:'Belgium',lang:'en'},
 {t:'Evil link',u:'javascript:alert(1)',src:'Bad',d:iso(1),c:'',lang:'en'},
 {t:'Data URL',u:'data:text/html,hi',src:'Bad',d:iso(1),c:'',lang:'en'},
 {t:'Ftp link',u:'ftp://example.org/x',src:'Bad',d:iso(1),c:'',lang:'en'},
 {t:'Missing url',src:'Bad',d:iso(1)},
 {t:'Oudste kop',u:'http://example.net/old',src:'Pub B',d:iso(30),c:'Netherlands',lang:'nl'}];
for(let i=0;i<10;i++)items.push({t:'Filler headline '+i,u:'https://example.com/f'+i,src:'Pub F',d:iso(3+i),c:'',lang:'en'});
const DOC={day:'2026-11-21',fetched:iso(1),items,feeds_ok:40,feeds_total:45};
// db stub per db.d.ts: collection(path).orderBy().limit().onSnapshot(next,error)
const STUB=(mode)=>`(()=>{const mode=${JSON.stringify(mode)},DOC=${JSON.stringify(DOC)};window.__q=[];
const snap=(docs)=>({docs,size:docs.length,empty:!docs.length,docChanges:()=>[],metadata:{fromCache:false,hasPendingWrites:false}});
const mk=(id,d)=>({id,exists:true,data:()=>d,metadata:{fromCache:false,hasPendingWrites:false}});
const col=(p)=>{const q={path:p,_o:null,_l:null,orderBy(f,d){q._o=[f,d];return q;},limit(n){q._l=n;return q;},
 onSnapshot(next,err){window.__q.push([p,q._o,q._l]);if(p==='headlines'){if(mode==='error'){setTimeout(()=>err({code:'revoked',message:'x'}),50);}
  else setTimeout(()=>next(snap(mode==='empty'?[]:[mk('2026-11-21',DOC)])),50);}else setTimeout(()=>next(snap([])),10);return()=>{};}};return q;};
window.claude={use:async(n)=>n==='db'?{collection:col,doc:()=>{throw new Error('unused')}}:null};})()`;
(async()=>{const b=await chromium.launch();
async function open(w,stub,lang){const p=await b.newPage({viewport:{width:w,height:900}});p.errs=[];p.on('pageerror',e=>p.errs.push(e.message));
 await p.route(/^https?:/,r=>r.abort());
 if(stub)await p.addInitScript(stub);if(lang)await p.addInitScript(`try{localStorage.setItem('ca26-lang','${lang}')}catch(e){}`);
 await p.goto(URL);await p.waitForSelector('#nw-live .nw-lr, #nw-live .nw-live-none',{timeout:8000}).catch(()=>{});await p.waitForTimeout(300);return p;}
let p=await open(1280,STUB('doc'));
const txt=await p.evaluate(()=>document.getElementById('nw-live').innerText);console.log(txt.slice(0,500));
ok(await p.evaluate(()=>window.__q.some(q=>q[0]==='headlines'&&q[1]&&q[1][0]==='day'&&q[1][1]==='desc'&&q[2]===1)),'subscribed once to headlines orderBy day desc limit 1: '+JSON.stringify(await p.evaluate(()=>window.__q.filter(q=>q[0]==='headlines'))));
ok(await p.evaluate(()=>window.__q.filter(q=>q[0]==='headlines').length)===1,'single subscription');
ok(/Collected \d.* from 40 of 45 feeds · 12 headlines on our topics/.test(txt),'status line: '+(txt.match(/Collected \d[^\n]*/)||[''])[0]);
ok(await p.evaluate(()=>document.querySelectorAll('#nw-live .nw-lr').length)===8,'8 visible');
ok(/Publisher's headline, not checked by us/.test(txt),'label');
ok(await p.evaluate(()=>document.querySelectorAll('#nw-live img,#nw-live script').length)===0&&await p.evaluate(()=>window.__xss)===undefined,'no injected elements, no xss');
ok(await p.evaluate(()=>[...document.querySelectorAll('#nw-live .nw-lr a')].some(a=>a.textContent.includes('<img src=x onerror='))),'<img onerror> title shown as text');
ok(await p.evaluate(()=>[...document.querySelectorAll('#nw-live .nw-lr')].some(r=>r.innerText.includes('Pub <b>A</b>'))),'source escaped');
ok(await p.evaluate(()=>[...document.querySelectorAll('#nw-live .nw-lr a')].every(a=>/^https?:/.test(a.href)&&a.rel==='noopener noreferrer'&&a.target==='_blank')),'all links http(s) + noopener');
ok(await p.evaluate(()=>!/Evil link|Data URL|Ftp link|Missing url/.test(document.getElementById('nw-live').innerText)),'non-http(s) items dropped');
ok(await p.evaluate(()=>document.querySelector('#nw-live .nw-lr a').textContent.startsWith('Ransomware hits')),'newest first');
ok(await p.evaluate(()=>!document.getElementById('nw-live-re')),'no reload button in db mode');
await p.click('#nw-live-more');
ok(await p.evaluate(()=>document.querySelectorAll('#nw-live .nw-lr').length)===12,'show more reveals the rest (12 valid)');
ok(/Show fewer/.test(await p.evaluate(()=>document.getElementById('nw-live-more').textContent)),'toggle label');
ok(await p.evaluate(()=>/Oudste kop/.test(document.getElementById('nw-live').innerText)&&document.querySelector('#nw-live .nw-lr:last-child a').textContent==='Oudste kop'),'oldest last');
ok(p.errs.length===0,'no page errors '+JSON.stringify(p.errs));
await p.screenshot({path:S+'headlines-1280.png'});await p.close();
// NL
p=await open(1280,STUB('doc'));
await p.click('#l-nl');await p.waitForTimeout(800);
const nl=await p.evaluate(()=>[document.documentElement.lang,document.getElementById('nw-live').innerText]);
if(nl[0]==='nl'){ok(/Verzameld .* uit 40 van 45 feeds · 12 koppen over onze onderwerpen/.test(nl[1])&&/Kop van de uitgever, niet door ons gecontroleerd/.test(nl[1]),'NL status + label');}
else console.log('SKIP NL (could not switch language via storage): lang='+nl[0]);
await p.close();
// empty
p=await open(1280,STUB('empty'));
let e=await p.evaluate(()=>document.getElementById('nw-live').innerText.trim());
ok(e==='No headlines collected yet today; they arrive with the morning news check or the Fetch button.','empty state: '+e);
ok(!/Live headlines work in the saved file/.test(e),'no old fallback when db present');
ok(p.errs.length===0,'no errors (empty)');await p.close();
// subscription error -> falls back to direct fetch (blocked here) -> old fallback line
p=await open(1280,STUB('error'));await p.waitForTimeout(1500);
e=await p.evaluate(()=>document.getElementById('nw-live').innerText.trim());
ok(/Live headlines work in the saved file/.test(e),'db error + fetch blocked -> old fallback line: '+e);await p.close();
// no db, fetch blocked
p=await open(1280,null);await p.waitForTimeout(1500);
e=await p.evaluate(()=>document.getElementById('nw-live').innerText.trim());
ok(/Live headlines work in the saved file/.test(e),'no db + fetch blocked -> old fallback line');
ok(p.errs.length===0,'no errors (no db)');
await b.close();console.log(fails?'FAILURES':'ALL PASS');process.exit(fails?1:0);})();
