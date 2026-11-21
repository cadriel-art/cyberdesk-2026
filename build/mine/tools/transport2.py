from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join(' <span class="tag %s">%s</span>'%(T[x][1],T[x][0]) for x in s)
D={
'Croatia':([('Date not given','The Brodosplit shipyard was hit by the Qilin ransomware group. One mention in a trade report; no date or detail found.','R')],
 'One thin report.','Eén mager bericht.'),
'Denmark':([('Oct 2025','A new criminal group that targets logistics firms claimed it had stolen data from the freight company DSV. DSV said its operations were not disrupted and its systems were fully working; the claim later vanished from the group\'s site.','KN'),
 ('11 Nov 2026','The shipping company Maersk confirmed that an attacker reached one older local system, inherited through an earlier takeover, and took data. A ransomware group demands $5 million.','C')],
 'The world\'s second-largest container line was reached through a forgotten old system.','De op één na grootste containerrederij ter wereld werd bereikt via een vergeten oud systeem.'),
'France':([('Aug 2025','Air France (with KLM) said customer data was taken through an outside supplier, in the week of 28 July. No payment data. Nobody named by the airlines; researchers suspect the criminal group ShinyHunters.','CS'),
 ('Dec 2025','Software that lets an outsider control computers from a distance was found on the passenger ferry GNV Fantastic in the port of Sète. France\'s domestic intelligence service is investigating; a Latvian crew member was charged with acting for an unnamed foreign power. The ferry company says the attempt was stopped without consequences. Russia was mentioned in the press, not by the authorities; the suspect\'s lawyer disputes it.','CS')],
 'A ferry was targeted from the inside, by a crew member, for a foreign state that has not been named.','Een veerboot werd van binnenuit geviseerd, door een bemanningslid, voor een buitenlandse staat die niet genoemd is.'),
'Germany':([('21 May 2025','A joint warning by American, German, Canadian, Australian and other security agencies said that unit 26165 of Russian military intelligence (also known as APT28, a code name) was attacking dozens of logistics and technology firms that move aid to Ukraine, across air, sea and rail. It said the unit had used access to private cameras near border crossings, military sites and railway stations. The warning names sectors, among them ports and airports, not individual ports; a later academic analysis named Hamburg and Rotterdam.','CK'),
 ('19–20 Sep 2025','Berlin Brandenburg Airport was hit by the same ransomware at the check-in supplier Collins Aerospace as Brussels; average delays of about an hour were reported.','C'),
 ('Feb 2026','Deutsche Bahn\'s website and booking app were knocked offline by a flood of traffic. Information and booking worked again by 18 February. No customer data stolen. The company would not say who was behind it.','C')],
 'The trains ran; the booking did not.','De treinen reden; het boeken niet.'),
'Greece':([('Jan 2026','A failure of air traffic control radio grounded or disrupted flights for several hours; about 120 flights were grounded at the two largest airports. The government said a cyberattack was unlikely; a judicial inquiry was opened.','CN')],
 'A big outage that was, as far as known, not an attack.','Een grote storing die, voor zover bekend, geen aanval was.'),
'Ireland':([('Sep 2025','Dublin and Cork airports reported smaller effects from the Collins Aerospace ransomware. One source.','R')],
 'A side effect of the same supplier attack.','Een neveneffect van dezelfde aanval op een leverancier.'),
'Italy':([('Dec 2025','The port authority for the central Adriatic (Ancona) reported an attack, later claimed by the ransomware group Anubis. Whether terminal work was affected is unclear.','CK'),
 ('7 Feb 2026','Rail sabotage near Bologna and Pesaro on the first full day of the Winter Olympics: a physical attack, described on the page about drones and sabotage.','C'),
 ('Oct 2026','A fault in the national data network forced air traffic control to cut capacity by up to half; full capacity was back the same day. The operator ruled out a cyberattack.','CN')],
 'The air traffic fault was technical; the rail attack was physical; only the port case was a hack.','De storing in het luchtverkeer was technisch; de aanval op het spoor was fysiek; alleen het havengeval was een hack.'),
'Lithuania':([('Since Oct 2025','Vilnius Airport closed more than 20 times because of balloons from Belarus. See the page about drones and sabotage.','C'),
 ('2026','Lithuania said transmitters in Russia\'s Kaliningrad region can falsify satellite positioning signals up to 450 km away, covering much of Poland, the Baltic states and part of the Nordic countries.','K')],
 'An airport closed by balloons, under a sky where the positioning signal cannot be trusted.','Een luchthaven gesloten door ballonnen, onder een hemel waar het positiesignaal niet te vertrouwen is.'),
'Netherlands':([('Aug 2025','KLM (with Air France) said customer data was taken through an outside supplier.','C'),
 ('26 Dec 2025','Eurail, the Utrecht company behind the Interrail pass, was breached: data of 308,777 people, including passport details and, for young travellers on the EU\'s DiscoverEU scheme, bank and health details. In February 2026 the data was offered for sale. Affected people were notified from 27 March 2026.','C'),
 ('Jan 2026','The Amsterdam appeal court gave a hacker seven years for breaking into port systems in Rotterdam and Antwerp in 2020–2021; about 210 kg of cocaine came in through Rotterdam with his help.','C'),
 ('9 Nov 2026','Dozens of aircraft over the Netherlands and Belgium lost their satellite positioning signal; experts place the source at sea north of Texel and suspect deliberate jamming. Update 16 Nov 2026: Dutch air traffic control calls deliberate jamming plausible and says safety was not compromised; seven aircraft had trouble on approach to Schiphol. There is no official finding and nobody is named.','CS')],
 'Three hundred thousand passports leaked from a rail-pass company, and it took three months to tell the people.','Driehonderdduizend paspoorten gelekt bij een treinpasbedrijf, en het duurde drie maanden om het de mensen te zeggen.'),
'Spain':([('Nov 2025','Iberia said customer data was exposed through a supplier; passwords and bank details not affected. The criminal group Everest claims 596 GB and demands $6 million; the airline has not confirmed those figures.','CK'),
 ('24–25 Mar 2026','Ransomware at the Port of Vigo: digital systems cut off, work continued by hand. A ransom was demanded; group and payment not confirmed.','C'),
 ('24–26 Sep 2026','The rail companies Adif and Renfe: Adif saw unusual activity on 24 September and its website went down on the 25th; Renfe said customer names and email addresses were reached through Adif\'s servers, and a later notice mentions identity numbers, journeys and encrypted passwords. Trains ran normally. Press figures of 500 GB and claims that the attack was run by artificial intelligence are not confirmed by either company.','CK')],
 'An airline, a port and the railways in ten months; in each case the service kept running.','Een luchtvaartmaatschappij, een haven en het spoor in tien maanden; telkens bleef de dienst draaien.'),
'Sweden':([('17–18 Sep 2026','Two passenger flights lost satellite navigation over the south-east, near Gotland and Öland; both landed normally on other instruments. One source. The transport agency describes continuous jamming and more organised signal-faking in the region.','R')],
 'Signal loss over the Baltic has become routine.','Signaalverlies boven de Oostzee is routine geworden.'),
'Switzerland':([('Oct 2025','The same group that named DSV listed the freight company Kuehne+Nagel as a victim. The company said only that it was aware of the mentions.','K')],
 'A claim by criminals, not confirmed.','Een bewering van criminelen, niet bevestigd.'),
}
NONE=['Austria','Bulgaria','Cyprus','Czechia','Estonia','Finland','Hungary','Iceland','Latvia','Liechtenstein','Luxembourg','Malta','Norway','Poland','Portugal','Romania','Slovakia','Slovenia']
assert len(D)+len(NONE)==30
def card(n):
    ev,se,sn=D[n]
    return '<div class="country" id="t-%s"><h4>%s <small>%d on record</small></h4><ul>%s</ul><p class="pl"><b>What it shows:</b> %s<span class="plnl"><b>NL – Wat het toont:</b> %s</span></p></div>'%(n,n,len(ev),''.join('<li><b>%s:</b> %s%s</li>'%(d,t,tg(s)) for d,t,s in ev),se,sn)
