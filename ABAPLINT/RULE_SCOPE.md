# Interpreting clean known-defect outcomes

The historical label FALSE_NEGATIVE_OBSERVED is an acceptance-policy label, not an assertion that eight supported upstream rules were broken. This release adds a maintainer-facing classification without rewriting historical records. No POTENTIAL_UPSTREAM_ISSUE is assigned because this review has not established a supported-contract contradiction. The additional EXPECTED_STATIC_RULE_FINDING label denotes expected policy findings in non-blind-spot controls.

Pinned primary implementation inspected: @abaplint/core 2.120.81 build/src/rules/check_syntax.js (ABAPObject only), build/src/rules/cds_parser_error.js (DDLS/DDLX parse errors), build/src/objects/behavior_definition.js (entity-reference extraction), and build/src/abap/5_syntax/statements/call_function.js (missing/not-released function check in Cloud branch). These files are available after npm ci and are not vendored here. Rule metadata links in original diagnostics are retained; current website documentation may differ from the pinned implementation.

| Original clean case | Publication classification | Enabled-rule scope and uncertainty |
|---|---|---|
| [T01_03](cases/T01_03/README.md) | CONFIGURATION_GAP; MISSING_DEPENDENCY | errorNamespace excludes CL_* names. The case intentionally supplies no such class. Silence under this policy is not a supported-rule contradiction. check_syntax resolution is namespace/configuration dependent; missing target SAP catalogs are not supplied. |
| [T03_02](cases/T03_02/README.md) | MISSING_DEPENDENCY; UNSUPPORTED_SEMANTIC_CHECK | The CDS source is absent. cds_parser_error detects parsing, not a complete CDS dependency contract. The selected LSP emitted no source-resolution finding. Pinned cds_parser_error.run handles DDLS/DDLX parse errors. check_syntax.run applies to ABAPObject, not a full CDS semantic verifier. |
| [T03_04](cases/T03_04/README.md) | MISSING_DEPENDENCY; UNSUPPORTED_SEMANTIC_CHECK | Association target is absent. The transpiler reported an unsupported association definition; this is not independently established as an enabled-rule defect. CDS parser coverage does not promise full association/target resolution. |
| [T03_05](cases/T03_05/README.md) | UNSUPPORTED_SEMANTIC_CHECK; MISSING_DEPENDENCY | The referenced behavior implementation is absent. Artifact processing did not execute RAP behavior or prove BDEF semantics. cds_parser_error does not check BDEF, and check_syntax is limited to ABAPObject. No complete BDEF semantic rule was qualified. |
| [T03_06](cases/T03_06/README.md) | UNSUPPORTED_SEMANTIC_CHECK | Deliberately malformed BDEF received no findings. The enabled rules did not provide a qualified BDEF grammar/semantic validator. Pinned BDEF parsing extracts entity references; cds_parser_error covers DDLS/DDLX, not BDEF syntax. |
| [T05_03](cases/T05_03/README.md) | MISSING_DEPENDENCY; UNSUPPORTED_SEMANTIC_CHECK | Classic v758 case supplies no enqueue function/lock object. Invocation fails. The pinned CALL FUNCTION syntax path checks absent functions specifically in Cloud; this case is classic. Pinned call_function.runSyntax performs the missing/not-released function check for LanguageVersion.Cloud, not equivalent classic validation. |
| [T05_04](cases/T05_04/README.md) | MISSING_DEPENDENCY; UNSUPPORTED_SEMANTIC_CHECK | Classic v758 case supplies no update function or SAP scheduler. Invocation fails before update semantics. No supported classic missing-function promise was established. The enabled check_syntax function-resolution behavior differs by language profile; it cannot establish a SAP update environment. |
| [T06_01](cases/T06_01/README.md) | EXPECTED_STATIC_ACCEPTANCE | The valid expression has integer intermediate calculation semantics, while the frozen mathematical oracle requests truncation of the exact quotient. This is a source-contract pitfall, not a requirement a static syntax rule promises to verify. check_syntax does not prove the stated business/mathematical contract. Original 10/27 matches are retained; no runtime defect established. |

Keep configuration namespace, target syntax profile, absent local catalogs, unsupported semantic checks, business-oracle correctness and runtime/adapter behavior separate. The R4 client mismatch belongs to the custom minimal adapter, not a verified upstream defect or SAP vulnerability. T06_01 is a valid expression that fails the chosen mathematical contract; the published negative oracle must not be silently converted into an ABAP semantic oracle. All SAP compiler/release/activation/runtime questions remain unverified.


## Technical revalidation (2026-10-19)

All 42 original cases and 57 source artifacts retained. This is a technical interpretation audit, not a new generation benchmark. All 42 descriptions reconciled; six priority cases reviewed; eight supplemental controls excluded from historical denominators.

5/6 priority interpretations qualified within local evidence; T04_06 release-specific SELECT grammar unresolved. SAP compiler/activation/runtime: NOT_EXECUTED for all cases. Zero demonstrated upstream defects. The eight historical policy acceptance blind spots are not eight product defects.

- T02_05: ordinary available local classes; component/release violation not established.
- T03_05: missing root confounds missing implementation-class attribution; root-only control is not a repaired BO.
- T04_06: classic v758; check_subrc is unrelated to CLIENT SPECIFIED legality. Exact target syntax requires SAP verification.
- T06_06/07/08: valid selected SQLite oracles over an injected NULL; target SAP DDIC physical nullability unverified. Zero-row controls reveal which outputs discriminate the data states.

Historical outcomes remain 21/42 strictly clean, 8 policy acceptance blind spots, 15 locally verified main cases, and selected 57/76 returned matches against 77 frozen expectations. Original-only is 56/75. Retain 19 mismatches and T06_10 missing returned result. Three earlier CDS supplements remain separate.

See [TECHNICAL_REVALIDATION.md](TECHNICAL_REVALIDATION.md).
