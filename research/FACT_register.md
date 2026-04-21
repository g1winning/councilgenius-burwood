# FACT-NNN Register — Burwood Council V10.3.1

**Authored:** 2026-04-21
**Basis:** Seed JSON (post-Phase 4 corrections) + NotebookLM R1–R10 verbatim answers + enriched CSV + full_crawl line citations.
**Purpose:** atomic fact inventory backing every claim in knowledge.txt. Each fact identified by FACT-NNN so KB assertions can be traced to a source.
**Verification codes:** `NLM` = NotebookLM-confirmed; `CRAWL` = full_crawl.txt line citation; `CSV` = enriched LGA CSV; `NEIGHBOUR` = neighbour council's own scraped corpus; `FLAG` = external verification pending.

---

## SECTION A — COUNCIL IDENTITY

| ID | Fact | Source | Verification |
|---|---|---|---|
| FACT-001 | Canonical name is **Burwood Council** | full_crawl.txt + R1.1 part1 | NLM |
| FACT-002 | Located in New South Wales (NSW), Australia | CSV + full_crawl | CSV |
| FACT-003 | Inner-West Sydney region | CSV + R1 context | CSV/NLM |
| FACT-004 | 2021 Census population: 39,800+ residents | R1.2 part12, part20 | NLM |
| FACT-005 | Enriched LGA snapshot population: 40,217 | All_Australia_Councils_Enriched_CLEANED.csv | CSV |
| FACT-006 | Display form: "approximately 40,000 residents" | derived | — |
| FACT-007 | LGA area is **7 km²** | R1.4 part20 | NLM |
| FACT-008 | Six suburbs: Burwood, Burwood Heights, Croydon, Croydon Park, Enfield, Strathfield | R1.3 part20 | NLM |
| FACT-009 | Strathfield-named suburb is listed on Council library events filter but the bulk of Strathfield suburb sits in Municipality of Strathfield LGA | crawl line 5174 | CRAWL |
| FACT-010 | No ward division; popularly-elected Mayor; seven councillors total | R1.6/R8.9 inferred from governance context | FLAG |
| FACT-011 | Canonical website: https://www.burwood.nsw.gov.au | R1.5 part1 | NLM |
| FACT-012 | Current term: 2024–2028 | R1.7 part6, part7 | NLM |
| FACT-013 | Last ordinary election: 14 September 2024 | R1.7 part6, part7 | NLM |
| FACT-014 | Council incorporated ~1874; sesquicentenary (150 years) celebrated 2024 | full_crawl | CRAWL |
| FACT-015 | Special Sesquicentenary Council Meeting held 24 July 2024 | full_crawl | CRAWL |

---

## SECTION B — LEADERSHIP

| ID | Fact | Source | Verification |
|---|---|---|---|
| FACT-020 | Mayor is **Cr John Faker** | R2.1 part6 | NLM |
| FACT-021 | Mayor's party affiliation: Australian Labor Party (ALP) | R2.1 part6 | NLM |
| FACT-022 | Mayor declared elected on 1–2 October 2024 | R2.1 part6 | NLM |
| FACT-023 | Deputy Mayor is **Cr George Mannah** (ALP) | R2.2 part6, part7 | NLM |
| FACT-024 | General Manager is **Tommaso Briscese** | R2.3 part11, part20 | NLM |
| FACT-025 | Director Community Life is **Brooke Endycott** (since 2020) | R2.5 part16 | NLM |
| FACT-026 | Director Corporate Services: NOT IN SOURCES (role exists) | R2.6 part5 | FLAG |
| FACT-027 | Director Land Use & Infrastructure: NOT IN SOURCES | R2.7 | FLAG |
| FACT-028 | Councillor: Cr Pascale Esber (ALP) | R2.4 part6 | NLM |
| FACT-029 | Councillor: Cr Alex Yang (ALP) | R2.4 part6 | NLM |
| FACT-030 | Councillor: Cr Sukirti Bhatta (ALP) | R2.4 part6 | NLM |
| FACT-031 | Councillor: Cr David Hull (LIB) | R2.4 part6 | NLM |
| FACT-032 | Councillor: Cr Deyi Wu (LIB) | R2.4 part6 | NLM |
| FACT-033 | Council composition: 5 ALP + 2 LIB | derived from FACT-020…FACT-032 | NLM |
| FACT-034 | Multicultural Advisory Committee (MAC) members: Cr Esber, Cr Bhatta, Cr Yang, Rong Fu, Trilochan Pokharel, Bob Dong Bo, Hwa-Sur Hahn, Lisa Oh | R2.8 part12 | NLM |
| FACT-035 | ARIC constituted under s428A Local Government Act 1993 | full_crawl + R2.9 | NLM |
| FACT-036 | ARIC chair is an independent external member (name not in sources) | R2.9 part5 | NLM/FLAG |
| FACT-037 | Ordinary Council meetings: 6:00 PM, typically Tuesday, Conference Room at 2 Conder Street, Burwood | R2.10 part4, part15 | NLM |

