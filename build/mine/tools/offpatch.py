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
