# Burwood Council V10.3.1 — R1-R10 Research Matrix (100 Questions)

**Council:** Burwood Council (NSW)
**Build version:** V10.3.1
**Generated:** 2026-04-21
**Purpose:** Phase 3 research matrix per COUNCILGENIUS_SKILL_V10.md §Phase 3.
**Use:** All 100 questions will be submitted in Phase 3.5 as a block-query against Burwood NotebookLM notebook (seeded with full_crawl.txt + notebooklm/ part files 1-20 + pdf corpus). Answers feed Phase 4 cross-reference audit + Phase 6 knowledge.txt.
**Baseline answers column:** derived from full_crawl.txt grep passes during Phase 3. "GAP" = flag for Phase 3.5 NotebookLM or Phase 4.5 knowledge_gaps.txt.

---

## R1 — Council, Councillors, Governance

| # | Question | Baseline answer from full_crawl.txt | Status |
|---|---|---|---|
| R1.1 | Who is the Mayor of Burwood Council? | Cr John Faker | MATCH |
| R1.2 | Who is the Deputy Mayor? | Cr George Mannah | MATCH |
| R1.3 | List all current councillors with their first and last names. | Faker, Mannah, Esber, Yang, Bhatta, Hull, Wu-Coshott | PARTIAL — need full first names |
| R1.4 | How many councillors does Burwood have, and are they ward-elected or at-large? | 7 councillors total; at-large (no wards); popularly-elected Mayor | MATCH |
| R1.5 | When is the current Council term — start and end dates? | Sep 2024 to Sep 2028 (NSW LGA election cycle) | GAP — verify |
| R1.6 | What is the Mayor's term — 1 year, 2 years, or full 4-year term? | Popularly elected — 4-year Mayoral term (NSW s230 LGA option) | GAP — verify |
| R1.7 | Where and when are ordinary Council meetings held? Are they livestreamed? | Council Chambers, 2 Conder Street; livestream implied from webcast references | GAP — confirm schedule |
| R1.8 | What is the Council Chamber address and meeting frequency? | 2 Conder Street, Burwood — monthly (NSW standard) | PARTIAL |
| R1.9 | Does Burwood Council have any declared divisions or conflicts-of-interest in the current term? | Annual disclosure returns due 30 Sep; published on website | GAP — specific declarations |
| R1.10 | Which portfolios do individual councillors hold? | Not specified in scraped corpus | GAP |

---

## R2 — Executive / Administration

| # | Question | Baseline answer | Status |
|---|---|---|---|
| R2.1 | Who is the General Manager? | Tommaso Briscese | MATCH |
| R2.2 | When was the GM appointed? | Not in corpus | GAP |
| R2.3 | List the Directors / executive team (Corporate, Planning, Community, Operations, etc.) | Not consolidated in corpus | GAP |
| R2.4 | What is the total FTE of Council staff? | Not in corpus | GAP — Annual Report |
| R2.5 | What are Customer Service Centre opening hours? | Mon-Fri 8:30am - 4:45pm | MATCH |
| R2.6 | What are the primary contact phone numbers and their purposes? | (02) 9911 9911 main; (02) 9078 6170 wet weather; 13 69 99 self-serve; (02) 9911 9993 internal ombudsman | MATCH |
| R2.7 | What is Council's physical address and postal address? | 2 Conder Street Burwood NSW 2134 / PO Box 2044 Burwood North NSW 2134 | MATCH |
| R2.8 | What is Council's general email? | council@burwood.nsw.gov.au | MATCH |
| R2.9 | Is there a dedicated business email? | business@burwood.nsw.gov.au | MATCH |
| R2.10 | What languages is Council's website available in? | 8 languages incl. WeChat QR code | PARTIAL — need list |

---

## R3 — Plans, Policies, Strategy

| # | Question | Baseline answer | Status |
|---|---|---|---|
| R3.1 | Name the current Community Strategic Plan and its time horizon. | Burwood2036 (10 years) | MATCH |
| R3.2 | When was Burwood2036 adopted? | 2024-25 cycle — verify exact date | PARTIAL |
| R3.3 | What is the current Delivery Program name and years? | Delivery Program 2024-28 (standard NSW 4-year) | GAP — verify |
| R3.4 | Name the current Operational Plan and financial year. | Operational Plan 2025-26 (FY25-26) | GAP — verify |
| R3.5 | What is the Resourcing Strategy composed of? | Long Term Financial Plan + Workforce Management Strategy + Asset Management Strategy (NSW IP&R standard) | GAP — verify documents list |
| R3.6 | What is the name of Council's Local Environmental Plan? | Burwood LEP | PARTIAL — year? |
| R3.7 | What is the name of Council's Development Control Plan? | Burwood Development Control Plan (BDCP) | MATCH |
| R3.8 | What is Council's community engagement platform name? | Participate Burwood | MATCH |
| R3.9 | Does Council have a Reconciliation Action Plan (RAP)? | Not in corpus | GAP |
| R3.10 | Does Council have a Disability Inclusion Action Plan (DIAP)? | Multicultural Advisory Committee referenced; DIAP to verify | GAP |

