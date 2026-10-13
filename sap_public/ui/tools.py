"""CAPABILITIES: what has been proven hands-on, what is blocked or unproven, and what each SAP tool needs.\n\nThe capability map comes from the published content bundle (projected from the private workbench); the tool catalogue\nbelow it is static reference data. No access is inferred and nothing is executed here.\n"""
from __future__ import annotations

import streamlit as st

from .. import catalog
from .. import findings as F
from . import common
from ..safety import https_url_on, md_escape
from .common import chip


def render() -> None:
    c = common.content()
    st.title('Capabilities')
    st.caption('What has actually been validated hands-on, what is blocked, and what is not yet established. '
               'Documentation never proves that anyone has access.')
    common.content_banner(c)
    caps = c['release'].get('capabilities') or []
    if not caps:
        st.info('The capability map has not been published yet.')
    order = list(F.STATUS_TEXT)
    for status in order:
        group = [x for x in caps if x.get('status') == status]
        if not group:
            continue
        label, color = F.STATUS_TEXT[status]
        st.subheader(label)
        cols = st.columns(2)
        for i, x in enumerate(group):
            with cols[i % 2].container(border=True):
                st.markdown(f"**{md_escape(x.get('name', ''), 120)}**  " + chip(label, color))
                if x.get('validated_on'):
                    st.caption(f"Last validated {md_escape(str(x['validated_on']))}"
                               + (f" · {md_escape(F.EVIDENCE_LABEL.get(x.get('evidence_class'), ''), 120)}" if x.get('evidence_class') else ''))
                if x.get('invocations'):
                    st.caption('Validated operations: ' + md_escape(', '.join(x['invocations'])[:200]))
                st.write(md_escape(x.get('note', ''), 400))
    with st.expander('SAP developer tool catalogue (what exists and what it needs)', expanded=not caps):
        _catalogue()
    common.footer()


def _catalogue() -> None:
    data = catalog.tools()
    tools = data['tools']
    counts = {}
    for t in tools:
        counts[t['state']] = counts.get(t['state'], 0) + 1
    st.markdown('  '.join(chip(f"{catalog.STATE_TEXT[k][0]} {counts[k]}", catalog.STATE_TEXT[k][1])
                           for k in data['states'] if k in counts))
    query = st.text_input('Filter', key='tools_filter', placeholder='name, e.g. MCP or CAP').strip().lower()
    for state in data['states']:
        group = [t for t in tools if t['state'] == state and (not query or query in (t['name'] + t['what']).lower())]
        if not group:
            continue
        label, color, blurb = catalog.STATE_TEXT[state]
        st.subheader(label)
        st.caption(blurb)
        cols = st.columns(2)
        for i, t in enumerate(group):
            with cols[i % 2].container(border=True):
                st.markdown(f"**{md_escape(t['name'], 120)}**  " + chip(label, color) +
                            ('  ' + chip('runs in this app', 'green') if t.get('runs_here') else ''))
                st.write(md_escape(t['what'], 200))
                st.caption(md_escape(t['note'], 300))
                url = https_url_on(_host(t['url']), t['url'])
                if url:
                    st.markdown(f'[Official source]({url})')
    st.info('Anything that needs a trial, a licence or software on your machine is described here but never run or '
            'simulated by this edition.')


def _host(url: str) -> str:
    return url.split('/')[2].lower() if url.startswith('https://') and len(url.split('/')) > 2 else ''
