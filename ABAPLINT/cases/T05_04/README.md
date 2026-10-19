# T05_04 — Absent update function

CASE_ID=T05_04

TRACK=T05

ORIGINAL_REQUIREMENT: Absent update function. The original frozen record defines expectedStatic=DEFECT; Frozen inventory has no update function. SAP update-task scheduler not available.. The exact frozen input/output expectations are in [case.json](case.json). R4 did not supply an independently authored enterprise requirements document.

SOURCE_FILES: [zcl_r4_case.clas.abap](src/zcl_r4_case.clas.abap). Source types: ABAP. These files are exact original frozen bytes, not simplified/regenerated examples.

TARGET_LANGUAGE_VERSION=v758

ABAPLINT_CONFIGURATION=[v758.json](../../config/v758.json); [approved hashes](../../config/approved.json). Original 22-rule policy is preserved; v758/v702 profiles are the original explicit R4 variants.

DEPENDENCIES: only the supplied source files, no configured dependency repositories (dependencies=[]). The case explicitly declares an unavailable dependency. No target SAP catalog, DDIC activation, released API or SAP host environment is supplied.

EXPECTED_DIAGNOSTICS: original category **DEFECT**. Frozen inventory has no update function. SAP update-task scheduler not available. The historical expectations do not specify an exact diagnostic message for every case; no exact-message oracle is invented. Behavioral reference arrays are separate.

ACTUAL_DIAGNOSTICS: [original extracted arrays](diagnostics.json); [sanitized full LSP trace](lsp-trace.sanitized.json).

### zcl_r4_case.clas.abap

No diagnostics: original published array is empty.

STATIC_VERDICT=VALIDATION_PASS; historical acceptance classification=FALSE_NEGATIVE_OBSERVED.

OFFSTACK_EXECUTION_VERDICT=EXECUTION_ERROR; selected declared checks 0/0 returned matches, 0 expected. Classification=UNSUPPORTED. [Original output](offstack-original.sanitized.json). 

SAP_VERIFICATION_STATUS=SAP_EVIDENCE_REQUIRED; NOT_EXECUTED. Target release/compiler, real dependencies, activation and relevant SAP runtime tests.

ROOT_CAUSE_CLASSIFICATION=MISSING_DEPENDENCY; UNSUPPORTED_SEMANTIC_CHECK. Classic v758 case supplies no update function or SAP scheduler. Invocation fails before update semantics. No supported classic missing-function promise was established.

RULE_SCOPE_AND_UNCERTAINTY: The enabled check_syntax function-resolution behavior differs by language profile; it cannot establish a SAP update environment. See [rule-scope notes](../../RULE_SCOPE.md). No confirmed upstream issue is asserted.

KNOWN_LIMITATIONS: SYNTHETIC_ENTERPRISE_PATTERN; same-investigator synthetic oracle, exact profile/configured dependencies only, limited off-stack host/database coverage. A lint finding or silence cannot establish SAP correctness. Related final-closure capability classifications are included in case.json without replacing the original R4 labels.

REPRODUCTION_STEPS: from ABAPLINT follow [environment setup](../../METHODOLOGY.md), then run `node harness/reproduce.cjs T05_04`. This executes the public portable LSP/runtime derivatives against these exact sources and compares with published historical outputs. Missing prerequisites and mismatches must be reported, not relabeled as passes. Reproduction validation status is recorded separately in [results/reproduction-validation.json](../../results/reproduction-validation.json). No SAP connection is used.

EVIDENCE_PROVENANCE: original logical record `R4/fixtures/cases/T05_04`; config `R4/config/v758.json`; raw LSP `R4/logs/T05_04.json`; runtime `R4/runtime/T05_04/result.json`. Hash mapping: [publication provenance](../../results/provenance.json). Sources retain original SHA-256; traces/results are sanitized derivatives with separate public hashes. All original local records remain private and unchanged.

PUBLIC_REPRODUCTION_STATUS=REPRODUCED_WITH_EXTERNAL_PINNED_PREREQUISITES. The independently executed public runner matched this case's original static diagnostics and runtime outcome, including any recorded failure. External prerequisites remain required.


## Technical revalidation clarification

This clarification supersedes earlier interpretation where inconsistent; original evidence and scores are retained.

**CASE_ID**: T05_04

**SCENARIO**: Absent update function

**SOURCE_TYPE**: ABAP

**TEST_CATEGORY**: Intentional negative test

**ABAP_GENUINENESS_ASSESSMENT**: Intentional negative synthetic ABAP/CDS/BDEF input; validity is not assumed. Missing function module metadata. Pinned missing-function check is Cloud-specific while this case uses classic configuration; silence is not an established upstream defect.

**STATIC_RESULT**: VALIDATION_PASS

**OBSERVED_DIAGNOSTICS**: `{"zcl_r4_case.clas.abap":[]}`

**EXPECTED_BEHAVIOR**: `{"frozenStatic":"DEFECT","frozenDefect":"Frozen inventory has no update function. SAP update-task scheduler not available.","frozenReferences":[]}`

**ROOT_CAUSE_CLASSIFICATION**: MISSING_DEPENDENCY_METADATA

**OFFSTACK_RESULT**: `{"status":"UNSUPPORTED","returned":0,"matched":0,"frozenExpected":0,"record":"cases/T05_04/offstack-original.sanitized.json","selectedRecord":"cases/T05_04/offstack-original.sanitized.json"}`

**SAP_VALIDATION_REQUIRED**: YES: exact release, compiler/activation, dependency metadata and relevant business runtime. NOT_EXECUTED.

**REPRODUCTION_LINK**: node harness/reproduce.cjs T05_04

**SUPPLEMENTAL_CONTROL_IF_ANY**: `[]`

**INTERPRETATION**: Missing function module metadata. Pinned missing-function check is Cloud-specific while this case uses classic configuration; silence is not an established upstream defect.
