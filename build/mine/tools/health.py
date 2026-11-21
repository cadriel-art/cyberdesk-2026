from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
import re as _re, collections as _col
def _sector_phrase(M):
    """Rank of health among sectors in the register (computed): returns e.g. 'the second most-hit sector in this file\'s register, after government (40 entries)'"""
    _h=open(M+'cyber-incident-register.html',encoding='utf-8').read()
    _c=_col.Counter(_re.findall(r'<tr[^>]*data-s="([a-z]+)"',_h[_h.index('id="reg2"'):]))
    _c.pop('other',None)   # "other" is a catch-all, not a sector
    _names={'gov':'government','health':'health','food':'food and retail','finance':'finance','energy':'energy','transport':'transport','water':'water','telecom':'telecom','education':'education'}
    _r=[k for k,_ in _c.most_common()]
    _pos=_r.index('health')+1
    if _pos==1: return 'the most-hit sector in this file\'s register (%d entries)'%_c['health']
    _ord={2:'second',3:'third'}.get(_pos,'%dth'%_pos)
    return 'the %s most-hit sector in this file\'s register, after %s (%d entries)'%(_ord,' and '.join(_names.get(k,k) for k in _r[:_pos-1]),_c['health'])
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join('<span class="tag %s">%s</span> '%(T[x][1],T[x][0]) for x in s)
EV=[
('Nov 2025','Websites','Health websites knocked offline','Two related campaigns by the pro-Russian group NoName057(16) hit telecom, health and intelligence websites.','R'),
('13 Jan 2026','Hospital','AZ Monica, Antwerp and Deurne','Ransomware. The hospital switched off every server as a precaution. Operations were cancelled, about 70 patients were sent home and seven in critical care were moved to other hospitals; it ran at about half capacity and worked on paper. The hospital says it paid no ransom and that, as far as it knows, no patient data was stolen. The federal computer crime unit and the national cyber team investigated; nobody has been named.','C'),
('13 Jan 2026','Hospital','Was a ransom demanded?','One report quotes the prosecutor saying no ransom was demanded; others describe it as ransomware with a demand. Not settled in the sources found.','R'),
('13–14 Jan 2026','Sector','The government\'s own measurement','A report by the hospitals\' shared security platform SHIELD and the federal health ministry, based on measurements in more than fifty hospitals: three in four must take urgent extra steps to reach the required level. Smaller and psychiatric hospitals lag most, for lack of money and specialists; Flemish hospitals score better on average than Walloon and Brussels ones. The government has put in €105 million since 2022, of which €40 million in 2024.','C'),
('14 Jan 2026','Supplier','71,000 patient records within reach','After AZ Monica a security firm found that a supplier of patient-registration software used by AZ Monica also served other hospitals, and that passwords for their platforms were circulating. Its testers could reach the data of about 71,000 patients; one report says the details of at least five hospitals were found on the dark web. The firm warned the national cyber centre and the hospitals; the holes were closed. It saw no sign that criminals had taken the patient files. The hospitals were not named.','CN','The exposure is confirmed by the firm that found it; theft by criminals is not shown.'),
('19 Feb 2026','Hospital','AZ Monica back','Medication, imaging, emergency systems and the website worked again after about five weeks; visitor wifi stayed off. The prosecutor\'s investigation was still open.','C'),
('26 Mar 2026','Clinic','Louise Medical Center, Brussels','The Qilin ransomware group listed the clinic and threatened to publish patient data. A Belgian blog says Qilin claimed two Belgian health targets within 24 hours; the second is not named. No confirmation by the clinic found.','K'),
('7–16 Apr 2026','Supplier','ChipSoft, the Dutch maker of hospital record software','Ransomware at ChipSoft on 7 April forced Dutch hospitals to close patient portals. Early reports said Belgian hospitals were affected too, and VRT reported on the Antwerp hospital group ZAS, a customer. On 16 April ChipSoft said no Belgian care institution was hit and that data was taken only at a few Dutch ones; on 29 April it said experts confirmed the stolen data was destroyed.','CN','The attack is confirmed; harm to Belgian hospitals is denied by the company.'),
('18 Apr 2026','Law','Deadline for hospitals','As "essential entities" under the cybersecurity law, hospitals had to show by this date that they meet the required level or have a plan; late or incomplete files can bring fines. How hospitals did is not published in the sources found.','C'),
('May 2026','Data','Two unverified offers on criminal forums','A seller claimed to have data from the medical-practice platform cabinetmedical.be; another offered a database said to belong to the health insurance fund Christelijke Mutualiteit. Neither was independently verified.','K'),
]
rows=''.join('<tr><td class="nowrap"><b>%s</b><br><span class="small">%s</span></td><td><b>%s.</b> %s%s</td><td>%s</td></tr>'%(r[0],r[1],r[2],r[3],(' <span class="small"><i>%s</i></span>'%r[5]) if len(r)>5 else '',tg(r[4])) for r in EV)
SEC='''<section id="health">
<h2>Health: Belgium</h2>
<p class="sub">Hospitals, clinics, health software and patient data in 2025 and 2026. Health is '''+_sector_phrase(M)+'''. The other countries follow.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>One Belgian hospital was knocked out for weeks: AZ Monica in Antwerp, in January 2026. Operations were cancelled, seven critical patients were moved, and staff worked on paper while the main systems took about five weeks to come back. The same week the government's own measurement said three in four hospitals are not at the level the law asks. And the look behind AZ Monica found something worse than the attack: a small software supplier through which the files of about 71,000 patients in other hospitals could be reached. Hospitals are attacked for money, not politics: nobody has blamed a state for any Belgian case.</p>
<p class="pb-nl"><b>NL:</b> Eén Belgisch ziekenhuis lag wekenlang plat: AZ Monica in Antwerpen, in januari 2026. Operaties werden geschrapt, zeven kritieke patiënten werden overgebracht, en het personeel werkte op papier terwijl het ongeveer vijf weken duurde voor de hoofdsystemen weer werkten. Dezelfde week zei de eigen meting van de overheid dat drie op de vier ziekenhuizen niet het niveau halen dat de wet vraagt. En wie achter AZ Monica keek, vond iets ergers dan de aanval: een kleine softwareleverancier via wie de dossiers van ongeveer 71.000 patiënten in andere ziekenhuizen bereikbaar waren. Ziekenhuizen worden aangevallen voor geld, niet voor politiek: voor geen enkel Belgisch geval is een staat aangewezen.</p></div>
<div class="warnbox"><b>Labels.</b> <span class="tag t-conf">Confirmed</span> stated by the hospital, an authority or named researchers. <span class="tag t-rep">Reported</span> in the press, not verified. <span class="tag t-claim">Claimed</span> said by one party, here mostly criminals on their own sites. <span class="tag t-none">Not proven</span> looked into and not found, or denied by the organisation. Two labels on one line: the first is for the event, the second for the harm in Belgium.</div>
<h3>Figures</h3>
<table><thead><tr><th>Figure</th><th>What it is</th><th>Source</th></tr></thead><tbody>
<tr><td><b>3 in 4</b></td><td>Hospitals that must take urgent extra steps to reach the required level (measured in more than fifty hospitals).</td><td>SHIELD and the federal health ministry, January 2026</td></tr>
<tr><td><b>€105 million</b></td><td>Federal money for hospital cybersecurity since 2022 (€40 million of it in 2024).</td><td>Federal government</td></tr>
<tr><td><b>About 5 weeks</b></td><td>Time until AZ Monica's main systems worked again (13 January to 19 February 2026).</td><td>The hospital, via press</td></tr>
<tr><td><b>7 / about 70</b></td><td>Critical patients moved to other hospitals / patients sent home at AZ Monica.</td><td>The hospital, via press</td></tr>
<tr><td><b>71,000</b></td><td>Patients whose data could be reached through one supplier of registration software, in at least three to five hospitals.</td><td>Security firm Secutec, via VRT</td></tr>
<tr><td><b>Up to 3,000 a day</b></td><td>Attacks against care institutions, according to one expert quoted by VRT. An expert's estimate, not a measured figure.</td><td>VRT, 13 January 2026</td></tr>
<tr><td><b>18 April 2026</b></td><td>Legal deadline for hospitals to show they meet the cybersecurity level.</td><td>Centre for Cybersecurity Belgium</td></tr>
</tbody></table>
<h3>What happened, in order</h3>
<table><thead><tr><th>Date</th><th>Event</th><th>Status</th></tr></thead><tbody>'''+rows+'''</tbody></table>
<h3>Before 2025, for comparison</h3>
<ul>
<li><b>May 2022:</b> Vivalia, a group of hospitals in the province of Luxembourg; the LockBit group threatened to publish 400 GB of patient and staff data.</li>
<li><b>March 2023:</b> CHU Saint-Pierre in Brussels: servers disconnected, ambulances diverted, paper procedures.</li>
<li><b>March 2024:</b> the pharmacy and health-retail group Goed: data stolen, card payments and digital prescriptions disrupted.</li>
</ul>
<h3>Proven and not proven</h3>
<table><thead><tr><th>Proven</th><th>Not proven</th></tr></thead><tbody>
<tr><td>AZ Monica was shut down by ransomware and needed about five weeks to recover.</td><td>Who did it, and whether a ransom was demanded.</td></tr>
<tr><td>Through one supplier the data of about 71,000 patients could be reached.</td><td>That criminals actually took those patient files.</td></tr>
<tr><td>Three in four hospitals were below the required level in January 2026.</td><td>How many reached it by the legal deadline of 18 April.</td></tr>
<tr><td>ChipSoft was hit and Dutch hospitals closed their portals.</td><td>Any harm in Belgium: the company says there was none.</td></tr>
</tbody></table>
<p class="pl"><b>What it shows:</b> The weak point is rarely the big hospital system; it is the small supplier plugged into it, and the small hospital that cannot afford its own specialists. AZ Monica did two things right that cost nothing: it pulled the plug at once, and it could work on paper. The measure that would help most is a shared security service for the hospitals that cannot pay for their own.<span class="plnl"><b>NL – Wat het toont:</b> Het zwakke punt is zelden het grote ziekenhuissysteem; het is de kleine leverancier die erop is aangesloten, en het kleine ziekenhuis dat geen eigen specialisten kan betalen. AZ Monica deed twee dingen goed die niets kosten: het trok meteen de stekker uit, en het kon op papier werken. De maatregel die het meest zou helpen, is een gedeelde beveiligingsdienst voor de ziekenhuizen die er zelf geen kunnen betalen.</span></p>
<p class="small"><b>Corrected on 16 November 2026:</b> earlier versions of this file said Belgian hospital portals were disconnected in the ChipSoft attack and named a ransomware group. ChipSoft's statement of 16 April 2026 says no Belgian care institution was hit, and the group name could not be confirmed. The register and the country card now say so.</p>
<h3>Still open</h3>
<ul>
<li>The outcome of the Antwerp prosecutor's investigation into AZ Monica, and what the recovery cost.</li>
<li>Which hospitals shared the leaking supplier, and whether patients were told.</li>
<li>How hospitals did against the 18 April 2026 deadline.</li>
<li>Whether the Brussels clinic and the health insurance fund confirm the criminals' claims.</li>
<li>Care homes, pharmacies, laboratories and general practices: nothing found for 2025–2026.</li>
</ul>
<p class="src">Sources: see the linked list below.</p>
</section>'''
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='health')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'health'" not in t:
    a="{'k': 'failures', 'en': 'Avoidable failures'"; assert a in t
    t=t.replace(a,"{'k': 'health', 'en': 'Health: Belgium', 'nl': 'Gezondheid: België', 'src': ('R', 'health')}, "+a,1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['health']" not in t:
    t+='''
INTRO['health']=("Hospitals, clinics and patient data in Belgium: the one hospital knocked out for weeks, the supplier that left 71,000 files within reach, and how ready the sector is.","Ziekenhuizen, klinieken en patiëntgegevens in België: het ene ziekenhuis dat wekenlang platlag, de leverancier die 71.000 dossiers bereikbaar liet, en hoe klaar de sector is.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '#p-health td' not in t:
    t=t.replace('</style>','@media(max-width:699px){#p-health td,#p-health th{overflow-wrap:anywhere;padding-left:3px;padding-right:3px;font-size:12px}#p-health .tag{font-size:9px;letter-spacing:0;padding:1px 4px}#p-health table{table-layout:fixed;width:100%}}\n</style>',1)
    open(a,'w',encoding='utf-8').write(t)
print('health ok')
