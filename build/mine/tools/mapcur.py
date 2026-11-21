# Hand curation of the subject-page events (ids from mapclass.build()). Register rows are all kept.
def R(a,b): return set(range(a,b+1))
DROP={4,7,8,9,10,13,14,15,17,18,19,20,21,22,23,27,30,31,32,33,35,36,38,39,42,43,48,49,51,58,62,63,77,85,88,90,91,
 122,126,125,127,131,136,141,143,149,157,165,166,170,171,181,184,185,186,190,191,192,194,204,209,215,217,221,222,
 229,231,233,234,237,246,250,254,256,259,260,290,298,57}|R(65,67)|R(69,75)|R(78,82)|R(98,105)|R(304,307)|R(309,314)|R(317,327)|{89}
# later development -> the event it belongs to
FOLLOW={47:46,52:40,60:56,110:107,119:118,120:117,124:123,128:86,140:138,159:158,162:161,163:161,173:169,179:177,197:196,199:198,239:238,248:247}
# place overrides: id -> name in G, or (lat,lon,label,approx), or '' for country level
PL={1:'Antwerp',3:'Brussels Airport',5:'Liège Airport',12:'Brussels Airport',26:'Brussels Airport',37:'Brussels Airport',25:'',34:'',
 83:(57.3,20.0,'Sea between Latvia and Gotland',1),84:(55.9,16.6,'Baltic Sea, cable between Germany and Finland',1),86:(59.75,24.9,'Gulf of Finland',1),87:(57.3,20.4,'Sea between Latvia and Gotland',1),
 92:(54.3,4.6,'North Sea, north of Texel',1),95:(47.25,15.0,'Styria',1),111:(43.2,29.2,'Black Sea, off Bulgaria',1),133:'',134:'',
 151:(55.90,27.17,'Krāslava district',1),152:(56.51,27.33,'Rēzekne',0),158:(49.63,6.20,'Findel airport',0),169:(51.80,21.75,'Mika, on the Warsaw–Lublin line',0),
 177:(45.65,25.60,'Brașov',0),178:(44.0,29.4,'Black Sea, off Romania',1),180:(49.00,21.24,'Prešov',0),183:'',188:(57.67,12.29,'Gothenburg-Landvetter Airport',0),189:(47.4,8.1,'Canton Aargau',1),
 193:(51.59,7.66,'Kamen',0),202:(41.54,2.44,'Mataró',0),214:(43.62,13.51,'Ancona',0),218:(54.71,20.51,'Kaliningrad region (source of the signal)',1),224:(42.24,-8.72,'Vigo',0),226:(56.8,17.6,'Baltic Sea, near Gotland and Öland',1),
 235:'',236:'',268:(55.65,12.47,'Hvidovre',0),276:(48.11,5.14,'Chaumont',0),280:(49.25,11.09,'Roth',0),281:(54.09,13.38,'Greifswald',0),284:(50.66,12.20,'Greiz',0),297:(50.09,18.22,'Racibórz',0),303:(46.85,9.53,'Chur',0),
 40:'Brussels',46:'Brussels',53:'Brussels',29:'Antwerp',164:(60.19,11.10,'Oslo Airport',0),135:(48.35,11.79,'Munich Airport',0),117:(55.62,12.65,'Copenhagen Airport',0),144:(53.43,-6.25,'Dublin Airport',0)}
# layer overrides
LY={1:['drones','intim'],11:['spying'],37:['intim','transport'],116:['intim','transport'],129:['intim'],130:['intim'],134:['intim','transport'],148:['intim','schools'],
 121:['sabotage'],174:['energy'],182:['energy'],183:['sabotage','transport'],294:['health'],50:['spying'],53:['spying','elections'],46:['intim','elections'],76:['spying','gov'],68:['defence','gov'],
 106:['spying'],146:['spying'],147:['spying'],153:['spying'],315:['spying','defence'],316:['spying','defence'],308:['gov','defence'],108:['drones'],137:['sabotage','transport'],145:['sabotage','transport'],
 218:['jamming','transport'],226:['jamming','transport'],92:['jamming','transport'],83:['cables'],84:['cables'],86:['cables'],87:['cables'],142:['sabotage'],168:['sabotage'],172:['spying','sabotage'],
 28:['transport'],29:['transport'],247:['spying','elections'],45:['elections','gov'],154:['drones','transport'],3:['drones','transport'],5:['drones','transport'],12:['drones','transport'],
 117:['drones','transport'],135:['drones','transport'],139:['drones','transport'],144:['drones','transport'],158:['drones','transport'],164:['drones','transport'],188:['drones','transport'],
 113:['drones','defence'],0:['drones','defence'],2:['drones','defence'],161:['drones','defence'],187:['drones','defence'],6:['drones','energy'],133:['food'],160:['food'],
 107:['sabotage','defence'],109:['sabotage','defence'],115:['sabotage','defence'],123:['sabotage','defence'],177:['sabotage','defence'],180:['sabotage','defence'],138:['drones','sabotage','transport'],
 150:['sabotage','transport'],169:['sabotage','transport'],111:['drones','transport'],178:['drones','transport'],16:['water'],196:['water'],198:['water']}
