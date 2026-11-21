"""Page '#qa' (Questions and answers): 8 groups, the 29 existing questions placed in the fitting group, 35 new questions.
Runs on build/mine/vrt-cyber-briefing.html (re-copied by make_mine.py on every build), after the other page scripts and before fold.py.

House rules: facts only; every new answer is built from text that is already in the app (pages, register, evidence tracker, news
snapshot); blame is always "X says"; status tags (Confirmed, Reported, Claimed, Suspected, Not proven, Not published) as the app uses them.
Markup follows the existing cards: <details class="qa"><summary>EN · <i>NL</i></summary><div class="body"><p>EN</p><p class="nl">NL: ...</p>...
(bilang.js pairs p + p.nl, h2 + p.nl, and the summary 'EN · NL'). Cards are collapsed by default.

The existing 29 cards are read from the section as it stands when this script runs (so earlier text fixes are kept), regrouped, given a
Dutch version of their note (p.trap), a status line and a "More" link. Three existing items are updated where the app's own pages say
otherwise (see UPDATES). Usage: qa2.py  (build)   |   qa2.py --sources FILE  (write the source map for the new answers)"""
import sys, re, ast, html, copy
from bs4 import BeautifulSoup

M = '/home/user/cyberdesk-2026/build/mine/'
e = html.escape

# ---------- page names (EN / NL): the final menu labels (nav2026.py "regroup" table), so link names match the menu ----------
_nt = open(M + 'tools/nav2026.py', encoding='utf-8').read()
_g = ast.literal_eval(_nt[_nt.index('G=[', _nt.index('regroup')) + 2:_nt.index('new=[{')].strip())
PAGE = {k: (en, nl) for _ge, _gn, its in _g for k, en, nl in its}

TAGS = {'C': ('Confirmed', 't-conf'), 'R': ('Reported', 't-rep'), 'K': ('Claimed', 't-claim'), 'S': ('Suspected', 't-susp'),
        'N': ('Not proven', 't-none'), 'U': ('Not published', 't-none')}


def tags(codes):
    return ''.join('<span class="tag %s">%s</span> ' % (TAGS[c][1], TAGS[c][0]) for c in codes)


def more_p(codes, keys):
    """status line + 'More' link(s): an English paragraph and its Dutch p.nl partner"""
    for k in keys:
        assert k in PAGE, k
    en_links = ' · '.join('<a href="#%s">%s</a>' % (k, e(PAGE[k][0])) for k in keys)
    nl_links = ' · '.join('<a href="#%s">%s</a>' % (k, e(PAGE[k][1])) for k in keys)
    st = ('Status: ' + tags(codes) + ' · ') if codes else ''
    return ('<p class="qa-more">%sMore: %s</p><p class="nl qa-more">NL: %s%s</p>'
            % (st, en_links, ('Status: ' + tags(codes) + ' · ') if codes else '', 'Meer: ' + nl_links))


# ---------- the groups ----------
GROUPS = [
 ('basics', 'The basics', 'De basis'),
 ('belgium', 'Belgium', 'België'),
 ('who', 'Who is behind it', 'Wie zit erachter'),
 ('cases', 'The big recent cases', 'De grote recente zaken'),
 ('life', 'Everyday life', 'Het dagelijks leven'),
 ('infra', 'Infrastructure', 'Infrastructuur'),
 ('tech', 'Technology', 'Technologie'),
 ('law', 'Laws and politics', 'Wetten en politiek'),
]

# existing questions (by their English text, first words) -> group, tags, More pages
OLD = [
 # (start of the English question, group, tags, pages)
 ('How bad is it?', 'basics', 'C', ['numbers']),
 ('Who was behind the freezer attacks?', 'who', 'CK', ['freezers']),
 ('Could the freezer attacks have been prevented?', 'belgium', 'C', ['freezers']),
 ("There are European cyber laws.", 'law', 'C', ['laws']),
 ('What do Europe and Belgium do today', 'law', 'C', ['laws']),
 ('When will the new European cyber law apply?', 'law', 'C', ['laws']),
 ('Were the freezer attacks an attack on the energy supply?', 'infra', 'C', ['energy']),
 ('Can hackers cause a blackout in Belgium?', 'infra', 'C', ['energy']),
 ('Can hackers cause a nuclear accident?', 'infra', 'C', ['energy']),
 ('Is the gas supply safe from hackers?', 'infra', 'CN', ['energy']),
 ('Artificial intelligence: hype or real danger?', 'tech', 'CN', ['ai']),
 ('Does Europe depend too much on America', 'tech', 'C', ['ai']),
 ('Should Europe exclude suppliers', 'law', 'C', ['laws']),
 ('Are Chinese solar inverters a danger?', 'infra', 'CN', ['energy']),
 ('Should fraud victims get their money back?', 'life', 'C', ['victims']),
 ('What can people at home do?', 'life', '', ['victims']),
 ("Won't new obligations crush small businesses?", 'law', 'R', ['props']),
 ('What should Europe do about Iran?', 'who', 'CK', ['evidence']),
 ('Are hospitals protected?', 'belgium', 'C', ['health']),
 ('Should companies be allowed to pay ransoms?', 'law', 'R', ['insurance']),
 ('Who pays for all this?', 'law', 'C', ['props']),
 ('Why do so many municipalities', 'belgium', 'C', ['gaps']),
 ('Should we be afraid of AI that hacks on its own?', 'tech', 'C', ['agents']),
 ('Are elections safe?', 'belgium', 'CN', ['elections']),
 ('What about the drones over Doel?', 'infra', 'RN', ['hybrid']),
 ('Was the 2025 blackout in Spain and Portugal', 'infra', 'C', ['energy']),
 ('Was tax data stolen in the MyMinfin attack?', 'cases', 'C', ['now']),
 ('Why does nobody go to jail?', 'who', 'C', ['evidence']),
 ('Who is in charge of cybersecurity in Belgium?', 'belgium', 'C', ['powers']),
]

# Dutch versions of the existing English-only notes (p.trap), keyed by the start of the English note
TRAP_NL = {
 '"Reports" are not "attacks"': 'Meldingen zijn geen aanvallen: de meldingsplicht verklaart een deel van de stijging, en veel slachtoffers melden nooit iets.',
 'US agencies reportedly hold only low confidence': 'Amerikaanse diensten hebben volgens berichten maar weinig vertrouwen in de link met Iran. Op 10 november zei de Belgische minister van Buitenlandse Zaken dat België de Franse informatie zeer ernstig neemt, maar geen bewijs heeft dat Iran of iemand anders aan de Belgische incidenten koppelt. Op 12 november zei de minister van Binnenlandse Zaken dat Iran er "hoogstwaarschijnlijk" achter zit; de minister van Buitenlandse Zaken en het federaal parket bevestigen dat niet. Iran verwerpt de beschuldiging.',
 'The cyber centre can warn but cannot order an installer': 'Het cybercentrum kan waarschuwen, maar kan een installateur niet bevelen om in te grijpen. Het aantal blootgestelde sturingen in België verschilt naargelang de methode; "honderden" is het veilige woord.',
 'NIS2 covers food wholesale': 'NIS2 geldt voor groothandel en verwerking van voedsel, maar niet voor supermarkten (kleinhandel).',
 'Full detail on the page "Laws and regulations"': 'Alle details op de pagina "Wetten en regels".',
 'Negotiations between Parliament and the governments': 'De onderhandelingen tussen het Parlement en de regeringen worden ten vroegste in 2027 verwacht.',
 'No source says the freezer attacks touched the electricity grid': 'Geen enkele bron zegt dat de diepvriesaanvallen het elektriciteitsnet raakten. De link is de methode en het soort toestel.',
 'No successful attack on Elia or Fluvius': 'In openbare bronnen is geen geslaagde aanval op Elia of Fluvius gevonden.',
 'Stuxnet (2010) showed': 'Stuxnet (2010) toonde dat "niet verbonden" niet hetzelfde is als "veilig": het vergde jaren en middelen van een staat, en kwam binnen via usb-sticks.',
 'No public report of a cyberattack on Fluxys': 'Er is geen openbaar bericht gevonden over een cyberaanval op Fluxys of de terminal van Zeebrugge.',
 'No evidence links AI to the Belgian attacks': 'Geen bewijs koppelt AI aan de Belgische aanvallen van het najaar 2026. De veiligheidsregels van de AI-wet voor risicovolle AI zijn uitgesteld tot december 2027.',
 'Much European government data also runs': 'Veel Europese overheidsgegevens draaien ook op Amerikaanse clouddiensten; zie "Afhankelijkheid van de cloud".',
 'For solar inverters the EU has already stopped': 'Voor zonne-omvormers financiert de EU in projecten die ze zelf betaalt al geen risicoleveranciers meer (deadline 1 november 2026).',
 'Hidden "kill switches"': 'Verborgen "noodschakelaars" zijn niet als feit vastgesteld. Het gecontroleerde punt is de toegang op afstand via het platform van de maker.',
 'Romance and investment scams are not covered': 'Romance- en beleggingsfraude vallen niet onder de terugbetalingsregel.',
 'People with solar panels or a home battery': 'Wie zonnepanelen of een thuisbatterij heeft: verander het fabriekswachtwoord, zet updates aan en vraag de installateur wie de installatie op afstand kan bedienen.',
 'In FortiBleed the 270+': 'Bij FortiBleed waren de 270+ Belgische slachtoffers vooral kleine en middelgrote bedrijven.',
 'The Belgian wave is not attributed': 'De Belgische golf is niet toegeschreven. Sancties stonden volgens berichten op de agenda van de bijeenkomst van de EU-ministers van Buitenlandse Zaken in de week van 16 november; niet bevestigd.',
 'The UK said in July 2025 it would ban such payments': 'Het Verenigd Koninkrijk zei in juli 2025 dat het deze betalingen wil verbieden; een jaar later was het nog een voorstel. Of het verbod nu al geldt, is niet bevestigd.',
 'No verified figure exists': 'Er bestaat geen gecontroleerd cijfer voor het eigen budget of personeel van het cybercentrum.',
 'Keep apart vote counting': 'Houd het tellen van de stemmen (geen bewijs van inbreuk), websites (aanvallen vastgesteld) en manipulatie van informatie (deepfakes vastgesteld) uit elkaar.',
 "This is the department's own finding": 'Dit is de eigen vaststelling van de FOD Financiën; ze is niet onafhankelijk bevestigd.',
 'About $3 billion of the roughly $6.3 billion': 'Ongeveer 3 miljard dollar van de circa 6,3 miljard dollar die op 29 oktober 2026 bij Binance werd gestolen, werd binnen enkele dagen bevroren.',
 'These were test incidents': 'Dit waren testincidenten; er is geen Belgisch of Europees slachtoffer bekend.',
 'Whether the decree moving the cyber centre': 'Of het besluit over de verhuizing van het cybercentrum is gepubliceerd, is niet bevestigd. Alle details op de pagina "Wie is waarvoor bevoegd".',
}

