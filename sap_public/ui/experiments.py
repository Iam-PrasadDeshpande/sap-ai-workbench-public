"""EXPERIMENTS: six hands-on exercises, each WHY > WHAT > HOW > RUN > RESULT > NEXT."""
from __future__ import annotations

import streamlit as st

from .. import comparison, improve, knowledge, ledger, limits, report, synthetic
from ..contract import CLAIM_TEXT, EVIDENCE_CLASSES, EVIDENCE_TEXT, LIMITS
from ..safety import md_escape
from . import common
from .common import chip, section

LAYER_TEXT = {
    'TRANSPORT_SUCCESS': 'SAP\'s service answered', 'SCHEMA_VALIDATION': 'The answer had the expected shape',
    'SOURCE_RELEVANCE': 'The sources look relevant', 'ANSWER_GROUNDING': 'The reading path only uses returned sources',
    'OWNER_USEFULNESS': 'It answered your question'}
LAYER_COLOR = {'PASSED': 'green', 'PARTIAL': 'orange', 'FAILED': 'red', 'NOT_ASSESSED': 'gray', 'AWAITING_YOU': 'blue'}


class _NotCacheable(Exception):
    """Carries a failed lookup out of the cache wrapper so failures are never cached."""


@st.cache_data(ttl=LIMITS['cache_ttl_seconds'], max_entries=LIMITS['cache_max_entries'], show_spinner=False)
def _cached_lookup(question: str) -> dict:
    res = knowledge.investigate(question)
    if not res['ok']:
        raise _NotCacheable(res)
    return res


def render() -> None:
    s = common.state()
    st.title('Experiments')
    st.caption('Pick an exercise, run it, and see exactly what it proved. Nothing here contacts an SAP system.')
    names = [n for _, n in common.EXERCISES]
    wanted = common.EXERCISE_NAMES.get(st.session_state.get('exercise', 'knowledge'), names[0])
    picked = common.choose('Exercise', names, key='exercise_pick', default=wanted)
    ex = next(k for k, n in common.EXERCISES if n == picked)
    st.session_state['exercise'] = ex
    {'knowledge': _knowledge, 'architecture-comparison': _comparison, 'synthetic-lab': _lab,
     'evidence-assessment': _evidence, 'improvement-analysis': _improvement, 'learning-report': _report}[ex](s)


def _select(ex: str) -> None:
    st.session_state['exercise'] = ex
    st.session_state['exercise_pick'] = common.EXERCISE_NAMES[ex]


def _next(*targets) -> None:
    section('NEXT', 'What to do next')
    cols = st.columns(len(targets))
    for col, (ex, label) in zip(cols, targets, strict=True):
        col.button(label, key=f'next_{ex}_{label}', on_click=_select, args=(ex,))


# ------------------------------------------------------------------------------------------------ A: knowledge
def _knowledge(s) -> None:
    st.header('SAP knowledge lookup')
    common.lifecycle_strip(('IDENTIFY', 'EVALUATE', 'ALIGN WITH HANDS-ON'))
    c1, c2 = st.columns(2)
    with c1:
        section('WHY', 'The problem')
        st.write('Before choosing tools you need grounded, source-cited guidance. Memory and model guesses are not '
                 'evidence.')
        section('WHAT', 'What you get')
        st.write('Real results from SAP\'s public developer MCP servers: tutorials, concepts and links, each with a '
                 'relevance indication and an honest list of what is still missing.')
    with c2:
        section('HOW', 'How it works')
        st.write('Your question goes to two fixed SAP endpoints (search and knowledge graph) using read-only tools. '
                 'No other address can be reached. The results are scored by a transparent term-overlap check; no AI '
                 'model is involved.')
        st.caption('Limits: 300 characters, 15 lookups per session, results cached for 10 minutes.')
    section('RUN', 'Ask a question')
    q = st.text_input('Your SAP engineering question', max_chars=LIMITS['question_max_chars'], key='k_question',
                      placeholder='e.g. How do I expose a CAP service to an AI agent?')
    reason = limits.check_lookup_allowed(s['lookup_state'])
    if reason:
        st.info(reason)
    if st.button('Look it up in SAP\'s developer content', type='primary', key='k_run', disabled=bool(reason)):
        try:
            knowledge.normalize_question(q)
        except ValueError as exc:
            st.error(md_escape(str(exc)))
        else:
            with st.spinner('Asking SAP\'s public developer service...'):
                try:
                    res = _cached_lookup(q)
                except _NotCacheable as nc:
                    res = nc.args[0]
            limits.record_lookup(s['lookup_state'])      # stamped at completion so slow lookups still space out
            s['knowledge'] = res
            if res['sources']:
                common.add_evidence(ledger.new_entry(
                    'knowledge', f"Lookup: {res['question'][:80]}", 'PUBLIC_SAP_API',
                    f"{len(res['sources'])} sources retrieved from SAP's public developer service",
                    source='developers.sap.com', limitations=res['limitations'],
                    details={'retrieved_at': res['retrieved_at']}))
    section('RESULT', 'What came back')
    res = s['knowledge']
    if not res:
        st.info('No lookup yet. Ask a question above.')
    else:
        _knowledge_result(res)
    _next(('architecture-comparison', 'Compare two SAP approaches'), ('synthetic-lab', 'Try the synthetic lab'))


