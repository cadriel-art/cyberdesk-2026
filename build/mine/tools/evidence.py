import sys,html,collections
from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
sys.path.insert(0,M+'tools')
from evdata import C as CALL
C=[c for c in CALL if c[3]!='Lawful access']   # attacks only: court rulings on police access to encrypted phones are shown apart
NA=[c for c in CALL if c[3]=='Lawful access']
COURT_BEFORE=sum(1 for c in CALL if c[6]==6)
e=html.escape
LV={6:('Court verdict','Vonnis van een rechtbank','A court heard the evidence and ruled. The strongest proof there is; it can still be overturned on appeal.'),
5:('Charges, arrests or arrest warrants','Aanklacht, arrestatie of aanhoudingsbevel','A prosecutor believes there is enough to go to court. Not yet tested by a judge.'),
4:('Formal attribution by a government or agency','Formele toewijzing door een regering of dienst','An official position, usually based on intelligence that stays secret. Serious, but nobody outside can check it.'),
3:('Statement or suspicion by an official','Uitspraak of vermoeden van een gezagsdrager','A minister, a police chief or a prosecutor says who they think it was. It is not the formal position of the state, and colleagues sometimes disagree.'),
2:('Assessment by researchers or unnamed sources','Inschatting door onderzoekers of anonieme bronnen','Security companies, think tanks or journalists quoting insiders. Useful, sometimes commercial, never binding.'),
1:('The attackers\' own claim','Bewering van de aanvallers zelf','A post on Telegram or a leak site. Cheap to make, easy to fake, and sometimes made by groups that did nothing.'),
0:('Nobody named','Niemand genoemd','An investigation may be running, but no name has been put forward by anyone with authority.'),
'X':('Not an attack, or no evidence','Geen aanval, of geen bewijs','It looked like an attack and was first reported as one. An investigation found another cause, or nothing at all.')}
AC={'RU':'Russia (state services)','PR':'Pro-Russian groups','IR':'Iran','BY':'Belarus','CN':'China','KP':'North Korea','CR':'Criminal groups','DG':'Drug gangs','EX':'Extremists, no state','OT':'Other','FR':'A friendly state, by accident','UN':'A foreign state, not named','IN':'Individuals, no sponsor named','NO':'Nobody named','XX':'Not an attack'}
HN={'convicted':'Convicted','charged':'Charged','arrested':'Arrested','none':'Nobody caught'}
PG={'hybrid':'Drones, sabotage, hybrid: Belgium','hybrideu':'Drones, sabotage, hybrid: 30 countries','water':'Water: Belgium','watereu':'Water: 30 countries','transport':'Transport and ports: Belgium','transporteu':'Transport and ports: 30 countries','freezers':'The freezer attacks','eucountries':'By country','victims':'Every kind of victim & fraud','elections':'Elections and democracy: Belgium','electionseu':'Elections and democracy: 30 countries','health':'Health: Belgium','healtheu':'Health: 30 countries','defence':'The defence side: Belgium','defenceeu':'The defence side: 30 countries','encryption':'Encryption and chat control: Belgium','encryptioneu':'Encryption: 30 countries'}
n=len(C); cl=collections.Counter(c[6] for c in C); ca=collections.Counter(c[4] for c in C); ch=collections.Counter(c[7] for c in C)
order=[6,5,4,3,2,1,0,'X']
mx=max(cl.values())
def chip(l): return '<span class="lv lv%s" title="%s">%s</span>'%(l,e(LV[l][0]),('L%s'%l) if l!='X' else '✕')
ladder=''.join('<div class="lad"><div class="lad-h">%s <b>%s</b> <i>%s</i></div><div class="lad-bar"><span class="lvb lv%s" style="width:%d%%"></span><em>%d</em></div><p class="small">%s</p></div>'%(chip(l),e(LV[l][0]),e(LV[l][1]),l,max(4,round(100*cl[l]/mx)),cl[l],e(LV[l][2])) for l in order)
# matrix people caught x sponsor firmness
caught=[c for c in C if c[7]!='none']; 
def strong(c): return c[6]!='X' and c[6]>=4
q=[sum(1 for c in C if c[7]!='none' and strong(c)),sum(1 for c in C if c[7]!='none' and not strong(c)),sum(1 for c in C if c[7]=='none' and strong(c)),sum(1 for c in C if c[7]=='none' and not strong(c) and c[6]!='X')]
# actor bars: by level mix
def abar(k):
    rows=[c for c in C if c[4]==k]; tot=len(rows)
    seg=''.join('<span class="lvb lv%s" style="flex:%d" title="%s: %d"></span>'%(l,sum(1 for c in rows if c[6]==l),e(LV[l][0]),sum(1 for c in rows if c[6]==l)) for l in order if any(c[6]==l for c in rows))
    best=max([c for c in rows if c[6]!='X'],key=lambda c:c[6],default=None)
    return tot,seg,best
