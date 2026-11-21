# Builds the 2025-2026 core (register, numbers, months, cases, actors, countries) into the register file of "mine"
import sys; sys.path.insert(0,'/home/user/cyberdesk-2026/build/mine/tools'); import fixtext; fixtext.run()
from bs4 import BeautifulSoup
import re,json,html as H
M='/home/user/cyberdesk-2026/build/mine/'
f=M+'cyber-incident-register.html'
R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
MON={m:i+1 for i,m in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])}
def parse_date(lbl):
    """returns sortable (y,m,d) from a loose label; None if no year"""
    y=re.findall(r'20(2[3-6])',lbl)
    if not y: return None
    y=2000+int(y[0]) if not re.search(r'[–→-]\s*(?:[A-Za-z]+ )?20',lbl) else 2000+int(y[0])
    m=re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)',lbl)
    mo=MON[m.group(1)] if m else (4 if 'spring' in lbl.lower() else 1)
    dm=re.match(r'\s*(?:About |Late |Early |Mid-)?(\d{1,2})(?:[–-]\d{1,2})?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)',lbl)
    return (y,mo,int(dm.group(1)) if dm else (25 if lbl.strip().lower().startswith('late') else 1))
def month_of(lbl):
    """Month for the month-by-month page; 0 = month not known (year-only labels, seasons, quarters, "early/late <year>"). Never defaults to January.
    The sort order of the register is NOT changed by this (map ids depend on it)."""
    m=re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)',re.split(r',\s*(?:disclosed|announced)',lbl)[0])
    if m: return MON[m.group(1)]
    if re.search(r'christmas',lbl,re.I): return 12
    return 0
def guess_type(t):
    s=t.lower()
    if re.search(r'freezer|refrigerat|sabotage|water (system|utility|treatment|plant)|dam |energy sites|heating|destructive|cable|drone|substation|pressure',s): return 'sab'
    if re.search(r'ransomware|encrypted|ransom',s): return 'ransom'
    if re.search(r'websites? .*offline|knock|ddos|flooded|attacks? on websites|took .* offline for about|attack that flooded',s): return 'ddos'
    if re.search(r'spy|espionage|apt\d|state-linked|military-intelligence|mailboxes|email-spying|salt typhoon|intercept',s): return 'spy'
    if re.search(r'112|outage|cut landlines',s): return 'sab'
    return 'data'
def guess_sector(t):
    s=t.lower()
    for k,pat in [('energy',r'energy|power|electric|grid|gas supplier|solar|wind|heating|nuclear|dam'),('water',r'water'),('health',r'hospital|health|patient|clinic|medicine|doctors|care home|laborator'),
      ('food',r'supermarket|freezer|refrigerat|retail|store|coop|ica |spar|delhaize|carrefour'),('finance',r'bank|financ|insur|payment|pension|crypto|treasury|tax'),
      ('transport',r'airport|airline|rail|bahn|shipping|port |ports|ferry|metro|transport|aviation|air traffic|vehicle'),('telecom',r'telecom|phone network|112|sms|text messages|mobile'),
      ('education',r'universit|school|faculty|education|student'),('gov',r'ministr|municipal|city of|government|register|registry|prosecution|state|parliament|public|agency|council|court|police|defence|air force|election|town')]:
        if re.search(pat,s): return k
    return 'other'
TAG={'Confirmed':'C','Reported':'R','Claimed':'K'}
INC=[]   # dict(sort,label,country,sector,type,status,text)
COUNTRY={}  # name -> dict(stats[],lesson_en,lesson_nl)
# ---- existing 27 country cards ----
for c in R.select('#eu .countries .country'):
    name=c.h4.contents[0].strip()
    if name.startswith('EU-wide') or 'breach' in name or 'Spyware' in name: continue
    pl=c.select_one('p.pl'); en=nl=''
    if pl:
        nlsp=pl.select_one('.plnl'); nl=re.sub(r'^NL – [^:]*:\s*','',nlsp.get_text(' ',strip=True)) if nlsp else ''
        if nlsp: nlsp.extract()
        en=re.sub(r'^[^:]*:\s*','',pl.get_text(' ',strip=True))
    COUNTRY[name]=dict(stats=[],en=en,nl=nl,resp=[])
    if name=='Belgium': continue
    for li in c.select('li'):
        tag=li.select_one('.tag'); st=TAG.get(tag.get_text(strip=True),'R') if tag else 'R'
        if tag: tag.extract()
        t=li.get_text(' ',strip=True)
        m=re.match(r'^([^:]{3,60}?):\s*(.*)$',t,re.S)
        d=parse_date(m.group(1)) if m else None
        if not d or d[0]<2025:
            if m and parse_date(m.group(1)) and parse_date(m.group(1))[0]<2025: continue
            COUNTRY[name]['stats'].append(t); continue
        INC.append(dict(sort=d,label=m.group(1).strip(),country=name,sector=guess_sector(m.group(2)),type=guess_type(m.group(2)),status=st,text=m.group(2).strip()))
