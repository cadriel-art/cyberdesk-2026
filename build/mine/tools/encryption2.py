from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join(' <span class="tag %s">%s</span>'%(T[x][1],T[x][0]) for x in s)
D={
'Austria':([('2025','Named in every count of the countries blocking the scanning duty.','R')],'Against, by all accounts.','Tegen, volgens alle tellingen.'),
'Czechia':([('Sep 2025','Prime Minister Petr Fiala said in public that Prague would not support the monitoring of citizens’ private correspondence. One of the few positions stated by a head of government in his own words.','C')],'The clearest "no" from the top of a government.','Het duidelijkste "nee" van de top van een regering.'),
'Denmark':([('Oct 2025','Holding the EU presidency, Denmark dropped the compulsory scanning from its compromise. Justice Minister Peter Hummelgaard said the screening would stay voluntary. It did so after a blocking minority formed, Germany among them.','C'),
 ('Nov 2025 – 2026','Campaigners disagree whether this was a withdrawal or a pause: the Council kept a permanent voluntary regime in its position, and the talks went on.','K')],
 'The country that had to give way, and the one most accused of trying again.','Het land dat moest toegeven, en dat het meest beschuldigd wordt van een nieuwe poging.'),
'Estonia':([('2025','Named among the opposing countries.','R')],'Against.','Tegen.'),
'Finland':([('2025','Named among the opposing countries.','R')],'Against.','Tegen.'),
'France':([('Feb–Mar 2025','In the law against drug trafficking the Senate inserted article 8 ter, obliging messaging services to give access to intercepted conversations. Critics, including people inside the government, called it worse than a back door, because the police would be added as a hidden extra reader in a conversation. The interior minister denied it was a back door. The law commission of the National Assembly deleted the article, and on 20 March the Assembly rejected the amendments that tried to put it back.','C'),
 ('12–13 Jun 2025','The Constitutional Council struck down six provisions of the law (decision 2025-885 DC) and the law was promulgated on 13 June 2025 as law 2025-532. Whether the encryption article appears anywhere in the final text could not be verified in the sources found; the Assembly had removed it.','CN'),
 ('17 Nov 2026','The National Assembly adopted the "résilience" bill in first reading by 464 votes to 64 with 16 abstentions, according to specialist press. MPs deleted article 16 bis, added by the Senate, on encrypted messaging, by 69 votes to 37 (AEF info; this split is not cross-checked elsewhere). The bill transposes the NIS2 and CER directives; reports differ on how many entities it covers (about 15,000, or more than 18,000 according to the government). A joint Senate-Assembly committee (CMP) is still to come.','C'),
 ('2025–2026','France is named in most counts as a supporter of the EU scanning duty.','R')],
 'A country that pushes for access in Europe and refused it at home, within four months.','Een land dat in Europa toegang bepleit en ze thuis weigerde, binnen vier maanden.'),
'Germany':([('Sep–Oct 2025','Germany joined the opposition and forced the Council vote to be delayed. The interior ministry said it could not support measures that break encryption; Justice Minister Stefanie Hubig said chat control without cause must be taboo in a state under the rule of law.','C'),
 ('2026','One campaign tracker reports that the instructions given to German negotiators since June 2026 no longer rule out a compulsory detection that would supplement the voluntary scanning. Not confirmed elsewhere.','K')],
 'The weight that stopped it, and the position most often said to be shifting.','Het gewicht dat het tegenhield, en de positie waarvan het vaakst gezegd wordt dat ze schuift.'),
'Hungary':([('2025','Named in some counts as a supporter.','R')],'Reported as for, no statement found.','Gemeld als voor, geen verklaring gevonden.'),
'Ireland':([('2025','Named in some counts as a supporter. Ireland hosts the European headquarters of the largest messaging companies, so the duty would be enforced there.','R')],'Where the law would actually land.','Waar de wet echt zou neerkomen.'),
'Italy':([('2025–2026','The counts contradict each other: one lists Italy among the formal opponents in June 2026, others among the supporters. No Italian government statement was found.','K')],'The clearest example of why these lists should be read with care.','Het duidelijkste voorbeeld waarom deze lijstjes met zorg gelezen moeten worden.'),
'Luxembourg':([('Sep–Oct 2025','Joined the opposition together with Germany, which helped create the blocking minority.','R')],'A small vote that mattered.','Een kleine stem die telde.'),
'Netherlands':([('2025','Named among the opposing countries, after a period of being undecided. One later count lists it among the four formal opponents.','R')],'Against, after hesitating.','Tegen, na aarzelen.'),
'Poland':([('2023–2025','Reported to have opposed the scanning duty since it was proposed, and to have kept that position across a change of government.','R')],'The only position said to have survived a change of government.','De enige positie waarvan gezegd wordt dat ze een regeringswissel overleefde.'),
'Portugal':([('2025','Named in some counts as a supporter.','R')],'Reported as for.','Gemeld als voor.'),
'Slovenia':([('2025','Named among the opposing countries.','R')],'Against.','Tegen.'),
'Spain':([('2025','Named in most counts as one of the strongest supporters of the scanning duty.','R')],'Reported as the firmest "yes".','Gemeld als het stevigste "ja".'),
'Sweden':([('Feb 2025 – 2026','A bill on data storage and access to electronic information would oblige messaging services such as Signal and WhatsApp to keep messages and give the police access to a suspect’s history. The government wanted it in force on 1 March 2026.','C'),
 ('Feb–Apr 2025','Signal said it would leave Sweden rather than comply, because the change would weaken its whole network. The Global Encryption Coalition wrote to parliament warning the same.','C'),
 ('2025','The Swedish Armed Forces opposed the bill, warning that such an access mechanism could be used by people it was not meant for. Their own chief information officer had told staff to use Signal for calls and messages that do not concern classified information. The justice minister, the security service and the national police backed the bill.','C'),
 ('2026','What parliament finally decided could not be established in the sources found.','N')],
 'The one country whose own army said in public that the bill would make it less safe.','Het enige land waarvan het eigen leger publiek zei dat het wetsvoorstel het onveiliger zou maken.'),
'Cyprus':([('2025','Named in some counts as a supporter. Cyprus held the presidency for one round of the talks in June 2026.','R')],'Reported as for.','Gemeld als voor.'),
}
NONE=['Bulgaria','Croatia','Greece','Iceland','Latvia','Liechtenstein','Lithuania','Malta','Norway','Romania','Slovakia','Switzerland']
assert len(D)+len(NONE)==30,(len(D),len(NONE))
def card(n):
    ev,se,sn=D[n]
    return '<div class="country" id="e-%s"><h4>%s <small>%d on record</small></h4><ul>%s</ul><p class="pl"><b>What it shows:</b> %s<span class="plnl"><b>NL – Wat het toont:</b> %s</span></p></div>'%(n,n,len(ev),''.join('<li><b>%s:</b> %s%s</li>'%(d,t,tg(s)) for d,t,s in ev),se,sn)
