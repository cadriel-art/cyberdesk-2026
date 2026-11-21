"""Collect every dated event in the file into one list for the map. No side effects."""
import ast,re,json
from bs4 import BeautifulSoup
M='/home/user/cyberdesk-2026/build/mine/'
def lit(f,name):
    t=ast.parse(open(M+'tools/'+f+'.py',encoding='utf-8').read())
    for n in t.body:
        if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id==name:
            return ast.literal_eval(n.value)
MON={'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12,'spring':4,'summer':7,'autumn':10,'winter':1}
def when(lbl):
    """(year, month or 0) of the first moment named in a date label."""
    y=re.search(r'(20\d\d)',lbl); 
    if not y: return None
    y=int(y.group(1)); head=lbl[:lbl.find(str(y))+4].lower()
    ms=[MON[w] for w in re.findall(r'[a-z]+',head) if w in MON] or [MON[w[:3]] for w in re.findall(r'[a-z]+',head) if w[:3] in MON and len(w)>3 and w not in('mark','mart','junction','deck','decided','nove')]
    # a range like "24 Sep – 2 Oct 2025": take the first month
    return (y, ms[0] if ms else 0)
def collect():
    E=[]
    def add(src,country,date,text,st,title='',cat=''):
        E.append(dict(src=src,country=country,date=date,text=text,st=st,title=title,cat=cat))
    for f in ['hybrid','water','transport','elections','health','defence']:
        for r in lit(f,'EV'):
            if len(r)==4 or f in('hybrid','water'): add(f,'Belgium',r[0],r[2],r[3],r[1])
            else: add(f,'Belgium',r[0],r[3],r[4],r[2],r[1])
    for r in lit('cables','EV'): add('cables',r[2],r[0],r[3],r[4],r[2],r[1])
    for r in lit('schools','EV'): add('schools',r[1],r[0],r[3],r[4],r[2],'')
    for f in ['hybrid2','water2','transport2','elections2','health2','defence2']:
        for c,v in lit(f,'D').items():
            for ev in v[0]: add(f[:-1]+'eu',c,ev[0],ev[1],ev[2])
    R=BeautifulSoup(open(M+'cyber-incident-register.html',encoding='utf-8').read(),'html.parser')
    for tr in R.select('#reg2t tbody tr'):
        td=tr.find_all('td')
        add('reg2',tr['data-c'],td[0].get_text(' ',strip=True),td[2].get_text(' ',strip=True),{'Confirmed':'C','Reported':'R','Claimed':'K'}.get(td[3].get_text(strip=True),'R'),'',tr['data-s']+'|'+tr['data-t']+'|'+tr.get('data-sub',''))
    return E
if __name__=='__main__':
    import collections
    E=collect(); print(len(E),collections.Counter(e['src'] for e in E))
    print(collections.Counter(e['country'] for e in E if e['src'] in('cables','schools')))
    print(collections.Counter(e['cat'] for e in E if e['src']!='reg2'))
    print(collections.Counter(e['st'] for e in E))
    bad=[e['date'] for e in E if not when(e['date'])]; print('nodate',bad)
    print(sorted(set((e['date'],when(e['date'])) for e in E if when(e['date']) and when(e['date'])[1]==0))[:40])
    json.dump(E,open(M+'tools/_events.json','w'),ensure_ascii=False)
