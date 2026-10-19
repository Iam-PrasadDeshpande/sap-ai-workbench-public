# T04_06 — Explicit cross-client classic SQL

CASE_ID=T04_06

TRACK=T04

ORIGINAL_REQUIREMENT: Explicit cross-client classic SQL. The original frozen record defines expectedStatic=OBSERVE; no additional defect assertion. The exact frozen input/output expectations are in [case.json](case.json). R4 did not supply an independently authored enterprise requirements document.

SOURCE_FILES: [zcl_r4_case.clas.abap](src/zcl_r4_case.clas.abap), [zr4_data.tabl.xml](src/zr4_data.tabl.xml). Source types: ABAP, DDIC_XML. These files are exact original frozen bytes, not simplified/regenerated examples.

TARGET_LANGUAGE_VERSION=v758

ABAPLINT_CONFIGURATION=[v758.json](../../config/v758.json); [approved hashes](../../config/approved.json). Original 22-rule policy is preserved; v758/v702 profiles are the original explicit R4 variants.

DEPENDENCIES: only the supplied source files, no configured dependency repositories (dependencies=[]). The historical behavior path uses a custom minimal SQLite adapter and synthetic rows in case.json. No target SAP catalog, DDIC activation, released API or SAP host environment is supplied.

EXPECTED_DIAGNOSTICS: original category **OBSERVE**. This is an observation/positive-control fixture, not an assertion of full enterprise correctness. The historical expectations do not specify an exact diagnostic message for every case; no exact-message oracle is invented. Behavioral reference arrays are separate.

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
        "character": 65
      }
    },
    "code": "check_subrc",
    "codeDescription": {
      "href": "https://rules.abaplint.org/check_subrc/"
    },
    "message": "Check sy-subrc",
    "source": "abaplint"
  }
]
```

STATIC_VERDICT=VALIDATION_FAIL; historical acceptance classification=PARTIAL.

OFFSTACK_EXECUTION_VERDICT=LOCAL_VERIFIED; selected declared checks 1/1 returned matches, 1 expected. Classification=LOCAL_VERIFIED. [Original output](offstack-original.sanitized.json). 

SAP_VERIFICATION_STATUS=SAP_EVIDENCE_REQUIRED; NOT_EXECUTED. Explicit privileged cross-client access requires target policy and negative tests; aggregate local behavior is not a security approval.

ROOT_CAUSE_CLASSIFICATION=EXPECTED_STATIC_RULE_FINDING. No contradiction of a supported static rule contract is established by this case. Retain all policy findings and behavioral outcomes separately.

RULE_SCOPE_AND_UNCERTAINTY: Observed exact rule policy; no SAP correctness inference. See [rule-scope notes](../../RULE_SCOPE.md). No confirmed upstream issue is asserted.

KNOWN_LIMITATIONS: SYNTHETIC_ENTERPRISE_PATTERN; same-investigator synthetic oracle, exact profile/configured dependencies only, limited off-stack host/database coverage. A lint finding or silence cannot establish SAP correctness. Related final-closure capability classifications are included in case.json without replacing the original R4 labels.

REPRODUCTION_STEPS: from ABAPLINT follow [environment setup](../../METHODOLOGY.md), then run `node harness/reproduce.cjs T04_06`. This executes the public portable LSP/runtime derivatives against these exact sources and compares with published historical outputs. Missing prerequisites and mismatches must be reported, not relabeled as passes. Reproduction validation status is recorded separately in [results/reproduction-validation.json](../../results/reproduction-validation.json). No SAP connection is used.

EVIDENCE_PROVENANCE: original logical record `R4/fixtures/cases/T04_06`; config `R4/config/v758.json`; raw LSP `R4/logs/T04_06.json`; runtime `R4/runtime/T04_06/result.json`. Hash mapping: [publication provenance](../../results/provenance.json). Sources retain original SHA-256; traces/results are sanitized derivatives with separate public hashes. All original local records remain private and unchanged.

PUBLIC_REPRODUCTION_STATUS=REPRODUCED_WITH_EXTERNAL_PINNED_PREREQUISITES. The independently executed public runner matched this case's original static diagnostics and runtime outcome, including any recorded failure. External prerequisites remain required.


## Technical revalidation clarification

This clarification supersedes earlier interpretation where inconsistent; original evidence and scores are retained.

**CASE_ID**: T04_06

**SCENARIO**: Explicit cross-client classic SQL

**SOURCE_TYPE**: ABAP; DDIC_XML

**TEST_CATEGORY**: Requires additional qualification

**ABAP_GENUINENESS_ASSESSMENT**: Synthetic language/model fixture, not an extracted or SAP-activated enterprise object. Classic v758 CLIENT SPECIFIED with @rv: only check_subrc observed. Exact release-specific SELECT/strict-mode legality remains unresolved. Obsolete syntax is not by itself proof this fixture fails the SAP compiler.

**STATIC_RESULT**: VALIDATION_FAIL

**OBSERVED_DIAGNOSTICS**: `{"zcl_r4_case.clas.abap":[{"severity":1,"range":{"start":{"line":7,"character":4},"end":{"line":7,"character":65}},"code":"check_subrc","codeDescription":{"href":"https://rules.abaplint.org/check_subrc/"},"message":"Check sy-subrc","source":"abaplint"}]}`

**EXPECTED_BEHAVIOR**: `{"frozenStatic":"OBSERVE","frozenDefect":null,"frozenReferences":[{"input":{},"expected":104}]}`

**ROOT_CAUSE_CLASSIFICATION**: UNRESOLVED_REQUIRES_SAP

**OFFSTACK_RESULT**: `{"status":"LOCAL_VERIFIED","returned":1,"matched":1,"frozenExpected":1,"record":"cases/T04_06/offstack-original.sanitized.json","selectedRecord":"cases/T04_06/offstack-original.sanitized.json"}`

**SAP_VALIDATION_REQUIRED**: YES: exact release, compiler/activation, dependency metadata and relevant business runtime. NOT_EXECUTED.

**REPRODUCTION_LINK**: node harness/reproduce.cjs T04_06

**SUPPLEMENTAL_CONTROL_IF_ANY**: `["SR_T04_06_SUBRC_ONLY","SR_T04_06_USING_CLIENT","SR_T04_06_NO_ESCAPE"]`

**INTERPRETATION**: Classic v758 CLIENT SPECIFIED with @rv: only check_subrc observed. Exact release-specific SELECT/strict-mode legality remains unresolved. Obsolete syntax is not by itself proof this fixture fails the SAP compiler.