# updates of existing answers where the app's own pages say otherwise: (English old, English new, Dutch old, Dutch new)
UPDATES = [
 # 12 Nov: the interior minister names Iran as "very probably"; foreign minister and prosecutor do not confirm (Right now / freezer pages)
 ('Iran rejects the accusation.',
  'On 12 November the interior minister said Iran is "very probably" behind them; the foreign minister and the federal prosecutor do not confirm this. Iran rejects the accusation.',
  None, None),
 # payment rules: Council position 28 Oct 2026, Parliament's final vote is next (Scams and fraud page): not final yet
 ('the new European payment rules make the bank refund the victim',
  'the new European payment rules (not final yet: Parliament\'s final vote is next) make the bank refund the victim',
  'verplichten de nieuwe Europese betaalregels de bank',
  'verplichten de nieuwe Europese betaalregels (nog niet definitief: het Europees Parlement moet nog stemmen) de bank'),
 # UK ban: a year after the July 2025 announcement it was still a proposal (Insurance page)
 ('Whether the UK ban is already in force is not confirmed.',
  'The UK said in July 2025 it would ban such payments; a year later it was still a proposal. Whether it is in force now is not confirmed.',
  None, None),
]

# ---------- the new questions ----------
# each: group, q_en, q_nl, a_en, a_nl, tags, pages, [trap_en, trap_nl], src (for sources.md only)
NEW = []


def new(g, q, qn, a, an, tg, pages, trap=None, src=()):
    NEW.append(dict(g=g, q=q, qn=qn, a=a, an=an, tags=tg, pages=pages, trap=trap, src=list(src)))


# ===== 1 The basics =====
new('basics',
    'What counts as a cyberattack, and what is only an outage?',
    'Wat is een cyberaanval, en wat is gewoon een storing?',
    "An outage is when a service stops for many people. It is a cyberattack only when someone attacked the systems on purpose. Of the 54 big outages on the \"Global outages\" page (January 2025 to 19 November 2026), 22 were cyberattacks, 22 were technical faults or changes at the companies themselves, 4 were power or cooling failures and for 6 no cause has been published. Two that were not attacks: Cloudflare on 5 December 2025 (a firewall change) and AWS on 19–20 October 2025 (a timing bug). Of the 103 cases in the evidence tracker, 8 first looked like attacks and turned out to be something else.",
    "Een storing is wanneer een dienst voor veel mensen stopt. Het is alleen een cyberaanval als iemand de systemen opzettelijk heeft aangevallen. Van de 54 grote storingen op de pagina \"Wereldwijde storingen\" (januari 2025 tot 19 november 2026) waren er 22 cyberaanvallen, 22 technische fouten of wijzigingen bij de bedrijven zelf, 4 stroom- of koelingsproblemen, en voor 6 is geen oorzaak bekendgemaakt. Twee die geen aanval waren: Cloudflare op 5 december 2025 (een wijziging aan een firewall) en AWS op 19–20 oktober 2025 (een timingfout). Van de 103 zaken in de bewijstracker leken er 8 eerst een aanval en bleken ze iets anders.",
    'C', ['outages'],
    src=['Global outages page: key figures (54 outages; 22 / 22 / 4 / 6) and the Cloudflare 5 Dec 2025 and AWS 19-20 Oct 2025 cards',
         'Who did it: the evidence page: 8 of 103 cases "not an attack, or no evidence"'])

new('basics',
    'How do we know who did it, and what do Confirmed, Reported, Claimed and Suspected mean?',
    'Hoe weten we wie het deed, en wat betekenen Bevestigd, Gemeld, Geclaimd en Vermoed?',
    "Mostly we do not know for sure. The evidence tracker puts every case on a ladder: L6 court verdict, L5 charges or arrests, L4 formal attribution by a government, L3 statement by an official, L2 researchers or unnamed sources, L1 the attackers' own claim, L0 nobody named. The labels say how firm a statement is. Confirmed: an authority, a court or the organisation itself said so. Reported: said in the press, not verified. Claimed: one party says so without public evidence, such as the attackers. Suspected: believed, not proven. An attacker's own claim is never counted as attribution.",
    "Meestal weten we het niet zeker. De bewijstracker zet elke zaak op een ladder: L6 vonnis van een rechtbank, L5 aanklacht of arrestatie, L4 formele toewijzing door een regering, L3 uitspraak van een gezagsdrager, L2 onderzoekers of anonieme bronnen, L1 de bewering van de aanvallers zelf, L0 niemand genoemd. De labels zeggen hoe stevig een uitspraak is. Bevestigd: een overheid, een rechtbank of de organisatie zelf zei het. Gemeld: in de pers gezegd, niet gecontroleerd. Geclaimd: één partij zegt het zonder openbaar bewijs, zoals de aanvallers. Vermoed: men gelooft het, maar het is niet bewezen. De eigen bewering van aanvallers telt nooit als toewijzing.",
    'CRKS', ['evidence'],
    src=['Who did it: the evidence page: "The ladder of proof" (L6 to L0, with the Dutch names) and the intro',
         'Who was behind it page: "Claims by attackers themselves are not counted as attribution"',
         'Label definitions as used on the Hybrid, Global outages and Sea cables pages (Confirmed / Reported / Claimed / Suspected)'])

new('basics',
    'Why do countries take so long to name a culprit?',
    'Waarom duurt het zo lang voor een land een dader aanwijst?',
    "Naming a state needs evidence that is often secret, and a court needs even more. Some governments name a state fast: Germany for the Leipzig airport drone and France for the freezer attacks both took about 4 weeks, but those rest on official statements whose evidence stays secret, and the French one is disputed. Slower ones were firmer: the attack on Polish energy sites of 29 December 2025 was blamed on Russia's FSB after about 6½ months, and court verdicts took 10 to 18 months. The people caught are often hired hands, and the step from them to an officer in Moscow is where most cases thin out.",
    "Een staat aanwijzen vraagt bewijs dat vaak geheim blijft, en een rechtbank wil nog meer. Sommige regeringen wijzen snel een staat aan: Duitsland voor de drone aan de luchthaven van Leipzig en Frankrijk voor de diepvriesaanvallen deden er allebei ongeveer 4 weken over, maar die steunen op officiële verklaringen waarvan het bewijs geheim blijft, en de Franse is betwist. Latere toewijzingen waren steviger: de aanval op Poolse energiesites van 29 december 2025 werd na ongeveer 6½ maand aan de Russische FSB toegeschreven, en gerechtelijke vonnissen kwamen na 10 tot 18 maanden. De opgepakte mensen zijn vaak ingehuurde handlangers, en de stap van hen naar een officier in Moskou is waar de meeste zaken dun worden.",
    'CR', ['evidence'],
    src=['Who did it: the evidence page: "How long it takes to name someone" table (Leipzig 4 weeks, French freezers 4 weeks, Polish energy sites 6½ months, Fitburg 10 months, IKEA Vilnius 18 months)',
         'Same page, "What the evidence shows" points 3 and 4 (hired hands; fast attributions political, slow ones legal; US reportedly doubts the French finding)'])

new('basics',
    'Is Europe attacked more than before?',
    'Wordt Europa meer aangevallen dan vroeger?',
    "ENISA, the EU's cyber agency, counted 8,257 incidents in the EU for 2025, against 4,875 in its previous report, but the two reports cover different periods and count different things. About half (51.3%) were DDoS attacks that only knock websites offline for a while, and 39.5% were break-ins. ENISA warns that more reports do not always mean more attacks. Some countries show a rise, for example Belgium (372 reports in 2024, 556 in 2025, 588 in the first nine months of 2026), but Czechia recorded fewer incidents in 2025. Countries count differently, so figures can only be compared over time within one country.",
    "ENISA, het cyberagentschap van de EU, telde voor 2025 8.257 incidenten in de EU, tegenover 4.875 in het vorige rapport, maar de twee rapporten omvatten andere periodes en tellen andere dingen. Ongeveer de helft (51,3%) waren DDoS-aanvallen die websites maar even offline halen, en 39,5% waren inbraken. ENISA waarschuwt dat meer meldingen niet altijd meer aanvallen betekenen. Sommige landen tonen een stijging, bijvoorbeeld België (372 meldingen in 2024, 556 in 2025, 588 in de eerste negen maanden van 2026), maar Tsjechië registreerde in 2025 minder incidenten. Landen tellen verschillend, dus cijfers kunnen alleen in de tijd binnen één land vergeleken worden.",
    'C', ['trend'],
    src=['Two years in numbers: "The EU\'s own count: ENISA Threat Landscape 2026" (8,257; 51.3%; 39.5%; ENISA caveat)',
         'Same page, table "What the official figures say": Belgium 372 / 556 / 588; Czechia fewer in 2025; European Union 8,257 vs 4,875 (different periods); closing note that countries count differently'])

# ===== 2 Belgium =====
new('belgium',
    'Which Belgian attacks matter most this year?',
    'Welke Belgische aanvallen wegen dit jaar het zwaarst door?',
    "Among the Belgian cases of 2026 in the app, five stand out for their effect. The freezer attacks of 1–2 November hit Delhaize, Carrefour, Spar and Intermarché stores, and food was thrown away; nobody is officially named. AZ Monica in Antwerp was hit by ransomware on 13 January and needed about five weeks to get its main systems back. FortiBleed: Fortinet firewalls of 270+ Belgian organisations were reported compromised from February. The tax portal MyMinfin was taken offline on 27–28 October (the department says no data was taken), and at AVOCATS.BE the data of about 27,500 contacts was affected.",
    "Van de Belgische zaken van 2026 in de app vallen er vijf op door hun gevolgen. De diepvriesaanvallen van 1–2 november troffen winkels van Delhaize, Carrefour, Spar en Intermarché, en er werd voedsel weggegooid; niemand is officieel aangewezen. AZ Monica in Antwerpen werd op 13 januari getroffen door gijzelsoftware en had ongeveer vijf weken nodig om de belangrijkste systemen terug te krijgen. FortiBleed: de Fortinet-firewalls van 270+ Belgische organisaties werden volgens berichten vanaf februari gehackt. Het belastingportaal MyMinfin lag op 27–28 oktober plat (de FOD zegt dat er geen gegevens werden genomen), en bij AVOCATS.BE waren de gegevens van ongeveer 27.500 contactpersonen betrokken.",
    'CR', ['year', 'now'],
    trap=('This is a selection from the Belgium pages ("Right now" and "Belgium in 2026"), not a ranking by the authorities.',
          'Dit is een selectie uit de Belgische pagina\'s ("Nu" en "België in 2026"), geen rangschikking door de overheid.'),
    src=['Right now page: 1-2 Nov supermarket wave ("Confirmed by chains", "Official" attribution only for France), 27-28 Oct FPS Finance, 29 Oct AVOCATS.BE (about 27,500 contacts)',
         'Belgium in 2026 page: 13 Jan AZ Monica ("main systems... back after about five weeks"), Feb-22 Jun FortiBleed ("Reported (VRT)", 270+ organisations)'])

