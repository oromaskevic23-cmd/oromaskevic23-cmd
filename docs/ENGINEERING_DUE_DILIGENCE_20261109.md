# CONSTRUCTOR AI — Engineering Due Diligence

**Public evidence snapshot:** 9 November 2026  
**Founder and final architectural authority:** Alexander Nikolaevich Romaskevich (RomaskevicH)  
**Stage:** Working, reproducible local prototype; **not** a production autonomous software factory  
**Product:** [CONSTRUCTOR AI](https://github.com/oromaskevic23-cmd/CONSTRUCTOR-AI) within IMPERIAL Core

## Executive assessment

CONSTRUCTOR AI is the current flagship product. Its public Template Studio exports three reviewed **local, single-user** applications: Task Manager, Business CRM and Business Dashboard. Visitors can inspect source, run deterministic checks and test the exported applications. This supports a prototype demonstration, not a claim of enterprise sales, arbitrary prompt-to-production generation, deployed autonomous agents or external security certification.

**Evaluation route:** [Open the demonstration](https://oromaskevic23-cmd.github.io/Capital-Core-Public/reference/constructor-ai/studio/studio.html) · [Review source](https://github.com/oromaskevic23-cmd/CONSTRUCTOR-AI) · [Read investor/pilot scope](https://github.com/oromaskevic23-cmd/oromaskevic23-cmd/blob/main/docs/CONSTRUCTOR_AI_INVESTOR_OVERVIEW.md)

The published demo URL is supplied by the project; check its live reachability directly before a meeting. The evidence below concerns source revision and GitHub checks, not continuous public-site uptime.

## Evidence table

| Claim | Evidence | Scope / limitation |
| --- | --- | --- |
| Template Studio has runnable source and a reproducible verification procedure | [Public repository](https://github.com/oromaskevic23-cmd/CONSTRUCTOR-AI), [acceptance documentation](https://github.com/oromaskevic23-cmd/CONSTRUCTOR-AI/blob/898d1abe2616cb92104b64dc126e0875cc9acddf/docs/FLAGSHIP_ACCEPTANCE.md) | Three predefined templates, local single-user output |
| Project-controlled source validation passed at a fixed revision | [GitHub Actions run 42001525579](https://github.com/oromaskevic23-cmd/CONSTRUCTOR-AI/actions/runs/42001525579) | Successful on 5 November 2026 for commit `898d1abe2616cb92104b64dc126e0875cc9acddf`; not an external audit |
| Chromium browser acceptance passed at the same fixed revision | [GitHub Actions run 42001525556](https://github.com/oromaskevic23-cmd/CONSTRUCTOR-AI/actions/runs/42001525556) | Real browser test of reviewed local templates and exports; not cross-browser or production acceptance |
| The product can generate arbitrary custom production applications from a prompt | **Not established** | Controlled real-model experiments and bounded local candidates do not satisfy full-product acceptance |
| A production, multi-user hosted service operates with a customer SLA | **Not established** | No externally verifiable deployment/uptime/availability proof supplied here |
| Revenue, paying customers or signed investor commitments exist | **Not established** | No customer contract, invoice, payment evidence or independently confirmed investor commitment supplied here |
| External cybersecurity certification has been obtained | **Not established** | Repository-level tests and security architecture are not certification |

## Independent reproducibility

Use Node.js 22+, npm and unzip. Reproduce the **tested revision** rather than assuming a moving `main` has identical results:

```sh
git clone https://github.com/oromaskevic23-cmd/CONSTRUCTOR-AI.git
cd CONSTRUCTOR-AI
git checkout 898d1abe2616cb92104b64dc126e0875cc9acddf
npm ci --ignore-scripts --no-audit --no-fund
npm run verify
node tools/build-acceptance.mjs acceptance-output
node tools/verify-acceptance.mjs acceptance-output
```

This procedure is an invitation to inspect project-controlled acceptance; running it is the reviewer's own verification. CI status alone does not prove that external, independent human testing was completed.

## Target platform and security architecture

The long-term IMPERIAL Core system uses a **Federated Multi-Orchestrator Architecture**: HANTER as AI Command Center, multiple specialized orchestrators, dynamic Nano Core Agents, VELION for model intelligence and ORION for collective intelligence. Execution governance requires **AI Passport**, **Enterprise Skills**, **Guardian Core**, **Approval Gateway**, **Audit Ledger**, **Zero Trust**, **ProofGraph**, **IntentLock**, **Owner Kill Switch**, and explicit **Public/Private Boundary** and **CRYPTO IMPERIAL Ecosystem Boundary**.

These are architectural requirements. No statement here implies that each is deployed for the Template Studio or that the platform operates as a commercial, autonomous 24/7 service.

## Risks and acceptance gates

| Priority | Required evidence before commercial-readiness claim |
| --- | --- |
| P0 | One complete, bounded requirement-to-code workflow using an authorized real model, isolated execution, independent QA and an explicit Owner approval gate |
| P0 | Valid production identity and revocation controls for any agent performing consequential actions |
| P0 | Reproducible source-to-artifact provenance, pinned supply chain and security review of the concrete deployment |
| P1 | Written, limited-scope customer pilot, acceptance criteria and honest failure/rejection recording |
| P1 | Multi-user authentication, retention/privacy controls, tested backup/restore, support, uptime and total operating cost |
| P1 | Commercial rights and third-party license review before any sale or transfer |

## Pilot / investor request

Potential reviewers can propose a **single bounded use case** (for example, a small business task board or client pipeline), an evaluation environment, acceptance criteria and a decision timeline. Do not send credentials or customer personal data in an initial public inquiry.

No customer outcome, contract, financing, external endorsement, company valuation or acquisition offer is asserted by this document. Any negotiated terms require separate documented agreement.

Contact the founder: [oromaskevic23@gmail.com](mailto:oromaskevic23@gmail.com).  
Authorship of original project contributions: **Alexander Nikolaevich Romaskevich — RomaskevicH**; third-party code, models and contributions retain their own rights.

## Evidence maintenance

This document is a **dated snapshot**, not continuous monitoring. Update it only after recording a new commit, actual test run, deployed endpoint proof, signed acceptance or independently checkable external evidence. A proposed feature, branch, passing mock test or local simulated worker must never be reported as production capability.
