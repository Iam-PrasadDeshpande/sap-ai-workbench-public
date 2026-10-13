"""Public capability catalog and release information (static, versioned, read-only data).

`data/capabilities.json` is GENERATED from the private workbench's canonical capability contract
(scripts/gen_public_capabilities.py) so both editions share one set of capability identities. It holds identity and
official-reference facts only: execution evidence reaches this site solely through owner-approved content releases.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data'
CATALOG_SCHEMA = 'sap-public.capability-catalog/1'
CATEGORIES = ('AI_NATIVE', 'AI_ENABLING_FRAMEWORK', 'AI_INTEGRATION', 'DISCOVERY')
_ID = re.compile(r'SAP-\d{2}')
_REF = re.compile(r'https://[a-z0-9.-]+/[^\s<>"]*|https://[a-z0-9.-]+')


def capabilities() -> dict:
    data = json.loads((DATA / 'capabilities.json').read_text(encoding='utf-8'))
    if data.get('schema') != CATALOG_SCHEMA:
        raise ValueError('unexpected capability catalog schema')
    seen = set()
    for c in data['capabilities']:
        if not _ID.fullmatch(str(c.get('capability_id', ''))) or c['capability_id'] in seen:
            raise ValueError('malformed or duplicate capability id')
        seen.add(c['capability_id'])
        if c.get('category') not in CATEGORIES:
            raise ValueError(f"unknown category {c.get('category')}")
        if c.get('sap_source_reference') and not _REF.fullmatch(c['sap_source_reference']):
            raise ValueError('official reference is not an https URL')
    return data


def release() -> dict:
    return json.loads((DATA / 'release.json').read_text(encoding='utf-8'))
