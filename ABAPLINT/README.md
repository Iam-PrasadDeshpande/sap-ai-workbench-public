# abaplint in Agentic ABAP Engineering — Independent Local Assessment (R1–R4)

**Author:** Prasad Deshpande  
**Study date:** October 2026  
**Research status:** `RESEARCH_COMPLETE_WITH_LIMITATIONS`  
**Adoption verdict:** `CONDITIONAL_LOCAL_GATE_ONLY`  
**Target:** abaplint core `2.120.81` as bundled in VS Code extension `larshp.vscode-abaplint` `0.6.698`, with selected pinned off-stack transpilation/runtime components in later rounds.

## Why this evaluation

An AI agent can generate convincing ABAP, but that is not the same as producing source that parses, satisfies dependency contracts, runs as intended, or is valid on a specific SAP release. I examined how far a local abaplint-based workflow can go before a real SAP environment becomes necessary.

These four rounds evaluated **abaplint static analysis, Codex-assisted ABAP repair and selected off-stack behavior**. They **did not directly evaluate Open SteamGate**, its ADT integration, SEGW/OData compatibility, or its complete runtime surface.

## What was observed

| Round | Scope | Grounded result |
| --- | --- | --- |
| **R1** | Installed VS Code language server; ABAP/CDS and cross-object static checks | Static lint worked within configured scope. Configuration and dependency availability materially changed diagnostic results. No SAP execution. |
| **R2** | Fail-closed validation and agent-guided repair | **19/19** validation sentinels passed; **five** static-repair cases converged. Incorrect business logic could remain lint-clean. |
| **R3** | Generation-only Codex vs Codex with abaplint feedback; selected off-stack behavioral checks | Initial comparison: **9/10** static acceptance and **8/9** executable tasks in *each* arm. Repeated repair study: **15/15** whole executable tasks and **2,016/2,016** withheld checks in *each* arm. No incremental output-quality lift was established on these synthetic tasks. |
| **R4** | Six enterprise ABAP areas, **42** frozen synthetic cases | **42/42** qualified local static analyses; **21/42** strictly clean; **eight** known-defect cases accepted by strict static validation. Selected off-stack execution covered **15** cases and **57/76** completed reference checks matched. All 42 cases still require SAP-side evidence for SAP claims. |

R4's original **77 frozen expectations vs 76 completed checks** were reconciled: `T06_10` was invoked but produced no reference value because its database was not initialized. The separately documented adapter recovery does not change the historical **57/76** score. The CDS supplement was kept separate.

The R3 arms had both strong baseline performance and a synthetic test ceiling. A finding of **no observed quality lift** is not proof that abaplint can never improve agent output. The withheld test checks are not thousands of independent human-authored programming tasks.

## Where abaplint helps

- Catches configured ABAP syntax and static-analysis issues early, before SAP contact.
- Supplies machine-readable diagnostics for bounded agent repair loops.
- Helps enforce a repeatable coding policy when configuration, source discovery and sentinel diagnostics are verified.
- Supports a useful off-stack workflow when coupled with **separate** transpilation/runtime components for supported ABAP subsets.

## What a reliable pipeline still needs

1. **A validated lint configuration:** pin versions and policy; prove a known-invalid sentinel is actually flagged. Zero diagnostics alone must not imply PASS.
2. **Dependency and release-contract evidence:** SAP-standard objects, DDIC contracts, released APIs and the target ABAP language version cannot be assumed from a small local repository.
3. **Independent behavioral tests:** a source file can be lint-clean but implement the wrong business rule. Off-stack execution provides evidence only for its supported subset.
4. **SAP-side qualification:** compiler/activation, ATC, ABAP Unit, RAP behavior, authorizations, client handling, locking, LUW/update behavior and SAP/HANA database semantics remain outside this local proof.

## Important limitations

- Some apparent failures or mismatches were **configured-pipeline or adapter limitations**, not demonstrated upstream abaplint defects. In particular, R4's client-query mismatch came from an incomplete SQLite adapter.
- Static-analysis acceptance blind spots describe the **tested policy and environment**; they are not all allegations that the linter is defective.
- No SAP-system calls occurred, and no SAP runtime equivalence was established.
- `FOR ... WHERE` case T07 remained unresolved against a live SAP compiler.
- R1–R4 used synthetic/model-authored tasks; there was no independently human-authored gold benchmark or formal external peer review.
- The original local evidence and manifests are retained privately. This public-facing summary is a **sanitized synthesis of owner-reported local results**, not a fully reproducible evidence release or independent forensic audit.

