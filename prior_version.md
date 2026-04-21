# Phase 1.5 — Prior-version discovery

**Council:** Burwood Council (NSW)
**Run date:** 2026-04-21
**Skill version:** V10.3.1
**Search scope:** current working folder only (CG_INDEX §4.1–§4.3 + root). No online lookups.

## Result

| Field | Value |
|---|---|
| Prior build found? | **no** |
| Prior version | n/a |
| Prior KB path | n/a |
| Prior KB line count | n/a |
| Prior page.html path | n/a |
| Prior brand tokens | n/a — to be derived fresh in Phase 7 from scraped homepage snapshot (`full_crawl.txt`) and visible live-site styling |
| Prior deployed URL | n/a — Burwood has never been deployed as a CouncilGenius product |
| Prior research artefacts | n/a |

## Searches performed

1. `COUNCIL GENIUS BEHEMOTH/BUILD EVERY CG/` (V9 fleet) — no match
2. `COUNCIL GENIUS BEHEMOTH/COUNCILS BUILT PRE 13Apr/**/*burwood*` — no match
3. `scraper steup/**/*burwood*` — no match
4. Workspace-wide `find … -iname "*burwood*"` — only matches are this V10.3.1 build's own scaffold + the NSW corpus folder itself
5. Any `knowledge.txt` with `burwood` in the path — none

## Consequences for this build

- **Phase 6.5 (cross-version KB diff) — SKIPPED.** Recorded in BUILD_REPORT.md §4.
- **Phase 7 brand inheritance rule — N/A.** No prior `page.html` to inherit from. Brand tokens will be derived from Burwood's live visual identity as represented in `full_crawl.txt` homepage snapshot (masthead colour, footer acknowledgement text, typography). Default to generic V10 chrome only where the council's own signals are silent.
- **Phase 9 deployed URL preservation — N/A.** This will be a brand-new Railway URL. User will nominate/approve.

## Note

Burwood's inner-west Sydney footprint (next to City of Canada Bay, Strathfield, Inner West, Canterbury-Bankstown) means OUT-OF-AREA routing in Phase 6 §9 and Phase 7 server prompt must list those four neighbours with current phone + URL. Phone numbers for neighbours will be independently verified against each neighbour's own scraped corpus (all four are in `COUNCIL_GENIUS_V10/NSW/`) before being written into the KB — no carry-over phones without verification, per V10.1 retained rule.
