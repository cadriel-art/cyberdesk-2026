from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join(' <span class="tag %s">%s</span>'%(T[x][1],T[x][0]) for x in s)
D={
'Denmark':([('Oct 2025','After the drone reports Denmark banned all civilian drone flights for the days when European leaders met in Copenhagen.','C')],'A ban on flying, not a rule for shooting.','Een vliegverbod, geen regel om te schieten.'),
'Estonia':([('2025–2026','The army\'s Cyber Command has about 300 people. Behind it stands the cyber unit of the volunteer Defence League, staffed by IT professionals; in wartime the command would grow to about four times its size from that pool. A separate civilian cyber reserve of the state IT authority has held five exercises with operators of vital services, the latest at Tallinn Airport.','C'),
 ('2026','Estonia spends an estimated 5.1% of its economy on core defence.','C')],
 'The model others look at: volunteers from the IT sector, practised every year.','Het model waar anderen naar kijken: vrijwilligers uit de IT-sector, die elk jaar oefenen.'),
'Finland':([('Dec 2025','Finland and Poland announced that they will jointly lead the EU project to guard the eastern border (Eastern Flank Watch).','C'),
 ('Jan–Apr 2026','A break-in at the phone-management service of the state IT centre Valtori reportedly exposed data on military officers, diplomats and counter-terrorism staff; police widened the investigation in April.','CR')],
 'Even here the soldiers\' data leaked through an office service, not through the army.','Zelfs hier lekten de gegevens van militairen via een kantoordienst, niet via het leger.'),
'France':([('2025–2030','The army is building a Cyber Defence Regiment that will reach 400 people from the three services by 2030, next to its cyber command.','C'),
 ('Aug (year not confirmed)','Parliament passed a law letting approved operators of vital infrastructure and their contractors detect, jam and shoot down drones near designated sites. Reported in October 2026.','R'),
 ('2026','An estimated 2.22% of the economy on core defence.','C')],
 'The first country to let the owners of power plants and airports bring down drones themselves.','Het eerste land dat de eigenaars van centrales en luchthavens zelf drones laat neerhalen.'),
'Germany':([('Jun 2025','The Cyber and Information Domain Service, a full branch of the armed forces, counted 15,659 people.','C'),
 ('26 Feb 2026','Parliament changed the aviation security law: the armed forces may jam or shoot down drones when a state asks for help, and the defence ministry decides alone. Flying a drone into an airport\'s security zone became a crime.','C'),
 ('2026','An estimated 2.69% of the economy on core defence.','C')],
 'By far the largest military cyber branch in the EU, and now a legal basis to shoot at drones at home.','Veruit de grootste militaire cybertak in de EU, en nu een wettelijke basis om in eigen land op drones te schieten.'),
'Greece':([('5 Feb 2026','A high-ranking military officer was arrested on espionage charges; for whom is not stated in the reports found.','CS'),
 ('Apr 2026','Reuters reported that Russia-linked hackers broke into 27 email accounts of the Hellenic National Defence General Staff, part of a wider campaign whose main target was Ukraine. The General Staff did not answer questions. Less established outlets name the Russian military-intelligence group APT28.','RK'),
 ('2026','An estimated 3.65% of the economy on core defence.','C')],
 'The one EU army whose own mailboxes are reported broken into in these two years.','Het enige EU-leger waarvan de eigen mailboxen in deze twee jaar gekraakt zouden zijn.'),
'Italy':([('2026','A proposal for a national military cyber body: 1,200 to 1,500 people at first, growing to 5,000 including reservists. An estimated 2.1% of the economy on core defence.','R')],'A plan on paper.','Een plan op papier.'),
'Latvia':([('2026','An estimated 4.92% of the economy on core defence. The July 2026 draft drew a record 1,560 volunteers; the aim is 4,000 conscripts a year by 2028.','C')],'Money and conscripts, no separate cyber figure found.','Geld en dienstplichtigen, geen apart cybercijfer gevonden.'),
'Lithuania':([('2026','The highest spender in NATO: an estimated 5.33% of the economy on core defence. 5,000 conscripts are called up for 2026, with new cyber training. Lithuania is named among the countries that passed a law on bringing down drones; no details found. It has no civilian volunteer cyber reserve.','CR')],
 'The biggest budget, but no volunteer cyber reserve like Estonia\'s.','Het grootste budget, maar geen vrijwillige cyberreserve zoals die van Estland.'),
'Netherlands':([('2025–2026','The defence cyber strategy of 2025 treats cyber as a military domain in its own right; a defence cyber academy is being set up and recruitment for the cyber command is a priority. The Netherlands commits to NATO\'s 3.5% for core defence only, not to the extra 1.5%.','C')],
 'Building the school before the force.','Eerst de school bouwen, dan de strijdmacht.'),
'Norway':([('2026','Norway takes part in the EU\'s Eastern Flank Watch and commits to the 3.5% for core defence only.','C')],'In the EU project without being in the EU.','In het EU-project zonder in de EU te zitten.'),
'Poland':([('2026','About 6,500 people in the Cyberspace Defence Forces, with defensive, reconnaissance and offensive tasks, plus a reserve called the Cyber Legion of around 3,000 (ministry, February 2026).','C'),
 ('2026','An estimated 4.68% of the economy on core defence. Poland co-leads Eastern Flank Watch and says it wants a working drone wall within three months, a national timetable.','CK')],
 'A cyber army of thousands with a reserve half its size.','Een cyberleger van duizenden met een reserve die half zo groot is.'),
'Portugal':([('2026','An estimated 2.1% of the economy on core defence. Nothing specific on cyber forces found.','C')],'Only the spending figure.','Alleen het uitgavencijfer.'),
'Romania':([('2025','The president signed a law allowing troops to shoot down drones in Romanian airspace. Date taken from a headline.','R')],'A law made for drones that stray in from the war next door.','Een wet gemaakt voor drones die uit de oorlog ernaast binnendwalen.'),
'Spain':([('2 Feb 2026','The Joint Cyberspace Command presented a growth plan: 1,500 people by 2030, three times its present strength.','C')],'Tripling in four years, from a small base.','Verdrievoudigen in vier jaar, vanaf een kleine basis.'),
}
NONE=['Austria','Bulgaria','Croatia','Cyprus','Czechia','Hungary','Iceland','Ireland','Liechtenstein','Luxembourg','Malta','Slovakia','Slovenia','Sweden','Switzerland']
assert len(D)+len(NONE)==30,(len(D),len(NONE))
def card(n):
    ev,se,sn=D[n]
    return '<div class="country" id="f-%s"><h4>%s <small>%d on record</small></h4><ul>%s</ul><p class="pl"><b>What it shows:</b> %s<span class="plnl"><b>NL – Wat het toont:</b> %s</span></p></div>'%(n,n,len(ev),''.join('<li><b>%s:</b> %s%s</li>'%(d,t,tg(s)) for d,t,s in ev),se,sn)
