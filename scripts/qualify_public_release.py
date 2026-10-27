"""Offline qualification for the public SHA-256 manifest and approved research-note set."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

EXPECTED_APPROVALS = {
    'KS01': 'b3f4da6d43b3e2ab16ecb76ced012dbb7170453c89e669166606b6457c93a82e',
    'KS04': 'c9cd1f31eb0da4c103d24f19cc20183ab06c762d02813282449da8072f5735e1',
    'KS05': 'b0212b3d81a44df957bd7d86c3d4738ad6c42554a4f18122ea3faa39bdb567fc',
}


def digest_of(files: dict[str, str]) -> str:
    body = ''.join(f'{path}\t{value}\n' for path, value in sorted(files.items()))
    return hashlib.sha256(body.encode('utf-8')).hexdigest()


def qualify(root: Path, expected_commit: str) -> dict:
    root = Path(root).resolve()
    sys.path.insert(0, str(root))
    from sap_public import integrity, sessions
    from sap_public.session_approvals import APPROVED_CONTENT_SHA256

    failures = []
    if {key: APPROVED_CONTENT_SHA256.get(key) for key in EXPECTED_APPROVALS} != EXPECTED_APPROVALS:
        failures.append('owner approval registry does not match the approved KS01/KS04/KS05 digests')

    integrity_result = integrity.verify(root)
    if integrity_result.get('status') != 'VERIFIED':
        failures.append(f"application manifest verification failed: {integrity_result.get('problems', [])}")
    manifest = json.loads((root / 'PUBLIC_MANIFEST.json').read_text(encoding='utf-8'))
    if manifest.get('source_commit') != expected_commit:
        failures.append('manifest source_commit does not match the qualified source commit')

    listed_content = {entry['path']: entry['sha256'] for entry in manifest.get('content_at_build', {}).get('files', [])}
    actual_content = {}
    for path in sorted((root / 'content').rglob('*')):
        if path.is_file() and path.suffix != '.pyc' and '__pycache__' not in path.parts:
            actual_content[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    if listed_content != actual_content:
        failures.append('content-at-build inventory does not match the current content files')
    if digest_of(listed_content) != manifest.get('content_at_build', {}).get('content_digest'):
        failures.append('content-at-build digest does not match its inventory')
    if digest_of({entry['path']: entry['sha256'] for entry in manifest.get('files', [])}) != manifest.get('artifact_digest'):
        failures.append('application artifact digest does not match its inventory')

    loaded = sessions.load(root / 'content' / 'sessions')
    shown_ids = {doc.get('session_id') for doc in loaded.get('sessions', [])}
    if loaded.get('withheld') or shown_ids != set(EXPECTED_APPROVALS):
        failures.append(f"session load/approval gate mismatch: shown={sorted(shown_ids)}, withheld={loaded.get('withheld')}")
    for doc in loaded.get('sessions', []):
        sid = doc.get('session_id')
        if sessions.problems(doc):
            failures.append(f'{sid} fails schema, digest, URL or public-content checks')
        if sessions.digest_of(doc) != EXPECTED_APPROVALS.get(sid) or not sessions.approved(doc):
            failures.append(f'{sid} does not match its exact registered approval digest')

    return {
        'status': 'PASS' if not failures else 'FAIL',
        'source_commit': manifest.get('source_commit'),
        'artifact_digest': manifest.get('artifact_digest'),
        'manifest_file_count': len(manifest.get('files', [])),
        'content_file_count': len(actual_content),
        'approved_sessions': sorted(shown_ids),
        'privacy_and_schema_checks': 'PASS' if not failures else 'FAIL',
        'failures': failures,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--source-commit', required=True)
    args = parser.parse_args(argv)
    if not re.fullmatch(r'[0-9a-f]{40}', args.source_commit):
        parser.error('--source-commit must be a full lowercase Git commit id')
    result = qualify(args.root, args.source_commit)
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
