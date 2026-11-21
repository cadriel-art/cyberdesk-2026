"""Round 2: new start page (#home). Runs after build_app.py and before offline.py (see build_all.sh).
Replaces the body of the #p-home article with: what this is, key numbers (computed from the built pages), What's new
(static fallback from the build's updates; the online file refreshes it from the live `updates` collection that the
Updates page already reads), Belgium first, Start here, and the full page list grouped like the menu."""
import re,json,html
from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
P=M+'cyber-desk.html'
s=open(P,encoding='utf-8').read()
if 'id="hm-root"' in s:
    print('home2 already applied'); raise SystemExit
soup=BeautifulSoup(s,'html.parser')
nav=json.loads(re.search(r'const NAV = (\[.*?\]);\n',s).group(1))
E=lambda x:html.escape(str(x),quote=True)
def L(en,nl): return '<span class="hl hl-en">%s</span><span class="hl hl-nl">%s</span>'%(en,nl)

# ---------- key numbers: all computed from the built pages / data files ----------
rows=soup.select('#reg2t tbody tr')
n_reg=len(rows); n_conf=sum(1 for r in rows if r.get('data-st')=='c')
n_ctry=len(soup.select('#p-eucountries .country[id^="c-"]'))
stx={}
for d in soup.select('#p-evidence .statsx .stx'):
    stx[d.select_one('span').get_text(strip=True)]=int(d.select_one('b').get_text(strip=True))
n_cases=stx['cases tracked']; n_attr=stx['formal attributions by a state']
n_src=len(soup.select('#p-sources ul.src li'))
snap=json.load(open(M+'tools/news_snapshot.json',encoding='utf-8')); n_news=len(snap)
n_map=int(re.search(r'(\d+) entries in',soup.select_one('#p-map p.sub').get_text()).group(1))
NUMS=[('reg2',n_reg,'incidents in the register','incidenten in het register',L('%d confirmed'%n_conf,'%d bevestigd'%n_conf)),
 ('eucountries',n_ctry,'countries covered','landen in beeld','' ),
 ('evidence',n_cases,'cases on the evidence tracker','zaken in de bewijstracker',''),
 ('evidence',n_attr,'formal attributions by a state','formele toeschrijvingen door een staat',''),
 ('news',n_news,'news items in the reader','nieuwsberichten in de lezer',L('snapshot of this build','momentopname van deze build')),
 ('sources',n_src,'sources','bronnen','')]
NUMDATA=[(k,n,en) for k,n,en,nl,x in NUMS]

# ---------- one-line descriptions (EN, NL), shortened from each page's subtitle ----------
def sub(k):
    e=soup.select_one('#p-%s p.sub'%k); return e.get_text(' ',strip=True) if e else ''
def num(k,pat,g=1):
    m=re.search(pat,sub(k)); return m.group(g) if m else None
