"""Page '#outages': Global outages. Built from tools/outages_data.json (merged from the two fact-checked files)."""
import json,html,re,collections
from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
e=html.escape
D=json.load(open(M+'tools/outages_data.json',encoding='utf-8'))
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not published','t-none')}
TW={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Nobody named','t-none')}
KIND={'technical':'Technical fault or change','physical':'Power or cooling failure','cyberattack':'Cyberattack','unknown':'Cause not published'}
def tag(s,t=T): return '<span class="tag %s">%s</span>'%(t[s][1],t[s][0])
main=sorted([x for x in D if not x['background']],key=lambda x:(x['sort'],x['id']),reverse=True)
bg=sorted([x for x in D if x['background']],key=lambda x:(x['sort'],x['id']),reverse=True)
N=len(main)
kc=collections.Counter(x['kind'] for x in main)
att=[x for x in main if x['kind']=='cyberattack']
plat=[x for x in main if x['kind']!='cyberattack']
cconf=sum(1 for x in main if x['cause_status']=='C')
wc=collections.Counter(x['who_status'] for x in att)
assert kc['cyberattack']*2<N, 'sub-line says most were not attacks'
# ---------- key figures
def tile(n,l): return '<div class="stx"><b>%s</b><span>%s</span></div>'%(n,e(l))
tiles=''.join([tile(N,'outages in the period'),tile(kc['technical'],'technical faults or changes'),tile(kc['physical'],'power or cooling failures'),tile(kc['cyberattack'],'cyberattacks'),tile(kc['unknown'],'cause not published'),
 tile(cconf,'with a cause confirmed by the company or an authority'),
 tile(wc['C'],'attacks with a culprit formally named by an authority'),tile(wc['R'],'attacks with a culprit named only by media reports'),tile(wc['K'],'attacks where only the attackers (or a party) claim it'),tile(wc['N'],'attacks where nobody is named')])
# ---------- pattern findings (all computed)
def company_key(c): return re.split(r'[ (/]',c.strip())[0]
def lst(a): return a[0] if len(a)==1 else ', '.join(a[:-1])+' and '+a[-1]
F=[]
tc=collections.Counter(x['kind'] for x in plat)
nopub=tc['unknown']
if not any(x['kind']=='cyberattack' for x in plat):
    F.append('Of the %d platform and network outages (cloud, internet, telecom and online services), %d were put down to a technical fault or change, %d to a power or cooling failure and %d have no published cause. None of them is blamed on a cyberattack in the sources seen. For %d of the %d the company or an authority confirmed the cause.'%(len(plat),tc['technical'],tc['physical'],nopub,sum(1 for x in plat if x['cause_status']=='C'),len(plat)))
byco=collections.defaultdict(list)
for x in plat: byco[company_key(x['company'])].append(x['company'])
top=sorted([(k,len(v)) for k,v in byco.items() if len(v)>=3],key=lambda z:(-z[1],z[0]))
if top:
    parts=[]
    for k,n in top:
        names=sorted(set(byco[k])); parts.append('%s (%d%s)'%(k,n,'; counted together: '+lst(names) if len(names)>1 else ''))
    tot=sum(n for _,n in top)
    F.append('%s of the %d platform outages were at just %s: %s. Counted by company name only.'%(['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen'][tot] if tot<19 else tot,len(plat),['zero','one','two','three','four','five'][len(top)]+' companies' if len(top)<6 else '%d companies'%len(top),'; '.join(parts)))
ph=[x for x in main if x['kind']=='physical']
if ph:
    F.append('%d outages were traced to physical problems in data centres (power or cooling), at %s.'%(len(ph),lst(sorted(set(company_key(x['company']) if company_key(x['company'])!='Google' else x['company'] for x in ph)))))
if att:
    F.append('Of the %d outages caused by cyberattacks, the company or an authority confirmed the attack itself in %d, but a culprit was formally named by an authority in only %d. In %d the only name is a group\'s own claim, in %d it is reported by media, and in %d nobody is named (status in the sources seen).'%(len(att),sum(1 for x in att if x['cause_status']=='C'),wc['C'],wc['K'],wc['R'],wc['N']))
NOTE='A "Claimed" culprit is not a finding: this file records only that the claim was made.'
pattern='<h3>What the pattern shows</h3><ul>'+''.join('<li>%s</li>'%e(f) for f in F)+'</ul><p class="small">%s Counts are made from the cards above, not from outside statistics.</p>'%e(NOTE)
# ---------- cards
LINKS={'collins-airports-2025':[('transporteu','the transport page for 30 countries')],'french-fridges-2026':[('freezers','the freezer attacks'),('evidence','the evidence tracker')],'ahold-delhaize-2026':[('reg2','the register 2025–2026')]}
def short_co(c):
    s=re.sub(r'\s*\(.*?\)','',c); s=re.split(r' - ',s)[0].strip()
    return s
def short_sv(s): return s if len(s)<=70 else s[:67].rsplit(' ',1)[0]+'…'
def card(x):
    y=x['sort'][:4]; sc=short_co(x['company'])
    t=' '.join([x['company'],x['service'],x['what'],x['what_nl'],x['cause'],x['cause_nl'],x['who'],x['where'],x['date'],x['europe']]).lower()
    s='<details class="og-card" data-kind="%s" data-cs="%s" data-year="%s" data-t="%s"><summary><span class="og-d">%s</span><b class="og-c">%s</b><span class="og-s">%s</span><span class="og-k og-k-%s">%s</span>%s</summary><div class="og-b">'%(x['kind'],x['cause_status'],y,e(t),e(x['date']),e(sc),e(short_sv(x['service'])),x['kind'],e(KIND[x['kind']]),tag(x['cause_status']))
    s+='<h4>What happened</h4><p>%s</p><p class="nl"><b>NL:</b> %s</p>'%(e(x['what']),e(x['what_nl']))
    if sc!=x['company']: s+='<p><b>Company:</b> %s. <b>Service:</b> %s</p>'%(e(x['company']),e(x['service']))
    elif x['service'] and len(x['service'])>70: s+='<p><b>Service:</b> %s</p>'%e(x['service'])
    s+='<p><b>Duration:</b> %s. <b>Where:</b> %s</p>'%(e(x['duration'].rstrip('.')),e(x['where'].rstrip('.')))
    s+='<h4>What caused it</h4><p>%s %s</p><p class="nl"><b>NL:</b> %s</p>'%(e(x['cause']),tag(x['cause_status']),e(x['cause_nl']))
    if x['kind']=='cyberattack' and x.get('who'):
        s+='<h4>Who is blamed</h4><p>%s %s</p>'%(e(x['who']),(tag('R',TW).replace('Reported','Formal attribution, contested') if x['id']=='french-fridges-2026' else tag(x['who_status'],TW)))
    if x['europe']: s+='<h4>Europe and Belgium</h4><p>%s</p>'%e(x['europe'])
    if x['id'] in LINKS: s+='<p class="small"><b>Also in this file:</b> '+', '.join('<a href="#%s">%s</a>'%(k,e(n)) for k,n in LINKS[x['id']])+'.</p>'
    s+='<h4>Sources</h4><ul class="og-src">'+''.join('<li><a href="%s" target="_blank" rel="noopener noreferrer">%s — %s</a>%s</li>'%(e(u['url']),e(u['publisher']),e(u['title']),(' <span class="small">(%s)</span>'%e(u['date'])) if u.get('date') else '') for u in x['sources'])+'</ul></div></details>'
    return s
years=sorted({x['sort'][:4] for x in main},reverse=True)
opt=lambda pairs:''.join('<option value="%s">%s</option>'%(a,e(b)) for a,b in pairs)
filters='''<div class="filters2 og-f" id="ogf" role="group" aria-label="Filter the outages">
<select data-f="kind" aria-label="Kind of outage"><option value="">All kinds</option>%s</select>
<select data-f="cs" aria-label="Status of the cause"><option value="">Any cause status</option>%s</select>
<select data-f="year" aria-label="Year"><option value="">All years</option>%s</select>
<input type="search" id="og-q" placeholder="Search company, place, cause…" aria-label="Search the outages">
<select id="og-sort" aria-label="Sort order"><option value="new">Newest first</option><option value="old">Oldest first</option></select>
</div><p class="small" id="og-count" aria-live="polite">%d of %d shown</p>'''%(opt([(k,KIND[k]) for k in ('technical','physical','cyberattack','unknown')]),opt([(k,T[k][0]) for k in 'CRKSN' if any(x['cause_status']==k for x in main)]),opt([(y,y) for y in years]),N,N)
SEC='''<section id="outages">
<h2>Global outages: when the world's biggest services went down</h2>
<p class="sub">1 January 2025 to 19 November 2026, plus background from 2024: %d outages of major online services and company systems. @@MIX@@</p>
<p class="nl"><b>NL:</b> 1 januari 2025 tot 19 november 2026, plus achtergrond uit 2024: %d storingen bij grote onlinediensten en bedrijfssystemen. @@MIXNL@@</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>An outage here means a big online service, network or company system that stopped working for many people at once. Each card shows two separate things: the cause, which is what happened, and for cyberattacks also who is blamed, which can be only a claim. The labels say how firm a statement is: Confirmed means the company or an authority said so, Reported means credible media said so, Claimed means only the attackers or an unverified party said so, Suspected means it is a guess, and Not published means no explanation has been given yet. The descriptions are in English, each with a Dutch summary.</p>
<p class="pb-nl"><b>NL:</b> Een storing betekent hier dat een grote onlinedienst, een netwerk of een bedrijfssysteem uitviel voor veel mensen tegelijk. Elke kaart toont twee aparte dingen: de oorzaak, dus wat er gebeurde, en bij cyberaanvallen ook wie de schuld krijgt, wat soms alleen een bewering is. De labels tonen hoe stevig een uitspraak is: Bevestigd betekent dat het bedrijf of een overheid het zei, Gemeld dat betrouwbare media het zeiden, Geclaimd dat alleen de aanvallers of een niet-geverifieerde partij het zeiden, Vermoed dat het een gok is, en Niet gepubliceerd dat er nog geen uitleg is. De beschrijvingen zijn in het Engels, elk met een Nederlandse samenvatting.</p></div>
<p class="small"><b>Scope:</b> unlike the rest of this file, which is about Europe, this page is worldwide by design: it lists big companies and services anywhere in the world, not only in Europe.</p>
<p class="small nl"><b>NL:</b> In tegenstelling tot de rest van dit dossier, dat over Europa gaat, is deze pagina bewust wereldwijd: ze toont grote bedrijven en diensten overal ter wereld, niet alleen in Europa.</p>
<h3>Key figures</h3>
<p class="small">Counted from the %d outages in the period below. The 2024 background items are not counted.</p>
<div class="statsx">%s</div>
<h3>The outages, newest first</h3>
%s
<div class="og-list" id="og-list">%s</div>
<details class="og-bg"><summary><b>Background: 2024 outages people still refer to</b> <span class="small">(%d)</span></summary><div class="og-list">%s</div></details>
%s
<p class="src">Sources: each card lists its own sources; the full list is below.</p>
</section>'''%(N,N,N,tiles,filters,''.join(card(x) for x in main),len(bg),''.join(card(x) for x in bg),pattern)
SEC=SEC.replace('@@MIX@@','%d were cyberattacks; %d were technical faults or changes at the companies themselves, %d were power or cooling failures, and for %d no cause has been published.'%(kc['cyberattack'],kc['technical'],kc['physical'],kc['unknown']))
SEC=SEC.replace('@@MIXNL@@','%d waren cyberaanvallen; %d waren technische fouten of wijzigingen bij de bedrijven zelf, %d waren stroom- of koelingsproblemen, en voor %d is geen oorzaak bekendgemaakt.'%(kc['cyberattack'],kc['technical'],kc['physical'],kc['unknown']))
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='outages')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
# ---------- nav, home, intro
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'k': 'outages'" not in t:
    m=re.search(r"\{'k': 'evidence'[^}]*\}, ",t); assert m
    t=t[:m.end()]+"{'k': 'outages', 'en': 'Global outages', 'nl': 'Wereldwijde storingen', 'src': ('R', 'outages')}, "+t[m.end():]
