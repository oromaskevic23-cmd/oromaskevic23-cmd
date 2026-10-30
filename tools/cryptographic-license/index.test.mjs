import { test } from "node:test";
import assert from "node:assert/strict";
import { generateKeyPairSync } from "node:crypto";
import { canonicalPayload, issueLicense, verifyLicense, SCHEMA, ISSUER } from "./index.mjs";

const OWNER = generateKeyPairSync("ed25519");
const ROGUE = generateKeyPairSync("ed25519");
const RSA = generateKeyPairSync("rsa", { modulusLength: 2048 });
const pem = k => k.export({ format: "pem", type: "spki" }).toString();
const secret = k => k.export({ format: "pem", type: "pkcs8" }).toString();
const h = "a".repeat(64), contract = "b".repeat(64), approval = "c".repeat(64);
const payload = () => ({
  schema: SCHEMA, issuer: ISSUER, licenseId: "IC-LICENSE-TEST-0001",
  keyId: "OWNER-VAULT-KEY-001", productId: "CONSTRUCTOR-AI",
  customerId: "TEST-CUSTOMER-NOT-REAL", artifactSha256: h,
  contractSha256: contract, approvalSha256: approval,
  rights: ["BACKUP", "RUN"], notBefore: "2026-10-30T18:00:00.000Z",
  expiresAt: "2026-10-31T18:00:00.000Z", maxInstances: 1
});
const trust = { "OWNER-VAULT-KEY-001": pem(OWNER.publicKey) };
const expected = () => ({
  productId: "CONSTRUCTOR-AI", customerId: "TEST-CUSTOMER-NOT-REAL",
  artifactSha256: h, contractSha256: contract,
  approvalSha256: approval, right: "RUN"
});
const now = new Date("2026-10-30T19:00:00.000Z");
const cert = () => issueLicense({ payload: payload(),
  privateKeyPem: secret(OWNER.privateKey) });
const verify = (c, changes = {}) => verifyLicense({
  certificate: c, trustedPublicKeys: trust, expected: expected(), now, ...changes
});
test("valid test certificate verifies only signature/scope, not legal authority", () => {
  const result = verify(cert());
  assert.equal(result.valid, true);
  assert.equal(result.code, "SIGNATURE_AND_SCOPE_VERIFIED_NOT_LEGAL_CLEARANCE");
  assert.equal(result.maxInstances, 1);
});
test("deterministic canonical payload excludes object insertion-order ambiguity", () => {
  const p = payload();
  assert.equal(canonicalPayload(p), canonicalPayload(Object.fromEntries(
    Object.entries(p).reverse())));
});
test("tampered artifact hash cannot be accepted", () => {
  const c = cert(); c.payload.artifactSha256 = "f".repeat(64);
  assert.equal(verify(c).valid, false);
});
test("tampered rights cannot be accepted", () => {
  const c = cert(); c.payload.rights = ["BACKUP", "RUN", "USE"];
  assert.equal(verify(c).valid, false);
});
test("rogue self-signed certificate rejected by external trust pin", () => {
  const fake = issueLicense({ payload: payload(),
    privateKeyPem: secret(ROGUE.privateKey) });
  assert.equal(verify(fake).valid, false);
});
test("unknown key-id fails closed, even with good Ed25519 signature", () => {
  const p = payload(); p.keyId = "ROGUE-KEY-0000001";
  const fake = issueLicense({ payload: p,
    privateKeyPem: secret(OWNER.privateKey) });
  assert.equal(verify(fake).valid, false);
});
test("expired or not-yet-valid certificate rejected", () => {
  const c = cert();
  assert.equal(verify(c, { now: new Date("2026-11-01T00:00:00.000Z") }).valid, false);
  assert.equal(verify(c, { now: new Date("2026-10-29T00:00:00.000Z") }).valid, false);
});
test("revoked certificate and revoked signer rejected", () => {
  assert.equal(verify(cert(), { revokedLicenseIds: ["IC-LICENSE-TEST-0001"] }).valid, false);
  assert.equal(verify(cert(), { revokedKeyIds: ["OWNER-VAULT-KEY-001"] }).valid, false);
});
test("product, customer, artifact, contract, approval and requested right must match", () => {
  for (const [k, value] of [
    ["productId", "VELION"], ["customerId", "SOMEONE-ELSE"],
    ["artifactSha256", "f".repeat(64)], ["contractSha256", "f".repeat(64)],
    ["approvalSha256", "f".repeat(64)], ["right", "USE"]
  ]) {
    assert.equal(verify(cert(), { expected: { ...expected(), [k]: value } }).valid, false, k);
  }
});
test("missing expected approval hash and missing external trust both fail closed", () => {
  const e = expected(); delete e.approvalSha256;
  assert.equal(verify(cert(), { expected: e }).valid, false);
  assert.equal(verify(cert(), { trustedPublicKeys: {} }).valid, false);
});
test("extra envelope keys or payload fields are denied", () => {
  assert.equal(verify({ ...cert(), publicKey: pem(OWNER.publicKey) }).valid, false);
  assert.equal(verify({ ...cert(), payload: { ...payload(), magic: "ALLOW" } }).valid, false);
});
test("out-of-order or duplicate permissions are denied", () => {
  for (const rights of [["RUN", "BACKUP"], ["RUN", "RUN"], ["PAYMENT_CONFIRMED"]]) {
    assert.throws(() => canonicalPayload({ ...payload(), rights }), /LICENSE_RIGHTS_DENIED/);
  }
});
test("non-Ed25519 signatures denied", () => {
  assert.throws(() => issueLicense({ payload: payload(),
    privateKeyPem: secret(RSA.privateKey) }), /ED25519_ONLY/);
});
test("invalid maximum instance count, time range or unknown claims denied", () => {
  assert.throws(() => canonicalPayload({ ...payload(), maxInstances: 0 }), /LICENSE_INSTANCE_LIMIT_DENIED/);
  assert.throws(() => canonicalPayload({ ...payload(), expiresAt: "2030-11-01T00:00:00.000Z" }), /LICENSE_DURATION_DENIED/);
  assert.throws(() => canonicalPayload({ ...payload(), issuer: "ROGUE" }), /LICENSE_ISSUER_OR_VERSION_DENIED/);
});
test("malformed signature encoding denied", () => {
  const c = cert(); c.signature = "ignored";
  assert.equal(verify(c).valid, false);
});