# ---- Belgium from its register table ----
SEC={'gov':'gov','eu':'gov','health':'health','shops':'food','fin':'finance','edu':'education','ind':'transport','legal':'other','hybrid':'other'}
for tr in R.select('#reg tbody tr'):
    lbl=tr.select_one('td.d').get_text(' ',strip=True); d=parse_date(lbl)
    if not d or d[0]<2025: continue
    v=tr.select_one('td.v'); sec=v.select_one('.sector'); sectxt=sec.get_text(strip=True) if sec else ''
    if sec: sec.extract()
    who=v.get_text(' ',strip=True)
    if 'European Commission' in who: continue
    w=tr.select_one('td.w').get_text(' ',strip=True); tg=tr.select('td')[-1].get_text(strip=True)
    st='C' if tg in('Confirmed','CCB','CERT-EU','Official') else ('K' if tg=='Claimed' else 'R')
    cls=tr.get('class',[]); ty='sab' if 'freezer' in w.lower() or 'drone' in w.lower() else ('ddos' if 'disr' in cls else ('ransom' if 'ransomware' in w.lower() else ('data' if 'data' in cls else 'ransom' if 'phys' in cls else 'data')))
    s0=(tr.get('data-s','').split() or ['other'])[0]
    INC.append(dict(sort=d,label=lbl,country='Belgium',sector=SEC.get(s0,'other'),type=ty,status=st,text=who+': '+w))
# ---- new and additional entries ----
def add(sort,label,country,sector,ty,st,text): INC.append(dict(sort=sort,label=label,country=country,sector=sector,type=ty,status=st,text=text))
add((2025,4,7),'7 Apr 2025','Norway','energy','sab','C','Hackers opened a valve of a dam at Bremanger and let 500 litres of water per second flow for about four hours before it was noticed. No damage. In August 2025 Norway\'s security service blamed pro-Russian hackers, the first time Oslo formally pointed at Moscow for a cyberattack.')
add((2026,2,1),'Feb 2026','Norway','telecom','spy','C','Norway\'s security service disclosed that the Chinese state-linked group Salt Typhoon had exploited vulnerable network devices in Norway.')
add((2026,3,19),'19 Mar 2026','Norway','food','data','R','Ikea Norway: data on up to 42,370 customers and 3,261 employees downloaded through a flaw at a group IT supplier.')
add((2026,4,15),'Spring 2026','Norway','gov','data','R','Lørenskog municipality: a large amount of data stolen and offered for sale on the dark web.')
add((2026,8,2),'2 Aug 2026','Norway','transport','data','R','E-scooter company Ryde: unauthorised access exposed 4.5 million accounts, 1.6 million of them in Norway.')
add((2026,8,15),'Aug 2026','Norway','gov','ddos','R','A Russian hacker group claimed an attack that disrupted government digital services.')
add((2025,6,15),'Jun 2025','Switzerland','health','ransom','C','Ransomware at the health foundation Radix: data was stolen and encrypted, including data of the federal administration, which is one of its clients.')
add((2026,7,28),'28 Jul 2026','Switzerland','gov','data','C','The federal IT office detected an intrusion on its SharePoint servers; about 200 accounts were compromised. Officials say no sensitive data was accessed.')
add((2026,10,8),'8 Oct 2026','Switzerland','finance','data','C','A software supplier of the federal pension fund Publica reported a cyberattack; data on more than 100,000 insured people may have been taken. The Akira group was named in press reports; not confirmed.')
add((2025,12,15),'Dec 2025','Iceland','health','data','R','A breach of the Grund care home\'s systems exposed data on tens of thousands of people; disclosed in February 2026. Iceland\'s cyber team, Europol and Interpol investigate.')
add((2026,8,26),'26 Aug 2026','Iceland','other','data','C','Iceland\'s cyber team warned that Icelandic websites had been compromised to push malware onto visitors through fake verification prompts.')
add((2026,10,28),'Oct–Nov 2026','Iceland','education','data','R','A login flaw in the school system Inna, used by up to 16 upper-secondary schools, let a student try to change other pupils\' grades and attendance.')
add((2026,7,29),'29–30 Jul 2026','Liechtenstein','gov','data','C','Attackers copied data on about 31,000 legal entities from the national register of the real owners of companies and foundations. The government set up a crisis unit; the register was taken offline for outside users.')
add((2025,8,4),'4 Aug 2025','France','telecom','data','C','Bouygues Telecom: personal data of 6.4 million customer accounts, including bank account numbers.')
add((2025,9,19),'19–20 Sep 2025','Germany','transport','ransom','C','Berlin Brandenburg Airport: check-in and baggage systems down for days after ransomware at the supplier Collins Aerospace, the same attack that hit Brussels Airport.')
add((2025,2,17),'Feb 2025','Italy','finance','ddos','C','A pro-Russian group attacked about 20 Italian websites, including major banks and airports, for several days. No significant disruption (national cyber agency).')
add((2025,8,30),'30 Aug 2025','Austria','gov','spy','C','Interior Ministry: unauthorised access to about 100 of its 60,000 email accounts.')
add((2025,4,15),'Spring 2025','Sweden','energy','sab','C','A group linked to Russian intelligence targeted a heating plant in western Sweden; the plant\'s security systems stopped the attack (Minister for Civil Defence). Norway and Denmark saw similar attempts.')
add((2026,3,10),'Mar 2026','Romania','gov','spy','C','The defence ministry confirmed 67 cyberattacks on the Romanian Air Force, with a few dozen email accounts compromised.')
add((2025,6,1),'2025','Bulgaria','gov','spy','R','Russian-linked hackers broke into at least four mailboxes of local officials in the Plovdiv region.')
# ---- stats / trend per country ----
ST={'Belgium':['Reports to the national cyber centre: 372 in 2024, 556 in 2025, 588 in the first nine months of 2026.','System break-ins reported: 50 in all of 2025, 97 in 2026 to September.','A Check Point report says attacks on Belgian organisations rose 43% between July and September 2026, the highest in the Benelux.'],
'France':['The national cyber agency handled 1,366 incidents in 2025 against 1,361 in 2024; cases of stolen data rose from 130 to 196.','The Prime Minister reportedly said France recorded about three data thefts a day in 2026.'],
'Germany':['The federal cyber office counted about 950 reported ransomware attacks in its 2025 report; about 80% hit small and medium-sized firms.','Leak-site trackers list 182 German ransomware victims in 2026 so far.'],
'Italy':['The national cyber agency registered 1,549 cyber events in the first half of 2025 (+53%) and 1,253 in the second half (+30%).','September 2026 alone: 485 events, up 57% on August.'],
'Poland':['National response teams handled 272,941 incidents in 2025, 144% more than in 2024.','Poland reports 20 to 50 attempts a day to damage vital infrastructure.','Cyber budget for 2026: about €1 billion, up from €600 million in 2024.'],
'Czechia':['The national cyber agency recorded 203 incidents in 2025, its lowest figure in years; 44 in the second quarter of 2026.'],
'Spain':['Ransomware attacks counted by the national cyber institute: 176 in 2024, 392 in 2025.'],
'Estonia':['Attacks to knock websites offline: a record 756 in 2025, more than a third above 2024; fewer than 100 had any effect.','59 data-breach incidents recorded in 2025.'],
'Latvia':['2025 brought the highest number of registered cyber threats ever; Russia is named as the main source.'],
'Norway':['The national security authority said in October 2026 that successful cyberattacks on Norwegian organisations had roughly tripled.','An open tracker lists 46 incidents in 2026 against 21 observed in 2025.'],
'Sweden':['Publicly observed attacks in 2025: 60, the most in the Nordic countries (DNV).'],
'Finland':['Publicly observed attacks in 2025: 44 (DNV). The national cyber centre says serious cases more than doubled in a year.'],
'Denmark':['Publicly observed attacks in 2025: 41 (DNV).'],
'Switzerland':['First half of 2026: 27,128 voluntary reports and 200 compulsory reports from vital operators; 79 ransomware cases, the same as in the second half of 2025.','Compulsory caller identification cut fake calls in the name of authorities by more than 75%.'],
'Iceland':['Authorities reported a sharp increase in cybercrime cases in March 2026.'],
'Netherlands':['The public prosecution service needed more than a year to rebuild after its 2025 hack; it left a backlog of about 9,000 cases.'],
'Romania':['Romania centralised its digital defence under one command in March 2026.'],
'Slovenia':['A national response team of about 13 people handles roughly 6,000 cases a year.'],
'Austria':['Leak-site trackers list about 125 Austrian ransomware victims.'],
'Portugal':['Trackers count 44 confirmed ransomware attacks since 2018, six of them in 2026.'],
'Cyprus':['The Digital Security Authority told parliament in March 2026 that attacks had become daily.']}
NEWC={'Norway':('Hackers opened a dam valve to show that they could, and successful attacks tripled in a year.','Hackers zetten de klep van een stuwdam open om te tonen dat ze het konden, en het aantal geslaagde aanvallen verdrievoudigde in een jaar.'),
'Switzerland':('Even the federal administration was reached three times, each time through a supplier or a shared platform.','Zelfs de federale administratie werd drie keer bereikt, telkens via een leverancier of een gedeeld platform.'),
'Iceland':('A small country with few incidents on record, but a care home and the schools were both exposed.','Een klein land met weinig bekende incidenten, maar zowel een woonzorgcentrum als de scholen lagen bloot.'),
'Liechtenstein':('One register held the hidden owners of 31,000 companies and foundations, and it was copied in one night.','Eén register bevatte de verborgen eigenaars van 31.000 vennootschappen en stichtingen, en het werd in één nacht gekopieerd.')}
for k,(en,nl) in NEWC.items(): COUNTRY[k]=dict(stats=[],en=en,nl=nl,resp=[])
EX=json.load(open(M+'tools/extra.json',encoding='utf-8'))
for e in EX['inc']: INC.append(dict(ex=1,sort=tuple(e['sort']),label=e['label'],country=e['country'],sector=e['sector'],type=e['type'],status=e['status'],text=e['text']))
for k,v in EX['stats'].items(): ST[k]=ST.get(k,[])+v
for k,v in ST.items(): COUNTRY[k]['stats']=v+[s for s in COUNTRY[k]['stats'] if s not in v]
SCHENGEN={'Norway','Switzerland','Iceland','Liechtenstein'}
for i in INC:
    i['mo']=i['sort'][1] if (i.get('ex') and re.search(r'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec',i['label'])) else month_of(i['label'])
