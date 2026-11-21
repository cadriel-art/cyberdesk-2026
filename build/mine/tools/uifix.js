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
var SEL='#ev-count,.hn,.ev-who,.lv,.filters button,#p-register td,#p-register .tag,.gapx.prof small,#ps-summary,#ps-summary b,.lad-h b,.lad p.small,.tag,.pill,th,summary,option,legend,label,button,h3,h4,h5,h3 small,h4 small,.count,.brand small,.nw-fh';
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
    fixIds();fixHeadings();failuresNote();translate();
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
