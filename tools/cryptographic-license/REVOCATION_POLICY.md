# Signed revocation evidence — Sprint 013

**Status:** Offline reference implementation and tests. **NOT deployed to production** and not a customer license issuer.
**Architect / Founder:** Alexander Nikolaevich Romaskevich (RomaskevicH).
**Original reference source license:** MIT, scoped to this separately licensed module; IMPERIAL Core proprietary sources remain governed by their own licenses.

## Threat and fix

The original license verifier checks a supplied list of revoked license IDs and
key IDs, but it cannot establish who produced the list or whether it is fresh.
An empty or stale list could be supplied by an attacker.

The additional API, **verifyLicenseWithFreshRevocations**, denies the license
unless a separately pinned Ed25519 revocation signer authenticates a snapshot
that is within its valid time interval. It then passes both authenticated
revocation ID sets into the existing license verifier.

The older **verifyLicense** and **verify-cli.mjs** remain OFFLINE DIAGNOSTIC
reference implementations only. They are NOT standalone production runtime gates.

## Strict signed snapshot

The envelope must have exactly two properties: payload and signature.
The payload has only schema, keyId, issuedAt, expiresAt,
revokedLicenseIds and revokedKeyIds.

- Schema: imperial.revocations.ed25519.v1.
- Lifetime: at most 24 hours; future or expired snapshots are denied.
- IDs: canonical, unique, sorted, maximum 10,000 in each list.
- Signature: canonical JSON Ed25519, validated against a separately pinned
  public key from trustedRevocationPublicKeys. The snapshot never supplies trust.
- License issuer public keys are pinned separately.
- No embedded private keys, network requests, billing, production licenses
  or live customer issuing service.

## Integration example

~~~js
import { verifyLicenseWithFreshRevocations } from "./revocation-policy.mjs";
const result = verifyLicenseWithFreshRevocations({
  certificate,
  trustedPublicKeys,
  expected,                   // independently established scope and hashes
  revocationSnapshot,
  trustedRevocationPublicKeys,
  now: new Date()
});
if (!result.valid) throw new Error(result.code);
~~~

## Production blockers

1. Snapshot replay is possible until expiry. A 24-hour maximum validity is
   NOT instant revocation. Add monotonic epochs and anti-rollback persistent
   state or fresh signed server responses before customer activation.
2. Production must use a hardened trusted clock/time source.
3. A signed maxInstances field is NOT enforcement. Add atomic server-side
   customer-scoped instance leases/heartbeats with expiry and bounded concurrency.
4. A hash is not legal clearance. Verify origin, chain of title, accepted
   commercial agreement, approval authenticity and external payment evidence.
5. The commercial private signing key must stay inside an approved Vault/KMS,
   with rotation, independent access controls, Audit Ledger events, Owner Kill
   Switch, recovery and secrets incident procedures.
6. GitHub Rulesets, private repositories, model/dataset rights and an
   independently reviewed SBOM remain separate acceptance gates.
7. Do not equate GitHub Actions PASS with an operating license server.

## Architectural integration

Architect → HANTER Command Center → federated orchestrators → Nano Core
Agents. Guardian Core policy, AI Passport identity and Approval Gateway
authorization are mandatory before any issuing action. Independent QA and
Audit Ledger must produce inspectable evidence. CONSTRUCTOR AI enforces
product-side entitlement checks. VELION MAX is only one VELION runtime mode.

Keep the Public/Private Boundary and CRYPTO IMPERIAL Ecosystem Boundary.
IMPERIUM is conceived as a long-term digital currency for AI agents
worldwide; global deployment or adoption is NOT established.

## Test command

~~~sh
node --test tools/cryptographic-license/index.test.mjs tools/cryptographic-license/revocation-policy.test.mjs
~~~

Tests use only ephemeral in-memory Ed25519 keys and standard Node.js modules.
**Commercial issuance remains DISABLED.**
