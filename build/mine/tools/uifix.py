"""App-wide UI fixes (audit U1/U2/U3/U5/U6). Called at the end of fold.py: appends uifix.css / uifix.js to app_template.html
(make_mine.py re-copies the template on every build, so this runs every build). Marker 'uifix:' makes it idempotent."""
M='/home/user/cyberdesk-2026/build/mine/'
def main():
    a=M+'tools/app_template.html'; t=open(a,encoding='utf-8').read()
    if 'uifix: audit fixes' in t: print('uifix already applied'); return
    css=open(M+'tools/uifix.css',encoding='utf-8').read(); js=open(M+'tools/uifix.js',encoding='utf-8').read()
    assert '</style>' in t
    css+=open(M+'tools/bilang.css',encoding='utf-8').read()+open(M+'tools/menu3.css',encoding='utf-8').read()
    t=t.replace('</style>',css+'</style>',1)
    t=t.rstrip()+'\n<script>\n'+js+'\n</script>\n'
    for extra in ('bilang.js','menu3.js'):   # UX round 3: one language at a time, grouped menu
        t=t.rstrip()+'\n<script>\n'+open(M+'tools/'+extra,encoding='utf-8').read()+'\n</script>\n'
    open(a,'w',encoding='utf-8').write(t)
    print('uifix ok')
main()