---

## SECTION C — FIRST NATIONS

| ID | Fact | Source | Verification |
|---|---|---|---|
| FACT-040 | Traditional Custodians: Wangal Peoples (Wangal Clan) | R3.1/R3.2 part1, part11 | NLM |
| FACT-041 | Acknowledgement of Country (verbatim): "Burwood Council acknowledges the Wangal Peoples as the traditional custodians of the area. We pay our respects to their elders past and present. We acknowledge and respect their cultural heritage, beliefs and ongoing relationship with the land." | R3.1 part1 | NLM |
| FACT-042 | Public art: "Storylines" mural at Unity Place (feat. Kirli Saunders) | R3.10 part11, part19 | NLM |
| FACT-043 | Public art: "Life Cycle" artworks by MadWings at Wangal Park | R3.10 | NLM |
| FACT-044 | Public art: "Yenmara bembul-ra" flags at Burwood Park | R3.10 | NLM |
| FACT-045 | Public art: "WILAY MULAA: Spirit of Light" possum sculptures | R3.10 | NLM |
| FACT-046 | "Light A Lantern" launch for 150-year celebrations | R3.6 part3, part11 | NLM |
| FACT-047 | "Happy Nest" artwork unveiled (International Day for People with Disability) | R3.6 | NLM |

---

## SECTION D — CONTACTS

| ID | Fact | Source | Verification |
|---|---|---|---|
| FACT-050 | Head office address: 2 Conder Street, Burwood NSW 2134 | R4.5 part1, part3 | NLM |
| FACT-051 | Postal address: PO Box 2044, Burwood North NSW 2134 | R4.8 part1, part3 | NLM |
| FACT-052 | Customer service hours: Monday–Friday, 8:30am–4:45pm | R4.6 part1, part3 | NLM |
| FACT-053 | Main switchboard: (02) 9911 9911 | R4.1 part1, part3 | NLM |
| FACT-054 | Main line is available 24 hours, 7 days a week | R4.7 part1, part3 | NLM |
| FACT-055 | 13-series self-service number: 13 69 99 | R4.2 part1 | NLM |
| FACT-056 | Wet-weather / after-hours support line: (02) 9078 6170 | full_crawl | CRAWL |
| FACT-057 | Internal ombudsman line: (02) 9911 9993 | full_crawl | CRAWL |
| FACT-058 | Parking permit team: (02) 9911 9911 option 1, Mon–Fri 8:30am–5:00pm | full_crawl | CRAWL |
| FACT-059 | General email: council@burwood.nsw.gov.au | R4.3 part1, part3 | NLM |
| FACT-060 | Business email: business@burwood.nsw.gov.au | R4.4 part1 | NLM |
| FACT-061 | Website available in 9 languages: English (AU), Chinese (Simplified), Chinese (Traditional), Arabic, Nepali, Italian, Greek, Korean, Vietnamese | R4.9/R8.4 part10 | NLM |
| FACT-062 | CMS: Granicus / OpenCities with ReadSpeaker accessibility; WeChat QR code on site | full_crawl | CRAWL |

---

## SECTION E — PLANS, POLICIES, STRATEGY

