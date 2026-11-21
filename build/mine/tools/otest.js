const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();
for(const [w,h] of [[1500,1200],[390,900]]){
const p=await b.newPage({viewport:{width:w,height:h}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+S+'cyber-desk.html#map');await p.waitForTimeout(1300);
await p.locator('#mp-wrap').scrollIntoViewIfNeeded();await p.waitForTimeout(400);
const r=await p.evaluate(()=>{const heads=[...document.querySelectorAll('#mp-mk .mp-m')].map(m=>{const c=m.querySelector('.hit').getBoundingClientRect();return [c.left+c.width/2,c.top+c.height/2,c.width/2];});
 let ov=0;for(let i=0;i<heads.length;i++)for(let j=i+1;j<heads.length;j++){const a=heads[i],b=heads[j];if(Math.hypot(a[0]-b[0],a[1]-b[1])<(a[2]+b[2])*0.62)ov++;}
 const tab=[...document.querySelectorAll('#mp-svg [tabindex="0"]')].length;
 return {pins:heads.length,overlappingPairs:ov,tabStopsInMap:tab,labels:document.querySelectorAll('#mp-lbl text').length};});
console.log(w,JSON.stringify(r),errs);
if(w===1500){
 // arrow keys move between marks
 await p.focus('#mp-svg [tabindex="0"]');const k0=await p.evaluate(()=>document.activeElement.getAttribute('aria-label'));
 await p.keyboard.press('ArrowRight');const k1=await p.evaluate(()=>document.activeElement.getAttribute('aria-label'));
 console.log('arrow moves focus:',k0!==k1,'|',(k1||'').slice(0,50));
 // double-click zoom
 const vb0=await p.getAttribute('#mp-svg','viewBox');const bx=await p.locator('#mp-svg').boundingBox();
 await p.mouse.dblclick(bx.x+bx.width*0.45,bx.y+bx.height*0.55);await p.waitForTimeout(400);
 console.log('dblclick zoom:',vb0,'->',await p.getAttribute('#mp-svg','viewBox'));
 // series origin with time filter hiding the first entry
 await p.click('[data-story="reset"]');await p.selectOption('#mp-camp','freezer');
 await p.evaluate(()=>{const s=document.querySelector('#mp-t');s.value=22;s.dispatchEvent(new Event('input',{bubbles:true}));const m=document.querySelector('#mp-tm');m.value='one';m.dispatchEvent(new Event('change',{bubbles:true}));});
 await p.waitForTimeout(400);
 console.log('ghost origin:',await p.evaluate(()=>document.querySelectorAll('#mp-lines circle.ghost').length),'| note:',(await p.locator('#mp-campnote').innerText()).slice(0,140));
}
await p.close();}
await b.close();})();