nev=sum(len(D[n][0]) for n in D)
SEC='''<section id="transporteu">
<h2>Transport and ports: the other 30 countries</h2>
<p class="sub">Airports, airlines, ports, shipping, rail and logistics in the other 26 EU countries plus Norway, Iceland, Switzerland and Liechtenstein, 2025 and 2026. %d events in %d countries.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>Across Europe the pattern is the same as in Belgium: transport is hit through a supplier, and what is lost is mostly data and booking systems, not the planes, ships or trains themselves. One supplier's ransomware slowed airports in four countries. Airlines in France, the Netherlands and Spain lost customer data through outside firms. The rail-pass company Eurail leaked the passports of more than 300,000 travellers. Two cases stand apart: a French ferry where a crew member is charged with planting remote-control software for a foreign state, and the steady disturbance of satellite positioning over the Baltic and now the North Sea. Three big outages that looked like attacks were not: Greece, Italy and the Iberian blackout.</p>
<p class="pb-nl"><b>NL:</b> In heel Europa is het patroon hetzelfde als in België: vervoer wordt geraakt via een leverancier, en wat verloren gaat zijn vooral gegevens en boekingssystemen, niet de vliegtuigen, schepen of treinen zelf. De ransomware bij één leverancier vertraagde luchthavens in vier landen. Luchtvaartmaatschappijen in Frankrijk, Nederland en Spanje verloren klantgegevens via externe bedrijven. Het treinpasbedrijf Eurail lekte de paspoorten van meer dan 300.000 reizigers. Twee gevallen staan apart: een Franse veerboot waar een bemanningslid wordt beschuldigd van het plaatsen van afstandsbedieningssoftware voor een buitenlandse staat, en de aanhoudende verstoring van satellietpositionering boven de Oostzee en nu de Noordzee. Drie grote storingen die op aanvallen leken, waren het niet: Griekenland, Italië en de Iberische stroompanne.</p></div>
<div class="warnbox"><b>Labels.</b> <span class="tag t-conf">Confirmed</span> stated by the organisation, an authority or a court. <span class="tag t-rep">Reported</span> in the press, not verified. <span class="tag t-susp">Suspected</span> believed, not proven. <span class="tag t-claim">Claimed</span> said by one party (a government, or the attackers themselves) without evidence shown in public. <span class="tag t-none">Not proven</span> looked into, nothing found, or denied by the organisation. Two labels on one line: the first is for the event, the second for who was behind it.</div>
<h3>By kind of transport</h3>
<table><thead><tr><th>Kind</th><th>What happened</th><th>Where</th></tr></thead><tbody>
<tr><td><b>Airports</b></td><td>Ransomware at one check-in supplier (September 2025)</td><td>Belgium, Germany, Ireland (and the UK)</td></tr>
<tr><td><b>Airlines</b></td><td>Customer data taken through outside suppliers</td><td>France, Netherlands, Spain</td></tr>
<tr><td><b>Air traffic control</b></td><td>Outages that were not attacks</td><td>Greece (Jan 2026), Italy (Oct 2026)</td></tr>
<tr><td><b>Satellite positioning</b></td><td>Jamming and signal-faking</td><td>Baltic states, Sweden, Poland; North Sea (Nov 2026)</td></tr>
<tr><td><b>Sea ports</b></td><td>Ransomware; drug gangs with hackers</td><td>Spain (Vigo), Italy (Ancona); Netherlands and Belgium (court case)</td></tr>
<tr><td><b>Ships and shipping lines</b></td><td>Remote-control software planted on a ferry; break-in at Maersk</td><td>France; Denmark</td></tr>
<tr><td><b>Rail</b></td><td>Booking knocked offline; customer data stolen; passports leaked</td><td>Germany; Spain; Netherlands (Eurail)</td></tr>
<tr><td><b>Freight and logistics</b></td><td>Data-theft claims by a group that targets logistics</td><td>Denmark, Switzerland (claims); CEVA (confirmed, Jul 2026)</td></tr>
</tbody></table>
<h3>Counts and statements by others</h3>
<ul>
<li>The EU cyber agency ENISA says transport has been among the five most attacked sectors for two years; its Europe-wide exercise of 10–11 June 2026, with about 5,000 participants, simulated an attack on rail and shipping. <span class="tag t-conf">Confirmed</span></li>
<li>Thirteen coastal European countries and Iceland issued a joint statement in January 2026 on growing interference with satellite navigation for shipping in the Baltic and North Sea. <span class="tag t-conf">Confirmed</span></li>
<li>About 123,000 flights over the Baltic region were affected by signal interference in the first four months of 2025. Quoted by a tracking site without a primary source. <span class="tag t-rep">Reported</span></li>
<li>A maritime security firm counts 828 cyber incidents in shipping and ports in 2025 against 408 in 2024. A commercial count. <span class="tag t-claim">Claimed</span></li>
</ul>
<h3>Countries with something on record</h3>
<div class="countries">%s</div>
<h3>Nothing specific found</h3>
<p>%s.</p>
<p class="small">For several of these countries there are physical events that touch transport, described on the page about drones and sabotage: the railway explosion in Poland, the airport closures in Luxembourg, the ships sunk off Romania and Bulgaria, the sea cables off Finland and Estonia, and the false bomb threats at Prague airport. Nothing found means nothing came up in searches on 15 November 2026; it is not proof that nothing happened.</p>
<p class="pl"><b>What it shows:</b> Almost nobody attacked a train, a plane or a ship directly. They attacked the companies around them: the check-in supplier, the booking site, the customer database, the freight forwarder. The rule that follows is simple and still rarely applied: know which outside firms you cannot run without, and have a way to work for a week without each of them.<span class="plnl"><b>NL – Wat het toont:</b> Bijna niemand viel een trein, een vliegtuig of een schip rechtstreeks aan. Ze vielen de bedrijven eromheen aan: de leverancier van de check-in, de boekingssite, de klantendatabank, de expediteur. De regel die daaruit volgt is eenvoudig en wordt nog zelden toegepast: weet zonder welke externe bedrijven je niet kunt draaien, en zorg dat je een week zonder elk van hen kunt werken.</span></p>
<p class="src">Sources: see the linked list below.</p>
</section>'''%(nev,len(D),''.join(card(n) for n in sorted(D)),', '.join(NONE))
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='transporteu')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
w=R.find('section',id='transport'); p=w.find('p',class_='sub'); p.string=p.get_text().replace('The other countries follow.','The other 30 countries have their own page.')
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'transporteu'" not in t:
    a="'src': ('R', 'transport')}, "; assert a in t
    t=t.replace(a,a+"{'k': 'transporteu', 'en': 'Transport and ports: 30 countries', 'nl': 'Vervoer en havens: 30 landen', 'src': ('R', 'transporteu')}, ",1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['transporteu']" not in t:
    t+='''
INTRO['transporteu']=("Airports, airlines, ports, ships, rail and freight in the other 30 countries: what was hit, how, and what turned out not to be an attack.","Luchthavens, luchtvaartmaatschappijen, havens, schepen, spoor en vracht in de andere 30 landen: wat geraakt werd, hoe, en wat geen aanval bleek te zijn.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '#p-transporteu td' not in t:
    t=t.replace('</style>','@media(max-width:699px){#p-transporteu td,#p-transporteu th{overflow-wrap:anywhere;padding-left:3px;padding-right:3px;font-size:12px}#p-transporteu table{table-layout:fixed;width:100%}}\n</style>',1)
    open(a,'w',encoding='utf-8').write(t)
print('transport2 ok',nev,len(D))
