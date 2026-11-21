from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join(' <span class="tag %s">%s</span>'%(T[x][1],T[x][0]) for x in s)
D={
'Denmark':([('Late 2024','Attackers changed the water pressure at the Tureby Alkestrup waterworks near Køge; at least three pipes burst and homes were left without water. The head of the waterworks said it happened after a switch to cheaper, weaker security.','C'),
 ('19 Dec 2025','The Danish Defence Intelligence Service publicly blamed Russia: the attack was carried out by the pro-Russian group Z-Pentest, which the service says the Russian state uses as an instrument. Denmark summoned the Russian ambassador. Denmark\'s first public attribution of this kind.','CK')],
 'A small waterworks saved money on security and pipes burst.','Een klein waterbedrijf bespaarde op beveiliging en de leidingen sprongen.'),
'Germany':([('Late Jun 2026','The municipal utilities of Kamen, Bönen and Bergkamen were attacked; the customer portal and direct debits failed, the supply did not.','R'),
 ('2026','Only water suppliers serving 500,000 people or more fall under the German rules for critical infrastructure; most are below that line. No case found of attackers taking over the controls of a German water plant.','R')],
 'Most German water suppliers are too small to fall under the strict rules.','De meeste Duitse waterbedrijven zijn te klein om onder de strenge regels te vallen.'),
'Netherlands':([('11 Aug 2025','The intelligence service warned that Dutch water and power companies had been targeted; an official said Russia is "embedding itself" in vital sectors so it can disrupt them later. No disruption so far.','CK')],
 'A warning about attackers getting ready, not about damage done.','Een waarschuwing over aanvallers die zich voorbereiden, niet over aangerichte schade.'),
'Norway':([('7 Apr 2025','Attackers opened a valve at a dam in Bremanger and let about 500 litres of water per second run for four hours before it was noticed. No damage. The way in was a weak password on a control panel reachable from the internet.','C'),
 ('Aug 2025','The head of the security service attributed it to pro-Russian hackers. The Russian embassy called that unfounded. One legal study notes that no formal written attribution has been published.','CK')],
 'One weak password moved real water.','Eén zwak wachtwoord zette echt water in beweging.'),
'Poland':([('2025','Attackers got into the control systems of five water treatment plants: Jabłonna Lacka, Szczytno, Małdyty, Tolkmicko and Sierakowo. They had administrator rights and could change pump settings and alarm limits. The way in: factory passwords never changed and control systems reachable from the internet. From the security agency\'s report of May 2026.','C'),
 ('2025','Who did it: the agency\'s report names Russian and Belarusian state groups in general, but did not formally pin these five break-ins on them. Researchers call the attribution unconfirmed.','S'),
 ('Aug 2025','The deputy prime minister said an attempt to break into the water supply of a large Polish city had been stopped. The city was not named.','CK')],
 'The clearest European case: five plants, default passwords, open to the internet.','Het duidelijkste Europese geval: vijf installaties, standaardwachtwoorden, open naar het internet.'),
'Romania':([('Dec 2025','Ransomware hit the national water authority Apele Române: about 1,000 computer systems affected. Dams and water operations kept running. The attackers used a standard Windows encryption tool. Nobody claimed it and the authority named nobody.','C')],
 'The offices went down; the dams did not, because the two were separate.','De kantoren vielen uit; de dammen niet, omdat de twee gescheiden waren.'),
'Spain':([('21 Apr 2025','Ransomware at Aigües de Mataró, which serves about 130,000 people: internal systems encrypted, customer data exposed. Supply and water quality not affected (company statement). The year is inferred; the report found gives only the day.','C'),
 ('3 Jul 2026','The public water company Acosol (Málaga) reported an attack that affected its information systems and may have exposed customer data.','R')],
 'Office systems and customer data were hit, not the water.','Kantoorsystemen en klantgegevens werden geraakt, niet het water.'),
}
NONE=['Austria','Bulgaria','Croatia','Cyprus','Czechia','Estonia','Finland','France','Greece','Hungary','Iceland','Ireland','Italy','Latvia','Liechtenstein','Lithuania','Luxembourg','Malta','Portugal','Slovakia','Slovenia','Sweden','Switzerland']
assert len(D)+len(NONE)==30
def card(n):
    ev,se,sn=D[n]
    return '<div class="country" id="w-%s"><h4>%s <small>%d on record</small></h4><ul>%s</ul><p class="pl"><b>What it shows:</b> %s<span class="plnl"><b>NL – Wat het toont:</b> %s</span></p></div>'%(n,n,len(ev),''.join('<li><b>%s:</b> %s%s</li>'%(d,t,tg(s)) for d,t,s in ev),se,sn)
