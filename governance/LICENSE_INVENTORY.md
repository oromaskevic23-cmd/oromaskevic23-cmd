# Central IP License Inventory — IMPERIAL Core GitHub Profile

**Evidence:** first successful central read-only GitHub Actions public audit on 2026-10-30, run [41120216750](https://github.com/oromaskevic23-cmd/oromaskevic23-cmd/actions/runs/41120216750).

- Public repositories checked: **20**
- Verified founder provenance declarations: **20 / 20**
- Root LICENSE/LICENCE/COPYING files found: **0 / 20**
- Commercial releases or customer licenses authorized: **0**
- Owner account also contains private repositories: **NOT covered by this public workflow**
- Nested third-party licenses, fonts, media, model weights, SPDX SBOMs and contribution assignments: **NOT certified**

**This central profile repository itself has no root LICENSE file in the observed check.** Public source availability does not supply an open-source permission or establish exclusive ownership of third-party material.

**Automation:** [imperial-ip-surveillance.yml](../.github/workflows/imperial-ip-surveillance.yml), twice-daily schedule plus code-change triggers. The workflow is limited to read-only public metadata and founder documents and fails on incomplete provenance following the new guard update.

**Private source boundary:** Review private provenance inside authorized private repositories; do not expose their code, agreements or internal project names in the public JSON report.

**Decision required for any actual rights grant:** The Architect must select and approve an appropriate license **for each independently cleared asset**, with necessary legal review. The default remains `UNRESOLVED / NO EXPLICIT LICENSE GRANT`, not a false MIT/Apache-2.0 claim.

See [Enterprise IP Licensing Standard](../docs/IMPERIAL_ENTERPRISE_LICENSING_STANDARD.md) and [Release Approval Template](../docs/IP_RELEASE_APPROVAL_TEMPLATE.md).
