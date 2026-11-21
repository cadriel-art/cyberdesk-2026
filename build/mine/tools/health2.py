from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join(' <span class="tag %s">%s</span>'%(T[x][1],T[x][0]) for x in s)
D={
'Austria':([('23 Jul 2026','The ransomware group TheGentlemen listed a fertility clinic in Wels as a victim.','K')],'A claim on a criminal site.','Een bewering op een criminele site.'),
'Bulgaria':([('Date not found','The state IT company said it fought off a very large flood of traffic aimed at the national health information system.','R')],'The national system held.','Het nationale systeem hield stand.'),
'Croatia':([('Jun 2026','The Ministry of Health said an attack hit some of its applications; the system with patients\' medical data was not affected. The group TheGentlemen claimed the ministry and threatened to publish data.','CK')],'The ministry was hit, the patient files were kept apart.','Het ministerie werd geraakt, de patiëntendossiers stonden apart.'),
'Cyprus':([('Date not found','The Bank of Cyprus Oncology Centre confirmed that patient and staff data taken from its systems was published.','C')],'Cancer patients\' data ended up online.','Gegevens van kankerpatiënten kwamen online.'),
'Czechia':([('7 and 13 Jul 2026','Ransomware at two healthcare bodies, attributed to the Qilin group; the victims were not named.','R'),('Aug 2026','Patient and staff data of a Czech healthcare body were offered for sale.','R')],'Unnamed victims, known only from the criminals\' side.','Niet bij naam genoemde slachtoffers, alleen bekend van de kant van de criminelen.'),
'Denmark':([('1 Aug 2026','Hvidovre Hospital stopped ransomware on the network that runs the building\'s technical systems; access-card data of about 7,600 staff may have been taken. Patient care was not affected.','C'),('Date not found','Patient data leaked from a chain of GP practices.','R')],'The attack reached the building systems, not the wards.','De aanval bereikte de gebouwsystemen, niet de afdelingen.'),
'Estonia':([('2025','Criminals encrypted the patient data, records and appointments of a family medicine centre (national cyber agency).','C')],'Even a single GP practice is a target.','Zelfs één huisartsenpraktijk is een doelwit.'),
'Finland':([('Mar 2025','A breach at Pharmadata, an IT supplier to pharmacies, was called the most serious incident of the period by the national cyber centre.','C')],'A supplier to pharmacies, not a pharmacy.','Een leverancier van apotheken, geen apotheek.'),
'France':([('Summer 2025','A private hospital lost the data of 524,867 patients and of 202,246 contact persons. In September 2026 the data regulator fined it €500,000 for inadequate protection of its patient-record system.','C'),
 ('8 Sep 2025','Public hospitals in the Hauts-de-France region were targeted through the servers that hold patients\' identity data.','R'),
 ('2026','The health software company Cegedim Santé: the health minister confirmed the attack could concern more than 15 million people. The company had filed a criminal complaint in October 2025 and reportedly said nothing in public for four months.','C'),
 ('25 May 2026','The health-insurance payment operator Almerys confirmed a breach covering 15.4 million social security numbers.','C'),
 ('2 Jul 2026','Chaumont hospital: data lost and critical systems unavailable.','C'),
 ('20 Sep 2026','Hôpital Paris Saint-Joseph confirmed a leak covering 15,044 patients.','C'),
 ('1–2 Nov 2026','Cold rooms used by the French blood service (Établissement français du sang) at three sites were tampered with through an outside refrigeration contractor: temperature and defrost settings were pushed abnormally high, in the same night as the freezer attacks on supermarkets. The blood service says it was contained quickly, "without impact" on stored products and samples. The Paris prosecutor opened an investigation and gave it to the cybercrime office and the domestic intelligence service. Nobody has been named for this attack. Asked whether Iran was behind it, Foreign Minister Barrot declined to say while the investigation runs; the Paris prosecutor has not linked it to the supermarket cases.','C'),
 ('Nov 2026','The university hospital of Reims confirmed that patient data was exposed through an attack on the software maker Softway Medical; how many people is not known.','C')],
 'The biggest losses in Europe, and almost all through companies that serve the hospitals.','De grootste verliezen in Europa, en bijna allemaal via bedrijven die de ziekenhuizen bedienen.'),
'Germany':([('7 Jul 2025','The Ameos hospital group shut down all its systems after an attack; several states opened data-protection proceedings.','C'),
 ('Jan 2026','The district clinic in Roth (Bavaria) cut its internet link as a precaution; the emergency room closed briefly and prescriptions were written by hand.','C'),
 ('Feb 2026','BDH-Klinik Greifswald: the communication network was paralysed and theft of patient data was later confirmed.','C'),
 ('May 2026','A billing firm for hospitals lost the data of more than 100,000 private patients of university hospitals. In late May ransomware at a hospital group (not named) postponed operations and sent emergency patients elsewhere.','R'),
 ('Oct 2026','Charité Berlin: contact details of about 140,000 people.','R'),
 ('15 Nov 2026','The district hospital of Greiz-Ronneburg (Thuringia): the emergency room in Greiz could not take patients; state police and prosecutors were called in. The hospital says patient safety is not at risk.','C')],
 'Emergency rooms closed in four separate cases in eighteen months.','Spoedafdelingen sloten in vier afzonderlijke gevallen in achttien maanden.'),
'Iceland':([('Dec 2025','A break-in at the Grund care home exposed data on tens of thousands of people; disclosed in February 2026. Iceland\'s cyber team, Europol and Interpol investigate.','R')],'A care home held data on a large share of a small country.','Een woonzorgcentrum bewaarde gegevens over een groot deel van een klein land.'),
'Ireland':([('Late Mar 2026','The health-recruitment platform Healthdaq detected a break-in; a criminal group claims 431 GB, including CVs and identity documents.','CK'),
 ('15 Apr 2026','The medical-device maker Medtronic, headquartered in Dublin: health information of 3.8 million people reportedly stolen worldwide; the company attributes it to the ShinyHunters group.','RK')],
 'A device maker and a recruiter: health data sits in many places besides hospitals.','Een toestellenmaker en een rekruteerder: gezondheidsgegevens zitten op veel plaatsen buiten ziekenhuizen.'),
'Italy':([('May 2025','An activist-hacker group got into a hospital\'s camera system and published footage from operating rooms.','R'),
 ('Sep 2025','The public health body ASST Rhodense, which runs hospitals near Milan: stolen medical documents and prescriptions were published on the attackers\' site.','R'),
 ('2025–2026','A sector body counts 20% more attacks on hospitals in 2025, 47% of them ransomware. In 2026 at least four large private health facilities in Milan and Rome were reportedly hit, and the INC Ransom group listed the Policlinico Triestino (2 Sep 2026; not confirmed by the hospital).','RK')],
 'Operating-room video online: the damage is not only to files.','Beelden uit operatiekamers online: de schade zit niet alleen in dossiers.'),
'Lithuania':([('Jun 2026','About 62,000 records with personal data of doctors leaked from an agency of the Ministry of Health.','C')],'Here the doctors\' data leaked, not the patients\'.','Hier lekten de gegevens van artsen, niet van patiënten.'),
'Luxembourg':([('Date not found','A major attack on a firm that hosts health data for doctors\' practices was reported.','R')],'Again a host, not a practice.','Opnieuw een hostingbedrijf, geen praktijk.'),
'Netherlands':([('Jul 2025','The laboratory Clinical Diagnostics, which analyses cervical-cancer screening, was hit by ransomware. The count of people affected grew from more than 405,000 women to about 941,000 people in later reports. The health inspectorate found it had not met legal security standards.','C'),
 ('7 Apr 2026','Ransomware at ChipSoft, whose patient-record software runs in 70 to 80% of Dutch hospitals. Eleven hospitals cut their links; data came from its cloud service used by GPs, rehabilitation clinics and an eye hospital. A criminal group (Embargo) claimed 100 GB; ChipSoft said on 29 April that the stolen data was destroyed. The number of patients was never disclosed.','CK')],
 'One software maker serves most hospitals of a country: when it falls, they all cut the cord.','Eén softwaremaker bedient de meeste ziekenhuizen van een land: als die valt, trekken ze allemaal de stekker uit.'),
'Poland':([('8 and 13 Mar 2025','Ransomware at the Interior Ministry hospital in Kraków and at the Bonifraterskie Medical Centre in Warsaw.','C'),
 ('7–8 Mar 2026','The regional hospital in Szczecin worked on paper after ransomware; the attackers reportedly demanded several million dollars. Hospitals in Kraków and Szczecin needed national emergency support.','C'),
 ('24 Mar 2026','The Eskulap medical centre in Racibórz: records encrypted, high risk that data was stolen.','C'),
 ('2026','The national e-health centre counts 13 ransomware incidents in health care so far in 2026 against 10 in all of 2025. A leak at a medical software platform covered close to 19 million people; investigators said in February 2026 they had identified who was behind it.','CS')],
 'The only country that publishes a yearly count for health, and it is rising.','Het enige land dat een jaartelling voor de zorg publiceert, en ze stijgt.'),
'Portugal':([('May 2026','The judicial police confirmed that personal data of more than 100,000 users of the national health service was stolen. The attackers posed as a doctor; investigators say artificial intelligence may have been used. No suspect yet.','C')],
 'They did not break in: they logged in as a doctor.','Ze braken niet in: ze logden in als arts.'),
'Slovakia':([('Jan 2025','The national health insurer was targeted, in the same weeks as the attack that shut the land registry.','R')],'Reported, little detail.','Gemeld, weinig details.'),
'Spain':([('Oct 2026','The health service of Extremadura detected on 5 October that its online health-centre app had been breached: clinical information of 18,416 users. Police arrested the suspected attacker in Mérida on 29 October.','CS')],
 'A rare case with an arrest within a month.','Een zeldzaam geval met een arrestatie binnen de maand.'),
'Switzerland':([('Jun 2025','Ransomware at the health foundation Radix: data stolen and encrypted, including data of the federal administration, one of its clients.','C'),
 ('Nov 2026','Two medical centres in Chur confirmed that patient data, including prescriptions and X-rays, was taken; the Cloak group claims 87 GB.','CK')],
 'A small foundation held government data too.','Een kleine stichting bewaarde ook overheidsgegevens.'),
}
NONE=['Greece','Hungary','Latvia','Liechtenstein','Malta','Norway','Romania','Slovenia','Sweden']
assert len(D)+len(NONE)==30,(len(D),len(NONE))
def card(n):
    ev,se,sn=D[n]
    return '<div class="country" id="m-%s"><h4>%s <small>%d on record</small></h4><ul>%s</ul><p class="pl"><b>What it shows:</b> %s<span class="plnl"><b>NL – Wat het toont:</b> %s</span></p></div>'%(n,n,len(ev),''.join('<li><b>%s:</b> %s%s</li>'%(d,t,tg(s)) for d,t,s in ev),se,sn)
