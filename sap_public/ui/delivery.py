"""DELIVERY & CI/CD (public): approved release information only. No internal ports, paths, PRs or commit history."""
from __future__ import annotations

import streamlit as st

from .. import catalog, integrity
from ..contract import ABSENT_CAPABILITIES, EDITION, LIMITS, VERSION
from ..safety import md_escape
from .common import chip


def render() -> None:
    rel = catalog.release()
    st.subheader('Release and integrity')
    st.caption('What this public edition is, what has been verified, and what it will not do.')
    c1, c2, c3 = st.columns(3)
    with c1.container(border=True):
        st.caption('PUBLISHED VERSION')
        st.markdown(f'**{md_escape(rel["version"])}** ' + chip(rel['edition'].replace('_', ' ').title(), 'blue'))
    with c2.container(border=True):
        st.caption('PUBLICATION')
        pub = rel.get('published_on')
        st.markdown(chip('Published ' + md_escape(str(pub)), 'green') if pub else chip('Not yet published', 'orange'))
    with c3.container(border=True):
        st.caption('PUBLIC EXPERIMENT AVAILABILITY')
        st.markdown(chip('Read-only research site', 'green') + '  ' + chip('1 optional SAP documentation lookup', 'blue'))

    st.subheader('Supported capabilities')
    for c in rel['capabilities']:
        st.markdown('- ' + md_escape(c))
    st.subheader('Verified public tests')
    st.write(md_escape(rel.get('verified_public_tests', 'Not recorded.')))
    st.subheader('Known limitations')
    for c in rel['known_limitations']:
        st.markdown('- ' + md_escape(c))
    st.subheader('Release changes')
    for c in rel['changes']:
        st.markdown('- ' + md_escape(c))
    st.subheader('Release attestation')
    att = integrity.verify()
    if att['status'] == 'NOT_VERIFIED':
        st.info('This copy is a development tree without a release manifest, so its integrity is not verified.')
    else:
        st.markdown(chip('Files match the release manifest' if att['status'] == 'VERIFIED' else 'Files differ from the release manifest',
                         'green' if att['status'] == 'VERIFIED' else 'red'))
        st.caption(f"{att['file_count']} files · artifact digest {md_escape(att['digest'][:16])}…. This is a self-check "
                   'that detects accidental drift; it is not a signature.')
    with st.expander('Safety limits and what this edition does not have'):
        st.markdown('\n'.join(f"- {k.replace('_', ' ')}: {v}" for k, v in LIMITS.items()))
        st.markdown('Not present, by construction: ' + ', '.join(c.replace('_', ' ') for c in ABSENT_CAPABILITIES) + '.')
    st.caption(f'{EDITION} {VERSION}. The private engineering edition, its evidence and its release governance are not '
               'part of this application.')