def _knowledge_result(res: dict) -> None:
    if res['failure']:
        st.warning('SAP\'s public service did not answer cleanly: ' + md_escape(res['failure']) +
                   '. This is a normal outcome for a best-effort public service; try again later.')
    st.markdown(chip(EVIDENCE_TEXT[res['evidence_class']][0], 'green' if res['ok'] else 'orange') +
                f"  retrieved {md_escape(res['retrieved_at'])}")
    st.markdown('**What was and was not shown**')
    for ly in res['layers']:
        a, b, c = st.columns([3, 2, 5])
        a.write(LAYER_TEXT[ly['layer']])
        b.markdown(chip(ly['status'].replace('_', ' ').title(), LAYER_COLOR.get(ly['status'], 'gray')))
        c.caption(md_escape(ly['detail']))
    good = [x for x in res['sources'] if x['relevance'] != 'WEAK']
    weak = [x for x in res['sources'] if x['relevance'] == 'WEAK']
    st.markdown('**Sources, most relevant first** (relevance is a heuristic, not a judgement)')
    for src in good:
        _source(src)
    if weak:
        with st.expander(f'Weak or low-signal matches ({len(weak)})'):
            for src in weak:
                _source(src)
    if not res['sources']:
        st.caption('No sources were returned.')
    if res['concepts']:
        st.markdown('**Related concepts:** ' + ', '.join(md_escape(c['name']) for c in res['concepts']))
    with st.expander('What is still missing'):
        for m in res['missing_evidence']:
            st.markdown('- ' + md_escape(m))
        st.caption(md_escape(res['limitations']))


def _source(src: dict) -> None:
    title = md_escape(src['title'] or src['slug'] or 'untitled', 160)
    head = f"[{title}]({src['url']})" if src['url'] else title
    col = {'STRONG': 'green', 'MODERATE': 'blue', 'WEAK': 'orange'}[src['relevance']]
    st.markdown(f"- {head} · {chip(src['relevance'].title(), col)} · {md_escape(src['reason'], 160)}")
    if src.get('snippet'):
        st.caption(md_escape(src['snippet'], 260))


