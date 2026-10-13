"""Display-time text hygiene and deterministic source-relevance assessment.

Nothing here rewrites stored data or sealed receipts and nothing here is AI reasoning. Relevance is a transparent
term-overlap heuristic plus a low-signal page-type rule; it is shown as a heuristic, never as proof of usefulness.
"""
from __future__ import annotations

import re
import unicodedata

REPLACEMENT = '�'
MARKER = '[unreadable]'
_STOP = frozenset('''a an and are as at be but by can could do does for from has have how i if in into is it its of on or
our should so than that the their then there these this to up use used using was we what when where which who why will
with would you your available about over under per via'''.split())
_LOW_SIGNAL = re.compile(r'\b(validation|quiz|survey|badge|assessment|week\s*\d+|devtoberfest|leaderboard|giveaway)\b', re.I)
LABELS = ('STRONG', 'MODERATE', 'WEAK')


def normalize_text(value, limit: int = 600) -> tuple[str, dict]:
    """NFC-normalize, drop control characters, replace runs of U+FFFD with a visible marker. Returns (text, info)."""
    text = str(value or '')
    lost = len(re.findall(f'{REPLACEMENT}+', text))
    chars = text.count(REPLACEMENT)
    text = re.sub(f'{REPLACEMENT}+', MARKER, text)
    text = unicodedata.normalize('NFC', text)
    text = ''.join(ch if (ch.isprintable() or ch in '\n\t') else ' ' for ch in text)
    text = re.sub(r'[ \t]+', ' ', text).strip()
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + '…'
    return text, {'unreadable_runs': lost, 'unreadable_characters': chars}


def _stem(w: str) -> str:
    for suf in ('ing', 'ies', 'es', 's'):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[: -len(suf)] + ('y' if suf == 'ies' else '')
    return w


def terms(text: str) -> set[str]:
    words = re.findall(r'[a-z0-9]+', str(text).lower().replace('-', ' '))
    return {_stem(w) for w in words if len(w) >= 3 and w not in _STOP}


def assess_source(question: str, source: dict) -> dict:
    q = terms(question)
    title, _ = normalize_text(source.get('title', ''), 200)
    snippet, info = normalize_text(source.get('snippet', ''), 400)
    slug = str(source.get('slug', ''))
    hay = terms(f'{title} {slug} {snippet}')
    hit = sorted(q & hay)
    coverage = (len(hit) / len(q)) if q else 0.0
    low_signal = bool(_LOW_SIGNAL.search(f'{title} {slug}'))
    if low_signal:
        label, why = 'WEAK', 'event / quiz / validation style page, not engineering guidance'
    elif coverage >= 0.35:
        label, why = 'STRONG', f'matches {len(hit)} of {len(q)} question terms'
    elif coverage >= 0.15:
        label, why = 'MODERATE', f'matches {len(hit)} of {len(q)} question terms'
    else:
        label, why = 'WEAK', f'matches only {len(hit)} of {len(q)} question terms'
    return {'title': title, 'url': source.get('url', ''), 'slug': slug, 'snippet': snippet,
            'upstream_score': source.get('score'), 'relevance': label, 'reason': why, 'matched_terms': hit,
            'coverage': round(coverage, 2), 'low_signal_page_type': low_signal, 'encoding': info}


def assess_sources(question: str, sources: list[dict]) -> list[dict]:
    """Assessed sources ordered strongest first (stable); original order breaks ties."""
    rank = {name: i for i, name in enumerate(LABELS)}
    scored = [assess_source(question, s) for s in sources if isinstance(s, dict)]
    return [x for _, x in sorted(enumerate(scored), key=lambda t: (rank[t[1]['relevance']], -t[1]['coverage'], t[0]))]


def assurance_layers(*, calls: list[dict], checks: list[dict], receipt_problems: list, assessed: list[dict] | None,
                     has_sources: bool) -> list[dict]:
    """The five separate layers. A passed layer never implies the next one."""
    ok_calls = sum(1 for c in calls if c.get('ok'))
    refused = sum(1 for c in calls if not c.get('ok') and (c.get('refused') or str(c.get('tool_name', '')).split(' ')[0] in ('POST', 'PATCH', 'DELETE', 'PUT')))
    layers = []
    if calls:
        # Deliberately refused write attempts are expected outcomes in the CAP experiment, not transport failures.
        def expected_refusal(c):
            return bool(c.get('refused')) or str(c.get('tool_name', '')).split(' ')[0] in ('POST', 'PATCH', 'DELETE', 'PUT')
        unexpected = [c for c in calls if not c.get('ok') and not expected_refusal(c)]
        layers.append({'layer': 'TRANSPORT_SUCCESS', 'status': 'PASSED' if not unexpected else 'FAILED',
                       'detail': f'{ok_calls} of {len(calls)} calls succeeded' + (f'; {refused} refused as designed' if refused else '')})
    else:
        layers.append({'layer': 'TRANSPORT_SUCCESS', 'status': 'NOT_ASSESSED', 'detail': 'no calls recorded'})
    failed = [c for c in checks if not c.get('passed')]
    layers.append({'layer': 'SCHEMA_VALIDATION',
                   'status': 'PASSED' if (checks and not failed and not receipt_problems) else
                   ('NOT_ASSESSED' if not checks else 'FAILED'),
                   'detail': (f'{len(checks) - len(failed)} of {len(checks)} deterministic checks passed; receipt '
                              + ('intact' if not receipt_problems else 'has problems'))})
    if has_sources and assessed is not None:
        good = [a for a in assessed if a['relevance'] in ('STRONG', 'MODERATE')]
        status = 'PASSED' if assessed and len(good) == len(assessed) else ('PARTIAL' if good else 'FAILED')
        layers.append({'layer': 'SOURCE_RELEVANCE', 'status': status,
                       'detail': f'{len(good)} of {len(assessed)} returned sources look relevant (heuristic term overlap)'})
    else:
        layers.append({'layer': 'SOURCE_RELEVANCE', 'status': 'NOT_APPLICABLE', 'detail': 'this experiment returns no sources'})
    grounding = next((c for c in checks if c.get('name') == 'recommendation_cites_only_returned_sources'), None)
    layers.append({'layer': 'ANSWER_GROUNDING',
                   'status': ('PASSED' if grounding['passed'] else 'FAILED') if grounding else 'NOT_ASSESSED',
                   'detail': ('every citation is a source the tools returned (does not mean the advice is correct)'
                              if grounding else 'no grounding check was recorded for this run')})
    layers.append({'layer': 'OWNER_USEFULNESS', 'status': 'AWAITING_OWNER',
                   'detail': 'only you can judge whether this answered your engineering question'})
    return layers
