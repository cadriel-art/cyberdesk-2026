from bs4 import BeautifulSoup
import re
M='/home/user/cyberdesk-2026/build/mine/'
# 1 section in the register file
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
SEC='''<section id="printsel">
<h2>Print a selection</h2>
<p class="sub">Choose pages and countries, then print them as one document with a cover, a list of contents and page breaks between pages. To save it as a file, choose "Save as PDF" in the print dialog.</p>
<p class="nl"><b>NL:</b> Kies pagina's en landen en druk ze af als één document, met een voorblad, een inhoudsopgave en een nieuwe bladzijde per pagina. Kies "Opslaan als pdf" in het afdrukvenster om er een bestand van te maken.</p>
<h3>Ready-made sets</h3>
<div class="filters" id="ps-presets">
<button type="button" data-set="short">The short version</button>
<button type="button" data-set="attacks">Everything on the attacks</button>
<button type="button" data-set="belgium">Belgium</button>
<button type="button" data-set="subjects">Subject by subject</button>
<button type="button" data-set="beyond">Beyond hacking</button>
<button type="button" data-set="laws">Laws and ideas</button>
<button type="button" data-set="all">Whole file</button>
<button type="button" data-set="none">Clear</button>
</div>
<h3>Pages</h3>
<div id="ps-pages" class="ps-grid"></div>
<h3>Countries</h3>
<p class="small">Tick countries to print only those country cards. Leave all unticked and tick "By country (31)" above to print every country.</p>
<div id="ps-countries" class="ps-chips"></div>
<h3>Options</h3>
<div class="ps-opts">
<fieldset><legend>Language on paper</legend>
<label><input type="radio" name="ps-lang" value="en" checked> English only (shorter)</label>
<label><input type="radio" name="ps-lang" value="both"> English and Dutch</label>
<p class="small">The incident lists exist in English only, so a Dutch-only printout is not possible.</p></fieldset>
<fieldset><legend>Style</legend>
<label><input type="radio" name="ps-style" value="light" checked> Light (thin borders, saves ink)</label>
<label><input type="radio" name="ps-style" value="colour"> Colour (as on screen)</label></fieldset>
<fieldset><legend>Extras</legend>
<label><input type="checkbox" id="ps-cover" checked> Cover and list of contents</label>
<label><input type="checkbox" id="ps-terms"> "Terms on this page" tables</label></fieldset>
</div>
<div class="callout" id="ps-summary" aria-live="polite">Nothing selected yet.</div>
<p><button type="button" class="printbtn ps-go" id="ps-go" data-print="multi">Print the selection</button></p>
<p class="small">Page numbers in the footer work in Chrome and Edge. In other browsers, switch on "headers and footers" in the print dialog.</p>
</section>'''
old=R.find('section',id='printsel')
if old: old.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
# 2 nav + intro
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'printsel'" not in t:
    a="{'k': 'glossary'"; assert a in t
    t=t.replace(a,"{'k': 'printsel', 'en': 'Print a selection', 'nl': 'Een selectie afdrukken', 'src': ('R', 'printsel')}, "+a,1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['printsel']" not in t:
    t+='''
INTRO['printsel']=("Make your own printed document from this file: tick what you want, and it prints as one neat document.","Maak je eigen afgedrukte document uit dit dossier: vink aan wat je wilt, en het wordt als één net document afgedrukt.")
'''
    open(l,'w',encoding='utf-8').write(t)
# 3 template css + js
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
CSS="""
.ps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}
.ps-grid fieldset,.ps-opts fieldset{border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:0;background:var(--paper);min-width:0}
.ps-grid legend,.ps-opts legend{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);padding:0 4px}
.ps-grid label,.ps-opts label{display:flex;gap:8px;align-items:flex-start;font-size:14px;padding:3px 0;cursor:pointer}
.ps-grid .ps-all{font-weight:600;border-bottom:1px solid var(--line);margin-bottom:4px;padding-bottom:6px}
.ps-chips{display:flex;flex-wrap:wrap;gap:6px}
.ps-chips label{font-size:13px;padding:4px 10px;border-radius:999px;border:1px solid var(--line);background:var(--paper);cursor:pointer;display:inline-flex;gap:6px;align-items:center}
.ps-opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin-bottom:12px}
.ps-go{font-size:15px!important;padding:10px 18px!important;background:var(--ink)!important;color:var(--bg)!important;border-color:var(--ink)!important}
@media print{
  .termsbox{display:none!important}
  body.p-terms .termsbox{display:block!important}
  body.p-light .plainbox,body.p-light .callout,body.p-light .joe,body.p-light .pl,body.p-light .pl2,body.p-light .message,body.p-light .card,body.p-light .card2{background:#fff!important;border:1px solid #bbb!important}
  body.p-light .tag{background:#fff!important;border:1px solid #999!important;color:#111!important}
  body.p-light th{background:#fff!important;border-bottom:1.5px solid #111!important}
  body.pl-en .plnl,body.pl-en .pb-nl,body.pl-en .joe-nl,body.pl-en p.nl,body.pl-en .nlcol,body.pl-en .nl-inline{display:none!important}
  body.print-multi #pages > .page{display:none!important}
  body.print-multi #pages > .page.psel{display:block!important;break-before:page}
  body.print-multi #p-printsel{display:none!important}
  body.print-multi #printhead{border:0!important;break-after:page;padding-top:60mm;font-size:11pt}
  body.print-multi #printhead b{font-size:26pt;line-height:1.1;margin-bottom:8mm}
  body.print-multi #printhead ol{margin:6mm 0 0;padding-left:6mm;font-size:11pt;columns:2;column-gap:10mm}
  body.print-multi #printhead .cv-meta{color:#444;margin-top:4mm}
  body.print-multi.no-cover #printhead{display:none!important}
  body.print-csel #p-eucountries section > :not(.countries):not(h2){display:none!important}
  body.print-csel #p-eucountries .countries .country:not(.solo){display:none!important}
  body.print-csel #p-eucountries > .plainbox{display:none!important}
  #pages > .page, #pages > .page > section, #pages .page p, #pages .page .sub{max-width:none!important}
  body.print-csel #p-eucountries .country.solo{break-inside:auto!important;margin-bottom:8mm}
  body.print-csel #p-eucountries .country.solo h4{break-after:avoid}
  .src a[href^="http"]::after{content:" (" attr(href) ")";font-size:7.5pt;color:#444;word-break:break-all}
  @page{margin:14mm 12mm 16mm;@bottom-center{content:counter(page);font-size:9pt;color:#444}}
}
"""
JS="""
/* ---------- print a selection ---------- */
const PSETS={short:['trend','cases','qa','evidence'],attacks:['trend','cases','reg2','months','eucountries','actors','energy','water','watereu','transport','transporteu','health','healtheu','failures','good'],belgium:['now','freezers','year','back','register','numbers','tools','powers','hybrid','water','transport','health','elections','defence'],beyond:['hybrid','hybrideu','elections','electionseu','defence','defenceeu','evidence','outages','prepare'],subjects:['energy','water','watereu','transport','transporteu','health','healtheu','elections','electionseu','hybrid','hybrideu'],laws:['laws','files','gaps','props','ideas','who'],all:null,none:[]};
function psKeys(){return NAV.flatMap(g=>g.items).filter(i=>!i.live&&i.k!=='printsel'&&i.k!=='home').map(i=>i.k);}
function psInit(){
  const box=document.getElementById('ps-pages'); if(!box||box.dataset.done) return; box.dataset.done=1;
  document.querySelectorAll('#pages table').forEach(tb=>{const ths=[...tb.querySelectorAll('thead th')];ths.forEach((th,i)=>{if(th.textContent.trim()==='NL'){th.classList.add('nlcol');tb.querySelectorAll('tbody tr').forEach(tr=>{const c=tr.children[i];if(c)c.classList.add('nlcol');});}});});
  box.innerHTML=NAV.map((g,gi)=>{const its=g.items.filter(i=>!i.live&&i.k!=='printsel'&&i.k!=='home');if(!its.length)return '';return '<fieldset><legend>'+esc(g.en)+'</legend><label class="ps-all"><input type="checkbox" data-grp="'+gi+'"> All of this group</label>'+its.map(i=>'<label><input type="checkbox" data-pg="'+i.k+'" data-g="'+gi+'"> '+esc(i.en)+'</label>').join('')+'</fieldset>';}).join('');
  const cb=document.getElementById('ps-countries');
  cb.innerHTML=[...document.querySelectorAll('#p-eucountries .countries .country')].filter(c=>c.id&&c.id.indexOf('c-')===0).map(c=>'<label><input type="checkbox" data-ct="'+c.id+'"> '+esc(c.querySelector('h4').childNodes[0].textContent.trim())+'</label>').join('');
  const root=document.getElementById('p-printsel');
  root.addEventListener('change',e=>{const t=e.target;if(t.dataset.grp!==undefined){root.querySelectorAll('input[data-g="'+t.dataset.grp+'"]').forEach(x=>x.checked=t.checked);}psSummary();});
  document.getElementById('ps-presets').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;const set=PSETS[b.dataset.set];root.querySelectorAll('input[data-pg]').forEach(x=>x.checked=(set===null)||set.includes(x.dataset.pg));root.querySelectorAll('input[data-ct],input[data-grp]').forEach(x=>x.checked=false);psSummary();});
  psSummary();
}
function psState(){
  const root=document.getElementById('p-printsel');
  const pages=[...root.querySelectorAll('input[data-pg]:checked')].map(x=>x.dataset.pg);
  const cts=[...root.querySelectorAll('input[data-ct]:checked')].map(x=>x.dataset.ct);
  const langSel=(root.querySelector('input[name="ps-lang"]:checked')||{}).value||'en';
  const style=(root.querySelector('input[name="ps-style"]:checked')||{}).value||'light';
  return {pages,cts,langSel,style,cover:document.getElementById('ps-cover').checked,terms:document.getElementById('ps-terms').checked};
}
function psLen(el,en){ let n=el.textContent.length; if(en){ el.querySelectorAll('.plnl,.pb-nl,.joe-nl,p.nl,.nlcol').forEach(x=>n-=x.textContent.length); } return Math.max(n,0); }
function psSummary(){
  const s=psState(); const out=document.getElementById('ps-summary'); if(!out) return;
  let pages=s.pages.slice(); if(s.cts.length&&!pages.includes('eucountries')) pages.push('eucountries');
  if(!pages.length){out.textContent='Nothing selected yet.';return;}
  let chars=0; const en=s.langSel==='en';
  pages.forEach(k=>{const p=document.getElementById('p-'+k);if(!p)return; if(k==='eucountries'&&s.cts.length){s.cts.forEach(id=>{const c=document.getElementById(id);if(c)chars+=psLen(c,en);});} else {let n=psLen(p,en); if(!s.terms){const tb=p.querySelector('.termsbox'); if(tb) n-=tb.textContent.length;} chars+=Math.max(n,0);}});
  const est=Math.max(pages.length,Math.round(chars/1600))+(s.cover?1:0);
  out.innerHTML='<b>'+pages.length+' page'+(pages.length>1?'s':'')+' selected'+(s.cts.length?' · '+s.cts.length+' countr'+(s.cts.length>1?'ies':'y'):'')+'.</b> About '+est+' sheet'+(est>1?'s':'')+' of A4 (rough estimate; the print dialog shows the exact number).';
}
function doPrintMulti(){
  const s=psState(); let pages=s.pages.slice(); if(s.cts.length&&!pages.includes('eucountries')) pages.push('eucountries');
  if(!pages.length){alert('Select at least one page or country first.');return;}
  const order=psKeys().filter(k=>pages.includes(k));
  const opened=[]; const cls=['print-multi', s.style==='light'?'p-light':'p-colour', s.langSel==='en'?'pl-en':'pl-both'];
  if(!s.cover) cls.push('no-cover'); if(s.terms) cls.push('p-terms'); if(s.cts.length) cls.push('print-csel');
  order.forEach(k=>{const p=document.getElementById('p-'+k); if(!p) return; p.classList.add('psel'); p.querySelectorAll('details:not([open])').forEach(d=>{d.open=true;opened.push(d);});});
  s.cts.forEach(id=>{const c=document.getElementById(id); if(c) c.classList.add('solo');});
  document.body.classList.add(...cls);
  let head=document.getElementById('printhead'); if(!head){head=document.createElement('div');head.id='printhead';document.getElementById('pages').insertBefore(head,document.getElementById('pages').firstChild);}
  const d=new Date().toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric'});
  const names=order.map(k=>{const it=item(k); let n=it?it.i.en:k; if(k==='eucountries'&&s.cts.length){n+=': '+s.cts.map(id=>document.getElementById(id).querySelector('h4').childNodes[0].textContent.trim()).join(', ');} return n;});
  head.innerHTML='<b>Cyberattacks on Europe, 2025–2026</b>A selection from "Cyber Attacks 2026": the 27 EU countries plus Norway, Iceland, Switzerland and Liechtenstein.<div class="cv-meta">Facts as of 12 November 2026 · printed on '+esc(d)+' · '+(s.langSel==='en'?'English':'English and Dutch')+'</div><ol>'+names.map(n=>'<li>'+esc(n)+'</li>').join('')+'</ol>';
  const done=()=>{opened.forEach(x=>x.open=false);document.body.classList.remove(...cls);document.querySelectorAll('.page.psel').forEach(p=>p.classList.remove('psel'));document.querySelectorAll('.country.solo').forEach(c=>c.classList.remove('solo'));window.removeEventListener('afterprint',done);};
  window.addEventListener('afterprint',done);
  try{ window.print(); }catch(e){ done(); alert('Printing is not available here. Open the offline copy of this file and print from there.'); }
}
"""
if 'function psInit' not in t:
    t=t.replace('</style>',CSS+'</style>',1)
    assert t.count('function addPN(k){')==1
    t=t.replace('function addPN(k){',JS+'\nfunction addPN(k){')
    # hook: init when the page opens; route the multi button; light style for single prints
    assert t.count("  addPN(k);addPrint(k);")==1
    t=t.replace("  addPN(k);addPrint(k);","  addPN(k);addPrint(k);if(k==='printsel')psInit();")
    o="document.addEventListener('click',e=>{const b=e.target.closest('.printbtn');if(!b)return;e.preventDefault();doPrint("
    assert o in t
    t=t.replace(o,"document.addEventListener('click',e=>{const b=e.target.closest('.printbtn');if(!b)return;e.preventDefault();if(b.dataset.print==='multi'){doPrintMulti();return;}doPrint(")
    # single-page prints: light style by default, both languages
    o2="  const done=()=>{opened.forEach(d=>d.open=false);document.body.classList.remove('print-solo');"
    assert o2 in t
    t=t.replace(o2,"  document.body.classList.add('p-light');\n  const done=()=>{opened.forEach(d=>d.open=false);document.body.classList.remove('print-solo','p-light');")
    # no print bar on the selection page itself
    o3="function addPrint(k){\n  const p=document.getElementById('p-'+k); if(!p||k==='search') return;"
    assert o3 in t; t=t.replace(o3,"function addPrint(k){\n  const p=document.getElementById('p-'+k); if(!p||k==='search'||k==='printsel') return;")
    open(a,'w',encoding='utf-8').write(t)
q=M+'tools/pdf.js'; s=open(q,encoding='utf-8').read()
if "p-printsel" not in s:
    s=s.replace("document.querySelectorAll('.pn').forEach(e=>e.remove());","document.querySelectorAll('.pn').forEach(e=>e.remove());const _ps=document.getElementById('p-printsel');if(_ps)_ps.remove();")
    open(q,'w',encoding='utf-8').write(s)
print('print2 ok')
