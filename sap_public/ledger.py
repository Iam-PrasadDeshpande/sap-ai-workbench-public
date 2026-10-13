"""Experiment D: session evidence ledger. The public edition can only mint non-authoritative evidence.

The ledger lives in the visitor's session only. It never becomes a record of authority: SAP trial and enterprise
readback, and local framework execution, are refused here by construction.
"""
from __future__ import annotations

from datetime import datetime, timezone

from .contract import (
    CLAIM_REQUIREMENTS,
    CLAIM_TEXT,
    EVIDENCE_CLASSES,
    EVIDENCE_TEXT,
    LIMITS,
    MINTABLE_EVIDENCE,
    NOT_CREATABLE_PUBLICLY,
)
from .safety import clean_text


class EvidenceRefused(PermissionError):
    pass


def new_entry(kind: str, title: str, evidence_class: str, summary: str, *, source: str = '', limitations: str = '',
              details: dict | None = None, clock=None) -> dict:
    if evidence_class not in EVIDENCE_CLASSES:
        raise EvidenceRefused('unknown evidence class')
    if evidence_class in NOT_CREATABLE_PUBLICLY:
        raise EvidenceRefused(f'{evidence_class} cannot be created in the public edition: it needs a private '
                              'environment and owner authority')
    if evidence_class not in MINTABLE_EVIDENCE:
        raise EvidenceRefused('evidence class not permitted')
    stamp = (clock or (lambda: datetime.now(timezone.utc)))().isoformat(timespec='seconds')
    return {'kind': clean_text(kind, 40), 'title': clean_text(title, 140), 'evidence_class': evidence_class,
            'summary': clean_text(summary, 400), 'source': clean_text(source, 300),
            'limitations': clean_text(limitations, 300), 'recorded_at': stamp,
            'details': {str(k)[:40]: clean_text(v, 200) for k, v in (details or {}).items()}}


def add(ledger: list, entry: dict) -> list:
    """Append within the bound. Returns a new list so callers never share mutable state across sessions."""
    if entry.get('evidence_class') not in MINTABLE_EVIDENCE:
        raise EvidenceRefused('only publicly creatable evidence may be added')
    out = list(ledger)[-(LIMITS['ledger_max_entries'] - 1):] + [entry]
    return out


def classes_present(ledger: list) -> set:
    return {e['evidence_class'] for e in ledger if e.get('evidence_class') in MINTABLE_EVIDENCE}


def assess_claim(ledger: list, claim_id: str) -> dict:
    """Deterministic: which evidence classes this claim needs, which the ledger has, and what is missing."""
    if claim_id not in CLAIM_REQUIREMENTS:
        raise KeyError(claim_id)
    needs = CLAIM_REQUIREMENTS[claim_id]
    have = classes_present(ledger)
    public_possible = [c for c in needs if c in MINTABLE_EVIDENCE]
    met = bool(needs) and all(c in have for c in needs if c in MINTABLE_EVIDENCE) and len(public_possible) == len(needs)
    # Claims whose proof class cannot be created publicly are never "supported" here, whatever the ledger holds.
    if len(public_possible) != len(needs):
        status = 'CANNOT_BE_PROVEN_HERE'
    elif claim_id == 'EXISTS_IN_SAP_DOCS':
        status = 'SUPPORTED' if ('PUBLIC_SAP_API' in have or 'DOCUMENTATION' in have) else 'NOT_YET_SUPPORTED'
    else:
        status = 'SUPPORTED' if met else 'NOT_YET_SUPPORTED'
    return {'claim_id': claim_id, 'claim': CLAIM_TEXT[claim_id], 'status': status,
            'needs': [{'class': c, 'label': EVIDENCE_TEXT[c][0], 'present': c in have,
                       'creatable_here': c in MINTABLE_EVIDENCE} for c in needs],
            'explanation': {
                'SUPPORTED': 'The ledger holds evidence of the kind this claim needs (still a public-edition result).',
                'NOT_YET_SUPPORTED': 'Run the relevant exercise to add evidence of the required kind.',
                'CANNOT_BE_PROVEN_HERE': 'This claim needs evidence that only a private environment with an authorised '
                                         'SAP system can produce. The public edition will never mark it proven.'}[status]}
