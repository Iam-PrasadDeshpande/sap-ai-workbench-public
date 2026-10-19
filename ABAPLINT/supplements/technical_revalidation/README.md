# Supplemental control index

Eight separately frozen controls; excluded from all original 42-case counts and scores. Inputs frozen before execution. Each changes one declared source or adapter dimension from the stated base; CLIENT variants use the explicitly subrc-handled base. No control establishes SAP validity.

Preparation initially had a JavaScript syntax error and an ensuing missing catalog before successful freezing; the failed preparation script is retained privately. These are preparation errors, not R4 results.

## SR_T03_05_ROOT_ONLY

**id**: SR_T03_05_ROOT_ONLY

**originCase**: T03_05

**change**: Add root to the CDS declaration only; retain original BDEF/missing implementation/authorization/key choices.

**profile**: cloud

**expected**: Observe whether the local gate distinguishes the root declaration. This is not a complete repaired RAP model.

**static**: `{"state":"VALIDATION_PASS","reason":null,"diagnostics":{"zr4_view.bdef.asbdef":[],"zr4_view.ddls.asddls":[]},"qualified":true}`

**runtime**: `{"id":"SR_T03_05_ROOT_ONLY","label":"SR_T03_05_ROOT_ONLY","utc":"2026-10-19T16:51:50.441Z","stages":{"transpiled":true,"loaded":true},"checks":[],"sqlTrace":[],"sap":"SAP_EVIDENCE_REQUIRED","engine":"@abaplint/transpiler/runtime 2.14.8","phase":"load","status":"ARTIFACT_TRANSPILED_NO_BEHAVIOR","coverage":"Transpiler returning does not establish CDS/BDEF semantic execution"}`

**SAPCompiler**: NOT_EXECUTED

**historicalScoresChanged**: `false`

**rawLSP**: Generated locally under .repro; not a historical R4 result

**failureStage**: See recorded stages

## SR_T04_06_SUBRC_ONLY

**id**: SR_T04_06_SUBRC_ONLY

**originCase**: T04_06

**change**: Add only explicit sy-subrc handling; retain CLIENT SPECIFIED and @rv.

**profile**: v758

**expected**: Isolate the original unrelated check_subrc finding. A clean result still does not adjudicate target SAP grammar.

**static**: `{"state":"VALIDATION_PASS","reason":null,"diagnostics":{"zcl_r4_case.clas.abap":[]},"qualified":true}`

**runtime**: `{"id":"SR_T04_06_SUBRC_ONLY","label":"SR_T04_06_SUBRC_ONLY","utc":"2026-10-19T16:51:52.060Z","stages":{"transpiled":true,"loaded":true,"invoked":true},"checks":[{"input":{},"actual":104,"completed":true,"expected":104,"pass":true}],"sqlTrace":[{"operation":"select","sql":"SELECT sum( amount )  from \"zr4_data\""},{"operation":"dialect_translation","original":"SELECT sum( amount )  from \"zr4_data\"","sqlite":"SELECT sum( amount )  from \"zr4_data\""}],"sap":"SAP_EVIDENCE_REQUIRED","engine":"@abaplint/transpiler/runtime 2.14.8","phase":"execute","database":"Node built-in SQLite, in-memory, custom minimal adapter; not SAP HANA","completed":1,"referenceExecuted":1,"referencePassed":1,"status":"LOCAL_VERIFIED"}`

**SAPCompiler**: NOT_EXECUTED

**historicalScoresChanged**: `false`

**rawLSP**: Generated locally under .repro; not a historical R4 result

**failureStage**: See recorded stages

## SR_T04_06_USING_CLIENT

**id**: SR_T04_06_USING_CLIENT

**originCase**: T04_06

**change**: Start from the subrc-handled form; replace CLIENT SPECIFIED with USING CLIENT literal 100, keeping @rv.

**profile**: v758

**expected**: Current-client-selection contract for synthetic rows expects 5 if implemented; record unsupported/mismatching adapter behavior without fixing it.

**static**: `{"state":"VALIDATION_PASS","reason":null,"diagnostics":{"zcl_r4_case.clas.abap":[]},"qualified":true}`