---

## R4 — Economy, Business, Planning

| # | Question | Baseline answer | Status |
|---|---|---|---|
| R4.1 | What are the top industries in Burwood by employment? | Retail/hospitality dominant (Westfield Burwood); property services; education — to confirm | GAP |
| R4.2 | How many local businesses operate in the Burwood LGA? | Not in corpus | GAP |
| R4.3 | Who is Council's largest commercial ratepayer? | Not published | GAP |
| R4.4 | What is the annual economic development budget? | Not in corpus | GAP |
| R4.5 | Where is the main commercial precinct? | Burwood Road CBD + Westfield Burwood | MATCH |
| R4.6 | What development application lodgement volume occurs annually? | Not in corpus | GAP |
| R4.7 | What is the DA average determination time? | Not in corpus | GAP |
| R4.8 | How do I lodge a DA? | NSW Planning Portal + Council; BLPP determines | MATCH |
| R4.9 | When does the BLPP hold a public meeting? | Only when DA attracts 10 or more unique objections | MATCH |
| R4.10 | Are there current Planning Proposals on exhibition? | Register of variations to development standards published | PARTIAL |

---

## R5 — Environment, Sustainability

| # | Question | Baseline answer | Status |
|---|---|---|---|
| R5.1 | Has Council declared a climate emergency? | Not in corpus | GAP |
| R5.2 | What is the net-zero target year? | Not in corpus | GAP |
| R5.3 | What is the tree canopy target? | BDCP s6.1 protects trees; numeric canopy target not in corpus | GAP |
| R5.4 | Does Council run a Greening Burwood or equivalent program? | Not explicitly named | GAP |
| R5.5 | What is the e-waste policy? | E-Waste, Mattress and White Goods drop-off days; Council Operations Centre 8 Kingsbury St Croydon Park | MATCH |
| R5.6 | What catchment/waterways are in the LGA? | Iron Cove / Parramatta River catchment — to verify | GAP |
| R5.7 | Does Council have a Biodiversity Strategy? | Not in corpus | GAP |
| R5.8 | What is the FOGO service status? | No FOGO — separate garden-organics green bin fortnightly (not combined food+garden) | PARTIAL |
| R5.9 | What community environmental programs run? | Not consolidated | GAP |
| R5.10 | Who collects Burwood's recycling? | Not named in corpus (likely commercial contractor) | GAP |

---

## R6 — Residents — Rates, Bins, Pets, Parking, Planning

| # | Question | Baseline answer | Status |
|---|---|---|---|
| R6.1 | When is my bin day? | Per-address lookup tool on Council website; no single council-wide day | MATCH |
| R6.2 | What bins does a single dwelling receive? | 120L red weekly + 240L yellow fortnightly + 240L green fortnightly | MATCH |
| R6.3 | How do I pay my rates? | Online portal; direct debit; instalment; email rates notice option | MATCH |
| R6.4 | What is the pensioner rebate? | Up to $250 off rates + waste charges for eligible pensioners | MATCH |
| R6.5 | How do I register my pet in NSW? | NSW Pet Registry — lifetime registration (one-off). Additional annual permits apply for restricted/dangerous dogs and non-desexed cats >4mo | MATCH |
| R6.6 | How much does pet registration cost? | Fees set by NSW State Government via NSW Pet Registry; not quoted by Council | MATCH (deliberate) |
| R6.7 | How do I get a parking permit? | ePermit online system; Resident/Visitor/Business/Commuter categories; digital, vehicle-reg linked | MATCH |
| R6.8 | What is 2P Prime? | Residential parking permit replaced annually with rates notice | MATCH |
| R6.9 | How do I lodge a DA? | Via NSW Planning Portal to Council; BLPP determination | MATCH |
| R6.10 | How do I request a tree removal? | BDCP s6.1 Tree Preservation — exemptions listed; otherwise permission required | MATCH |

---

## R7 — Relief, Emergency, Resilience

| # | Question | Baseline answer | Status |
|---|---|---|---|
| R7.1 | What number do I call in a life-threatening emergency? | 000 | MATCH |
| R7.2 | What number is NSW SES for storm/flood? | 132 500 | MATCH |
| R7.3 | Which fire service covers Burwood? | Fire and Rescue NSW (urban); NSW RFS at rural fringes | PARTIAL |
| R7.4 | Where are Burwood's designated evacuation centres? | Not in corpus | GAP — NSW Reconstruction Authority registry |
| R7.5 | Does Council run a community resilience program? | Household Safety Booklet PDF available; MAC references community safety | PARTIAL |
| R7.6 | What is the Disaster Dashboard URL? | Not in corpus — likely NSW state-level | GAP |
| R7.7 | Is there a Local Emergency Management Committee (LEMC)? | Standard NSW arrangement — to confirm | GAP |
| R7.8 | What is Council's role in heatwave response? | Not in corpus | GAP |
| R7.9 | Does Council provide sandbag collection in floods? | Standard NSW SES self-collection — verify Burwood-specific | GAP |
| R7.10 | What is the internal ombudsman / disclosure hotline? | (02) 9911 9993 — Public Interest Disclosures Act 1994 | MATCH |