SEC='''<section id="watereu">
<h2>Water: the other 30 countries</h2>
<p class="sub">Attacks on drinking water, waste water and dams in the other 26 EU countries plus Norway, Iceland, Switzerland and Liechtenstein, 2025 and 2026. Something is on record for %d countries; for %d nothing was found.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>In three countries attackers reached the machinery itself: a valve opened at a Norwegian dam, pipes burst at a Danish waterworks, and five Polish treatment plants had their controls taken over. All three got in the same simple way: a weak or factory password on a control panel that could be reached from the internet. In Romania and Spain the offices were hit by ransomware but the water kept flowing, because offices and machinery were kept apart. For most countries nothing is on record.</p>
<p class="pb-nl"><b>NL:</b> In drie landen raakten aanvallers tot bij de machines zelf: een klep geopend aan een Noorse dam, gesprongen leidingen bij een Deens waterbedrijf, en vijf Poolse zuiveringsinstallaties waarvan de besturing werd overgenomen. Alle drie kwamen op dezelfde eenvoudige manier binnen: een zwak of standaardwachtwoord op een bedieningspaneel dat vanaf het internet bereikbaar was. In Roemenië en Spanje werden de kantoren getroffen door ransomware, maar het water bleef stromen, omdat kantoren en machines gescheiden waren. Voor de meeste landen is niets bekend.</p></div>
<div class="warnbox"><b>Labels.</b> <span class="tag t-conf">Confirmed</span> stated by the organisation, an authority or a court. <span class="tag t-rep">Reported</span> in the press, not verified. <span class="tag t-susp">Suspected</span> believed, not proven. <span class="tag t-claim">Claimed</span> said by one party (a government, a minister) without evidence shown in public or tested in court. Two labels on one line: the first is for the event, the second for who was behind it.</div>
<h3>Did they reach the machinery?</h3>
<table><thead><tr><th>Country</th><th>What was reached</th><th>Way in</th><th>Who, and how firm</th></tr></thead><tbody>
<tr><td><b>Poland</b>, 2025</td><td>Controls of five treatment plants</td><td>Factory passwords, controls open to the internet</td><td>Not formally attributed</td></tr>
<tr><td><b>Norway</b>, Apr 2025</td><td>A dam valve, open for four hours</td><td>Weak password on an internet-facing panel</td><td>Security service chief: pro-Russian hackers; Russia denies</td></tr>
<tr><td><b>Denmark</b>, late 2024</td><td>Water pressure; three pipes burst</td><td>Weaker, cheaper security</td><td>Intelligence service blames Russia (Dec 2025)</td></tr>
<tr><td><b>Romania</b>, Dec 2025</td><td>Offices only (about 1,000 systems)</td><td>Ransomware</td><td>Nobody named</td></tr>
<tr><td><b>Spain</b>, 2025 and 2026</td><td>Offices and customer data only</td><td>Ransomware</td><td>Nobody named</td></tr>
</tbody></table>
<h3>Counts and assessments by others</h3>
<ul>
<li>The EU cyber agency ENISA ranks drinking water and waste water among the least mature sectors it assessed (2026). <span class="tag t-conf">Confirmed</span></li>
<li>The water sector's own information centre (WaterISAC) says water companies were the largest group of targets seen in activist-hacker activity in 2025. <span class="tag t-claim">Claimed</span></li>
<li>United States, from 27 July 2026: water companies in at least seven states reported attackers changing settings on control devices reachable from the internet (FBI). Outside Europe, kept as the warning case. <span class="tag t-conf">Confirmed</span></li>
</ul>
<h3>Countries with something on record</h3>
<div class="countries">%s</div>
<h3>Nothing found</h3>
<p>%s.</p>
<p class="small">Nothing found means nothing came up in searches in English and the main national languages on 15 November 2026. It is not proof that nothing happened: small water companies rarely make the news, and many countries do not publish incidents.</p>
<p class="pl"><b>What it shows:</b> Water is attacked less often than hospitals or town halls, but it is where attackers have most often reached real machinery. The three cases where that happened share one cause that costs almost nothing to fix: a control panel on the open internet with a weak password.<span class="plnl"><b>NL – Wat het toont:</b> Water wordt minder vaak aangevallen dan ziekenhuizen of gemeentehuizen, maar het is de sector waar aanvallers het vaakst echte machines bereikten. De drie gevallen waar dat gebeurde, hebben één oorzaak gemeen die bijna niets kost om op te lossen: een bedieningspaneel op het open internet met een zwak wachtwoord.</span></p>
<p class="src">Sources: see the linked list below.</p>
</section>'''%(len(D),len(NONE),''.join(card(n) for n in sorted(D)),', '.join(NONE))
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='watereu')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
# Belgium water page: pointer to the other countries
w=R.find('section',id='water'); p=w.find('p',class_='sub'); p.string=p.get_text().replace('The other countries follow.','The other 30 countries have their own page.')
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'watereu'" not in t:
    a="'src': ('R', 'water')}, "; assert a in t
    t=t.replace(a,a+"{'k': 'watereu', 'en': 'Water: 30 countries', 'nl': 'Water: 30 landen', 'src': ('R', 'watereu')}, ",1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['watereu']" not in t:
    t+='''
INTRO['watereu']=("Where attackers reached water plants and dams in the other 30 countries, how they got in, and who was blamed.","Waar aanvallers waterinstallaties en dammen bereikten in de andere 30 landen, hoe ze binnenkwamen, en wie de schuld kreeg.")
'''
    open(l,'w',encoding='utf-8').write(t)
print('water2 ok')
