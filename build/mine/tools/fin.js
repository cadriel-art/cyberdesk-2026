const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:1000}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+S+'cyber-desk.html#map');await p.waitForTimeout(1500);
await p.locator('#mp-wrap').scrollIntoViewIfNeeded();await p.waitForTimeout(300);
const box=await p.locator('#mp-mk .mp-m').nth(5).boundingBox();await p.mouse.click(box.x+box.width/2,box.y+box.height*0.3);
await p.waitForTimeout(500);await p.locator('#mp-wrap').screenshot({path:S+'fin.png'});console.log('errors',errs);await b.close();})();
