const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();const e=[];p.on('pageerror',x=>e.push(x.message));
await p.goto('file:///home/user/cyberdesk-2026/build/mine/cyber-desk-offline.html#ideas');await p.waitForTimeout(1500);
console.log(await p.evaluate(()=>[document.querySelectorAll('#p-ideas ol.ideas li').length,document.querySelectorAll('#p-ideas li[data-id]').length,document.querySelectorAll('#p-ideas li .n').length]),e);await b.close();})();
