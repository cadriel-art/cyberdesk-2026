"""Page '#prepare': Ready at home: stock-up advice. Built from tools/prepare_data.json (merged by prepare_merge.py from the two verified research files)."""
import json,html,re,collections
from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
e=html.escape
DATA=json.load(open(M+'tools/prepare_data.json',encoding='utf-8'))
ALL=DATA['countries']; EVENTS=DATA['events']
EU=[x for x in ALL if x['country']=='EU'][0]
CT=[x for x in ALL if x['country']!='EU']
CT.sort(key=lambda x:(x['country']!='Belgium',x['country']))
N=len(CT); assert N==31
BE=CT[0]; assert BE['country']=='Belgium'
NLN={'Belgium':'België','Netherlands':'Nederland','Luxembourg':'Luxemburg','France':'Frankrijk','Germany':'Duitsland','Austria':'Oostenrijk','Switzerland':'Zwitserland','Liechtenstein':'Liechtenstein','Italy':'Italië','Spain':'Spanje','Portugal':'Portugal','Ireland':'Ierland','Malta':'Malta','Greece':'Griekenland','Cyprus':'Cyprus','Sweden':'Zweden','Finland':'Finland','Norway':'Noorwegen','Denmark':'Denemarken','Iceland':'IJsland','Estonia':'Estland','Latvia':'Letland','Lithuania':'Litouwen','Poland':'Polen','Czechia':'Tsjechië','Slovakia':'Slowakije','Hungary':'Hongarije','Slovenia':'Slovenië','Croatia':'Kroatië','Romania':'Roemenië','Bulgaria':'Bulgarije','EU':'EU'}
def tag(s): return '<span class="tag %s">%s</span>'%(('t-conf','Confirmed') if s=='C' else ('t-rep','Reported'))
def bfirst(names): return sorted(names,key=lambda c:(c!='Belgium',c))
def lst(a,w='and'): a=list(a); return a[0] if len(a)==1 else ', '.join(a[:-1])+' '+w+' '+a[-1]
def nl(names): return [NLN[c] for c in names]
# ---------------- counts
CC=[x['country'] for x in CT if x['adv']=='C']; RC=[x['country'] for x in CT if x['adv']=='R']; NC=[x['country'] for x in CT if x['adv']=='N']
nC,nR,nN=len(CC),len(RC),len(NC); assert nC+nR+nN==N
ADV=[x for x in CT if x['adv']!='N']; nA=len(ADV)
BK=collections.defaultdict(list)
for x in ADV: BK[x['bucket']].append(x['country'])
b3,b1,b10,b0=BK['3d'],BK['1w'],BK['10d'],BK['']
assert len(b3)+len(b1)+len(b10)+len(b0)==nA
EARL=[c for c in bfirst([x['country'] for x in ADV if x['earlier']])]
MAILY=bfirst([x['country'] for x in CT if x['mail']=='yes'])
MAILYR=bfirst({v['country'] for v in EVENTS if v['kind']=='mailing'})
NEWK=collections.defaultdict(set)
for v in EVENTS:
    if v['kind'] in ('launch','mailing') and v['country']!='EU': NEWK[v['country']].add(v['st'])
