const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:1100},deviceScaleFactor:2});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+S+'cyber-desk.html#map');await p.waitForTimeout(1200);
await p.locator('#mp').screenshot({path:S+'z0.png'});
for(let i=0;i<4;i++){await p.click('.mp-zoom [data-z=in]');await p.waitForTimeout(150);}
await p.locator('#mp-svg').screenshot({path:S+'z1.png'});
console.log('labels',await p.evaluate(()=>[...document.querySelectorAll('#mp-lbl text')].slice(0,6).map(t=>t.textContent+':'+t.getAttribute('font-size'))),errs);
await p.click('#mp-tall');await p.waitForTimeout(300);
console.log('tall h',await p.evaluate(()=>document.querySelector('#mp-svg').getBoundingClientRect().height));
await b.close();})();
