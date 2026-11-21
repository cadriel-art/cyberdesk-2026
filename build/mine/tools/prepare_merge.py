"""One-off merge: prepare/west.json + prepare/northeast.json -> tools/prepare_data.json
Neutral wording (no first-person researcher voice), lead-editor corrections for EU and Belgium,
and a few structured helper fields (bucket, mail, short table strings, dated events) taken ONLY from the verified fields."""
import json,re
S='/home/user/cyberdesk-2026/build/'
L=json.load(open(S+'research/prepare/west.json',encoding='utf-8'))+json.load(open(S+'research/prepare/northeast.json',encoding='utf-8'))
D={x['country']:x for x in L}
R=[ # (country, field, old, new)
('Netherlands','households','as reported in search results','as reported'),
('Luxembourg','water','as reported by search summary of the guide','as reported'),
('France','households','I found no confirmation of a mailing to every household','a mailing to every household was not found in the sources checked'),
('France','news_2025_2026','No newer official push found for 2026 in my searches.','No newer official push for 2026 was found in the sources checked.'),
('France','text','It is a free public guide, not a mailing to every home, as far as I could confirm.','It is a free public guide; a mailing to every home was not found in the sources checked.'),
('Germany','items','(not confirmed in this session)','(not confirmed in the sources checked)'),
('Germany','text','I found no confirmed official update in 2026.','No confirmed official update in 2026 was found in the sources checked.'),
('Germany','text_nl','een bevestigde officiele update in 2026 vond ik niet.','een bevestigde officiële update in 2026 is in de gecontroleerde bronnen niet gevonden.'),
('Austria','text','I found no new 2025-2026 government campaign telling households to stock up.','No new 2025-2026 government campaign telling households to stock up was found in the sources checked.'),
('Austria','text_nl','vond ik niet.','is in de gecontroleerde bronnen niet gevonden.'),
('Switzerland','text','I found no new urgent call in 2025-2026.','No new urgent call in 2025-2026 was found in the sources checked.'),
('Switzerland','text_nl','vond ik niet.','is in de gecontroleerde bronnen niet gevonden.'),
('Liechtenstein','text_nl','een dringende oproep vond ik niet.','een dringende oproep is in de gecontroleerde bronnen niet gevonden.'),
('Italy','text','but I could not open the official page.','but the official page could not be checked.'),
('Italy','text_nl','maar de officiele pagina kon ik niet openen.','maar de officiële pagina kon niet worden nagekeken.'),
('Italy','text_nl','een aparte Italiaanse campagne vond ik niet.','een aparte Italiaanse campagne is in de gecontroleerde bronnen niet gevonden.'),
('Spain','text','I could not confirm either from an official page, and found no new state campaign in 2026.','Neither could be confirmed from an official page, and no new state campaign in 2026 was found in the sources checked.'),
('Spain','text_nl','Ik kon geen van beide op een officiele pagina bevestigen en vond geen nieuwe staatscampagne in 2026.','Geen van beide kon op een officiële pagina worden bevestigd, en een nieuwe staatscampagne in 2026 is in de gecontroleerde bronnen niet gevonden.'),
('Portugal','text','; I could not open the official ANEPC site.','; the official ANEPC site could not be checked.'),
('Portugal','text_nl','de officiele ANEPC-site kon ik niet openen.','de officiële ANEPC-site kon niet worden nagekeken.'),
('Portugal','text_nl','Een gedateerde nationale campagne vond ik niet.','Een gedateerde nationale campagne is in de gecontroleerde bronnen niet gevonden.'),
('Malta','text','I found no Maltese official advice to keep a food and water stock or a 72-hour figure.','No Maltese official advice to keep a food and water stock or a 72-hour figure was found in the sources checked.'),
('Malta','text_nl','vond ik niet.','is in de gecontroleerde bronnen niet gevonden.'),
('Greece','text','I could not open that site, so a Greek official kit list is unconfirmed.','That site could not be checked, so a Greek official kit list is unconfirmed.'),
('Greece','text_nl','Die site kon ik niet openen, dus','Die site kon niet worden nagekeken, dus'),
('Cyprus','text','I only saw this through media.','This is known only through media.'),
('Cyprus','text_nl','Ik zag dit alleen via media.','Dit is alleen via media bekend.'),
('Sweden','text','We found no new household edition in 2025-2026 and no new push in November 2026.','No new household edition in 2025-2026 and no new push in November 2026 were found in the sources checked.'),
('Sweden','text_nl','We vonden geen nieuwe huishoudeditie in 2025-2026 en geen nieuwe oproep in november 2026.','Een nieuwe huishoudeditie in 2025-2026 en een nieuwe oproep in november 2026 zijn in de gecontroleerde bronnen niet gevonden.'),
('Norway','text','We found no new urgent call in 2026.','No new urgent call in 2026 was found in the sources checked.'),
('Norway','text_nl','We vonden in 2026 geen nieuwe dringende oproep.','Een nieuwe dringende oproep in 2026 is in de gecontroleerde bronnen niet gevonden.'),
('Denmark','text','We found no new urgent call in autumn 2026.','No new urgent call in autumn 2026 was found in the sources checked.'),
('Denmark','text_nl','We vonden in het najaar van 2026 geen nieuwe dringende oproep.','Een nieuwe dringende oproep in het najaar van 2026 is in de gecontroleerde bronnen niet gevonden.'),
('Estonia','text','We found no newer edition.','No newer edition was found in the sources checked.'),
('Estonia','text_nl','We vonden geen nieuwere uitgave.','Een nieuwere uitgave is in de gecontroleerde bronnen niet gevonden.'),
('Latvia','text','We could not confirm a new edition in 2026.','A new edition in 2026 could not be confirmed.'),
('Latvia','text_nl','konden we niet bevestigen.','kon niet worden bevestigd.'),
('Poland','text','We did not read the official text ourselves.','The official text was not checked directly.'),
('Poland','text_nl','We hebben de officiele tekst zelf niet gelezen.','De officiële tekst is niet rechtstreeks nagekeken.'),
('Czechia','text','We found no new push in 2026.','No new push in 2026 was found in the sources checked.'),
('Czechia','text_nl','We vonden in 2026 geen nieuwe oproep.','Een nieuwe oproep in 2026 is in de gecontroleerde bronnen niet gevonden.'),
('Slovakia','text','which we could not check in the original.','which could not be checked in the original.'),
('Slovakia','text_nl','wat we niet in het origineel konden controleren.','wat niet in het origineel kon worden gecontroleerd.'),
('Hungary','text','We found no national Hungarian government campaign telling households to stock up.','No national Hungarian government campaign telling households to stock up was found in the sources checked.'),
('Hungary','text','but we could not verify it on an official page.','but it could not be verified on an official page.'),
('Hungary','text_nl','We vonden geen nationale Hongaarse overheidscampagne die huishoudens oproept een voorraad aan te leggen.','Een nationale Hongaarse overheidscampagne die huishoudens oproept een voorraad aan te leggen is in de gecontroleerde bronnen niet gevonden.'),
('Hungary','text_nl','maar we konden dat niet op een officiele pagina nagaan.','maar dat kon niet op een officiële pagina worden nagegaan.'),
('Slovenia','text','We did not retrieve the URSZR page itself.','The URSZR page itself was not checked.'),
('Slovenia','text_nl','De pagina van URSZR zelf hebben we niet kunnen ophalen.','De pagina van URSZR zelf is niet nagekeken.'),
('Romania','text','We could not confirm a new government stock-up campaign in 2026;','A new government stock-up campaign in 2026 could not be confirmed;'),
('Romania','text_nl','konden we niet bevestigen;','kon niet worden bevestigd;'),
('Bulgaria','text','We found no official Bulgarian national campaign asking households to keep an emergency stock.','No official Bulgarian national campaign asking households to keep an emergency stock was found in the sources checked.'),
('Bulgaria','text_nl','We vonden geen officiele Bulgaarse nationale campagne die huishoudens oproept een noodvoorraad aan te leggen.','Een officiële Bulgaarse nationale campagne die huishoudens oproept een noodvoorraad aan te leggen is in de gecontroleerde bronnen niet gevonden.'),
]
for c,f,o,n in R:
    v=D[c][f]; assert o in v,(c,f,o); D[c][f]=v.replace(o,n)
