const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();
for(const w of [390,1280]){const p=await b.newPage({viewport:{width:w,height:w==390?900:1000}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+S+'cyber-desk-offline.html#outages');await p.waitForTimeout(500);
const r=await p.evaluate(()=>({sw:document.documentElement.scrollWidth,iw:innerWidth,cards:document.querySelectorAll('#p-outages .og-card').length,count:document.getElementById('og-count').textContent}));console.log(w,JSON.stringify(r),errs);
await p.screenshot({path:S+'outages-'+w+'.png',fullPage:false});
if(w==390){await p.evaluate(()=>{const c=document.querySelector('#p-outages .og-card');c.open=true;document.querySelectorAll('#p-outages .og-card')[26].open=true});
 await p.evaluate(()=>document.querySelector('#p-outages .og-card').scrollIntoView());await p.waitForTimeout(200);
 console.log('open overflow',await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth));await p.screenshot({path:S+'outages-390-open.png'});}
// filters
await p.selectOption('#ogf select[data-f=kind]','cyberattack');console.log('kind',await p.textContent('#og-count'));
await p.selectOption('#ogf select[data-f=kind]','');await p.fill('#og-q','cloudflare');console.log('q',await p.textContent('#og-count'));await p.fill('#og-q','');
await p.selectOption('#og-sort','old');console.log('first visible',await p.evaluate(()=>{const c=[...document.querySelectorAll('#og-list .og-card')].sort((a,b)=>a.style.order-b.style.order)[0];return c.querySelector('.og-d').textContent}));
await p.close();}
await b.close();})();
