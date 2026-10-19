# T03_02 — CDS missing source

CASE_ID=T03_02

TRACK=T03

ORIGINAL_REQUIREMENT: CDS missing source. The original frozen record defines expectedStatic=DEFECT; Missing CDS source from frozen inventory. The exact frozen input/output expectations are in [case.json](case.json). R4 did not supply an independently authored enterprise requirements document.

SOURCE_FILES: [zr4_view.ddls.asddls](src/zr4_view.ddls.asddls). Source types: CDS. These files are exact original frozen bytes, not simplified/regenerated examples.

TARGET_LANGUAGE_VERSION=Cloud (historical LSP reports v816 + Cloud)

ABAPLINT_CONFIGURATION=[cloud.json](../../config/cloud.json); [approved hashes](../../config/approved.json). Original 22-rule policy is preserved; v758/v702 profiles are the original explicit R4 variants.

DEPENDENCIES: only the supplied source files, no configured dependency repositories (dependencies=[]). No target SAP catalog, DDIC activation, released API or SAP host environment is supplied.

EXPECTED_DIAGNOSTICS: original category **DEFECT**. Missing CDS source from frozen inventory The historical expectations do not specify an exact diagnostic message for every case; no exact-message oracle is invented. Behavioral reference arrays are separate.

ACTUAL_DIAGNOSTICS: [original extracted arrays](diagnostics.json); [sanitized full LSP trace](lsp-trace.sanitized.json).

### zr4_view.ddls.asddls

No diagnostics: original published array is empty.

STATIC_VERDICT=VALIDATION_PASS; historical acceptance classification=FALSE_NEGATIVE_OBSERVED.

OFFSTACK_EXECUTION_VERDICT=LOCAL_TOOLCHAIN_ERROR; selected declared checks 0/0 returned matches, 0 expected. Classification=PARTIAL. [Original output](offstack-original.sanitized.json). 

SAP_VERIFICATION_STATUS=SAP_EVIDENCE_REQUIRED; NOT_EXECUTED. Target release/compiler, real dependencies, activation and relevant SAP runtime tests.

ROOT_CAUSE_CLASSIFICATION=MISSING_DEPENDENCY; UNSUPPORTED_SEMANTIC_CHECK. The CDS source is absent. cds_parser_error detects parsing, not a complete CDS dependency contract. The selected LSP emitted no source-resolution finding.

RULE_SCOPE_AND_UNCERTAINTY: Pinned cds_parser_error.run handles DDLS/DDLX parse errors. check_syntax.run applies to ABAPObject, not a full CDS semantic verifier. See [rule-scope notes](../../RULE_SCOPE.md). No confirmed upstream issue is asserted.

KNOWN_LIMITATIONS: SYNTHETIC_ENTERPRISE_PATTERN; same-investigator synthetic oracle, exact profile/configured dependencies only, limited off-stack host/database coverage. A lint finding or silence cannot establish SAP correctness. Related final-closure capability classifications are included in case.json without replacing the original R4 labels.

REPRODUCTION_STEPS: from ABAPLINT follow [environment setup](../../METHODOLOGY.md), then run `node harness/reproduce.cjs T03_02`. This executes the public portable LSP/runtime derivatives against these exact sources and compares with published historical outputs. Missing prerequisites and mismatches must be reported, not relabeled as passes. Reproduction validation status is recorded separately in [results/reproduction-validation.json](../../results/reproduction-validation.json). No SAP connection is used.

EVIDENCE_PROVENANCE: original logical record `R4/fixtures/cases/T03_02`; config `R4/config/cloud.json`; raw LSP `R4/logs/T03_02.json`; runtime `R4/runtime/T03_02/result.json`. Hash mapping: [publication provenance](../../results/provenance.json). Sources retain original SHA-256; traces/results are sanitized derivatives with separate public hashes. All original local records remain private and unchanged.

PUBLIC_REPRODUCTION_STATUS=REPRODUCED_WITH_EXTERNAL_PINNED_PREREQUISITES. The independently executed public runner matched this case's original static diagnostics and runtime outcome, including any recorded failure. External prerequisites remain required.


## Technical revalidation clarification

This clarification supersedes earlier interpretation where inconsistent; original evidence and scores are retained.

**CASE_ID**: T03_02

**SCENARIO**: CDS missing source

**SOURCE_TYPE**: CDS

**TEST_CATEGORY**: Intentional negative test

**ABAP_GENUINENESS_ASSESSMENT**: Intentional negative synthetic ABAP/CDS/BDEF input; validity is not assumed. Intentional missing CDS dependency. Processing does not establish dependency resolution or target SAP activation; no demonstrated upstream contract violation.

**STATIC_RESULT**: VALIDATION_PASS

**OBSERVED_DIAGNOSTICS**: `{"zr4_view.ddls.asddls":[]}`

**EXPECTED_BEHAVIOR**: `{"frozenStatic":"DEFECT","frozenDefect":"Missing CDS source from frozen inventory","frozenReferences":[]}`

**ROOT_CAUSE_CLASSIFICATION**: MISSING_DEPENDENCY_METADATA

**OFFSTACK_RESULT**: `{"status":"PARTIAL","returned":0,"matched":0,"frozenExpected":0,"record":"cases/T03_02/offstack-original.sanitized.json","selectedRecord":"cases/T03_02/offstack-original.sanitized.json"}`

**SAP_VALIDATION_REQUIRED**: YES: exact release, compiler/activation, dependency metadata and relevant business runtime. NOT_EXECUTED.

**REPRODUCTION_LINK**: node harness/reproduce.cjs T03_02

**SUPPLEMENTAL_CONTROL_IF_ANY**: `[]`

**INTERPRETATION**: Intentional missing CDS dependency. Processing does not establish dependency resolution or target SAP activation; no demonstrated upstream contract violation.
