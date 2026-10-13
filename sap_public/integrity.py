"""Public artifact integrity: verify the deployed files against PUBLIC_MANIFEST.json (hash, allowlist, digest).

This is a self-check that detects accidental drift, a partial upload or an unexpected extra file. It is NOT a defence
against someone who controls the deployment (they could change files and the manifest together). It makes no claim
about Windows Authenticode: the public edition has its own release attestation (source commit + artifact digest +
file allowlist + dependency pin), produced by scripts/build_public_artifact.py.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'PUBLIC_MANIFEST.json'
ALLOWED_SUFFIXES = ('.py', '.json', '.csv', '.toml', '.txt', '.md')
IGNORED_DIRS = ('__pycache__', 'tests', '.git', 'content')   # content/ has its own verification (findings.load)


def digest_of(files: dict) -> str:
    lines = ''.join(f'{k}\t{v}\n' for k, v in sorted(files.items()))
    return hashlib.sha256(lines.encode('utf-8')).hexdigest()


def scan(root: Path = ROOT) -> dict:
    """path (posix, relative) -> sha256 for every deployable file under root, excluding the manifest itself."""
    out = {}
    for p in sorted(Path(root).rglob('*')):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if any(part in IGNORED_DIRS for part in rel.parts) or rel.name == MANIFEST or rel.suffix == '.pyc':
            continue
        out[rel.as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def verify(root: Path = ROOT) -> dict:
    mpath = Path(root) / MANIFEST
    if not mpath.exists():
        return {'status': 'NOT_VERIFIED', 'problems': ['no manifest in this checkout (development tree)'], 'digest': ''}
    rec = json.loads(mpath.read_text(encoding='utf-8'))
    want = {f['path']: f['sha256'] for f in rec.get('files', [])}
    have = scan(root)
    problems = []
    for k in sorted(set(want) - set(have)):
        problems.append(f'missing {k}')
    for k in sorted(set(have) - set(want)):
        problems.append(f'unexpected {k}')
    for k in sorted(set(want) & set(have)):
        if want[k] != have[k]:
            problems.append(f'changed {k}')
    for k in have:
        if Path(k).suffix not in ALLOWED_SUFFIXES or (Path(k).suffix == '.md' and k != 'README.md'):   # .md: root README only
            problems.append(f'file type not allowed {k}')
    if digest_of(want) != rec.get('artifact_digest'):
        problems.append('manifest digest does not match its own file list')
    from . import findings
    c = findings.load(Path(root) / 'content')
    return {'status': 'VERIFIED' if not problems else 'FAILED', 'problems': problems[:20],
            'digest': rec.get('artifact_digest', ''), 'version': rec.get('version'),
            'file_count': len(have), 'source_commit': rec.get('source_commit', ''),
            'content': {'status': c['status'], 'version': c['served_version'],
                        'built_with': (rec.get('content_at_build') or {}).get('current_release_digest', '')}}
