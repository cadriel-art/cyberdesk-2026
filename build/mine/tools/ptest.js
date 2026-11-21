const { chromium } = require('playwright');
const F='file:///home/user/cyberdesk-2026/build/mine/cyber-desk-offline.html';
const O='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{window.__printed=0;window.print=()=>{window.__printed++;};});
// 1 page print with filter
await p.goto(F+'#reg2');await p.waitForTimeout(400);
await p.selectOption('#reg2f select[data-k="c"]','Poland');
await p.click('#p-reg2 .printbar .printbtn');await p.waitForTimeout(100);
console.log('printed calls',await p.evaluate(()=>window.__printed),'| head:',await p.textContent('#printhead'));
await p.emulateMedia({media:'print'});
await p.pdf({path:O+'t-reg.pdf',format:'A4'});
console.log('side visible in print:',await p.isVisible('#side'),'| rows visible:',await p.locator('#reg2t tbody tr:visible').count());
await p.screenshot({path:O+'t-reg.png',fullPage:false});
await p.emulateMedia({media:'screen'});
// 2 single country
await p.goto(F+'#eucountries');await p.waitForTimeout(400);
await p.click('#c-Latvia .printbtn');await p.waitForTimeout(100);
console.log('head:',await p.textContent('#printhead'),'| solo class:',await p.evaluate(()=>document.body.classList.contains('print-solo')));
await p.emulateMedia({media:'print'});
console.log('countries visible in solo print:',await p.locator('.countries .country:visible').count());
await p.pdf({path:O+'t-latvia.pdf',format:'A4'});
await p.screenshot({path:O+'t-latvia.png'});
// 3 qa page: details opened
await p.emulateMedia({media:'screen'});
await p.evaluate(()=>{document.body.classList.remove('print-solo')});
await p.goto(F+'#qa');await p.waitForTimeout(300);
await p.click('#p-qa .printbar .printbtn');
console.log('qa details open:',await p.locator('#p-qa details[open]').count(),'of',await p.locator('#p-qa details').count());
await p.emulateMedia({media:'print'});await p.pdf({path:O+'t-qa.pdf',format:'A4'});
// 390 width overflow with button
await p.emulateMedia({media:'screen'});await p.setViewportSize({width:390,height:800});await p.goto(F+'#eucountries');await p.waitForTimeout(300);
console.log('overflow 390:',await p.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth));
console.log('errors',errs);await b.close();})();
