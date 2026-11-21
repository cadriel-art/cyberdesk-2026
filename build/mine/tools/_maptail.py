# ---------- events ----------
E=mapclass.build(); byi={x['i']:x for x in E}
def txt(s): return re.sub(r'\s+',' ',BeautifulSoup(s,'html.parser').get_text(' ')).strip()
foll=collections.defaultdict(list)
for k,v in mapcur.FOLLOW.items(): foll[v].append(byi[k])
case_of={v:k for k,v in mapcur.CASE.items()}
AC={'RU':'Russia (state services)','PR':'Pro-Russian groups','IR':'Iran','BY':'Belarus','CN':'China','KP':'North Korea','CR':'Criminal groups','DG':'Drug gangs','EX':'Extremists, no state','OT':'Other','FR':'A friendly state','UN':'A state, not named','NO':'Nobody named','XX':'Not an attack'}
OUT=[]
for x in E:
    i=x['i']
    if i in mapcur.DROP or i in mapcur.FOLLOW or not x['w'] or x['w'][0]<2025: continue
    pl=mapcur.PL.get(i,x['pl']); c=x['country']
    if isinstance(pl,tuple): lat,lon,label,ap=pl; prec=1 if ap else 0
    elif pl: g=G[pl]; lat,lon=g[0],g[1]; label=pl; prec=1 if len(g)>3 and g[3] else 0
    else:
        if c not in CEN: continue
        lat,lon=CEN[c]; label=''; prec=2
    if isinstance(pl,tuple) and c not in CEN: c=''
    X,Y=XY(lat,lon)
    lay=mapcur.LY.get(i) or x['lay']
    if x['src']=='reg2' and 'food' in lay and not re.search(r'freezer|refriger|supermarket|food|grocer',x['text'].lower()):
        lay=[('business' if k=='food' else k) for k in lay]
    lay=list(dict.fromkeys(lay))
    st=x['st']; fl=sorted(foll.get(i,[]),key=lambda f:(f['w'][0],f['w'][1]))
    rec=dict(i=i,y=x['w'][0],m=x['w'][1],d=x['date'],c=c,p=label,pr=prec,x=round(X,1),yy=round(Y,1),l=lay,s=st,
             np=1 if ('N' in st or any('N' in f['st'] for f in fl)) else 0, cf=1 if 'C' in st else 0,
             t=txt(x['title']) if x['src']!='reg2' else '', tx=txt(x['text']), g=x['src'],
             f=[[f['date'],txt(f['text'])] for f in fl])
    if i in case_of:
        cs=C[case_of[i]]; rec['lv']=cs[6]; rec['a']=cs[4]; rec['w']=cs[5]; rec['by']=cs[8]; rec['ct']=cs[1]
        if cs[6]=='X': rec['np']=1
    OUT.append(rec)
ids={r['i'] for r in OUT}
CAMP=[]
for k,en,nl,nen,nnl,lst in mapcur.CAMP:
    miss=[q for q in lst if q not in ids]; assert not miss,(k,miss)
    CAMP.append(dict(k=k,en=en,nl=nl,nen=nen,nnl=nnl,ids=lst))
for k in mapcur.CASE.values(): assert k in ids,k

# ---------- families, layers, icons ----------
FAM=[('hyb','Physical and hybrid attacks','Fysieke en hybride aanvallen','#c0392b'),
     ('svc','Essential services hit','Essentiële diensten geraakt','#0f766e'),
     ('inf','Information war and spying','Informatieoorlog en spionage','#7c3aed'),
     ('biz','Companies and defence industry','Bedrijven en defensie-industrie','#b45309')]
LAY=[('drones','Drones and balloons','Drones en ballonnen','hyb'),
     ('sabotage','Sabotage and arson','Sabotage en brandstichting','hyb'),
     ('cables','Sea cables and pipelines','Zeekabels en pijpleidingen','hyb'),
     ('jamming','Satellite-signal jamming','Storing van satellietsignalen','hyb'),
     ('intim','Hoax threats and intimidation','Valse dreigingen en intimidatie','hyb'),
     ('food','Food and shop freezers','Voedsel en winkeldiepvriezers','svc'),
     ('water','Water','Water','svc'),
     ('energy','Energy','Energie','svc'),
     ('health','Health','Gezondheid','svc'),
     ('transport','Transport and ports','Vervoer en havens','svc'),
     ('schools','Schools and universities','Scholen en universiteiten','svc'),
     ('gov','Government and public services','Overheid en openbare diensten','svc'),
     ('elections','Elections and disinformation','Verkiezingen en desinformatie','inf'),
     ('spying','Spying','Spionage','inf'),
     ('business','Companies: ransomware and data leaks','Bedrijven: ransomware en datalekken','biz'),
     ('defence','Defence','Defensie','biz')]
