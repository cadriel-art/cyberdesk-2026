const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();
for(const w of [390,1280]){const p=await b.newPage({viewport:{width:w,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+S+(process.argv[2]||'cyber-desk.html'));
const keys=await p.evaluate(()=>[...document.querySelectorAll('#nav a')].map(a=>a.dataset.k));
const bad=[];
for(const k of keys){await p.evaluate(k=>{location.hash=k},k);await p.waitForTimeout(40);const r=await p.evaluate(k=>{const pg=document.getElementById('p-'+k);return {vis:pg&&!pg.hidden,len:pg?pg.innerText.length:0,o:document.documentElement.scrollWidth-window.innerWidth}},k);if(!r.vis||r.len<80||r.o>0)bad.push([k,r]);}
console.log(w,'pages',keys.length,'bad',JSON.stringify(bad));
console.log('errors',errs);await p.close();}
await b.close();})();