prep=re.search(r'Of the (\d+) countries covered, (\d+) have official advice.*?, (\d+) have it only through media reports.*?and (\d+) have none',sub('prepare'))
outg=re.search(r'(\d+) outages of major online services',sub('outages'))
gl=num('glossary',r'\((\d+) terms\)')
D={
'news':("Headlines on attacks, sabotage and drones, with filters for country and subject.","Nieuwskoppen over aanvallen, sabotage en drones, met filters voor land en onderwerp."),
'intel':("Three short lists that keep this file current: the last week, cases that moved on the proof ladder, and open questions.","Drie korte lijsten die dit dossier actueel houden: de voorbije week, zaken die opschoven op de bewijsladder en open vragen."),
'trend':("How the picture changed in two years, from official figures first and this file's own register second.","Hoe het beeld in twee jaar veranderde, eerst volgens officiële cijfers, dan volgens het eigen register."),
'cases':("The ten incidents that define the two years, each in a few lines.","De tien incidenten die de twee jaar bepalen, elk in enkele regels."),
'qa':("The questions people ask most, each with a short, sourced answer and a note on what is not certain.","De vragen die mensen het meest stellen, elk met een kort, gebrond antwoord en een noot over wat niet zeker is."),
'reg2':("%d incidents in 31 countries, in date order, with filters for year, country, sector and kind of attack."%n_reg,"%d incidenten in 31 landen, op datum, met filters voor jaar, land, sector en soort aanval."%n_reg),
'months':("2026 first, then 2025; confirmed incidents kept apart from reported and claimed ones.","Eerst 2026, dan 2025; bevestigde incidenten staan apart van gerapporteerde en geclaimde."),
'eucountries':("The 27 EU Member States plus Norway, Iceland, Switzerland and Liechtenstein, in alphabetical order.","De 27 EU-lidstaten plus Noorwegen, IJsland, Zwitserland en Liechtenstein, alfabetisch."),
'map':("%d entries in 31 countries and at sea, January 2025 to November 2026. Click a pin to see what is known."%n_map,"%d meldingen in 31 landen en op zee, januari 2025 tot november 2026. Klik op een speld om te zien wat bekend is."%n_map),
'evidence':("%d attacks, alarms and plots, each with the same five questions: who is named, by whom, on what evidence, who denies it, what is unknown."%n_cases,"%d aanvallen, alarmen en complotten, elk met dezelfde vijf vragen: wie wordt genoemd, door wie, op welk bewijs, wie ontkent, wat is onbekend."%n_cases),
'outages':("%s outages of major online services and company systems, 2025 to 19 November 2026."%(outg.group(1) if outg else ''),"%s storingen bij grote onlinediensten en bedrijfssystemen, 2025 tot 19 november 2026."%(outg.group(1) if outg else '')),
'energy':("Why the freezer attacks and the attacks on power systems are one story, and every energy source one by one.","Waarom de diepvriesaanvallen en de aanvallen op stroomsystemen één verhaal zijn, en elke energiebron apart."),
'water':("Drinking water and waste water in 2025 and 2026: Belgian water companies, what the law asks, lessons from abroad.","Drinkwater en afvalwater in 2025 en 2026: de Belgische watermaatschappijen, wat de wet vraagt, lessen uit het buitenland."),
'watereu':("Attacks on drinking water, waste water and dams in the rest of Europe, 2025 and 2026.","Aanvallen op drinkwater, afvalwater en dammen in de rest van Europa, 2025 en 2026."),
'transport':("Airports, sea ports, rail, post and logistics in Belgium, 2025 and 2026: attacks, crime, outages and false alarms.","Luchthavens, zeehavens, spoor, post en logistiek in België, 2025 en 2026: aanvallen, misdaad, storingen en valse alarmen."),
'transporteu':("Airports, airlines, ports, shipping, rail and logistics in the rest of Europe.","Luchthavens, luchtvaartmaatschappijen, havens, scheepvaart, spoor en logistiek in de rest van Europa."),
'health':("Hospitals, clinics, health software and patient data in Belgium, 2025 and 2026.","Ziekenhuizen, klinieken, gezondheidssoftware en patiëntgegevens in België, 2025 en 2026."),
'healtheu':("Hospitals, clinics, laboratories, health software and patient data in the rest of Europe.","Ziekenhuizen, klinieken, laboratoria, gezondheidssoftware en patiëntgegevens in de rest van Europa."),
'failures':("Most of these attacks did not need genius: documented cases where a door was left open, and who should have closed it.","De meeste van deze aanvallen vroegen geen genie: gedocumenteerde gevallen met een openstaande deur, en wie die had moeten sluiten."),
'good':("Most of this file is alarming. These cases show that action pays off.","Het meeste in dit dossier is onrustwekkend. Deze gevallen tonen dat optreden loont."),
'now':("The cluster of incidents from the last four weeks.","De reeks incidenten van de voorbije vier weken."),
'freezers':("What happened, how it worked, why warned shops still got hit, who was responsible, and what must change.","Wat er gebeurde, hoe het werkte, waarom gewaarschuwde winkels toch getroffen werden, wie verantwoordelijk was en wat moet veranderen."),
'year':("Every recorded 2026 incident in Belgium, in date order.","Elk geregistreerd incident van 2026 in België, op datum."),
'back':("Background from 2023 to 2025 that shows the pattern.","Achtergrond uit 2023 tot 2025 die het patroon toont."),
'register':("Public record of Belgian incidents, 2023 to 10 Nov 2026, oldest first, with filters.","Openbaar register van Belgische incidenten, 2023 tot 10 nov 2026, oudste eerst, met filters."),
'numbers':("The key figures, each with what it means and how to word it accurately.","De kerncijfers, elk met wat het betekent en hoe je het correct verwoordt."),
'tools':("Belgium does not start from nothing. The tools exist, but they work unevenly.","België begint niet van nul. De instrumenten bestaan, maar werken ongelijk."),
'powers':("How cybersecurity is split across Europe, the federal government, the regions, the communities and the municipalities.","Hoe cyberveiligheid verdeeld is over Europa, de federale overheid, de gewesten, de gemeenschappen en de gemeenten."),
'laws':("Everything in place, being negotiated or planned, explained from the ground up.","Alles wat bestaat, wordt onderhandeld of gepland, uitgelegd vanaf nul."),
'encryption':("Whether the police may read private messages, where Belgium stands, and what Belgium's own biggest case says about it.","Mag de politie privéberichten lezen? Waar België staat en wat de grootste Belgische zaak daarover zegt."),
'encryptioneu':("Where each of the rest of Europe stands on letting the police read private messages.","Waar elk van de rest van Europa staat over politietoegang tot privéberichten."),
'files':("Where each EU law file stands, status as of 12 Nov 2026.","Waar elk Europees wetsdossier staat, stand van 12 nov 2026."),
'gaps':("The gaps in protection, each tied to documented cases with dates and numbers.","De hiaten in de bescherming, elk gekoppeld aan gedocumenteerde gevallen met data en cijfers."),
'props':("Each proposal is tied to a 2026 case, with what it means in plain words.","Elk voorstel is gekoppeld aan een zaak uit 2026, met wat het betekent in gewone woorden."),
'ideas':("Ideas grouped by theme that go further than the Commission's current proposals.","Ideeën per thema die verder gaan dan de huidige voorstellen van de Commissie."),
'who':("The people who hold the relevant roles, as of the latest sources found.","De mensen die de relevante functies bekleden, volgens de recentste bronnen."),
'victims':("Nobody is too small or too big: every kind of victim and fraud, and who should have protected them.","Niemand is te klein of te groot: alle soorten slachtoffers en fraude, en wie hen had moeten beschermen."),
'insurance':("Who is insured against a cyberattack, what insurers demand, and whether paying a ransom is allowed.","Wie verzekerd is tegen een cyberaanval, wat verzekeraars eisen en of losgeld betalen mag."),
'skills':("How many cybersecurity people Belgium and Europe have, how many they lack, and what is being done.","Hoeveel cyberveiligheidsmensen België en Europa hebben, hoeveel er ontbreken en wat eraan gedaan wordt."),
'citizens':("How well people in the EU recognise and report online threats, and what most people still don't do.","Hoe goed mensen in de EU online dreigingen herkennen en melden, en wat de meesten nog niet doen."),
'prepare':(("Which of %s countries advise an emergency stock at home: %s officially, %s through media reports, %s none found."%prep.group(1,2,3,4)) if prep else '',("In welke van %s landen officieel advies bestaat voor een noodvoorraad thuis: %s officieel, %s via media, %s geen gevonden."%prep.group(1,2,3,4)) if prep else ''),
'ai':("AI makes good attackers faster and bad attackers good enough. No authority has said AI was used in the Belgian incidents.","AI maakt goede aanvallers sneller en slechte aanvallers goed genoeg. Geen enkele overheid zegt dat AI is gebruikt bij de Belgische incidenten."),
'agents':("New in 2026, documented by the companies themselves: AI agents that left their test environments and broke into real systems.","Nieuw in 2026, door de bedrijven zelf gedocumenteerd: AI-agenten die hun testomgeving verlieten en inbraken in echte systemen."),
'cloud':("A sovereignty question that follows from the Mythos episode.","Een soevereiniteitsvraag die volgt uit de Mythos-episode."),
'quantum':("A forward-looking answer to \"What's the next big threat?\"","Een vooruitkijkend antwoord op \"Wat is de volgende grote dreiging?\""),
'hybrid':("Drones over airports, bases and nuclear plants, suspected sabotage, spying and hoaxes, in Belgium.","Drones boven luchthavens, bases en kerncentrales, vermoede sabotage, spionage en hoaxes, in België."),
'hybrideu':("The same subject for the rest of Europe.","Hetzelfde onderwerp voor de rest van Europa."),
'elections':("Attacks on politics itself in Belgium: fakes, hijacked accounts, spyware, bribery, spying and pressure on politicians.","Aanvallen op de politiek zelf in België: fakes, gekaapte accounts, spyware, omkoping, spionage en druk op politici."),
'electionseu':("Interference with elections and with people in politics in the rest of Europe.","Inmenging in verkiezingen en in mensen in de politiek in de rest van Europa."),
'defence':("What the Belgian army does about cyber and hybrid threats: its cyber branch, people and money, and attacks on Defence itself.","Wat het Belgische leger doet tegen cyber- en hybride dreigingen: de cybertak, mensen en geld, en aanvallen op Defensie zelf."),
'defenceeu':("Military cyber forces, reserves, money and the rules for acting at home in the rest of Europe.","Militaire cybermachten, reservisten, geld en de regels voor optreden in eigen land in de rest van Europa."),
'schools':("Attacks on schools, which are ordinary crime against badly defended organisations, and the laws to protect children online.","Aanvallen op scholen, gewone misdaad tegen slecht verdedigde organisaties, en de wetten om kinderen online te beschermen."),
'cables':("The cables under the sea that carry the internet, and the satellite signal that tells ships and aircraft where they are.","De kabels onder zee die het internet dragen, en het satellietsignaal dat schepen en vliegtuigen hun positie geeft."),
'more':("An index of the subjects worked out in this file, the subjects still to come, and the questions public sources do not answer.","Een index van de uitgewerkte onderwerpen, de onderwerpen die nog komen en de vragen die openbare bronnen niet beantwoorden."),
'printsel':("Choose pages and countries, then print them as one document with a cover and a list of contents.","Kies pagina's en landen en druk ze af als één document met omslag en inhoudstafel."),
'glossary':("Every technical term in one plain sentence each, in English and Dutch%s."%((' (%s terms)'%gl) if gl else ''),"Elke technische term in één gewone zin, in het Engels en Nederlands%s."%((' (%s termen)'%gl) if gl else '')),
'sources':("Every source used in this file, %d in all, sorted by type of source."%n_src,"Elke bron die in dit dossier gebruikt is, %d in totaal, gesorteerd per soort bron."%n_src),
'updates':("Dated updates added since the briefing.","Gedateerde updates sinds de briefing."),
}
# Belgian counts of countries in the "other N countries" wording come from the page subtitles (26 others + 4 non-EU = 30 in the menu)
missing=[i['k'] for g in nav for i in g['items'] if i['k'] not in D and i['k']!='home']
assert not missing, missing
def desc(k): return L(E(D[k][0]),E(D[k][1]))
def name(i): return L(E(i['en']),E(i['nl']))
def live(i): return ' <span class="hm-live">LIVE</span>' if i.get('live') else ''
IT={i['k']:i for g in nav for i in g['items']}

