"""ASK THE WORKBENCH: questions answered from the owner's published findings only (no model, no private access)."""
from __future__ import annotations

import streamlit as st

from .. import ask as ask_engine
from .. import findings as F
from .. import knowledge, limits
from ..contract import LIMITS
from ..safety import https_url_on, md_escape
from . import common
from .common import chip

EXAMPLES = (
    'What have you actually validated with SAP CAP and MCP?',
    'What are the limitations of AI-assisted ABAP RAP development?',
    'Which SAP AI capabilities are proven hands-on?',
    'How did Fiori/UI5 integration behave?',
    'What remains blocked by SAP trial or license access?',
    'What changed in your latest experiments?',
)
STATUS_CHIP = {'ANSWERED': ('Answered from published findings', 'green'), 'PARTIAL': ('Partly answered', 'orange'),
               'NOT_ESTABLISHED': ('Not established', 'red')}


def _set(q: str) -> None:
    st.session_state['ask_question'] = q
    st.session_state['ask_q_input'] = q
    st.session_state['ask_autorun'] = True


def render() -> None:
    c = common.content()
    rel = c['release']
    st.title('Ask the Workbench')
    st.caption('Answers are assembled from the published findings only. If the published evidence does not cover a '
               'question, the answer says it has not been established. Nothing you type is stored or sent to any '
               'private system.')
    common.content_banner(c)
    if 'ask_q_input' not in st.session_state and st.session_state.get('ask_question'):
        st.session_state['ask_q_input'] = st.session_state['ask_question']
    q = st.text_input('Your question', key='ask_q_input', max_chars=ask_engine.MAX_QUESTION,
                      placeholder='e.g. What have you validated with SAP CAP and MCP?')
    run = st.button('Ask', type='primary', key='ask_run')
    st.caption('Try one of these:')
    cols = st.columns(3)
    for i, ex in enumerate(EXAMPLES):
        cols[i % 3].button(ex, key=f'ask_ex_{i}', on_click=_set, args=(ex,))
    if run:
        st.session_state['ask_question'] = q
    autorun = st.session_state.pop('ask_autorun', False)
    if (run or autorun) and st.session_state.get('ask_question', '').strip():
        st.session_state['ask_active'] = st.session_state['ask_question']      # survives the reruns buttons cause
    question = st.session_state.get('ask_active', '')
    if not question.strip():
        st.info('Ask a question to see which published findings support an answer.')
        common.footer()
        return

    res = ask_engine.answer(question, rel, status_of_content=c['status'])
    label, color = STATUS_CHIP[res['status']]
    st.markdown(chip(label, color) + f"  content version {md_escape(str(res.get('release_version', 0)))}")
    st.write(md_escape(res['summary'], 900))
    for f in res['findings']:
        with st.container(border=True):
            st.markdown(f"**{md_escape(f['title'], 160)}**  " + chip(md_escape(f['validation_status'] or '?').title(),
                        'green' if f['validation_status'] == 'VALIDATED' else 'orange'))
            st.caption(f"Executed {md_escape(str(f['execution_date']))} · evidence: {md_escape(f['evidence_label'] or str(f['evidence_class']))}"
                       + (' · superseded' if f['state'] == 'SUPERSEDED' else '') + (' · older than 180 days' if f['stale'] else ''))
            st.caption('What it supports: ' + md_escape(F.TIER_TEXT.get(f.get('evidence_tier'), 'not established'), 200))
            for line in f['excerpt']:
                st.write(md_escape(line, 300))
            for lim in f['limitations']:
                st.caption('Limitation: ' + md_escape(lim, 240))
            for s in f['sources']:
                url = s['url']
                host = url.split('/')[2].lower() if url.startswith('https://') and len(url.split('/')) > 2 else ''
                safe = https_url_on(host, url) if host.endswith('.sap.com') else ''
                if safe:
                    st.markdown(f"[{md_escape(s['title'] or url, 120)}]({safe})")
            st.caption('Finding ' + md_escape(f['finding_id']))
    for cap in res['capabilities']:
        st.markdown(f"- **{md_escape(cap.get('name', ''), 120)}**: {md_escape(F.STATUS_TEXT.get(cap.get('status'), (str(cap.get('status')), ''))[0], 160)}. "
                    + md_escape(cap.get('note', ''), 240))
    for lim in res['limitations']:
        st.markdown(f"- Limitation ({md_escape(lim['title'], 80)}): {md_escape(lim['text'], 260)}")
    for ch in res['changes']:
        st.markdown('- ' + md_escape(ch if isinstance(ch, str) else str(ch.get('text', '')), 260))
    if res['not_established']:
        with st.expander('What is not established'):
            for n in res['not_established']:
                st.markdown('- ' + md_escape(n, 200))

    st.divider()
    st.markdown('**Supplementary context (optional)**')
    st.caption("SAP's public developer content can add background. It is SAP's documentation, not the owner's "
               'experimental proof, and it is labelled as such.')
    s = common.state()
    reason = limits.check_lookup_allowed(s['lookup_state'])
    if reason:
        st.info(reason)
    if st.button("Look in SAP's public documentation", key='ask_sup', disabled=bool(reason)):
        try:
            knowledge.normalize_question(question)
        except ValueError as exc:
            st.error(md_escape(str(exc)))
        else:
            with st.spinner("Asking SAP's public developer service..."):
                out = knowledge.investigate(question)
            limits.record_lookup(s['lookup_state'])
            if out['failure']:
                st.warning("SAP's public service did not answer cleanly: " + md_escape(out['failure'], 160))
            shown = [x for x in out['sources'] if x['relevance'] != 'WEAK'][:LIMITS['sources_shown']]
            if not shown:
                st.caption('No clearly relevant SAP documentation was returned.')
            for x in shown:
                url = https_url_on('developers.sap.com', x['url'])
                head = f"[{md_escape(x['title'] or x['slug'], 140)}]({url})" if url else md_escape(x['title'] or x['slug'], 140)
                st.markdown('- ' + head + '  ' + chip('SAP documentation', 'gray'))
    common.footer()
