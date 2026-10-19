# T03_06 — Deliberately malformed BDEF

CASE_ID=T03_06

TRACK=T03

ORIGINAL_REQUIREMENT: Deliberately malformed BDEF. The original frozen record defines expectedStatic=DEFECT; Deliberately malformed BDEF artifact; no valid grammar header.. The exact frozen input/output expectations are in [case.json](case.json). R4 did not supply an independently authored enterprise requirements document.

SOURCE_FILES: [zr4_bad.bdef.asbdef](src/zr4_bad.bdef.asbdef). Source types: BDEF. These files are exact original frozen bytes, not simplified/regenerated examples.

TARGET_LANGUAGE_VERSION=Cloud (historical LSP reports v816 + Cloud)

ABAPLINT_CONFIGURATION=[cloud.json](../../config/cloud.json); [approved hashes](../../config/approved.json). Original 22-rule policy is preserved; v758/v702 profiles are the original explicit R4 variants.

DEPENDENCIES: only the supplied source files, no configured dependency repositories (dependencies=[]). No target SAP catalog, DDIC activation, released API or SAP host environment is supplied.

EXPECTED_DIAGNOSTICS: original category **DEFECT**. Deliberately malformed BDEF artifact; no valid grammar header. The historical expectations do not specify an exact diagnostic message for every case; no exact-message oracle is invented. Behavioral reference arrays are separate.

ACTUAL_DIAGNOSTICS: [original extracted arrays](diagnostics.json); [sanitized full LSP trace](lsp-trace.sanitized.json).

### zr4_bad.bdef.asbdef

No diagnostics: original published array is empty.

STATIC_VERDICT=VALIDATION_PASS; historical acceptance classification=FALSE_NEGATIVE_OBSERVED.

OFFSTACK_EXECUTION_VERDICT=ARTIFACT_TRANSPILED_NO_BEHAVIOR; selected declared checks 0/0 returned matches, 0 expected. Classification=UNSUPPORTED. [Original output](offstack-original.sanitized.json). 

SAP_VERIFICATION_STATUS=SAP_EVIDENCE_REQUIRED; NOT_EXECUTED. Target release/compiler, real dependencies, activation and relevant SAP runtime tests.

ROOT_CAUSE_CLASSIFICATION=UNSUPPORTED_SEMANTIC_CHECK. Deliberately malformed BDEF received no findings. The enabled rules did not provide a qualified BDEF grammar/semantic validator.

RULE_SCOPE_AND_UNCERTAINTY: Pinned BDEF parsing extracts entity references; cds_parser_error covers DDLS/DDLX, not BDEF syntax. See [rule-scope notes](../../RULE_SCOPE.md). No confirmed upstream issue is asserted.

KNOWN_LIMITATIONS: SYNTHETIC_ENTERPRISE_PATTERN; same-investigator synthetic oracle, exact profile/configured dependencies only, limited off-stack host/database coverage. A lint finding or silence cannot establish SAP correctness. Related final-closure capability classifications are included in case.json without replacing the original R4 labels.

REPRODUCTION_STEPS: from ABAPLINT follow [environment setup](../../METHODOLOGY.md), then run `node harness/reproduce.cjs T03_06`. This executes the public portable LSP/runtime derivatives against these exact sources and compares with published historical outputs. Missing prerequisites and mismatches must be reported, not relabeled as passes. Reproduction validation status is recorded separately in [results/reproduction-validation.json](../../results/reproduction-validation.json). No SAP connection is used.

EVIDENCE_PROVENANCE: original logical record `R4/fixtures/cases/T03_06`; config `R4/config/cloud.json`; raw LSP `R4/logs/T03_06.json`; runtime `R4/runtime/T03_06/result.json`. Hash mapping: [publication provenance](../../results/provenance.json). Sources retain original SHA-256; traces/results are sanitized derivatives with separate public hashes. All original local records remain private and unchanged.

PUBLIC_REPRODUCTION_STATUS=REPRODUCED_WITH_EXTERNAL_PINNED_PREREQUISITES. The independently executed public runner matched this case's original static diagnostics and runtime outcome, including any recorded failure. External prerequisites remain required.


## Technical revalidation clarification

This clarification supersedes earlier interpretation where inconsistent; original evidence and scores are retained.

**CASE_ID**: T03_06

**SCENARIO**: Deliberately malformed BDEF

**SOURCE_TYPE**: BDEF

**TEST_CATEGORY**: Intentional negative test

**ABAP_GENUINENESS_ASSESSMENT**: Intentional negative synthetic ABAP/CDS/BDEF input; validity is not assumed. Intentionally malformed BDEF accepted by the observed policy; no BDEF semantic validation contract established for the configured tool.

**STATIC_RESULT**: VALIDATION_PASS

**OBSERVED_DIAGNOSTICS**: `{"zr4_bad.bdef.asbdef":[]}`

**EXPECTED_BEHAVIOR**: `{"frozenStatic":"DEFECT","frozenDefect":"Deliberately malformed BDEF artifact; no valid grammar header.","frozenReferences":[]}`

**ROOT_CAUSE_CLASSIFICATION**: UNSUPPORTED_SEMANTIC_CHECK

**OFFSTACK_RESULT**: `{"status":"UNSUPPORTED","returned":0,"matched":0,"frozenExpected":0,"record":"cases/T03_06/offstack-original.sanitized.json","selectedRecord":"cases/T03_06/offstack-original.sanitized.json"}`

**SAP_VALIDATION_REQUIRED**: YES: exact release, compiler/activation, dependency metadata and relevant business runtime. NOT_EXECUTED.

**REPRODUCTION_LINK**: node harness/reproduce.cjs T03_06

**SUPPLEMENTAL_CONTROL_IF_ANY**: `[]`

**INTERPRETATION**: Intentionally malformed BDEF accepted by the observed policy; no BDEF semantic validation contract established for the configured tool.
