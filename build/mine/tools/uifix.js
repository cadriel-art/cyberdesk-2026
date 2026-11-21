/* uifix: app-wide UI fixes from the UX audit (U2 terms closed, U3 Dutch UI strings, U5 accessibility).
   Language switch = document.documentElement.lang ('en' | 'nl'), set by the app's drawNav() on every page change. */
(function(){
'use strict';
var doc=document,root=doc.documentElement;
function lang(){return root.lang==='nl'?'nl':'en';}

/* ---------- page names from the app's own NAV table (EN -> NL) ---------- */
var NAV=null,NAVK={},NAVEN={};
try{
  var ss=doc.scripts;
  for(var i=0;i<ss.length;i++){
    var tx=ss[i].text,ix=tx.indexOf('const NAV = ');
    if(ix>=0){var ex=tx.indexOf(';\n',ix);NAV=JSON.parse(tx.slice(ix+12,ex));break;}
  }
}catch(e){}
NAV=NAV||[];
NAV.forEach(function(g){
  if(g.en&&g.nl)NAVEN[g.en]=g.nl;
  (g.items||[]).forEach(function(it){NAVK[it.k]=it;if(it.en&&it.nl&&it.en!==it.nl)NAVEN[it.en]=it.nl;});
});
window.cdUI={pageName:function(k,l){var it=NAVK[k];return it?(it[l]||it.en):k;}};

/* ---------- dictionaries ---------- */
var CT={'Austria':'Oostenrijk','Belgium':'België','Bulgaria':'Bulgarije','Croatia':'Kroatië','Cyprus':'Cyprus','Czechia':'Tsjechië','Denmark':'Denemarken','Estonia':'Estland','Finland':'Finland','France':'Frankrijk','Germany':'Duitsland','Greece':'Griekenland','Hungary':'Hongarije','Iceland':'IJsland','Ireland':'Ierland','Italy':'Italië','Latvia':'Letland','Liechtenstein':'Liechtenstein','Lithuania':'Litouwen','Luxembourg':'Luxemburg','Malta':'Malta','Netherlands':'Nederland','Norway':'Noorwegen','Poland':'Polen','Portugal':'Portugal','Romania':'Roemenië','Slovakia':'Slowakije','Slovenia':'Slovenië','Spain':'Spanje','Sweden':'Zweden','Switzerland':'Zwitserland','United Kingdom':'Verenigd Koninkrijk','United States':'Verenigde Staten','Ukraine':'Oekraïne','Europe':'Europa','European Union':'Europese Unie','EU':'EU','International':'Internationaal'};
window.cdUI.ctry=function(c){return lang()==='nl'&&CT[c]?CT[c]:c;};
var MONTHS={January:'januari',February:'februari',March:'maart',April:'april',May:'mei',June:'juni',July:'juli',August:'augustus',September:'september',October:'oktober',November:'november',December:'december'};
var D={
/* status tags: same words the app already uses in its Dutch prose */
'Confirmed':'Bevestigd','Reported':'Gemeld','Claimed':'Geclaimd','Suspected':'Vermoed','Not proven':'Niet bewezen','Proven':'Bewezen','Not published':'Niet gepubliceerd','Check':'Controle','Nobody named':'Niemand genoemd','Official':'Officieel','Not found':'Niet gevonden','None found':'Niets gevonden','Confirmed by chains':'Bevestigd door ketens','Claimed, not confirmed':'Geclaimd, niet bevestigd','Claimed / check':'Geclaimd / controle','Police':'Politie','Official source':'Officiële bron',
/* table headers */
'Term':'Begrip','In plain words':'In gewone woorden','Status':'Status','Date':'Datum','Who':'Wie','Figure':'Cijfer','Country':'Land','What it is':'Wat het is','Event':'Gebeurtenis','Source':'Bron','2026 example':'Voorbeeld uit 2026','What it does, in plain words':'Wat het doet, in gewone woorden','When it matters to you':'Wanneer het jou raakt','What happened':'Wat er gebeurde','Case':'Zaak','What':'Wat','Kind':'Soort','Where':'Waar','Source and status':'Bron en status','Where it stands':'Waar het staat','Sector':'Sector','Body':'Instantie','Where and when':'Waar en wanneer','What it means for you':'Wat het voor jou betekent','Situation':'Situatie','How firm':'Hoe stevig','Role':'Rol','Link to this topic':'Link met dit onderwerp','What was seen':'Wat er te zien was','Subject':'Onderwerp','Latest step':'Laatste stap','Level':'Niveau','Case, who is named, who says so':'Zaak, wie genoemd wordt, wie het zegt','Open question':'Open vraag','What to watch for':'Waarop letten','Official or published figures':'Officiële of gepubliceerde cijfers','Kind of attack':'Soort aanval','What is known':'Wat bekend is','Sender named firmly (L4–L6)':'Afzender stevig genoemd (L4–L6)','Sender not named firmly (L0–L3)':'Afzender niet stevig genoemd (L0–L3)','A person was caught':'Een persoon werd gepakt','Nobody was caught':'Niemand werd gepakt','Happened':'Gebeurd','Named or decided':'Genoemd of beslist','Time':'Tijd','What came out':'Wat eruit kwam','One side says':'Eén kant zegt','The other side says':'De andere kant zegt','What was reached':'Wat bereikt werd','Way in':'Manier van binnenkomen','Who, and how firm':'Wie, en hoe stevig','Main threat seen':'Belangrijkste dreiging','Worst case in the two years':'Ergste geval in twee jaar','What kind of organisation':'Soort organisatie','People concerned':'Betrokken mensen','What stopped':'Wat stilviel','Their part':'Hun aandeel','When':'Wanneer','Why it matters':'Waarom het telt','Incidents':'Incidenten','Victim':'Slachtoffer','What applies':'Wat geldt','Tool':'Hulpmiddel','What it is, in plain words':'Wat het is, in gewone woorden','Who it\'s for, and how to use it':'Voor wie het is, en hoe je het gebruikt','The limit':'De grens','2026 evidence':'Bewijs uit 2026','Their responsibility':'Hun verantwoordelijkheid','Who to contact':'Wie je belt','For scanning':'Voor scanning','Against scanning':'Tegen scanning','What it proves for the police':'Wat het bewijst voor de politie','What it proves for the critics':'Wat het bewijst voor de critici','Position':'Standpunt','Countries named':'Genoemde landen','What it would do':'Wat het zou doen','Where it ended':'Waar het eindigde','File':'Dossier','What could still be added':'Wat nog kan worden toegevoegd','How they get in':'Hoe ze binnenkomen','Verified example':'Gecontroleerd voorbeeld','Example':'Voorbeeld','Who should carry it':'Wie het zou moeten dragen','Country · sector · kind':'Land · sector · soort','Why it is disputed':'Waarom het betwist wordt','Who was blamed, and how firmly':'Wie de schuld kreeg, en hoe stevig','Who was behind it':'Wie erachter zat','Who says it, and when':'Wie het zegt, en wanneer','What it would cover':'Wat het zou dekken','What it tells you':'Wat het je zegt','What it does not have':'Wat het niet heeft','What it counts':'Wat het telt','What a school has':'Wat een school heeft','The question':'De vraag','Outcome':'Uitkomst','Item':'Onderdeel','How it works':'Hoe het werkt','How far it has got':'Hoe ver het staat','Election':'Verkiezing','Effect on the result':'Effect op de uitslag','Children on social media':'Kinderen op sociale media','Attacks on schools':'Aanvallen op scholen','Approach':'Aanpak','Count':'Aantal','Who counts it that way':'Wie het zo telt','Look at':'Kijkt naar','Can do at home':'Kan thuis','Who may act':'Wie mag ingrijpen','Since':'Sinds','Share of the economy':'Aandeel van de economie','Note':'Opmerking','Reserve or volunteers':'Reserve of vrijwilligers','Pages':'Pagina\'s',
/* summaries and headings */
'Still open':'Nog open','Proven and not proven':'Bewezen en niet bewezen','What happened, in order':'Wat er gebeurde, in volgorde','Figures':'Cijfers','Nothing specific found':'Niets specifieks gevonden','Sources':'Bronnen','Nothing found':'Niets gevonden','Countries with something on record':'Landen met iets geregistreerd','What caused it':'Wat de oorzaak was','Who is blamed':'Wie de schuld krijgt','Europe and Belgium':'Europa en België','Key figures':'Kerncijfers','Terms on this page':'Begrippen op deze pagina','What the sources say':'Wat de bronnen zeggen','Counts by others':'Tellingen door anderen','Counts and assessments by others':'Tellingen en beoordelingen door anderen','Counts and statements by others':'Tellingen en verklaringen door anderen','Limits of this page':'Grenzen van deze pagina','Limits of this tracker':'Grenzen van deze tracker',
/* filters (reg2, outages, evidence, prepare) */
'All years':'Alle jaren','All countries':'Alle landen','All kinds':'Alle soorten','All subjects':'Alle onderwerpen','All sectors':'Alle sectoren','Confirmed only':'Alleen bevestigd','Newest first':'Nieuwste eerst','Oldest first':'Oudste eerst','Confirmed and unconfirmed':'Bevestigd en onbevestigd','Reported and claimed only':'Alleen gemeld en geclaimd','Any cause status':'Elke status van de oorzaak','Food and retail':'Voeding en handel','Finance':'Financiën','Telecom':'Telecom','Government':'Overheid','Education':'Onderwijs','Energy':'Energie','Water':'Water','Health':'Gezondheid','Transport':'Transport','Other':'Overig','Spying':'Spionage','Espionage':'Spionage','Sabotage or physical effect':'Sabotage of fysiek effect','Ransomware':'Ransomware','Data theft or leak':'Datadiefstal of lek','Websites knocked offline':'Websites platgelegd','Kind of attack not disclosed':'Soort aanval niet bekendgemaakt','Technical fault or change':'Technische storing of wijziging','Power or cooling failure':'Stroom- of koelingsstoring','Cyberattack':'Cyberaanval','Cause not published':'Oorzaak niet gepubliceerd','Yes: official advice':'Ja: officieel advies','Yes, via media only':'Ja, alleen via de media','Mailed to households only':'Alleen naar huishoudens gestuurd','Reset':'Herstellen','Open all':'Alles openen','Close':'Sluiten',
/* print a selection */
'Ready-made sets':'Kant-en-klare sets','The short version':'De korte versie','Everything on the attacks':'Alles over de aanvallen','Subject by subject':'Onderwerp per onderwerp','Laws and ideas':'Wetten en ideeën','Whole file':'Het hele dossier','Clear':'Wissen','Countries':'Landen','Options':'Opties','Language on paper':'Taal op papier','Style':'Stijl','Extras':'Extra','English only (shorter)':'Alleen Engels (korter)','English and Dutch':'Engels en Nederlands','Light (thin borders, saves ink)':'Licht (dunne randen, bespaart inkt)','Colour (as on screen)':'Kleur (zoals op het scherm)','Cover and list of contents':'Omslag en inhoudsopgave','"Terms on this page" tables':'Tabellen "Begrippen op deze pagina"','Print the selection':'Selectie afdrukken','All of this group':'Heel deze groep','What follows: laws and ideas':'Wat volgt: wetten en ideeën','Beyond hacking':'Voorbij het hacken'
};
var SUBJ={'Energy and the grid':'Energie en het net','Water':'Water','Health':'Gezondheid','Transport and ports':'Transport en havens','Elections and democracy':'Verkiezingen en democratie','Not on a subject page':'Niet op een onderwerppagina','By country':'Per land'};
var ALIAS={'Hybrid: Belgium':'hybrid','Hybrid: 30 countries':'hybrideu','Democracy: Belgium':'elections','Democracy: 30 countries':'electionseu','Transport: Belgium':'transport','Transport: 30 countries':'transporteu','Defence: Belgium':'defence','Defence: 30 countries':'defenceeu','Encryption: Belgium':'encryption','Encryption: 30 countries':'encryptioneu','Health: Belgium':'health','Health: 30 countries':'healtheu','Water: Belgium':'water','Water: 30 countries':'watereu','Register 2025–2026':'reg2','Sea cables and signals':'cables','Evidence tracker':'evidence','Skills and jobs':'skills','Children and schools':'schools','Insurance':'insurance','Global outages':'outages','Ready at home: stock-up advice':'prepare'};
var TAGPRE={'Reported':'Gemeld','Confirmed':'Bevestigd','Claimed':'Geclaimd','Official':'Officieel','Suspected':'Vermoed'};
var ATTR={'Language':'Taal','freezers, MyMinfin, Iran…':'diepvriezers, MyMinfin, Iran…','Subject':'Onderwerp','Country':'Land','Status':'Status','Sector':'Sector','Kind of attack':'Soort aanval','Year':'Jaar','Order':'Volgorde','Kind':'Soort','Who is named':'Wie wordt genoemd','How firm':'Hoe stevig','People caught':'Gepakte personen','Filter the outages':'Filter de storingen','Kind of outage':'Soort storing','Status of the cause':'Status van de oorzaak','Search company, place, cause…':'Zoek bedrijf, plaats, oorzaak…','Sort order':'Sortering','Filter the countries':'Filter de landen','Official advice':'Officieel advies','Search country, agency, guide…':'Zoek land, instantie, gids…','Search: Leipzig, Iran, cables...':'Zoek: Leipzig, Iran, kabels...','Filter by sector':'Filter op sector','Close':'Sluiten','Search the news':'Zoek in het nieuws'};

/* evidence ladder: level names (EN -> NL, the NL names are those the tracker already prints in italics) and descriptions */
var LVN={'Court verdict':'Vonnis van een rechtbank','Charges, arrests or arrest warrants':'Aanklacht, arrestatie of aanhoudingsbevel','Formal attribution by a government or agency':'Formele toewijzing door een regering of dienst','Statement or suspicion by an official':'Uitspraak of vermoeden van een gezagsdrager','Assessment by researchers or unnamed sources':'Inschatting door onderzoekers of anonieme bronnen','The attackers\' own claim':'Bewering van de aanvallers zelf','Nobody named':'Niemand genoemd','Not an attack, or no evidence':'Geen aanval, of geen bewijs'};
var LVD={'A court heard the evidence and ruled. The strongest proof there is; it can still be overturned on appeal.':'Een rechtbank heeft het bewijs gehoord en uitspraak gedaan. Het sterkste bewijs dat bestaat; in beroep kan het nog worden herzien.',
'A prosecutor believes there is enough to go to court. Not yet tested by a judge.':'Een openbaar ministerie vindt dat er genoeg is om naar de rechtbank te stappen. Nog niet getoetst door een rechter.',
'An official position, usually based on intelligence that stays secret. Serious, but nobody outside can check it.':'Een officieel standpunt, meestal gebaseerd op inlichtingen die geheim blijven. Zwaarwichtig, maar niemand daarbuiten kan het nagaan.',
'A minister, a police chief or a prosecutor says who they think it was. It is not the formal position of the state, and colleagues sometimes disagree.':'Een minister, een politiebaas of een procureur zegt wie volgens hem of haar de dader was. Het is niet het officiële standpunt van de staat, en collega\'s zijn het soms oneens.',
'Security companies, think tanks or journalists quoting insiders. Useful, sometimes commercial, never binding.':'Beveiligingsbedrijven, denktanks of journalisten die insiders citeren. Nuttig, soms commercieel, nooit bindend.',
'A post on Telegram or a leak site. Cheap to make, easy to fake, and sometimes made by groups that did nothing.':'Een bericht op Telegram of een lekkensite. Goedkoop om te maken, makkelijk te vervalsen, en soms gedaan door groepen die niets hebben uitgespookt.',
'An investigation may be running, but no name has been put forward by anyone with authority.':'Er loopt misschien een onderzoek, maar niemand met gezag heeft een naam naar voren geschoven.',
'It looked like an attack and was first reported as one. An investigation found another cause, or nothing at all.':'Het leek op een aanval en werd eerst zo gemeld. Uit onderzoek bleek een andere oorzaak, of helemaal niets.'};
var D2={'Russia (state services)':'Rusland (staatsdiensten)','Pro-Russian groups':'Pro-Russische groepen','Iran':'Iran','Belarus':'Belarus','China':'China','North Korea':'Noord-Korea','Criminal groups':'Criminele groepen','Drug gangs':'Drugsbendes','Extremists, no state':'Extremisten, geen staat','Other':'Overige','A friendly state, by accident':'Een bevriende staat, per ongeluk','A foreign state, not named':'Een buitenlandse staat, niet genoemd','Individuals, no sponsor named':'Individuen, geen opdrachtgever genoemd','Not an attack':'Geen aanval','Not attributed':'Niet toegewezen',
'Convicted':'Veroordeeld','Charged':'Aangeklaagd','Arrested':'Aangehouden','Nobody caught':'Niemand gepakt',
'Bribery':'Omkoping','Cyber':'Cyber','Drones':'Drones','Elections':'Verkiezingen','Energy':'Energie','Hoax':'Valse melding','Pressure':'Druk','Provocation':'Provocatie','Sabotage':'Sabotage','Sea':'Zee','Spying':'Spionage','Spyware':'Spyware','Transport':'Transport','Water':'Water',
'By proof level':'Op bewijsniveau','Newest first':'Nieuwste eerst',
'Government & public':'Overheid en openbare diensten','EU institutions (Brussels)':'EU-instellingen (Brussel)','Health':'Gezondheid','Shops & food':'Winkels en voeding','Banks, telecom & finance':'Banken, telecom en financiën','Education':'Onderwijs','Industry & transport':'Industrie en transport','Legal & media':'Juridisch en media','Hybrid':'Hybride','All':'Alle',
'Sources for this page':'Bronnen voor deze pagina','All sources for this page':'Alle bronnen voor deze pagina',
'Official: governments, EU bodies, agencies, police, courts':'Officieel: regeringen, EU-organen, diensten, politie, rechtbanken','The organisations themselves: companies, operators, sector bodies':'De organisaties zelf: bedrijven, operatoren, sectororganen','Public broadcasters and news agencies':'Openbare omroepen en persagentschappen','Newspapers and news sites':'Kranten en nieuwssites','Specialist press: cyber, technology, energy, defence':'Vakpers: cyber, technologie, energie, defensie','Security companies and incident trackers':'Beveiligingsbedrijven en incidenttrackers','Research institutes, think tanks and law firms':'Onderzoeksinstituten, denktanks en advocatenkantoren','Reference works, used as a pointer only':'Naslagwerken, alleen als wegwijzer gebruikt',
'Formal attribution by a government':'Formele toewijzing door een regering','Statement by an official':'Uitspraak van een gezagsdrager','Charges, arrests or warrants':'Aanklacht, arrestatie of bevel','Researchers or unnamed sources':'Onderzoekers of anonieme bronnen'};
var FP={'Who is named':'Wie wordt genoemd','How firm':'Hoe stevig','Kind':'Soort','People caught':'Gepakte personen'};
var D3={'The pattern, in plain words':'Het patroon, in gewone woorden','The register at a glance, in plain words':'Het register in een oogopslag, in gewone woorden','The point, in plain words':'De kern, in gewone woorden','What AI changes, in plain words':'Wat AI verandert, in gewone woorden','What this means, in plain words':'Wat dit betekent, in gewone woorden','What these scams look like to the victim':'Hoe deze oplichting er voor het slachtoffer uitziet','Is this dangerous for ordinary people?':'Is dit gevaarlijk voor gewone mensen?','How to read this map, and how not to':'Hoe je deze kaart leest, en hoe niet',"The EU's own count: ENISA Threat Landscape 2026":'De eigen telling van de EU: ENISA Threat Landscape 2026','As published by ENISA':'Zoals gepubliceerd door ENISA','Background: 2024 outages people still refer to':'Achtergrond: storingen uit 2024 waar mensen nog naar verwijzen','Their answer:':'Hun antwoord:','Methods seen:':'Gebruikte methoden:','Hardest proof:':'Sterkste bewijs:',
'For most incidents nobody is named. An attacker\'s own claim is not an attribution.':'Bij de meeste incidenten wordt niemand genoemd. De bewering van de aanvaller zelf is geen toewijzing.','Sorted by type in the full source register under Reference.':'Gesorteerd per soort in het volledige bronnenregister onder Naslag.'};
(function(){for(var k in D3)if(D3[k]&&!Object.prototype.hasOwnProperty.call(D,k))D[k]=D3[k];})();
var NA=function(n,one,many){return n+' '+(n==1?one:many);};
(function(){for(var k in D2)if(!Object.prototype.hasOwnProperty.call(D,k))D[k]=D2[k];})();
function cn(c){return CT[c]||c;}
function has(o,k){return Object.prototype.hasOwnProperty.call(o,k);}
function tr(s){
  var m;
  if(has(D,s))return D[s];
  if(has(LVN,s))return LVN[s];
  if((m=/^(Who is named|How firm|Kind|People caught): all$/.exec(s)))return FP[m[1]]+': alle';
  if((m=/^(\d+) cases? shown\.$/.exec(s)))return m[1]+(m[1]==1?' zaak':' zaken')+' getoond.';
  if((m=/^(\d+) of (\d+) cases shown\.$/.exec(s)))return m[1]+' van '+m[2]+' zaken getoond.';
  if((m=/^All (\d+) cases$/.exec(s)))return 'Alle '+m[1]+' zaken';
  if((m=/^(\d+) cases?$/.exec(s)))return m[1]+(m[1]==1?' zaak':' zaken');
  if((m=/^(January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})$/.exec(s)))return MONTHS[m[1]]+' '+m[2];
  if((m=/^Month not known, (\d{4})$/.exec(s)))return 'Maand onbekend, '+m[1];
  if((m=/^· (\d+) recorded$/.exec(s)))return '· '+m[1]+' geregistreerd';
  if(has(LVD,s))return LVD[s];
  if(s==='Nothing selected yet.')return 'Nog niets geselecteerd.';
  if((m=/^(L\d|✕) · (.+)$/.exec(s))&&has(LVN,m[2]))return m[1]+' · '+LVN[m[2]];
  if((m=/^(\d+) pages? selected(?: · (\d+) countr(?:y|ies))?\.$/.exec(s)))return m[1]+(m[1]==1?' pagina':' pagina\'s')+' geselecteerd'+(m[2]?' · '+m[2]+(m[2]==1?' land':' landen'):'')+'.';
  if((m=/^About (\d+) sheets? of A4 \(rough estimate; the print dialog shows the exact number\)\.$/.exec(s)))return 'Ongeveer '+m[1]+(m[1]==1?' blad':' bladen')+' A4 (ruwe schatting; het afdrukvenster toont het exacte aantal).';
  if(has(CT,s))return CT[s];
  if(has(ALIAS,s)&&NAVK[ALIAS[s]])return NAVK[ALIAS[s]].nl;
  if(has(NAVEN,s))return NAVEN[s];
  if((m=/^(\d+) on record$/.exec(s)))return m[1]+' geregistreerd';
  if(s==='nothing found')return 'niets gevonden';
  if((m=/^(.+?) (\d+) on record$/.exec(s)))return cn(m[1])+' '+m[2]+' geregistreerd';
  if((m=/^(.+?) nothing found$/.exec(s)))return cn(m[1])+' niets gevonden';
  if((m=/^More on the page [“"](.+)[”"]$/.exec(s))){var pn=has(NAVEN,m[1])?NAVEN[m[1]]:m[1];return 'Meer op de pagina “'+pn+'”';}
  if((m=/^From strongest to weakest\. The bar shows how many of the (\d+) cases sit on each step\.$/.exec(s)))return 'Van sterkst naar zwakst. De balk toont hoeveel van de '+m[1]+' zaken op elke trede staan.';
  if((m=/^Background: 2024 outages people still refer to \((\d+)\)$/.exec(s)))return 'Achtergrond: storingen uit 2024 waar mensen nog naar verwijzen ('+m[1]+')';
  if((m=/^Sources for this page \((\d+)\)$/.exec(s)))return 'Bronnen voor deze pagina ('+m[1]+')';
  if((m=/^All sources for this page \((\d+)\)$/.exec(s)))return 'Alle bronnen voor deze pagina ('+m[1]+')';
  if((m=/^Terms on this page · Begrippen op deze pagina \((\d+)\)$/.exec(s)))return 'Begrippen op deze pagina ('+m[1]+')';
  if((m=/^(\d+) of (\d+) incidents shown$/.exec(s)))return m[1]+' van '+m[2]+' incidenten getoond';
  if((m=/^(January|February|March|April|May|June|July|August|September|October|November|December) (\d{4}) · (\d+) recorded$/.exec(s)))return MONTHS[m[1]]+' '+m[2]+' · '+m[3]+' geregistreerd';
  if((m=/^Month not found, (\d{4}) · (\d+) recorded$/.exec(s)))return 'Maand onbekend, '+m[1]+' · '+m[2]+' geregistreerd';
  if((m=/^EU AND SCHENGEN(.*)$/.exec(s)))return 'EU EN SCHENGEN'+m[1];
  if((m=/^(Reported|Confirmed|Claimed|Official|Suspected) \((.+)\)$/.exec(s)))return TAGPRE[m[1]]+' ('+(CT[m[2]]||m[2])+')';
  if((m=/^(.+) \((\d+)\)$/.exec(s))){var b=SUBJ[m[1]]||D[m[1]]||NAVEN[m[1]];if(b)return b+' ('+m[2]+')';}
  if(s.indexOf(' / ')>0){var ps=s.split(' / '),o=[],ok=true;ps.forEach(function(p){var t=D[p];if(t)o.push(t);else ok=false;});if(ok)return o.join(' / ');}
  return null;
}

/* ---------- applying the Dutch strings (text nodes and attributes; EN is restored when switching back) ---------- */
var SEL='#ev-count,.hn,.ev-who,.lv,.filters button,#p-register td,#p-register .tag,.gapx.prof small,#ps-summary,#ps-summary b,.lad-h b,.lad p.small,.tag,.pill,th,summary,option,legend,label,button,h3,h4,h5,h3 small,h4 small,.count,.brand small,.nw-fh,summary b,summary span.small,#p-evidence p,#p-evidence p>b,#p-evidence p.small a,p.small,.mp-help summary';
var textOrig=new Map(),attrOrig=new Map(),touchedT=[],touchedA=[];
function norm(s){return s.replace(/\s+/g,' ').trim();}
function doNode(n){
  if(textOrig.has(n))return;
  var v=n.nodeValue,t=norm(v);if(!t)return;
  var out=tr(t);
  if(out===null)return;
  var lead=/^\s*/.exec(v)[0],trail=/\s*$/.exec(v)[0];
  textOrig.set(n,v);touchedT.push(n);n.nodeValue=lead+out+trail;
}
function doEl(el){
  if(el.tagName==='OPTION'&&!el.hasAttribute('value'))el.setAttribute('value',el.textContent);
  var k=el.tagName==='LABEL'?el.querySelector('input[data-pg]'):null;
  if(k&&NAVK[k.dataset.pg]){
    for(var c=el.firstChild;c;c=c.nextSibling)if(c.nodeType===3&&norm(c.nodeValue)){
      if(!textOrig.has(c)){textOrig.set(c,c.nodeValue);touchedT.push(c);c.nodeValue=' '+NAVK[k.dataset.pg].nl;}
      break;
    }
    return;
  }
  for(var c2=el.firstChild;c2;c2=c2.nextSibling)if(c2.nodeType===3)doNode(c2);
}
function doAttrs(scope){
  var els=scope.querySelectorAll('[placeholder],[aria-label],.lv[title],.lvb[title]');
  for(var i=0;i<els.length;i++){
    var e=els[i];
    ['placeholder','aria-label','title'].forEach(function(a){
      var v=e.getAttribute(a);if(!v)return;
      var rec=attrOrig.get(e);if(rec&&rec[a]!==undefined)return;
      var t=has(ATTR,v)?ATTR[v]:null;
      if(!t&&e.matches('.lv,.lvb')){var mm=/^(.+?)(: \d+)?$/.exec(v);if(mm&&has(LVN,mm[1]))t=LVN[mm[1]]+(mm[2]||'');}
      if(!t&&e.matches('.lv')&&has(D2,v))t=D2[v];
      if(!t)return;
      if(!rec){rec={};attrOrig.set(e,rec);touchedA.push(e);}
      rec[a]=v;e.setAttribute(a,t);
    });
  }
}
function restore(){
  touchedT.forEach(function(n){if(textOrig.has(n)){n.nodeValue=textOrig.get(n);textOrig.delete(n);}});touchedT=[];
  touchedA.forEach(function(e){var r=attrOrig.get(e);if(r)for(var a in r)e.setAttribute(a,r[a]);attrOrig.delete(e);});touchedA=[];
}
function translate(){
  if(lang()!=='nl'){if(touchedT.length||touchedA.length)restore();return;}
  var scopes=[doc.getElementById('side'),doc.getElementById('pages')];
  scopes.forEach(function(sc){
    if(!sc)return;
    var els=sc.querySelectorAll(SEL);
    for(var i=0;i<els.length;i++)doEl(els[i]);
    doAttrs(sc);
  });
  if(touchedT.length>8000)touchedT=touchedT.filter(function(n){return n.isConnected;});
}

/* ---------- U2: informative boxes start closed (print and the print buttons still open them) ---------- */
function closeTerms(){
  var b=doc.querySelectorAll('details.termsbox[open]');
  for(var i=0;i<b.length;i++)b[i].removeAttribute('open');
}

/* ---------- U5: duplicate ids, one h1 per page, no skipped heading levels ---------- */
function fixIds(){
  var s=doc.querySelectorAll('#s-ai');
  if(s.length>1){var p=s[1].closest('article.page');s[1].id='s-'+(p?p.id.slice(2):'ai2');}
}
function fixHeadings(){
  var pages=doc.querySelectorAll('#pages > article.page');
  for(var pi=0;pi<pages.length;pi++){
    var p=pages[pi],hs=[].slice.call(p.querySelectorAll('h1,h2,h3,h4,h5,h6'));
    if(!hs.length)continue;
    if(!p.querySelector('h1')){
      var f=hs[0],h=doc.createElement('h1');
      for(var a=0;a<f.attributes.length;a++)h.setAttribute(f.attributes[a].name,f.attributes[a].value);
      h.classList.add('pgt');
      while(f.firstChild)h.appendChild(f.firstChild);
      f.parentNode.replaceChild(h,f);hs[0]=h;
    }
    var prev=0;
    for(var i=0;i<hs.length;i++){
      var e=hs[i],L=+e.tagName.charAt(1),eff=L;
      if(prev&&L>prev+1)eff=prev+1;
      if(eff!==L)e.setAttribute('aria-level',eff);else if(e.hasAttribute('aria-level'))e.removeAttribute('aria-level');
      prev=eff;
    }
  }
}

/* ---------- failures page: lists are English only ---------- */
function failuresNote(){
  var s=doc.getElementById('s-failures');if(!s||s.querySelector('.eo-note'))return;
  var sub=s.querySelector('.sub');if(!sub)return;
  var p=doc.createElement('p');p.className='nl small eo-note';
  p.innerHTML='<b>NL:</b> De lijsten en tabellen op deze pagina staan alleen in het Engels.';
  sub.parentNode.insertBefore(p,sub.nextSibling);
}

/* ---------- skip link ---------- */
var skip=doc.createElement('a');
skip.className='skiplink';skip.href='#pages';skip.textContent='Skip to content';
doc.body.insertBefore(skip,doc.body.firstChild);
skip.addEventListener('click',function(e){
  e.preventDefault();
  var t=doc.querySelector('#pages > article.page:not([hidden]) h1')||doc.getElementById('pages');
  t.setAttribute('tabindex','-1');t.focus();
  if(t.scrollIntoView)t.scrollIntoView({block:'start'});
});

/* ---------- search page opened directly: go home with the search box focused ---------- */
function searchGuard(){
  if(location.hash!=='#search')return;
  var pg=doc.getElementById('p-search');
  if(pg&&!pg.textContent.trim()){
    location.replace('#home');
    var q=doc.getElementById('q');if(q)setTimeout(function(){q.focus();},50);
  }
}
window.addEventListener('hashchange',function(){setTimeout(searchGuard,30);});

/* ---------- run, and re-run when the app re-renders ---------- */
var pagesEl=doc.getElementById('pages'),mo=null,timer=null;
function apply(){
  if(mo)mo.disconnect();
  try{
    fixIds();fixHeadings();translate();   /* failuresNote() retired in round 3: bilang.js adds one note per page */
    skip.textContent=lang()==='nl'?'Naar de inhoud':'Skip to content';
  }catch(e){}
  if(mo)attach();
}
function attach(){
  if(pagesEl)mo.observe(pagesEl,{childList:true,subtree:true});
  var sd=doc.getElementById('side');if(sd)mo.observe(sd,{childList:true,subtree:true});
  mo.observe(root,{attributes:true,attributeFilter:['lang']});
}
function sched(){clearTimeout(timer);timer=setTimeout(apply,90);}
mo=new MutationObserver(sched);
closeTerms();
apply();
searchGuard();
})();