NEWC=bfirst([c for c in NEWK if c in [x['country'] for x in ADV]]); NEWC_C=[c for c in NEWC if 'C' in NEWK[c]]; NEWC_R=[c for c in NEWC if 'C' not in NEWK[c]]
NOTNEW=bfirst([x['country'] for x in ADV if x['country'] not in NEWC])
DIG=[x['country'] for x in CT if x['mail']=='digital']; PLAN=[x['country'] for x in CT if x['mail']=='planned']; OTH=[x['country'] for x in CT if x['mail']=='other']
assert all(v['date'][-4:] in ('2025','2026') or v['sort'][:4] in ('2025','2026') for v in EVENTS)
# ---------------- what the lists contain
# keyword matching, English, case-insensitive, on the 'items' and 'water' fields of the countries with advice (EU excluded).
# Ambiguous words are left out on purpose:
#  water      : \bwater\b | litre            (items or water field)
#  food       : non-perishable | long-life | ready-to-eat | shelf-stable | keeps without | no cooking | little preparation | canned | tinned | dried food | dry food  (a bare "food" is not counted)
#  medicines  : medic                         (medicine, medicines, medication)
#  radio      : radio
#  torch      : torch | flashlight | headlamp (the bare word "light" is left out: it can mean lighting in general)
#  batteries  : \bbatteries\b | spare batter  ("battery radio" does not count as batteries)
#  cash       : \bcash\b
#  power bank : power ?bank | charger         ("backup power", "power sources" are left out)
#  hygiene    : hygiene | toilet
#  documents  : document
#  first aid  : first[- ]aid
KW=[('Drinking water','Drinkwater',r'\bwater\b|litre'),
('Food that keeps or needs no cooking','Voeding die houdbaar is of niet gekookt hoeft te worden',r'non-perishable|long-life|ready-to-eat|shelf-stable|keeps without|no cooking|little preparation|canned|tinned|dried food|dry food'),
('Medicines','Medicijnen',r'medic'),('Battery or wind-up radio','Radio op batterijen of krachtstroom',r'radio'),('Torch or flashlight','Zaklamp',r'torch|flashlight|headlamp'),
('Spare batteries','Reservebatterijen',r'\bbatteries\b|spare batter'),('Cash','Contant geld',r'\bcash\b'),('Power bank or phone charger','Powerbank of telefoonlader',r'power ?bank|charger'),
('Hygiene items','Hygiëneproducten',r'hygiene|toilet'),('Copies of important documents','Kopieën van belangrijke documenten',r'document'),('First-aid kit','EHBO-set',r'first[- ]aid')]
CNT=[]
for en,nlx,rx in KW:
    hit=[x['country'] for x in ADV if re.search(rx,(x['items']+' '+x['water']).lower())]
    CNT.append((en,nlx,len(hit),hit))
CNT.sort(key=lambda z:-z[2])
# ---------------- body of a country card
def srcs(c):
    return '<ul class="pr-src">'+''.join('<li><a href="%s" target="_blank" rel="noopener noreferrer">%s: %s</a>%s</li>'%(e(s['url']),e(s['publisher']),e(s['title']),(' <span class="small">(%s)</span>'%e(s['date'])) if s.get('date') and s['date']!='n.d.' else '') for s in c['sources'])+'</ul>'
def advtxt(c): return {'C':'Yes','R':'Yes, via media only','N':'None found'}[c['adv']]
def dl(c):
    rows=[('Official advice',advtxt(c)+' '+tag(c['status'])),('Agency',e(c['agency'])),('Guide or campaign',e(c['guide'])),('First',e(c['first'])),('Latest',e(c['latest'])),('How long',e(c['hours'])),('What to keep',e(c['items'])),('Water',e(c['water'])),('Sent to every household?',e(c['households'])),('Why the authorities give it',e(c['reason'])),('What changed in 2025–2026',e(c['news_2025_2026']))]
    if c['country']=='EU': rows[0]=('Status of the guidance','Non-binding guidance from the Commission '+tag(c['status']))
    return '<dl class="pr-dl">'+''.join('<dt>%s</dt><dd>%s</dd>'%(k,v) for k,v in rows if v.strip() and v.strip()!=tag(c['status']))+'</dl>'
def body(c):
    return dl(c)+'<h4>What the sources say</h4><p>%s</p><p class="nl"><b>NL:</b> %s</p><h4>Sources</h4>%s'%(e(c['text']),e(c['text_nl']),srcs(c))
def bigcard(c,title,opn,cls):
    adv='Official advice: yes' if c['adv']=='C' else advtxt(c)
    one={'Belgium':'The National Crisis Centre (NCCN) advises a 72-hour emergency kit. Campaign "Samen voorbereid" launched 21 April 2026, planned to run four years.','EU':'Non-binding guidelines dated 30 October 2026 ask member states to help households cope for at least 72 hours. No quantities are set.'}[c['country']]
    return '<details class="pr-card %s"%s><summary><b>%s</b> %s<span class="pr-one">%s</span></summary><div class="pr-b">%s</div></details>'%(cls,' open' if opn else '',e(title),tag(c['status']),e(one),body(c))
