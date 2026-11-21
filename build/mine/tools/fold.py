"""Turns every 'In plain words' box in the app into a card that is collapsed by default."""
M='/home/user/cyberdesk-2026/build/mine/'
CSS='''
details.plainbox{padding:0}
details.plainbox>summary{cursor:pointer;list-style:none;display:flex;align-items:center;gap:7px;padding:10px 14px;
 font-family:var(--f-mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);font-weight:600}
details.plainbox>summary::-webkit-details-marker{display:none}
details.plainbox>summary::before{content:"\\25B8";font-size:11px;letter-spacing:0;transition:transform .15s}
details.plainbox[open]>summary::before{transform:rotate(90deg)}
details.plainbox>summary:hover{text-decoration:underline}
details.plainbox>.pb-body{padding:0 14px 12px}
details.plainbox>.pb-body>p:last-child{margin-bottom:0}
@media print{details.plainbox>.pb-body{display:block!important}}
'''
JS='''<script>
(function(){
function fold(){
  var bs=document.querySelectorAll('div.plainbox');
  for(var i=0;i<bs.length;i++){
    var b=bs[i],h=b.querySelector(':scope > .pb-h');
    if(!h)continue;
    var d=document.createElement('details');
    d.className=b.className;
    var s=document.createElement('summary');
    s.textContent=h.textContent;
    d.appendChild(s);
    var body=document.createElement('div');
    body.className='pb-body';
    h.parentNode.removeChild(h);
    while(b.firstChild)body.appendChild(b.firstChild);
    d.appendChild(body);
    if(b.id)d.id=b.id;
    b.parentNode.replaceChild(d,b);
  }
}
var opened=[],printing=false;
function bp(){if(printing)return;printing=true;opened=[];
  var ds=document.querySelectorAll('details');
  for(var i=0;i<ds.length;i++)if(!ds[i].open){ds[i].open=true;opened.push(ds[i]);}}
function ap(){if(!printing)return;printing=false;
  for(var i=0;i<opened.length;i++)opened[i].open=false;opened=[];}
window.addEventListener('beforeprint',function(){fold();bp();});
window.addEventListener('afterprint',ap);
if(window.matchMedia){try{var mq=window.matchMedia('print');var mh=function(e){if(e.matches){fold();bp();}else ap();};
  if(mq.addEventListener)mq.addEventListener('change',mh);else if(mq.addListener)mq.addListener(mh);}catch(e){}}
document.addEventListener('DOMContentLoaded',fold);
setInterval(fold,600);
fold();
})();
</script>'''
a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
if 'details.plainbox>summary' not in t:
    t=t.replace('</style>',CSS+'</style>',1)
    t=t.rstrip()+'\n'+JS+'\n'
    open(a,'w',encoding='utf-8').write(t)
print('fold ok')
# app-wide UI fixes (contrast, Dutch UI strings, skip link, headings ...): see uifix.py / uifix.css / uifix.js
import sys; sys.path.insert(0,M+'tools')
import uifix
