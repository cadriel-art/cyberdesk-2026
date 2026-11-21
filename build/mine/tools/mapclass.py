import re,json,sys,collections
sys.path.insert(0,'.')
from mapcollect import collect,when
from mapgeo import G,CEN
LAY=['food','drones','sabotage','cables','jamming','water','energy','health','transport','elections','defence','schools','gov','spying','business']
SUB={'hybrid':None,'hybrideu':None,'water':'water','watereu':'water','transport':'transport','transporteu':'transport','elections':'elections','electionseu':'elections','health':'health','healtheu':'health','defence':'defence','defenceeu':'defence','cables':'cables','schools':'schools'}
KW=[('jamming',r'jamm|\bgps\b|satellite signal|spoof|navigation signal|satellite navigation'),
('cables',r'\bcables?\b|anchor|pipeline'),
('drones',r'\bdrones?\b|balloon'),
('food',r'freezer|supermarket|\bfood\b|dairy|meat |brewer|grocer'),
('sabotage',r'arson|sabotag|explosi|incendiar|set fire|\bfires?\b|parcel|bomb'),
('spying',r'\bspy|spying|espionage|spies\b|intelligence officer')]
def layers(e):
    t=(e['title']+' '+e['text']).lower(); out=[]
    for k,rx in KW:
        if re.search(rx,t): out.append(k)
    if e['src']=='reg2':
        s,ty,sub=e['cat'].split('|')
        m={'health':'health','gov':'gov','education':'schools','energy':'energy','water':'water','transport':'transport','food':'food','defence':'defence','telecom':'business','finance':'business','other':'business','media':'business'}.get(s,'business')
        out=[x for x in out if x in('drones','sabotage','jamming')]  # in the register the sector decides
        if ty=='spy': out.append('spying')
        out.append(m)
        if sub and sub!='none' and sub not in out: out.append(sub)
    else:
        s=SUB[e['src']]
        if e['src'] in('water','watereu','health','healtheu','schools','elections','electionseu'): out=[x for x in out if x not in('food','cables')]+[s]
        elif s: out.append(s)
        if not out: out=['sabotage'] if e['src'].startswith('hybrid') else [s]
    seen=[]; [seen.append(x) for x in out if x not in seen]; return seen
NAMES=sorted([k for k,v in G.items() if v],key=len,reverse=True)
def place(e):
    t=e['title']+' '+e['text']
    hits=[]
    for n in NAMES:
        m=re.search(r'(?<![\w-])'+re.escape(n)+r'(?![\w-])',t)
        if m: hits.append((m.start(),n))
    hits.sort()
    c=e['country']
    for pos,n in hits:
        g=G[n]
        if g[2]==c or (g[2]=='' ): return n
    return ''
def status(st):
    if len(st)<=3: return st
    s=st.lower(); o=''
    if 'confirmed' in s: o+='C'
    if 'reported' in s or 'on record' in s: o+='R'
    if 'claim' in s: o+='K'
    if 'suspected' in s: o+='S'
    if 'not proven' in s or 'not a confirmed' in s: o+='N'
    return o or 'R'
def build():
    out=[]
    import hashlib,os
    P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'_mapids.json'); IDS=json.load(open(P)); nxt=max(max(IDS.values())+1,1000); ch=False
    for e in collect():
        w=when(e['date'])
        k=hashlib.md5((e['src']+'|'+e['country']+'|'+e['date']+'|'+(e['title']+e['text'])[:60]).encode()).hexdigest()[:12]
        if k not in IDS: IDS[k]=nxt; nxt+=1; ch=True
        i=IDS[k]
        e['i']=i; e['w']=w; e['lay']=layers(e); e['pl']=place(e); e['st']=status(e['st'])
        out.append(e)
    if ch: json.dump(IDS,open(P,'w'))
    return out
if __name__=='__main__':
    E=build()
    for e in E:
        if not e['w'] or e['w'][0]<2025: flag='OLD'
        elif e['country'] not in CEN: flag='CTR'
        else: flag=''
        print('%d|%s|%s|%s|%s|%s|%s|%s%s'%(e['i'],e['src'][:6],e['country'][:14],e['date'][:12],','.join(e['lay']),e['pl'],flag,(e['title'][:30]+': ' if e['title'] else ''),e['text'][:95].replace('\n',' ')))
