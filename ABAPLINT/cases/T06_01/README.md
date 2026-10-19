# T06_01 — R3 regression: integer intermediate before truncation

CASE_ID=T06_01

TRACK=T06

ORIGINAL_REQUIREMENT: R3 regression: integer intermediate before truncation. The original frozen record defines expectedStatic=OBSERVE; Frozen mathematical contract truncates exact rational toward zero; integer intermediate may violate it.. The exact frozen input/output expectations are in [case.json](case.json). R4 did not supply an independently authored enterprise requirements document.

SOURCE_FILES: [zcl_r4_case.clas.abap](src/zcl_r4_case.clas.abap). Source types: ABAP. These files are exact original frozen bytes, not simplified/regenerated examples.

TARGET_LANGUAGE_VERSION=Cloud (historical LSP reports v816 + Cloud)

ABAPLINT_CONFIGURATION=[cloud.json](../../config/cloud.json); [approved hashes](../../config/approved.json). Original 22-rule policy is preserved; v758/v702 profiles are the original explicit R4 variants.

DEPENDENCIES: only the supplied source files, no configured dependency repositories (dependencies=[]). No target SAP catalog, DDIC activation, released API or SAP host environment is supplied.

EXPECTED_DIAGNOSTICS: original category **OBSERVE**. Frozen mathematical contract truncates exact rational toward zero; integer intermediate may violate it. The historical expectations do not specify an exact diagnostic message for every case; no exact-message oracle is invented. Behavioral reference arrays are separate.

ACTUAL_DIAGNOSTICS: [original extracted arrays](diagnostics.json); [sanitized full LSP trace](lsp-trace.sanitized.json).

### zcl_r4_case.clas.abap

No diagnostics: original published array is empty.

STATIC_VERDICT=VALIDATION_PASS; historical acceptance classification=FALSE_NEGATIVE_OBSERVED.

OFFSTACK_EXECUTION_VERDICT=REFERENCE_MISMATCH; selected declared checks 10/27 returned matches, 27 expected. Classification=PARTIAL. [Original output](offstack-original.sanitized.json). 

SAP_VERIFICATION_STATUS=SAP_EVIDENCE_REQUIRED; NOT_EXECUTED. Target release/compiler, real dependencies, activation and relevant SAP runtime tests.

ROOT_CAUSE_CLASSIFICATION=EXPECTED_STATIC_ACCEPTANCE. The valid expression has integer intermediate calculation semantics, while the frozen mathematical oracle requests truncation of the exact quotient. This is a source-contract pitfall, not a requirement a static syntax rule promises to verify.

RULE_SCOPE_AND_UNCERTAINTY: check_syntax does not prove the stated business/mathematical contract. Original 10/27 matches are retained; no runtime defect established. See [rule-scope notes](../../RULE_SCOPE.md). No confirmed upstream issue is asserted.

KNOWN_LIMITATIONS: R3_ARITHMETIC_REGRESSION_PATTERN; same-investigator synthetic oracle, exact profile/configured dependencies only, limited off-stack host/database coverage. A lint finding or silence cannot establish SAP correctness. Related final-closure capability classifications are included in case.json without replacing the original R4 labels.

REPRODUCTION_STEPS: from ABAPLINT follow [environment setup](../../METHODOLOGY.md), then run `node harness/reproduce.cjs T06_01`. This executes the public portable LSP/runtime derivatives against these exact sources and compares with published historical outputs. Missing prerequisites and mismatches must be reported, not relabeled as passes. Reproduction validation status is recorded separately in [results/reproduction-validation.json](../../results/reproduction-validation.json). No SAP connection is used.

EVIDENCE_PROVENANCE: original logical record `R4/fixtures/cases/T06_01`; config `R4/config/cloud.json`; raw LSP `R4/logs/T06_01.json`; runtime `R4/runtime/T06_01/result.json`. Hash mapping: [publication provenance](../../results/provenance.json). Sources retain original SHA-256; traces/results are sanitized derivatives with separate public hashes. All original local records remain private and unchanged.

PUBLIC_REPRODUCTION_STATUS=REPRODUCED_WITH_EXTERNAL_PINNED_PREREQUISITES. The independently executed public runner matched this case's original static diagnostics and runtime outcome, including any recorded failure. External prerequisites remain required.


