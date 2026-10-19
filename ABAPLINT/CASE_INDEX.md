# Original frozen R4 cases

Exactly 42 original IDs. Source links lead to exact recovered files. Counts are a synthetic capability probe, not model accuracy. Static clean does not mean SAP correct. All cases require SAP evidence.

| Case | Track | Scenario | Profile | Static | Interpretation |
|---|---|---|---|---|---|
| [T01_01](cases/T01_01/README.md) | T01 | Available synthetic cross-class dependency | cloud | clean | EXPECTED_STATIC_ACCEPTANCE |
| [T01_02](cases/T01_02/README.md) | T01 | Missing custom class | cloud | findings | MISSING_DEPENDENCY |
| [T01_03](cases/T01_03/README.md) | T01 | Missing external class outside error namespace | cloud | clean | CONFIGURATION_GAP |
| [T01_04](cases/T01_04/README.md) | T01 | Missing data element | cloud | findings | MISSING_DEPENDENCY |
| [T01_05](cases/T01_05/README.md) | T01 | Missing DDIC structure/component | cloud | findings | MISSING_DEPENDENCY |
| [T01_06](cases/T01_06/README.md) | T01 | Missing transparent table | cloud | findings | MISSING_DEPENDENCY |
| [T01_07](cases/T01_07/README.md) | T01 | Missing interface reference | cloud | findings | MISSING_DEPENDENCY |
| [T02_01](cases/T02_01/README.md) | T02 | Classic transaction in Cloud profile | cloud | findings | EXPECTED_STATIC_RULE_FINDING |
| [T02_02](cases/T02_02/README.md) | T02 | Same transaction in classic v758 | v758 | clean | EXPECTED_STATIC_ACCEPTANCE |
| [T02_03](cases/T02_03/README.md) | T02 | Modern expression under old v702 | v702 | findings | EXPECTED_STATIC_RULE_FINDING |
| [T02_04](cases/T02_04/README.md) | T02 | Modern expression under v758 | v758 | clean | EXPECTED_STATIC_ACCEPTANCE |
| [T02_05](cases/T02_05/README.md) | T02 | API exists locally but release contract absent | cloud | clean | EXPECTED_STATIC_ACCEPTANCE |
| [T03_01](cases/T03_01/README.md) | T03 | CDS over local synthetic table | cloud | clean | UNSUPPORTED_SEMANTIC_CHECK |
| [T03_02](cases/T03_02/README.md) | T03 | CDS missing source | cloud | clean | MISSING_DEPENDENCY |
| [T03_03](cases/T03_03/README.md) | T03 | Malformed CDS definition | cloud | findings | UNSUPPORTED_SEMANTIC_CHECK |
| [T03_04](cases/T03_04/README.md) | T03 | CDS missing association target | cloud | clean | MISSING_DEPENDENCY |
| [T03_05](cases/T03_05/README.md) | T03 | Managed BDEF with missing implementation class | cloud | clean | UNSUPPORTED_SEMANTIC_CHECK |
| [T03_06](cases/T03_06/README.md) | T03 | Deliberately malformed BDEF | cloud | clean | UNSUPPORTED_SEMANTIC_CHECK |
| [T03_07](cases/T03_07/README.md) | T03 | EML entity read with absent behavior contract | cloud | findings | UNSUPPORTED_SEMANTIC_CHECK |
| [T03_08](cases/T03_08/README.md) | T03 | RAP commit without business object/save environment | cloud | clean | UNSUPPORTED_SEMANTIC_CHECK |
| [T04_01](cases/T04_01/README.md) | T04 | Authorization result checked | cloud | clean | UNSUPPORTED_SEMANTIC_CHECK |
| [T04_02](cases/T04_02/README.md) | T04 | Authorization result ignored | cloud | findings | UNSUPPORTED_SEMANTIC_CHECK |
| [T04_03](cases/T04_03/README.md) | T04 | Missing deny branch in synthetic policy | cloud | findings | EXPECTED_STATIC_RULE_FINDING |
| [T04_04](cases/T04_04/README.md) | T04 | Explicit synthetic policy guard | cloud | clean | EXPECTED_STATIC_ACCEPTANCE |
| [T04_05](cases/T04_05/README.md) | T04 | Implicit client handling over local client table | cloud | findings | OFFSTACK_ADAPTER_LIMITATION |
| [T04_06](cases/T04_06/README.md) | T04 | Explicit cross-client classic SQL | v758 | findings | EXPECTED_STATIC_RULE_FINDING |
| [T05_01](cases/T05_01/README.md) | T05 | COMMIT WORK with no configured database | v758 | clean | EXPECTED_STATIC_ACCEPTANCE |
| [T05_02](cases/T05_02/README.md) | T05 | ROLLBACK WORK with no configured database | v758 | clean | EXPECTED_STATIC_ACCEPTANCE |
| [T05_03](cases/T05_03/README.md) | T05 | Absent enqueue function | v758 | clean | MISSING_DEPENDENCY |
| [T05_04](cases/T05_04/README.md) | T05 | Absent update function | v758 | clean | MISSING_DEPENDENCY |
| [T05_05](cases/T05_05/README.md) | T05 | Local SQLite transaction rollback | v758 | findings | EXPECTED_STATIC_RULE_FINDING |
| [T05_06](cases/T05_06/README.md) | T05 | Local SQLite transaction commit | v758 | findings | EXPECTED_STATIC_RULE_FINDING |
| [T06_01](cases/T06_01/README.md) | T06 | R3 regression: integer intermediate before truncation | cloud | clean | EXPECTED_STATIC_ACCEPTANCE |
| [T06_02](cases/T06_02/README.md) | T06 | R3 regression: decimal before division | cloud | clean | EXPECTED_STATIC_ACCEPTANCE |
| [T06_03](cases/T06_03/README.md) | T06 | Packed decimal rounding boundary | cloud | findings | EXPECTED_STATIC_RULE_FINDING |
| [T06_04](cases/T06_04/README.md) | T06 | Decimal cancellation beyond binary integer exactness | cloud | findings | EXPECTED_STATIC_RULE_FINDING |
| [T06_05](cases/T06_05/README.md) | T06 | Open SQL filtering and aggregation | cloud | findings | EXPECTED_STATIC_RULE_FINDING |
| [T06_06](cases/T06_06/README.md) | T06 | Open SQL null predicate | cloud | clean | EXPECTED_STATIC_ACCEPTANCE |
| [T06_07](cases/T06_07/README.md) | T06 | Open SQL null to initial conversion | cloud | clean | OFFSTACK_ADAPTER_LIMITATION |
| [T06_08](cases/T06_08/README.md) | T06 | Open SQL null aggregate | cloud | findings | EXPECTED_STATIC_RULE_FINDING |
| [T06_09](cases/T06_09/README.md) | T06 | Empty SQL aggregate initial result | cloud | findings | EXPECTED_STATIC_RULE_FINDING |
| [T06_10](cases/T06_10/README.md) | T06 | Open SQL from internal table | cloud | findings | UNSUPPORTED_SEMANTIC_CHECK |

