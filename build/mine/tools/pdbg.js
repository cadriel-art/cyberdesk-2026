const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
p.on('pageerror',e=>console.log('PAGEERR',e.message));p.on('console',m=>{if(m.type()==='error')console.log('CONSOLE',m.text())});
await p.goto('file:///home/user/cyberdesk-2026/build/mine/cyber-desk-offline.html#reg2');await p.waitForTimeout(600);
console.log(await p.evaluate(()=>({bar:!!document.querySelector('#p-reg2 .printbar'),fn:typeof addPrint,first:document.querySelector('#p-reg2').firstElementChild.className,vis:getComputedStyle(document.querySelector('#p-reg2 .printbar')||document.body).display})));
await b.close();})();
