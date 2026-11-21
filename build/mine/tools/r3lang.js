// UX round 3 language test: switching, H1/title/crumb, search in both languages, print modes.
const { chromium } = require('playwright');
const F='file:///home/user/cyberdesk-2026/build/mine/cyber-desk-offline.html';
let fails=0;const ok=(c,m)=>{console.log((c?'PASS ':'FAIL ')+m);if(!c)fails++;};
(async()=>{const b=await chromium.launch();
const ctx=await b.newContext({viewport:{width:1280,height:900}});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto(F+'#register');await p.waitForTimeout(900);
const st=()=>p.evaluate(()=>{const pg=document.querySelector('#pages > article.page:not([hidden])');const vis=e=>getComputedStyle(e).display!=='none';
 return {h1:pg.querySelector('h1').textContent,title:document.title,crumb:pg.querySelector('.crumb').textContent,lang:document.documentElement.lang,
  nlv:[...pg.querySelectorAll('.nl-x')].filter(vis).length,env:[...pg.querySelectorAll('.en-x')].filter(vis).length,mt:document.querySelector('#mtitle').textContent}});
let s=await st();console.log(JSON.stringify(s));
ok(s.lang==='en'&&s.h1==='All attacks on Belgium since 2023'&&s.nlv===0&&s.env>0,'EN: English H1, no Dutch visible');
ok(s.crumb==='Belgium'&&s.title.startsWith('All attacks on Belgium'),'EN crumb and title');
await p.click('#l-nl');await p.waitForTimeout(500);s=await st();console.log(JSON.stringify(s));
ok(s.lang==='nl'&&s.h1==='Alle aanvallen op België sinds 2023'&&s.env===0&&s.nlv>0,'NL: Dutch H1, no English counterpart visible, Dutch visible');
ok(s.crumb==='België'&&s.title.startsWith('Alle aanvallen op België')&&s.mt==='Alle aanvallen op België sinds 2023','NL crumb, title, header title');
await p.click('#l-en');await p.waitForTimeout(500);s=await st();ok(s.lang==='en'&&s.nlv===0&&s.h1==='All attacks on Belgium since 2023','back to EN');
// search: both languages indexed, snippet in active language
await p.click('#l-nl');await p.waitForTimeout(300);
for(const [lang,q] of [['nl','vriezers'],['nl','freezers'],['en','vriezers'],['en','freezers']]){
  await p.click('#l-'+lang);await p.waitForTimeout(250);
  await p.fill('#q',q);await p.keyboard.press('Enter');await p.waitForTimeout(500);
  const r=await p.evaluate(()=>({n:document.querySelectorAll('#p-search .results a').length,sn:(document.querySelector('#p-search .results a span')||{}).textContent||''}));
  ok(r.n>0,`${lang} search "${q}" finds ${r.n} pages; snippet: ${r.sn.slice(0,70)}`);
  if(q==='freezers'&&lang==='nl')ok(!/^NL:/.test(r.sn),'no NL: glue in snippet');
}
// print modes on a bilingual page
await p.goto(F+'#eucountries');await p.waitForTimeout(600);
const cnt=async cls=>{await p.evaluate(c=>{document.body.classList.remove('pl-en','pl-nl','pl-both','print-multi');if(c)document.body.classList.add('print-multi',c)},cls);await p.waitForTimeout(100);
 return p.evaluate(()=>{const pg=document.querySelector('#p-eucountries');const vis=e=>getComputedStyle(e).display!=='none';return {nl:[...pg.querySelectorAll('.nl-x')].filter(vis).length,en:[...pg.querySelectorAll('.en-x')].filter(vis).length}})};
await p.click('#l-en');await p.waitForTimeout(300);
let c=await cnt('pl-en');ok(c.nl===0&&c.en>0,'print EN only in EN mode '+JSON.stringify(c));
c=await cnt('pl-both');ok(c.nl>0&&c.en>0,'print both '+JSON.stringify(c));
c=await cnt('pl-nl');ok(c.nl>0&&c.en===0,'print Dutch first (UI in EN) '+JSON.stringify(c));
await p.click('#l-nl');await p.waitForTimeout(300);
c=await cnt('pl-en');ok(c.nl===0&&c.en>0,'print EN only while UI is NL '+JSON.stringify(c));
c=await cnt('');ok(c.en===0&&c.nl>0,'print this page follows the screen (NL) '+JSON.stringify(c));
// print selection page offers the Dutch-first option and preselects it in NL
await p.evaluate(()=>document.body.classList.remove('pl-en','pl-nl','pl-both','print-multi'));
await p.goto(F+'#printsel');await p.waitForTimeout(600);
const ps=await p.evaluate(()=>({opts:[...document.querySelectorAll('input[name=ps-lang]')].map(i=>i.value),sel:(document.querySelector('input[name=ps-lang]:checked')||{}).value}));
ok(ps.opts.join()==='en,nl,both'&&ps.sel==='nl','print selection options '+JSON.stringify(ps));
ok(errs.length===0,'no errors '+errs);
console.log('FAILS',fails);await b.close();process.exit(fails?1:0);})();
