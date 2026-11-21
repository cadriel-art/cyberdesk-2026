"""Usage: python3 snap_from_dump.py <dump_dir>/news  -> writes tools/news_snapshot.json"""
import json,glob,sys,os
out=[]
for p in glob.glob(os.path.join(sys.argv[1],'*.json')):
    d=json.load(open(p,encoding='utf-8'))
    doc=dict(d['data']) if isinstance(d.get('data'),dict) else dict(d)
    doc['id']=d.get('id') or os.path.basename(p)[:-5]; out.append(doc)
out.sort(key=lambda x:x.get('d',''),reverse=True)
json.dump(out,open(os.path.join(os.path.dirname(__file__),'news_snapshot.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('snapshot',len(out))
