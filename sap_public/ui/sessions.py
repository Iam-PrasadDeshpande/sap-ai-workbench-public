"""KNOWLEDGE SESSIONS: owner-approved research notes (read-only). Sits beside, never inside, the findings pipeline.

The page is drawn by ks_page.py, the one presentation implementation shared with the private workbench; this module
only turns a verified, registry-approved document into that page's view model.
"""
from __future__ import annotations

import streamlit as st

from .. import sessions as S
from ..safety import md_escape
from . import common, ks_page
from .common import chip

NOTE_VIEW = 'Research notes'


def view_model(doc: dict) -> dict:
    sections = doc.get('sections') or []
    views = doc.get('views') or [{'key': 'article', 'name': 'Article'}]
    n = 0
    out_views = []
    for v in views:
        secs = []
        for el in sections:
            if el.get('view', views[0]['key']) == v['key']:
                n += 1
                secs.append({'number': n, 'title': el.get('title', ''), 'markdown': el.get('markdown', ''),
                             'diagram': bool(el.get('diagram'))})
        if secs:
            out_views.append({'key': v['key'], 'name': v['name'], 'sections': secs})
    diagram = None
    if doc.get('diagram_svg'):
        diagram = {'source': doc['diagram_svg'], 'caption': doc.get('diagram_caption') or 'Architecture', 'mermaid': None}
    lines = [f"Content digest (verified against the signed approval registry): `{doc.get('content_sha256', '')}`"]
    if doc.get('lineage_note'):
        lines.append(md_escape(str(doc['lineage_note']), 400))
    return {
        'key_prefix': 'ks_pub',
        'heading': f"{doc['session_id']}: {doc['title']}",
        'subtitle': doc.get('subtitle', ''),
        'meta': [
            {'caption': 'Revision', 'text': f"{doc.get('revision', '?')} ({doc.get('date', '')})"},
            {'caption': 'Evidence status', 'text': str(doc.get('evidence_status', 'See evidence section'))},
            {'caption': 'Publication status', 'chip': ('Published, owner-approved content', 'green')},
        ],
        'identity': {'lines': lines,
                     'caption': 'Evidence classes describe how each statement is supported. Nothing here was '
                                'independently re-verified beyond what each claim states.'},
        'views': out_views,
        'claims': doc.get('claims') or [],
        'claim_columns': ('claim_id', 'claim', 'evidence_class', 'limitation'),
        'claims_title': 'Evidence register (public projection)',
        'references': doc.get('references') or [],
        'diagram': diagram,
        'footer': 'Independent work; not affiliated with or endorsed by SAP. Research notes describe one trial-system '
                  'configuration and may be outdated; SAP tools change.',
    }


def render() -> None:
    res = S.load()
    st.caption('Research notes are written articles derived from a reviewed research document. They are not execution '
               'findings: each states which parts were documented by SAP, observed in a trial system, or reported by '
               'the owner, and which were not verified.')
    if not res['sessions']:
        st.info('No research notes are published yet. A note appears here only after the research owner approves it.')
        return
    ids = [d['session_id'] for d in res['sessions']]
    sid = common.choose('Session', ids, key='ks_pub_session', default=st.query_params.get('session'))
    doc = next(d for d in res['sessions'] if d['session_id'] == sid)
    ks_page.render(view_model(doc), choose=common.choose, chip=chip, blocks=S.blocks,
                   plain=lambda s: s.replace('**', '').replace('`', ''), esc=md_escape)


def _open_session(sid: str) -> None:
    st.session_state['fnd_view'] = NOTE_VIEW
    st.session_state['ks_pub_session'] = sid
    st.query_params['view'] = NOTE_VIEW
    st.query_params['session'] = sid


def featured_banner() -> None:
    """Featured knowledge-session banner for the Hands-on Evaluations landing view. Data-driven (see S.featured)."""
    items = S.featured(S.load()['sessions'])
    if not items:
        return
    e = items[0]
    with st.container(border=True, key='ks_featured_banner'):
        st.markdown(f"**{md_escape(e['label'], 80)}**")
        st.markdown(f"### {md_escape(e['title'], 160)}")
        st.write(md_escape(e['description'], 400))
        st.button(e['action_label'], key=f"ks_featured_{e['session_id']}", type='primary',
                  on_click=_open_session, args=(e['session_id'],))