**runtime**: `{"id":"SR_T04_06_USING_CLIENT","label":"SR_T04_06_USING_CLIENT","utc":"2026-10-19T16:51:53.771Z","stages":{},"checks":[],"sqlTrace":[],"sap":"SAP_EVIDENCE_REQUIRED","engine":"@abaplint/transpiler/runtime 2.14.8","phase":"transpile","status":"LOCAL_TOOLCHAIN_ERROR","error":"Error: parser_error, Statement does not exist in the configured ABAP version(or a parser error), \"select\", zcl_r4_case.clas.abap:8\n    at Transpiler.validate (LOCAL_PATH_REDACTED\node_modules\\@abaplint\\transpiler\\build\\src\\index.js:158:19)\n    at Transpiler.run (LOCAL_PATH_REDACTED\node_modules\\@abaplint\\transpiler\\build\\src\\index.js:85:14)\n    at Transpiler.runRaw (LOCAL_PATH_REDACTED\node_modules\\@abaplint\\transpiler\\build\\src\\index.js:79:21)\n    at run (LOCAL_PATH_REDACTED\n    at Object.<anonymous> (LOCAL_PATH_REDACTED\n    at Module._compile (node:internal/modules/cjs/loader:1871:14)\n    at Object..js (node:internal/modules/cjs/loader:2002:10)\n    at Module.load (node:internal/modules/cjs/loader:1594:32)\n    at Module._load (node:internal/modules/cjs/loader:1396:12)\n    at wrapModuleLoad (node:internal/modules/cjs/loader:255:19)"}`

**SAPCompiler**: NOT_EXECUTED

**historicalScoresChanged**: `false`

**rawLSP**: Generated locally under .repro; not a historical R4 result

**failureStage**: Local transpiler parsing

## SR_T04_06_NO_ESCAPE

**id**: SR_T04_06_NO_ESCAPE

**originCase**: T04_06

**change**: Start from the subrc-handled form; remove only the host-variable escape @, retaining classic CLIENT SPECIFIED.

**profile**: v758

**expected**: Observe classic parser behavior separately from the escaped-host form; no SAP legality promise.

**static**: `{"state":"VALIDATION_PASS","reason":null,"diagnostics":{"zcl_r4_case.clas.abap":[]},"qualified":true}`

**runtime**: `{"id":"SR_T04_06_NO_ESCAPE","label":"SR_T04_06_NO_ESCAPE","utc":"2026-10-19T16:51:55.441Z","stages":{"transpiled":true,"loaded":true,"invoked":true},"checks":[{"input":{},"actual":104,"completed":true,"expected":104,"pass":true}],"sqlTrace":[{"operation":"select","sql":"SELECT sum( amount )  from \"zr4_data\""},{"operation":"dialect_translation","original":"SELECT sum( amount )  from \"zr4_data\"","sqlite":"SELECT sum( amount )  from \"zr4_data\""}],"sap":"SAP_EVIDENCE_REQUIRED","engine":"@abaplint/transpiler/runtime 2.14.8","phase":"execute","database":"Node built-in SQLite, in-memory, custom minimal adapter; not SAP HANA","completed":1,"referenceExecuted":1,"referencePassed":1,"status":"LOCAL_VERIFIED"}`

**SAPCompiler**: NOT_EXECUTED

**historicalScoresChanged**: `false`

**rawLSP**: Generated locally under .repro; not a historical R4 result

**failureStage**: See recorded stages

## SR_T06_06_ZERO_ROW

**id**: SR_T06_06_ZERO_ROW

**originCase**: T06_06

**change**: Keep ABAP/DDIC source byte-identical; replace the seeded nullable row amount null with integer initial value 0. Leave the permissive adapter schema unchanged.

**profile**: cloud

**expected**: No SQL NULL row means count is 0.

**static**: `{"state":"VALIDATION_PASS","reason":null,"diagnostics":{"zcl_r4_case.clas.abap":[]},"qualified":true}`

**runtime**: `{"id":"SR_T06_06_ZERO_ROW","label":"SR_T06_06_ZERO_ROW","utc":"2026-10-19T16:51:57.156Z","stages":{"transpiled":true,"loaded":true,"invoked":true},"checks":[{"input":{},"actual":0,"completed":true,"expected":0,"pass":true}],"sqlTrace":[{"operation":"select","sql":"SELECT count( * )  from \"zr4_data\" WHERE \"amount\" IS NULL"},{"operation":"dialect_translation","original":"SELECT count( * )  from \"zr4_data\" WHERE \"amount\" IS NULL","sqlite":"SELECT count( * )  from \"zr4_data\" WHERE \"amount\" IS NULL"}],"sap":"SAP_EVIDENCE_REQUIRED","engine":"@abaplint/transpiler/runtime 2.14.8","phase":"execute","database":"Node built-in SQLite, in-memory, custom minimal adapter; not SAP HANA","completed":1,"referenceExecuted":1,"referencePassed":1,"status":"LOCAL_VERIFIED"}`

**SAPCompiler**: NOT_EXECUTED

**historicalScoresChanged**: `false`

**rawLSP**: Generated locally under .repro; not a historical R4 result

**failureStage**: See recorded stages

## SR_T06_07_ZERO_ROW

**id**: SR_T06_07_ZERO_ROW

**originCase**: T06_07

**change**: Keep ABAP/DDIC source byte-identical; replace the seeded nullable row amount null with integer initial value 0. Leave the permissive adapter schema unchanged.

**profile**: cloud

**expected**: Initial integer 0 returns 0, but this does not test NULL transfer.