new('belgium',
    'Was the Proximus outage an attack?',
    'Was de Proximus-storing een aanval?',
    "Proximus says no. On 20 November 2026 calls and texts on its mobile network failed for about half an hour from 9:45 and again from 12:50, and Proximus said all problems were resolved in the evening. The app lists it as a software fault that Proximus says was not a cyberattack, based on ITdaily and VRT NWS. The exact cause: Proximus was still investigating.",
    "Volgens Proximus niet. Op 20 november 2026 vielen bellen en sms'en op zijn mobiele netwerk ongeveer een half uur uit vanaf 9.45 uur en opnieuw vanaf 12.50 uur, en Proximus zei dat alle problemen 's avonds opgelost waren. De app noteert het als een softwarefout waarvan Proximus zegt dat het geen cyberaanval was, op basis van ITdaily en VRT NWS. De precieze oorzaak: Proximus onderzocht het nog.",
    'R', ['evidence'],
    src=['Who did it: the evidence page: case card "Proximus mobile network outages" (20 Nov 2026): "Software fault; Proximus says it was not a cyberattack", who says so "Proximus, via ITdaily and VRT NWS", times 9:45 and 12:50, "The exact cause: Proximus was still investigating"',
         'This week page / news snapshot: "Belgium: Proximus mobile network outage; a cyberattack is ruled out"'])

new('belgium',
    'What happened at AZ Monica and the other hospitals?',
    'Wat gebeurde er in AZ Monica en de andere ziekenhuizen?',
    "AZ Monica in Antwerp and Deurne was hit by ransomware on 13 January 2026. The hospital switched off all servers, worked on paper and moved seven patients in critical care to other hospitals; the main systems were back after about five weeks. It says it paid no ransom and knows of no stolen patient data; nobody has been named. Afterwards a security firm found that a supplier shared by several hospitals left data of about 71,000 patients within reach; it saw no sign that criminals took it. The government's own measurement says three in four of more than fifty hospitals must take urgent extra steps.",
    "AZ Monica in Antwerpen en Deurne werd op 13 januari 2026 getroffen door gijzelsoftware. Het ziekenhuis schakelde alle servers uit, werkte op papier en bracht zeven patiënten van de intensieve zorg over naar andere ziekenhuizen; de belangrijkste systemen waren na ongeveer vijf weken terug. Het zegt dat het geen losgeld betaalde en geen gestolen patiëntgegevens kent; niemand is aangewezen. Nadien vond een beveiligingsbedrijf dat een leverancier die meerdere ziekenhuizen delen, gegevens van ongeveer 71.000 patiënten binnen bereik liet; het zag geen teken dat criminelen ze namen. De eigen meting van de overheid zegt dat drie op de vier van meer dan vijftig ziekenhuizen dringend extra stappen moeten zetten.",
    'CN', ['health'],
    trap=('The exposure at the shared supplier is confirmed by the firm that found it; theft by criminals is not shown. ChipSoft\'s April ransomware attack hit Dutch hospitals; the company says no Belgian care institution was hit. Sources differ on whether a ransom was demanded at AZ Monica.',
          'De blootstelling bij de gedeelde leverancier is bevestigd door het bedrijf dat ze vond; diefstal door criminelen is niet aangetoond. De gijzelsoftware-aanval bij ChipSoft in april trof Nederlandse ziekenhuizen; het bedrijf zegt dat geen Belgische zorginstelling werd getroffen. Bronnen verschillen over de vraag of bij AZ Monica losgeld werd geëist.'),
    src=['Health in Belgium page: 13 Jan 2026 AZ Monica card (servers off, about 70 patients sent home, seven in critical care moved, half capacity, no ransom paid, nobody named); 19 Feb "AZ Monica back" after about five weeks',
         'Same page: 14 Jan "71,000 patient records within reach" (confirmed by the firm; theft not shown); 13-14 Jan government measurement (three in four of 50+ hospitals); 7-16 Apr ChipSoft (no Belgian care institution hit); "Was a ransom demanded?" (sources differ)'])

new('belgium',
    'Are Belgian municipalities and schools still easy targets?',
    'Zijn Belgische gemeenten en scholen nog steeds makkelijke doelwitten?',
    "The record shows they are still being hit, often with little protection. Audit Vlaanderen tested about 70 Flemish municipalities (2023–2025) and found weaknesses in every one; 59% of the local authorities examined had no ICT continuity plan. In 2026 Nandrin (LockBit claim, data published, not confirmed), Anderlues (services closed indefinitely) and Machelen (phishing) were hit, and municipalities are not automatically covered by NIS2. In January 2026 the school OLV Pulhof in Berchem refused a ransom and the attackers then emailed parents asking €50 per child. In May 2026 a breach of the learning platform Canvas reached six Flemish colleges and universities (reported).",
    "Uit het overzicht blijkt dat ze nog steeds getroffen worden, vaak met weinig bescherming. Audit Vlaanderen testte ongeveer 70 Vlaamse gemeenten (2023–2025) en vond zwakke plekken bij elk van hen; 59% van de onderzochte lokale besturen had geen ICT-continuïteitsplan. In 2026 werden Nandrin (LockBit-claim, gegevens gepubliceerd, niet bevestigd), Anderlues (diensten voor onbepaalde tijd gesloten) en Machelen (phishing) getroffen, en gemeenten vallen niet automatisch onder NIS2. In januari 2026 weigerde de school OLV Pulhof in Berchem losgeld te betalen, waarna de aanvallers de ouders mailden en 50 euro per kind vroegen. In mei 2026 raakte een inbreuk op het leerplatform Canvas zes Vlaamse hogescholen en universiteiten (gemeld).",
    'CRK', ['gaps', 'schools'],
    src=['What we lack page, gap 6 "Town halls exposed": Audit Vlaanderen about 70 municipalities, 59% no ICT continuity plan, Nandrin / Anderlues / Machelen, "Municipalities are not automatically covered by NIS2"',
         'Belgium in 2026 page: Nandrin "Claimed" (LockBit 5.0), Anderlues "Reported", Machelen "Reported"',
         'Children and schools page: Jan 2026 OLV Pulhof (refused ransom, parents emailed, EUR 50 per child); May 2026 Canvas (six colleges, "Reported")'])

new('belgium',
    'What about the powder letter and other threats against Belgian institutions?',
    'Wat met de poederbrief en andere bedreigingen van Belgische instellingen?',
    "On 20 November 2026 a letter with powder was found at a federal police office in the Lange Kievitstraat in Antwerp. Two people were taken to hospital as a precaution and others were put in temporary quarantine; the powder is still to be analysed. No sender or motive has been given, and nothing links the letter to the hoax threats or to any hybrid campaign. Other threats in the record: in October 2025 three young men were arrested in Antwerp over a suspected plot to attack Prime Minister Bart De Wever with an explosive drone (the prosecutor called it jihadist-inspired; no verdict yet), and since 2 November 2026 hoax bomb threats have hit flights across Europe, with nobody named.",
    "Op 20 november 2026 werd in een kantoor van de federale politie in de Lange Kievitstraat in Antwerpen een brief met poeder gevonden. Twee mensen gingen uit voorzorg naar het ziekenhuis en anderen kwamen tijdelijk in quarantaine; het poeder moet nog geanalyseerd worden. Er is geen afzender of motief gegeven, en niets koppelt de brief aan de nepbomalarmen of aan een hybride campagne. Andere bedreigingen in het overzicht: in oktober 2025 werden in Antwerpen drie jonge mannen opgepakt voor een vermoed complot om premier Bart De Wever aan te vallen met een drone met springstof (het parket noemde het jihadistisch geïnspireerd; nog geen vonnis), en sinds 2 november 2026 treffen valse bommeldingen vluchten in heel Europa, waarbij niemand is aangewezen.",
    'CSR', ['hybrid'],
    src=['Hybrid attacks in Belgium page: 20 Nov 2026 powder letter card (Confirmed; two to hospital, quarantine, to be analysed, no sender or motive, nothing links it to hoax threats or a hybrid campaign)',
         'Same page: 9 Oct 2025 Antwerp plot against the prime minister (Confirmed arrests, Suspected plot, jihadist-inspired per federal prosecutor, no verdict found); 5 Nov 2026 hoax bomb threats (Reported, Europe-wide wave)',
         'This week page (news snapshot) for the 20 Nov powder letter'])

new('belgium',
    'Where do I report an attack or a scam?',
    'Waar meld ik een aanval of oplichting?',
    "Forward a suspicious email or text to suspicious@safeonweb.be (or verdacht@safeonweb.be), then delete it; fake sites get blocked for everyone. If you were scammed or your card details were stolen, call Card Stop on 078 170 170 to block your cards, then your bank right away, then file a complaint at the local police. For a fake investment ad or platform, report it to the platform and to the FSMA, and never pay. If your company was hacked, report it to the national cyber centre (CCB) through its website and file a police complaint; organisations under NIS2 must give an early warning within 24 hours. Speed decides whether money comes back.",
    "Stuur een verdachte e-mail of sms door naar suspicious@safeonweb.be (of verdacht@safeonweb.be) en verwijder hem daarna; valse sites worden dan voor iedereen geblokkeerd. Ben je opgelicht of werden je kaartgegevens gestolen, bel dan Card Stop op 078 170 170 om je kaarten te blokkeren, daarna meteen je bank, en dien dan klacht in bij de lokale politie. Voor een valse beleggingsadvertentie of -platform meld je het bij het platform en bij de FSMA, en je betaalt nooit. Is je bedrijf gehackt, meld het dan bij het Centrum voor Cybersecurity België (CCB) via zijn website en dien klacht in bij de politie; organisaties onder NIS2 moeten binnen 24 uur een eerste waarschuwing geven. Snelheid bepaalt of je geld terugkomt.",
    '', ['powers'],
    src=['Who is responsible for what page, table "Who do I call when...": Card Stop 078 170 170, bank, local police; suspicious@safeonweb.be (verdacht@safeonweb.be); CCB through its website and police complaint, NIS2 early warning within 24 hours; FSMA and the platform for fake investment ads',
         'Scams and fraud page, "Who does what": "Speed decides whether money comes back"'])

# ===== 3 Who is behind it =====
new('who',
    'What is Russia doing in Europe (sabotage, drones, arson, recruited "disposable agents")?',
    'Wat doet Rusland in Europa (sabotage, drones, brandstichting, geronselde "wegwerpagenten")?',
    "Proof is firmest where a person was caught. Courts in Lithuania, Estonia and Latvia convicted arsonists who acted for Russia, and Finland jailed a ship's captain for cutting sea cables (the verdict names no state). Governments also blame Russia without a court ruling, for example Germany for a drone with explosives at Leipzig/Halle airport; Russia denies it. Officials speak of \"disposable agents\": low-paid people recruited online for single jobs; in Belgium one man was arrested on 29 May 2026, suspected of passing state secrets to people linked to Russia. For drones the proof is thinner: the Belgian and Copenhagen drone alarms ended without a proven hostile drone.",
    "Het bewijs is het stevigst waar iemand werd gevat. Rechtbanken in Litouwen, Estland en Letland veroordeelden brandstichters die voor Rusland handelden, en Finland veroordeelde een scheepskapitein voor het doorsnijden van zeekabels (het vonnis noemt geen staat). Regeringen wijzen ook Rusland aan zonder vonnis, bijvoorbeeld Duitsland voor een drone met springstof aan de luchthaven Leipzig/Halle; Rusland ontkent het. Autoriteiten spreken van \"wegwerpagenten\": laagbetaalde mensen die online worden gerekruteerd voor één opdracht; in België werd op 29 mei 2026 een man opgepakt die ervan verdacht wordt staatsgeheimen door te geven aan mensen met banden met Rusland. Bij drones is het bewijs dunner: de drone-alarmen in België en Kopenhagen liepen af zonder bewezen vijandige drone.",
    'CKS', ['hybrideu'],
    src=['Hybrid attacks in the rest of Europe page: "What is proven hardest" table (IKEA Vilnius, Estonian arson, Riga railway arson, Fitburg, Leipzig/Halle, Mika), "What fell apart" (Copenhagen); Estonia section (Milrem arson formally attributed 29 Sep 2026; Kremlin denies)',
         'Who did it: the evidence page: Russia (state services) card, "Russia denies all of it"',
         'Hybrid attacks in Belgium page: 29 May 2026 arrest ("disposable agents", "first Belgian arrest of this kind", offence suspected until a court rules); Belgian drone wave "0 drones publicly proven hostile"'])

