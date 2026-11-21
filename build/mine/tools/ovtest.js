const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();
for(const [w,h] of [[1500,1200],[390,900]]){
const p=await b.newPage({viewport:{width:w,height:h}});
await p.goto('file://'+S+'cyber-desk.html#map');await p.waitForTimeout(1300);
await p.locator('#mp-wrap').scrollIntoViewIfNeeded();await p.waitForTimeout(400);
const r=await p.evaluate(()=>{
 const heads=[...document.querySelectorAll('#mp-mk .mp-m')].map(m=>{const pth=m.querySelector('path').getBoundingClientRect();
   const rad=pth.width/2;return {x:pth.left+pth.width/2,y:pth.top+rad,r:rad,i:m.dataset.i};});
 const cls=[...document.querySelectorAll('#mp-mk .mp-cl circle')].map(c=>{const b=c.getBoundingClientRect();return {x:b.left+b.width/2,y:b.top+b.height/2,r:b.width/2,i:'cl'};});
 const all=heads.concat(cls);let bad=[];
 for(let i=0;i<all.length;i++)for(let j=i+1;j<all.length;j++){const a=all[i],q=all[j];const d=Math.hypot(a.x-q.x,a.y-q.y);
   if(d<(a.r+q.r)*0.85)bad.push([a.i,q.i,Math.round(d),Math.round(a.r+q.r)]);}
 return {marks:all.length,headR:heads.length?Math.round(heads[0].r*10)/10:0,visiblyOverlapping:bad.length,examples:bad.slice(0,6)};});
console.log(w,JSON.stringify(r));await p.close();}
await b.close();})();
