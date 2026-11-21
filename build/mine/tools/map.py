"""Builds the page '#map': a layered map of every dated incident in the file."""
import sys,json,math,html,re,collections
from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
sys.path.insert(0,M+'tools')
import mapclass,mapcur
from mapgeo import G,CEN
from evdata import C
e=html.escape

# ---------- projection (Lambert azimuthal equal-area, centred on 52N 10E) ----------
P0,L0=math.radians(52),math.radians(10)
def proj(lat,lon):
    p,l=math.radians(lat),math.radians(lon)
    c=1+math.sin(P0)*math.sin(p)+math.cos(P0)*math.cos(p)*math.cos(l-L0)
    if c<1e-9: return (9e9,9e9)
    k=math.sqrt(2/c)
    return (k*math.cos(p)*math.sin(l-L0), -k*(math.cos(P0)*math.sin(p)-math.sin(P0)*math.cos(p)*math.cos(l-L0)))
corners=[proj(a,b) for a,b in [(63.4,-24.6),(36.8,-9.6),(34.5,34.7),(70.2,31.2),(71.3,25.5),(34.8,24.5),(33.4,14.4),(66.5,-14.5),(51.4,-10.6),(43.2,30.0)]]
x0=min(c[0] for c in corners); x1=max(c[0] for c in corners); y0=min(c[1] for c in corners); y1=max(c[1] for c in corners)
W=1000.0; S=W/(x1-x0)*0.96; PADX=W*0.02; H=round((y1-y0)*S+2*PADX)
def XY(lat,lon):
    x,y=proj(lat,lon); return ((x-x0)*S+PADX,(y-y0)*S+PADX)

# ---------- country outlines ----------
T=json.load(open(M+'tools/countries-50m.json'))
sx,sy=T['transform']['scale']; tx,ty=T['transform']['translate']
ARCS=[]
for a in T['arcs']:
    x=y=0; pts=[]
    for dx,dy in a:
        x+=dx; y+=dy; pts.append((x*sx+tx,y*sy+ty))
    ARCS.append(pts)
def ring(idx):
    out=[]
    for i in idx:
        a=ARCS[i] if i>=0 else ARCS[~i][::-1]
        out+=a if not out else a[1:]
    return out
def dp(pts,tol):
    if len(pts)<3: return pts
    keep=[False]*len(pts); keep[0]=keep[-1]=True; st=[(0,len(pts)-1)]
    while st:
        a,b=st.pop()
        if b<=a+1: continue
        ax,ay=pts[a]; bx,by=pts[b]; dx,dy=bx-ax,by-ay; n=math.hypot(dx,dy) or 1e-9
        m=0;mi=-1
        for i in range(a+1,b):
            d=abs((pts[i][0]-ax)*dy-(pts[i][1]-ay)*dx)/n if n>1e-6 else math.hypot(pts[i][0]-ax,pts[i][1]-ay)
            if d>m: m=d;mi=i
        if m>tol: keep[mi]=True; st+= [(a,mi),(mi,b)]
    return [p for p,k in zip(pts,keep) if k]
MAR=60
def inside(p): return -MAR<=p[0]<=W+MAR and -MAR<=p[1]<=H+MAR
def path(geom):
    polys=geom['arcs'] if geom['type']=='MultiPolygon' else [geom['arcs']]
    d=''
    for poly in polys:
        for r in poly:
            ll=ring(r)
            if not any(-40<=lo<=60 and 25<=la<=75 for lo,la in ll): continue
            pts=[XY(la,lo) for lo,la in ll]
            if not any(inside(p) for p in pts): continue
            # squash runs of far-outside points
            q=[]
            for p in pts:
                if inside(p) or not q or inside(q[-1]): q.append(p)
                else: q[-1]=p if False else q[-1]
            q=dp(q,0.45)
            if len(q)<4: continue
            s=''; last=None
            for p in q:
                t='%.1f,%.1f'%p
                if t!=last: s+=('M' if last is None else 'L')+t; last=t
            d+=s+'Z'
    return d
