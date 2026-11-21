# Housekeeping: subject index page (#more) and a Subject filter in the register.
import re
from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
import re as _re
_h=open(M+'cyber-incident-register.html',encoding='utf-8').read()
import re as _re2
def _edu_years(_h):
    """years (as strings) of the register rows whose sector is education, order of attributes does not matter"""
    _o=[]
    for _t in _re2.findall(r'<tr\b[^>]*>',_h[_h.index('id="reg2"'):]):
        if 'data-s="education"' in _t:
            _m=_re2.search(r'data-y="(\d{4})"',_t)
            if _m: _o.append(_m.group(1))
    return _o
import collections as _col
_c=_col.Counter(_re.findall(r'<tr[^>]*data-s="([a-z]+)"',_h[_h.index('id="reg2"'):])); _c.pop('other',None)
_rk=[k for k,_ in _c.most_common()].index('health')+1
assert _rk==1 or _c.most_common(1)[0][0]=='gov' and _rk==2, 'health rank changed: update wording'
HEALTH_RANK='The most-hit sector in the register.' if _rk==1 else 'After government, the sector with most entries in the register (%d).'%_c['health']
EDU26=_edu_years(_h).count('2026')

# ---------- 1. Subject filter in the register ----------
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
reg=R.find('section',id='reg2')
SUBN=[('energy','Energy and the grid'),('water','Water'),('health','Health'),('transport','Transport and ports'),
      ('elections','Elections and democracy'),('none','Not on a subject page')]
ELEC=re.compile(r'election|parliament|political part|politician|campaign|ballot|voter',re.I)
cnt={k:0 for k,_ in SUBN}
for tr in reg.select('tbody tr'):
    s=tr.get('data-s',''); txt=tr.get_text(' ',strip=True)
    sub = s if s in ('energy','water','health','transport') else ('elections' if ELEC.search(txt) else 'none')
    tr['data-sub']=sub; cnt[sub]+=1
sel=reg.find('div',id='reg2f').find('select',attrs={'data-k':'sub'})
if sel: sel.decompose()
opts=''.join('<option value="%s">%s (%d)</option>'%(k,n,cnt[k]) for k,n in SUBN)
reg.find('div',id='reg2f').append(BeautifulSoup('<select data-k="sub" aria-label="Subject"><option value="">All subjects</option>%s</select>'%opts,'html.parser'))
old=reg.find('p',class_='subnote')
if old: old.decompose()
note=('<p class="small subnote"><b>Subject</b> links each incident to the page that works that subject out: '
 '<a href="#energy">energy</a>, <a href="#water">water</a> (and <a href="#watereu">30 countries</a>), '
 '<a href="#transport">transport and ports</a> (and <a href="#transporteu">30 countries</a>), '
 '<a href="#health">health</a> (and <a href="#healtheu">30 countries</a>), '
 '<a href="#elections">elections and democracy</a> (and <a href="#electionseu">30 countries</a>). '
 'The subject is worked out from the sector and the description, so a few entries may sit in the wrong one. '
 'Drones, sabotage and cut sea cables are <b>not</b> in this register, because they are not cyberattacks; they are counted apart on '
 '<a href="#hybrid">the page for Belgium</a> and <a href="#hybrideu">for the other 30 countries</a>.'
 '<span class="plnl"><b>NL:</b> <b>Onderwerp</b> koppelt elk incident aan de pagina die dat onderwerp uitwerkt. Het onderwerp wordt afgeleid uit de sector en de beschrijving, dus enkele items kunnen verkeerd zitten. Drones, sabotage en doorgesneden zeekabels staan <b>niet</b> in dit register, want het zijn geen cyberaanvallen; ze worden apart geteld.</span></p>')