# Austria/Switzerland/Malta NL sentences start with the claim; fix the dangling sentence start
# (they read: "Een nieuwe ... oproept voorraad aan te leggen is in de gecontroleerde bronnen niet gevonden.")
# --- lead-editor: Belgium
b=D['Belgium']
b['guide']="Campaign 'Samen voorbereid' / 'Prêts ensemble' (four years) with the brochure 'Samen voorbereid' and the page 'Een noodpakket bij je thuis'"
b['hours']='72 hours'
b['items']=("A 72-hour emergency kit: water and food for at least 3 days (long-life, no cooking needed), necessary medicines for at least 72 hours, torch, battery or wind-up radio, power bank, hygiene items, basic first-aid kit, a small amount of cash, pet food. "
 "The NCCN distinguishes a compact evacuation backpack from a larger kit kept at home, and says no expensive pre-packed kit is needed.")
b['households']='Public campaign online and in media; brochure available online (NL/FR/DE/EN) and a print-ready version offered to authorities and organisations. A mailing to every household was not found in the sources checked.'
b['reason']=("The NCCN says emergencies can happen 'anywhere and at any time' and stresses that it does not want to cause panic; it wants people to be able to cope alone in the first 72 hours, when help may take time (per VRT NWS). "
 "One secondary source links the campaign to geopolitical tension and climate change; the NCCN itself naming war was not found in the sources checked.")
