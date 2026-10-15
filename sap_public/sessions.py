"""Public research notes (knowledge sessions): owner-approved, digest-verified, read-only.

A session is a research article derived from a reviewed master document. It is NOT a sealed-run finding and never
enters the findings pipeline. Content lives in content/sessions/ and is shown only when the exact content digest is
listed in the approval registry (session_approvals.py). The registry is a Python module of the signed package, so
changing it needs a new signed release by the owner's pinned identity; whoever can edit a content file alone cannot
approve it. An `approval` object inside a content file is informational and never authorizes display. Nothing here
executes anything, writes anything or calls the network.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from . import findings as F
from . import session_approvals as A

ROOT = Path(__file__).resolve().parents[1]
SESSIONS_DIR = ROOT / 'content' / 'sessions'
INDEX_SCHEMA = 'sap-public.sessions-index/1'
SESSION_SCHEMA = 'sap-public.session/1'     # views/featured/diagram flags are optional additions; flat sections stay
_ID = re.compile(r'^KS\d{2}$')
_HTTP = re.compile(r'https?://[^\s)>\]|"]+', re.IGNORECASE)   # case-insensitive: HTTPS://x is a link too
ALLOWED_HOSTS = ('developers.sap.com', 'help.sap.com', 'api.sap.com')   # exact hostnames, https only
ALLOWED_GITHUB_PATH = '/SAP-samples/'                                    # host github.com, this path prefix only
# (parts are assembled so this source never carries the private identifiers literally)
_EXTRA_FORBIDDEN = re.compile(r'(?i)(TRL' r'_EN\w*|\bZAI' r'SAP\b|\bZZ[A-Z_]{4,}|sap-client|\.hana\.ondemand\.com|\\repotree|[A-Za-z]:\\|bearer\s+[A-Za-z0-9._-]{12,})')


def url_allowed(url: str) -> bool:
    """https only, exact hostname from the allowlist (or github.com under /SAP-samples/), no credentials, no odd port."""
    try:
        u = urlsplit(url)
        host, port = (u.hostname or ''), u.port
    except ValueError:
        return False
    if u.scheme != 'https' or u.username is not None or u.password is not None or port not in (None, 443):
        return False
    if host in ALLOWED_HOSTS:
        return True
    return host == 'github.com' and u.path.startswith(ALLOWED_GITHUB_PATH)


_TAG = re.compile(r'<\s*[/!?]?\s*[A-Za-z]')                       # raw HTML, HTML comments and <autolinks>
_ENTITY = re.compile(r'&(?:#[0-9]+|#[xX][0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]*);|&(?:lt|gt|quot)\b')
_INLINE_DEST = re.compile(r'\]\(\s*(<[^>\n]*>?|[^\s)]*)')           # [text](dest "title") and ![alt](dest)
_REF_DEF = re.compile(r'(?m)^[ ]{0,3}\[[^\]\n]+\]:[ \t]*(<[^>\n]*>?|\S*)')   # [label]: dest
_BARE_AUTOLINK = re.compile(r'(?i)(?<![A-Za-z0-9])www\.|[A-Za-z0-9._+-]+@[A-Za-z0-9-]+\.[A-Za-z]')


def _dest_ok(dest: str) -> bool:
    """A Markdown link destination is acceptable only as an allowlisted absolute https URL (or a same-page #anchor)."""
    d = dest.strip()
    if d.startswith('<'):
        d = d[1:].rstrip('>')
    if re.search(r'[\x00-\x20\x7f\\]', d) or '%' in d.split('#', 1)[0].replace('%20', ''):
        return False                                                 # control, space, backslash or percent-encoded
    return d.startswith('#') and len(d) > 1 or url_allowed(d)


def markdown_link_problems(text: str) -> list[str]:
    """Reasons this Markdown could render a link or image outside the host policy (empty list = acceptable).

    Deliberately conservative: raw HTML, entity-obfuscated text, www./e-mail autolinks and any link or image
    destination (inline or reference-style) that is not an allowlisted absolute https URL are all refused.
    """
    out = []
    if _TAG.search(text):
        out.append('raw HTML or autolink markup')
    if any(m.group(0) != '&amp;' for m in _ENTITY.finditer(text)):
        out.append('HTML entity form')
    if _BARE_AUTOLINK.search(text):
        out.append('www or e-mail autolink')
    for rx in (_INLINE_DEST, _REF_DEF):
        for m in rx.finditer(text):
            if not _dest_ok(m.group(1)):
                out.append('Markdown destination outside the allowed hosts')
                break
    return out


def _str(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def schema_problems(doc: dict) -> list[str]:
    """Element-level schema: the renderer calls .get() on these, so every element must be a dict of strings."""
    out = []
    for name, req in (('sections', ('key', 'title', 'markdown')), ('claims', ('claim_id', 'claim')),
                      ('references', ('label', 'url'))):
        v = doc.get(name)
        if v is None and name != 'sections':
            continue
        if not isinstance(v, list) or (name == 'sections' and not v):
            out.append('no sections' if name == 'sections' else f'{name} is not a list')
            continue
        for el in v:
            if not isinstance(el, dict) or not all(_str(el.get(k)) for k in req):
                out.append(f'malformed {name} element')
                break
    for k in ('title', 'subtitle', 'revision', 'date', 'evidence_status', 'lineage_note', 'diagram_caption'):
        if k in doc and not isinstance(doc[k], str):
            out.append(f'{k} is not text')
    views = doc.get('views')
    if views is not None:
        if not isinstance(views, list) or not views or not all(
                isinstance(v, dict) and _str(v.get('key')) and _str(v.get('name')) for v in views):
            out.append('malformed views')
        else:
            keys = [v['key'] for v in views]
            if len(set(keys)) != len(keys):
                out.append('duplicate view key')
            for el in doc.get('sections') or []:
                if isinstance(el, dict) and el.get('view') not in keys:
                    out.append('section names an unknown view')
                    break
    elif any(isinstance(el, dict) and 'view' in el for el in doc.get('sections') or []):
        out.append('sections name a view but no views are declared')
    feat = doc.get('featured')
    if feat is not None and (not isinstance(feat, dict) or not all(_str(feat.get(k)) for k in
                                                                    ('title', 'description', 'action_label'))):
        out.append('malformed featured banner')
    return out


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def digest_of(doc: dict) -> str:
    body = {k: v for k, v in doc.items() if k not in ('approval', 'content_sha256')}
    return hashlib.sha256(canonical(body).encode('utf-8')).hexdigest()


def _strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from _strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from _strings(v)


def problems(doc) -> list[str]:
    """Reasons a session must not be shown (empty list = acceptable). Never raises."""
    if not isinstance(doc, dict):
        return ['not an object']
    out = []
    if doc.get('schema') != SESSION_SCHEMA:
        out.append('unexpected schema')
    if not _ID.match(str(doc.get('session_id', ''))):
        out.append('invalid session id')
    out.extend(schema_problems(doc))
    if digest_of(doc) != doc.get('content_sha256'):
        out.append('content digest mismatch')
    for s in _strings({k: v for k, v in doc.items() if k not in ('approval', 'diagram_svg')}):
        if F.violations(s) or _EXTRA_FORBIDDEN.search(s):
            out.append('non-public text')
            break
        if any(not url_allowed(u) for u in _HTTP.findall(s)):
            out.append('URL outside the allowed hosts')
            break
        if markdown_link_problems(s):
            out.append('Markdown link form outside the allowed hosts')
            break
    for r in doc.get('references') or []:
        if isinstance(r, dict) and isinstance(r.get('url'), str) and not url_allowed(r['url']):
            out.append('reference URL outside the allowed hosts')
            break
    svg = doc.get('diagram_svg')
    if svg is not None and (not isinstance(svg, str) or not svg.lstrip().startswith('<svg') or
                            re.search(r'(?i)<script|on\w+\s*=|javascript:|<foreignObject|href\s*=\s*["\']https?:', svg) or
                            _EXTRA_FORBIDDEN.search(svg)):
        out.append('diagram is not a plain SVG')
    return out


def approved(doc: dict, registry=None) -> bool:
    """True only when the digest of this exact content is listed for this session id in the signed registry."""
    reg = A.APPROVED_CONTENT_SHA256 if registry is None else registry
    sid, dg = doc.get('session_id'), digest_of(doc)
    return isinstance(sid, str) and doc.get('content_sha256') == dg and reg.get(sid) == dg


def load(root: Path | None = None, registry=None) -> dict:
    """Return {'status', 'sessions': [approved and verified docs], 'withheld': [{'session_id','reason'}]}."""
    base = Path(root) if root else SESSIONS_DIR
    idx_path = base / 'index.json'
    if not idx_path.is_file():
        return {'status': 'EMPTY', 'sessions': [], 'withheld': []}
    try:
        idx = json.loads(idx_path.read_text(encoding='utf-8'))
    except ValueError:
        return {'status': 'UNAVAILABLE', 'sessions': [], 'withheld': []}
    if not isinstance(idx, dict) or idx.get('schema') != INDEX_SCHEMA or not isinstance(idx.get('sessions'), list):
        return {'status': 'UNAVAILABLE', 'sessions': [], 'withheld': []}
    shown, withheld = [], []
    for sid in idx['sessions']:
        if not isinstance(sid, str) or not _ID.match(sid):
            withheld.append({'session_id': str(sid)[:12], 'reason': 'invalid id'})
            continue
        try:
            doc = json.loads((base / f'{sid}.json').read_text(encoding='utf-8'))
        except (OSError, ValueError):
            withheld.append({'session_id': sid, 'reason': 'unreadable'})
            continue
        probs = problems(doc)
        if probs:
            withheld.append({'session_id': sid, 'reason': '; '.join(probs)})
        elif not approved(doc, registry):
            withheld.append({'session_id': sid, 'reason': 'not in the signed approval registry'})
        else:
            shown.append(doc)
    return {'status': 'OK' if shown else 'EMPTY', 'sessions': shown, 'withheld': withheld}


def featured(sessions: list) -> list[dict]:
    """Banner entries of approved sessions that declare `featured`, ordered by featured.order then session id.

    The banner text is the session's own data: featuring KS02 or KS03 means setting `featured` in that session's
    canonical file. There is no separate banner content source and nothing here can show an unapproved session.
    """
    out = []
    for d in sessions:
        f = d.get('featured')
        if isinstance(f, dict):
            out.append({'session_id': d['session_id'], 'label': f'FEATURED KNOWLEDGE SESSION • {d["session_id"]}',
                        'title': f['title'], 'description': f['description'], 'action_label': f['action_label'],
                        'order': f.get('order') if isinstance(f.get('order'), int) else 1000})
    return sorted(out, key=lambda e: (e['order'], e['session_id']))


def blocks(markdown: str) -> list[tuple]:
    """Split Markdown into ('text', str) and ('table', header, rows) so tables scroll inside their own widget."""
    lines = markdown.split('\n')
    out, buf, i = [], [], 0

    def flush():
        nonlocal buf
        s = '\n'.join(buf).strip()
        if s:
            out.append(('text', s))
        buf = []

    while i < len(lines):
        ln = lines[i]
        if ln.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|$', lines[i + 1].strip()):
            flush()
            header = [c.strip() for c in ln.strip().strip('|').split('|')]
            j, rows = i + 2, []
            while j < len(lines) and lines[j].startswith('|'):
                rows.append([c.strip() for c in lines[j].strip().strip('|').split('|')])
                j += 1
            out.append(('table', header, rows))
            i = j
        else:
            buf.append(ln)
            i += 1
    flush()
    return out
