const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();
for(const w of [390,1280]){const p=await b.newPage({viewport:{width:w,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+S+(process.argv[2]||'cyber-desk.html'));
const keys=await p.evaluate(()=>[...document.querySelectorAll('#nav a')].map(a=>a.dataset.k));
const bad=[];
for(const k of keys){await p.evaluate(k=>{location.hash=k},k);await p.waitForTimeout(40);const r=await p.evaluate(k=>{const pg=document.getElementById('p-'+k);return {vis:pg&&!pg.hidden,len:pg?pg.innerText.length:0,o:document.documentElement.scrollWidth-window.innerWidth}},k);if(!r.vis||r.len<80||r.o>0)bad.push([k,r]);}
console.log(w,'pages',keys.length,'bad',JSON.stringify(bad));
await p.evaluate(()=>{location.hash='register'});await p.waitForTimeout(50);await p.click('#p-register .filters button[data-f="health"]');console.log('health rows',await p.$$eval('#p-register tbody tr:not([hidden])',r=>r.length));
await p.evaluate(()=>{location.hash='ideas'});await p.waitForTimeout(50);await p.click('#p-ideas li[data-id="i5"] [data-s="push"]');console.log('idea pressed',await p.getAttribute('#p-ideas li[data-id="i5"] [data-s="push"]','aria-pressed'));
if(w===390){await p.click('#menu');}
await p.fill('#q','Monica');await p.waitForTimeout(400);console.log('results',await p.$$eval('#p-search .results a',a=>a.length));
await p.click('#p-search .results a');await p.waitForTimeout(100);console.log('marks',await p.$$eval('mark[data-hl]',m=>m.length));
await p.evaluate(()=>{location.hash='rehearse'});await p.waitForTimeout(50);await p.click('#reveal');await p.click('[data-r="script"]');
if(w===390){await p.evaluate(()=>{location.hash='home'});await p.waitForTimeout(50);await p.screenshot({path:S+'app-home-m.png'});await p.click('#menu');await p.waitForTimeout(300);await p.screenshot({path:S+'app-menu-m.png'});}
else {await p.evaluate(()=>{location.hash='now'});await p.waitForTimeout(50);await p.screenshot({path:S+'app-now-d.png'});}
console.log('errors',errs);await p.close();}
await b.close();})();