PROF={'RU':('Sabotage by hired hands (arson, railways, arms factories), spying, hacks on energy and air traffic, drones.','Every court verdict that names a state names Russia, and every one of them is about a person who was caught: an arsonist, a spy. For hacks and drones the proof stops at government statements.','Russia denies all of it.'),
'PR':('Knocking websites offline; opening or changing industrial controls that were left on the internet.','These groups announce their own attacks, so the claim is cheap. What matters is the step from "a group that cheers for Russia" to "a tool of the Russian state": Denmark took that step formally, Norway only in a speech.','The groups boast; Russia denies any link.'),
'IR':('Sabotage of freezer controls in supermarkets.','One formal attribution, by France, backed by a judicial investigation and requested arrest warrants, but with no evidence published. In Belgium a minister repeats it and the prosecutor does not.','Iran denies; US agencies reportedly have low confidence.'),
'BY':('Balloons and at least one drone across the Lithuanian border.','Lithuania blames the Belarusian state for tolerating or steering smugglers. The balloons are real; the degree of state direction is the open question.','Belarus denies.'),
'CN':('Quiet spying on ministries and network equipment.','Two formal attributions. No sabotage is laid at China\'s door in this file.','China denies.'),
'CR':('Ransomware and data theft for money.','Almost always known only from the criminals\' own leak sites. Companies often confirm the break-in but not the group or the amounts.','—'),
'DG':('Bribing or pressuring port staff; now and then hacking port companies.','The best-proven category after spying: a conviction and a prosecutor\'s case.','—'),
'EX':('Arson, rail sabotage, a drone plot.','Reminds us that not every fire is a foreign state: jihadist-inspired plotters in Antwerp, a group claiming the Czech arms-factory arson, anarchists suspected in Italy.','—'),
'UN':('A crew member with remote-control software; break-ins at state registers; a drone at an airport.','Authorities say "a foreign state" and stop there, which is honest about what they can prove.','—'),
'NO':('Everything from airport ransomware to bomb hoaxes.','The second-largest group. Naming nobody is the normal outcome, not a failure.','—'),
'XX':('Drones nobody found, a cable cut by bad seamanship, outages with technical causes.','Seven alarms that turned out to be something else. Each was first reported as a possible attack.','—')}
profs=''
for k in ['RU','PR','IR','BY','CN','CR','DG','EX','UN','NO','XX']:
    tot,seg,best=abar(k)
    m,p,d=PROF[k]
    profs+='<div class="gapx prof"><h4>%s <small>%d case%s</small></h4><div class="mix">%s</div><p class="small"><b>Methods seen:</b> %s</p><p>%s</p>%s%s</div>'%(e(AC[k]),tot,'' if tot==1 else 's',seg,e(m),e(p),('<p class="small"><b>Hardest proof:</b> %s — %s (%s)</p>'%(e(LV[best[6]][0]),e(best[1]),e(best[2]))) if best else '',('<p class="small"><b>Their answer:</b> %s</p>'%e(d)) if d!='—' else '')
# cases
def case(i,c,cls='evc'):
    d,t,co,dom,a,who,l,h,by,ev,den,unk,pk=c
    f=lambda lab,val: '' if val in ('—','') else '<div class="ef"><span>%s</span><p>%s</p></div>'%(lab,e(val))
    return ('<details class="%s" data-i="%d" data-r="%d" data-a="%s" data-l="%s" data-d="%s" data-h="%s" data-t="%s"><summary>%s<span class="ev-d">%s</span><span class="ev-t">%s <small>%s</small></span><span class="ev-who">%s</span><span class="hn hn-%s">%s</span></summary><div class="ev-body">'
            '<div class="ef"><span>Who is named</span><p><b>%s</b> · %s</p></div>%s%s%s%s<div class="ef"><span>How firm</span><p>%s <b>%s.</b> %s</p></div><p class="small"><a href="#%s">More on the page "%s"</a></p></div></details>')%(
            cls,i,order.index(l),a,l,e(dom),h,e((t+' '+co+' '+who+' '+AC[a]).lower()),chip(l),e(d),e(t),e(co),e(AC[a]),h,HN[h],e(who),e(AC[a]),f('Who says so',by),f('Evidence made public',ev),f('Denial or other explanation',den),f('Still unknown',unk),chip(l),e(LV[l][0]),e(LV[l][2]),pk,e(PG[pk]))