# ---------- what's new: static fallback from the build ----------
ups=json.load(open(M+'tools/updates_snapshot.json',encoding='utf-8'))
ups=[u for u in ups if not u.get('app')]   # app/feature notes stay on the Updates page only
ups=sorted(ups,key=lambda u:(u.get('order',0),u.get('id','')),reverse=True)[:3]   # newest by `order`; ties by id
TAGNL={'New':'Nieuw','Check':'Controle','Attribution':'Toeschrijving','New incidents':'Nieuwe incidenten','Correction':'Correctie'}
def upd_card(u):
    return ('<li class="hm-upd"><div class="hm-when">%s%s</div><b>%s</b><p>%s</p></li>'%(E(u.get('date','')),(' · '+L(E(u['tag']),E(TAGNL.get(u['tag'],u['tag'])))) if u.get('tag') else '',
        L(E(u.get('title','')),E(u.get('title_nl') or u.get('title',''))),L(E(short(u.get('body',''))),E(short(u.get('body_nl') or u.get('body',''))))))
def short(t,n=190):
    t=t.strip()
    if len(t)<=n: return t
    c=t[:n]; i=max(c.rfind('. '),c.rfind('; '))
    r=(c[:i+1] if i>60 else c[:c.rfind(' ')]+'…')
    return r[:-1]+'…' if r.endswith(';') else r
