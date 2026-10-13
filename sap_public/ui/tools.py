"""SAP AI CAPABILITIES: the evaluated capability catalog with category, official reference, access, evidence level and
the hands-on status of each tool. Identities come from the generated canonical catalog; evidence only from the
verified, owner-approved content release. Nothing is executed or inferred here."""
from __future__ import annotations

import streamlit as st

from .. import evaluation as E
from ..safety import https_url_on, md_escape
from . import common, overview
from .common import chip


def render() -> None:
    c = common.content()
    data, items = E.evaluated(c['release'])
    st.title('SAP AI Capabilities')
    st.caption('What SAP exposes for AI-assisted development, how it is classified, what it needs, and what the '
               'published evidence shows. Being listed is never the same as being executed.')
    common.content_banner(c)
    cov = E.coverage(items)
    st.markdown(chip(f"{cov['total']} capabilities", 'violet') + '  '
                + chip(f"{cov['hands_on']} with published hands-on evidence", 'green') + '  '
                + chip(f"{cov['documentation']} documentation only", 'blue'))

    f1, f2, f3 = st.columns(3)
    cats = ['All categories'] + list(data['categories'].values())
    cat = f1.selectbox('Category', cats, key='cap_cat')
    ev = f2.selectbox('Evidence', E.EVIDENCE_FILTERS, key='cap_ev')
    q = f3.text_input('Technology or name', key='cap_q', max_chars=80, placeholder='e.g. CAP, MCP, UI5').strip().lower()
    shown = [i for i in items
             if (cat == 'All categories' or data['categories'][i['category']] == cat) and E.matches(i, ev)
             and (not q or q in f"{i['name']} {i['official_description']} {' '.join(i.get('components') or [])}".lower())]
    st.caption(f'{len(shown)} of {len(items)} capabilities')
    if shown:
        overview.table(('Capability', 'Category', 'Evidence level', 'Hands-on status'),
                       [(i['name'], [(SHORT_CATEGORY[i['category']], ''),
                                     (E.LEVEL_TEXT.get(i['evaluation'].get('evidence_level'), ''),
                                      E.LEVEL_COLOR.get(i['evaluation'].get('evidence_level'), 'gray')),
                                     _hands_on(i)]) for i in shown],
                       'SAP AI capability evaluation overview')
        st.markdown('#### Details by capability')
    for i in shown:
        _card(i, data)
    if not shown:
        st.info('No capability matches these filters.')
    with st.expander('How to read this page'):
        st.markdown('- **Category** separates SAP AI-native products from AI-enabling frameworks (such as CAP and '
                    'SAPUI5), AI integration tooling and public discovery services.\n'
                    '- **Official reference check** says the SAP page or endpoint answered when it was checked. It is '
                    'a source fact, never an execution.\n'
                    '- **Evidence level** is the strongest published evidence: documentation only, local validation '
                    'only, or SAP system validation. It is never a score.\n'
                    '- **Not yet evaluated** means no published hands-on evidence exists. It is not a negative result.')
    common.footer()


SHORT_CATEGORY = {'AI_NATIVE': 'AI-native', 'AI_ENABLING_FRAMEWORK': 'AI-enabling framework',
                  'AI_INTEGRATION': 'AI integration', 'DISCOVERY': 'Discovery'}


def _hands_on(i: dict) -> tuple:
    comps = i['evaluation'].get('components') or []
    done = [c for c in comps if c.get('last_execution_status') == 'OPERATION_VERIFIED']
    if not comps:
        return ('No executable tool evaluated', 'gray')
    if done:
        return (f'{len(done)} of {len(comps)} tools verified in published evidence', 'green')
    return ('No published hands-on evidence yet', 'gray')


def _card(i: dict, data: dict) -> None:
    e = i['evaluation']
    lvl = e.get('evidence_level', 'NOT_ASSESSED')
    with st.container(border=True):
        st.markdown(f"**{md_escape(i['name'], 140)}**  ·  {md_escape(i['capability_id'])}")
        st.markdown(chip(data['categories'][i['category']], 'violet') + '  '
                    + chip('Evidence: ' + E.LEVEL_TEXT.get(lvl, lvl), E.LEVEL_COLOR.get(lvl, 'gray')))
        st.write(md_escape(i['official_description'], 300))
        st.caption('Engineering purpose: ' + md_escape(i['engineering_purpose'], 300))
        st.caption('Access: ' + md_escape(i['access_requirements'], 200) + ' · Licensing: '
                   + md_escape(i['licensing_or_entitlement_status'], 120))
        url = i.get('sap_source_reference') or ''
        host = url.split('/')[2].lower() if url.startswith('https://') and len(url.split('/')) > 2 else ''
        safe = https_url_on(host, url) if host else ''
        st.caption(E.source_text(i.get('source_check') or {}))
        if safe:
            st.markdown(f'[Official reference]({safe})')
        for comp in e.get('components') or []:
            marker, color, text = E.EXECUTION_TEXT.get(comp.get('last_execution_status'), E.EXECUTION_TEXT['NOT_YET_TESTED'])
            line = chip(marker, color) + ' ' + md_escape(comp.get('name') or comp.get('key'), 100) + ': ' + md_escape(text, 160)
            if comp.get('run_id') is not None:
                line += f" (published run {md_escape(str(comp['run_id']))}, {md_escape(str(comp.get('executed_on') or ''))})"
            st.markdown(line)
            if comp.get('evidence_tier') == 'AUTHORIZATION_BLOCKED':
                st.caption(E.TIER_TEXT['AUTHORIZATION_BLOCKED'])
            if comp.get('last_execution_status') in ('OPERATION_VERIFIED', 'DISCOVERY_ONLY'):
                st.caption('What it supports: ' + md_escape(E.TIER_TEXT.get(comp.get('evidence_tier'), 'not established'), 200)
                           + ' · Not proven: ' + md_escape(comp.get('not_proven', ''), 240))
        with st.expander('Assessment, limitations and next evaluation'):
            labels = dict(data.get('dimensions') or [])
            for key, d in (e.get('dimensions') or {}).items():
                st.markdown(f"**{md_escape(labels.get(key, key), 80)}:** "
                            + chip(E.LEVEL_TEXT.get(d.get('level'), d.get('level', '')), E.LEVEL_COLOR.get(d.get('level'), 'gray'))
                            + ' ' + md_escape(d.get('statement', ''), 400))
            st.caption('Method: ' + md_escape(data.get('assessment_method', ''), 600))
            st.markdown('**Next hands-on evaluation:** ' + md_escape(i['next_hands_on_action'], 300))
            for imp in i.get('improvement_opportunities') or []:
                st.markdown('- Improvement opportunity (hypothesis): ' + md_escape(imp, 200))
