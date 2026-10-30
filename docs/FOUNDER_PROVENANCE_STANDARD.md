# IMPERIAL Core — Founder Authorship and Repository Provenance Standard v1.0

**Owner-designated founding architect:** Alexander Nikolaevich Romaskevich (RomaskevicH).  
**Applicability:** Original IMPERIAL Core repositories where first-party ownership/origin is supported by current repository evidence.

## Required files and checks

1. Preserve **AUTHORS.md** with the founding architect, GitHub signature, contributor provenance, and explicit third-party rights boundary.
2. Make the founder discoverable in the repository **README.md**.
3. Retain all pre-existing `LICENSE`, `LICENCE`, `COPYING`, `NOTICE`, `PROVENANCE`, and upstream authorship records; never rewrite Git commit history to claim existing contributors' work.
4. Maintain `.github/CODEOWNERS` for review guidance. GitHub CODEOWNERS alone is **not** a protected branch or mandatory approval.
5. Verify changes with the reusable `.github/workflows/enterprise-founder-authorship.yml`: checks required attribution and blocks deletion/movement of pre-existing tracked license/notice artifacts in pull requests. All new repositories should use a full Git-history checkout for comparison.
6. Do not assert third-party clearance, registered trademark rights, corporation status, exclusive ownership of machine-generated output, or permission to use material without its original license.
7. A repository with no top-level LICENSE has **UNRESOLVED LICENSE STATUS**, not an inferred proprietary license or open-source license. Any relevant dependency, vendor snapshot, training content, or upstream license still requires separate detailed examination.

## Explicit project boundaries

- **Third-party forks:** Robbyant/lingbot-vla-v2 (Apache-2.0); 666ghj/MiroFish (AGPL-3.0): preserve upstream authors and license. Not IMPERIAL-original.
- **SHPAIZMAN-ORCHESTRATOR:** brother's separate business ownership and beneficiary boundary, not an IMPERIAL Core original repository for a blanket founder ownership assertion.
- **Existing original modules:** distinguish authorship of project conception and architecture from individual authored code lines and actual contributions.
- **Security:** preserve Guardian Core, Approval Gateway, AI Passport, Audit Ledger, Zero Trust, Public/Private Boundary and CRYPTO IMPERIAL Ecosystem Boundary.

## Enforcement limitations

A GitHub Actions PASS is a **bounded provenance check**, not comprehensive legal/license clearance. Workflow deletion, bypassed CI, and unreviewed force pushes may defeat it unless required branch rulesets, required status checks, and review requirements are configured. For private repositories, new GitHub-hosted CI jobs are skipped by default unless the $0 Actions budget hard-stop has been verified; this protects the FREE_ONLY requirement at the expense of automatic verification coverage. Do not claim enforceable protection in those repositories without a working independent approval mechanism.

**Version:** 1.0 — 2026-10-30. No old commits rewritten.
