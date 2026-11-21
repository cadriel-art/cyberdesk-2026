from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join(' <span class="tag %s">%s</span>'%(T[x][1],T[x][0]) for x in s)
D={
'Bulgaria':([('2025–2026','Websites knocked offline in attacks that authorities and experts attribute to pro-Russian groups; ahead of the 2026 election the government started a programme against disinformation and asked the EU for help. From a US Congress research report.','R')],
 'Preparation rather than a recorded attack.','Voorbereiding, geen geregistreerde aanval.'),
'Cyprus':([('13 Nov 2026','The president said he does not rule out interference by artificial intelligence in the next elections: "we are of course all vulnerable".','C')],
 'A warning, nothing on record yet.','Een waarschuwing, nog niets geregistreerd.'),
'Czechia':([('3–4 Oct 2025','Parliamentary election. Researchers found networks linked to Russia trying to undermine trust in the vote, and clusters of accounts on TikTok, X and Telegram pushing foreign stories, but no operation able to change the result.','CN'),
 ('Autumn 2025','The fact-checker Demagog found hundreds of fake TikTok accounts spreading pro-Russian and anti-establishment content, and no evidence that the network was run from or by Russia.','CN')],
 'Plenty of noise, no effect found, and the Russian hand not shown.','Veel lawaai, geen effect gevonden, en de Russische hand niet aangetoond.'),
'Denmark':([('Nov 2025','Websites were attacked before the local elections. In December Danish military intelligence blamed the pro-Russian group NoName057(16) and linked it to the Russian state.','CK'),
 ('2026','A Nordic fact-checking network counts 247 attacks by activist-hacker groups on Denmark in 2026; they rise around elections and decisions that go against Russia. Not tied to one election.','R')],
 'Websites go down around every vote; the vote itself is on paper.','Websites gaan plat rond elke stembusgang; het stemmen zelf gebeurt op papier.'),
'France':([('May 2025','The state agency against foreign digital interference (Viginum) published a technical report on the Russian operation known as Storm-1516.','C'),
 ('6 Mar 2026','Before the municipal elections France accused Russia over a fake website aimed at a centre-right candidate for mayor of Paris. Viginum said it was probably the Storm-1516 network. It reached few people: under 20,000 views on X.','CK'),
 ('Mar 2026','Viginum also found 28 Facebook pages and 15 French-language websites run from abroad that pushed alarmist AI-made content; it judged the aim to be profit, not politics. A fake audio clip of the mayor of Grenoble was made with free voice-cloning tools.','C'),
 ('2026','New: the agency published a weekly bulletin on foreign interference during the campaign.','C')],
 'France now tells voters every week what it sees, and says when a fake is small.','Frankrijk vertelt kiezers nu elke week wat het ziet, en zegt het erbij wanneer een vervalsing klein is.'),
'Germany':([('Feb 2025','Federal election, 23 February. Fake videos claimed the AfD party was missing from postal ballots; researchers counted more than 700 fake accounts in the last week. Two days before the vote the government said it had indications of a Russian campaign.','C'),
 ('12 Dec 2025','The foreign ministry: "We can now state definitively that Russia, through the Storm 1516 campaign, sought to influence and destabilise the most recent federal election." The Russian ambassador was summoned. The same day Germany blamed Russian military intelligence for the 2024 attack on air traffic control.','CK'),
 ('Aug 2026','A deepfake of Chancellor Merz using the stolen logo of Deutsche Welle was attributed to Storm-1516. One technology outlet.','R'),
 ('Sep 2026','A Russian disinformation campaign was reported ahead of the state election in Saxony-Anhalt. One outlet.','R')],
 'The only country that has formally blamed a state for interfering in a national election in these two years.','Het enige land dat in deze twee jaar formeel een staat de schuld gaf van inmenging in een nationale verkiezing.'),
'Hungary':([('Feb–Mar 2026','TikTok removed two networks of fake accounts; a pro-Kremlin network impersonated Euronews to spread fake reports about the election.','C'),
 ('Mar–Apr 2026','Two Russian operations, Storm-1516 and "Matryoshka", spread fake videos, for example that Hungarian men would be drafted to fight for Ukraine if the opposition won. Analysts add that most of the disinformation in the campaign came from inside Hungary.','CK'),
 ('Spring 2026','An attack on the app of the opposition party Tisza reportedly led to stolen data that was then passed to pro-government media. One source.','R'),
 ('Spring 2026','The then government declassified part of an intelligence report claiming that IT specialists close to Tisza were linked to Ukraine\'s volunteer hacker force. The opposition called it a fabrication.','K'),
 ('12 Apr 2026','Election day. International observers: a lively contest with record turnout, but no equal chances because of the ruling party\'s advantages; several AI-made videos by political actors circulated. The opposition won and formed the government.','C')],
 'Foreign fakes were there, but the heavier pressure came from inside the country.','Er waren buitenlandse vervalsingen, maar de zwaarste druk kwam van binnen het land.'),
'Italy':([('5 Jun 2025','The parliamentary committee that oversees the secret services confirmed that the government used the spyware Graphite, made by the firm Paragon, against two migration activists, and called that lawful. It found no evidence that the services targeted a journalist whose phone had also been attacked.','C'),
 ('Jun 2025','Researchers at Citizen Lab then confirmed with high confidence that two journalists, one of them Italian, were hit with the same spyware. Paragon ended its contracts with Italy on 9 June, saying Italy refused a check that would have settled who targeted the journalist; Italy disputes that account.','CS')],
 'Here the state itself used spyware on its critics, and nobody has said who targeted the journalists.','Hier gebruikte de staat zelf spyware tegen zijn critici, en niemand heeft gezegd wie de journalisten viseerde.'),
'Netherlands':([('Oct 2025','Before the election of 29 October a newspaper revealed that two members of parliament of the PVV party secretly ran a Facebook page posting hundreds of AI-made images of an opposition leader; the page had 74 million views between June and October. The party leader apologised; the opposition filed a police complaint.','C'),
 ('After the vote','An election observatory found significant digital manipulation, including new AI threats and failing moderation by platforms, and concluded the election was "tested, but fundamentally free and fair".','C')],
 'The fake images came from sitting members of parliament, not from abroad.','De nepbeelden kwamen van zetelende parlementsleden, niet uit het buitenland.'),
'Norway':([('Sep 2025','Parliamentary election. Websites were knocked offline; the security service linked an attack on the website of the Conservative Party to a pro-Russian hacker group. The Swedish psychological-defence agency concludes the attempts had no effect.','CK')],
 'Attempts, no effect.','Pogingen, geen effect.'),
'Poland':([('Apr 2025','Prime Minister Tusk said attackers tried for about twelve hours to take over computers of his party\'s office and campaign staff, and spoke of foreign interference from "the east".','CK'),
 ('14–16 May 2025','Days before the first round of the presidential election the state research institute NASK found political adverts on Facebook that may have been paid from abroad and that outspent every campaign committee in a week; Meta blocked them. On 16 May Tusk said Russian hackers on Telegram had knocked party websites offline.','CK'),
 ('Jan–Jun 2025','NASK tracked more than 10,000 accounts spreading disinformation; the ministry called the Russian attempts unprecedented. Independent experts found the interference lower than expected, and international observers praised the countermeasures.','C')],
 'A government that shouted early, and observers who say the defence worked.','Een regering die vroeg alarm sloeg, en waarnemers die zeggen dat de verdediging werkte.'),
'Portugal':([('May 2025','During the snap election a false story, dressed up as a CNN report, said Russian state groups had carried out a cyberattack. CNN Portugal denied it. Fact-checkers say much of the false content matched known Russian operations.','CS')],
 'A fake about an attack that did not happen.','Een vervalsing over een aanval die niet gebeurde.'),
'Romania':([('Dec 2024','Background: the constitutional court annulled the first round of the presidential election, citing manipulation of opinion by a foreign state. Moscow denies it.','C'),
 ('4 May 2025','First round of the rerun. Pro-Russian hackers claimed attacks on government websites, among them the interior and justice ministries.','CK'),
 ('18–19 May 2025','Run-off, won by the centrist Nicușor Dan. Telegram\'s founder Pavel Durov sent every Romanian user a message alleging that France had asked him to silence conservative voices; France denies it. Romanian ministries accused Russia of interfering in the run-off.','CK'),
 ('2025–2026','The European Commission\'s investigation into TikTok\'s handling of election risks was still running months later.','C'),
 ('Nov 2026','The candidate barred from the rerun, Călin Georgescu, is on trial in two cases (an attempt against the constitutional order; promoting fascist leaders), has been in pre-trial detention since 29 September and was indicted on 12 November for a €1.1 million fraud.','CS')],
 'The only annulled national election in the EU; the proof of who steered it has still not been tested in court.','De enige vernietigde nationale verkiezing in de EU; het bewijs van wie ze stuurde is nog altijd niet voor de rechter getoetst.'),
'Sweden':([('Sep 2026','Parliamentary election. The pro-Russian "Matryoshka" network spread false claims of election fraud and fabricated videos against the prime minister. The psychological-defence agency said Sweden was not a priority target for Russia; the security service still ranks Russia first for interference. Voting is on paper.','CK')],
 'Fakes about fraud, aimed at trust in the count.','Vervalsingen over fraude, gericht op het vertrouwen in de telling.'),
}
NONE=['Austria','Croatia','Estonia','Finland','Greece','Iceland','Ireland','Latvia','Liechtenstein','Lithuania','Luxembourg','Malta','Slovakia','Slovenia','Spain','Switzerland']
assert len(D)+len(NONE)==30
def card(n):
    ev,se,sn=D[n]
    return '<div class="country" id="d-%s"><h4>%s <small>%d on record</small></h4><ul>%s</ul><p class="pl"><b>What it shows:</b> %s<span class="plnl"><b>NL – Wat het toont:</b> %s</span></p></div>'%(n,n,len(ev),''.join('<li><b>%s:</b> %s%s</li>'%(d,t,tg(s)) for d,t,s in ev),se,sn)