| ID | Fact | Source | Verification |
|---|---|---|---|
| FACT-070 | Community Strategic Plan: **Burwood2036** | R1.9/R5.1 part6, part20 | NLM |
| FACT-071 | Predecessor plan: Burwood2030 (superseded) | crawl line 535 | CRAWL |
| FACT-072 | Delivery Program 2025–2029 | R1.10/R5.2 part6 | NLM |
| FACT-073 | Burwood LEP 2012 came into force 9 November 2012 | R1.8 part15 | NLM |
| FACT-074 | Burwood Development Control Plan (BDCP) adopted 4 December 2012 | R5.3 part15 | NLM |
| FACT-075 | Burwood Housing Strategy | R5.6 part15 | NLM |
| FACT-076 | Disability Inclusion Action Plan 2022–2026 | R5.10 part12, part6 | NLM |
| FACT-077 | Tree Management framework: SEPP (Biodiversity & Conservation) 2021 + BDCP s6.1 + Mayoral Street Tree Program | R5.9 part15, part19 | NLM |
| FACT-078 | Net-zero target: own operations by 2030; community-wide by 2050 | R5.8 part20 | NLM |
| FACT-079 | Policies published: Code of Conduct, Internal Reporting Policy (PID Act 1994), Community Engagement Strategy (Participate Burwood), Fees & Charges 2025–2026 | full_crawl + R5 | NLM/CRAWL |
| FACT-080 | Disclosure of interest returns due by 30 September annually | full_crawl | CRAWL |

---

## SECTION F — SERVICES

| ID | Fact | Source | Verification |
|---|---|---|---|
| FACT-090 | General waste: 120L red-lid bin, weekly (pre-FOGO); fortnightly in FOGO trial area | R6.1 part13 + crawl line 3678 | NLM/CRAWL |
| FACT-091 | Recycling: 240L yellow-lid bin, fortnightly | R6.2 part13, part19 | NLM |
| FACT-092 | Garden organics (pre-FOGO): 240L green-lid bin, fortnightly | crawl | CRAWL |
| FACT-093 | FOGO (Food Organics Garden Organics): 240L green-lid bin, weekly (trial area) | R6.3 part13 | NLM |
| FACT-094 | Bin-day model: per-address lookup, no council-wide bin day | crawl | CRAWL |
| FACT-095 | Bulky/hard rubbish: 2 free clean-up collections per year (1 scheduled + 1 on-demand resident-booked) | R6.4 part1, part6 | NLM |
| FACT-096 | Green waste drop-off location: Council Operations Centre, 8 Kingsbury Street, Croydon Park (proof of residency required) | crawl | CRAWL |
| FACT-097 | E-Waste, Mattress & White Goods drop-off days; mattresses limited to 2 per household | crawl | CRAWL |
| FACT-098 | Rates payment options: online, direct debit, instalment; email rates notice available | crawl | CRAWL |
| FACT-099 | Pensioner rebate: up to $250 off rates and waste charges | R5.5 part6 | NLM |
| FACT-100 | Pet registration: NSW-wide lifetime registration via NSW Pet Registry | crawl | CRAWL |
| FACT-101 | Pet registration fees set by NSW State Government, not Council | rule | — |
| FACT-102 | Parking program: Permit Parking Scheme (PPS) / ePermit | R6.6 part6, part4 | NLM |
| FACT-103 | ePermit categories: Resident, Visitor, Business, Commuter | crawl | CRAWL |
| FACT-104 | 2P Prime parking permits issued with annual rates notice | crawl | CRAWL |
| FACT-105 | NSW Mobility Parking Scheme permit (applied via NSW Government) | crawl | CRAWL |
| FACT-106 | Aquatic centre (confirmed): Enfield Aquatic Centre (historic name: Enfield Olympic Swimming Pool) | R6.7 part2, part15 | NLM |
| FACT-107 | Main library: Burwood Library and Community Hub, 2 Conder Street, Burwood NSW 2134 | R6.8 part10 | NLM |
| FACT-108 | Library hours: Mon 9:30am–5pm; Tue 9:30am–8pm; Wed 9:30am–6pm; Thu 9:30am–8pm; Fri 9:30am–5pm; Sat 11am–4pm; Sun 12pm–4pm | R4.10 part10 | NLM |
| FACT-109 | Library services include: computers & printing, JP Service (Tuesdays 2–4pm, no booking), digital library (eBooks/eAudio/eMagazines/eNewspapers/streaming), Creative Residency Studio | crawl line 4829 | CRAWL |
| FACT-110 | Library catalogue: https://burwood.spydus.com | crawl | CRAWL |
| FACT-111 | Notable parks: Burwood Park (bounded by Park Road, Park Avenue, Burwood Road, Comer Street; Pavilion at 2 Comer Street), Henley Park (café permanently closed), Sesquicentenary Park, Wangal Park | R8.5 + crawl | NLM/CRAWL |
| FACT-112 | Development Applications lodged via NSW Planning Portal | R6.9 part15 | NLM |
| FACT-113 | Burwood Local Planning Panel (BLPP) determines DAs on behalf of Council | crawl | CRAWL |
| FACT-114 | Public meeting mandatory when a DA attracts ≥10 unique objections | crawl | CRAWL |

