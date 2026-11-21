from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
SEC='''<section id="skills">
<h2>Skills and jobs</h2>
<p class="sub">How many cybersecurity people Belgium and Europe have, how many they are short, and what is being done about it. A numbers page: Belgium first, then Europe. Because these are statistics rather than incidents, there are no country cards here.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>Every page in this file ends at the same place: somebody had to notice, patch, warn or respond, and there was nobody. Belgium has about 9,750 full-time cybersecurity jobs and cannot fill roughly one specialist post in eight. Europe is short somewhere between a quarter of a million and half a million people, depending on who counts and how. The newest EU report says the problem is changing shape: not simply too few bodies, but too few people with the right skills, while the number of graduates grows more slowly than the need.</p>
<p class="pb-nl"><b>NL:</b> Elke pagina in dit dossier eindigt op dezelfde plek: iemand moest iets opmerken, herstellen, waarschuwen of reageren, en er was niemand. België telt ongeveer 9.750 voltijdse cyberbanen en krijgt ruwweg één specialistenpost op acht niet ingevuld. Europa komt tussen een kwart miljoen en een half miljoen mensen tekort, naargelang wie telt en hoe. Het nieuwste EU-rapport zegt dat het probleem van vorm verandert: niet gewoon te weinig mensen, maar te weinig mensen met de juiste vaardigheden, terwijl het aantal afgestudeerden trager groeit dan de nood.</p></div>
<div class="warnbox"><b>These numbers are not comparable with each other.</b> There is no agreed way to count a "cybersecurity job" or a "gap". One count measures unfilled advertised posts, another the difference between the staff organisations have and what they say they need, a third all of information security. Figures from different bodies and different years are set out separately below, never added together.
<span class="plnl"><b>NL – Deze cijfers zijn onderling niet vergelijkbaar.</b> Er is geen afgesproken manier om een "cyberbaan" of een "tekort" te tellen. Cijfers van verschillende instanties en jaren staan hieronder apart, nooit opgeteld.</span></div>
<h3>Belgium in numbers</h3>
<table><thead><tr><th>Figure</th><th>What it is</th><th>Source and status</th></tr></thead><tbody>
<tr><td><b>9,750</b></td><td>Full-time jobs in the Belgian cybersecurity sector in 2025, up from 6,405 in 2021: growth of 52% in four years.</td><td>Agoria study, via trade press <span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>6,190</b></td><td>Specialists needed for specialist roles, by the same study.</td><td>Agoria, via trade press <span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>About 4,000</b></td><td>Unfilled cybersecurity vacancies, the figure most often quoted in Belgium. It does not match the 6,190 above and the sources do not explain the difference.</td><td>Agoria, via trade press <span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>12.4%</b></td><td>Share of cybersecurity posts standing empty, against 5.3% across Belgian IT: more than twice the rate.</td><td>Agoria, via trade press <span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>Double by 2030</b></td><td>The expected size of the Belgian cyber sector.</td><td>Agoria, via trade press <span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>Falling</b></td><td>Belgian IT employment overall lost jobs in 2025, and in Wallonia IT vacancies fell 22%. Cybersecurity is the exception inside a shrinking sector.</td><td>Trade press; regional employment services <span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>Not public</b></td><td>The size of the army’s Cyber Force, which is recruiting reservists. See <a href="#defence">the defence page</a>.</td><td>Defence declined to say <span class="tag t-conf">Confirmed</span></td></tr>
</tbody></table>
<h3>Europe in numbers</h3>
<table><thead><tr><th>Figure</th><th>What it counts</th><th>Who says it, and when</th></tr></thead><tbody>
<tr><td><b>About 424,000</b></td><td>Unfilled cybersecurity positions in Europe, against about 1.4 million people employed in the field; said to be up nearly 10% in a year.</td><td>ISC2 workforce study, through a trade article; the report itself was not found <span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>At least 300,000</b></td><td>Specified cybersecurity openings in Europe.</td><td>ENISA, May 2025 <span class="tag t-conf">Confirmed</span></td></tr>
<tr><td><b>260,000 to 500,000</b></td><td>The EU shortage, on the Commission’s own earlier estimate. The width of that range is itself the point.</td><td>European Commission, 2023 <span class="tag t-conf">Confirmed</span></td></tr>
<tr><td><b>76% and 71%</b></td><td>Share of organisations that find it hard to attract, and to retain, cybersecurity staff.</td><td>ENISA investments survey, December 2025 <span class="tag t-conf">Confirmed</span></td></tr>
<tr><td><b>A changing problem</b></td><td>The EU’s November 2026 report says the gap has grown and has shifted from a shortage of staff to a shortage of skills, with graduate numbers rising more slowly than the need.</td><td>ENISA, State of Cybersecurity in the Union 2026 <span class="tag t-conf">Confirmed</span></td></tr>
<tr><td><b>Money moved, not people</b></td><td>Organisations are spending on technology and outsourcing instead of hiring, because they cannot find the people.</td><td>ENISA, December 2025 <span class="tag t-conf">Confirmed</span></td></tr>
</tbody></table>
<h3>What is being done</h3>
<table><thead><tr><th>Where</th><th>What</th><th>How far it has got</th></tr></thead><tbody>
<tr><td><b>EU</b></td><td>The Cybersecurity Skills Academy, set up in April 2023 to pull existing schemes together.</td><td>21 companies and bodies had made pledges and 10 partnerships existed by spring 2026. An early target of 200,000 people trained by 2025 was set; no progress figure against it was found.</td></tr>
<tr><td><b>EU</b></td><td>A Cybersecurity Skills Coalition, a joint body of member states, set up in June 2026 and seated in Athens. Its tasks include measuring the gap itself.</td><td>Founded by Greece, Cyprus, Austria, Croatia and Slovenia, with Poland as an observer. <b>Belgium is not a founder.</b></td></tr>
<tr><td><b>EU</b></td><td>A common description of cyber jobs (the European Cybersecurity Skills Framework), 12 profiles, so that training and vacancies speak the same language.</td><td>In force; under revision, with a public consultation planned for the end of 2026.</td></tr>
<tr><td><b>Company pledges</b></td><td>Individual commitments under the Academy.</td><td>IBM: 25,000 EU citizens trained by the end of 2026. Mastercard with a threat-intelligence firm: more than 650 staff of small firms, students and teachers by the end of 2028. A trade article mentions a much larger pledge by a network equipment maker, unverified.</td></tr>
<tr><td><b>Belgium</b></td><td>The Cyber Security Challenge, a student competition, and the national cyber centre’s free tools and training for organisations and small firms.</td><td>The competition final was held on 28 March 2026. The centre also joined an EU project to train small firms, with a first call for money expected in early 2026, and ran crisis-exercise training for colleges from March to May 2026.</td></tr>
<tr><td><b>Belgium</b></td><td>The army recruits cyber reservists; about a quarter of the Cyber Force are reservists.</td><td>A public call to specialists in March 2026. See <a href="#defence">the defence page</a>.</td></tr>
</tbody></table>
<h3>Why it stays unsolved</h3>
<ul>
<li><b>The shortage is structural, not a bad year.</b> Belgian analysis calls it a lasting mismatch between what employers ask and what the labour market offers, not a passing shock.</li>
<li><b>The ones who need people most can pay least.</b> Every page in this file ends there: small hospitals, towns, water companies and schools compete for the same specialists as banks and the army, and lose. See <a href="#health">health</a> and <a href="#water">water</a>.</li>
<li><b>Buying tools instead of hiring.</b> The EU’s own survey finds organisations moving money to technology and outsourcing because they cannot recruit, which stores up the same problem.</li>
<li><b>Nobody agrees what to count.</b> Without a common measure, no one can say whether any of the programmes is working. The new EU coalition has been given exactly that job, three years after the Academy started.</li>
</ul>
<h3>Proven and not proven</h3>
<table><thead><tr><th>Proven</th><th>Not proven</th></tr></thead><tbody>
<tr><td>Cybersecurity posts in Belgium stand empty at more than twice the rate of IT as a whole.</td><td>The exact number missing: the same study is quoted as 4,000 and as 6,190.</td></tr>
<tr><td>Attracting and keeping staff is hard for about three organisations in four across the EU.</td><td>Whether the EU Skills Academy has closed any of the gap: no progress figure exists.</td></tr>
<tr><td>The Belgian cyber sector grew 52% in four years while IT overall shrank.</td><td>That growth is reaching the organisations that need it most.</td></tr>
<tr><td>Europe’s gap is somewhere between 260,000 and about 424,000.</td><td>Any single reliable European figure.</td></tr>
</tbody></table>
<p class="pl"><b>What it shows:</b> This is the quiet reason behind most of the failures in this file. Not one of the attacks here needed a clever trick; they needed somebody absent. Belgium is not short of money for cybersecurity so much as short of people to spend it on, and the organisations that cannot hire are exactly the hospitals, towns and water companies that keep appearing in the register. The one measure that matches the problem is shared staff, paid once and used by many small bodies, which is also the idea that costs the least.<span class="plnl"><b>NL – Wat het toont:</b> Dit is de stille reden achter de meeste fouten in dit dossier. Geen van de aanvallen hier had een slim trucje nodig; ze hadden iemand nodig die er niet was. België komt minder geld tekort voor cyberveiligheid dan mensen om het aan te besteden, en de organisaties die niemand kunnen aanwerven zijn net de ziekenhuizen, gemeenten en waterbedrijven die telkens in het register opduiken. De ene maatregel die bij het probleem past, is gedeeld personeel, één keer betaald en door veel kleine organisaties gebruikt, en dat is ook het idee dat het minst kost.</span></p>
<h3>Still open</h3>
<ul>
<li>Why the Belgian study is quoted as both 4,000 and 6,190 missing specialists.</li>
<li>How many people the EU Skills Academy has actually trained against its target of 200,000.</li>
<li>The share of women in Belgian cybersecurity work, and salary levels: no figure found.</li>
<li>Country-by-country gap figures for Germany, France, Poland or the Netherlands: none published that could be found.</li>
<li>Why Belgium is not among the founders of the new EU skills coalition.</li>
<li>How many of the 9,750 Belgian jobs sit in companies that sell security, and how many inside the organisations that have to defend themselves.</li>
</ul>
<p class="src">Sources: see the linked list below.</p>
</section>'''
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='skills')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'skills'" not in t:
    a="{'k': 'citizens', 'en': 'How alert are citizens?'"; assert a in t
    t=t.replace(a,"{'k': 'skills', 'en': 'Skills and jobs', 'nl': 'Mensen en vacatures', 'src': ('R', 'skills')}, "+a,1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['skills']" not in t:
    t+='''
INTRO['skills']=("How many cybersecurity people Belgium and Europe have, how many they are short, and whether anything being done about it is working.","Hoeveel mensen voor cyberveiligheid Belgie en Europa hebben, hoeveel ze tekortkomen, en of wat eraan gedaan wordt iets oplevert.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '#p-skills td' not in t:
    t=t.replace('</style>','@media(max-width:699px){#p-skills td,#p-skills th{overflow-wrap:anywhere;padding-left:3px;padding-right:3px;font-size:12px}#p-skills table{table-layout:fixed;width:100%}}\n</style>',1)
    open(a,'w',encoding='utf-8').write(t)
print('skills ok')
