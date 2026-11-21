const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();
async function open(w,h,extra){const c=await b.newContext(Object.assign({viewport:{width:w,height:h}},extra||{}));const p=await c.newPage();p.errs=[];p.on('pageerror',e=>p.errs.push(e.message));
 await p.goto('file://'+S+'cyber-desk.html#map');await p.waitForTimeout(1300);await p.locator('#mp-wrap').scrollIntoViewIfNeeded();await p.waitForTimeout(400);return p;}
// P1 dark print
let p=await open(1500,1200,{colorScheme:'dark'});
const dk=await p.evaluate(()=>getComputedStyle(document.querySelector('#mp')).getPropertyValue('--mp-sea').trim());
await p.emulateMedia({media:'print'});await p.evaluate(()=>window.dispatchEvent(new Event('beforeprint')));await p.waitForTimeout(300);
const pr=await p.evaluate(()=>{const cs=getComputedStyle(document.querySelector('#mp'));
 const pin=document.querySelector('#mp-mk .mp-m path');
 return {sea:cs.getPropertyValue('--mp-sea').trim(),land:cs.getPropertyValue('--mp-land').trim(),seaFill:getComputedStyle(document.querySelector('.mp-sea')).fill,landFill:getComputedStyle(document.querySelector('.mp-cov path')).fill,
  details:[...document.querySelectorAll('details')].filter(d=>!d.open).length,list:document.querySelectorAll('#mp-list .mp-li').length,listH:document.querySelector('#mp-list').getBoundingClientRect().height,
  pbVisible:[...document.querySelectorAll('details.plainbox')].filter(d=>d.querySelector('.pb-body').getBoundingClientRect().height>0).length,pbTotal:document.querySelectorAll('details.plainbox').length};});
console.log('P1 dark screen sea',dk,'| print',JSON.stringify(pr));
await p.screenshot({path:S+'tools/fx_p1.png',clip:{x:0,y:0,width:1500,height:1200}}).catch(()=>{});
await p.evaluate(()=>window.dispatchEvent(new Event('afterprint')));
console.log('P2 after afterprint closed details:',await p.evaluate(()=>[...document.querySelectorAll('details')].filter(d=>!d.open).length),'printing class',await p.evaluate(()=>document.querySelector('#mp').classList.contains('mp-printing')));
await p.close();
// I1 fullscreen CSS emulate via class mp-fsx
p=await open(1100,900);
await p.click('#mp-wrap [data-z]:not([data-z])').catch(()=>{});
await p.evaluate(()=>document.querySelector('#mp-mapcol').classList.add('mp-fsx'));
await p.locator('.mp-m').first().click({force:true});await p.waitForTimeout(300);
console.log('I1 (fsx class emulation) drawer display',await p.evaluate(()=>{const d=document.querySelector('#mp-drawer');return [getComputedStyle(d).display,getComputedStyle(d).position,d.textContent.length,getComputedStyle(document.querySelector('#mp-mapcol')).paddingTop]}));
// real fullscreen attempt
const fs=await p.evaluate(async()=>{try{await document.querySelector('#mp-mapcol').requestFullscreen();await new Promise(r=>setTimeout(r,400));return [!!document.fullscreenElement,document.querySelector('#mp-mapcol').matches(':fullscreen'),getComputedStyle(document.querySelector('#mp-drawer')).display,getComputedStyle(document.querySelector('#mp-svg')).maxHeight,getComputedStyle(document.querySelector('#mp-mapcol')).backgroundColor]}catch(e){return 'err '+e.message}});
console.log('I1 real fullscreen',JSON.stringify(fs));
await p.close();
// I4 live region
p=await open(1500,1000);
console.log('I4 wide(tall auto):',await p.evaluate(()=>['#mp-drawer','#mp-card'].map(s=>{const e=document.querySelector(s);return s+':'+e.getAttribute('role')+'/'+e.getAttribute('aria-live')+'/'+getComputedStyle(e).display})),'tall',await p.evaluate(()=>document.querySelector('#mp').classList.contains('tall')));
await p.click('#mp-tall');await p.waitForTimeout(300);
console.log('I4 after untall:',await p.evaluate(()=>['#mp-drawer','#mp-card'].map(s=>{const e=document.querySelector(s);return s+':'+e.getAttribute('role')+'/'+e.getAttribute('aria-live')})));
await p.click('#mp-tall');await p.waitForTimeout(300);
// V5
const svgw=await p.evaluate(()=>document.querySelector('#mp-svg').getBoundingClientRect().width);console.log('V5 svg width at 1500 (tall default):',svgw);
await p.close();
p=await open(1280,900);console.log('V5 svg width at 1280:',await p.evaluate(()=>document.querySelector('#mp-svg').getBoundingClientRect().width),'errs',p.errs);await p.close();
// I5 play card refresh, I6, I3, I2
p=await open(1500,1000);
await p.locator('.mp-m').first().click({force:true});await p.waitForTimeout(200);
console.log('I3 selected',await p.evaluate(()=>document.querySelector('#mp-drawer').textContent.length>0));
await p.evaluate(()=>document.activeElement&&document.activeElement.blur());await p.focus('#mp-zoom,.mp-zoom button').catch(()=>{});
await p.focus('#mp-play');await p.keyboard.press('Escape');await p.waitForTimeout(200);
console.log('I3 after Esc with focus on play button: drawer empty',await p.evaluate(()=>document.querySelector('#mp-drawer').textContent.length===0));
// I6
await p.selectOption('#mp-camp','freezer');await p.waitForTimeout(200);
await p.click('.mp-chip[data-all="0"]');await p.click('.mp-chip[data-k="drones"]');await p.selectOption('#mp-camp','');await p.waitForTimeout(200);
console.log('I6 on after deselect (expect only drones pressed):',await p.evaluate(()=>[...document.querySelectorAll('.mp-chip[data-k][aria-pressed="true"]')].map(c=>c.dataset.k)));
// I5
await p.click('.mp-sbtn[data-story="reset"]');await p.click('#mp-play');await p.waitForTimeout(300);
const n0=await p.evaluate(()=>document.querySelector('#mp-tl').textContent);
await p.click('#mp-play');
console.log('I5 (play started) t label',n0);
await p.close();
// I2 cluster focus
p=await open(1500,1000);
const cl=await p.evaluate(()=>{const c=document.querySelector('#mp-mk .mp-cl');return c?c.dataset.cl:null});console.log('cluster present',!!cl);
if(cl){await p.focus('#mp-mk .mp-cl');await p.keyboard.press('Enter');await p.waitForTimeout(300);
 console.log('I2 focus after Enter:',await p.evaluate(()=>{const a=document.activeElement;return a&&a.getAttribute&&(a.getAttribute('class')+' '+(a.getAttribute('aria-label')||'').slice(0,40))}));}
await p.close();
await b.close();})();
