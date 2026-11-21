const FOOT=(()=>{try{return require('fs').readFileSync(__dirname+'/pdf_footer.local.txt','utf8').trim()+' ';}catch(e){return 'Cyber Attacks 2026 · ';}})();
const { chromium } = require('playwright');
const F='file:///home/user/cyberdesk-2026/build/mine/cyber-desk-offline.html';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1100,height:1400}});
await p.emulateMedia({colorScheme:'light'});
await p.goto(F+'#home');await p.waitForTimeout(300);
// render dynamic pages once, keep their HTML

await p.evaluate(()=>{location.hash='updates'});await p.waitForTimeout(150);
await p.evaluate(()=>{location.hash='home'});await p.waitForTimeout(150);
await p.evaluate(()=>{
  document.querySelectorAll('.pn').forEach(e=>e.remove());const _ps=document.getElementById('p-printsel');if(_ps)_ps.remove();
  document.querySelectorAll('#pages > .page').forEach(pg=>{const k=pg.id.slice(2);pg.hidden=(k==='search'||k==='rehearse');});
  document.querySelectorAll('details').forEach(d=>d.open=true);
  document.querySelectorAll('.ictl, #idea-banner, .filters, .filters2, .printbar, .printbtn, #count, .lng').forEach(e=>e.remove());
  document.querySelectorAll('a[href^="#"]').forEach(a=>{const k=a.getAttribute('href').slice(1);if(document.getElementById('p-'+k))a.setAttribute('href','#p-'+k);});
  const st=document.createElement('style');st.textContent=`
   .side,.mtop,.scrim{display:none!important}
   .shell{display:block!important}
   .page{max-width:none!important;padding:0!important}
   #pages > .page{break-before:page}
   #p-home{break-before:auto}
   body{font-size:12.5px!important;background:#fff!important}
   .home-grid a,.ev,.card,.card2,.gap,.prop,details.qa,.country,.fail,.stat,.num,ol.ideas li,tr{break-inside:avoid}
   .tbl{overflow:visible!important}
   h2{font-size:21px!important}
   .crumb{color:#556072}
   .home-grid{grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:6px!important}
   .home-grid a{padding:7px 9px!important}
   .home-grid a b{font-size:12.5px!important}`;
  document.head.appendChild(st);
  const h=document.querySelector('#p-home .sub');if(h)h.insertAdjacentHTML('afterend','<p class="note">PDF edition, generated 12 Nov 2026. The interactive version has search and filters.</p>');
});
await p.pdf({path:'/home/user/cyberdesk-2026/app/Cyber-Attacks-2026.pdf',format:'A4',printBackground:true,margin:{top:'14mm',bottom:'14mm',left:'12mm',right:'12mm'},displayHeaderFooter:true,headerTemplate:'<div></div>',footerTemplate:'<div style="font-size:8px;color:#888;width:100%;text-align:center;font-family:Arial">'+FOOT+'<span class="pageNumber"></span>/<span class="totalPages"></span></div>'});
await b.close();})();