# register rows that repeat a subject-page event, or are summaries
DROP|={332,337,341,345,346,349,354,355,360,366,375,376,377,390,394,396,399,402,420,421,426,429,436,444,450,451,457,463,467,469,472,482,483,496,504,517,519,525,528,551,552,553,379,382,415}
PL.update({419:'',507:'',430:'',542:'',530:''})
LY.update({507:['sabotage','energy']})
DROP|={160}
# tracker case index -> event id
CASE={0:155,1:121,2:150,3:153,4:106,5:146,6:86,7:29,8:114,9:129,10:133,11:169,13:172,14:142,15:208,16:11,17:147,18:1,19:28,20:180,21:115,23:138,24:398,25:393,26:395,27:123,28:177,29:356,30:434,31:410,32:167,33:154,34:218,35:152,36:430,37:196,38:542,39:2,40:144,41:178,42:107,43:156,44:113,45:139,46:414,47:351,48:200,49:198,50:161,51:207,52:145,54:92,55:211,56:45,57:223,58:205,59:214,60:484,61:206,62:26,63:37,64:158,65:506,66:369,67:220,68:225,69:201,70:137,71:117,72:164,73:83,74:182,75:212,76:216,78:40,79:46,80:53,81:238,82:235,83:252,84:251,85:247,86:258,87:249,88:244,89:56,90:61,91:301,92:294,93:287,95:68,96:316}
# waves that crossed borders: (key, EN, NL, note EN, note NL, event ids)
CAMP=[
('freezer','The freezer wave, Oct–Nov 2026','De diepvriesgolf, okt–nov 2026','Reports say the same kind of refrigeration controller was attacked in many countries, including the cold rooms of the French blood service on the same night as the Belgian shops. France says Iran is behind its own wave: that is the French claim, not proven here. Other countries have named nobody, and no authority has said that all of these are one attack.','Volgens meldingen werd in veel landen hetzelfde soort koelregelaar aangevallen, ook de koelcellen van de Franse bloeddienst, in dezelfde nacht als de Belgische winkels. Frankrijk zegt dat Iran achter zijn eigen golf zit: dat is de Franse bewering, hier niet bewezen. Andere landen noemen niemand, en geen enkele overheid heeft gezegd dat dit alles één aanval is.',[133,542,543,544,545,546,547,538,539,521,1001]),
('collins','Airport check-in supplier, Sep 2025','Leverancier van check-in aan luchthavens, sep 2025','According to the reports, one ransomware attack (criminals lock the data and demand money) on one supplier, Collins Aerospace, hit several airports at once.','Volgens de berichten trof één ransomware-aanval (criminelen zetten gegevens op slot en vragen geld) bij één leverancier, Collins Aerospace, meerdere luchthavens tegelijk.',[26,210,213]),
('hoax','Hoax bomb threats, Nov 2026','Valse bommeldingen, nov 2026','A Europe-wide wave of false threats against flights and schools. Nobody has been named.','Een Europese golf van valse dreigingen tegen vluchten en scholen. Niemand is aangewezen.',[37,116,134,148]),
('cables','Baltic cable damage, 2025–2026','Kabelschade in de Oostzee, 2025–2026','A series of damaged cables. One case ended in prison sentences, one was ruled an accident, others have no outcome.','Een reeks beschadigde kabels. Eén zaak eindigde met celstraffen, één bleek een ongeval, andere hebben geen uitkomst.',[83,84,86,87]),
('dronealarm','Drone alarms at airports and bases, Sep–Dec 2025','Dronealarmen bij luchthavens en bases, sep–dec 2025','Reports that followed each other across Europe. No link between them is proven, and several ended with no proof of a drone.','Meldingen die elkaar in Europa opvolgden. Een verband is niet bewezen, en meerdere eindigden zonder bewijs van een drone.',[117,118,135,164,0,2,3,5,6,161,188,144]),
('storm','Fake election videos (Storm-1516)','Valse verkiezingsvideo\'s (Storm-1516)','Fake videos that researchers link to one Russian operation, seen in several elections.','Valse video\'s die onderzoekers linken aan één Russische operatie, gezien bij meerdere verkiezingen.',[238,240,243]),
('leipzig','Leipzig drone and the linked arson plots, 2026','Drone in Leipzig en de gelinkte brandstichtingen, 2026','German investigators were reported to link the Leipzig drone and the foiled Skyeton arson. The link is reported, not proven in court.','Duitse speurders zouden de drone in Leipzig en de verijdelde brand bij Skyeton linken. Dat verband is gemeld, niet bewezen voor een rechter.',[138,180]),
]

CASE[99]=1000
LY.update({1000:['sabotage','defence'],1001:['health','food']})
PL.update({1000:'',1001:''})