nev=sum(len(D[n][0]) for n in D)
SEC='''<section id="defenceeu">
<h2>The defence side: the other 30 countries</h2>
<p class="sub">Military cyber forces, reserves, money and the rules for acting at home, in the other 26 EU countries plus Norway, Iceland, Switzerland and Liechtenstein, 2025 and 2026. @@N@@ entries in @@C@@ countries.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>Three things stand out. First, size: Germany has a whole branch of its armed forces for cyber with more than 15,000 people and Poland about 6,500 plus a reserve; most others have a few hundred. Second, the countries nearest to Russia spend far more: Lithuania, Estonia, Latvia and Poland are all above 4.5% of their economy, against about 2% for Belgium, Italy and Portugal. Third, the law is catching up with drones: Germany now lets its army jam or shoot them down at home, France lets the owners of vital sites do it, and Europe is discussing the same for utilities. On cyber help for hospitals and towns, only Estonia has a practised volunteer reserve.</p>
<p class="pb-nl"><b>NL:</b> Drie dingen vallen op. Eén, de omvang: Duitsland heeft een hele tak van zijn strijdkrachten voor cyber met meer dan 15.000 mensen en Polen ongeveer 6.500 plus een reserve; de meeste andere hebben er enkele honderden. Twee, de landen het dichtst bij Rusland geven veel meer uit: Litouwen, Estland, Letland en Polen zitten allemaal boven 4,5% van hun economie, tegen ongeveer 2% voor België, Italië en Portugal. Drie, de wet haalt de drones in: Duitsland laat zijn leger ze nu in eigen land storen of neerhalen, Frankrijk laat de eigenaars van vitale sites dat doen, en Europa bespreekt hetzelfde voor nutsbedrijven. Voor cyberhulp aan ziekenhuizen en gemeenten heeft alleen Estland een geoefende vrijwilligersreserve.</p></div>
<div class="warnbox"><b>Labels.</b> <span class="tag t-conf">Confirmed</span> stated by a government, an army, NATO or the EU. <span class="tag t-rep">Reported</span> in the press, not verified. <span class="tag t-claim">Claimed</span> said by one party without public evidence. <span class="tag t-susp">Suspected</span> arrested or believed, not judged. Two labels on one line: the first is for the event, the second for a detail or for who was behind it.</div>
<h3>Spending on core defence, 2026</h3>
<p class="small">NATO estimates published in July 2026, as reported by Reuters: share of the economy spent on core defence. NATO's goal, agreed in The Hague in June 2025, is 3.5% for core defence plus up to 1.5% for wider security such as cybersecurity and vital infrastructure, by 2035.</p>
<table><thead><tr><th>Country</th><th>Share of the economy</th><th>Note</th></tr></thead><tbody>
<tr><td><b>Lithuania</b></td><td>5.33%</td><td>Highest in NATO</td></tr>
<tr><td><b>Estonia</b></td><td>5.1%</td><td></td></tr>
<tr><td><b>Latvia</b></td><td>4.92%</td><td></td></tr>
<tr><td><b>Poland</b></td><td>4.68%</td><td></td></tr>
<tr><td><b>Greece</b></td><td>3.65%</td><td>The fifth country already above 3.5%</td></tr>
<tr><td><b>Germany</b></td><td>2.69%</td><td></td></tr>
<tr><td><b>France</b></td><td>2.22%</td><td></td></tr>
<tr><td><b>Italy</b>, <b>Portugal</b></td><td>2.1%</td><td></td></tr>
<tr><td><b>Belgium</b></td><td>2.0%</td><td>Plus 1.43% counted as resilience (see the Belgium page)</td></tr>
<tr><td><b>European members and Canada together</b></td><td>2.53%</td><td></td></tr>
</tbody></table>
<h3>How big the military cyber forces are</h3>
<table><thead><tr><th>Country</th><th>People</th><th>Reserve or volunteers</th></tr></thead><tbody>
<tr><td><b>Germany</b></td><td>15,659 (June 2025), a full branch of the armed forces</td><td>Not found</td></tr>
<tr><td><b>Poland</b></td><td>About 6,500</td><td>Cyber Legion, around 3,000</td></tr>
<tr><td><b>Spain</b></td><td>About 500 now; 1,500 planned for 2030</td><td>Not found</td></tr>
<tr><td><b>Italy</b></td><td>Proposed: 1,200–1,500, later 5,000</td><td>Included in the proposal</td></tr>
<tr><td><b>France</b></td><td>A new regiment of 400 by 2030, next to the cyber command</td><td>Not found</td></tr>
<tr><td><b>Estonia</b></td><td>About 300</td><td>Volunteer Defence League cyber unit; grows fourfold in war</td></tr>
<tr><td><b>Belgium</b></td><td>Not public</td><td>About a quarter of staff are reservists</td></tr>
</tbody></table>
<p class="small">Spain's present strength is worked out from "tripling to 1,500"; it is not a published figure. The sizes are not comparable one to one: Germany's branch also covers signals and intelligence.</p>
<h3>Rules for bringing down drones at home</h3>
<table><thead><tr><th>Country</th><th>Who may act</th><th>Since</th></tr></thead><tbody>
<tr><td><b>Germany</b></td><td>The armed forces, at the request of a state; the defence ministry decides alone</td><td>26 February 2026</td></tr>
<tr><td><b>France</b></td><td>Approved operators of vital infrastructure and their contractors</td><td>A law passed in August; year not confirmed</td></tr>
<tr><td><b>Romania</b></td><td>The army, in national airspace</td><td>2025 (reported)</td></tr>
<tr><td><b>Lithuania</b></td><td>A similar law is reported; no details found</td><td>—</td></tr>
<tr><td><b>Belgium</b></td><td>No such law found; emergency equipment bought in 2025</td><td>—</td></tr>
</tbody></table>
<p class="small">On 21 October 2026 Reuters reported that Europe is weighing more powers for utilities and infrastructure companies to bring down drones.</p>
<h3>At EU and NATO level</h3>
<ul>
<li><b>Eastern Flank Watch</b>, with its "drone wall": approved as a joint project by member states on 28 September 2026, with an indicative €60 to 100 billion up to 2036; twelve member states plus Norway and Ukraine take part; Finland and Poland lead. A first capacity against drones is promised for the end of 2026 and full operation for 2027–2028. Critics say that so far it is mostly a budget line. <span class="tag t-conf">Confirmed</span> <span class="tag t-claim">Claimed</span></li>
<li><b>Attacks on the arms industry:</b> the EU institutions' own cyber team reported a suspected Russia-linked campaign against European defence companies in August 2026; the French defence group Thales confirmed a data leak through an outside firm in May 2026. <span class="tag t-conf">Confirmed</span> <span class="tag t-susp">Suspected</span></li>
</ul>
<h3>Countries with something on record</h3>
<div class="countries">@@CARDS@@</div>
<h3>Nothing specific found</h3>
<p>@@NONE@@.</p>
<p class="small">Nothing found means the searches of 16 November 2026 gave no figure or event for the country's military cyber side; several of these countries are neutral or not in NATO. Sweden and Finland have volunteer units, but no numbers were found.</p>
<p class="pl"><b>What it shows:</b> Armies are getting money and, slowly, the legal right to act at home, first of all against drones. What almost nobody has is the bridge to civilian life that Estonia built years ago: IT people who volunteer, train with the airport and the hospital every year, and are called when it goes wrong. That costs little compared with air defence, and it is the part that would have helped in most of the attacks in this file.<span class="plnl"><b>NL – Wat het toont:</b> Legers krijgen geld en, langzaam, het wettelijke recht om in eigen land op te treden, in de eerste plaats tegen drones. Wat bijna niemand heeft, is de brug naar het burgerleven die Estland jaren geleden bouwde: IT'ers die zich vrijwillig melden, elk jaar oefenen met de luchthaven en het ziekenhuis, en opgeroepen worden als het misgaat. Dat kost weinig in vergelijking met luchtverdediging, en het is het deel dat bij de meeste aanvallen in dit dossier geholpen zou hebben.</span></p>
<p class="src">Sources: see the linked list below.</p>
</section>'''.replace('@@N@@',str(nev)).replace('@@C@@',str(len(D))).replace('@@CARDS@@',''.join(card(n) for n in sorted(D))).replace('@@NONE@@',', '.join(NONE))
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='defenceeu')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
w=R.find('section',id='defence'); p=w.find('p',class_='sub'); p.string=p.get_text().replace('The other countries follow.','The other 30 countries have their own page.')
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'defenceeu'" not in t:
    a="'src': ('R', 'defence')}, "; assert a in t
    t=t.replace(a,a+"{'k': 'defenceeu', 'en': 'The defence side: 30 countries', 'nl': 'De defensiekant: 30 landen', 'src': ('R', 'defenceeu')}, ",1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['defenceeu']" not in t:
    t+='''
INTRO['defenceeu']=("Military cyber forces, reserves, spending and the rules for acting at home in the other 30 countries, side by side.","Militaire cybertroepen, reserves, uitgaven en de regels om in eigen land op te treden in de andere 30 landen, naast elkaar.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '#p-defenceeu td' not in t:
    t=t.replace('</style>','@media(max-width:699px){#p-defenceeu td,#p-defenceeu th{overflow-wrap:anywhere;padding-left:3px;padding-right:3px;font-size:12px}#p-defenceeu table{table-layout:fixed;width:100%}}\n</style>',1)
    open(a,'w',encoding='utf-8').write(t)
print('defence2 ok',nev,len(D))
