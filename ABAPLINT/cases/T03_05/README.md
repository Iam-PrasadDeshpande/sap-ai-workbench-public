# T03_05 — Managed BDEF with missing implementation class

CASE_ID=T03_05

TRACK=T03

ORIGINAL_REQUIREMENT: Managed BDEF with missing implementation class. The original frozen record defines expectedStatic=DEFECT; Referenced managed implementation class absent from frozen inventory.. The exact frozen input/output expectations are in [case.json](case.json). R4 did not supply an independently authored enterprise requirements document.

SOURCE_FILES: [zr4_view.bdef.asbdef](src/zr4_view.bdef.asbdef), [zr4_view.ddls.asddls](src/zr4_view.ddls.asddls), [zr4_data.tabl.xml](src/zr4_data.tabl.xml). Source types: BDEF, CDS, DDIC_XML. These files are exact original frozen bytes, not simplified/regenerated examples.

TARGET_LANGUAGE_VERSION=Cloud (historical LSP reports v816 + Cloud)

ABAPLINT_CONFIGURATION=[cloud.json](../../config/cloud.json); [approved hashes](../../config/approved.json). Original 22-rule policy is preserved; v758/v702 profiles are the original explicit R4 variants.

DEPENDENCIES: only the supplied source files, no configured dependency repositories (dependencies=[]). No target SAP catalog, DDIC activation, released API or SAP host environment is supplied.

EXPECTED_DIAGNOSTICS: original category **DEFECT**. Referenced managed implementation class absent from frozen inventory. The historical expectations do not specify an exact diagnostic message for every case; no exact-message oracle is invented. Behavioral reference arrays are separate.

ACTUAL_DIAGNOSTICS: [original extracted arrays](diagnostics.json); [sanitized full LSP trace](lsp-trace.sanitized.json).

### zr4_view.bdef.asbdef

No diagnostics: original published array is empty.

### zr4_view.ddls.asddls

No diagnostics: original published array is empty.

STATIC_VERDICT=VALIDATION_PASS; historical acceptance classification=FALSE_NEGATIVE_OBSERVED.

OFFSTACK_EXECUTION_VERDICT=ARTIFACT_TRANSPILED_NO_BEHAVIOR; selected declared checks 0/0 returned matches, 0 expected. Classification=UNSUPPORTED. [Original output](offstack-original.sanitized.json). 

SAP_VERIFICATION_STATUS=SAP_EVIDENCE_REQUIRED; NOT_EXECUTED. Target release/compiler, real dependencies, activation and relevant SAP runtime tests.

ROOT_CAUSE_CLASSIFICATION=UNSUPPORTED_SEMANTIC_CHECK; MISSING_DEPENDENCY. The referenced behavior implementation is absent. Artifact processing did not execute RAP behavior or prove BDEF semantics.

RULE_SCOPE_AND_UNCERTAINTY: cds_parser_error does not check BDEF, and check_syntax is limited to ABAPObject. No complete BDEF semantic rule was qualified. See [rule-scope notes](../../RULE_SCOPE.md). No confirmed upstream issue is asserted.

KNOWN_LIMITATIONS: SYNTHETIC_ENTERPRISE_PATTERN; same-investigator synthetic oracle, exact profile/configured dependencies only, limited off-stack host/database coverage. A lint finding or silence cannot establish SAP correctness. Related final-closure capability classifications are included in case.json without replacing the original R4 labels.

REPRODUCTION_STEPS: from ABAPLINT follow [environment setup](../../METHODOLOGY.md), then run `node harness/reproduce.cjs T03_05`. This executes the public portable LSP/runtime derivatives against these exact sources and compares with published historical outputs. Missing prerequisites and mismatches must be reported, not relabeled as passes. Reproduction validation status is recorded separately in [results/reproduction-validation.json](../../results/reproduction-validation.json). No SAP connection is used.

EVIDENCE_PROVENANCE: original logical record `R4/fixtures/cases/T03_05`; config `R4/config/cloud.json`; raw LSP `R4/logs/T03_05.json`; runtime `R4/runtime/T03_05/result.json`. Hash mapping: [publication provenance](../../results/provenance.json). Sources retain original SHA-256; traces/results are sanitized derivatives with separate public hashes. All original local records remain private and unchanged.

PUBLIC_REPRODUCTION_STATUS=REPRODUCED_WITH_EXTERNAL_PINNED_PREREQUISITES. The independently executed public runner matched this case's original static diagnostics and runtime outcome, including any recorded failure. External prerequisites remain required.


## Technical revalidation clarification

This clarification supersedes earlier interpretation where inconsistent; original evidence and scores are retained.

**CASE_ID**: T03_05

**SCENARIO**: Managed BDEF with missing implementation class

**SOURCE_TYPE**: BDEF; CDS; DDIC_XML

**TEST_CATEGORY**: Requires additional qualification

**ABAP_GENUINENESS_ASSESSMENT**: Synthetic language/model fixture, not an extracted or SAP-activated enterprise object. Missing implementation class is not the sole issue: associated CDS lacks root. Strict managed authorization and key creation also require target modeling review. No SAP compiler execution.

**STATIC_RESULT**: VALIDATION_PASS

**OBSERVED_DIAGNOSTICS**: `{"zr4_view.bdef.asbdef":[],"zr4_view.ddls.asddls":[]}`

**EXPECTED_BEHAVIOR**: `{"frozenStatic":"DEFECT","frozenDefect":"Referenced managed implementation class absent from frozen inventory.","frozenReferences":[]}`

**ROOT_CAUSE_CLASSIFICATION**: MULTIPLE_DEFECTS_IN_FIXTURE

**OFFSTACK_RESULT**: `{"status":"UNSUPPORTED","returned":0,"matched":0,"frozenExpected":0,"record":"cases/T03_05/offstack-original.sanitized.json","selectedRecord":"cases/T03_05/offstack-original.sanitized.json"}`

**SAP_VALIDATION_REQUIRED**: YES: exact release, compiler/activation, dependency metadata and relevant business runtime. NOT_EXECUTED.

**REPRODUCTION_LINK**: node harness/reproduce.cjs T03_05

**SUPPLEMENTAL_CONTROL_IF_ANY**: `["SR_T03_05_ROOT_ONLY"]`

**INTERPRETATION**: Missing implementation class is not the sole issue: associated CDS lacks root. Strict managed authorization and key creation also require target modeling review. No SAP compiler execution.
