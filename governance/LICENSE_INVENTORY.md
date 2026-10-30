# IMPERIAL Core — Canonical GitHub Licensing Inventory

**Current verified status:** 30 October 2026, after owner-authorized LICENSE commits.  
**Scope:** All 27 repositories available to the connected GitHub account of `oromaskevic23-cmd`.  
**Source of verification:** direct authenticated reads of `LICENSE` on each repository's `main` branch.  
**Historical automated snapshot:** [GitHub public audit 41120216750](https://github.com/oromaskevic23-cmd/oromaskevic23-cmd/actions/runs/41120216750) predates the LICENSE rollout (then 0/20 public roots).

## Current root-file and identity findings

| Item | Verified |
| --- | ---: |
| Owner-accessible GitHub repositories | **27** |
| Public repositories | **20** |
| Private repositories | **7** |
| Root LICENSE files read from `main` | **27 / 27** |
| Files identifying founder Alexander Nikolaevich Romaskevich | **27 / 27** |
| Private repositories with explicit proprietary LICENSE | **7 / 7** |
| Public repositories with original-rights, source-available proprietary LICENSE | **20 / 20** |
| Standard MIT text for standalone original verifier SDK | **Present** |
| Real customer commercial EULAs granted and authenticated by this audit | **0** |
| Fully cleared dependency/model/media rights chains | **NOT VERIFIED** |

**Important distinction:** A root `LICENSE` exists in all 27 repositories, but it is a custom **proprietary** notice scoped only to original rights actually held. It does **not** certify ownership of all assets or turn third-party licensed materials into proprietary originals.

The isolated MIT reference module is separately licensed at
[`tools/cryptographic-license/LICENSE`](../tools/cryptographic-license/LICENSE).
A GitHub `Other / NOASSERTION` repository-level license classification is expected
for the *profile repository's custom root LICENSE*. GitHub should **not**
misrepresent the entire IMPERIAL Core portfolio as MIT-licensed.

## Cryptographic entitlements — independently checked

The actual offline Ed25519 license verification implementation is under
[`tools/cryptographic-license/`](../tools/cryptographic-license/README.md).
[PR #10](https://github.com/oromaskevic23-cmd/oromaskevic23-cmd/pull/10)
and [GitHub CI run 41124875200](https://github.com/oromaskevic23-cmd/oromaskevic23-cmd/actions/runs/41124875200)
confirm **16 / 16 passing tests** and no production signing key in code.

Production signing, legally executed customer contracts, independently validated
Owner approval receipts, Vault/KMS secret storage, operational online revocation,
HANTER production worker and real sales are **NOT** established by these tests.
Never misclassify CI as a paid order or client license sale.

## Continuous controls

- [Public repository IP audit](../.github/workflows/imperial-ip-surveillance.yml)
  runs on the public profile repository at `29 4,16 * * *` and manually;
  it only inventories **public** repositories by read-only API.
- [Founder authorship and license guard](../.github/workflows/enterprise-founder-authorship.yml)
  is reused across the portfolio and checks attribution and selected notice
  deletion/movement. Mandatory branch approval / anti-force-push protections
  require GitHub Rulesets and separate confirmed repository administration.
- **Private** repositories are not scanned by the public audit and their
  source, rights documents and credentials must never be copied into public CI.
- The organization-wide third-party SBOM, legal chain-of-title, model licensing,
  trademark registrations and customer financial claims remain distinct
  unfinished evidence requirements.

## Policy and records

- [Enterprise licensing standard](../docs/IMPERIAL_ENTERPRISE_LICENSING_STANDARD.md)
- [Commercial product license draft](../docs/COMMERCIAL_SOFTWARE_LICENSE_TERM_SHEET_DRAFT.md)
- [Release approval checklist](../docs/IP_RELEASE_APPROVAL_TEMPLATE.md)
- [Founding authorship](../AUTHORS.md)

**NOT A RIGHTS CLEARANCE CERTIFICATE.** License file presence, founder identity,
digital signatures and software test passes are separate from legal copyright
title, externally confirmed customer approval and production revenue.
