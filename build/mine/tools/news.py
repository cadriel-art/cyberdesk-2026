"""Adds the live page '#news' (news reader with a side section for posts on X)."""
import sys,json
M='/home/user/cyberdesk-2026/build/mine/'
SUBJ={'food':('Food and shop freezers','Voedsel en winkeldiepvriezers'),'drones':('Drones and balloons','Drones en ballonnen'),'sabotage':('Sabotage and arson','Sabotage en brandstichting'),'cables':('Sea cables and pipelines','Zeekabels en pijpleidingen'),'jamming':('Satellite-signal jamming','Storing van satellietsignalen'),'intim':('Hoax threats and intimidation','Valse dreigingen en intimidatie'),'spying':('Spying','Spionage'),'water':('Water','Water'),'energy':('Energy','Energie'),'health':('Health','Gezondheid'),'transport':('Transport and ports','Vervoer en havens'),'elections':('Elections and disinformation','Verkiezingen en desinformatie'),'defence':('Defence','Defensie'),'schools':('Schools and universities','Scholen en universiteiten'),'gov':('Government and public services','Overheid en openbare diensten'),'business':('Companies: ransomware and data leaks','Bedrijven: ransomware en datalekken'),'laws':('Laws and regulations','Wetten en regels'),'encryption':('Encryption and "chat control"','Versleuteling en "chat control"'),'ai':('Artificial intelligence','Artificiële intelligentie')}
b=M+'tools/build_app.py'; t=open(b,encoding='utf-8').read()
import re,ast
nav=ast.literal_eval(re.search(r'^NAV=(\[.*\])$',t,re.M).group(1))
PG={i['k']:i['en'] for g in nav for i in g['items']}
if "'k': 'news'" not in t:
    a="{'k': 'trend', "
    assert a in t
    t=t.replace(a,"{'k': 'news', 'en': 'News reader', 'nl': 'Nieuwslezer', 'live': 1, 'dyn': 1}, "+a,1); open(b,'w',encoding='utf-8').write(t)
import os
FP=M+'tools/news_feeds.json'
FEEDS=json.load(open(FP,encoding='utf-8')) if os.path.exists(FP) else []
SNAP=json.load(open(M+'tools/news_snapshot.json',encoding='utf-8'))
js=open(M+'tools/news.js',encoding='utf-8').read()
for k,v in (('@@SNAP@@',SNAP),('@@FEEDS@@',FEEDS),('@@SUBJ@@',SUBJ),('@@PG@@',PG)): js=js.replace(k,json.dumps(v,ensure_ascii=False).replace('</','<\\/'))
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if '.nw-grid' not in t:
    t=t.replace('</style>',open(M+'tools/news.css').read()+'</style>',1)
    t=t.rstrip()+'\n<script>\n'+js+'\n</script>\n'
    open(a,'w',encoding='utf-8').write(t)
print('news ok',len(SNAP),'feeds',len(FEEDS))
