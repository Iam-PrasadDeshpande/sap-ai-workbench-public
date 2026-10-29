"""Build the read-only site's SHA-256 release manifest; no signing or network access."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_SUFFIXES = ('.py', '.json', '.csv', '.toml', '.txt', '.md')
EXCLUDED_DIRS = ('__pycache__', 'tests', '.git', 'content')


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_of(files: dict[str, str]) -> str:
    return sha256(''.join(f'{path}\t{value}\n' for path, value in sorted(files.items())).encode('utf-8'))


def git_head(root: Path) -> str:
    result = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], check=True,
                            capture_output=True, text=True, encoding='utf-8')
    value = result.stdout.strip()
    if not re.fullmatch(r'[0-9a-f]{40}', value):
        raise ValueError('could not resolve a full Git commit id')
    return value


def build_manifest(root: Path, source_commit: str) -> dict:
    root = Path(root).resolve()
    if not re.fullmatch(r'[0-9a-f]{40}', source_commit):
        raise ValueError('source_commit must be a full lowercase Git commit id')

    from sap_public import integrity, sessions
    documents = sessions.load(root / 'content' / 'sessions')
    expected_ids = {'KS01', 'KS04', 'KS05', 'KS07'}
    if documents['withheld'] or {d.get('session_id') for d in documents['sessions']} != expected_ids:
        raise ValueError('refusing to build: all expected owner-approved sessions must validate and load')

    code_files = integrity.scan(root)
    for name in code_files:
        path = Path(name)
        if path.suffix not in ALLOWED_SUFFIXES or (path.suffix == '.md' and name != 'README.md'):
            raise ValueError(f'refusing non-allowlisted public file: {name}')
        if any(part in EXCLUDED_DIRS for part in path.parts):
            raise ValueError(f'refusing excluded path in public inventory: {name}')

    content_files = {}
    for path in sorted((root / 'content').rglob('*'), key=lambda item: item.relative_to(root).as_posix()):
        if not path.is_file() or path.suffix == '.pyc' or '__pycache__' in path.parts:
            continue
        name = path.relative_to(root).as_posix()
        if path.suffix not in ALLOWED_SUFFIXES:
            raise ValueError(f'refusing non-allowlisted content file: {name}')
        content_files[name] = sha256(path.read_bytes())

    release = json.loads((root / 'data' / 'release.json').read_text(encoding='utf-8'))
    content_index = json.loads((root / 'content' / 'index.json').read_text(encoding='utf-8'))
    requirements = (root / 'requirements.txt').read_text(encoding='utf-8')
    pins = [line.strip() for line in requirements.splitlines() if line.strip() and not line.lstrip().startswith('#')]
    if len(pins) != 1 or not re.fullmatch(r'streamlit==\d+\.\d+\.\d+', pins[0]):
        raise ValueError('expected one exact Streamlit dependency pin')

    return {
        'schema': 'sap-public.artifact-manifest/1',
        'edition': 'PUBLIC_INTERACTIVE',
        'version': release['version'],
        'source_commit': source_commit,
        'built_by': 'scripts/build_public_manifest.py',
        'allowlist': {'suffixes': list(ALLOWED_SUFFIXES), 'excluded_dirs': ['__pycache__', 'tests'],
                      'entry_point': 'app.py'},
        'dependency': {'requirements_txt_sha256': sha256(requirements.encode('utf-8')), 'pins': pins},
        'files': [{'path': name, 'sha256': value} for name, value in sorted(code_files.items())],
        'file_count': len(code_files),
        'artifact_digest': digest_of(code_files),
        'content_at_build': {
            'files': [{'path': name, 'sha256': value} for name, value in sorted(content_files.items())],
            'content_digest': digest_of(content_files),
            'current_release': content_index.get('current'),
            'current_release_digest': content_index.get('current_digest'),
            'releases': len(content_index.get('releases', [])),
        },
    }


def write_manifest(root: Path, source_commit: str) -> dict:
    root = Path(root).resolve()
    manifest = build_manifest(root, source_commit)
    target = root / 'PUBLIC_MANIFEST.json'
    temp = target.with_suffix('.json.tmp')
    temp.write_text(json.dumps(manifest, indent=1, sort_keys=True) + '\n', encoding='utf-8', newline='\n')
    temp.replace(target)
    return manifest


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--source-commit', help='commit whose application files are being attested; defaults to HEAD')
    args = parser.parse_args(argv)
    root = args.root.resolve()
    sys.path.insert(0, str(root))
    commit = args.source_commit or git_head(root)
    manifest = write_manifest(root, commit)
    print(json.dumps({'status': 'BUILT', 'source_commit': commit,
                      'artifact_digest': manifest['artifact_digest'],
                      'content_digest': manifest['content_at_build']['content_digest'],
                      'file_count': manifest['file_count']}, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
