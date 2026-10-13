"""Experiment C: synthetic engineering lab on FABRICATED utility billing exceptions.

Real, deterministic, bounded logic: no randomness, no network, no process, no SAP. Amounts are handled as integer cents.
Nothing here proves anything about SAP S/4HANA, SAP AI Core, Joule or any tenant: it demonstrates a technique.
"""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data' / 'billing_synthetic.csv'
AS_OF = date(2026, 10, 1)                     # fixed so every visitor gets the same, reproducible results
CATEGORIES = ('DUPLICATE_BILL', 'ESTIMATED_READ', 'LATE_PAYMENT_APPLIED', 'METER_FAULT', 'TARIFF_MISMATCH')
STATUSES = ('OPEN', 'IN_REVIEW', 'RESOLVED')
LABEL = 'FABRICATED DATA: generated test records, no real customer, not from any SAP system.'

# The documented reference rule the visitor's criteria are compared with (a stand-in for a business policy).
REFERENCE = {'description': 'High priority = status OPEN and amount of at least 500.00 EUR',
             'statuses': ('OPEN',), 'min_amount_cents': 50_000}


def _cents(text: str) -> int:
    whole, _, frac = str(text).partition('.')
    return int(whole) * 100 + int((frac + '00')[:2])


def load_cases(path: Path = DATA) -> list:
    rows = []
    with Path(path).open(encoding='utf-8', newline='') as fh:
        for r in csv.DictReader(fh):
            opened = date.fromisoformat(r['openedOn'])
            rows.append({'id': r['ID'], 'customer_ref': r['customerRef'], 'meter_id': r['meterId'],
                         'category': r['category'], 'status': r['status'], 'amount_cents': _cents(r['amount']),
                         'currency': r['currency'], 'opened_on': r['openedOn'], 'age_days': (AS_OF - opened).days,
                         'note': r['note']})
    return rows


def money(cents: int, currency: str = 'EUR') -> str:
    return f'{cents // 100}.{cents % 100:02d} {currency}'


def summary(cases: list) -> list:
    out = {}
    for c in cases:
        k = (c['category'], c['status'])
        n, tot = out.get(k, (0, 0))
        out[k] = (n + 1, tot + c['amount_cents'])
    return [{'category': k[0], 'status': k[1], 'cases': n, 'total': money(tot)} for k, (n, tot) in sorted(out.items())]


def _flag(case: dict, crit: dict) -> bool:
    return (case['status'] in crit['statuses'] and case['category'] in crit['categories']
            and case['amount_cents'] >= crit['min_amount_cents'] and case['age_days'] >= crit['min_age_days'])


def normalize_criteria(statuses=None, categories=None, min_amount=0.0, min_age_days=0) -> dict:
    # None means "not specified" (everything); an empty selection means the visitor selected nothing, so nothing matches.
    st = tuple(s for s in (STATUSES if statuses is None else statuses) if s in STATUSES)
    ct = tuple(c for c in (CATEGORIES if categories is None else categories) if c in CATEGORIES)
    cents = max(0, min(10_000_000, int(round(float(min_amount) * 100))))
    age = max(0, min(365, int(min_age_days)))
    return {'statuses': st, 'categories': ct, 'min_amount_cents': cents, 'min_age_days': age}


def evaluate(crit: dict, cases: list | None = None) -> dict:
    """Apply the visitor's criteria and compare the flagged set with the reference rule. Deterministic."""
    cases = cases if cases is not None else load_cases()
    ref = {'statuses': REFERENCE['statuses'], 'categories': CATEGORIES,
           'min_amount_cents': REFERENCE['min_amount_cents'], 'min_age_days': 0}
    flagged = {c['id'] for c in cases if _flag(c, crit)}
    expected = {c['id'] for c in cases if _flag(c, ref)}
    tp, fp, fn = flagged & expected, flagged - expected, expected - flagged
    prec = (len(tp), len(flagged))
    rec = (len(tp), len(expected))
    return {
        'criteria': crit, 'reference': REFERENCE['description'], 'flagged': sorted(flagged), 'expected': sorted(expected),
        'true_positive': sorted(tp), 'false_positive': sorted(fp), 'false_negative': sorted(fn),
        'precision': prec, 'recall': rec, 'matches_reference': flagged == expected,
        'explanation': ('Your criteria flag exactly the reference set.' if flagged == expected else
                        f'{len(fn)} reference case(s) are missed and {len(fp)} extra case(s) are flagged.'),
        'evidence_class': 'SYNTHETIC_DEMONSTRATION', 'label': LABEL,
        'proves': 'That this rule technique behaves as described on these fabricated records. Nothing about SAP.'}


def ratio_text(pair: tuple) -> str:
    n, d = pair
    return 'n/a (nothing flagged)' if d == 0 else f'{n} of {d} ({100 * n // d}%)'


def where_ai_could_add_value() -> list:
    """Static, explicit reasoning about this data set - what a model could and could not contribute."""
    return [
        {'area': 'Reading the free-text note', 'ai_helps': 'Classifying or summarising unstructured notes.',
         'but': 'Here every note is templated, so a rule does as well; the benefit appears with real, messy text.'},
        {'area': 'Threshold choice', 'ai_helps': 'Suggesting thresholds from history.',
         'but': 'This set has no outcome history; a threshold would be a guess, not a learned value.'},
        {'area': 'Explaining a flag to a clerk', 'ai_helps': 'Drafting a plain-language explanation.',
         'but': 'The explanation must cite the record fields; it must not be treated as the decision.'}]


def needs_real_sap_readback() -> list:
    return [
        'Whether these field names and statuses match an SAP S/4HANA Utilities billing document or invoicing exception.',
        'Authorization, volume and performance behaviour of the real OData / API surface.',
        'Whether SAP AI Core, Generative AI Hub or Joule are entitled and behave as documented in your tenant.',
        'Any claim that the technique works on your data: that needs your system, not fabricated records.']
