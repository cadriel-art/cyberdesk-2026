// UX round 3 menu test: 7 groups as headings, collapse by click, keyboard, current group open, routes unchanged.
const { chromium } = require('playwright');
const F='file:///home/user/cyberdesk-2026/build/mine/cyber-desk-offline.html';
let fails=0;const ok=(c,m)=>{console.log((c?'PASS ':'FAIL ')+m);if(!c)fails++;};
(async()=>{const b=await chromium.launch();
for(const [w,h] of [[1280,900],[390,844]]){
 const ctx=await b.newContext({viewport:{width:w,height:h},isMobile:w<600,hasTouch:w<600});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto(F+'#home');await p.waitForTimeout(800);
 if(w<600){await p.click('#menu');await p.waitForTimeout(300);}
 const g=await p.evaluate(()=>[...document.querySelectorAll('#nav .nav-g')].map(x=>({h:x.querySelector('h2')&&x.querySelector('h2').textContent,lab:x.getAttribute('aria-labelledby'),role:x.getAttribute('role'),open:x.querySelector('button').getAttribute('aria-expanded'),n:x.querySelectorAll('a').length})));
 ok(g.length===7,`${w} 7 groups ${JSON.stringify(g.map(x=>x.h+':'+x.n))}`);
 ok(g.every(x=>x.h&&x.lab&&x.role==='group'),`${w} headings + aria groups`);
 ok(g[0].open==='true',`${w} current group open`);
 if(w>=1000)ok(g.every(x=>x.open==='true'),`${w} desktop: all open`); else ok(g.slice(1).every(x=>x.open==='false'),`${w} phone: others closed`);
 // toggle by click
 const btn=p.locator('#nav .nav-gb').nth(2);
 await btn.click();await p.waitForTimeout(100);
 const st1=await btn.getAttribute('aria-expanded');
 await btn.click();await p.waitForTimeout(100);
 const st2=await btn.getAttribute('aria-expanded');
 ok(st1!==st2,`${w} click toggles (${st1}->${st2})`);
 // keyboard
 await btn.focus();await p.keyboard.press('Enter');await p.waitForTimeout(100);
 const st3=await btn.getAttribute('aria-expanded');ok(st3===st1,`${w} Enter toggles`);
 await p.keyboard.press('Space');await p.waitForTimeout(100);
 ok((await btn.getAttribute('aria-expanded'))===st2,`${w} Space toggles`);
 // open every group and check each link goes to its route
 await p.evaluate(()=>document.querySelectorAll('#nav .nav-gb[aria-expanded=false]').forEach(b=>b.click()));
 const keys=await p.evaluate(()=>[...document.querySelectorAll('#nav a[data-k]')].map(a=>a.dataset.k));
 ok(keys.length===59,`${w} 59 menu links (${keys.length})`);
 // old routes still work
 const old=['now','freezers','year','back','register','numbers','tools','powers','reg2','months','eucountries','map','evidence','outages','energy','water','watereu','transport','transporteu','health','healtheu','failures','good','laws','encryption','encryptioneu','files','gaps','props','ideas','who','victims','insurance','skills','citizens','prepare','ai','agents','cloud','quantum','hybrid','hybrideu','elections','electionseu','defence','defenceeu','schools','cables','more','printsel','glossary','sources','updates','news','intel','trend','cases','qa','home'];
 let bad=[];for(const k of old){await p.evaluate(k=>{location.hash='#'+k},k);await p.waitForTimeout(60);const r=await p.evaluate(()=>{const a=document.querySelector('#pages > article.page:not([hidden])');return a&&a.id});if(r!=='p-'+k)bad.push(k+'->'+r);}
 ok(bad.length===0,`${w} all old #keys route ${bad}`);
 // navigating opens the group of the target
 await p.evaluate(()=>location.hash='#qa');await p.waitForTimeout(300);
 const cur=await p.evaluate(()=>{const a=document.querySelector('#nav a[aria-current=page]');return a&&a.closest('.nav-g').querySelector('button').getAttribute('aria-expanded')});
 ok(cur==='true',`${w} group of current page open after route`);
 ok(errs.length===0,`${w} no errors ${errs}`);
 await ctx.close();}
console.log('FAILS',fails);await b.close();process.exit(fails?1:0);})();
