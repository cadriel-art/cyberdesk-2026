(function(){
var D=@@DATA@@;
var NS='http://www.w3.org/2000/svg';
var FAMC={},FAMN={},LAYN={},LAYF={},LAYORD=[],LYC={};
D.fam.forEach(function(f){FAMC[f[0]]=f[3];FAMN[f[0]]={en:f[1],nl:f[2]};});
D.lay.forEach(function(l){LAYN[l[0]]={en:l[1],nl:l[2]};LAYF[l[0]]=l[3];LAYORD.push(l[0]);});
var LVC={6:'#08306b',5:'#1f5fa8',4:'#3a84c4',3:'#74add1',2:'#a6cee3',1:'#cfe3f1',0:'#94a3b8',X:'#cbd5e1'};
var LVN={en:{6:'A court has ruled',5:'Charges, arrests or warrants',4:'A government has formally named them',3:'An official has said so',2:'Researchers or unnamed sources',1:"The attackers' own claim",0:'Nobody named',X:'Not an attack, or no evidence'},
         nl:{6:'Een rechtbank heeft geoordeeld',5:'Aanklacht, arrestatie of aanhoudingsbevel',4:'Een regering heeft hen formeel aangewezen',3:'Een gezagsdrager heeft het gezegd',2:'Onderzoekers of anonieme bronnen',1:'Bewering van de aanvallers zelf',0:'Niemand genoemd',X:'Geen aanval, of geen bewijs'}};
var AGRP={RU:'ru',PR:'pr',CN:'cn',IR:'st',KP:'st',BY:'st',CR:'cx',DG:'cx',EX:'cx',OT:'ot',FR:'ot'};
var ACC={ru:'#d55e00',pr:'#e8a06a',cn:'#0072b2',st:'#a4509a',cx:'#4d4d4d',ot:'#8c6d1f'};
var AGN={en:{ru:'Russia (state services)',pr:'Pro-Russian groups',cn:'China',st:'Another state (Iran, Belarus, North Korea)',cx:'Criminals or extremists',ot:'Other'},
         nl:{ru:'Rusland (staatsdiensten)',pr:'Pro-Russische groepen',cn:'China',st:'Een andere staat (Iran, Belarus, Noord-Korea)',cx:'Criminelen of extremisten',ot:'Andere'}};
var ACN={RU:'Rusland (staatsdiensten)',PR:'Pro-Russische groepen',IR:'Iran',BY:'Belarus',CN:'China',KP:'Noord-Korea',CR:'Criminele groepen',DG:'Drugsbendes',EX:'Extremisten, geen staat',OT:'Andere',FR:'Een bevriende staat',UN:'Een staat, niet genoemd',NO:'Niemand genoemd',XX:'Geen aanval'};
var PA='#f2a93b',PR='#fbe6bd',PRL='#b86e00',PN='#e9eaec',PNL='#7a828c';
var PALEO='#5f6368',PALE='#aab6c6',GREYF='#e2e8f0',GREYS='#64748b',GREYI='#334155',HALO='#fff',LANDC='#f2efe7';
var SHB=['#eef1f5','#dbe3ec','#c2cedd','#a7b7cb','#8a9db6'];
var MON={en:['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],nl:['jan','feb','mrt','apr','mei','jun','jul','aug','sep','okt','nov','dec']};
var TMAX=23;
var STORY=[
 {k:'freezer',en:'The freezer wave',nl:'De diepvriesgolf',lay:['food'],camp:'freezer'},
 {k:'drones',en:'Drone alarms',nl:'Dronealarmen',lay:['drones'],camp:'dronealarm'},
 {k:'cables',en:'Sea cables and jamming',nl:'Zeekabels en storing',lay:['cables','jamming'],camp:'cables'},
 {k:'fire',en:'Sabotage and arson',nl:'Sabotage en brandstichting',lay:['sabotage'],camp:''},
 {k:'hosp',en:'Hospitals and health',nl:'Ziekenhuizen en zorg',lay:['health'],camp:''},
 {k:'info',en:'Elections and spying',nl:'Verkiezingen en spionage',lay:['elections','spying'],camp:''},
 {k:'np',en:'Checked: not an attack',nl:'Onderzocht: geen aanval',lay:null,camp:'',st:'np'},
 {k:'court',en:'Where someone is named',nl:'Waar iemand is aangewezen',lay:null,camp:'',mode:'who'},
 {k:'prep',en:'Ready at home',nl:'Klaar thuis',lay:null,camp:''}
];
var S={on:{},mode:'lay',st:'all',camp:'',t:TMAX,tm:'cum',view:'pl',sel:null,country:null,story:'',listN:60,shade:false,prep:false,pdim:false,
       vb:{x:0,y:0,w:D.W},timer:null,cn:{},max:1};
LAYORD.forEach(function(k){S.on[k]=true;});
var root,svg,gm,gb,gl,glb,gsl,gpl,byId={};
D.ev.forEach(function(ev){byId[ev.i]=ev;});
function palette(){
  var cs=getComputedStyle(root);
  function v(n,f){var x=cs.getPropertyValue(n);x=x&&x.trim();return x||f;}
  D.fam.forEach(function(f){FAMC[f[0]]=v('--fam-'+f[0],f[3]);});
  LAYORD.forEach(function(k){LYC[k]=v('--ly-'+k,FAMC[LAYF[k]]);});
  [6,5,4,3,2,1,0,'X'].forEach(function(k){LVC[k]=v('--lv-'+String(k).toLowerCase(),LVC[k]);});
  Object.keys(ACC).forEach(function(k){ACC[k]=v('--ac-'+k,ACC[k]);});
  PALE=v('--mp-pale',PALE);PALEO=v('--mp-pale-ol',PALEO);GREYF=v('--mp-np',GREYF);GREYS=v('--mp-nps',GREYS);GREYI=v('--mp-npi',GREYI);
  PA=v('--mp-pa',PA);PR=v('--mp-pr',PR);PRL=v('--mp-prl',PRL);PN=v('--mp-pn',PN);PNL=v('--mp-pnl',PNL);
  HALO=v('--mp-halo',HALO);LANDC=v('--mp-land',LANDC);
  SHB=[1,2,3,4,5].map(function(i){return v('--sh-'+i,SHB[i-1]);});
}
function hex(c){c=(c||'').trim();if(c.charAt(0)!=='#')return null;
  if(c.length===4)c='#'+c[1]+c[1]+c[2]+c[2]+c[3]+c[3];
  if(c.length<7)return null;
  return [parseInt(c.substr(1,2),16),parseInt(c.substr(3,2),16),parseInt(c.substr(5,2),16)];}
function mix(a,b,t){return 'rgb('+Math.round(a[0]+(b[0]-a[0])*t)+','+Math.round(a[1]+(b[1]-a[1])*t)+','+Math.round(a[2]+(b[2]-a[2])*t)+')';}
function lg(){return document.documentElement.lang==='nl'?'nl':'en';}
function L(en,nl){return lg()==='nl'?nl:en;}
function CN(c){return (lg()==='nl'&&window.cdUI&&window.cdUI.ctry)?window.cdUI.ctry(c):c;}
var DM={January:'januari',February:'februari',March:'maart',April:'april',May:'mei',June:'juni',July:'juli',August:'augustus',September:'september',October:'oktober',November:'november',December:'december',Jan:'jan',Feb:'feb',Mar:'mrt',Apr:'apr',Jun:'jun',Jul:'jul',Aug:'aug',Sep:'sep',Sept:'sep',Oct:'okt',Nov:'nov',Dec:'dec'};
function DT(s){if(lg()!=='nl'||!s)return s;return String(s).replace(/\b(About|Late|Early|Mid|Spring|Summer|Autumn|Winter)\b/g,function(w){return {About:'Rond',Late:'Eind',Early:'Begin',Mid:'Half',Spring:'Lente',Summer:'Zomer',Autumn:'Herfst',Winter:'Winter'}[w];}).replace(/\b(January|February|March|April|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\b/g,function(m){return DM[m];}).replace(/\bMay\b/g,'mei');}
function cut(s,n){s=String(s||'');return s.length>n?s.slice(0,n)+'…':s;}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function el(n,a){var x=document.createElementNS(NS,n);for(var k in a)x.setAttribute(k,a[k]);return x;}
function tIdx(ev){return ev.m?(ev.y-2025)*12+ev.m-1:null;}
function layOk(ev){return ev.l.some(function(k){return S.on[k];});}
function stOk(ev){if(S.st==='conf')return ev.cf&&!ev.np;if(S.st==='unc')return !ev.cf&&!ev.np;if(S.st==='np')return !!ev.np;return true;}
function timeOk(ev){if(S.t>=TMAX)return true;var i=tIdx(ev);
  if(S.tm==='one')return i!==null&&i===S.t;
  if(i===null)return (ev.y-2025)*12+11<=S.t;
  return i<=S.t;}
function vis(ev){return layOk(ev)&&stOk(ev)&&timeOk(ev);}
function visNT(ev){return layOk(ev)&&stOk(ev);}
function famOf(ev){var k=ev.l.filter(function(k){return S.on[k];})[0]||ev.l[0];return LAYF[k];}
function iconOf(ev){return ev.l.filter(function(k){return S.on[k];})[0]||ev.l[0];}
function colour(ev){
  if(S.mode==='lv')return ev.lv===undefined?PALE:LVC[ev.lv];
  if(S.mode==='who'){var g=AGRP[ev.a];return (ev.lv!==undefined&&ev.lv!=='X'&&ev.lv>=4&&g&&ACC[g])?ACC[g]:PALE;}
  return LYC[iconOf(ev)]||FAMC[famOf(ev)];
}
function focusKey(){
  var a=document.activeElement;if(!a||!root||!root.contains(a))return null;
  var d=a.dataset||{},c=a.classList;
  if(a.id)return '#'+a.id;
  if(c.contains('mp-chip')&&d.prep!==undefined)return '.mp-chip[data-prep="1"]';
  if(c.contains('mp-chip')&&d.k!==undefined)return '.mp-chip[data-k="'+d.k+'"]';
  if(c.contains('mp-chip')&&d.all!==undefined)return '.mp-chip[data-all="'+d.all+'"]';
  if(c.contains('mp-fh'))return '.mp-fh[data-fam="'+d.fam+'"]';
  if(c.contains('mp-sbtn'))return '.mp-sbtn[data-story="'+d.story+'"]';
  if(c.contains('mp-sp'))return '.mp-sp[data-m="'+d.m+'"]';
  if(c.contains('mp-bar')&&d.l)return '.mp-bar[data-l="'+d.l+'"]';
  if(c.contains('mp-bar')&&d.c)return '.mp-bar[data-c="'+d.c+'"]';
  if(c.contains('mp-m'))return '.mp-m[data-i="'+d.i+'"]';
  if(c.contains('mp-cl'))return '.mp-cl[data-cl="'+d.cl+'"]';
  if(c.contains('mp-b'))return '.mp-b[data-c="'+d.c+'"]';
  if(c.contains('mp-li'))return '.mp-li[data-i="'+d.i+'"]';
  return null;}
function refocus(k){if(!k)return;var n;try{n=root.querySelector(k);}catch(e){return;}
  if(n&&n.focus)try{n.focus({preventScroll:true});}catch(e2){try{n.focus();}catch(e3){}}}
function markKey(m){return m.classList.contains('mp-m')?'m:'+m.dataset.i:(m.classList.contains('mp-cl')?'cl:'+m.dataset.cl:'b:'+m.dataset.c);}
function markXY(m){var r=/translate\(([-\d.]+),([-\d.]+)\)/.exec(m.getAttribute('transform')||'');return r?[+r[1],+r[2]]:[0,0];}
function marks(){var a=[].slice.call(root.querySelectorAll('#mp-mk .mp-m,#mp-mk .mp-cl,#mp-badge .mp-b'));
  a.sort(function(p,q){var A=markXY(p),B=markXY(q);return (A[0]-B[0])||(A[1]-B[1]);});return a;}
function rove(){var a=marks();if(!a.length)return;var act=null;
  a.forEach(function(m){m.setAttribute('tabindex','-1');if(S.rov&&markKey(m)===S.rov)act=m;});
  (act||a[0]).setAttribute('tabindex','0');}
function bin(v){return v>=40?4:v>=20?3:v>=10?2:v>=5?1:0;}
function camp(){for(var i=0;i<D.camp.length;i++)if(D.camp[i].k===S.camp)return D.camp[i];return null;}
function scale(){var r=svg.getBoundingClientRect(),h=S.vb.w*D.H/D.W;
  S.k=Math.max(0.6,Math.min(1,(r.width||900)/900));
  if(!r.width)return S.vb.w/1000;
  return Math.max(S.vb.w/r.width,h/Math.max(r.height,1));}
function setVB(){var v=S.vb,h=v.w*D.H/D.W;svg.setAttribute('viewBox',v.x.toFixed(1)+' '+v.y.toFixed(1)+' '+v.w.toFixed(1)+' '+h.toFixed(1));}
function clampVB(){var v=S.vb;v.w=Math.max(D.W/16,Math.min(D.W,v.w));var h=v.w*D.H/D.W;
  v.x=Math.max(-50,Math.min(D.W+50-v.w,v.x));v.y=Math.max(-50,Math.min(D.H+50-h,v.y));}
var PINP='M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7z';
function pin(ev,r,col,sc){
  var s=r/7,hy=-13*s;
  var g=el('g',{'class':'mp-m','data-i':ev.i,tabindex:'-1',role:'button','aria-label':DT(ev.d)+', '+(ev.c?CN(ev.c):L('at sea','op zee'))+(ev.p?', '+ev.p:'')+': '+cut(ev.t||ev.tx,80)});
  var np=ev.np,pale=(col===PALE);
  var fill=np?GREYF:(ev.cf?col:HALO),stroke=np?HALO:(ev.cf?HALO:col),ink=np?GREYI:(ev.cf?HALO:col);
  if(pale&&!np){fill=ev.cf?PALE:HALO;stroke=PALEO;ink=ev.cf?HALO:PALEO;}
  g.appendChild(el('circle',{cx:0,cy:hy,r:Math.max(13*s,12*sc),'class':'hit'}));
  g.appendChild(el('circle',{cx:0,cy:hy,r:r*1.75,'class':'halo'}));
  var inner=el('g',{transform:'scale('+s.toFixed(3)+') translate(-12,-22)'});
  var p=el('path',{d:PINP,fill:fill,stroke:stroke,'stroke-width':(pale&&!np?2.2:(ev.cf||np?1.5:2.2))/s});
  if(ev.pr===1)p.setAttribute('stroke-dasharray',(3/s).toFixed(2)+' '+(2/s).toFixed(2));
  inner.appendChild(p);
  g.appendChild(inner);
  var ic=D.icon[iconOf(ev)];
  if(ic){var is=0.6*s;
    var ip=el('path',{d:ic,'class':'ic',stroke:ink,transform:'translate(0,'+hy.toFixed(2)+') scale('+is.toFixed(3)+')'});
    ip.setAttribute('stroke-width',(2.0/is).toFixed(2));g.appendChild(ip);}
  if(np)g.appendChild(el('path',{d:'M'+(-r*.62)+','+(hy-r*.62)+'L'+(r*.62)+','+(hy+r*.62),stroke:HALO,'stroke-width':1.8,'vector-effect':'non-scaling-stroke',fill:'none'}));
  var t=el('title',{});
  t.textContent=DT(ev.d)+' · '+(ev.c?CN(ev.c):L('At sea','Op zee'))+(ev.p?' · '+ev.p:'')+' — '+cut(ev.t||ev.tx,100);
  g.appendChild(t);
  g.setAttribute('transform','translate('+ev._x.toFixed(1)+','+ev._y.toFixed(1)+')');
  if(S.sel===ev.i)g.classList.add('sel');
  var c2=camp();if(c2&&c2.ids.indexOf(ev.i)<0)g.classList.add('dim');
  return g;
}
var PSTAT={C:{en:'Confirmed',nl:'Bevestigd'},R:{en:'Reported via media',nl:'Gemeld via de media'},N:{en:'None found',nl:'Niets gevonden'}};
var PCOUNT=0;for(var pk in D.prep)PCOUNT++;
function prepFill(st){return st==='C'?PA:(st==='R'?'url(#mp-pat-R)':'url(#mp-pat-N)');}
function prepDefs(sc){
  var d=svg.querySelector('#mp-defs');
  if(!d){d=el('defs',{id:'mp-defs'});svg.insertBefore(d,svg.firstChild);
    function pat(id,w,tr){var p=el('pattern',{id:id,patternUnits:'userSpaceOnUse',width:w,height:w,patternTransform:tr});d.appendChild(p);return p;}
    var r=pat('mp-pat-R',8,'rotate(45)');r.appendChild(el('rect',{'class':'bg',x:0,y:0,width:8,height:8}));r.appendChild(el('rect',{'class':'ln',x:0,y:0,width:3,height:8}));
    var n=pat('mp-pat-N',8,'');n.appendChild(el('rect',{'class':'bg',x:0,y:0,width:8,height:8}));n.appendChild(el('path',{'class':'ln',d:'M0,0.5H8M0.5,0V8',fill:'none'}));
    var lr=pat('mp-lpat-R',6,'rotate(45)');lr.appendChild(el('rect',{'class':'bg',width:6,height:6}));lr.appendChild(el('rect',{'class':'ln',width:2.4,height:6}));
    var ln=pat('mp-lpat-N',6,'');ln.appendChild(el('rect',{'class':'bg',width:6,height:6}));ln.appendChild(el('path',{'class':'ln',d:'M0,0.5H6M0.5,0V6',fill:'none'}));}
  [['mp-pat-R',8,PR,PRL,3,0],['mp-pat-N',8,PN,PNL,0,1],['mp-lpat-R',6,PR,PRL,2.4,0],['mp-lpat-N',6,PN,PNL,0,1]].forEach(function(q){
    var p=d.querySelector('#'+q[0]);if(!p)return;var k=q[0].charAt(3)==='l'?1:sc,w=q[1]*(q[0].charAt(3)==='l'?1:sc);
    p.setAttribute('width',w.toFixed(2));p.setAttribute('height',w.toFixed(2));
    var bg=p.querySelector('.bg'),ln=p.querySelector('.ln');
    bg.setAttribute('width',w.toFixed(2));bg.setAttribute('height',w.toFixed(2));bg.setAttribute('fill',q[2]);
    if(q[5]){ln.setAttribute('stroke',q[3]);ln.setAttribute('stroke-width',(1.1*(k===1?1:sc)).toFixed(2));
      ln.setAttribute('d','M0,'+(0.5*(k===1?1:sc)).toFixed(2)+'H'+w.toFixed(2)+'M'+(0.5*(k===1?1:sc)).toFixed(2)+',0V'+w.toFixed(2));}
    else{ln.setAttribute('fill',q[3]);ln.setAttribute('width',(q[4]*(k===1?1:sc)).toFixed(2));ln.setAttribute('height',w.toFixed(2));}
  });
}
function envPath(x,y,w,h){return 'M'+x.toFixed(1)+','+y.toFixed(1)+'h'+w.toFixed(1)+'v'+h.toFixed(1)+'h'+(-w).toFixed(1)+'zM'+x.toFixed(1)+','+y.toFixed(1)+'l'+(w/2).toFixed(1)+','+(h*0.6).toFixed(1)+'l'+(w/2).toFixed(1)+','+(-h*0.6).toFixed(1);}
function draw(){
  if(!svg)return;
  var _fk=focusKey();
  palette();
  var sc=scale(),kk2=S.k,list=D.ev.filter(vis);S.vis=list;
  prepDefs(sc);root.classList.toggle('pdim',!!(S.prep&&S.pdim));
  var cn={},max=0;
  list.forEach(function(ev){if(ev.c){cn[ev.c]=(cn[ev.c]||0)+1;if(cn[ev.c]>max)max=cn[ev.c];}});
  S.cn=cn;S.max=max||1;
  root.querySelectorAll('.mp-cov path').forEach(function(p){
    var v=cn[p.dataset.c]||0;
    var ptl=p.querySelector('title');if(ptl)ptl.textContent=CN(p.dataset.c);
    var pp=S.prep&&D.prep[p.dataset.c];
    p.style.fill=pp?prepFill(pp.s):(S.shade?(v?SHB[bin(v)]:LANDC):LANDC);
    p.classList.toggle('sel',S.country===p.dataset.c);
  });
  function free(bx,arr){for(var q=0;q<arr.length;q++){var o=arr[q];
    if(bx[0]<o[2]&&bx[2]>o[0]&&bx[1]<o[3]&&bx[3]>o[1])return false;}return true;}
  function box(x,y,w,h){return [x-w/2,y-h/2,x+w/2,y+h/2];}
  var boxes=[],bboxes=[];
  // pins and clusters first, so the country counts and the names can keep out of their way
  gm.textContent='';
  var pins=list.filter(function(ev){return ev.pr<2&&(S.view==='pl'||!ev.c);});
  var pos={},RAD=30*sc*kk2,rh=9.2*sc*kk2,groups=[],par=[],clEls=[];
  pins.sort(function(a,b){return (a.cf?1:0)-(b.cf?1:0);});
  pins.forEach(function(ev,k){ev._x=ev.x;ev._y=ev.yy;par[k]=k;});
  function root_(k){while(par[k]!==k){par[k]=par[par[k]];k=par[k];}return k;}
  for(var gi=0;gi<pins.length;gi++)for(var gj=gi+1;gj<pins.length;gj++)
    if(Math.hypot(pins[gi].x-pins[gj].x,pins[gi].yy-pins[gj].yy)<RAD){var ra=root_(gi),rb=root_(gj);if(ra!==rb)par[rb]=ra;}
  var gmap={};pins.forEach(function(ev,k){var rk=root_(k);(gmap[rk]=gmap[rk]||[]).push(ev);});
  Object.keys(gmap).forEach(function(k){groups.push(gmap[k]);});
  groups.forEach(function(a){
    if(a.length===1){var e0=a[0];pos[e0.i]=[e0.x,e0.yy];
      boxes.push(box(e0.x,e0.yy-10*sc*kk2,20*sc*kk2,26*sc*kk2));gm.appendChild(pin(e0,9.8*sc*kk2,colour(e0),sc));return;}
    var ax=0,ay=0;a.forEach(function(e2){ax+=e2.x;ay+=e2.yy;});ax/=a.length;ay/=a.length;
    var sel=a.some(function(e2){return e2.i===S.sel;});
    var spread=(a.length<=3)||(S.vb.w<D.W/6&&a.length<=12);
    if(spread){
      var per=Math.min(a.length,4),gap=2.15*rh;
      a.forEach(function(e2,k){var row=Math.floor(k/per),col=k%per,inRow=Math.min(per,a.length-row*per);
        e2._x=ax+(col-(inRow-1)/2)*gap;e2._y=ay+row*gap*1.45;pos[e2.i]=[e2._x,e2._y];
        boxes.push(box(e2._x,e2._y-9*sc*kk2,19*sc*kk2,25*sc*kk2));
        gm.appendChild(pin(e2,9.2*sc*kk2,colour(e2),sc));});
      return;}
    a.forEach(function(e2){pos[e2.i]=[ax,ay];});
    var fams={};a.forEach(function(e2){var f=colour(e2);fams[f]=(fams[f]||0)+1;});
    var best='',bn=0;for(var f in fams)if(fams[f]>bn){bn=fams[f];best=f;}
    var r=(11+6*Math.min(1,a.length/14))*sc*kk2;
    var g=el('g',{'class':'mp-cl'+(sel?' sel':''),'data-cl':a.map(function(e2){return e2.i;}).join(','),tabindex:'-1',role:'button','aria-label':a.length+' '+L('incidents close together','incidenten vlak bij elkaar')});
    g.appendChild(el('circle',{r:r,stroke:best}));
    var tx=el('text',{y:(r*0.36).toFixed(1),'font-size':(r*1.0).toFixed(1)});tx.textContent=a.length;g.appendChild(tx);
    var ti=el('title',{});ti.textContent=a.length+' '+L('incidents close together: click to zoom in','incidenten vlak bij elkaar: klik om in te zoomen');g.appendChild(ti);
    g.setAttribute('transform','translate('+ax.toFixed(1)+','+ay.toFixed(1)+')');
    boxes.push(box(ax,ay,r*2,r*2));
    clEls.push(g);
  });
  clEls.forEach(function(g){gm.appendChild(g);});
  S.pos=pos;
  // country counts
  gb.textContent='';
  var cmp=camp(),cmpC={};
  if(cmp)cmp.ids.forEach(function(i){var e2=byId[i];if(e2&&e2.c)cmpC[e2.c]=1;});
  var bc={},leaders=[];
  list.forEach(function(ev){if(ev.c&&(S.view==='tot'||ev.pr===2))bc[ev.c]=(bc[ev.c]||0)+1;});
  var bmax=1;for(var kk in bc)if(bc[kk]>bmax)bmax=bc[kk];
  var DIRS=[[0,0],[0,.9],[0,-.9],[-.9,0],[.9,0],[-.7,.7],[.7,.7],[-.7,-.7],[.7,-.7],[0,1.8],[0,-1.8],[-1.8,0],[1.8,0],[-1.4,1.4],[1.4,1.4],[-1.4,-1.4],[1.4,-1.4]];
  function clear(bx){var m=1e9;
    for(var q=0;q<boxes.length;q++){var o=boxes[q];
      var dx=Math.max(o[0]-bx[2],bx[0]-o[2],0),dy=Math.max(o[1]-bx[3],bx[1]-o[3],0);
      var d=(dx||dy)?Math.hypot(dx,dy):-Math.min(Math.min(bx[2],o[2])-Math.max(bx[0],o[0]),Math.min(bx[3],o[3])-Math.max(bx[1],o[1]));
      if(d<m)m=d;}
    return m;}
  var CP={};root.querySelectorAll('.mp-cov path').forEach(function(p){CP[p.dataset.c]=p;});
  function inside(c,x,y){var p=CP[c];
    if(!p||!p.isPointInFill||typeof DOMPoint==='undefined')return false;
    try{return p.isPointInFill(new DOMPoint(x,y));}catch(e){return false;}}
  Object.keys(bc).sort(function(x,y){return bc[y]-bc[x];}).forEach(function(c){
    var p=D.cen[c];if(!p)return;var v=bc[c];
    var hh=((S.view==='tot'?15:11.5)+(S.view==='tot'?11:5)*Math.pow(v/bmax,0.5))*sc*kk2;
    var ww=Math.max(hh,(hh*0.62)*String(v).length+hh*0.5);
    var px=p[0],py=p[1],bx=box(px,py,ww,hh),bs=-1e9;
    for(var di=0;di<DIRS.length;di++){
      var nx=p[0]+DIRS[di][0]*(ww*0.62+6*sc),ny=p[1]+DIRS[di][1]*(hh*0.72+6*sc);
      if(di&&!inside(c,nx,ny))continue;
      var nb=box(nx,ny,ww,hh),s2=clear(nb)-di*0.04*sc;
      if(s2>bs){bs=s2;px=nx;py=ny;bx=nb;if(s2>5*sc)break;}}
    var lead=false;
    if(bs<2*sc){
      var RING=[[0,1],[1,.7],[1,0],[1,-.7],[0,-1],[-1,-.7],[-1,0],[-1,.7]],done=false;
      for(var ri=2.2;ri<=7.0&&!done;ri+=1.2)for(var qi=0;qi<RING.length;qi++){
        var qx=p[0]+RING[qi][0]*ri*(ww*0.6+7*sc),qy=p[1]+RING[qi][1]*ri*(hh*0.9+7*sc),qb=box(qx,qy,ww,hh);
        if(clear(qb)>2.5*sc){px=qx;py=qy;bx=qb;lead=true;done=true;break;}}}
    if(lead)leaders.push([p[0],p[1],px,py]);
    var g=el('g',{'class':'mp-b','data-c':c,tabindex:'-1',role:'button','aria-label':CN(c)+': '+v});
    if(lead){var ln=el('line',{'class':'lead',x1:(p[0]-px).toFixed(1),y1:(p[1]-py).toFixed(1),x2:0,y2:0});g.appendChild(ln);
      g.appendChild(el('circle',{'class':'leaddot',cx:(p[0]-px).toFixed(1),cy:(p[1]-py).toFixed(1),r:(2.2*sc).toFixed(1)}));}
    g.appendChild(el('rect',{x:(-ww/2).toFixed(1),y:(-hh/2).toFixed(1),width:ww.toFixed(1),height:hh.toFixed(1),rx:(hh*0.26).toFixed(1)}));
    var t2=el('text',{y:(hh*0.33).toFixed(1),'font-size':(hh*0.78).toFixed(1)});t2.textContent=v;g.appendChild(t2);
    var ti2=el('title',{});ti2.textContent=CN(c)+': '+v+' '+(S.view==='tot'?L('incidents','incidenten'):L('incidents where only the country is known','incidenten waarvan alleen het land bekend is'));g.appendChild(ti2);
    g.setAttribute('transform','translate('+px.toFixed(1)+','+py.toFixed(1)+')');
    if(S.country===c)g.classList.add('sel');
    if(cmp&&!cmpC[c])g.classList.add('dim');
    gb.appendChild(g);
    bc[c]={v:v,r:hh/2,w:ww,h:hh,x:px,y:py};
    boxes.push(bx);bboxes.push(bx);
  });
  list.forEach(function(ev){if(ev.pr===2&&ev.c&&bc[ev.c])pos[ev.i]=[bc[ev.c].x,bc[ev.c].y];});
  // labels
  glb.textContent='';
  var fs=Math.max(11*sc*Math.max(0.78,kk2),9*sc),zoomed=S.vb.w<D.W*0.46;
  var lb=boxes.slice(),lbl=[];
  function crossed(bx){for(var q=0;q<leaders.length;q++){var l=leaders[q],n=Math.max(2,Math.ceil(Math.hypot(l[2]-l[0],l[3]-l[1])/(2*sc)));
      for(var j=0;j<=n;j++){var px2=l[0]+(l[2]-l[0])*j/n,py2=l[1]+(l[3]-l[1])*j/n;
        if(px2>bx[0]-1&&px2<bx[2]+1&&py2>bx[1]-1&&py2<bx[3]+1)return true;}}return false;}
  function put(name,x,y,size,cls,cc,rx){
    name=CN(name);
    var w=name.length*size*0.53,h=size*1.05,bx=[x-w/2,y-h*0.85,x+w/2,y+h*0.25];
    if(!(rx?free(bx,bboxes.concat(lbl)):free(bx,lb))||crossed(bx))return false;
    if(cc&&!inside(cc,x,y))return false;
    lb.push(bx);lbl.push(bx);
    var t=el('text',{x:x.toFixed(1),y:y.toFixed(1),'font-size':size.toFixed(1)});
    if(cls)t.setAttribute('class',cls);
    t.textContent=name;glb.appendChild(t);return true;}
  if(!S.cbw){S.cbw={};root.querySelectorAll('.mp-cov path').forEach(function(p){try{S.cbw[p.dataset.c]=p.getBBox().width;}catch(e){}});}
  var narrow=kk2<0.8;
  Object.keys(D.cen).sort(function(a,b){return (cn[b]||0)-(cn[a]||0);}).forEach(function(c){
    var b=bc[c],half=CN(c).length*fs*0.27,done=false,lw=CN(c).length*fs*0.53;
    if(S.cbw[c]!==undefined&&lw>S.cbw[c]*(narrow?1.0:1.6)&&(narrow||!b))return;
    var anchors=b?[[D.cen[c][0],D.cen[c][1],0,0],[b.x,b.y,b.w/2,b.h/2]]:[[D.cen[c][0],D.cen[c][1],0,0]];
    var big=S.cbw[c]!==undefined&&S.cbw[c]>=3*lw;
    for(var pass=0;pass<2&&!done;pass++){if(pass===1&&!big)break;
    for(var ai=0;ai<anchors.length&&!done;ai++){
      var p=anchors[ai],hw=p[2],hh2=p[3];
      var cands=[[0,hh2+fs*1.0],[0,-hh2-fs*0.3],[hw+fs*0.5+half,fs*0.35],[-hw-fs*0.5-half,fs*0.35],
                 [hw+fs*0.4+half,hh2+fs*1.1],[-hw-fs*0.4-half,hh2+fs*1.1],[0,hh2+fs*2.2],[0,-hh2-fs*1.5],
                 [hw+fs*0.4+half,-hh2-fs*0.6],[-hw-fs*0.4-half,-hh2-fs*0.6],[0,hh2+fs*3.4],[half+fs*1.6,hh2+fs*2.3]];
      for(var ci=0;ci<cands.length;ci++)
        if(put(c,p[0]+cands[ci][0],p[1]+cands[ci][1],fs,cn[c]?'':'q',c,pass===1)){done=true;break;}}}
    if(!done&&b&&!narrow){var hw2=b.w/2,hh3=b.h/2,hf=CN(c).length*fs*0.27;
      put(c,b.x,b.y+hh3+fs*1.0,fs,cn[c]?'':'q')||put(c,b.x,b.y-hh3-fs*0.3,fs,cn[c]?'':'q')||
      put(c,b.x+hw2+fs*0.5+hf,b.y+fs*0.35,fs,cn[c]?'':'q')||put(c,b.x-hw2-fs*0.5-hf,b.y+fs*0.35,fs,cn[c]?'':'q');}
  });
  if(zoomed){var seen={};
    pins.forEach(function(ev){if(!ev.p||seen[ev.p])return;seen[ev.p]=1;
      var pp=pos[ev.i];if(!pp)return;
      var nm=cut(ev.p,24),cz=Math.max(9.5*sc*kk2,9*sc),by=pp[1]+3*sc*kk2+cz*0.95,ay=pp[1]-23*sc*kk2-cz*0.3;
      put(nm,pp[0],by,cz,'city')||put(nm,pp[0],ay,cz,'city');});}
  gpl.textContent='';S.plN=0;
  if(S.prep){
    var pf=Math.max(9.5*sc*Math.max(0.8,kk2),8.5*sc),ph=pf*1.5;
    Object.keys(D.prep).sort(function(a,b){return (S.cbw&&S.cbw[b]||0)-(S.cbw&&S.cbw[a]||0);}).forEach(function(c){
      var pr=D.prep[c],cp=D.cen[c];if(!cp)return;
      var tw=pr.d.length*pf*0.58,ew=pr.m?pf*1.0:0,gap=pr.m?pf*0.3:0,w=tw+ew+gap+pf*0.9;
      var OFF=[[0,0],[0,.9],[0,-.9],[-.55,0],[.55,0],[-.5,.9],[.5,.9],[-.5,-.9],[.5,-.9],[0,1.8],[0,-1.8],[-.9,.9],[.9,.9],[-.9,-.9],[.9,-.9],[0,2.7],[0,-2.7]];
      for(var oi=0;oi<OFF.length;oi++){
        var x=cp[0]+OFF[oi][0]*w,y=cp[1]+OFF[oi][1]*ph,bx=box(x,y,w,ph);
        if(!inside(c,x,y)||!inside(c,x-w*0.4,y)||!inside(c,x+w*0.4,y))continue;
        if(!free(bx,lb)||crossed(bx))continue;
        lb.push(bx);S.plN++;
        var g=el('g',{'class':'mp-pl'+(S.country===c?' sel':''),'data-c':c,role:'img','aria-label':CN(c)+': '+PSTAT[pr.s][lg()]+(pr.s==='N'?'':', '+pr.d)+(pr.m?', '+L('mailed to every household','naar elk huishouden gestuurd'):'')});
        g.setAttribute('transform','translate('+x.toFixed(1)+','+y.toFixed(1)+')');
        g.appendChild(el('rect',{x:(-w/2).toFixed(1),y:(-ph/2).toFixed(1),width:w.toFixed(1),height:ph.toFixed(1),rx:(ph*0.4).toFixed(1)}));
        var off=pr.m?-(ew+gap)/2:0;
        var t3=el('text',{x:off.toFixed(1),y:(pf*0.36).toFixed(1),'font-size':pf.toFixed(1)});t3.textContent=pr.d;g.appendChild(t3);
        if(pr.m)g.appendChild(el('path',{d:envPath(off+tw/2+gap,-pf*0.36,ew,pf*0.72)}));
        var t4=el('title',{});t4.textContent=CN(c)+': '+PSTAT[pr.s][lg()]+(pr.s==='N'?'':' · '+pr.d)+(pr.m?' · '+L('mailed to every household','naar elk huishouden gestuurd'):'');g.appendChild(t4);
        gpl.appendChild(g);break;}
    });}
  gsl.textContent='';
  D.sea.forEach(function(s){
    var nm=lg()==='nl'?s[3]:s[2],fsz=Math.max(11.5*sc,9*sc),w=nm.length*fsz*0.5,bx=[s[0]-w/2,s[1]-fsz*0.8,s[0]+w/2,s[1]+fsz*0.3];
    if(!free(bx,lb)||crossed(bx))return;
    lb.push(bx);
    var t=el('text',{x:s[0],y:s[1],'font-size':fsz.toFixed(1)});t.textContent=nm;gsl.appendChild(t);});
  // wave lines
  gl.textContent='';
  var c3=camp();
  S.campGhost=null;
  if(c3){var mem=c3.ids.map(function(i){return byId[i];}).filter(Boolean).sort(function(a,b){return (a.y-b.y)||((a.m||0)-(b.m||0))||(a.i-b.i);});
    var first=mem[0],o=pos[first.i];
    if(!o){o=(first.pr===2&&first.c)?(bc[first.c]&&bc[first.c].x!==undefined?[bc[first.c].x,bc[first.c].y]:D.cen[first.c]):[first.x,first.yy];
      S.campGhost=first.d;
      gl.appendChild(el('circle',{cx:o[0].toFixed(1),cy:o[1].toFixed(1),r:(9*sc).toFixed(1),'class':'ghost'}));}
    var rest=mem.slice(1).filter(function(ev){return pos[ev.i];}).map(function(ev){return pos[ev.i];});
    if(rest.length)gl.appendChild(el('path',{d:rest.map(function(p){return 'M'+o[0].toFixed(1)+','+o[1].toFixed(1)+'L'+p[0].toFixed(1)+','+p[1].toFixed(1);}).join('')}));}
  root.querySelector('#mp-count').textContent=list.length+' '+L('of','van')+' '+D.ev.length+' '+L('incidents shown','incidenten getoond')+' · '+Object.keys(cn).length+' '+L('countries','landen');
  chips();panel();listing();printnote();campnote();
  rove();refocus(_fk);
}
function printnote(){
  var pn=root.querySelector('#mp-printnote');if(!pn)return;
  var on=LAYORD.filter(function(k){return S.on[k];}).map(function(k){return LAYN[k][lg()];});
  var c=camp();
  pn.textContent=L('Map settings: ','Kaartinstellingen: ')+(S.vis?S.vis.length:0)+' '+L('incidents','incidenten')+' · '+root.querySelector('#mp-tl').textContent+' · '+
    L('layers: ','lagen: ')+(on.length===LAYORD.length?L('all','alle'):on.join(', '))+' · '+root.querySelector('#mp-st').selectedOptions[0].textContent+' · '+
    L('colour: ','kleur: ')+root.querySelector('#mp-mode').selectedOptions[0].textContent+
    ' · '+L('view: ','weergave: ')+root.querySelector('#mp-view [aria-pressed="true"]').textContent+
    (S.shade&&!S.prep?' · '+L('countries shaded by how much is shown','landen gekleurd naar hoeveel getoond wordt'):'')+
    (S.prep?' · '+L('layer Ready at home is on: countries coloured by stock-up advice (official advice, advice via media only, none found), with the time to be ready; these are not incidents and are not counted above','laag Klaar thuis staat aan: landen gekleurd naar advies over een noodvoorraad (officieel advies, alleen via media, niets gevonden), met de tijd om klaar te zijn; dit zijn geen incidenten en ze zijn hierboven niet meegeteld'):'')+(c?' · '+c[lg()]:'');
}
function icoSvg(k,col,size){
  return '<svg width="'+size+'" height="'+size+'" viewBox="-11 -11 22 22" aria-hidden="true"><path d="'+D.icon[k]+'" fill="none" stroke="'+col+'" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/></svg>';
}
function chips(){
  palette();
  var box=root.querySelector('#mp-lay'),cnt={};
  var save=S.on;S.on={};LAYORD.forEach(function(k){S.on[k]=true;});
  D.ev.forEach(function(ev){if(vis(ev))ev.l.forEach(function(k){cnt[k]=(cnt[k]||0)+1;});});
  S.on=save;
  var h='<div class="mp-fg"><button type="button" class="mp-chip mp-ctl" data-all="1">'+L('All','Alles')+'</button><button type="button" class="mp-chip mp-ctl" data-all="0">'+L('None','Geen')+'</button></div>';
  D.fam.forEach(function(f){
    var ks=LAYORD.filter(function(k){return LAYF[k]===f[0];}),fc=FAMC[f[0]]||f[3];
    function lyc(k){return LYC[k]||fc;}
    h+='<div class="mp-fg" style="--c:'+fc+'"><button type="button" class="mp-fh" data-fam="'+f[0]+'" title="'+L('Show only this group; click again for all','Toon alleen deze groep; klik opnieuw voor alles')+'"><i></i>'+esc(FAMN[f[0]][lg()])+'</button>';
    ks.forEach(function(k){h+='<button type="button" class="mp-chip" style="--c:'+lyc(k)+'" data-k="'+k+'" aria-pressed="'+(S.on[k]?'true':'false')+'">'+icoSvg(k,'currentColor',13)+esc(LAYN[k][lg()])+' <small>'+(cnt[k]||0)+'</small></button>';});
    h+='</div>';
  });
  var hp='<div class="mp-fg mp-fg-prep"><span class="mp-fhx"><i></i>'+L('Ready at home','Klaar thuis')+'</span><button type="button" class="mp-chip mp-prep" data-prep="1" aria-pressed="'+(S.prep?'true':'false')+'" title="'+L('A map layer, not a type of attack: colours the countries by what the government advises people to keep at home. Not counted in the incidents.','Een kaartlaag, geen soort aanval: kleurt de landen naar wat de overheid adviseert om thuis te hebben. Niet meegeteld bij de incidenten.')+'"><svg width="15" height="13" viewBox="-1 -1 18 14" aria-hidden="true"><path d="M0,0h16v12h-16zM0,0l8,7l8,-7" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>'+L('Stock-up advice by country','Advies noodvoorraad per land')+'</button></div>';
  box.innerHTML=h;
  var bp=root.querySelector('#mp-layprep');if(bp)bp.innerHTML=hp;else box.insertAdjacentHTML('beforeend',hp);
  var n2=LAYORD.filter(function(k){return S.on[k];}).length,lc2=root.querySelector('#mp-laycount');
  if(lc2)lc2.textContent='('+n2+'/'+LAYORD.length+')';
}
function tlabel(){
  var b=root.querySelector('#mp-tl'),sl=root.querySelector('#mp-t');
  if(S.t>=TMAX){b.textContent=S.tm==='one'?L('All months (no month chosen)','Alle maanden (geen maand gekozen)')
    :L('Whole period: Jan 2025 – Nov 2026','Hele periode: jan 2025 – nov 2026');
    if(sl)sl.setAttribute('aria-valuetext',b.textContent);return;}
  var y=2025+Math.floor(S.t/12),m=S.t%12;
  b.textContent=(S.tm==='cum'?L('Up to ','T/m '):'')+MON[lg()][m]+' '+y;
  if(sl)sl.setAttribute('aria-valuetext',b.textContent);
}
function legend(){
  palette();
  var h='',ink='currentColor';
  function sw(inner){return '<svg width="17" height="17" viewBox="-9 -9 18 18" aria-hidden="true">'+inner+'</svg>';}
  var ex=S.mode==='lay'?LYC.drones||FAMC.hyb:(S.mode==='lv'?LVC[5]:ACC.ru);
  function pinsw(fill,stroke,dash){return '<svg width="15" height="19" viewBox="0 0 24 26" aria-hidden="true"><path d="'+PINP+'" fill="'+fill+'" stroke="'+stroke+'" stroke-width="1.8"'+(dash?' stroke-dasharray="3 2"':'')+'/></svg>';}
  h+='<span>'+pinsw(ex,HALO)+L('Confirmed: solid evidence it happened','Bevestigd: stevig bewijs dat het gebeurde')+'</span>';
  h+='<span>'+pinsw(HALO,ex)+L('Reported, claimed or suspected','Gemeld, geclaimd of vermoed')+'</span>';
  h+='<span>'+pinsw(GREYF,HALO)+L('Checked: not an attack, or not proven','Onderzocht: geen aanval, of niet bewezen')+'</span>';
  h+='<span>'+pinsw(HALO,ex,1)+L('Place is approximate, such as a stretch of sea','Plaats bij benadering, zoals een stuk zee')+'</span>';
  h+='<span>'+sw('<rect x="-8" y="-5.5" width="16" height="11" rx="3" fill="var(--paper)" stroke="'+ink+'" stroke-width="1.4"/><text y="3.4" font-size="8.5" text-anchor="middle" fill="'+ink+'" font-weight="700">7</text>')+(S.view==='tot'?L('all entries of this country','alle meldingen van dit land'):L('only the country is known','alleen het land is bekend'))+'</span>';
  h+='<span>'+sw('<circle r="7" fill="var(--paper)" stroke="'+ex+'" stroke-width="2"/><text y="3.2" font-size="9" text-anchor="middle" fill="var(--ink)" font-weight="700">4</text>')+L('several close together: click to zoom in','meerdere vlak bij elkaar: klik om in te zoomen')+'</span>';
  if(S.camp)h+='<span>'+sw('<path d="M-8,4L8,-4" stroke="'+ink+'" stroke-width="1.6" stroke-dasharray="4 3"/>')+L('same series, not necessarily the same culprit','zelfde reeks, niet noodzakelijk dezelfde dader')+'</span>'
    +'<span style="opacity:.3">'+sw('<circle r="6" fill="'+ex+'"/>')+L('not part of this series','niet in deze reeks')+'</span>';
  if(S.shade&&!S.prep){h+='<span><span class="mp-steps">'+SHB.map(function(c){return '<i style="background:'+c+'"></i>';}).join('')+'</span> '+L('1-4, 5-9, 10-19, 20-39, 40+ entries shown','1-4, 5-9, 10-19, 20-39, 40+ getoond')+'</span>';}
  if(S.mode==='lay')h+='<span>'+L('Every type of attack has its own colour and picture: see the buttons above the map.','Elk soort aanval heeft een eigen kleur en pictogram: zie de knoppen boven de kaart.')+'</span>';
  if(S.mode==='lv'){h+='<span><b>'+L('Proof level, strongest first','Bewijsniveau, sterkste eerst')+':</b></span>';
    [6,5,4,3,2,1,0,'X'].forEach(function(k){h+='<span><i style="background:'+LVC[k]+'"></i>'+(k==='X'?'✕':L('Level ','Niveau ')+k)+' '+esc(LVN[lg()][k])+'</span>';});
    h+='<span><i style="background:'+PALE+'"></i>'+L('not in the evidence tracker','niet in de bewijstracker')+'</span>';}
  if(S.mode==='who'){var seen={};
    D.ev.forEach(function(ev){var g=AGRP[ev.a];if(ev.lv!==undefined&&ev.lv!=='X'&&ev.lv>=4&&g)seen[g]=1;});
    Object.keys(seen).forEach(function(k){h+='<span><i style="background:'+ACC[k]+'"></i>'+esc(AGN[lg()][k])+'</span>';});
    h+='<span><i style="background:'+PALE+'"></i>'+L('nobody formally named','niemand formeel aangewezen')+'</span>';}
  if(S.prep){
    function lsw(f){return '<svg width="24" height="15" viewBox="0 0 24 15" aria-hidden="true"><rect x="0.7" y="0.7" width="22.6" height="13.6" rx="2" fill="'+f+'" stroke="var(--mp-coast)" stroke-width="1.2"/></svg>';}
    h+='<div class="mp-lg-prep"><b>'+L('Ready at home: stock-up advice per country (a layer, not incidents)','Klaar thuis: advies noodvoorraad per land (een laag, geen incidenten)')+'</b>'+
      '<span>'+lsw(PA)+L('Official advice from the government','Officieel advies van de overheid')+'</span>'+
      '<span>'+lsw('url(#mp-lpat-R)')+L('Advice known only through the media (diagonal stripes)','Advies alleen bekend via de media (diagonale strepen)')+'</span>'+
      '<span>'+lsw('url(#mp-lpat-N)')+L('None found (grey, grid pattern)','Niets gevonden (grijs, ruitpatroon)')+'</span>'+
      '<span><svg width="48" height="16" viewBox="0 0 48 16" aria-hidden="true"><rect x="0.7" y="1" width="46.6" height="14" rx="5" fill="var(--paper)" stroke="'+PRL+'" stroke-width="1.2"/><text x="14" y="11.4" font-size="8.5" font-weight="700" fill="var(--ink)" text-anchor="middle">72 h</text><path d="M28,5h11v7h-11zM28,5l5.5,4.4l5.5,-4.4" fill="none" stroke="var(--ink)" stroke-width="1"/></svg>'+L('how long the advice says to be ready ("—": no figure); an envelope means a printed guide was mailed to every household','hoe lang het advies zegt klaar te zijn ("—": geen aantal); een envelop betekent dat een gedrukte gids naar elk huishouden is gestuurd')+'</span>'+
      '<span>'+L('EU: the European Commission\'s non-binding guidelines of 30 October 2026 ask member states to help households cope for at least 72 hours.','EU: de niet-bindende richtlijnen van de Europese Commissie van 30 oktober 2026 vragen de lidstaten huishoudens te helpen minstens 72 uur zelfstandig te blijven.')+'</span>'+
      (S.shade?'<span>'+L('The stock-up layer is on, so it replaces the shading by number of incidents.','De laag noodvoorraad staat aan en vervangt dus de kleuring naar aantal incidenten.')+'</span>':'')+
      '<label><span class="small">'+L('Open the advice of a country: ','Open het advies van een land: ')+'</span><select id="mp-prepsel" aria-label="'+L('Choose a country to see its stock-up advice','Kies een land om het advies over een noodvoorraad te zien')+'"><option value="">'+L('Choose a country','Kies een land')+'</option>'+
      Object.keys(D.prep).sort().map(function(c){return '<option value="'+esc(c)+'">'+esc(CN(c))+'</option>';}).join('')+'</select></label></div>';}
  h+='<div class="mp-printkey"><b>'+L('Pictures used on the pins','Pictogrammen op de spelden')+'</b>'+
    LAYORD.map(function(k){return '<span>'+icoSvg(k,'#000',14)+esc(LAYN[k][lg()])+'</span>';}).join('')+'</div>';
  root.querySelector('#mp-legend').innerHTML=h;
}
function stText(ev){
  var o=[],s=ev.s;
  if(s.indexOf('C')>=0)o.push(L('Confirmed','Bevestigd'));
  if(s.indexOf('R')>=0)o.push(L('Reported','Gemeld'));
  if(s.indexOf('K')>=0)o.push(L('Claimed','Geclaimd'));
  if(s.indexOf('S')>=0)o.push(L('Suspected','Vermoed'));
  if(ev.np)o.push(L('Not an attack, or not proven','Geen aanval, of niet bewezen'));
  return o;
}
function card(){
  if(S.sel!==null&&byId[S.sel]&&!vis(byId[S.sel]))S.sel=null;
  var box={innerHTML:'',style:{}};var H='',BC='';
  if(S.sel!==null&&byId[S.sel]){
    var ev=byId[S.sel],where=(ev.c?CN(ev.c):L('At sea','Op zee'))+(ev.p?' · '+ev.p:'');
    var prec=ev.pr===0?L('place named by a source','plaats genoemd door een bron'):ev.pr===1?L('approximate area','gebied bij benadering'):L('only the country is known','alleen het land is bekend');
    var ttl=ev.t||ev.ct||(ev.tx.length>110?ev.tx.slice(0,110)+'…':ev.tx);
    var h='<button type="button" class="mp-x" aria-label="'+L('Close','Sluiten')+'">×</button><h4>'+esc(ttl)+'</h4>'+
      '<p class="mp-meta">'+esc(DT(ev.d))+' · '+esc(where)+' ('+prec+')</p><div class="mp-tags">';
    ev.l.forEach(function(k){h+='<span class="mp-pill c" style="--c:'+(LYC[k]||FAMC[LAYF[k]])+'">'+esc(LAYN[k][lg()])+'</span>';});
    stText(ev).forEach(function(s){h+='<span class="mp-pill">'+esc(s)+'</span>';});
    h+='</div>';
    if(ttl!==ev.tx)h+='<p>'+esc(ev.tx)+'</p>';
    if(ev.f.length){h+='<div class="mp-later"><b>'+L('What happened later','Wat er later gebeurde')+'</b>';
      ev.f.forEach(function(f){h+='<p><b>'+esc(f[0])+':</b> '+esc(f[1])+'</p>';});h+='</div>';}
    if(ev.lv!==undefined){h+='<div class="mp-later"><b>'+L('Who is named, and how strong the evidence is','Wie wordt genoemd, en hoe sterk het bewijs is')+'</b><p><span class="mp-pill c" style="--c:'+LVC[ev.lv]+'">'+
      (ev.lv==='X'?'✕':L('Level ','Niveau ')+ev.lv)+' '+esc(LVN[lg()][ev.lv])+'</span> '+esc(ev.w)+(ev.by&&ev.by!=='—'?'<br><span class="small">'+L('Source of that: ','Bron daarvan: ')+esc(ev.by)+'</span>':'')+
      '</p><p class="small"><a href="#evidence">'+L('Full case in the evidence tracker','Volledige zaak in de bewijstracker')+'</a></p></div>';}
    h+='<p class="small mp-src"><a href="#'+ev.g+'">'+L('Source page: ','Bronpagina: ')+esc(D.pg[ev.g]||ev.g)+'</a></p>';
    H=h;BC=colour(ev);putcard(H,BC);return;
  }
  if(S.country&&S.prep&&D.prep[S.country]){
    var pc=D.prep[S.country],cc=S.country,pcol=pc.s==='C'?PA:(pc.s==='R'?PRL:PNL);
    var nAll=D.ev.filter(function(ev){return ev.c===cc;}).length;
    var h4='<button type="button" class="mp-x" aria-label="'+L('Close','Sluiten')+'">×</button><h4>'+esc(CN(cc))+': '+L('stock-up advice','advies noodvoorraad')+'</h4>'+
      '<div class="mp-tags"><span class="mp-pill" style="background:'+pcol+';color:'+(pc.s==='N'?'#fff':'#1b1303')+';border-color:'+pcol+'">'+esc(PSTAT[pc.s][lg()])+'</span></div>'+
      '<dl class="mp-dl"><dt>'+L('How long','Hoe lang')+'</dt><dd>'+esc(pc.h)+'</dd><dt>'+L('Water','Water')+'</dt><dd>'+esc(pc.w)+'</dd>'+
      '<dt>'+L('Mailed to every household','Naar elk huishouden gestuurd')+'</dt><dd>'+(pc.m?L('Yes','Ja'):L('No','Nee'))+'</dd><dt>'+L('Latest update','Laatste update')+'</dt><dd>'+esc(pc.la)+'</dd></dl>'+
      '<p>'+esc(pc.en)+'</p><p class="mp-nl"><b>NL:</b> '+esc(pc.nl)+'</p>'+
      '<p class="small">'+L('Guide: ','Gids: ')+(pc.u?'<a href="'+esc(pc.u)+'" target="_blank" rel="noopener">'+esc(cut(pc.g,110))+'</a>':esc(cut(pc.g,110)))+'</p>'+
      '<p class="small"><a href="#prepare">'+L('Full details on the page Ready at home','Alle details op de pagina Klaar thuis')+'</a></p>'+
      '<p class="mp-hint">'+L('This layer is not an incident. Incidents in this file for '+cc+': ','Deze laag is geen incident. Incidenten in dit dossier voor '+CN(cc)+': ')+nAll+'.</p>';
    putcard(h4,pcol);return;
  }
  if(S.country){
    var c=S.country,all=D.ev.filter(function(ev){return ev.c===c;}),v=all.filter(vis),by={},conf=0,np=0;
    v.forEach(function(ev){by[ev.l[0]]=(by[ev.l[0]]||0)+1;if(ev.cf&&!ev.np)conf++;if(ev.np)np++;});
    var h2='<button type="button" class="mp-x" aria-label="'+L('Close','Sluiten')+'">×</button><h4>'+esc(CN(c))+'</h4>'+
      '<p class="mp-meta">'+v.length+' '+L('shown with the current settings','getoond met de huidige instellingen')+' ('+all.length+' '+L('in total','in totaal')+') · '+
      conf+' '+L('confirmed','bevestigd')+' · '+np+' '+L('not an attack or not proven','geen aanval of niet bewezen')+'</p><div class="mp-tags">';
    Object.keys(by).sort(function(a,b){return by[b]-by[a];}).forEach(function(k){
      h2+='<span class="mp-pill c" style="--c:'+(LYC[k]||FAMC[LAYF[k]])+'">'+esc(LAYN[k][lg()])+' '+by[k]+'</span>';});
    h2+='</div><p class="small">'+L('A high number mostly means a country reports openly. ','Een hoog cijfer betekent vooral dat een land open rapporteert. ')+
      '<a href="#eucountries">'+L('Country pages','Landenpagina\'s')+'</a></p>';
    H=h2;putcard(H,'');return;
  }
  putcard('','');
}
function liveRegions(){
  var small=window.matchMedia?matchMedia('(max-width:699px)').matches:window.innerWidth<700;
  var useDrawer=small||root.classList.contains('tall')||!!(document.fullscreenElement||document.webkitFullscreenElement);
  var dr=root.querySelector('#mp-drawer'),cd=root.querySelector('#mp-card');
  [[dr,useDrawer],[cd,!useDrawer]].forEach(function(p){if(!p[0])return;
    if(p[1]){p[0].setAttribute('role','status');p[0].setAttribute('aria-live','polite');}
    else{p[0].removeAttribute('role');p[0].setAttribute('aria-live','off');}});
}
function putcard(h,col){
  liveRegions();
  ['#mp-card','#mp-drawer'].forEach(function(s){var b=root.querySelector(s);if(!b)return;b.innerHTML=h;b.style.borderLeftColor=col||'';});
}
function campnote(){
  var c=camp(),b=root.querySelector('#mp-campnote');
  b.innerHTML=c?'<b>'+esc(c[lg()])+'.</b> '+esc(lg()==='nl'?c.nnl:c.nen)+
    (S.campGhost?' <span class="small"><b>'+L('The first entry of this series (','Het eerste item van deze reeks (')+esc(S.campGhost)+L(') falls outside the time shown; the lines still start from it, at the dashed circle.',') valt buiten de getoonde tijd; de lijnen vertrekken er toch van, bij de gestippelde cirkel.')+'</b></span>':'')+
    ' <span class="small">('+c.ids.length+' '+
    L('incidents; the lines start at the first incident and mean "same wave", not "same culprit")','incidenten; de lijnen vertrekken bij het eerste incident en betekenen "zelfde golf", niet "zelfde dader")')+'</span>':'';
}
function panel(){
  var ntc=D.ev.filter(visNT),mc=[],i;
  for(i=0;i<23;i++)mc.push(0);
  ntc.forEach(function(ev){var t=tIdx(ev);if(t!==null&&t<23)mc[t]++;});
  var mx=Math.max.apply(null,mc)||1,h='';
  for(i=0;i<23;i++){var y=2025+Math.floor(i/12),m=i%12;
    var on=(S.t===i);
    h+='<button type="button" class="mp-sp'+(on?' on':'')+(y===2026?' y2':'')+'" data-m="'+i+'" aria-pressed="'+on+'" aria-label="'+MON[lg()][m]+' '+y+': '+mc[i]+'" title="'+MON[lg()][m]+' '+y+': '+mc[i]+'"><i style="height:'+Math.max(1,Math.round(mc[i]/mx*54))+'px"></i></button>';}
  root.querySelector('#mp-spark').innerHTML=h;
  var ye=root.querySelector('#mp-years');
  if(ye)ye.innerHTML='<span>'+L('Jan 2025','jan 2025')+'</span><span>'+L('Jan 2026','jan 2026')+'</span><span>'+L('Nov 2026','nov 2026')+'</span>';
  var cn=S.cn,ks=Object.keys(cn).sort(function(a,b){return cn[b]-cn[a];}),lim=S.allC?ks.length:8,h2='';
  ks.slice(0,lim).forEach(function(c){
    h2+='<button type="button" class="mp-bar'+(S.country===c?' on':'')+'" aria-pressed="'+(S.country===c)+'" data-c="'+esc(c)+'"><span><span class="t">'+esc(CN(c))+'</span><span class="g" style="width:'+Math.round(cn[c]/S.max*100)+'%"></span></span><em>'+cn[c]+'</em></button>';});
  if(ks.length>8)h2+='<button type="button" class="mp-more2" id="mp-allc">'+(S.allC?L('Show fewer','Toon minder'):L('Show all','Toon alle')+' ('+ks.length+')')+'</button>';
  if(!ks.length)h2='<p class="mp-hint">'+L('Nothing shown with these settings.','Niets getoond met deze instellingen.')+'</p>';
  root.querySelector('#mp-cbars').innerHTML=h2;
  var lc={},lmax=1;
  (S.vis||[]).forEach(function(ev){ev.l.forEach(function(k){if(S.on[k]){lc[k]=(lc[k]||0)+1;if(lc[k]>lmax)lmax=lc[k];}});});
  var h3='',solo=LAYORD.filter(function(k){return S.on[k];});
  LAYORD.filter(function(k){return lc[k];}).sort(function(a,b){return lc[b]-lc[a];}).forEach(function(k){
    h3+='<button type="button" class="mp-bar'+(solo.length===1&&solo[0]===k?' on':'')+'" aria-pressed="'+(solo.length===1&&solo[0]===k)+'" data-l="'+k+'" style="--c:'+FAMC[LAYF[k]]+'"><span><span class="t">'+esc(LAYN[k][lg()])+'</span><span class="g" style="width:'+Math.round(lc[k]/lmax*100)+'%"></span></span><em>'+lc[k]+'</em></button>';});
  root.querySelector('#mp-lbars').innerHTML=h3||'<p class="mp-hint">'+L('No layer is switched on.','Geen enkele laag staat aan.')+'</p>';
}
function listing(){
  var v=(S.vis||[]).slice().sort(function(a,b){return (b.y-a.y)||((b.m||0)-(a.m||0))||(b.i-a.i);});
  root.querySelector('#mp-listsum').textContent=L('List of the entries shown','Lijst van de getoonde meldingen')+' ('+v.length+')'+
    (v.length>S.listN?' · '+L('first ','eerste ')+S.listN+L(' on paper',' op papier'):'');
  var h='';
  v.slice(0,S.listN).forEach(function(ev){
    h+='<button type="button" class="mp-li" data-i="'+ev.i+'"><span>'+esc(DT(ev.d))+'</span><span><i style="background:'+colour(ev)+'"></i><b>'+
      esc(ev.c?CN(ev.c):L('At sea','Op zee'))+(ev.p?' · '+esc(ev.p):'')+':</b> '+esc(cut((ev.t?ev.t+'. ':'')+ev.tx,190))+'</span></button>';});
  if(v.length>S.listN)h+='<div class="mp-more"><button type="button" class="mp-chip mp-ctl" id="mp-morebtn">'+L('Show all','Toon alles')+' ('+v.length+')</button></div>';
  root.querySelector('#mp-list').innerHTML=h;
}
function zoomTo(evs,pad){
  if(!evs.length)return;
  var x0=1e9,x1=-1e9,y0=1e9,y1=-1e9;
  evs.forEach(function(ev){var x=ev.pr===2&&D.cen[ev.c]?D.cen[ev.c][0]:ev.x,y=ev.pr===2&&D.cen[ev.c]?D.cen[ev.c][1]:ev.yy;
    if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;});
  var bw=Math.max(x1-x0,40),bh=Math.max(y1-y0,40);
  S.vb.w=Math.min(D.W,Math.max(bw,bh*D.W/D.H)*(pad||1.5));
  var h=S.vb.w*D.H/D.W;
  S.vb.x=(x0+x1)/2-S.vb.w/2;S.vb.y=(y0+y1)/2-h/2;
  clampVB();setVB();
}
function zoomAt(f,cx,cy){
  var v=S.vb,h=v.w*D.H/D.W;
  if(cx===undefined){cx=v.x+v.w/2;cy=v.y+h/2;}
  var nw=Math.max(D.W/16,Math.min(D.W,v.w*f)),k=nw/v.w;
  v.x=cx-(cx-v.x)*k;v.y=cy-(cy-v.y)*k;v.w=nw;clampVB();setVB();draw();
}
function svgPt(e){
  var r=svg.getBoundingClientRect(),v=S.vb,h=v.w*D.H/D.W,sc=Math.max(v.w/r.width,h/r.height);
  var ox=(r.width-v.w/sc)/2,oy=(r.height-h/sc)/2;
  return [v.x+(e.clientX-r.left-ox)*sc,v.y+(e.clientY-r.top-oy)*sc,sc];
}
function stories(){
  var h='';
  STORY.forEach(function(s){h+='<button type="button" class="mp-sbtn" data-story="'+s.k+'" aria-pressed="'+(S.story===s.k?'true':'false')+'">'+esc(s[lg()])+'</button>';});
  h+='<button type="button" class="mp-sbtn" data-story="reset">'+L('Show everything','Toon alles')+'</button>';
  root.querySelector('#mp-story').innerHTML=h;
}
function labels(){
  root.querySelectorAll('#mp [data-en]').forEach(function(x){x.textContent=x.getAttribute(lg()==='nl'?'data-nl':'data-en');});
  root.querySelectorAll('#mp [data-t-en]').forEach(function(x){
    var t=x.getAttribute(lg()==='nl'?'data-t-nl':'data-t-en');x.setAttribute('title',t);x.setAttribute('aria-label',t);});
  var sel=root.querySelector('#mp-camp'),cur=S.camp;
  sel.innerHTML='<option value="">'+L('None','Geen')+'</option>'+D.camp.map(function(c){return '<option value="'+c.k+'">'+esc(c[lg()])+'</option>';}).join('');
  sel.value=cur;
  var yo=D.ev.filter(function(e2){return !e2.m;}).length,sh=root.querySelector('#mp-sparkhint');
  if(sh)sh.textContent=L('Click a month to see only that month. ','Klik op een maand om alleen die maand te zien. ')+yo+L(' entries carry only a year and are in no bar.',' meldingen hebben alleen een jaartal en staan in geen enkele balk.');
  stories();
}
function all(){var k=focusKey();labels();tlabel();legend();draw();card();campnote();refocus(k);}
function select(i){
  S.sel=i;S.country=null;
  root.querySelectorAll('.mp-cov path.sel').forEach(function(p){p.classList.remove('sel');});
  draw();card();
}
function stop(){if(S.timer){clearInterval(S.timer);S.timer=null;var b=root.querySelector('#mp-play');
  if(b){b.textContent='▶';b.setAttribute('aria-label',L('Play through the months','Speel de maanden af'));}}}
function runStory(k){
  if(k==='reset'){stop();S.story='';S.prevOn=null;S.shade=false;S.prep=false;S.pdim=false;
    var sc0=root.querySelector('#mp-shade');if(sc0)sc0.checked=false;
    LAYORD.forEach(function(x){S.on[x]=true;});
    S.camp='';S.st='all';S.mode='lay';S.sel=null;S.country=null;S.t=TMAX;S.tm='cum';S.view='pl';S.allC=false;S.listN=60;
    S.vb={x:0,y:0,w:D.W};setVB();
    root.querySelector('#mp-st').value='all';root.querySelector('#mp-mode').value='lay';
    root.querySelector('#mp-t').value=TMAX;root.querySelector('#mp-tm').value='cum';
    root.querySelectorAll('#mp-view button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.v==='pl');});
    all();return;}
  var s=null;STORY.forEach(function(x){if(x.k===k)s=x;});
  if(!s)return;
  stop();S.story=k;S.sel=null;S.country=null;S.prevOn=null;S.camp=s.camp||'';S.st=s.st||'all';S.mode=s.mode||'lay';
  S.t=TMAX;S.tm='cum';root.querySelector('#mp-t').value=TMAX;root.querySelector('#mp-tm').value='cum';
  LAYORD.forEach(function(x){S.on[x]=s.lay?s.lay.indexOf(x)>=0:true;});
  if(s.camp&&!s.lay){var c=camp();if(c)c.ids.forEach(function(i){byId[i].l.forEach(function(x){S.on[x]=true;});});}
  root.querySelector('#mp-st').value=S.st;root.querySelector('#mp-mode').value=S.mode;
  var sub=D.ev.filter(vis);
  if(s.camp)sub=D.ev.filter(function(ev){return camp().ids.indexOf(ev.i)>=0;});
  S.prep=(k==='prep');S.pdim=S.prep;
  if(k==='cables'||k==='freezer'||k==='drones')zoomTo(sub,1.6);else {S.vb={x:0,y:0,w:D.W};setVB();}
  all();
}
function init(r){
  root=r;svg=r.querySelector('#mp-svg');gm=r.querySelector('#mp-mk');gb=r.querySelector('#mp-badge');
  gl=r.querySelector('#mp-lines');glb=r.querySelector('#mp-lbl');gsl=r.querySelector('#mp-sealbl');gpl=r.querySelector('#mp-pl');
  r.dataset.ready='1';S.vb={x:0,y:0,w:D.W};setVB();
  r.classList.toggle('tall',window.innerWidth>=1280);
  var tb=r.querySelector('#mp-tall');if(tb)tb.setAttribute('aria-pressed',r.classList.contains('tall')?'true':'false');
  if(window.innerWidth<760){var dl=r.querySelector('#mp-lays');if(dl)dl.open=false;}
  r.addEventListener('click',function(e){
    var t=e.target;
    if(t.closest&&t.closest('#mp-ftog')){var mc=r.querySelector('#mp-mapcol'),on2=mc.classList.toggle('mp-showf');var fb=t.closest('#mp-ftog');fb.setAttribute('aria-expanded',on2?'true':'false');setTimeout(draw,60);return;}
    if(t.closest&&t.closest('#mp-legjump')){var lgd=r.querySelector('#mp-legend');if(lgd){try{lgd.scrollIntoView({block:'start',behavior:'smooth'});}catch(x){lgd.scrollIntoView();}}return;}
    var c=t.closest('.mp-chip');
    if(c&&c.dataset.prep){S.prep=!S.prep;S.pdim=false;S.story='';all();return;}
    if(c&&c.dataset.k){S.on[c.dataset.k]=!S.on[c.dataset.k];S.prevOn=null;S.story='';all();return;}
    if(c&&c.dataset.all!==undefined){var v=c.dataset.all==='1';LAYORD.forEach(function(k){S.on[k]=v;});S.prevOn=null;S.story='';all();return;}
    var fh=t.closest('.mp-fh');
    if(fh){var f=fh.dataset.fam,ks=LAYORD.filter(function(k){return LAYF[k]===f;});
      var allOn=ks.every(function(k){return S.on[k];});
      var onlyThis=LAYORD.every(function(k){return S.on[k]===(LAYF[k]===f);});
      LAYORD.forEach(function(k){S.on[k]=onlyThis?true:(LAYF[k]===f);});
      S.prevOn=null;S.story='';all();return;}
    var sb=t.closest('.mp-sbtn');if(sb){stop();runStory(sb.dataset.story);if(sb.dataset.story==='reset'){var mc3=r.querySelector('#mp-mapcol'),ft3=r.querySelector('#mp-ftog');if(mc3&&!mc3.classList.contains('mp-showf')){mc3.classList.add('mp-showf');if(ft3)ft3.setAttribute('aria-expanded','true');setTimeout(draw,60);}}return;}
    var vb=t.closest('#mp-view button');if(vb){S.view=vb.dataset.v;
      r.querySelectorAll('#mp-view button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.v===S.view);});
      legend();draw();return;}
    if(t.closest('.mp-skip')){var ls=r.querySelector('#mp-listbox');if(ls){ls.open=true;var su=r.querySelector('#mp-listsum');if(su)su.focus();}return;}
    if(t.id==='mp-morebtn'){S.listN=9999;listing();return;}
    if(t.id==='mp-allc'){S.allC=!S.allC;panel();return;}
    var sp=t.closest('.mp-sp');
    if(sp){stop();var m=+sp.dataset.m;
      if(S.t===m&&S.tm==='one'){S.t=TMAX;}else{S.t=m;S.tm='one';r.querySelector('#mp-tm').value='one';}
      r.querySelector('#mp-t').value=S.t;tlabel();draw();card();return;}
    var bb=t.closest('.mp-bar');
    if(bb){if(bb.dataset.c!==undefined){S.sel=null;S.country=S.country===bb.dataset.c?null:bb.dataset.c;draw();card();}
      else{var k2=bb.dataset.l,solo=LAYORD.filter(function(x){return S.on[x];});
        if(solo.length===1&&solo[0]===k2)LAYORD.forEach(function(x){S.on[x]=true;});
        else LAYORD.forEach(function(x){S.on[x]=x===k2;});
        S.prevOn=null;S.story='';all();}
      return;}
    var z=t.closest('.mp-zoom button');
    if(z){var zz=z.dataset.z;
      if(zz==='reset'){S.vb={x:0,y:0,w:D.W};setVB();draw();}
      else if(zz==='tall'){var on=r.classList.toggle('tall');S.tallUser=true;z.setAttribute('aria-pressed',on?'true':'false');liveRegions();setTimeout(draw,60);}
      else if(zz==='full'){
        try{if(document.fullscreenElement||document.webkitFullscreenElement){(document.exitFullscreen||document.webkitExitFullscreen).call(document);}
          else{var fe=r.querySelector('#mp-mapcol')||r;(fe.requestFullscreen||fe.webkitRequestFullscreen).call(fe);}}catch(e){}
        setTimeout(draw,120);}
      else zoomAt(zz==='in'?.6:1/.6);
      return;}
    if(t.closest('.mp-x')){S.sel=null;S.country=null;
      r.querySelectorAll('.mp-cov path.sel').forEach(function(p){p.classList.remove('sel');});draw();card();return;}
    var li=t.closest('.mp-li');
    if(li){var ev=byId[+li.dataset.i];
      zoomTo([ev],4);if(S.vb.w>D.W/5){S.vb.w=D.W/5;clampVB();setVB();}
      select(ev.i);
      var cb=r.querySelector('.mp-drawer:not(:empty)')||r.querySelector('#mp-card');
      if(cb)cb.scrollIntoView({block:'nearest',behavior:'smooth'});return;}
    if(t.id==='mp-play'){if(S.timer){stop();return;}
      S.t=(S.t>=TMAX)?0:Math.min(S.t+1,TMAX);
      t.textContent='❚❚';t.setAttribute('aria-label',L('Pause','Pauzeren'));
      r.querySelector('#mp-t').value=S.t;tlabel();draw();card();
      S.timer=setInterval(function(){S.t++;r.querySelector('#mp-t').value=S.t;tlabel();draw();card();if(S.t>=TMAX)stop();},850);return;}
  });
  r.addEventListener('change',function(e){
    var t=e.target;
    if(t.id==='mp-shade'){S.shade=t.checked;legend();draw();}
    else if(t.id==='mp-prepsel'){if(t.value){S.sel=null;S.country=t.value;}var fk=focusKey();legend();draw();card();refocus(fk);}
    else if(t.id==='mp-mode'){S.mode=t.value;legend();draw();card();}
    else if(t.id==='mp-st'){S.st=t.value;S.story='';all();}
    else if(t.id==='mp-camp'){S.camp=t.value;S.story='';
      if(S.camp){var c=camp();
        if(c){if(!S.prevOn){S.prevOn={};LAYORD.forEach(function(k){S.prevOn[k]=S.on[k];});}
          c.ids.forEach(function(i){byId[i].l.forEach(function(k){S.on[k]=true;});});}}
      else if(S.prevOn){LAYORD.forEach(function(k){S.on[k]=S.prevOn[k];});S.prevOn=null;}
      all();}
    else if(t.id==='mp-tm'){S.tm=t.value;tlabel();draw();card();}
  });
  r.addEventListener('input',function(e){if(e.target.id==='mp-t'){stop();S.t=+e.target.value;tlabel();draw();card();}});
  r.addEventListener('focusin',function(e){var m=e.target.closest&&e.target.closest('.mp-m,.mp-cl,.mp-b');if(m)S.rov=markKey(m);});
  document.addEventListener('keydown',function(e){
    if(e.key!=='Escape'||e.defaultPrevented||(S.sel===null&&!S.country)||!document.body.contains(r))return;
    var rc=r.getBoundingClientRect();if(rc.bottom<0||rc.top>(window.innerHeight||0)||!rc.width)return;
    S.sel=null;S.country=null;r.querySelectorAll('.mp-cov path.sel').forEach(function(p){p.classList.remove('sel');});draw();card();});
  r.addEventListener('keydown',function(e){
    var mk=e.target.closest&&e.target.closest('.mp-m,.mp-cl,.mp-b');
    if(mk&&['ArrowRight','ArrowDown','ArrowLeft','ArrowUp','Home','End'].indexOf(e.key)>=0){
      e.preventDefault();var ms=marks(),i=ms.indexOf(mk),n=ms.length;
      var k=e.key==='Home'?0:e.key==='End'?n-1:(e.key==='ArrowRight'||e.key==='ArrowDown')?Math.min(n-1,i+1):Math.max(0,i-1);
      ms.forEach(function(m){m.setAttribute('tabindex','-1');});ms[k].setAttribute('tabindex','0');S.rov=markKey(ms[k]);
      try{ms[k].focus({preventScroll:true});}catch(_){ms[k].focus();}
      return;}
    var m=e.target.closest&&(e.target.closest('.mp-m')||e.target.closest('.mp-b')||e.target.closest('.mp-cl'));
    if(m&&(e.key==='Enter'||e.key===' ')){e.preventDefault();hit(m);}});
  var ptr={},drag=null,moved=false,pinch=null,ctimer=null;
  svg.addEventListener('pointerdown',function(e){
    ptr[e.pointerId]=[e.clientX,e.clientY];moved=false;
    var ids=Object.keys(ptr);
    if(ids.length===1)drag={x:e.clientX,y:e.clientY,vx:S.vb.x,vy:S.vb.y,sc:svgPt(e)[2]};
    else if(ids.length===2){var a=ptr[ids[0]],b=ptr[ids[1]];pinch={d:Math.hypot(a[0]-b[0],a[1]-b[1]),w:S.vb.w};drag=null;}});
  svg.addEventListener('pointermove',function(e){
    if(!ptr[e.pointerId])return;
    ptr[e.pointerId]=[e.clientX,e.clientY];var ids=Object.keys(ptr);
    if(pinch&&ids.length===2){var a=ptr[ids[0]],b=ptr[ids[1]],d=Math.hypot(a[0]-b[0],a[1]-b[1]);
      var p=svgPt({clientX:(a[0]+b[0])/2,clientY:(a[1]+b[1])/2});moved=true;
      zoomAt((pinch.w*pinch.d/Math.max(d,1))/S.vb.w,p[0],p[1]);return;}
    if(drag){var dx=e.clientX-drag.x,dy=e.clientY-drag.y;
      if(Math.abs(dx)+Math.abs(dy)>5){moved=true;svg.classList.add('drag');try{svg.setPointerCapture(e.pointerId);}catch(_){}}
      if(moved){S.vb.x=drag.vx-dx*drag.sc;S.vb.y=drag.vy-dy*drag.sc;clampVB();setVB();}}});
  function up(e){delete ptr[e.pointerId];if(Object.keys(ptr).length<2)pinch=null;
    if(!Object.keys(ptr).length){drag=null;svg.classList.remove('drag');if(moved)draw();}}
  function hit(m){
    if(m.classList.contains('mp-m')){select(+m.dataset.i);return;}
    if(m.classList.contains('mp-pl')){S.sel=null;S.country=S.country===m.dataset.c?null:m.dataset.c;draw();card();return;}
    if(m.classList.contains('mp-b')){S.sel=null;S.country=S.country===m.dataset.c?null:m.dataset.c;
      if(S.country)zoomTo(D.ev.filter(function(ev){return ev.c===S.country&&vis(ev);}),2.2);
      draw();card();return;}
    if(m.classList.contains('mp-cl')){var ids=m.dataset.cl.split(',').map(Number),oc=markXY(m),hadF=(document.activeElement===m);
      S.sel=null;S.country=null;zoomTo(ids.map(function(i){return byId[i];}),3.2);draw();card();
      if(hadF){var ms=marks(),bi=-1,bd=1e18;
        ms.forEach(function(q,qi){var xy=markXY(q),dd=Math.hypot(xy[0]-oc[0],xy[1]-oc[1]);if(dd<bd){bd=dd;bi=qi;}});
        if(bi>=0){S.rov=markKey(ms[bi]);rove();try{ms[bi].focus({preventScroll:true});}catch(_){ms[bi].focus();}}}
      return;}
  }
  svg.addEventListener('pointerup',function(e){
    var was=moved;up(e);if(was)return;
    var st=(document.elementsFromPoint?document.elementsFromPoint(e.clientX,e.clientY):[document.elementFromPoint(e.clientX,e.clientY)]).filter(Boolean);
    var m=null,t=null,i2;
    for(i2=0;i2<st.length&&!m;i2++)if(st[i2].closest)m=st[i2].closest('.mp-m,.mp-cl');
    if(!m)for(i2=0;i2<st.length&&!m;i2++)if(st[i2].closest)m=st[i2].closest('.mp-b');
    if(!m)for(i2=0;i2<st.length&&!m;i2++)if(st[i2].closest)m=st[i2].closest('.mp-pl');
    if(m){hit(m);return;}
    t=st[0];if(!t||!t.closest)return;
    var p=t.closest('.mp-cov path');
    if(p){var cc=p.dataset.c;clearTimeout(ctimer);
      ctimer=setTimeout(function(){S.sel=null;S.country=S.country===cc?null:cc;draw();card();},260);}});
  svg.addEventListener('dblclick',function(e){clearTimeout(ctimer);e.preventDefault();
    var pp=svgPt(e);zoomAt(e.shiftKey?2:0.5,pp[0],pp[1]);});
  svg.addEventListener('pointercancel',up);
  var hintT;
  svg.addEventListener('wheel',function(e){
    if(!e.ctrlKey&&!e.metaKey){
      var hh=r.querySelector('#mp-wheelhint');
      if(hh){hh.textContent=L('Hold Ctrl (or Cmd) and scroll to zoom','Houd Ctrl (of Cmd) ingedrukt en scroll om te zoomen');
        hh.classList.add('on');clearTimeout(hintT);hintT=setTimeout(function(){hh.classList.remove('on');},1100);}
      return;}
    e.preventDefault();var p=svgPt(e);zoomAt(e.deltaY>0?1.25:.8,p[0],p[1]);},{passive:false});
  ['fullscreenchange','webkitfullscreenchange'].forEach(function(ev){document.addEventListener(ev,function(){liveRegions();setTimeout(draw,120);});});
  var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){if(root&&document.body.contains(root)){
    if(!S.tallUser){var w2=window.innerWidth>=1280;if(root.classList.contains('tall')!==w2){root.classList.toggle('tall',w2);var tb2=root.querySelector('#mp-tall');if(tb2)tb2.setAttribute('aria-pressed',w2?'true':'false');}}
    liveRegions();draw();card();}},200);});
  function pr(on){if(!root||!document.body.contains(root)||S.printing===on)return;S.printing=on;root.classList.toggle('mp-printing',on);palette();draw();}
  window.addEventListener('beforeprint',function(){pr(true);});
  window.addEventListener('afterprint',function(){pr(false);});
  all();
}
function look(){var r=document.getElementById('mp');if(r&&!r.dataset.ready)init(r);}
setInterval(look,500);document.addEventListener('DOMContentLoaded',look);
new MutationObserver(function(){if(root&&document.body.contains(root))all();}).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
})();
