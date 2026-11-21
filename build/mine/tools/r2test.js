const { chromium } = require('playwright');
const O='/tmp/claude-0/-home-user-cyberdesk-2026/f8cf100d-5e4d-5da9-85e8-2780be2a451a/scratchpad/r2/';
const S='file:///home/user/cyberdesk-2026/build/mine/cyber-desk-offline.html';
let fails=0; const ok=(c,m)=>{console.log((c?'PASS ':'FAIL ')+m); if(!c)fails++;};
(async()=>{const b=await chromium.launch();
for(const [w,h,lang,scheme] of [[390,844,'en','light'],[390,844,'nl','dark'],[1280,900,'en','light'],[1280,900,'nl','dark']]){
 const tag=`${w}-${lang}-${scheme}`;
 const ctx=await b.newContext({viewport:{width:w,height:h},colorScheme:scheme,isMobile:w<600,hasTouch:w<600});
 const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(l=>{try{localStorage.setItem('cyberdesk2:lang',JSON.stringify(l))}catch(e){}},lang);
 await p.goto(S+'#map'); await p.waitForTimeout(1200);
 // map first
 const r=await p.evaluate(()=>{const m=document.querySelector('#mp-svg').getBoundingClientRect();return {top:m.top,bot:m.bottom,h:m.height,ih:innerHeight}});
 ok(r.top<r.ih*0.6&&Math.min(r.bot,r.ih)-r.top>=r.ih*0.3,`${tag} map in first screen (top ${Math.round(r.top)}, visible ${Math.round(Math.min(r.bot,r.ih)-r.top)})`);
 // filters toggle
 await p.click('#mp-ftog'); await p.waitForTimeout(200);
 ok(await p.evaluate(()=>getComputedStyle(document.querySelector('#mp-mapcol .mp-row')).display!=='none'),`${tag} filters open`);
 if(w<600||true) await p.screenshot({path:O+`map-filters-${tag}.png`});
 await p.click('#mp-ftog'); await p.waitForTimeout(150);
 // legend
 await p.click('#mp-legjump'); await p.waitForTimeout(900);
 ok(await p.evaluate(()=>{const l=document.querySelector('#mp-legend').getBoundingClientRect();return l.top<innerHeight&&l.bottom>0}),`${tag} legend reachable`);
 await p.evaluate(()=>scrollTo(0,0)); await p.waitForTimeout(300);
 // select a pin
 await p.evaluate(()=>document.querySelector('#mp-svg').scrollIntoView({block:'start'}));await p.waitForTimeout(200);
 const pin=await p.evaluate(()=>{const ms=[...document.querySelectorAll('#mp-mk .mp-m')];for(const m of ms){const r=m.getBoundingClientRect();const sv=document.querySelector('#mp-svg').getBoundingClientRect();if(r.width>0&&r.left>sv.left+60&&r.right<sv.right-60&&r.top>sv.top+60&&r.bottom<sv.top+Math.min(sv.height,innerHeight*0.5)-10)return [r.left+r.width/2,r.top+r.height/2];}return null});
 console.log(tag,'pin',pin); if(pin) await p.mouse.click(pin[0],pin[1]); await p.waitForTimeout(600);
 const d=await p.evaluate(()=>{const e=document.querySelector('#mp-drawer');const cs=getComputedStyle(e);const r=e.getBoundingClientRect();const h4=e.querySelector('h4');const src=e.querySelector('.mp-src');const sr=src&&src.getBoundingClientRect();const svg=document.querySelector('#mp-svg').getBoundingClientRect();return {pos:cs.position,w:r.width,h:r.height,top:r.top,ih:innerHeight,iw:innerWidth,h4:h4?h4.getBoundingClientRect().height:0,lh:h4?parseFloat(getComputedStyle(h4).lineHeight):0,srcVis:sr?(sr.bottom<=innerHeight+1&&sr.top>=0):null,empty:!e.innerHTML.trim(),svgTop:svg.top}});
 console.log(tag,JSON.stringify(d));
 if(w<600){ ok(!d.empty&&d.pos==='fixed'&&d.w>=d.iw-1,`${tag} sheet fixed full width`); ok(d.h<=d.ih*0.46,`${tag} sheet <=45% (${Math.round(d.h/d.ih*100)}%)`); ok(d.srcVis!==false,`${tag} source link visible`); ok(d.h4<=d.lh*3.4+1,`${tag} headline <=3 lines`);}
 else ok(!d.empty&&d.pos!=='fixed',`${tag} desktop drawer not a sheet (${d.pos})`);
 await p.screenshot({path:O+`map-pin-${tag}.png`});
 // fullscreen-pattern (fsx) on phone
 // TOC
 await p.goto(S+'#evidence'); await p.waitForTimeout(1800);
 const t=await p.evaluate(()=>{const e=document.querySelector('#p-evidence .u-toc');return e?{n:e.querySelectorAll('a').length,txt:e.querySelector('summary').textContent}:null});
 ok(t&&t.n>=3,`${tag} TOC on evidence: ${JSON.stringify(t)}`);
 await p.click('#p-evidence .u-toc summary'); await p.waitForTimeout(200);
 await p.screenshot({path:O+`toc-${tag}.png`});
 await p.keyboard.press('Tab'); 
 const y0=await p.evaluate(()=>scrollY);
 await p.click('#p-evidence .u-toc a:nth-child(1) >> nth=2').catch(()=>{});
 await p.evaluate(()=>document.querySelectorAll('#p-evidence .u-toc a')[2].click()); await p.waitForTimeout(900);
 ok(await p.evaluate(()=>scrollY)>y0,`${tag} TOC link scrolls`);
 // back to top
 await p.evaluate(()=>scrollTo(0,0)); await p.waitForTimeout(300);
 ok(!(await p.evaluate(()=>document.querySelector('.u-btt').classList.contains('on'))),`${tag} btt hidden at top`);
 await p.evaluate(h=>scrollTo(0,h*2),h); await p.waitForTimeout(500);
 ok(await p.evaluate(()=>document.querySelector('.u-btt').classList.contains('on')),`${tag} btt shown after 2 screens`);
 const bt=await p.evaluate(()=>document.querySelector('.u-btt').getAttribute('aria-label'));
 ok(bt===(lang==='nl'?'Naar boven':'Back to top'),`${tag} btt label ${bt}`);
 await p.screenshot({path:O+`btt-${tag}.png`});
 await p.focus('.u-btt'); await p.keyboard.press('Enter'); await p.waitForTimeout(1200);
 ok(await p.evaluate(()=>scrollY)<5,`${tag} btt keyboard returns to top`);
 // no toc on short page & home
 await p.goto(S+'#home'); await p.waitForTimeout(800);
 ok(await p.evaluate(()=>!document.querySelector('.u-toc')),`${tag} no TOC on home`);
 ok(errs.length===0,`${tag} no page errors ${errs.join('|')}`);
 await ctx.close();}
console.log('FAILS',fails);await b.close();})();
