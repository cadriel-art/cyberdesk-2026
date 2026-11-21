import os
D='/home/user/cyberdesk-2026/build/mine/tools/'
def rd(f): return open(D+f,encoding='utf-8').read()
t=rd('uifix.js')
old="var k=pg.id.slice(2),s=split(pg),h1=$('h1',pg);"
if old in t:
    t=t.replace(old,"var k=pg.id.slice(2);if(k==='home')return;var s=split(pg),h1=$('h1',pg);")
if 'UX round 2 (R2)' not in t: t=t.rstrip()+'\n'+rd('r2.js.part')
open(D+'uifix.js','w',encoding='utf-8').write(t)
c=rd('uifix.css')
if 'UX round 2 (R2)' not in c: c=c.rstrip()+'\n'+rd('r2.css.part')
open(D+'uifix.css','w',encoding='utf-8').write(c)
print('ok')
