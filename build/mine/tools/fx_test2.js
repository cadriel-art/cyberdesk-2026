const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();
async function open(w,h,extra){const c=await b.newContext(Object.assign({viewport:{width:w,height:h}},extra||{}));const p=await c.newPage();p.errs=[];p.on('pageerror',e=>p.errs.push(e.message));
 await p.goto('file://'+S+'cyber-desk.html#map');await p.waitForTimeout(1300);await p.locator('#mp-wrap').scrollIntoViewIfNeeded();await p.waitForTimeout(400);return p;}
let p=await open(1500,1000);
await p.selectOption('#mp-tm','one');await p.click('.mp-bar[data-c]');await p.waitForTimeout(200);
const m0=await p.evaluate(()=>document.querySelector('#mp-drawer .mp-meta').textContent);
await p.click('#mp-play');await p.waitForTimeout(2000);
const m1=await p.evaluate(()=>{const e=document.querySelector('#mp-drawer .mp-meta');return e&&e.textContent});
console.log('I5 card meta before/after ticks:',m0,'|',m1);await p.click('#mp-play');await p.close();
// visuals
for(const [w,h,cs] of [[1500,1100,'light'],[1500,1100,'dark'],[390,844,'light']]){
 p=await open(w,h,{colorScheme:cs});
 const info=await p.evaluate(()=>{const t=[...document.querySelectorAll('#mp-lbl text')];const sc=document.querySelector('#mp-svg');const r=sc.getBoundingClientRect(),vb=sc.viewBox.baseVal;const k=Math.min(r.width/vb.width,r.height/vb.height);
 return {labels:t.length,minFontPx:Math.min(...t.map(x=>+x.getAttribute('font-size')*k)).toFixed(1),sea:[...document.querySelectorAll('#mp-sealbl text')].map(x=>x.textContent)}});
 console.log(w,cs,JSON.stringify(info));
 await p.locator('#mp-svg').screenshot({path:S+'tools/fx_map_'+w+cs+'.png'});
 if(w===1500&&cs==='light'){ // zoom to Benelux-ish: click zoom in thrice
  for(let i=0;i<3;i++){await p.click('[data-z="in"]');await p.waitForTimeout(200);}
  await p.locator('#mp-svg').screenshot({path:S+'tools/fx_zoom.png'});
  await p.selectOption('#mp-mode','lv');await p.waitForTimeout(300);await p.locator('#mp-svg').screenshot({path:S+'tools/fx_lv.png'});}
 console.log('errs',p.errs);await p.close();}
await b.close();})();
