const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:1050},deviceScaleFactor:2});
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+S+'cyber-desk.html#map');await p.waitForTimeout(1500);
await p.locator('#mp').screenshot({path:S+'v1.png'});
// reset after a time filter
await p.evaluate(()=>{document.querySelector('#mp-t').value=5;document.querySelector('#mp-t').dispatchEvent(new Event('input',{bubbles:true}))});
await p.waitForTimeout(200);await p.click('[data-story="freezer"]');await p.waitForTimeout(400);
console.log('story after time filter:',await p.locator('#mp-count').innerText());
await p.click('[data-story="reset"]');await p.waitForTimeout(400);
console.log('after reset:',await p.locator('#mp-count').innerText(),await p.locator('#mp-tl').innerText());
// shading toggle + proof mode legend
await p.check('#mp-shade');await p.waitForTimeout(300);await p.locator('#mp-svg').screenshot({path:S+'v-shade.png'});
await p.uncheck('#mp-shade');await p.selectOption('#mp-mode','lv');await p.waitForTimeout(300);
await p.locator('#mp').screenshot({path:S+'v-proof.png'});
await p.selectOption('#mp-mode','lay');await p.waitForTimeout(200);
// drawer in wide view
await p.click('#mp-tall');await p.waitForTimeout(400);
const box=await p.locator('#mp-mk .mp-m').first().boundingBox();await p.mouse.click(box.x+box.width/2,box.y+box.height/2);
await p.waitForTimeout(400);
console.log('drawer visible:',await p.evaluate(()=>{const d=document.querySelector('#mp-drawer');const r=d.getBoundingClientRect();return {w:Math.round(r.width),vis:getComputedStyle(d).display}}));
await p.locator('#mp').screenshot({path:S+'v-drawer.png'});
console.log('errors',errs);
// plainbox folding across the app
await p.goto('file://'+S+'cyber-desk.html#now');await p.waitForTimeout(900);
console.log('folded boxes:',await p.evaluate(()=>({det:document.querySelectorAll('details.plainbox').length,div:document.querySelectorAll('div.plainbox').length,open:document.querySelectorAll('details.plainbox[open]').length})));
await b.close();})();
