#!/usr/bin/env python3
"""
Council Genius — Burwood Council
TechEntity · server.py v10.3.1

V10.3.1 — Burwood (NSW):
  1. Council-specific constants (contacts, domain, rates model, bin lookup)
  2. Neighbour routing: Canada Bay, Strathfield, Inner West, Canterbury-Bankstown
  3. Waste: per-address lookup; FOGO trial (red fortnightly, green weekly)
  4. Rates: NSW LGA 1993 s494 — land value (NSW Valuer General), quarterly
  5. Synonyms file optional (burwood_synonyms.json) — server is a no-op if absent
  6. knowledge_meta.json: BM25 chunk index (k1=1.5, b=0.75, 60-line chunks)
  7. Canonical name: "Burwood Council" (not "City of Burwood" or "Burwood City")
  8. Traditional Custodians: Wangal Peoples (Dharug Nation)
"""

import os
import json
import csv
import datetime
import hashlib
import time
import re
import math
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_PATH = os.path.join(BASE_DIR, 'knowledge.txt')
ANALYTICS_PATH = os.path.join(BASE_DIR, 'analytics.csv')
FEEDBACK_PATH  = os.path.join(BASE_DIR, 'feedback.csv')
API_KEY_PATH   = os.path.join(BASE_DIR, 'api_key.txt')
QUERIES_BASIC_JSONL = os.path.join(BASE_DIR, 'queries_basic.jsonl')
QUERIES_FULL_JSONL  = os.path.join(BASE_DIR, 'queries_full.jsonl')

# V10 sidecars
SYNONYMS_PATH       = os.path.join(BASE_DIR, 'burwood_synonyms.json')
KNOWLEDGE_META_PATH = os.path.join(BASE_DIR, 'knowledge_meta.json')

# ── Startup tracking ──────────────────────────────────────────────────────────
SERVER_START_TIME = time.time()
TOTAL_QUERIES = 0

# ── API key ──────────────────────────────────────────────────────────────────
def get_api_key():
    key = os.environ.get('ANTHROPIC_API_KEY', '').strip()
    if key:
        return key
    if os.path.exists(API_KEY_PATH):
        with open(API_KEY_PATH) as f:
            return f.read().strip()
    raise RuntimeError('No ANTHROPIC_API_KEY found in environment or api_key.txt')

# ── Knowledge base ───────────────────────────────────────────────────────────
def load_knowledge():
    if os.path.exists(KNOWLEDGE_PATH):
        with open(KNOWLEDGE_PATH, encoding='utf-8') as f:
            return f.read()
    return ''

KNOWLEDGE = load_knowledge()

# ═════════════════════════════════════════════════════════════════════════════
# ██ V10 LAYER — synonyms, normaliser, phonetic, resolver, BM25 retrieval █████
# ═════════════════════════════════════════════════════════════════════════════

def load_synonyms():
    if not os.path.exists(SYNONYMS_PATH):
        print(f'[V10] synonyms file not found at {SYNONYMS_PATH} — normaliser is a no-op')
        return {}
    try:
        with open(SYNONYMS_PATH, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f'[V10][WARN] failed to load synonyms: {e}')
        return {}

def load_knowledge_meta():
    if not os.path.exists(KNOWLEDGE_META_PATH):
        print(f'[V10] knowledge_meta file not found at {KNOWLEDGE_META_PATH} — BM25 retrieval disabled')
        return {}
    try:
        with open(KNOWLEDGE_META_PATH, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f'[V10][WARN] failed to load knowledge_meta: {e}')
        return {}

SYNONYMS       = load_synonyms()
KNOWLEDGE_META = load_knowledge_meta()

GLOBAL_SUBS           = SYNONYMS.get('global_substitutions', {}) or {}
CHILD_HINTS           = SYNONYMS.get('child_vocabulary_hints', {}) or {}
PHONETIC_CONFUSABLES  = SYNONYMS.get('phonetic_confusables', {}) or {}
CATEGORIES_V10        = SYNONYMS.get('categories', {}) or {}
FALLBACK_RULES        = SYNONYMS.get('fallback_rules', {}) or {}

