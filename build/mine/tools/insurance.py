from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
SEC='''<section id="insurance">
<h2>Insurance</h2>
<p class="sub">Who is insured against a cyberattack, what insurers demand before they pay, and whether paying a ransom, or being reimbursed for one, is allowed. Belgium first, then Europe. A numbers page, so no country cards.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>Insurers can change behaviour faster than any law: they decide what a company must have in place before it is covered at all. That makes them, quietly, one of the strongest cybersecurity regulators in Europe. Two things stand out. Belgian small firms are the least insured of any country in the survey that measured it. And since 2023 every standalone cyber policy written in the main European market must exclude attacks backed by a state, with the insurer, not a court, deciding whether an attack qualifies. Most of the attacks in this file are blamed on states or on groups linked to them.</p>
<p class="pb-nl"><b>NL:</b> Verzekeraars kunnen gedrag sneller veranderen dan eender welke wet: zij bepalen wat een bedrijf in orde moet hebben voor het überhaupt gedekt is. Dat maakt hen stilzwijgend een van de sterkste cybertoezichthouders van Europa. Twee dingen vallen op. Belgische kleine bedrijven zijn het minst verzekerd van alle landen in de enquete die het mat. En sinds 2023 moet elke aparte cyberpolis op de belangrijkste Europese markt aanvallen uitsluiten die door een staat gesteund zijn, waarbij de verzekeraar, niet een rechtbank, beslist of een aanval daaronder valt. De meeste aanvallen in dit dossier worden aan staten of aan daaraan gelinkte groepen toegeschreven.</p></div>
<div class="warnbox"><b>Almost every number here comes from the industry itself.</b> Insurers, brokers and their market bodies publish these figures; there is no public statistics office for cyber insurance. They use different definitions of "insured", different samples and different years, and they contradict each other: one survey puts Belgian small firms at 55% insured, another puts European small firms at 15%. Both appear below, side by side, because neither can be checked against the other. Treat every figure as a claim by the people who sell the product.
<span class="plnl"><b>NL – Bijna elk cijfer hier komt van de sector zelf.</b> Verzekeraars, makelaars en hun organisaties publiceren deze cijfers; er is geen openbaar statistiekbureau voor cyberverzekering. Ze gebruiken verschillende definities, steekproeven en jaren, en ze spreken elkaar tegen. Behandel elk cijfer als een bewering van wie het product verkoopt.</span></div>
<h3>Belgium</h3>
<table><thead><tr><th>Figure</th><th>What it is</th><th>Source and status</th></tr></thead><tbody>
<tr><td><b>55%</b></td><td>Belgian small and medium firms with cyber cover, on its own or inside another policy. <b>The lowest of the ten countries surveyed</b>, against an international average of 64%.</td><td>Hiscox Cyber Readiness Report 2026, a survey of 6,800 decision-makers <span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>45%</b></td><td>The same thing the other way round: nearly half of Belgian small firms have no cyber insurance at all.</td><td>Same survey, via trade press <span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>42%</b></td><td>Of the Belgian firms without cover, the share that say they will take one within a year.</td><td>Same survey <span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>€2,500–€5,500</b></td><td>Indicative yearly premium for a firm of 50 to 100 staff with €1 million of cover, in 2026. Another broker quotes from €500. These are sales pages, not market data.</td><td>Belgian brokers <span class="tag t-claim">Claimed</span></td></tr>
<tr><td><b>€50,000–€250,000</b></td><td>Cost of a ransomware incident at a Belgian small firm, attributed to the national cyber centre by a secondary source.</td><td>Secondary <span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>Not found</b></td><td>Any figure from the Belgian insurers’ own federation on how many businesses hold cyber cover, or on what was paid out.</td><td>Searched; its 2024 key-figures report has no cyber data <span class="tag t-none">Not found</span></td></tr>
</tbody></table>
<h3>Europe</h3>
<table><thead><tr><th>Figure</th><th>What it is</th><th>Source and status</th></tr></thead><tbody>
<tr><td><b>$15–16 billion</b></td><td>Cyber insurance premiums worldwide, 2024–2026. Europe is put at roughly a fifth to a quarter of that, about $3.9 billion.</td><td>Reinsurers and brokers <span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>15%</b></td><td>Share of European small and medium firms that buy cyber insurance, called the main reason for the protection gap. Hard to square with the 55% for Belgium above; the definitions differ.</td><td>Marsh, quoted by the European risk managers’ federation <span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>More than 70%</b></td><td>Share of companies in France, Germany, Italy and Spain together said to have no cyber cover. Italy alone: 22% insured.</td><td>Howden broker report 2025 <span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>Less than 5%</b></td><td>Share of all cyber risk insured worldwide, on a reinsurer’s measure. A third definition again.</td><td>Munich Re <span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>−22%, then +15–20%</b></td><td>Prices fell 22% from their 2022 peak and about 6% further in 2025; a rating agency expects a rise of 15 to 20% in 2026.</td><td>Howden; S&amp;P Global Ratings <span class="tag t-rep">Reported</span></td></tr>
<tr><td><b>Mostly small firms</b></td><td>Most cyber claims by number come from micro and small companies, not large ones.</td><td>Munich Re <span class="tag t-rep">Reported</span></td></tr>
</tbody></table>
<h3>The exclusion that matters most</h3>
<p>Since <b>31 March 2023</b>, syndicates in the main European cyber market have had to write an exclusion for state-backed attacks into every standalone cyber policy. It is the single rule that decides whether the attacks described in this file are covered.</p>
<table><thead><tr><th>How it works</th><th>Why it is disputed</th></tr></thead><tbody>
<tr><td>The policy does not pay for an attack carried out by, or on behalf of, a state.</td><td>Nearly every serious case in this file is blamed on a state or a group linked to one, usually without proof that would stand in court. See <a href="#evidence">the evidence tracker</a>.</td></tr>
<tr><td>The usual threshold is an attack with a "major detrimental impact on the functioning of a state".</td><td>Almost nothing reaches that bar. A ransomware attack on a hospital does not, even when a state is blamed, so the grey zone is where most claims sit.</td></tr>
<tr><td>Under the standard wording, the insurer decides whether an attack was state-backed.</td><td>Not a court, not a government, not an agreed outside body. The company blaming Russia in its press release is arguing against its own claim.</td></tr>
<tr><td>Exclusions widened again through 2025 and 2026, while prices fell.</td><td>Cover got cheaper and narrower at the same time.</td></tr>
</tbody></table>
<p class="small">The best-known test of an older war exclusion, over the NotPetya attack of 2017, was decided against the insurers: the courts held the wording required real military action. Commentators say it set no binding precedent for today’s cyber-specific wording. <span class="tag t-rep">Reported</span></p>
<h3>Paying a ransom</h3>
<ul>
<li><b>No EU-wide ban exists.</b> Most member states do not make paying a ransom a crime. Paying can still break sanctions law if the money reaches a listed group, and an insurer will refuse to fund such a payment. <span class="tag t-conf">Confirmed</span></li>
<li><b>France</b> settled the question in a law of 24 January 2023: an insurer may reimburse a ransom, but only if the victim files a complaint with the police within 72 hours of becoming aware of the attack. It turns the insurance payout into a lever for reporting. <span class="tag t-rep">Reported</span></li>
<li><b>A ban was proposed and dropped.</b> An EU-level proposal to forbid ransom payments and to forbid insurers from reimbursing them was debated in 2021 and not adopted. <span class="tag t-rep">Reported</span></li>
<li><b>The United Kingdom</b> said in July 2025 that it would ban payments by public bodies and operators of vital services. A year later it was still a proposal. Outside this file’s 31 countries, but the nearest live example. <span class="tag t-rep">Reported</span></li>
<li><b>Portugal</b> is described by one source as an exception that restricts cover for ransom payments; the detail could not be verified. <span class="tag t-claim">Claimed</span></li>
<li><b>The insurers’ own argument against a ban:</b> an international insurance research body holds that forbidding payment or reimbursement would push the transactions underground, where nobody can see them. <span class="tag t-rep">Reported</span></li>
<li><b>Belgium:</b> no rule found either way, and no figure on whether Belgian insurers reimburse ransoms. This is idea 13 in <a href="#ideas">the list of 53</a>. <span class="tag t-none">Not found</span></li>
</ul>
<h3>Proven and not proven</h3>
<table><thead><tr><th>Proven</th><th>Not proven</th></tr></thead><tbody>
<tr><td>Standalone cyber policies in the main European market must exclude state-backed attacks, since March 2023.</td><td>How often that exclusion has actually been used to refuse a claim: no figure published.</td></tr>
<tr><td>France ties reimbursement of a ransom to reporting the crime within 72 hours.</td><td>Whether that increased reporting: no evaluation found.</td></tr>
<tr><td>There is no EU ban on paying, and a 2021 proposal was dropped.</td><td>Belgium’s own position on reimbursement.</td></tr>
<tr><td>Take-up among small firms is low across Europe, on every measure used.</td><td>How low: the surveys give 15%, 22%, 45% and 55% for overlapping things.</td></tr>
</tbody></table>
<p class="pl"><b>What it shows:</b> Insurance is the fastest lever nobody is pulling. An insurer can demand two-step login and tested backups tomorrow, where a law takes four years. But the product is drifting the wrong way for the risks in this file: narrower every year, with the state-backed exclusion aimed squarely at the attacks that are actually happening, and judged by the insurer itself. Two cheap fixes follow. Require the exclusion to rest on a formal public attribution rather than the insurer’s own view, and copy the French rule tying any reimbursement to reporting the attack, so that the register in this file stops being so short.<span class="plnl"><b>NL – Wat het toont:</b> Verzekering is de snelste hefboom waar niemand aan trekt. Een verzekeraar kan morgen tweestapsverificatie en geteste back-ups eisen, waar een wet vier jaar duurt. Maar het product schuift de verkeerde kant op voor de risico’s in dit dossier: elk jaar smaller, met de uitsluiting voor staatsaanvallen gericht op net die aanvallen die echt gebeuren, en beoordeeld door de verzekeraar zelf. Twee goedkope ingrepen volgen daaruit. Laat die uitsluiting steunen op een formele publieke toewijzing in plaats van op de mening van de verzekeraar, en neem de Franse regel over die vergoeding koppelt aan aangifte, zodat het register in dit dossier minder kort wordt.</span></p>
<h3>Still open</h3>
<ul>
<li>How many Belgian organisations hold cyber cover, from a Belgian source rather than an insurer’s survey.</li>
<li>Whether Belgian insurers reimburse ransoms, and whether Belgium wants to change that.</li>
<li>How often the state-backed exclusion has been used to refuse a European claim.</li>
<li>What Portugal actually did.</li>
<li>Whether the French 72-hour rule increased reporting.</li>
<li>Why Belgian small firms are the least insured of the countries surveyed.</li>
</ul>
<p class="src">Sources: see the linked list below.</p>
</section>'''
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='insurance')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'insurance'" not in t:
    a="{'k': 'skills', 'en': 'Skills and jobs'"; assert a in t
    t=t.replace(a,"{'k': 'insurance', 'en': 'Insurance', 'nl': 'Verzekering', 'src': ('R', 'insurance')}, "+a,1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['insurance']" not in t:
    t+='''
INTRO['insurance']=("Who is insured against an attack, what insurers demand first, and the exclusion that may leave most of the attacks in this file uncovered.","Wie verzekerd is tegen een aanval, wat verzekeraars eerst eisen, en de uitsluiting die de meeste aanvallen in dit dossier onverzekerd kan laten.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '#p-insurance td' not in t:
    t=t.replace('</style>','@media(max-width:699px){#p-insurance td,#p-insurance th{overflow-wrap:anywhere;padding-left:3px;padding-right:3px;font-size:12px}#p-insurance table{table-layout:fixed;width:100%}}\n</style>',1)
    open(a,'w',encoding='utf-8').write(t)
print('insurance ok')
