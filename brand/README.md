# IMPERIAL Core — One Corporate Symbol Policy

**Canonical decision:** 3 November 2026.  
**Authority:** Alexander Nikolaevich Romaskevich (RomaskevicH) · Founder, Owner, CEO & Chief Systems Architect.  
**Policy ID:** `IMPERIAL-CORE-CORPORATE-SYMBOL-LOCK-001`.  
**Status:** Pinned in the official GitHub profile with tested integrity checks; **cross-repository enforcement not yet verified**.

## One symbol, many digital agents

**The single corporate mark is the existing GitHub profile asset:**
[`assets/imperial-core-emblem.webp`](../assets/imperial-core-emblem.webp).

This is the asset identified in the present GitHub profile repository as the IMPERIAL Core emblem. Do **not** generate a new corporate symbol for a website, CRM, broker avatar, real estate presentation, HANTER or a new service. Do **not** substitute a newly invented eye, bird, crown, animal, abstract letter or different insignia for this existing corporate mark.

**Authoritative bytes:** the Git blob fingerprint (SHA-1 of the Git blob object, not the raw file's SHA-256) is
`7749da03da49d4434fc826d0f26793785a3cab42`.

The actual canonical path, SHA, and permitted variations are machine-readable in [`brand/corporate-symbol-lock.json`](../brand/corporate-symbol-lock.json). [`tools/check_corporate_symbol.py`](../tools/check_corporate_symbol.py) checks the original file bytes, location, policy and approved-variation fields. [GitHub Actions](../.github/workflows/corporate-symbol-lock.yml) runs this check and adversarial tests.

### Allowed on Capital Core / universal NCA avatars

- Every agent can have a unique fictional visual persona, face, name, hairstyle, professional outfit, role and city. No agent is required to look like another.
- Apartment, penthouse, luxury villa, commercial property, skyscraper and other real-estate backgrounds may vary.
- Local agent/team names and agent-specific visual identity are separate from the legal/project-level corporate branding.
- The **IMPERIAL Core corporate emblem remains the exact approved mark**, without regeneration, repainting, geometric redesign, AI reimagining or replacement. Reversible scaling and unmodified overlays are allowed so long as the emblem remains legible and intact.
- A separate product logo (e.g. a cryptocurrency token logo, HANTER-specific banner or IMPERIAL EYE interface glyph) is **not** an alternative IMPERIAL Core corporate mark, and must not occupy the corporate logo slot.

### Required implementation pattern

Other official websites/repositories should reference this exact original GitHub asset, or package the identical asset bytes and verify their Git blob fingerprint. Example remote image reference:

```text
https://raw.githubusercontent.com/oromaskevic23-cmd/oromaskevic23-cmd/main/assets/imperial-core-emblem.webp
```

Use a locally bundled copy for production only if its bytes match the pinned source. Preserve creator attribution and existing asset provenance documents. This policy governs visual consistency; it does not independently establish legal title to images or transfer copyright from contributors.

### Release gate

1. Brand audit finds the existing corporate logo positions in each website, CRM, public dashboard, Capital Core or NCA agent card.
2. Replace only incorrect **corporate-mark placements** with the canonical asset; leave original NCA avatars, third-party trademarks and distinct product images intact.
3. Validate the source hash, page layout, crop, responsive/mobile rendering, accessibility text and that a product-specific logo is never misrepresented as IMPERIAL Core corporate emblem.
4. Record the exact touched paths and GitHub Actions/test evidence.
5. Any actual corporate emblem **change requires the Architect's separate explicit approval**, a new approved source file and evidence-backed versioned decision. No agent or template may silently decide such a change.

**Limitations:** GitHub CODEOWNERS and CI tests alone do not stop a repository administrator from replacing files or bypassing branch checks. Active protected branches/rulesets and verified enforcement are separate requirements. No company-wide deployment is claimed by the existence of this policy.

**Principle:** ONE corporate emblem · UNLIMITED distinct NCA personas · ZERO invented alternate corporate identities.
