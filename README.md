# SAP AI Evaluation Workbench

**From SAP Developer Capabilities to Practical Engineering Proof.** A read-only website that evaluates the AI and
AI-enabling developer capabilities SAP makes available, starting from developers.sap.com: what each capability is
for, what access it needs, what has been practically evaluated, and what the evidence says about its usefulness,
maturity and limitations. Hands-on results come from sealed experiment receipts in Prasad Deshpande's private
engineering workbench and are published only after they pass validation and the owner approves them.

Visitors can browse the capability catalog, read and compare hands-on evaluations and ask the evidence questions. Nothing on the site runs an SAP
operation, signs in to an SAP system, writes visitor input to storage or calls a language model. Questions live only
in the memory of the visitor's browser session. The app has no accounts and no analytics; the Streamlit framework sets
a technical request-forgery protection cookie, and the hosting platform operates under its own terms.

A finding validated against SAP's public developer service shows what SAP publishes. It does not show that a
capability works in any SAP tenant.

## What is in this repository
| Path | What it is |
| --- | --- |
| `app.py`, `sap_public/` | The Streamlit application (public edition only; it has no access to the private workbench) |
| `content/` | Versioned research content: `index.json` and immutable `releases/NNNN.json` |
| `data/` | Static reference data, including `capabilities.json`, generated from the private workbench's canonical capability contract (identity only, no execution evidence) |
| `PUBLIC_MANIFEST.json` | File list with SHA-256 hashes, the artifact digest and the source commit of the qualified build |
| `requirements.txt` | The single pinned dependency |

## How integrity is checked
- **Code:** the *Evaluation Framework* page compares every file with `PUBLIC_MANIFEST.json` and shows the result. A
  change to any code file without a new qualified build shows as a failed check.
- **Content:** each release carries a digest that chains to the previous release, and each finding carries its own
  hash. The site serves the newest release that verifies. If the newest one fails, it serves the last good release and
  says so; if none verifies, it shows nothing.

These checks detect accidental drift or a partial upload. They are not a defence against someone who controls this
repository.

## How content changes
Content changes arrive as commits that touch `content/` only, made by the owner's local publication workflow after a
finding has been validated and approved. Research notes are displayed only when their exact canonical content digest
is registered in `sap_public/session_approvals.py`. For this read-only public site, the owner-approved release
procedure rebuilds `PUBLIC_MANIFEST.json` and runs the repository's offline qualification checks; the manifest records
SHA-256 hashes and detects drift, but is not a cryptographic signature. This procedure does not change private
workbench D012 signing requirements. Code changes arrive only as a new qualified build. This repository has no CI
workflow.

## Running it
Streamlit Community Cloud: entry point `app.py`, Python 3.12. Locally:

```
pip install -r requirements.txt
streamlit run app.py
```

SAP, SAP BTP, SAP Fiori, SAPUI5, ABAP and other SAP products mentioned are trademarks or registered trademarks of
SAP SE. This is independent research; it is not affiliated with, sponsored by or endorsed by SAP SE.

© 2026 Prasad Deshpande. All rights reserved.