# ------------------------------------------------------------------------------------- B: architecture comparison
def _comparison(s) -> None:
    st.header('Architecture comparison')
    common.lifecycle_strip(('EVALUATE', 'COMPARE'))
    data = comparison.load()
    section('WHY', 'The problem')
    st.write('Choosing between SAP approaches is a trade-off. This lays the facts side by side and labels where each '
             'one comes from.')
    section('WHAT', 'What you get')
    st.write('A qualitative comparison with source labels, plus a transparent tally of your own priorities. There are '
             'no scores, percentages or prices.')
    section('HOW', 'How it works')
    st.write('Curated, versioned data. Each statement is marked as published documentation or as an observation from the '
             'project\'s own test runs in a private environment (assistant-run, not independently verified).')
    section('RUN', 'Choose a scenario and your priorities')
    titles = {p['title']: p['id'] for p in data['pairs']}
    title = st.selectbox('Scenario', list(titles), key='cmp_pair')
    pair = comparison.pair_by_id(data, titles[title])
    st.caption(md_escape(pair['question']))
    labels = {p['text']: p['id'] for p in pair['priorities']}
    picked = st.multiselect('Your priorities', list(labels), key=f"cmp_prio_{pair['id']}")
    if st.button('Compare', type='primary', key='cmp_run'):
        s['comparison'] = comparison.assess(pair, [labels[p] for p in picked])
        common.add_evidence(ledger.new_entry(
            'comparison', pair['title'][:100], 'DOCUMENTATION',
            f"Qualitative comparison; leaning: {s['comparison']['lean_name'] or s['comparison']['lean']}",
            limitations='Documentation and project test observations only; nothing executed here.'))
    section('RESULT', 'The comparison')
    cols = st.columns(len(pair['options']))
    facets = dict(data['facets'])
    for col, opt in zip(cols, pair['options'], strict=True):
        with col.container(border=True):
            st.markdown(f"**{md_escape(opt['name'], 140)}**")
            for key, label in facets.items():
                cell = opt['cells'][key]
                st.markdown(f"_{md_escape(label)}_  \n{md_escape(cell['text'], 500)}")
                st.markdown(chip('Observed in project tests' if cell['basis'] == 'PROJECT_TEST_OBSERVATION' else 'Documentation',
                                 'violet' if cell['basis'] == 'PROJECT_TEST_OBSERVATION' else 'gray') +
                            (f"  [source]({cell['source']})" if cell['source'] else ''))
    res = s['comparison']
    if res and res['pair_id'] == pair['id']:
        with st.container(border=True):
            lean = res['lean_name'] or {'DEPENDS': 'It depends', 'NO_PRIORITIES': 'Select priorities first'}[res['lean']]
            st.markdown(f"**Leaning (qualitative): {md_escape(lean)}**")
            st.write(md_escape(res['why']))
            for r in res['reasons']:
                st.markdown(f"- {md_escape(r['priority'])} → {md_escape(r['option'], 80)}: {md_escape(r['because'])}")
            st.caption(md_escape(res['caveat']))
    _next(('synthetic-lab', 'Try the synthetic lab'), ('evidence-assessment', 'Check what is proven'))


