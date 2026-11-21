const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});const e=[];p.on('pageerror',x=>e.push(x.message));
await p.goto('file:///home/user/cyberdesk-2026/build/mine/cyber-desk-offline.html#water');await p.waitForTimeout(500);
await p.screenshot({path:'../h.png',fullPage:true});
await p.setViewportSize({width:390,height:800});await p.waitForTimeout(200);console.log('ovf',await p.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth),e);await b.close();})();
