"""Experiment A: SAP developer knowledge investigation against SAP's public developer MCP servers.

A structurally successful MCP response is NOT reported as a useful or correct answer: transport, shape, relevance and
grounding are separate layers, and usefulness is left to the visitor.
"""
from __future__ import annotations

import re
import time
from datetime import datetime, timezone

from .contract import ALLOWED_SOURCE_HOST, LIMITS
from .mcp import McpError, PublicMcpClient
from .relevance import assess_sources
from .safety import clean_text, https_url_on

SEARCH = 'https://developers.sap.com/mcp/search'
GRAPH = 'https://developers.sap.com/mcp/graph'
TECH_NEXT = (
    (r'\bcap\b|cds|odata|node\.?js', 'synthetic-lab',
     'Run the synthetic billing lab to see how a CAP-style service exposes records to people and agents.'),
    (r'\babap\b|\brap\b|adt', 'architecture-comparison',
     'Compare ABAP RAP with CAP for an AI-enabled application before choosing where to start.'),
    (r'\bfiori\b|ui5|frontend|\bui\b', 'architecture-comparison',
     'Compare SAPUI5/Fiori with a generic front end for the same scenario.'),
)


def normalize_question(question) -> str:
    q = clean_text(question, LIMITS['question_max_chars'])
    if len(q) < 8:
        raise ValueError('Please enter a question of at least 8 characters.')
    return q


def _sources_from_search(structured) -> list:
    rows = structured.get('result') if isinstance(structured, dict) else None
    out = []
    for item in rows if isinstance(rows, list) else []:
        if not isinstance(item, dict):
            continue
        url = str(item.get('url') or '')
        if url.startswith('/'):
            url = f'https://{ALLOWED_SOURCE_HOST}{url}'
        out.append({'title': str(item.get('title', ''))[:160], 'url': url, 'score': item.get('score'),
                    'slug': str(item.get('slug', ''))[:120], 'snippet': str(item.get('snippet', ''))[:300]})
    return out


def investigate(question: str, *, client_factory=PublicMcpClient, clock=time.time) -> dict:
    """Run the bounded lookup. Raises ValueError for a bad question; network trouble is returned as a failed result."""
    q = normalize_question(question)
    started = datetime.fromtimestamp(clock(), timezone.utc).isoformat(timespec='seconds')
    calls, sources, concepts, layers_notes = [], [], [], []
    failure = ''
    try:
        search = client_factory(SEARCH)
        search.connect()
        r1 = search.call('semantic_search', {'query': q, 'topK': 5})
        calls.append(r1)
        sources = _sources_from_search(r1['structured'])
        r2 = search.call('search_tutorials', {'query': q, 'limit': 5})
        calls.append(r2)
        graph = client_factory(GRAPH)
        graph.connect()
        r3 = graph.call('kg_search_concepts', {'query': q, 'maxConcepts': 5, 'maxTutorials': 5})
        calls.append(r3)
        res = (r3['structured'] or {}).get('result', {}) if isinstance(r3['structured'], dict) else {}
        concepts = [c for c in (res.get('concepts') or []) if isinstance(c, dict)][:6]
        for t in res.get('tutorials') or []:
            if isinstance(t, dict) and t.get('slug'):
                sources.append({'title': str(t.get('title', ''))[:160],
                                'url': f"https://{ALLOWED_SOURCE_HOST}/tutorials/{str(t['slug'])[:120]}",
                                'score': t.get('score'), 'slug': str(t['slug'])[:120], 'snippet': ''})
    except McpError as exc:
        failure = clean_text(str(exc), 160)
    uniq = list({s['url']: s for s in sources if https_url_on(ALLOWED_SOURCE_HOST, s['url'])}.values())
    assessed = assess_sources(q, uniq)[: LIMITS['sources_shown']]
    for a in assessed:
        a['url'] = https_url_on(ALLOWED_SOURCE_HOST, a['url'])
    good = [a for a in assessed if a['relevance'] != 'WEAK']
    layers = [
        {'layer': 'TRANSPORT_SUCCESS', 'status': 'PASSED' if calls and not failure and all(c['ok'] for c in calls) else
         ('FAILED' if failure or calls else 'NOT_ASSESSED'), 'detail': f'{sum(1 for c in calls if c["ok"])} of {len(calls)} calls succeeded'},
        {'layer': 'SCHEMA_VALIDATION', 'status': 'PASSED' if assessed else 'FAILED',
         'detail': f'{len(assessed)} well-formed sources on {ALLOWED_SOURCE_HOST}'},
        {'layer': 'SOURCE_RELEVANCE', 'status': ('PASSED' if assessed and len(good) == len(assessed) else
                                                 'PARTIAL' if good else 'FAILED' if assessed else 'NOT_ASSESSED'),
         'detail': f'{len(good)} of {len(assessed)} look relevant (term-overlap heuristic, not a judgement)'},
        {'layer': 'ANSWER_GROUNDING', 'status': 'PASSED' if assessed else 'NOT_ASSESSED',
         'detail': 'every reading-path item is a source the tools returned; this does not make the advice correct'},
        {'layer': 'OWNER_USEFULNESS', 'status': 'AWAITING_YOU',
         'detail': 'only you can judge whether this answers your engineering question'}]
    nxt = [{'exercise': ex, 'suggestion': msg} for pat, ex, msg in TECH_NEXT if re.search(pat, q.lower())]
    return {
        'question': q, 'retrieved_at': started, 'ok': bool(assessed) and not failure, 'failure': failure,
        'evidence_class': 'PUBLIC_SAP_API' if assessed else 'DOCUMENTATION',
        'sources': assessed,
        'concepts': [{'name': clean_text(c.get('name') or c.get('slug') or '', 120),
                      'url': f"https://{ALLOWED_SOURCE_HOST}/concepts/{clean_text(c.get('slug') or '', 80)}"}
                     for c in concepts if c.get('slug')],
        'layers': layers, 'notes': layers_notes,
        'missing_evidence': ['Nothing here shows that the technique works in your system.',
                             'No SAP system was contacted; only SAP\'s public developer content was searched.'],
        'next': nxt[:2] or [{'exercise': 'architecture-comparison',
                             'suggestion': 'Compare two SAP approaches for your scenario next.'}],
        'limitations': 'Public anonymous best-effort service; results can change and may be incomplete.'}
