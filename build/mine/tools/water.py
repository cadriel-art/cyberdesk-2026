from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join('<span class="tag %s">%s</span> '%(T[x][1],T[x][0]) for x in s)
EV=[
('Aug 2025 (twice) and Nov 2025','Vivaqua (Brussels)','Three attacks that flood a website with traffic until it goes down. The website was unreachable for four hours in total. The water supply itself was not affected. From the company\'s own annual report.','C'),
('2025','Vivaqua (Brussels)','The company reports phishing attempts every day and says phishing and other attacks are rising, pointing at the geopolitical situation. No number given.','C'),
('9 Oct 2025','De Watergroep (Flanders)','Warned customers about fake emails and text messages that abuse its planned merger of services with Farys under the name Waterunie. This is fraud against customers, not an attack on the water system.','C'),
('Mar 2026','Farys and the town of Zelzate','New fake messages: "submit your meter reading" and a promised refund of €124. Fraud against customers.','C'),
('May 2026','Aquaduin (Koksijde)','Reported many fake emails in the name of De Watergroep or Waterunie. Fraud against customers.','C'),
('23 Jun 2026','Vivaqua','Says the threat continues in 2026 and that it has strengthened its security to spot threats earlier (VRT).','C'),
('2026','The sector in Europe','The EU cyber agency ENISA ranks drinking water and waste water among the least mature of all the sectors it assessed; waste water is the weaker of the two.','C'),
('2 Nov 2026 onwards','Not water, but the same kind of equipment','The freezer attacks reached Belgium: small industrial controllers that were reachable from the internet. Water plants use the same kind of controllers. No Belgian water company has been reported hit, and one Belgian report says explicitly that the freezer incidents do not show a threat to drinking water.','CN','The freezer attacks are confirmed; a link to Belgian water is not proven.'),
]
rows=''.join('<tr><td class="nowrap"><b>%s</b></td><td><b>%s.</b> %s%s</td><td>%s</td></tr>'%(r[0],r[1],r[2],(' <span class="small"><i>%s</i></span>'%r[4]) if len(r)>4 else '',tg(r[3])) for r in EV)
SEC='''<section id="water">
<h2>Water: Belgium</h2>
<p class="sub">Drinking water and waste water in 2025 and 2026: what happened to Belgian water companies, what the law asks of them, and what happened abroad that Belgium can learn from. The other countries follow.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>No attack on the Belgian water supply itself is on record for 2025 or 2026: no pump stopped, no water quality changed, no plant taken over. What is on record is smaller: the website of the Brussels water company knocked offline three times, daily phishing, and waves of fake bills sent to customers. The worry is what happened elsewhere. In the United States, Poland, Denmark and Norway, attackers did reach the controls of water plants and dams, through small control devices left reachable from the internet. Whether Belgian water plants have such devices exposed is not public.</p>
<p class="pb-nl"><b>NL:</b> Voor 2025 en 2026 is geen aanval op de Belgische watervoorziening zelf bekend: geen pomp stilgelegd, geen waterkwaliteit gewijzigd, geen installatie overgenomen. Wat wel bekend is, is kleiner: de website van het Brusselse waterbedrijf drie keer platgelegd, dagelijkse phishing, en golven van valse facturen naar klanten. De zorg is wat elders gebeurde. In de Verenigde Staten, Polen, Denemarken en Noorwegen raakten aanvallers wel aan de besturing van waterinstallaties en dammen, via kleine stuurtoestellen die vanaf het internet bereikbaar waren. Of Belgische waterinstallaties zulke toestellen open hebben staan, is niet publiek.</p></div>
<div class="warnbox"><b>Labels.</b> <span class="tag t-conf">Confirmed</span> stated by the company, an authority or a court. <span class="tag t-rep">Reported</span> in the press, not verified. <span class="tag t-susp">Suspected</span> believed, not proven. <span class="tag t-claim">Claimed</span> said by one party without public evidence. <span class="tag t-none">Not proven</span> looked into, nothing found.</div>
<h3>Figures</h3>
<table><thead><tr><th>Figure</th><th>What it is</th><th>Source</th></tr></thead><tbody>
<tr><td><b>0</b></td><td>Attacks on record that touched water production, treatment or quality in Belgium, 2025–2026. As far as public sources show on 15 November 2026.</td><td>Searches in Dutch, French and English</td></tr>
<tr><td><b>3</b></td><td>Attacks that knocked Vivaqua's website offline in 2025 (August twice, November).</td><td>Vivaqua annual report, via VRT</td></tr>
<tr><td><b>4 hours</b></td><td>Total time that website was unreachable.</td><td>Same</td></tr>
<tr><td><b>Daily</b></td><td>Phishing attempts reported by Vivaqua.</td><td>Same</td></tr>
<tr><td><b>4</b></td><td>Public warnings about fake messages in the name of water companies, October 2025 to May 2026 (De Watergroep, Farys, Zelzate, Aquaduin).</td><td>VRT; Test-Aankoop; Farys</td></tr>
</tbody></table>
<h3>What happened, in order</h3>
<table><thead><tr><th>Date</th><th>Event</th><th>Status</th></tr></thead><tbody>'''+rows+'''</tbody></table>
<h3>What the law asks</h3>
<ul>
<li><b>Cybersecurity:</b> drinking water and waste water are on the list of highly critical sectors in the EU cybersecurity directive (NIS2). The Belgian law dates from 26 April 2024 and has applied since 18 October 2024. Large water companies are "essential entities": stricter checks and higher fines. The national cyber centre (CCB) supervises; the law allows part of that to be handed to a sector authority. <span class="tag t-conf">Confirmed</span></li>
<li><b>Physical protection:</b> a second EU directive, on the resilience of critical entities, also covers water. The Belgian law to apply it was still described as a proposal in the sources found; its current status was not verified. <span class="tag t-rep">Reported</span></li>
<li><b>The level expected:</b> a supplier's guide says most Belgian water companies are expected to reach the "Essential" level of the Belgian security framework CyFun. A commercial source, not an official one. <span class="tag t-claim">Claimed</span></li>
<li><b>Exercises:</b> the CCB held a national cyber crisis exercise on 23 October 2025 and announced a larger one for 2026; the national cyber crisis plan was revised in 2026. Whether water companies took part is not stated. <span class="tag t-conf">Confirmed</span></li>
</ul>
<h3>What happened abroad</h3>
<table><thead><tr><th>Where and when</th><th>What</th><th>Status</th></tr></thead><tbody>
<tr><td><b>United States, July 2026</b></td><td>Attackers got into control devices that were reachable from the internet at more than 30 town water plants in Minnesota and changed the passwords, locking the operators out. The US cyber agency told all water companies to take such devices off the internet. Sources differ on whether Iran-linked actors were named.</td><td><span class="tag t-conf">Confirmed</span> <span class="tag t-susp">Suspected</span></td></tr>
<tr><td><b>Netherlands, Aug 2025</b></td><td>An intelligence service warned that Dutch water and power companies had been targeted.</td><td><span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>Poland, 2025</b></td><td>Attackers got into the control systems of water plants. See the country page for Poland.</td><td><span class="tag t-conf">Confirmed</span></td></tr>
<tr><td><b>Denmark, 2024</b></td><td>Hackers changed the pressure in a water system. Outside the two years of this file; kept as background.</td><td><span class="tag t-conf">Confirmed</span></td></tr>
<tr><td><b>Germany, Aug 2024</b></td><td>An army base near Cologne was sealed off after suspected tampering with its drinking water. No culprit was found. Background.</td><td><span class="tag t-susp">Suspected</span> <span class="tag t-none">Not proven</span></td></tr>
</tbody></table>
<h3>Proven and not proven</h3>
<table><thead><tr><th>Proven</th><th>Not proven</th></tr></thead><tbody>
<tr><td>Belgian water companies are attacked on their websites and by phishing, and say it is rising.</td><td>That anyone reached the controls of a Belgian water plant.</td></tr>
<tr><td>Criminals use the names of water companies to defraud customers.</td><td>That those fraud waves are linked to any state.</td></tr>
<tr><td>Abroad, exposed control devices were the way in.</td><td>Whether Belgian water plants have such devices exposed. No public audit found.</td></tr>
<tr><td>The sector is among the least mature in Europe (ENISA).</td><td>How Belgian companies score individually.</td></tr>
</tbody></table>
<p class="pl"><b>What it shows:</b> Belgium has had the warning without the accident. The same kind of control device that was hijacked in Belgian supermarket freezers in November 2026 also runs pumps and valves in water plants. The cheap fix is known from the American case: find every control device that can be reached from the internet and take it off.<span class="plnl"><b>NL – Wat het toont:</b> België heeft de waarschuwing gekregen zonder het ongeval. Hetzelfde soort stuurtoestel dat in november 2026 in Belgische supermarktdiepvriezers werd gekaapt, stuurt ook pompen en kleppen in waterinstallaties aan. De goedkope oplossing is bekend uit het Amerikaanse geval: zoek elk stuurtoestel dat vanaf het internet bereikbaar is en haal het eraf.</span></p>
<h3>Still open</h3>
<ul>
<li>Whether any Belgian water company has checked for control devices reachable from the internet, and what it found.</li>
<li>Which authority inspects water companies in practice: the CCB alone, or a regional water authority as well.</li>
<li>The status of the Belgian law on the resilience of critical entities.</li>
<li>Figures for the Walloon companies (SWDE, CILE, inBW) and the Flemish ones (De Watergroep, Farys, Pidpa, water-link): none publish attack numbers as Vivaqua did.</li>
<li>Waste-water treatment (Aquafin and others): nothing found at all.</li>
</ul>
<p class="src">Sources: VRT NWS (9 Oct 2025; 7 Mar, 4 May and 23 Jun 2026); Test-Aankoop; Farys; ENISA NIS360 (2026); Centre for Cybersecurity Belgium; CISA via BleepingComputer (Jul 2026); NL Times (11 Aug 2025); VRT NWS (15 Aug 2024).</p>
</section>'''
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='water')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'water'" not in t:
    a="{'k': 'failures', 'en': 'Avoidable failures'"; assert a in t
    t=t.replace(a,"{'k': 'water', 'en': 'Water: Belgium', 'nl': 'Water: België', 'src': ('R', 'water')}, "+a,1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['water']" not in t:
    t+='''
INTRO['water']=("Drinking water and waste water: what is on record for Belgium, what the law asks, and the foreign cases that show how it can go wrong.","Drinkwater en afvalwater: wat voor België bekend is, wat de wet vraagt, en de buitenlandse gevallen die tonen hoe het mis kan gaan.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '#p-watereu td' not in t:
    t=t.replace('</style>','@media(max-width:699px){#p-water td,#p-water th,#p-watereu td,#p-watereu th{overflow-wrap:anywhere;padding-left:3px;padding-right:3px;font-size:12px}#p-water .tag,#p-watereu .tag{font-size:9px;letter-spacing:0;padding:1px 4px}#p-watereu table{table-layout:fixed;width:100%}}\n</style>',1)
    open(a,'w',encoding='utf-8').write(t)
print('water ok')