nev=sum(len(D[n][0]) for n in D)
SEC='''<section id="healtheu">
<h2>Health: the other 30 countries</h2>
<p class="sub">Hospitals, clinics, laboratories, health software and patient data in the other 26 EU countries plus Norway, Iceland, Switzerland and Liechtenstein, 2025 and 2026. @@N@@ entries in @@C@@ countries.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>Two kinds of damage. The first is care that stops: emergency rooms closed in Germany and Poland, operations postponed, staff back on paper. The second is data that leaks, and here the numbers are far larger and the cause is nearly always the same: not the hospital, but a company that works for hospitals. A French payment operator lost 15.4 million social security numbers; a French software maker's breach may concern more than 15 million people; a Dutch laboratory lost the data of about 941,000 people; a Polish software platform close to 19 million. Almost all of it is crime for money. No state has been blamed for an attack on a hospital in these countries in these two years.</p>
<p class="pb-nl"><b>NL:</b> Twee soorten schade. De eerste is zorg die stilvalt: spoedafdelingen gesloten in Duitsland en Polen, operaties uitgesteld, personeel terug op papier. De tweede is gegevens die lekken, en daar zijn de cijfers veel groter en is de oorzaak bijna altijd dezelfde: niet het ziekenhuis, maar een bedrijf dat voor ziekenhuizen werkt. Een Franse betalingsoperator verloor 15,4 miljoen rijksregisternummers; het lek bij een Franse softwaremaker kan meer dan 15 miljoen mensen treffen; een Nederlands laboratorium verloor de gegevens van ongeveer 941.000 mensen; een Pools softwareplatform bijna 19 miljoen. Bijna alles is misdaad voor geld. Voor geen enkele aanval op een ziekenhuis in deze landen is in deze twee jaar een staat aangewezen.</p></div>
<div class="warnbox"><b>Labels.</b> <span class="tag t-conf">Confirmed</span> stated by the organisation, an authority or a regulator. <span class="tag t-rep">Reported</span> in the press, not verified. <span class="tag t-claim">Claimed</span> said by one party, here mostly criminals on their own sites. <span class="tag t-susp">Suspected</span> a person arrested or identified, not yet judged. Two labels on one line: the first is for the event, the second for who was behind it.</div>
<h3>The largest data losses</h3>
<table><thead><tr><th>Who</th><th>What kind of organisation</th><th>People concerned</th><th>Status</th></tr></thead><tbody>
<tr><td><b>A Polish medical software platform</b></td><td>Software supplier</td><td>Close to 19 million</td><td><span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>Almerys</b>, France, May 2026</td><td>Payment operator for health insurance</td><td>15.4 million social security numbers</td><td><span class="tag t-conf">Confirmed</span></td></tr>
<tr><td><b>Cegedim Santé</b>, France</td><td>Health software maker</td><td>Possibly more than 15 million</td><td><span class="tag t-conf">Confirmed</span></td></tr>
<tr><td><b>Medtronic</b>, Ireland, Apr 2026</td><td>Medical-device maker</td><td>3.8 million worldwide</td><td><span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>Clinical Diagnostics</b>, Netherlands, Jul 2025</td><td>Laboratory</td><td>About 941,000 (first count: 405,000)</td><td><span class="tag t-conf">Confirmed</span></td></tr>
<tr><td><b>A French private hospital</b>, summer 2025</td><td>Hospital</td><td>524,867 patients and 202,246 contacts; fined €500,000</td><td><span class="tag t-conf">Confirmed</span></td></tr>
<tr><td><b>Charité</b>, Germany, Oct 2026</td><td>University hospital</td><td>About 140,000 (contact details)</td><td><span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>National health service</b>, Portugal, May 2026</td><td>Public health service</td><td>More than 100,000</td><td><span class="tag t-conf">Confirmed</span></td></tr>
</tbody></table>
<p class="small">Five of these eight are not hospitals but companies that work for them.</p>
<h3>Where care itself stopped</h3>
<table><thead><tr><th>Where and when</th><th>What stopped</th></tr></thead><tbody>
<tr><td><b>Ameos group</b>, Germany, Jul 2025</td><td>All systems shut down across a hospital group</td></tr>
<tr><td><b>Kraków and Warsaw</b>, Poland, Mar 2025</td><td>Files encrypted at two hospitals</td></tr>
<tr><td><b>Roth</b>, Germany, Jan 2026</td><td>Emergency room closed briefly; prescriptions by hand</td></tr>
<tr><td><b>Szczecin</b>, Poland, Mar 2026</td><td>A regional hospital on paper; national emergency support called in</td></tr>
<tr><td><b>A German hospital group</b>, May 2026</td><td>Operations postponed, emergency patients sent elsewhere</td></tr>
<tr><td><b>Chaumont</b>, France, Jul 2026</td><td>Critical systems unavailable, data lost</td></tr>
<tr><td><b>Greiz</b>, Germany, 15 Nov 2026</td><td>Emergency room could not take patients</td></tr>
</tbody></table>
<h3>Counts by others</h3>
<ul>
<li>Poland's national e-health centre: 13 ransomware incidents in health care so far in 2026, against 10 in all of 2025. <span class="tag t-conf">Confirmed</span></li>
<li>France's digital health agency: 15% of care institutions had an incident that disrupted their work between 2022 and 2025. <span class="tag t-rep">Reported</span></li>
<li>Italy, a sector body: attacks on hospitals up 20% in 2025; 47% were ransomware. <span class="tag t-claim">Claimed</span></li>
<li>The EU cyber agency: ransomware was 54% of health incidents in 2023 and 45% in 2024; in its 2026 review health is still among the sectors "in the risk zone". An EU support centre for hospitals is to start an early-warning service by 2026 at the latest; whether it has started was not confirmed. <span class="tag t-conf">Confirmed</span></li>
</ul>
<h3>Countries with something on record</h3>
<div class="countries">@@CARDS@@</div>
<h3>Nothing specific found</h3>
<p>@@NONE@@.</p>
<p class="small">Most entries on this page were already in the country cards of this file; new here are the French fine, Reims, Greiz, Roth, Portugal, the two Italian cases and the later Dutch count. Nothing found means nothing came up in searches up to 16 November 2026.</p>
<p class="pl"><b>What it shows:</b> A hospital can do everything right and still lose its patients' data, because the data also sits with the laboratory, the billing firm, the software maker and the payment operator. The law treats hospitals as vital; many of these suppliers are far smaller and far less checked. The two things that limited the damage were old-fashioned: being able to work on paper for weeks, and keeping the patient files apart from everything else, as Croatia's ministry did.<span class="plnl"><b>NL – Wat het toont:</b> Een ziekenhuis kan alles goed doen en toch de gegevens van zijn patiënten verliezen, omdat die gegevens ook bij het laboratorium, het facturatiebedrijf, de softwaremaker en de betalingsoperator zitten. De wet behandelt ziekenhuizen als vitaal; veel van deze leveranciers zijn veel kleiner en worden veel minder gecontroleerd. De twee dingen die de schade beperkten, waren ouderwets: wekenlang op papier kunnen werken, en de patiëntendossiers gescheiden houden van al de rest, zoals het Kroatische ministerie deed.</span></p>
<p class="src">Sources: see the linked list below.</p>
</section>'''.replace('@@N@@',str(nev)).replace('@@C@@',str(len(D))).replace('@@CARDS@@',''.join(card(n) for n in sorted(D))).replace('@@NONE@@',', '.join(NONE))
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='healtheu')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
w=R.find('section',id='health'); p=w.find('p',class_='sub'); p.string=p.get_text().replace('The other countries follow.','The other 30 countries have their own page.')
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'healtheu'" not in t:
    a="'src': ('R', 'health')}, "; assert a in t
    t=t.replace(a,a+"{'k': 'healtheu', 'en': 'Health: 30 countries', 'nl': 'Gezondheid: 30 landen', 'src': ('R', 'healtheu')}, ",1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['healtheu']" not in t:
    t+='''
INTRO['healtheu']=("Hospitals and health data in the other 30 countries: where care stopped, where data leaked, and why the supplier is usually the way in.","Ziekenhuizen en gezondheidsgegevens in de andere 30 landen: waar de zorg stilviel, waar gegevens lekten, en waarom de leverancier meestal de weg naar binnen is.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '#p-healtheu td' not in t:
    t=t.replace('</style>','@media(max-width:699px){#p-healtheu td,#p-healtheu th{overflow-wrap:anywhere;padding-left:3px;padding-right:3px;font-size:11.5px}#p-healtheu table{table-layout:fixed;width:100%}}\n</style>',1)
    open(a,'w',encoding='utf-8').write(t)
print('health2 ok',nev,len(D))
