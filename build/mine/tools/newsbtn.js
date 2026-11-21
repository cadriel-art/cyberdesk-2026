const { chromium } = require('playwright');
const S='/home/user/cyberdesk-2026/build/mine/';
const URL='file://'+S+'cyber-desk-offline.html#news';
let fails=0;const ok=(c,m)=>{console.log((c?'PASS ':'FAIL ')+m);if(!c)fails++;};
const STUB=(mode)=>`(()=>{window.__calls=[];window.__lists=0;const mode=${JSON.stringify(mode)};
window.claude={use:async(n)=>{
 if(n==='mcp')return{
  listTools:async(s)=>{window.__lists++;return{servers:[{server:'Claude Code Remote',authStatus:'connected',tools:mode==='nolist'?[{name:'list_triggers',description:''}]:[{name:'fire_trigger',description:''}]}]};},
  callTool:async(s,t,i)=>{window.__calls.push([s,t,i]);if(mode==='blocked'){throw{code:'blocked_by_policy',message:'x'};}return{content:[],payload:{ok:true}};}};
 return null;}};})()`;
(async()=>{const b=await chromium.launch();
async function open(w,stub){const p=await b.newPage({viewport:{width:w,height:900},deviceScaleFactor:1});p.errs=[];p.on('pageerror',e=>p.errs.push(e.message));p.on('console',m=>{if(m.type()==='error')p.errs.push(m.text())});
 if(stub)await p.addInitScript(stub);await p.goto(URL);await p.waitForSelector('#nw-feeds',{state:'attached'});await p.waitForTimeout(500);return p;}
// a
let p=await open(1280);
ok(await p.evaluate(()=>!document.getElementById('nw-feeds').open),'feeds card collapsed');
const rows=await p.evaluate(()=>document.querySelectorAll('#nw-feeds li').length);ok(rows>=1,'feeds listed: '+rows);
console.log(await p.evaluate(()=>{const d=document.getElementById('nw-feeds');d.open=true;return d.innerText.slice(0,600)}));
// b
ok(await p.evaluate(()=>{const b=document.getElementById('nw-fetch'),a=b&&b.querySelector('a.nw-fopen');return !!b&&!b.hidden&&!!a&&a.href.indexOf('claude.ai/artifact/1TUsEzWWR2P9biSw9tQt82')>0;}),'saved file (file://): link to the online app shown');
ok(p.errs.length===0,'no errors (absent) '+JSON.stringify(p.errs));await p.close();
// c
p=await open(1280,STUB('ok'));
ok(await p.evaluate(()=>!document.getElementById('nw-fetch').hidden),'button visible with stub');
await p.screenshot({path:S+'news-btn-1280.png'});
await p.click('#nw-fbtn');await p.waitForTimeout(300);
let c=await p.evaluate(()=>window.__calls);ok(c.length===1&&c[0][0]==='Claude Code Remote'&&c[0][1]==='fire_trigger'&&c[0][2].trigger_id==='trig_01Ny3on9sf9yEF9WGoJxDR2k'&&c[0][2].text.startsWith('On-demand run'),'one call, right input '+JSON.stringify(c));
ok(await p.evaluate(()=>window.__lists)===1,'listTools called once');
const st=await p.evaluate(()=>[document.getElementById('nw-fmsg').textContent,document.getElementById('nw-fbtn').disabled]);ok(/Started/.test(st[0])&&st[1],'started status + disabled: '+st);
await p.evaluate(()=>document.getElementById('nw-fbtn').click());await p.waitForTimeout(200);
ok((await p.evaluate(()=>window.__calls.length))===1,'second click does nothing');
await p.reload();await p.waitForTimeout(600);
ok(await p.evaluate(()=>document.getElementById('nw-fbtn').disabled),'still disabled after reload (localStorage)');
ok(p.errs.length===0,'no errors (stub) '+JSON.stringify(p.errs));await p.close();
// unavailable cases
for(const m of ['nolist','blocked']){p=await open(1280,STUB(m));await p.click('#nw-fbtn');await p.waitForTimeout(300);
 const r=await p.evaluate(()=>[document.getElementById('nw-fmsg').textContent,document.getElementById('nw-fbtn').disabled,window.__calls.length]);
 ok(/Only the owner/.test(r[0])&&r[1]&&r[2]===(m==='blocked'?1:0),m+': unavailable '+r);
 await p.evaluate(()=>document.getElementById('nw-fbtn').click());await p.waitForTimeout(100);
 ok((await p.evaluate(()=>window.__calls.length))===(m==='blocked'?1:0)&&(await p.evaluate(()=>window.__lists))===1,m+': not called again');await p.close();}
// NL + mobile
p=await open(390,STUB('ok'));await p.evaluate(()=>{const e=document.querySelector('[data-lang=nl],#lang-nl,button[data-l=nl]');});
await p.screenshot({path:S+'news-btn-390.png'});
ok((await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth))<=0,'390 no horizontal overflow');await p.close();
await b.close();console.log(fails?'FAILURES '+fails:'ALL PASS');process.exit(fails?1:0);})();
