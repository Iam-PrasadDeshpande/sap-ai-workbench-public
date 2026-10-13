"""REVIEWS: compare, inspect evidence, get an evidence-linked recommendation and a sanitized report.

Visitors have no authority here: nothing on this page records an approval or an owner decision.
"""
from __future__ import annotations

import streamlit as st

from .. import improve, ledger, report
from ..contract import CLAIM_TEXT, EVIDENCE_TEXT
from ..safety import md_escape
from . import common
from .common import chip


def render() -> None:
    s = common.state()
    st.title('Reviews')
    st.caption('Inspect what you have found, what it proves, and what to do next. This page cannot approve anything: '
               'decisions about SAP adoption belong to you and your own governance.')
    st.subheader('Where your findings stand')
    cmp_, lab, know = s['comparison'], s['lab'], s['knowledge']
    c1, c2, c3 = st.columns(3)
    c1.metric('Knowledge lookups', 1 if know else 0)
    c2.metric('Comparisons', 1 if cmp_ else 0)
    c3.metric('Synthetic lab runs', 1 if lab else 0)

    st.subheader('Recommendation (qualitative)')
    if not (know or cmp_ or lab):
        st.info('Nothing to review yet. Run an exercise first.')
        st.button('Open the exercises', key='rev_open', on_click=common.goto, args=('experiments',))
    else:
        with st.container(border=True):
            if cmp_:
                lean = cmp_['lean_name'] or {'DEPENDS': 'It depends on your priorities',
                                             'NO_PRIORITIES': 'Select priorities in the comparison'}[cmp_['lean']]
                st.markdown(f"**Leaning:** {md_escape(lean)} — {md_escape(cmp_['why'])}")
                st.caption(md_escape(cmp_['caveat']))
            else:
                st.markdown('**No comparison yet.** Run the architecture comparison to get a leaning.')
            if lab:
                st.markdown(f"**Synthetic exercise:** {md_escape(lab['explanation'])}")
            if know and know.get('sources'):
                st.markdown(f"**Source-grounded:** {len(know['sources'])} SAP sources retrieved "
                            f"({md_escape(know['retrieved_at'])}).")
        st.caption('This is evidence-linked but not proof. Documentation and synthetic results do not show that '
                   'anything works in your SAP system.')

    st.subheader('What your evidence supports')
    for cid, text in CLAIM_TEXT.items():
        res = ledger.assess_claim(s['ledger'], cid)
        col = {'SUPPORTED': 'green', 'NOT_YET_SUPPORTED': 'orange', 'CANNOT_BE_PROVEN_HERE': 'gray'}[res['status']]
        st.markdown(f"- {md_escape(text)} {chip(res['status'].replace('_', ' ').title(), col)}")
    with st.expander('Evidence kinds explained'):
        for label, text in EVIDENCE_TEXT.values():
            st.markdown(f'- **{md_escape(label)}**: {md_escape(text)}')

    st.subheader('Improvements and next steps')
    imp = improve.analyse(s['ledger'], know, lab, cmp_)
    for key, title in (('testable_improvements', 'Testable improvements'), ('hypotheses', 'Hypotheses (not findings)')):
        st.markdown(f'**{title}**')
        if not imp[key]:
            st.caption('None yet.')
        for i in imp[key]:
            st.markdown(f"- {md_escape(i['text'])} _({md_escape(i['basis'], 100)})_")
    st.markdown('**Next hands-on activity**')
    for t in imp['next_hands_on_activity']:
        st.markdown('- ' + md_escape(t))

    st.subheader('Download')
    claims = [ledger.assess_claim(s['ledger'], c) for c in ('EXISTS_IN_SAP_DOCS', 'TECHNIQUE_IS_SOUND', 'WORKS_IN_MY_TENANT')]
    rep = report.build('', know, cmp_, lab, s['ledger'], imp, claims)
    st.caption(f"Publication state of the report: {report.PUBLICATION_STATE}. It is an educational draft; "
               'nobody has reviewed or approved it.')
    d1, d2 = st.columns(2)
    d1.download_button('Report (Markdown)', report.to_markdown(rep), report.filename('report', '.md'), 'text/markdown',
                       key='rev_md')
    d2.download_button('Report (JSON)', report.to_json(rep), report.filename('report', '.json'), 'application/json',
                       key='rev_json')
