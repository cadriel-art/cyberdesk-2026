from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join('<span class="tag %s">%s</span> '%(T[x][1],T[x][0]) for x in s)
EV=[
('2–3 Oct 2025','Elsenborn army camp','About fifteen drones were reported over the camp in eastern Belgium during the night. This is the first case in the federal prosecutor\'s file. Origin unknown; the investigation was still open in April 2026.','R'),
('9 Oct 2025','Antwerp: plot with an explosive drone','Police arrested three young men suspected of preparing an attack on Prime Minister Bart De Wever with a home-made explosive carried by a drone. A home-made explosive and a 3D printer were found. The federal prosecutor called it jihadist-inspired, so this is terrorism, not a foreign state. One suspect was released; the lawyers of the two others deny any attack plan. No verdict found.','CS','The arrests and the finds are confirmed; the plot itself is suspected until a court rules.'),
('Early Nov 2025','Kleine-Brogel air base','Drones were reported over the base on several nights. Defence Minister Theo Francken called it "a clear mission targeting Kleine-Brogel" and pointed at Russia. No evidence for that has been made public.','RK','The sightings are reported; the link to Russia is a claim by the minister.'),
('4 Nov 2025','Brussels Airport and Liège Airport','Both airports stopped air traffic in the evening after drone reports. Brussels Airport counted 81 cancelled and 24 diverted flights. This is the day the Crisis Centre gives as the first of the wave.','CS','The closure and the cancelled flights are confirmed; that real drones caused it is suspected. A later VRT fact-check found that some of the footage showed helicopters and a plane.'),
('6 Nov 2025','National Security Council','The government decided to make the National Air Security Centre in Beauvechain (Bevekom) fully operational by 1 January 2026, staffed around the clock by Defence, police, customs and aviation services, and agreed in principle to an emergency plan of €50 million for detection, jammers and drone guns. Anti-drone teams from Germany, the United Kingdom and France came to help.','C'),
('7 Nov 2025','Liège Airport','Flights were halted again for a short time after a new drone report.','CS','The stop is confirmed; the drone is suspected.'),
('9 Nov 2025','Doel nuclear plant','Five drones were reported over the plant in the evening. The plant kept running; no danger to the reactors was reported.','R'),
('Nov–Dec 2025','Airports','Brussels and Liège airports stopped air traffic nine times in all: seven times in November, twice in December (Interior Minister Quintin in parliament).','C'),
('21 Jan 2026','The official count','The National Crisis Centre had logged 558 reports of suspicious drones since September 2025: 130 over military sites and 66 over nuclear sites. The minister added that the total may be too high, and that some flights may never have been reported.','C','The number of reports is confirmed. A report is not a confirmed drone.'),
('13 Apr 2026','VRT Pano investigation','The programme found no confirmed evidence that hostile drones flew over Belgium in late 2025. In several cases the "drones" were police helicopters or ordinary aircraft. The federal prosecutor said 26 investigations into about 40 incidents were still open and drew no conclusion. Some security sources kept saying they had little doubt about Russia, without evidence being shown.','CN','The findings of the broadcaster are on record; hostile drones are not proven.'),
('17 Apr – 16 Sep 2026','The €50 million purchase','The Brussels prosecutor opened an investigation into the emergency purchase of anti-drone equipment, bought without competition and against a negative advice. The federal audit service declined to look into it (May). A parliamentary committee asked the Court of Audit for an audit (June). On 16 September the prosecutor closed the case: no criminal offence. The audit question is still open.','C'),
('29 May 2026','Arrest for leaking state secrets','A 46-year-old man was arrested in an investigation led by military intelligence, suspected of passing state secrets to people linked to Russia. Reported as the first Belgian arrest of this kind. Officials speak of "disposable agents": low-paid people recruited online for single jobs. What was leaked is not public.','CS','The arrest is confirmed; the offence is suspected until a court rules.'),
('11–12 Sep 2026','Brussels Airport','A drone was seen on a Friday evening around 21:45, by eye and on radar according to air traffic control. Landings stopped for about 25 minutes and three flights were diverted (two to Ostend, one to Liège). A second sighting the next evening had little effect. Type and pilot unknown. The date comes from secondary reports.','R'),
('29 Sep 2026','Chief of Defence','After a National Security Council on hybrid threats, General Frederik Vansina said there was no concrete threat against Belgium at that moment, while Belgium and Europe are strengthening themselves.','C'),
('Oct–Nov 2026','The freezer attacks','Who is behind the attacks on supermarket freezers is disputed. France accuses Iran\'s Revolutionary Guard for the attack of 11–12 October on more than 700 French sites, and Paris prosecutors opened a judicial investigation and requested international arrest warrants. In Belgium the interior minister says there are "enough elements" that Iran is very probably behind it; the foreign minister and the federal prosecutor say that cannot be confirmed at this stage. Pro-Russian groups (NoName057(16), Z-Pentest) claimed the attacks; Russia denies. See the page on the freezer attacks.','SK','Suspected and claimed, by several sides at once; no Belgian attribution.'),
('5 Nov 2026','Hoax bomb threats','False bomb threats hit more than 27 flights in a Europe-wide wave. Nobody has been named.','R'),
]
rows=''.join('<tr><td class="nowrap"><b>%s</b></td><td><b>%s.</b> %s%s</td><td>%s</td></tr>'%(d,t,x,(' <span class="small"><i>%s</i></span>'%r[4]) if len(r)>4 else '',tg(s)) for r in EV for d,t,x,s in [r[:4]])
SEC='''<section id="hybrid">
<h2>Drones, sabotage and hybrid threats: Belgium</h2>
<p class="sub">Physical and mixed threats in 2025 and 2026: drones over airports, bases and nuclear plants, suspected sabotage, spying and hoaxes. The other 30 countries have their own page. These events are counted apart and are not part of the 227 cyber incidents in the register.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>A "hybrid threat" is pressure on a country that stays below open war: a drone over an airport, a cut cable, a fire, a false bomb alarm, a hack. Each one is small and hard to pin on anyone, and that is the point. In Belgium the late-2025 drone wave closed airports nine times and led to €50 million of emergency spending. One year later, not a single drone has been publicly proven to be hostile, and nobody has been charged for the sightings.</p>
<p class="pb-nl"><b>NL:</b> Een "hybride dreiging" is druk op een land die onder de grens van open oorlog blijft: een drone boven een luchthaven, een doorgesneden kabel, een brand, een vals bomalarm, een hack. Elk feit is klein en moeilijk aan iemand toe te schrijven, en dat is net de bedoeling. In België sloot de dronegolf van eind 2025 negen keer een luchthaven en leidde ze tot 50 miljoen euro aan noodaankopen. Een jaar later is van geen enkele drone publiek bewezen dat hij vijandig was, en niemand is aangeklaagd voor de waarnemingen.</p></div>
<div class="warnbox"><b>How to read the labels on this page.</b> <span class="tag t-conf">Confirmed</span> an authority, court or the organisation itself stated it. <span class="tag t-rep">Reported</span> seen or reported, not verified. <span class="tag t-susp">Suspected</span> believed by investigators or commentators, not proven. <span class="tag t-claim">Claimed</span> said by one party, such as a minister, without public evidence. <span class="tag t-none">Not proven</span> looked into, and no evidence found. One event can carry two labels: the closed airport is confirmed, the drone behind it is suspected.
<span class="plnl"><b>NL – Zo lees je de labels.</b> Confirmed = bevestigd door een overheid, rechtbank of de organisatie zelf. Reported = gezien of gemeld, niet nagekeken. Suspected = vermoed door speurders of commentatoren, niet bewezen. Claimed = beweerd door één partij, bijvoorbeeld een minister, zonder publiek bewijs. Not proven = onderzocht, en geen bewijs gevonden. Eén feit kan twee labels dragen: de gesloten luchthaven is bevestigd, de drone erachter is vermoed.</span></div>
<h3>Figures</h3>
<table><thead><tr><th>Figure</th><th>What it is</th><th>Source</th></tr></thead><tbody>
<tr><td><b>558</b></td><td>Reports of suspicious drones, September 2025 to 21 January 2026. Reports, not confirmed drones.</td><td>Interior Minister, in parliament</td></tr>
<tr><td><b>130 / 66</b></td><td>Of those reports: over military sites / over nuclear sites.</td><td>Same</td></tr>
<tr><td><b>9</b></td><td>Times air traffic was stopped at Brussels or Liège (7 in November, 2 in December 2025).</td><td>Same</td></tr>
<tr><td><b>81 / 24</b></td><td>Flights cancelled / diverted at Brussels Airport around 4 November 2025.</td><td>Brussels Airport</td></tr>
<tr><td><b>26 and about 40</b></td><td>Open investigations and incidents at the federal prosecutor in April 2026. It was 8 investigations and 17 incidents in November 2025; one report says 29.</td><td>Federal prosecutor, via VRT</td></tr>
<tr><td><b>€50 million</b></td><td>Emergency anti-drone purchase, without competition.</td><td>Government; Brussels prosecutor</td></tr>
<tr><td><b>0</b></td><td>Drones publicly proven hostile; people charged for the sightings. As far as public sources show on 13 November 2026.</td><td>VRT Pano; federal prosecutor</td></tr>
</tbody></table>
<h3>What happened, in order</h3>
<table><thead><tr><th>Date</th><th>Event</th><th>Status</th></tr></thead><tbody>'''+rows+'''</tbody></table>
<h3>Proven and not proven</h3>
<table><thead><tr><th>Proven</th><th>Not proven</th></tr></thead><tbody>
<tr><td>Airports were closed nine times and flights were cancelled.</td><td>That real drones were behind each closure.</td></tr>
<tr><td>558 reports came in.</td><td>How many were drones. Some were helicopters and planes.</td></tr>
<tr><td>A minister pointed at Russia.</td><td>That Russia, or any state, sent drones over Belgium.</td></tr>
<tr><td>€50 million was spent in a hurry; the prosecutor found no crime.</td><td>Whether the equipment was the right buy. The audit request is open.</td></tr>
<tr><td>Sightings dropped sharply after the wave.</td><td>Why: deterrence by the new equipment, or fewer mistaken reports.</td></tr>
</tbody></table>
<p class="pl"><b>What it shows:</b> The damage was real even where the drone was not proven: closed airports, cancelled flights, €50 million and a political row. A country that cannot quickly tell a drone from a helicopter pays twice, once in disruption and once in trust.<span class="plnl"><b>NL – Wat het toont:</b> De schade was echt, ook waar de drone niet bewezen is: gesloten luchthavens, geschrapte vluchten, 50 miljoen euro en een politieke rel. Een land dat een drone niet snel van een helikopter kan onderscheiden, betaalt twee keer: één keer in hinder en één keer in vertrouwen.</span></p>
<h3>Still open</h3>
<ul>
<li>The outcome of the federal prosecutor's investigations into the sightings: nothing published.</li>
<li>Whether the National Air Security Centre reached full operation on 1 January 2026 as planned: no 2026 source found.</li>
<li>The audit of the €50 million purchase by the Court of Audit: no result found.</li>
<li>The trial of the Antwerp drone-plot suspects: no date or verdict found.</li>
<li>Sabotage of rail, cables or satellite navigation in Belgium in 2025–2026: nothing found in public sources.</li>
</ul>
<p class="src">Sources: VRT NWS and Pano (13 Apr, 17 Apr, 18 May, 3 Jun, 16 Sep, 29 Sep 2026; live blog Nov 2025); Belga; The Brussels Times; Anadolu (21 Jan and Jun 2026); Euronews; Dronewatch; Al Jazeera (Oct and Nov 2025).</p>
</section>'''
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='hybrid')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'hybrid'" not in t:
    a="{'en': 'Explore', 'nl': 'Verkennen', 'items': ["; assert a in t
    t=t.replace(a,"{'en': 'Beyond hacking', 'nl': 'Meer dan hacken', 'items': [{'k': 'hybrid', 'en': 'Drones, sabotage, hybrid: Belgium', 'nl': 'Drones, sabotage, hybride: België', 'src': ('R', 'hybrid')}, ",1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['hybrid']" not in t:
    t+='''
INTRO['hybrid']=("Threats that are not hacks: drones, suspected sabotage, spying and hoaxes. Every line says whether it is confirmed, reported, suspected, claimed or not proven.","Dreigingen die geen hacks zijn: drones, vermoede sabotage, spionage en valse meldingen. Bij elke regel staat of het bevestigd, gemeld, vermoed, beweerd of niet bewezen is.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '.t-susp' not in t:
    t=t.replace('</style>','.tag.t-susp{background:var(--amber-soft);color:#7a4a00;border:1px dashed #b98a2e}\n.tag.t-none{background:transparent;color:var(--muted);border:1px solid var(--line);text-decoration:line-through}\n@media(min-width:700px){.nowrap{white-space:nowrap}}\n@media(max-width:699px){#p-hybrid td,#p-hybrid th{overflow-wrap:anywhere;padding-left:4px;padding-right:4px}#p-hybrid .tag{font-size:9px;letter-spacing:0;padding:1px 4px}}\n</style>',1)
    open(a,'w',encoding='utf-8').write(t)
print('hybrid ok')