nev=sum(len(D[n][0]) for n in D)
SEC='''<section id="encryptioneu">
<h2>Encryption and "chat control": the other 30 countries</h2>
<p class="sub">Where each country stands on letting the police read private messages, and the national laws that go further than the EU one. @@N@@ entries in @@C@@ countries.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>Europe split in two over this, and the split does not follow the usual lines. A group led by Germany, with Poland, Austria, the Netherlands, Finland, Estonia, Czechia, Slovenia and Luxembourg, blocked the compulsory scanning in the autumn of 2025, and Denmark, which held the presidency, dropped it. France, Spain, Italy, Portugal, Ireland, Hungary and Cyprus are named on the other side, Belgium nowhere. Meanwhile two countries tried on their own what the EU could not agree: Sweden with a bill that would make messaging services keep messages, and France with an article that would add the police as a hidden reader. The French article was taken out by its own parliament. What Sweden decided could not be established.</p>
<p class="pb-nl"><b>NL:</b> Europa viel hierover in twee, en de breuklijn volgt niet de gewone lijnen. Een groep onder leiding van Duitsland, met Polen, Oostenrijk, Nederland, Finland, Estland, Tsjechië, Slovenië en Luxemburg, blokkeerde in het najaar van 2025 de verplichte scanning, en Denemarken, dat het voorzitterschap had, liet ze vallen. Frankrijk, Spanje, Italië, Portugal, Ierland, Hongarije en Cyprus worden aan de andere kant genoemd, België nergens. Intussen probeerden twee landen op eigen houtje wat de EU niet eens raakte: Zweden met een wetsvoorstel dat berichtendiensten berichten zou doen bewaren, en Frankrijk met een artikel dat de politie als verborgen meelezer zou toevoegen. Het Franse artikel werd door het eigen parlement geschrapt. Wat Zweden besliste, kon niet worden vastgesteld.</p></div>
<div class="warnbox"><b>Read the country lists with care.</b> There is no official published list of how each government stands. Everything below comes from campaign trackers and press reports, and they contradict each other: Italy appears on both sides, the number of opposing countries is given as five, six, seven or nine depending on the tracker and the date, and positions changed between meetings. Only the statements made in a government’s own words are marked Confirmed here.
<span class="plnl"><b>NL – Lees de landenlijsten met zorg.</b> Er is geen officiële gepubliceerde lijst van hoe elke regering staat. Alles hieronder komt van actiegroepen en persberichten, en die spreken elkaar tegen. Alleen uitspraken in de eigen woorden van een regering staan hier als bevestigd.</span></div>
<h3>Where countries are said to stand</h3>
<table><thead><tr><th>Position</th><th>Countries named</th><th>How firm</th></tr></thead><tbody>
<tr><td><b>Against a compulsory scanning duty</b></td><td>Germany, Poland, Austria, Netherlands, Finland, Estonia, Czechia, Slovenia, Luxembourg</td><td><span class="tag t-conf">Confirmed</span> for Germany and Czechia, in ministers’ own words; <span class="tag t-rep">Reported</span> for the rest</td></tr>
<tr><td><b>For</b></td><td>France, Spain, Italy, Portugal, Ireland, Hungary, Cyprus</td><td><span class="tag t-rep">Reported</span>; no government statement found for any of them</td></tr>
<tr><td><b>Gave way as presidency</b></td><td>Denmark</td><td><span class="tag t-conf">Confirmed</span>, the justice minister said so</td></tr>
<tr><td><b>No public position</b></td><td>Belgium</td><td><span class="tag t-conf">Confirmed</span>; see <a href="#encryption">the Belgium page</a></td></tr>
<tr><td><b>Not in the EU, so no vote</b></td><td>Norway, Iceland, Switzerland, Liechtenstein</td><td><span class="tag t-conf">Confirmed</span></td></tr>
<tr><td><b>Contradicted between sources</b></td><td>Italy, and the size of the opposing group</td><td><span class="tag t-claim">Claimed</span></td></tr>
</tbody></table>
<h3>What countries tried on their own</h3>
<table><thead><tr><th>Country</th><th>What it would do</th><th>Where it ended</th></tr></thead><tbody>
<tr><td><b>Sweden</b></td><td>Oblige messaging services to keep messages and give police access to a suspect’s history; in force from 1 March 2026 as proposed</td><td>Signal said it would leave the country; the armed forces opposed it; the outcome in parliament was not found</td></tr>
<tr><td><b>France</b></td><td>Article 8 ter: oblige messaging services to open access to intercepted conversations, by adding a hidden reader</td><td>Deleted by the National Assembly’s law commission; attempts to restore it rejected on 20 March 2025</td></tr>
<tr><td><b>Belgium</b></td><td>Already in force: refusing to give a password is punishable; telephone and internet records are kept</td><td>See <a href="#encryption">the Belgium page</a></td></tr>
</tbody></table>
<h3>What the courts decided</h3>
<ul>
<li><b>EncroChat, 30 April 2024.</b> The EU Court of Justice, sitting as a Grand Chamber, ruled in case C-670/22 on three points. A prosecutor may ask another member state for data from a cracked encrypted phone network without a judge’s order. The law of the country handing over the evidence is the test for whether it was lawfully obtained. The accused must be able to challenge the evidence for it to be used. It is the ruling every national court now works from. <span class="tag t-conf">Confirmed</span></li>
<li><b>Belgium, Sky ECC.</b> The Antwerp court of appeal and the Court of Cassation rejected the procedural challenges; 1,206 convictions. See <a href="#encryption">the Belgium page</a>. <span class="tag t-conf">Confirmed</span></li>
<li><b>Germany and the Netherlands.</b> Both had EncroChat cases that reached their highest courts; what those courts held after the EU ruling was not found. <span class="tag t-none">Not found</span></li>
</ul>
<h3>Countries with something on record</h3>
<div class="countries">@@CARDS@@</div>
<h3>Nothing specific found</h3>
<p>@@NONE@@.</p>
<p class="small">Four of these are not in the EU and have no vote on the regulation: Norway, Iceland, Switzerland and Liechtenstein. For the others, no position and no national law on encryption came up in the searches of 16 November 2026.</p>
<p class="pl"><b>What it shows:</b> The argument is not between countries that care about children and countries that care about privacy. It is between those who believe a door can be built for the police alone, and those who do not. The most telling voice is not a privacy group: it is the Swedish army, which told its own government that the law would make the country less safe, having already told its own staff to use the app the law would weaken.<span class="plnl"><b>NL – Wat het toont:</b> De discussie gaat niet tussen landen die om kinderen geven en landen die om privacy geven. Ze gaat tussen wie gelooft dat je een deur kunt bouwen voor alleen de politie, en wie niet. De veelzeggendste stem is geen privacygroep: het is het Zweedse leger, dat zijn eigen regering zei dat de wet het land onveiliger zou maken, nadat het zijn eigen personeel al had aangeraden de app te gebruiken die de wet zou verzwakken.</span></p>
<h3>Still open</h3>
<ul>
<li>What the Swedish parliament decided about the data storage bill.</li>
<li>Whether the French encryption article survived anywhere in the promulgated law of 13 June 2025.</li>
<li>Whether a seventh round of EU talks happened, and with what result.</li>
<li>Any official list of national positions: none is published.</li>
<li>What the German and Dutch supreme courts held on EncroChat after the EU ruling.</li>
<li>Whether Germany’s position has really shifted since June 2026, as one tracker says.</li>
</ul>
<p class="src">Sources: see the linked list below.</p>
</section>'''.replace('@@N@@',str(nev)).replace('@@C@@',str(len(D))).replace('@@CARDS@@',''.join(card(n) for n in sorted(D))).replace('@@NONE@@',', '.join(NONE))
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='encryptioneu')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
w=R.find('section',id='encryption'); p=w.find('p',class_='sub')
p.string=p.get_text()+' The other 30 countries have their own page.'
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'encryptioneu'" not in t:
    a="'src': ('R', 'encryption')}, "; assert a in t
    t=t.replace(a,a+"{'k': 'encryptioneu', 'en': 'Encryption: 30 countries', 'nl': 'Versleuteling: 30 landen', 'src': ('R', 'encryptioneu')}, ",1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['encryptioneu']" not in t:
    t+='''
INTRO['encryptioneu']=("Which governments want the police to be able to read private messages and which refuse, and the national laws that went further than the EU one.","Welke regeringen willen dat de politie priveberichten kan lezen en welke weigeren, en de nationale wetten die verder gingen dan de Europese.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '#p-encryptioneu td' not in t:
    t=t.replace('</style>','@media(max-width:699px){#p-encryptioneu td,#p-encryptioneu th{overflow-wrap:anywhere;padding-left:3px;padding-right:3px;font-size:12px}#p-encryptioneu table{table-layout:fixed;width:100%}}\n</style>',1)
    open(a,'w',encoding='utf-8').write(t)
print('encryption2 ok',nev,len(D))
