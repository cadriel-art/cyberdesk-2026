const { chromium } = require('playwright');
const O='/tmp/claude-0/-home-user-cyberdesk-2026/f8cf100d-5e4d-5da9-85e8-2780be2a451a/scratchpad/r3/';
const F='file:///home/user/cyberdesk-2026/build/mine/cyber-desk-offline.html';
(async()=>{const b=await chromium.launch();
for(const [w,h] of [[1280,900],[390,844]])for(const lang of ['en','nl'])for(const scheme of ['light','dark']){
 const tag=`${w}-${lang}-${scheme}`;
 const ctx=await b.newContext({viewport:{width:w,height:h},colorScheme:scheme,isMobile:w<600,hasTouch:w<600});
 const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(l=>{try{localStorage.setItem('cyberdesk2:lang',JSON.stringify(l))}catch(e){}},lang);
 for(const k of ['home','now','qa','eucountries','updates']){
  await p.goto(F+'#'+k);await p.waitForTimeout(900);
  if(!(scheme==='dark'&&['qa','eucountries'].includes(k)&&w<600)) await p.screenshot({path:O+`${k}-${tag}.png`});
 }
 // menu
 await p.goto(F+'#now');await p.waitForTimeout(700);
 if(w<600){await p.click('#menu');await p.waitForTimeout(500);}
 await p.screenshot({path:O+`menu-${tag}.png`});
 if(errs.length)console.log(tag,errs);
 await ctx.close();}
await b.close();})();
