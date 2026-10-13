"""Published findings: the only research content the public edition shows, loaded from a versioned, verified bundle.

The public runtime never executes anything to produce a finding and never reads the private workbench. Findings arrive
as plain JSON files under `content/` that the owner's private pipeline projected from sealed experiment receipts and
that passed the owner's publication policy. This module only reads and VERIFIES them:

  content/index.json                 which release is current, plus the history of earlier releases
  content/releases/NNNN.json         one immutable release (all findings visible in that version)

A release is accepted only if its digest matches the index, every finding's own hash matches, the schema is the
expected one and no text field trips the public-side safety scan. A release that fails verification is never shown;
the loader falls back to the newest earlier release that verifies (rollback by construction) and says so.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / 'content'
INDEX_SCHEMA = 'sap-public.content-index/1'
RELEASE_SCHEMA = 'sap-public.content-release/1'
FINDING_SCHEMA = 'sap-public.finding/1'
STALE_AFTER_DAYS = 180
MAX_FINDINGS = 200
MAX_BYTES = 2_000_000

FINDING_STATES = ('PUBLISHED', 'SUPERSEDED', 'RETRACTED')
STATUS_TEXT = {
    'VALIDATED_HANDS_ON': ('Validated hands-on', 'green'),
    'DOCUMENTATION_RETRIEVED': ("SAP's public documentation retrieved; not executed in an SAP system", 'blue'),
    'READ_ONLY_LISTING_VALIDATED': ('Read-only listing validated; SAP object readback not proven', 'blue'),
    'DISCOVERY_ONLY': ('Discovered only; no operation validated', 'blue'),
    'ACCESS_REQUIRED': ('Needs an entitlement or trial that is not available here', 'orange'),
    'NOT_VALIDATED': ('Not validated', 'gray'),
    'NO_PROGRAMMATIC_INTERFACE': ('No programmatic interface found', 'gray'),
}
EVIDENCE_LABEL = {
    'SAP_PUBLIC_API': "Answer retrieved from SAP's public developer service",
    'LOCAL_FRAMEWORK_EXECUTION': 'Executed locally with SAP CAP / Node tooling on synthetic data',
    'LOCAL_MODEL_EXECUTION': 'Executed locally with a model (advisory)',
    'DOCUMENTATION_ONLY': 'Documentation only (nothing proven by execution)',
    'SAP_SANDBOX_MOCK': 'SAP sandbox or mock data',
    'SAP_TRIAL_READBACK': 'Read back from an SAP trial system',
}

# Defense in depth: the private pipeline scans too, but the public runtime never trusts its input.
_FORBIDDEN = (
    re.compile(r'[A-Za-z]:\\'), re.compile(r'(?i)/(home|users)/[^\s]+'), re.compile(r'(?i)\b(bearer|api[_-]?key|secret|password|token)\s*[:=]'),
    # (patterns are assembled from parts so this file itself never contains the literal private identifiers)
    re.compile(r'(?i)\bADT_' r'MCP_' r'TOKEN\b|\bSAP_' r'WB_[A-Z_]+\b'), re.compile(r'\b127\.0\.0\.1\b|\blocalhost\b'),
    re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+'), re.compile(r'(?i)BEGIN (RSA |EC )?PRIVATE KEY'),
    re.compile(r'(?i)\.sql' r'ite\d?\b'),
    re.compile(r'\bTRL' r'_EN\b'),                   # the owner's private SAP destination identifier
    re.compile(r'<\s*script', re.I), re.compile(r'(?i)javascript:'))
_TEXT_FIELDS = ('title', 'technology', 'question', 'objective', 'setup', 'target', 'evidence_label', 'what_it_proves',
                'validation_text')
_LIST_FIELDS = ('verified_observations', 'technical_findings', 'limitations', 'improvements', 'failures')


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def finding_hash(f: dict) -> str:
    return sha256(canonical({k: v for k, v in f.items() if k != 'content_sha256'}))


def release_digest(r: dict) -> str:
    return sha256(canonical({k: v for k, v in r.items() if k != 'digest'}))


def violations(text) -> list[str]:
    s = str(text)
    return [p.pattern[:30] for p in _FORBIDDEN if p.search(s)]


def _walk_text(f: dict):
    for k in _TEXT_FIELDS:
        yield k, f.get(k, '')
    for k in _LIST_FIELDS:
        for i, item in enumerate(f.get(k) or []):
            yield f'{k}[{i}]', item.get('text', '') if isinstance(item, dict) else item
    for s in f.get('sources') or []:
        yield 'sources.title', s.get('title', '')


def check_finding(f) -> list[str]:
    """Problems with one finding (empty list = acceptable)."""
    if not isinstance(f, dict):
        return ['not an object']
    p = []
    if f.get('schema') != FINDING_SCHEMA:
        p.append('unexpected finding schema')
    if not re.fullmatch(r'F[0-9]{4,}-[a-z0-9-]{3,60}', str(f.get('finding_id', ''))):
        p.append('malformed finding id')
    if f.get('state') not in FINDING_STATES:
        p.append('unknown state')
    if f.get('content_sha256') != finding_hash(f):
        p.append('finding hash does not match its content')
    if f.get('state') != 'RETRACTED':
        if f.get('validation_status') not in ('VALIDATED', 'NOT_VALIDATED', 'VALIDATION_FAILED'):
            p.append('unknown validation status')
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(f.get('execution_date', ''))):
            p.append('malformed execution date')
        for url in [s.get('url', '') for s in f.get('sources') or []]:
            if not re.fullmatch(r'https://[a-z0-9.-]+\.sap\.com/[^\s<>"]*', url):
                p.append(f'source url not on an sap.com host: {url[:60]}')
    for name, text in _walk_text(f):
        v = violations(text)
        if v:
            p.append(f'non-public content in {name}')
    return p


def check_release(r) -> list[str]:
    if not isinstance(r, dict):
        return ['release is not an object']
    p = []
    if r.get('schema') != RELEASE_SCHEMA:
        p.append('unexpected release schema')
    if r.get('digest') != release_digest(r):
        p.append('release digest does not match its content')
    if r.get('fixture'):
        p.append('fixture content is not publishable')
    fs = r.get('findings')
    if not isinstance(fs, list) or len(fs) > MAX_FINDINGS:
        p.append('findings missing or too many')
    return p


def _read_json(path: Path):
    if not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise ValueError(f'{path.name}: missing or too large')
    return json.loads(path.read_text(encoding='utf-8'))


def _verify_release_file(root: Path, entry: dict, allow_fixture: bool):
    rel = entry.get('file', '')
    if not re.fullmatch(r'releases/\d{4}\.json', rel):
        raise ValueError('index entry has an unexpected file path')
    r = _read_json(root / rel)
    problems = check_release(r)
    if allow_fixture:
        problems = [x for x in problems if 'fixture' not in x]
    if r.get('digest') != entry.get('digest'):
        problems.append('release digest differs from the index')
    if problems:
        raise ValueError('; '.join(problems))
    return r


PUBLISHED_SOURCE = 'PRIVATE_WORKBENCH_RECEIPTS'

# What a piece of evidence can support, from weakest to strongest. Public documentation retrieval is never execution,
# and local execution is never an SAP system readback.
TIER_TEXT = {
    'DOCUMENTATION_RETRIEVED': "documentation retrieved (shows what SAP publishes; nothing was executed in an SAP system)",
    'LOCAL_EXECUTION_VALIDATED': 'executed and validated locally (not in an SAP system)',
    'SAP_SYSTEM_READBACK_VALIDATED': 'validated by reading back from an SAP system',
    'NOT_ESTABLISHED': 'not established',
    'AUTHORIZATION_BLOCKED': 'blocked: needs an SAP entitlement, trial or licence that is not available',
}
_CLASS_TIER = {'SAP_PUBLIC_API': 'DOCUMENTATION_RETRIEVED', 'DOCUMENTATION_ONLY': 'DOCUMENTATION_RETRIEVED',
               'LOCAL_FRAMEWORK_EXECUTION': 'LOCAL_EXECUTION_VALIDATED', 'LOCAL_MODEL_EXECUTION': 'LOCAL_EXECUTION_VALIDATED',
               'SAP_SANDBOX_MOCK': 'LOCAL_EXECUTION_VALIDATED', 'SAP_TRIAL_READBACK': 'SAP_SYSTEM_READBACK_VALIDATED'}
DOC_CLASSES = ('SAP_PUBLIC_API', 'DOCUMENTATION_ONLY')


def finding_tier(f: dict) -> str:
    if f.get('state') == 'RETRACTED' or f.get('validation_status') != 'VALIDATED':
        return 'NOT_ESTABLISHED'
    return _CLASS_TIER.get(f.get('evidence_class'), 'NOT_ESTABLISHED')


def capability_tier(c: dict) -> str:
    st_ = c.get('status')
    if st_ == 'ACCESS_REQUIRED':
        return 'AUTHORIZATION_BLOCKED'
    if st_ in ('VALIDATED_HANDS_ON', 'READ_ONLY_LISTING_VALIDATED', 'DOCUMENTATION_RETRIEVED'):
        return _CLASS_TIER.get(c.get('evidence_class'), 'NOT_ESTABLISHED')
    return 'NOT_ESTABLISHED'


def _normalize_capability(c: dict) -> dict:
    """P9: a capability 'validated' only by public documentation retrieval is shown as exactly that."""
    if c.get('status') == 'VALIDATED_HANDS_ON' and c.get('evidence_class') in DOC_CLASSES:
        return {**c, 'status': 'DOCUMENTATION_RETRIEVED'}
    return c


def _retractions(root: Path, idx: dict, entries: list) -> dict:
    """Retractions are authoritative across versions: the index's list and every tombstone in ANY release file
    (verified or not) apply to whichever release is served, including a fallback or a rolled-back release. Honouring an
    unverified tombstone can only hide content, never show it."""
    out = {}
    listed = idx.get('retracted')
    if isinstance(listed, dict):
        for fid, info in listed.items():
            out[str(fid)] = info if isinstance(info, dict) else {}
    for e in entries:
        rel = str(e.get('file', ''))
        if not re.fullmatch(r'releases/\d{4}\.json', rel):
            continue
        try:
            r = _read_json(root / rel)
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        for f in (r.get('findings') or []) if isinstance(r, dict) else []:
            if isinstance(f, dict) and f.get('state') == 'RETRACTED' and f.get('finding_id'):
                out.setdefault(str(f['finding_id']), {'retracted_on': f.get('retracted_on'),
                                                      'retraction_reason': f.get('retraction_reason')})
    return out


def _tombstone(f: dict, info: dict) -> dict:
    reason = str(info.get('retraction_reason') or 'Retracted by the research owner.')[:300]
    return {'schema': FINDING_SCHEMA, 'finding_id': f.get('finding_id'), 'state': 'RETRACTED',
            'title': f.get('title', f.get('finding_id')), 'recipe_id': f.get('recipe_id', ''),
            'retracted_on': str(info.get('retracted_on') or '')[:10],
            'retraction_reason': reason if not violations(reason) else 'Retracted by the research owner.'}


def empty_release(note: str = 'No findings have been published yet.') -> dict:
    return {'schema': RELEASE_SCHEMA, 'version': 0, 'published_at': None, 'findings': [], 'capabilities': [],
            'changes': [], 'note': note, 'digest': ''}


def load(root: Path | None = None, *, allow_fixture: bool = False) -> dict:
    """-> {'status': OK|DEGRADED|EMPTY|UNAVAILABLE, 'release': dict, 'problems': [...], 'served_version': int, 'history': [...]}.

    DEGRADED means the newest release failed verification and an earlier verified release is being served instead.
    """
    root = Path(root or CONTENT_DIR)
    try:
        idx = _read_json(root / 'index.json')
        if idx.get('schema') != INDEX_SCHEMA or not isinstance(idx.get('releases'), list):
            raise ValueError('unexpected index schema')
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {'status': 'UNAVAILABLE', 'release': empty_release('Published content is not available right now.'),
                'problems': [f'index: {exc}'], 'served_version': 0, 'history': []}
    entries = sorted([e for e in idx['releases'] if isinstance(e, dict)], key=lambda e: e.get('version', 0), reverse=True)
    wanted = idx.get('current')
    ordered = [e for e in entries if e.get('file') == wanted] + [e for e in entries if e.get('file') != wanted]
    problems = []
    for n, entry in enumerate(ordered):
        try:
            rel = _verify_release_file(root, entry, allow_fixture)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            problems.append(f"release {entry.get('version')}: {exc}")
            continue
        findings, dropped = [], 0
        for f in rel['findings']:
            fp = check_finding(f)
            if fp:
                dropped += 1
                problems.append(f"finding {str(f.get('finding_id', '?'))[:20]}: {fp[0]}")
            else:
                findings.append(f)
        gone = _retractions(root, idx, entries)
        findings = [_tombstone(f, gone[f.get('finding_id')]) if f.get('finding_id') in gone and f.get('state') != 'RETRACTED'
                    else f for f in findings]
        caps = []
        for c in rel.get('capabilities') or []:
            if isinstance(c, dict) and not violations(f"{c.get('name', '')} {c.get('note', '')}"):
                caps.append(_normalize_capability(c))
            else:
                dropped += 1
                problems.append('capability entry with non-public content dropped')
        rel = {**rel, 'findings': findings, 'capabilities': caps}
        status = 'DEGRADED' if n > 0 or dropped else ('OK' if findings or caps else 'EMPTY')
        gone_titles = [str(f.get('title', '')) for f in findings if f.get('state') == 'RETRACTED' and f.get('title')]
        history = [{'version': e.get('version'), 'published_at': e.get('published_at'),
                    'note': ('Release note withheld: it refers to retracted content.'
                             if any(t in str(e.get('note', '')) for t in gone_titles) else e.get('note', ''))}
                   for e in entries]
        return {'status': status, 'release': rel, 'problems': problems, 'served_version': rel.get('version', 0),
                'history': history, 'test_content': rel.get('source') != PUBLISHED_SOURCE}
    return {'status': 'UNAVAILABLE', 'release': empty_release('Published content is not available right now.'),
            'problems': problems or ['no release verified'], 'served_version': 0, 'history': []}


# ---------------------------------------------------------------------------------------------- views
def age_days(f: dict, today: date | None = None) -> int | None:
    try:
        d = datetime.strptime(f['execution_date'], '%Y-%m-%d').date()
    except (KeyError, ValueError):
        return None
    return ((today or datetime.now(timezone.utc).date()) - d).days


def is_stale(f: dict, today: date | None = None) -> bool:
    a = age_days(f, today)
    return a is not None and a > STALE_AFTER_DAYS


def visible(release: dict, include_superseded: bool = True) -> list[dict]:
    out = [f for f in release.get('findings', []) if f.get('state') != 'RETRACTED']
    if not include_superseded:
        out = [f for f in out if f.get('state') == 'PUBLISHED']
    return sorted(out, key=lambda f: (f.get('execution_date', ''), f.get('finding_id', '')), reverse=True)


def retracted(release: dict) -> list[dict]:
    return [f for f in release.get('findings', []) if f.get('state') == 'RETRACTED']


def by_id(release: dict, finding_id: str) -> dict | None:
    return next((f for f in release.get('findings', []) if f.get('finding_id') == finding_id), None)


def comparable(a: dict, b: dict) -> tuple[bool, str]:
    """Two findings are comparable only when they test the same technology under the same evidence class and scope
    and both are validated. Otherwise a comparison would be an opinion, so none is produced."""
    if a.get('state') == 'RETRACTED' or b.get('state') == 'RETRACTED':
        return False, 'one of the findings was retracted'
    for f in (a, b):
        if f.get('validation_status') != 'VALIDATED':
            return False, 'both findings must be validated'
    if a.get('technology') != b.get('technology'):
        return False, 'they evaluate different technologies'
    if a.get('evidence_class') != b.get('evidence_class') or a.get('scope') != b.get('scope'):
        return False, 'they were obtained with a different evidence class or scope'
    return True, 'same technology, evidence class and scope'
