"""Knowledge-session page: the ONE presentation implementation, used by the private workbench and the public site.

This file is the single source. scripts/sync_shared_ui.py copies it byte-for-byte into the two apps that render it
and a test fails if either copy differs, so the two UIs cannot drift apart. It imports only streamlit: everything
app-specific (the segmented control, the badge markup, the Markdown block splitter, text escaping) is passed in by the
caller, which is why it can be shipped in a public artifact that must not import any private module.

It is read-only presentation. It executes nothing, calls no network and reads no file: the caller hands it an
already-verified view model.

View model (dict):
  key_prefix   widget-key prefix, unique per host app
  heading      '<id>: <title>'                    subtitle  one line
  meta         [{'caption': str, 'text': str} | {'caption': str, 'chip': (label, colour)}]  (three columns)
  identity     None | {'lines': [markdown], 'caption': str}             'Content identity' expander
  views        [{'key', 'name', 'sections': [{'number', 'title', 'markdown', 'diagram': bool}]}]
  claims       [{'claim_id', 'claim', 'evidence_class', ...}]           shown on the 'references' view
  claim_columns, claims_title
  references   [{'label', 'url'}]                                       shown on the 'references' view
  diagram      None | {'source': path-or-svg, 'caption': str, 'mermaid': str | None}
  footer       caption shown under the page
"""
from __future__ import annotations

import streamlit as st


def render(vm: dict, *, choose, chip, blocks, plain, esc=lambda s, n=0: s) -> None:
    p = vm['key_prefix']
    st.subheader(esc(vm['heading'], 220))
    if vm.get('subtitle'):
        st.caption(esc(vm['subtitle'], 400))
    meta = vm.get('meta') or []
    if meta:
        for col, m in zip(st.columns(len(meta)), meta, strict=False):
            col.caption(m['caption'])
            if 'chip' in m:
                col.markdown(chip(*m['chip']))
            else:
                col.markdown(esc(m['text'], 120))
    ident = vm.get('identity')
    if ident:
        with st.expander('Content identity', expanded=False):
            for line in ident['lines']:
                st.markdown(line)
            if ident.get('caption'):
                st.caption(ident['caption'])
    views = vm['views']
    names = [v['name'] for v in views]
    pick = choose('Section', names, key=f'{p}_view', default=st.query_params.get('ksview'))
    view = next(v for v in views if v['name'] == pick)
    for idx, sec in enumerate(view['sections']):
        with st.expander(f"{sec['number']}. {esc(sec['title'], 160)}", expanded=(idx == 0)):
            _blocks(vm, sec, f"{view['key']}_{sec['number']}", blocks, plain)
    if view['key'] == 'references':
        claims = vm.get('claims') or []
        if claims:
            st.markdown('#### ' + vm.get('claims_title', 'Claim register'))
            classes = sorted({str(c.get('evidence_class', '')) for c in claims})
            want = st.multiselect('Evidence class', classes, key=f'{p}_class')
            rows = [c for c in claims if not want or str(c.get('evidence_class', '')) in want]
            cols = vm.get('claim_columns') or ('claim_id', 'claim', 'evidence_class', 'limitation')
            st.dataframe([{k: plain(str(r.get(k, ''))) for k in cols} for r in rows], hide_index=True, height=360)
        refs = vm.get('references') or []
        if refs:
            st.markdown('#### Official references')
            for r in refs:
                st.markdown(f"- [{esc(r.get('label', ''), 160)}]({r.get('url', '')})")
    if vm.get('footer'):
        st.caption(vm['footer'])


def _diagram(vm: dict) -> None:
    d = vm.get('diagram')
    if not d:
        return
    st.image(d['source'], caption=d.get('caption', ''))
    if d.get('mermaid'):
        with st.expander('Diagram source (Mermaid) and text explanation'):
            st.code(d['mermaid'], language='text')


def _blocks(vm: dict, sec: dict, key: str, blocks, plain) -> None:
    n = 0
    for b in blocks(sec['markdown']):
        n += 1
        if b[0] == 'text':
            st.markdown(b[1])
        elif b[0] == 'table':
            header, rows = b[1], b[2]
            data = [{h: plain(c) for h, c in zip(header, r, strict=False)} for r in rows]
            st.dataframe(data, hide_index=True, key=f"{vm['key_prefix']}_t_{key}_{n}")
        elif b[0] == 'diagram':
            _diagram(vm)
    if sec.get('diagram'):
        _diagram(vm)