---

## R8 — Community, Services, Housing, Youth

| # | Question | Baseline answer | Status |
|---|---|---|---|
| R8.1 | Does Council run Maternal & Child Health? | Not confirmed — NSW MCH is commonly SLHD-run, not Council | GAP — verify |
| R8.2 | What Early Education (child care) services does Council operate? | Not in corpus | GAP |
| R8.3 | What youth programs run through Council? | Library "Youth" category in events; specific youth services not consolidated | PARTIAL |
| R8.4 | What housing initiatives does Council support? | Not in corpus | GAP |
| R8.5 | What community halls / venues does Council hire out? | Conference Room at Burwood Library and Community Hub; Burwood Park Pavilion (2 Comer Street) | PARTIAL |
| R8.6 | What libraries does Burwood operate? | Burwood Library and Community Hub at 2 Conder Street | MATCH |
| R8.7 | What are library opening hours? | Not consolidated in corpus — linked per-page | GAP |
| R8.8 | Does Burwood have a Justice of the Peace service? | Yes — JP Service Tuesdays 2:00-4:00pm at Burwood Library, no booking required | MATCH |
| R8.9 | What seniors programs run? | Library events include "Seniors" category; specific seniors programs not consolidated | PARTIAL |
| R8.10 | What multicultural programs run? | MAC + Library multicultural programs; 8-language website | PARTIAL |

---

## R9 — Stakeholders, Partners, External Bodies

| # | Question | Baseline answer | Status |
|---|---|---|---|
| R9.1 | What is Burwood's sister-city relationship? | Sandakan (Sabah, Malaysia) | MATCH |
| R9.2 | Which regional alliance is Burwood a member of? | Vibrancy Alliance (Burwood + Canada Bay + Canterbury-Bankstown + Randwick) | MATCH |
| R9.3 | Which NSW state electorate covers Burwood? | Not in corpus | GAP — NSW Electoral Commission |
| R9.4 | Which federal electorate covers Burwood? | Not in corpus | GAP — AEC |
| R9.5 | Which Local Health District? | Sydney Local Health District — to verify | GAP |
| R9.6 | Which Police Area Command? | Burwood PAC — to verify | GAP |
| R9.7 | What business chambers operate? | Croydon Park Business Chamber | PARTIAL |
| R9.8 | Does Council partner with any universities? | Not in corpus | GAP |
| R9.9 | What is the MAC membership? | Independent community members + Councillor representation — specific list to verify | GAP |
| R9.10 | What is the ARIC membership? | Independent audit chair + independent members + Councillor under s428A — specific list to verify | GAP |

---

## R10 — OUT-OF-AREA Routing (Neighbours)

| # | Question | Baseline answer | Status |
|---|---|---|---|
| R10.1 | What is the neighbour council to the east? | City of Canada Bay | MATCH |
| R10.2 | What is the neighbour council to the west? | Municipality of Strathfield | MATCH |
| R10.3 | What is the neighbour council to the south? | City of Canterbury-Bankstown | MATCH |
| R10.4 | What is the neighbour council to the north? | Inner West Council | MATCH |
| R10.5 | What is Canada Bay's switchboard number? | (02) 9911 6555 (to verify in NotebookLM); corpus scrape returned NSW service-directory numbers | PARTIAL |
| R10.6 | What is Strathfield's switchboard number? | (02) 9748 9999 | MATCH (scraped profile) |
| R10.7 | What is Canterbury-Bankstown's switchboard? | (02) 9707 9000 (to verify); customer line 13 77 88 | PARTIAL |
| R10.8 | What is Inner West's switchboard? | 1300 052 637 / (02) 9392 5000 | MATCH |
| R10.9 | What suburb is the edge between Burwood and Canada Bay? | Burwood Heights / Concord West boundary — to verify | GAP |
| R10.10 | Does any part of "Strathfield" suburb lie inside Burwood LGA boundary? | Burwood's Library filter shows Strathfield suburb; but most of Strathfield is in Strathfield Council. Boundary to verify. | PARTIAL |

---

## Summary (Phase 3 baseline before Phase 3.5 NotebookLM block-query)

- Total questions: 100
- MATCH (answered from full_crawl.txt): 44
- PARTIAL (partially answered — needs NotebookLM refinement): 22
- GAP (not in corpus — needs NotebookLM first, then knowledge_gaps.txt if still empty): 34

**Phase 3.5 action:** Submit full R1-R10 matrix as 10-block NotebookLM query against Burwood notebook. Reconcile responses → MATCH / PARTIAL / NEW / CONFLICT / GAP triage per V10.3 skill §Phase 3.5.
