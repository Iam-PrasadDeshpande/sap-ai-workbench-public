from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'scripts'))

from sap_public import integrity, sessions
from sap_public.session_approvals import APPROVED_CONTENT_SHA256
from build_public_manifest import write_manifest


EXPECTED = {
    'KS01': 'b3f4da6d43b3e2ab16ecb76ced012dbb7170453c89e669166606b6457c93a82e',
    'KS04': 'c9cd1f31eb0da4c103d24f19cc20183ab06c762d02813282449da8072f5735e1',
    'KS05': 'b0212b3d81a44df957bd7d86c3d4738ad6c42554a4f18122ea3faa39bdb567fc',
}


class PublicReleaseTests(unittest.TestCase):
    def test_registry_preserves_existing_approvals_and_adds_exact_ks05_digest(self):
        self.assertEqual({key: APPROVED_CONTENT_SHA256.get(key) for key in EXPECTED}, EXPECTED)

    def test_all_three_exactly_approved_sessions_load(self):
        result = sessions.load(ROOT / 'content' / 'sessions')
        self.assertEqual(result['withheld'], [])
        self.assertEqual({doc['session_id'] for doc in result['sessions']}, set(EXPECTED))

    def test_each_approved_session_passes_schema_privacy_and_digest_checks(self):
        result = sessions.load(ROOT / 'content' / 'sessions')
        for doc in result['sessions']:
            with self.subTest(session=doc['session_id']):
                self.assertEqual(sessions.problems(doc), [])
                self.assertEqual(sessions.digest_of(doc), EXPECTED[doc['session_id']])
                self.assertTrue(sessions.approved(doc))

    def test_missing_approval_fails_closed(self):
        doc = json.loads((ROOT / 'content' / 'sessions' / 'KS05.json').read_text(encoding='utf-8'))
        self.assertFalse(sessions.approved(doc, {}))

    def test_changed_note_content_fails_its_digest_check(self):
        doc = json.loads((ROOT / 'content' / 'sessions' / 'KS05.json').read_text(encoding='utf-8'))
        doc['title'] += ' altered'
        self.assertIn('content digest mismatch', sessions.problems(doc))

    def test_current_manifest_verifies(self):
        self.assertEqual(integrity.verify(ROOT)['status'], 'VERIFIED')

    def test_manifest_detects_code_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            clone = Path(temp) / 'site'
            shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns('.git', 'tests', '__pycache__'))
            (clone / 'app.py').write_text((clone / 'app.py').read_text(encoding='utf-8') + '\n# tampered\n', encoding='utf-8')
            self.assertEqual(integrity.verify(clone)['status'], 'FAILED')

    def test_builder_creates_repeatable_manifest_and_inventory(self):
        with tempfile.TemporaryDirectory() as temp:
            clone = Path(temp) / 'site'
            shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns('.git', 'tests', '__pycache__'))
            commit = 'a' * 40
            first = write_manifest(clone, commit)
            first_bytes = (clone / 'PUBLIC_MANIFEST.json').read_bytes()
            second = write_manifest(clone, commit)
            self.assertEqual(first, second)
            self.assertEqual(first_bytes, (clone / 'PUBLIC_MANIFEST.json').read_bytes())
            self.assertEqual(integrity.verify(clone)['status'], 'VERIFIED')
            actual = {p.relative_to(clone).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in (clone / 'content').rglob('*') if p.is_file() and p.suffix != '.pyc'}
            listed = {e['path']: e['sha256'] for e in second['content_at_build']['files']}
            self.assertEqual(listed, actual)


if __name__ == '__main__':
    unittest.main()