# ---------------- what changed
EV=sorted(EVENTS,key=lambda v:(v['sort'],v['country']),reverse=True)
def evli(v):
    return '<li class="pr-ev%s"><span class="pr-d">%s</span> · <b>%s</b> · %s %s<br><span class="small nl">%s</span></li>'%(' pr-evbe' if v['country']=='Belgium' else '',e(v['date']),e(v['country'] if v['country']!='EU' else 'European Union'),e(v['en']),tag(v['st']),e(v['nl']))
# ---------------- table rows
def row(c):
    nm=c['country']; src=c['sources'][0]['url'] if c['sources'] else ''
    ag=c['agency']
    agl='<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'%(e(src),e(ag)) if src else e(ag)
    t=' '.join([nm,NLN[nm],c['agency'],c['guide'],c['text'],c['items'],c['households'],advtxt(c)]).lower()
    mailed='1' if c['mail'] in ('yes','digital') else '0'
    tg=' '+tag(c['status']) if c['adv']!='N' else ''
    return ('<details class="pr-row%s" data-adv="%s" data-mail="%s" data-t="%s"><summary class="pr-sum">'
     '<span class="c c1" data-l="Country"><b>%s</b></span><span class="c" data-l="Official advice">%s%s</span><span class="c" data-l="How long">%s</span><span class="c" data-l="Water per person per day">%s</span>'
     '<span class="c" data-l="Sent to every household?">%s</span><span class="c" data-l="Latest update">%s</span><span class="c" data-l="Agency and guide">%s<br><span class="small">%s</span></span></summary>'
     '<div class="pr-b">%s</div></details>')%(' pr-rowbe' if nm=='Belgium' else '',c['adv'],mailed,e(t),e(nm),advtxt(c),tg,e(c['hours_s']),e(c['water_s']),e(c['mail_s']),e(c['latest_s']),agl,e(c['guide']),body(c))
head='<div class="pr-head" aria-hidden="true"><span>Country</span><span>Official advice</span><span>How long</span><span>Water per person per day</span><span>Sent to every household?</span><span>Latest update</span><span>Agency and guide</span></div>'
filters='''<div class="filters2 pr-f" id="prf" role="group" aria-label="Filter the countries">
<select id="pr-adv" aria-label="Official advice"><option value="">All countries</option><option value="C">Yes: official advice</option><option value="R">Yes, via media only</option><option value="N">None found</option></select>
<label class="pr-chk"><input type="checkbox" id="pr-mail"> Mailed to households only</label>
<input type="search" id="pr-q" placeholder="Search country, agency, guide…" aria-label="Search the countries">
</div><p class="small" id="pr-count" aria-live="polite">%d of %d shown</p>'''%(N,N)
# ---------------- bars
bars=''.join('<div class="pr-bar"><span class="pr-bl">%s<br><span class="small nl">%s</span></span><span class="pr-bt" role="img" aria-label="%d of %d"><i style="width:%.1f%%"></i></span><b class="pr-bn">%d</b></div>'%(e(en),e(nlx),n,nA,100.0*n/nA,n) for en,nlx,n,h in CNT)
# ---------------- sub line + plain box + verdict (all computed)
def dur_en():
    s='Where the advice gives a length, it is 72 hours (3 days) in %d countries (some say "at least"), about one week in %d (%s) and 10 to 14 days in %d (%s)'%(len(b3),len(b1),lst(bfirst(b1)),len(b10),lst(b10))
    if b0: s+='; %d give no single figure (%s)'%(len(b0),lst(bfirst(b0)))
    return s+'.'
def dur_nl():
    s='Waar het advies een duur noemt, is dat 72 uur (3 dagen) in %d landen (soms "minstens"), ongeveer een week in %d (%s) en 10 tot 14 dagen in %d (%s)'%(len(b3),len(b1),lst(nl(bfirst(b1)),'en'),len(b10),lst(nl(b10),'en'))
    if b0: s+='; %d geven geen duidelijk cijfer (%s)'%(len(b0),lst(nl(bfirst(b0)),'en'))
    return s+'.'
