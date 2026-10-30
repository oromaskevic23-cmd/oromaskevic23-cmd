# IMPERIAL Core — cryptographically verifiable product licenses

**Reference implementation:** `index.mjs` and `index.test.mjs`.  
**SPDX code license:** `MIT` (full unmodified text in this directory's [LICENSE](LICENSE)).  
**Project founder / original architecture authority:** Alexander Nikolaevich Romaskevich (RomaskevicH).  
**Native name:** recorded in the source-code header; GitHub documentation remains English only.  
**Runtime status:** verified offline test implementation; **NOT a deployed production HANTER Vault license signer**.

## Different licenses serve different purposes

1. **Ordinary legal source license:** the repository root [LICENSE](../../LICENSE) reserves proprietary rights in original IMPERIAL Core material unless a narrower license applies. It is **not** an OSI open-source license. Existing GitHub Terms of Service, third-party terms and contributor rights prevail where applicable.
2. **Standard GitHub-recognized open-source license:** the *isolated reference code in this directory only* is under the standard **MIT** license. GitHub detects repository-level badges from root LICENSE; **the overall profile repo must not be incorrectly advertised as MIT**.
3. **Cryptographic customer license certificate:** JSON claims digitally signed with Ed25519. A valid certificate proves it was signed by a key trusted by the verifier and that bound scope/time/artifact data were not modified; **it does not by itself prove who legally owns all IP, customer payment or Owner authorization**.

## Certificate contract

The canonical signer binds: `schema`, `issuer`, `licenseId`, `keyId`, `productId`, `customerId`, `artifactSha256`, `contractSha256`, `approvalSha256`, sorted rights (`BACKUP, RUN, TEST, USE`), ISO-8601 UTC validity window (max 366 days), and `maxInstances` (1..1000).

The public certificate contains only `{ "payload": {...}, "signature": "<base64>" }`. Never put public/private keys into the certificate payload or trust user-supplied cert keys. Verifiers require a **separately pinned** Ed25519 public-key registry.

## External mandatory authorization gates

- Verify the Owner-controlled approval reference against **Approval Gateway/Audit Ledger**, not just a 64-character hash.
- Confirm a legally approved **signed customer contract** and legitimate rights holder for the artifact. A hash without a verified source is not approval.
- Compare the licensed `artifactSha256` against a locally calculated SHA-256 of the **exact binary or software bundle** being executed; do not reuse a declared hash as its own evidence.
- Match customer ID, contract digest, approval digest, requested right, product, key ID, `maxInstances` and current UTC time. Enforce runtime instance count separately.
- Read a **fresh authenticated** license/key revocation list and implement rotation; an offline stale list cannot guarantee non-revocation.
- Do not issue production certificates with ephemeral CI keys. The signer private key belongs in an approved **HANTER secure Vault/KMS**, never a GitHub repository, Actions log, browser, chat, client application or LICENSE file.
- A cryptographic entitlement does not autonomously initiate purchases, crypto transfers, CUSTOMER_ACCEPTED or PAYMENT_CONFIRMED.
- Preserves Guardian Core, Zero Trust, AI Passport, Enterprise Skills, ProofGraph and Public/Private Boundary.

## Quick test

```shell
node --test tools/cryptographic-license/index.test.mjs
```

Only built-in Node.js `node:crypto` and `node:test`, no network, payments, secrets or dependencies. The test suite creates **ephemeral test Ed25519 keys in-memory** and covers tampering, unknown keys, expiry, revocations, prohibited permissions, foreign customers and missing Owner/contract bindings. A passing test does not issue a real customer license.

The standard MIT text is legally applicable **only to these first-party reference implementation files**; it does not grant MIT rights to VELION, HANTER, CONSTRUCTOR AI, licensed model weights, graphics, private data or the complete IMPERIAL Core ecosystem.

**Enterprise standard:** [Licensing and release gates](../../docs/IMPERIAL_ENTERPRISE_LICENSING_STANDARD.md).  
**Customer agreement:** [Commercial license draft](../../docs/COMMERCIAL_SOFTWARE_LICENSE_TERM_SHEET_DRAFT.md).

**Production certificate issuance:** NOT ENABLED; requires explicit Owner approval, KMS/Vault and independently verified legal/operational prerequisites.