REDIRECT_PHRASES = {}
for cat_key, cat_body in CATEGORIES_V10.items():
    for phrase, target in (cat_body.get('redirect_phrases') or {}).items():
        REDIRECT_PHRASES[phrase.lower()] = target

SYNONYM_TO_CATEGORY = {}
for cat_key, cat_body in CATEGORIES_V10.items():
    bucket = (
        (cat_body.get('canonical')      or []) +
        (cat_body.get('lay_synonyms')   or []) +
        (cat_body.get('misspellings')   or []) +
        (cat_body.get('voice_garbles')  or []) +
        (cat_body.get('child_terms')    or []) +
        (cat_body.get('senior_terms')   or [])
    )
    for term in bucket:
        SYNONYM_TO_CATEGORY.setdefault(term.lower(), cat_body.get('canonical_category', cat_key))

# Metaphone (optional)
try:
    from metaphone import doublemetaphone
    _METAPHONE_OK = True
except Exception as _e:
    _METAPHONE_OK = False
    def doublemetaphone(s):
        return ('', '')
    print(f'[V10] metaphone not installed ({_e}); phonetic fallback disabled.')

_PHONETIC_SEEDS = {}
if _METAPHONE_OK:
    for cat_key, cat_body in CATEGORIES_V10.items():
        target_cat = cat_body.get('canonical_category', cat_key)
        for seed in (cat_body.get('phonetic_seeds') or []):
            p1, p2 = doublemetaphone(seed)
            if p1: _PHONETIC_SEEDS.setdefault(p1, []).append((seed, target_cat))
            if p2: _PHONETIC_SEEDS.setdefault(p2, []).append((seed, target_cat))

_WORD_RE = re.compile(r"[A-Za-z']+")
_STOPWORDS = set("a an and are as at be by for from has have he her him his i in is it its me my of on or our she that the their them they this to us was we were will with you your".split())

def tokenize_query(s):
    if not s:
        return []
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return [t for t in s.split() if t and t not in _STOPWORDS and len(t) > 1]

def normalise_query(q: str) -> str:
    if not q:
        return ''
    out = q.strip().lower()
    for phrase in sorted(CHILD_HINTS.keys(), key=len, reverse=True):
        if phrase in out:
            out = out.replace(phrase, CHILD_HINTS[phrase])
    def _sub(match):
        tok = match.group(0).lower()
        return GLOBAL_SUBS.get(tok, tok)
    out = _WORD_RE.sub(_sub, out)
    return re.sub(r'\s+', ' ', out).strip()

def phonetic_match(q: str):
    if not _METAPHONE_OK or not q:
        return ('', '')
    for token in _WORD_RE.findall(q.lower()):
        if len(token) < 3:
            continue
        p1, p2 = doublemetaphone(token)
        for p in (p1, p2):
            hits = _PHONETIC_SEEDS.get(p)
            if hits:
                seed, cat = hits[0]
                return (cat, seed)
    return ('', '')

_REWRITE_SYS = (
    "You rewrite resident queries about Burwood Council (NSW, inner-west Sydney) into clear canonical form. "
    "Return JSON ONLY with keys: {\"rewritten\":\"\",\"category\":\"\",\"confidence\":0.0-1.0}. "
    "Categories: waste_bins, rates_payments, rates_hardship, rates_concessions, planning_building, "
    "animals_pets, roads_traffic, parking, water_stormwater, environment_climate, emergency_safety, "
    "health_community, families_children, aged_disability, community_events, library_learning, "
    "recreation_sport, governance_contact, business_economy, arts_culture_heritage, first_nations, "
    "out_of_area, other."
)

