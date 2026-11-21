const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();
for(const w of [1400,390]){const p=await b.newPage({viewport:{width:w,height:1100},deviceScaleFactor:2});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+S+'cyber-desk.html#map');await p.waitForTimeout(1500);
console.log(w,await p.evaluate(()=>({pins:document.querySelectorAll('.mp-m').length,cl:document.querySelectorAll('.mp-cl').length,badge:document.querySelectorAll('.mp-b').length,cnt:document.querySelector('#mp-count').textContent,o:document.documentElement.scrollWidth-window.innerWidth})),errs);
await p.locator('#mp').screenshot({path:S+'map-'+w+'.png'});
if(w===1400){await p.click('[data-story="freezer"]');await p.waitForTimeout(500);await p.locator('#mp').screenshot({path:S+'map-story.png'});
 await p.click('[data-story="reset"]');await p.waitForTimeout(400);await p.click('[data-v="tot"]');await p.waitForTimeout(400);await p.locator('#mp-svg').screenshot({path:S+'map-tot.png'});console.log('errs',errs);}
await p.close();}
await b.close();})();
