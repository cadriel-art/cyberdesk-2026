from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join('<span class="tag %s">%s</span> '%(T[x][1],T[x][0]) for x in s)
EV=[
('14 Mar 2025','Money','Huawei and the European Parliament','Belgian police raided more than 20 addresses and sealed two offices inside the European Parliament in an investigation into bribes paid by lobbyists for the Chinese company Huawei. Four people were charged with bribery and membership of a criminal organisation, a fifth with money laundering. Huawei lobbyists were banned from the Parliament.','C'),
('30 Apr 2025','Fakes','Deepfake of the prime minister','Fake videos of Prime Minister Bart De Wever promise viewers quick money through an investment platform; fake Le Soir articles go with them. Fact-checkers traced it to fraudsters. In May a deepfake also used the Flemish minister-president.','C','Fraud for money, not election manipulation.'),
('Sep 2025','Fakes','More deepfakes','A new fake video uses real footage of a 2024 interview with a forged voice of the prime minister; another fake advert adds a well-known VRT journalist.','C'),
('9 Oct 2025','Violence','Drone plot against the prime minister','Three young men were arrested in Antwerp; the federal prosecutor called the plot jihadist-inspired. See the page on drones and sabotage.','CS'),
('9 Dec 2025','Fakes','Fake party profiles','Fake Facebook profiles of Vlaams Belang and N-VA politicians lured followers into WhatsApp groups with "exclusive news" and investment advice.','C'),
('8–14 Dec 2025','Websites','Provinces and towns knocked offline','The pro-Russian group NoName057(16) aimed 57.3% of all its attacks that week at Belgium, by a security firm\'s count.','R'),
('17–18 Dec 2025','Pressure','Intimidation over the frozen Russian money','The Guardian, quoting European intelligence and security officials, reported a Russian intimidation campaign against Belgian politicians and the bosses of Euroclear, the Brussels firm that holds about €185 billion of frozen Russian assets. The sources believe Russian military intelligence is behind it but disagree on how serious the threat is. The prime minister\'s spokesman would not comment, for safety reasons.','RS','Reported by one newspaper on unnamed sources; no Belgian service has confirmed it.'),
('Dec 2025','Pressure','The prime minister\'s own words','Bart De Wever said publicly: "Moscow has let us know that in the event of a seizure, Belgium and I personally will feel the effects for eternity."','C'),
('2026','Law','Spying and foreign interference become crimes','Belgium\'s new Penal Code, voted in February 2024, replaces the code of 1867 and comes into force in 2026. Spying and foreign interference are punishable in peacetime, and secretly influencing democratic processes to harm national interests counts as interference. The exact date of entry into force was not verified.','C'),
('30 Apr 2026','Voting','A new voting system','The government approved a draft agreement to develop a new electronic voting system that works offline. The present voting computers have been in use since 2012 and the supplier\'s contract ends in January 2027. Background: in June 2024 at least 2,171 voters were given the wrong ballots.','C'),
('May–Sep 2026','Spying','Three cases linked to China','A chip researcher held since May for allegedly sending secrets to a Chinese copy of his company; a Canadian former NATO intern arrested in July, suspected of spying for China; a Chinese national arrested in September over chip secrets. From press reports; investigations continue.','RS'),
('29 May 2026','Spying','State secrets to people linked to Russia','A 46-year-old man was arrested. See the page on drones and sabotage.','CS'),
('16 Jun 2026','Money','Immunity vote in the Huawei case','The European Parliament lifted the immunity of one Italian member (344 for, 234 against, 25 abstentions) and kept it for the others whom Belgian prosecutors had asked about; reports differ on whether that is three or four. He denies wrongdoing. By September one outlet called the investigation stalled, with about 15 current and former members drawn in.','C'),
('3 Jul 2026','Spyware','Pegasus on the phone of a member of the spyware inquiry','Researchers at Citizen Lab found that the iPhone of a former Greek member of the European Parliament was infected at least three times with the spyware Pegasus in 2022 and 2023, while he sat on the Parliament\'s own committee investigating spyware. The Parliament says a detection service has been open to all members since 2022. Belgian member Saskia Bricmont called for binding rules. No state has been named.','C'),
('Sep 2026','Accounts','X accounts of two Flemish politicians hijacked','The profiles of Sander Loones and Siegfried Bracke were taken over by crypto fraudsters, who posted forged photos of expensive cars supposedly bought with crypto profits.','C','Fraud for money.'),
]
rows=''.join('<tr><td class="nowrap"><b>%s</b><br><span class="small">%s</span></td><td><b>%s.</b> %s%s</td><td>%s</td></tr>'%(r[0],r[1],r[2],r[3],(' <span class="small"><i>%s</i></span>'%r[5]) if len(r)>5 else '',tg(r[4])) for r in EV)
SEC='''<section id="elections">
<h2>Elections and democracy: Belgium</h2>
<p class="sub">Attacks on politics itself in 2025 and 2026: fakes, hijacked accounts, spyware, bribery, spying and pressure on politicians. The Belgian institutions and the European Parliament in Brussels together. The other countries follow.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>Belgium held no national, regional or local election in 2025 or 2026: the last were in June and October 2024. So there was no vote to attack, and no attack on a vote is on record. What these two years show is pressure on the people and places of politics. Fraudsters use fake videos of the prime minister to sell fake investments. A Chinese company's lobbyists are charged with bribing members of the European Parliament. A member of the Parliament's spyware inquiry turns out to have had spyware on his own phone. And one newspaper reports that Russian intelligence tried to frighten Belgian politicians over the frozen Russian money held in Brussels.</p>
<p class="pb-nl"><b>NL:</b> België hield in 2025 en 2026 geen nationale, regionale of lokale verkiezingen: de laatste waren in juni en oktober 2024. Er was dus geen stembusgang om aan te vallen, en er is geen aanval op een stembusgang bekend. Wat deze twee jaar tonen, is druk op de mensen en plaatsen van de politiek. Oplichters gebruiken nepvideo's van de premier om nepbeleggingen te verkopen. Lobbyisten van een Chinees bedrijf worden beschuldigd van het omkopen van leden van het Europees Parlement. Een lid van de spyware-onderzoekscommissie van het Parlement blijkt zelf spyware op zijn telefoon te hebben gehad. En één krant meldt dat de Russische inlichtingendienst Belgische politici probeerde bang te maken over het bevroren Russische geld in Brussel.</p></div>
<div class="warnbox"><b>Labels.</b> <span class="tag t-conf">Confirmed</span> stated by an authority, a court, the organisation itself or named researchers. <span class="tag t-rep">Reported</span> in the press, not verified. <span class="tag t-susp">Suspected</span> believed, not proven: this includes anyone arrested or charged but not yet judged. <span class="tag t-claim">Claimed</span> said by one party without public evidence. Two labels on one line: the first is for the event, the second for who was behind it.</div>
<h3>Figures</h3>
<table><thead><tr><th>Figure</th><th>What it is</th><th>Source</th></tr></thead><tbody>
<tr><td><b>0</b></td><td>Elections held in Belgium in 2025–2026, and attacks on a vote on record.</td><td>Election calendar; searches</td></tr>
<tr><td><b>5</b></td><td>People charged in the Huawei bribery case (four for bribery, one for money laundering).</td><td>Belgian federal prosecutor, via press</td></tr>
<tr><td><b>1</b></td><td>Member of the European Parliament whose immunity was lifted in that case, of four or five requested.</td><td>European Parliament vote, 16 June 2026</td></tr>
<tr><td><b>3 times</b></td><td>A parliamentarian's phone was infected with Pegasus while he investigated spyware.</td><td>Citizen Lab, July 2026</td></tr>
<tr><td><b>€185 billion</b></td><td>Frozen Russian assets held at Euroclear in Brussels, the reason for the reported pressure.</td><td>Press</td></tr>
<tr><td><b>2012</b></td><td>Year the present voting computers came into use; the supplier's contract ends in January 2027.</td><td>Federal government</td></tr>
<tr><td><b>2,171</b></td><td>Voters given the wrong ballots in June 2024 (a human mistake, not an attack). Background.</td><td>College of experts</td></tr>
</tbody></table>
<h3>What happened, in order</h3>
<table><thead><tr><th>Date</th><th>Event</th><th>Status</th></tr></thead><tbody>'''+rows+'''</tbody></table>
<h3>By kind of threat</h3>
<table><thead><tr><th>Kind</th><th>What was seen</th><th>Who was behind it</th></tr></thead><tbody>
<tr><td><b>Fakes and hijacked accounts</b></td><td>Deepfakes of the prime minister, fake party profiles, two hijacked X accounts</td><td>Fraudsters after money, in every case found</td></tr>
<tr><td><b>Bribery</b></td><td>Lobbyists paying members of the European Parliament</td><td>Lobbyists for Huawei (charged, not judged)</td></tr>
<tr><td><b>Spyware</b></td><td>Pegasus on a parliamentarian's phone</td><td>Nobody named</td></tr>
<tr><td><b>Spying</b></td><td>Arrests linked to China and to Russia</td><td>Suspected; no verdict</td></tr>
<tr><td><b>Intimidation</b></td><td>Reported threats over the frozen Russian assets</td><td>Russian military intelligence, according to unnamed officials</td></tr>
<tr><td><b>Websites knocked offline</b></td><td>Provinces and towns, December 2025</td><td>A pro-Russian group that claims its attacks</td></tr>
<tr><td><b>The vote itself</b></td><td>Nothing: no election was held</td><td>—</td></tr>
</tbody></table>
<h3>Proven and not proven</h3>
<table><thead><tr><th>Proven</th><th>Not proven</th></tr></thead><tbody>
<tr><td>Deepfakes of Belgian politicians circulate widely.</td><td>That any was made to influence a vote. Those examined were investment fraud.</td></tr>
<tr><td>People were charged with bribing parliamentarians for Huawei.</td><td>That any parliamentarian took a bribe: none has been tried, and most kept their immunity.</td></tr>
<tr><td>Spyware was on the phone of a member of the spyware inquiry.</td><td>Who put it there.</td></tr>
<tr><td>The prime minister said Moscow threatened him over the frozen assets.</td><td>The wider intimidation campaign: one newspaper, unnamed sources, no official confirmation.</td></tr>
</tbody></table>
<p class="pl"><b>What it shows:</b> In Belgium the fake video is, so far, a tool of thieves, not of foreign states. The pressure on democracy that is on record came through older routes: money for lobbyists, spyware on a phone, a threat passed to a prime minister. The next real test is the next election, and the voting computers will be replaced before it.<span class="plnl"><b>NL – Wat het toont:</b> In België is de nepvideo voorlopig een werktuig van dieven, niet van vreemde staten. De druk op de democratie die bekend is, kwam langs oudere wegen: geld voor lobbyisten, spyware op een telefoon, een dreigement aan een premier. De volgende echte test is de volgende verkiezing, en de stemcomputers worden daarvoor vervangen.</span></p>
<h3>Still open</h3>
<ul>
<li>The investigation opened in April 2024 into politicians paid by Russia through the "Voice of Europe" network: no update found.</li>
<li>Whether the Huawei case reaches a court, and when.</li>
<li>Who infected the parliamentarian's phone.</li>
<li>Whether Belgian security services confirm the intimidation over the frozen assets.</li>
<li>The exact date the new Penal Code applies, and the first case brought under its interference rules.</li>
<li>How Belgian parties protect their own systems and candidates: nothing public found.</li>
<li>Websites of the Flemish Parliament and the Belga news agency were knocked offline in October 2024, around the local elections. That is just outside this file's two years.</li>
</ul>
<p class="src">Sources: see the linked list below.</p>
</section>'''
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='elections')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'elections'" not in t:
    a="{'k': 'more', 'en': 'More subjects to explore'"; assert a in t
    t=t.replace(a,"{'k': 'elections', 'en': 'Elections and democracy: Belgium', 'nl': 'Verkiezingen en democratie: België', 'src': ('R', 'elections')}, "+a,1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['elections']" not in t:
    t+='''
INTRO['elections']=("Attacks on politics itself in Belgium and at the European Parliament: fakes, hijacked accounts, spyware, bribery, spying and threats.","Aanvallen op de politiek zelf in België en bij het Europees Parlement: vervalsingen, gekaapte accounts, spyware, omkoping, spionage en dreigementen.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '#p-elections td' not in t:
    t=t.replace('</style>','@media(max-width:699px){#p-elections td,#p-elections th{overflow-wrap:anywhere;padding-left:3px;padding-right:3px;font-size:12px}#p-elections .tag{font-size:9px;letter-spacing:0;padding:1px 4px}#p-elections table{table-layout:fixed;width:100%}}\n</style>',1)
    open(a,'w',encoding='utf-8').write(t)
print('elections ok')
