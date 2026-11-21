const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+S+'cyber-desk.html#intel');await p.waitForTimeout(800);await p.locator('#p-intel').screenshot({path:S+'intel.png'});
await p.goto('file://'+S+'cyber-desk.html#map');await p.waitForTimeout(1200);await p.selectOption('#mp-camp','freezer');await p.emulateMedia({media:'print'});await p.waitForTimeout(200);
console.log(await p.locator('#mp-printnote').innerText(),errs);await p.pdf({path:'/home/user/Print-sample-Map.pdf',format:'A4'});await b.close();})();
