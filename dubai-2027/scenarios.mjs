// Illustrative public walkthrough. Static examples only; not the agent or its policy.
const entries = {
  match: {title:'Matching invoice', input:'Invoice: AED 1,000 · purchase order: AED 1,000 · bank unchanged.', outcome:'MATCH RECOMMENDED', explanation:'A matching invoice may receive a recommendation. This does not authorize payment.', control:'Bounded recommendation', payment:'NONE'},
  exception: {title:'Invoice exception', input:'Invoice: AED 1,250 · purchase order: AED 1,000 · bank details changed.', outcome:'HUMAN REVIEW REQUIRED', explanation:'The illustrated exception is routed to an authorized reviewer. No payment is executed.', control:'Guardian Core / Approval Gateway — architectural concepts', payment:'NONE'},
  unauthorized: {title:'Unauthorized review', input:'A user without review authority attempts to record a decision.', outcome:'REQUEST DENIED', explanation:'Identity alone does not grant approval authority.', control:'AI Passport / Zero Trust — architectural concepts', payment:'NONE'},
  stopped: {title:'Owner emergency stop', input:'The owner has stopped the local prototype; a new submission is attempted.', outcome:'SUBMISSION BLOCKED', explanation:'The demonstrated local stop persists across restart. This is not a distributed availability claim.', control:'Owner Kill Switch', payment:'NONE'}
};
for(const entry of Object.values(entries))Object.freeze(entry);
export const SCENARIO_IDS=Object.freeze(Object.keys(entries));
export function scenarioFor(id){
  if(typeof id!=='string'||!Object.hasOwn(entries,id))throw new Error('Unknown illustrative scenario');
  return entries[id];
}
export function renderScenario(root,id){
  const s=scenarioFor(id);
  for(const [field,value] of Object.entries(s)){
    const target=root.querySelector('[data-scenario-field="'+field+'"]');
    if(!target)throw new Error('Missing scenario field: '+field);
    target.textContent=value;
  }
}