SUB_EN=('Of the %d countries covered, %d have official advice to keep an emergency stock at home (Confirmed: from the government or agency itself), %d have it only through media reports (Reported) and %d have none found in the sources checked. '%(N,nC,nR,nN))+dur_en()+' This is precautionary advice, not a warning that an attack is coming.'
SUB_NL=('Van de %d landen hebben %d officieel advies om thuis een noodvoorraad te hebben (Bevestigd: van de overheid of het agentschap zelf), %d enkel via mediaberichten (Gemeld) en %d geen gevonden in de gecontroleerde bronnen. '%(N,nC,nR,nN))+dur_nl()+' Dit is voorzorgsadvies, geen waarschuwing dat er een aanval komt.'
cash=[c for en,_,n,c in CNT if en=='Cash'][0]
PLAIN_EN=('<p><b>What the advice is.</b> Be able to cope at home, without outside help, for at least 72 hours (three days); some countries ask for a week or more. The lists usually name drinking water, food that keeps or needs no cooking, necessary medicines, a battery or wind-up radio, a torch and some cash (%d of the %d lists with advice include cash).</p>'
 '<p><b>Why it is in a file about cyberattacks.</b> The authorities name long power cuts and outages of water and communications among the reasons, and some name cyberattacks directly. Luxembourg\'s government says its guide prepares households for a prolonged power cut, natural disaster or cyberattack. The guide of France\'s national defence and security secretariat (SGDSN) covers cyberattacks and armed conflict among its scenarios. The Icelandic booklet mentions power cuts, cyberattacks, technical failures and international tension. The European Commission lists extreme weather, power outages, cyber and hybrid threats and conflict. Other countries mainly cite storms, floods and blackouts, so not every guide mentions cyberattacks.</p>'
 '<p><b>What is old and what is new.</b> The idea is not new: in %d countries the sources show a guide or campaign from before 2025 (for example Norway mailed households in 2018 and Latvia published its 72-hour booklet in 2020). What is new in 2025–2026 is formal campaigns and household mailings, listed below.</p>'
 '<p><b>Precaution, not a warning.</b> Several authorities said so explicitly. Belgium\'s National Crisis Centre stresses that it does not want to cause panic (VRT NWS). According to media, Iceland\'s Justice Minister said the booklet is not a response to a specific threat. Croatia\'s Interior Ministry said the push is not tied to a specific expected event. Cyprus\'s Civil Defence deputy spokesperson said the EU recommendation should not be read as a warning that war is imminent. The acting director of Slovenia\'s civil protection administration said the aim is to prepare for unpredictable events, not to frighten.</p>')%(len(cash),nA,len(EARL))
