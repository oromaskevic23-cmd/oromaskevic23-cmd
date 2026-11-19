// Public evidence-index validator. Node.js 22+; standard library only.
// Does NOT verify GitHub Actions outcomes, third-party independence or live deployment.
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export function validateIndex(m){
 const fail=(s)=>{throw new Error(s)};
 if(!m||typeof m!=="object"||Array.isArray(m))fail("manifest must be object");
 if(m.schema_version!=="1.0"||m.project!=="IMPERIAL Core"||m.public_architecture!=="Federated Multi-Orchestrator Architecture")fail("unexpected identity/schema");
 if(!/^\d{4}-\d\d-\d\d$/.test(m.as_of)||typeof m.description!=="string"||m.description.length<30)fail("as_of or description invalid");
 for(const k of ["unified_production_runtime_verified","independent_certification_verified","championship_submission_verified"]){if(typeof m[k]!=="boolean")fail(k+" must be boolean");}
 if(!Array.isArray(m.records)||m.records.length<5)fail("missing evidence records");
 const seen=new Set(),types=new Set(["github_actions_job_success","documented_local_reference","public_developer_report","architecture_target"]);
 for(const x of m.records){
  for(const k of ["id","component","evidence_class","source","claim","scope","limitation"]){if(typeof x?.[k]!=="string"||x[k].trim().length<3)fail("incomplete "+k);}
  if(!/^[a-z0-9-]+$/.test(x.id)||seen.has(x.id))fail("invalid or duplicate record id");
  seen.add(x.id);
  if(!types.has(x.evidence_class))fail("invalid evidence class");
  if(!x.source.startsWith("https://github.com/oromaskevic23-cmd/")||/[\s?#]/.test(x.source))fail("nonpublic or non-GitHub source");
  if(x.evidence_class==="github_actions_job_success"&&!/\/actions\/runs\/\d+$/.test(x.source))fail("CI source must be a run");
  if(typeof x.independent!=="boolean"||typeof x.production!=="boolean")fail("independent/production must be explicit");
  if(x.independent||x.production)fail("unsubstantiated independent or production assertion");
  if(x.limitation.length<18)fail("missing meaningful limitation");
 }
 return {valid:true,checked_records:m.records.length,unique_ids:seen.size,verified_external_runs:m.records.filter(x=>x.evidence_class==="github_actions_job_success").length,scope:"static index validation only: does not query external links or rerun tests"};
}

const isMain = process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  try {
    const path = resolve(dirname(fileURLToPath(import.meta.url)), "../docs/EVIDENCE_INDEX.json");
    const manifest = JSON.parse(readFileSync(path,"utf8"));
    process.stdout.write(JSON.stringify(validateIndex(manifest), null, 2) + "\n");
  } catch (err) {
    process.stderr.write("EVIDENCE_INDEX_FAIL: " + err.message + "\n");
    process.exitCode = 1;
  }
}