## Technical revalidation clarification

This clarification supersedes earlier interpretation where inconsistent; original evidence and scores are retained.

**CASE_ID**: T06_01

**SCENARIO**: R3 regression: integer intermediate before truncation

**SOURCE_TYPE**: ABAP

**TEST_CATEGORY**: Intentional negative test

**ABAP_GENUINENESS_ASSESSMENT**: Intentional negative synthetic ABAP/CDS/BDEF input; validity is not assumed. ABAP numeric expression is a negative against the mathematical oracle; 17 mismatches do not imply that check_syntax promises mathematical contract verification.

**STATIC_RESULT**: VALIDATION_PASS

**OBSERVED_DIAGNOSTICS**: `{"zcl_r4_case.clas.abap":[]}`

**EXPECTED_BEHAVIOR**: `{"frozenStatic":"OBSERVE","frozenDefect":"Frozen mathematical contract truncates exact rational toward zero; integer intermediate may violate it.","frozenReferences":[{"input":{"NUMERATOR":-7,"DENOMINATOR":-2},"expected":3},{"input":{"NUMERATOR":-7,"DENOMINATOR":2},"expected":-3},{"input":{"NUMERATOR":-7,"DENOMINATOR":3},"expected":-2},{"input":{"NUMERATOR":-5,"DENOMINATOR":-2},"expected":2},{"input":{"NUMERATOR":-5,"DENOMINATOR":2},"expected":-2},{"input":{"NUMERATOR":-5,"DENOMINATOR":3},"expected":-1},{"input":{"NUMERATOR":-1,"DENOMINATOR":-2},"expected":0},{"input":{"NUMERATOR":-1,"DENOMINATOR":2},"expected":0},{"input":{"NUMERATOR":-1,"DENOMINATOR":3},"expected":0},{"input":{"NUMERATOR":0,"DENOMINATOR":-2},"expected":0},{"input":{"NUMERATOR":0,"DENOMINATOR":2},"expected":0},{"input":{"NUMERATOR":0,"DENOMINATOR":3},"expected":0},{"input":{"NUMERATOR":1,"DENOMINATOR":-2},"expected":0},{"input":{"NUMERATOR":1,"DENOMINATOR":2},"expected":0},{"input":{"NUMERATOR":1,"DENOMINATOR":3},"expected":0},{"input":{"NUMERATOR":5,"DENOMINATOR":-2},"expected":-2},{"input":{"NUMERATOR":5,"DENOMINATOR":2},"expected":2},{"input":{"NUMERATOR":5,"DENOMINATOR":3},"expected":1},{"input":{"NUMERATOR":7,"DENOMINATOR":-2},"expected":-3},{"input":{"NUMERATOR":7,"DENOMINATOR":2},"expected":3},{"input":{"NUMERATOR":7,"DENOMINATOR":3},"expected":2},{"input":{"NUMERATOR":2147483647,"DENOMINATOR":-2},"expected":-1073741823},{"input":{"NUMERATOR":2147483647,"DENOMINATOR":2},"expected":1073741823},{"input":{"NUMERATOR":2147483647,"DENOMINATOR":3},"expected":715827882},{"input":{"NUMERATOR":-2147483648,"DENOMINATOR":-2},"expected":1073741824},{"input":{"NUMERATOR":-2147483648,"DENOMINATOR":2},"expected":-1073741824},{"input":{"NUMERATOR":-2147483648,"DENOMINATOR":3},"expected":-715827882}]}`

**ROOT_CAUSE_CLASSIFICATION**: VALID_NEGATIVE_TEST

**OFFSTACK_RESULT**: `{"status":"PARTIAL","returned":27,"matched":10,"frozenExpected":27,"record":"cases/T06_01/offstack-original.sanitized.json","selectedRecord":"cases/T06_01/offstack-original.sanitized.json"}`

**SAP_VALIDATION_REQUIRED**: YES: exact release, compiler/activation, dependency metadata and relevant business runtime. NOT_EXECUTED.

**REPRODUCTION_LINK**: node harness/reproduce.cjs T06_01

**SUPPLEMENTAL_CONTROL_IF_ANY**: `[]`

**INTERPRETATION**: ABAP numeric expression is a negative against the mathematical oracle; 17 mismatches do not imply that check_syntax promises mathematical contract verification.
