// Static evidence-index regression tests. Zero network calls and no paid CI.
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { validateIndex } from "../tools/verify_public_evidence.mjs";

const index = JSON.parse(readFileSync(new URL("../docs/EVIDENCE_INDEX.json",import.meta.url),"utf8"));
const clone = ()=>structuredClone(index);
test("public index validates under strict scope",()=>{
  const status=validateIndex(index);
  assert.equal(status.checked_records,8);
  assert.equal(status.verified_external_runs,4);
});
test("duplicate claims rejected",()=>{const m=clone();m.records[1].id=m.records[0].id;assert.throws(()=>validateIndex(m),/duplicate/);});
test("outside-domain proof rejected",()=>{const m=clone();m.records[0].source="https://invalid.example/fake";assert.throws(()=>validateIndex(m),/source/);});
test("unproven production denied",()=>{const m=clone();m.records[0].production=true;assert.throws(()=>validateIndex(m),/unsubstantiated/);});
test("unproven independent review denied",()=>{const m=clone();m.records[0].independent=true;assert.throws(()=>validateIndex(m),/unsubstantiated/);});
test("CI evidence must link an actual run route",()=>{const m=clone();m.records[0].source="https://github.com/oromaskevic23-cmd/CONSTRUCTOR-AI";assert.throws(()=>validateIndex(m),/CI source/);});
test("missing limitation rejected",()=>{const m=clone();m.records[0].limitation="no";assert.throws(()=>validateIndex(m),/meaningful limitation/);});
