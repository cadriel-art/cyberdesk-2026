# Cyber Attacks 2026

A bilingual (English / Dutch) single-file app about cyberattacks and hybrid threats in the 27 EU countries plus Norway, Iceland, Switzerland and Liechtenstein, 2025–2026 (the UK and Ukraine are left out). Belgium comes first.

House rules for all content:

- Facts only, nothing invented.
- Every claim is marked **Confirmed / Reported / Claimed / Suspected / Not proven**.
- Blame is never stated as fact: the text says who says it.
- Plain language for a general audience, in English and Dutch.
- Every source is registered on the Sources page, sorted by type.

## What is where

| Path | What it is |
|---|---|
| `app/Cyber-Attacks-2026.html` | The saved file: open it in a browser. Works without claude.ai; the News reader shows the news as of the last build plus live headlines from 7 feeds. |
| `app/Cyber-Attacks-2026-online.html` | The version published on claude.ai (private artifact). Its News reader reads the live news database and has the "Fetch today's news" button. |
| `build/` | Everything needed to rebuild: the build scripts, page scripts, data files and research data. |
| `build/research/` | Fact-checked research files used to make the outages, stock-up and November news pages. |

## Rebuilding

**Note:** some build inputs come from other projects and are deliberately not in this repository: the folder `build/tools/`, two source HTML files in `build/`, `build/mine/tools/make_mine.py` and the PDF. They are kept locally next to the repository (listed in `.gitignore`). Without them, `build_all.sh` cannot run; the finished app in `app/` and all page scripts and data are complete here.

The repository is the working folder: all scripts use the path `/home/user/cyberdesk-2026/build/`. Clone it to `/home/user/cyberdesk-2026` (the default place in a Claude cloud session). On another machine, either clone it to that same path or replace that path in the scripts (one search-and-replace over `build/`).

```bash
build/mine/tools/build_all.sh
```

Requirements: Python 3 with BeautifulSoup (`bs4`), Node.js with Playwright and Chromium (for the tests and the PDF).

The build writes `build/mine/cyber-desk.html` (online version) and `build/mine/cyber-desk-offline.html` (saved file), and copies them into `app/` as `Cyber-Attacks-2026-online.html` and `Cyber-Attacks-2026.html`. The PDF is made from `build/mine/tools/` with `node pdf.js` and lands in `app/`.

Tests (run from `build/mine/tools/`):

```bash
node fx_check3.js cyber-desk-offline.html
```

Other checks in the same folder: `ovtest.js`, `otest.js`, `preptest.js`, `newsbtn.js`, `livetest.js`.

The build order is in `build/mine/tools/build_all.sh`.

Before a build, refresh `build/mine/tools/news_snapshot.json` from the live news database (dump the `news` collection, then run `python3 build/mine/tools/snap_from_dump.py <dump>/news`), so the saved file carries the latest news.

## Live parts (not in this repository)

- **Published app**: a private claude.ai artifact. Its database holds two collections, `updates` (the Updates panel) and `news` (the News reader).
- **Daily news task**: a scheduled Claude task runs every morning at 06:47 Brussels time. It reads the working feeds listed in `build/mine/tools/news_feeds.json` and adds checked items to the `news` collection. The "Fetch today's news" button in the online app starts the same task on demand.
