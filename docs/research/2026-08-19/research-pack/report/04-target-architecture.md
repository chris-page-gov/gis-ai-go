# Target architecture: one governance spine, four deployable planes

> **Evidence notation.** Bracketed identifiers such as `[S-MCP-SPEC]` resolve through [`data/sources.json`](../data/sources.json). **Verified fact**, **assumption**, **recommendation** and **unresolved question** are deliberately separated. Retrieval date: **19 August 2026**.


## Product boundary

Locus Accord is a **governed geospatial knowledge and action platform**. It comprises a public knowledge/discovery site, an MCP/control gateway, deterministic geospatial execution and an evidence service. It is not:

- a replacement for OS, ONS, Nomis, LandIS or HMLR systems of record;
- a general-purpose arbitrary URL or code execution service;
- a licence reseller;
- a repository of browser-supplied API keys;
- an autonomous authority for legal, planning, ownership or safety-critical decisions;
- a promise that every provider and data tier shares one deployment.

## Six-control governance spine

| Control | Purpose | Principal components | Deployable plane |
| --- | --- | --- | --- |
| C1 Domain knowledge and semantics | Make concepts, identifiers, relationships, metadata, temporal meaning, provenance, uncertainty and fitness for purpose explicit. | OKF 0.2 bundle<br>domain profiles<br>identifier registry<br>source-native metadata<br>catalogue crosswalks | presentation<br>control |
| C2 Authority, identity and policy | Authenticate actors and workloads, preserve delegated authority, evaluate licence and purpose, and attach obligations. | OIDC/OAuth 2.1<br>Entra Conditional Access<br>OPA<br>authority context<br>transaction permits | control |
| C3 Durable workflow and human control | Make multi-step processes deterministic, resumable, reviewable and reversible rather than relying on an LLM plan. | Arazzo 1.1<br>MCP Tasks<br>MRTR<br>approval service<br>state store | control<br>evidence |
| C4 MCP, APIs and events | Provide policy-filtered discovery, invocation, routing, service contracts and event integration. | MCP 2026-07-28<br>OpenAPI<br>OGC APIs<br>AsyncAPI<br>MCP Apps<br>WebMCP experiment | presentation<br>control |
| C5 Authoritative systems, data and computation | Keep source systems authoritative and perform deterministic geospatial and statistical operations in tested software. | provider adapters<br>PostGIS<br>object storage<br>Python geospatial execution<br>isolated caches | execution-data |
| C6 Evidence, audit and assurance | Record requests, policy decisions, approvals, data versions, transformations, outputs, receipts and operational assurance. | OpenTelemetry<br>Trace Context<br>W3C PROV mapping<br>append-only audit<br>result receipt<br>transparency record | evidence |

The controls describe the route from intent to accountable action. The planes describe what can be deployed, isolated and operated. Identity, security, privacy, licensing, lifecycle, accessibility and incident control cross all six controls.

## Deployable systems view

| Plane | Contains | Trust boundary |
| --- | --- | --- |
| Presentation plane | static OKF Explorer<br>MapLibre map<br>evidence cards<br>MCP Apps<br>optional WebMCP read-only tools | No protected credentials or licensed feature payloads in public browser assets. |
| Control plane | TypeScript MCP gateway<br>identity broker<br>OPA PDP<br>workflow controller<br>rate/cost controls<br>credential selection | Every discover and invoke decision requires trusted identity and policy context. |
| Execution and data plane | Python deterministic geospatial service<br>PostGIS<br>object stores<br>provider adapters<br>tier-isolated caches | Provider credentials and licensed data stay server-side and tier-isolated. |
| Evidence plane | trace store<br>append-only audit events<br>policy decision records<br>evidence receipts<br>evaluation and incident records | Evidence is immutable enough for challenge and reconstructability; logs exclude secrets and unnecessary personal query content. |

See the portable diagrams:

- [`context.svg`](../assets/diagrams/context.svg)
- [`containers.svg`](../assets/diagrams/containers.svg)
- [`six-control-spine.svg`](../assets/diagrams/six-control-spine.svg)
- [`evidence-flow.svg`](../assets/diagrams/evidence-flow.svg)

## Open tier request

1. A user or agent searches the static OKF pack.
2. Optional open MCP requests carry an anonymous/public authority context.
3. Policy filters records/tools and attaches attribution, rate and feature-count obligations.
4. Deterministic execution queries a public source or approved open cache.
5. A result envelope and receipt name source versions, transformations and rights.

## Protected request

1. The AI host passes a delegated user token and verifiable client metadata.
2. The gateway validates the human, organisation, host/client, workload and current enterprise device posture.
3. OPA evaluates action, resource, purpose, legal authority, entitlement, geography, resolution, output, risk, cost and destination.
4. A sensitive operation receives a short-lived transaction permit; approval is obtained where required.
5. The credential broker selects a provider workload credential. The provider token never becomes user authority and never reaches the browser.
6. Execution occurs in the protected plane; maps, exports and caches enforce returned obligations.
7. Evidence links actor chain, decision, provider call, source version, transformation and output.

## Human-led and agentic processes

Both tracks use the same policy, systems and evidence spine. In the human-led track, a person selects data and invokes deterministic operations. In the agentic track, an agent proposes the same action under a named delegation. The agent does not gain authority because it can discover or call a tool. Approval, permit, resource and purpose remain explicit.

## Deployment isolation

Share source code, API/schema contracts, OKF profiles, policy templates and conformance tests. Separate open, PSGA and commercial:

- runtime deployments and network policies;
- databases, object stores and cache namespaces;
- encryption keys and service identities;
- provider credentials and quotas;
- audit access and retention;
- release manifests and emergency suspension.

This costs more than a single shared service but reduces the highest-impact leakage and licence risks.