nowcards=''.join(upd_card(u) for u in ups)

# ---------- assemble ----------
status=re.search(r'Status as of [0-9]+ \w+ \d{4}',s[s.index('id="p-home"'):s.index('id="p-home"')+4000])
status=status.group(0) if status else ''
status_nl=re.sub('Status as of','Stand van',status)
h=[]
h.append('<div class="crumb">Cyber Attacks 2026</div><div id="hm-root">')
h.append('<h2>%s</h2>'%L('Cyberattacks on Europe, 2025–2026','Cyberaanvallen op Europa, 2025–2026'))
h.append('<p class="sub hm-what">%s</p>'%L('A dated, sourced record of cyberattacks in the 27 EU countries plus Norway, Iceland, Switzerland and Liechtenstein, over two years, with Belgium first. Confirmed incidents are kept apart from reported and claimed ones.','Een gedateerd, gebrond overzicht van cyberaanvallen in de 27 EU-landen plus Noorwegen, IJsland, Zwitserland en Liechtenstein, over twee jaar, met België eerst. Bevestigde incidenten staan apart van gerapporteerde en geclaimde.'))
h.append('<p class="hm-meta">%s · %s · %s</p>'%(L(E(status),E(status_nl)),L('31 countries · 2025 and 2026','31 landen · 2025 en 2026'),L('Prepared with Claude (Anthropic)','Opgesteld met Claude (Anthropic)')))
# numbers
h.append('<h3 class="hm-h">%s</h3><ul class="hm-nums">'%L('The file in numbers','Het dossier in cijfers'))
for k,n,en,nl,x in NUMS:
    h.append('<li><a href="#%s"><b>%d</b><span>%s</span>%s</a></li>'%(k,n,L(en,nl),('<small>%s</small>'%x) if x else ''))
