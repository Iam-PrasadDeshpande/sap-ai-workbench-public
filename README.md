# SAP AI Evaluation Workbench: published research

A read-only website that presents Prasad Deshpande's published SAP AI engineering findings: what was tried, where it
ran, what was observed, what it proves and what it does not. Each finding comes from a sealed experiment receipt in
the owner's private workbench and is published only after it passes validation and an owner-approved publication
policy.

Visitors can browse, search and compare findings and ask questions about them. Nothing on the site runs an SAP
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
| `data/` | Static reference data used by the site |
| `PUBLIC_MANIFEST.json` | File list with SHA-256 hashes, the artifact digest and the source commit of the qualified build |
| `requirements.txt` | The single pinned dependency |

## How integrity is checked
- **Code:** the *Method & Evidence* page compares every file with `PUBLIC_MANIFEST.json` and shows the result. A
  change to any code file without a new qualified build shows as a failed check.
- **Content:** each release carries a digest that chains to the previous release, and each finding carries its own
  hash. The site serves the newest release that verifies. If the newest one fails, it serves the last good release and
  says so; if none verifies, it shows nothing.

These checks detect accidental drift or a partial upload. They are not a defence against someone who controls this
repository.

## How content changes
Content changes arrive as commits that touch `content/` only, made by the owner's local publication workflow after a
finding has been validated and approved. Code changes arrive only as a new qualified build. This repository has no
CI workflow.

## Running it
Streamlit Community Cloud: entry point `app.py`, Python 3.12. Locally:

```
pip install -r requirements.txt
streamlit run app.py
```

SAP, SAP BTP, SAP Fiori, SAPUI5, ABAP and other SAP products mentioned are trademarks or registered trademarks of
SAP SE. This is independent research; it is not affiliated with, sponsored by or endorsed by SAP SE.

© 2026 Prasad Deshpande. All rights reserved.
