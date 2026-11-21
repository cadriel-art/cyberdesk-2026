const { chromium } = require('playwright');
const F='file:///home/user/cyberdesk-2026/build/mine/cyber-desk-offline.html';
const EN=/\b(the|and|of|was|were|not|with|for|that|this|has|have|from|were|which|their|its|are|is|by|on)\b/i;
(async()=>{const b=await chromium.launch();const p=await (await b.newContext({viewport:{width:1280,height:900}})).newPage();
for(const pg of ['water','transport','health','hybrid','elections','defence','encryption']){
 await p.goto(F+'#'+pg);await p.waitForTimeout(700);await p.click('#l-nl');await p.waitForTimeout(500);
 const r=await p.evaluate((pg)=>{const a=document.querySelector('#p-'+pg);const out=[];
  const note=[...a.querySelectorAll('.bl-note')].filter(e=>getComputedStyle(e).display!=='none'&&e.offsetParent).map(e=>e.textContent);
  const w=document.createTreeWalker(a,NodeFilter.SHOW_TEXT);let n;
  while(n=w.nextNode()){const t=n.textContent.replace(/\s+/g,' ').trim();if(t.length<3)continue;let e=n.parentElement,vis=true;
   for(;e&&e!==a;e=e.parentElement){const cs=getComputedStyle(e);if(cs.display==='none'||cs.visibility==='hidden'){vis=false;break}if(e.closest&&0)break}
   if(vis&&!n.parentElement.closest('a,script,style'))out.push(t)}
  return {note,out}},pg);
 const bad=r.out.filter(t=>t.split(/\s+/).filter(w=>EN.test(w)).length>=2||/^[A-Z][a-z]+ [a-z]+ [a-z]+/.test(t)&&EN.test(t));
 console.log('==',pg,'note:',JSON.stringify(r.note),'visible nodes',r.out.length,'suspect',bad.length);bad.slice(0,40).forEach(t=>console.log('  ',t.slice(0,140)));}
await b.close()})();
