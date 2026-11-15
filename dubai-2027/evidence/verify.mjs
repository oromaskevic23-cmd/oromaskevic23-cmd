// Public evidence integrity verifier; no competition implementation or private data.
export const EXPECTED_FINGERPRINT = 'fbbd13d5389b8d8748ca9c0252b7690917ff825e1bcf56d5553e379ec79da080';
const REQUIRED_LIMITS = [
  'No independent QA', 'No live LLM evaluation', 'No browser end-to-end acceptance',
  'No measured client savings', 'No production deployment or contest acceptance claimed'
];
const SCHEMA = 'imperial-dubai-public-checkpoint-v1';
function require(condition, message) { if (!condition) throw new Error(message); }
function exactKeys(obj, keys) {
  return obj !== null && typeof obj === 'object' && !Array.isArray(obj) &&
    Object.keys(obj).length === keys.length && keys.every(k => Object.hasOwn(obj,k));
}
function decode64(text) {
  const s = text.trim();
  require(/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(s) && s.length > 0, 'Invalid base64');
  const bin = atob(s);
  require(btoa(bin) === s, 'Noncanonical base64');
  return Uint8Array.from(bin, c => c.charCodeAt(0));
}
function hex(bytes) { return Array.from(new Uint8Array(bytes), x => x.toString(16).padStart(2,'0')).join(''); }
function count(n) { return Number.isSafeInteger(n) && n >= 0; }
function checks(item, additional = []) {
  require(exactKeys(item,['passed','total',...additional]) && count(item.passed) && count(item.total) && item.total > 0 && item.passed <= item.total, 'Invalid test counts');
}
export function validateCheckpoint(p) {
  require(exactKeys(p,['schema','date','scope','signer','python','javascript_ui_state','ed25519_proof_tests','showcase_assertions','synthetic_benchmark','private_sample_signature_verified','limits']), 'Unexpected checkpoint fields');
  require(p.schema === SCHEMA && p.date === '2026-11-15' && p.scope === 'DEVELOPER_RUN_LOCAL_SYNTHETIC' && p.signer === 'EPHEMERAL_DEMO_KEY_NOT_VERIFIED_OWNER_IDENTITY', 'Unexpected checkpoint scope');
  checks(p.python,['seconds']); checks(p.javascript_ui_state); checks(p.ed25519_proof_tests,['included_in_python']); checks(p.showcase_assertions,['separate_run']);
  require(Number.isFinite(p.python.seconds) && p.python.seconds > 0, 'Invalid test duration');
  require(p.ed25519_proof_tests.included_in_python === true && p.ed25519_proof_tests.total <= p.python.total && p.ed25519_proof_tests.passed <= p.python.passed, 'Cryptographic subset mismatch');
  require(p.showcase_assertions.separate_run === true, 'Showcase scope missing');
  const b = p.synthetic_benchmark;
  require(exactKeys(b,['cases','review_cases','false_matches','real_payments']) && Object.values(b).every(count) && b.cases > 0 && b.review_cases <= b.cases && b.false_matches <= b.cases && b.real_payments === 0, 'Invalid synthetic benchmark');
  require(p.private_sample_signature_verified === true, 'Private sample verification claim missing');
  require(Array.isArray(p.limits) && p.limits.length === REQUIRED_LIMITS.length && REQUIRED_LIMITS.every(x => p.limits.includes(x)), 'Required claim limitations missing');
  return p;
}
export async function verifyCheckpoint(checkpointBytes, signatureText, keyText, subtle = globalThis.crypto?.subtle) {
  require(subtle, 'WebCrypto unavailable');
  require(checkpointBytes instanceof Uint8Array && checkpointBytes.length > 0 && checkpointBytes.length <= 16384, 'Invalid checkpoint size');
  require(typeof signatureText === 'string' && signatureText.length <= 256 && typeof keyText === 'string' && keyText.length <= 512, 'Invalid key or signature input');
  const pem = keyText.trim().match(/^-----BEGIN PUBLIC KEY-----\r?\n([A-Za-z0-9+/=\r\n]+)\r?\n-----END PUBLIC KEY-----$/);
  require(pem, 'Invalid public key PEM');
  const der = decode64(pem[1].replace(/\r?\n/g,''));
  require(der.length === 44 && hex(der.slice(0,12)) === '302a300506032b6570032100', 'Ed25519 key required');
  const fingerprint = hex(await subtle.digest('SHA-256', der));
  require(fingerprint === EXPECTED_FINGERPRINT, 'Unexpected demonstration key fingerprint');
  const sig = decode64(signatureText);
  require(sig.length === 64, 'Invalid Ed25519 signature length');
  const key = await subtle.importKey('spki', der, {name:'Ed25519'}, false, ['verify']);
  require(await subtle.verify({name:'Ed25519'}, key, sig, checkpointBytes), 'Signature verification failed');
  const data = validateCheckpoint(JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(checkpointBytes)));
  return {verified:true,fingerprint,checkpoint:data,meaning:'Integrity of the published summary only; not independent QA, signer identity or proof of real-world execution.'};
}