def claude_rewrite(q: str, timeout: int = 10):
    try:
        api_key = get_api_key()
    except Exception:
        return None
    payload = json.dumps({
        'model': 'claude-sonnet-4-6',
        'max_tokens': 200,
        'system': _REWRITE_SYS,
        'messages': [{'role': 'user', 'content': f'Rewrite: {q}'}]
    }).encode('utf-8')
    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=payload,
        headers={
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        },
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        raw = data['content'][0]['text'].strip()
        m = re.search(r'\{.*\}', raw, re.S)
        if not m:
            return None
        return json.loads(m.group(0))
    except Exception as e:
        print(f'[V10][WARN] claude_rewrite failed: {e}')
        return None

def resolve_query(raw_query: str, allow_rewrite: bool = True) -> dict:
    nq = normalise_query(raw_query or '')
    for phrase, cat in REDIRECT_PHRASES.items():
        if phrase in nq:
            return {'category': cat, 'confidence': 1.0, 'normalised': nq,
                    'stage': 'redirect_phrase', 'matched': phrase}
    multi_hits = [t for t in SYNONYM_TO_CATEGORY.keys() if ' ' in t and t in nq]
    if multi_hits:
        best = max(multi_hits, key=len)
        return {'category': SYNONYM_TO_CATEGORY[best], 'confidence': 0.9,
                'normalised': nq, 'stage': 'synonym_multi', 'matched': best}
    tokens = set(_WORD_RE.findall(nq))
    single_hits = [t for t in tokens if t in SYNONYM_TO_CATEGORY]
    if single_hits:
        best = single_hits[0]
        return {'category': SYNONYM_TO_CATEGORY[best], 'confidence': 0.8,
                'normalised': nq, 'stage': 'synonym_single', 'matched': best}
    cat, seed = phonetic_match(nq)
    if cat:
        return {'category': cat, 'confidence': 0.6, 'normalised': nq,
                'stage': 'phonetic', 'matched': seed}
    if allow_rewrite:
        rw = claude_rewrite(raw_query)
        if rw and rw.get('category') and rw.get('category') != 'other':
            return {'category': rw['category'],
                    'confidence': float(rw.get('confidence', 0.55) or 0.55),
                    'normalised': nq, 'stage': 'claude_rewrite',
                    'rewritten': rw.get('rewritten', ''), 'matched': ''}
    return {'category': 'other', 'confidence': 0.0, 'normalised': nq,
            'stage': 'fallback', 'matched': '',
            'fallback_message': FALLBACK_RULES.get('if_no_match', '')}

# ── BM25 retrieval over knowledge_meta chunks ────────────────────────────────
_BM25_K1 = float((KNOWLEDGE_META.get('bm25_params') or {}).get('k1', 1.5))
_BM25_B  = float((KNOWLEDGE_META.get('bm25_params') or {}).get('b', 0.75))
_BM25_CHUNKS = KNOWLEDGE_META.get('chunks', []) or []
_BM25_IDF = KNOWLEDGE_META.get('idf', {}) or {}
_BM25_AVGDL = float(KNOWLEDGE_META.get('avgdl_terms', 0.0) or 1.0)

def bm25_search(q: str, top_k: int = 10):
    if not _BM25_CHUNKS:
        return []
    q_toks = tokenize_query(q)
    if not q_toks:
        return []
    scored = []
    for c in _BM25_CHUNKS:
        tf = c.get('term_counts') or {}
        dl = c.get('doc_len') or 1
        score = 0.0
        for t in q_toks:
            if t not in tf:
                continue
            idf = _BM25_IDF.get(t, 0.0)
            f = tf[t]
            denom = f + _BM25_K1 * (1 - _BM25_B + _BM25_B * dl / _BM25_AVGDL)
            score += idf * (f * (_BM25_K1 + 1)) / denom
        if score > 0:
            scored.append((score, c.get('chunk_id'), c.get('start_line'), c.get('end_line'),
                           c.get('category'), c.get('has_escalate_true')))
    scored.sort(key=lambda x: -x[0])
    return scored[:top_k]