## Architecture decision

```text
AI-generated ABAP
    -> dependency and target-release contract checks
    -> configuration / sentinel validation
    -> abaplint static analysis
    -> bounded agent repair and revalidation
    -> off-stack behavioral tests (supported subset)
    -> SAP-side verification (separately authorized)
```

**Decision:** Adopt abaplint as a **conditional local engineering gate**, not as an autonomous SAP developer, semantic RAP verifier, or replacement for SAP testing. No extra REA intermediary was justified by these experiments.

## Relationship to Open SteamGate

[Open SteamGate](https://github.com/oisee/open-steamgate) proposes a broader off-stack ABAP experience involving local runtime and developer tooling. This evaluation focused on abaplint and selected transpilation/runtime functions, **not Open SteamGate itself**. Whether its ADT compatibility, OData, RAP-adjacent behavior and SAP-semantics coverage meet enterprise requirements would need a separate direct test of that project.

## References

- [abaplint](https://github.com/abaplint/abaplint)
- [abaplint VS Code extension](https://github.com/abaplint/vscode-abaplint)
- [abaplint transpiler/runtime](https://github.com/abaplint/transpiler)
- [abaplint configuration documentation](https://github.com/abaplint/abaplint/blob/main/docs/getting_started.md)
- [Open SteamGate](https://github.com/oisee/open-steamgate)

*Independent research; not affiliated with or endorsed by SAP SE, abaplint, or Open SteamGate. Historical local evidence was frozen with documented gaps. Publication and evidence-release review remain separate decisions.*

## Exact 42-case R4 review package

The original summary above is retained. This research-branch candidate includes a traceable review package of the original 42 frozen R4 cases: [case index](CASE_INDEX.md), [methodology and setup](METHODOLOGY.md), [exact configurations](config/cloud.json), [rule-scope interpretation](RULE_SCOPE.md), [provenance](results/provenance.json) and [public artifact manifest](EVIDENCE_MANIFEST.sha256).

This is a local research reproduction package, not an upstream bug list. Eight historical clean known-defect acceptances are individually explained; most involve configuration, missing metadata or semantic checks outside the qualified rule scope. No upstream issue is confirmed here. Original sources and configuration bytes are retained, while traces and portable harnesses are sanitized derivatives. Read [reproduction validation](results/reproduction-validation.json) for actual coverage and any failures. Public external dependencies and the exact extension server are required; this is not a dependency-free/self-contained distribution.

The original summary-only evidence-release caveat remains historical context. This additional package releases the enumerated synthetic R4 inputs and sanitized outputs; it does not release unrelated private inventories or establish independent human-gold, SAP equivalence, or full enterprise semantics.

### Public harness validation

The portable package was independently rerun locally with freshly installed pinned npm dependencies and the matching installed extension server: **42/42 original static diagnostic outcomes and 42/42 original runtime outcomes reproduced**, including intended failures and unsupported cases; T06_07's separate adapter recovery also reproduced. The final selected references remain 57/76 of 77 expectations. Reproduction is not a claim that all programs passed or that SAP behavior is equivalent. See [validation record](results/reproduction-validation.json).


## Technical revalidation (2026-10-19)

All 42 original cases and 57 source artifacts retained. This is a technical interpretation audit, not a new generation benchmark. All 42 descriptions reconciled; six priority cases reviewed; eight supplemental controls excluded from historical denominators.

5/6 priority interpretations qualified within local evidence; T04_06 release-specific SELECT grammar unresolved. SAP compiler/activation/runtime: NOT_EXECUTED for all cases. Zero demonstrated upstream defects. The eight historical policy acceptance blind spots are not eight product defects.

- T02_05: ordinary available local classes; component/release violation not established.
- T03_05: missing root confounds missing implementation-class attribution; root-only control is not a repaired BO.
- T04_06: classic v758; check_subrc is unrelated to CLIENT SPECIFIED legality. Exact target syntax requires SAP verification.
- T06_06/07/08: valid selected SQLite oracles over an injected NULL; target SAP DDIC physical nullability unverified. Zero-row controls reveal which outputs discriminate the data states.

Historical outcomes remain 21/42 strictly clean, 8 policy acceptance blind spots, 15 locally verified main cases, and selected 57/76 returned matches against 77 frozen expectations. Original-only is 56/75. Retain 19 mismatches and T06_10 missing returned result. Three earlier CDS supplements remain separate.

See [TECHNICAL_REVALIDATION.md](TECHNICAL_REVALIDATION.md).