ALIAS={}
land=[]
for g in T['objects']['countries']['geometries']:
    n=g['properties']['name']
    if n in('Antarctica','Greenland') or g.get('arcs') is None: continue
    d=path(g)
    if d: land.append((n,d))
cov=[(n,d) for n,d in land if n in CEN]; ctx=[(n,d) for n,d in land if n not in CEN]
assert len(cov)==31,[n for n in CEN if n not in dict(cov)]
SVGLAND='<g class="mp-ctx">'+''.join('<path d="%s"/>'%d for n,d in ctx)+'</g><g class="mp-cov">'+''.join('<path data-c="%s" d="%s"><title>%s</title></path>'%(e(n),d,e(n)) for n,d in cov)+'</g>'

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
FAM=[('hyb','Physical and hybrid attacks','Fysieke en hybride aanvallen','#d55e00'),
     ('svc','Essential services hit','Essentiële diensten geraakt','#0072b2'),
     ('inf','Misleading information and spying','Misleidende informatie en spionage','#a4509a'),
     ('biz','Companies and defence industry','Bedrijven en defensie-industrie','#8c6d1f')]
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
# ---------- layer 'Ready at home': stock-up advice per country (from prepare_data.json, fields already on the file) ----------
PD=json.load(open(M+'tools/prepare_data.json',encoding='utf-8'))
def shorten(t,maxc=300,maxs=2):
    t=re.sub(r'\s+',' ',t or '').strip()
    ss=re.split(r"(?<=[.!?])\s+(?=[A-Z0-9'\"\u2018\u201c(\u00c0-\u00de])",t)
    out=[]
    for s_ in ss:
        if out and (len(out)>=maxs or len(' '.join(out+[s_]))>maxc): break
        out.append(s_)
    return ' '.join(out)
DURL={'3d':'72 h','1w':'1 wk','10d':'10\u201314 d','':'\u2014'}
PREP={}
for r_ in PD['countries']:
    c_=r_['country']
    if c_=='EU': continue
    assert c_ in CEN,c_
    adv=r_['adv']; assert adv in 'CRN'
    PREP[c_]=dict(s=adv,d=DURL[r_['bucket']] if adv!='N' else '\u2014',m=(r_['mail']=='yes'),h=r_['hours_s'],w=r_['water_s'],la=r_['latest_s'],
        en=shorten(r_['text']),nl=shorten(r_['text_nl']),g=r_['guide'],u=(r_['sources'][0]['url'] if r_['sources'] else ''))
assert len(PREP)==31 and set(PREP)==set(CEN),set(CEN)^set(PREP)
EUP=[r_ for r_ in PD['countries'] if r_['country']=='EU'][0]
PREU=dict(en=shorten(EUP['text'],400,2),nl=shorten(EUP['text_nl'],400,2),u=EUP['sources'][0]['url'])

DATA=json.dumps(dict(ev=OUT,prep=PREP,preu=PREU,fam=FAM,lay=LAY,icon=ICON,camp=CAMP,pg=PG,ac=AC,W=W,H=H,
  cen={k:[round(v,1) for v in XY(*CEN[k])] for k in CEN},off=LBLOFF,
  sea=[[round(XY(a,b)[0],1),round(XY(a,b)[1],1),en,nl] for a,b,en,nl in SEA]),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')

SEC=open(M+'tools/map_sec.html',encoding='utf-8').read()
nmo=sum(1 for r in OUT if not r['m'])
for k,v in (('@@N@@',n),('@@NC@@',nc),('@@NMO@@',nmo),('@@W@@',int(W)),('@@H@@',H),('@@LAND@@',SVGLAND),('@@NPL@@',npl),('@@NAP@@',nap),('@@NCO@@',nco)): SEC=SEC.replace(k,str(v))

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
