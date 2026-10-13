"""Ask the Workbench: deterministic, evidence-grounded answers assembled ONLY from published findings.

No model, no paid API and no network call is made here. A question is tokenized, matched against the published
findings and capability map by transparent term overlap, and the answer is assembled from the matching records with
their dates, evidence classes, validation status, limitations and sources. If the published evidence does not cover
the question the answer is NOT_ESTABLISHED; the engine never fills the gap with a guess.
"""
from __future__ import annotations

import re

from . import findings as F

MAX_QUESTION = 300
STOP = frozenset('''a an and are as at be been but by can could did do does for from had has have how i in into is it its
me my of on or our so than that the their them then there these they this those to was we were what when where which who
whom why will with would you your about any also not no yes please tell show give know say said done made make
work behave behaves behaved behaviour behavior happen happened actually really experiment experiments finding findings
result results published research workbench perform performed run ran use used using get got
sap ai capability capabilities technology technologies tool tools remain remains remaining still left
established establish establishes evidence based only yet far ever whether prasad deshpande owner owners
integration integrate integrated'''.split())
# A4/A5: generic verbs ("established") and the owner's name are not topics: counting them made every answer partial.
SYNONYMS = (
    ('cap', 'cds', 'capire'), ('fiori', 'ui5', 'sapui5', 'openui5'), ('abap', 'rap'), ('mcp', 'protocol'),
    ('agent', 'agents', 'agentic'), ('ai', 'llm', 'genai', 'model'), ('odata', 'service'), ('trial', 'sandbox'),
)
_SYN = {w: set(g) - {w} for g in SYNONYMS for w in g}
INTENTS = {
    'LATEST': frozenset({'latest', 'recent', 'recently', 'new', 'newest', 'changed', 'change', 'update', 'updated', 'updates'}),
    'PROVEN': frozenset({'proven', 'prove', 'validated', 'validate', 'verified', 'verify', 'hands', 'handson', 'works', 'worked'}),
    'BLOCKED': frozenset({'blocked', 'block', 'license', 'licence', 'licensing', 'entitlement', 'access', 'trial', 'cannot', 'unable', 'unavailable'}),
    # an SAP system/tenant word is required: "Fiori and UI5 integration" is a local question, not a system claim
    'SYSTEM': frozenset({'tenant', 'tenants', 'production', 'landscape', 'system', 'systems', 's4hana', 'readback'}),
    'DOCUMENTATION': frozenset({'documentation', 'documented', 'document', 'docs', 'doc'}),
    'UNPROVEN': frozenset({'unproven', 'unverified', 'untested', 'unvalidated', 'gap', 'gaps', 'missing', 'outstanding',
                           'pending', 'open'}),
    'LIMITATIONS': frozenset({'limitation', 'limitations', 'limit', 'limits', 'limited', 'risk', 'risks', 'caveat', 'caveats', 'weakness'}),
}
COVERED = 0.6        # share of the topic terms one finding must cover for the answer to count as ANSWERED
W = {'title': 3.0, 'technology': 2.0, 'question': 2.0, 'objective': 1.0, 'observations': 1.0, 'findings': 1.0,
     'limitations': 1.0, 'improvements': 0.5}
MIN_COVERAGE = 0.34


def _stem(w: str) -> str:
    if len(w) > 4 and w.endswith('ies'):
        return w[:-3] + 'y'
    if len(w) > 4 and w.endswith('ing'):
        return w[:-3]
    if len(w) > 3 and w.endswith('ed'):
        return w[:-2]
    if len(w) > 3 and w.endswith('s') and not w.endswith('ss'):
        return w[:-1]
    return w


def tokens(text: str) -> list[str]:
    out = []
    for w in re.findall(r"[a-z0-9]+", str(text).lower()):
        if len(w) < 2 or w in STOP:
            continue
        out.append(_stem(w))
    return out


# intents are stemmed with the same function as the question, so "validated" matches "validate"
INTENTS = {name: frozenset(_stem(w) for w in words) for name, words in INTENTS.items()}
INTENT_WORDS = frozenset().union(*INTENTS.values())


def _expand(term: str) -> set[str]:
    return {term} | _SYN.get(term, set())


def _flat(items) -> str:
    return ' '.join(i.get('text', '') if isinstance(i, dict) else str(i) for i in (items or []))


