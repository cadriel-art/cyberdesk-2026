"""Page '#intel': week in brief, what moved on the proof ladder, watchlist. Also: 9 Nov details on the transport pages."""
import sys,html,re,json
from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
sys.path.insert(0,M+'tools')
from evdata import C as CALL
C=[c for c in CALL if c[3]!='Lawful access']   # court rulings on police access to encrypted phones are not attacks
e=html.escape
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join(' <span class="tag %s">%s</span>'%(T[x][1],T[x][0]) for x in s if x in T)
def txt(s): return re.sub(r'\s+',' ',BeautifulSoup(s,'html.parser').get_text(' ')).strip()
# The week in brief, 12 to 19 November 2026: an explicit list. Newest first. Only items that are already in this file.
# sort = day of month (November 2026); st = status codes; page = page key to link to
WEEK=[
dict(sort=18.9,date='13-18 Nov 2026',place='United States (outage wave)',st='C',page='outages',text="Separate outages hit the FAA (13 Nov), JPMorgan Chase and United (16 Nov), Apple, Marriott and the NSA's internal network (17 Nov) and PlayStation Network (18 Nov). On 18 November the White House, DNI Clayton and Secretary of State Rubio said there was no indication of a cyberattack and that the incidents were not related (the officials' statement)."),
dict(sort=19,date='19 Nov 2026',place='European Commission (Brussels)',st='C',page='reg2',text="A Commission spokesperson confirmed an 'AI-generated cyber campaign', first detected on 22 October. Internal staff services such as the Sysper HR platform, payroll and leave requests were taken offline as a precaution for more than ten days. The Commission says it found no evidence of a data breach affecting staff as a whole and knows of no ransom demand; the investigation is open. Politico reported that CERT-EU identified the AI hacking tool ARTEX; the Commission did not confirm this. Nobody is named (The Record)."),
dict(sort=18.5,date='17-20 Nov 2026',place='Norway (Equinor)',st='C',page='reg2',text="Equinor said on 17 November that it had detected an ongoing cyberattack on certain IT systems, with production not affected and no sign of data theft. On 19 November it said the attack did not appear to target Equinor specifically; on 20 November it said the attack had been stopped, with no sign that data was stolen or altered. The kind of attack has not been disclosed and nobody is named."),
dict(sort=18.4,date='18 Nov 2026',place='Norway (Skagerak Energi)',st='C',page='reg2',text="The power company Skagerak Energi said outsiders had broken into some of its IT systems, one day after Equinor. It says operations were not affected and there is no sign of information leaking; it informed the energy regulator, KraftCERT and the National Security Authority. Whether the two attacks are linked is not known. Nobody is named (Industrial Cyber, Dark Reading)."),
dict(sort=18.3,date='18 Nov 2026',place='Bulgaria',st='C',page='reg2',text="Digital transformation minister Ivan Vasilev said intruders had been inside government document-exchange systems since 2021 and had taken more than 130 GB, about 62 million pages. A new monitoring system detected the activity in August 2026. He said several international hacking groups are believed involved, with no conclusive link to a foreign state, and no evidence so far that citizens' personal data was compromised."),
dict(sort=18.2,date='18 Nov 2026',place='France (Chargemap)',st='C',page='reg2',text="The EV-charging platform Chargemap told users that attackers got in on 8 November through a flaw in an old technical interface, closed on 12 November. Stolen data includes e-mail addresses, names, dates of birth and phone numbers; the company says payment details were not taken. The number of affected accounts is unknown. Reported by VRT NWS."),
dict(sort=18.1,date='18 Nov 2026',place='Ireland (credit unions)',st='C',page='reg2',text="Credit-union minister Robert Troy told RTE that about 40 of Ireland's 160 credit unions were affected by an October attack on their online-banking software provider, Wellington IT, which told them only in mid-November. Saved payee details (names, account numbers, addresses) may have been accessed; reports say passwords, PINs and card details were not affected."),
dict(sort=17,date='17 Nov 2026',place='France',st='C',page='encryptioneu',text="The National Assembly adopted the \"résilience\" bill (NIS2 and CER directives) in first reading by 464 votes to 64, according to specialist press. MPs deleted article 16 bis on encrypted messaging, added by the Senate, by 69 votes to 37 (one source, AEF info). A joint Senate-Assembly committee is still to come."),
dict(sort=16,date='16 Nov 2026',place='Lithuania (customs)',st='C',page='reg2',text="Lithuanian Customs said it identified a cyber incident on 10 November and shut down its Common User Management Portal (BAP), which also gives access to EU customs platforms such as ICS2. The acting customs chief called it a deliberate attack; data of possibly several hundred individuals and companies may be affected. Some services reopened on 16 November. No attacker is named."),
dict(sort=15.5,date='15 Nov 2026',place='Estonia',st='R',page='hybrideu',text="Foreign minister Margus Tsahkna said Estonia would close all road border crossings with Russia from 1 December (the Narva freight rail crossing stays open for now). He says Estonia has clear evidence that Russian military intelligence (GRU) ordered the Threod Systems arson attempt; no evidence has been published. The Foreign Ministry clarified that the road crossings (Narva, Luhamaa, Koidula) close on 1 December; the interior minister said the Narva freight rail crossing stays open for now. The government has yet to formally decide scope and duration. Russia denies it: Kremlin spokesman Peskov called the accusation baseless."),
dict(sort=15,date='15 Nov 2026',place='Germany',st='C',page='healtheu',text="The district hospital of Greiz-Ronneburg (Thuringia): the emergency room in Greiz could not take patients; state police and prosecutors were called in. The hospital says patient safety is not at risk."),
dict(sort=14.5,date='14 Nov 2026',place='Estonia (Threod Systems)',st='CK',page='hybrideu',text="An attempt to blow up and set fire to the building of the drone maker Threod Systems was stopped at 3:06 at night. Eight Latvian citizens were detained, and prosecutors asked a court to keep five in custody. The security service KAPO said the attack was ordered by Russian military intelligence; it has published no evidence."),
dict(sort=14,date='14 Nov 2026',place='France (Maileva)',st='C',page='reg2',text="La Poste announced that a cyberattack on its subsidiary Maileva, which sends mail for corporate clients, exposed the first names, surnames and postal addresses of 22 million people who receive mail from Maileva's business customers. Reports date the intrusion to mid-September. The Paris prosecutor's cybercrime section opened an investigation. The perpetrators have not been identified."),
dict(sort=13,date='13 Nov 2026',place='Cyprus',st='C',page='electionseu',text="The president said he does not rule out interference by artificial intelligence in the next elections: \"we are of course all vulnerable\"."),
dict(sort=12.3,date='12 Nov 2026',place='Poland',st='C',page='hybrideu',text="A third man was indicted for helping prepare the Mika attack; the sabotage charge carries ten years to life. No conviction yet."),
dict(sort=12.2,date='12 Nov 2026',place='Norway',st='C',page='hybrideu',text="PST raised its warning: it expects Russian intelligence to try sabotage in Norway in the coming year, most likely against defence firms. It has found no sabotage attempts so far, but Russia-linked actors have mapped targets."),
dict(sort=12.1,date='12 Nov 2026',place='Belgium',st='KN',page='freezers',text='Interior Minister Quintin said Iran is "very probably" behind the freezer attacks. Foreign Minister Prévot and the federal prosecutor do not confirm this.'),
]
wk=''.join('<li><b>%s · %s:</b> %s%s <a href="#%s">More</a></li>'%(e(w['date']),e(w['place']),e(w['text']),tg(w['st']),w['page']) for w in sorted(WEEK,key=lambda w:-w['sort']))
SNAP=json.load(open(M+'tools/news_snapshot.json',encoding='utf-8'))
nw=''.join('<li><b>%s · %s:</b> %s <a href="%s" target="_blank" rel="noopener noreferrer">%s</a></li>'%(e(n['d']),e(n['c'] or 'Europe'),e(n['t']),e(n['url']),e(n['src'])) for n in SNAP if n['d']>='2026-11-12')
MON={'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12,'spring':4,'summer':7,'autumn':10}
def dkey(d):
    ys=re.findall(r'20\d\d',d); y=int(ys[-1]) if ys else 0
    ms=[MON[w[:3]] if w[:3] in MON and w not in MON else MON.get(w,0) for w in re.findall(r'[a-z]+',d.lower())]; ms=[m for m in ms if m]
    ds=re.findall(r'(?<!\d)(\d{1,2})(?!\d)',re.sub(r'20\d\d','',d))
    return (y,ms[-1] if ms else 0,int(ds[-1]) if ds else 0)
LVN={6:'Court verdict',5:'Charges, arrests or warrants',4:'Formal attribution by a government',3:'Statement by an official',2:'Researchers or unnamed sources',1:"The attackers' own claim",0:'Nobody named','X':'Not an attack, or no evidence'}
rows=sorted(C,key=lambda c:dkey(c[0]),reverse=True)
def row(c): return '<tr><td class="d">%s</td><td><span class="lv lv%s" title="%s">%s</span></td><td><b>%s</b> <small>%s</small><br><span class="small">%s%s</span></td></tr>'%(e(c[0]),c[6],e(LVN[c[6]]),('L%s'%c[6]) if c[6]!='X' else '✕',e(c[1]),e(c[2]),e(c[5]),(' · says: '+e(c[8])) if c[8] not in('—','') else '')
recent=[c for c in rows if dkey(c[0])>=(2026,9,0)]; older=[c for c in rows if dkey(c[0])<(2026,9,0)]
WATCH=[
('Who attacked the Belgian supermarket freezers','The federal prosecutor opened an investigation on 3 Nov 2026. France blames Iran for its own wave; a Belgian minister repeats that, the prosecutor does not.','A statement by the federal prosecutor; any arrests under the French warrants that were requested; an EU decision on sanctions.','freezers'),
('What caused the loss of satellite signals on 9 Nov 2026','Dutch air traffic control calls deliberate jamming plausible. No official finding, nobody named.','The outcome of the Dutch investigation; an official statement on the ships seen north of Texel.','cables'),
('"Chat control": will there be a deal','The sixth round of talks (29 Sep 2026) gave only a preliminary understanding on public content. No date found for a next round.','A date for the next round; a text of the compromise.','encryption'),
('Fitburg cable case, Finland','Prison sentences on 5 Nov 2026. The captain said he will appeal. The court did not say who, if anyone, ordered it.','The appeal; any finding on who gave the order.','hybrideu'),
('Eagle S cable case, Finland','The appeal court ruled in Aug 2026 that Finland has jurisdiction; the case went back to the lower court. The accused have left the country.','A new trial date.','hybrideu'),
('Railway explosion near Mika, Poland','A third man was indicted on 12 Nov 2026. No conviction yet.','The trial and the verdict.','hybrideu'),
('Arson at Milrem Robotics, Estonia','Estonia formally blamed Russian security services on 29 Sep 2026. Three suspects were handed over by Latvia.','Charges and a trial.','hybrideu'),
('Drone with explosives at Leipzig/Halle Airport','Germany formally blamed Russia on 1 Sep 2026. Investigators were reported to link it to a foiled arson in Slovakia.','Charges; proof of the reported link.','hybrideu'),
('Fire next to an arms maker in Brașov, Romania','The intelligence service named a Russia-coordinated network on 26 Oct 2026; three suspects.','Charges and a trial.','hybrideu'),
('Hoax bomb threats against flights and schools','A Europe-wide wave in Nov 2026. Paris prosecutors are examining whether a foreign power is behind it. Nobody named.','Any arrest; any official attribution.','hybrid'),
('Egisto Ott spy case, Austria','Convicted on 20 May 2026: four years and one month. He appealed.','The appeal ruling.','hybrideu'),
('Bribery case around Huawei and the European Parliament','The Parliament lifted the immunity of one member on 16 Jun 2026.','Charges; a trial date.','elections'),
('TikTok and the Romanian election','The European Commission\'s investigation was still running at the last check.','A decision by the Commission.','electionseu'),
('Cold rooms of the French blood service, 1–2 Nov 2026','Checked and now in the file. The blood service says stored products were not affected. The Paris prosecutor opened an investigation. Nobody named.','The outcome of the investigation; whether it is linked to the supermarket freezer wave.','healtheu'),
('Attempted arson at Threod Systems, Estonia','14 Nov 2026: eight Latvian citizens detained. The security service says Russian military intelligence ordered it; no evidence published. Russia denies it.','Charges and a trial.','hybrideu'),
('European Commission staff systems hit by a cyber campaign','Detected on 22 Oct 2026; confirmed by the Commission on 19 Nov 2026 as an \'AI-generated cyber campaign\'. No evidence of a breach affecting staff as a whole, no ransom demand known; the investigation is open. No actor named; Politico reports that CERT-EU identified the AI tool ARTEX, not confirmed by the Commission.','What the investigation finds; whether personal data was taken.','reg2'),
('Equinor and Skagerak Energi cyberattacks, Norway','Equinor: disclosed 17 Nov 2026, stopped on 20 Nov; production unaffected, no sign of data theft. Skagerak Energi: break-in disclosed 18 Nov, still being handled. Kind of attack not disclosed; nobody named; no known link between the two.','The type of attack; whether the two are linked; who did it.','reg2'),
('Estonia: closing the border crossings with Russia','Announced 15 Nov 2026 for 1 Dec. The Foreign Ministry named the road crossings (Narva, Luhamaa, Koidula); Narva freight rail stays open for now. No formal cabinet decision yet.','The formal government decision on scope and duration.','hybrideu'),
('Rules to protect children online (EU KIDS Act)','Proposed by the Commission on 17 Sep 2026.','Positions of the Parliament and the member states.','schools'),
]
wl=''.join('<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td><a href="#%s">Page</a></td></tr>'%(e(a),e(b),e(c),p) for a,b,c,p in WATCH)
SEC='''<section id="intel">
<h2>Intel desk: this week, what moved, watchlist</h2>
<p class="sub">Three short lists that keep this file current: what happened in the last week, which cases changed on the proof ladder, and which open questions to keep an eye on. Status: 20 November 2026.</p>
<div class="plainbox"><div class="pb-h">In plain words</div><p>Start here if you have five minutes. Everything on this page comes from the other pages of this file, with the same labels. Only the part called "from the news reader" is not yet verified by us.</p><p class="pb-nl"><b>NL:</b> Begin hier als je vijf minuten hebt. Alles op deze pagina komt van de andere pagina's van dit dossier, met dezelfde labels. Alleen het deel "uit de nieuwslezer" is nog niet door ons geverifieerd. De lijsten zelf zijn in het Engels.</p></div>
<h3>1. The week in brief: 12 to 20 November 2026</h3>
<ul class="intel-wk">@@WK@@</ul>
<p><b>From the news reader, not yet verified by us:</b></p><ul class="intel-wk">@@NW@@</ul>
<div class="callout"><b>What did not change this week:</b> Belgium has still not formally blamed anyone for the freezer attacks; there is still no date for the next round of talks on "chat control"; the cause of the 9 November signal loss is still not confirmed. Re-checked on 19 November 2026.</div>
<h3>2. What moved on the proof ladder</h3>
<p>Each line is the latest step in a case: a verdict, a charge, a formal statement, or a closed investigation. Newest first. The levels are those of the <a href="#evidence">evidence tracker</a>: L6 is a court verdict, L0 means nobody is named, ✕ means it turned out not to be an attack.</p>
<div class="tbl"><table class="intel-t"><thead><tr><th>Latest step</th><th>Level</th><th>Case, who is named, who says so</th></tr></thead><tbody>@@REC@@</tbody></table></div>
<details class="gapx"><summary>Earlier steps (@@NOLD@@ cases, before September 2026)</summary><div class="tbl"><table class="intel-t"><tbody>@@OLD@@</tbody></table></div></details>
<p class="small">From now on, every change of level is added at the top of this list with its date and reason.</p>
<h3>3. Watchlist: open questions</h3>
<p>No dates are given unless an authority announced one. "No date" is the honest answer for most of these.</p>
<div class="tbl"><table class="intel-t intel-w"><thead><tr><th>Open question</th><th>Where it stands</th><th>What to watch for</th><th></th></tr></thead><tbody>@@WL@@</tbody></table></div>
</section>'''
for k,v in (('@@WK@@',wk),('@@NW@@',nw),('@@REC@@',''.join(map(row,recent))),('@@OLD@@',''.join(map(row,older))),('@@NOLD@@',str(len(older))),('@@WL@@',wl)): SEC=SEC.replace(k,v)
R=BeautifulSoup(open(M+'cyber-incident-register.html',encoding='utf-8').read(),'html.parser')
old=R.find('section',id='intel')
if old: old.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(M+'cyber-incident-register.html','w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'k': 'intel'" not in t:
    a="{'k': 'trend', "; assert a in t
    t=t.replace(a,"{'k': 'intel', 'en': 'Intel desk: this week, what moved, watchlist', 'nl': 'Inlichtingendesk: deze week, wat bewoog, volglijst', 'src': ('R', 'intel')}, "+a,1)
    a='To see who is blamed for what'; assert a in t
    t=t.replace(a,'New: <a href="#map">the map</a>, <a href="#news">the news reader</a> and <a href="#intel">the intel desk</a>. '+a,1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['intel']" not in t:
    t=t.rstrip()+'''
INTRO['intel']=("The five-minute page: what happened this week, which cases got firmer or weaker proof, and which open questions to watch.","De pagina van vijf minuten: wat er deze week gebeurde, welke zaken steviger of zwakker bewijs kregen, en welke open vragen je moet volgen.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '.intel-wk' not in t:
    t=t.replace('</style>','''
.intel-wk li{margin:0 0 8px}.intel-t td,.intel-t th{vertical-align:top}.intel-t td.d{white-space:nowrap;font-size:13px}
@media(max-width:699px){#p-intel td,#p-intel th{overflow-wrap:anywhere;padding-left:4px;padding-right:4px;font-size:12.5px}#p-intel table{table-layout:fixed;width:100%}.intel-t td.d{white-space:normal;width:22%}.intel-t:not(.intel-w) td:nth-child(2),.intel-t:not(.intel-w) th:nth-child(2){width:15%}.intel-w td:last-child,.intel-w th:last-child{width:12%}}
@media print{.intel-t tr{break-inside:avoid}.lv{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
</style>''',1); open(a,'w',encoding='utf-8').write(t)
print('intel ok',len(recent),len(older),len(WATCH))
