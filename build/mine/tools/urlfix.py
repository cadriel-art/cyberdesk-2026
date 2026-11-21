"""Post-build fixes on the two output files (moved links, labels). Run after offpatch.py (see build_all.sh)."""
M='/home/user/cyberdesk-2026/build/mine/'
R=[
('https://www.vrt.be/vrtnws/nl/liveblog/quintin-ook-in-ons-land-aanwijzingen-voor-iraanse-betrokkenhei~1793610043244/','https://www.vrt.be/vrtnws/nl/liveblog/quintin-verdedigt-uitspraken-over-betrokkenheid-iran-bij-cyberaa~1793610043244/'),
('https://www.euronews.com/my-europe/2025/03/26/','https://www.euronews.com/2025/03/26/'),
('https://www.euronews.com/my-europe/2025/05/14/','https://www.euronews.com/2025/05/14/'),
('https://www.euronews.com/next/2025/09/05/','https://www.euronews.com/2025/09/05/'),
('https://www.euronews.com/next/2026/09/09/','https://www.euronews.com/2026/09/09/'),
('VRT NWS: Quintin sees indications of Iranian involvement (12 Nov 2026)','VRT NWS (12 Nov 2026): Quintin on indications of Iranian involvement; the page now leads with Minister Prevot saying the data do not suffice to hold Iran responsible'),
]
for f in ('cyber-desk.html','cyber-desk-offline.html'):
    s=open(M+f,encoding='utf-8').read()
    for a,b in R:
        if a not in s: print('urlfix: no match',f,a[:60])
        s=s.replace(a,b)
    open(M+f,'w',encoding='utf-8').write(s)
print('urlfix ok')
