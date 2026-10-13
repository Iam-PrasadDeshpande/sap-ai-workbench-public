"""Experiment E: improvement analysis. Every item is either OBSERVED (tied to a result) or a HYPOTHESIS, never mixed."""
from __future__ import annotations


def analyse(ledger: list, knowledge: dict | None = None, lab: dict | None = None, comparison: dict | None = None) -> dict:
    observed, hypotheses, improvements, next_evidence, next_activity = [], [], [], [], []

    if knowledge:
        weak = [s for s in knowledge.get('sources', []) if s.get('relevance') == 'WEAK']
        if knowledge.get('failure'):
            observed.append({'text': f"The public lookup failed: {knowledge['failure']}.",
                             'basis': 'knowledge lookup result'})
            improvements.append({'text': 'Retry later; the public service is best-effort.', 'basis': 'OBSERVED'})
        if weak:
            observed.append({'text': f'{len(weak)} of {len(knowledge.get("sources", []))} returned sources look weakly '
                                     'related to the question.', 'basis': 'relevance heuristic on the returned sources'})
            improvements.append({'text': 'Rephrase with the product or tool name; weak matches are hidden by default.',
                                 'basis': 'OBSERVED'})
        if knowledge.get('ok') and not weak:
            hypotheses.append({'text': 'A narrower question may surface more specific tutorials.',
                               'basis': 'HYPOTHESIS: no defect was observed'})
        next_evidence.append('Open the top source and confirm it addresses your scenario.')
        for n in knowledge.get('next', []):
            next_activity.append(n['suggestion'])

    if lab:
        if not lab.get('matches_reference'):
            observed.append({'text': lab['explanation'], 'basis': 'synthetic lab result'})
            if lab.get('false_negative'):
                improvements.append({'text': f"Lower the amount threshold or widen status/category to catch "
                                             f"{len(lab['false_negative'])} missed case(s).", 'basis': 'OBSERVED'})
            if lab.get('false_positive'):
                improvements.append({'text': f"Tighten the criteria to drop {len(lab['false_positive'])} extra case(s).",
                                     'basis': 'OBSERVED'})
        else:
            observed.append({'text': 'The criteria reproduce the reference set exactly.', 'basis': 'synthetic lab result'})
            hypotheses.append({'text': 'A real data set will contain ambiguous cases this fabricated set does not.',
                               'basis': 'HYPOTHESIS: not testable on fabricated records'})
        next_evidence.append('Repeat the same exercise on a small, approved extract from your own system.')
        next_activity.append('Compare the rule baseline with a model-assisted triage on the same cases (private lab).')

    if comparison:
        if comparison.get('lean') in ('DEPENDS', 'NO_PRIORITIES'):
            observed.append({'text': comparison['why'], 'basis': 'comparison tally'})
        hypotheses.append({'text': 'The leaning could change once the required access is available to you.',
                           'basis': 'HYPOTHESIS: depends on your entitlements'})
        next_evidence.extend(comparison.get('required_validation', [])[:2])
        next_activity.append('Run the hands-on step named for the leaning option.')

    if not (knowledge or lab or comparison):
        next_activity.append('Start with the knowledge lookup or the synthetic lab.')

    classes = sorted({e['evidence_class'] for e in ledger})
    if 'PUBLIC_SAP_API' not in classes and ledger:
        next_evidence.append('No retrieval from SAP\'s public developer service is in your ledger yet.')
    if classes and set(classes) <= {'DOCUMENTATION', 'SYNTHETIC_DEMONSTRATION'}:
        observed.append({'text': 'Nothing in your ledger comes from an SAP system.', 'basis': 'ledger composition'})
    return {'observed_limitations': observed, 'hypotheses': hypotheses, 'testable_improvements': improvements,
            'required_next_evidence': list(dict.fromkeys(next_evidence)),
            'next_hands_on_activity': list(dict.fromkeys(next_activity))[:4],
            'note': 'OBSERVED items follow from results above; HYPOTHESIS items are proposals, not findings.'}
