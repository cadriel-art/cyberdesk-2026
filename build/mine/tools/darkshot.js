const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:1000},colorScheme:'dark',deviceScaleFactor:1});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+S+'cyber-desk.html#map');await p.waitForTimeout(1200);
await p.locator('#mp-svg').screenshot({path:S+'dark.png'});console.log('dark ok',errs);
await p.click('[data-v="tot"]');await p.waitForTimeout(400);await p.locator('#mp-svg').screenshot({path:S+'dark-tot.png'});
await b.close();})();