Summary: 42 qualified static analyses; 21 strict clean outcomes; eight historical acceptance blind spots; 15 main cases verified for selected local properties; 57/76 completed reference checks matched against 77 frozen expectations; T06_10 has no returned reference due database initialization; 13 unsupported configured-pipeline cases; 42/42 require SAP evidence. The [CDS supplement](supplements/cds-ddl-results.json) is separate (3/3) and is not included in the 42-case or reference totals. [Machine-readable mapping](results/case-manifest.json).


## Reconciled technical classifications

All required assessment fields are in each linked case clarification and the [machine-readable CSV](results/technical-revalidation-classification.csv). Earlier root-cause labels remain historical; these interpretations qualify them.

| Case | Scenario | Test category | Technical root cause | Controls |
|---|---|---|---|---|
| [T01_01](cases/T01_01/README.md#technical-revalidation-clarification) | Available synthetic cross-class dependency | Representative language pattern | VALID_REPRESENTATIVE_PATTERN | None |
| [T01_02](cases/T01_02/README.md#technical-revalidation-clarification) | Missing custom class | Intentional negative test | MISSING_DEPENDENCY_METADATA | None |
| [T01_03](cases/T01_03/README.md#technical-revalidation-clarification) | Missing external class outside error namespace | Intentional negative test | CONFIGURATION_LIMITATION | None |
| [T01_04](cases/T01_04/README.md#technical-revalidation-clarification) | Missing data element | Intentional negative test | MISSING_DEPENDENCY_METADATA | None |
| [T01_05](cases/T01_05/README.md#technical-revalidation-clarification) | Missing DDIC structure/component | Intentional negative test | MISSING_DEPENDENCY_METADATA | None |
| [T01_06](cases/T01_06/README.md#technical-revalidation-clarification) | Missing transparent table | Intentional negative test | MISSING_DEPENDENCY_METADATA | None |
| [T01_07](cases/T01_07/README.md#technical-revalidation-clarification) | Missing interface reference | Intentional negative test | MISSING_DEPENDENCY_METADATA | None |
| [T02_01](cases/T02_01/README.md#technical-revalidation-clarification) | Classic transaction in Cloud profile | Intentional negative test | VALID_NEGATIVE_TEST | None |
| [T02_02](cases/T02_02/README.md#technical-revalidation-clarification) | Same transaction in classic v758 | Representative language pattern | VALID_REPRESENTATIVE_PATTERN | None |
| [T02_03](cases/T02_03/README.md#technical-revalidation-clarification) | Modern expression under old v702 | Intentional negative test | VALID_NEGATIVE_TEST | None |
| [T02_04](cases/T02_04/README.md#technical-revalidation-clarification) | Modern expression under v758 | Representative language pattern | VALID_REPRESENTATIVE_PATTERN | None |
| [T02_05](cases/T02_05/README.md#technical-revalidation-clarification) | API exists locally but release contract absent | Representative language pattern | VALID_REPRESENTATIVE_PATTERN | None |
| [T03_01](cases/T03_01/README.md#technical-revalidation-clarification) | CDS over local synthetic table | Representative language pattern | VALID_REPRESENTATIVE_PATTERN | None |
| [T03_02](cases/T03_02/README.md#technical-revalidation-clarification) | CDS missing source | Intentional negative test | MISSING_DEPENDENCY_METADATA | None |
| [T03_03](cases/T03_03/README.md#technical-revalidation-clarification) | Malformed CDS definition | Intentional negative test | VALID_NEGATIVE_TEST | None |
| [T03_04](cases/T03_04/README.md#technical-revalidation-clarification) | CDS missing association target | Intentional negative test | MISSING_DEPENDENCY_METADATA | None |
| [T03_05](cases/T03_05/README.md#technical-revalidation-clarification) | Managed BDEF with missing implementation class | Requires additional qualification | MULTIPLE_DEFECTS_IN_FIXTURE | SR_T03_05_ROOT_ONLY |
| [T03_06](cases/T03_06/README.md#technical-revalidation-clarification) | Deliberately malformed BDEF | Intentional negative test | UNSUPPORTED_SEMANTIC_CHECK | None |
| [T03_07](cases/T03_07/README.md#technical-revalidation-clarification) | EML entity read with absent behavior contract | Requires additional qualification | UNSUPPORTED_SEMANTIC_CHECK | None |
| [T03_08](cases/T03_08/README.md#technical-revalidation-clarification) | RAP commit without business object/save environment | Representative language pattern | UNSUPPORTED_SEMANTIC_CHECK | None |
| [T04_01](cases/T04_01/README.md#technical-revalidation-clarification) | Authorization result checked | Representative language pattern | UNSUPPORTED_SEMANTIC_CHECK | None |
| [T04_02](cases/T04_02/README.md#technical-revalidation-clarification) | Authorization result ignored | Intentional negative test | VALID_NEGATIVE_TEST | None |
| [T04_03](cases/T04_03/README.md#technical-revalidation-clarification) | Missing deny branch in synthetic policy | Simulated semantic scenario | UNSUPPORTED_SEMANTIC_CHECK | None |
| [T04_04](cases/T04_04/README.md#technical-revalidation-clarification) | Explicit synthetic policy guard | Simulated semantic scenario | VALID_REPRESENTATIVE_PATTERN | None |
| [T04_05](cases/T04_05/README.md#technical-revalidation-clarification) | Implicit client handling over local client table | Simulated semantic scenario | OFFSTACK_ADAPTER_LIMITATION | None |
| [T04_06](cases/T04_06/README.md#technical-revalidation-clarification) | Explicit cross-client classic SQL | Requires additional qualification | UNRESOLVED_REQUIRES_SAP | SR_T04_06_SUBRC_ONLY, SR_T04_06_USING_CLIENT, SR_T04_06_NO_ESCAPE |
| [T05_01](cases/T05_01/README.md#technical-revalidation-clarification) | COMMIT WORK with no configured database | Simulated semantic scenario | UNSUPPORTED_SEMANTIC_CHECK | None |
| [T05_02](cases/T05_02/README.md#technical-revalidation-clarification) | ROLLBACK WORK with no configured database | Simulated semantic scenario | UNSUPPORTED_SEMANTIC_CHECK | None |
| [T05_03](cases/T05_03/README.md#technical-revalidation-clarification) | Absent enqueue function | Intentional negative test | MISSING_DEPENDENCY_METADATA | None |
| [T05_04](cases/T05_04/README.md#technical-revalidation-clarification) | Absent update function | Intentional negative test | MISSING_DEPENDENCY_METADATA | None |
| [T05_05](cases/T05_05/README.md#technical-revalidation-clarification) | Local SQLite transaction rollback | Simulated semantic scenario | OFFSTACK_ADAPTER_LIMITATION | None |
| [T05_06](cases/T05_06/README.md#technical-revalidation-clarification) | Local SQLite transaction commit | Simulated semantic scenario | OFFSTACK_ADAPTER_LIMITATION | None |
| [T06_01](cases/T06_01/README.md#technical-revalidation-clarification) | R3 regression: integer intermediate before truncation | Intentional negative test | VALID_NEGATIVE_TEST | None |
| [T06_02](cases/T06_02/README.md#technical-revalidation-clarification) | R3 regression: decimal before division | Representative language pattern | VALID_REPRESENTATIVE_PATTERN | None |
| [T06_03](cases/T06_03/README.md#technical-revalidation-clarification) | Packed decimal rounding boundary | Representative language pattern | VALID_REPRESENTATIVE_PATTERN | None |
| [T06_04](cases/T06_04/README.md#technical-revalidation-clarification) | Decimal cancellation beyond binary integer exactness | Representative language pattern | VALID_REPRESENTATIVE_PATTERN | None |
| [T06_05](cases/T06_05/README.md#technical-revalidation-clarification) | Open SQL filtering and aggregation | Simulated semantic scenario | OFFSTACK_ADAPTER_LIMITATION | None |
| [T06_06](cases/T06_06/README.md#technical-revalidation-clarification) | Open SQL null predicate | Simulated semantic scenario | OFFSTACK_ADAPTER_LIMITATION | SR_T06_06_ZERO_ROW, SR_T06_06_NOTNULL_SCHEMA |
| [T06_07](cases/T06_07/README.md#technical-revalidation-clarification) | Open SQL null to initial conversion | Simulated semantic scenario | OFFSTACK_ADAPTER_LIMITATION | SR_T06_07_ZERO_ROW |
| [T06_08](cases/T06_08/README.md#technical-revalidation-clarification) | Open SQL null aggregate | Simulated semantic scenario | OFFSTACK_ADAPTER_LIMITATION | SR_T06_08_ZERO_ROW |
| [T06_09](cases/T06_09/README.md#technical-revalidation-clarification) | Empty SQL aggregate initial result | Simulated semantic scenario | VALID_REPRESENTATIVE_PATTERN | None |
| [T06_10](cases/T06_10/README.md#technical-revalidation-clarification) | Open SQL from internal table | Requires additional qualification | OFFSTACK_ADAPTER_LIMITATION | None |
