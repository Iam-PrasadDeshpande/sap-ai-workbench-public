"""RESEARCH (home): who this is, what is published, how to read it, and the newest verified findings."""
from __future__ import annotations

import streamlit as st

from .. import findings as F
from ..safety import md_escape
from . import common
from .common import chip

POSITIONING = 'Real experiments, verified findings and practical SAP AI engineering insights.'
READ_FIRST = (
    ('Independent research', 'This is independent research conducted by Prasad Deshpande.'),
    ('Real experiments', 'The experiments were performed hands-on in a private engineering workbench, not here.'),
    ('Evidence-backed', 'Each published outcome is backed by a sealed execution record and states what it proves.'),
    ('Browse and question', 'You can browse findings, search them, compare them and ask questions about them.'),
    ('No execution here', 'This website does not let visitors execute SAP operations or reach any SAP system.'),
    ('Unknown stays unknown', 'Anything unproven, blocked or not yet investigated is labelled as such.'),
    ('Updated by publication', 'New findings appear when the owner approves and publishes a content update.'),
)


def finding_card(f: dict, key: str) -> None:
    ev = F.EVIDENCE_LABEL.get(f.get('evidence_class'), f.get('evidence_label') or f.get('evidence_class', ''))
    with st.container(border=True):
        st.markdown(f"**{md_escape(f.get('title', ''), 160)}**")
        chips = [chip(ev, 'blue'), chip('Validated' if f.get('validation_status') == 'VALIDATED' else 'Not validated',
                                        'green' if f.get('validation_status') == 'VALIDATED' else 'orange'),
                 chip('Executed ' + md_escape(f.get('execution_date', '?')), 'gray')]
        if f.get('state') == 'SUPERSEDED':
            chips.append(chip('Superseded', 'orange'))
        if F.is_stale(f):
            chips.append(chip(f'Older than {F.STALE_AFTER_DAYS} days', 'orange'))
        st.markdown('  '.join(chips))
        for o in (f.get('verified_observations') or [])[:1]:
            st.write(md_escape(o['text'] if isinstance(o, dict) else o, 300))
        lim = (f.get('limitations') or [])[:1]
        if lim:
            st.caption('Limitation: ' + md_escape(lim[0]['text'] if isinstance(lim[0], dict) else lim[0], 220))
        st.button('Open this finding', key=key, on_click=_open_finding, args=(f['finding_id'],))


def _open_finding(fid: str) -> None:
    st.session_state['finding_selected'] = fid
    common.goto('findings')


def render() -> None:
    c = common.content()
    rel = c['release']
    st.title('SAP AI Evaluation Workbench')
    st.subheader(POSITIONING)
    st.write('Independent SAP AI engineering research by Prasad Deshpande: real experiments run in a private '
             'engineering workbench, published here only after the evidence is validated and the findings are '
             'approved for public view.')
    common.content_banner(c)

    st.markdown('### Recent verified findings')
    recent = F.visible(rel, include_superseded=False)[:3]
    if not recent:
        st.info('There are no published findings to show yet. When the owner approves a validated experiment, it '
                'appears here with its evidence, its limitations and what is still unproven.')
    for i, f in enumerate(recent):
        finding_card(f, f'home_f_{i}')
    if recent:
        st.button('Browse all findings', key='home_all', on_click=common.goto, args=('findings',))

    st.markdown('### Ask about the published research')
    q = st.text_input('Your question', key='home_q', max_chars=300,
                      placeholder='e.g. What have you validated with SAP CAP and MCP?')
    if st.button('Ask the Workbench', type='primary', key='home_ask') and q.strip():
        st.session_state['ask_question'] = q.strip()
        st.session_state['ask_autorun'] = True
        common.goto('ask')

    with st.container(border=True):
        st.markdown('**Read this first**')
        for title, text in READ_FIRST:
            st.markdown(f'- **{md_escape(title)}.** {md_escape(text)}')
    caps = rel.get('capabilities') or []
    if caps:
        proven = sum(1 for x in caps if x.get('status') == 'VALIDATED_HANDS_ON')
        st.caption(f'Capability map: {len(caps)} capabilities, {proven} validated hands-on.')
    st.markdown(chip('Read-only', 'green') + '  ' + chip('No sign-in', 'gray') + '  ' +
                chip('Nothing is stored about you', 'gray'))
    common.footer()
