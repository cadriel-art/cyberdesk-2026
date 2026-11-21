const { chromium } = require('playwright');const fs=require('fs');
const EN=new Set(JSON.parse(fs.readFileSync(process.argv[2],'utf8')));
const F='file:///home/user/cyberdesk-2026/build/mine/cyber-desk-offline.html';
(async()=>{const b=await chromium.launch();const p=await (await b.newContext({viewport:{width:1280,height:900}})).newPage();
for(const pg of ['water','transport','health','hybrid','elections','defence','encryption']){
 await p.goto(F+'#'+pg);await p.waitForTimeout(600);await p.click('#l-nl');await p.waitForTimeout(400);
 const out=await p.evaluate((pg)=>{const a=document.querySelector('#p-'+pg);const out=[];const w=document.createTreeWalker(a,NodeFilter.SHOW_TEXT);let n;
  while(n=w.nextNode()){const t=n.textContent.replace(/\s+/g,' ').trim();if(t.length<3)continue;let e=n.parentElement,vis=true;
   for(;e&&e!==a;e=e.parentElement){const cs=getComputedStyle(e);if(cs.display==='none'||cs.visibility==='hidden'){vis=false;break}}
   if(vis)out.push(t)}return out},pg);
 const bad=out.filter(t=>EN.has(t));
 console.log('==',pg,out.length,bad.length,JSON.stringify(bad));
 const note=await p.evaluate(pg=>[...document.querySelectorAll('#p-'+pg+' .bl-note')].filter(e=>e.offsetParent).length,pg);console.log('  note visible:',note)}
await b.close()})();