PLAIN_NL=('<p><b>Wat het advies is.</b> Thuis minstens 72 uur (drie dagen) zonder hulp van buitenaf kunnen overleven; sommige landen vragen een week of meer. De lijsten noemen meestal drinkwater, voeding die houdbaar is of niet gekookt hoeft te worden, noodzakelijke medicijnen, een radio op batterijen of krachtstroom, een zaklamp en wat contant geld (%d van de %d lijsten met advies bevatten contant geld).</p>'
 '<p><b>Waarom dit in een dossier over cyberaanvallen staat.</b> De autoriteiten noemen langdurige stroomuitval en storingen van water en communicatie als redenen, en sommige noemen cyberaanvallen rechtstreeks. De regering van Luxemburg zegt dat haar gids huishoudens voorbereidt op een langdurige stroomuitval, natuurramp of cyberaanval. De gids van het Franse nationale secretariaat voor defensie en veiligheid (SGDSN) behandelt onder meer cyberaanvallen en gewapend conflict. Het IJslandse boekje noemt stroomuitval, cyberaanvallen, technische storingen en internationale spanning. De Europese Commissie noemt extreem weer, stroomuitval, cyber- en hybride dreigingen en conflict. Andere landen noemen vooral stormen, overstromingen en black-outs, dus niet elke gids vermeldt cyberaanvallen.</p>'
 '<p><b>Wat oud is en wat nieuw.</b> Het idee is niet nieuw: in %d landen tonen de bronnen een gids of campagne van vóór 2025 (Noorwegen stuurde bijvoorbeeld al in 2018 een brochure naar de huishoudens en Letland publiceerde zijn 72-urenboekje in 2020). Nieuw in 2025–2026 zijn formele campagnes en bedelingen aan huishoudens, hieronder opgelijst.</p>'
 '<p><b>Voorzorg, geen waarschuwing.</b> Meerdere autoriteiten zeiden dat uitdrukkelijk. Het Belgische Nationaal Crisiscentrum benadrukt dat het geen paniek wil zaaien (VRT NWS). Volgens media zei de IJslandse minister van Justitie dat het boekje geen reactie is op een specifieke dreiging. Het Kroatische ministerie van Binnenlandse Zaken zei dat de oproep niet aan een specifiek verwacht evenement is gekoppeld. De woordvoerder van de Cypriotische civiele bescherming zei dat de EU-aanbeveling niet gelezen moet worden als een waarschuwing dat oorlog op handen is. De waarnemend directeur van de Sloveense civiele bescherming zei dat het erom gaat voor onvoorspelbare gebeurtenissen klaar te zijn, niet om bang te maken.</p>')%(len(cash),nA,len(EARL))
nm_en=lambda a:lst(a); 
V_EN=['<p><b>Yes, for most countries.</b> %d of the %d countries have stock-up advice in some form: %d from the government or agency itself (Confirmed) and %d known only through media (Reported). %d have none found in the sources checked (%s)%s.</p>'%(nA,N,nC,nR,nN,lst(bfirst(NC)),'; for Malta, the only item found is an emergency manual and a fire blanket for every household, with no stock-up advice' if 'Malta' in NC else ''),
 '<p><b>Long-standing in some countries, new in many.</b> In %d countries the sources show a guide or campaign from before 2025 (%s), and the European Commission first announced the 72-hour aim on 26 March 2025. What is new in 2025–2026 is formal campaigns: %d countries launched a new campaign, guide, brochure or mailing dated 2025 or 2026 (%s), of which %d are shown by the authority itself and %d only through media. For the other %d countries with advice (%s) no such dated item was found in the sources checked.</p>'%(len(EARL),lst(EARL),len(NEWC),lst(NEWC),len(NEWC_C),len(NEWC_R),len(NOTNEW),lst(NOTNEW)),
 '<p><b>Mailings to every household exist in only some countries.</b> A printed guide or booklet reached households in %d countries (%s); in %d of them the delivery is dated 2025–2026 (%s). %s used digital post, %s plans a mailing for January (announced, not confirmed as started)%s. In the other countries the advice is online or in public campaigns.</p>'%(len(MAILY),lst(MAILY),len(MAILYR),lst(MAILYR),lst(DIG),lst(PLAN),', and Malta delivered a manual and fire blanket without stock-up advice' if OTH else ''),
 '<p><b>The authorities frame it as precaution.</b> Belgium\'s National Crisis Centre says it does not want to cause panic; according to media, Iceland, Croatia, Cyprus and Slovenia said the advice is not a response to a specific threat, not a sign that war is imminent, or not meant to frighten (details in the box at the top).</p>']