def _doc_fields(f: dict) -> dict:
    return {'title': f.get('title', ''), 'technology': f.get('technology', ''), 'question': f.get('question', ''),
            'objective': f.get('objective', ''), 'observations': _flat(f.get('verified_observations')),
            'findings': _flat(f.get('technical_findings')), 'limitations': _flat(f.get('limitations')),
            'improvements': _flat(f.get('improvements'))}


_NOT_YET = re.compile(r'(?i)\bnot\s+(?:yet\s+)?(?:been\s+)?(?:proven|proved|validated|tested|established|verified|shown)\b')


def classify(question: str) -> tuple[set, list[str]]:
    toks = tokens(question)
    intents = {name for name, words in INTENTS.items() if any(t in words for t in toks)}
    if _NOT_YET.search(str(question)):
        intents.add('UNPROVEN')
    topic = [t for t in toks if t not in INTENT_WORDS]
    return intents, list(dict.fromkeys(topic))


def _score(topic: list[str], fields: dict) -> tuple[float, list[str]]:
    bag = {k: set(tokens(v)) for k, v in fields.items()}
    score, hit = 0.0, []
    for term in topic:
        alts = _expand(term)
        best = 0.0
        for k, toks in bag.items():
            if toks & alts:
                best = max(best, W[k])
        if best:
            score += best
            hit.append(term)
    return score, hit


def _finding_view(f: dict, hit: list[str], score: float) -> dict:
    obs = [o['text'] if isinstance(o, dict) else str(o) for o in f.get('verified_observations') or []]
    tech = [o['text'] if isinstance(o, dict) else str(o) for o in f.get('technical_findings') or []]
    return {'finding_id': f['finding_id'], 'title': f.get('title', ''), 'state': f.get('state'),
            'execution_date': f.get('execution_date'), 'evidence_class': f.get('evidence_class'),
            'evidence_label': f.get('evidence_label') or F.EVIDENCE_LABEL.get(f.get('evidence_class'), ''),
            'validation_status': f.get('validation_status'), 'scope': f.get('scope'),
            'excerpt': (obs[:1] + tech[:1]) or [], 'limitations': [x['text'] if isinstance(x, dict) else str(x)
                                                                    for x in f.get('limitations') or []][:3],
            'sources': [{'title': s.get('title', ''), 'url': s.get('url', '')} for s in f.get('sources') or []][:5],
            'superseded_by': f.get('superseded_by'), 'matched_terms': hit, 'score': round(score, 2),
            'stale': F.is_stale(f), 'evidence_tier': F.finding_tier(f)}


def _cap_view(c: dict) -> dict:
    return {**c, 'evidence_tier': F.capability_tier(c)}


def _tier_counts(findings: list) -> str:
    n = {}
    for f in findings:
        if f.get('state') == 'PUBLISHED':
            t = F.finding_tier(f)
            n[t] = n.get(t, 0) + 1
    return '; '.join(f'{k} finding(s): {F.TIER_TEXT[t]}' for t, k in sorted(n.items())) or 'no current findings'


