"""Shared UI helpers and session-state access. All state is the visitor's own session; nothing persists."""
from __future__ import annotations

import streamlit as st

from .. import findings as findings_mod
from .. import ledger as ledger_mod
from ..safety import md_escape

EXERCISES = (
    ('knowledge', 'SAP knowledge lookup'),
    ('architecture-comparison', 'Architecture comparison'),
    ('synthetic-lab', 'Synthetic billing lab'),
    ('evidence-assessment', 'Evidence assessment'),
    ('improvement-analysis', 'Improvement analysis'),
    ('learning-report', 'Learning report'),
)
EXERCISE_NAMES = dict(EXERCISES)
LIFECYCLE = ('IDENTIFY', 'EVALUATE', 'ALIGN WITH HANDS-ON', 'PROVE', 'COMPARE', 'SCOPE FOR IMPROVEMENT')
PAGES: dict = {}
PRACTICE_VIEW = 'Practice exercises (optional)'

SITE = 'https://prasaddeshpande.com'
FOOTER_LINKS = (
    ('Research Methodology', 'Research methodology'),
    ('Evidence & Limitations', 'Evidence & limitations'),
    ('Privacy', 'Privacy'),
    ('Contact', 'Contact'),
)

def chip(label: str, color: str = 'gray') -> str:
    color = color if color in ('red', 'orange', 'yellow', 'blue', 'green', 'violet', 'gray') else 'gray'
    return f':{color}-badge[{md_escape(label, 80)}]'


def state() -> dict:
    ss = st.session_state
    ss.setdefault('ledger', [])
    ss.setdefault('knowledge', None)
    ss.setdefault('comparison', None)
    ss.setdefault('lab', None)
    ss.setdefault('lookup_state', {})
    return ss


def add_evidence(entry: dict) -> None:
    st.session_state['ledger'] = ledger_mod.add(st.session_state.get('ledger', []), entry)


def goto(key: str, exercise: str | None = None) -> None:
    if exercise:
        st.session_state['exercise'] = exercise
    if key in ('experiments', 'reviews'):          # the practice exercises live under Method & Evidence
        st.session_state['method_view'] = PRACTICE_VIEW
        key = 'method'
    page = PAGES.get(key)
    if page is not None:
        st.switch_page(page)


def choose(label: str, options, key: str, default=None):
    options = list(options)
    default = default if default in options else options[0]
    picked = st.segmented_control(label, options, default=default, key=key, label_visibility='collapsed')
    return picked if picked in options else default


def section(prefix: str, title: str) -> None:
    st.markdown(f'#### {prefix} · {title}')


def lifecycle_strip(active: tuple = ()) -> None:
    cols = st.columns(len(LIFECYCLE))
    for col, name in zip(cols, LIFECYCLE, strict=True):
        col.markdown(chip(name, 'blue' if name in active else 'gray'))


def _open_view(view: str) -> None:
    """Footer navigation: open a Method & Evidence view in the SAME tab (markdown links would open a new one)."""
    st.session_state['method_view'] = view
    page = PAGES.get('method')
    if page is not None:
        st.switch_page(page)


def footer() -> None:
    """Brand footer shown on every page. Static text and navigation buttons only."""
    st.divider()
    st.markdown('**Architected by Prasad™**  \n**SAP AI Evaluation Workbench**  \n'
                'Independent SAP AI engineering research, experiments and evidence.')
    st.caption('Architected, designed and developed by Prasad Deshpande.')
    st.caption('© 2026 Prasad Deshpande. All rights reserved.')
    st.markdown(f'Website: [{SITE}]({SITE})')
    cols = st.columns(len(FOOTER_LINKS) + 2)
    for col, (label, view) in zip(cols, FOOTER_LINKS, strict=False):
        col.button(label, key=f'footer_{view}', type='tertiary', on_click=_open_view, args=(view,))

def content() -> dict:
    """Verified published content (see sap_public/findings.py). Cheap: a few small JSON files."""
    return findings_mod.load()


def content_banner(c: dict) -> None:
    rel = c['release']
    if c['status'] == 'UNAVAILABLE':
        st.warning('Published content cannot be verified right now, so nothing is shown. This is a safe failure, not '
                   'an empty result.')
    elif c['status'] == 'DEGRADED':
        st.warning(f"Showing the last verified release (version {c['served_version']}). A newer release failed "
                   'verification and is not shown.')
    if c.get('test_content'):
        st.error('Test content: this copy is serving a test bundle, not published research. Nothing here is a finding.')
    if c['status'] == 'EMPTY':
        st.info('No findings have been published yet. They appear here only after the research owner approves them.')
    pub = rel.get('published_at')
    st.caption(f"Content version {rel.get('version', 0)}" + (f' · published {str(pub)[:10]}' if pub else ''))