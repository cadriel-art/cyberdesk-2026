from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
T={'C':('Confirmed','t-conf'),'R':('Reported','t-rep'),'K':('Claimed','t-claim'),'S':('Suspected','t-susp'),'N':('Not proven','t-none')}
def tg(s): return ''.join(' <span class="tag %s">%s</span>'%(T[x][1],T[x][0]) for x in s)
NONE='Nothing specific found in public sources for 2025–2026. That is not proof that nothing happened.'
# country: (events[(date,text,status)], shows_en, shows_nl)
D={
'Austria':([('20 May 2026','A Vienna court convicted former intelligence officer Egisto Ott of spying for Russia: four years and one month. He passed information to Russian services and to the fugitive Jan Marsalek, including a secure government laptop for €20,000. He has appealed.','C')],
 'The Austrian problem is spying from the inside, not drones.','Het Oostenrijkse probleem is spionage van binnenuit, niet drones.'),
'Bulgaria':([('10 Aug 2026','Explosion and fire at an ammunition warehouse of the arms maker EMCO, which supplies Ukraine. The interior minister first pointed away from outside causes.','C'),
 ('Aug 2026','A drone exploded near the Trans-Balkan gas pipeline. One source; no official finding.','R'),
 ('12 Sep 2026','A second fire at another EMCO depot near Tsareva Livada, 33 days later. Nobody hurt. The minister said sabotage is one of the lines of inquiry and ordered every ammunition depot inspected.','CS'),
 ('Autumn 2026','The state news agency reported that prosecutors see a link between four ammunition-warehouse blasts and suspect Russia. Russia rejects this.','S'),
 ('Oct 2026','Drones hit two commercial ships in Bulgaria\'s economic zone at sea, a first. On 13 October the HS Dignity was struck; 11 sailors missing, five survivors (Bloomberg). The prime minister summoned the Russian ambassador; Bulgaria has not formally blamed Russia.','CS')],
 'Arms depots that supply Ukraine keep burning, and the war at sea has reached Bulgarian waters.','Wapendepots die Oekraïne bevoorraden blijven branden, en de oorlog op zee heeft de Bulgaarse wateren bereikt.'),
'Croatia':([('Aug 2026','One news round-up mentions an arson investigation near Omiš taking a terrorism angle. Not confirmed in a primary source.','R')],
 'Nothing solid on record.','Niets hards bekend.'),
'Cyprus':([('Early Mar 2026','Drones hit the British base RAF Akrotiri on the island, damaging a hangar. Cypriot officials said they were launched from Lebanon, probably by Hezbollah, during the Iran war. Not a Russian case. Greece and France sent jets, frigates and anti-drone systems.','CS')],
 'Cypriot officials say the drones came from Lebanon, probably launched by Hezbollah, not from Russia.','Cypriotische autoriteiten zeggen dat de drones uit Libanon kwamen, waarschijnlijk gelanceerd door Hezbollah, en niet uit Rusland.'),
'Czechia':([('2025','A Prague court sentenced a Colombian man to eight years for an arson attack and for planning another; the case is believed to be possibly linked to Russia.','CS'),
 ('20 Mar 2026','Arson at a warehouse of the defence firm LPP Holding in Pardubice. Suspects were held in Czechia, Slovakia and later Bulgaria on terrorism charges. A group claimed it over the firm\'s Israeli ties; Czech intelligence asked publicly whether Russia used that group as cover.','CS'),
 ('Nov 2026','Prague airport was among the worst hit by the Europe-wide hoax bomb threats: nine flights on one day.','R')],
 'An arms factory burned, and nobody can yet say for whom.','Een wapenfabriek brandde, en niemand kan al zeggen in wiens opdracht.'),
'Denmark':([('22–23 Sep 2025','Copenhagen Airport closed for about four hours after reports of two or three large drones; at least 35 incoming flights were diverted. Police did not shoot, because of the fuel depots and the full aircraft nearby. On 23 September Prime Minister Mette Frederiksen called it "the most serious attack on Danish critical infrastructure to date" and said she could not rule out Russia. Nobody was named.','CS'),
 ('24 Sep – 2 Oct 2025','61 reports of drones over Aalborg and military sites in Jutland.','R'),
 ('2026','The police district reviewed those 61 reports: no evidence of illegal drone flights that concern security. It withdrew its earlier word "verified".','CN'),
 ('25 Jun 2026','Police closed the nine-month Copenhagen investigation: no evidence that the flying objects were drones, although drone activity "cannot be ruled out". No suspects.','CN'),
 ('20 Nov 2026','Denmark\'s security service PET said Russian intelligence services planned and initiated a plot to kill the Ukrainian rapper Kyivstoner in Denmark. Two Danish men with links to the banned gang Loyal to Familia are charged and in custody; they were reportedly arrested in September with weapons in their car in Hellerup, shortly before his concert on 25 September, and reportedly plead not guilty. Foreign Minister Lars Løkke Rasmussen said Russia\'s defence attaché must leave Denmark within seven days. No evidence of the Russian role has been published; the report found does not give a Russian response.','CK')],
 'The case that started Europe\'s drone alarm ended with no proof of a single drone.','De zaak die het Europese dronealarm startte, eindigde zonder bewijs van één drone.'),
'Estonia':([('Jan 2025','Arson at a supermarket in Osula and later at a Ukrainian restaurant in Tallinn. A court sentenced a man to six and a half years and said it was ordered by Russian military intelligence. Date of the verdict not found.','C'),
 ('31 Dec 2025','The cargo ship Fitburg dragged its anchor about 130 km and damaged cables, partly in Estonia\'s zone. See Finland for the verdict.','C'),
 ('Aug 2026','Arson at a Tallinn building used by Milrem Robotics, which makes military robots. Three Latvian suspects were detained in Latvia and handed over.','C'),
 ('29 Sep 2026','The Estonian government and its security service formally said the Milrem arson was "commissioned by Russian security services". The Kremlin denies it.','CK'),
 ('14 Nov 2026','An attempt to blow up and set fire to the building of the drone maker Threod Systems was stopped at 3:06 at night. Eight Latvian citizens were detained, and prosecutors asked a court to keep five in custody. The security service KAPO said the attack was ordered by Russian military intelligence; it has published no evidence. It is the second attack on an Estonian defence firm in three months. The prime minister asked for the necessary steps to close the border with Russia; see 15 November for the announcement and what is not yet decided.','CK'),
 ('15 Nov 2026','Foreign minister Margus Tsahkna said Estonia would close all road border crossings with Russia from 1 December (the Narva freight rail crossing stays open for now). He says Estonia has clear evidence that Russian military intelligence (GRU) ordered the attempted arson of 14 November at Threod Systems; no evidence has been published. The Foreign Ministry later clarified that the road crossings (Narva, Luhamaa, Koidula) close on 1 December. Interior minister Igor Taro said, per Interfax, that the freight rail crossing at Narva stays open for now. The government has yet to formally decide the scope and duration. Russia denies it: Kremlin spokesman Peskov called the accusation baseless. Suspects have been detained.','R'),
 ('21 Nov 2026','The Estonian Defence Forces issued, then lifted, a possible drone-threat alert for Lääne-Viru and Ida-Viru counties through the public EE-ALARM system (alert at 4:42, all clear at 6:49). NATO fighter jets, Turkish Air Force aircraft, were airborne in response. One ERR reader reported hearing a drone at 6:13; no drone is confirmed over Estonia in the report. At the same time the governor of Russia\'s Leningrad Oblast said air defences had downed drones (the number he gave rose from six to 93), and Finland restricted air and sea traffic in the eastern Gulf of Finland. ERR says a similar alert on 11 November came as Ukrainian drones struck the Russian port of Ust-Luga.','CR')],
 'Estonia names Russia quickly and takes cases to court.','Estland wijst Rusland snel aan en brengt zaken voor de rechter.'),
'Finland':([('3 Oct 2025','Eagle S (cables cut in December 2024): the Helsinki court dismissed the case, saying Finland had no jurisdiction.','C'),
 ('31 Dec 2025','The Fitburg damaged undersea cables between Finland and Estonia.','C'),
 ('Aug 2026','The appeal court reversed the Eagle S ruling: Finland does have jurisdiction, because the damage was felt there. The case goes back to the lower court; the three accused have left the country.','C'),
 ('5 Nov 2026','Fitburg: the Russian captain got three and a half years and an Azerbaijani crew member two years and ten months for aggravated sabotage. The court found they acted on purpose. The captain will appeal. The reports found do not say who, if anyone, ordered it.','C'),
 ('21 Nov 2026','The Russian dry-cargo ship Sparta II caught fire in the Gulf of Finland after what Russian officials called a strike by two drones. Finland\'s Ministry of Defence said the attack took place in international waters and that Finland notified its allies; the Finnish Border Guard said the burning ship drifted into Finnish territorial waters, that it leads rescue and oil-spill preparation, and that other shipping is not in danger. Prime Minister Petteri Orpo wrote that a drone strike hit a Russian merchant vessel and that Ukraine has the right to fight back; Finland\'s Defence Forces twice restricted sea and air traffic in the gulf as a precaution against stray drones. Who launched the drones has not been officially confirmed. As background, ERR notes that Ukrainian military intelligence classes the ship as having carried weapons and that it is on the US sanctions list. No pollution had been reported at the time (ERR News, citing Yle).','CR')],
 'The first prison sentences in Europe for cutting sea cables.','De eerste gevangenisstraffen in Europa voor het doorsnijden van zeekabels.'),
'France':([('9 Sep 2025','Nine pig heads were left outside mosques around Paris. Three Serbs were later convicted in Serbia (house arrest) for acts in France and Germany; Serbia\'s interior ministry said the group was trained by a man acting for a foreign intelligence service. No state was named by a court.','CS'),
 ('2025','Four Russian men were arrested on suspicion of plotting to kill the Russian dissident Vladimir Osechkin, who lives in France.','CS'),
 ('Feb 2026','A research count (ICCT/GLOBSEC) puts France second in Europe with 20 Russia-linked incidents since 2022.','K'),
 ('Jun 2026','French investigators were reported to be working on several suspected Russia-linked cases, among them railway infrastructure and a Belarus-born man held near Toulouse after filming a military drone prototype.','R'),
 ('11–12 Oct 2026','Freezer controls at more than 700 supermarket sites were attacked (a cyber case, listed here because of who is blamed). French authorities suspect Iran\'s Revolutionary Guard; Paris prosecutors opened a judicial investigation and requested international arrest warrants. Pro-Russian groups also claimed it.','CK'),
 ('Nov 2026','Paris prosecutors are examining whether foreign powers are behind the hoax bomb threats against flights.','C')],
 'In France the tool is provocation meant to divide people, as much as sabotage.','In Frankrijk is het wapen provocatie om mensen tegen elkaar op te zetten, evenzeer als sabotage.'),
'Germany':([('2–3 Oct 2025','Munich Airport closed twice in 24 hours after drone reports.','CS'),
 ('2025','The federal police chief counted more than 1,000 suspicious drone flights. One Frankfurt shutdown turned out to be a 41-year-old hobby pilot testing a new drone.','C'),
 ('Jul 2026','Fire on the rail line between Düsseldorf and Cologne damaged signal cables; investigated as possible sabotage. No link to any state found.','S'),
 ('4 Aug 2026','Leipzig/Halle Airport: a drone carrying explosives was found near a Ukrainian Antonov cargo plane; the charge did not go off. Three drones were found in all. Reports differ on details.','C'),
 ('11 Aug 2026','A drone forced repeated closures at Hanover Airport; federal police could not stop it with their equipment (Der Spiegel).','R'),
 ('1 Sep 2026','The German government formally blamed Russia for the Leipzig attack ("police investigations, patterns of the act and intelligence findings") and ordered the Russian consulate general in Bonn closed. Russia called it absurd. No arrests found.','CK'),
 ('Sep 2026','A confidential police report, cited by Süddeutsche Zeitung, counts more than 165 suspected acts of sabotage and nearly 750 suspicious drone incidents since January 2026.','R'),
 ('28 Oct 2026','Two Belarusian men were arrested in southern Germany, suspected of planning fires near a railway line and a power line for Russia. Romania links them to the Brașov fire.','CS')],
 'The first case in the EU where a government formally blamed Russia for a drone with explosives at an airport.','De eerste zaak in de EU waarin een regering Rusland formeel de schuld gaf van een drone met explosieven op een luchthaven.'),
'Greece':([],'Greece appears as a helper (jets and frigates for Cyprus in March 2026), not as a target.','Griekenland duikt op als helper (jets en fregatten voor Cyprus in maart 2026), niet als doelwit.'),
'Hungary':([('Sep 2026','After the Leipzig case the new government called Russian hybrid activity a serious threat. One outlet notes that no sabotage incidents have been recorded in Hungary; not checked against official data.','R')],
 'No incidents on record.','Geen incidenten bekend.'),
'Iceland':([],'','' ),
'Ireland':([('1 Dec 2025','Four or five military-style drones appeared near Dublin Airport shortly after President Zelensky\'s plane landed. The prime minister called it "suggestive" of a Russian-inspired hybrid campaign; the Russian embassy called that baseless. Police are still looking at whether they took off from land or from a ship; no evidence against three sanctioned ships nearby. The navy had no means to stop them.','CS')],
 'Three-quarters of the main transatlantic cables pass near a country with almost no means to guard them.','Driekwart van de belangrijkste trans-Atlantische kabels loopt langs een land dat ze nauwelijks kan bewaken.'),
'Italy':([('7 Feb 2026','On the first full day of the Winter Olympics, cables were cut near Bologna, a crude explosive device was found by a track and a switch burned near Pesaro; delays of up to two and a half hours. Nobody claimed it; investigators looked at anarchist groups. No state link reported.','CS'),
 ('28 Apr 2026','Two people were convicted at first instance for mapping ports and barracks for Russia.','C'),
 ('7 Jul 2026','Two former intelligence agents were arrested in Rome for selling classified information to a Russian agent with diplomatic cover; five others, four of them soldiers, are under investigation.','CS'),
 ('Nov 2026','More than 6,000 schools received threats in the week of the hoax bomb threats against flights. One source; nobody named.','R')],
 'Italy\'s confirmed cases are about spies; its sabotage case points at home-grown extremists.','De bevestigde Italiaanse zaken gaan over spionnen; de sabotagezaak wijst naar binnenlandse extremisten.'),
'Latvia':([('Jan 2025','A data cable between Latvia and Gotland was damaged. See Sweden: prosecutors found it was not sabotage.','CN'),
 ('Oct 2025 – Jan 2026','Four arson attacks on railway sites in Riga. Two people received prison sentences in September 2026 for acting on Russia\'s behalf.','C'),
 ('Mar 2026','A drone came down in the Krāslava district; identified as Ukrainian, flying in from Russia.','C'),
 ('7 May 2026','Two drones crashed in Latvia; one set an oil depot in Rēzekne on fire. The army identified them as Ukrainian drones aimed at Russia that strayed. The defence minister was dismissed and the government fell within a week.','C'),
 ('30 Jun 2026','A Riga court sentenced an electrician to five and a half years for spying for Russian military intelligence.','C')],
 'The drones that brought down a government were a friend\'s, not an enemy\'s.','De drones die een regering deden vallen, waren van een bondgenoot, niet van een vijand.'),
'Liechtenstein':([],'',''),
'Lithuania':([('Since Oct 2025','Balloons carrying smuggled cigarettes from Belarus have closed Vilnius Airport again and again: more than 20 times by one count. Lithuania closed the border from 29 October to 19 November 2025 and declared a state of emergency on 9 December 2025. It blames Belarus for letting it happen and calls it a hybrid attack.','CK'),
 ('24 Nov 2025','A Vilnius court sentenced a young Ukrainian to three years and four months for the 2024 arson at IKEA and an attempted attack in Šiauliai, carried out for Russian military intelligence.','C'),
 ('15 Sep 2026','Italian jets on NATO air policing shot down a drone near Pratkūnai. Officials said it most likely came from Belarus and was likely carrying explosives.','CS'),
 ('21–22 Sep 2026','Vilnius Airport closed again for more than three hours because of balloons.','C')],
 'Cheap balloons can close a capital\'s airport twenty times.','Goedkope ballonnen kunnen de luchthaven van een hoofdstad twintig keer sluiten.'),
'Luxembourg':([('18 Sep 2026','Findel airport closed for just over three hours after unidentified drones were seen: 19 aircraft diverted, more than 1,800 passengers affected (government statement).','CS'),
 ('20 or 21 Sep 2026','A second closure of about 52 minutes; sources differ on the day. No operator, motive or state link identified; investigation open, no suspects.','CS'),
 ('Oct–Nov 2026','The freezer attacks also hit Luxembourg. France blames Iran for its own wave; no finding for Luxembourg found.','S')],
 'Europe\'s main air-cargo hub was stopped twice in days, and nobody knows by whom.','Een van Europa\'s grootste vrachtluchthavens lag twee keer stil in enkele dagen, en niemand weet door wie.'),
'Malta':([],'',''),
'Netherlands':([('Nov–Dec 2025','Drones were reported over Volkel air base and Eindhoven; soldiers fired at them, and Eindhoven Airport stopped traffic on 22 November. A research institute counted nine incidents.','CS'),
 ('26 Jan 2026','The investigation produced no suspects and no recovered drone.','CN'),
 ('Jul 2026','A British think tank (IISS) said the drones were probably launched from ships of the Russian "shadow fleet". Dutch authorities have not named anyone; Russia denies it.','K')],
 'Shots were fired at drones nobody has found.','Er werd geschoten op drones die niemand heeft teruggevonden.'),
'Norway':([('Late Sep 2025','Oslo Airport was disrupted by drone reports. Police found no evidence of the drones.','CN'),
 ('2025','The security service PST: not one case in 2025 of a drone flown by a foreign power; many reports were not drones at all.','CN'),
 ('12 Nov 2026','PST raised its warning: it expects Russian intelligence to try sabotage in Norway in the coming year, most likely against defence firms. It has found no sabotage attempts so far, but Russia-linked actors have mapped targets.','C')],
 'No proven drone, but an official warning that sabotage is expected.','Geen bewezen drone, maar een officiële waarschuwing dat sabotage verwacht wordt.'),
'Poland':([('9–10 Sep 2025','About 19 drones crossed into Poland during a Russian attack on Ukraine; three or four were shot down, the first time a NATO member fired in this war. A house in Wyryki-Wola was destroyed by debris; nobody hurt. Poland invoked NATO\'s Article 4. Moscow denied responsibility.','C'),
 ('Oct 2025','Eight people detained over suspected Russia-linked sabotage. At least 44 had been detained for spying or sabotage since 2022 (count of August 2025).','C'),
 ('15–17 Nov 2025','An explosive device damaged the Warsaw–Lublin railway near Mika; the next day a train with 475 passengers braked hard near Puławy. Nobody hurt. The government called both sabotage by Russian intelligence. Two Ukrainian suspects fled to Belarus.','CK'),
 ('Dec 2025','A Russian man was charged with directing a sabotage ring from the Moscow region.','C'),
 ('Feb 2026','A research count (ICCT/GLOBSEC) puts Poland first in Europe: 31 of 151 Russia-linked incidents since 2022.','K'),
 ('10 Nov 2026','Two Ukrainian men were detained for photographing infrastructure and military sites and for car arson, paid partly in cryptocurrency.','CS'),
 ('12 Nov 2026','A third man was indicted for helping prepare the Mika attack; the sabotage charge carries ten years to life. No conviction yet.','C'),
 ('18–20 Nov 2026','Poland says it prevented a planned Russian "false-flag" provocation on the border with the Kaliningrad exclave around the turn of October and November. The newspaper Rzeczpospolita reported it on 18 November, citing unnamed senior officials. Prime Minister Tusk had said on 3 November that Poland "managed to prevent a provocation" after "individuals with flashlights" were seen; the defence minister and a retired general who advises him have since said something was prevented. The adviser, Mieczysław Bieniek, gave as an example people crossing the border in Ukrainian or Polish uniforms to stage an attack. Officials gave no further details and no evidence has been published; the report found does not give a Russian response.','K'),
 ('19 Nov 2026','Two Ukrainians were charged over "Slava UPA" graffiti on three monuments in Poznań in early November. Prosecutors say Nikita S., "acting on behalf of Russian intelligence" for $500, persuaded Dmytro Y. to paint the slogans to incite hatred between Poles and Ukrainians. Similar graffiti appeared in Gdańsk, Gdynia and Warsaw; a 17-year-old Ukrainian was held and charged over Gdańsk and Gdynia. The outlet MOST reported a Telegram advert offering $500 for such work. The Russian-intelligence link is the prosecutors\' charge; no court has tested it.','CK'),
 ('20 Nov 2026','Defence minister Kosiniak-Kamysz confirmed that two Russian missiles and what is probably a jet-powered drone came down in south-eastern Poland during one of the largest Russian attacks on Ukraine: a Kh-101 cruise missile at Nowy Lipowiec, another missile at Rudnik nad Sanem and the probable drone at Mołodycz. No injuries or damage to critical infrastructure were reported. Prime Minister Tusk said there was no doubt the objects were Russian and that it "does seem" an intentional provocation. NATO jets were scrambled; Secretary General Rutte spoke of "grave violations of Polish airspace".','CK')],
 'The most targeted country in Europe, with the longest list of arrests.','Het meest geviseerde land van Europa, met de langste lijst arrestaties.'),
'Portugal':([('28 Apr 2025','The Iberian blackout hit Portugal too. Officials found no sign of a cyberattack or sabotage.','CN')],
 'Nothing else on record.','Verder niets bekend.'),
'Romania':([('Sep 2025','A drone entered Romanian airspace during a Russian attack on Ukraine; fragments have fallen on Romanian soil repeatedly since 2022.','C'),
 ('May 2026','A Russian drone reportedly hit an apartment building in Galați, injuring two. One source.','R'),
 ('14 Sep 2026','Fire at the Carfil industrial site in Brașov, next to a state arms maker; the arms production itself was not damaged.','C'),
 ('Oct 2026','Drones struck commercial ships off Romania. A grain ship sank on 5 October about 30 nautical miles out, two crew killed. The Khoryv sank on 23 October off Constanța, one dead and three missing; the president said a Russian drone did it. Bloomberg counts seven ships hit off Romania and Bulgaria and more than two dozen sailors killed, the first deaths from drones inside EU waters.','CK'),
 ('26 Oct 2026','The intelligence service said a Russia-coordinated network was behind the Brașov fire. Three suspects (two Belarusians, one Ukrainian) are under investigation; reports differ on whether they are in custody. Russia denies it.','CK')],
 'The first deaths: sailors killed by drones in EU waters.','De eerste doden: zeelieden gedood door drones in EU-wateren.'),
'Slovakia':([('Aug 2026','Police said they foiled an arson attack on the Skyeton drone factory near Prešov: two suspects held in Slovakia, one in Germany. A Latvian suspect said he was hired through Telegram by a Russian speaker. The Russian embassy denied any role.','CS'),
 ('Sep 2026','German investigators were reported to link the Skyeton plot, an arson in Munich and the Leipzig drone to Russian military intelligence, with part of the network working from Slovakia. Media reports, not a charge.','R')],
 'A plot stopped before the fire.','Een complot dat gestopt werd vóór de brand.'),
'Slovenia':([],'',''),
'Spain':([('28 Apr 2025','The Iberian blackout: officials and a later report found no cyberattack.','CN'),
 ('May 2025','Copper cable was stolen at five points on the Madrid–Seville high-speed line, stopping trains. The transport minister called it "serious sabotage". No link to any state found.','CS'),
 ('Jul 2025','Spain led a Europol operation against a network that recruited saboteurs remotely; two central figures live in Russia.','C'),
 ('Nov 2026','The foreign minister called the hoax bomb threats most likely "an attempt at hybrid aggression". Nobody has been named.','K')],
 'Not every stopped train is sabotage; copper thieves do it too.','Niet elke stilstaande trein is sabotage; koperdieven doen het ook.'),
'Sweden':([('26 Jan 2025','A data cable between Latvia and Gotland was damaged; Sweden seized the ship Vezhen on suspicion of sabotage. Prosecutors then concluded it was weather, poor equipment and poor seamanship: not sabotage.','CN'),
 ('Sep 2025','Drones were reported over the Karlskrona archipelago, near the main naval base. Police said it was unclear what the object was.','R'),
 ('Nov 2025','Gothenburg-Landvetter Airport stopped traffic after drone reports; police opened an investigation for aviation sabotage. Outcome not found.','CS'),
 ('21 Nov 2026','A newspaper investigation found that a Russian tech firm backed by an oligarch close to President Putin has been collecting data from hundreds of thousands, possibly millions, of Swedes through websites where people accept cookies (France 24). The report says Sweden is particularly exposed because of its open public-records system. The summary found does not say whether the data reached Russian state bodies or whether Swedish authorities will open a formal investigation. The firm is not named here.','R')],
 'The best-known "sabotage" case turned out to be bad seamanship.','De bekendste "sabotagezaak" bleek slecht zeemanschap.'),
'Switzerland':([('Oct 2025','Several drones were reported over strategically important sites in canton Aargau.','R'),
 ('25 Jun 2026','The federal intelligence service: Russia\'s hybrid conflict "is becoming more aggressive and hits Switzerland directly". It identified "disposable agents" with links to Switzerland and says Russia misuses Swiss computer systems for sabotage abroad. No arrests in Switzerland found.','C')],
 'A warning from the intelligence service, without a public case to show.','Een waarschuwing van de inlichtingendienst, zonder publieke zaak om te tonen.'),
}
order=sorted(D)
def card(n):
    ev,se,sn=D[n]
    if not ev and not se:
        body='<p class="small">%s</p>'%NONE
    else:
        body=('<ul>'+''.join('<li><b>%s:</b> %s%s</li>'%(d,t,tg(s)) for d,t,s in ev)+'</ul>') if ev else ''
        body+='<p class="pl"><b>What it shows:</b> %s<span class="plnl"><b>NL – Wat het toont:</b> %s</span></p>'%(se,sn)
    return '<div class="country" id="h-%s"><h4>%s <small>%s</small></h4>%s</div>'%(n.replace(' ','-'),n,('%d on record'%len(ev)) if ev else 'nothing found',body)
