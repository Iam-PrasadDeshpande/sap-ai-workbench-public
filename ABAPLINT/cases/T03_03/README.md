# T03_03 — Malformed CDS definition

CASE_ID=T03_03

TRACK=T03

ORIGINAL_REQUIREMENT: Malformed CDS definition. The original frozen record defines expectedStatic=DEFECT; Deliberately malformed CDS syntax. The exact frozen input/output expectations are in [case.json](case.json). R4 did not supply an independently authored enterprise requirements document.

SOURCE_FILES: [zr4_view.ddls.asddls](src/zr4_view.ddls.asddls). Source types: CDS. These files are exact original frozen bytes, not simplified/regenerated examples.

TARGET_LANGUAGE_VERSION=Cloud (historical LSP reports v816 + Cloud)

ABAPLINT_CONFIGURATION=[cloud.json](../../config/cloud.json); [approved hashes](../../config/approved.json). Original 22-rule policy is preserved; v758/v702 profiles are the original explicit R4 variants.

DEPENDENCIES: only the supplied source files, no configured dependency repositories (dependencies=[]). No target SAP catalog, DDIC activation, released API or SAP host environment is supplied.

EXPECTED_DIAGNOSTICS: original category **DEFECT**. Deliberately malformed CDS syntax The historical expectations do not specify an exact diagnostic message for every case; no exact-message oracle is invented. Behavioral reference arrays are separate.

ACTUAL_DIAGNOSTICS: [original extracted arrays](diagnostics.json); [sanitized full LSP trace](lsp-trace.sanitized.json).

### zr4_view.ddls.asddls

```json
[
  {
    "severity": 1,
    "range": {
      "start": {
        "line": 0,
        "character": 0
      },
      "end": {
        "line": 0,
        "character": 56
      }
    },
    "code": "cds_parser_error",
    "codeDescription": {
      "href": "https://rules.abaplint.org/cds_parser_error/"
    },
    "message": "CDS Parser error",
    "source": "abaplint"
  }
]
```

STATIC_VERDICT=VALIDATION_FAIL; historical acceptance classification=PARTIAL.

OFFSTACK_EXECUTION_VERDICT=LOCAL_TOOLCHAIN_ERROR; selected declared checks 0/0 returned matches, 0 expected. Classification=PARTIAL. [Original output](offstack-original.sanitized.json). 

SAP_VERIFICATION_STATUS=SAP_EVIDENCE_REQUIRED; NOT_EXECUTED. Target release/compiler, real dependencies, activation and relevant SAP runtime tests.

ROOT_CAUSE_CLASSIFICATION=UNSUPPORTED_SEMANTIC_CHECK. Only the recorded parser/artifact/runtime stage was exercised; enterprise semantics remain unsupported or unverified in this configured path.

RULE_SCOPE_AND_UNCERTAINTY: Do not promote artifact handling, style findings or failed invocation to semantic verification. See [rule-scope notes](../../RULE_SCOPE.md). No confirmed upstream issue is asserted.

KNOWN_LIMITATIONS: SYNTHETIC_ENTERPRISE_PATTERN; same-investigator synthetic oracle, exact profile/configured dependencies only, limited off-stack host/database coverage. A lint finding or silence cannot establish SAP correctness. Related final-closure capability classifications are included in case.json without replacing the original R4 labels.

REPRODUCTION_STEPS: from ABAPLINT follow [environment setup](../../METHODOLOGY.md), then run `node harness/reproduce.cjs T03_03`. This executes the public portable LSP/runtime derivatives against these exact sources and compares with published historical outputs. Missing prerequisites and mismatches must be reported, not relabeled as passes. Reproduction validation status is recorded separately in [results/reproduction-validation.json](../../results/reproduction-validation.json). No SAP connection is used.

EVIDENCE_PROVENANCE: original logical record `R4/fixtures/cases/T03_03`; config `R4/config/cloud.json`; raw LSP `R4/logs/T03_03.json`; runtime `R4/runtime/T03_03/result.json`. Hash mapping: [publication provenance](../../results/provenance.json). Sources retain original SHA-256; traces/results are sanitized derivatives with separate public hashes. All original local records remain private and unchanged.

PUBLIC_REPRODUCTION_STATUS=REPRODUCED_WITH_EXTERNAL_PINNED_PREREQUISITES. The independently executed public runner matched this case's original static diagnostics and runtime outcome, including any recorded failure. External prerequisites remain required.


## Technical revalidation clarification

This clarification supersedes earlier interpretation where inconsistent; original evidence and scores are retained.

**CASE_ID**: T03_03

**SCENARIO**: Malformed CDS definition

**SOURCE_TYPE**: CDS

**TEST_CATEGORY**: Intentional negative test

**ABAP_GENUINENESS_ASSESSMENT**: Intentional negative synthetic ABAP/CDS/BDEF input; validity is not assumed. Intentional malformed CDS negative; retain exact parser diagnostics rather than treat as a representative valid model.

**STATIC_RESULT**: VALIDATION_FAIL

**OBSERVED_DIAGNOSTICS**: `{"zr4_view.ddls.asddls":[{"severity":1,"range":{"start":{"line":0,"character":0},"end":{"line":0,"character":56}},"code":"cds_parser_error","codeDescription":{"href":"https://rules.abaplint.org/cds_parser_error/"},"message":"CDS Parser error","source":"abaplint"}]}`

**EXPECTED_BEHAVIOR**: `{"frozenStatic":"DEFECT","frozenDefect":"Deliberately malformed CDS syntax","frozenReferences":[]}`

**ROOT_CAUSE_CLASSIFICATION**: VALID_NEGATIVE_TEST

**OFFSTACK_RESULT**: `{"status":"PARTIAL","returned":0,"matched":0,"frozenExpected":0,"record":"cases/T03_03/offstack-original.sanitized.json","selectedRecord":"cases/T03_03/offstack-original.sanitized.json"}`

**SAP_VALIDATION_REQUIRED**: YES: exact release, compiler/activation, dependency metadata and relevant business runtime. NOT_EXECUTED.

**REPRODUCTION_LINK**: node harness/reproduce.cjs T03_03

**SUPPLEMENTAL_CONTROL_IF_ANY**: `[]`

**INTERPRETATION**: Intentional malformed CDS negative; retain exact parser diagnostics rather than treat as a representative valid model.