b['text']=("The federal National Crisis Centre (NCCN) launched the four-year campaign 'Samen voorbereid' on 21 April 2026. It advises a 72-hour emergency kit with water, food that needs no cooking, medicines, a torch and a radio, and distinguishes a compact evacuation backpack from a larger kit kept at home. "
 "According to VRT NWS (21 April 2026), no expensive pre-packed kit is needed, and the centre stresses that it does not want to cause panic. A mailing to every household was not found in the sources checked. Details are taken from the NCCN brochure and pages and from VRT NWS.")
b['text_nl']=("Het federale Nationaal Crisiscentrum (NCCN) lanceerde op 21 april 2026 de vierjarige campagne 'Samen voorbereid'. Het raadt een noodpakket voor 72 uur aan, met water, voeding die niet gekookt hoeft te worden, medicijnen, een zaklamp en een radio, en maakt onderscheid tussen een compacte evacuatierugzak en een groter pakket thuis. "
 "Volgens VRT NWS (21 april 2026) is er geen duur kant-en-klaar pakket nodig, en benadrukt het centrum dat het geen paniek wil zaaien. Een bedeling aan elk huishouden is in de gecontroleerde bronnen niet gevonden. De details komen uit de brochure en de pagina's van het NCCN en uit VRT NWS.")
b['news_2025_2026']=b['news_2025_2026'].replace('(VRT, Business AM, Paris Match)','(VRT NWS, Business AM, Paris Match)')
urls=[s['url'] for s in b['sources']]
BR='https://crisiscentrum.be/sites/default/files/documents/files/WEB-Brochure%20Samen%20voorbereid-NL.pdf'
if BR not in urls: b['sources'].insert(0,{'url':BR,'title':'Brochure Samen voorbereid (NL)','publisher':'Nationaal Crisiscentrum','date':'2026','type':'off'})
# --- lead-editor: EU
e=D['EU']
e['latest']='Guidelines dated 30 October 2026; made public in early November 2026, according to media'
e['guide']="Preparedness Union Strategy (26 March 2025); 'Guidelines on Population Preparedness under the EU Preparedness Union Strategy', Communication C(2026) 8250, with staff working document SWD(2026) 826 (both dated 30 October 2026)"
e['first']='26 March 2025 (Preparedness Union Strategy)'
e['hours']='at least 72 hours'
e['water']='No quantity is set by the Commission; left to the member states'
e['news_2025_2026']=("26 March 2025: the Preparedness Union Strategy first announced the aim that people should be able to cope for at least 72 hours. "
 "30 October 2026: the Commission's population preparedness guidelines, Communication C(2026) 8250 and staff working document SWD(2026) 826, are dated this day; according to media they were made public in early November 2026 (presented on 3 November at the European Civil Protection Forum).")
e['text']=("The Commission's Preparedness Union Strategy of 26 March 2025 first announced the aim that people should be able to cope for at least 72 hours in a crisis. The Commission's 'Guidelines on Population Preparedness under the EU Preparedness Union Strategy', Communication C(2026) 8250, and the staff working document SWD(2026) 826 are both dated 30 October 2026; according to media they were made public in early November 2026. "
 "The guidance is non-binding. It asks member states to help households meet their essential needs for at least 72 hours, sets no specific quantities (no EU kit list and no litres of water) and carries no penalties.")