h.append('</ul>')
# what's new
h.append('<h3 class="hm-h">%s</h3><ul class="hm-new" id="hm-new">%s</ul><p class="hm-more"><a href="#updates">%s</a></p>'%(L("What's new","Wat is nieuw"),nowcards,L('All updates →','Alle updates →')))
# Belgium first
BE=['now','freezers','year','register','numbers','powers']   # first six pages of the Belgium group
h.append('<section class="hm-be" aria-labelledby="hm-be-h"><h3 class="hm-h" id="hm-be-h">%s</h3><ul class="hm-cards">'%L('Belgium first','België eerst'))
for k in BE:
    h.append('<li><a href="#%s"><b>%s</b><span>%s</span></a></li>'%(k,name(IT[k]),desc(k)))
h.append('</ul></section>')
# start here
ST=['news','trend','cases','qa','intel']   # the Start here group, minus the overview
h.append('<h3 class="hm-h">%s</h3><ol class="hm-steps">'%L('Start here','Begin hier'))
for k in ST:
    h.append('<li><a href="#%s"><b>%s</b>%s<span>%s</span></a></li>'%(k,name(IT[k]),live(IT[k]),desc(k)))
h.append('</ol>')
h.append('<div class="callout warn hm-not"><b>%s</b> %s</div>'%(L('What this file is not.','Wat dit dossier niet is.'),L('It is not a complete count. Most victims are never named, countries publish very differently, and the research looked harder at 2026 than at 2025. Use it for the pattern and for the individual cases, not for totals.','Het is geen volledige telling. De meeste slachtoffers worden nooit genoemd, landen publiceren heel verschillend en het onderzoek keek scherper naar 2026 dan naar 2025. Gebruik het voor het patroon en voor de afzonderlijke gevallen, niet voor totalen.')))
# all pages
h.append('<h3 class="hm-h">%s</h3>'%L('All pages','Alle pagina’s'))
for g in nav:
    its=[i for i in g['items'] if i['k']!='home']
    if not its: continue
    h.append('<section class="hm-grp"><h4>%s</h4><ul class="hm-list">'%L(E(g['en']),E(g['nl'])))
    for i in its:
        h.append('<li><a href="#%s"><b>%s</b>%s<span>%s</span></a></li>'%(i['k'],name(i),live(i),desc(i['k'])))
    h.append('</ul></section>')
h.append('</div>')
body=''.join(h)

a=s.index('<article class="page" id="p-home"'); z=s.index('</article>',a)
open_tag=s[a:s.index('>',a)+1]
s=s[:a]+open_tag+body+s[z:]

# online: refresh "What's new" from the live `updates` collection that the Updates page already reads
old="updates=snap.docs.map(d=>d.data()||{});"
assert s.count(old)==1
s=s.replace(old,old+"if(window.__homeUpd)window.__homeUpd(updates);")
css=open(M+'tools/home2.css',encoding='utf-8').read(); js=open(M+'tools/home2.js',encoding='utf-8').read()
i=s.index('</style>'); s=s[:i]+css+s[i:]
k=s.rindex('</script>'); s=s[:k]+js+'\n'+s[k:]
open(P,'w',encoding='utf-8').write(s)
print('home2 ok',NUMDATA)
