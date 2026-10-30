import { test } from "node:test";
import assert from "node:assert/strict";
import { generateKeyPairSync } from "node:crypto";
import { canonicalRevocations, signRevocationSnapshot, verifyRevocationSnapshot,
  verifyLicenseWithFreshRevocations, verifyLicenseWithAtomicCheckpoint, REVOCATION_SCHEMA } from "./revocation-policy.mjs";
import { issueLicense, SCHEMA, ISSUER } from "./index.mjs";

const lic = generateKeyPairSync("ed25519");
const rev = generateKeyPairSync("ed25519");
const rogue = generateKeyPairSync("ed25519");
const pub = pair => pair.publicKey.export({ format: "pem", type: "spki" }).toString();
const priv = pair => pair.privateKey.export({ format: "pem", type: "pkcs8" }).toString();
const h = value => value.repeat(64);
const now = new Date("2026-10-30T19:00:00.000Z");
const snapshotPayload = () => ({ schema: REVOCATION_SCHEMA, keyId: "REVOCATION-KEY-001",
  sequence: 1, issuedAt: "2026-10-30T18:00:00.000Z", expiresAt: "2026-10-31T18:00:00.000Z",
  revokedLicenseIds: [], revokedKeyIds: [] });
const snapshot = (payload = snapshotPayload(), pair = rev) =>
  signRevocationSnapshot({ payload, privateKeyPem: priv(pair) });
const verifySnapshot = (s, opts = {}) => verifyRevocationSnapshot({
  snapshot: s, trustedPublicKeys: { "REVOCATION-KEY-001": pub(rev) }, now, ...opts
});
const claim = () => ({ schema: SCHEMA, issuer: ISSUER,
  licenseId: "TEST-LICENSE-001", keyId: "LICENSE-KEY-001", productId: "CONSTRUCTOR-AI",
  customerId: "TEST-CUSTOMER-001", artifactSha256: h("a"),
  contractSha256: h("b"), approvalSha256: h("c"), rights: ["RUN"],
  notBefore: "2026-10-30T18:00:00.000Z", expiresAt: "2026-10-31T18:00:00.000Z",
  maxInstances: 1 });
const expected = () => ({ productId: "CONSTRUCTOR-AI", customerId: "TEST-CUSTOMER-001",
  artifactSha256: h("a"), contractSha256: h("b"), approvalSha256: h("c"), right: "RUN" });
const check = (revocationSnapshot = snapshot(), options = {}) =>
  verifyLicenseWithFreshRevocations({
    certificate: issueLicense({ payload: claim(), privateKeyPem: priv(lic) }),
    trustedPublicKeys: { "LICENSE-KEY-001": pub(lic) }, expected: expected(),
    revocationSnapshot, trustedRevocationPublicKeys: { "REVOCATION-KEY-001": pub(rev) },
    now, ...options
  });

test("fresh independently signed revocation data allows a scoped test certificate", () => {
  const r = check(); assert.equal(r.valid, true); assert.equal(r.revocationValidUntil,
    "2026-10-31T18:00:00.000Z");
});
test("no revocation snapshot, no trust registry, and an invalid clock fail closed", () => {
  assert.equal(check(undefined, { revocationSnapshot: null }).valid, false);
  assert.equal(check(snapshot(), { trustedRevocationPublicKeys: {} }).valid, false);
  assert.equal(verifySnapshot(snapshot(), { now: new Date(NaN) }).valid, false);
});
test("expired and future dated snapshots are both denied", () => {
  assert.equal(verifySnapshot(snapshot(), { now: new Date("2026-11-01T00:00:00.000Z") }).valid, false);
  assert.equal(verifySnapshot(snapshot(), { now: new Date("2026-10-29T00:00:00.000Z") }).valid, false);
});
test("tampered signed revocation list is denied", () => {
  const s = snapshot(); s.payload.revokedLicenseIds.push("TEST-LICENSE-001");
  assert.equal(verifySnapshot(s).valid, false);
});
test("untrusted alternate Ed25519 signer is denied", () => {
  assert.equal(verifySnapshot(snapshot(snapshotPayload(), rogue)).valid, false);
});
test("signed license and signer revocation both block authorization", () => {
  const p = snapshotPayload(); p.revokedLicenseIds = ["TEST-LICENSE-001"];
  assert.equal(check(snapshot(p)).valid, false);
  p.revokedLicenseIds = []; p.revokedKeyIds = ["LICENSE-KEY-001"];
  assert.equal(check(snapshot(p)).valid, false);
});
test("replay cannot exceed a 24-hour signed validity window", () => {
  const p = snapshotPayload(); p.expiresAt = "2026-11-01T18:00:00.000Z";
  assert.throws(() => canonicalRevocations(p), /REVOCATION_VALIDITY_DENIED/);
});
test("duplicate, unordered or malformed revocation IDs are denied", () => {
  for (const ids of [["TEST-LICENSE-001", "TEST-LICENSE-001"],
    ["ZZZZZZZZ", "AAAAAAAA"], ["bad id"]]) {
    assert.throws(() => canonicalRevocations({ ...snapshotPayload(), revokedLicenseIds: ids }),
      /REVOCATION_IDS_DENIED/);
  }
});
test("unknown schema, extra envelope keys, and embedded keys are denied", () => {
  assert.throws(() => canonicalRevocations({ ...snapshotPayload(), schema: "v2" }),
    /REVOCATION_ISSUER_DENIED/);
  assert.equal(verifySnapshot({ ...snapshot(), publicKey: pub(rev) }).valid, false);
});
test("invalid customer scope cannot be repaired by a signed revocation snapshot", () => {
  assert.equal(check(snapshot(), { expected: { ...expected(), customerId: "OTHER-CUSTOMER" } }).valid, false);
});