nev=sum(len(D[n][0]) for n in D); nwith=sum(1 for n in D if D[n][0])
SEC='''<section id="hybrideu">
<h2>Drones, sabotage and hybrid threats: the other 30 countries</h2>
<p class="sub">The same subject as the Belgium page, for the other 26 EU countries plus Norway, Iceland, Switzerland and Liechtenstein, 2025 and 2026. %d events in %d countries. Counted apart from the cyber register.</p>
<div class="plainbox"><div class="pb-h">In plain words</div>
<p>Two very different stories sit under the same word. The drone sightings over airports mostly fell apart when police looked closely: Denmark, Norway, the Netherlands and Belgium all ended with no proof. The sabotage is the opposite: it is proven in court. Finland jailed a ship's captain for cutting cables, Estonia, Latvia and Lithuania convicted arsonists working for Russian intelligence, Germany formally blamed Russia for a drone with explosives at Leipzig airport, and in October 2026 sailors were killed by drones in EU waters off Romania and Bulgaria.</p>
<p class="pb-nl"><b>NL:</b> Onder hetzelfde woord zitten twee heel verschillende verhalen. De dronewaarnemingen boven luchthavens vielen meestal uiteen toen de politie goed keek: Denemarken, Noorwegen, Nederland en België eindigden allemaal zonder bewijs. De sabotage is het omgekeerde: die is bewezen voor de rechter. Finland veroordeelde een kapitein voor het doorsnijden van kabels, Estland, Letland en Litouwen veroordeelden brandstichters die voor de Russische inlichtingendienst werkten, Duitsland gaf Rusland formeel de schuld van een drone met explosieven op de luchthaven van Leipzig, en in oktober 2026 werden zeelieden gedood door drones in EU-wateren voor Roemenië en Bulgarije.</p></div>
<div class="warnbox"><b>Labels.</b> <span class="tag t-conf">Confirmed</span> stated by an authority, a court or the organisation itself. <span class="tag t-rep">Reported</span> in the press, not verified. <span class="tag t-susp">Suspected</span> believed, not proven. <span class="tag t-claim">Claimed</span> said by one party (a minister, a government, a think tank) without evidence shown in public or tested in court. <span class="tag t-none">Not proven</span> investigated, no evidence found. Two labels on one line: the first is for the event, the second for who or what was behind it. A government blaming Russia is marked Confirmed (it said so) and Claimed (no court has tested it).</div>
<h3>What is proven hardest</h3>
<table><thead><tr><th>Case</th><th>Country</th><th>How firm</th></tr></thead><tbody>
<tr><td>Fitburg cable cutting: captain and crew member jailed (5 Nov 2026)</td><td>Finland / Estonia</td><td>Court verdict; under appeal</td></tr>
<tr><td>IKEA arson for Russian military intelligence: prison (24 Nov 2025)</td><td>Lithuania</td><td>Court verdict, guilty plea</td></tr>
<tr><td>Restaurant and supermarket arson ordered by Russian military intelligence: six and a half years</td><td>Estonia</td><td>Court verdict</td></tr>
<tr><td>Railway arson in Riga for Russia: prison (Sep 2026)</td><td>Latvia</td><td>Court verdict</td></tr>
<tr><td>Former intelligence officer spied for Russia (20 May 2026)</td><td>Austria</td><td>Court verdict; under appeal</td></tr>
<tr><td>Drone with explosives at Leipzig/Halle Airport (4 Aug 2026)</td><td>Germany</td><td>Device found; government formally blames Russia; no trial</td></tr>
<tr><td>Railway explosion near Mika (Nov 2025)</td><td>Poland</td><td>Government blames Russia; indictments; no verdict</td></tr>
<tr><td>Ships sunk by drones, sailors killed (Oct 2026)</td><td>Romania / Bulgaria</td><td>Deaths confirmed; Romania's president blames Russia; no formal finding</td></tr>
</tbody></table>
<h3>What fell apart</h3>
<table><thead><tr><th>Alarm</th><th>Country</th><th>Outcome</th></tr></thead><tbody>
<tr><td>Copenhagen Airport closed by "drones" (Sep 2025)</td><td>Denmark</td><td>Police, June 2026: no evidence they were drones</td></tr>
<tr><td>61 drone reports over Jutland (Sep–Oct 2025)</td><td>Denmark</td><td>No evidence; the word "verified" withdrawn</td></tr>
<tr><td>Drone reports at Oslo Airport and elsewhere (2025)</td><td>Norway</td><td>Security service: no foreign drone found in 2025</td></tr>
<tr><td>Drones over Volkel and Eindhoven (Nov 2025)</td><td>Netherlands</td><td>No suspects, no drone recovered</td></tr>
<tr><td>Cable cut by the ship Vezhen (Jan 2025)</td><td>Sweden / Latvia</td><td>Prosecutors: weather and poor seamanship</td></tr>
<tr><td>Iberian blackout (Apr 2025)</td><td>Spain / Portugal</td><td>No cyberattack or sabotage found</td></tr>
</tbody></table>
<h3>Counts by others</h3>
<ul>
<li><b>151</b> Russia-linked sabotage incidents in Europe from February 2022 to February 2026, of which 41 newly added: Poland 31, France 20, Lithuania 15, Germany 15, Estonia 11 (ICCT/GLOBSEC, a research count, not an official one). <span class="tag t-claim">Claimed</span></li>
<li><b>144</b> suspected drone sightings across Europe, 2024–2026 (IISS, a think tank). <span class="tag t-claim">Claimed</span></li>
<li><b>145</b> sabotage incidents linked to Russia since 2022 (Associated Press count). Other trackers count far more; definitions differ widely. <span class="tag t-claim">Claimed</span></li>
<li>From <b>2 November 2026</b>: hoax bomb threats against dozens of flights and then newsrooms across Europe, including the UK, France, Italy, Spain, Czechia and Belgium. No group or state named; French prosecutors are looking at a foreign link. <span class="tag t-conf">Confirmed</span> <span class="tag t-susp">Suspected</span></li>
</ul>
<h3>Country by country</h3>
<div class="countries">%s</div>
<p class="pl"><b>What it shows:</b> Treat the two halves differently. For drones over airports, the lesson of 2025–2026 is better detection and calmer communication, because most alarms could not be proven. For sabotage, the lesson is the opposite: it is real, it is cheap, it is done by hired hands recruited online, and it has moved from fires in shops to arms factories, railways, sea cables and ships.<span class="plnl"><b>NL – Wat het toont:</b> Behandel de twee helften verschillend. Voor drones boven luchthavens is de les van 2025–2026: betere detectie en rustiger communiceren, want de meeste alarmen konden niet bewezen worden. Voor sabotage is de les omgekeerd: ze is echt, ze is goedkoop, ze wordt uitgevoerd door online geronselde handlangers, en ze is opgeschoven van brandjes in winkels naar wapenfabrieken, spoorwegen, zeekabels en schepen.</span></p>
<h3>Limits of this page</h3>
<ul>
<li>Built from public reporting found by search on 15 November 2026. Some dates and numbers come from a single report and are marked Reported.</li>
<li>Thin or empty countries (Iceland, Liechtenstein, Malta, Slovenia, Croatia, Greece, Hungary, Portugal) may simply be less reported in the sources searched.</li>
<li>Not found: the outcome of the Swedish airport investigations, arrests in the Leipzig case, any verdict in Poland's Mika case, who sent the hoax threats.</li>
</ul>
<p class="src">Sources: Reuters, AP, AFP, Bloomberg, NPR, Defense News, CNN, Al Jazeera, Euronews; national: Finnish Police, Yle, ERR, LRT, Latvian armed forces, Notes from Poland, Polskie Radio, VRT, NL Times, The Local, Irish Times, Irish Examiner, ANSA, Il Post, SRF, BTA, Romania Insider, Paperjam and the Luxembourg government; Dronewatch; ICCT/GLOBSEC; IISS.</p>
</section>'''%(nev,nwith,''.join(card(n) for n in order))
f=M+'cyber-incident-register.html'; R=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
o=R.find('section',id='hybrideu')
if o: o.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(f,'w',encoding='utf-8').write(str(R))
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'hybrideu'" not in t:
    a="'src': ('R', 'hybrid')}, "; assert a in t
    t=t.replace(a,a+"{'k': 'hybrideu', 'en': 'Drones, sabotage, hybrid: 30 countries', 'nl': 'Drones, sabotage, hybride: 30 landen', 'src': ('R', 'hybrideu')}, ",1)
    open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['hybrideu']" not in t:
    t+='''
INTRO['hybrideu']=("The same threats in the other 30 countries: what was proven in court, what a government claims, and what fell apart when police looked closely.","Dezelfde dreigingen in de andere 30 landen: wat voor de rechter bewezen is, wat een regering beweert, en wat uiteenviel toen de politie goed keek.")
'''
    open(l,'w',encoding='utf-8').write(t)
print('hybrid2 ok',nev,nwith,len(order))
