# Independent technical review — founder profile

## What you can reproduce without credentials or payments

- **Source:** [CONSTRUCTOR AI](https://github.com/oromaskevic23-cmd/CONSTRUCTOR-AI) is a Node 22+ repository containing a working offline Task Manager and separate plan-only, mocked AI gateway contracts.
- **Commands:** `npm run verify`, then `npm start`; inspect the local app on `http://127.0.0.1:4173`.
- **Live metadata review:** [Public Proof Verification PR #4](https://github.com/oromaskevic23-cmd/IMPERIAL-Core-Public/pull/4) proposes a zero-dependency Python tool verifying the recorded PR SHA, GitHub Actions job and workflow status for four projects. Use the *review branch* until merged: `python3 tools/verify_milestones.py --live`.
- **Direct evidence:** [Dated register](https://github.com/oromaskevic23-cmd/IMPERIAL-Core-Public/blob/main/docs/EVIDENCE.md), with immutable source revision, PR, CI job links and limitations.

## What we do not assert

A task app running locally is not a production app-building system. Offline or mocked inference tests are not live model inference. CI metadata cannot prove cloud uptime, customers, settled revenue, comprehensive security or external certifications. Proof verifier rechecks PR/run/job metadata, not the contents or hashes of historical CI logs.

**Security:** never submit credentials to a public issue, demo, clone or review branch. Zero Trust, Fail Closed, evidence-first. No paid software required.
