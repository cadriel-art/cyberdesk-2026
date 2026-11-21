from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join('<span class="tag %s">%s</span> '%(T[x][1],T[x][0]) for x in s)
EV=[
('10 Feb 2025','Sea','Port of Ostend','A cyberattack on the port was reported. No details on impact found.','R'),
('2025','Post','bpost','Ransomware; core operations were not disrupted.','R'),
('19–28 Sep 2025','Air','Brussels Airport, through its supplier Collins Aerospace','Ransomware hit the check-in and boarding software that many airlines share. Staff went back to pen and paper. On Sunday 21 September 44 to 50 departures were cancelled; for Monday the airport asked airlines to cancel half of all departures (nearly 140); by Wednesday the cut was down to 10%. Disruption lasted until 28 September. The EU cyber agency confirmed it was ransomware at a supplier. British police arrested a man in West Sussex and released him on bail; no charge found.','C'),
('Nov–Dec 2025','Air','Brussels and Liège airports','Air traffic stopped nine times after drone reports. No drone was ever proven. See the page on drones and hybrid threats.','CN','The closures are confirmed; the drones are not proven.'),
('Nov 2025','Sea','Port of Antwerp: a drug gang that also tried hacking','Police held 11 people (5 remanded) for smuggling at least 495 kg of cocaine through the port in shipments of bananas and second-hand cars. Investigators found the gang had earlier tried to break into the computer system of an Antwerp freight forwarder. It failed, partly because the firm was about to change systems. The prosecutor called such an attempt "rather exceptional".','C'),
('Jan 2026','Sea','Hacker of port systems: seven years','The Amsterdam appeal court sentenced a 44-year-old man to seven years for breaking into port systems in Rotterdam, Barendrecht and Antwerp between September 2020 and April 2021, so that cocaine could pass unnoticed. In Antwerp a terminal employee plugged in a USB stick with malware for him. The crime is older; the verdict falls in this period.','C'),
('16 Jan 2026','Sea','Port of Antwerp: staff screening','Port employees in sensitive jobs are screened by the federal police and security services. A news agency headline speaks of hundreds suspended; no official number found. Unions call the screening too strict.','R'),
('21 Jan 2026','Sea','Customs figure','Customs intercepted 55 tonnes of cocaine in the port of Antwerp in 2025.','C'),
('3 Apr 2026','Sea','A prosecutor\'s office for the port','The government approved a separate prosecutor\'s office against organised drug crime in the Antwerp port area, with money from 2027. In the previous year Belgian courts handled 80 cases of drug imports through Antwerp: 242 convictions, 918 years of prison.','C'),
('16 Jun 2026','Sea','PortAware','A campaign to protect port staff against approaches by criminals.','C'),
('Jul–Aug 2026','Road and warehouses','CEVA Logistics','An attack from 29 July hit at least eight European warehouses of this logistics group and exposed customer data of web shops. The reports do not say whether a Belgian warehouse was among them.','CN','The attack is confirmed; a Belgian site is not.'),
('11–12 Sep 2026','Air','Brussels Airport','A drone seen by eye and on radar: landings stopped for about 25 minutes, three flights diverted. Operator unknown.','R'),
('5 Oct 2026','Rail','Infrabel','A computer problem left train information and the journey planner out of date. Infrabel said it was not a hack and had no effect on safety or punctuality.','CN','The outage is confirmed; an attack is ruled out by the company.'),
('5 Nov 2026','Air','Hoax bomb threats','A LOT flight from Warsaw was searched on landing in Brussels and a Ryanair flight to Charleroi was affected, in the Europe-wide wave. All false; nobody named.','R'),
('9 Nov 2026','Air','Satellite navigation disturbed','Dozens of aircraft over Belgium, the Netherlands, eastern England and north-west Germany lost their satellite positioning signal. Experts place the source at sea north of Texel and suspect deliberate jamming from a ship. Russian ships were in the North Sea at the time; that link is speculation. Update 16 Nov 2026: Dutch air traffic control calls deliberate jamming plausible and says safety was not compromised; seven aircraft had trouble on approach to Schiphol. There is no official finding and nobody is named.','CS','The disturbance is confirmed; deliberate jamming is suspected; nobody is named.'),
('11 Nov 2026','Sea','Maersk','The Danish shipping company confirmed a break-in to an older system; a ransomware group demands $5 million. No effect on Antwerp found.','CN','The break-in is confirmed; an effect in Belgium is not.'),
]
rows=''.join('<tr><td class="nowrap"><b>%s</b><br><span class="small">%s</span></td><td><b>%s.</b> %s%s</td><td>%s</td></tr>'%(r[0],r[1],r[2],r[3],(' <span class="small"><i>%s</i></span>'%r[5]) if len(r)>5 else '',tg(r[4])) for r in EV)
SEC='''<section id="transport">
<h2>Transport and ports: Belgium</h2>
<p class="sub">Airports, sea ports, rail, post and logistics in 2025 and 2026: attacks, crime, outages and false alarms. The other countries follow.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>Belgian transport was stopped most often through someone else's weak point. The biggest case, nine days of trouble at Brussels Airport in September 2025, was ransomware at an American supplier whose check-in software many airlines share. In the port of Antwerp the threat is different: drug gangs who bribe or pressure staff, and who now and then try hacking as well. On the railways nothing cyber is on record; the daily problem there is cable theft. And three times in two years air traffic was upset by things that are not hacks at all: drone reports, false bomb threats and, on 9 November 2026, a disturbed satellite signal.</p>
<p class="pb-nl"><b>NL:</b> Het Belgische vervoer viel het vaakst stil door de zwakke plek van iemand anders. Het grootste geval, negen dagen hinder op Brussels Airport in september 2025, was ransomware bij een Amerikaanse leverancier van wie veel luchtvaartmaatschappijen de check-insoftware delen. In de haven van Antwerpen is de dreiging anders: drugsbendes die personeel omkopen of onder druk zetten, en die af en toe ook proberen te hacken. Bij het spoor is niets over cyber bekend; het dagelijkse probleem daar is kabeldiefstal. En drie keer in twee jaar werd het luchtverkeer verstoord door dingen die helemaal geen hacks zijn: dronemeldingen, valse bommeldingen en, op 9 november 2026, een verstoord satellietsignaal.</p></div>
<div class="warnbox"><b>Labels.</b> <span class="tag t-conf">Confirmed</span> stated by the organisation, an authority or a court. <span class="tag t-rep">Reported</span> in the press, not verified. <span class="tag t-susp">Suspected</span> believed, not proven. <span class="tag t-claim">Claimed</span> said by one party without public evidence. <span class="tag t-none">Not proven</span> looked into, nothing found. Two labels on one line: the first is for the event, the second for the cause or the Belgian link.</div>
<h3>Figures</h3>
<table><thead><tr><th>Figure</th><th>What it is</th><th>Source</th></tr></thead><tbody>
<tr><td><b>9 days</b></td><td>Disruption at Brussels Airport after the ransomware at its check-in supplier (19–28 September 2025).</td><td>Brussels Airport; ENISA</td></tr>
<tr><td><b>Half</b></td><td>Share of Monday departures the airport asked airlines to cancel on 22 September 2025 (nearly 140 flights).</td><td>Brussels Airport, via press</td></tr>
<tr><td><b>55 tonnes</b></td><td>Cocaine intercepted by customs in the port of Antwerp in 2025.</td><td>Customs, via VRT</td></tr>
<tr><td><b>80 / 242 / 918</b></td><td>Court cases on drug imports through Antwerp in one year / convictions / years of prison.</td><td>Minister of Justice, April 2026</td></tr>
<tr><td><b>255</b></td><td>Cable thefts on the railway in 2024, down from 451 in 2023. A political party cites 223 for 2024; the counts differ.</td><td>Infrabel</td></tr>
<tr><td><b>9</b></td><td>Times air traffic was stopped at Brussels or Liège for drone reports, November–December 2025.</td><td>Interior Minister</td></tr>
<tr><td><b>0</b></td><td>Cyberattacks on record against NMBS/SNCB, Infrabel, De Lijn, MIVB/STIB or TEC in 2025–2026, as far as public sources show.</td><td>Searches, 15 November 2026</td></tr>
</tbody></table>
<h3>What happened, in order</h3>
<table><thead><tr><th>Date</th><th>Event</th><th>Status</th></tr></thead><tbody>'''+rows+'''</tbody></table>
<h3>By kind of transport</h3>
<table><thead><tr><th>Kind</th><th>Main threat seen</th><th>Worst case in the two years</th></tr></thead><tbody>
<tr><td><b>Air</b></td><td>A shared supplier; false alarms (drones, bomb hoaxes); disturbed satellite signal</td><td>Nine days at Brussels Airport, September 2025</td></tr>
<tr><td><b>Sea ports</b></td><td>Drug gangs using insiders, sometimes with hacking</td><td>No successful hack in 2025–2026 found; one failed attempt on a freight forwarder</td></tr>
<tr><td><b>Rail</b></td><td>Cable theft; ordinary computer faults</td><td>No attack on record</td></tr>
<tr><td><b>Post and logistics</b></td><td>Ransomware at the company or its logistics partner</td><td>bpost (2025), operations kept running</td></tr>
<tr><td><b>Bus, tram, metro</b></td><td>Nothing found for 2025–2026</td><td>Nothing on record</td></tr>
</tbody></table>
<h3>Proven and not proven</h3>
<table><thead><tr><th>Proven</th><th>Not proven</th></tr></thead><tbody>
<tr><td>One supplier's ransomware stopped check-in at Brussels Airport for days.</td><td>Who did it. A man was arrested in Britain and bailed; no charge or verdict found.</td></tr>
<tr><td>Drug gangs have hacked port companies before and one tried again in 2025.</td><td>That any port system was successfully hacked in 2025–2026.</td></tr>
<tr><td>Port staff are screened and some were suspended.</td><td>How many: "hundreds" is a headline, not an official figure.</td></tr>
<tr><td>Satellite positioning was disturbed over Belgium on 9 November 2026.</td><td>That it was deliberate, and by whom.</td></tr>
</tbody></table>
<p class="pl"><b>What it shows:</b> In transport, your security is only as good as that of the company whose software or staff you depend on. Brussels Airport was not hacked; its supplier was. The port's computers were not broken into in these two years; its people are the way in. That is why the answers on record are about suppliers and staff: backup procedures on paper, screening, and a prosecutor's office for the port.<span class="plnl"><b>NL – Wat het toont:</b> In het vervoer is je beveiliging maar zo goed als die van het bedrijf van wiens software of personeel je afhangt. Brussels Airport werd niet gehackt; zijn leverancier wel. In de computers van de haven werd in deze twee jaar niet ingebroken; de mensen zijn er de weg naar binnen. Daarom gaan de bekende antwoorden over leveranciers en personeel: noodprocedures op papier, screening, en een parket voor de haven.</span></p>
<h3>Still open</h3>
<ul>
<li>What Brussels Airport and the airlines changed after September 2025, and whether a second supplier or an offline fallback now exists.</li>
<li>The outcome of the British investigation into the Collins Aerospace attack.</li>
<li>The official number of port staff suspended after screening.</li>
<li>The source of the satellite-signal disturbance of 9 November 2026.</li>
<li>Whether any Belgian warehouse was hit in the CEVA Logistics attack.</li>
<li>Bus, tram and metro companies and the smaller ports (Ghent, Zeebrugge, Liège): nothing found for 2025–2026.</li>
</ul>
<p class="src">Sources: see the linked list below.</p>
</section>'''
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='transport')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'transport'" not in t:
    a="{'k': 'failures', 'en': 'Avoidable failures'"; assert a in t
    t=t.replace(a,"{'k': 'transport', 'en': 'Transport and ports: Belgium', 'nl': 'Vervoer en havens: België', 'src': ('R', 'transport')}, "+a,1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['transport']" not in t:
    t+='''
INTRO['transport']=("Airports, ports, rail, post and logistics in Belgium: what stopped them, what was crime, and what was a false alarm.","Luchthavens, havens, spoor, post en logistiek in België: wat ze stillegde, wat misdaad was, en wat vals alarm was.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '#p-transport td' not in t:
    t=t.replace('</style>','@media(max-width:699px){#p-transport td,#p-transport th{overflow-wrap:anywhere;padding-left:3px;padding-right:3px;font-size:12px}#p-transport .tag{font-size:9px;letter-spacing:0;padding:1px 4px}#p-transport table{table-layout:fixed;width:100%}}\n</style>',1)
    open(a,'w',encoding='utf-8').write(t)
print('transport ok')
