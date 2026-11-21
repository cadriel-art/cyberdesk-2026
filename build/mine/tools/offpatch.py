"""Runs after offline.py: makes the offline file truly offline (no web-font requests)."""
import re
p='/home/user/cyberdesk-2026/build/mine/cyber-desk-offline.html'
s=open(p,encoding='utf-8').read(); n=len(s)
s=re.sub(r'<link[^>]*fonts\.(?:googleapis|gstatic)\.com[^>]*>','',s)
if 'name="viewport"' not in s:
    s=re.sub(r'(<head[^>]*>)',r'\1<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">',s,count=1)
open(p,'w',encoding='utf-8').write(s)
print('offpatch: web-font links removed' if len(s)<n else 'offpatch: nothing to remove')

# UI fixes in the static markup of both output files (the same fixes also run at load time in uifix.js):
# 1. the second id="s-ai" (page "agents") becomes s-agents, 2. "Terms on this page" boxes start closed.
for _p in (p, p.replace('cyber-desk-offline.html','cyber-desk.html')):
    try: _s=open(_p,encoding='utf-8').read()
    except FileNotFoundError: continue
    _a=_s.find('<section id="s-ai">'); _b=_s.find('<section id="s-ai">',_a+1) if _a>=0 else -1
    if _b>=0: _s=_s[:_b]+'<section id="s-agents">'+_s[_b+len('<section id="s-ai">'):]
    _s=re.sub(r'(<details class="termsbox")\s+open(?:="[^"]*")?',r'\1',_s)
    open(_p,'w',encoding='utf-8').write(_s)
print('offpatch: ids and termsbox fixed')

# UX round 3 (C): the saved file's Updates page (and, via home2.py, the home "What's new") use the saved snapshot of the live
# `updates` collection (tools/updates_snapshot.json, newest by `order` first) instead of the three updates embedded in offline.py.
import json
_snap=json.load(open('/home/user/cyberdesk-2026/build/mine/tools/updates_snapshot.json',encoding='utf-8'))
_snap.sort(key=lambda u:(u.get('order',0),u.get('id','')),reverse=True)
_s=open(p,encoding='utf-8').read()
_m=re.search(r'const OFFLINE=true; let updates=(\[.*?\]), updatesSlow=false,',_s,re.S)
assert _m, 'offline updates array not found'
_new=json.dumps([{k:v for k,v in u.items() if k!='id'} for u in _snap],ensure_ascii=False).replace('</','<\\/')
_s=_s[:_m.start(1)]+_new+_s[_m.end(1):]
_top=_snap[0]['date']   # e.g. "21 Nov 2026"
from datetime import datetime as _dt
_d=_dt.strptime(_top,'%d %b %Y')
_NLM=['januari','februari','maart','april','mei','juni','juli','augustus','september','oktober','november','december']
_en='%d %s %d'%(_d.day,_d.strftime('%B'),_d.year); _nl='%d %s %d'%(_d.day,_NLM[_d.month-1],_d.year)
_a="News since the briefing, as of 12 November 2026. Newer updates are in the online version."
_b="Nieuws sinds de briefing, stand van 10 november 2026. Nieuwere updates staan in de online versie."
assert _s.count(_a)==1 and _s.count(_b)==1
_s=_s.replace(_a,"News since the briefing, as of %s (saved copy of the live updates). Newer updates are in the online version."%_en)
_s=_s.replace(_b,"Nieuws sinds de briefing, stand van %s (bewaarde kopie van de live updates). Nieuwere updates staan in de online versie."%_nl)
open(p,'w',encoding='utf-8').write(_s)
print('offpatch: updates snapshot',len(_snap),'items, newest',_top)

# tags on the Updates page in Dutch (both files)
_tg="${u.tag?` · ${esc(u.tag)}`:''}"
_tg2="${u.tag?` · ${esc(lang==='nl'?(({New:'Nieuw',Check:'Controle',Attribution:'Toeschrijving','New incidents':'Nieuwe incidenten',Correction:'Correctie'})[u.tag]||u.tag):u.tag)}`:''}"
for _p in (p, p.replace('cyber-desk-offline.html','cyber-desk.html')):
    _s=open(_p,encoding='utf-8').read()
    if _s.count(_tg)==1:
        open(_p,'w',encoding='utf-8').write(_s.replace(_tg,_tg2)); print('offpatch: update tags in Dutch',_p[-22:])
