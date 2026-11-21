"""Pre-build text fixes for upstream text that is re-copied by make_mine.py (register, briefing, content.json).
Run from the top of year2026.py. Each rule is (old, new); a rule that matches nothing is reported, not fatal."""
import json,datetime
M='/home/user/cyberdesk-2026/build/mine/'
FILES=[M+'cyber-incident-register.html',M+'vrt-cyber-briefing.html',M+'tools/content.json']
RULES=[
# F2 AZ Monica: one figure everywhere (hospital via press: main systems back after about 5 weeks, 19 Feb)
("Paper for about 3 weeks.","Worked on paper; main systems back after about 5 weeks (19 Feb)."),
("about three weeks on paper.","worked on paper; main systems back after about five weeks."),
("about three weeks on paper;","worked on paper, main systems back after about five weeks;"),
("Then AZ Monica ran on paper for three weeks.","Then AZ Monica needed about five weeks to get its main systems back."),
("AZ Monica worked on paper for three weeks.","AZ Monica needed about five weeks to get its main systems back."),
("AZ Monica ran on paper for about three weeks and transferred seven patients","AZ Monica worked on paper, needed about five weeks to get its main systems back and transferred seven patients"),
("AZ Monica needed about three weeks to restore patient records","AZ Monica needed about five weeks to get its main systems back"),
("AZ Monica in Antwerp worked on paper for about three weeks in January 2026 and transferred seven patients.","AZ Monica in Antwerp worked on paper in January 2026, needed about five weeks to get its main systems back and transferred seven patients."),
("AZ Monica in Antwerpen werkte in januari 2026 ongeveer drie weken op papier en bracht zeven patiënten over.","AZ Monica in Antwerpen werkte in januari 2026 op papier, had ongeveer vijf weken nodig om de hoofdsystemen terug te krijgen en bracht zeven patiënten over."),
("Electronic patient records came back only after about three weeks.","The main systems, patient records included, were back only after about five weeks (19 February)."),
("For about three weeks, doctors and nurses worked on paper.","For weeks, doctors and nurses worked on paper."),
("Ongeveer drie weken werkten artsen en verpleegkundigen op papier.","Weken lang werkten artsen en verpleegkundigen op papier."),
# F3 warning to attack: 13 Oct -> 2 Nov = 20 days
("Belgian shops were hit 19 days later.","Belgian shops were hit on 2 November, 20 days later."),
("De Belgische winkels werden 19 dagen later getroffen.","De Belgische winkels werden op 2 november getroffen, 20 dagen later."),
("Nineteen days after the warning, Belgian stores were hit.","Twenty days after the warning (13 October to 2 November), Belgian stores were hit."),
("Nineteen days later the stores were hit.","Twenty days later (on 2 November) the stores were hit."),
("Nineteen days, and nobody was obliged to act.","Twenty days, and nobody was obliged to act."),
("hit on 2 November: 19 days of inaction.","hit on 2 November: 20 days between warning and attack."),
('<div class="n">19 days</div>','<div class="n">20 days</div>'),
("and 19 days later the attack came","and 20 days later the attack came"),
("en 19 dagen later kwam de aanval","en 20 dagen later kwam de aanval"),
# F6 ENISA
("analysed more than 8,000 serious incidents","counted 8,257 incidents"),
# F7 freezer: media-sourced fire count, France's claim
("controllers, 15+ fires. Attributed by France to Iran's Revolutionary Guards unit Shahid Kaveh on 9 Nov.","controllers; at least 15 fires, according to media reports. France says Iran's Revolutionary Guards unit Shahid Kaveh was behind it (9 Nov); Iran denies it, and US agencies reportedly have low confidence in the link."),
("(about 700 sites, at least 15 fires) to Shahid Kaveh","(about 700 sites, at least 15 fires according to media reports) to Shahid Kaveh"),
("at least 15 fires; food losses in the tens of millions across Europe (Facilities Dive).","at least 15 fires, according to media reports; food losses in the tens of millions across Europe (Facilities Dive)."),
("French supermarket sites sabotaged in October, 15+ fires","French supermarket sites sabotaged in October, at least 15 fires (media reports)"),
("Attributed by France to Iran's IRGC.","France says Iran's IRGC was behind it."),
("France, 11–12 October: about 700 supermarket sites, at least 15 fires.","France, 11–12 October: about 700 supermarket sites, at least 15 fires according to media reports."),
("France counted at least 15 fires.","media reports count at least 15 fires in France."),
# F11 Estonia / Threod
# F14 language
("Both China and Russia spy on a mid-sized Member State,","Czech authorities say both China and Russia spy on a mid-sized Member State,"),
("Zowel China als Rusland bespioneren een middelgrote lidstaat,","De Tsjechische autoriteiten zeggen dat zowel China als Rusland een middelgrote lidstaat bespioneren,"),
("drone attack on Leipzig airport, blamed on Russia.","drone attack on Leipzig airport, which the German federal government blames on Russia."),
("the government formally blamed China's state-linked group APT31","the government formally blamed China's state-linked group APT31 (a hacking group known by that code name)"),
("Russia's FSB Centre 16","a unit of Russia's FSB security service (Centre 16)"),
("Who holds what in Belgium:</b> Elia runs the high-voltage grid; Fluvius (Flanders), ORES and RESA (Wallonia) and Sibelga (Brussels) run the local grids; the CREG is the federal energy regulator; the FANC supervises nuclear sites; the Centre for Cybersecurity Belgium coordinates cyber incidents; the federal energy minister and the regional energy ministers share the policy.","Who holds what in Belgium:</b> Elia runs the high-voltage grid. Fluvius (Flanders), ORES and RESA (Wallonia) and Sibelga (Brussels) run the local grids. The CREG is the federal energy regulator. The FANC supervises nuclear sites. The Centre for Cybersecurity Belgium coordinates cyber incidents. The federal energy minister and the regional energy ministers share the policy."),
]
RAWJSON=[('"n": "19 days"','"n": "20 days"')]
def run():
    texts={f:open(f,encoding='utf-8').read() for f in FILES}
    for a,b in RULES:
        hits=0
        for f in FILES:
            ea,eb=(json.dumps(a)[1:-1],json.dumps(b)[1:-1]) if f.endswith('.json') else (a,b)
            n=texts[f].count(ea)
            if n: texts[f]=texts[f].replace(ea,eb); hits+=n
        if not hits: print('fixtext: no match for',a[:60])
    for a,b in RAWJSON:
        k=M+'tools/content.json'
        if a in texts[k]: texts[k]=texts[k].replace(a,b)
        else: print('fixtext: no match for',a)
    for f in FILES: open(f,'w',encoding='utf-8').write(texts[f])
if __name__=='__main__': run()
