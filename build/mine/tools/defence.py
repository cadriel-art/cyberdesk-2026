from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join('<span class="tag %s">%s</span> '%(T[x][1],T[x][0]) for x in s)
EV=[
('Oct 2022','Structure','Background: a cyber branch of the army','Belgium set up a Cyber Command inside Defence, now called the Belgian Cyber Force. It sits close to military intelligence and deals with threats from abroad; the civilian Centre for Cybersecurity Belgium (CCB) leads national policy.','C'),
('Mid-2025','Money','The Strategic Vision','The government agreed a defence plan of about €34 billion in investments up to 2034. It includes cyber, electronic warfare, drones and counter-drones, and air defence. A trade report puts half a billion euros on cybersecurity projects up to 2034 and €965 million on military data centres, inside a €1.6 billion package for digital resilience.','CR','The plan is confirmed; the cyber sub-totals come from one trade report.'),
('Summer 2025','People','New commander','Major General Pierre Ciparisse has led the Cyber Force since the summer of 2025. He calls staff the first priority and gives no headcount.','C'),
('7 Nov 2025','Incident','Military intelligence websites knocked offline','The pro-Russian group NoName057(16) claimed an attack on several websites of the military intelligence service. Defence said the sites were briefly unreachable, nothing was broken into and no data leaked.','CK','The outage is confirmed; who did it is the group\'s own claim.'),
('17 Nov 2025 – 20 Feb 2026','People','A competition to find reservists','The Cyber Force ran a public challenge to attract cyber reservists.','C'),
('Nov–Dec 2025','Drones','Emergency purchases','About €50 million of anti-drone equipment and a strengthened air security centre, after the drone reports. See the page on drones and sabotage.','C'),
('Jan 2026','Partners','A telecom firm as strategic partner','Defence chose Proximus NXT as its strategic partner for cyber defence.','C'),
('Feb 2026','People','Who works there','32% of the Cyber Force\'s staff were civilians in February 2026. In an interview the commander gave a mix of 47% military, 25% reservists and the rest civilians; the two figures come from different moments.','R'),
('Mar 2026','People','A call to experts','The defence minister publicly asked cyber specialists to join the Cyber Force as reserve officers.','C'),
('2026','Tasks','What the army may do at home','The operations plan for 2026, approved by the government, says the Cyber Force supports the competent authorities with monitoring and threat analysis, and that Defence\'s Cyber Rapid Response Teams stand ready for serious national cyber incidents.','C'),
('Late Apr 2026','Money','The NATO count','Belgium reported 3.44% of its economy spent on defence and security: 2.01% on the military and, counted for the first time, 1.43% on "strategic resilience" (cybersecurity, counter-terrorism, vital infrastructure). For 2026 the defence budget is €10.6 billion.','C'),
('May 2025 – spring 2026','Incident','The civilian intelligence service, not the army','Attackers used flaws in phone-management software (Ivanti) at an outside partner to reach personal data of staff of State Security; disclosed in June 2026. Classified data stayed safe; nobody has been named.','C'),
('29 May 2026','Spying','An arrest led by military intelligence','A man suspected of passing state secrets to people linked to Russia. See the page on drones and sabotage.','CS'),
('Jun 2026','People','Training bought in','The government approved a contract for advanced digital training and certificates for the cyber branch.','C'),
('8 Jul 2026','Money','The next years','Belgium will keep military spending at 2% of the economy until 2029; a path towards NATO\'s 3.5% goal still has to be drawn up.','C'),
]
rows=''.join('<tr><td class="nowrap"><b>%s</b><br><span class="small">%s</span></td><td><b>%s.</b> %s%s</td><td>%s</td></tr>'%(r[0],r[1],r[2],r[3],(' <span class="small"><i>%s</i></span>'%r[5]) if len(r)>5 else '',tg(r[4])) for r in EV)
SEC='''<section id="defence">
<h2>The defence side: Belgium</h2>
<p class="sub">What the army does about cyber and hybrid threats in 2025 and 2026: its cyber branch, its people and money, what it may do at home, and the attacks on Defence itself. The other countries follow.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>Belgium has a cyber branch of the army, the Cyber Force, and a civilian cyber centre, the CCB. The army looks outward and the CCB looks after the country; the 2026 plan lets the army help at home with watching and analysing threats, and keeps rapid teams ready for a serious national incident. The money has grown fast on paper: since April 2026 Belgium counts 1.43% of its economy as "resilience" spending for NATO, cybersecurity included. The people are the hard part: the Cyber Force leans on reservists and civilians and is publicly asking specialists to sign up. No break-in at Defence itself is on record for these two years; its intelligence websites were knocked offline once.</p>
<p class="pb-nl"><b>NL:</b> België heeft een cybertak van het leger, de Cyber Force, en een burgerlijk cybercentrum, het CCB. Het leger kijkt naar buiten en het CCB zorgt voor het land; het plan voor 2026 laat het leger in eigen land helpen met het bewaken en analyseren van dreigingen, en houdt snelle teams klaar voor een ernstig nationaal incident. Het geld is op papier snel gegroeid: sinds april 2026 telt België 1,43% van zijn economie als "weerbaarheidsuitgaven" voor de NAVO, cyberveiligheid inbegrepen. De mensen zijn het moeilijke deel: de Cyber Force steunt op reservisten en burgers en vraagt specialisten publiek om zich aan te melden. Voor deze twee jaar is geen inbraak bij Defensie zelf bekend; de websites van zijn inlichtingendienst lagen één keer plat.</p></div>
<div class="warnbox"><b>Labels.</b> <span class="tag t-conf">Confirmed</span> stated by the government, Defence or a court. <span class="tag t-rep">Reported</span> in the press, not verified. <span class="tag t-claim">Claimed</span> said by one party without public evidence. <span class="tag t-susp">Suspected</span> arrested or believed, not judged. Two labels on one line: the first is for the event, the second for a detail or for who was behind it.</div>
<h3>Figures</h3>
<table><thead><tr><th>Figure</th><th>What it is</th><th>Source</th></tr></thead><tbody>
<tr><td><b>3.44%</b></td><td>Share of the economy Belgium reports to NATO for defence and security (April 2026): 2.01% military, 1.43% resilience.</td><td>Federal government, via Belga</td></tr>
<tr><td><b>€10.6 billion</b></td><td>Defence budget for 2026; 41% goes to European contracts, 7% to American ones.</td><td>Press</td></tr>
<tr><td><b>€34 billion</b></td><td>Investments in the defence plan up to 2034.</td><td>Federal government</td></tr>
<tr><td><b>€0.5 billion</b></td><td>Cybersecurity projects up to 2034, plus €965 million for military data centres.</td><td>One trade report</td></tr>
<tr><td><b>32%</b></td><td>Civilians in the Cyber Force, February 2026. About a quarter are reservists, by the commander's account.</td><td>Reported</td></tr>
<tr><td><b>Not public</b></td><td>How many people the Cyber Force has.</td><td>The commander declined to say</td></tr>
<tr><td><b>1</b></td><td>Attack on Defence systems on record in the two years: websites of military intelligence offline for a short time, November 2025.</td><td>Defence, via VRT</td></tr>
</tbody></table>
<h3>What happened, in order</h3>
<table><thead><tr><th>Date</th><th>Event</th><th>Status</th></tr></thead><tbody>'''+rows+'''</tbody></table>
<h3>Who does what</h3>
<table><thead><tr><th>Body</th><th>Looks at</th><th>Can do at home</th></tr></thead><tbody>
<tr><td><b>Cyber Force</b> (army)</td><td>Threats from abroad; protects military systems; works with military intelligence</td><td>Supports the authorities with monitoring and analysis; rapid teams for a serious national incident</td></tr>
<tr><td><b>Centre for Cybersecurity Belgium</b> (civilian)</td><td>National policy, warnings, supervision of vital organisations</td><td>Leads the national response</td></tr>
<tr><td><b>Military intelligence</b></td><td>Spying and sabotage against Defence</td><td>Led the investigation behind the May 2026 arrest</td></tr>
<tr><td><b>State Security</b> (civilian)</td><td>Spying, interference and extremism in the country</td><td>Was itself hit through a supplier in 2025–2026</td></tr>
<tr><td><b>Air security centre</b></td><td>One picture of the sky: Defence, police, customs, aviation</td><td>Strengthened after the 2025 drone reports</td></tr>
</tbody></table>
<h3>Proven and not proven</h3>
<table><thead><tr><th>Proven</th><th>Not proven</th></tr></thead><tbody>
<tr><td>The army may support civil authorities in a cyber crisis and keeps rapid teams for it.</td><td>That those teams were ever sent to a hospital or town hall: nothing found, also not for AZ Monica.</td></tr>
<tr><td>Belgium counts 1.43% of its economy as resilience spending.</td><td>How much of that is new money for cybersecurity and how much is existing spending counted differently.</td></tr>
<tr><td>The Cyber Force relies on reservists and civilians and is recruiting.</td><td>Its size, and whether it has the people it needs.</td></tr>
</tbody></table>
<p class="pl"><b>What it shows:</b> The budget line exists and the rapid teams exist, but the link between the army's cyber people and a small hospital in trouble is still a sentence in a plan. The cheapest gain is to practise it: one yearly exercise in which the Cyber Force, the CCB, a hospital and a town hall work through the same attack.<span class="plnl"><b>NL – Wat het toont:</b> De begrotingslijn bestaat en de snelle teams bestaan, maar de schakel tussen de cybermensen van het leger en een klein ziekenhuis in nood is nog een zin in een plan. De goedkoopste winst is het te oefenen: één jaarlijkse oefening waarin de Cyber Force, het CCB, een ziekenhuis en een gemeentehuis dezelfde aanval doorlopen.</span></p>
<h3>Still open</h3>
<ul>
<li>The size of the Cyber Force and of its reserve.</li>
<li>Whether a Cyber Rapid Response Team has been used for a civilian incident, and under which rule.</li>
<li>What exactly is counted in the 1.43% for resilience.</li>
<li>Belgium's rules for striking back in cyberspace: no 2025–2026 source found.</li>
<li>Whether the air security centre is fully working (see the page on drones).</li>
</ul>
<p class="src">Sources: see the linked list below.</p>
</section>'''
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='defence')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'defence'" not in t:
    a="{'k': 'more', 'en': 'More subjects to explore'"; assert a in t
    t=t.replace(a,"{'k': 'defence', 'en': 'The defence side: Belgium', 'nl': 'De defensiekant: België', 'src': ('R', 'defence')}, "+a,1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['defence']" not in t:
    t+='''
INTRO['defence']=("What the Belgian army does about cyber and hybrid threats: its cyber branch, the people and money, and what it may do inside the country.","Wat het Belgische leger doet aan cyber- en hybride dreigingen: zijn cybertak, de mensen en het geld, en wat het in eigen land mag doen.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '#p-defence td' not in t:
    t=t.replace('</style>','@media(max-width:699px){#p-defence td,#p-defence th{overflow-wrap:anywhere;padding-left:3px;padding-right:3px;font-size:12px}#p-defence .tag{font-size:9px;letter-spacing:0;padding:1px 4px}#p-defence table{table-layout:fixed;width:100%}}\n</style>',1)
    open(a,'w',encoding='utf-8').write(t)
print('defence ok')
