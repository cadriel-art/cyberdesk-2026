#!/usr/bin/env python3
"""Post-build step (runs on both output files, after offpatch.py): Dutch text for English-only blocks.

tools/nl_text.json maps the exact English text of an element (whitespace-normalised; <b>/<i>/<a> written as [b]..[/b], [i]..[/i],
[1]..[/1]) to Dutch (same markers). For every element on the listed pages whose text matches a key and that has no Dutch counterpart
yet, the element's content is wrapped as <span class="en-x">English</span><span class="nl-x"> Dutch</span>: exactly the markup
bilang.js produces, so bilang.css shows English in EN mode and Dutch in NL mode, and the search index, the table of contents and the
print modes already understand it. Text that sits next to other markup (a label before a <span class="tag">, a letter badge in a
heading, the name in a table cell that also holds a sector line) is a "segment": the bare text node is wrapped the same way and
looked up on its own.
Links (<a>) inside an element are kept: write [1]words[/1] in the Dutch for the 1st link, [2]..[/2] for the 2nd; a Dutch text without
those markers gets the English link texts appended as "(bron: ...)", so a source link is never dropped.
<div class="bilingual"> (an EN block and an NL block side by side) gets en-x / nl-x on its two halves.
Unmatched keys are reported (did the upstream English change?) and never fail the build. Re-running is harmless (en-x/nl-x are skipped).
Usage: nltext.py [--pages now,freezers,...|all] [file ...]   (default: both output files, the 8 core Belgium pages)"""
import sys, os, re, json
from bs4 import BeautifulSoup, NavigableString, Tag

HERE = os.path.dirname(os.path.abspath(__file__)); M = os.path.dirname(HERE) + '/'
PAGES = ['now', 'freezers', 'year', 'back', 'register', 'numbers', 'powers', 'tools', 'water', 'transport', 'health', 'hybrid', 'elections', 'defence', 'encryption']
MAP = json.load(open(HERE + '/nl_text.json', encoding='utf-8'))
SIMPLE = {'b', 'strong', 'i', 'em', 'a', 'code', 'br', 'small', 'sub', 'sup'}
SKIPTAG = {'script', 'style', 'svg', 'button', 'select', 'option', 'nav', 'textarea'}
SKIPCLS = {'printbar', 'pn', 'filters', 'crumb', 'bl-note', 'u-toc', 'nl', 'plnl', 'pb-nl', 'joe-nl', 'nl-x', 'en-x', 'bl-gone', 'eo-note'}
# round-3 pages: the intro box and the terms box already carry their own Dutch (pb-nl / NL column): leave them alone
BL_PAGES = {'water', 'transport', 'health', 'hybrid', 'elections', 'defence', 'encryption'}
BL_SKIP = {'plainbox', 'termsbox'}
CUR = {'skip': set()}
DUTCHCLS = {'nl', 'plnl', 'pb-nl', 'joe-nl', 'nl-x'}
LET = re.compile(r'[A-Za-z]{3}')


def norm(t): return re.sub(r'\s+', ' ', t).strip()
def cls(e): return set(e.get('class') or [])


def already_dutch(e):
    """round-3 pages: the element already has its own Dutch next to it (a child span.plnl / p.nl, or a following p.nl / p.pb-nl / 'NL:' paragraph)"""
    for c in e.children:
        if isinstance(c, Tag) and cls(c) & {'plnl', 'joe-nl', 'nl', 'pb-nl'}: return True
    n = e.find_next_sibling()
    if n is not None and n.name in ('p', 'div', 'ul', 'li', 'blockquote'):
        if cls(n) & {'nl', 'pb-nl', 'joe-nl', 'plnl'}: return True
        f = n.find(True)
        if f is not None and f.name == 'b' and re.match(r'\s*NL\s*[:–-]', f.get_text()) and n.get_text().strip().startswith('NL'): return True
    return False


def simple_desc(e):
    """True when everything inside is plain inline formatting (so the element's text can be one key)."""
    for d in e.find_all(True):
        if d.name in SIMPLE and (d.name in ('a', 'br') or not d.get('class')):
            continue
        if d.name == 'span' and not d.get('class') and simple_desc(d):
            continue
        return False
    return True


