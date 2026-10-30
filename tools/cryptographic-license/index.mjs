/**
 * SPDX-License-Identifier: MIT
 * Original component: IMPERIAL Core cryptographic license verifier v1.
 * Project founder: Alexander Nikolaevich Romaskevich (RomaskevicH)
 * Native name: Ромаскевич Александр Николаевич
 *
 * IMPORTANT: a valid Ed25519 signature binds machine-readable claims only.
 * It cannot establish IP title, payment, customer acceptance, Owner approval
 * authenticity, or the enforceability of a separate commercial agreement.
 */
import { createPrivateKey, createPublicKey, sign, verify } from "node:crypto";

export const SCHEMA = "imperial.license.ed25519.v1";
export const ISSUER = "Alexander Nikolaevich Romaskevich (RomaskevicH)";
const FIELDS = Object.freeze([
  "schema", "issuer", "licenseId", "keyId", "productId", "customerId",
  "artifactSha256", "contractSha256", "approvalSha256", "rights",
  "notBefore", "expiresAt", "maxInstances"
]);
const RIGHTS = new Set(["BACKUP", "RUN", "TEST", "USE"]);
const ID = /^[A-Za-z0-9._:-]{8,100}$/;
const SHA = /^[a-f0-9]{64}$/;
const B64 = /^[A-Za-z0-9+/]+={0,2}$/;
const UTC = /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$/;
const DAY = 86_400_000;
const requireValid = (ok, code) => { if (!ok) throw new Error(code); };

export function canonicalPayload(payload) {
  requireValid(payload && typeof payload === "object" &&
    !Array.isArray(payload) && Object.keys(payload).length === FIELDS.length &&
    FIELDS.every(k => Object.hasOwn(payload, k)), "LICENSE_SCHEMA_DENIED");
  requireValid(payload.schema === SCHEMA && payload.issuer === ISSUER,
    "LICENSE_ISSUER_OR_VERSION_DENIED");
  requireValid(["licenseId", "keyId", "productId", "customerId"]
    .every(k => typeof payload[k] === "string" && ID.test(payload[k])),
    "LICENSE_IDENTIFIERS_DENIED");
  requireValid(["artifactSha256", "contractSha256", "approvalSha256"]
    .every(k => typeof payload[k] === "string" && SHA.test(payload[k])),
    "LICENSE_SHA256_DENIED");
  requireValid(Array.isArray(payload.rights) && payload.rights.length > 0 &&
    payload.rights.length <= RIGHTS.size &&
    payload.rights.every((r, i) => RIGHTS.has(r) &&
      (i === 0 || payload.rights[i - 1] < r)),
    "LICENSE_RIGHTS_DENIED");
  requireValid(Number.isSafeInteger(payload.maxInstances) &&
    payload.maxInstances >= 1 && payload.maxInstances <= 1000,
    "LICENSE_INSTANCE_LIMIT_DENIED");
  requireValid(["notBefore", "expiresAt"].every(k =>
    typeof payload[k] === "string" && UTC.test(payload[k]) &&
    Number.isFinite(Date.parse(payload[k])) &&
    new Date(payload[k]).toISOString() === payload[k]),
    "LICENSE_TIME_FORMAT_DENIED");
  const start = Date.parse(payload.notBefore);
  const end = Date.parse(payload.expiresAt);
  requireValid(end > start && end - start <= 366 * DAY,
    "LICENSE_DURATION_DENIED");
  return JSON.stringify(Object.fromEntries(FIELDS.slice().sort()
    .map(k => [k, payload[k]])));
}

export function issueLicense({ payload, privateKeyPem }) {
  const canonical = canonicalPayload(payload);
  requireValid(typeof privateKeyPem === "string" && privateKeyPem.length > 0,
    "PRIVATE_SIGNING_KEY_REQUIRED");
  const key = createPrivateKey(privateKeyPem);
  requireValid(key.asymmetricKeyType === "ed25519", "ED25519_ONLY");
  const signature = sign(null, Buffer.from(canonical, "utf8"), key)
    .toString("base64");
  return { payload: JSON.parse(canonical), signature };
}

/**
 * Offline verification. The trusted public keys MUST be pinned by the caller,
 * outside the attacker-supplied certificate. Never trust embedded key material.
 *
 * expected MUST contain productId, customerId, artifactSha256,
 * contractSha256, approvalSha256 and right; callers separately enforce
 * approval authenticity, payment status, revocation freshness and instance
 * concurrency. No network calls, writes, billing or external actions.
 */
export function verifyLicense({
  certificate, trustedPublicKeys, expected, now = new Date(),
  revokedLicenseIds = [], revokedKeyIds = []
} = {}) {
  try {
    requireValid(certificate && typeof certificate === "object" &&
      !Array.isArray(certificate) &&
      Object.keys(certificate).length === 2 &&
      Object.hasOwn(certificate, "payload") &&
      Object.hasOwn(certificate, "signature"), "ENVELOPE_DENIED");
    const canonical = canonicalPayload(certificate.payload);
    const p = certificate.payload;
    requireValid(typeof certificate.signature === "string" &&
      certificate.signature.length === 88 && B64.test(certificate.signature) &&
      Buffer.from(certificate.signature, "base64")
        .toString("base64") === certificate.signature, "SIGNATURE_FORMAT_DENIED");
    requireValid(trustedPublicKeys && typeof trustedPublicKeys === "object" &&
      !Array.isArray(trustedPublicKeys) &&
      Object.hasOwn(trustedPublicKeys, p.keyId),
      "UNKNOWN_SIGNER_DENIED");
    const pem = trustedPublicKeys[p.keyId];
    requireValid(typeof pem === "string" && pem.length > 0,
      "UNTRUSTED_KEY_DENIED");
    const key = createPublicKey(pem);
    requireValid(key.asymmetricKeyType === "ed25519", "ED25519_ONLY");
    requireValid(verify(null, Buffer.from(canonical, "utf8"), key,
      Buffer.from(certificate.signature, "base64")), "BAD_SIGNATURE_DENIED");
    requireValid(now instanceof Date && Number.isFinite(now.getTime()),
      "INVALID_CLOCK_DENIED");
    requireValid(now.getTime() >= Date.parse(p.notBefore) &&
      now.getTime() < Date.parse(p.expiresAt), "EXPIRED_OR_NOT_YET_VALID_DENIED");
    requireValid(Array.isArray(revokedLicenseIds) &&
      Array.isArray(revokedKeyIds) &&
      !revokedLicenseIds.includes(p.licenseId) &&
      !revokedKeyIds.includes(p.keyId), "REVOKED_DENIED");
    requireValid(expected && typeof expected === "object" &&
      ["productId", "customerId", "artifactSha256",
        "contractSha256", "approvalSha256", "right"].every(k =>
        typeof expected[k] === "string" && expected[k].length > 0),
      "EXPECTED_SCOPE_REQUIRED");
    requireValid(["productId", "customerId", "artifactSha256",
      "contractSha256", "approvalSha256"].every(k => p[k] === expected[k]) &&
      RIGHTS.has(expected.right) && p.rights.includes(expected.right),
      "LICENSE_SCOPE_DENIED");
    return Object.freeze({
      valid: true, code: "SIGNATURE_AND_SCOPE_VERIFIED_NOT_LEGAL_CLEARANCE",
      licenseId: p.licenseId, maxInstances: p.maxInstances,
      expiresAt: p.expiresAt
    });
  } catch (error) {
    return Object.freeze({ valid: false,
      code: error instanceof Error ? error.message : "LICENSE_DENIED" });
  }
}
