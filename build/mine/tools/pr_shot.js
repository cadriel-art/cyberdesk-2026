const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();
for(const w of [390,1280]){const p=await b.newPage({viewport:{width:w,height:900}});
await p.goto('file://'+S+'cyber-desk-offline.html#prepare');await p.waitForTimeout(800);
const r=await p.evaluate(()=>{const pg=document.getElementById('p-prepare');const o=document.documentElement.scrollWidth-window.innerWidth;
 let wide=[];pg.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();if(r.right>window.innerWidth+1&&r.width>0)wide.push(e.tagName+'.'+e.className+':'+Math.round(r.right))});
 return {o,vis:!pg.hidden,wide:wide.slice(0,8),sub:pg.querySelector('.sub').innerText,count:document.getElementById('pr-count').innerText}});
console.log(w,JSON.stringify(r));
await p.screenshot({path:S+'prepare-'+w+'.png',fullPage:true});await p.close();}
await b.close();})();
