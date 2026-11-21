const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1440,height:1000}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+S+'cyber-desk-offline.html#map');await p.waitForTimeout(1500);
console.log(await p.evaluate(()=>{const t=[...document.querySelectorAll('#mp-svg text')].map(x=>x.textContent);return ['Germany','France','Poland','Spain','Italy','Sweden','Norway','Finland','Romania'].map(n=>n+':'+t.includes(n)).join(' ')}),errs);
await p.locator('#mp-svg').screenshot({path:S+'map-labels-1440.png'});
// mouse click focus
const pin=p.locator('.mp-m').first();await pin.click({force:true});
console.log('outline',await p.evaluate(()=>{const a=document.activeElement;return a?getComputedStyle(a).outlineStyle+' '+a.className.baseVal:''}));
await b.close();})();
