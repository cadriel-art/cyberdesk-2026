const { chromium } = require('playwright');
const O='/tmp/claude-0/-home-user-cyberdesk-2026/f8cf100d-5e4d-5da9-85e8-2780be2a451a/scratchpad/r2/';
const S='file:///home/user/cyberdesk-2026/build/mine/cyber-desk-offline.html';
(async()=>{const b=await chromium.launch();
const jobs=JSON.parse(process.argv[2]); // [{hash,w,h,lang,scheme,name,full,action}]
for(const j of jobs){
 const ctx=await b.newContext({viewport:{width:j.w,height:j.h},colorScheme:j.scheme||'light',isMobile:j.w<600,deviceScaleFactor:1});
 const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(l=>{try{localStorage.setItem('cyberdesk2:lang',JSON.stringify(l))}catch(e){}},j.lang||'en');
 await p.goto(S+'#'+j.hash); await p.waitForTimeout(1200);
 if(j.js) await p.evaluate(j.js);
 await p.waitForTimeout(500);
 await p.screenshot({path:O+j.name+'.png',fullPage:!!j.full});
 if(errs.length)console.log(j.name,'ERR',errs);
 await ctx.close();}
await b.close();})();
