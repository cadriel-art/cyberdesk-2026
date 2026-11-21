from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join('<span class="tag %s">%s</span> '%(T[x][1],T[x][0]) for x in s)
EV=[
('Mar 2021','Belgium','Sky ECC is broken open','Belgian investigators, with French and Dutch help, read about a billion messages from the encrypted phone service Sky ECC. It becomes the largest criminal investigation in Belgian history. Background, before this file’s two years, but it is the reason Belgium matters in this debate.','C'),
('May 2022','EU','The proposal that became known as "chat control"','The European Commission proposes a regulation against child sexual abuse online. Its heart is the "detection order": a judge or authority could oblige a messaging service to search its users’ messages for known abuse images. Critics say that cannot be done on an end-to-end encrypted service without weakening the encryption for everyone.','C'),
('14 Jun 2023','Belgium','The courts back the Sky ECC evidence','The Antwerp court of appeal rejects, with reasons, all procedural objections against the intercepted and decrypted messages. The Court of Cassation later rejects procedural objections too.','C'),
('Dec 2023','Belgium','A thousand convictions','1,000 individual convictions in 81 trials on Sky ECC material.','C'),
('2022–2024','Belgium','Keeping telephone and internet records','The data retention law of 20 July 2022 (published 8 August 2022) replaces the 2016 law that the Constitutional Court had annulled in April 2021. The new law is itself challenged; the Constitutional Court ruled on those challenges on 26 September 2024 (judgment 97/2024), among other things on lawyers’ professional secrecy. Which parts were annulled is not stated in the sources found.','CR','The law and the judgment are confirmed; the outcome of the judgment is not.'),
('Jun 2025','EU','ProtectEU: the police want a way in','The Commission publishes a roadmap for lawful and effective access to data for law enforcement, with a separate technology roadmap on encryption. An expert group is to report by 2026, and the aim is to give Europol a next-generation decryption capacity from 2030. Updating the EU rules on keeping telephone and internet records is named as a possible next step.','C'),
('12 Sep 2025','Belgium','Belgium does not take a side','At the EU justice ministers’ meeting Belgium does not explicitly oppose the detection orders. Interior Minister Quintin says Belgium has no position yet and speaks of a balance between privacy and fighting the spread of such images.','R'),
('Oct 2025','Belgium','Pressure at home','A newspaper reports from good sources that Belgium will probably vote against. The Flemish minister-president asks for extra privacy guarantees while supporting the aim. In the Flemish Parliament a proposal for a resolution asks Belgium to reject the regulation.','R'),
('Nov 2025','EU','Mandatory scanning is dropped','Governments take compulsory detection orders out of the Council’s position. Campaigners warn that the wording on "risk mitigation" could still push encrypted services the same way.','CK','The change is confirmed; what the remaining wording would do is contested.'),
('Mar–Jul 2026','EU','The temporary permission, and a Belgian abstention','The temporary exception that lets providers look for abuse images voluntarily runs out and is then restored: on 23 July 2026 it is extended to 3 April 2028. It covers unencrypted messages only. Belgium abstained in the vote.','C'),
('29 Jun 2026','EU','Age checks taken out','At the fifth round of talks the negotiators agree that this regulation is not the place to regulate age verification. From a campaign source.','R'),
('29 Sep 2026','EU','Sixth round, still no deal','The sixth round of talks between Parliament, Council and Commission ends without agreement on detection orders. Technical talks continue. Campaign sources expect a further attempt in November or on 8 December 2026; the date is not confirmed.','RK'),
('Oct 2026','Belgium','Sky ECC, five years on','The federal prosecutor and the Antwerp prosecutor publish the result: 1,206 people convicted, 3,684 years of prison, in 178 court rulings, mostly for drugs.','C'),
('2022–2026','Belgium','The other side of the same case','Defence lawyers challenge the reliability of the Sky ECC material. A forensic expert finds the digital evidence unreliable and says filtering duplicated or changed messages; an Antwerp court refuses extra time to examine it. Earlier objections about a possibly falsified police record were rejected. Courts have so far accepted the evidence.','RN','The challenges are reported; a court has not found the evidence unlawful.'),
]
rows=''.join('<tr><td class="nowrap"><b>%s</b><br><span class="small">%s</span></td><td><b>%s.</b> %s%s</td><td>%s</td></tr>'%(r[0],r[1],r[2],r[3],(' <span class="small"><i>%s</i></span>'%r[5]) if len(r)>5 else '',tg(r[4])) for r in EV)
SEC='''<section id="encryption">
<h2>Encryption and "chat control": Belgium</h2>
<p class="sub">The fight over whether the police may read private messages, where Belgium stands, and what Belgium’s own biggest case says about it. A law page: no attacks here, but the rules that decide how safe everyone’s messages are.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>End-to-end encryption means only you and the person you write to can read the message, not even the company carrying it. Police and prosecutors say that leaves them blind to crimes against children and to organised crime. The EU has been arguing since 2022 about a law that would oblige messaging services to search messages for known abuse images, nicknamed "chat control". Security experts answer that a service cannot search what it cannot read, so the only way is to weaken the encryption, and a weakness built for the police is a weakness for everyone. Belgium has not taken a public side. It abstained in the one vote that has been held.</p>
<p class="pb-nl"><b>NL:</b> Eind-tot-eindversleuteling betekent dat alleen jij en de persoon aan wie je schrijft het bericht kunnen lezen, zelfs het bedrijf dat het vervoert niet. Politie en parket zeggen dat ze daardoor blind zijn voor misdaden tegen kinderen en voor georganiseerde misdaad. De EU discussieert sinds 2022 over een wet die berichtendiensten zou verplichten berichten te doorzoeken op gekende beelden van misbruik, bijgenaamd "chat control". Beveiligingsexperts antwoorden dat een dienst niet kan doorzoeken wat hij niet kan lezen, dus de enige weg is de versleuteling verzwakken, en een zwakke plek gemaakt voor de politie is een zwakke plek voor iedereen. België heeft publiek geen kant gekozen. Het onthield zich bij de enige stemming die er is geweest.</p></div>
<div class="warnbox"><b>Labels.</b> <span class="tag t-conf">Confirmed</span> stated by a government, an EU institution, a court or a prosecutor. <span class="tag t-rep">Reported</span> in the press or by a campaign group, not verified. <span class="tag t-claim">Claimed</span> asserted by one side of the argument. <span class="tag t-none">Not proven</span> raised and not upheld.
<span class="plnl"><b>NL – Labels.</b> Confirmed = gezegd door een overheid, een EU-instelling, een rechtbank of een parket. Reported = in de pers of door een actiegroep, niet nagekeken. Claimed = beweerd door één kant van het debat. Not proven = opgeworpen en niet aanvaard.</span>
<br><b>A warning about the sources on this page.</b> Much of what is written about "chat control" comes from campaign groups on both sides, and their accounts of dates and of what was agreed do not always match. Where sources conflict, this page says so and uses the public broadcaster’s account.</div>
<h3>The two arguments, as they are actually made</h3>
<table><thead><tr><th>For scanning</th><th>Against scanning</th></tr></thead><tbody>
<tr><td>Images of child abuse are shared on ordinary messaging services, and nobody sees them.</td><td>True, and nobody disputes it. The argument is about the method, not the aim.</td></tr>
<tr><td>Services can look for <i>known</i> images without a human reading anything.</td><td>On an end-to-end encrypted service the search has to happen on your own phone, before the message is locked. That is a door into the device.</td></tr>
<tr><td>A judge or authority would have to order it, case by case.</td><td>Once the door exists, who may open it is a political decision that can change.</td></tr>
<tr><td>Police already lose cases because they cannot read what they lawfully seized.</td><td>Belgium proved with Sky ECC that police can get in without a law that weakens everyone’s phone.</td></tr>
<tr><td>Criminals move to services outside the EU.</td><td>Which is also the reason the law would mostly reach ordinary users.</td></tr>
</tbody></table>
<h3>What happened, in order</h3>
<table><thead><tr><th>Date</th><th>Event</th><th>Status</th></tr></thead><tbody>'''+rows+'''</tbody></table>
<h3>What Belgium itself already allows</h3>
<ul>
<li><b>Giving up your password.</b> The Court of Cassation ruled on 4 February 2020 that the right to silence and the presumption of innocence are no bar to punishing someone who refuses to give a password or PIN code. Sources disagree on whether such an order may be given to the suspect personally or only to others who know the code. <span class="tag t-conf">Confirmed</span> <span class="tag t-rep">Reported</span></li>
<li><b>Keeping telephone and internet records.</b> The law of 20 July 2022 obliges operators to keep identification and traffic data and to hand them over to the authorities. It replaced the 2016 law, which the Constitutional Court annulled in April 2021 because general, undifferentiated storage was too far-reaching. The 2022 law was itself challenged, and the Constitutional Court ruled on those challenges on 26 September 2024. <span class="tag t-conf">Confirmed</span></li>
<li><b>Breaking in.</b> The Sky ECC operation shows Belgium already has, and uses, the power to get at encrypted communications with a court’s approval, without any new EU law. <span class="tag t-conf">Confirmed</span></li>
</ul>
<h3>The Belgian case that both sides quote</h3>
<p>Sky ECC is the strongest argument each side has, which is why it belongs on this page.</p>
<table><thead><tr><th>What it proves for the police</th><th>What it proves for the critics</th></tr></thead><tbody>
<tr><td>1,206 people convicted and 3,684 years of prison in 178 rulings, mostly for drug crime.</td><td>All of it was obtained by attacking one criminal service, not by weakening everybody’s messaging.</td></tr>
<tr><td>The courts, up to the Court of Cassation, have upheld the evidence against repeated procedural challenges.</td><td>A forensic expert found the material unreliable in places, and defence teams say filtering duplicated or altered messages.</td></tr>
<tr><td>Without reading the messages the network could not have been taken apart.</td><td>About a billion messages of all users were read, not only those of the people later charged.</td></tr>
</tbody></table>
<h3>Proven and not proven</h3>
<table><thead><tr><th>Proven</th><th>Not proven</th></tr></thead><tbody>
<tr><td>The temporary rule letting providers scan voluntarily runs to 3 April 2028 and covers unencrypted messages only.</td><td>What the permanent regulation will say: after six rounds of talks there is no agreement.</td></tr>
<tr><td>Belgium abstained in the July 2026 vote and had taken no public position before that.</td><td>How Belgium will vote on the permanent text.</td></tr>
<tr><td>Belgium can already compel a password and keep telephone records.</td><td>That Belgian police are blocked by encryption in practice: no Belgian figure found.</td></tr>
<tr><td>Sky ECC produced more than 1,200 convictions.</td><td>That the same result needs a general scanning duty.</td></tr>
</tbody></table>
<p class="pl"><b>What it shows:</b> Belgium is the country with the least reason to need "chat control" and the quietest voice in the argument. It broke the biggest encrypted criminal network in Europe with a court order and good police work, it can already force a password out of a suspect, and it keeps everyone’s telephone records. What it has not done is say in public what it wants, which is why nobody can hold it to anything.<span class="plnl"><b>NL – Wat het toont:</b> België is het land dat "chat control" het minst nodig heeft en de stilste stem in het debat. Het brak het grootste versleutelde criminele netwerk van Europa open met een gerechtelijk bevel en goed politiewerk, het kan al een wachtwoord afdwingen van een verdachte, en het bewaart ieders telefoongegevens. Wat het niet gedaan heeft, is publiek zeggen wat het wil, en daardoor kan niemand het ergens aan houden.</span></p>
<h3>Still open</h3>
<ul>
<li>Belgium’s official position on the permanent regulation: none found.</li>
<li>What the Constitutional Court actually decided on 26 September 2024 about the 2022 data retention law.</li>
<li>Whether a seventh round of EU talks takes place, and when: campaign sources give November or 8 December 2026.</li>
<li>What the Commission’s expert group on encryption technology concluded, due in 2026.</li>
<li>The outcome of the reliability challenge to the Sky ECC material in the cases still running.</li>
<li>How many Belgian investigations actually fail because of encryption: no figure published.</li>
</ul>
<p class="src">Sources: see the linked list below.</p>
</section>'''
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='encryption')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'encryption'" not in t:
    a="{'k': 'files', 'en': 'Where each law stands'"; assert a in t
    t=t.replace(a,"{'k': 'encryption', 'en': 'Encryption and \"chat control\"', 'nl': 'Versleuteling en \"chat control\"', 'src': ('R', 'encryption')}, "+a,1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['encryption']" not in t:
    t+='''
INTRO['encryption']=("Whether the police may read private messages: the EU fight over \\"chat control\\", where Belgium stands, and what the Sky ECC case says about it.","Of de politie priveberichten mag lezen: de EU-strijd over \\"chat control\\", waar Belgie staat, en wat de Sky ECC-zaak daarover zegt.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '#p-encryption td' not in t:
    t=t.replace('</style>','@media(max-width:699px){#p-encryption td,#p-encryption th{overflow-wrap:anywhere;padding-left:3px;padding-right:3px;font-size:12px}#p-encryption .tag{font-size:9px;letter-spacing:0;padding:1px 4px}#p-encryption table{table-layout:fixed;width:100%}}\n</style>',1)
    open(a,'w',encoding='utf-8').write(t)
print('encryption ok')
