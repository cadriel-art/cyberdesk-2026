"""Usage: python3 updates_snap_from_dump.py <dump_dir>/updates  -> writes tools/updates_snapshot.json
(the same way snap_from_dump.py makes news_snapshot.json). Newest by `order` first."""
import json,glob,sys,os
out=[]
for p in glob.glob(os.path.join(sys.argv[1],'*.json')):
    d=json.load(open(p,encoding='utf-8'))
    doc=dict(d['data']) if isinstance(d.get('data'),dict) else dict(d)
    doc['id']=d.get('id') or os.path.basename(p)[:-5]; out.append(doc)
out.sort(key=lambda x:(x.get('order',0),x.get('id','')),reverse=True)
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'updates_snapshot.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('updates snapshot',len(out))
