/* ===== UX round 3 (B): one language at a time =====
   The app has long carried Dutch next to English (.plnl, .pb-nl, .joe-nl, p.nl, span.nl, div.nl, "English · <i>Dutch</i>" headings,
   "A · B" summaries, tables with an NL column). This script pairs each Dutch piece with its English counterpart once per page,
   marks them (.nl-x = Dutch, .en-x = English counterpart) and bilang.css shows only one of them, by html[lang].
   NL mode: Dutch where it exists, English where it does not (one short note per page). EN mode: English only.
   Print: "English only" (pl-en) / "Dutch first" (pl-nl) / "English and Dutch" (pl-both) in Print a selection; other printing follows the screen. */
(function(){
'use strict';
var doc=document,root=doc.documentElement;
function lang(){return root.lang==='nl'?'nl':'en';}
function $(s,r){return (r||doc).querySelector(s);}
function $$(s,r){return [].slice.call((r||doc).querySelectorAll(s));}
var pagesEl=$('#pages'); if(!pagesEl) return;

/* page names and groups from the app's NAV table */
var NAVK={},GRP={};
try{var ss=doc.scripts;for(var i=0;i<ss.length;i++){var tx=ss[i].text,ix=tx.indexOf('const NAV = ');if(ix>=0){var ex=tx.indexOf(';\n',ix);JSON.parse(tx.slice(ix+12,ex)).forEach(function(g){(g.items||[]).forEach(function(it){NAVK[it.k]=it;GRP[it.k]=g;});});break;}}}catch(e){}

function mk(tag,cls,txt){var e=doc.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e;}
function tn(s){return doc.createTextNode(s);}
var uid=0;
function isHead(n){return n&&/^H[1-6]$/.test(n.tagName);}
function wrapText(n){ /* a text node with real words becomes <span class="en-x"> */
  var s=mk('span','en-x');n.parentNode.insertBefore(s,n);s.appendChild(n);return s;
}

/* ---- the "NL:" / "NL – label:" markers at the start of Dutch pieces ---- */
function capSpan(rest){var f=rest.charAt(0),o=mk('span','nl-cap',f);var r=doc.createDocumentFragment();r.appendChild(o);r.appendChild(tn(rest.slice(1)));return r;}
function tidyLabel(e){
  var f=e.firstChild;while(f&&f.nodeType===3&&!f.nodeValue.trim())f=f.nextSibling;
  if(!f)return false;
  if(f.nodeType===1&&f.tagName==='B'){
    var m=/^NL\s*([:–-])\s*([\s\S]*)$/.exec(f.textContent);
    if(!m)return false;
    var dash=m[1]!==':';
    if(!m[2].trim()){f.classList.add('nl-lbl');return dash;}
    f.textContent='';f.appendChild(mk('span','nl-lbl','NL'+(dash?' – ':': ')));f.appendChild(capSpan(m[2]));return dash;
  }
  if(f.nodeType===3){
    var m2=/^(\s*NL\s*[:–-]\s*)([\s\S]*)$/.exec(f.nodeValue);
    if(!m2)return false;
    var s=mk('span','nl-lbl',m2[1].trim()+' ');
    e.insertBefore(s,f);var frag=capSpan(m2[2]);e.insertBefore(frag,f);e.removeChild(f);
  }
  return false;
}

/* ---- block-level Dutch (p.pb-nl, div.pb-nl, p.joe-nl, p.nl, div.nl) ---- */
var BLK={P:1,UL:1,OL:1,DIV:1};
function blockPartners(e){
  var out=[],prev=e.previousElementSibling;
  while(prev&&(prev.classList.contains('u-toc')||prev.classList.contains('bl-note')||prev.classList.contains('printbar')||prev.classList.contains('bl-gone')))prev=prev.previousElementSibling;
  if(!prev)return out;
  var all=e.classList.contains('pb-nl')||e.tagName==='DIV';
  if(all){
    for(var s=prev;s;s=s.previousElementSibling){
      if(s.classList.contains('nl-x')||s.classList.contains('bl-gone')||isHead(s)||!BLK[s.tagName])break;
      if(s.classList.contains('pb-terms'))continue;
      out.push(s);
    }
  }else if(BLK[prev.tagName]&&!prev.classList.contains('nl-x'))out.push(prev);
  return out;
}
function swapHeading(h,e){
  if(h.dataset.bsw)return;
  var en=h.textContent,m=/\s*(\(\d+\))\s*$/.exec(en),cnt=m?' '+m[1]:'';
  var wrap=mk('span','en-x');while(h.firstChild)wrap.appendChild(h.firstChild);
  var nl=mk('span','nl-x',e.textContent.replace(/^\s*NL\s*[:–-]\s*/,'').trim()+cnt);
  h.appendChild(wrap);h.appendChild(nl);h.dataset.bsw='1';
  e.classList.add('bl-gone');e.setAttribute('aria-hidden','true');
}

/* ---- inline Dutch (span.plnl, span.nl, small.nl) inside the English sentence's own element ---- */
var KEEP='.tag,.pill,br,.pr-d,.small,.sector,.count,button,svg,input,.printbtn,.live';
function inlinePartners(e,dash){
  var par=e.parentElement,out=[],keepB=(par.tagName==='LI')&&!dash;
  for(var n=par.firstChild;n;n=n.nextSibling){
    if(n===e||n.nodeType===8)continue;
    if(n.nodeType===3){if(/^[\s·|,;:–—-]*$/.test(n.nodeValue))continue;out.push(n);continue;}
    if(n.nodeType!==1)continue;
    if(n.classList.contains('nl-x')||n.classList.contains('en-x')||n.matches('.plnl,.nl,.pb-nl,.joe-nl'))continue;
    if(n.matches(KEEP))continue;
    if(n.tagName==='B'&&keepB)continue;
    out.push(n);
  }
  return out;
}
function placeInline(e){ /* Dutch right after the English words, before a status tag that followed them */
  var p=e.previousSibling;while(p&&p.nodeType===3&&!p.nodeValue.trim())p=p.previousSibling;
  if(!p||p.nodeType!==1||!p.matches('.tag,.pill,.small'))return;
  var first=p;while(true){var q=first.previousSibling;while(q&&q.nodeType===3&&!q.nodeValue.trim())q=q.previousSibling;if(q&&q.nodeType===1&&q.matches('.tag,.pill,.small'))first=q;else break;}
  var before=first.previousSibling;while(before&&before.nodeType===3&&!before.nodeValue.trim())before=before.previousSibling;
  if(before&&!(before.nodeType===1&&before.tagName==='BR'))first.parentNode.insertBefore(e,first);
}

function pairOne(e){
  if(e.classList.contains('nl-x')||e.classList.contains('eo-note')||e.closest('.hl,#hm-root'))return;
  var inline=(e.tagName==='SPAN'||e.tagName==='SMALL');
  var fb=e.firstElementChild,dash=!!(fb&&fb.tagName==='B'&&/^NL\s*[–-]/.test(fb.textContent));
  tidyLabel(e);
  var id=++uid;e.classList.add('nl-x');
  if(inline){
    var ps=inlinePartners(e,dash);
    ps.forEach(function(n){var x=n.nodeType===3?wrapText(n):n;x.classList.add('en-x');x.dataset.bq=id;});
    if(ps.length)placeInline(e);
  }else{
    var prev=e.previousElementSibling;while(prev&&(prev.classList.contains('u-toc')||prev.classList.contains('bl-note')||prev.classList.contains('printbar')))prev=prev.previousElementSibling;
    if(prev&&isHead(prev)&&e.tagName==='P'&&!prev.dataset.bsw&&e.parentNode&&e.parentNode.tagName==='SECTION'){swapHeading(prev,e);return;}
    var bp=blockPartners(e),enLen=0;
    bp.forEach(function(x){enLen+=x.textContent.length;});
    /* a Dutch line much shorter than the English it sits beside is a summary, not a translation: keep the English facts visible too */
    if(enLen>500&&e.textContent.length<0.3*enLen){e.dataset.bpartial='1';e.dataset.bp=id;return;}
    bp.forEach(function(x){x.classList.add('en-x');x.dataset.bq=id;});
  }
  e.dataset.bp=id;
}

/* ---- Dutch tail inside one element: "English text <br><b>NL:</b> Dutch text" ---- */
function trailingNL(b){
  var par=b.parentElement;if(!par||par.closest('.nl-x'))return;
  var id=++uid,nl=mk('span','nl-x');nl.dataset.bp=id;
  var prev=b.previousSibling,br=null;
  while(prev&&prev.nodeType===3&&!prev.nodeValue.trim())prev=prev.previousSibling;
  if(prev&&prev.nodeType===1&&prev.tagName==='BR')br=prev;
  var rest=[];for(var n=b;n;n=n.nextSibling)rest.push(n);
  par.insertBefore(nl,b);rest.forEach(function(n){nl.appendChild(n);});
  tidyLabel(nl);
  if(br){br.className='bl-sep en-x nl-x';}
  var ens=[];
  for(var s=par.firstChild;s&&s!==nl;s=s.nextSibling){
    if(s===br)continue;
    if(s.nodeType===3){if(s.nodeValue.trim())ens.push(s);continue;}
    if(s.nodeType===1&&!s.matches(KEEP))ens.push(s);
  }
  ens.forEach(function(n){var x=n.nodeType===3?wrapText(n):n;x.classList.add('en-x');x.dataset.bq=id;});
}

/* ---- headings and summaries: "English · Dutch" ---- */
function splitDot(h){
  if(h.dataset.bd)return;
  var nodes=[].slice.call(h.childNodes),ix=-1;
  for(var i=0;i<nodes.length;i++)if(nodes[i].nodeType===3&&nodes[i].nodeValue.indexOf(' · ')>=0){ix=i;break;}
  if(ix<0)return;
  var v=nodes[ix].nodeValue,k=v.indexOf(' · '),a=v.slice(0,k),b=v.slice(k+3);
  var en=mk('span','en-x'),nl=mk('span','nl-x');
  for(i=0;i<ix;i++)en.appendChild(nodes[i]);
  var cm=/\((\d+)\)\s*$/.exec(b);
  en.appendChild(tn(a+((cm&&!/\(\d+\)\s*$/.test(a))?' ('+cm[1]+')':'')));
  nl.appendChild(tn(b));
  for(i=ix+1;i<nodes.length;i++)nl.appendChild(nodes[i]);
  while(h.firstChild)h.removeChild(h.firstChild);
  h.appendChild(en);h.appendChild(nl);h.dataset.bd='1';
}
function splitH4(h){
  var i=null;for(var c=h.firstElementChild;c;c=c.nextElementSibling)if(c.tagName==='I'){i=c;break;}
  if(!i||i.classList.contains('nl-x'))return;
  var p=i.previousSibling;
  if(!p||p.nodeType!==3||!/\s·\s*$/.test(p.nodeValue))return;
  p.nodeValue=p.nodeValue.replace(/\s·\s*$/,'');
  var w=wrapText(p),sep=mk('span','bl-sep en-x nl-x',' · ');
  h.insertBefore(sep,i);i.classList.add('nl-x');
}

/* ---- tables with an "NL" column: Dutch column replaces the English one before it ---- */
var HDR={'In plain words':'In gewone woorden','EN':'Betekenis','What it means for you':'Wat het voor jou betekent'};
function fixCols(t){
  if(t.dataset.bc)return;
  var ths=$$('thead th',t),ix=-1;
  for(var i=0;i<ths.length;i++)if(ths[i].textContent.trim()==='NL'){ix=i;break;}
  if(ix<1)return;
  t.dataset.bc='1';
  var pt=ths[ix-1].textContent.trim();
  $$('tr',t).forEach(function(r){
    var c=r.children;if(c.length<=ix)return;
    c[ix].classList.add('nl-x');c[ix-1].classList.add('en-x');
  });
  var h=ths[ix];h.textContent='';h.appendChild(mk('span','',HDR[pt]||pt));
}

/* ---- one page ---- */
function structure(pg){
  if(pg.dataset.bl)return;pg.dataset.bl='1';
  $$('p.nl,div.nl,.pb-nl,.joe-nl,.plnl,span.nl,small.nl',pg).forEach(pairOne);
  $$('b',pg).filter(function(x){return /^NL\s*[:–-]/.test(x.textContent)&&!x.closest('.nl-x,.nl-lbl')&&x.parentElement&&!x.parentElement.matches('p.nl,div.nl,.pb-nl,.joe-nl,.plnl,span.nl,small.nl');}).forEach(trailingNL);
  $$('details.plainbox>summary,details.termsbox>summary,details.qa>summary,.pb-h,.joe-h',pg).forEach(splitDot);
  $$('h4',pg).forEach(splitH4);
  $$('table',pg).forEach(fixCols);
  /* note on pages that stay partly English in Dutch mode */
  var k=pg.id.slice(2);
  if(/^(home|search|printsel|map|news|updates)$/.test(k))return;
  var chars=0,paired=0;$$('.nl-x',pg).forEach(function(x){if(!x.parentElement.closest('.nl-x'))paired+=x.textContent.length;});
  $$('p,li,td',pg).forEach(function(e){
    if(e.closest('.en-x,.nl-x,.termsbox,.plainbox,.u-toc,.printbar,.pn,summary,.bl-note'))return;
    if(e.querySelector('.nl-x,p,li,td,ul,ol,table'))return;
    var n=e.textContent.trim().length;if(n>40)chars+=n;
  });
  if(chars>=900&&chars>0.5*paired){
    var sub=$('.sub',pg)||$('h1',pg),note=mk('p','small bl-note');
    note.textContent=paired>400?'Let op: een deel van deze pagina staat alleen in het Engels.':'Let op: deze pagina staat voorlopig alleen in het Engels.';
    if(sub)sub.parentNode.insertBefore(note,sub.nextSibling);
  }
}

/* ---- titles and the group line follow the menu in the active language ---- */
function chrome(pg){
  var k=pg.id.slice(2),it=NAVK[k],g=GRP[k];if(!it||k==='home'||k==='search')return;
  var h=$('h1',pg);
  if(h&&!h.children.length){var w=it[lang()]||it.en;if(h.textContent!==w)h.textContent=w;}
  var c=$('.crumb',pg);
  if(c&&g){var w2=g[lang()]||g.en;if(c.textContent!==w2)c.textContent=w2;}
}
function run(){
  if(mo)mo.disconnect();
  try{$$('#pages > article.page').forEach(function(pg){structure(pg);chrome(pg);});}catch(e){if(window.console)console.warn('bilang',e);}
  if(!indexed){indexed=true;try{if(window.cdUI&&window.cdUI.reindex)window.cdUI.reindex();}catch(e){}}
  if(mo)attach();
}
var mo=null,timer=null,indexed=false;
function attach(){mo.observe(pagesEl,{childList:true,subtree:true});mo.observe(root,{attributes:true,attributeFilter:['lang']});}
function sched(){clearTimeout(timer);timer=setTimeout(run,60);}
mo=new MutationObserver(sched);
run();
window.cdBilang={rerun:run};
})();
