"""SAP AI Evaluation Workbench - public SAP AI capability evaluation site (Streamlit Community Cloud entry point).

A read-only, evidence-driven view of SAP AI and AI-enabling developer capabilities: the canonical capability catalog,
the owner's approved hands-on evaluations and questions answered from them. Five workspaces: Mission & Overview, SAP AI
Capabilities, Hands-on Evaluations, Ask the Evidence, Evaluation Framework. Self-contained: it imports nothing outside
this folder and contains no privileged capability (see sap_public/contract.py and the isolation tests).
"""
from __future__ import annotations

import streamlit as st
from sap_public.ui import ask, common, findings, home, method, tools

st.set_page_config(page_title='SAP AI Evaluation Workbench', page_icon='🧭', layout='wide')

WORKSPACES = (
    ('home', 'Mission & Overview', ':material/flag:', home.render),
    ('capabilities', 'SAP AI Capabilities', ':material/build:', tools.render),
    ('findings', 'Hands-on Evaluations', ':material/science:', findings.render),
    ('ask', 'Ask the Evidence', ':material/forum:', ask.render),
    ('method', 'Evaluation Framework', ':material/rule:', method.render),
)
common.PAGES.clear()
for key, title, icon, fn in WORKSPACES:
    common.PAGES[key] = st.Page(fn, title=title, icon=icon, url_path=key, default=(key == 'home'))
st.navigation(list(common.PAGES.values()), position='top').run()
