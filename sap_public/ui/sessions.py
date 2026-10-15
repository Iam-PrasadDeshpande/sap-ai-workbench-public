"""KNOWLEDGE SESSIONS: owner-approved research notes (read-only). Sits beside, never inside, the findings pipeline."""
from __future__ import annotations

import streamlit as st

from .. import sessions as S
from ..safety import md_escape
from . import common
from .common import chip


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
    st.header(md_escape(f"{doc['session_id']}: {doc['title']}", 200))
    st.write(md_escape(doc.get('subtitle', ''), 400))
    st.markdown(chip('Revision ' + md_escape(str(doc.get('revision', '?')), 30), 'gray') + '  ' +
                chip(md_escape(str(doc.get('date', '')), 20), 'gray') + '  ' +
                chip(md_escape(str(doc.get('evidence_status', 'See evidence section')), 60), 'blue'))
    for sec in doc['sections']:
        st.markdown(f"### {md_escape(sec.get('title', ''), 160)}")
        for b in S.blocks(sec.get('markdown', '')):
            if b[0] == 'text':
                st.markdown(b[1])
            else:
                header, rows = b[1], b[2]
                st.dataframe([{h: c.replace('**', '').replace('`', '') for h, c in zip(header, r, strict=False)}
                              for r in rows], hide_index=True)
        if sec.get('key') == 'architecture' and doc.get('diagram_svg'):
            st.image(doc['diagram_svg'], caption='Tool-invocation path and source-editing path')
    claims = doc.get('claims') or []
    if claims:
        st.markdown('### Evidence register (public projection)')
        st.dataframe([{k: str(c.get(k, '')) for k in ('claim_id', 'claim', 'evidence_class', 'limitation')} for c in claims],
                     hide_index=True)
    refs = doc.get('references') or []
    if refs:
        st.markdown('### Official references')
        for r in refs:
            st.markdown(f"- [{md_escape(r.get('label', ''), 160)}]({r.get('url', '')})")
    st.caption('Independent work; not affiliated with or endorsed by SAP. Research notes describe one trial-system '
               'configuration and may be outdated; SAP tools change.')