HO={'convicted':0,'charged':1,'arrested':2,'none':3}
MON={'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
import re as _re
def dkey(d):
    """Latest moment a date label refers to, as (year, month, day)."""
    ys=[(m.start(),int(m.group())) for m in _re.finditer(r'20\d\d',d)]
    if not ys: return (0,0,0)
    pos,y=max(ys,key=lambda t:(t[1],t[0]))
    pre=d[:pos]
    ms=[(m.start(),MON[m.group()[:3].lower()]) for m in _re.finditer(r'(?i)jan\w*|feb\w*|mar\w*|apr\w*|may|jun\w*|jul\w*|aug\w*|sep\w*|oct\w*|nov\w*|dec\w*',pre)]
    mo=ms[-1][1] if ms else 0
    if not mo:
        low=pre.lower()
        for w,n in (('spring',4),('summer',7),('autumn',10),('fall',10),('winter',1)):
            if w in low: mo=n; break
    day=0
    if ms:
        h=_re.search(r'(\d{1,2})\s*$',pre[:ms[-1][0]])
        if h and 1<=int(h.group(1))<=31: day=int(h.group(1))
    return (y,mo,day)
BYDATE=sorted(C,key=lambda c:(dkey(c[0]),-order.index(c[6])),reverse=True)
cases=''.join(case(i,c) for i,c in enumerate(BYDATE))
BYNA=sorted(NA,key=lambda c:dkey(c[0]),reverse=True)
NAHTML='<details class="evna" id="ev-notattacks"><summary><b>Not attacks: court rulings on police access to encrypted phones</b> <span class="small">(%d)</span><span class="plnl"><b>NL:</b> Geen aanvallen: rechterlijke uitspraken over politietoegang tot versleutelde telefoons</span></summary><p class="small">These %d cases are court rulings and police operations about reading encrypted phones, not attacks. They are left out of every count, bar, table and filter above and below.<span class="plnl"><b>NL:</b> Deze %d zaken gaan over rechterlijke uitspraken en politieoperaties rond het uitlezen van versleutelde telefoons, geen aanvallen. Ze zitten niet in de tellingen, balken, tabellen en filters.</span></p>%%s</details>'%(len(NA),len(NA),len(NA))
NAHTML=NAHTML%''.join(case(i,c,'evn') for i,c in enumerate(BYNA))
doms=sorted({c[3] for c in C})
opt=lambda L: ''.join('<option value="%s">%s</option>'%(e(str(k)),e(v)) for k,v in L)
FIL='''<div class="filters evf" id="evf"><input type="search" id="ev-q" placeholder="Search: Leipzig, Iran, cables..." aria-label="Search cases">
<select data-k="a" aria-label="Who is named"><option value="">Who is named: all</option>%s</select>
<select data-k="l" aria-label="How firm"><option value="">How firm: all</option>%s</select>
<select data-k="d" aria-label="Kind"><option value="">Kind: all</option>%s</select>
<select data-k="h" aria-label="People caught"><option value="">People caught: all</option>%s</select>
<select id="ev-sort" aria-label="Order"><option value="date">Newest first</option><option value="level">By proof level</option></select><button type="button" id="ev-reset">Reset</button> <button type="button" id="ev-open">Open all</button></div>
<p class="small" id="ev-count" aria-live="polite">%d cases shown.</p>'''%(opt([(k,AC[k]) for k in AC if ca[k]]),opt([(l,('L%s · '%l if l!='X' else '✕ · ')+LV[l][0]) for l in order]),opt([(x,x) for x in doms]),opt(list(HN.items())),n)
TT=[('Leipzig airport drone','Germany','4 Aug 2026','1 Sep 2026','4 weeks','Formal attribution'),
('French freezer sabotage','France','11–12 Oct 2026','9 Nov 2026','4 weeks','Formal attribution and requested arrest warrants'),
('Milrem arson','Estonia','Aug 2026','29 Sep 2026','About 6 weeks','Formal attribution'),
('Mika railway explosion','Poland','15–17 Nov 2025','Nov 2025','Days','Government statement; charges later'),
('Bremanger dam','Norway','7 Apr 2025','Aug 2025','4 months','Speech by the security chief'),
('Polish energy sites','Poland','29 Dec 2025','13 Jul 2026','6½ months','Formal attribution with sanctions'),
('Copenhagen "drones"','Denmark','22 Sep 2025','25 Jun 2026','9 months','No evidence found'),
('Fitburg sea cables','Finland / Estonia','31 Dec 2025','5 Nov 2026','10 months','Court verdict'),
('Køge waterworks','Denmark','Late 2024','Dec 2025','About 12 months','Formal attribution'),
('German air traffic control','Germany','Aug 2024','12 Dec 2025','16 months','Formal attribution'),
('IKEA Vilnius arson','Lithuania','May 2024','24 Nov 2025','18 months','Court verdict'),
('Czech Foreign Ministry','Czechia','Since 2022','28 May 2025','About 3 years','Formal attribution')]
tt=''.join('<tr><td><b>%s</b><br><span class="small">%s</span></td><td>%s</td><td>%s</td><td><b>%s</b></td><td>%s</td></tr>'%x for x in TT)
verd_state=sum(1 for c in C if c[6]==6 and c[4]=='RU'); verd=cl[6]
old=BeautifulSoup(open(M+'cyber-incident-register.html',encoding='utf-8').read(),'html.parser')
SEC='''<section id="evidence">
<h2>Who did it: the evidence tracker</h2>
<p class="sub">%d attacks, alarms and plots from this file, 2025–2026, each with the same five questions: who is named, who says so, what evidence was made public, who denies it, and what is still unknown. Hacks, drones, sabotage, sea cables, water and transport together.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>"Russia did it" can mean a judge heard the evidence and convicted someone, or it can mean a minister said so on the radio. This page keeps those apart. Every case gets a level from L6 (a court verdict) down to L0 (nobody named), plus a separate mark for alarms that turned out not to be attacks. It also separates two things that are usually mixed up: catching the person who did it, and proving who sent them.</p>
<p class="pb-nl"><b>NL:</b> "Rusland deed het" kan betekenen dat een rechter het bewijs hoorde en iemand veroordeelde, of dat een minister het op de radio zei. Deze pagina houdt die uit elkaar. Elk geval krijgt een niveau van L6 (een vonnis) tot L0 (niemand genoemd), plus een apart teken voor alarmen die geen aanval bleken te zijn. Ze scheidt ook twee dingen die meestal door elkaar lopen: de persoon vatten die het deed, en bewijzen wie hem stuurde.</p></div>
<div class="statsx">
<div class="stx"><b>%d</b><span>cases tracked</span></div>
<div class="stx"><b>%d</b><span>court verdicts</span></div>
<div class="stx"><b>%d</b><span>formal attributions by a state</span></div>
<div class="stx"><b>%d</b><span>with nobody named</span></div>
<div class="stx"><b>%d</b><span>alarms that were not attacks</span></div>
<div class="stx"><b>%d</b><span>with a person arrested, charged or convicted</span></div>
</div>
<h3>The ladder of proof</h3>
<p class="small">From strongest to weakest. The bar shows how many of the %d cases sit on each step.</p>
<div class="ladx">%s</div>
<h3>Caught the hand, or named the sender?</h3>
<p class="small">Two different questions. "Hand" means a person arrested, charged or convicted. "Sender named firmly" means level L4 or higher. The seven false alarms are left out.</p>
<table class="mx"><thead><tr><th></th><th>Sender named firmly (L4–L6)</th><th>Sender not named firmly (L0–L3)</th></tr></thead><tbody>
<tr><th>A person was caught</th><td><b>%d</b><br><span class="small">The strongest cases: arson and spying trials, the Milrem and Brașov fires.</span></td><td><b>%d</b><br><span class="small">Hands without a proven sender: the Fitburg crew, the ferry in Sète, the Skyeton plot.</span></td></tr>
<tr><th>Nobody was caught</th><td><b>%d</b><br><span class="small">A state says who, on secret evidence: Leipzig, the Polish energy sites, the French freezers.</span></td><td><b>%d</b><br><span class="small">Claims, suspicions and silence: most hacks.</span></td></tr>
</tbody></table>
<h3>What the evidence shows</h3>
<div class="gapsx">
<div class="gapx"><h4><span class="gn">1</span>Proof is strongest where a body was caught</h4><p>Of the %d court verdicts, %d name Russia as the one who ordered it, and every one of those is an arson or a spying case with a suspect in the dock. Not one verdict in this file is for a hack carried out from abroad.</p><p class="nl"><b>NL:</b> Van de %d vonnissen noemen er %d Rusland als opdrachtgever, en elk daarvan is een brandstichting of een spionagezaak met een verdachte in de beklaagdenbank. Geen enkel vonnis in dit dossier gaat over een hack vanuit het buitenland.</p></div>
<div class="gapx"><h4><span class="gn">2</span>For hacks, the top of the ladder is a government's word</h4><p>The Polish energy sites, German air traffic control, the Czech ministry, the French freezers: all rest on formal statements whose evidence stays secret. That is how intelligence works, but it means the public is asked to trust, not to check.</p><p class="nl"><b>NL:</b> De Poolse energiesites, de Duitse luchtverkeersleiding, het Tsjechische ministerie, de Franse diepvriezers: ze steunen allemaal op formele verklaringen waarvan het bewijs geheim blijft. Zo werken inlichtingen, maar het publiek wordt gevraagd te vertrouwen, niet te controleren.</p></div>
<div class="gapx"><h4><span class="gn">3</span>The sender hides behind hired hands</h4><p>The people caught are Ukrainians, Belarusians, Latvians, a Colombian, Serbs: recruited online, paid small sums, often in cryptocurrency, and told little. Courts convict them easily. The step from them to an officer in Moscow is where most cases thin out.</p><p class="nl"><b>NL:</b> De mensen die gevat worden zijn Oekraïners, Belarussen, Letten, een Colombiaan, Serviërs: online geronseld, met kleine bedragen betaald, vaak in cryptomunten, en weinig ingelicht. Rechtbanken veroordelen hen vlot. De stap van hen naar een officier in Moskou is waar de meeste zaken dun worden.</p></div>
<div class="gapx"><h4><span class="gn">4</span>Fast attributions are political, slow ones are legal</h4><p>Germany and France named a state within four weeks; a court verdict took ten to eighteen months. The fast ones come with expelled diplomats and closed consulates. They are also the ones most disputed: the United States is reported to doubt the French finding on Iran.</p><p class="nl"><b>NL:</b> Duitsland en Frankrijk noemden een staat binnen vier weken; een vonnis duurde tien tot achttien maanden. De snelle komen met uitgewezen diplomaten en gesloten consulaten. Het zijn ook de meest betwiste: de Verenigde Staten zouden twijfelen aan de Franse conclusie over Iran.</p></div>
<div class="gapx"><h4><span class="gn">5</span>A claim is the cheapest evidence there is</h4><p>Pro-Russian groups claimed the freezer attacks that France pins on Iran, then deleted the posts. Ransomware groups list victims who say nothing was taken. A claim tells you who wants the credit, not who did it.</p><p class="nl"><b>NL:</b> Pro-Russische groepen eisten de diepvriesaanvallen op die Frankrijk aan Iran toeschrijft, en wisten daarna hun berichten. Ransomwaregroepen zetten slachtoffers op hun lijst die zeggen dat er niets is buitgemaakt. Een claim zegt wie de eer wil, niet wie het deed.</p></div>
<div class="gapx"><h4><span class="gn">6</span>Some alarms were not attacks at all</h4><p>%d of the %d cases turned out to be something else: drones nobody could find, a cable cut by bad seamanship, outages with technical causes. Most of them were blamed on Russia by officials and media in the first days. The correction came months later and got far less attention.</p><p class="nl"><b>NL:</b> %d van de %d gevallen bleken iets anders te zijn: drones die niemand kon vinden, een kabel doorgesneden door slecht zeemanschap, storingen met een technische oorzaak. De meeste werden de eerste dagen door overheden en media aan Rusland toegeschreven. De rechtzetting kwam maanden later en kreeg veel minder aandacht.</p></div>
</div>
<h3>How long it takes to name someone</h3>
<table><thead><tr><th>Case</th><th>Happened</th><th>Named or decided</th><th>Time</th><th>What came out</th></tr></thead><tbody>%s</tbody></table>
<h3>Where the sides disagree</h3>
<table><thead><tr><th>Case</th><th>One side says</th><th>The other side says</th></tr></thead><tbody>
<tr><td><b>Freezer attacks, France</b></td><td>France: a unit of Iran's Revolutionary Guards; arrest warrants requested.</td><td>Iran denies. US agencies reportedly have low confidence. Pro-Russian groups claimed it themselves.</td></tr>
<tr><td><b>Freezer attacks, Belgium</b></td><td>Interior minister: very probably Iran.</td><td>Foreign minister: not enough information. Federal prosecutor: cannot confirm. Dutch ministry: no sign of Iran in the Netherlands.</td></tr>
<tr><td><b>Drones over Belgium, 2025</b></td><td>Defence minister: Russia.</td><td>VRT's Pano: no evidence of hostile drones. Prosecutor: no conclusion.</td></tr>
<tr><td><b>Drones over Dutch bases</b></td><td>A British think tank: launched from Russian shadow-fleet ships.</td><td>Dutch investigation: no suspects, no drone recovered.</td></tr>
<tr><td><b>Bremanger dam, Norway</b></td><td>Security chief: pro-Russian hackers.</td><td>Russian embassy: unfounded. Legal scholars: no formal written attribution exists.</td></tr>
<tr><td><b>Five Polish water plants</b></td><td>Press and some researchers: Russia-linked groups.</td><td>The security agency's own report did not pin these break-ins on anyone.</td></tr>
<tr><td><b>Pardubice arms-factory arson</b></td><td>A group claimed it over the firm's Israeli ties.</td><td>Czech intelligence asks whether Russia used the group as cover.</td></tr>
<tr><td><b>Bulgarian ammunition depots</b></td><td>Prosecutors: the blasts are linked, Russia suspected.</td><td>The interior minister first pointed away from outside causes; Russia rejects it.</td></tr>
</tbody></table>
<h3>Who is named, and how firmly</h3>
<p class="small">One card per named party. The coloured strip shows the mix of proof levels for that party, strongest on the left.</p>
<div class="gapsx">%s</div>
<h3>All %d cases</h3>
<p class="small">Newest first. Switch the order to group the cases by how firm the proof is. Click a case to open it: the first mark is the level of proof for who is named, the last says whether a person was caught. Case texts are in English only.<span class="plnl"><b>NL:</b> Nieuwste eerst. Wissel de volgorde om de gevallen te groeperen volgens hoe hard het bewijs is.</span></p>
%s
<div id="ev-list">%s</div>
%s
<h3>Five questions to ask of any "X did it"</h3>
<ol>
<li><b>Who is saying it?</b> A court, a government, one minister, a company with something to sell, or the attackers themselves.</li>
<li><b>Was anyone caught?</b> A person in custody can be questioned and tried. A group name on Telegram cannot.</li>
<li><b>Is the evidence public?</b> If not, you are being asked to trust the speaker.</li>
<li><b>Does anyone with access disagree?</b> A prosecutor who will not confirm, an ally with "low confidence", a second ministry that says "too early".</li>
<li><b>Is it the hand or the sender?</b> Convicting the man who lit the fire is not the same as proving who paid him.</li>
</ol>
<p class="nl"><b>NL – Vijf vragen bij elke "X deed het":</b> Wie zegt het? Is er iemand gevat? Is het bewijs publiek? Spreekt iemand met toegang het tegen? Gaat het over de hand of over de opdrachtgever?</p>
<p class="pl"><b>What it shows:</b> Europe is good at catching the people who light the fires and poor at proving, in public, who sent them. For hacks it is weaker still: in two years not one foreign hacker stood before a European judge in the cases in this file. The honest summary is not "Russia is behind everything" and not "nothing is proven". It is that the proof is solid for sabotage and spying by hired hands, official but unchecked for the big hacks, and absent for most drone alarms.<span class="plnl"><b>NL – Wat het toont:</b> Europa is goed in het vatten van wie de branden aansteekt en zwak in het publiek bewijzen wie hen stuurde. Voor hacks is het nog zwakker: in twee jaar stond in de gevallen van dit dossier geen enkele buitenlandse hacker voor een Europese rechter. De eerlijke samenvatting is niet "Rusland zit overal achter" en ook niet "niets is bewezen". Het bewijs is stevig voor sabotage en spionage door handlangers, officieel maar oncontroleerbaar voor de grote hacks, en afwezig voor de meeste dronealarmen.</span></p>
<h3>Limits of this tracker</h3>
<ul>
<li>It covers the cases worked out in this file, not every incident in the register. Most of the %d register incidents have nobody named and are not repeated here.</li>
<li>The level is my reading of public reporting found by search up to 15 November 2026. Where reports differ, the lower level is used.</li>
<li>A level says how firmly someone is named, not whether they did it. L0 does not mean innocent; L4 does not mean proven.</li>
<li>For the pages added on 13–15 November the linked sources were not opened one by one; see the Sources page.</li>
</ul>
<h3>The earlier list: formal attributions of hacks, by state</h3>
%s
</section>'''
import re
reg_n=227
m=re.search(r'holds <b>(\d+)</b> incidents',str(old.find('section',id='trend')) or '')
if m: reg_n=int(m.group(1))
oa=old.find('section',id='actors'); oldlist=str(oa.find('div',class_='gapsx')) if oa else ''
SEC=SEC%(n, n,cl[6],cl[4],cl[0],cl['X'],len(caught), n,ladder, q[0],q[1],q[2],q[3], verd,verd_state,verd,verd_state, cl['X'],n,cl['X'],n, tt, profs, n, FIL, cases, NAHTML, reg_n, oldlist)
o=old.find('section',id='evidence')
if o: o.decompose()
old.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(M+'cyber-incident-register.html','w',encoding='utf-8').write(str(old))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
a="{'k': 'actors', 'en': 'Who was behind it', 'nl': 'Wie erachter zat', 'src': ('R', 'actors')}"
if a in t:
    t=t.replace(a,"{'k': 'evidence', 'en': 'Who did it: evidence tracker', 'nl': 'Wie deed het: bewijstracker', 'src': ('R', 'evidence')}"); open(b,'w',encoding='utf-8').write(t)
else: assert "'evidence'" in t
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['evidence']" not in t:
    t+='''
INTRO['evidence']=("For every big case: who is blamed, by whom, on what evidence, and how firm that is, from a court verdict down to nobody named.","Voor elk groot geval: wie de schuld krijgt, van wie, op welk bewijs, en hoe stevig dat is, van een vonnis tot niemand genoemd.")
'''
    open(l,'w',encoding='utf-8').write(t)
CSS='''
.lv{display:inline-block;min-width:26px;text-align:center;font-family:var(--f-mono);font-size:10.5px;font-weight:700;padding:2px 5px;border-radius:5px;color:#fff;vertical-align:middle}
.lv6,.lvb.lv6{background:#14532d}.lv5,.lvb.lv5{background:#15803d}.lv4,.lvb.lv4{background:#0f766e}.lv3,.lvb.lv3{background:#b45309}.lv2,.lvb.lv2{background:#c2410c}.lv1,.lvb.lv1{background:#9f1239}.lv0,.lvb.lv0{background:#64748b}.lvX,.lvb.lvX{background:#94a3b8}
.lv.lvX{color:#0f172a}
.statsx{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin:14px 0}
.stx{border:1px solid var(--line);border-radius:10px;padding:12px;background:var(--paper)}
.stx b{display:block;font-size:28px;line-height:1.1}.stx span{font-size:12.5px;color:var(--muted)}
.ladx{display:grid;gap:8px}
.lad{border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--paper)}
.lad-h i{color:var(--muted);font-size:13px;margin-left:6px}
.lad-bar{display:flex;align-items:center;gap:8px;margin:6px 0 2px}
.lad-bar .lvb{display:block;height:10px;border-radius:5px}
.lad-bar em{font-style:normal;font-family:var(--f-mono);font-size:12px}
.lad p{margin:2px 0 0}
table.mx th,table.mx td{vertical-align:top}table.mx td b{font-size:24px}
.mix{display:flex;height:10px;border-radius:5px;overflow:hidden;margin:4px 0 8px;gap:2px}
.mix .lvb{display:block;min-width:6px}
.evf{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.evf input[type=search]{flex:1 1 200px;min-width:0;padding:7px 10px;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:inherit;font:inherit}
.evf select{max-width:100%;padding:6px 8px;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:inherit;font:inherit;font-size:13px}
.evc{border:1px solid var(--line);border-radius:10px;background:var(--paper);margin:6px 0}
.evc>summary{display:grid;grid-template-columns:34px 118px 1fr auto auto;gap:8px;align-items:center;padding:9px 12px;cursor:pointer;list-style:none}
.evc>summary::-webkit-details-marker{display:none}
.ev-d{font-family:var(--f-mono);font-size:11.5px;color:var(--muted)}
.ev-t{font-weight:600;font-size:14.5px}.ev-t small{font-weight:400;color:var(--muted);margin-left:4px}
.ev-who{font-size:12px;border:1px solid var(--line);border-radius:999px;padding:2px 9px;white-space:nowrap}
.hn{font-family:var(--f-mono);font-size:10px;text-transform:uppercase;letter-spacing:.06em;padding:2px 6px;border-radius:5px;border:1px solid var(--line);color:var(--muted);white-space:nowrap}
.hn-convicted{background:#14532d;color:#fff;border-color:#14532d}.hn-charged{background:#15803d;color:#fff;border-color:#15803d}.hn-arrested{border-color:#15803d;color:#15803d}
.ev-body{padding:4px 14px 12px;border-top:1px solid var(--line)}
.ef{display:grid;grid-template-columns:170px 1fr;gap:10px;padding:6px 0;border-bottom:1px dashed var(--line)}
.ef>span{font-family:var(--f-mono);font-size:10.5px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);padding-top:3px}
.ef p{margin:0}
@media(max-width:699px){.evc>summary{grid-template-columns:34px 1fr;}.ev-d{grid-column:2}.ev-t{grid-column:1/-1}.ev-who,.hn{grid-column:auto;justify-self:start}.ef{grid-template-columns:1fr;gap:2px}#p-evidence td,#p-evidence th{overflow-wrap:anywhere;padding-left:3px;padding-right:3px;font-size:12px}#p-evidence table{table-layout:fixed;width:100%}}
@media print{.evf,#ev-count{display:none!important}.evc{break-inside:avoid}.lv,.lvb,.hn-convicted,.hn-charged{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
'''
CSS=CSS.replace('.evc{border','.evc,.evn{border').replace('.evc>summary{','.evc>summary,.evn>summary{').replace('.evc>summary::-webkit','.evc>summary::-webkit-details-marker,.evn>summary::-webkit-details-marker{display:none}.evc>summary::-webkit').replace('@media(max-width:699px){.evc>summary{','@media(max-width:699px){.evn>summary{grid-template-columns:34px 1fr}.evc>summary{')
CSS+='.evna{border:1px dashed var(--line);border-radius:10px;margin:14px 0;padding:0 12px}.evna>summary{cursor:pointer;padding:10px 0}\n'
JS='''<script>
(function(){
function apply(){var root=document.getElementById('p-evidence');if(!root)return;var f={};root.querySelectorAll('#evf select').forEach(function(s){f[s.dataset.k]=s.value;});var q=(root.querySelector('#ev-q').value||'').trim().toLowerCase();var n=0,tot=0;
root.querySelectorAll('.evc').forEach(function(c){tot++;var ok=(!f.a||c.dataset.a===f.a)&&(!f.l||c.dataset.l===f.l)&&(!f.d||c.dataset.d===f.d)&&(!f.h||c.dataset.h===f.h)&&(!q||c.dataset.t.indexOf(q)>=0||c.textContent.toLowerCase().indexOf(q)>=0);c.hidden=!ok;if(ok)n++;});
var el=root.querySelector('#ev-count');if(el)el.textContent=n+' of '+tot+' cases shown.';}
function evsort(){var root=document.getElementById('p-evidence');if(!root)return;var s=root.querySelector('#ev-sort');if(!s)return;var box=root.querySelector('#ev-list');
var a=[].slice.call(box.querySelectorAll('.evc'));var byL=s.value==='level';
a.sort(function(x,y){var dx=+x.dataset.i,dy=+y.dataset.i;if(!byL)return dx-dy;var rx=+x.dataset.r,ry=+y.dataset.r;return rx!==ry?rx-ry:dx-dy;});
a.forEach(function(d){box.appendChild(d);});}
document.addEventListener('change',function(e){if(e.target&&e.target.id==='ev-sort'){evsort();return;}if(e.target.closest&&e.target.closest('#evf'))apply();});
document.addEventListener('input',function(e){if(e.target.id==='ev-q')apply();});
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('#ev-reset,#ev-open');if(!b)return;var root=document.getElementById('p-evidence');
if(b.id==='ev-reset'){root.querySelectorAll('#evf select').forEach(function(s){s.value='';});root.querySelector('#ev-q').value='';var so=root.querySelector('#ev-sort');if(so){so.value='date';evsort();}apply();}
else{var all=[].slice.call(root.querySelectorAll('.evc:not([hidden])'));var open=all.some(function(d){return !d.open;});all.forEach(function(d){d.open=open;});b.textContent=open?'Close all':'Open all';}});
})();
</script>'''
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '.evc>summary' not in t:
    t=t.replace('</style>',CSS+'</style>',1)
    t=t.rstrip()+'\n'+JS+'\n'
    open(a,'w',encoding='utf-8').write(t)
print('evidence ok',n,dict(cl),q,'court verdicts before',COURT_BEFORE,'after',cl[6],'excluded',len(NA))
