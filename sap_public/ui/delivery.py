"""DELIVERY & CI/CD (public): approved release information only. No internal ports, paths, PRs or commit history."""
from __future__ import annotations

import streamlit as st

from .. import catalog, integrity
from ..contract import ABSENT_CAPABILITIES, EDITION, LIMITS, VERSION
from ..safety import md_escape
from . import common
from .common import chip


def render() -> None:
    rel = catalog.release()
    st.subheader('Release and integrity')
    st.caption('What this public edition is, what has been verified, and what it will not do.')
    content = common.content()['release']
    n_find = len([f for f in content.get('findings', []) if f.get('state') != 'RETRACTED'])
    n_eval = len(content.get('evaluations', []))
    version = content.get('version', 0)
    stage = {'TECHNICAL_PREVIEW': 'Technical preview'}.get(rel.get('release_stage'), 'Not stated')
    accepted = rel.get('owner_acceptance') == 'ACCEPTED'
    st.markdown('**Release status.** Four separate facts; none of them implies another.')
    c1, c2, c3, c4 = st.columns(4)
    with c1.container(border=True):
        st.caption('APPLICATION')
        st.markdown(chip('Release stage: ' + stage + ' build', 'blue'))
        st.caption(f'Version {md_escape(rel["version"])}. A release-stage label only; it makes no statement about hosting.')
    with c2.container(border=True):
        st.caption('OWNER UAT AND ACCEPTANCE')
        st.markdown(chip('Accepted by the owner', 'green') if accepted else chip('Not recorded yet', 'orange'))
        st.caption("Acceptance is the owner's own recorded decision, separate from deployment.")
    with c3.container(border=True):
        st.caption('PUBLISHED EVALUATION CONTENT')
        if n_find or n_eval:
            st.markdown(chip(f'Content release {version} available', 'green'))
        else:
            st.markdown(chip('No evaluation content published yet', 'gray'))
        st.caption('Versioned and hash-verified; see the attestation below.')
    with c4.container(border=True):
        st.caption('APPROVED FINDINGS')
        st.markdown(chip(f'{n_find} approved' if n_find else 'Zero findings approved', 'green' if n_find else 'gray'))
        st.caption('A finding appears only after the owner approves its exact content.')
    st.caption('Official SAP references on the capability pages are source checks, not approved findings.')

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
