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