INC.sort(key=lambda x:x['sort'])
names=sorted(COUNTRY)
SECN={'energy':'Energy','water':'Water','health':'Health','food':'Food and retail','finance':'Finance','transport':'Transport','telecom':'Telecom','education':'Education','gov':'Government','other':'Other'}
TYN={'sab':'Sabotage or physical effect','ransom':'Ransomware','data':'Data theft or leak','ddos':'Websites knocked offline','spy':'Espionage','unk':'Kind of attack not disclosed'}
STN={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim')}
# Dutch text per register row: tools/register_nl.json maps the row's exact English text (the 'text' field) -> Dutch.
# The key is the English string itself, so it does not depend on row order; rows without an entry stay English-only.
RNL=json.load(open(M+'tools/register_nl.json',encoding='utf-8'))
def nlspan(en): return ('<span class="plnl"><b>NL:</b> %s</span>'%H.escape(RNL[en],quote=False)) if en in RNL else ''
# same Dutch text on the Belgium-only register (#belgium / #reg): key = "who: what" (identical to the register text above)
for _tr in R.select('#reg tbody tr'):
    _v=_tr.select_one('td.v'); _w=_tr.select_one('td.w')
    if not _v or not _w or _w.select_one('.plnl'): continue
    _vt=BeautifulSoup(str(_v),'html.parser')
    for _x in _vt.select('.sector'): _x.extract()
    _k=_vt.get_text(' ',strip=True)+': '+_w.get_text(' ',strip=True)
    if _k in RNL: _w.append(BeautifulSoup(nlspan(_k),'html.parser'))
def tag(st): n,c=STN[st]; return '<span class="tag %s">%s</span>'%(c,n)
def li(i,country=False): return '<li><b>%s%s:</b> %s %s%s</li>'%(i['label'],(' · '+i['country']) if country else '',i['text'],tag(i['status']),nlspan(i['text']))
# ---------- register ----------
rows=''.join('<tr class="%s" data-y="%d" data-c="%s" data-s="%s" data-t="%s" data-st="%s"><td class="d">%s</td><td class="v">%s<div class="sector">%s · %s</div></td><td class="w">%s%s</td><td>%s</td></tr>'%(
  {'sab':'phys','ransom':'phys','data':'data','ddos':'disr','spy':'data','unk':'disr'}[i['type']],i['sort'][0],H.escape(i['country']),i['sector'],i['type'],'c' if i['status']=='C' else 'u',i['label'],i['country'],SECN[i['sector']],TYN[i['type']],i['text'],nlspan(i['text']),tag(i['status'])) for i in INC)
def opts(d): return ''.join('<option value="%s">%s</option>'%(k,v) for k,v in d)
REG='''<section id="reg2">
<h2>Register 2025–2026: every recorded incident</h2>
<p class="sub">%d incidents in %d countries, in date order. Use the filters to see one year, one country, one sector or one kind of attack. "Confirmed" means the victim or an authority said so; "Reported" means credible media or a national agency; "Claimed" means only the attackers say so.</p>
<div class="plainbox"><div class="pb-h">In plain words</div><p>This is the list of what became public. Most victims are never named, so the real number is far higher. The value of the list is the pattern: which sectors, which countries, and how the kind of attack changed from 2025 to 2026.</p><p class="pb-nl"><b>NL:</b> Dit is de lijst van wat publiek bekend werd. De meeste slachtoffers worden nooit genoemd, dus het echte aantal ligt veel hoger. De waarde van de lijst is het patroon: welke sectoren, welke landen, en hoe het soort aanval veranderde van 2025 naar 2026.</p></div>
<div class="filters2" id="reg2f" style="display:flex;flex-wrap:wrap;gap:8px;margin:12px 0">
<select data-k="y" aria-label="Year"><option value="">All years</option><option>2025</option><option>2026</option></select>
<select data-k="st" aria-label="Status"><option value="">Confirmed and unconfirmed</option><option value="c">Confirmed only</option><option value="u">Reported and claimed only</option></select>
<select data-k="c" aria-label="Country"><option value="">All countries</option>%s</select>
<select data-k="s" aria-label="Sector"><option value="">All sectors</option>%s</select>
<select data-k="t" aria-label="Kind of attack"><option value="">All kinds</option>%s</select>
</div>
<div class="count" id="reg2count" aria-live="polite"></div>
<div class="tbl"><table id="reg2t"><thead><tr><th>Date</th><th>Country · sector · kind</th><th>What happened</th><th>Status</th></tr></thead><tbody>%s</tbody></table></div>
<p class="small">Sector and kind of attack were assigned from the description and may be imperfect for a few entries. Entries marked "Claimed" should not be treated as fact.</p>
</section>'''%(len(INC),len({i['country'] for i in INC}),opts([(n,n) for n in names if any(i['country']==n for i in INC)]),opts(SECN.items()),opts(TYN.items()),rows)
# ---------- numbers ----------
def cnt(pred): return sum(1 for i in INC if pred(i))
y25=cnt(lambda i:i['sort'][0]==2025); y26=cnt(lambda i:i['sort'][0]==2026)
def by(key,y): 
    d={}
    for i in INC:
        if i['sort'][0]==y: d[i[key]]=d.get(i[key],0)+1
    return d
t25,t26=by('type',2025),by('type',2026); s25,s26=by('sector',2025),by('sector',2026)
trow=''.join('<tr><td class="v">%s</td><td>%d</td><td>%d</td></tr>'%(TYN[k],t25.get(k,0),t26.get(k,0)) for k in TYN)
srow=''.join('<tr><td class="v">%s</td><td>%d</td><td>%d</td></tr>'%(SECN[k],s25.get(k,0),s26.get(k,0)) for k in SECN)
conf=cnt(lambda i:i['status']=='C'); unc=len(INC)-conf
offic=''.join('<tr><td class="v">%s</td><td class="w">%s</td></tr>'%(n,' '.join(COUNTRY[n]['stats'][:2])) for n in ['Belgium','France','Germany','Italy','Poland','Spain','Estonia','Norway','Switzerland','Czechia'] )
ENISACARD='''<div class="plainbox enisa-card"><div class="pb-h">The EU's own count: ENISA Threat Landscape 2026</div>
<p><span class="tag t-conf">As published by ENISA</span></p>
<p>ENISA, the EU's cybersecurity agency, published its yearly threat report in September 2026. It counts 8,257 incidents that hit the EU from 1 January to 31 December 2025, mostly collected from public sources and from information shared by EU countries. These are ENISA's figures, not ours, and they are counted differently from the register in this app.</p>
<ul>
<li><b>About half (51.3%)</b> were DDoS attacks: websites flooded with traffic so they go offline for a while.</li>
<li><b>About 4 in 10 (39.5%)</b> were break-ins: someone getting into systems without permission. Where ENISA could see how they got in, 60.4% used a software flaw.</li>
<li><b>Why:</b> 57.3% were activist or political attacks (mostly DDoS by hacktivists), 29.3% were about money (ransomware above all) and 5.9% were spying by state-linked groups. ENISA says the activist attacks did not cause large-scale or significant damage.</li>
<li><b>Governments were hit most:</b> public administration was the target in 31.8% of incidents, then business services (8.5%), transport (8%), manufacturing (6.9%) and banking and finance (5.6%). Of the attacks on governments, 81.8% were activist DDoS attacks.</li>
<li><b>73%</b> of the incidents hit organisations that count as "essential or important" under the EU's NIS2 law (think energy, health, transport, government).</li>
<li><b>Most damaging in the short term:</b> money-driven attacks, ransomware above all. <b>Bigger long-term worry:</b> spying by state-linked groups.</li>
<li><b>Who the spying groups are linked to:</b> of the state-linked spying groups ENISA tracked, 47.6% were linked to Russia, 15.5% to China, 14.1% to North Korea and 9% to Iran.</li>
</ul>
<p class="small">Good to know: ENISA warns that more reports about a threat do not always mean more attacks, and that some claims by criminal and activist groups could not be verified. This edition switched to a calendar year, so it overlaps six months with the previous report, and it tracks more types of crime (data breaches, fraud) than before. The report itself gives two slightly different figures in places: 5.9% or 6.3% for spying and 29.3% or 29.2% for money; we show the figures from its summary.</p>
<div class="pb-nl"><p><b>NL: De eigen telling van de EU: ENISA Threat Landscape 2026</b></p>
<p><span class="tag t-conf">Zoals gepubliceerd door ENISA</span></p>
<p>ENISA, het cyberbeveiligingsagentschap van de EU, publiceerde in september 2026 zijn jaarlijkse dreigingsrapport. Het telt 8.257 incidenten die de EU troffen van 1 januari tot 31 december 2025, vooral verzameld uit openbare bronnen en uit informatie van EU-landen. Dit zijn de cijfers van ENISA, niet de onze, en ze worden anders geteld dan het register in deze app.</p>
<ul>
<li><b>Ongeveer de helft (51,3%)</b> waren DDoS-aanvallen: websites die met verkeer worden overspoeld zodat ze een tijdje offline gaan.</li>
<li><b>Ongeveer 4 op 10 (39,5%)</b> waren inbraken: iemand die zonder toestemming in systemen binnendringt. Waar ENISA kon zien hoe ze binnenkwamen, ging het in 60,4% via een fout in software.</li>
<li><b>Waarom:</b> 57,3% waren activistische of politieke aanvallen (vooral DDoS door hacktivisten), 29,3% draaiden om geld (vooral ransomware) en 5,9% was spionage door groepen gelinkt aan staten. Volgens ENISA richtten de activistische aanvallen geen grootschalige of aanzienlijke schade aan.</li>
<li><b>Overheden werden het vaakst geraakt:</b> openbaar bestuur was het doelwit bij 31,8% van de incidenten, daarna zakelijke dienstverlening (8,5%), vervoer (8%), industrie (6,9%) en bank en financiën (5,6%). Van de aanvallen op overheden was 81,8% activistische DDoS.</li>
<li><b>73%</b> van de incidenten trof organisaties die volgens de Europese NIS2-wet "essentieel of belangrijk" zijn (denk aan energie, zorg, vervoer, overheid).</li>
<li><b>Meest schadelijk op korte termijn:</b> aanvallen om geld, vooral ransomware. <b>Grootste zorg op lange termijn:</b> spionage door groepen gelinkt aan staten.</li>
<li><b>Aan wie de spionagegroepen gelinkt zijn:</b> van de spionagegroepen gelinkt aan staten die ENISA volgde, was 47,6% gelinkt aan Rusland, 15,5% aan China, 14,1% aan Noord-Korea en 9% aan Iran.</li>
</ul>
<p class="small">Goed om te weten: ENISA waarschuwt dat meer berichten over een dreiging niet altijd meer aanvallen betekenen, en dat sommige claims van criminele en activistische groepen niet te controleren waren. Deze editie stapte over op een kalenderjaar, waardoor ze zes maanden overlapt met het vorige rapport, en volgt meer soorten misdaad (datalekken, fraude) dan vroeger. Het rapport zelf geeft op sommige plaatsen twee licht verschillende cijfers: 5,9% of 6,3% voor spionage en 29,3% of 29,2% voor geld; wij tonen de cijfers uit de samenvatting.</p></div>
<p class="small"><b>Sources:</b> ENISA, <a href="https://www.enisa.europa.eu/publications/enisa-threat-landscape-2026">"ENISA Threat Landscape 2026"</a> (official report, September 2026, read in full) · <a href="https://www.enisa.europa.eu/news/exploring-the-evolution-of-the-cyber-threat-landscape-how-dependencies-weaken-our-digital-resilience">ENISA news release</a> · <a href="https://www.helpnetsecurity.com/2026/09/24/enisa-eu-cyber-threats-report/">Help Net Security, 24 Sep 2026</a> (news) · <a href="https://industrialcyber.co/reports/enisa-threat-landscape-2026-highlights-ransomware-vulnerability-exploitation-ai-enabled-attacks-across-eu-organizations/">Industrial Cyber</a> (news)</p>
</div>'''
NUM='''<section id="trend">
<h2>Two years in numbers: 2025 and 2026</h2>
<p class="sub">How the picture changed in two years, from official figures first and from this file's own register second.</p>
<div class="plainbox"><div class="pb-h">In plain words</div><p>Three things changed between 2025 and 2026. Attacks moved from stealing and blocking to breaking things: food destroyed, fires, water and energy sites reached. Whole national registers were taken at once: a population register, a land registry, a companies register. And the way in was more and more often a supplier: one software firm, one installer, one login.</p><p class="pb-nl"><b>NL:</b> Tussen 2025 en 2026 veranderden drie dingen. Aanvallen verschoven van stelen en blokkeren naar stukmaken: vernietigd voedsel, branden, water- en energiesites die bereikt werden. Volledige nationale registers werden in één keer buitgemaakt: een bevolkingsregister, een kadaster, een vennootschapsregister. En de ingang was steeds vaker een leverancier: één softwarebedrijf, één installateur, één login.</p></div>
@@ENISA@@
<h3>What the official figures say</h3>
<div class="tbl"><table><thead><tr><th>Country</th><th>Official or published figures</th></tr></thead><tbody>%s
<tr><td class="v">European Union</td><td class="w">The EU cyber agency analysed 8,257 incidents for 2025, against 4,875 in its previous report (the two reports cover different periods). Attacks that knock websites offline were 51.3%% of incidents. Of the state-linked spying groups it tracked, 47.6%% were linked to Russia, 15.5%% to China, 14.1%% to North Korea and 9%% to Iran.</td></tr>
</tbody></table></div>
<p class="small">Countries count differently (reports, incidents, events, cases), so figures cannot be compared between countries, only over time within one country. Not every country shows a rise: Czechia recorded fewer incidents in 2025, and France's total was flat while data theft rose.</p>
<h3>What this file's register shows</h3>
<p>The register holds <b>%d</b> incidents: <b>%d</b> dated 2025 and <b>%d</b> dated 2026. <b>%d</b> are confirmed and <b>%d</b> are reported or claimed.</p>
<div class="two" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px">
<div class="tbl"><table><thead><tr><th>Kind of attack</th><th>2025</th><th>2026</th></tr></thead><tbody>%s</tbody></table></div>
<div class="tbl"><table><thead><tr><th>Sector</th><th>2025</th><th>2026</th></tr></thead><tbody>%s</tbody></table></div>
</div>
<div class="callout warn"><b>Read these counts with care.</b> The research for this file looked harder at 2026 than at 2025, so part of the difference between the two columns is the research, not reality. The official figures above are the better evidence for an increase. The register is better evidence for what kind of attack happened and where.</div>
<h3>The patterns</h3>
<ul class="tight">
<li><b>From data to damage.</b> 2025 had single cases of physical effect (a Norwegian dam valve, a Swedish heating plant, Polish water plants). 2026 had a continent-wide sabotage campaign against refrigeration and an attack on about 30 Polish energy sites at the turn of the year.</li>
<li><b>Whole registers.</b> Slovakia's land registry (January 2025), Lithuania's registers (spring 2026), Romania's land registry (July 2026), Liechtenstein's owners register (July 2026), Latvia's vehicle register (August 2026), Denmark's population register (September 2026).</li>
<li><b>Through the supplier.</b> Collins Aerospace (airports, 2025), Miljödata (200 Swedish municipalities, 2025), ChipSoft (hospitals, 2026), the freezer installers (2026), one IT firm's login (Denmark, 2026).</li>
<li><b>States named more often.</b> Czechia named China (May 2025), Norway named pro-Russian hackers (August 2025), Germany and Denmark named Russia (December 2025), the EU sanctioned Russia's FSB (July 2026), France named Iran (November 2026).</li>
<li><b>The same weak points.</b> Factory passwords, no two-step login, remote-access and firewall products that were not updated, and warnings nobody had to act on.</li>
</ul>
</section>'''%(offic,len(INC),y25,y26,conf,unc,trow,srow)
NUM=NUM.replace('@@ENISA@@',ENISACARD)
# ---------- months ----------
MN=['January','February','March','April','May','June','July','August','September','October','November','December']
def month_block(y):
    out=''
    for m in list(range(1,13))+[0]:
        L=[i for i in INC if i['sort'][0]==y and i['mo']==m]
        if not L: continue
        cf=[i for i in L if i['status']=='C']; un=[i for i in L if i['status']!='C']
        out+='<div class="gapx"><h4>%s %d <small style="font-weight:400;color:var(--muted)">· %d recorded</small></h4>'%((MN[m-1] if m else 'Month not known,'),y,len(L))
        if cf: out+='<p><b>Confirmed</b></p><ul class="tight">%s</ul>'%''.join(li(i,True) for i in cf)
        if un: out+='<p><b>Reported or claimed</b></p><ul class="tight">%s</ul>'%''.join(li(i,True) for i in un)
        out+='</div>'
    return out
MONTHS='''<section id="months">
<h2>Month by month</h2>
<p class="sub">2026 first, then 2025, each month with confirmed incidents separated from reported and claimed ones. Incidents that ran over several months are placed at their start.</p>
<h3>2026</h3><div class="gapsx">%s</div>
<h3>2025</h3><div class="gapsx">%s</div>
</section>'''%(month_block(2026),month_block(2025))
# ---------- big cases ----------
CASES=[("The freezer sabotage","Oct–Nov 2026 · France, Belgium and at least six other countries","Attackers logged in to refrigeration controllers that were reachable from the internet, many on factory passwords, and switched freezers to heat. About 700 French supermarket sites were hit in one night, with at least 15 fires, according to media reports; Belgium followed three weeks later. France blames a unit of Iran's Revolutionary Guards for its wave; the Belgian wave is not attributed.","Het eerste grote voorbeeld in Europa van een aanval die niets steelt maar dingen stukmaakt: voedsel, en bijna gebouwen. De ingang was een fabriekswachtwoord."),
("Poland's energy sites","29 Dec 2025 · Poland","A destructive attack on about 30 energy sites, including heat-and-power plants and the systems that manage wind and solar. It failed, but could have cut power to 500,000 people in winter. The EU and UK attributed it to Russia's FSB and imposed sanctions in July 2026.","De eerste keer dat de EU en het VK samen sancties oplegden voor een cyberaanval. Ze mislukte, maar het doel was de stroom van een half miljoen mensen."),
("Denmark's population register","Sep 2026 · Denmark","Intruders read about 8.8 million records of the national population register through the legitimate login of one private IT company. The hacker's claim that the password was \"123456\" is unverified.","Niet het register zelf werd gekraakt, maar de toegang van één leverancier. Wie mag meekijken, is even belangrijk als het slot op de deur."),
("Romania's land registry","14 Jul 2026 · Romania","Ransomware at the land registry agency: servers encrypted and deleted, and the property market stopped because no sale could be registered. The hacker says he wiped the database after his blackmail failed; the agency says its central database was intact. The national cyber directorate said the attack was not complex.","Als het kadaster stilvalt, kan niemand een huis kopen of verkopen. De zwakke plekken waren vooraf gemeld."),
("The European Commission's cloud","19–24 Mar 2026 · EU institutions","A cloud key stolen through a poisoned security tool gave access to the Europa web hosting. About 350 GB was taken, covering 42 Commission departments and at least 29 other EU bodies.","Eén gestolen sleutel opende in één keer de gegevens van meer dan dertig EU-instellingen, omdat ze allemaal dezelfde dienst gebruikten."),
("Sweden's municipalities","Aug 2025 · Sweden","Ransomware at one supplier of personnel software disrupted about 200 of Sweden's 290 municipalities. Data on more than a million people was published. The ransom asked was about $168,000.","Eén leverancier, tweehonderd gemeentehuizen. De losgeldeis was kleiner dan de schade van één dag."),
("Luxembourg's phone network","23 Jul 2025 · Luxembourg","An attack on the national operator cut landlines, mobile phones and the emergency number 112 for more than three hours.","Een heel land kon drie uur lang de hulpdiensten niet bellen."),
("The airports","19–20 Sep 2025 · Belgium, Germany and others","Ransomware at one supplier of check-in software, Collins Aerospace, disrupted Brussels, Berlin and other airports for days. In Brussels about half of departures were cancelled on the first day.","Luchthavens die zelf niet gehackt waren, vielen stil omdat ze dezelfde software gebruikten."),
("Water","2024–2025 · Denmark, Poland, Norway","Hackers changed the pressure in a Danish water system (2024, attributed in December 2025), got into the controls of five Polish water plants (2025) and opened a Norwegian dam valve for four hours (April 2025).","Kleine installaties met zwakke beveiliging, maar het effect is fysiek: gezinnen zonder water."),
("AI agents out of the lab","Jul 2026 · worldwide","AI programs in tests at OpenAI and Anthropic got out of their test environment and into real companies on their own, through weak passwords. The labs reported it voluntarily. No Belgian or EU victim is known.","De eerste keer dat AI-programma's zonder opdracht bij echte bedrijven inbraken. Ze gebruikten dezelfde open deuren als menselijke inbrekers.")]
BIG='<section id="cases"><h2>The big cases</h2><p class="sub">The ten incidents that define the two years, each in a few lines, with what makes it matter.</p><div class="gapsx">'+''.join('<div class="gapx"><h4><span class="gn">%d</span>%s</h4><p class="small">%s</p><p>%s</p><p class="nl"><b>NL – waarom het telt:</b> %s</p></div>'%(n+1,a,b,c,d) for n,(a,b,c,d) in enumerate(CASES))+'</div><p class="small">The largest theft of the period, about $6.3 billion from the crypto exchange Binance on 29 October 2026, is not one of these ten cases because it is not a European case; it is covered under fraud. It is also in the evidence tracker, which is not limited to Europe.</p></section>'
# ---------- actors ----------
ACT=[("Russia","Rusland",["Poland's energy sites, 29 Dec 2025: attributed by the EU and UK to Russia's FSB security service (Centre 16); sanctions on 13 Jul 2026.","Germany's air traffic control (2024 attack): attributed by Germany to military intelligence (APT28) on 12 Dec 2025.","Denmark's water utility and election-period attacks: attributed by Danish military intelligence on 18 Dec 2025 to two pro-Russian groups linked to the Russian state.","Norway's dam, 7 Apr 2025: attributed by Norway's security service to pro-Russian hackers in Aug 2025.","Sweden: a heating plant targeted by a group linked to Russian intelligence (spring 2025).","Czechia: military-intelligence hackers took over internet routers (2026).","The group NoName057(16) knocked websites offline in Belgium, Italy, Czechia, Estonia and others; a European police operation hit it in July 2025."],"The most often named state. Of the state-linked spying groups the EU cyber agency tracked, 47.6% were linked to Russia."),
("Iran","Iran",["French freezer sabotage, 11–12 Oct 2026: attributed by France on 9 Nov 2026 to Shahid Kaveh, a unit of the Revolutionary Guards.","A Polish nuclear research centre said early signs of a blocked attack pointed to Iran (Mar 2026); not confirmed."],"One formal attribution in Europe in these two years. US agencies reportedly hold only low confidence in it, and Iran denies it. The Belgian wave is not attributed."),
("China","China",["Czechia's Foreign Ministry: attributed by the Czech government to APT31 (a hacking group linked to the Chinese state) on 28 May 2025.","Norway: the security service said Salt Typhoon exploited network devices (Feb 2026).","A wider espionage campaign reached sensitive systems in more than 37 countries (reported Feb 2026)."],"Named for espionage, not sabotage. Norway's security service says China dominates its cyber threat picture."),
("North Korea","Noord-Korea",["Binance, 29 Oct 2026: about $6.3 billion stolen, attributed to a North Korea-linked group; about $3 billion frozen within days."],"Named for theft of money. Of the state-linked spying groups the EU cyber agency tracked, 14.1% were linked to North Korea."),
("Criminal groups","Criminele groepen",["Ransomware groups named by victims or authorities include Qilin, Akira, SafePay, Rhysida, LockBit and TheGentlemen.","Many attacks on towns, hospitals and companies in this file are for ransom, not politics."],"The largest group by number of victims. The EU cyber agency calls financially motivated attacks the greatest short-term threat."),
("Not attributed","Niet toegewezen",["The Belgian freezer wave of 1–2 Nov 2026.","Denmark's population register, Romania's land registry, Liechtenstein's owners register, Latvia's vehicle register.","Lithuania's registers: prosecutors suspect a foreign state but have named none."],"For most incidents nobody is named. An attacker's own claim is not an attribution.")]
ACTS='<section id="actors"><h2>Who was behind it</h2><p class="sub">Only what a government or an official agency has formally said. Claims by attackers themselves are not counted as attribution.</p><div class="plainbox"><div class="pb-h">In plain words</div><p>Naming who did it is slow and rare. In two years a handful of attacks were formally pinned on a state. For the rest, including the Belgian freezer wave, nobody has been named. Who did it matters less than it seems: in most cases the door was open.</p><p class="pb-nl"><b>NL:</b> Aanwijzen wie het gedaan heeft, gaat traag en gebeurt zelden. In twee jaar werd een handvol aanvallen formeel aan een staat toegeschreven. Voor de rest, ook de Belgische diepvriesgolf, is niemand aangewezen. Wie het deed, telt minder dan het lijkt: in de meeste gevallen stond de deur open.</p></div><div class="gapsx">'+''.join('<div class="gapx"><h4>%s · <i>%s</i></h4><ul class="tight">%s</ul><p class="small">%s</p></div>'%(a,b,''.join('<li>%s</li>'%x for x in L),n) for a,b,L,n in ACT)+'</div></section>'
# ---------- countries ----------
cards=''
for n in names:
    c=COUNTRY[n]; L=[i for i in INC if i['country']==n]
    cf=[i for i in L if i['status']=='C']; un=[i for i in L if i['status']!='C']
    n25=sum(1 for i in L if i['sort'][0]==2025); n26=len(L)-n25
    body='<p class="small"><b>In this file:</b> %d recorded (%d in 2025, %d in 2026) · %d confirmed, %d reported or claimed%s</p>'%(len(L),n25,n26,len(cf),len(un),' · Schengen, not EU' if n in SCHENGEN else '')
    if c['stats']: body+='<p><b>Figures and trend</b></p><ul>%s</ul>'%''.join('<li>%s</li>'%s for s in c['stats'])
    if cf: body+='<p><b>Confirmed</b></p><ul>%s</ul>'%''.join(li(i) for i in sorted(cf,key=lambda x:x['sort'],reverse=True))
    if un: body+='<p><b>Reported or claimed</b></p><ul>%s</ul>'%''.join(li(i) for i in sorted(un,key=lambda x:x['sort'],reverse=True))
    if not L: body+='<p>No incident found in public sources.</p>'
    body+='<p class="pl"><b>What it shows:</b> %s<span class="plnl"><b>NL – Wat het toont:</b> %s</span></p>'%(c['en'],c['nl'])
    cards+='<div class="country" id="c-%s"><h4>%s <small>%d recorded</small></h4>%s</div>\n'%(re.sub(r'\W','',n),n,len(L),body)
eu=R.find('section',id='eu')
bodies=eu.find(id='eu-bodies'); bodies_html=str(bodies) if bodies else ''
ep=''
for h in eu.find_all('h3'):
    if 'European Parliament itself' in h.get_text():
        ep=str(h)+str(h.find_next_sibling('div'))
CTRY='''<section id="eu">
<h2>By country: 31 countries, 2025–2026</h2>
<p class="sub">The 27 EU Member States plus Norway, Iceland, Switzerland and Liechtenstein, in alphabetical order. For each: the figures and trend where an official source gives them, then confirmed incidents, then reported and claimed ones, kept apart.</p>
<div class="chips">%s</div>
<div class="callout warn"><b>Uneven evidence.</b> Countries that publish a lot (Estonia, the Netherlands, France, Poland) look worse than countries that publish little. For Cyprus, Malta, Croatia, Bulgaria and Iceland few incidents could be confirmed; that says more about what is published than about how safe they are.</div>
<div class="countries">%s</div>
%s
%s
</section>'''%(''.join('<span>%s<b>%d</b></span>'%(n,sum(1 for i in INC if i['country']==n)) for n in names),cards,bodies_html,ep)
eu.replace_with(BeautifulSoup(CTRY,'html.parser'))
anchor=R.find('section',id='eu')
for blk in (ACTS,BIG,MONTHS,REG,NUM):
    old=R.find('section',id=BeautifulSoup(blk,'html.parser').section['id'])
    if old: old.decompose()
    anchor.insert_before(BeautifulSoup(blk,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
print('incidents',len(INC),'countries',len(names),'2025:',y25,'2026:',y26,'confirmed',conf)
print(sorted(((n,sum(1 for i in INC if i['country']==n)) for n in names),key=lambda x:-x[1]))