def marked(e):
    out = []; n = [0]
    def rec(x):
        for c in x.children:
            if isinstance(c, NavigableString):
                if type(c).__name__ in ('Comment', 'Doctype', 'CData', 'Declaration', 'ProcessingInstruction'): continue
                out.append(str(c))
            elif c.name == 'a': n[0] += 1; i = n[0]; out.append('[%d]' % i); rec(c); out.append('[/%d]' % i)
            elif c.name in ('b', 'strong'): out.append('[b]'); rec(c); out.append('[/b]')
            elif c.name in ('i', 'em'): out.append('[i]'); rec(c); out.append('[/i]')
            elif c.name == 'br': out.append(' ')
            else: rec(c)
    rec(e); return norm(''.join(out))


def has_dutch(e):
    if cls(e) & DUTCHCLS: return True
    for d in e.find_all(True):
        if cls(d) & DUTCHCLS: return True
        if d.name == 'b' and re.match(r'\s*NL\s*[:–-]', d.get_text()): return True
    return False


def build_nl(nl, links, soup):
    """Dutch string with [b] [i] [n] markers -> (<span> holding the nodes, set of link numbers used)."""
    root = soup.new_tag('span'); cur = root; used = set(); stack = []
    for part in re.split(r'(\[/?(?:b|i|\d+)\])', nl):
        m = re.fullmatch(r'\[(/?)(b|i|\d+)\]', part)
        if not m:
            if part: cur.append(NavigableString(part))
            continue
        close, kind = m.group(1), m.group(2)
        if not close:
            if kind.isdigit() and int(kind) <= len(links):
                t = soup.new_tag('a'); t.attrs = dict(links[int(kind) - 1].attrs); used.add(int(kind))
            elif kind.isdigit(): t = soup.new_tag('span')
            else: t = soup.new_tag(kind)
            cur.append(t); stack.append(cur); cur = t
        elif stack: cur = stack.pop()
    return root, used


def pair(soup, en_nodes, root, lead=''):
    en = soup.new_tag('span'); en['class'] = 'en-x'
    for n in en_nodes: en.append(n)
    nl = soup.new_tag('span'); nl['class'] = 'nl-x'
    if lead: nl.append(NavigableString(lead))
    for n in list(root.contents): nl.append(n.extract())
    return en, nl


def process_article(html, found):
    soup = BeautifulSoup(html, 'html.parser')
    art = soup.find('article'); mods = []; stat = {'el': 0, 'seg': 0, 'bil': 0}

    def walk(e):
        if e.name in SKIPTAG or cls(e) & (SKIPCLS | CUR['skip']): return
        if CUR['skip'] and already_dutch(e): return
        if simple_desc(e):
            t = marked(e)
            if LET.search(t):
                nl = MAP.get(t)
                if nl is not None:
                    found.add(t)
                    if has_dutch(e): return
                    links = e.find_all('a')
                    en_nodes = [c.extract() for c in list(e.children)]
                    root, used = build_nl(nl, links, soup)
                    miss = [a for i, a in enumerate(links, 1) if i not in used]
                    if miss:
                        root.append(NavigableString(' (bron: '))
                        for j, a in enumerate(miss):
                            if j: root.append(NavigableString(', '))
                            t2 = soup.new_tag('a'); t2.attrs = dict(a.attrs); t2.string = a.get_text(); root.append(t2)
                        root.append(NavigableString(')'))
                    en, nlx = pair(soup, en_nodes, root, ' ')
                    e.append(en); e.append(nlx); mods.append(e); stat['el'] += 1
            return
        if e.name == 'div' and 'bilingual' in cls(e):
            kids = [c for c in e.children if isinstance(c, Tag)]
            if len(kids) == 2 and all(c.name == 'div' for c in kids):
                lab = [(k.find('span', class_='lang').get_text().strip() if k.find('span', class_='lang') else '') for k in kids]
                if lab == ['EN', 'NL']:
                    kids[0]['class'] = (kids[0].get('class') or []) + ['en-x']; kids[1]['class'] = (kids[1].get('class') or []) + ['nl-x']
                    mods.append(e); stat['bil'] += 1; found.add('<bilingual>')
            return
        for c in list(e.children):
            if isinstance(c, Tag): walk(c)
            elif type(c).__name__ == 'NavigableString':
                t = norm(str(c))
                if not LET.search(t): continue
                nl = MAP.get(t)
                if nl is None: continue
                found.add(t)
                s = str(c); lead = s[:len(s) - len(s.lstrip())]; trail = s[len(s.rstrip()):]
                root, _ = build_nl(nl, [], soup)
                en, nlx = pair(soup, [NavigableString(s.strip())], root)
                for x in (NavigableString(lead), en, nlx, NavigableString(trail)): c.insert_before(x)
                c.extract(); mods.append(e); stat['seg'] += 1

    for c in list(art.children):
        if isinstance(c, Tag): walk(c)
    return soup, art, mods, stat


