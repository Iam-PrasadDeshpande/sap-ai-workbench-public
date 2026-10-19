# R4 technical revalidation

All 42 original cases and 57 source artifacts retained. This is a technical interpretation audit, not a new generation benchmark. All 42 descriptions reconciled; six priority cases reviewed; eight supplemental controls excluded from historical denominators.

5/6 priority interpretations qualified within local evidence; T04_06 release-specific SELECT grammar unresolved. SAP compiler/activation/runtime: NOT_EXECUTED for all cases. Zero demonstrated upstream defects. The eight historical policy acceptance blind spots are not eight product defects.

- T02_05: ordinary available local classes; component/release violation not established.
- T03_05: missing root confounds missing implementation-class attribution; root-only control is not a repaired BO.
- T04_06: classic v758; check_subrc is unrelated to CLIENT SPECIFIED legality. Exact target syntax requires SAP verification.
- T06_06/07/08: valid selected SQLite oracles over an injected NULL; target SAP DDIC physical nullability unverified. Zero-row controls reveal which outputs discriminate the data states.

Historical outcomes remain 21/42 strictly clean, 8 policy acceptance blind spots, 15 locally verified main cases, and selected 57/76 returned matches against 77 frozen expectations. Original-only is 56/75. Retain 19 mismatches and T06_10 missing returned result. Three earlier CDS supplements remain separate.

Reproduce original cases: `node harness/reproduce.cjs --all`. Reproduce separate controls: `node harness/reproduce-tech-controls.cjs`. Both require pinned public dependencies and exact ABAPLINT_SERVER prerequisite described in README. No installation is performed by either command.

See [six-case assessment](results/six-case-technical-assessment.json), [all-case classifications](results/technical-revalidation-cases.json), [CSV](results/technical-revalidation-classification.csv), [source register](results/technical-revalidation-references.json) and [separate controls](supplements/technical_revalidation/README.md).

Source register distinguishes retrieved primary search extracts from unavailable SAP SPA bodies and exact release pages. Current/historical docs inform modeling; none constitutes a SAP compiler invocation. No target-specific grammar claim is made from inaccessible documentation.