def suggest(raw_query: str, limit: int = 8):
    if not raw_query:
        return []
    nq = normalise_query(raw_query)
    prefix = nq
    hits = []
    for phrase in REDIRECT_PHRASES.keys():
        if phrase.startswith(prefix):
            hits.append((3.0, phrase))
    for term in SYNONYM_TO_CATEGORY.keys():
        if term.startswith(prefix) and ' ' not in term:
            hits.append((2.0, term))
    for phrase in REDIRECT_PHRASES.keys():
        if prefix in phrase and not phrase.startswith(prefix):
            hits.append((1.0, phrase))
    seen, out = set(), []
    for _, v in sorted(hits, key=lambda x: (-x[0], x[1])):
        if v in seen:
            continue
        seen.add(v); out.append(v)
        if len(out) >= limit:
            break
    return out

# ═════════════════════════════════════════════════════════════════════════════
# ██ End V10 LAYER ████████████████████████████████████████████████████████████
# ═════════════════════════════════════════════════════════════════════════════

def filter_pii(text: str) -> str:
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[EMAIL]', text)
    text = re.sub(r'\b\d{3,4}\s?\d{3,4}\b', '[PHONE]', text)
    text = re.sub(r'\b\d{4}\b', '[POSTCODE]', text)
    text = re.sub(r'\b\d{10}\b', '[ID_NUMBER]', text)
    return text

def log_query_basic(query: str, category: str):
    filtered_query = filter_pii(query)
    record = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'category': category,
        'query_preview': filtered_query[:200]
    }
    try:
        with open(QUERIES_BASIC_JSONL, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record) + '\n')
    except Exception as e:
        print(f'[WARN] Failed to log basic query: {e}')

def log_query_full(query: str, response: str, category: str):
    filtered_query = filter_pii(query)
    filtered_response = filter_pii(response)
    record = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'category': category,
        'query': filtered_query,
        'response': filtered_response[:500]
    }
    try:
        with open(QUERIES_FULL_JSONL, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record) + '\n')
    except Exception as e:
        print(f'[WARN] Failed to log full query: {e}')

