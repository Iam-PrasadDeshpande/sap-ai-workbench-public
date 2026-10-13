"""SAP AI capability evaluations for the public site: the generated canonical catalog joined with the evaluations of
the verified, owner-approved content release. Pure data, no Streamlit, no network.

A capability without a published evaluation is shown at documentation level from its official reference: listed is
never presented as executed, and missing evidence is "not yet evaluated hands-on", never a negative result.
"""
from __future__ import annotations

from . import catalog
from . import findings as F

LIFECYCLE = ('Official SAP developer sources', 'Capability discovery', 'Classification',
             'Engineering relevance & maturity assessment', 'Authorized hands-on execution', 'Validated receipts',
             'Evidence-based comparison', 'Public-safe evaluation projection', 'Owner-controlled publication',
             'Engineering adoption insights')

LEVEL_TEXT = {
    'NOT_ASSESSED': 'Not assessed',
    'INSUFFICIENT_EVIDENCE': 'Insufficient evidence',
    'DOCUMENTATION_ONLY': 'Documentation only',
    'LOCAL_VALIDATION_ONLY': 'Local validation only',
    'SYSTEM_VALIDATION_AVAILABLE': 'SAP system validation available',
}
LEVEL_COLOR = {'SYSTEM_VALIDATION_AVAILABLE': 'green', 'LOCAL_VALIDATION_ONLY': 'green', 'DOCUMENTATION_ONLY': 'blue',
               'INSUFFICIENT_EVIDENCE': 'orange', 'NOT_ASSESSED': 'gray'}
EXECUTION_TEXT = {
    'OPERATION_VERIFIED': ('VERIFIED', 'green', 'Tool operation executed in published evidence; checks passed'),
    'DISCOVERY_ONLY': ('DISCOVERY ONLY', 'blue', 'The tool listed its operations; no operation was validated'),
    'NOT_YET_TESTED': ('NOT YET EVALUATED', 'gray', 'No published hands-on evidence yet'),
    'NO_QUALIFYING_RUN': ('NOT YET EVALUATED', 'gray', 'No published hands-on evidence yet'),
    'NO_EXPERIMENT': ('NO EXPERIMENT', 'gray', 'No hands-on experiment exists for this tool yet'),
    'NOT_APPLICABLE': ('NOT APPLICABLE', 'gray', 'No programmatic interface to evaluate'),
    'LATEST_RUN_FAILED': ('NOT ESTABLISHED', 'orange', 'Not established in published evidence'),
    'RECEIPT_UNVERIFIABLE': ('NOT ESTABLISHED', 'orange', 'Not established in published evidence'),
}
TIER_TEXT = {
    'DOCUMENTATION_RETRIEVED': 'Documentation retrieved (what SAP publishes; nothing executed in an SAP system)',
    'LOCAL_EXECUTION_VALIDATED': 'Executed and validated locally (not in an SAP system)',
    'SAP_SYSTEM_READBACK_VALIDATED': 'Validated by reading back from an SAP system',
    'NOT_ESTABLISHED': 'Not established',
    'AUTHORIZATION_BLOCKED': 'Blocked: needs an SAP entitlement, trial or licence',
}
EVIDENCE_FILTERS = ('All evidence levels', 'Hands-on evidence published', 'Documentation only', 'Not assessed')
SOURCE_TEXT = {'REFERENCE_REACHABLE': 'Official reference reachable on {d} (a source check, not an execution)',
               'REFERENCE_NOT_CHECKABLE': 'Official reference could not be checked automatically',
               'NOT_CHECKED': 'Official reference not checked', 'NO_REFERENCE': 'No official reference recorded'}


def _default(cap: dict, data: dict) -> dict:
    """Documentation-level evaluation for a catalog entry with no published evidence (mirrors the private rules)."""
    ref = cap.get('sap_source_reference')
    doc = 'DOCUMENTATION_ONLY' if ref else 'NOT_ASSESSED'
    src = cap.get('source_check') or {}
    dims = {}
    for key, _label in data.get('dimensions') or []:
        dims[key] = {'level': 'NOT_ASSESSED', 'statement': 'Not assessed: no published hands-on evidence.',
                     'basis': 'NOT_ASSESSED'}
    if 'official_availability' in dims:
        dims['official_availability'] = {'level': doc, 'statement': source_text(src) if ref else 'No official reference.',
                                         'basis': 'SOURCE' if src.get('state') == 'REFERENCE_REACHABLE' else 'NOT_ASSESSED'}
    if 'accessibility' in dims:
        dims['accessibility'] = {'level': doc, 'statement': 'Stated requirement (not tested): '
                                 + str(cap.get('access_requirements', '')), 'basis': 'SOURCE'}
    return {'capability_id': cap['capability_id'], 'evidence_level': doc, 'dimensions': dims,
            'components': [{'key': k, 'name': k, 'last_execution_status': 'NOT_YET_TESTED',
                            'evidence_tier': 'NOT_ESTABLISHED', 'run_id': None} for k in cap.get('components') or []],
            'published': False}