def answer(question: str, release: dict, *, status_of_content: str = 'OK') -> dict:
    q = ' '.join(str(question or '').split())[:MAX_QUESTION]
    intents, topic = classify(q)
    findings = F.visible(release)
    caps = release.get('capabilities') or []
    res = {'question': q, 'intents': sorted(intents), 'topic_terms': topic, 'release_version': release.get('version'),
           'release_published_at': release.get('published_at'), 'content_status': status_of_content,
           'status': 'NOT_ESTABLISHED', 'summary': '', 'findings': [], 'capabilities': [], 'limitations': [],
           'not_established': [], 'changes': []}
    if not q:
        res['summary'] = 'Ask about a technology or a capability, for example "What have you validated with CAP and MCP?".'
        return res
    if not findings and not caps:
        res['summary'] = ('No findings have been published yet, so this has not been established. Published content '
                          'appears here only after the owner approves it.')
        res['not_established'] = [f'Nothing published mentions "{t}".' for t in topic] or ['Nothing is published yet.']
        return res

    # --- score every published finding and capability against the topic terms
    scored = []
    for f in findings:
        s, hit = _score(topic, _doc_fields(f)) if topic else (0.0, [])
        scored.append((s, hit, f))
    cap_scored = []
    for c in caps:
        s, hit = _score(topic, {'title': c.get('name', ''), 'technology': c.get('key', ''), 'question': '', 'objective': '',
                                 'observations': c.get('note', ''), 'findings': '', 'limitations': '', 'improvements': ''}) \
            if topic else (0.0, [])
        cap_scored.append((s, hit, c))

    def covered(hit):
        return (len(hit) / len(topic)) if topic else 1.0

    matched = [(s, h, f) for s, h, f in scored if (not topic and intents) or (topic and covered(h) >= MIN_COVERAGE and s > 0)]
    matched_caps = [(s, h, c) for s, h, c in cap_scored if (not topic and intents) or (topic and covered(h) >= MIN_COVERAGE and s > 0)]

    pool = matched if topic else [(0, [], f) for f in findings]
    cap_pool = matched_caps if topic else [(0, [], c) for c in caps]
    special = None
    if 'UNPROVEN' in intents:
        special = 'UNPROVEN'
        open_caps = [c for s, h, c in cap_pool if F.capability_tier(c) in ('NOT_ESTABLISHED', 'AUTHORIZATION_BLOCKED')]
        weak = [(s, h, f) for s, h, f in pool if F.finding_tier(f) in ('NOT_ESTABLISHED', 'DOCUMENTATION_RETRIEVED')
                and f.get('state') == 'PUBLISHED']
        res['capabilities'] = [_cap_view(c) for c in open_caps]
        res['findings'] = [_finding_view(f, h, s) for s, h, f in weak[:6]]
        blocked = sum(1 for c in open_caps if F.capability_tier(c) == 'AUTHORIZATION_BLOCKED')
        idle = len(open_caps) - blocked
        docs = sum(1 for _s, _h, f in weak if F.finding_tier(f) == 'DOCUMENTATION_RETRIEVED')
        res['status'] = 'ANSWERED' if (open_caps or weak) else 'NOT_ESTABLISHED'
        res['summary'] = (f"Not yet established: {idle} capabilit{'y is' if idle == 1 else 'ies are'} not validated, and "
                          f"{blocked} {'is' if blocked == 1 else 'are'} blocked by SAP entitlement, trial or licence access. "
                          f"{docs} published finding(s) rest on documentation retrieval only, which shows what SAP publishes "
                          'but does not prove that anything runs in an SAP system.'
                          if (open_caps or weak) else 'Nothing published lists an open or unproven area for this question.')
    elif 'SYSTEM' in intents and not ({'LATEST', 'DOCUMENTATION'} & intents):
        special = 'SYSTEM'
        system = [(s, h, f) for s, h, f in pool
                  if F.finding_tier(f) == 'SAP_SYSTEM_READBACK_VALIDATED' and f.get('state') == 'PUBLISHED']
        res['findings'] = [_finding_view(f, h, s) for s, h, f in sorted(system, key=lambda x: -x[0])[:6]]
        res['capabilities'] = [_cap_view(c) for s, h, c in cap_pool if F.capability_tier(c) == 'SAP_SYSTEM_READBACK_VALIDATED']
        if res['findings'] or res['capabilities']:
            res['status'] = 'ANSWERED'
            res['summary'] = (f"{len(res['findings'])} published finding(s) were validated by reading back from an SAP "
                              'system. Their scope and limitations are listed below.')
        else:
            res['status'] = 'NOT_ESTABLISHED'
            res['summary'] = ('No. None of the published evidence was obtained from an SAP system or tenant, so an SAP '
                              f"system integration has not been established. What is published: {_tier_counts(findings)}.")
            res['not_established'] = ['No published finding reads back from an SAP system or tenant.']
    elif 'DOCUMENTATION' in intents:
        special = 'DOCUMENTATION'
        docs = [(s, h, f) for s, h, f in pool if F.finding_tier(f) == 'DOCUMENTATION_RETRIEVED']
        res['findings'] = [_finding_view(f, h, s) for s, h, f in sorted(docs, key=lambda x: -x[0])[:6]]
        res['capabilities'] = [_cap_view(c) for s, h, c in cap_pool if F.capability_tier(c) == 'DOCUMENTATION_RETRIEVED']
        res['status'] = 'ANSWERED'
        res['summary'] = (f"{len(res['findings'])} published finding(s) are based only on documentation retrieval: they "
                          'show what SAP publishes, not that it works in an SAP system.' if res['findings'] else
                          'None of the published findings is based only on documentation.')
    if special:
        return res
    if 'LATEST' in intents:
        latest = sorted(matched if topic else [(0, [], f) for f in findings],
                        key=lambda x: (x[2].get('execution_date', ''), x[2]['finding_id']), reverse=True)[:5]
        res['findings'] = [_finding_view(f, h, s) for s, h, f in latest]
        res['changes'] = list((release.get('changes') or [])[:5])
    elif 'PROVEN' in intents:
        proven = [(s, h, f) for s, h, f in (matched if topic else [(0, [], f) for f in findings])
                  if f.get('validation_status') == 'VALIDATED' and f.get('state') == 'PUBLISHED']
        res['findings'] = [_finding_view(f, h, s) for s, h, f in sorted(proven, key=lambda x: -x[0])[:6]]
        res['capabilities'] = [_cap_view(c) for s, h, c in cap_pool
                               if c.get('status') in ('VALIDATED_HANDS_ON', 'READ_ONLY_LISTING_VALIDATED', 'DOCUMENTATION_RETRIEVED')]
    elif 'BLOCKED' in intents:
        # A6: only an entitlement/trial/licence need is "blocked"; not validated is reported separately, never as blocked
        res['capabilities'] = [_cap_view(c) for s, h, c in cap_pool if c.get('status') == 'ACCESS_REQUIRED']
        idle = [c.get('name', '') for s, h, c in cap_pool if c.get('status') in ('NOT_VALIDATED', 'DISCOVERY_ONLY')]
        if idle:
            res['not_established'].append(f"{len(idle)} capabilit{'y is' if len(idle) == 1 else 'ies are'} not validated yet "
                                          'but not blocked: ' + ', '.join(idle[:8]) + '.')
        lim = []
        for s, h, f in (matched if topic else [(0, [], f) for f in findings]):
            for x in f.get('limitations') or []:
                t = x['text'] if isinstance(x, dict) else str(x)
                if re.search(r'(?i)trial|licen[cs]|entitle|access|authori[sz]', t):
                    lim.append({'finding_id': f['finding_id'], 'title': f.get('title', ''), 'text': t})
        res['limitations'] = lim[:8]
    elif 'LIMITATIONS' in intents:
        for s, h, f in sorted(matched if topic else [(0, [], f) for f in findings], key=lambda x: -x[0])[:6]:
            for x in (f.get('limitations') or [])[:3]:
                res['limitations'].append({'finding_id': f['finding_id'], 'title': f.get('title', ''),
                                           'text': x['text'] if isinstance(x, dict) else str(x)})
        res['findings'] = [_finding_view(f, h, s) for s, h, f in sorted(matched, key=lambda x: -x[0])[:4]]
    else:
        res['findings'] = [_finding_view(f, h, s) for s, h, f in sorted(matched, key=lambda x: -x[0])[:6]]
        res['capabilities'] = [_cap_view(c) for s, h, c in sorted(matched_caps, key=lambda x: -x[0])[:4]]

    # --- what is NOT established: topic words nothing published mentions
    seen = set()
    for s, h, f in scored:
        seen |= set(h)
    for s, h, c in cap_scored:
        seen |= set(h)
    res['not_established'] += [f'Nothing published mentions "{t}".' for t in topic if t not in seen]

    if res['findings'] or res['capabilities'] or res['limitations'] or res['changes']:
        full = bool(res['findings']) and (not topic or any(len(x['matched_terms']) == len(topic) for x in res['findings']))
        best = max([len(x['matched_terms']) / len(topic) for x in res['findings']] or [0]) if topic else 1.0
        res['status'] = 'ANSWERED' if (full or not topic or best >= COVERED) else 'PARTIAL'
        parts = []
        if res['findings']:
            top = res['findings'][0]
            parts.append(f"{len(res['findings'])} published finding(s) address this. The most relevant is "
                         f"\"{top['title']}\" (executed {top['execution_date']}, evidence: {top['evidence_label'] or top['evidence_class']}, "
                         f"validation: {top['validation_status']}; what it supports: {F.TIER_TEXT[top['evidence_tier']]}).")
        if res['capabilities']:
            parts.append(f"{len(res['capabilities'])} related capabilit{'y' if len(res['capabilities']) == 1 else 'ies'} "
                         'in the published capability map.')
        if res['limitations'] and not res['findings']:
            parts.append(f"{len(res['limitations'])} published limitation(s) are relevant.")
        if res['not_established']:
            parts.append('Parts of the question are not covered by published evidence.')
        res['summary'] = ' '.join(parts)
    else:
        res['status'] = 'NOT_ESTABLISHED'
        res['summary'] = ('This has not been established in the published findings. Nothing published matches the '
                          'question closely enough to support an answer, and no answer is guessed.')
    return res