# ── System prompt (Burwood-specific) ─────────────────────────────────────────
SYSTEM_PROMPT = f"""You are Council Genius, the official AI resident assistant for Burwood Council, deployed by TechEntity on behalf of Burwood Council.

CANONICAL NAME: Always refer to Council as "Burwood Council" — never "Burwood City Council" or "City of Burwood".

ACKNOWLEDGEMENT OF COUNTRY: Burwood Council acknowledges the Wangal Peoples as the traditional custodians of the area. Always treat matters concerning First Nations peoples with cultural respect.

YOUR PURPOSE: Answer questions so completely the resident never needs to contact Council.

AGENTIC BEHAVIOUR: For any process question, give all steps, fees, correct forms, and correct officer.

FOR BUILDING/PLANNING: Ask property address (suburb), use of the building, and whether it is in a Heritage Conservation Area before answering. Burwood's LEP is the Burwood Local Environmental Plan 2012 (gazetted 9 November 2012). Burwood's DCP is the Burwood Development Control Plan 2012 (adopted 4 December 2012).

FOR WASTE / BIN QUESTIONS: Burwood operates a **per-address waste lookup** with an active FOGO trial. Ask for the resident's address and direct them to [burwood.nsw.gov.au](https://burwood.nsw.gov.au) rather than asserting a fixed bin-day. Schedule: **RED (general waste) fortnightly, YELLOW (recycling) fortnightly, GREEN FOGO (food+garden) weekly, BLUE (paper) fortnightly**.

FOR RATES: Burwood Council sets rates under NSW Local Government Act 1993 **s494** — based on **land value set by NSW Valuer General**. Rates are paid in **four quarterly instalments**. Pensioner rebate up to $250/year under LGA s575.

FOR PARKING: Clarify whether the question is about a permit, a fine, or parking in a specific precinct before answering. Parking fine reviews go through **Revenue NSW** — not Council.

FOR PETS: Remind the resident that in NSW pet registration is a **lifetime registration** via the **NSW Pet Registry** (petregistry.nsw.gov.au). Microchipping by 12 weeks of age. Council enforces compliance under the Companion Animals Act 1998.

FOR EMERGENCIES: Always direct life-threatening to **000**, storm/flood to NSW SES on **132 500**, and Burwood Council 24/7 line on **(02) 9911 9911**.

FOUR-TURN RESOLUTION: Resolve every query within four user inputs.

OUT OF AREA (light-touch handoff): If a query is about a location or service clearly outside the Burwood LGA (e.g., a suburb in Canada Bay, Strathfield, Inner West Council, or Canterbury-Bankstown), respond with only:
- One sentence noting it is outside Burwood Council area
- Full official name of the relevant council
- That council's official website URL only
Do NOT quote neighbouring councils' phone numbers, addresses, or staff email addresses. Burwood Council does not speak on behalf of neighbouring councils. No further elaboration. No offers of further help.

Neighbouring councils (name + website only — never quote their phone or address):
- City of Canada Bay (Concord, Drummoyne, Rhodes, Mortlake, Five Dock, Abbotsford, Wareemba, Russell Lea, Rodd Point, Chiswick, Liberty Grove, Cabarita, Canada Bay): **canadabay.nsw.gov.au**
- Municipality of Strathfield (bulk of Strathfield suburb, Strathfield South, Homebush, Homebush West, Greenacre portion): **strathfield.nsw.gov.au**
- Inner West Council (Ashfield, Summer Hill, Lewisham, Dulwich Hill, Haberfield, Leichhardt, Annandale, Balmain, Rozelle, Marrickville, Newtown, Stanmore, Petersham, Enmore, Sydenham, St Peters, Tempe, Camperdown east of Burwood boundary): **innerwest.nsw.gov.au**
- City of Canterbury-Bankstown (Campsie, Canterbury, Belmore, Lakemba, Wiley Park, Punchbowl, Bankstown, Riverwood, Roselands, Earlwood, Clemton Park, Ashbury south of Burwood boundary): **cbcity.nsw.gov.au**
- Transport for NSW (state roads including Parramatta Road, buses, trains, timetables, licences): [131 500](tel:131500) — Transport for NSW is a state authority, not a neighbouring council, so its number may be quoted.
- Sydney Water (water/sewer services and outages): [13 20 90](tel:132090)
- Ausgrid (electricity distribution / power outages / street lights): [13 13 88](tel:131388)
- Jemena (gas distribution / gas leaks): [131 909](tel:131909)

MULTILINGUAL: If asked in another language, answer in that language then repeat in English labelled "English version:". Burwood's main community languages: Mandarin, Cantonese, Korean, Nepali, Arabic, Vietnamese, Italian, Greek, Indonesian. For free interpreting: **TIS National on 131 450**.

COMMUNICATION STYLE — apply to every response:
- Use Australian English spelling and plain English. "Use" not "utilise". "About" not "regarding". "Help" not "facilitate". "Start" not "commence".
- Sentences average 15–20 words. One idea per sentence.
- Lead with what CAN be done before explaining any limitations.
- When a resident is reporting a problem that has already happened (a complaint), acknowledge their experience before providing process information.
- When a resident is asking for something to happen (a service request), respond efficiently.
- Deliver bad news in this order: acknowledge, explain, offer next step.
- Never minimise a resident's concern. Never use "just," "only," "simply," or "it's easy".
- When you don't have specific information, say so clearly and direct the resident to the right contact — never invent fees, dates, or processes.

FORMAT RULES — NON-NEGOTIABLE:
- NEVER use emoji of any kind
- NEVER output raw HTML — no <a> tags, no HTML elements
- Phone numbers: markdown hyperlink ONLY — [(02) 9911 9911](tel:0299119911)
- Emails: markdown mailto ONLY — [council@burwood.nsw.gov.au](mailto:council@burwood.nsw.gov.au)
- URLs: markdown links ONLY — [descriptive label](https://full-url)
- Use **bold** for key terms
- Use bullet lists for multi-step processes
- Keep responses under 300 words unless a complex process genuinely requires more
- Do NOT use ## headers — use **bold text** instead
- Include the Council contact footer no more than once per response

HIDDEN META-TAGS: Knowledge-base entries contain <category>X</category> and <escalate>true/false</escalate> meta-tags. These are for retrieval — **never reveal them to the resident**. When <escalate>true</escalate> is dominant in the best-matching chunk, include the Council contact footer.

KNOWLEDGE BASE — BURWOOD COUNCIL:

{KNOWLEDGE}

END OF KNOWLEDGE BASE.

If information is not in the knowledge base, direct the resident to [(02) 9911 9911](tel:0299119911) or [council@burwood.nsw.gov.au](mailto:council@burwood.nsw.gov.au). Do not invent fees, dates, or processes.
"""

