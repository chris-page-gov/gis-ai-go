# Identity, policy and licensing: authority is a chain, not a token

> **Evidence notation.** Bracketed identifiers such as `[S-MCP-SPEC]` resolve through [`data/sources.json`](../data/sources.json). **Verified fact**, **assumption**, **recommendation** and **unresolved question** are deliberately separated. Retrieval date: **19 August 2026**.


## Actor chain

Preserve:

**human → AI host → agent → MCP client → gateway → geospatial execution → upstream provider**

Each link has an identifier, issuer, version, delegation/purpose, trace context and expiry where applicable. A provider client-credentials token proves the platform project to the provider; the platform’s policy decision proves whether this human/agent action is permitted. [S-OS-AUTH] [S-TOKEN-EXCHANGE]

## Authentication model

- human sessions: OIDC/OAuth authorisation code with PKCE and enterprise federation;
- service/cache refresh: managed identity or workload identity federation;
- on-behalf-of/token exchange: used where the enterprise identity provider supports a bounded audience and delegation;
- sensitive calls: audience-restricted short-lived transaction permits, optionally sender-constrained with DPoP or mTLS;
- revocation/introspection: checked according to risk and provider capability;
- enterprise-managed authorisation: tested per MCP host and identity environment, not assumed. [S-OAUTH-BCP] [S-TOKEN-EXCHANGE] [S-RAR] [S-DPOP] [S-MCP-EMA]

## Authority context

The canonical schema is [`schemas/authority-context.schema.json`](../schemas/authority-context.schema.json). It includes actor, subject, organisation, roles, agent, AI host, client, workload, trusted device posture, action, resource/dataset attributes, purpose, legal authority, licence entitlement, geography/resolution constraints, risk, output, quota, evidence, policy version, approval, decision, obligations, expiry and trace ID.

The synthetic example deliberately contains no real person, credential or licensed data: [`data/examples/authority-context.example.json`](../data/examples/authority-context.example.json).

## Device posture

**Recommendation.** For the first protected pilot, Entra Conditional Access and Intune supply compliance/posture evidence. The gateway verifies issuer, audience, observed time and validity. A posture change invalidates or re-evaluates permits and running workflows at material boundaries. A `device_compliant=true` value sent by a client is never sufficient. [S-ENTRA-CA] [S-INTUNE]

## Policy architecture

- **PAP:** version-controlled policy repository with owner, review, tests, approval and rollback;
- **PIPs:** identity, device, organisation entitlement, licence/contract, provider status, dataset classification, risk, cost/quota and workflow state;
- **PDP:** OPA/Rego, returning allow/deny and obligations;
- **PEPs:** search, capability listing, workflow controller, gateway, credential broker, cache, query engine, map/tile, export and evidence access;
- **decision cache:** short-lived and keyed by material authority/resource/policy attributes; never a general allow cache.

The engine-neutral decision schema is [`schemas/policy-decision.schema.json`](../schemas/policy-decision.schema.json).

## ABAC dimensions

| Dimension | Examples |
| --- | --- |
| Subject/actor | organisation, membership, role, accreditation, clearance, contract, user/agent/application identity |
| Device/environment | managed/compliant posture, authentication strength, network/location, time, risk |
| Resource | provider, dataset, record/field/feature, licence tier, classification, personal data, geography, resolution, version, freshness, cost |
| Action | discover, view, query, intersect, join, route, export, cache, redistribute, derive, publish |
| Context/purpose | declared purpose, legal authority, project, emergency, intended audience, destination, aggregate/record-level use |

## Licence and policy are obligations, not labels

A policy allow may require attribution, aggregate-only output, masking, maximum features, reduced resolution, watermarking, no persistent export, human approval, rate/cost limits, retention or a managed destination. PEPs must prove each obligation was applied before the result is released.

**Unresolved question.** The precise PSGA/commercial cache, derivation and redistribution conditions must be confirmed from the selected product agreements before implementation. This research pack contains no licensed data.
