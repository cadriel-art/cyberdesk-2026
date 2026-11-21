const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1500,height:1200}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+S+'cyber-desk.html#map');await p.waitForTimeout(1300);
await p.locator('#mp-wrap').scrollIntoViewIfNeeded();await p.waitForTimeout(500);
const res=await p.evaluate(()=>{let blocked=[],tot=0,off=0;
 document.querySelectorAll('#mp-mk .mp-m, #mp-mk .mp-cl').forEach(m=>{
  const r=m.getBoundingClientRect();const x=r.left+r.width/2,y=r.top+r.height*0.3;
  if(y<0||y>innerHeight||x<0||x>innerWidth){off++;return;}
  tot++;const st=document.elementsFromPoint(x,y);let hit=false;
  for(const e of st){if(e.closest&&e.closest('.mp-m,.mp-cl')){hit=true;break;}if(e.closest&&e.closest('.mp-b'))break;}
  if(!hit)blocked.push((m.dataset.i||m.dataset.cl||'?'));});
 return {tested:tot,offscreen:off,blocked:blocked.length,which:blocked.slice(0,8)};});
console.log(JSON.stringify(res));
// a real click on the biggest cluster, which sits under the Belgium count
const cl=await p.evaluate(()=>{const c=document.querySelector('#mp-mk .mp-cl');const r=c.getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2,n:c.dataset.cl.split(',').length};});
await p.mouse.click(cl.x,cl.y);await p.waitForTimeout(500);
console.log('cluster of',cl.n,'-> card:',(await p.locator('#mp-card').innerText()).split('\n').slice(0,2).join(' | '));
console.log('errors',errs);await b.close();})();
