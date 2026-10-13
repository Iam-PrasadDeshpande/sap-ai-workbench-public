"""Experiment B: evidence-labelled, qualitative architecture comparison. No scores, no prices, no percentages."""
from __future__ import annotations

import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data' / 'comparison.json'
BASES = ('DOCUMENTATION', 'PROJECT_TEST_OBSERVATION')
BASIS_TEXT = {'DOCUMENTATION': 'Published documentation or general reasoning',
              'PROJECT_TEST_OBSERVATION': ('Observed in the project''s own test runs in the private edition (assistant-run under '
                                 'owner authorization; not independently verified, not reproducible here)')}


def load(path: Path = DATA) -> dict:
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    validate(data)
    return data


def validate(data: dict) -> None:
    """Fail loudly if the curated data breaks the rules: allowed bases, https sources, no invented numbers."""
    facets = {k for k, _ in data['facets']}
    for pair in data['pairs']:
        ids = {o['id'] for o in pair['options']}
        for o in pair['options']:
            if set(o['cells']) != facets:
                raise ValueError(f"{pair['id']}/{o['id']}: facets incomplete")
            for k, c in o['cells'].items():
                if c['basis'] not in BASES:
                    raise ValueError(f"{pair['id']}/{o['id']}/{k}: unknown basis")
                if c['source'] and not c['source'].startswith('https://'):
                    raise ValueError(f"{pair['id']}/{o['id']}/{k}: source must be https")
                if re.search(r'\d+\s*%|\$\s*\d|€\s*\d|\bUSD\b|\bEUR\s*\d', c['text']):
                    raise ValueError(f"{pair['id']}/{o['id']}/{k}: numeric score or price is not allowed")
        for p in pair['priorities']:
            if p['favors'] not in ids:
                raise ValueError(f"{pair['id']}: priority favors an unknown option")


def pair_by_id(data: dict, pair_id: str) -> dict:
    for p in data['pairs']:
        if p['id'] == pair_id:
            return p
    raise KeyError(pair_id)


def assess(pair: dict, selected_priorities: list) -> dict:
    """Qualitative lean from the visitor's own priorities. It is a transparent tally, not a score or a verdict."""
    chosen = [p for p in pair['priorities'] if p['id'] in set(selected_priorities)]
    tally = {o['id']: [] for o in pair['options']}
    for p in chosen:
        tally[p['favors']].append(p)
    ranked = sorted(tally.items(), key=lambda kv: -len(kv[1]))
    if not chosen:
        lean, why = 'NO_PRIORITIES', 'Select the priorities that apply to you.'
    elif len(ranked) > 1 and len(ranked[0][1]) == len(ranked[1][1]):
        lean, why = 'DEPENDS', 'Your priorities point equally to more than one option; validate both.'
    else:
        lean, why = ranked[0][0], f'{len(ranked[0][1])} of your {len(chosen)} priorities point to this option.'
    names = {o['id']: o['name'] for o in pair['options']}
    lowest = [o for o in pair['options']]
    return {
        'pair_id': pair['id'], 'title': pair['title'], 'lean': lean, 'lean_name': names.get(lean, ''),
        'why': why, 'reasons': [{'option': names[k], 'priority': p['text'], 'because': p['because']}
                                for k, ps in tally.items() for p in ps],
        'caveat': ('This is a qualitative tally of your stated priorities against documented facts or observations from the project\'s own test runs. '
                   'It is not a score, a feasibility figure or a recommendation to buy.'),
        'required_validation': [o['cells']['next_step']['text'] for o in lowest],
        'evidence_class': 'DOCUMENTATION',
        'options': [o['id'] for o in pair['options']]}
