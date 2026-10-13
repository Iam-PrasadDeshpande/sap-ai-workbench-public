"""FINDINGS: browse, filter, read and compare the published findings. Nothing here executes anything."""
from __future__ import annotations

import streamlit as st

from .. import findings as F
from ..safety import https_url_on, md_escape
from . import common
from .common import chip
from .home import finding_card


def _text(item) -> str:
    return item['text'] if isinstance(item, dict) else str(item)


def _bullets(items, empty='None recorded.') -> None:
    items = list(items or [])
    if not items:
        st.caption(empty)
    for it in items:
        basis = it.get('basis') if isinstance(it, dict) else None
        st.markdown('- ' + md_escape(_text(it), 500) + (f'  _({md_escape(basis, 40)})_' if basis else ''))


def detail(f: dict, rel: dict) -> None:
    if f.get('state') == 'RETRACTED':
        st.error(f"This finding was retracted on {md_escape(str(f.get('retracted_on', '?')))}: "
                 f"{md_escape(f.get('retraction_reason', 'no reason recorded'), 300)}. It is kept as a record only.")
        return
    st.header(md_escape(f.get('title', ''), 200))
    ev = F.EVIDENCE_LABEL.get(f.get('evidence_class'), f.get('evidence_label', ''))
    st.markdown(chip(ev, 'blue') + '  ' + chip(md_escape(f.get('validation_status', '?')).title(),
                                               'green' if f.get('validation_status') == 'VALIDATED' else 'orange') +
                '  ' + chip('Executed ' + md_escape(f.get('execution_date', '?')), 'gray'))
    if f.get('state') == 'SUPERSEDED':
        st.warning(f"Superseded by {md_escape(str(f.get('superseded_by', 'a newer finding')))}. Read the newer finding first.")
    if F.is_stale(f):
        st.warning(f"This was executed more than {F.STALE_AFTER_DAYS} days ago. Tools and services change; treat it as "
                   'a dated observation.')
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('#### Engineering question')
        st.write(md_escape(f.get('question', ''), 600))
        st.markdown('#### Objective and setup')
        st.write(md_escape(f.get('objective', ''), 600))
        st.caption(md_escape(f.get('setup', ''), 600))
        st.markdown('#### Where and how it was executed')
        st.write(md_escape(f.get('target', ''), 400) + ' Scope: ' + md_escape(f.get('scope', ''), 120))
    with c2:
        st.markdown('#### What it proves, and what it does not')
        st.write(md_escape(f.get('what_it_proves', ''), 600))
        st.markdown('#### Technology evaluated')
        st.write(md_escape(f.get('technology', ''), 200))
        st.markdown('#### Receipt')
        st.caption('Execution receipt ' + md_escape(str(f.get('receipt_sha256', ''))[:16]) +
                   '… A receipt proves the record is intact, not that SAP behaves as described.')
    st.markdown('#### Verified observations')
    _bullets(f.get('verified_observations'))
    st.markdown('#### Technical findings')
    _bullets(f.get('technical_findings'))
    st.markdown('#### Limitations')
    _bullets(f.get('limitations'), 'No limitations recorded (that does not mean there are none).')
    if f.get('failures'):
        st.markdown('#### Failures')
        _bullets(f.get('failures'))
    st.markdown('#### Improvement opportunities')
    _bullets(f.get('improvements'))
    comp = f.get('comparison') or {}
    st.markdown('#### Comparison')
    st.write(md_escape(comp.get('text', 'No comparable data.'), 500))
    if f.get('sources'):
        st.markdown('#### Sources')
        for s in f['sources']:
            url = s.get('url', '')
            host = url.split('/')[2].lower() if url.startswith('https://') and len(url.split('/')) > 2 else ''
            safe = https_url_on(host, url) if host.endswith('.sap.com') else ''
            st.markdown(f"- [{md_escape(s.get('title') or url, 140)}]({safe})" if safe else '- ' + md_escape(s.get('title', ''), 140))
    st.caption(f"Finding {md_escape(f.get('finding_id', ''))} · published {md_escape(str(f.get('published_at', ''))[:10])} "
               f"· content version {md_escape(str(rel.get('version', '')))}")


def render() -> None:
    c = common.content()
    rel = c['release']
    st.title('Findings')
    st.caption('Published results of hands-on experiments, with their evidence and limits. Read-only.')
    common.content_banner(c)
    items = F.visible(rel)
    tomb = F.retracted(rel)
    if not items and not tomb:
        st.info('No findings are published yet.')
        common.footer()
        return
    sel = st.session_state.get('finding_selected') or st.query_params.get('finding')
    chosen = F.by_id(rel, sel) if sel else None
    if chosen:
        if st.button('← All findings', key='fnd_back'):
            st.session_state.pop('finding_selected', None)
            st.query_params.pop('finding', None)
            st.rerun()
        detail(chosen, rel)
        common.footer()
        return

    techs = sorted({f.get('technology', '') for f in items})
    classes = sorted({f.get('evidence_class', '') for f in items})
    c1, c2, c3 = st.columns(3)
    q = c1.text_input('Search findings', key='fnd_q', max_chars=100).strip().lower()
    tech = c2.multiselect('Technology', techs, key='fnd_tech')
    cls = c3.multiselect('Evidence class', classes, key='fnd_cls', format_func=lambda x: F.EVIDENCE_LABEL.get(x, x))
    shown = [f for f in items if (not tech or f.get('technology') in tech) and (not cls or f.get('evidence_class') in cls)
             and (not q or q in (f.get('title', '') + ' ' + f.get('technology', '') + ' ' + f.get('question', '')).lower())]
    st.caption(f'{len(shown)} of {len(items)} findings')
    for i, f in enumerate(shown):
        finding_card(f, f'fnd_open_{i}')
    if tomb:
        with st.expander(f'Retracted findings ({len(tomb)})'):
            for t in tomb:
                st.markdown(f"- {md_escape(t.get('title', t['finding_id']), 140)} · retracted "
                            f"{md_escape(str(t.get('retracted_on', '?')))}: {md_escape(t.get('retraction_reason', ''), 200)}")

    st.markdown('### Compare two findings')
    if len(items) < 2:
        st.caption('A comparison needs at least two published findings.')
    else:
        names = {f"{f.get('title', '')[:70]} ({f.get('execution_date', '?')})": f for f in items}
        a = st.selectbox('First finding', list(names), key='cmp_a')
        b = st.selectbox('Second finding', list(names), index=1, key='cmp_b')
        fa, fb = names[a], names[b]
        if fa['finding_id'] == fb['finding_id']:
            st.caption('Pick two different findings.')
        else:
            ok, why = F.comparable(fa, fb)
            if not ok:
                st.warning(f'Not comparable: {why}. No comparison is made, because it would be an opinion rather '
                           'than a result.')
            else:
                st.success('Comparable: ' + why + '.')
            cols = st.columns(2)
            for col, f in zip(cols, (fa, fb), strict=True):
                with col.container(border=True):
                    st.markdown(f"**{md_escape(f.get('title', ''), 120)}**")
                    st.caption(md_escape(f.get('execution_date', '')) + ' · ' + md_escape(F.EVIDENCE_LABEL.get(f.get('evidence_class'), '')))
                    for o in (f.get('verified_observations') or [])[:4]:
                        st.markdown('- ' + md_escape(o['text'] if isinstance(o, dict) else o, 200))
                    for o in (f.get('limitations') or [])[:2]:
                        st.caption('Limitation: ' + md_escape(o['text'] if isinstance(o, dict) else o, 200))
    common.footer()
