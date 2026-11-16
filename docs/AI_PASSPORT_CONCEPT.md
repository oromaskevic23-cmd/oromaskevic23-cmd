# AI Passport — Identity and Credential Concept

**Status:** design concept, 16 November 2026. The accompanying artwork is illustrative; it is not an issued credential or evidence of a deployed passport service.

## Purpose

AI Passport is a proposed identity and credential layer for Nano Core Agents and other authorized agents in the Federated Multi-Orchestrator Architecture. A human or system should be able to identify an agent, understand its specialty, and verify the origin and current status of a credential. **Identity is not authority.** A valid passport alone does not allow an agent to access data, approve a transaction or perform an operation.

## Two views

| Public view | Authorized internal view |
| --- | --- |
| Agent display name, non-sensitive identifier, specialty and issuer. | Agent identity binding, tenant/domain, permitted capabilities and their limits. |
| Credential version and a verification reference where appropriate. | Policy decisions, consent, approval records, revocation details and relevant audit links. |
| Optional work-quality information only when measured with a published method and sample. | Evidence needed to review a particular operation, subject to least-privilege access. |

The name, ID, QR code, 98.7% score and statuses in the example artwork are fictional. The image's QR code is not presented as a working verifier. A score must include its measurement period, denominator, methodology and limitations; absent verified data, the score is **not measured**.

## Proposed lifecycle and checks

1. An authorized issuer binds a unique agent identifier to a credential and an independently managed verification key. The credential states its scope, version and validity period.
2. A verifier checks the issuer, digital signature, validity period, intended audience and current revocation status against trusted records. Unavailable or stale required status fails closed.
3. Guardian Core evaluates the requested operation against current policy and context. Enterprise Skills describe capabilities; capability is not permission.
4. Approval Gateway requires a separate approval where policy calls for one. Authorization is scoped to the operation and must be checked at execution time.
5. Audit Ledger records the decision and evidence reference without exposing secrets or unnecessary personal information. The Owner can revoke or stop according to the applicable control design.

These are requirements for a future implementation, not a statement that the components are currently integrated. Key enrollment, rotation, revocation, privacy, replay protection, availability and independent security testing require separate design and evidence.

## Boundaries

- A public card is a presentation layer, not a secret, access token or proof of authorization.
- The Public/Private Boundary prevents disclosure of private agent configuration, private keys and sensitive operational details.
- The CRYPTO IMPERIAL Ecosystem Boundary remains separate; an AI Passport does not confer wallet access or payment authority.
- VELION is the intelligence core; HANTER is the AI Command Center. Federation retains bounded domain orchestrators, professional teams and a dynamic number of agents.

## Acceptance before a live claim

Demonstrate issuance and independent verification with trusted keys; expired, revoked, modified and replayed credentials must be rejected. Exercise least-privilege operation checks, approvals and audit continuity with meaningful negative tests. Document the public and internal data fields, threat model and unresolved limitations. Obtain independent security review before calling the service production-ready.
