# T04_04 — Explicit synthetic policy guard

CASE_ID=T04_04

TRACK=T04

ORIGINAL_REQUIREMENT: Explicit synthetic policy guard. The original frozen record defines expectedStatic=OBSERVE; no additional defect assertion. The exact frozen input/output expectations are in [case.json](case.json). R4 did not supply an independently authored enterprise requirements document.

SOURCE_FILES: [zcl_r4_case.clas.abap](src/zcl_r4_case.clas.abap). Source types: ABAP. These files are exact original frozen bytes, not simplified/regenerated examples.

TARGET_LANGUAGE_VERSION=Cloud (historical LSP reports v816 + Cloud)

ABAPLINT_CONFIGURATION=[cloud.json](../../config/cloud.json); [approved hashes](../../config/approved.json). Original 22-rule policy is preserved; v758/v702 profiles are the original explicit R4 variants.

DEPENDENCIES: only the supplied source files, no configured dependency repositories (dependencies=[]). No target SAP catalog, DDIC activation, released API or SAP host environment is supplied.

EXPECTED_DIAGNOSTICS: original category **OBSERVE**. This is an observation/positive-control fixture, not an assertion of full enterprise correctness. The historical expectations do not specify an exact diagnostic message for every case; no exact-message oracle is invented. Behavioral reference arrays are separate.

ACTUAL_DIAGNOSTICS: [original extracted arrays](diagnostics.json); [sanitized full LSP trace](lsp-trace.sanitized.json).

### zcl_r4_case.clas.abap

No diagnostics: original published array is empty.

STATIC_VERDICT=VALIDATION_PASS; historical acceptance classification=LOCAL_VERIFIED.

OFFSTACK_EXECUTION_VERDICT=LOCAL_VERIFIED; selected declared checks 3/3 returned matches, 3 expected. Classification=LOCAL_VERIFIED. [Original output](offstack-original.sanitized.json). 

SAP_VERIFICATION_STATUS=SAP_EVIDENCE_REQUIRED; NOT_EXECUTED. Local iv policy is not SAP authorization; validate user/role/object mapping and all access paths on target.

ROOT_CAUSE_CLASSIFICATION=EXPECTED_STATIC_ACCEPTANCE. No contradiction of a supported static rule contract is established by this case. Retain all policy findings and behavioral outcomes separately.

RULE_SCOPE_AND_UNCERTAINTY: Observed exact rule policy; no SAP correctness inference. See [rule-scope notes](../../RULE_SCOPE.md). No confirmed upstream issue is asserted.

KNOWN_LIMITATIONS: SYNTHETIC_ENTERPRISE_PATTERN; same-investigator synthetic oracle, exact profile/configured dependencies only, limited off-stack host/database coverage. A lint finding or silence cannot establish SAP correctness. Related final-closure capability classifications are included in case.json without replacing the original R4 labels.

REPRODUCTION_STEPS: from ABAPLINT follow [environment setup](../../METHODOLOGY.md), then run `node harness/reproduce.cjs T04_04`. This executes the public portable LSP/runtime derivatives against these exact sources and compares with published historical outputs. Missing prerequisites and mismatches must be reported, not relabeled as passes. Reproduction validation status is recorded separately in [results/reproduction-validation.json](../../results/reproduction-validation.json). No SAP connection is used.

EVIDENCE_PROVENANCE: original logical record `R4/fixtures/cases/T04_04`; config `R4/config/cloud.json`; raw LSP `R4/logs/T04_04.json`; runtime `R4/runtime/T04_04/result.json`. Hash mapping: [publication provenance](../../results/provenance.json). Sources retain original SHA-256; traces/results are sanitized derivatives with separate public hashes. All original local records remain private and unchanged.

PUBLIC_REPRODUCTION_STATUS=REPRODUCED_WITH_EXTERNAL_PINNED_PREREQUISITES. The independently executed public runner matched this case's original static diagnostics and runtime outcome, including any recorded failure. External prerequisites remain required.


## Technical revalidation clarification

This clarification supersedes earlier interpretation where inconsistent; original evidence and scores are retained.

**CASE_ID**: T04_04

**SCENARIO**: Explicit synthetic policy guard

**SOURCE_TYPE**: ABAP

**TEST_CATEGORY**: Simulated semantic scenario

**ABAP_GENUINENESS_ASSESSMENT**: Synthetic language/model fixture, not an extracted or SAP-activated enterprise object. Explicit integer guard simulation; local matched output is not a SAP role or authorization test.

**STATIC_RESULT**: VALIDATION_PASS

**OBSERVED_DIAGNOSTICS**: `{"zcl_r4_case.clas.abap":[]}`

**EXPECTED_BEHAVIOR**: `{"frozenStatic":"OBSERVE","frozenDefect":null,"frozenReferences":[{"input":{"IV":0},"expected":0},{"input":{"IV":1},"expected":1},{"input":{"IV":-1},"expected":0}]}`

**ROOT_CAUSE_CLASSIFICATION**: VALID_REPRESENTATIVE_PATTERN

**OFFSTACK_RESULT**: `{"status":"LOCAL_VERIFIED","returned":3,"matched":3,"frozenExpected":3,"record":"cases/T04_04/offstack-original.sanitized.json","selectedRecord":"cases/T04_04/offstack-original.sanitized.json"}`

**SAP_VALIDATION_REQUIRED**: YES: exact release, compiler/activation, dependency metadata and relevant business runtime. NOT_EXECUTED.

**REPRODUCTION_LINK**: node harness/reproduce.cjs T04_04

**SUPPLEMENTAL_CONTROL_IF_ANY**: `[]`

**INTERPRETATION**: Explicit integer guard simulation; local matched output is not a SAP role or authorization test.
