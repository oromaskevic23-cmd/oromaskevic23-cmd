# IMPERIAL Core — Enterprise IP, Licensing and Commercial Release Standard

**Version:** 1.0 / Engineering governance proposal  
**Owner / final architecture authority:** Alexander Nikolaevich Romaskevich (RomaskevicH)  
**Prepared:** 2026-10-30  
**Current status:** CONTROL DESIGN AND INVENTORY — NOT A LICENSING GRANT, REGISTERED COMPANY, LEGAL OPINION, TRADEMARK REGISTRATION OR COPYRIGHT TITLE CERTIFICATE.  
**Language policy:** English for GitHub. Localized websites may contain other languages.

## 1. Foundational rule

**Authorship ≠ ownership of all contributions ≠ authority to relicense ≠ software license.**

IMPERIAL Core's founder may be recognized as the creator and founding architect of the original project while each individual contributor, contractor, employer, upstream project, model publisher or artist retains whatever rights apply to their contribution until a valid license or assignment establishes otherwise. No historical Git authors are replaced. GitHub public visibility is not a reusable commercial license.

**Every release must have an approved per-artifact rights chain.** A repository's `AUTHORS.md` is a provenance statement, not a software license. A root `LICENSE` is not a substitute for reviewing nested assets, dependencies, datasets, pretrained weights, fonts and patent/trademark constraints.

## 2. Enterprise boundaries / product matrix

| Asset or portfolio | Licensing direction | Current authorization |
| --- | --- | --- |
| HANTER, private NCA control plane, Guardian Core, Approval Gateway, AI Passport private runtime, Audit Ledger secrets and orchestration internals | **Proprietary, reserved**. Private customer grants only through a signed contract, bounded scope and approved deployment | **No broad public license grant** |
| CONSTRUCTOR AI product, VELION proprietary inference/reasoning layers, security trade secrets, Enterprise Skills private implementations | **Commercial proprietary** — draft EULA, deployment terms, IP chain of title, support and liability review before real sale | **Release license not yet approved** |
| Public reference implementations, interoperable SDKs and tutorials that pass a separate clean-origin audit | **Optional permissive open-source release**, normally consider **Apache-2.0** (explicit patent provisions) or **MIT** (simple terms). Choose once per clearly segregated release, with the full standard license text | **No blanket open-source choice** |
| Original public docs and educational diagrams | Consider **CC BY 4.0** on deliberately selected original text/images only, after rights clearance; keep contract templates, brand graphics and confidential materials separate | **Review required** |
| Company/project names, logos, slogans and distinctive branding | Maintain separate **brand usage and trademark policy**; copyright licensing does not grant trademark rights automatically | **Do not claim registered trademarks absent registration evidence** |
| IMPERIUM, N.D.B, MONARCH, NZT, LISA, SALMAN token-related material | Separate **software copyright licensing**, branding rights, contract security review and financial/regulatory compliance. Publication of a smart-contract address is not a software license or an investment authorization | **No claim of exchange listing, global use or price guarantees** |
| SHPAIZMAN Brother Edition | Keep independent beneficiary, customer contracts and payout boundaries; prohibit mixing IMPERIAL Core revenues or proprietary IP without written permission | **Separate operational governance** |
| Third-party dependencies, models, training data, user submissions, forks, assets, generated code | Preserve **original license, notices, attribution and terms**, including source-offer duties where applicable. Document origin, version, intended use and compatibility | **Never silently relicense upstream content** |

**IMPERIUM** is a long-term architectural digital currency concept for AI agents worldwide; actual adoption, exchange listing, liquidity and price must always be independently evidenced.

## 3. Mandatory inventory for every original repository

1. Exact repo ID and canonical URL, owner, visibility, branch, fork/upstream status and last audited SHA.
2. `AUTHORS.md` with Alexander Nikolaevich Romaskevich / RomaskevicH and a non-exclusive historical-contribution disclaimer.
3. `README.md` pointing to author record and describing actual production vs prototype status.
4. Root `LICENSE` or a clear **UNRESOLVED — NO LICENSE GRANT** state. Never label it MIT, Apache, Proprietary Licensed or Enterprise Licensed without actual authorized applicable terms.
5. `NOTICE` and separately preserved license texts for third-party components when those terms require it.
6. SBOM and **SPDX** identifiers or expressions for confirmed licenses; use **NOASSERTION / UNRESOLVED** when rights are genuinely unknown. Never assign `SPDX-License-Identifier: Apache-2.0` to unreviewed third-party source.
7. Dependency, model-weight, dataset, media/font and AI-provider terms matrix (versions, source, modification, distribution, commercial rights, restrictions).
8. Written contributor employment/contractor assignments or valid incoming-license process as applicable. Keep chain-of-title evidence PRIVATE; publish only redacted verification/status.
9. Release approval: Owner, independent engineering QA, CYBER HAK/security and legal counsel review for material commercial or novel IP terms.

