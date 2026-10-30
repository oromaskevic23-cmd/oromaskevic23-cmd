# IMPERIAL Core — Product License Release Approval Record (Template)

**Status: BLANK / NOT AUTHORIZED.** Not a software license, legal opinion, corporate representation, payment request or approval in itself.

## A. Required identity and authority
- Product / repository and canonical immutable commit SHA: **TBD**
- Release version / artifact SHA-256 / SBOM digest: **TBD**
- Rights-holding individual or established legal entity, with supporting chain of title: **TBD**
- Authorized IP/licensing decision-maker: **Alexander Nikolaevich Romaskevich (RomaskevicH)**, subject to verified rights
- Legal jurisdiction and competent counsel: **TBD — COUNSEL REVIEW REQUIRED**

## B. License classification

Choose **one verified classification for each separately identifiable artifact**, not one label for an entire mixed-rights repository.

| Class | Potential form | Mandatory rights evidence |
| --- | --- | --- |
| Internal control plane / proprietary source | No public grant; separate negotiated license | Authorship, contributor assignments, upstream terms |
| Sellable CONSTRUCTOR AI / VELION component | Proprietary customer EULA / order form / service terms | Ownership chain, provenance, permitted territory, delivery obligations |
| Approved original open SDK/reference | Exact complete standard MIT or Apache-2.0 text | Every necessary right to grant, dependency compatibility, notices |
| Selected original documentation or artwork | Explicit CC BY 4.0 or other owner-approved license | Source, image/font provenance, brand exclusions and attribution |
| Third-party package, model, dataset, font, media or fork | Its actual upstream license, **not** the project's invented replacement | Identified upstream license/version, permitted usage, retained notice |

`UNRESOLVED`, `NOASSERTION` and `REQUIRES_COUNSEL_REVIEW` are **NOT** authorization.

## C. Evidence manifest

Record a manifest privately, with only redacted status publicly:

- `artifacts[]`: immutable path, SHA-256, original/upstream source, rights holder and confirmed SPDX expression
- `dependencies[]`: purl/package/version, upstream LICENSE and NOTICE, SBOM path and compatibility decision
- `models[]`: provider/model/version/weights license, commercial-use and hosting limitations
- `datasets[]`: source provenance, privacy permission, training/reuse terms and removal duties
- `media[]`: creator, asset source, rights, font redistribution and trademark restrictions
- `contributions[]`: actual Git authors, verified assignments/licenses where needed
- `security[]`: CYBER HAK scan results, Guardian/Approval, independent QA evidence
- `business[]`: product support, customer terms, refunds, tax and regulatory analysis where applicable

**Public/Private Boundary:** Never upload private agreements, keys, identities, client details or confidential evidence to a public repository.

## D. Hard release gates

These are separate, necessary checks: **all must be affirmative and evidenced** for a claim of a licensed commercial release.

1. `IP_ORIGIN_VERIFIED` — authenticated originals and contributors identified.
2. `THIRD_PARTY_TERMS_CLEARED` — upstream rights and obligations mapped.
3. `OWNER_LICENSE_SCOPE_APPROVED` — specific artifact and permitted distribution documented.
4. `LEGAL_COUNSEL_REVIEWED_IF_REQUIRED` — material legal risks reviewed.
5. `GUARDIAN_AND_CYBER_HAK_PASS` — defensible security evidence.
6. `INDEPENDENT_QA_PASS` — technical product verifies under approved environment.
7. `APPROVAL_GATEWAY_APPROVED` — immutable owner decision with audit reference.
8. `CUSTOMER_TERMS_APPROVED` — contract/price/taxes/payout boundary accepted.
9. `EXTERNAL_PAYMENT_RECEIPT` — mandatory before `PAYMENT_CONFIRMED`, not before a free release.

If any required pre-release item is missing, classify as `HOLD_FOR_REVIEW`. No agent or workflow can interpret this blank template as authorization.

## E. Recorded decision

- Decision: **NOT MADE**
- Approved license text reference / SHA: **NOT SET**
- Approved signer + authenticated signature: **NOT SET**
- Approval Gateway event ID: **NOT SET**
- ProofGraph/Audit Ledger receipt: **NOT SET**
- Effective start date: **NOT SET**

## F. Post-release

Keep signed source archives, immutable proofs, correct notices and versioned license texts; maintain inbound reporting for violations, upstream changes, third-party takedowns, product vulnerabilities, renewal and termination. Changes to a prior open-source grant cannot be represented as revocation of rights already granted under that grant.

**Standard:** [Enterprise Licensing Standard](IMPERIAL_ENTERPRISE_LICENSING_STANDARD.md).