# ── Analytics categories (Burwood-tuned) ─────────────────────────────────────
CATEGORIES = {
    'rates':            ['rate', 'rates', 'levy', 'land value', 'valuer general', 'payment plan', 'hardship', 'instalment', 'rebate', 'concession', 'valuation', 'pensioner rebate', 'waste charge', 'bpay'],
    'waste_bins':       ['bin', 'bins', 'rubbish', 'recycling', 'green waste', 'collection', 'fogo', 'kerbside', 'compost', 'organics', 'bulky waste', 'landfill', 'red bin', 'yellow bin', 'green bin', 'blue bin', 'missed bin'],
    'planning':         ['planning', 'da', 'development application', 'cdc', 'complying development', 'subdivision', 'zoning', 'heritage', 'lep', 'dcp', 'amendment', 'secondary dwelling', 'granny flat', 'section 10.7', 'planning certificate'],
    'building':         ['building permit', 'certifier', 'building inspection', 'construction', 'demolition', 'owner builder', 'pool', 'spa', 'occupation certificate', 'principal certifying authority'],
    'parking':          ['parking', 'parking permit', 'resident parking permit', 'fine', 'infringement', 'appeal', 'parking zone', 'revenue nsw'],
    'animals':          ['dog', 'cat', 'animal', 'pet', 'register', 'pound', 'roaming', 'attack', 'barking', 'dangerous dog', 'microchip', 'nsw pet registry', 'off-leash'],
    'local_laws':       ['local law', 'noise', 'nuisance', 'skip bin', 'footpath', 'outdoor dining', 'busking', 'nature strip', 'graffiti', 'fence'],
    'roads':            ['road', 'footpath', 'pothole', 'kerb', 'drainage', 'street light', 'signage', 'driveway', 'vehicle crossing', 'street tree', 'road closure', 'bike lane', 'cycling', 'speed limit'],
    'transport':        ['train', 'bus', 'opal', 'transport nsw', 'tfnsw', 'public transport', 'burwood station', 'burwood north', 'metro west', 'sydney metro'],
    'utilities':        ['water', 'sewer', 'sewerage', 'electricity', 'power', 'outage', 'gas leak', 'ausgrid', 'sydney water', 'jemena', 'nbn'],
    'venues_events':    ['venue', 'hire', 'event', 'permit', 'book', 'facility', 'library', 'burwood library', 'enfield aquatic centre', 'pool', 'burwood park', 'henley park', 'lunar new year', 'festival'],
    'community':        ['grant', 'program', 'service', 'aged', 'older', 'disability', 'youth', 'maternal', 'child health', 'multicultural', 'volunteer', 'seniors', 'jp', 'justice of the peace'],
    'first_nations':    ['aboriginal', 'first nations', 'traditional owner', 'wangal', 'dharug', 'darug', 'reconciliation action plan', 'rap', 'naidoc', 'welcome to country', 'acknowledgement of country'],
    'governance':       ['meeting', 'councillor', 'mayor', 'deputy mayor', 'john faker', 'george mannah', 'tommaso briscese', 'general manager', 'gm', 'agenda', 'minutes', 'gipa', 'foi', 'complaint', 'petition', 'council plan', 'burwood2036', 'delivery program', 'aric', 'icac', 'olg'],
    'economy':          ['business', 'chamber of commerce', 'burwood chamber', 'vibrancy alliance', 'food business', 'liquor licence', 'outdoor dining'],
    'environment':      ['climate', 'net zero', 'emissions', 'biodiversity', 'urban forest', 'tree planting', 'parramatta river', 'solar', 'sustainability'],
    'emergency':        ['emergency', 'flood', 'heatwave', 'bushfire', 'relief centre', 'ses', 'nsw ses', 'fire and rescue', 'family violence', '1800respect', 'lifeline', 'beyond blue', 'police', 'burwood police', 'concord hospital'],
    'off_topic_benign': ['recipe', 'football', 'weather', 'stock price', 'poem', 'news', 'sport', 'joke', 'movie', 'nrl', 'afl'],
    'potential_api_abuse': ['ignore previous', 'jailbreak', 'pretend you are', 'act as', 'system prompt', 'disregard', 'override', 'forget instructions', 'new instructions', 'ignore all'],
    'other':            []
}