nev=sum(len(D[n][0]) for n in D)
SEC='''<section id="electionseu">
<h2>Elections and democracy: the other 30 countries</h2>
<p class="sub">Interference with elections and with the people in politics, in the other 26 EU countries plus Norway, Iceland, Switzerland and Liechtenstein, 2025 and 2026. %d events in %d countries.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>About a dozen national elections were held in these two years, and in none of them was the counting or the voting itself attacked; most of Europe votes on paper. What was attacked is the talk around the vote. The same two Russian operations, known as Storm-1516 and Matryoshka, turn up in Germany, France, Hungary and Sweden with fake videos about ballot fraud. Party websites were knocked offline in Poland and Norway. But the reports also show three less comfortable things: observers usually found no effect on the result, a good part of the fakes came from inside the country, and in Italy the spyware on critics' phones was the state's own.</p>
<p class="pb-nl"><b>NL:</b> In deze twee jaar werden een twaalftal nationale verkiezingen gehouden, en bij geen enkele werd het tellen of het stemmen zelf aangevallen; het grootste deel van Europa stemt op papier. Wat aangevallen werd, is het gesprek rond de stembusgang. Dezelfde twee Russische operaties, bekend als Storm-1516 en Matrjosjka, duiken op in Duitsland, Frankrijk, Hongarije en Zweden met nepvideo's over stembusfraude. Partijwebsites werden platgelegd in Polen en Noorwegen. Maar de rapporten tonen ook drie minder comfortabele dingen: waarnemers vonden meestal geen effect op de uitslag, een flink deel van de vervalsingen kwam van binnen het land, en in Italië was de spyware op de telefoons van critici van de staat zelf.</p></div>
<div class="warnbox"><b>Labels.</b> <span class="tag t-conf">Confirmed</span> stated by an authority, a court, observers or named researchers. <span class="tag t-rep">Reported</span> in the press, not verified. <span class="tag t-susp">Suspected</span> believed, not proven. <span class="tag t-claim">Claimed</span> said by one party (a government, a minister, a platform owner) without evidence shown in public. <span class="tag t-none">Not proven</span> looked for and not found. Two labels on one line: the first is for the event, the second for who was behind it or whether it had effect.</div>
<h3>The elections of 2025–2026, at a glance</h3>
<table><thead><tr><th>Election</th><th>What was seen</th><th>Who was blamed, and how firmly</th><th>Effect on the result</th></tr></thead><tbody>
<tr><td><b>Germany</b>, Feb 2025</td><td>Fake videos about ballot fraud; 700+ fake accounts</td><td>Russia (Storm-1516): formal statement by the government, Dec 2025</td><td>None reported</td></tr>
<tr><td><b>Romania</b>, May 2025 (rerun)</td><td>Government websites attacked; a message from Telegram's owner to all users</td><td>Russia (ministries); France (Telegram's owner, denied)</td><td>The rerun stood; the 2024 round had been annulled</td></tr>
<tr><td><b>Poland</b>, May–Jun 2025</td><td>Party computers and websites attacked; adverts paid from abroad</td><td>Russia: the prime minister's statement</td><td>Observers: defence worked</td></tr>
<tr><td><b>Portugal</b>, May 2025</td><td>A fake report about a cyberattack</td><td>Matches known Russian operations (fact-checkers)</td><td>None reported</td></tr>
<tr><td><b>Norway</b>, Sep 2025</td><td>Websites knocked offline, a party site among them</td><td>A pro-Russian group (security service)</td><td>None</td></tr>
<tr><td><b>Czechia</b>, Oct 2025</td><td>Hundreds of fake TikTok accounts</td><td>Russia-linked networks (researchers); not shown for the TikTok network</td><td>None found</td></tr>
<tr><td><b>Netherlands</b>, Oct 2025</td><td>AI-made images of an opposition leader, 74 million views</td><td>Two members of parliament of a Dutch party</td><td>"Tested, but free and fair"</td></tr>
<tr><td><b>France</b>, Mar 2026 (municipal)</td><td>A fake website against a Paris candidate; AI content farms</td><td>Russia (Storm-1516), probably, says the state agency</td><td>Small reach</td></tr>
<tr><td><b>Hungary</b>, Apr 2026</td><td>Fake videos; fake news sites; a reported theft from a party app</td><td>Russia for the fakes (researchers); most disinformation domestic</td><td>The opposition won</td></tr>
<tr><td><b>Sweden</b>, Sep 2026</td><td>False claims of election fraud</td><td>The pro-Russian Matryoshka network</td><td>Not a priority target, says the agency</td></tr>
</tbody></table>
<p class="small">Denmark, Latvia, Slovenia, Cyprus, Bulgaria and Ireland also voted or will vote in this period; for them nothing specific about an attack on the election was found, beyond what is on the country cards.</p>
<h3>Statements and measures at EU level</h3>
<ul>
<li><b>15 Dec 2025:</b> the EU put sanctions on John Mark Dougan, an American in Moscow, for running a network of fake news sites and supporting Storm-1516. <span class="tag t-conf">Confirmed</span></li>
<li><b>Who runs Storm-1516:</b> European and US authorities attribute it to a Moscow "centre for geopolitical expertise" and to Russian military intelligence; leaked documents reported in 2026 point the same way and also to the Russian presidential administration. <span class="tag t-conf">Confirmed</span> <span class="tag t-claim">Claimed</span></li>
<li><b>Mar 2026:</b> the EU's diplomatic service warned in its yearly report that the elections in Slovenia, Hungary, Bulgaria, Cyprus, Estonia, Sweden, Latvia and Denmark could face the same patterns. <span class="tag t-conf">Confirmed</span></li>
</ul>
<h3>Countries with something on record</h3>
<div class="countries">%s</div>
<h3>Nothing specific found</h3>
<p>%s.</p>
<p class="small">Nothing found means nothing came up in searches on 15 November 2026. Spyware cases in Greece and Spain date from before 2025; the infection of a Greek former member of the European Parliament is on the Belgium page, because it concerns the Parliament.</p>
<p class="pl"><b>What it shows:</b> Nobody hacked a ballot box. The attacks are on belief: fake videos saying the count is rigged, fake reports of attacks that never happened. Three lessons stand out from the countries that handled it best. Vote on paper. Tell the public quickly and plainly what you see, including when it is small, as France now does every week. And look at home as well as abroad: in the Netherlands and Hungary, and with Italy's spyware, the source was domestic.<span class="plnl"><b>NL – Wat het toont:</b> Niemand hackte een stembus. De aanvallen richten zich op het geloof: nepvideo's die zeggen dat de telling vervalst is, nepberichten over aanvallen die nooit gebeurden. Drie lessen vallen op bij de landen die het best reageerden. Stem op papier. Vertel het publiek snel en duidelijk wat je ziet, ook wanneer het klein is, zoals Frankrijk nu elke week doet. En kijk in eigen land evengoed als in het buitenland: in Nederland en Hongarije, en bij de Italiaanse spyware, lag de bron binnenlands.</span></p>
<p class="src">Sources: see the linked list below.</p>
</section>'''%(nev,len(D),''.join(card(n) for n in sorted(D)),', '.join(NONE))
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='electionseu')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
w=R.find('section',id='elections'); p=w.find('p',class_='sub'); p.string=p.get_text().replace('The other countries follow.','The other 30 countries have their own page.')
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'electionseu'" not in t:
    a="'src': ('R', 'elections')}, "; assert a in t
    t=t.replace(a,a+"{'k': 'electionseu', 'en': 'Elections and democracy: 30 countries', 'nl': 'Verkiezingen en democratie: 30 landen', 'src': ('R', 'electionseu')}, ",1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['electionseu']" not in t:
    t+='''
INTRO['electionseu']=("The elections of 2025 and 2026 in the other 30 countries: what was faked or attacked, who was blamed, and whether it changed anything.","De verkiezingen van 2025 en 2026 in de andere 30 landen: wat vervalst of aangevallen werd, wie de schuld kreeg, en of het iets veranderde.")
'''
    open(l,'w',encoding='utf-8').write(t)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '#p-electionseu td' not in t:
    t=t.replace('</style>','@media(max-width:699px){#p-electionseu td,#p-electionseu th{overflow-wrap:anywhere;padding-left:3px;padding-right:3px;font-size:11.5px}#p-electionseu table{table-layout:fixed;width:100%}}\n</style>',1)
    open(a,'w',encoding='utf-8').write(t)
print('elections2 ok',nev,len(D))
