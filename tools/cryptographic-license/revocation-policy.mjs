/**
 * SPDX-License-Identifier: MIT
 * IMPERIAL Core — independently pinned, time-bounded Ed25519 revocation evidence.
 * Original project architecture: Alexander Nikolaevich Romaskevich (RomaskevicH).
 * This is an offline reference implementation, not a production revocation service.
 */
import { createPrivateKey, createPublicKey, sign, verify } from "node:crypto";
import { verifyLicense } from "./index.mjs";

export const REVOCATION_SCHEMA = "imperial.revocations.ed25519.v1";
const FIELDS = Object.freeze([
  "schema", "keyId", "issuedAt", "expiresAt", "revokedLicenseIds", "revokedKeyIds"
]);
const MAX_VALIDITY_MS = 24 * 60 * 60 * 1000;
const ID = /^[A-Za-z0-9._:-]{8,100}$/;
const UTC = /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$/;
const B64 = /^[A-Za-z0-9+/]+={0,2}$/;
const requireValid = (condition, code) => {
  if (!condition) throw new Error(code);
};
const exactShape = (obj, fields) => obj !== null && typeof obj === "object" &&
  !Array.isArray(obj) && Object.keys(obj).length === fields.length &&
  fields.every(key => Object.hasOwn(obj, key));
const validTimestamp = value => typeof value === "string" && UTC.test(value) &&
  Number.isFinite(Date.parse(value)) && new Date(value).toISOString() === value;
const validIds = ids => Array.isArray(ids) && ids.length <= 10000 &&
  ids.every((v, i) => typeof v === "string" && ID.test(v) &&
    (i === 0 || ids[i - 1] < v));

export function canonicalRevocations(payload) {
  requireValid(exactShape(payload, FIELDS), "REVOCATION_SCHEMA_DENIED");
  requireValid(payload.schema === REVOCATION_SCHEMA &&
    typeof payload.keyId === "string" && ID.test(payload.keyId),
    "REVOCATION_ISSUER_DENIED");
  requireValid(validTimestamp(payload.issuedAt) && validTimestamp(payload.expiresAt),
    "REVOCATION_TIME_FORMAT_DENIED");
  const age = Date.parse(payload.expiresAt) - Date.parse(payload.issuedAt);
  requireValid(age > 0 && age <= MAX_VALIDITY_MS, "REVOCATION_VALIDITY_DENIED");
  requireValid(validIds(payload.revokedLicenseIds) && validIds(payload.revokedKeyIds),
    "REVOCATION_IDS_DENIED");
  return JSON.stringify(Object.fromEntries(FIELDS.slice().sort()
    .map(key => [key, payload[key]])));
}

// Only for isolated test/demo signers. Real private keys must stay in a KMS/Vault.
export function signRevocationSnapshot({ payload, privateKeyPem }) {
  const canonical = canonicalRevocations(payload);
  requireValid(typeof privateKeyPem === "string" && privateKeyPem.length > 0,
    "REVOCATION_SIGNER_REQUIRED");
  const key = createPrivateKey(privateKeyPem);
  requireValid(key.asymmetricKeyType === "ed25519", "ED25519_ONLY");
  return { payload: JSON.parse(canonical),
    signature: sign(null, Buffer.from(canonical, "utf8"), key).toString("base64") };
}

export function verifyRevocationSnapshot({ snapshot, trustedPublicKeys, now = new Date() } = {}) {
  try {
    requireValid(exactShape(snapshot, ["payload", "signature"]),
      "REVOCATION_ENVELOPE_DENIED");
    const canonical = canonicalRevocations(snapshot.payload);
    const p = snapshot.payload;
    requireValid(typeof snapshot.signature === "string" &&
      snapshot.signature.length === 88 && B64.test(snapshot.signature) &&
      Buffer.from(snapshot.signature, "base64").toString("base64") === snapshot.signature,
      "REVOCATION_SIGNATURE_FORMAT_DENIED");
    requireValid(trustedPublicKeys !== null && typeof trustedPublicKeys === "object" &&
      !Array.isArray(trustedPublicKeys) && Object.hasOwn(trustedPublicKeys, p.keyId),
      "REVOCATION_UNTRUSTED_SIGNER_DENIED");
    const pem = trustedPublicKeys[p.keyId];
    requireValid(typeof pem === "string" && pem.length > 0,
      "REVOCATION_UNTRUSTED_KEY_DENIED");
    const key = createPublicKey(pem);
    requireValid(key.asymmetricKeyType === "ed25519", "ED25519_ONLY");
    requireValid(verify(null, Buffer.from(canonical, "utf8"), key,
      Buffer.from(snapshot.signature, "base64")),
      "REVOCATION_BAD_SIGNATURE_DENIED");
    requireValid(now instanceof Date && Number.isFinite(now.getTime()),
      "REVOCATION_INVALID_CLOCK_DENIED");
    requireValid(now.getTime() >= Date.parse(p.issuedAt) &&
      now.getTime() < Date.parse(p.expiresAt),
      "REVOCATION_STALE_OR_FUTURE_DENIED");
    return Object.freeze({ valid: true, code: "FRESH_SIGNED_REVOCATIONS_VERIFIED",
      revokedLicenseIds: Object.freeze([...p.revokedLicenseIds]),
      revokedKeyIds: Object.freeze([...p.revokedKeyIds]),
      validUntil: p.expiresAt });
  } catch (error) {
    return Object.freeze({ valid: false,
      code: error instanceof Error ? error.message : "REVOCATION_DENIED" });
  }
}

// Fail closed unless a fresh, independently signed revocation snapshot verifies.
// Legal approval, external payment evidence, artifact digest and running instance
// enforcement are separate gates and are NEVER established by this function.
export function verifyLicenseWithFreshRevocations({
  certificate, trustedPublicKeys, expected, revocationSnapshot,
  trustedRevocationPublicKeys, now = new Date()
} = {}) {
  const revocations = verifyRevocationSnapshot({
    snapshot: revocationSnapshot, trustedPublicKeys: trustedRevocationPublicKeys, now
  });
  if (!revocations.valid) return Object.freeze({ valid: false, code: revocations.code });
  const license = verifyLicense({ certificate, trustedPublicKeys, expected, now,
    revokedLicenseIds: revocations.revokedLicenseIds,
    revokedKeyIds: revocations.revokedKeyIds });
  if (!license.valid) return license;
  return Object.freeze({ ...license,
    code: "SIGNATURE_SCOPE_AND_FRESH_REVOCATIONS_VERIFIED_NOT_LEGAL_CLEARANCE",
    revocationValidUntil: revocations.validUntil });
}
