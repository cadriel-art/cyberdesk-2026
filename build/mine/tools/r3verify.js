// UX round 3 verification: every page, NL and EN, no duplicate EN+NL pairs visible, nothing empty.
const { chromium } = require('playwright');
const F='file:///home/user/cyberdesk-2026/build/mine/cyber-desk-offline.html';
let fails=0;const bad=[];const ok=(c,m)=>{if(!c){fails++;bad.push(m);console.log('FAIL '+m);}};
(async()=>{const b=await chromium.launch();
const summary={};
for(const lang of ['nl','en']){
 const ctx=await b.newContext({viewport:{width:1280,height:900}});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(l=>{try{localStorage.setItem('cyberdesk2:lang',JSON.stringify(l))}catch(e){}},lang);
 await p.goto(F+'#home');await p.waitForTimeout(900);
 const keys=await p.evaluate(()=>[...document.querySelectorAll('#pages > article.page')].map(a=>a.id.slice(2)).filter(k=>k!=='search'));
 let enOnly=[];
 for(const k of keys){
  await p.evaluate(k=>{location.hash='#'+k},k);await p.waitForTimeout(350);
  const r=await p.evaluate((lang)=>{
   const pg=document.querySelector('#pages > article.page:not([hidden])');const o={};
   o.len=pg.innerText.length;o.h1=(pg.querySelector('h1')||{}).textContent||'';
   o.dupVis=0;o.dupEx=[];o.nlHiddenInNL=0;o.enHiddenInEN=0;o.emptyNL=0;o.lowRatio=[];
   const vis=e=>getComputedStyle(e).display!=='none';
   pg.querySelectorAll('.nl-x[data-bp]').forEach(n=>{
     const id=n.dataset.bp;const ens=[...pg.querySelectorAll('.en-x[data-bq="'+id+'"]')];
     const nlTxt=n.textContent.replace(/^\s*NL\s*[:–-]?\s*/,'').trim();
     if(!nlTxt)o.emptyNL++;
     if(lang==='nl'){ if(!vis(n))o.nlHiddenInNL++; ens.forEach(e=>{if(vis(e)){o.dupVis++;o.dupEx.push(e.textContent.slice(0,60));}});
        const enLen=ens.reduce((a,e)=>a+e.textContent.length,0); if(ens.length&&nlTxt.length<0.3*enLen&&enLen>200)o.lowRatio.push([nlTxt.length,enLen,nlTxt.slice(0,40)]); }
     else { if(vis(n)){o.dupVis++;o.dupEx.push('NLvisibleInEN '+n.textContent.slice(0,50));} ens.forEach(e=>{if(!vis(e))o.enHiddenInEN++;}); }
   });
   // unpaired nl-x still visible in EN
   if(lang==='en'){pg.querySelectorAll('.nl-x').forEach(n=>{if(vis(n)&&!n.closest('.nl-x:not(:scope)')){o.dupVis++;o.dupEx.push('nl-x visible '+n.textContent.slice(0,40));}});}
   const txt=pg.innerText;
   o.nlMarker=(txt.match(/(^|\n|\s)NL\s*[:–]/g)||[]).length;
   o.enNLtext=0; // dutch-looking strings in EN mode: pages' visible text containing " gewone woorden"
   if(lang==='en'&&/In gewone woorden|Begrippen op deze pagina/.test(txt))o.enNLtext=1;
   o.note=!!pg.querySelector('.bl-note')&&vis(pg.querySelector('.bl-note'));
   return o;},lang);
  summary[lang+':'+k]=r;
  ok(r.len>300||k==='updates'||k==='home'&&r.len>300,`${lang} ${k} visible text ${r.len}`);
  ok(r.dupVis===0,`${lang} ${k} duplicates visible ${r.dupVis} ${JSON.stringify(r.dupEx.slice(0,3))}`);
  ok(r.nlMarker===0,`${lang} ${k} visible "NL:" marker x${r.nlMarker}`);
  ok(r.emptyNL===0,`${lang} ${k} empty NL element x${r.emptyNL}`);
  ok(lang==='en'||r.nlHiddenInNL===0,`${lang} ${k} NL hidden in NL x${r.nlHiddenInNL}`);
  ok(lang==='nl'||r.enHiddenInEN===0,`${lang} ${k} EN hidden in EN x${r.enHiddenInEN}`);
  ok(r.enNLtext===0,`${lang} ${k} Dutch heading visible in EN`);
  if(r.lowRatio.length)console.log('lowratio',lang,k,JSON.stringify(r.lowRatio.slice(0,3)));
  if(lang==='nl'&&r.note)enOnly.push(k);
 }
 ok(errs.length===0,`${lang} page errors ${errs.join('|')}`);
 if(lang==='nl')console.log('NL pages with the "only in English" note:',enOnly.join(' '));
 await ctx.close();
}
require('fs').writeFileSync('/tmp/claude-0/-home-user-cyberdesk-2026/f8cf100d-5e4d-5da9-85e8-2780be2a451a/scratchpad/r3/verify.json',JSON.stringify(summary,null,1));
console.log('pages checked per language:',Object.keys(summary).length/2,'FAILS',fails);
await b.close();process.exit(fails?1:0);})();
