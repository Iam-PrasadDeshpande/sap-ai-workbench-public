"""MISSION & OVERVIEW (home): what this is and why, the SAP source foundation, how capabilities are evaluated, current
coverage, recent validated observations and the next validation priorities. The first screen explains the purpose."""
from __future__ import annotations

import streamlit as st

from .. import evaluation as E
from .. import findings as F
from ..safety import md_escape
from . import common, overview
from .common import chip

HERO = 'From SAP Developer Capabilities to Practical Engineering Proof'
SUPPORT = ('Explore which AI and AI-enabling developer capabilities SAP makes available, how they can be used, what has '
           'been practically evaluated, and what the evidence tells us about their usefulness, maturity and limitations.')
READ_FIRST = (
    ('Independent research', 'This is independent research conducted by Prasad Deshpande.'),
    ('Real experiments', 'The experiments were performed hands-on in a private engineering workbench, not here.'),
    ('Evidence-backed', 'Each published outcome is backed by a sealed execution record and states what it proves.'),
    ('Browse and question', 'You can browse findings, search them, compare them and ask questions about them.'),
    ('No execution here', 'This website does not let visitors execute SAP operations or reach any SAP system.'),
    ('Unknown stays unknown', 'Anything unproven, blocked or not yet investigated is labelled as such.'),
    ('Updated by publication', 'New findings appear when the owner approves and publishes a content update.'),
)
SHORT_CATEGORY = {'AI_NATIVE': 'AI-native capabilities', 'AI_ENABLING_FRAMEWORK': 'AI-enabling frameworks',
                  'AI_INTEGRATION': 'AI integration services and tools',
                  'DISCOVERY': 'developer discovery and documentation services'}
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
        st.caption('What it supports: ' + md_escape(F.TIER_TEXT.get(F.finding_tier(f), 'not established'), 200))
        for o in (f.get('verified_observations') or [])[:1]:
            st.write(md_escape(o['text'] if isinstance(o, dict) else o, 300))
        lim = (f.get('limitations') or [])[:1]
        if lim:
            st.caption('Limitation: ' + md_escape(lim[0]['text'] if isinstance(lim[0], dict) else lim[0], 220))
        st.button('Open this evaluation', key=key, on_click=_open_finding, args=(f['finding_id'],))


def _open_finding(fid: str) -> None:
    st.session_state['finding_selected'] = fid
    common.goto('findings')


def render() -> None:
    c = common.content()
    rel = c['release']
    data, items = E.evaluated(rel)
    cov = E.coverage(items)
    st.title('SAP AI Evaluation Workbench')
    st.subheader(HERO)
    st.write(SUPPORT)
    overview.render()
    st.write(md_escape(data['mission'], 400))
    st.caption('developers.sap.com is the primary discovery foundation, supplemented by related official SAP '
               'documentation, developer services and public MCP endpoints. Official documentation is the starting '
               'point, not proof. Nothing on this site executes an SAP operation.')
    common.content_banner(c)

    st.markdown('### Current evaluation coverage')
    st.write(f"{cov['total']} SAP capabilities in the catalog · {cov['hands_on']} with published hands-on evidence · "
             f"{cov['documentation']} at documentation level only.")
    st.caption(' · '.join(f'{n} {SHORT_CATEGORY[k]}' for k, n in cov['by_category'].items() if n)
               + '. Listed is not executed: hands-on evidence appears only when the owner approves a validated result.')
    st.button('See the SAP AI capabilities', key='home_caps', on_click=common.goto, args=('capabilities',))

    st.markdown('### Recent validated observations')
    recent = F.visible(rel, include_superseded=False)[:3]
    if not recent:
        st.info('There are no published findings to show yet. When the owner approves a validated experiment, it '
                'appears here with its evidence, its limitations and what is still unproven.')
    for i, f in enumerate(recent):
        finding_card(f, f'home_f_{i}')
    if recent:
        st.button('Browse all hands-on evaluations', key='home_all', on_click=common.goto, args=('findings',))

    st.markdown('### Next engineering validation priorities')
    st.caption('The owner\'s planned next hands-on steps (plans, not results), starting with those that need no SAP '
               'entitlement.')
    for i in E.priorities(items):
        st.markdown(f"- **{md_escape(i['name'], 120)}**: {md_escape(i['next_hands_on_action'], 300)}")

    st.markdown('### Ask the evidence')
    q = st.text_input('Your question', key='home_q', max_chars=300,
                      placeholder='e.g. Has SAP CAP MCP integration been validated?')
    if st.button('Ask the Evidence', type='primary', key='home_ask') and q.strip():
        st.session_state['ask_question'] = q.strip()
        st.session_state['ask_autorun'] = True
        common.goto('ask')

    with st.expander('Read this first', expanded=False):
        st.markdown('**Read this first**')
        for title, text in READ_FIRST:
            st.markdown(f'- **{md_escape(title)}.** {md_escape(text)}')
    st.markdown(chip('Read-only', 'green') + '  ' + chip('No sign-in', 'gray') + '  ' +
                chip('Nothing is stored about you', 'gray'))
    common.footer()