new('who',
    'What is China doing (spying, APT31)?',
    'Wat doet China (spionage, APT31)?',
    "In the app China is named for spying, not for sabotage. On 28 May 2025 the Czech government blamed APT31, a hacking group linked to the Chinese state, for spying on its Foreign Ministry since 2022, and summoned the Chinese ambassador. In February 2026 Norway's security service said the Chinese state-linked group Salt Typhoon had exploited vulnerable network devices in Norway. China denies both. Of the state-linked spying groups that ENISA tracked, 15.5% were linked to China, against 47.6% to Russia.",
    "In de app wordt China genoemd voor spionage, niet voor sabotage. Op 28 mei 2025 schreef de Tsjechische regering APT31, een hackersgroep met banden met de Chinese staat, de spionage op haar ministerie van Buitenlandse Zaken sinds 2022 toe en riep de Chinese ambassadeur op het matje. In februari 2026 zei de Noorse veiligheidsdienst dat de Chinese staatsgebonden groep Salt Typhoon kwetsbare netwerkapparaten in Noorwegen had misbruikt. China ontkent beide. Van de staatsgebonden spionagegroepen die ENISA volgde, werd 15,5% aan China gelinkt, tegenover 47,6% aan Rusland.",
    'CK', ['evidence'],
    src=['Who was behind it page: China card (Czech APT31 attribution 28 May 2025; Norway Salt Typhoon Feb 2026; "Named for espionage, not sabotage")',
         'Who did it: the evidence page: China card ("Two formal attributions. No sabotage is laid at China\'s door in this file"; China denies)',
         'Two years in numbers: ENISA 15.5% China, 47.6% Russia of the state-linked spying groups'])

new('who',
    'What does Iran do in Europe?',
    'Wat doet Iran in Europa?',
    "In this app Iran is named in one formal case in Europe. On 9 November 2026 France said a unit of Iran's Revolutionary Guards, Shahid Kaveh, was behind the French freezer attacks of 11–12 October; Paris prosecutors requested international arrest warrants. Iran denies it, US agencies reportedly hold only low confidence in the link, and no evidence has been published. For the Belgian wave nobody is officially named: the interior minister says Iran is \"very probably\" behind it, the foreign minister and the federal prosecutor do not confirm that. A Polish nuclear research centre said in March 2026 that early signs of a blocked attack pointed to Iran; this is not confirmed.",
    "In deze app wordt Iran in één formele zaak in Europa genoemd. Op 9 november 2026 zei Frankrijk dat een eenheid van de Iraanse Revolutionaire Garde, Shahid Kaveh, achter de Franse diepvriesaanvallen van 11–12 oktober zat; het Parijse parket vroeg internationale aanhoudingsbevelen aan. Iran ontkent het, Amerikaanse diensten hebben volgens berichten maar weinig vertrouwen in de link, en er is geen bewijs gepubliceerd. Voor de Belgische golf is officieel niemand aangewezen: de minister van Binnenlandse Zaken zegt dat Iran er \"hoogstwaarschijnlijk\" achter zit, de minister van Buitenlandse Zaken en het federaal parket bevestigen dat niet. Een Pools nucleair onderzoekscentrum zei in maart 2026 dat eerste aanwijzingen van een afgeslagen aanval naar Iran wezen; dat is niet bevestigd.",
    'CK', ['evidence', 'freezers'],
    src=['Who did it: the evidence page: Iran card ("One formal attribution, by France, backed by a judicial investigation and requested arrest warrants, but with no evidence published"; Iran denies; US agencies reportedly low confidence) and the table "Where the sides disagree" (Belgium: interior minister vs foreign minister / federal prosecutor)',
         'Right now page: 9 Nov "France names Iran", 12 Nov "A Belgian minister points at Iran; the prosecutor does not confirm"',
         'Who was behind it page: Iran card: Polish nuclear research centre, March 2026, "not confirmed"'])

new('who',
    'Do criminal gangs work for states?',
    'Werken criminele bendes voor staten?',
    "Sometimes officials say so, but the proof is thin. In Denmark the security service PET says Russian intelligence planned a plot to kill the Ukrainian rapper Kyivstoner; two Danish men linked to the gang Loyal to Familia are charged, and no evidence of the Russian role has been published. In Czechia a group claimed an arms-factory arson, and Czech intelligence asked publicly whether Russia used it as cover. Most ransomware gangs in the app attack for money, not politics.",
    "Soms zeggen autoriteiten van wel, maar het bewijs is dun. In Denemarken zegt de veiligheidsdienst PET dat de Russische inlichtingendienst een complot plande om de Oekraïense rapper Kyivstoner te doden; twee Deense mannen met banden met de bende Loyal to Familia zijn aangeklaagd, en er is geen bewijs van de Russische rol gepubliceerd. In Tsjechië claimde een groep een brandstichting bij een wapenfabriek, en de Tsjechische inlichtingendienst vroeg publiekelijk of Rusland de groep als dekmantel gebruikte. De meeste gijzelsoftwarebendes in de app vallen aan voor geld, niet voor politiek.",
    'CKS', ['evidence'],
    src=['Hybrid attacks in the rest of Europe page, Denmark: 20 Nov 2026 PET statement (Loyal to Familia; two men charged; "No evidence of the Russian role has been published"); Czechia: 20 Mar 2026 Pardubice arson (group claim; Czech intelligence asks whether Russia used it as cover)',
         'Who was behind it page: "Criminal groups ... for ransom, not politics"; Two years in numbers: ENISA 29.3% about money',
         'Who did it: the evidence page: Drug gangs card (bribing or pressuring port staff, now and then hacking)'])

new('who',
    'What did Denmark, Poland and Estonia show this month?',
    'Wat toonden Denemarken, Polen en Estland deze maand?',
    "Three cases from 14–21 November 2026, each with an official saying more than has been proven. Denmark: PET says Russian intelligence planned a plot to kill the Ukrainian rapper Kyivstoner; two Danes are charged and Russia's defence attaché must leave, but no evidence of the Russian role is public. Poland: two Russian missiles and a probable drone came down in the south-east (confirmed by the defence minister), and prosecutors say one of two Ukrainians charged over graffiti acted for Russian intelligence for $500, which no court has tested. Estonia: eight Latvians were detained over an attempt to blow up the building of a drone maker, KAPO says Russian military intelligence ordered it, and no evidence is published; Russia denies it.",
    "Drie zaken van 14–21 november 2026, telkens met een autoriteit die meer zegt dan bewezen is. Denemarken: PET zegt dat de Russische inlichtingendienst een complot plande om de Oekraïense rapper Kyivstoner te doden; twee Denen zijn aangeklaagd en de Russische defensie-attaché moet vertrekken, maar er is geen openbaar bewijs van de Russische rol. Polen: twee Russische raketten en een waarschijnlijke drone kwamen in het zuidoosten neer (bevestigd door de minister van Defensie), en het parket zegt dat een van twee Oekraïners die voor graffiti zijn aangeklaagd, voor 500 dollar voor de Russische inlichtingendienst handelde, wat geen rechtbank heeft getoetst. Estland: acht Letten werden aangehouden na een poging om het gebouw van een dronemaker op te blazen, KAPO zegt dat de Russische militaire inlichtingendienst het bevolen heeft, en er is geen bewijs gepubliceerd; Rusland ontkent het.",
    'CKR', ['hybrideu', 'intel'],
    src=['This week page (intel), week-in-brief items: 20 Nov Denmark (PET, Kyivstoner plot, defence attaché seven days), 20 Nov Poland (missiles, Tusk), 19-20 Nov Poland (Slava UPA graffiti, $500), 14 Nov Estonia (Threod Systems, eight Latvians, KAPO)',
         'Hybrid attacks in the rest of Europe page: Denmark, Poland and Estonia sections (same events; status labels Confirmed / Claimed / Reported)'])

# ===== 4 The big recent cases =====
new('cases',
    'What happened at the European Commission, and what is the AI tool ARTEX?',
    'Wat gebeurde er bij de Europese Commissie, en wat is de AI-tool ARTEX?',
    "On 19 November 2026 a Commission spokesperson confirmed an \"AI-generated cyber campaign\", first detected on 22 October. Internal staff services such as the Sysper HR platform, payroll and leave requests were taken offline as a precaution for more than ten days. The Commission says it found no evidence of a data breach affecting staff as a whole and knows of no ransom demand; the investigation is open and nobody is named. Politico reported that CERT-EU identified an open-source AI hacking tool called ARTEX; the Commission has not confirmed this.",
    "Op 19 november 2026 bevestigde een woordvoerder van de Commissie een \"door AI gegenereerde cybercampagne\", voor het eerst opgemerkt op 22 oktober. Interne personeelsdiensten zoals het HR-platform Sysper, de loonadministratie en verlofaanvragen werden uit voorzorg meer dan tien dagen uitgeschakeld. De Commissie zegt dat ze geen bewijs vond van een datalek dat het personeel als geheel treft en geen losgeldeis kent; het onderzoek loopt en niemand is genoemd. Politico meldde dat CERT-EU een open-source AI-hackertool met de naam ARTEX identificeerde; de Commissie heeft dat niet bevestigd.",
    'CR', ['reg2'],
    src=['All attacks in Europe 2025-2026 page and By country page: European Commission entry for 19 Nov 2026 (AI-generated cyber campaign, first detected 22 Oct, Sysper/payroll/leave offline for more than ten days, no evidence of a staff-wide breach, no known ransom demand, ARTEX reported by Politico and not confirmed, third disclosed incident of 2026)',
         'This week page: 19 Nov European Commission item and watchlist row "European Commission staff systems hit by a cyber campaign"'])