/* ===== UX round 1 (R1): route focus and titles, phone menu, empty states, search, wide tables, live badge ===== */
(function(){
'use strict';
var doc=document,root=doc.documentElement;
function lang(){return root.lang==='nl'?'nl':'en';}
function T(en,nl){return lang()==='nl'?nl:en;}
function $(s,r){return (r||doc).querySelector(s);}
function $$(s,r){return [].slice.call((r||doc).querySelectorAll(s));}
var side=$('#side'),nav=$('#nav'),pagesEl=$('#pages'),menuBtn=$('#menu'),mtop=$('.mtop'),qEl=$('#q');
var NAVK={};
try{var ss=doc.scripts;for(var i=0;i<ss.length;i++){var tx=ss[i].text,ix=tx.indexOf('const NAV = ');if(ix>=0){var ex=tx.indexOf(';\n',ix);JSON.parse(tx.slice(ix+12,ex)).forEach(function(g){(g.items||[]).forEach(function(it){NAVK[it.k]=it;});});break;}}}catch(e){}
function setText(el,s){if(el&&el.textContent!==s)el.textContent=s;}
function pname(k){var it=NAVK[k];return it?(it[lang()]||it.en):'';}
function activePage(){return $('#pages > article.page:not([hidden])');}
function mq900(){return window.matchMedia&&window.matchMedia('(max-width:900px)').matches;}

/* ---------- search index (built now, in the original language, before any Dutch string is applied) ---------- */
var NLSEL='.nl,.pb-nl,.plnl,.joe-nl,[lang="nl"]';
function split(pg){
  var c=pg.cloneNode(true),nl=[];
  $$('script,style,textarea',c).forEach(function(e){e.remove();});
  /* round 3: pieces marked by bilang.js (.nl-x = Dutch) go to the Dutch text, the rest stays English */
  $$('.nl-lbl',c).forEach(function(e){e.remove();});
  $$('.nl-x',c).forEach(function(e){if(e.parentNode&&!(e.parentNode&&e.parentNode.closest&&e.parentNode.closest('.nl-x'))&&!e.matches('.bl-sep,br'))nl.push(e.textContent);});
  $$('.nl-x',c).forEach(function(e){if(e.parentNode)e.remove();});
  var heads=$$('h1,h2,h3,h4,summary',c).map(function(h){return h.textContent.replace(/\s+/g,' ').trim();}).filter(function(s){return s&&!/^NL:/.test(s);});
  $$(NLSEL,c).forEach(function(e){if(e.parentNode&&!e.parentNode.closest(NLSEL)){nl.push(e.textContent);}});
  $$(NLSEL,c).forEach(function(e){if(e.parentNode)e.remove();});
  $$('b,strong',c).forEach(function(b){
    if(b.parentNode&&/^NL:\s*$/.test(b.textContent)){var s='',n=b.nextSibling;while(n){var nx=n.nextSibling;s+=n.textContent+' ';n.remove();n=nx;}nl.push(s);b.remove();}
  });
  $$('p,li,td,th,tr,h1,h2,h3,h4,div,summary,section,span.sector',c).forEach(function(e){e.appendChild(doc.createTextNode(' '));});
  var cl=function(s){return s.replace(/\b(?:In plain words|Terms on this page|Sources for this page)\s*·\s*(?:In gewone woorden|Begrippen op deze pagina|Bronnen voor deze pagina)/g,' ').replace(/\bNL:\s*/g,'').replace(/\s+/g,' ').trim();};
  return {en:cl(c.textContent),nl:cl(nl.join(' ')),heads:heads};
}
var INDEX=[];
function buildIndex(){
INDEX.length=0;
try{
  $$('#pages > article.page[data-static]').forEach(function(pg){
    var k=pg.id.slice(2);if(k==='home')return;var s=split(pg),h1=$('h1',pg);
    INDEX.push({k:k,en:s.en,nl:s.nl,heads:s.heads,titles:[(NAVK[k]&&NAVK[k].en)||'',(NAVK[k]&&NAVK[k].nl)||'',h1?h1.textContent:''].join('\n').toLowerCase(),all:(s.en+' '+s.nl).toLowerCase()});
  });
  var C=JSON.parse($('#data').textContent);
  var qa=(C.qa||[]),qen=qa.map(function(q){return [q.q,q.a,q.trap].join(' ');}).join(' '),qnl=qa.map(function(q){return [q.qnl,q.nl].join(' ');}).join(' ');
  INDEX.push({k:'rehearse',en:qen,nl:qnl,heads:[],titles:((NAVK.rehearse&&(NAVK.rehearse.en+'\n'+NAVK.rehearse.nl))||'').toLowerCase(),all:(qen+' '+qnl).toLowerCase()});
}catch(e){}
}
buildIndex();
window.cdUI=window.cdUI||{};window.cdUI.reindex=buildIndex;window.cdUI.index=INDEX;   /* bilang.js calls this after it has marked the Dutch pieces */
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function count(t,q){var i=t.indexOf(q),n=0;while(i>-1){n++;i=t.indexOf(q,i+q.length);}return n;}
function snip(txt,q){var i=txt.toLowerCase().indexOf(q);if(i<0)return null;var s=Math.max(0,i-70);return (s?'…':'')+txt.slice(s,i+q.length+90)+'…';}
function runSearch(v){
  var q=v.toLowerCase(),stem=(q.indexOf(' ')<0&&q.length>=6)?q.slice(0,4):null,out=[];
  INDEX.forEach(function(e){
    var n=count(e.all,q);if(!n)return;
    var tScore=e.titles.indexOf(q)>=0?1000:(stem&&e.titles.indexOf(stem)>=0?500:0);
    var hh=0;e.heads.forEach(function(h){if(h.toLowerCase().indexOf(q)>=0)hh++;});
    var dens=Math.min(40,n/Math.max(1,e.all.length/1000)*2);
    var act=lang()==='nl'?e.nl:e.en,oth=lang()==='nl'?e.en:e.nl;
    out.push({k:e.k,n:n,score:tScore+Math.min(hh,5)*60+Math.min(n,40)+dens,snip:snip(act,q)||snip(oth,q)||''});
  });
  out.sort(function(a,b){return b.score-a.score||b.n-a.n;});
  return out;
}
var pendingHL=null;
function renderSearch(v){
  var out=runSearch(v),p=$('#p-search');if(!p)return;
  p.innerHTML='<div class="crumb">'+esc(T('Search everything','Zoek in alles'))+'</div><h1 class="pgt" id="srh">“'+esc(v)+'”</h1><p class="sub">'+(out.length?(lang()==='nl'?out.length+" pagina's met resultaten":out.length+' pages with results'):T('Nothing found.','Niets gevonden.'))+'</p><div class="results">'+out.map(function(r){
    var it=NAVK[r.k];return '<a href="#'+r.k+'" data-hl="'+esc(v)+'"><b>'+esc(it?(it[lang()]||it.en):r.k)+' <span class="pill blue">'+r.n+'</span></b><span>'+esc(r.snip)+'</span></a>';}).join('')+'</div>';
  $$('a[data-hl]',p).forEach(function(a){a.addEventListener('click',function(){pendingHL=a.getAttribute('href')==='#rehearse'?null:a.dataset.hl;});});
  p.dataset.q=v;
}
function doSearch(v){
  if(v.length<2){if(activePage()&&activePage().id==='p-search')location.hash='#home';return;}
  renderSearch(v);
  var ap=activePage();
  if(ap&&ap.id==='p-search'){try{history.replaceState({cdq:v},'',location.href);}catch(e){}document.title=T('Search','Zoeken')+': “'+v+'” · Cyber Attacks 2026';return;}
  try{history.pushState({cdq:v},'','#search');}catch(e){}
  window.dispatchEvent(new HashChangeEvent('hashchange'));
}
var sT=null;
window.addEventListener('input',function(e){
  if(!e.target||e.target.id!=='q')return;
  e.stopPropagation();e.stopImmediatePropagation();
  clearTimeout(sT);var v=e.target.value.trim();sT=setTimeout(function(){doSearch(v);},180);
},true);
window.addEventListener('popstate',function(e){
  var s=e.state;
  if(location.hash==='#search'&&s&&s.cdq){renderSearch(s.cdq);if(qEl)qEl.value=s.cdq;}
});
function highlight(pg,v){
  if(!pg||!v)return;var lv=v.toLowerCase();
  var w=doc.createTreeWalker(pg,NodeFilter.SHOW_TEXT,{acceptNode:function(n){return n.nodeValue.toLowerCase().indexOf(lv)>=0&&!n.parentNode.closest('script,style,textarea')?NodeFilter.FILTER_ACCEPT:NodeFilter.FILTER_REJECT;}});
  var nodes=[];while(w.nextNode())nodes.push(w.currentNode);var first=null;
  nodes.forEach(function(n){var i=n.nodeValue.toLowerCase().indexOf(lv),m=doc.createElement('mark');m.dataset.hl='1';var after=n.splitText(i);after.splitText(v.length);m.textContent=after.nodeValue;after.replaceWith(m);if(!first)first=m;var d=m.closest('details');if(d)d.open=true;});
  if(first)first.scrollIntoView({block:'center'});
}

/* ---------- route changes: focus the H1, set the title, show the active sidebar item ---------- */
var lastKey=null,routedAt=0;
function pageTitle(){
  var ap=activePage(),k=ap?ap.id.slice(2):'';
  if(k==='search'){var q=ap.dataset.q;return T('Search','Zoeken')+(q?': “'+q+'”':'');}
  return pname(k)||($('h1',ap)||{}).textContent||'';
}
function setTitle(){var t=pageTitle();doc.title=(t?t+' · ':'')+'Cyber Attacks 2026';}
function sideReveal(){
  var a=$('a[aria-current="page"]',nav);if(!a||!side)return;
  var ar=a.getBoundingClientRect(),sr=side.getBoundingClientRect(),pad=40;
  if(ar.top<sr.top+pad)side.scrollTop-=(sr.top+pad-ar.top);
  else if(ar.bottom>sr.bottom-pad)side.scrollTop+=(ar.bottom-sr.bottom+pad);
}
function onRoute(first){
  var ap=activePage();if(!ap)return;
  var k=ap.id;
  var changed=(k!==lastKey);lastKey=k;
  setTitle();
  sideReveal();
  if(first||!changed)return;
  routedAt=Date.now();
  try{focusHead();}catch(e){}
  setTimeout(refocus,250);
  if(pendingHL){var v=pendingHL;pendingHL=null;setTimeout(function(){highlight(ap,v);},0);}
  setTimeout(measureTables,60);
}
function focusHead(){
  var ap=activePage();if(!ap)return;
  var h=$('h1',ap)||$('h2',ap)||$('h3,h4',ap)||pagesEl;
  h.setAttribute('tabindex','-1');h.focus({preventScroll:true});
}
function refocus(){
  var ae=doc.activeElement;
  if(Date.now()-routedAt<1500&&(!ae||ae===doc.body||!ae.isConnected))focusHead();
}
var routeMO=new MutationObserver(function(){onRoute(false);});
if(pagesEl)routeMO.observe(pagesEl,{attributes:true,attributeFilter:['hidden'],subtree:false,childList:false});
new MutationObserver(function(){setTitle();syncLang();}).observe(root,{attributes:true,attributeFilter:['lang']});
/* the page may be changed by the app before we see it: also refresh title and sidebar on hashchange (after the app has routed) */
window.addEventListener('hashchange',function(){setTimeout(function(){onRoute(false);sideReveal();},0);});

/* ---------- LIVE badge on the menu (the app flags live:1 items; the saved file drops the badge) ---------- */
function liveBadges(){
  $$('a[data-k]',nav).forEach(function(a){
    var it=NAVK[a.dataset.k];
    var b=a.querySelector('.live');
    if(it&&it.live){
      if(!b){b=doc.createElement('span');b.className='live';b.textContent='LIVE';a.appendChild(b);}
      b.title=T('Updated automatically','Wordt automatisch bijgewerkt');
    }
  });
}
if(nav){new MutationObserver(function(){liveBadges();sideReveal();}).observe(nav,{childList:true});liveBadges();}

/* ---------- phone menu: Close button, Esc, focus return, header with EN/NL, one-line title ---------- */
var closeBtn=null;
function menuOpen(){return side&&side.classList.contains('open');}
function measureTop(){if(mtop){var h=Math.round(mtop.getBoundingClientRect().height);if(h>0)root.style.setProperty('--mtop-h',h+'px');}}
function closeDrawer(focusMenu){
  if(!menuOpen())return;
  menuBtn.click();
  if(focusMenu&&menuBtn)menuBtn.focus();
}
function syncLang(){
  if(closeBtn){closeBtn.lastChild.textContent=T('Close menu','Menu sluiten');}
  var nl=lang()==='nl';
  var a=$('#m-nl'),b=$('#m-en');
  if(a)a.setAttribute('aria-pressed',nl);if(b)b.setAttribute('aria-pressed',!nl);
  if(menuBtn)menuBtn.setAttribute('aria-label',T('Menu','Menu'));
}
if(side&&menuBtn&&mtop){
  closeBtn=doc.createElement('button');closeBtn.type='button';closeBtn.className='side-close';
  closeBtn.innerHTML='<span aria-hidden="true">✕</span><span></span>';
  closeBtn.addEventListener('click',function(){closeDrawer(true);});
  side.insertBefore(closeBtn,side.firstChild);
  /* title block: brand line + page name, each on one line */
  var b=$('b',mtop),sp=$('#mtitle'),wrap=doc.createElement('div');wrap.className='mt-t';
  mtop.insertBefore(wrap,b);wrap.appendChild(b);wrap.appendChild(sp);
  /* EN/NL also in the phone header */
  var g=doc.createElement('div');g.className='lng mt-lng';g.setAttribute('role','group');g.setAttribute('aria-label','Language');
  g.innerHTML='<button type="button" id="m-nl" aria-pressed="false">NL</button><button type="button" id="m-en" aria-pressed="false">EN</button>';
  mtop.appendChild(g);
  $('#m-nl').addEventListener('click',function(){$('#l-nl').click();});
  $('#m-en').addEventListener('click',function(){$('#l-en').click();});
  new MutationObserver(function(){
    if(menuOpen()){measureTop();setTimeout(function(){if(menuOpen())closeBtn.focus();},30);}
    else if(Date.now()-routedAt>400){var ae=doc.activeElement;if(!ae||ae===doc.body||side.contains(ae))menuBtn.focus();}
  }).observe(side,{attributes:true,attributeFilter:['class']});
  doc.addEventListener('keydown',function(e){
    if(!menuOpen())return;
    if(e.key==='Escape'){e.preventDefault();closeDrawer(true);return;}
    if(e.key==='Tab'&&mq900()){
      var f=$$('button,a[href],input,select',side).filter(function(x){return x.offsetParent!==null;});if(!f.length)return;
      var first=f[0],last=f[f.length-1];
      if(e.shiftKey&&doc.activeElement===first){e.preventDefault();last.focus();}
      else if(!e.shiftKey&&doc.activeElement===last){e.preventDefault();first.focus();}
    }
  });
  window.addEventListener('resize',measureTop);measureTop();
  /* a safe-area or font change can resize the header after load */
  if(window.ResizeObserver)new ResizeObserver(measureTop).observe(mtop);
}

/* ---------- empty states for filters, and a Reset button ---------- */
var FILTERS=[
 {page:'reg2',box:'#reg2f',rows:'#reg2t tbody tr',after:'#reg2count',hide:'#reg2t',addReset:true},
 {page:'outages',box:'#ogf',rows:'#og-list .og-card',after:'#og-count',addReset:true},
 {page:'prepare',box:'#prf',rows:'#pr-table .pr-row',after:'#pr-count',hide:'#pr-table',addReset:true},
 {page:'evidence',box:'#evf',rows:'#ev-list .evc',after:'#ev-count',resetSel:'#ev-reset'}
];
function resetBox(box){
  $$('select,input',box).forEach(function(c){
    if(/sort/i.test(c.id||''))return;
    if(c.type==='checkbox'){if(c.checked){c.checked=false;c.dispatchEvent(new Event('change',{bubbles:true}));}}
    else if(c.tagName==='SELECT'){if(c.selectedIndex!==0){c.selectedIndex=0;c.dispatchEvent(new Event('change',{bubbles:true}));}}
    else if(c.value){c.value='';c.dispatchEvent(new Event('input',{bubbles:true}));c.dispatchEvent(new Event('change',{bubbles:true}));}
  });
}
function filterBits(f){
  var box=$(f.box);if(!box)return;
  var rb=box.querySelector('.u-reset');
  if(f.addReset&&!rb){
    rb=doc.createElement('button');rb.type='button';rb.className='u-reset';
    rb.addEventListener('click',function(){resetBox(box);});
    box.appendChild(rb);
  }
  setText(rb,T('Reset filters','Filters herstellen'));
  var msg=doc.getElementById('u-empty-'+f.page);
  if(!msg){
    var anchor=$(f.box);if(!anchor)return;
    msg=doc.createElement('div');msg.id='u-empty-'+f.page;msg.className='u-empty';msg.setAttribute('role','status');msg.hidden=true;
    msg.innerHTML='<p></p><button type="button" class="u-reset"></button>';
    anchor.parentNode.insertBefore(msg,anchor.nextSibling);
    msg.querySelector('button').addEventListener('click',function(){
      if(f.resetSel){var r=$(f.resetSel);if(r){r.click();return;}}
      resetBox(box);
    });
  }
  var rows=$$(f.rows),vis=rows.filter(function(r){return !r.hidden;}).length;
  var zero=rows.length>0&&vis===0;
  msg.hidden=!zero;
  setText(msg.querySelector('p'),T('Nothing matches these filters.','Niets gevonden met deze filters.'));
  setText(msg.querySelector('button'),T('Reset filters','Filters herstellen'));
  if(f.hide){$$(f.hide).forEach(function(e){(e.closest('.tbl')||e).classList.toggle('u-hide',zero);});}
}
function filtersAll(){FILTERS.forEach(function(f){try{filterBits(f);}catch(e){}});}
['change','input','click'].forEach(function(ev){doc.addEventListener(ev,function(e){
  if(e.target&&e.target.closest&&e.target.closest('.filters2,.filters,.evf,.og-f,.pr-f,.u-empty'))setTimeout(filtersAll,0);
});});

/* ---------- wide tables: fade on the edge with more, one-line hint ---------- */
function measureTables(){
  var ap=activePage();if(!ap)return;
  $$('.tbl',ap).forEach(function(w){
    if(!w.offsetParent)return;
    var over=w.scrollWidth>w.clientWidth+2,hint=w.previousElementSibling;
    if(!(hint&&hint.classList&&hint.classList.contains('tbl-hint'))){
      if(!over)return;
      hint=doc.createElement('p');hint.className='tbl-hint';w.parentNode.insertBefore(hint,w);
    }
    setText(hint,T('Swipe sideways to see all columns','Veeg opzij om alle kolommen te zien'));
    hint.classList.toggle('on',over);
    w.classList.toggle('u-ov-r',over&&w.scrollLeft+w.clientWidth<w.scrollWidth-2);
    w.classList.toggle('u-ov-l',over&&w.scrollLeft>2);
    if(over){if(!w.hasAttribute('tabindex')){w.setAttribute('tabindex','0');w.setAttribute('role','region');}w.setAttribute('aria-label',hint.textContent);}
  });
}
doc.addEventListener('scroll',function(e){if(e.target&&e.target.classList&&e.target.classList.contains('tbl'))measureTables();},true);
window.addEventListener('resize',function(){clearTimeout(measureTables.t);measureTables.t=setTimeout(measureTables,100);});

/* ---------- run, and keep up when the app re-renders ---------- */
var tick=null;
function again(){clearTimeout(tick);tick=setTimeout(function(){filtersAll();measureTables();setTitle();refocus();},120);}
if(pagesEl)new MutationObserver(again).observe(pagesEl,{childList:true,subtree:true});
new MutationObserver(again).observe(root,{attributes:true,attributeFilter:['lang']});
syncLang();filtersAll();onRoute(true);
setTimeout(function(){measureTables();},200);
/* a results link such as #search opened directly keeps working: the earlier guard sends it home */
})();

