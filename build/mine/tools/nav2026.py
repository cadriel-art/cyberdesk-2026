import re,json
M='/home/user/cyberdesk-2026/build/mine/'
def it(k,en,nl,src=None,**kw):
    d={'k':k,'en':en,'nl':nl}
    if src: d['src']=src
    d.update(kw); return d
NAV=[{'en':'Start','nl':'Start','items':[it('home','Overview','Overzicht'),it('trend','Two years in numbers','Twee jaar in cijfers',('R','trend')),it('cases','The big cases','De grote zaken',('R','cases')),it('qa','Questions and answers','Vragen en antwoorden',('P','qa'))]},
{'en':'The attacks','nl':'De aanvallen','items':[it('reg2','Register 2025–2026 (filter)','Register 2025–2026 (filter)',('R','reg2')),it('months','Month by month','Maand per maand',('R','months')),it('eucountries','By country (31)','Per land (31)',('R','eu')),it('actors','Who was behind it','Wie erachter zat',('R','actors')),it('energy','Energy and the grid','Energie en het stroomnet',('P','energy')),it('failures','Avoidable failures','Vermijdbare fouten',('R','failures')),it('good','Good news: defence works','Goed nieuws',('P','good'))]},
{'en':'Belgium','nl':'België','items':[it('now','Right now: Oct–Nov 2026','Nu: okt–nov 2026',('P','now')),it('freezers','The freezer attacks: whole story','De diepvriesaanvallen: het hele verhaal',('P','freezers')),it('year','Belgium 2026: full year','België 2026: heel het jaar',('P','year')),it('back','2023–2025 essentials','2023–2025: de kern',('P','back')),it('register','Belgium register since 2023 (filter)','Register België sinds 2023 (filter)',('R','belgium')),it('numbers','Belgian numbers to know','Belgische cijfers om te kennen',('P','numbers')),it('tools','What Belgium has','Wat België heeft',('P','tools')),it('powers','Who is responsible for what','Wie is waarvoor bevoegd',('P','powers'))]},
{'en':'What follows: laws and ideas','nl':'Wat volgt: wetten en ideeën','items':[it('laws','Laws and regulations','Wetten en regels',('P','laws')),it('files','Where each law stands','Waar elke wet staat',('R','files')),it('gaps','What we lack','Wat ontbreekt',('P','gaps')),it('props','Proposals','Voorstellen',('P','props')),it('ideas','53 ideas','53 ideeën',('R','ideas')),it('who',"Who's who",'Wie is wie',('R','who'))]},
{'en':'People','nl':'Mensen','items':[it('victims','Every kind of victim & fraud','Alle slachtoffers & fraude',('P','victims')),it('citizens','How alert are citizens?','Hoe alert zijn burgers?',('P','citizens'))]},
{'en':'Technology','nl':'Technologie','items':[it('ai','AI: what is real','AI: wat is echt',('P','ai')),it('agents','AI agents that hacked companies','AI-agenten die bedrijven hackten',('R','ai')),it('cloud','Cloud dependence','Afhankelijkheid van de cloud',('P','cloud')),it('quantum',"What's next: quantum",'Wat komt: kwantum',('P','quantum'))]},
{'en':'Explore','nl':'Verkennen','items':[it('more','More subjects to explore','Meer onderwerpen om te verkennen',('P','more'))]},
{'en':'Reference','nl':'Naslag','items':[it('glossary','Glossary','Woordenlijst',('R','glossary')),it('sources','Sources','Bronnen'),it('updates','Updates','Updates',live=1,dyn=1)]}]
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
i=t.index('NAV=['); j=t.index('pages=[]'); t=t[:i]+'NAV='+repr(NAV)+'\n'+t[j:]
a=t.index("home='''"); z=t.index("pages.append(home)")
home="""home='''<article class="page" id="p-home" data-static hidden><section id="s-home">
<div class="crumb">Cyber Attacks 2026</div>
<h2>Cyberattacks on Europe, 2025–2026</h2>
<p class="sub">Every recorded attack that could be traced in the 27 EU countries plus Norway, Iceland, Switzerland and Liechtenstein, over two years, to show how the picture changed. Confirmed incidents are kept apart from reported and claimed ones. Each item is dated and sourced.</p>
<p class="nl"><b>NL:</b> Elke gekende aanval die we konden terugvinden in de 27 EU-landen plus Noorwegen, IJsland, Zwitserland en Liechtenstein, over twee jaar, om te tonen hoe het beeld veranderde. Bevestigde incidenten staan apart van gerapporteerde en geclaimde. Elk item heeft een datum en een bron. De taal kies je bovenaan in het menu.</p>
<div class="meta" style="display:flex;flex-wrap:wrap;gap:8px 18px;font-family:var(--f-mono);font-size:12.5px;color:var(--muted)"><span>Status as of 16 Nov 2026</span><span>31 countries · 2025 and 2026</span><span>Prepared with Claude (Anthropic)</span></div>
<div class="callout" style="margin-top:14px"><b>Start here · Begin hier:</b> <a href="#trend">Two years in numbers</a>, then <a href="#cases">the big cases</a>, then <a href="#reg2">the register</a> with its filters, or go straight to <a href="#eucountries">a country</a>. To see who is blamed for what, and on what evidence: <a href="#evidence">the evidence tracker</a>. For an overview of every subject in this file: <a href="#more">subjects and what is still open</a>.</div>
<div class="plainbox" style="margin-top:12px"><div class="pb-h">What is in this file · Wat in dit dossier zit</div>
<ul class="tight">
<li><b>The attacks · De aanvallen:</b> the full register for 2025–2026 with filters, month by month, 31 countries, who was behind it, and energy. · <i>Het volledige register 2025–2026 met filters, maand per maand, 31 landen, wie erachter zat, en energie.</i></li>
<li><b>Belgium · België:</b> the last weeks, the freezer attacks, the full year, and the Belgian register since 2023. · <i>De voorbije weken, de diepvriesaanvallen, het volledige jaar, en het Belgische register sinds 2023.</i></li>
<li><b>What follows · Wat volgt:</b> the laws, what is missing, eight proposals and 53 ideas. · <i>De wetten, wat ontbreekt, acht voorstellen en 53 ideeën.</i></li>
<li><b>Beyond hacking · Meer dan hacken:</b> drones and sabotage, elections and democracy, the defence side, and an index of subjects. · <i>Drones en sabotage, verkiezingen en democratie, de defensiekant, en een index van onderwerpen.</i></li>
<li><b>Subject by subject · Onderwerp per onderwerp:</b> energy, water, transport and ports, health — each first for Belgium, then for the other 30 countries. · <i>Energie, water, vervoer en havens, gezondheid — telkens eerst voor België, dan voor de andere 30 landen.</i></li>
<li><b>People, Technology, Reference:</b> fraud and citizens, AI and cloud, glossary, the typed source register and updates. · <i>Fraude en burgers, AI en cloud, woordenlijst, het gesorteerde bronnenregister en updates.</i></li>
</ul></div>
<div class="callout warn" style="margin-top:12px"><b>What this file is not.</b> It is not a complete count. Most victims are never named, countries publish very differently, and the research looked harder at 2026 than at 2025. Use it for the pattern and for the individual cases, not for totals.</div>
<div class="home-grid" id="home-grid"></div>
</section></article>'''
"""
t=t[:a]+home+t[z:]
t=t.replace('Status as of 16 Nov 2026','Status as of '+__import__('datetime').date.today().strftime('%-d %b %Y'))
open(b,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
t=t.replace('<title>Cyber Desk Belgium EU</title>','<title>Cyber Attacks 2026</title>').replace('<b>Cyber Desk</b><small>BELGIUM AND THE EU</small>','<b>Cyber Attacks 2026</b><small>EU AND SCHENGEN · 2025–2026</small>').replace('<b>Cyber Desk</b><span id="mtitle">','<b>Cyber Attacks 2026</b><span id="mtitle">')
JS='''
/* ---------- register 2025-2026 filters ---------- */
(function(){const box=document.getElementById('reg2f');if(!box)return;const rows=[...document.querySelectorAll('#reg2t tbody tr')];const cnt=document.getElementById('reg2count');
function apply(){const f={};box.querySelectorAll('select').forEach(s=>{if(s.value)f[s.dataset.k]=s.value});let n=0;rows.forEach(r=>{const ok=Object.keys(f).every(k=>r.dataset[k]===f[k]);r.hidden=!ok;if(ok)n++;});if(cnt)cnt.textContent=n+' of '+rows.length+' incidents shown';}
box.addEventListener('change',apply);apply();})();
'''
if 'register 2025-2026 filters' not in t:
    k=t.rindex('</script>'); t=t[:k]+JS+t[k:]
t=t.replace('</style>','.filters2 select{font:inherit;font-size:13.5px;padding:7px 10px;border-radius:8px;border:1px solid var(--line);background:var(--paper);color:var(--ink);max-width:100%}\n</style>',1)
open(a,'w',encoding='utf-8').write(t)

# ---------- printing ----------
t=open(a,encoding='utf-8').read()
PCSS="""
.printbar{display:flex;justify-content:flex-end;gap:8px;margin:0 0 8px}
.printbtn{font:inherit;font-size:13px;padding:6px 12px;border-radius:8px;border:1px solid var(--line);background:var(--paper);color:var(--ink);cursor:pointer}
.printbtn:hover{border-color:var(--accent)}
.country .printbtn{font-size:11.5px;padding:3px 8px;margin-left:8px}
#printhead{display:none}
@media print{
  :root{--bg:#fff!important;--paper:#fff!important;--ink:#111!important;--muted:#444!important;--line:#bbb!important;--accent:#1f4fd1!important;--accent-soft:#eef2fc!important;color-scheme:light!important}
  html,body{background:#fff!important}
  body{font-size:11.5pt!important}
  .side,.mtop,.scrim,.pn,.printbar,.printbtn,.filters,.filters2,.lng,.home-grid,#q,#q-label,.ictl{display:none!important}
  .shell{display:block!important}
  .mainc,main{margin:0!important;padding:0!important;max-width:none!important}
  #pages > .page{max-width:none!important;padding:0!important}
  #pages > .page[hidden]{display:none!important}
  #printhead{display:block!important;border-bottom:2px solid #111;padding-bottom:6px;margin-bottom:12px;font-size:10pt}
  #printhead b{font-size:13pt;display:block}
  .tbl{overflow:visible!important;border:0!important}
  table{font-size:9.5pt!important}
  thead{display:table-header-group}
  th{position:static!important}
  tr,li,.gapx,.country,.card,.card2,.prop,details.qa,.stat,.callout,.plainbox,ol.ideas li{break-inside:avoid}
  h2,h3,h4{break-after:avoid}
  .countries{display:block!important}
  .country{margin-bottom:10px}
  a{color:#111!important;text-decoration:none!important}
  details.qa > summary{list-style:none}
  body.print-solo #pages > .page:not([hidden]) > :not(section){display:none!important}
  body.print-solo #pages > .page:not([hidden]) section > :not(.countries){display:none!important}
  body.print-solo .countries .country:not(.solo){display:none!important}
  @page{margin:14mm 12mm}
}
"""
PJS="""
/* ---------- printing ---------- */
function addPrint(k){
  const p=document.getElementById('p-'+k); if(!p||k==='search') return;
  if(!p.querySelector(':scope > .printbar')){
    const bar=document.createElement('div'); bar.className='printbar';
    bar.innerHTML='<button type="button" class="printbtn" data-print="page">'+(lang==='nl'?'Deze pagina afdrukken':'Print this page')+'</button>';
    p.insertBefore(bar,p.firstChild);
  } else { p.querySelector(':scope > .printbar .printbtn').textContent=(lang==='nl'?'Deze pagina afdrukken':'Print this page'); }
  if(k==='eucountries'){
    p.querySelectorAll('.countries .country').forEach(c=>{
      if(c.id&&c.id.indexOf('c-')===0&&!c.querySelector('.printbtn')){
        const b=document.createElement('button'); b.type='button'; b.className='printbtn'; b.dataset.print='country'; b.textContent=(lang==='nl'?'Afdrukken':'Print');
        const h=c.querySelector('h4'); if(h) h.appendChild(b);
      }
    });
  }
}
function doPrint(solo){
  const p=document.getElementById('p-'+cur); if(!p) return;
  const opened=[]; p.querySelectorAll('details:not([open])').forEach(d=>{d.open=true;opened.push(d);});
  let head=document.getElementById('printhead'); if(!head){head=document.createElement('div');head.id='printhead';document.getElementById('pages').insertBefore(head,document.getElementById('pages').firstChild);}
  const it=item(cur); let title=it?(it.i[lang]||it.i.en):'';
  if(solo){ document.body.classList.add('print-solo'); solo.classList.add('solo'); title=solo.querySelector('h4').childNodes[0].textContent.trim(); }
  let extra='';
  if(cur==='reg2'&&!solo){ const f=[...document.querySelectorAll('#reg2f select')].filter(s=>s.value).map(s=>s.options[s.selectedIndex].text); const c=document.getElementById('reg2count'); extra=(f.length?' · '+(lang==='nl'?'Filter: ':'Filter: ')+f.join(', '):'')+(c?' · '+c.textContent:''); }
  const d=new Date(); const ds=d.toLocaleDateString(lang==='nl'?'nl-BE':'en-GB',{day:'numeric',month:'long',year:'numeric'});
  head.innerHTML='<b>'+esc(title)+'</b>Cyber Attacks 2026 · EU and Schengen · 2025–2026 · '+(lang==='nl'?'afgedrukt op ':'printed on ')+esc(ds)+esc(extra);
  const done=()=>{opened.forEach(d=>d.open=false);document.body.classList.remove('print-solo');document.querySelectorAll('.country.solo').forEach(c=>c.classList.remove('solo'));window.removeEventListener('afterprint',done);};
  window.addEventListener('afterprint',done);
  try{ window.print(); }catch(e){ done(); alert(lang==='nl'?'Afdrukken werkt hier niet. Open de offline versie van dit bestand en druk daar af.':'Printing is not available here. Open the offline copy of this file and print from there.'); }
}
document.addEventListener('click',e=>{const b=e.target.closest('.printbtn');if(!b)return;e.preventDefault();doPrint(b.dataset.print==='country'?b.closest('.country'):null);});
"""
if 'function addPrint' not in t:
    t=t.replace('</style>',PCSS+'</style>',1)
    assert t.count('  addPN(k);')==1
    t=t.replace('  addPN(k);','  addPN(k);addPrint(k);')
    assert t.count('function addPN(k){')==1; t=t.replace('function addPN(k){',PJS+'\nfunction addPN(k){')
    open(a,'w',encoding='utf-8').write(t)

o=M+'tools/offline.py'; t=open(o,encoding='utf-8').read()
t=t.replace("rep('<title>Cyber Desk Belgium EU</title>','<title>Cyber Desk Belgium EU (offline)</title>')","rep('<title>Cyber Attacks 2026</title>','<title>Cyber Attacks 2026 (offline)</title>')").replace('rep("<small>BELGIUM AND THE EU</small>","<small>BELGIUM AND THE EU · OFFLINE</small>")','rep("<small>EU AND SCHENGEN · 2025–2026</small>","<small>EU AND SCHENGEN · 2025–2026 · OFFLINE</small>")')
open(o,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
t+='''
INTRO['trend']=("How the two years compare: what official agencies counted (including the EU agency's own 2026 report, in a closed box), what this file's own list shows, and the five patterns that stand out.","Hoe de twee jaren zich verhouden: wat de officiële diensten telden (ook het eigen rapport van het EU-agentschap, in een dichte kaart), wat de lijst in dit dossier toont, en de vijf patronen die opvallen.")
INTRO['cases']=("The ten attacks that best show what changed, each in a few lines.","De tien aanvallen die het best tonen wat er veranderde, telkens in enkele regels.")
INTRO['reg2']=("The full list of recorded attacks in 31 countries over two years. Use the filters to narrow it down.","De volledige lijst van gekende aanvallen in 31 landen over twee jaar. Gebruik de filters om ze te verfijnen.")
INTRO['months']=("The same incidents, grouped by month, so you can see how each year built up.","Dezelfde incidenten, gegroepeerd per maand, zodat je ziet hoe elk jaar zich opbouwde.")
INTRO['actors']=("Which states and groups have been officially named, and for which attacks. For most attacks nobody has been named.","Welke staten en groepen officieel aangewezen zijn, en voor welke aanvallen. Voor de meeste aanvallen is niemand aangewezen.")
INTRO['eucountries']=("Each of the 31 countries on its own: the official figures where they exist, then what is confirmed, then what is only reported or claimed.","Elk van de 31 landen apart: de officiële cijfers waar die bestaan, dan wat bevestigd is, dan wat alleen gerapporteerd of geclaimd is.")
'''
open(l,'w',encoding='utf-8').write(t)
p=M+'tools/pdf.js'; t=open(p,encoding='utf-8').read()
t=t.replace('Cyber-Desk-Belgium-EU.pdf','Cyber-Attacks-2026.pdf').replace('PDF edition of the Cyber Desk, generated 12 Nov 2026.','PDF edition, generated 12 Nov 2026.')
open(p,'w',encoding='utf-8').write(t)
print('nav ok')
