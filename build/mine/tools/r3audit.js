// UX round 3 audit: in NL mode, visible English-looking text that sits next to visible Dutch text (missed pairs),
// and how much of each page is Dutch / English.
const { chromium } = require('playwright');
const F='file:///home/user/cyberdesk-2026/build/mine/cyber-desk-offline.html';
(async()=>{const b=await chromium.launch();
const ctx=await b.newContext({viewport:{width:1280,height:900}});const p=await ctx.newPage();
await p.addInitScript(()=>{try{localStorage.setItem('cyberdesk2:lang','"nl"')}catch(e){}});
await p.goto(F+'#home');await p.waitForTimeout(900);
const keys=await p.evaluate(()=>[...document.querySelectorAll('#pages > article.page')].map(a=>a.id.slice(2)).filter(k=>k!=='search'&&k!=='home'));
let total=0;
for(const k of keys){
 await p.evaluate(k=>{location.hash='#'+k},k);await p.waitForTimeout(300);
 const r=await p.evaluate(()=>{
  const EN=new Set('the and of to in is that for was were with by on as are it be this at from or not has have had which who their its but an a'.split(' '));
  const NL=new Set('de het een van en in is dat voor met op te zijn werd werden niet ook door als bij om aan naar zijn maar die dit deze er wordt'.split(' '));
  const sc=t=>{const w=t.toLowerCase().match(/[a-zà-ÿ']+/g)||[];let e=0,n=0;w.forEach(x=>{if(EN.has(x))e++;if(NL.has(x))n++;});return {e,n,w:w.length};};
  const pg=document.querySelector('#pages > article.page:not([hidden])');
  const vis=e=>{for(let x=e;x&&x!==pg;x=x.parentElement){if(getComputedStyle(x).display==='none')return false;}return true;};
  const flags=[];let enChars=0,nlChars=0;
  pg.querySelectorAll('p,li,td,summary,h3,h4,dd,div.callout').forEach(e=>{
    if(e.querySelector('p,li,td,ul,ol,table,div'))return; if(!vis(e))return;
    const t=e.innerText||'';const s=sc(t);if(s.w<6)return;
    const isEN=s.e>=2&&s.e>s.n*1.5, isNL=s.n>=2&&s.n>s.e*1.5;
    if(isEN)enChars+=t.length;else if(isNL)nlChars+=t.length;
    if(isEN){
      // is there a visible Dutch sibling / inside same parent?
      const par=e.parentElement;let nb=[...par.children].some(c=>c!==e&&vis(c)&&c.matches('.nl-x,.nl-x *')) || [...par.querySelectorAll('.nl-x')].some(vis) && par.tagName!=='SECTION' && !par.matches('#pages > article.page');
      if(nb)flags.push(t.slice(0,90).replace(/\s+/g,' '));
    }
    if(isNL&&e.closest('.en-x'))flags.push('NLinEN '+t.slice(0,60));
  });
  return {flags,enChars,nlChars};});
 total+=r.flags.length;
 console.log(k.padEnd(12),'EN chars',String(r.enChars).padStart(6),'NL chars',String(r.nlChars).padStart(6),'suspects',r.flags.length);
 r.flags.slice(0,4).forEach(f=>console.log('     ?',f));
}
console.log('suspect total',total);
await b.close();})();