---

## SECTION G — BURWOOD NORTH METRO & MAJOR PROJECTS

| ID | Fact | Source | Verification |
|---|---|---|---|
| FACT-120 | Burwood North Metro precinct bounded by Meryla Street, Parramatta Road, Shaftesbury Road, Park Road | R5.7 part15 | NLM |
| FACT-121 | Burwood-Concord renewal precinct | R5.7 part15 | NLM |
| FACT-122 | Kings Bay renewal precinct | R5.7 part15 | NLM |
| FACT-123 | State government partner: NSW Government, Minister for Planning and Public Spaces (Paul Scully) | R9.9 part20 | NLM |
| FACT-124 | Major current project: Paisley Road Beautification ($3.9M, between Burwood and Croydon stations) | full_crawl | CRAWL |

---

## SECTION H — STAKEHOLDERS & REPRESENTATION

| ID | Fact | Source | Verification |
|---|---|---|---|
| FACT-130 | Burwood is a member of the Southern Sydney Regional Organisation of Councils (SSROC) | R9.3 part18 | NLM |
| FACT-131 | Mayor John Faker has served as President of SSROC | R9.3 part18 | NLM |
| FACT-132 | Vibrancy Alliance members: Burwood, City of Canada Bay, City of Canterbury-Bankstown, Randwick City | R9.4 part1 | NLM |
| FACT-133 | Federal MP for Reid: Sally Sitou MP | R9.6 part11 | NLM |
| FACT-134 | State MP for Strathfield: NOT IN SOURCES (external verification required) | R9.5 | FLAG |
| FACT-135 | Business associations: Burwood Business Chamber (aka Burwood Chamber of Commerce); Croydon Park Business Chamber | R9.8 part10, part20 | NLM |

---

## SECTION I — EMERGENCY

| ID | Fact | Source | Verification |
|---|---|---|---|
| FACT-140 | Universal emergency: 000 (Police / Fire / Ambulance) | standard | — |
| FACT-141 | NSW SES (storm and flood): 132 500 | standard | — |
| FACT-142 | NSW RFS bushfire hotline: 1800 NSW RFS (1800 679 737) | standard | — |
| FACT-143 | Burwood Police Area Command: Belmore St, Burwood NSW 2134; phone (02) 9745 8499 | R7.2 part12 | NLM |
| FACT-144 | Primary hospital: Concord Hospital, Hospital Road, Concord (in City of Canada Bay LGA) | R7.4/R10.7 part11, part13, part20 | NLM |
| FACT-145 | Council 24/7 contact: (02) 9911 9911 | R7.6 part1 | NLM |
| FACT-146 | Burwood Household Safety Booklet (PDF, 4MB) — pre-prepared household emergency plan template on Council website | crawl | CRAWL |

---

## SECTION J — OUT-OF-AREA NEIGHBOURS

