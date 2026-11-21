const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:1400}});
for(const k of ['intel','evidence','outages']){await p.goto('file://'+S+'cyber-desk.html#'+k);await p.waitForTimeout(700);await p.screenshot({path:S+'iv-'+k+'.png'});}
await b.close();})();