**static**: `{"state":"VALIDATION_PASS","reason":null,"diagnostics":{"zcl_r4_case.clas.abap":[]},"qualified":true}`

**runtime**: `{"id":"SR_T06_07_ZERO_ROW","label":"SR_T06_07_ZERO_ROW","utc":"2026-10-19T16:51:58.876Z","stages":{"transpiled":true,"loaded":true,"invoked":true},"checks":[{"input":{},"actual":0,"completed":true,"expected":0,"pass":true}],"sqlTrace":[{"operation":"select","sql":"SELECT \"amount\" from \"zr4_data\" WHERE \"id\" = 2 UP TO 1 ROWS"},{"operation":"dialect_translation","original":"SELECT \"amount\" from \"zr4_data\" WHERE \"id\" = 2 UP TO 1 ROWS","sqlite":"SELECT \"amount\" from \"zr4_data\" WHERE \"id\" = 2 LIMIT 1"}],"sap":"SAP_EVIDENCE_REQUIRED","engine":"@abaplint/transpiler/runtime 2.14.8","phase":"execute","database":"Node built-in SQLite, in-memory, custom minimal adapter; not SAP HANA","completed":1,"referenceExecuted":1,"referencePassed":1,"status":"LOCAL_VERIFIED"}`

**SAPCompiler**: NOT_EXECUTED

**historicalScoresChanged**: `false`

**rawLSP**: Generated locally under .repro; not a historical R4 result

**failureStage**: See recorded stages

## SR_T06_08_ZERO_ROW

**id**: SR_T06_08_ZERO_ROW

**originCase**: T06_08

**change**: Keep ABAP/DDIC source byte-identical; replace the seeded nullable row amount null with integer initial value 0. Leave the permissive adapter schema unchanged.

**profile**: cloud

**expected**: SUM remains 10 for NULL or 0 in this row set, so the original aggregate cannot discriminate those data states.

**static**: `{"state":"VALIDATION_FAIL","reason":null,"diagnostics":{"zcl_r4_case.clas.abap":[{"severity":1,"range":{"start":{"line":7,"character":4},"end":{"line":7,"character":48}},"code":"check_subrc","codeDescription":{"href":"https://rules.abaplint.org/check_subrc/"},"message":"Check sy-subrc","source":"abaplint"}]},"qualified":true}`

**runtime**: `{"id":"SR_T06_08_ZERO_ROW","label":"SR_T06_08_ZERO_ROW","utc":"2026-10-19T16:52:00.593Z","stages":{"transpiled":true,"loaded":true,"invoked":true},"checks":[{"input":{},"actual":10,"completed":true,"expected":10,"pass":true}],"sqlTrace":[{"operation":"select","sql":"SELECT sum( amount )  from \"zr4_data\""},{"operation":"dialect_translation","original":"SELECT sum( amount )  from \"zr4_data\"","sqlite":"SELECT sum( amount )  from \"zr4_data\""}],"sap":"SAP_EVIDENCE_REQUIRED","engine":"@abaplint/transpiler/runtime 2.14.8","phase":"execute","database":"Node built-in SQLite, in-memory, custom minimal adapter; not SAP HANA","completed":1,"referenceExecuted":1,"referencePassed":1,"status":"LOCAL_VERIFIED"}`

**SAPCompiler**: NOT_EXECUTED

**historicalScoresChanged**: `false`

**rawLSP**: Generated locally under .repro; not a historical R4 result

**failureStage**: See recorded stages

## SR_T06_06_NOTNULL_SCHEMA

**id**: SR_T06_06_NOTNULL_SCHEMA

**originCase**: T06_06

**change**: Keep original source and NULL row unchanged; add a local SQLite NOT NULL DEFAULT 0 constraint to amount.

**profile**: cloud

**expected**: Local setup must reject the seeded NULL before ABAP invocation. This is a local data-state negative control, not a SAP compiler test.

**static**: `{"state":"VALIDATION_PASS","reason":null,"diagnostics":{"zcl_r4_case.clas.abap":[]},"qualified":true}`

**runtime**: `{"id":"SR_T06_06_NOTNULL_SCHEMA","label":"SR_T06_06_NOTNULL_SCHEMA","utc":"2026-10-19T16:52:02.320Z","stages":{"transpiled":true},"checks":[],"sqlTrace":[],"sap":"SAP_EVIDENCE_REQUIRED","engine":"@abaplint/transpiler/runtime 2.14.8","phase":"transpile","database":"Node built-in SQLite, in-memory, custom minimal adapter; not SAP HANA","status":"LOCAL_TOOLCHAIN_ERROR","error":"Error: NOT NULL constraint failed: zr4_data.amount\n    at run (LOCAL_PATH_REDACTED"}`

**SAPCompiler**: NOT_EXECUTED

**historicalScoresChanged**: `false`

**rawLSP**: Generated locally under .repro; not a historical R4 result

**failureStage**: SQLite adapter data initialization, before ABAP execution