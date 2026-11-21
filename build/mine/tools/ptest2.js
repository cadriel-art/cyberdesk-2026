const { chromium } = require('playwright');
const F='file:///home/user/cyberdesk-2026/build/mine/cyber-desk-offline.html';
const O='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:1000}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{window.__printed=0;window.print=()=>{window.__printed++;};});
await p.goto(F+'#printsel');await p.waitForTimeout(500);
console.log('page boxes',await p.locator('#ps-pages input[data-pg]').count(),'countries',await p.locator('#ps-countries input').count());
await p.screenshot({path:O+'t-sel.png',fullPage:true});
// preset short
await p.click('#ps-presets button[data-set="short"]');
console.log('summary:',await p.textContent('#ps-summary'));
await p.click('#ps-go');await p.waitForTimeout(150);
console.log('printed',await p.evaluate(()=>window.__printed),'classes',await p.evaluate(()=>document.body.className));
await p.emulateMedia({media:'print'});
console.log('visible pages in print:',await p.evaluate(()=>[...document.querySelectorAll('#pages > .page')].filter(x=>getComputedStyle(x).display!=='none').map(x=>x.id)));
console.log('NL hidden:',await p.evaluate(()=>getComputedStyle(document.querySelector('#p-qa p.nl')).display),'terms hidden:',await p.evaluate(()=>{const t=document.querySelector('#p-trend .termsbox');return t?getComputedStyle(t).display:'none-el'}));
await p.pdf({path:O+'t-short.pdf',format:'A4'});
await p.emulateMedia({media:'screen'});
// countries only: Belgium, France, Poland, both languages, colour
await p.reload();await p.waitForTimeout(500);
for(const id of ['c-Belgium','c-France','c-Poland']) await p.check('#ps-countries input[data-ct="'+id+'"]');
await p.check('input[name="ps-lang"][value="both"]');
console.log('summary:',await p.textContent('#ps-summary'));
await p.click('#ps-go');await p.waitForTimeout(150);
await p.emulateMedia({media:'print'});
console.log('countries visible:',await p.locator('#p-eucountries .country:visible').count());
await p.pdf({path:O+'t-3countries.pdf',format:'A4'});
// whole file estimate
await p.emulateMedia({media:'screen'});await p.reload();await p.waitForTimeout(500);
await p.click('#ps-presets button[data-set="all"]');console.log('all summary:',await p.textContent('#ps-summary'));
await p.click('#ps-go');await p.emulateMedia({media:'print'});await p.pdf({path:O+'t-all.pdf',format:'A4'});
await p.emulateMedia({media:'screen'});await p.setViewportSize({width:390,height:800});await p.goto(F+'#printsel');await p.waitForTimeout(400);
console.log('overflow 390:',await p.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth));
console.log('errors',errs);await b.close();})();