const checkpointStore = (initial = { sequence: 0, digest: "0".repeat(64) }) => {
  let current = { ...initial };
  return {
    async get() { return { ...current }; },
    async compareAndSwap({ expected: prev, next }) {
      if (current.sequence !== prev.sequence || current.digest !== prev.digest) return false;
      current = { ...next };
      return true;
    },
    getState() { return { ...current }; }
  };
};
const verifyAtomic = (store, revocationSnapshot = snapshot(), opts = {}) =>
  verifyLicenseWithAtomicCheckpoint({
    certificate: issueLicense({ payload: claim(), privateKeyPem: priv(lic) }),
    trustedPublicKeys: { "LICENSE-KEY-001": pub(lic) },
    expected: expected(), revocationSnapshot,
    trustedRevocationPublicKeys: { "REVOCATION-KEY-001": pub(rev) },
    checkpointStore: store, now, ...opts
  });

test("strict API requires trusted durable checkpoint adapter", async () => {
  assert.equal((await verifyAtomic(undefined)).valid, false);
  assert.equal((await verifyAtomic({ get: async () => null })).valid, false);
});
test("strict API atomically commits and permits identical snapshot", async () => {
  const store = checkpointStore();
  const signed = snapshot();
  assert.equal((await verifyAtomic(store, signed)).valid, true);
  assert.equal(store.getState().sequence, 1);
  assert.equal((await verifyAtomic(store, signed)).valid, true);
});
test("older signed sequence denied even if timestamp interval still valid", async () => {
  const store = checkpointStore();
  const newer = snapshot({ ...snapshotPayload(), sequence: 2 });
  assert.equal((await verifyAtomic(store, newer)).valid, true);
  const old = await verifyAtomic(store, snapshot());
  assert.equal(old.valid, false);
  assert.equal(old.code, "REVOCATION_ROLLBACK_DENIED");
});
test("same signed sequence with different authentic snapshot is a fork", async () => {
  const store = checkpointStore();
  assert.equal((await verifyAtomic(store, snapshot())).valid, true);
  const altered = snapshot({ ...snapshotPayload(),
    revokedLicenseIds: ["OTHER-TEST-LICENSE"] });
  const r = await verifyAtomic(store, altered);
  assert.equal(r.valid, false);
  assert.equal(r.code, "REVOCATION_FORK_DENIED");
});
test("atomic checkpoint conflict denies stale concurrent requests", async () => {
  const store = checkpointStore();
  let changed = false;
  const race = {
    get: () => store.get(),
    async compareAndSwap(args) {
      if (!changed) {
        changed = true;
        const higher = snapshot({ ...snapshotPayload(), sequence: 9 });
        const fromNewer = await verifyAtomic(store, higher);
        assert.equal(fromNewer.valid, true);
      }
      return store.compareAndSwap(args);
    }
  };
  const r = await verifyAtomic(race, snapshot());
  assert.equal(r.valid, false);
  assert.equal(r.code, "TRUSTED_CHECKPOINT_CAS_DENIED");
});
test("invalid persisted checkpoint denies without bootstrap defaults", async () => {
  assert.equal((await verifyAtomic(checkpointStore({ sequence: 0, digest: "a".repeat(64) }))).valid, false);
  assert.equal((await verifyAtomic(checkpointStore({ sequence: -1, digest: "a".repeat(64) }))).valid, false);
});
test("untrusted signer cannot advance persistent checkpoint", async () => {
  const store = checkpointStore();
  assert.equal((await verifyAtomic(store, snapshot(snapshotPayload(), rogue))).valid, false);
  assert.equal(store.getState().sequence, 0);
});
test("revoked license cannot advance persistent checkpoint", async () => {
  const store = checkpointStore();
  const p = { ...snapshotPayload(), revokedLicenseIds: ["TEST-LICENSE-001"] };
  assert.equal((await verifyAtomic(store, snapshot(p))).valid, false);
  assert.equal(store.getState().sequence, 0);
});
test("sequence must be a signed strictly positive safe integer", () => {
  for (const sequence of [0, -1, 1.1, Number.MAX_SAFE_INTEGER + 1, "1"]) {
    assert.throws(() => canonicalRevocations({ ...snapshotPayload(), sequence }),
      /REVOCATION_SEQUENCE_DENIED/);
  }
});