e['text_nl']=("De Preparedness Union Strategy van de Europese Commissie van 26 maart 2025 kondigde als eerste het doel aan dat mensen minstens 72 uur zelfstandig een crisis kunnen doorstaan. De 'Guidelines on Population Preparedness under the EU Preparedness Union Strategy', Mededeling C(2026) 8250, en het werkdocument van de diensten SWD(2026) 826 zijn beide gedateerd op 30 oktober 2026; volgens media werden ze begin november 2026 openbaar gemaakt. "
 "De richtsnoeren zijn niet-bindend. Ze vragen de lidstaten huishoudens te helpen om minstens 72 uur in hun essentiële behoeften te voorzien, leggen geen specifieke hoeveelheden vast (geen EU-lijst en geen aantal liters water) en voorzien geen sancties.")
BAD=re.compile(r"\bI\b|\bI'|\bwe\b|\bWe\b|\bmy\b|\bour\b|session|search results|searches|WebFetch|\bik\b|\bIk\b|\bvond ik\b|\bwe vonden\b|\bWe vonden\b|sessie|zoekresultaten|\bkon ik\b|\bzag ik\b|\bhebben we\b|\bkonden we\b",re.I)
for x in L:
    for k,v in x.items():
        if isinstance(v,str):
            if k.endswith('_nl') or k=='text_nl': D[x['country']][k]=v.replace('officiele','officiële')
            assert not BAD.search(D[x['country']][k]),(x['country'],k,BAD.search(D[x['country']][k]).group(0))