def end_of(s, start, tag):
    """offset just after the closing tag that matches the element opening at s[start]"""
    m = re.compile(r'<' + tag + r'''(?:"[^"]*"|'[^']*'|[^'">])*>''').match(s, start)
    if not m: return None
    depth = 1; pos = m.end()
    pat = re.compile(r'<(/?)' + tag + r'''\b(?:"[^"]*"|'[^']*'|[^'">])*>''')
    while depth:
        n = pat.search(s, pos)
        if not n: return None
        if n.group(1): depth -= 1
        elif not n.group(0).endswith('/>'): depth += 1
        pos = n.end()
    return pos


def run_file(path, pages, found_all):
    s = open(path, encoding='utf-8').read(); out = []; last = 0; per = {}; skipped = []
    for k in pages:
        m = re.search(r'<article\b[^>]*\bid="p-%s"' % re.escape(k), s)
        if not m: continue
        a = m.start(); b = s.find('</article>', a)
        if b < 0: continue
        b += len('</article>')
        html = s[a:b]
        # offsets of start tags inside this article
        lines = html.split('\n'); starts = [0]
        for ln in lines[:-1]: starts.append(starts[-1] + len(ln) + 1)
        found = set()
        CUR['skip'] = BL_SKIP if k in BL_PAGES else set()
        soup, art, mods, stat = process_article(html, found)
        found_all |= found
        per[k] = stat
        # splice the re-serialised outermost modified elements back into the original text
        new_ids = {id(x) for x in mods}
        top = []
        for x in mods:
            if any(id(p) in new_ids for p in x.parents): continue
            if not any(x is y for y in top): top.append(x)
        pos = {id(x): (x.sourceline, x.sourcepos) for x in top}
        edits = []
        for x in top:
            ln, col = pos[id(x)]
            if ln is None: skipped.append((k, x.name)); continue
            st = starts[ln - 1] + col; en = end_of(html, st, x.name)
            if en is None: skipped.append((k, x.name)); continue
            edits.append((a + st, a + en, str(x)))
        edits.sort()
        for st, en, new in edits:
            if st < last: continue
            out.append(s[last:st]); out.append(new); last = en
    out.append(s[last:])
    open(path, 'w', encoding='utf-8').write(''.join(out))
    return per, skipped


def main():
    args = sys.argv[1:]; pages = PAGES
    if args[:1] == ['--pages']:
        pages = None if args[1] == 'all' else args[1].split(','); args = args[2:]
    files = args or [M + 'cyber-desk-offline.html', M + 'cyber-desk.html']
    for f in files:
        if not os.path.exists(f): continue
        pg = pages
        if pg is None:
            pg = re.findall(r'<article\b[^>]*\bid="p-([a-z0-9]+)"', open(f, encoding='utf-8').read())
        found = set()
        per, skipped = run_file(f, pg, found)
        tot = {k: sum(v.values()) for k, v in per.items()}
        print('nltext %s: %s' % (os.path.basename(f), ', '.join('%s %d' % (k, n) for k, n in tot.items())))
        if skipped: print('nltext: could not place', skipped)
        if f.endswith('cyber-desk-offline.html'):
            unmatched = [k for k in MAP if k not in found]
            print('nltext: %d keys in nl_text.json, %d unmatched' % (len(MAP), len(unmatched)))
            for k in unmatched[:60]: print('  unmatched key: ' + k[:110])


if __name__ == '__main__':
    main()
