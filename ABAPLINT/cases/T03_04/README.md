# T03_04 — CDS missing association target

CASE_ID=T03_04

TRACK=T03

ORIGINAL_REQUIREMENT: CDS missing association target. The original frozen record defines expectedStatic=DEFECT; Missing association target from frozen inventory. The exact frozen input/output expectations are in [case.json](case.json). R4 did not supply an independently authored enterprise requirements document.

SOURCE_FILES: [zr4_view.ddls.asddls](src/zr4_view.ddls.asddls), [zr4_data.tabl.xml](src/zr4_data.tabl.xml). Source types: CDS, DDIC_XML. These files are exact original frozen bytes, not simplified/regenerated examples.

TARGET_LANGUAGE_VERSION=Cloud (historical LSP reports v816 + Cloud)

ABAPLINT_CONFIGURATION=[cloud.json](../../config/cloud.json); [approved hashes](../../config/approved.json). Original 22-rule policy is preserved; v758/v702 profiles are the original explicit R4 variants.

DEPENDENCIES: only the supplied source files, no configured dependency repositories (dependencies=[]). No target SAP catalog, DDIC activation, released API or SAP host environment is supplied.

EXPECTED_DIAGNOSTICS: original category **DEFECT**. Missing association target from frozen inventory The historical expectations do not specify an exact diagnostic message for every case; no exact-message oracle is invented. Behavioral reference arrays are separate.

ACTUAL_DIAGNOSTICS: [original extracted arrays](diagnostics.json); [sanitized full LSP trace](lsp-trace.sanitized.json).

### zr4_view.ddls.asddls

No diagnostics: original published array is empty.

STATIC_VERDICT=VALIDATION_PASS; historical acceptance classification=FALSE_NEGATIVE_OBSERVED.

OFFSTACK_EXECUTION_VERDICT=LOCAL_TOOLCHAIN_ERROR; selected declared checks 0/0 returned matches, 0 expected. Classification=UNSUPPORTED. [Original output](offstack-original.sanitized.json). 

SAP_VERIFICATION_STATUS=SAP_EVIDENCE_REQUIRED; NOT_EXECUTED. Target release/compiler, real dependencies, activation and relevant SAP runtime tests.

ROOT_CAUSE_CLASSIFICATION=MISSING_DEPENDENCY; UNSUPPORTED_SEMANTIC_CHECK. Association target is absent. The transpiler reported an unsupported association definition; this is not independently established as an enabled-rule defect.

RULE_SCOPE_AND_UNCERTAINTY: CDS parser coverage does not promise full association/target resolution. See [rule-scope notes](../../RULE_SCOPE.md). No confirmed upstream issue is asserted.

KNOWN_LIMITATIONS: SYNTHETIC_ENTERPRISE_PATTERN; same-investigator synthetic oracle, exact profile/configured dependencies only, limited off-stack host/database coverage. A lint finding or silence cannot establish SAP correctness. Related final-closure capability classifications are included in case.json without replacing the original R4 labels.

REPRODUCTION_STEPS: from ABAPLINT follow [environment setup](../../METHODOLOGY.md), then run `node harness/reproduce.cjs T03_04`. This executes the public portable LSP/runtime derivatives against these exact sources and compares with published historical outputs. Missing prerequisites and mismatches must be reported, not relabeled as passes. Reproduction validation status is recorded separately in [results/reproduction-validation.json](../../results/reproduction-validation.json). No SAP connection is used.

EVIDENCE_PROVENANCE: original logical record `R4/fixtures/cases/T03_04`; config `R4/config/cloud.json`; raw LSP `R4/logs/T03_04.json`; runtime `R4/runtime/T03_04/result.json`. Hash mapping: [publication provenance](../../results/provenance.json). Sources retain original SHA-256; traces/results are sanitized derivatives with separate public hashes. All original local records remain private and unchanged.

PUBLIC_REPRODUCTION_STATUS=REPRODUCED_WITH_EXTERNAL_PINNED_PREREQUISITES. The independently executed public runner matched this case's original static diagnostics and runtime outcome, including any recorded failure. External prerequisites remain required.


## Technical revalidation clarification

This clarification supersedes earlier interpretation where inconsistent; original evidence and scores are retained.

**CASE_ID**: T03_04

**SCENARIO**: CDS missing association target

**SOURCE_TYPE**: CDS; DDIC_XML

**TEST_CATEGORY**: Intentional negative test

**ABAP_GENUINENESS_ASSESSMENT**: Intentional negative synthetic ABAP/CDS/BDEF input; validity is not assumed. Intentional missing CDS dependency. Processing does not establish dependency resolution or target SAP activation; no demonstrated upstream contract violation.

**STATIC_RESULT**: VALIDATION_PASS

**OBSERVED_DIAGNOSTICS**: `{"zr4_view.ddls.asddls":[]}`

**EXPECTED_BEHAVIOR**: `{"frozenStatic":"DEFECT","frozenDefect":"Missing association target from frozen inventory","frozenReferences":[]}`

**ROOT_CAUSE_CLASSIFICATION**: MISSING_DEPENDENCY_METADATA

**OFFSTACK_RESULT**: `{"status":"UNSUPPORTED","returned":0,"matched":0,"frozenExpected":0,"record":"cases/T03_04/offstack-original.sanitized.json","selectedRecord":"cases/T03_04/offstack-original.sanitized.json"}`

**SAP_VALIDATION_REQUIRED**: YES: exact release, compiler/activation, dependency metadata and relevant business runtime. NOT_EXECUTED.

**REPRODUCTION_LINK**: node harness/reproduce.cjs T03_04

**SUPPLEMENTAL_CONTROL_IF_ANY**: `[]`

**INTERPRETATION**: Intentional missing CDS dependency. Processing does not establish dependency resolution or target SAP activation; no demonstrated upstream contract violation.
