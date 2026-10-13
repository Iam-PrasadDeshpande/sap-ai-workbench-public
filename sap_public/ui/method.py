"""METHOD & EVIDENCE: how the research is done and published, what the evidence means, privacy and contact."""
from __future__ import annotations

import streamlit as st

from .. import catalog
from .. import findings as F
from ..contract import EVIDENCE_TEXT
from ..safety import md_escape
from . import common, delivery, experiments, reviews
from .common import PRACTICE_VIEW, SITE, chip

VIEWS = ('Research methodology', 'Evidence & limitations', 'Release & integrity', 'Privacy', 'Contact', PRACTICE_VIEW)
PIPELINE = (
    ('Private hands-on', 'The experiment is run by the owner in the private engineering workbench.'),
    ('Execution receipt', 'Every call and check is sealed in a hash-linked receipt.'),
    ('Evidence validation', 'Deterministic checks decide whether the run passed. A model never decides.'),
    ('Public-safe projection', 'Only sanitized fields are projected: no paths, tokens, private data or audit records.'),
    ('Publication policy', 'Only findings the owner approved, or that match an owner-approved allowlist, are eligible.'),
    ('Versioned public content', 'Each update is an immutable, hash-verified release; the site can roll back.'),
)


def render() -> None:
    st.title('Method & Evidence')
    st.caption('How the research is done and published, what the evidence means, and what this site does not do.')
    default = st.query_params.get('view')
    view = common.choose('View', VIEWS, key='method_view', default=default)
    if view == 'Research methodology':
        _methodology()
    elif view == 'Evidence & limitations':
        _evidence()
    elif view == 'Release & integrity':
        delivery.render()
    elif view == 'Privacy':
        _privacy()
    elif view == 'Contact':
        _contact()
    else:
        _practice()
    common.footer()


def _methodology() -> None:
    st.subheader('Research methodology')
    st.write('The work follows six stages: identify the problem and its official SAP source, evaluate what is claimed '
             'and what access it needs, align with a hands-on step, prove what can be proven, compare only when '
             'comparable data exists, and scope what to improve. Every proposed improvement is either tied to an '
             'observation or labelled a hypothesis.')
    st.markdown('**From experiment to published finding**')
    for i, (name, text) in enumerate(PIPELINE, 1):
        st.markdown(f'{i}. **{md_escape(name)}**: {md_escape(text)}')
    st.markdown('**Rules that keep the research honest**')
    st.markdown('- Documentation, generated code, static fixtures and model answers are never presented as live SAP execution.\n'
                '- A verified receipt proves the record is intact. It does not prove SAP behaves as described.\n'
                '- A failed, unverified or ambiguous result stays private.\n'
                '- A newer finding can supersede an older one; a mistaken one is retracted and kept as a record.\n'
                '- No visitor can run SAP operations or reach the private workbench from this site.')


def _evidence() -> None:
    st.subheader('Evidence and limitations')
    st.markdown('**What the evidence labels mean**')
    for key, label in F.EVIDENCE_LABEL.items():
        st.markdown(f'- {chip(label, "blue")}')
    for key, (label, text) in EVIDENCE_TEXT.items():
        if key in ('PUBLIC_SAP_API', 'DOCUMENTATION'):
            st.markdown(f'- **{md_escape(label)}**: {md_escape(text)}')
    st.markdown('**What "validated" means**')
    st.write('All deterministic checks of that experiment passed in one run whose receipt re-verified. It says '
             'nothing about other systems, versions, tenants or data.')
    st.markdown('**Standing limitations**')
    for x in catalog.release()['known_limitations']:
        st.markdown('- ' + md_escape(x))
    st.markdown('- SAP trial and licence access limit what can be tested; blocked areas are listed in Capabilities.')


def _privacy() -> None:
    st.subheader('Privacy')
    st.markdown('- This application does not store your questions, searches or conversations: they are held only in '
                'the memory of your current browser session and are gone when it ends.\n'
                '- It has no accounts and no analytics (usage statistics are switched off). The Streamlit framework '
                'sets a technical cookie that protects requests against cross-site forgery; the application adds none.\n'
                "- If you press the optional \"Look in SAP's public documentation\" button, your question text is sent "
                'to SAP\'s public developer service (developers.sap.com) and nothing else.\n'
                '- The hosting platform (Streamlit Community Cloud) processes requests under its own terms.\n'
                '- Questions are never sent to the private engineering workbench, which has no connection to this site.')


def _contact() -> None:
    st.subheader('Contact')
    st.write('Prasad Deshpande, independent SAP AI engineering research.')
    st.caption('SAP, SAP BTP, SAP Fiori, SAPUI5, ABAP and other SAP products mentioned are trademarks or registered '
               'trademarks of SAP SE. This site is independent research; it is not affiliated with, sponsored by or '
               'endorsed by SAP SE.')
    st.markdown(f'Website: [{SITE}]({SITE})')
    st.caption('Please use the contact options on the website. Corrections to a published finding are welcome and '
               'are handled through the retraction and supersession process.')


def _practice() -> None:
    st.subheader('Practice exercises (optional)')
    st.info('These are small synthetic exercises for learning the method. They are not research results and are not '
            'part of the published findings.')
    part = common.choose('Section', ('Exercises', 'My session summary'), key='practice_part')
    if part == 'Exercises':
        experiments.render()
    else:
        reviews.render()
