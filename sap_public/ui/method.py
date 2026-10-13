"""EVALUATION FRAMEWORK: how SAP capabilities are sourced, classified, evaluated and published; what the evidence
levels mean; the public-private architecture; publication governance; release integrity; privacy and contact."""
from __future__ import annotations

import streamlit as st

from .. import catalog
from .. import evaluation as E
from .. import findings as F
from ..contract import EVIDENCE_TEXT
from ..safety import md_escape
from . import common, delivery, experiments, reviews
from .common import PRACTICE_VIEW, SITE, chip

VIEWS = ('Evaluation methodology', 'Capability classification', 'Maturity & usefulness', 'Evidence & limitations',
         'Architecture & governance', 'Release & integrity', 'Privacy', 'Contact', PRACTICE_VIEW)
PIPELINE = (
    ('Private hands-on', 'The experiment is run by the owner in the private engineering workbench.'),
    ('Execution receipt', 'Every call and check is sealed in a hash-linked receipt.'),
    ('Evidence validation', 'Deterministic checks decide whether the run passed. A model never decides.'),
    ('Public-safe projection', 'Only sanitized fields are projected: no paths, tokens, private data or audit records.'),
    ('Publication policy', 'Only findings the owner explicitly approved are published; automatic publication is disabled.'),
    ('Versioned public content', 'Each update is an immutable, hash-verified release; the site can roll back.'),
)
CRITERIA = (
    ('Official availability and documentation', 'Is there an official SAP reference, and does it answer?'),
    ('Accessibility and dependencies', 'What access, entitlement, licence or local software does it need?'),
    ('Technical integration feasibility', 'Could a bounded, read-only operation actually be integrated and run?'),
    ('Hands-on execution coverage', 'Which of its tools have a verified operation, and which only discovery?'),
    ('Functional behaviour and reliability', 'Did the deterministic checks pass, and in how many comparable runs?'),
    ('Engineering usefulness', 'Observed within scope; the judgment of usefulness is recorded separately by the owner.'),
    ('Operational limitations', 'What the evidence does not cover: scope, data, systems and versions.'),
    ('Adoption readiness', 'Needs SAP system validation and an owner judgment; a local prototype is not enough.'),
)


def render() -> None:
    st.title('Evaluation Framework')
    st.caption('How SAP capabilities are sourced, classified and evaluated, what the evidence means, and how results '
               'reach this site.')
    default = st.query_params.get('view')
    view = common.choose('View', VIEWS, key='method_view', default=default)
    if view == 'Evaluation methodology':
        _methodology()
    elif view == 'Capability classification':
        _classification()
    elif view == 'Maturity & usefulness':
        _maturity()
    elif view == 'Evidence & limitations':
        _evidence()
    elif view == 'Architecture & governance':
        _architecture()
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
    data = catalog.capabilities()
    st.subheader('Evaluation methodology')
    st.write(md_escape(data['mission'], 500))
    st.markdown('**Official source methodology.** developers.sap.com is the primary discovery foundation. Related '
                'official SAP documentation, developer services, public MCP endpoints and SAP\'s own open-source '
                'repositories supplement it. Each capability names its official reference and when it was last '
                'checked; a reachable reference is a source fact, never an execution.')
    st.write('The work follows six stages: identify the problem and its official SAP source, evaluate what is claimed '
             'and what access it needs, align with a hands-on step, prove what can be proven, compare only when '
             'comparable data exists, and scope what to improve. Every proposed improvement is either tied to an '
             'observation or labelled a hypothesis.')
    st.markdown('**Principles**')
    st.markdown('\n'.join(f'- {md_escape(p, 200)}' for p in data['principles']))
    st.markdown('**From experiment to published finding**')
    for i, (name, text) in enumerate(PIPELINE, 1):
        st.markdown(f'{i}. **{md_escape(name)}**: {md_escape(text)}')
    st.markdown('**Rules that keep the research honest**')
    st.markdown('- Documentation, generated code, static fixtures and model answers are never presented as live SAP execution.\n'
                '- A verified receipt proves the record is intact. It does not prove SAP behaves as described.\n'
                '- A failed, unverified or ambiguous result stays private.\n'
                '- A newer finding can supersede an older one; a mistaken one is retracted and kept as a record.\n'
                '- No visitor can run SAP operations or reach the private workbench from this site.')