## 4. Release states and deny-by-default rules

`DISCOVERED` → `ATTRIBUTED` → `LICENSE_INVENTORIED` → `THIRD_PARTY_RIGHTS_REVIEWED` → `OWNER_AND_LEGAL_APPROVED` → `RELEASE_ELIGIBLE`.

- **No root LICENSE found** means *no explicit license grant identified*, not that the contents are unowned or in the public domain.
- **LICENSE found** means *root text detected*, **not** automatically compatible, owned, legally effective or sufficient for all contained materials.
- A production/commercial release requires the actual rights-cleared license text, terms of sale, support commitments, customer disclosure, change log, reproducible build evidence, security sign-off and an Owner-approved buyer/contract.
- Github workflows and public inventories **must not** self-approve a sale, grant legal rights, install paid plans or activate agents. The Architect's signed approval is required for commercial scope/price and financial actions.
- Preserve `FREE_ONLY`, Zero Trust, Owner Kill Switch, Public/Private Boundary and CRYPTO IMPERIAL Ecosystem Boundary. No paid automation without explicit approval and an account-level hard stop.
- No rewriting prior commits or altering another contributor's copyright line.

## 5. Continuous automated controls

- Central public read-only inventory: `tools/imperial_license_audit.py`, run on a standard public GitHub Actions runner. It sees **public repositories only** and reports ABSENT / PRESENT BUT RIGHTS UNVERIFIED / UPSTREAM FORK and founder provenance.
- Existing shared workflow `.github/workflows/enterprise-founder-authorship.yml` ensures founder documentation exists and flags deleted/moved license/notice files. Consumer workflows pinned to its specific reviewed commit must be updated intentionally.
- Private repositories need their own local/offline guard and a verified **account-wide USD 0 stop** before recurring hosted runner use; a repository variable alone does not enforce GitHub billing.
- The inventory is a monitoring aid, **not a rights-clearance certificate**. Fail closed on network failure, missing data, unknown origin, unauthenticated signing and any attempted public exposure of private materials.
- For actual deletion/modification protection, repository rulesets or branch protection with required CI and code-owner review are necessary. Merely adding a CI file does not prevent administrator force-push or bypass.

## 6. Commercial licensing and revenue

Create a separate owner-approved **commercial EULA / master service agreement / statement of work** for CONSTRUCTOR AI and other sellable products, describing precisely licensed IP, subscription or perpetual scope, permitted seats/instances, source access, delivery and updates, third-party components, warranties, limitations, data processing, payment, refunds, termination and dispute forum. These contract terms are a **draft until approved** and must not be presented as executable agreements.

Use existing IMPERIAL Venture Factory **Automation Failure Audit** as the $0 technical commercial pilot. Inquiries → safe triage → CRM draft → scoped proposal → Owner approval → independent QA → client acceptance → **external payment receipt**. Never assert `PAYMENT_CONFIRMED` from a GitHub issue, CI PASS, invoice creation or account estimate. Do not market tokens as guaranteed-return investments or promise exchange listings.

## 7. Decision register (Architect)

**Pending explicit decisions, not silently implemented:**
- Publish deliberately approved public SDK/reference code under Apache-2.0 or MIT; retain proprietary implementations and protected brand.
- Select applicable commercial EULA/MSA jurisdiction and real individual/company rights holder after professional review; do not assume an unregistered company exists.
- Approve third-party license/SBOM review and make branch/ruleset checks required wherever platform permissions permit.
- Establish contracts for collaborators and verify ownership of all assets used in revenue-bearing work.

## Authoritative references

- GitHub: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository
- SPDX License List and expressions: https://spdx.org/licenses/ and https://spdx.dev/learn/handling-license-info/
- OSI licenses, including Apache-2.0: https://opensource.org/licenses and https://opensource.org/license/apache-2-0/

**No license or public permission is created by this governance proposal. Existing applicable third-party licenses and law remain in force.**