reg.find('div',id='reg2f').insert_after(BeautifulSoup(note,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
print('subject filter:',cnt)

# ---------- 2. "More subjects to explore" becomes an index ----------
BUILT=[
 ('Energy and the grid','energy',None,'Every energy source, one by one: nuclear, gas and LNG, oil and the port, offshore wind and sea cables, dams, district heating, charging points.'),
 ('Water','water','watereu','Drinking water and waste water. Three countries where attackers reached the machinery itself.'),
 ('Transport and ports','transport','transporteu','Airports, sea ports, rail, post and logistics. Mostly hit through a shared supplier.'),
 ('Health','health','healtheu','Hospitals, clinics, laboratories and patient data. '+HEALTH_RANK),
 ('Elections and democracy','elections','electionseu','Fakes, hijacked accounts, spyware, bribery, spying and pressure on politicians.'),
 ('Drones, sabotage and hybrid threats','hybrid','hybrideu','Events that are not hacks: drones, arson, cut sea cables, false bomb threats, jammed satellite signals.'),
 ('The defence side','defence','defenceeu','Military cyber forces, reserves, money, and what armies may do inside their own country.'),
 ('Who did it: the evidence tracker','evidence',None,'Every big case with the same five questions, and a level of proof from a court verdict down to nobody named.'),
 ('Global outages','outages',None,'The biggest outages of online services since 2025, what caused each one, and who is blamed when it was an attack.'),
 ('Ready at home: stock-up advice','prepare',None,'What governments tell people to keep in stock at home for at least 72 hours, which countries sent a guide to every household, and what changed in 2025–2026.'),
 ('Encryption and "chat control"','encryption','encryptioneu','Whether the police may read private messages, and what the Sky ECC case says about it.'),
 ('Skills and jobs','skills',None,'How many cybersecurity people Belgium and Europe have, and how many they are short.'),
 ('Insurance','insurance',None,'Who is covered, what insurers demand first, and the exclusion that may leave most of these attacks uninsured.'),
 ('Sea cables and satellite signals','cables',None,'The cables under the sea and the signal that tells ships and aircraft where they are.'),
 ('Children and schools','schools',None,'Attacks on schools, and the separate European laws on children and social media.'),
]
TODO=[('Encryption and "chat control"','What the stalled EU child-protection regulation would require of messaging apps, the security argument against weakening encryption, and where each country stands.'),
 ('Skills and jobs','The size of the shortage per country and per sector, what retraining exists, and how military cyber reserves are recruited.'),
 ('Insurance','How many organisations are covered, what insurers require before they pay, and whether reimbursing a ransom should be banned.'),
 ('Sea cables and satellite signals','The facts are spread over the drones and transport pages; they would fit together on one page.'),
 ('Children and schools','Schools, school platforms and pupils’ data. Education is %d incidents in the register for 2026.'%EDU26)]
OPEN=[('Who did it','For most incidents nobody is named, and for the big hacks the proof stops at a government statement whose evidence stays secret.'),
 ('Belgium, the freezer attacks','One minister points at Iran, the foreign minister and the federal prosecutor do not confirm. No Belgian attribution exists.'),
 ('Belgium, the drones of 2025','The federal prosecutor’s investigations into the sightings have produced nothing public, and the air security centre’s status is unclear.'),
 ('Belgium, hospitals','How many reached the legal cybersecurity level by the deadline of 18 April 2026 is not published.'),
 ('Belgium, water','Whether any Belgian water company has looked for control devices reachable from the internet, and what it found.'),
 ('Belgium, defence','The size of the Cyber Force, and whether its rapid teams have ever been sent to help a hospital or a town hall.'),
 ('Europe','Who sent the hoax bomb threats of November 2026, and what caused the loss of satellite positioning over the North Sea on 9 November 2026.')]
def row(n,a,b,d):
    links='<a href="#%s">Belgium</a>'%a + (' · <a href="#%s">the other 30 countries</a>'%b if b else '')
    if a in ('energy','evidence','outages','prepare'): links='<a href="#%s">open the page</a>'%a
    return '<tr><td><b>%s</b><br><span class="small">%s</span></td><td class="nowrap">%s</td></tr>'%(n,d,links)
SEC='''<section id="more">
<h2>Subjects in this file, and what is still open</h2>
<p class="sub">An index of the subjects worked out in this file, the subjects still to come, and the questions that public sources do not answer.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>This file started as a register of cyberattacks. It now also covers things that are not hacks at all: drones, arson, cut cables, fake videos. Each subject is done twice, first for Belgium and then for the other 30 countries, and each line carries a label saying how firm the fact is. This page is the way in, and the honest list of what is still missing.</p>
<p class="pb-nl"><b>NL:</b> Dit dossier begon als een register van cyberaanvallen. Het behandelt nu ook zaken die helemaal geen hacks zijn: drones, brandstichting, doorgesneden kabels, nepvideo’s. Elk onderwerp is twee keer gedaan, eerst voor België en dan voor de andere 30 landen, en elke regel draagt een label dat zegt hoe hard het feit is. Deze pagina is de ingang, en de eerlijke lijst van wat nog ontbreekt.</p></div>
<h3>Worked out in this file</h3>
<table><thead><tr><th>Subject</th><th>Pages</th></tr></thead><tbody>@@ROWS@@</tbody></table>
<h3>What is next</h3>
<table><thead><tr><th>Subject</th><th>What it would cover</th></tr></thead><tbody>@@TODO@@</tbody></table>
<h3>What is still open</h3>
<p class="small">The questions below are the ones that public sources did not answer by @@TODAY@@. Each is repeated under "Still open" on the page it belongs to.</p>
<table><thead><tr><th>Where</th><th>The question</th></tr></thead><tbody>@@OPEN@@</tbody></table>
<p class="pl"><b>What it shows:</b> The gaps are not random. They sit almost always at the same place: between an event everyone can see, and the name of whoever caused it. That is why this file keeps the two apart on every page.<span class="plnl"><b>NL – Wat het toont:</b> De gaten zijn niet toevallig. Ze zitten bijna altijd op dezelfde plek: tussen een gebeurtenis die iedereen kan zien, en de naam van wie ze veroorzaakte. Daarom houdt dit dossier die twee op elke pagina uit elkaar.</span></p>
</section>'''.replace('@@TODAY@@',__import__('datetime').date.today().strftime('%-d %B %Y')).replace('@@ROWS@@',''.join(row(*x) for x in BUILT)).replace('@@TODO@@',''.join('<tr><td><b>%s</b></td><td>%s</td></tr>'%x for x in TODO)).replace('@@OPEN@@',''.join('<tr><td class="nowrap"><b>%s</b></td><td>%s</td></tr>'%x for x in OPEN))
f=M+'vrt-cyber-briefing.html'; P=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
P.find('section',id='more').replace_with(BeautifulSoup(SEC,'html.parser'))
open(f,'w',encoding='utf-8').write(str(P))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
t=t.replace("'en': 'More subjects to explore', 'nl': 'Meer onderwerpen om te verkennen'","'en': 'Subjects and what is still open', 'nl': 'Onderwerpen en wat nog openstaat'")
open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['more']=(\"An index" not in t:
    t+='''
INTRO['more']=("An index of every subject in this file, the subjects still to come, and the questions public sources do not answer.","Een index van elk onderwerp in dit dossier, de onderwerpen die nog komen, en de vragen die publieke bronnen niet beantwoorden.")
'''
    open(l,'w',encoding='utf-8').write(t)
print('index page ok')
