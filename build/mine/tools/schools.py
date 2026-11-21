from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
import re as _re2
def _edu_years(_h):
    """years (as strings) of the register rows whose sector is education, order of attributes does not matter"""
    _o=[]
    for _t in _re2.findall(r'<tr\b[^>]*>',_h[_h.index('id="reg2"'):]):
        if 'data-s="education"' in _t:
            _m=_re2.search(r'data-y="(\d{4})"',_t)
            if _m: _o.append(_m.group(1))
    return _o
def _edu():
    _h=open(M+'cyber-incident-register.html',encoding='utf-8').read()
    _r=_edu_years(_h)
    return _r.count('2025'),_r.count('2026')
EDU25,EDU26=_edu()
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join('<span class="tag %s">%s</span> '%(T[x][1],T[x][0]) for x in s)
EV=[
('Jan 2026','Belgium','A school, and then its parents','Ransomware at the secondary school OLV Pulhof in Berchem, Antwerp, shortly after the Christmas holiday. The attackers said they had been inside the systems unnoticed for more than a year and claimed 45 GB of data, including identity cards, diplomas and mental-health records. They asked for about €100,000, then about €15,000. The school refused. The attackers then emailed the parents directly, asking €50 per child. Experts said that email probably did not come from the group it claimed to be. Belgian prosecutors are investigating.','CK','The attack and the approach to parents are confirmed; the amounts and the 45 GB are the attackers’ own claims.'),
('May 2026','Belgium','Six colleges and universities at once','A breach of the learning platform Canvas reached VUB, Thomas More, Artevelde, Karel de Grote, Erasmushogeschool and CVO Gent: names, email addresses and student numbers of thousands of people. Icelandic universities were named in the same breach.','R'),
('May 2026','Austria','Schools in Styria','A ransomware group claimed 21 GB of data from schools in Styria. The education authority refused to negotiate and the outage was repaired quickly.','K'),
('Aug 2026','France','The education ministry','A criminal claimed about 43 GB covering millions of pupils and staff. Not verified, and no ministry confirmation was found.','K'),
('2026','Italy','A university offline for days','La Sapienza in Rome was forced offline; the Interlock group claimed it and published the data after no ransom was paid.','R'),
('First half of 2026','Europe','What the trackers count','A commercial tracker counted 104 attacks on education in six months: 36 confirmed and 68 claimed but unconfirmed. The median ransom asked was about $420,000.','R'),
('2025–2026','Europe','In this file’s own register','Education incidents in this file\'s own register rose from 2025 to 2026 (the register table counts them). This file cannot tell how much of that is a real rise and how much is better reporting; see <a href="#reg2">the register</a>.','C'),
('17 Sep 2026','EU','A law aimed at children, not at schools','The Commission proposed the EU KIDS Act: no social media under 13, safety built into platforms and games by design, age checks certified by the EU using technology that proves an age without revealing who you are, and fines up to 6% of worldwide turnover. Comments were open until 3 December 2026.','C'),
('21 Jul – 14 Aug 2026','France','A national ban struck down','France passed a law barring under-15s from social media on 21 July 2026. The Constitutional Council blocked it on 14 August 2026.','C'),
('29 Oct 2026','Austria / EU','Brussels pauses a national law','The Commission put Austria’s draft ban for under-14s on hold, as it has done with other national rules, while its own proposal is on the table.','R'),
('2026','EU','Denmark pushes from the chair','Holding the EU presidency, Denmark wants a hard ban under 13 and parental consent from 13 to 15. One source gives its own national plan as under 15.','R'),
('Jun 2026','EU','Age checks taken out of the other law','In the "chat control" talks the negotiators agreed that that regulation is not the place to regulate age verification, which is why it now sits in the KIDS Act instead. See <a href="#encryption">encryption</a>.','R'),
('Dec 2025','Outside Europe','The example everyone quotes','Australia became the first country to ban social media for under-16s.','C'),
]
rows=''.join('<tr><td class="nowrap"><b>%s</b><br><span class="small">%s</span></td><td><b>%s.</b> %s%s</td><td>%s</td></tr>'%(r[0],r[1],r[2],r[3],(' <span class="small"><i>%s</i></span>'%r[5]) if len(r)>5 else '',tg(r[4])) for r in EV)
SEC='''<section id="schools">
<h2>Children and schools</h2>
<p class="sub">Two things that are usually discussed apart: attacks on schools, which are ordinary crime against badly defended organisations, and the laws being written to protect children online. One page for all 31 countries.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>Schools hold more sensitive information about more vulnerable people than almost any organisation of their size, and they are defended like a small business, because that is what they are. When a Belgian school refused to pay in January 2026, the attackers emailed the parents and asked for €50 per child. That is the whole problem in one sentence. Separately, Europe is writing rules to keep young children off social media, which is a different subject with the same word in it: those rules will not stop a single one of the attacks on this page.</p>
<p class="pb-nl"><b>NL:</b> Scholen bewaren meer gevoelige informatie over meer kwetsbare mensen dan bijna elke organisatie van hun grootte, en ze zijn verdedigd als een klein bedrijf, want dat zijn ze. Toen een Belgische school in januari 2026 weigerde te betalen, mailden de aanvallers de ouders en vroegen 50 euro per kind. Dat is het hele probleem in één zin. Daarnaast schrijft Europa regels om jonge kinderen van sociale media te houden, een ander onderwerp met hetzelfde woord erin: die regels houden geen enkele aanval op deze pagina tegen.</p></div>
<div class="warnbox"><b>Labels.</b> <span class="tag t-conf">Confirmed</span> stated by the school, an authority or an EU institution. <span class="tag t-rep">Reported</span> in the press, not verified. <span class="tag t-claim">Claimed</span> said by the attackers on their own site, which is where most numbers about stolen data come from. Treat every quantity of stolen data as a criminal’s sales pitch until someone else confirms it.
<span class="plnl"><b>NL – Labels.</b> Behandel elke hoeveelheid gestolen gegevens als de verkooppraat van een crimineel, tot iemand anders het bevestigt.</span></div>
<h3>What happened, in order</h3>
<table><thead><tr><th>Date</th><th>Event</th><th>Status</th></tr></thead><tbody>'''+rows+'''</tbody></table>
<h3>Why schools are hit so easily</h3>
<table><thead><tr><th>What a school has</th><th>What it does not have</th></tr></thead><tbody>
<tr><td>Identity documents, addresses and dates of birth of hundreds of minors</td><td>Anyone whose job is security</td></tr>
<tr><td>Health and welfare records, sometimes including mental-health notes</td><td>A budget that can compete for the people in <a href="#skills">skills and jobs</a></td></tr>
<tr><td>Diplomas and results, which are worth forging</td><td>Round-the-clock monitoring: the Belgian attackers sat inside for over a year</td></tr>
<tr><td>Parents who can be contacted directly and will panic</td><td>A legal duty: schools are not "essential entities" under the cybersecurity law, unlike hospitals</td></tr>
<tr><td>Holidays, when nobody is watching: the Belgian attack came just after Christmas</td><td>Any obligation to tell anyone, beyond data-protection rules</td></tr>
</tbody></table>
<h3>The two debates, kept apart</h3>
<table><thead><tr><th></th><th>Attacks on schools</th><th>Children on social media</th></tr></thead><tbody>
<tr><td><b>Who is the threat</b></td><td>Criminals after money</td><td>Platforms, strangers, and the children’s own exposure</td></tr>
<tr><td><b>Who is responsible</b></td><td>The school, with no money and no staff</td><td>The platform, and now the EU</td></tr>
<tr><td><b>What is being done</b></td><td>Almost nothing specific. No European programme for school security was found.</td><td>A draft EU law, three national laws, one of them struck down</td></tr>
<tr><td><b>Political attention</b></td><td>Low</td><td>High</td></tr>
</tbody></table>
<p class="small">Both matter. The point of putting them side by side is that the attention and the money are going almost entirely to the second.</p>
<h3>Proven and not proven</h3>
<table><thead><tr><th>Proven</th><th>Not proven</th></tr></thead><tbody>
<tr><td>A Belgian school was attacked and its parents were then asked for €50 per child.</td><td>Who did it, and whether the email to parents came from the same people.</td></tr>
<tr><td>Six Belgian colleges lost student data through one shared learning platform.</td><td>How many students in total.</td></tr>
<tr><td>Education incidents in this file went from {E25} to {E26} between 2025 and 2026.</td><td>How much of that is a real rise rather than better reporting.</td></tr>
<tr><td>The EU has proposed a children’s online safety law with age checks.</td><td>Whether it will pass, and whether age checks can be done without identifying everyone.</td></tr>
<tr><td>France passed an under-15 ban and its own court struck it down.</td><td>What the other countries’ courts would say.</td></tr>
</tbody></table>
<p class="pl"><b>What it shows:</b> A school is a small organisation holding the most sensitive records in a town, with no security staff and no legal duty to have any. Hospitals got money and a deadline after being named essential; schools were not named. The cheapest thing that would help is the same answer as everywhere else in this file: a shared security service that a hundred schools pay for once. The second cheapest is a rule that nobody may be asked to pay twice, so that a parent who gets an email demanding €50 knows immediately that it is a crime and where to report it.<span class="plnl"><b>NL – Wat het toont:</b> Een school is een kleine organisatie die de gevoeligste dossiers van een gemeente bewaart, zonder beveiligingspersoneel en zonder wettelijke plicht om dat te hebben. Ziekenhuizen kregen geld en een deadline nadat ze essentieel werden genoemd; scholen werden niet genoemd. Het goedkoopste wat zou helpen, is hetzelfde antwoord als overal in dit dossier: een gedeelde beveiligingsdienst die honderd scholen één keer betalen. Het op één na goedkoopste is een regel dat niemand twee keer mag worden aangesproken, zodat een ouder die een mail krijgt met een vraag van 50 euro meteen weet dat het misdaad is en waar hij het moet melden.</span></p>
<h3>Still open</h3>
<ul>
<li>Who attacked the Belgian school, and the outcome of the prosecutors’ investigation.</li>
<li>How many students were affected by the Canvas breach at the six Belgian institutions.</li>
<li>Whether any European country gives schools money or shared services for security: nothing found.</li>
<li>Whether the EU children’s law passes, and in what form.</li>
<li>Whether any parent actually paid the €50.</li>
<li>Figures on sextortion and online threats against children in Belgium: not found in these searches.</li>
</ul>
<p class="src">Sources: see the linked list below.</p>
</section>'''.replace('{E25}',str(EDU25)).replace('{E26}',str(EDU26))
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='schools')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'schools'" not in t:
    a="{'k': 'cables', "; assert a in t
    t=t.replace(a,"{'k': 'schools', 'en': 'Children and schools', 'nl': 'Kinderen en scholen', 'src': ('R', 'schools')}, "+a,1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['schools']" not in t:
    t+='''
INTRO['schools']=("Attacks on schools, which hold the most sensitive records in a town with no security staff, and the separate European laws being written to keep children off social media.","Aanvallen op scholen, die de gevoeligste dossiers van een gemeente bewaren zonder beveiligingspersoneel, en de aparte Europese wetten om kinderen van sociale media te houden.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '#p-schools td' not in t:
    t=t.replace('</style>','@media(max-width:699px){#p-schools td,#p-schools th{overflow-wrap:anywhere;padding-left:3px;padding-right:3px;font-size:12px}#p-schools .tag{font-size:9px;letter-spacing:0;padding:1px 4px}#p-schools table{table-layout:fixed;width:100%}}\n</style>',1)
    open(a,'w',encoding='utf-8').write(t)
print('schools ok')
