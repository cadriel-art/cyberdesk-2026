/* ===== UX round 3 (A): the menu groups are real headings (h2 with a toggle button) and can be collapsed =====
   The app redraws #nav on every route and language change; this script re-applies the grouping each time.
   Desktop: all groups open. Phone: only the group of the current page is open until the reader opens another.
   The group of the page you navigate to always opens (on a phone the groups you did not open yourself close again). State lives in memory only. */
(function(){
'use strict';
var doc=document,root=doc.documentElement,nav=doc.getElementById('nav');
if(!nav)return;
function mq(){return window.matchMedia&&window.matchMedia('(max-width:900px)').matches;}
var state=null,lastCur=null,touched={};
function curKey(){var a=nav.querySelector('a[aria-current="page"]');return a?a.dataset.k:null;}
function apply(){
  var groups=[].slice.call(nav.querySelectorAll(':scope > .nav-g'));
  if(!groups.length)return;
  var cur=curKey(),curGi=-1;
  groups.forEach(function(g,i){if(cur&&g.querySelector('a[data-k="'+cur+'"]'))curGi=i;});
  if(!state){state=groups.map(function(g,i){return mq()?(i!==curGi):false;});}
  if(cur!==lastCur){if(mq())state=state.map(function(c,i){return touched[i]?c:true;});if(curGi>=0)state[curGi]=false;lastCur=cur;}
  groups.forEach(function(g,i){
    if(g.dataset.m3)return;
    var sp=g.firstElementChild;if(!sp||sp.tagName!=='SPAN')return;
    g.dataset.m3='1';g.setAttribute('role','group');
    var hid='ng-h-'+i,lid='ng-l-'+i;
    var h=doc.createElement('h2');h.className='nav-gh';h.id=hid;
    var b=doc.createElement('button');b.type='button';b.className='nav-gb';b.setAttribute('aria-controls',lid);
    var t=doc.createElement('span');t.className='nav-gt';t.textContent=sp.textContent;
    var c=doc.createElement('span');c.className='nav-gc';c.setAttribute('aria-hidden','true');
    b.appendChild(t);b.appendChild(c);h.appendChild(b);
    var list=doc.createElement('div');list.className='nav-gl';list.id=lid;
    var kids=[].slice.call(g.children).filter(function(x){return x!==sp;});
    kids.forEach(function(a){list.appendChild(a);});
    g.removeChild(sp);g.setAttribute('aria-labelledby',hid);g.appendChild(h);g.appendChild(list);
    b.addEventListener('click',function(){state[i]=!state[i];touched[i]=true;paint(g,i);});
  });
  groups.forEach(function(g,i){paint(g,i);});
}
function paint(g,i){
  var b=g.querySelector('.nav-gb'),l=g.querySelector('.nav-gl');if(!b||!l)return;
  var open=!state[i];
  b.setAttribute('aria-expanded',open?'true':'false');
  if(open)l.removeAttribute('hidden');else l.setAttribute('hidden','');
  g.classList.toggle('nav-closed',!open);
}
var mo=new MutationObserver(function(){mo.disconnect();try{apply();}catch(e){}mo.observe(nav,{childList:true});});
mo.observe(nav,{childList:true});
apply();
})();