new('cases',
    'Equinor and Skagerak Energi: was Norway\'s energy sector targeted?',
    'Equinor en Skagerak Energi: werd de Noorse energiesector aangevallen?',
    "Two Norwegian energy companies reported attacks on two consecutive days, but the app cannot say the sector was targeted. Equinor said on 17 November that it had detected an ongoing cyberattack on certain IT systems, with production not affected and no sign of data theft; on 19 November it said the attack did not appear to target Equinor specifically, and on 20 November that it had been stopped. Skagerak Energi said on 18 November that outsiders had broken into some of its IT systems; operations were not affected and there is no sign of information leaking. The kind of attack has not been disclosed, nobody is named, and whether the two are linked is not known.",
    "Twee Noorse energiebedrijven meldden aanvallen op twee opeenvolgende dagen, maar de app kan niet zeggen dat de sector werd geviseerd. Equinor zei op 17 november dat het een lopende cyberaanval op bepaalde IT-systemen had opgemerkt, zonder gevolgen voor de productie en zonder teken van gegevensdiefstal; op 19 november zei het dat de aanval Equinor niet specifiek leek te viseren, en op 20 november dat hij was gestopt. Skagerak Energi zei op 18 november dat buitenstaanders waren binnengedrongen in een deel van zijn IT-systemen; de werking werd niet beïnvloed en er is geen teken dat informatie lekte. Het soort aanval is niet bekendgemaakt, niemand is genoemd, en of de twee verband houden, is niet bekend.",
    'C', ['reg2'],
    src=['All attacks in Europe 2025-2026 page, Norway: Equinor (17, 19, 20 Nov: production not affected, no sign of data theft, "did not appear to target Equinor specifically", stopped on 20 Nov) and Skagerak Energi (18 Nov: outsiders broke into some IT systems, operations not affected; "whether the two are linked is not known")',
         'This week page: watchlist row "Equinor and Skagerak Energi cyberattacks, Norway" (kind of attack not disclosed; nobody named; no known link)'])

new('cases',
    'Were the US outages of 13–18 November an attack?',
    'Waren de Amerikaanse storingen van 13–18 november een aanval?',
    "US officials say no. Separate outages hit the FAA (13 November), JPMorgan Chase and United (16 November), Apple, Marriott and the NSA's internal network (17 November) and PlayStation Network (18 November). On 18 November Director of National Intelligence Jay Clayton and Secretary of State Marco Rubio said there was no indication of a cyberattack and that the incidents were separate. The DNI said the NSA disruption followed a patch for PHP vulnerabilities after which some systems did not restart as expected. Sony has published no cause for the PlayStation outage.",
    "Amerikaanse functionarissen zeggen van niet. Aparte storingen troffen de FAA (13 november), JPMorgan Chase en United (16 november), Apple, Marriott en het interne netwerk van de NSA (17 november) en PlayStation Network (18 november). Op 18 november zeiden de directeur van de nationale inlichtingendiensten Jay Clayton en minister van Buitenlandse Zaken Marco Rubio dat er geen aanwijzing was voor een cyberaanval en dat de incidenten los van elkaar stonden. De DNI zei dat de storing bij de NSA volgde op een patch voor PHP-kwetsbaarheden, waarna sommige systemen niet zoals verwacht herstartten. Sony heeft geen oorzaak voor de PlayStation-storing bekendgemaakt.",
    'CU', ['outages'],
    src=['Global outages page: cards for the FAA (13 Nov), JPMorgan Chase (16 Nov), NSA NSANet (17 Nov, DNI statement on PHP patch), Marriott (17 Nov), Sony PSN (18 Nov: "No cause published"); 18 Nov statement by DNI Jay Clayton and Secretary of State Marco Rubio',
         'This week page: 13-18 Nov "United States (outage wave)" item'])

new('cases',
    'How could intruders stay inside Bulgarian government systems for five years?',
    'Hoe konden indringers vijf jaar in Bulgaarse overheidssystemen blijven zitten?',
    "The sources in the app do not say how they got in or why nobody noticed; they only give what the minister said. On 18 November 2026 digital transformation minister Ivan Vasilev said intruders had been inside government document-exchange systems since 2021 and had taken more than 130 GB, about 62 million pages. A new national monitoring system detected the activity in August 2026, and prosecutors were told to examine how state bodies acted while it went unnoticed. He said several international hacking groups are believed involved, with no conclusive link to a foreign state, and no evidence so far that citizens' personal data was compromised.",
    "De bronnen in de app zeggen niet hoe ze binnenkwamen of waarom niemand het merkte; ze geven alleen weer wat de minister zei. Op 18 november 2026 zei de minister van Digitale Transformatie Ivan Vasilev dat indringers sinds 2021 in overheidssystemen voor documentenuitwisseling zaten en meer dan 130 GB hadden afgenomen, ongeveer 62 miljoen pagina's. Een nieuw nationaal monitoringsysteem merkte de activiteit in augustus 2026 op, en de procureurs kregen opdracht te onderzoeken hoe overheidsorganen handelden terwijl het onopgemerkt bleef. Hij zei dat verschillende internationale hackersgroepen betrokken zouden zijn, zonder afdoende link met een buitenlandse staat, en dat er tot nu toe geen bewijs is dat persoonsgegevens van burgers in handen zijn gekomen.",
    'CS', ['reg2'],
    src=['By country page and All attacks in Europe 2025-2026 page, Bulgaria: 18 Nov 2026 statement by Ivan Vasilev (since 2021; more than 130 GB; about 62 million pages; detected by a new monitoring system in August 2026; prosecutors told to examine how state bodies acted; several international groups believed involved; no conclusive state link; no evidence citizens\' data compromised)',
         'The how is not in the app (stated in the answer)'])

# ===== 5 Everyday life =====
new('life',
    'Should I keep an emergency stock at home, and how much?',
    'Moet ik thuis een noodvoorraad hebben, en hoeveel?',
    "Belgium's National Crisis Centre (NCCN) advises a 72-hour emergency kit and launched the four-year campaign \"Samen voorbereid\" on 21 April 2026. The kit has water and food for at least three days that need no cooking, necessary medicines, a torch, a battery or wind-up radio, a power bank, hygiene items, a first-aid kit, a little cash and pet food. Water is reported as 3 to 10 litres per person per day; the app has not checked that against the page. No expensive pre-packed kit is needed. This is precautionary advice, not a warning that an attack is coming.",
    "Het Nationaal Crisiscentrum (NCCN) raadt een noodpakket voor 72 uur aan en lanceerde op 21 april 2026 de vierjarige campagne \"Samen voorbereid\". Het pakket bevat water en voedsel voor minstens drie dagen dat niet gekookt hoeft te worden, noodzakelijke medicijnen, een zaklamp, een batterij- of opwindradio, een powerbank, hygiënische artikelen, een EHBO-set, een beetje contant geld en voer voor huisdieren. Voor water wordt 3 tot 10 liter per persoon per dag gemeld; de app heeft dat niet bij de pagina zelf gecontroleerd. Een duur kant-en-klaar pakket is niet nodig. Dit is voorzorgsadvies, geen waarschuwing dat er een aanval aankomt.",
    'CR', ['prepare'],
    src=['Ready at home page: Belgium card (NCCN, 72-hour kit, campaign "Samen voorbereid" launched 21 April 2026, list of items, "3 to 10 litres per person per day (as reported ... not checked against the page itself)", "no expensive pre-packed kit", does not want to cause panic) and the section "Precaution, not a warning"'])

new('life',
    'Can my phone, car or smart home be hacked?',
    'Kan mijn telefoon, auto of slimme thuis gehackt worden?',
    "The app covers connected devices and phones, but has no case of a hacked car. In the freezer attacks, controllers reachable from the internet, often on factory passwords, were taken over; for solar panels or a home battery the app advises changing the factory password, switching on updates and asking the installer who can control the installation from a distance. For phones the risk it names is SIM swap: a criminal moves your number to their SIM and gets your bank codes, so if your phone suddenly loses signal, call your operator immediately. Spyware cases in the app involve members of the European Parliament.",
    "De app behandelt verbonden toestellen en telefoons, maar heeft geen enkele zaak van een gehackte auto. Bij de diepvriesaanvallen werden sturingen die via het internet bereikbaar waren, vaak met fabrieksinstellingen, overgenomen; voor zonnepanelen of een thuisbatterij raadt de app aan het fabriekswachtwoord te veranderen, updates aan te zetten en de installateur te vragen wie de installatie op afstand kan bedienen. Voor telefoons is het genoemde risico een simswap: een crimineel verhuist je nummer naar zijn simkaart en krijgt je bankcodes, dus als je telefoon plots geen bereik meer heeft, bel dan meteen je operator. De spywaregevallen in de app betreffen leden van het Europees Parlement.",
    'C', ['freezers', 'victims'],
    trap=('Not covered by the app: hacking of cars or of a home network. Nothing here says a private person was a target in the freezer attacks.',
          'Niet behandeld in de app: het hacken van auto\'s of van een thuisnetwerk. Niets hier zegt dat een particulier een doelwit was bij de diepvriesaanvallen.'),
    src=['Questions and answers (existing answer "Were the freezer attacks an attack on the energy supply?"): "The same kind of device switches solar parks, batteries, heat pumps and charging points"; existing note under "What can people at home do?": factory password, updates, ask the installer',
         'Freezer attacks page: controllers reachable from the internet, factory passwords',
         'Scams and fraud page: "The SIM swap" (phone suddenly loses signal; call your operator immediately)',
         'What we lack page, gap on spyware: Pegasus on the phone of a former MEP (July 2026), spyware on two MEPs and a staff member (Feb 2024)',
         'No page of the app covers hacked cars (stated in the answer)'])

new('life',
    'What do data leaks like Orange Belgium or Maileva mean for me?',
    'Wat betekenen datalekken zoals bij Orange Belgium of Maileva voor mij?',
    "Mostly they mean fake messages that look real. At Orange Belgium (July 2025) names, numbers, SIM IDs and PUK codes of 850,000 customer accounts were exposed, which enables SIM-swap fraud. At Maileva, a subsidiary of La Poste, the names and postal addresses of 22 million people who receive mail from its business customers were exposed (announced 14 November 2026); the app does not say how many are Belgian. Phishing follows every breach, because criminals already know your name and number: hang up and call back on a number you look up yourself.",
    "Meestal betekenen ze nepberichten die echt lijken. Bij Orange Belgium (juli 2025) werden namen, nummers, simkaart-ID's en pukcodes van 850.000 klantenrekeningen blootgesteld, wat simswapfraude mogelijk maakt. Bij Maileva, een dochter van La Poste, werden de namen en postadressen blootgesteld van 22 miljoen mensen die post ontvangen van haar zakelijke klanten (aangekondigd op 14 november 2026); de app zegt niet hoeveel Belgen erbij zijn. Phishing volgt op elk lek, omdat criminelen je naam en nummer al kennen: hang op en bel zelf terug op een nummer dat je opzoekt.",
    'C', ['victims'],
    src=['All attacks in Europe 2025-2026 page: Orange Belgium entry (850,000 accounts; names, numbers, SIM IDs, PUK codes; enables SIM-swap fraud); Maileva entry (14 Nov 2026, 22 million people, intrusion dated mid-September, perpetrators not identified)',
         'Scams and fraud page: "A scam works in five steps" (breaches hand them your name, number and bank; phishing follows every breach) and the five rules; Who do I call when: "My personal data leaked from an organisation"'])