V_NL=['<p><b>Ja, voor de meeste landen.</b> %d van de %d landen hebben in enige vorm advies voor een noodvoorraad: %d van de overheid of het agentschap zelf (Bevestigd) en %d enkel via media (Gemeld). %d hebben er geen gevonden in de gecontroleerde bronnen (%s)%s.</p>'%(nA,N,nC,nR,nN,lst(nl(bfirst(NC)),'en'),'; voor Malta is het enige wat gevonden werd een noodhandleiding en een brandblusdeken voor elk huishouden, zonder voorraadadvies' if 'Malta' in NC else ''),
 '<p><b>In sommige landen al lang, in veel landen nieuw.</b> In %d landen tonen de bronnen een gids of campagne van vóór 2025 (%s), en de Europese Commissie kondigde het 72-urendoel voor het eerst aan op 26 maart 2025. Nieuw in 2025–2026 zijn formele campagnes: %d landen lanceerden een nieuwe campagne, gids, brochure of bedeling met een datum in 2025 of 2026 (%s), waarvan %d door de autoriteit zelf worden getoond en %d enkel via media. Voor de andere %d landen met advies (%s) werd in de gecontroleerde bronnen geen dergelijk gedateerd item gevonden.</p>'%(len(EARL),lst(nl(EARL),'en'),len(NEWC),lst(nl(NEWC),'en'),len(NEWC_C),len(NEWC_R),len(NOTNEW),lst(nl(NOTNEW),'en')),
 '<p><b>Een bedeling aan elk huishouden bestaat maar in sommige landen.</b> Een gedrukte gids of een boekje kwam bij de huishoudens in %d landen (%s); in %d daarvan is de bezorging gedateerd in 2025–2026 (%s). %s gebruikte digitale post, %s plant een verzending in januari (aangekondigd, niet als gestart bevestigd)%s. In de andere landen staat het advies online of in publiekscampagnes.</p>'%(len(MAILY),lst(nl(MAILY),'en'),len(MAILYR),lst(nl(MAILYR),'en'),lst(nl(DIG),'en'),lst(nl(PLAN),'en'),', en Malta bezorgde een handleiding en een brandblusdeken zonder voorraadadvies' if OTH else ''),
 '<p><b>De autoriteiten presenteren het als voorzorg.</b> Het Belgische Nationaal Crisiscentrum zegt dat het geen paniek wil zaaien; volgens media zeiden IJsland, Kroatië, Cyprus en Slovenië dat het advies geen reactie is op een specifieke dreiging, geen teken dat oorlog op handen is, of niet bedoeld is om bang te maken (details in het kader bovenaan).</p>']
SEC='''<section id="prepare">
<h2>Ready at home: what governments tell people to keep in stock</h2>
<p class="sub">@@SUB@@</p>
<p class="nl"><b>NL:</b> @@SUBNL@@</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
@@PLAIN@@
<div class="pb-nl">@@PLAINNL@@</div></div>
<h3>Belgium</h3>
@@BE@@
<h3>The European Union</h3>
@@EU@@
<h3>What changed in 2025–2026</h3>
<p class="small">Only events dated 2025 or 2026, newest first, each with its status: Confirmed means the authority itself said it, Reported means only media did. A date range or a month is shown as given in the sources. @@NEV@@ events in @@NEVC@@ countries and the EU.</p>
<ul class="pr-evl">@@EV@@</ul>
<h3>Country by country</h3>
<p class="small">One row per country, Belgium first, then alphabetical. Open a row for the full text, the Dutch summary, the reasons given and every source. Water figures are the ones given in the guides or reported by media; they are not checked here and are not comparable.</p>
@@FILTERS@@
<div class="pr-table" id="pr-table">@@HEAD@@@@ROWS@@</div>
<h3>What the lists usually contain</h3>
<p class="small">Counted from the lists of the @@NA@@ countries with advice (the EU is not counted). A country counts when its list names the item; where the wording is vague (for example just "food" or "light") the item is left out rather than guessed, so these counts are minimums. For @@NR@@ of the @@NA@@ countries the list is known only from media.</p>
<div class="pr-bars">@@BARS@@</div>
<p class="small">Bars show the number of countries out of @@NA@@ with advice.</p>
<div class="callout pr-verdict"><h3>Is it true that many countries told citizens to stock up?</h3>
@@V@@
<div class="nl">@@VNL@@</div></div>
<p class="src">Sources: each card lists its own sources; the full list is below.</p>
</section>'''
for k,v in (('@@NEV@@',str(len(EV))),('@@NEVC@@',str(len({v['country'] for v in EV if v['country']!='EU'}))),('@@NA@@',str(nA)),('@@NR@@',str(nR)),('@@SUB@@',e(SUB_EN)),('@@SUBNL@@',e(SUB_NL)),('@@PLAIN@@',PLAIN_EN),('@@PLAINNL@@',PLAIN_NL),('@@BE@@',bigcard(BE,'Belgium',True,'pr-be')),('@@EU@@',bigcard(EU,'European Union (European Commission)',False,'pr-eu')),
 ('@@EV@@',''.join(evli(v) for v in EV)),('@@FILTERS@@',filters),('@@HEAD@@',head),('@@ROWS@@',''.join(row(c) for c in CT)),('@@BARS@@',bars),('@@V@@',''.join(V_EN)),('@@VNL@@',''.join(V_NL))):
    SEC=SEC.replace(k,v)