/* ===== UX round 2 (R2): "On this page" table of contents and "Back to top" ===== */
(function(){
'use strict';
var doc=document,root=doc.documentElement;
function lang(){return root.lang==='nl'?'nl':'en';}
function T(en,nl){return lang()==='nl'?nl:en;}
function $(s,r){return (r||doc).querySelector(s);}
function $$(s,r){return [].slice.call((r||doc).querySelectorAll(s));}
var NOTOC={home:1,map:1,search:1,news:1,updates:1,printsel:1};
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function activePage(){return $('#pages > article.page:not([hidden])');}
function txt(h){var c=h.cloneNode(true);$$('button,.printbtn,.live,small',c).forEach(function(x){x.parentNode.removeChild(x);});$$(lang()==='nl'?'.en-x':'.nl-x',c).forEach(function(x){x.parentNode.removeChild(x);});return c.textContent.replace(/\s+/g,' ').trim();}
function buildToc(){
  $$('.u-toc').forEach(function(e){e.parentNode.removeChild(e);});
  var pg=activePage();if(!pg)return;
  var k=pg.id.slice(2);if(NOTOC[k])return;
  if(pg.scrollHeight<3*window.innerHeight)return;
  var hs=$$('h2,h3',pg).filter(function(h){return !h.closest('details,.u-toc,.pn,.printbar')&&h.offsetParent!==null&&txt(h).length>1&&!/^(NL:|In plain words|In gewone woorden)/.test(txt(h));});
  var n2=hs.filter(function(h){return h.tagName==='H2';}).length;
  if(hs.length>40&&n2>=3)hs=hs.filter(function(h){return h.tagName==='H2';});
  if(hs.length>60)hs=hs.slice(0,60);
  if(hs.length<3)return;
  var d=doc.createElement('details');d.className='u-toc';
  var items=hs.map(function(h,i){
    if(!h.id)h.id='toc-'+k+'-'+i;
    return '<li class="'+(h.tagName==='H3'&&n2>0?'l3':'l2')+'"><a href="#'+h.id+'" data-toc="'+h.id+'">'+txt(h).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];})+'</a></li>';
  }).join('');
  d.innerHTML='<summary>'+T('On this page','Op deze pagina')+' <small>('+hs.length+')</small></summary><nav aria-label="'+T('On this page','Op deze pagina')+'"><ol>'+items+'</ol></nav>';
  var h1=$('h1',pg)||$('h2',pg),anchor=h1;
  if(h1&&h1.nextElementSibling&&h1.nextElementSibling.classList.contains('sub'))anchor=h1.nextElementSibling;
  if(anchor&&anchor.parentNode)anchor.parentNode.insertBefore(d,anchor.nextSibling);
}
doc.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('a[data-toc]');if(!a)return;
  e.preventDefault();
  var h=doc.getElementById(a.dataset.toc);if(!h)return;
  h.scrollIntoView({block:'start',behavior:reduce?'auto':'smooth'});
  h.setAttribute('tabindex','-1');try{h.focus({preventScroll:true});}catch(x){h.focus();}
});
var tt=null;
function sched(){clearTimeout(tt);tt=setTimeout(buildToc,250);setTimeout(buildToc,1200);}
window.addEventListener('hashchange',sched);
new MutationObserver(function(){sched();}).observe(root,{attributes:true,attributeFilter:['lang']});
window.addEventListener('load',sched);
sched();

/* back to top */
var b=doc.createElement('button');b.type='button';b.className='u-btt';
function lab(){var s=T('Back to top','Naar boven');b.innerHTML='<span aria-hidden="true">↑</span> <span class="u-btt-t">'+s+'</span>';b.setAttribute('aria-label',s);}
lab();doc.body.appendChild(b);
function upd(){b.classList.toggle('on',window.scrollY>1.5*window.innerHeight);}
window.addEventListener('scroll',upd,{passive:true});window.addEventListener('resize',upd);
new MutationObserver(lab).observe(root,{attributes:true,attributeFilter:['lang']});
b.addEventListener('click',function(){
  window.scrollTo({top:0,behavior:reduce?'auto':'smooth'});
  var h=$('#pages > article.page:not([hidden]) h1')||$('#pages');
  if(h){h.setAttribute('tabindex','-1');try{h.focus({preventScroll:true});}catch(x){}}
});
upd();
})();
