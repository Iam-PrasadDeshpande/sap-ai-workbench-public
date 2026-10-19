# T02_03 — Modern expression under old v702

CASE_ID=T02_03

TRACK=T02

ORIGINAL_REQUIREMENT: Modern expression under old v702. The original frozen record defines expectedStatic=RESTRICTION; no additional defect assertion. The exact frozen input/output expectations are in [case.json](case.json). R4 did not supply an independently authored enterprise requirements document.

SOURCE_FILES: [zcl_r4_case.clas.abap](src/zcl_r4_case.clas.abap). Source types: ABAP. These files are exact original frozen bytes, not simplified/regenerated examples.

TARGET_LANGUAGE_VERSION=v702

ABAPLINT_CONFIGURATION=[v702.json](../../config/v702.json); [approved hashes](../../config/approved.json). Original 22-rule policy is preserved; v758/v702 profiles are the original explicit R4 variants.

DEPENDENCIES: only the supplied source files, no configured dependency repositories (dependencies=[]). No target SAP catalog, DDIC activation, released API or SAP host environment is supplied.

EXPECTED_DIAGNOSTICS: original category **RESTRICTION**. This is an observation/positive-control fixture, not an assertion of full enterprise correctness. The historical expectations do not specify an exact diagnostic message for every case; no exact-message oracle is invented. Behavioral reference arrays are separate.

ACTUAL_DIAGNOSTICS: [original extracted arrays](diagnostics.json); [sanitized full LSP trace](lsp-trace.sanitized.json).

### zcl_r4_case.clas.abap

```json
[
  {
    "severity": 1,
    "range": {
      "start": {
        "line": 7,
        "character": 4
      },
      "end": {
        "line": 7,
        "character": 21
      }
    },
    "code": "parser_error",
    "codeDescription": {
      "href": "https://rules.abaplint.org/parser_error/"
    },
    "message": "Statement does not exist in the configured ABAP version(or a parser error), \"rv\"",
    "source": "abaplint"
  }
]
```

STATIC_VERDICT=VALIDATION_FAIL; historical acceptance classification=PARTIAL.

OFFSTACK_EXECUTION_VERDICT=SMOKE_COMPLETED_NO_ORACLE; selected declared checks 0/0 returned matches, 0 expected. Classification=PARTIAL. [Original output](offstack-original.sanitized.json). 

SAP_VERIFICATION_STATUS=SAP_EVIDENCE_REQUIRED; NOT_EXECUTED. Target release/compiler, real dependencies, activation and relevant SAP runtime tests.

ROOT_CAUSE_CLASSIFICATION=EXPECTED_STATIC_RULE_FINDING. No contradiction of a supported static rule contract is established by this case. Retain all policy findings and behavioral outcomes separately.

RULE_SCOPE_AND_UNCERTAINTY: Observed exact rule policy; no SAP correctness inference. See [rule-scope notes](../../RULE_SCOPE.md). No confirmed upstream issue is asserted.

KNOWN_LIMITATIONS: SYNTHETIC_ENTERPRISE_PATTERN; same-investigator synthetic oracle, exact profile/configured dependencies only, limited off-stack host/database coverage. A lint finding or silence cannot establish SAP correctness. Related final-closure capability classifications are included in case.json without replacing the original R4 labels.

REPRODUCTION_STEPS: from ABAPLINT follow [environment setup](../../METHODOLOGY.md), then run `node harness/reproduce.cjs T02_03`. This executes the public portable LSP/runtime derivatives against these exact sources and compares with published historical outputs. Missing prerequisites and mismatches must be reported, not relabeled as passes. Reproduction validation status is recorded separately in [results/reproduction-validation.json](../../results/reproduction-validation.json). No SAP connection is used.

EVIDENCE_PROVENANCE: original logical record `R4/fixtures/cases/T02_03`; config `R4/config/v702.json`; raw LSP `R4/logs/T02_03.json`; runtime `R4/runtime/T02_03/result.json`. Hash mapping: [publication provenance](../../results/provenance.json). Sources retain original SHA-256; traces/results are sanitized derivatives with separate public hashes. All original local records remain private and unchanged.

PUBLIC_REPRODUCTION_STATUS=REPRODUCED_WITH_EXTERNAL_PINNED_PREREQUISITES. The independently executed public runner matched this case's original static diagnostics and runtime outcome, including any recorded failure. External prerequisites remain required.


## Technical revalidation clarification

This clarification supersedes earlier interpretation where inconsistent; original evidence and scores are retained.

**CASE_ID**: T02_03

**SCENARIO**: Modern expression under old v702

**SOURCE_TYPE**: ABAP

**TEST_CATEGORY**: Intentional negative test

**ABAP_GENUINENESS_ASSESSMENT**: Intentional negative synthetic ABAP/CDS/BDEF input; validity is not assumed. Modern expression tested against the older v702 profile; preserve the observed version-related finding.

**STATIC_RESULT**: VALIDATION_FAIL

**OBSERVED_DIAGNOSTICS**: `{"zcl_r4_case.clas.abap":[{"severity":1,"range":{"start":{"line":7,"character":4},"end":{"line":7,"character":21}},"code":"parser_error","codeDescription":{"href":"https://rules.abaplint.org/parser_error/"},"message":"Statement does not exist in the configured ABAP version(or a parser error), \"rv\"","source":"abaplint"}]}`

**EXPECTED_BEHAVIOR**: `{"frozenStatic":"RESTRICTION","frozenDefect":null,"frozenReferences":[]}`

**ROOT_CAUSE_CLASSIFICATION**: VALID_NEGATIVE_TEST

**OFFSTACK_RESULT**: `{"status":"PARTIAL","returned":0,"matched":0,"frozenExpected":0,"record":"cases/T02_03/offstack-original.sanitized.json","selectedRecord":"cases/T02_03/offstack-original.sanitized.json"}`

**SAP_VALIDATION_REQUIRED**: YES: exact release, compiler/activation, dependency metadata and relevant business runtime. NOT_EXECUTED.

**REPRODUCTION_LINK**: node harness/reproduce.cjs T02_03

**SUPPLEMENTAL_CONTROL_IF_ANY**: `[]`

**INTERPRETATION**: Modern expression tested against the older v702 profile; preserve the observed version-related finding.
