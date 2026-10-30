#!/usr/bin/env node
/**
 * SPDX-License-Identifier: MIT
 * IMPERIAL Core: offline, read-only validation of an Ed25519 customer license.
 * No API calls, payments, key issuance, approval renewal or secret access.
 *
 * Usage:
 *   node tools/cryptographic-license/verify-cli.mjs CERT.json TRUSTED-KEYS.json EXPECTED.json REVOKED.json
 * Exit 0: signed technical entitlement matched; NOT legal or payment approval.
 * Exit 2: denied, missing/incomplete inputs, invalid certificate or revocation.
 */
import { readFileSync } from "node:fs";
import { verifyLicense } from "./index.mjs";

function readJson(name) {
  if (typeof name !== "string" || name.length === 0)
    throw new Error("REQUIRED_INPUT_FILE_MISSING");
  const content = readFileSync(name);
  if (content.length === 0 || content.length > 1048576)
    throw new Error("UNSAFE_INPUT_SIZE_DENIED");
  return JSON.parse(content.toString("utf8"));
}

try {
  if (process.argv.length !== 6)
    throw new Error("FOUR_EXPLICIT_INPUT_FILES_REQUIRED");
  const [cert, keys, expected, revocations] = process.argv.slice(2).map(readJson);
  if (!revocations || typeof revocations !== "object" ||
      !Array.isArray(revocations.revokedLicenseIds) ||
      !Array.isArray(revocations.revokedKeyIds))
    throw new Error("EXPLICIT_REVOCATION_STATE_REQUIRED");
  const result = verifyLicense({
    certificate: cert, trustedPublicKeys: keys, expected,
    revokedLicenseIds: revocations.revokedLicenseIds,
    revokedKeyIds: revocations.revokedKeyIds, now: new Date()
  });
  if (!result.valid) throw new Error(result.code);
  console.log("TECHNICAL_LICENSE_VERIFIED_NOT_LEGAL_CLEARANCE");
} catch (error) {
  console.error("TECHNICAL_LICENSE_DENIED: " +
    (error instanceof Error ? error.message : "UNKNOWN_ERROR"));
  process.exitCode = 2;
}