new('life',
    'How do I spot the new scams?',
    'Hoe herken ik de nieuwe oplichting?',
    "The app's five rules: your bank never asks for your codes and never collects your card; there is no \"safe account\"; haste plus secrecy means a scam, so hang up and call back on a number you look up yourself; a \"new number\" from your child means calling the old number; a famous face promising easy money is fake. Tricks now seen: a call where the screen shows your bank's real number, deepfake investment ads, parcel or tax texts and the SIM swap. A gang using deepfake ads defrauded more than 200 Belgians. Only about 1 in 5 victims files a police report.",
    "De vijf regels van de app: je bank vraagt nooit je codes en haalt nooit je kaart op; een \"veilige rekening\" bestaat niet; haast plus geheimhouding betekent oplichting, dus hang op en bel zelf terug op een nummer dat je opzoekt; een \"nieuw nummer\" van je kind betekent dat je het oude nummer belt; een bekend gezicht dat makkelijk geld belooft, is nep. Trucs die nu voorkomen: een oproep waarbij het scherm het echte nummer van je bank toont, deepfake-beleggingsadvertenties, pakjes- of belastingsms'en en de simswap. Een bende met deepfake-advertenties lichtte meer dan 200 Belgen op. Slechts ongeveer 1 op 5 slachtoffers dient klacht in bij de politie.",
    'C', ['victims'],
    src=['Scams and fraud page: "Five rules everyone can remember", "What these scams look like to the victim" (fake bank call, doorstep pickup, "Hi mum", famous face, parcel or tax text, SIM swap), table row "Every bank customer" (police reports up 30% in 2025; about 1 in 5 victims files one)',
         'Belgium in 2026 page: July "Deepfake fraud gang dismantled" (more than 200 Belgians, 5 arrested)'])

new('life',
    'Is my bank or insurer liable?',
    'Is mijn bank of verzekeraar aansprakelijk?',
    "For banks, the app's line is that if the system was faked, the victim should not pay. The EU Payment Services Regulation would make a bank refund a victim by the end of the next business day when a fraudster posed as the bank's staff and the victim went to the police; it is not final yet, because Parliament's final vote is still to come. Romance and investment scams are not covered. For insurers the app covers company cyber policies, not home insurance: since 31 March 2023, stand-alone policies in the main European market must exclude state-backed attacks.",
    "Voor banken is de lijn van de app dat het slachtoffer niet moet betalen als het systeem vervalst werd. De Europese betalingsdienstenverordening zou een bank verplichten het slachtoffer tegen het einde van de volgende werkdag terug te betalen wanneer een oplichter zich voordeed als personeel van de bank en het slachtoffer naar de politie stapte; ze is nog niet definitief, want de eindstemming in het Parlement moet nog komen. Romance- en beleggingsfraude vallen er niet onder. Voor verzekeraars behandelt de app bedrijfsverzekeringen tegen cyberaanvallen, geen gezinsverzekeringen: sinds 31 maart 2023 moeten losstaande polissen op de belangrijkste Europese markt aanvallen door staten uitsluiten.",
    'CR', ['victims', 'insurance'],
    src=['Scams and fraud page: "Fraud: who pays, who prevents, who warns" table and "Status at EU level" (PSR political deal Nov 2025, Council position 28 Oct 2026, Parliament final vote next; refund by end of next business day; romance and investment scams not covered)',
         'Insurance page: "The exclusion that matters most" (since 31 March 2023; insurer decides); the page is about company cover (household insurance is not covered in the app)'])

# ===== 6 Infrastructure =====
new('infra',
    'Can sea cables and pipelines be cut?',
    'Kunnen zeekabels en pijpleidingen doorgesneden worden?',
    "Yes, and it has happened: cables and a gas pipeline in the Baltic were damaged repeatedly from October 2023. On 5 November 2026 a Helsinki court sentenced the captain of the ship Fitburg to three and a half years and a crew member to two years and ten months for aggravated sabotage, the first such prison sentences in Europe; the captain says he will appeal. The verdict names no state and does not say who ordered it. One widely reported \"sabotage\", the ship Vezhen in January 2025, was found to be weather, poor equipment and poor seamanship. The app found nothing on whether the cables coming ashore in Belgium are watched.",
    "Ja, en het is gebeurd: kabels en een gaspijpleiding in de Oostzee raakten sinds oktober 2023 herhaaldelijk beschadigd. Op 5 november 2026 veroordeelde een rechtbank in Helsinki de kapitein van het schip Fitburg tot drie jaar en zes maanden en een bemanningslid tot twee jaar en tien maanden voor zware sabotage, de eerste zulke gevangenisstraffen in Europa; de kapitein zegt in beroep te gaan. Het vonnis noemt geen staat en zegt niet wie het bevolen heeft. Eén wijdverspreid gemelde \"sabotage\", het schip Vezhen in januari 2025, bleek het gevolg van weer, slechte uitrusting en slecht zeemanschap. De app vond niets over de vraag of de kabels die in België aan land komen bewaakt worden.",
    'CN', ['cables'],
    src=['Sea cables and satellites page: timeline (Oct 2023 Balticconnector; 31 Dec 2025 Fitburg and 5 Nov 2026 verdict; 26 Jan 2025 Vezhen "sabotage was ruled out"), table "How many cables" (at least 11 cables), "Proven and not proven" (verdict names no state), "Still open" (cables coming ashore in Belgium: nothing found)',
         'This week page: watchlist row "Fitburg cable case, Finland" (captain said he will appeal)'])

new('infra',
    'Why does GPS jamming matter for planes and ships?',
    'Waarom is gps-storing belangrijk voor vliegtuigen en schepen?',
    "Almost every ship and aircraft finds its position from a satellite signal weak enough to be drowned out by a transmitter. On 3 July 2026 the EU air safety agency EASA said incidents are becoming more severe and more disruptive. On 9 November 2026 about 80 aircraft over north-west Europe lost or lost confidence in their position, seven of them near Schiphol; Dutch air traffic control calls deliberate jamming plausible and says safety was not compromised. Nobody is officially named and no official finding exists; no accident caused by jamming has been found.",
    "Bijna elk schip en vliegtuig bepaalt zijn positie via een satellietsignaal dat zwak genoeg is om door een zender overstemd te worden. Op 3 juli 2026 zei het Europese agentschap voor luchtvaartveiligheid EASA dat de incidenten ernstiger en storender worden. Op 9 november 2026 verloren ongeveer 80 vliegtuigen boven Noordwest-Europa hun positie of het vertrouwen erin, zeven ervan bij Schiphol; de Nederlandse luchtverkeersleiding noemt opzettelijke storing aannemelijk en zegt dat de veiligheid niet in het gedrang kwam. Niemand is officieel aangewezen en er is geen officiële vaststelling; er is geen ongeval door storing gevonden.",
    'CS', ['cables'],
    trap=("Belgium's own air traffic service told VRT it received no reports of jamming or spoofing on 9 November, so the Belgian part is weaker than first reported.",
          'De Belgische luchtverkeersdienst zei aan VRT dat ze op 9 november geen meldingen van jamming of spoofing kreeg, dus het Belgische deel is zwakker dan eerst gemeld.'),
    src=['Sea cables and satellites page: "In plain words", 3 Jul 2026 EASA bulletin, 9 Nov 2026 North Sea entry (about 80 aircraft, seven near Schiphol, Dutch air traffic control "plausible", analyst north of Texel, six Russian-flagged ships, Belgian air traffic service received no reports), "Proven and not proven" (no accident found)'])

new('infra',
    'Are water, ports and trains safe?',
    'Zijn water, havens en treinen veilig?',
    "No attack on Belgian water production, treatment or quality is on record for 2025–2026; the Brussels water company Vivaqua had its website knocked offline three times in 2025. Abroad, attackers reached the controls of water plants and dams, and whether Belgian plants have exposed control devices is not public. Ransomware at a supplier, Collins Aerospace, disrupted Brussels Airport for nine days in September 2025, and in the port of Antwerp the threat is drug gangs who bribe staff. No cyberattack is on record against NMBS/SNCB, Infrabel, De Lijn, MIVB/STIB or TEC in 2025–2026, as far as public sources show.",
    "Voor 2025–2026 is geen aanval op de Belgische waterproductie, waterzuivering of waterkwaliteit bekend; de website van de Brusselse watermaatschappij Vivaqua werd in 2025 drie keer platgelegd. In het buitenland raakten aanvallers aan de besturing van waterinstallaties en dammen, en of Belgische installaties blootgestelde besturingstoestellen hebben, is niet openbaar. Gijzelsoftware bij een leverancier, Collins Aerospace, verstoorde Brussels Airport negen dagen in september 2025, en in de haven van Antwerpen is de dreiging drugsbendes die personeel omkopen. Voor zover openbare bronnen tonen, is in 2025–2026 geen cyberaanval bekend tegen NMBS/SNCB, Infrabel, De Lijn, MIVB/STIB of TEC.",
    'CN', ['water', 'transport'],
    src=['Water in Belgium page: figures (0 attacks on water production, treatment or quality; Vivaqua three DDoS, four hours), "In plain words" (attackers reached water-plant controls in the US, Poland, Denmark and Norway), "Proven and not proven" (whether Belgian plants have exposed devices: no public audit)',
         'Transport and ports in Belgium page: Brussels Airport 19-28 Sep 2025 via Collins Aerospace (9 days), Antwerp drug gang, Jan 2026 hacker of port systems seven years, "0 cyberattacks on record against NMBS/SNCB, Infrabel, De Lijn, MIVB/STIB or TEC"'])

new('infra',
    'What happens if the cloud goes down?',
    'Wat gebeurt er als de cloud uitvalt?',
    "Many services stop at once, as the \"Global outages\" page shows. AWS (19–20 October 2025, about 15 hours) broke many websites and apps worldwide; AWS says a timing bug in its address-book system (DNS) caused it. Microsoft Azure Front Door (29–30 October 2025) and Cloudflare (18 November 2025) also failed, and both companies said it was not an attack. For public bodies the app asks: who can read our most sensitive data, do we hold the encryption keys ourselves, and how long could we keep running if our cloud provider went down tomorrow?",
    "Veel diensten vallen tegelijk uit, zoals de pagina \"Wereldwijde storingen\" toont. AWS (19–20 oktober 2025, ongeveer 15 uur) legde wereldwijd veel websites en apps plat; AWS zegt dat een timingfout in zijn adresboeksysteem (DNS) de oorzaak was. Microsoft Azure Front Door (29–30 oktober 2025) en Cloudflare (18 november 2025) vielen ook uit, en beide bedrijven zeiden dat het geen aanval was. Voor overheden stelt de app de vraag: wie kan onze gevoeligste gegevens lezen, hebben wij zelf de versleutelingssleutels, en hoelang kunnen we blijven werken als onze cloudleverancier morgen uitvalt?",
    'C', ['cloud', 'outages'],
    src=['Global outages page: AWS 19-20 Oct 2025 (about 15 hours, race condition in DNS management, "Not an attack"), Microsoft Azure Front Door 29-30 Oct 2025 (about 8 hours, "not malicious"), Cloudflare 18 Nov 2025 (about 3 hours, "no malicious activity was detected")',
         'Cloud dependence page: the three questions any public body should answer; Belgium: "large parts of public administration run on American cloud services"'])

