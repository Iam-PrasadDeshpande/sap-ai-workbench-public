"""Per-session throttling for the one outbound feature. State is the caller's own session dict: nothing is shared."""
from __future__ import annotations

import time

from .contract import LIMITS


def check_lookup_allowed(state: dict, clock=time.monotonic) -> str:
    """Return '' if a lookup may run now, otherwise a plain-language reason. Does not change state."""
    used = int(state.get('lookups_used', 0))
    if used >= LIMITS['lookups_per_session']:
        return (f"This session has used its {LIMITS['lookups_per_session']} lookups. Reload the page to start a new "
                'session; the limit protects SAP\'s shared public service.')
    last = state.get('last_lookup_at')
    if last is not None:
        wait = LIMITS['min_seconds_between_lookups'] - (clock() - last)
        if wait > 0:
            return f'Please wait {int(wait) + 1} more second(s) before the next lookup.'
    return ''


def record_lookup(state: dict, clock=time.monotonic) -> None:
    state['lookups_used'] = int(state.get('lookups_used', 0)) + 1
    state['last_lookup_at'] = clock()