# ------------------------------------------------------------------------------------------- C: synthetic lab
def _lab(s) -> None:
    st.header('Synthetic billing lab')
    common.lifecycle_strip(('ALIGN WITH HANDS-ON', 'PROVE', 'COMPARE'))
    st.warning(synthetic.LABEL)
    cases = synthetic.load_cases()
    section('WHY', 'The problem')
    st.write('Billing exceptions pile up; someone must decide which to look at first. A deterministic rule is the '
             'baseline any AI approach has to beat.')
    section('WHAT', 'What you get')
    st.write('Set your own triage criteria and see exactly which cases they flag, compared with a documented '
             'reference rule, with every difference listed.')
    section('HOW', 'How it works')
    st.write('Plain, deterministic code over 48 fabricated records. No randomness, no network, no model, no SAP system.')
    st.caption('Reference rule: ' + synthetic.REFERENCE['description'] + f'. As-of date fixed at {synthetic.AS_OF}.')
    section('RUN', 'Set your criteria')
    c1, c2 = st.columns(2)
    statuses = c1.multiselect('Statuses to flag', synthetic.STATUSES, default=['OPEN'], key='lab_status')
    cats = c1.multiselect('Categories to flag', synthetic.CATEGORIES, default=list(synthetic.CATEGORIES), key='lab_cat')
    amount = c2.slider('Minimum amount (EUR)', 0, 2000, 500, step=25, key='lab_amount')
    age = c2.slider('Minimum age (days)', 0, 90, 0, step=5, key='lab_age')
    crit = synthetic.normalize_criteria(statuses, cats, amount, age)
    if st.button('Evaluate my criteria', type='primary', key='lab_run'):
        s['lab'] = synthetic.evaluate(crit, cases)
        common.add_evidence(ledger.new_entry(
            'lab', 'Synthetic billing triage', 'SYNTHETIC_DEMONSTRATION',
            f"{len(s['lab']['flagged'])} flagged; reference {len(s['lab']['expected'])}; "
            f"matches reference: {s['lab']['matches_reference']}",
            limitations='Fabricated records; proves a technique, not SAP behaviour.'))
    section('RESULT', 'What your criteria did')
    lab = s['lab']
    if not lab:
        st.info('Press "Evaluate my criteria".')
        st.markdown('**The data (fabricated)**')
        st.table([{k: str(v) for k, v in r.items()} for r in synthetic.summary(cases)])
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric('Flagged by you', len(lab['flagged']))
        m2.metric('In the reference set', len(lab['expected']))
        m3.metric('Agreement', 'exact' if lab['matches_reference'] else 'differs')
        st.write(md_escape(lab['explanation']))
        st.caption(f"Precision: {synthetic.ratio_text(tuple(lab['precision']))} · recall: "
                   f"{synthetic.ratio_text(tuple(lab['recall']))} · evidence: {EVIDENCE_TEXT['SYNTHETIC_DEMONSTRATION'][0]}")
        by_id = {c['id']: c for c in cases}
        for title, key in (('Missed (in reference, not flagged)', 'false_negative'),
                           ('Extra (flagged, not in reference)', 'false_positive')):
            if lab[key]:
                with st.expander(f'{title}: {len(lab[key])}'):
                    st.table([{'case': i, 'category': by_id[i]['category'], 'status': by_id[i]['status'],
                               'amount': synthetic.money(by_id[i]['amount_cents'])} for i in lab[key][:30]])
        st.download_button('Download this result as CSV', report.lab_csv(lab, cases), report.filename('lab', '.csv'),
                           'text/csv', key='lab_csv')
    with st.expander('Inspect a single case'):
        pick = st.selectbox('Case', [c['id'] for c in cases], key='lab_case')
        c = next(x for x in cases if x['id'] == pick)
        st.table([{'field': k, 'value': str(v)} for k, v in c.items() if k != 'amount_cents'] +
                 [{'field': 'amount', 'value': synthetic.money(c['amount_cents'], c['currency'])}])
        st.caption(synthetic.LABEL)
    with st.expander('Where could an AI model add value here?'):
        for r in synthetic.where_ai_could_add_value():
            st.markdown(f"**{md_escape(r['area'])}** — {md_escape(r['ai_helps'])} _But:_ {md_escape(r['but'])}")
    with st.expander('What would need real SAP readback'):
        for t in synthetic.needs_real_sap_readback():
            st.markdown('- ' + md_escape(t))
    _next(('evidence-assessment', 'Check what is proven'), ('improvement-analysis', 'See what to improve'))


# ------------------------------------------------------------------------------------ D: evidence assessment
def _evidence(s) -> None:
    st.header('Evidence assessment')
    common.lifecycle_strip(('PROVE', 'COMPARE'))
    section('WHY', 'The problem')
    st.write('A result is only as strong as its evidence. Documentation, a live lookup, a synthetic run and an SAP '
             'system readback are different things.')
    section('WHAT', 'What you get')
    st.write('Your session ledger, and a check of which claims it can and cannot support.')
    section('HOW', 'How it works')
    st.write('Fixed rules map each claim to the evidence kind it needs. This edition can create three kinds; the others '
             'are refused by construction.')
    section('RUN', 'Check a claim')
    claim_names = {v: k for k, v in CLAIM_TEXT.items()}
    claim = st.selectbox('Claim', list(claim_names), key='ev_claim')
    res = ledger.assess_claim(s['ledger'], claim_names[claim])
    section('RESULT', 'What your evidence supports')
    col = {'SUPPORTED': 'green', 'NOT_YET_SUPPORTED': 'orange', 'CANNOT_BE_PROVEN_HERE': 'gray'}[res['status']]
    st.markdown(chip(res['status'].replace('_', ' ').title(), col) + '  ' + md_escape(res['explanation']))
    for n in res['needs']:
        st.markdown(f"- Needs: {md_escape(n['label'])} - {'present' if n['present'] else 'not present'}"
                    f"{'' if n['creatable_here'] else ' (cannot be created in this edition)'}")
    st.markdown('**Your session ledger**')
    if not s['ledger']:
        st.info('The ledger is empty. Run an exercise to add evidence.')
    else:
        st.table([{'kind': e['evidence_class'], 'title': e['title'], 'summary': e['summary'],
                   'limits': e['limitations'], 'recorded': e['recorded_at']} for e in s['ledger']])
    with st.expander('Try to add a piece of evidence by hand'):
        cls = st.selectbox('Evidence class', list(EVIDENCE_CLASSES), key='ev_cls')
        text = st.text_input('Describe it (max 300 characters)', max_chars=300, key='ev_text')
        if st.button('Add to ledger', key='ev_add'):
            try:
                common.add_evidence(ledger.new_entry('manual', 'Manual entry', cls, text or 'no description'))
                st.success('Added to your session ledger (documentation-grade; it proves nothing about SAP).')
            except ledger.EvidenceRefused as exc:
                st.error(md_escape(str(exc), 300))
    _next(('improvement-analysis', 'See what to improve'), ('learning-report', 'Build the report'))


