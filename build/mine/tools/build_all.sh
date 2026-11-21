#!/bin/bash
# Full rebuild of Cyber Attacks 2026 (run from anywhere)
cd "$(dirname "$0")/.." || exit 1
python3 tools/make_mine.py && python3 tools/year2026.py; python3 tools/nav2026.py
for s in hybrid hybrid2 water water2 transport transport2 elections elections2 health health2 defence defence2 encryption encryption2 skills insurance cables schools evidence house map news intel outages prepare fold; do python3 tools/$s.py || echo "FAIL $s"; done
python3 tools/sources2.py && python3 tools/print2.py && python3 tools/build_app.py && python3 tools/offline.py && python3 tools/offpatch.py
python3 tools/urlfix.py
# copy the results into the repository's app/ folder
cp cyber-desk-offline.html ../../app/Cyber-Attacks-2026.html && cp cyber-desk.html ../../app/Cyber-Attacks-2026-online.html && echo "copied to app/"
