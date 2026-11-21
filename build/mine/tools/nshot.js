const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+S+'cyber-desk.html#news');await p.waitForTimeout(1500);console.log(await p.locator('#nw-state').innerText(),errs);
await p.locator('#p-news').screenshot({path:S+'news.png'});await b.close();})();