# ------------------------------------------------------------------------------------- E: improvement analysis
def _improvement(s) -> None:
    st.header('Improvement analysis')
    common.lifecycle_strip(('COMPARE', 'SCOPE FOR IMPROVEMENT'))
    section('WHY', 'The problem')
    st.write('Every result has limits. The useful question is what you could improve, and what evidence would show it.')
    section('WHAT', 'What you get')
    st.write('Observed limitations, hypotheses, testable improvements, the evidence you still need and the next hands-on '
             'step. Observations and hypotheses are never mixed.')
    section('HOW', 'How it works')
    st.write('Deterministic rules over your session results. No model writes these.')
    section('RUN', 'Analyse my session')
    result = improve.analyse(s['ledger'], s['knowledge'], s['lab'], s['comparison'])
    section('RESULT', 'What this shows')
    for key, title in (('observed_limitations', 'Observed limitations'), ('hypotheses', 'Hypotheses (proposals, not findings)'),
                       ('testable_improvements', 'Testable improvements')):
        st.markdown(f'**{title}**')
        items = result[key]
        if not items:
            st.caption('None from your results so far.')
        for i in items:
            st.markdown(f"- {md_escape(i['text'])}  \n  _{md_escape(i['basis'], 160)}_")
    st.markdown('**Required next evidence**')
    for t in result['required_next_evidence'] or ['Run an exercise first.']:
        st.markdown('- ' + md_escape(t))
    st.markdown('**Next hands-on activity**')
    for t in result['next_hands_on_activity']:
        st.markdown('- ' + md_escape(t))
    st.caption(md_escape(result['note']))
    _next(('learning-report', 'Build the report'), ('knowledge', 'Ask another question'))


# ------------------------------------------------------------------------------------------- F: learning report
def _report(s) -> None:
    st.header('Learning report')
    common.lifecycle_strip(('SCOPE FOR IMPROVEMENT',))
    section('WHY', 'The problem')
    st.write('You want to take what you learned somewhere else: a ticket, a design note, a colleague.')
    section('WHAT', 'What you get')
    st.write('A sanitized Markdown or JSON report of this session. Nothing is stored on any server.')
    section('HOW', 'How it works')
    st.write('Built from your session results only. Text is neutralized so the file cannot carry links, scripts or '
             'spreadsheet formulas.')
    section('RUN', 'Name your scenario')
    scenario = st.text_input('Scenario (optional)', max_chars=200, key='rep_scenario')
    claims = [ledger.assess_claim(s['ledger'], c) for c in ('EXISTS_IN_SAP_DOCS', 'TECHNIQUE_IS_SOUND',
                                                            'WORKS_IN_MY_TENANT')]
    imp = improve.analyse(s['ledger'], s['knowledge'], s['lab'], s['comparison'])
    rep = report.build(scenario, s['knowledge'], s['comparison'], s['lab'], s['ledger'], imp, claims)
    section('RESULT', 'Your report')
    md = report.to_markdown(rep)
    c1, c2 = st.columns(2)
    c1.download_button('Download Markdown', md, report.filename('report', '.md'), 'text/markdown', key='rep_md')
    c2.download_button('Download JSON', report.to_json(rep), report.filename('report', '.json'), 'application/json',
                       key='rep_json')
    with st.expander('Preview'):
        st.text(md)
    _next(('knowledge', 'Ask another question'), ('architecture-comparison', 'Compare approaches'))