_MAP_STATUS = {'VALIDATED_HANDS_ON': 'OPERATION_VERIFIED', 'READ_ONLY_LISTING_VALIDATED': 'OPERATION_VERIFIED',
               'DOCUMENTATION_RETRIEVED': 'OPERATION_VERIFIED', 'DISCOVERY_ONLY': 'DISCOVERY_ONLY',
               'NO_PROGRAMMATIC_INTERFACE': 'NOT_APPLICABLE'}
_TIER_LEVEL = {'DOCUMENTATION_RETRIEVED': 'DOCUMENTATION_ONLY', 'LOCAL_EXECUTION_VALIDATED': 'LOCAL_VALIDATION_ONLY',
               'SAP_SYSTEM_READBACK_VALIDATED': 'SYSTEM_VALIDATION_AVAILABLE'}
_ORDER = ('NOT_ASSESSED', 'INSUFFICIENT_EVIDENCE', 'DOCUMENTATION_ONLY', 'LOCAL_VALIDATION_ONLY',
          'SYSTEM_VALIDATION_AVAILABLE')


def _from_capability_map(ev: dict, cap: dict, mapped: dict) -> dict:
    """Content published before R8 carries only the per-tool capability map. Use it with the same rules, so an older
    release still shows its published component statuses (and a level never above them)."""
    comps, best, discovery = [], None, False
    for key in cap.get('components') or []:
        m = mapped.get(key)
        if not m:
            comps.append({'key': key, 'name': key, 'last_execution_status': 'NOT_YET_TESTED',
                          'evidence_tier': 'NOT_ESTABLISHED', 'run_id': None})
            continue
        tier = F.capability_tier(m)
        status = _MAP_STATUS.get(m.get('status'), 'NOT_YET_TESTED')
        comps.append({'key': key, 'name': m.get('name', key), 'last_execution_status': status, 'evidence_tier': tier,
                      'run_id': None, 'executed_on': m.get('validated_on'), 'operations': list(m.get('invocations') or []),
                      'not_proven': m.get('note', '')})
        discovery = discovery or status == 'DISCOVERY_ONLY'
        lvl = _TIER_LEVEL.get(tier) if status == 'OPERATION_VERIFIED' else None
        if lvl and (best is None or _ORDER.index(lvl) > _ORDER.index(best)):
            best = lvl
    # same rule as the private assessment: the strongest verified tier, else discovery-only is insufficient evidence
    level = best or ('INSUFFICIENT_EVIDENCE' if discovery else ev['evidence_level'])
    return {**ev, 'components': comps, 'evidence_level': level}


def source_text(src: dict) -> str:
    return SOURCE_TEXT.get(src.get('state'), SOURCE_TEXT['NOT_CHECKED']).format(d=src.get('last_checked') or '?')


def evaluated(release: dict) -> tuple[dict, list[dict]]:
    """-> (catalog data, [capability + its evaluation]) in catalog order. Published evaluations win; a published
    evaluation for an id not in the catalog is ignored (the catalog defines the identities)."""
    data = catalog.capabilities()
    pub = {e.get('capability_id'): e for e in release.get('evaluations') or [] if isinstance(e, dict)}
    mapped = {c.get('key'): c for c in release.get('capabilities') or [] if isinstance(c, dict)}
    out = []
    for cap in data['capabilities']:
        ev = pub.get(cap['capability_id'])
        if ev:
            ev = {**ev, 'published': True}
        else:
            ev = _default(cap, data)
            if mapped and set(cap.get('components') or []) & set(mapped):
                ev = _from_capability_map(ev, cap, mapped)
        out.append({**cap, 'evaluation': ev})
    return data, out


def has_hands_on(item: dict) -> bool:
    return item['evaluation'].get('evidence_level') in ('LOCAL_VALIDATION_ONLY', 'SYSTEM_VALIDATION_AVAILABLE')


def matches(item: dict, evidence_filter: str) -> bool:
    lvl = item['evaluation'].get('evidence_level')
    if evidence_filter == 'Hands-on evidence published':
        return has_hands_on(item)
    if evidence_filter == 'Documentation only':
        return lvl == 'DOCUMENTATION_ONLY'
    if evidence_filter == 'Not assessed':
        return lvl in ('NOT_ASSESSED', 'INSUFFICIENT_EVIDENCE')
    return True


def coverage(items: list[dict]) -> dict:
    return {'total': len(items), 'hands_on': sum(1 for i in items if has_hands_on(i)),
            'documentation': sum(1 for i in items if i['evaluation'].get('evidence_level') == 'DOCUMENTATION_ONLY'),
            'by_category': {k: sum(1 for i in items if i['category'] == k) for k in catalog.CATEGORIES}}


def priorities(items: list[dict], n: int = 3) -> list[dict]:
    """Next validation priorities: capabilities without hands-on evidence whose next action needs no SAP entitlement
    first (local, owner-authorizable experiments). A plan, never a result."""
    rank = {'NOT_REQUIRED': 0, 'NOT_DETERMINED': 1, 'REQUIRED': 2}
    todo = [i for i in items if not has_hands_on(i) and i.get('components')]
    todo.sort(key=lambda i: (rank.get(i.get('sap_entitlement'), 1), i['capability_id']))
    return todo[:n]
