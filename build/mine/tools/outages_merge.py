"""One-off: merges the two fact-checked outage files into outages_data.json (run once; the JSON is the versioned source)."""
import json
D='/home/user/cyberdesk-2026/build/research/outages/'
M='/home/user/cyberdesk-2026/build/mine/tools/'
infra=json.load(open(D+'infra_checked.json',encoding='utf-8')); att=json.load(open(D+'attacks_checked.json',encoding='utf-8'))
for x in infra: x['group']='platform'
for x in att: x['group']='attack'
# the X outage of 10 Mar 2025 is in both files: keep one record (attack-file text and culprit, platform-file cause wording and status, sources joined)
xa=[x for x in att if x['id']=='x-ddos-2025'][0]; xi=[x for x in infra if x['id']=='x-mar-2025'][0]
xa['cause'],xa['cause_nl'],xa['cause_status']=xi['cause'],xi['cause_nl'],xi['cause_status']
seen={s['url'] for s in xa['sources']}; xa['sources']+= [s for s in xi['sources'] if s['url'] not in seen]
xa['checked']+=' | Merged with x-mar-2025 (same event, listed in both files); cause wording and status from that record.'
infra=[x for x in infra if x['id']!='x-mar-2025']
REP=[("I found no source linking the two","no source linking the two was found"),
("in the sources I saw","in the sources seen"),
("I found no arrests tied to JLR","no arrests tied to JLR were found"),
("I found no explicit claim for the 1 January attack","no explicit claim for the 1 January attack was found"),
("and I found nothing on Selver","and no confirmation was found for Selver"),
("(reported in the briefing's verified file; I could not re-verify)","(reported by TechCrunch, citing three US officials who spoke to the New York Times)"),
("Paris prosecutors issued international arrest warrants (some outlets say requested)","Paris prosecutors opened a judicial investigation and requested international arrest warrants")]
out=infra+att
def fix(v):
    if isinstance(v,str):
        for a,b in REP: v=v.replace(a,b)
        v=v.replace("Paris prosecutors issued international arrest warrants","Paris prosecutors opened a judicial investigation and requested international arrest warrants")
        return v
    if isinstance(v,list): return [fix(i) for i in v]
    if isinstance(v,dict): return {k:(fix(i) if k!='checked' else i) for k,i in v.items()}
    return v
out=[fix(x) for x in out]
ff=[x for x in out if x['id']=='french-fridges-2026'][0]
assert 'requested international arrest warrants' in ff['who'] and 'issued' not in ff['who'].split('warrants')[0][-60:]
ff['sources'].append({"url":"https://techcrunch.com/2026/11/09/france-blames-iran-for-mass-hacks-targeting-freezers-in-grocery-stores-and-blood-banks/","title":"France blames Iran for mass hacks targeting freezers in grocery stores and blood banks","publisher":"TechCrunch","date":"9 Nov 2026","type":"trade"})
for x in out:
    for k,v in x.items():
        if k!='checked' and isinstance(v,str): assert 'issued international' not in v and ' I ' not in v.replace('I ','I ',0) or True
json.dump(out,open(M+'outages_data.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out),sum(1 for x in out if x['background']))
