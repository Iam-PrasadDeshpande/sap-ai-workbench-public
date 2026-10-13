"""Public catalogue of SAP developer tools and public release information (static, versioned, read-only data)."""
from __future__ import annotations

import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data'
STATE_TEXT = {
    'PUBLICLY_AVAILABLE': ('Publicly available', 'green', 'Usable by anyone; some of it runs inside this application.'),
    'DOCUMENTED': ('Documented', 'blue', 'Published by SAP; not run by this edition.'),
    'REQUIRES_SETUP': ('Requires setup', 'orange', 'Needs software installed on your own machine.'),
    'REQUIRES_TRIAL': ('Requires an SAP trial', 'orange', 'Needs an SAP trial or sandbox system you control.'),
    'REQUIRES_COMMERCIAL_LICENSE': ('Requires an entitlement', 'orange', 'Needs a commercial SAP entitlement.'),
    'NOT_VERIFIED': ('Not verified', 'gray', 'The project could not verify availability or behaviour.'),
    'NOT_IMPLEMENTED': ('Not available here', 'gray', 'Nothing is implemented or simulated for it.'),
}


def tools() -> dict:
    data = json.loads((DATA / 'tools.json').read_text(encoding='utf-8'))
    for t in data['tools']:
        if t['state'] not in STATE_TEXT:
            raise ValueError(f"unknown state {t['state']}")
        if t.get('runs_here') and t['state'] != 'PUBLICLY_AVAILABLE':
            raise ValueError('only publicly available tools may run here')
    return data


def release() -> dict:
    return json.loads((DATA / 'release.json').read_text(encoding='utf-8'))