ICON={
 'drones':'M-7,-6h14M0,-6v3M-4,-3h8l-2,8h-4z',
 'sabotage':'M0,8c-4,0-6,-3-6,-5c0,-3 3,-4 3,-7c0,-2-1,-3-1,-3c4,1 5,4 5,6c1,-1 1,-3 1,-3c2,2 4,4 4,7c0,2-2,5-6,5z',
 'cables':'M-9,2c2,-5 4,-6 6,-3M3,1c1,4 4,3 6,-2M-2,-2l4,4M2,-2l-4,4',
 'jamming':'M-7,5a9,9 0 0,1 14,0M-4,2a5,5 0 0,1 8,0M0,-1a1.6,1.6 0 1,0 0.1,0',
 'intim':'M0,-8l8,14h-16zM0,-3v4M0,3v1.5',
 'food':'M0,-9v18M-8,-4.5l16,9M-8,4.5l16,-9',
 'water':'M0,-9c4,5 6,7 6,10a6,6 0 0,1 -12,0c0,-3 2,-5 6,-10z',
 'energy':'M2,-9l-8,10h5l-1,8l8,-10h-5z',
 'health':'M-2.5,-8h5v5.5h5.5v5h-5.5v5.5h-5v-5.5h-5.5v-5h5.5z',
 'transport':'M0,-9l2,7l7,3v2l-7,-1.5l-1,5l3,2v1.5l-4,-1l-4,1v-1.5l3,-2l-1,-5l-7,1.5v-2l7,-3z',
 'schools':'M-9,-3l9,-4l9,4l-9,4zM-5,0.5v3.5c0,2 10,2 10,0v-3.5',
 'gov':'M-9,-1l9,-6l9,6M-7,-1v8M7,-1v8M-3,7v-5h6v5M-8,8h16',
 'elections':'M-7,-7h14v14h-14zM-3.5,0l3,3l6,-6.5',
 'spying':'M-9,0c4.5,-5.5 13.5,-5.5 18,0c-4.5,5.5 -13.5,5.5 -18,0M0,-2.2a2.2,2.2 0 1,0 0.1,0',
 'business':'M-5,-1v-3a5,5 0 0,1 10,0v3M-7,-1h14v9h-14z',
 'defence':'M0,-9l7.5,3v6c0,5 -4.5,7.5 -7.5,9c-3,-1.5 -7.5,-4 -7.5,-9v-6z'}
