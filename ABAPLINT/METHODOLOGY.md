# Reproduction method and limits

## Inputs and identities

This package recovers the 42 original frozen synthetic R4 cases from the historical case catalog and verifies every source file against the retained on-disk fixture. It does not regenerate sources from summaries or simplify failed cases. The exact Cloud configuration SHA-256 is **c8c999cac95baa1ebec47b22d735dd9d743184c16073e84e303c78a6a1521146**. It has 22 enabled rule entries, syntax.version=Cloud, errorNamespace=^(Z|Y|LCL_|TY_|LIF_|LTCL_), dependencies=[]. Original v758/v702 variants are separately preserved with their own hashes.

Historical tools: extension 0.6.698, bundled core 2.120.81, Node v24.18.0, transpiler/runtime 2.14.8. The installed LSP server bytes are pinned in [environment.json](results/environment.json). Runtime transpilation uses its own configuration and must not override a Cloud/static rejection. No SAP system is used.

## Setup

Obtain Node with node:sqlite support (historical version v24.18.0), the pinned public npm dependencies, and the public VS Code abaplint extension 0.6.698. Set ABAPLINT_SERVER to that extension's out-native/server.js; it must match the recorded SHA-256. This external distributable is not vendored. There is no remaining unpublished harness dependency: portable source is included, but this is not a dependency-free/self-contained package.

From the ABAPLINT directory:

```text
npm ci --ignore-scripts --no-audit --no-fund
node harness/reproduce.cjs --all
node harness/verify.cjs
```

On Windows invoke npm.cmd. Set ABAPLINT_SERVER with the normal environment mechanism for your platform; do not put personal paths or credentials into tracked files. To reproduce a single case use `node harness/reproduce.cjs T01_03`. All outputs go under ignored .repro/<unique-run>/; tests use only published fixture bytes, original profiles, synthetic dependencies and pinned packages. The runner requires the explicit matching server and reports missing prerequisites as errors. It does not switch to another engine or silently weaken policy.

## Actual LSP procedure

The historical client launched the installed server with --stdio, initialized a filesystem proxy, served only the experiment workspace, verified custom config load/profile/fallback state and source discovery, opened a frozen known-bad sentinel, required its check_syntax diagnostic, then required complete target publications and unchanged input hashes. Target source documents are classes/interfaces/CDS/BDEF; table XML is dependency input, not a separately published target. The included portable derivative preserves those controls while replacing personal paths/output routing. Full sanitized traces and unchanged diagnostic arrays are supplied per case.

## Behavioral procedure and recovery

Original synthetic sources are fed to Transpiler.runRaw; resulting JavaScript is loaded in a fresh runtime per case, and run is invoked with the frozen references. The custom SQLite adapter is intentionally minimal. No SAP roles/clients/DDIC/API catalogs, enqueue/update environment or RAP save sequence is supplied. BDEF/CDS artifact processing alone is not behavior. Unsupported host calls may return status while the surrounding method continues.

Original main attempts give 56/75 returned reference matches. T06_07's separate adapter version changes only terminal UP TO-to-LIMIT translation and adds one match, producing final 57/76 of 77 expectations. T06_10 was invoked but produced no returned reference because no database was initialized. The runner retains both T06_07 versions and compares the selected recovery without replacing original source/oracle. The CDS-DDL 3/3 supplement is published separately and excluded from the frozen-case totals.

## Classification and validation

All cases are synthetic/model-authored, with no independent human-gold or SAP equivalence. Deliberate negatives mean reference ratios are not generation accuracy. No code is fixed to improve reproduction counts. Public sources/configuration are exact copies; logs are sanitized data derivatives and portable harnesses are executable derivatives. [Provenance](results/provenance.json) records both original/public hashes. Only the actual new validation record may establish whether these derivatives reproduce historical outcomes. Historical expected-static categories are sometimes coarse observations rather than exact diagnostic oracles; the public runner compares original observed arrays without inventing expectations.

No GitHub issues are opened. Cases outside verified rule scope are not automatically product bugs. [Rule-scope notes](RULE_SCOPE.md), [case index](CASE_INDEX.md), [historical matrix](results/capability-matrix.json), and [reproduction validation](results/reproduction-validation.json) preserve the relevant distinctions.

## Separate supplement replay

Run `node harness/reproduce-cds-supplement.cjs` to replay the three historical SQLite CDS projection scenarios from the separately frozen supplemental plan. This remains outside the 42-case and 77-expectation denominators.


## Technical revalidation (2026-10-19)

All 42 original cases and 57 source artifacts retained. This is a technical interpretation audit, not a new generation benchmark. All 42 descriptions reconciled; six priority cases reviewed; eight supplemental controls excluded from historical denominators.

5/6 priority interpretations qualified within local evidence; T04_06 release-specific SELECT grammar unresolved. SAP compiler/activation/runtime: NOT_EXECUTED for all cases. Zero demonstrated upstream defects. The eight historical policy acceptance blind spots are not eight product defects.

- T02_05: ordinary available local classes; component/release violation not established.
- T03_05: missing root confounds missing implementation-class attribution; root-only control is not a repaired BO.
- T04_06: classic v758; check_subrc is unrelated to CLIENT SPECIFIED legality. Exact target syntax requires SAP verification.
- T06_06/07/08: valid selected SQLite oracles over an injected NULL; target SAP DDIC physical nullability unverified. Zero-row controls reveal which outputs discriminate the data states.

Historical outcomes remain 21/42 strictly clean, 8 policy acceptance blind spots, 15 locally verified main cases, and selected 57/76 returned matches against 77 frozen expectations. Original-only is 56/75. Retain 19 mismatches and T06_10 missing returned result. Three earlier CDS supplements remain separate.

See [TECHNICAL_REVALIDATION.md](TECHNICAL_REVALIDATION.md).
