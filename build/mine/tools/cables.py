from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join('<span class="tag %s">%s</span> '%(T[x][1],T[x][0]) for x in s)
EV=[
('Oct 2023','Cables','Finland–Estonia','The Balticconnector gas pipeline and two telecom cables were damaged. Background: before this file’s two years, and the start of the series.','C'),
('17–18 Nov 2024','Cables','Sweden–Lithuania and Finland–Germany','Two data cables cut within a day of each other. European ministers spoke of hybrid warfare. Background.','C'),
('25 Dec 2024','Cables','Finland–Estonia, the tanker Eagle S','A power cable and several data cables damaged. Finland boarded and held the ship. See <a href="#encryptioneu">the courts</a> and <a href="#hybrideu">the hybrid page</a>: the case was thrown out for lack of jurisdiction in October 2025 and revived on appeal in August 2026.','C'),
('26 Jan 2025','Cables','Latvia–Gotland, the ship Vezhen','Sweden seized the ship on suspicion of sabotage, then released it: prosecutors concluded the damage came from weather, poor equipment and poor seamanship. The clearest case of an alarm that was not an attack.','CN','The damage is confirmed; sabotage was ruled out.'),
('21 Feb 2025','Cables','Germany–Finland','A data cable damaged; sabotage suspected. No outcome found.','R'),
('Jan 2025','Response','NATO starts Baltic Sentry','A standing patrol of the Baltic to watch over cables and pipelines. A secondary source quotes NATO as saying sabotage fell sharply in its first year and that response times went from 17 hours to one; the primary document was not found.','CK','The operation is confirmed; its results are a claim relayed at second hand.'),
('31 Dec 2025','Cables','Finland–Estonia, the ship Fitburg','Finnish special forces boarded the ship; a drag mark about 10 km long was found on the seabed. On 5 November 2026 a Helsinki court sentenced the Russian captain to three and a half years and an Azerbaijani crew member to two years and ten months for aggravated sabotage. The first prison sentences in Europe for cutting sea cables.','C'),
('26 Jan 2026','Cables','Latvia–Gotland again','A fibre cable failed; NATO and police investigated. No outcome found.','R'),
('Jan 2026','Response','Thirteen countries and Iceland speak together','A joint statement on growing interference with satellite navigation for shipping in the Baltic and the North Sea.','C'),
('2024–2026','Signals','Jamming becomes normal','Flights meeting satellite-navigation interference rose from about 200 a day in early 2024 to about 900 a day by the second quarter, on a secondary count. Lithuania says transmitters in Kaliningrad can falsify signals up to 450 km away, which covers much of Poland, the Baltic states and part of the Nordic countries.','RK'),
('3 Jul 2026','Signals','The air safety agency raises the alarm again','EASA issued the fourth revision of its safety bulletin on satellite-navigation outages, saying incidents are becoming more severe, more sophisticated and more disruptive. Its worst-affected list for mid-July 2026 included Tallinn, Riga, Helsinki, Vilnius and Warsaw, alongside Ankara and Istanbul.','C'),
('Oct 2026','Signals','It reaches space','A Danish technical university study found that the jamming over Europe also disturbs the position-finding of satellites in low orbit as they pass over.','C'),
('9 Nov 2026','Signals','The North Sea','About 80 aircraft over north-west Europe, including planes approaching Amsterdam, lost or lost confidence in their satellite position. Seven of them had navigation trouble on approach to Schiphol. Dutch air traffic control calls deliberate jamming a plausible explanation and says safety was not compromised; the Dutch investigation is still open and no official finding exists. A data analyst places the source 80 to 110 nautical miles north of Texel, where six Russian-flagged ships were sailing; shipping news sites say three of them are on the EU sanctions list for carrying weapons. Belgium’s own air traffic service told VRT it received no reports of jamming or spoofing that day.','CS','The disturbance is confirmed; who caused it is suspected, and the Belgian part is weaker than first reported.'),
]
rows=''.join('<tr><td class="nowrap"><b>%s</b><br><span class="small">%s</span></td><td><b>%s.</b> %s%s</td><td>%s</td></tr>'%(r[0],r[1],r[2],r[3],(' <span class="small"><i>%s</i></span>'%r[5]) if len(r)>5 else '',tg(r[4])) for r in EV)
SEC='''<section id="cables">
<h2>Sea cables and satellite signals</h2>
<p class="sub">The two things everything else rests on: the cables under the sea that carry the internet, and the satellite signal that tells ships and aircraft where they are. One page for all 31 countries, because neither stops at a border.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>Almost all data between countries travels through cables lying on the seabed, and almost every ship and aircraft finds its position from a satellite signal weak enough to be drowned out by a transmitter on a truck. Both have been under pressure since late 2023. Cables in the Baltic were cut again and again; one case turned out to be bad seamanship, one ended in the first prison sentences in Europe, and most were never explained. The jamming of satellite signals has gone from an incident to a daily condition over the Baltic, and in November 2026 it reached the North Sea.</p>
<p class="pb-nl"><b>NL:</b> Bijna alle gegevens tussen landen lopen door kabels op de zeebodem, en bijna elk schip en vliegtuig bepaalt zijn plaats met een satellietsignaal dat zwak genoeg is om overstemd te worden door een zender op een vrachtwagen. Beide staan sinds eind 2023 onder druk. Kabels in de Oostzee werden keer op keer doorgesneden; één geval bleek slecht zeemanschap, één eindigde in de eerste gevangenisstraffen in Europa, en de meeste werden nooit verklaard. Het storen van satellietsignalen is van een incident een dagelijkse toestand geworden boven de Oostzee, en in november 2026 bereikte het de Noordzee.</p></div>
<div class="warnbox"><b>Labels.</b> <span class="tag t-conf">Confirmed</span> stated by an authority, a court or a named research body. <span class="tag t-rep">Reported</span> in the press, not verified. <span class="tag t-susp">Suspected</span> believed, not proven. <span class="tag t-claim">Claimed</span> asserted by one party. <span class="tag t-none">Not proven</span> investigated and ruled out. Most of the facts here also appear on <a href="#hybrideu">drones and sabotage</a> and <a href="#transporteu">transport</a>; this page puts them together.</div>
<h3>What happened, in order</h3>
<table><thead><tr><th>Date</th><th>Event</th><th>Status</th></tr></thead><tbody>'''+rows+'''</tbody></table>
<h3>How many cables, and how sure anyone is</h3>
<table><thead><tr><th>Count</th><th>Who counts it that way</th></tr></thead><tbody>
<tr><td><b>7 cuts</b> between November 2024 and January 2025</td><td>One tally of the intense period</td></tr>
<tr><td><b>At least 11 cables</b> damaged since late 2023, plus a gas pipeline</td><td>A wider tally including the earlier cases</td></tr>
<tr><td><b>None since January 2025</b></td><td>One research institute, writing in 2026. It contradicts the Fitburg case of 31 December 2025 and the Latvian cable of January 2026, both in this table.</td></tr>
<tr><td><b>1 case</b> proven in court</td><td>Fitburg, Helsinki, November 2026</td></tr>
<tr><td><b>1 case</b> proven not to be sabotage</td><td>Vezhen, Swedish prosecutors, 2025</td></tr>
</tbody></table>
<p class="small">The disagreement is not sloppiness: it is what happens when a count depends on whether you include accidents, pipelines, repeat damage to one cable, and incidents outside the Baltic.</p>
<h3>Why these two are different from everything else in this file</h3>
<ul>
<li><b>No computer is involved.</b> A cable is cut by an anchor and a signal is drowned out by a transmitter. None of the cyber laws in this file, and none of the two-step logins, make any difference.</li>
<li><b>Nobody owns the problem.</b> Cables are laid by private companies in international water. Satellite navigation is run from space by other states. The affected country often has no jurisdiction over any part of it.</li>
<li><b>Deniability is built in.</b> A dragging anchor looks like bad seamanship, which is why the Vezhen case matters: it proved that sometimes it really is.</li>
<li><b>The damage is invisible until it is total.</b> Jamming hurt nobody for two years. Ships and aircraft carry other instruments and crews are trained. But it is now routine, and the experts quoted say the real danger is not jamming but spoofing, where false positions are fed in and believed.</li>
</ul>
<h3>Proven and not proven</h3>
<table><thead><tr><th>Proven</th><th>Not proven</th></tr></thead><tbody>
<tr><td>Two men were convicted of cutting cables in the Baltic, in November 2026.</td><td>That anyone ordered them to. The verdict names no state.</td></tr>
<tr><td>One widely reported "sabotage" was weather and poor seamanship.</td><td>How many of the others were accidents too.</td></tr>
<tr><td>Satellite-navigation interference is severe, widespread and increasing, on the air safety agency’s own assessment.</td><td>Who is responsible for any single event, including 9 November 2026.</td></tr>
<tr><td>Jamming now disturbs satellites in orbit as well as aircraft.</td><td>That it has caused any accident: no case found.</td></tr>
<tr><td>NATO patrols the Baltic for this.</td><td>Whether the patrol is why incidents fell: the claim is relayed at second hand.</td></tr>
</tbody></table>
<p class="pl"><b>What it shows:</b> This is the part of the picture where Europe reacted fastest and most physically: warships in the Baltic within weeks, a joint statement by fourteen coastal states, prison sentences inside a year. It is also the part where the country suffering the damage can do least on its own. For Belgium the lesson is narrow and practical: it has no Baltic, but it has the North Sea, the cables that come ashore there, and an airport that was already stopped twice by things in the sky. The signal that failed over the North Sea on 9 November 2026 is the first time this reached Belgium’s own doorstep.<span class="plnl"><b>NL – Wat het toont:</b> Dit is het deel van het beeld waar Europa het snelst en het meest fysiek reageerde: oorlogsschepen in de Oostzee binnen enkele weken, een gezamenlijke verklaring van veertien kustlanden, gevangenisstraffen binnen het jaar. Het is ook het deel waar het getroffen land zelf het minst kan doen. Voor België is de les smal en praktisch: het heeft geen Oostzee, maar wel de Noordzee, de kabels die daar aan land komen, en een luchthaven die al twee keer is stilgelegd door iets in de lucht. Het signaal dat op 9 november 2026 uitviel boven de Noordzee is de eerste keer dat dit voor de Belgische deur kwam.</span></p>
<h3>Still open</h3>
<ul>
<li>Who caused the loss of satellite positioning over the North Sea on 9 November 2026.</li>
<li>Whether anyone ordered the Fitburg crew to drag their anchor.</li>
<li>What happened to the investigations into the February 2025 and January 2026 cable failures.</li>
<li>Whether the NATO patrol actually reduced the incidents, from a primary source.</li>
<li>An agreed count of damaged cables: every tally differs.</li>
<li>Whether the cables coming ashore in Belgium are watched at all: nothing found.</li>
</ul>
<p class="src">Sources: see the linked list below.</p>
</section>'''
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='cables')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'cables'" not in t:
    a="{'k': 'more', "; assert a in t
    t=t.replace(a,"{'k': 'cables', 'en': 'Sea cables and satellite signals', 'nl': 'Zeekabels en satellietsignalen', 'src': ('R', 'cables')}, "+a,1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['cables']" not in t:
    t+='''
INTRO['cables']=("The cables under the sea that carry the internet and the satellite signal that tells ships and aircraft where they are: both under pressure, and both outside any single country's reach.","De kabels onder zee die het internet dragen en het satellietsignaal dat schepen en vliegtuigen hun plaats geeft: allebei onder druk, en allebei buiten het bereik van een enkel land.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '#p-cables td' not in t:
    t=t.replace('</style>','@media(max-width:699px){#p-cables td,#p-cables th{overflow-wrap:anywhere;padding-left:3px;padding-right:3px;font-size:12px}#p-cables .tag{font-size:9px;letter-spacing:0;padding:1px 4px}#p-cables table{table-layout:fixed;width:100%}}\n</style>',1)
    open(a,'w',encoding='utf-8').write(t)
# nuance the transport pages with what skeyes said
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
for sid in ('transport','transporteu'):
    s=R.find('section',id=sid)
    if not s: continue
    for e in s.find_all(['td','li']):
        tx=e.get_text()
        if 'north of Texel' in tx and 'skeyes' not in tx and 'air traffic service' not in tx:
            for c in e.contents:
                if isinstance(c,str) and 'speculation' in c:
                    c.replace_with(c.replace('that link is speculation.','that link is speculation. Belgium’s own air traffic service later told VRT it had received no reports of jamming or spoofing that day.'))
                elif isinstance(c,str) and 'suspect deliberate jamming' in c and 'skeyes' not in c:
                    c.replace_with(c.replace('suspect deliberate jamming.','suspect deliberate jamming. Belgium’s own air traffic service later told VRT it had received no reports that day.'))
open(f,'w',encoding='utf-8').write(str(R))
print('cables ok')
