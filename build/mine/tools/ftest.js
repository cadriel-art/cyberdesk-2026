const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:1000}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+S+'cyber-desk.html#map');await p.waitForTimeout(1300);
// focus survives a chip toggle, a story, a month bar and a country bar
async function probe(sel,label){await p.focus(sel);await p.keyboard.press('Enter');await p.waitForTimeout(350);
  console.log(label,'focus ->',await p.evaluate(()=>{const a=document.activeElement;return a?(a.tagName+(a.dataset&&a.dataset.k?':'+a.dataset.k:'')+(a.dataset&&a.dataset.story?':'+a.dataset.story:'')+(a.dataset&&a.dataset.m?':'+a.dataset.m:'')+(a.dataset&&a.dataset.c?':'+a.dataset.c:'')):'none'}));}
await probe('.mp-chip[data-k="drones"]','chip');
await probe('.mp-sbtn[data-story="cables"]','story');
await probe('.mp-sbtn[data-story="reset"]','reset');
await probe('.mp-sp[data-m="10"]','month bar');
await probe('.mp-bar[data-c="Belgium"]','country bar');
// series keeps the chosen types
await p.click('[data-story="reset"]');await p.waitForTimeout(300);
await p.click('.mp-chip[data-all="0"]');await p.click('.mp-chip[data-k="water"]');await p.waitForTimeout(250);
const before=await p.evaluate(()=>[...document.querySelectorAll('.mp-chip[aria-pressed="true"]')].map(x=>x.dataset.k));
await p.selectOption('#mp-camp','freezer');await p.waitForTimeout(300);
await p.selectOption('#mp-camp','');await p.waitForTimeout(300);
const after=await p.evaluate(()=>[...document.querySelectorAll('.mp-chip[aria-pressed="true"]')].map(x=>x.dataset.k));
console.log('types before/after a series:',JSON.stringify(before),JSON.stringify(after));
// a pin under a country count is clickable
await p.click('[data-story="reset"]');await p.waitForTimeout(400);
const blocked=await p.evaluate(()=>{let n=0,tot=0;
 document.querySelectorAll('#mp-mk .mp-m, #mp-mk .mp-cl').forEach(m=>{const r=m.getBoundingClientRect();
  const x=r.left+r.width/2,y=r.top+r.height*0.35;const st=document.elementsFromPoint(x,y);
  tot++;let hit=false;for(const e of st){if(e.closest&&e.closest('.mp-m,.mp-cl')){hit=true;break;}if(e.closest&&e.closest('.mp-b'))break;}
  if(!hit)n++;});return {blocked:n,tot};});
console.log('marks blocked by a count badge:',JSON.stringify(blocked));
console.log('errors',errs);await b.close();})();
