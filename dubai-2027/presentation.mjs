import {verifyCheckpoint} from './evidence/verify.mjs';
const button=document.getElementById('verify-evidence');
const status=document.getElementById('verify-status');
button.addEventListener('click',async()=>{
  button.disabled=true;status.textContent='Checking signed checkpoint…';
  try{
    const files=['checkpoint.json','checkpoint.sig.b64','public-key.pem'];
    const responses=await Promise.all(files.map(name=>fetch(new URL('./evidence/'+name,location.href),{cache:'no-store',credentials:'omit'})));
    if(responses.some(r=>!r.ok))throw new Error('Public evidence file unavailable');
    const [data,sig,key]=await Promise.all([responses[0].arrayBuffer(),responses[1].text(),responses[2].text()]);
    const result=await verifyCheckpoint(new Uint8Array(data),sig,key);
    status.textContent='Signature valid · '+result.checkpoint.python.passed+'/'+result.checkpoint.python.total+' Python tests reported. '+result.meaning;
  }catch(error){status.textContent='Not verified: '+error.message+'. See the offline verification guide.';}
  finally{button.disabled=false;}
});