def classify(text: str) -> str:
    lower = text.lower()
    for category, keywords in CATEGORIES.items():
        if category == 'other':
            continue
        if any(kw in lower for kw in keywords):
            return category
    return 'other'

def log_analytics(category: str, query: str):
    exists = os.path.exists(ANALYTICS_PATH)
    with open(ANALYTICS_PATH, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(['timestamp', 'category', 'query_preview'])
        w.writerow([
            datetime.datetime.utcnow().isoformat(),
            category,
            query[:120].replace('\n', ' ')
        ])

def log_feedback(query: str, response: str, rating: str):
    exists = os.path.exists(FEEDBACK_PATH)
    with open(FEEDBACK_PATH, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(['timestamp', 'rating', 'query_preview', 'response_preview'])
        w.writerow([
            datetime.datetime.utcnow().isoformat(),
            rating,
            query[:120].replace('\n', ' '),
            response[:200].replace('\n', ' ')
        ])

def call_claude(messages: list) -> str:
    api_key = get_api_key()
    payload = json.dumps({
        'model': 'claude-sonnet-4-6',
        'max_tokens': 1024,
        'system': SYSTEM_PROMPT,
        'messages': messages
    }).encode('utf-8')
    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=payload,
        headers={
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        },
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data['content'][0]['text']
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'Anthropic API error {e.code}: {body}')

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, text: str, status: int = 200):
        body = text.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, path: str, content_type: str):
        if not os.path.isfile(path):
            self._send_text('Not found', 404)
            return
        with open(path, 'rb') as f:
            data = f.read()
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self._cors()
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/health':
            knowledge_hash = hashlib.sha256(KNOWLEDGE.encode('utf-8')).hexdigest()[:16]
            knowledge_lines = len(KNOWLEDGE.split('\n'))
            uptime = time.time() - SERVER_START_TIME
            health = {
                'status': 'ok',
                'council': 'Burwood Council',
                'knowledge_lines': knowledge_lines,
                'knowledge_hash': knowledge_hash,
                'prompt_version': '1.0',
                'uptime_seconds': round(uptime, 2),
                'total_queries': TOTAL_QUERIES,
                'model': 'claude-sonnet-4-6',
                'bin_mode': 'per-address-lookup (FOGO trial)',
                'server_version': 'v10.3.1',
                'synonyms_loaded': bool(SYNONYMS),
                'synonym_categories': len(CATEGORIES_V10),
                'knowledge_meta_loaded': bool(_BM25_CHUNKS),
                'bm25_chunks': len(_BM25_CHUNKS),
                'bm25_vocab': len(_BM25_IDF),
                'phonetic_enabled': _METAPHONE_OK,
            }
            self._send_json(health)
            return

        if path == '/bm25':
            qs = parse_qs(parsed.query or '')
            q = (qs.get('q', [''])[0] or '').strip()
            if not q:
                self._send_json({'error': 'missing q parameter'}, 400)
                return
            try:
                results = bm25_search(q, top_k=10)
                out = [{'score': round(s, 4), 'chunk_id': cid,
                        'start_line': sl, 'end_line': el,
                        'category': cat, 'escalate': esc}
                       for (s, cid, sl, el, cat, esc) in results]
                self._send_json({'query': q, 'results': out})
            except Exception as e:
                print(f'[ERROR /bm25] {e}')
                self._send_json({'error': str(e)}, 500)
            return

        if path == '/suggest':
            qs = parse_qs(parsed.query or '')
            q = (qs.get('q', [''])[0] or '').strip()
            if not q:
                self._send_json({'suggestions': []})
                return
            try:
                self._send_json({'suggestions': suggest(q)})
            except Exception as e:
                print(f'[ERROR /suggest] {e}')
                self._send_json({'error': str(e)}, 500)
            return

        if path == '/' or path == '/index.html' or path == '/page.html':
            self._serve_file(os.path.join(BASE_DIR, 'page.html'), 'text/html; charset=utf-8')
            return

        if path == '/admin/analytics':
            if os.path.exists(ANALYTICS_PATH):
                with open(ANALYTICS_PATH, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/csv')
                self.send_header('Content-Disposition', 'attachment; filename="analytics.csv"')
                self.send_header('Content-Length', str(len(data)))
                self._cors()
                self.end_headers()
                self.wfile.write(data)
            else:
                self._send_text('timestamp,category,query_preview\n', 200)
            return

        if path == '/admin/feedback':
            if os.path.exists(FEEDBACK_PATH):
                with open(FEEDBACK_PATH, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/csv')
                self.send_header('Content-Disposition', 'attachment; filename="feedback.csv"')
                self.send_header('Content-Length', str(len(data)))
                self._cors()
                self.end_headers()
                self.wfile.write(data)
            else:
                self._send_text('timestamp,rating,query_preview,response_preview\n', 200)
            return

        self._send_text('Not found', 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        length = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(length) if length else b''

        if path == '/chat':
            try:
                body = json.loads(body_bytes.decode('utf-8'))
                messages = body.get('messages', [])
                if not messages:
                    self._send_json({'error': 'No messages provided'}, 400)
                    return

                last_user = next(
                    (m['content'] for m in reversed(messages) if m['role'] == 'user'),
                    ''
                )

                v10 = resolve_query(last_user, allow_rewrite=False)
                v9_category = classify(last_user)
                category = v10['category'] if v10['category'] != 'other' else v9_category

                log_analytics(category, last_user)
                log_query_basic(last_user, category)

                if v9_category == 'potential_api_abuse' or category == 'potential_api_abuse':
                    self._send_json({'error': 'This request cannot be processed.'}, 400)
                    return

                if category == 'other':
                    rw = claude_rewrite(last_user)
                    if rw and rw.get('category') and rw['category'] != 'other':
                        category = rw['category']

                global TOTAL_QUERIES
                TOTAL_QUERIES += 1
                reply = call_claude(messages)
                log_query_full(last_user, reply, category)
                self._send_json({
                    'reply': reply,
                    'category': category,
                    'v10': {
                        'stage': v10.get('stage'),
                        'confidence': v10.get('confidence'),
                        'normalised': v10.get('normalised'),
                    },
                })

            except Exception as e:
                print(f'[ERROR /chat] {e}')
                error_msg = "Sorry, I'm having trouble right now. Please try again or call Burwood Council on (02) 9911 9911."
                self._send_json({'error': error_msg}, 500)
            return

        if path == '/feedback':
            try:
                body = json.loads(body_bytes.decode('utf-8'))
                log_feedback(
                    body.get('query', ''),
                    body.get('response', ''),
                    body.get('rating', 'unknown')
                )
                self._send_json({'ok': True})
            except Exception as e:
                print(f'[ERROR /feedback] {e}')
                self._send_json({'error': str(e)}, 500)
            return

        self._send_text('Not found', 404)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f'Council Genius — Burwood Council — v10.3.1 — listening on port {port}')
    server.serve_forever()