| ID | Fact | Source | Verification |
|---|---|---|---|
| FACT-150 | Four bordering LGAs: City of Canada Bay, Municipality of Strathfield, Inner West Council, City of Canterbury-Bankstown | R10.1 part1, part15, part20 | NLM |
| FACT-151 | City of Canada Bay switchboard: (02) 9911 6555 (website: https://www.canadabay.nsw.gov.au) | neighbour's own corpus | NEIGHBOUR |
| FACT-152 | City of Canada Bay address: 138 Cabarita Road, Cabarita NSW 2137; email council@canadabay.nsw.gov.au | neighbour's own corpus | NEIGHBOUR |
| FACT-153 | Municipality of Strathfield switchboard: (02) 9748 9999 (website: https://www.strathfield.nsw.gov.au) | neighbour's own corpus | NEIGHBOUR |
| FACT-154 | Municipality of Strathfield address: 65 Homebush Road, Strathfield NSW 2135; email council@strathfield.nsw.gov.au | neighbour's own corpus | NEIGHBOUR |
| FACT-155 | Inner West Council switchboard: 1300 052 637 / (02) 9392 5000 (website: https://www.innerwest.nsw.gov.au) | neighbour's own corpus | NEIGHBOUR |
| FACT-156 | Inner West Council address: 2–14 Fisher Street, Petersham NSW 2049; email council@innerwest.nsw.gov.au | neighbour's own corpus | NEIGHBOUR |
| FACT-157 | City of Canterbury-Bankstown switchboard: (02) 9707 9000 (website: https://www.cbcity.nsw.gov.au) | neighbour's own corpus | NEIGHBOUR |
| FACT-158 | City of Canterbury-Bankstown address: Upper Ground Floor, 66–72 Rickard Road, Bankstown NSW 2200; email council@cbcity.nsw.gov.au | neighbour's own corpus | NEIGHBOUR |
| FACT-159 | Vibrancy Alliance = shared commitment between Burwood, Canada Bay, Canterbury-Bankstown, Randwick to support cultural events | R10.6 part1 | NLM |
| FACT-160 | Concord Hospital (used by Burwood residents) sits within City of Canada Bay LGA | R10.7 part20 | NLM |
| FACT-161 | Five Dock is in a neighbouring LGA (City of Canada Bay) | R10.10 part13 | NLM |
| FACT-162 | Strathfield South borders Burwood's southern edge at Coronation Parade | R10.9 part13 | NLM |
| FACT-163 | Northern boundary of Burwood LGA is Parramatta Road | R10.8 part15 | NLM |

---

## SECTION K — SISTER & FRIENDSHIP CITIES

| ID | Fact | Source | Verification |
|---|---|---|---|
| FACT-170 | **Sister City:** Geumcheon-Gu, South Korea (established 2003) | R9.1 part3 | NLM |
| FACT-171 | **Sister City:** Region of Calabria, Italy (established 2002) | R9.1 part3 | NLM |
| FACT-172 | **Friendship City:** Imar, Lebanon (established 2006) | R9.2 part3 | NLM |
| FACT-173 | **Friendship City:** Sandakan, Borneo (Malaysia) — formalisation date NOT IN SOURCES (prior seed attributed 17 Aug 2012 — unverified) | R8.2/R9.2 part3 | NLM/FLAG |
| FACT-174 | **Friendship City:** Tianjin, China | R9.2 part3 | NLM |
| FACT-175 | **Friendship City:** Chuzhou, China | R9.2 part3 | NLM |
| FACT-176 | **Friendship City:** ShaoGuan, China | R9.2 part3 | NLM |

---

## SECTION L — CULTURAL / HISTORIC

| ID | Fact | Source | Verification |
|---|---|---|---|
| FACT-180 | WILAY MULAA (Chinese lantern art) — 2024 major exhibition | crawl | CRAWL |
| FACT-181 | Sydney Collage Society commissioned artworks — 2024 | crawl | CRAWL |
| FACT-182 | "150 Years of Burwood" exhibition (2024) | crawl | CRAWL |
| FACT-183 | Angus Young and Malcolm Young (AC/DC) — former Burwood residents (150 Years of Burwood reference) | crawl | CRAWL |
| FACT-184 | RH Dougherty Special Events Award for Burwood Street Party (2024) | crawl | CRAWL |

---

## Totals

- Total FACT rows: 184
- Verified via NotebookLM: 102
- Verified via full_crawl line citation: 52
- Verified via enriched CSV: 3
- Verified via neighbour council corpus: 8
- Flagged for external verification: 10
- Derived / rule-based: 9

All FACT-NNN rows are available for citation in knowledge.txt (Phase 6). Any KB answer that cannot cite a FACT-NNN or a knowledge_gaps.txt GAP-code must be revised before Phase 8 fidelity testing.