LBLOFF={'Luxembourg':[-2,20],'Liechtenstein':[26,4],'Malta':[0,16],'Cyprus':[0,17],'Slovenia':[-16,13],'Slovakia':[10,-9],'Belgium':[-20,-6],'Netherlands':[-24,-6],'Denmark':[-16,-8],'Switzerland':[-18,8],'Austria':[10,9],'Czechia':[2,-11],'Croatia':[8,8],'Hungary':[8,6],'Estonia':[10,-4],'Latvia':[12,0],'Lithuania':[6,6],'Ireland':[-10,2],'Portugal':[-10,4],'Iceland':[0,-14],'Norway':[-14,6],'Greece':[-8,2]}
SEA=[(56.2,2.5,'North Sea','Noordzee'),(57.2,19.6,'Baltic Sea','Oostzee'),(43.6,31.5,'Black Sea','Zwarte Zee'),(36.0,16.5,'Mediterranean Sea','Middellandse Zee'),(47.5,-12.5,'Atlantic Ocean','Atlantische Oceaan'),(66.5,0.5,'Norwegian Sea','Noorse Zee')]
PG={'hybrid':'Drones, sabotage, hybrid: Belgium','hybrideu':'Drones, sabotage, hybrid: 30 countries','water':'Water: Belgium','watereu':'Water: 30 countries','transport':'Transport and ports: Belgium','transporteu':'Transport and ports: 30 countries','elections':'Elections and democracy: Belgium','electionseu':'Elections and democracy: 30 countries','health':'Health: Belgium','healtheu':'Health: 30 countries','defence':'The defence side: Belgium','defenceeu':'The defence side: 30 countries','cables':'Sea cables and satellite signals','schools':'Children and schools','reg2':'Register 2025–2026'}
used=collections.Counter(k for r in OUT for k in r['l']); assert all(k in dict((a,b,c,d) and (a,b) for a,b,c,d in LAY) for k in used),used
n=len(OUT); nc=len({r['c'] for r in OUT if r['c']}); npl=sum(1 for r in OUT if r['pr']==0); nap=sum(1 for r in OUT if r['pr']==1); nco=sum(1 for r in OUT if r['pr']==2)
DATA=json.dumps(dict(ev=OUT,fam=FAM,lay=LAY,icon=ICON,camp=CAMP,pg=PG,ac=AC,W=W,H=H,
  cen={k:[round(v,1) for v in XY(*CEN[k])] for k in CEN},off=LBLOFF,
  sea=[[round(XY(a,b)[0],1),round(XY(a,b)[1],1),en,nl] for a,b,en,nl in SEA]),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')

SEC='''<section id="map">
<h2>The map: where it happened</h2>
<p class="sub">@@N@@ incidents in @@NC@@ countries and at sea, January 2025 to November 2026. Pick a story, switch layers on and off, move through time, and click any mark for the facts behind it.</p>
<div class="plainbox"><div class="pb-h">In plain words</div><p>The map shows two different things at the same time. A <b>pin</b> stands on a place that a source actually names, with a small picture of the kind of attack. A <b>numbered circle</b> in the middle of a country counts the incidents where we only know the country, so no pin can be placed; it says nothing about the town. The darker a country is shaded, the more incidents it has in the file. A <b>filled</b> pin is a confirmed incident, a <b>hollow</b> one is only reported, claimed or suspected, and a <b>grey crossed</b> one was investigated and found not to be an attack, or was never proven.</p><p class="pb-nl"><b>NL:</b> De kaart toont twee dingen tegelijk. Een <b>speld</b> staat op een plaats die een bron echt noemt, met een pictogram van het soort aanval. Een <b>genummerde cirkel</b> in het midden van een land telt de incidenten waarvan we alleen het land kennen, dus waar geen speld kan staan; die zegt niets over de stad. Hoe donkerder een land gekleurd is, hoe meer incidenten het in dit dossier heeft. Een <b>gevulde</b> speld is een bevestigd incident, een <b>holle</b> alleen gemeld, beweerd of vermoed, en een <b>grijze doorkruiste</b> werd onderzocht en bleek geen aanval, of werd nooit bewezen. De beschrijvingen van de incidenten zijn in het Engels.</p></div>
<div id="mp" class="mp">
 <div class="mp-stories"><span class="mp-slabel" data-en="Start with a story:" data-nl="Begin met een verhaal:">Start with a story:</span><span id="mp-story"></span></div>
 <div class="mp-body">
  <div class="mp-mapcol">
   <div class="mp-top">
    <div class="mp-row mp-row1">
     <div class="mp-seg" id="mp-view" role="group"><button type="button" data-v="pl" aria-pressed="true" data-en="Places" data-nl="Plaatsen">Places</button><button type="button" data-v="tot" aria-pressed="false" data-en="Country totals" data-nl="Landentotalen">Country totals</button></div>
     <label><span data-en="Colour by" data-nl="Kleur volgens">Colour by</span> <select id="mp-mode"><option value="lay" data-en="Kind of attack" data-nl="Soort aanval">Kind of attack</option><option value="lv" data-en="Proof level: how firm is the blame" data-nl="Bewijsniveau: hoe stevig is de beschuldiging">Proof level</option><option value="who" data-en="Who is formally named" data-nl="Wie formeel wordt aangewezen">Who is formally named</option></select></label>
     <label><span data-en="Show" data-nl="Toon">Show</span> <select id="mp-st"><option value="all" data-en="Everything" data-nl="Alles">Everything</option><option value="conf" data-en="Confirmed incidents only" data-nl="Alleen bevestigde incidenten">Confirmed only</option><option value="unc" data-en="Only reported, claimed or suspected" data-nl="Alleen gemeld, beweerd of vermoed">Reported only</option><option value="np" data-en="Only: not an attack, or not proven" data-nl="Alleen: geen aanval, of niet bewezen">Not an attack</option></select></label>
     <label><span data-en="Waves across borders" data-nl="Golven over grenzen">Waves across borders</span> <select id="mp-camp"><option value="" data-en="None" data-nl="Geen">None</option></select></label>
    </div>
    <details class="mp-lays" id="mp-lays" open><summary data-en="Layers" data-nl="Lagen">Layers</summary><div class="mp-lay" id="mp-lay"></div></details>
    <div class="mp-time">
     <button type="button" id="mp-play" aria-label="Play">▶</button>
     <input type="range" id="mp-t" min="0" max="23" value="23" step="1" aria-label="Time">
     <select id="mp-tm" aria-label="Time mode"><option value="cum" data-en="Up to this month" data-nl="Tot en met deze maand">Up to this month</option><option value="one" data-en="This month only" data-nl="Alleen deze maand">This month only</option></select>
     <b id="mp-tl"></b>
    </div>
   </div>
   <div class="mp-printnote" id="mp-printnote"></div>
   <div class="mp-wrap">
    <svg id="mp-svg" viewBox="0 0 @@W@@ @@H@@" role="img" aria-label="Map of Europe with incident marks"><rect class="mp-sea" x="-2000" y="-2000" width="5000" height="5000"/>@@LAND@@<g id="mp-sealbl"></g><g id="mp-lines"></g><g id="mp-lbl"></g><g id="mp-badge"></g><g id="mp-mk"></g></svg>
    <div class="mp-zoom"><button type="button" data-z="in" aria-label="Zoom in">+</button><button type="button" data-z="out" aria-label="Zoom out">−</button><button type="button" data-z="reset" aria-label="Reset">⟲</button></div>
    <div class="mp-count" id="mp-count"></div>
   </div>
   <div class="mp-legend" id="mp-legend"></div>
  </div>
  <aside class="mp-panel" id="mp-panel">
   <div class="mp-card" id="mp-card"></div>
   <div class="mp-campnote" id="mp-campnote"></div>
   <div class="mp-pbox"><h4 data-en="When it happened" data-nl="Wanneer het gebeurde">When it happened</h4><div class="mp-spark" id="mp-spark"></div><p class="mp-hint" data-en="Click a month to see only that month." data-nl="Klik op een maand om alleen die maand te zien.">Click a month to see only that month.</p></div>
   <div class="mp-pbox"><h4 data-en="Where it happened" data-nl="Waar het gebeurde">Where it happened</h4><div id="mp-cbars"></div></div>
   <div class="mp-pbox"><h4 data-en="What kind" data-nl="Welk soort">What kind</h4><div id="mp-lbars"></div></div>
  </aside>
 </div>
 <details class="mp-listbox" id="mp-listbox"><summary id="mp-listsum"></summary><div id="mp-list"></div></details>
</div>
<h3>How to read this map honestly</h3>
<ul>
<li><b>It shows what became public, not everything that happened.</b> Countries that report openly look worse than countries that stay silent. The shading says "how much is on record here", not "how unsafe this country is".</li>
<li><b>Where the mark sits:</b> @@NPL@@ incidents sit on a named place, @@NAP@@ on an approximate area such as a stretch of sea, and @@NCO@@ are counted in the circle in the middle of their country, because no source names the town.</li>
<li><b>Month unknown:</b> some incidents are only dated by year. They appear in "up to this month" once that year has ended, and always in the last position of the slider.</li>
<li><b>Colour by proof level</b> uses the scale of the <a href="#evidence">evidence tracker</a>. Only the cases studied there have a level; all other marks turn pale.</li>
<li><b>"Who is formally named"</b> colours a mark only when a court, a prosecutor or a government has named someone. Claims by the attackers themselves and guesses by researchers are left pale on purpose.</li>
<li><b>Waves across borders</b> draws lines from the first incident of a wave to the others. A line means "same wave", not "same culprit". The note in the panel says what is and is not proven.</li>
<li><b>One incident, one mark.</b> Where the same incident appears on several pages of this file it is shown once. Later developments, such as a verdict or a closed investigation, are inside the card of the original incident.</li>
</ul>
</section>'''
for k,v in (('@@N@@',n),('@@NC@@',nc),('@@W@@',int(W)),('@@H@@',H),('@@LAND@@',SVGLAND),('@@NPL@@',npl),('@@NAP@@',nap),('@@NCO@@',nco)): SEC=SEC.replace(k,str(v))

R=BeautifulSoup(open(M+'cyber-incident-register.html',encoding='utf-8').read(),'html.parser')
old=R.find('section',id='map')
if old: old.decompose()
R.find('section',id='glossary').insert_before(BeautifulSoup(SEC,'html.parser'))
open(M+'cyber-incident-register.html','w',encoding='utf-8').write(str(R))

b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
if "'k': 'map'" not in t:
    a="{'k': 'evidence', "
    assert a in t
    t=t.replace(a,"{'k': 'map', 'en': 'The map: where it happened', 'nl': 'De kaart: waar het gebeurde', 'src': ('R', 'map')}, "+a,1); open(b,'w',encoding='utf-8').write(t)
l=M+'tools/layman.py'; t=open(l,encoding='utf-8').read()
if "INTRO['map']" not in t:
    t=t.rstrip()+'''
INTRO['map']=("Every incident in this file on one map of Europe: pins where a place is known, counts where only the country is known, layers you switch on and off, and a time slider.","Elk incident uit dit dossier op één kaart van Europa: spelden waar de plaats bekend is, tellingen waar alleen het land bekend is, lagen die je aan en uit zet, en een tijdschuif.")
'''
    open(l,'w',encoding='utf-8').write(t)

CSS=open(M+'tools/map.css',encoding='utf-8').read(); JS=open(M+'tools/map.js',encoding='utf-8').read().replace('@@DATA@@',DATA)
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '.mp-wrap' not in t:
    t=t.replace('</style>',CSS+'</style>',1)
    t=t.rstrip()+'\n<script>\n'+JS+'\n</script>\n'
    open(a,'w',encoding='utf-8').write(t)
print('map ok',n,'events',nc,'countries; place',npl,'area',nap,'country',nco,'| svg kb',len(SVGLAND)//1024,'data kb',len(DATA)//1024)