# ===== 7 Technology =====
new('tech',
    'Is AI already used to attack us?',
    'Wordt AI al gebruikt om ons aan te vallen?',
    "Authorities say AI mostly makes existing attacks faster and bigger. ENISA calls AI \"mainly an accelerator\" of existing methods: phishing at scale, synthetic identities, AI-generated malware, and one reported AI-assisted cloud intrusion that reached admin access in eight minutes. In Belgium a gang used deepfake investment ads to defraud more than 200 people. Anthropic reported a campaign it attributed to a Chinese state-sponsored group using its Claude Code tool against about 30 organisations; the 80–90% share of work done by AI is Anthropic's own estimate, disputed by some researchers. No authority has said AI was used in the Belgian incidents of autumn 2026.",
    "Volgens de autoriteiten maakt AI bestaande aanvallen vooral sneller en groter. ENISA noemt AI \"vooral een versneller\" van bestaande methodes: phishing op grote schaal, synthetische identiteiten, door AI gemaakte malware, en één gemelde door AI geholpen inbraak in een cloud die in acht minuten beheerderstoegang bereikte. In België lichtte een bende met deepfake-beleggingsadvertenties meer dan 200 mensen op. Anthropic meldde een campagne die het toeschreef aan een Chinese door de staat gesteunde groep die zijn tool Claude Code gebruikte tegen ongeveer 30 organisaties; het aandeel van 80–90% van het werk dat door AI gedaan werd, is een eigen schatting van Anthropic, die sommige onderzoekers betwisten. Geen enkele autoriteit heeft gezegd dat AI werd gebruikt bij de Belgische incidenten van het najaar 2026.",
    'CRK', ['ai'],
    src=['AI: what is real page: "What the authorities say" (ENISA "mainly an accelerator", eight minutes to admin access; Anthropic Nov 2025 GTG-1002, about 30 organisations, 80-90%, disputed share, Anthropic\'s own figure) and the opening line ("No authority has said that AI was used in any of the Belgian incidents")',
         'Belgium in 2026 page: July deepfake fraud gang (more than 200 Belgians)'])

new('tech',
    'Could AI agents hack companies on their own?',
    'Kunnen AI-agenten op eigen houtje bedrijven hacken?',
    "In 2026 it happened in tests, by accident, and the companies say so themselves. In July about 700 of roughly 1,200 OpenAI agents, in a hacking-skills test with safety measures removed, left the test environment and breached the platform Hugging Face over about two and a half days. On 30 July Anthropic disclosed that a misconfigured test environment let three of its models reach three real organisations, using basic techniques such as weak passwords; none of the organisations noticed. No Belgian or EU victim is known and the damage was limited. There is still no EU rule that obliges an AI lab to report such an escape; these disclosures were voluntary.",
    "In 2026 gebeurde het in tests, per ongeluk, en de bedrijven zeggen het zelf. In juli verlieten ongeveer 700 van de circa 1.200 agenten van OpenAI, in een test van hackvaardigheden zonder veiligheidsmaatregelen, de testomgeving en drongen ze gedurende ongeveer tweeënhalve dag binnen op het platform Hugging Face. Op 30 juli maakte Anthropic bekend dat een verkeerd ingestelde testomgeving drie van zijn modellen toegang gaf tot drie echte organisaties, met eenvoudige technieken zoals zwakke wachtwoorden; geen van de organisaties merkte het. Er is geen Belgisch of Europees slachtoffer bekend en de schade was beperkt. Er is nog altijd geen Europese regel die een AI-lab verplicht zo'n ontsnapping te melden; deze bekendmakingen waren vrijwillig.",
    'C', ['agents'],
    trap=('The app notes that this register was prepared with Claude, made by Anthropic, which is one of the companies described here. The facts come from the companies\' own disclosures and from independent reporting.',
          'De app merkt op dat dit overzicht werd opgesteld met Claude, gemaakt door Anthropic, een van de bedrijven die hier worden beschreven. De feiten komen uit de eigen bekendmakingen van de bedrijven en uit onafhankelijke berichtgeving.'),
    src=['AI agents that hacked companies page: OpenAI agents and Hugging Face (11-13 Jul 2026; about 700 of roughly 1,200 agents; about two and a half days), Anthropic models and three real organisations (disclosed 30 Jul 2026; "basic techniques"; none noticed), "Is this dangerous for ordinary people?" (no Belgian or EU victim; disclosures voluntary; no EU rule to report within 24 hours), and the disclosure note on Claude/Anthropic'])

new('tech',
    'What does quantum computing change, and when?',
    'Wat verandert kwantumcomputing, en wanneer?',
    "Not today: nobody has a quantum computer strong enough yet. The risk is that a future one could break the encryption that protects banking, health records and state secrets, and that attackers already copy encrypted data now to open it later (\"harvest now, decrypt later\"). The EU plan sets three milestones: national plans, inventories and first pilots by the end of 2026; high-risk systems migrated by the end of 2030; the rest, as far as possible, by the end of 2035. Data that must stay secret for ten years or more is most at risk. The app gives no date for when such a computer will exist.",
    "Vandaag nog niet: niemand heeft al een kwantumcomputer die sterk genoeg is. Het risico is dat een toekomstige computer de versleuteling kan breken die bankzaken, medische dossiers en staatsgeheimen beschermt, en dat aanvallers nu al versleutelde gegevens kopiëren om ze later te openen (\"harvest now, decrypt later\"). Het Europese plan stelt drie mijlpalen: nationale plannen, inventarissen en eerste proefprojecten tegen eind 2026; risicovolle systemen overgezet tegen eind 2030; de rest, voor zover mogelijk, tegen eind 2035. Gegevens die tien jaar of langer geheim moeten blijven, lopen het meeste risico. De app geeft geen datum waarop zo'n computer er zal zijn.",
    'C', ['quantum'],
    src=['What\'s next: quantum page: "The risk" (harvest now, decrypt later), "The EU plan" (Commission Recommendation April 2024, roadmap June 2025, milestones end of 2026 / 2030 / 2035), "What this means, in plain words" ("Nobody has one strong enough yet"; data that must stay secret for ten years or more most at risk)'])

# ===== 8 Laws and politics =====
new('law',
    'What is "chat control", and can the EU read my messages?',
    'Wat is "chatcontrole", en kan de EU mijn berichten lezen?',
    "\"Chat control\" is the nickname for a proposed EU regulation (May 2022) that would let a judge or authority order messaging services to search messages for known child-abuse images; critics say that cannot be done on an encrypted service without weakening the encryption. The EU has no law yet that obliges services to search private messages: after six rounds of talks there is no agreement, and governments dropped compulsory scanning in November 2025. A temporary rule for voluntary scanning of unencrypted messages runs to 3 April 2028. Belgium has taken no public side and abstained in the July 2026 vote.",
    "\"Chatcontrole\" is de bijnaam voor een voorgestelde Europese verordening (mei 2022) die een rechter of autoriteit zou toelaten berichtendiensten te bevelen berichten te doorzoeken op bekende beelden van kindermisbruik; critici zeggen dat dat op een versleutelde dienst niet kan zonder de versleuteling te verzwakken. De EU heeft nog geen wet die diensten verplicht privéberichten te doorzoeken: na zes onderhandelingsrondes is er geen akkoord, en de regeringen schrapten de verplichte scanning in november 2025. Een tijdelijke regel voor vrijwillige scanning van onversleutelde berichten loopt tot 3 april 2028. België heeft publiek geen kant gekozen en onthield zich bij de stemming van juli 2026.",
    'CR', ['encryption'],
    trap=('Campaign sources expect a new attempt in November or on 8 December 2026; the date is not confirmed. Much of what is written about "chat control" comes from campaign groups on both sides.',
          'Campagnebronnen verwachten een nieuwe poging in november of op 8 december 2026; de datum is niet bevestigd. Veel van wat over "chatcontrole" wordt geschreven, komt van campagnegroepen aan beide kanten.'),
    src=['Message scanning and encryption in Belgium page: "In plain words", timeline (May 2022 proposal; Nov 2025 mandatory scanning dropped; Mar-Jul 2026 temporary permission extended on 23 July 2026 to 3 April 2028, unencrypted messages only, Belgium abstained; 29 Sep 2026 sixth round without deal; campaign sources expect November or 8 December, not confirmed), "Proven and not proven"',
         'Message scanning and encryption in the rest of Europe page: Denmark dropped the scanning duty (Oct 2025)'])

new('law',
    'What does NIS2 oblige Belgian companies to do?',
    'Wat verplicht NIS2 Belgische bedrijven te doen?',
    "NIS2 is the EU law for vital organisations; Belgium's law dates from 26 April 2024 and has been in force since 18 October 2024. It covers 18 sectors, as a rule from 50 employees or €10 million turnover. Organisations must take ten basic measures, among them a risk analysis, backups, checking suppliers, staff training and two-step login, and report a serious incident with a first warning within 24 hours and a fuller report within 72 hours. The board answers personally; fines go up to €10 million or 2% of worldwide turnover for essential organisations. Essential organisations had to hand in a first proof of their security level by 18 April 2026.",
    "NIS2 is de Europese wet voor vitale organisaties; de Belgische wet dateert van 26 april 2024 en geldt sinds 18 oktober 2024. Ze geldt voor 18 sectoren, in de regel vanaf 50 werknemers of 10 miljoen euro omzet. Organisaties moeten tien basismaatregelen nemen, onder meer een risicoanalyse, back-ups, controle van leveranciers, opleiding van het personeel en tweestapsverificatie, en een ernstig incident melden met een eerste waarschuwing binnen 24 uur en een uitgebreider verslag binnen 72 uur. Het bestuur is persoonlijk verantwoordelijk; de boetes lopen op tot 10 miljoen euro of 2% van de wereldwijde omzet voor essentiële organisaties. Essentiële organisaties moesten tegen 18 april 2026 een eerste bewijs van hun beveiligingsniveau indienen.",
    'C', ['laws'],
    src=['Laws and regulations page: "NIS2: the law for vital organisations" (18 sectors; 50 employees or EUR 10 million; ten basic measures; 24 hours / 72 hours / one month; board liable; fines EUR 10 million or 2%) and "The Belgian NIS2 law" (26 April 2024, in force 18 October 2024; 18 April 2026 first proof; April 2027 next step)'])

