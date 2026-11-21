const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();
for(const [w,h,name,scheme] of [[1280,900,'prep-layer-1280','light'],[390,844,'prep-layer-390','light'],[1280,900,'prep-layer-1280-dark','dark']]){
 const p=await b.newPage({viewport:{width:w,height:h},colorScheme:scheme});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file://'+S+'cyber-desk-offline.html#map');await p.waitForTimeout(1500);
 await p.evaluate(()=>document.querySelector('#mp-wrap').scrollIntoView());
 const before=await p.textContent('#mp-count');
 if(w<700)await p.evaluate(()=>{document.querySelector('#mp-lays').open=true});
 await p.click('.mp-chip[data-prep="1"]');await p.waitForTimeout(500);
 await p.evaluate(()=>document.querySelector('#mp-wrap').scrollIntoView());
 console.log(w,scheme,before,'|',await p.textContent('#mp-count'),await p.evaluate(()=>({labels:document.querySelectorAll('.mp-pl').length,pr:document.querySelector('.mp-chip[data-prep]').getAttribute('aria-pressed'),fills:[...document.querySelectorAll('.mp-cov path')].slice(0,3).map(x=>x.style.fill)})),errs);
 await p.locator('#mp').screenshot({path:S+name+(name.includes('dark')?'':'-full')+'.png'});
 await p.locator('#mp-wrap').screenshot({path:S+name+'.png'});
 await p.close();}
await b.close();})();