assert '%d' not in SEC and '@@' not in SEC
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='prepare')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
# ---------- nav, home, intro
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'k': 'prepare'" not in t:
    m=re.search(r"\{'k': 'citizens'[^}]*\}",t); assert m
    t=t[:m.end()]+", {'k': 'prepare', 'en': 'Ready at home: stock-up advice', 'nl': 'Klaar thuis: advies voor een noodvoorraad', 'src': ('R', 'prepare')}"+t[m.end():]
if 'the stock-up advice page' not in t:
    a=' and <a href="#outages">the global outages page</a>.'; assert a in t
    t=t.replace(a,', <a href="#outages">the global outages page</a> and <a href="#prepare">the stock-up advice page</a>.',1)
open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['prepare']" not in t:
    t=t.rstrip()+'''
INTRO['prepare']=("Which of the 31 countries tell people to keep an emergency stock at home, what the advice contains, and what changed in 2025–2026. It is precaution, not a warning that an attack is coming.","Welke van de 31 landen mensen vragen thuis een noodvoorraad te hebben, wat het advies inhoudt en wat er in 2025–2026 veranderde. Het is voorzorg, geen waarschuwing dat er een aanval komt.")
'''
    open(l,'w',encoding='utf-8').write(t)
# ---------- css + js
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
CSS='''
.pr-card,.pr-row{border:1px solid var(--line);border-radius:10px;background:var(--paper);overflow-wrap:anywhere;margin:8px 0}
.pr-be{border:2px solid var(--accent);background:var(--grey-soft)}
.pr-card>summary{cursor:pointer;list-style:none;padding:12px 14px;display:flex;flex-wrap:wrap;gap:4px 10px;align-items:center}
.pr-card>summary::-webkit-details-marker,.pr-row>summary::-webkit-details-marker{display:none}
.pr-card>summary::before{content:"\\25B8";color:var(--accent);font-size:12px;transition:transform .15s}
.pr-card[open]>summary::before{transform:rotate(90deg)}
.pr-one{flex:1 1 100%;font-size:13.5px;color:var(--muted)}
.pr-b{padding:2px 14px 12px;border-top:1px solid var(--line)}.pr-b h4{margin:12px 0 4px;font-size:13px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}.pr-b p{margin:4px 0}
.pr-dl{display:grid;grid-template-columns:minmax(0,170px) minmax(0,1fr);gap:6px 14px;margin:10px 0}.pr-dl dt{font-weight:600;color:var(--muted);font-size:13px}.pr-dl dd{margin:0;font-size:14px}
.pr-src{margin:4px 0;padding-left:18px}.pr-src li{margin:3px 0}
.pr-evl{list-style:none;margin:8px 0;padding:0;display:flex;flex-direction:column;gap:6px}
.pr-ev{border-left:3px solid var(--line);padding:4px 0 4px 12px;overflow-wrap:anywhere}.pr-evbe{border-left-color:var(--accent);background:var(--grey-soft)}
.pr-d{font-family:var(--f-mono);font-size:12px;color:var(--muted)}
.pr-f{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 4px;align-items:center}.pr-f input[type=search]{font:inherit;font-size:13.5px;padding:7px 10px;border-radius:8px;border:1px solid var(--line);background:var(--paper);color:var(--ink);flex:1 1 200px;min-width:0;max-width:100%}
.pr-chk{font-size:13.5px;display:flex;align-items:center;gap:6px}
.pr-head,.pr-sum{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr) minmax(0,1.2fr) minmax(0,1.1fr) minmax(0,1.4fr) minmax(0,1.1fr) minmax(0,1.7fr);gap:6px 10px;align-items:start}
.pr-head{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding:6px 14px}
.pr-sum{cursor:pointer;list-style:none;padding:10px 14px;font-size:12.5px}
.pr-sum .c{min-width:0;overflow-wrap:anywhere}.pr-sum .c1::before{content:"\\25B8";color:var(--accent);font-size:12px;margin-right:4px;display:inline-block;transition:transform .15s}
.pr-row[open]>.pr-sum .c1::before{transform:rotate(90deg)}
.pr-rowbe{border:2px solid var(--accent);background:var(--grey-soft)}
.pr-bars{display:flex;flex-direction:column;gap:8px;margin:8px 0}
.pr-bar{display:grid;grid-template-columns:minmax(0,240px) minmax(0,1fr) 28px;gap:10px;align-items:center}
.pr-bl{font-size:13.5px;overflow-wrap:anywhere}.pr-bt{display:block;height:14px;background:var(--grey-soft);border-radius:7px;overflow:hidden}.pr-bt i{display:block;height:100%;background:var(--accent);border-radius:7px}.pr-bn{font-family:var(--f-mono);font-size:13px;text-align:right}
.pr-verdict h3{margin-top:0}.pr-verdict p{margin:6px 0}
#p-prepare .pr-verdict,#p-prepare .pr-card,#p-prepare .pr-row,#p-prepare .pr-ev{overflow-wrap:anywhere}
@media(max-width:760px){.pr-head{display:none}.pr-sum{display:block;padding:10px 12px}.pr-sum .c{display:block;margin:3px 0}.pr-sum .c::after{content:none}
.pr-sum .c:not(.c1)::before{content:attr(data-l) ": ";font-weight:600;color:var(--muted)}.pr-sum .c1{font-size:15px;margin-bottom:6px}
.pr-dl{grid-template-columns:minmax(0,1fr);gap:2px}.pr-dl dd{margin-bottom:8px}.pr-bar{grid-template-columns:minmax(0,1fr) 28px}.pr-bl{grid-column:1/-1}.pr-bt{grid-column:1}}
@media print{.pr-card,.pr-row,.pr-ev,.pr-bar,.pr-verdict{break-inside:avoid}.pr-card>summary::before,.pr-row>summary .c1::before{content:""}.pr-row[hidden]{display:none}}
'''
JS='''
/* pr-filters */
(function(){const box=document.getElementById('prf');if(!box)return;const rows=[...document.querySelectorAll('#pr-table .pr-row')];const cnt=document.getElementById('pr-count');const sel=document.getElementById('pr-adv'),mail=document.getElementById('pr-mail'),q=document.getElementById('pr-q');
function apply(){const w=(q.value||'').toLowerCase().trim().split(/\\s+/).filter(Boolean);let n=0;
rows.forEach(r=>{const ok=(!sel.value||r.dataset.adv===sel.value)&&(!mail.checked||r.dataset.mail==='1')&&w.every(x=>r.dataset.t.indexOf(x)>-1);r.hidden=!ok;if(ok)n++;});
if(cnt)cnt.textContent=n+' of '+rows.length+' shown';}
sel.addEventListener('change',apply);mail.addEventListener('change',apply);q.addEventListener('input',apply);apply();})();
'''
if 'pr-row' not in t:
    t=t.replace('</style>',CSS+'</style>',1); k=t.rindex('</script>'); t=t[:k]+JS+t[k:]
    open(a,'w',encoding='utf-8').write(t)
print('prepare ok',nC,nR,nN,len(b3),len(b1),len(b10),len(b0),len(EARL),len(NEWC),len(MAILY),MAILYR)
print([(en,n) for en,_,n,_ in CNT],nA)