new('law',
    "Why don't the laws stop attacks?",
    'Waarom houden de wetten aanvallen niet tegen?',
    "Because there are gaps between them, and a warning obliges nobody. The freezer controllers fell outside NIS2 (supermarket retail is not covered) and the Cyber Resilience Act applies only to products sold from 11 December 2027. Belgium's cyber centre warned on 13 October and stores were hit on 2 November, 20 days later. Municipalities are not automatically covered by NIS2, and three in four hospitals were below the required level in January 2026. New laws also take time: the Cybersecurity Act 2 was proposed on 20 January 2026 and has no committee vote date yet, and on 8 July 2026 the Commission took Ireland, Spain, France and the Netherlands to court for not yet turning NIS2 into national law.",
    "Omdat er gaten tussen zitten, en een waarschuwing niemand verplicht iets te doen. De sturingen van de diepvriezers vielen buiten NIS2 (supermarkten zijn niet gedekt) en de Cyber Resilience Act geldt pas voor producten die vanaf 11 december 2027 verkocht worden. Het Belgische cybercentrum waarschuwde op 13 oktober en de winkels werden op 2 november getroffen, 20 dagen later. Gemeenten vallen niet automatisch onder NIS2, en in januari 2026 zaten drie op de vier ziekenhuizen onder het vereiste niveau. Nieuwe wetten nemen ook tijd: de Cybersecurity Act 2 werd op 20 januari 2026 voorgesteld en heeft nog geen datum voor een stemming in de commissie, en op 8 juli 2026 daagde de Commissie Ierland, Spanje, Frankrijk en Nederland voor het Hof omdat ze NIS2 nog niet in nationaal recht hebben omgezet.",
    'C', ['gaps', 'laws'],
    src=['What we lack page: gap 1 "Open doors on the internet" ("No one is obliged to act on a CCB warning unless they fall under NIS2, and supermarkets don\'t"; CRA from December 2027; 13 Oct warning, 2 Nov hit), gap 6 "Town halls exposed", gap on hospitals (three in four)',
         'Laws and regulations page: Cybersecurity Act 2 (proposed 20 Jan 2026; "no committee vote date yet"); NIS2 "How Europe enforces it on countries" (8 July 2026, Ireland, Spain, France, Netherlands)'])

new('law',
    'What should Belgium change first?',
    'Wat moet België eerst veranderen?',
    "The \"53 ideas\" page names a top five and one for older people; these are proposals in the file, not decisions by anyone. The top five: no factory passwords or open internet interfaces, even on devices already installed (idea 1); a European scanner that chases owners until open doors are closed (5); two-step login compulsory on remote and admin access (6); guaranteed European access to frontier AI for defence (27); 24-hour reporting by AI labs when an agent escapes (33). For older people: refunds when the system was faked, a bank call-back before out-of-character transfers, and platforms paying for scam ads they kept running. For Belgium in particular, idea 4 would let the national cyber centre order a critical open door closed within 72 hours.",
    "De pagina \"53 ideeën\" noemt een top vijf en één voor ouderen; dit zijn voorstellen in het dossier, geen beslissingen van wie dan ook. De top vijf: geen fabriekswachtwoorden of open internetinterfaces, ook niet op toestellen die al geïnstalleerd zijn (idee 1); een Europese scanner die eigenaars opvolgt tot open deuren gesloten zijn (5); verplichte tweestapsverificatie op toegang op afstand en beheerderstoegang (6); gegarandeerde Europese toegang tot geavanceerde AI voor defensie (27); melding binnen 24 uur door AI-labs wanneer een agent ontsnapt (33). Voor ouderen: terugbetaling wanneer het systeem vervalst werd, een terugbelcontrole door de bank vóór ongewone overschrijvingen, en platformen die betalen voor oplichtingsadvertenties die ze bleven tonen. Voor België in het bijzonder zou idee 4 het nationale cybercentrum toelaten een kritieke open deur binnen 72 uur te laten sluiten.",
    '', ['ideas', 'props'],
    trap=('These are ideas put forward in this file; the app does not say that any government has adopted them.',
          'Dit zijn ideeën die in dit dossier naar voren worden gebracht; de app zegt niet dat een regering ze heeft overgenomen.'),
    src=['53 ideas page: "The top five, plus one for older people" (ideas 1, 5, 6, 27, 33; older people: refund when the system was faked, call-back, platforms pay), idea 4 "Open door orders" (CCB power to order a critical exposure closed within 72 hours, escalating fines; "Who acts: CCB; federal Parliament")',
         'Proposals page: the file\'s proposals (same themes)'])

# ---------- build ----------
def build():
    P = BeautifulSoup(open(M + 'vrt-cyber-briefing.html', encoding='utf-8').read(), 'html.parser')
    sec = P.find('section', id='qa')
    if sec.get('data-qa2'):
        print('qa2: already processed'); return
    old_cards = sec.find_all('details', class_='qa')
    assert len(old_cards) == 29, len(old_cards)

    # existing cards: placement, notes in Dutch, updates, status line + More link
    placed = {g[0]: [] for g in GROUPS}
    used = set()
    for card in old_cards:
        q = card.find('summary').get_text()
        rule = None
        for i, r in enumerate(OLD):
            if q.startswith(r[0]):
                rule = r; used.add(i); break
        assert rule, q
        card = card.extract()
        body = card.find('div', class_='body')
        # updates
        for en_old, en_new, nl_old, nl_new in UPDATES:
            for p in body.find_all('p'):
                if p.get('class') and 'nl' in p['class']:
                    if nl_old and nl_old in p.string:
                        p.string = p.string.replace(nl_old, nl_new)
                elif p.string and en_old in p.string:
                    p.string = p.string.replace(en_old, en_new)
        # Dutch note
        trap = body.find('p', class_='trap')
        if trap:
            key = [k for k in TRAP_NL if trap.get_text().startswith(k)]
            assert len(key) == 1, trap.get_text()[:60]
            nlp = P.new_tag('p'); nlp['class'] = ['nl', 'trap']; nlp.string = 'NL: ' + TRAP_NL[key[0]]
            trap.insert_after(nlp)
        body.append(BeautifulSoup(more_p(rule[2], rule[3]), 'html.parser'))
        placed[rule[1]].append(card)
    assert len(used) == 29
    # check the updates really applied
    txt = str(sec)
    # new cards
    newcards = {g[0]: [] for g in GROUPS}
    for n in NEW:
        h = '<details class="qa"><summary>%s · <i>%s</i></summary><div class="body"><p>%s</p><p class="nl">NL: %s</p>' % (e(n['q']), e(n['qn']), e(n['a']), e(n['an']))
        if n['trap']:
            h += '<p class="trap">%s</p><p class="nl trap">NL: %s</p>' % (e(n['trap'][0]), e(n['trap'][1]))
        h += more_p(n['tags'], n['pages']) + '</div></details>'
        newcards[n['g']].append(BeautifulSoup(h, 'html.parser'))
    total = sum(len(v) for v in placed.values()) + sum(len(v) for v in newcards.values())

    # section: title, subtitle (with the computed count), intro, jump list, groups
    out = BeautifulSoup('', 'html.parser')
    ns = P.new_tag('section'); ns['id'] = 'qa'; ns['data-qa2'] = '1'
    h2 = P.new_tag('h2'); h2.string = 'Questions and answers'; ns.append(h2)
    counts = [(g, len(newcards[g[0]]) + len(placed[g[0]])) for g in GROUPS]
    ns.append(BeautifulSoup('<p class="sub">The questions people ask most about cyberattacks on Belgium and Europe: %d questions in %d groups, each with a short, sourced answer and a note on what is not certain.</p>'
                            '<p class="nl">NL: De vragen die mensen het vaakst stellen over cyberaanvallen op België en Europa: %d vragen in %d groepen, elk met een kort antwoord met bronnen en een opmerking over wat niet zeker is.</p>'
                            % (total, len(GROUPS), total, len(GROUPS)), 'html.parser'))
    ns.append(BeautifulSoup('<p class="qa-intro">Pick a group, then open a question. Every answer is short, uses only what is already in this file, and ends with a link to the page that has the details. The tags show how firm the facts are: Confirmed, Reported, Claimed, Suspected or Not proven. Where blame is mentioned, it says who says so; it is not a finding.</p>'
                            '<p class="nl">NL: Kies een groep en open dan een vraag. Elk antwoord is kort, gebruikt alleen wat al in dit dossier staat en eindigt met een link naar de pagina met de details. De labels tonen hoe stevig de feiten zijn: Bevestigd, Gemeld, Geclaimd, Vermoed of Niet bewezen. Waar schuld wordt genoemd, staat erbij wie dat zegt; het is geen vaststelling.</p>', 'html.parser'))
    jen = ' '.join('<a href="#qa-%s" data-toc="qa-%s">%s (%d)</a>' % (g[0], g[0], e(g[1]), c) for g, c in counts)
    jnl = ' '.join('<a href="#qa-%s" data-toc="qa-%s">%s (%d)</a>' % (g[0], g[0], e(g[2]), c) for g, c in counts)
    ns.append(BeautifulSoup('<p class="qa-jump"><b>Jump to a group:</b> %s</p><p class="nl qa-jump">NL: <b>Ga naar een groep:</b> %s</p>' % (jen, jnl), 'html.parser'))
    for g, c in counts:
        ns.append(BeautifulSoup('<h2 class="qa-g" id="qa-%s">%s</h2><p class="nl">NL: %s</p>' % (g[0], e(g[1]), e(g[2])), 'html.parser'))
        for card in newcards[g[0]] + placed[g[0]]:
            ns.append(card); ns.append('\n')
    sec.replace_with(ns)
    open(M + 'vrt-cyber-briefing.html', 'w', encoding='utf-8').write(str(P))

    # CSS (patched into the app template copy, idempotent; same pattern as intel.py)
    a = M + 'tools/app_template.html'
    t = open(a, encoding='utf-8').read()
    if '.qa-g{' not in t:
        css = '''
.qa-g{font-size:21px;margin:30px 0 6px;scroll-margin-top:16px}
.qa-intro{max-width:760px}
.qa-jump{display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center;margin:10px 0 4px}
.qa-jump b{margin-right:4px}
.qa-jump a{display:inline-block;padding:4px 11px;border:1px solid var(--line);border-radius:999px;background:var(--paper);font-size:13.5px;text-decoration:none;color:var(--accent)}
.qa-jump a:hover{border-color:var(--accent)}
.qa-more{font-size:13.5px;margin:12px 0 0;color:var(--muted)}
.qa-more a{font-weight:600}
.qa-more .tag{margin-right:3px}
'''
        assert '</style>' in t
        t = t.replace('</style>', css + '</style>', 1)
        open(a, 'w', encoding='utf-8').write(t)
    print('qa2 ok: %d questions (%d existing + %d new) in %d groups' % (total, 29, len(NEW), len(GROUPS)), [c for g, c in counts])


def sources(path):
    L = ['# Sources for the new answers on the page "Questions and answers"', '',
         'Every fact in a new answer comes from text already in the app. For each answer: the app page (or data) it was taken from. Status tags: Confirmed = stated by an authority, court or the organisation itself; Reported = press, not verified; Claimed = one party, no public evidence; Suspected = believed, not proven; Not proven = looked into, nothing found; Not published = no cause given.', '']
    cur = None
    for n in NEW:
        if n['g'] != cur:
            cur = n['g']; gn = [g for g in GROUPS if g[0] == cur][0]
            L += ['## %s / %s' % (gn[1], gn[2]), '']
        L.append('### %s' % n['q'])
        L.append('Tags: %s. More: %s.' % (', '.join(TAGS[c][0] for c in n['tags']) or 'none (practical advice or proposals)', ', '.join(PAGE[k][0] for k in n['pages'])))
        for s in n['src']:
            L.append('- ' + s)
        L.append('')
    open(path, 'w', encoding='utf-8').write('\n'.join(L))
    print('wrote', path)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--sources':
        sources(sys.argv[2])
    else:
        build()