# ---------------- structured helper fields (hand-set from the verified fields above) ----------------
# bucket: 3d = 72 hours / 3 days (some "at least", Romania 3-5 days, Germany at least 3 days with 10 if possible); 1w about a week; 10d 10-14 days; '' no single clear length given
BUCKET={'Austria':'10d','Switzerland':'1w','Sweden':'1w','Norway':'1w','Estonia':'1w','Liechtenstein':'','Ireland':'','Slovakia':'','Croatia':'','Romania':''}  # Croatia (reportedly 2 days vs 72 hours) and Romania (3 to 5 days) have no single length
SHORT={ # hours_s, water_s, mail code, mail_s, latest_s
'Belgium':('72 hours','3–10 l per person per day (as reported)','no','No: online and in the media; no mailing found','1 Oct 2026 (brochure)'),
'EU':('at least 72 hours','No quantity set','na','Not applicable (guidelines to member states)','30 Oct 2026'),
'Netherlands':('72 hours (3 days)','3 l (as reported)','yes','Yes: booklet distributed to households (about 8.5 million, as reported)','12 Oct 2026 (new campaign phase)'),
'Luxembourg':('72 hours','at least 3 l (as reported)','yes','Yes: about 300,000 copies from 14 Oct 2026','14 Oct 2026'),
'France':('72 hours','6 l for 72 hours (as reported)','no','No: free public guide; no mailing found','20 Nov 2025 (guide)'),
'Germany':('at least 3 days; 10 days if possible','2 l (as reported)','no','No: free booklet on order and as PDF','13 Oct 2025 (new guide)'),
'Austria':('10 to 14 days','2 l for drinking (as reported)','no','No: online information; no mailing found','2025 (OeZSV guide)'),
'Switzerland':('about 1 week','9 l per person (about 3 days)','no','No: campaign with retailers; free brochure','17 Feb 2025 (brochure)'),
'Liechtenstein':('3 days of water; 1 week of food','9 l per person (3 days)','no','No: public campaign','June 2026 (security strategy)'),
'Italy':('first 72 hours (per media)','—','no','No: no mailing found','Nov 2026 (media)'),
'Spain':('72 hours (3 days)','at least 1.5 l (Catalan guide, as reported)','no','No: no mailing found','17 Nov 2025 (Catalan update, per media)'),
'Portugal':('72 hours','3 l (per DECO Proteste)','no','No: no mailing found','10 Nov 2026 (media)'),
'Ireland':('no number of days in the booklet (per The Journal)','2–3 l (as reported)','yes','Yes: about 2.2 million booklets via An Post from 21 Sep 2026','21 Sep 2026 (delivery)'),
'Malta':('—','—','other','Manual and fire blanket to every household (not stock-up advice)','13–14 Apr 2026'),
'Greece':('—','—','no','No: none found','Nov 2026 (media)'),
'Cyprus':('at least 72 hours','—','no','No: advice via media and ministry posts','2 Mar 2026; Nov 2026 (media)'),
'Sweden':('at least 1 week','3–5 l (as reported)','yes','Yes: about 5 million copies, Nov 2024','21–27 Sep 2026 (preparedness week)'),
'Finland':('at least 72 hours','—','planned','Not yet: about 3.5 million printed guides planned for January, announced Oct 2026','Mid-Oct 2026 (mailing announced)'),
'Norway':('1 week (raised from 3 days)','about 20 l stored (3 l a day rule of thumb)','yes','Yes: brochure to every household, autumn 2024','27 Oct–2 Nov 2025 (campaign week)'),
'Denmark':('3 days (72 hours)','3 l (9 l for 3 days)','digital','Digital post (e-Boks) in 2024; no paper mailing found','Feb 2026 (brochure)'),
'Iceland':('at least 3 days','No fixed quantity','unclear','Not confirmed: booklet published online','3 Nov 2026 (booklet)'),
'Estonia':('1 week (72 hours as a first step in some material)','3 l (21 l a week)','yes','Yes: about 600,000 households, 2024 (per ERR)','2024 (printed manual)'),
'Latvia':('72 hours (3 days)','—','unclear','Not confirmed','April 2024 (revised edition)'),
'Lithuania':('72 hours (3 days)','sources differ (6 l or 12 l for 72 hours)','unclear','Not confirmed: 2024 leaflet reported at about 1 million households','5 Mar 2026 (brochure)'),
'Poland':('at least 3 days (72 hours)','3 l (as reported)','yes','Yes (per press): about 16–17 million households, Dec 2025–Jan 2026','Dec 2025–Jan 2026 (mailing)'),
'Czechia':('72 hours (3 days)','about 2 l per adult','yes','Yes: Czech Post, all households, autumn 2025','Autumn 2025 (mailing)'),
'Slovakia':('unclear: up to 14 days of food and drink per media; EU baseline 72 hours','3–5 l (press report)','no','No: published on the ministry website','Oct 2025 (handbook)'),
'Hungary':('—','—','no','No: none found','—'),
'Slovenia':('at least 3 days (72 hours)','7.5 l for all uses (per media)','no','No: no mailing found','Nov 2026 (media)'),
'Croatia':('72 hours (the site reportedly still says 2 days)','1.5–2 l (per media)','no','No: no mailing found','13 Oct 2026 (message)'),
'Romania':('3 to 5 days (72 hours at the low end)','at least 4 l (IGSU guide)','no','No: no mailing found','2026 (guide re-hosted)'),
'Bulgaria':('—','—','no','No: none found','—'),
}
EARLIER=['Sweden','Norway','Estonia','Latvia','Switzerland','Finland','Germany','Denmark','Lithuania','Liechtenstein']
# events: (sort, date shown, country, EN, NL, status C/R, kind)  kind: launch|mailing|plan|eu|other
EV=[
('2025-03-26','26 Mar 2025','EU',"The Preparedness Union Strategy is adopted, with an action asking for guidance so that people can cope for at least 72 hours.","De Preparedness Union Strategy wordt aangenomen, met een actie voor richtsnoeren zodat mensen minstens 72 uur zelfstandig kunnen blijven.",'C','eu'),
('2025-05-15','May 2025','Spain',"The civil protection directorate is reported to have published a family-plan model with a 72-hour kit; this is not verified on an official site.","De directie civiele bescherming zou een gezinsplan met een 72-uurskit hebben gepubliceerd; dit is niet op een officiële site nagegaan.",'R','launch'),
('2025-10-13','13 Oct 2025','Germany',"Interior Minister Dobrindt and BBK President Tiesler present the revised guide 'Vorsorgen fuer Krisen und Katastrophen'.","Minister van Binnenlandse Zaken Dobrindt en BBK-voorzitter Tiesler stellen de herziene gids 'Vorsorgen fuer Krisen und Katastrophen' voor.",'C','launch'),
('2025-10-15','Oct 2025','Slovakia',"The Interior Ministry publishes a handbook on what to do in a crisis or armed conflict.","Het ministerie van Binnenlandse Zaken publiceert een handboek over wat te doen bij een crisis of gewapend conflict.",'C','launch'),
('2025-10-27','27 Oct–2 Nov 2025','Norway',"Egenberedskapsuka, the yearly self-preparedness week of the civil protection directorate DSB.","Egenberedskapsuka, de jaarlijkse week van zelfredzaamheid van de directie civiele bescherming DSB.",'C','other'),
('2025-11-03','3 Nov 2025','Netherlands',"The government starts the 'Denk vooruit' campaign (NCTV).","De regering start de campagne 'Denk vooruit' (NCTV).",'C','launch'),
('2025-11-05','Oct–Nov 2025','Czechia',"The printed '72 hours' guide is mailed by Czech Post to all households (about 5 million copies, per press).","De gedrukte gids '72 uur' wordt door Czech Post naar alle huishoudens gestuurd (ongeveer 5 miljoen exemplaren, volgens de pers).",'C','mailing'),
('2025-11-17','17 Nov 2025','Netherlands',"Minister Van Oosten presents the booklet 'Bereid je voor op een noodsituatie'.","Minister Van Oosten stelt het boekje 'Bereid je voor op een noodsituatie' voor.",'C','launch'),
('2025-11-20','20 Nov 2025','France',"The SGDSN publishes the guide 'Tous responsables' with a 72-hour kit checklist.","De SGDSN publiceert de gids 'Tous responsables' met een checklist voor een 72-uurskit.",'C','launch'),
('2025-12-31','Dec 2025–Jan 2026','Poland',"The printed 'Poradnik bezpieczenstwa' is mailed to about 16–17 million households, according to press reports.","De gedrukte 'Poradnik bezpieczenstwa' wordt naar ongeveer 16–17 miljoen huishoudens gestuurd, volgens persberichten.",'R','mailing'),
('2026-01-15','Jan 2026','Sweden',"The civil defence agency MCF sends a separate brochure to about 130,000 businesses and organisations (secondary report).","De civiele-verdedigingsdienst MCF stuurt een aparte brochure naar ongeveer 130.000 bedrijven en organisaties (secundaire bron).",'R','other'),
('2026-01-24','Jan 2026','Ireland',"The booklet is announced, according to the Irish Times.","Het boekje wordt aangekondigd, volgens de Irish Times.",'R','other'),
('2026-02-15','Feb 2026','Denmark',"A new 'Totalberedskab' brochure repeats the three-day advice (as reported).","Een nieuwe brochure 'Totalberedskab' herhaalt het driedagenadvies (zoals gemeld).",'C','launch'),
('2026-03-02','2 Mar 2026','Cyprus',"Civil Defence issues a reminder about shelters and the household kit, according to the Cyprus Mail.","De Civil Defence herinnert aan schuilplaatsen en het noodpakket, volgens de Cyprus Mail.",'R','other'),
('2026-03-05','5 Mar 2026','Finland',"A citizen brochure on preparedness is published.","Een burgerbrochure over paraatheid wordt gepubliceerd.",'C','launch'),
('2026-03-05','5 Mar 2026','Lithuania',"A citizen brochure is listed by the EU Civil Protection Knowledge Network.","Een burgerbrochure wordt vermeld door het EU Civil Protection Knowledge Network.",'C','launch'),
('2026-04-13','13 Apr 2026','Malta',"The government announces an emergency manual and a fire blanket for every household; no stock-up advice was found in it.","De regering kondigt een noodhandleiding en een brandblusdeken voor elk huishouden aan; er is geen voorraadadvies in gevonden.",'R','other'),
('2026-04-21','21 Apr 2026','Belgium',"The National Crisis Centre (NCCN) launches the four-year campaign 'Samen voorbereid' and advises a 72-hour emergency kit.","Het Nationaal Crisiscentrum (NCCN) lanceert de vierjarige campagne 'Samen voorbereid' en raadt een noodpakket voor 72 uur aan.",'C','launch'),
('2026-06-02','2 Jun 2026','Germany',"A plain-language version of the guide is dated on the BBK site.","Een versie in eenvoudige taal van de gids staat gedateerd op de BBK-site.",'C','other'),
('2026-06-15','June 2026','Liechtenstein',"The government's security strategy presents the household stock as a personal precaution.","De veiligheidsstrategie van de regering presenteert de huisvoorraad als persoonlijke voorzorg.",'C','other'),
('2026-08-28','28 Aug 2026','Ireland',"Minister Helen McEntee launches the 'Be Emergency Ready' campaign.","Minister Helen McEntee lanceert de campagne 'Be Emergency Ready'.",'C','launch'),
('2026-09-21','21 Sep 2026','Ireland',"An Post begins delivering the booklet to about 2.2 million households, over three weeks.","An Post begint het boekje te bezorgen bij ongeveer 2,2 miljoen huishoudens, over drie weken.",'C','mailing'),
('2026-09-22','21–27 Sep 2026','Sweden',"Beredskapsveckan, the preparedness week of the civil defence agency MCF.","Beredskapsveckan, de paraatheidsweek van de civiele-verdedigingsdienst MCF.",'C','other'),
('2026-10-01','1 Oct 2026','Belgium',"The NCCN publishes the brochure 'Samen voorbereid' (VRT NWS, NCCN newsroom).","Het NCCN publiceert de brochure 'Samen voorbereid' (VRT NWS, nieuwskamer NCCN).",'C','launch'),
('2026-10-09','9 Oct 2026','Luxembourg',"Prime Minister Frieden, Interior Minister Gloden and High Commissioner Bley present the guide 'Mon Guide - 72H d'autonomie'.","Premier Frieden, minister van Binnenlandse Zaken Gloden en hoge commissaris Bley stellen de gids 'Mon Guide - 72H d'autonomie' voor.",'C','launch'),
('2026-10-12','12 Oct 2026','Netherlands',"A new phase of the 'Denk vooruit' campaign is announced by Minister Van Weel; step 1 is still the emergency kit.","Een nieuwe fase van de campagne 'Denk vooruit' wordt aangekondigd door minister Van Weel; stap 1 blijft het noodpakket.",'C','launch'),
('2026-10-13','13 Oct 2026','Croatia',"The Civil Protection Directorate publishes the message 'Otpornost pocinje kod kuce' (Resilience starts at home), according to Croatian media.","De directie civiele bescherming publiceert de boodschap 'Otpornost pocinje kod kuce' (Veerkracht begint thuis), volgens Kroatische media.",'R','launch'),
('2026-10-14','14 Oct 2026','Luxembourg',"Delivery of about 300,000 printed copies to households begins.","De bezorging van ongeveer 300.000 gedrukte exemplaren bij huishoudens begint.",'C','mailing'),
('2026-10-15','15 Oct 2026','Finland',"The Interior Ministry announces plans to mail about 3.5 million printed guides in January, according to Yle; the mailing has not been confirmed as started.","Het ministerie van Binnenlandse Zaken kondigt aan in januari ongeveer 3,5 miljoen gedrukte gidsen te versturen, volgens Yle; de verzending is niet als gestart bevestigd.",'R','plan'),
('2026-10-30','30 Oct 2026','EU',"The Commission's guidelines on population preparedness (Communication C(2026) 8250 and staff working document SWD(2026) 826) are dated this day. They were made public in early November 2026, according to media.","De richtsnoeren van de Commissie over bevolkingsparaatheid (Mededeling C(2026) 8250 en werkdocument SWD(2026) 826) dragen deze datum. Ze werden begin november 2026 openbaar gemaakt, volgens media.",'C','eu'),
('2026-11-03','3 Nov 2026','Iceland',"Civil Protection issues the booklet 'Verum vidbuin' (Be Prepared), urging households to cover basic needs for at least three days and keep some cash at home.","Civil Protection geeft het boekje 'Verum vidbuin' (Wees voorbereid) uit en vraagt huishoudens minstens drie dagen in hun basisbehoeften te kunnen voorzien en wat contant geld thuis te houden.",'R','launch'),
]
out=[]
for x in L:
    c=x['country']; y=D[c]; sh=SHORT[c]
    adv='C' if (y['has_advice']=='yes' and y['status']=='C') else ('R' if y['has_advice']=='yes' else 'N')
    y.update({'adv':adv,'bucket':BUCKET.get(c,'3d') if adv!='N' else '','hours_s':sh[0],'water_s':sh[1],'mail':sh[2],'mail_s':sh[3],'latest_s':sh[4],'earlier':c in EARLIER})
    out.append(y)
json.dump({'countries':out,'events':[dict(zip(('sort','date','country','en','nl','st','kind'),e)) for e in EV]},open(S+'mine/tools/prepare_data.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('merged',len(out),len(EV))