def _classification() -> None:
    data = catalog.capabilities()
    st.subheader('Capability classification')
    st.write('Every capability has one stable identity shared by the private workbench and this site, and exactly one '
             'category. Frameworks such as SAP CAP, SAPUI5/Fiori and ABAP RAP enable AI-assisted engineering but are '
             'not AI products themselves, so they are never classified as AI-native.')
    for key, label in data['categories'].items():
        names = [c['name'] for c in data['capabilities'] if c['category'] == key]
        with st.container(border=True):
            st.markdown(f'**{md_escape(label, 120)}** ({len(names)})')
            st.caption(md_escape(', '.join(names), 600))


def _maturity() -> None:
    data = catalog.capabilities()
    st.subheader('Maturity and usefulness')
    st.write('Each capability is assessed on eight independent dimensions. A dimension is reported as an evidence '
             'level, never as a percentage, rating or score, and never higher than the strongest published evidence '
             'allows. Absence of evidence reads "Not assessed": it is not a negative result.')
    for name, question in CRITERIA:
        st.markdown(f'- **{md_escape(name)}**: {md_escape(question)}')
    st.markdown('**Evidence levels**')
    for k, label in data['levels'].items():
        st.markdown(f"- {chip(label, E.LEVEL_COLOR.get(k, 'gray'))}")
    st.caption('Method: ' + md_escape(data['assessment_method'], 600))
    st.write('Observed results, hypotheses and engineering judgments are labelled separately. Usefulness and adoption '
             'readiness need the owner\'s recorded judgment; until then they say so.')


def _architecture() -> None:
    st.subheader('Architecture and publication governance')
    st.write('Two applications, one evaluation mission. The private SAP AI Engineering Workbench discovers '
             'capabilities, runs owner-authorized experiments, seals receipts and assesses capabilities; it is the '
             'execution authority. This public site presents the approved, public-safe projection of those results and '
             'can never execute an experiment or manufacture proof.')
    for i, step in enumerate(E.LIFECYCLE, 1):
        st.markdown(f'{i}. {md_escape(step)}')
    st.markdown('**Publication governance**')
    st.markdown('- Only findings the owner approves are published; automatic publication is disabled.\n'
                '- Each content release is immutable and hash-chained; retractions stay in force through rollback.\n'
                '- Text is screened for private content before publication and again by this site when it loads.\n'
                '- Capability evaluations are computed from published evidence only; nothing unapproved surfaces here.\n'
                '- Content updates do not change this site\'s code; code changes go through signing and qualification.')


def _evidence() -> None:
    st.subheader('Evidence and limitations')
    st.markdown('**What the evidence labels mean**')
    for key, label in F.EVIDENCE_LABEL.items():
        st.markdown(f'- {chip(label, "blue")}')
    for key, (label, text) in EVIDENCE_TEXT.items():
        if key in ('PUBLIC_SAP_API', 'DOCUMENTATION'):
            st.markdown(f'- **{md_escape(label)}**: {md_escape(text)}')
    st.markdown('**What each tier supports**')
    for key, text in F.TIER_TEXT.items():
        st.markdown(f'- {md_escape(text)}')
    st.markdown('**What "validated" means**')
    st.write('All deterministic checks of that experiment passed in one run whose receipt re-verified. It says '
             'nothing about other systems, versions, tenants or data.')
    st.markdown('**Standing limitations**')
    for x in catalog.release()['known_limitations']:
        st.markdown('- ' + md_escape(x))
    st.markdown('- SAP trial and licence access limit what can be tested; entitlement needs are listed per capability.')


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