a='<a href="#intel">the intel desk</a>.'
if 'the global outages page' not in t:
    assert a in t; t=t.replace(' and <a href="#intel">the intel desk</a>.',', <a href="#intel">the intel desk</a> and <a href="#outages">the global outages page</a>.',1)
open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['outages']" not in t:
    t=t.rstrip()+'''
INTRO['outages']=("The biggest outages of online services since 2025, what caused each one, and who is blamed when it was an attack. Almost half were cyberattacks; the rest were the companies' own faults, power failures, or have no published cause.","De grootste storingen van onlinediensten sinds 2025, wat elke veroorzaakte, en wie de schuld krijgt bij een aanval. Bijna de helft waren cyberaanvallen; de rest waren eigen fouten van de bedrijven, stroomproblemen, of heeft geen bekendgemaakte oorzaak.")
'''
    open(l,'w',encoding='utf-8').write(t)
# ---------- css + js
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
CSS='''
.og-f{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 4px}.og-f input{font:inherit;font-size:13.5px;padding:7px 10px;border-radius:8px;border:1px solid var(--line);background:var(--paper);color:var(--ink);flex:1 1 200px;min-width:0;max-width:100%}
.og-list{display:flex;flex-direction:column;gap:8px;margin:8px 0}
.og-card{border:1px solid var(--line);border-radius:10px;background:var(--paper);overflow-wrap:anywhere}
.og-card>summary{cursor:pointer;list-style:none;display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;padding:10px 12px}
.og-card>summary::-webkit-details-marker{display:none}
.og-card>summary::before{content:"\\25B8";color:var(--accent);font-size:12px;transition:transform .15s}
.og-card[open]>summary::before{transform:rotate(90deg)}
.og-d{font-family:var(--f-mono);font-size:12px;color:var(--muted)}.og-s{font-size:13px;color:var(--muted);flex:1 1 160px;min-width:0}
.og-k{font-size:11.5px;padding:1px 8px;border-radius:999px;border:1px solid var(--line);background:var(--grey-soft);color:var(--ink)}
.og-k-cyberattack{background:var(--red-soft);border-color:var(--red)}.og-k-physical{background:var(--amber-soft);border-color:var(--amber)}.og-k-unknown{background:transparent;border-style:dashed}
.og-b{padding:0 12px 10px;border-top:1px solid var(--line)}.og-b h4{margin:12px 0 4px;font-size:13px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}.og-b p{margin:4px 0}
.og-src{margin:4px 0;padding-left:18px}.og-src li{margin:3px 0}
#p-outages .tag.t-none{text-decoration:none}
.og-bg{margin:14px 0;border:1px dashed var(--line);border-radius:10px;padding:8px 12px}.og-bg>summary{cursor:pointer}
@media(max-width:699px){#p-outages .statsx{grid-template-columns:repeat(2,minmax(0,1fr))}#p-outages .stx b{font-size:24px}#p-outages .og-f select{flex:1 1 40%}}
@media print{.og-card{break-inside:avoid}.og-card[open]>summary::before{content:""}}
'''
JS='''
/* og-filters */
(function(){const box=document.getElementById('ogf');if(!box)return;const list=document.getElementById('og-list');const cards=[...list.querySelectorAll('.og-card')];const cnt=document.getElementById('og-count');const q=document.getElementById('og-q'),so=document.getElementById('og-sort');
function apply(){const f={};box.querySelectorAll('select[data-f]').forEach(s=>{if(s.value)f[s.dataset.f]=s.value});const w=(q.value||'').toLowerCase().trim().split(/\\s+/).filter(Boolean);let n=0;
cards.forEach((c,i)=>{const ok=Object.keys(f).every(k=>c.dataset[k]===f[k])&&w.every(x=>c.dataset.t.indexOf(x)>-1);c.hidden=!ok;if(ok)n++;c.style.order=so.value==='old'?cards.length-i:i;});
if(cnt)cnt.textContent=n+' of '+cards.length+' shown';}
box.addEventListener('change',apply);q.addEventListener('input',apply);apply();})();
'''
if '.og-card' not in t:
    t=t.replace('</style>',CSS+'</style>',1); k=t.rindex('</script>'); t=t[:k]+JS+t[k:]
    open(a,'w',encoding='utf-8').write(t)
print('outages ok',N,len(bg),dict(kc),cconf,dict(wc),len(F))
