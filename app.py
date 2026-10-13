"""SAP AI Evaluation Workbench - public research site (Streamlit Community Cloud entry point).

An evidence-backed, read-only view of the owner's published engineering findings. Five workspaces: Research (home),
Findings, Ask, Capabilities, Method & Evidence. Self-contained: it imports nothing outside this folder and contains no
privileged capability (see sap_public/contract.py and the isolation tests).
"""
from __future__ import annotations

import streamlit as st
from sap_public.ui import ask, common, findings, home, method, tools

st.set_page_config(page_title='SAP AI Evaluation Workbench', page_icon='🧭', layout='wide')

WORKSPACES = (
    ('home', 'Research', ':material/home:', home.render),
    ('findings', 'Findings', ':material/fact_check:', findings.render),
    ('ask', 'Ask the Workbench', ':material/forum:', ask.render),
    ('capabilities', 'Capabilities', ':material/build:', tools.render),
    ('method', 'Method & Evidence', ':material/rule:', method.render),
)
common.PAGES.clear()
for key, title, icon, fn in WORKSPACES:
    common.PAGES[key] = st.Page(fn, title=title, icon=icon, url_path=key, default=(key == 'home'))
st.navigation(list(common.PAGES.values()), position='top').run()
