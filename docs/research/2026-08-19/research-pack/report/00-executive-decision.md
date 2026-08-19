# Executive decision: start Locus Accord as a new governed platform

> **Evidence notation.** Bracketed identifiers such as `[S-MCP-SPEC]` resolve through [`data/sources.json`](../data/sources.json). **Verified fact**, **assumption**, **recommendation** and **unresolved question** are deliberately separated. Retrieval date: **19 August 2026**.


## Recommendation

**Recommendation.** Start a new repository, using **Locus Accord** (`locus-accord`) as a working codename, for a governed geospatial knowledge and action platform. Do not rewrite MCP-Geo in place. Keep MCP-Geo at commit `56683b33c0cd02842b7f3ee465414c68a1f3f2a6` as an archived learning journal and migrate only tested assets through the forensic harvest. [S-MCP-GEO]

The coherent default architecture is:

1. a **portable public presentation plane**: OKF 0.2 knowledge bundle, static Explorer, MapLibre-compatible map specifications, accessible data cards and an optional open, read-only WebMCP experiment;
2. a **TypeScript control plane**: MCP 2026-07-28 gateway, OIDC/OAuth, policy-filtered discovery, Open Policy Agent, explicit workflows, short-lived transaction permits and server-side upstream credential brokerage;
3. a **Python execution and data plane**: deterministic geospatial/statistical operations, provider adapters, PostGIS, object storage and physically separated open, PSGA and commercial caches; and
4. an **evidence plane**: Trace Context/OpenTelemetry, append-only audit, versioned policy decisions and result-level evidence receipts. [S-MCP-SPEC] [S-OKF-SPEC] [S-OPA] [S-PROV] [S-TRACE]

## Why this is the decision

**Verified fact.** MCP-Geo is a broad research prototype with a 103-tool surface, a FastAPI-centred implementation and explicit caveats that it is not production code. It contains valuable tests, failure cases, map fallbacks, geography semantics and OWASP artefacts, but it is not the right production skeleton. [S-MCP-GEO]

**Verified fact.** MCP 2026-07-28 is now the final baseline. It supports the stateless, routable and self-describing model that MCP-Geo had tracked as a release candidate. The successor should use the final specification and official SDK rather than preserve a default target of 2025-11-25. [S-MCP-SPEC] [S-MCP-RELEASE]

**Verified fact.** OKF 0.2 makes provenance, trust, lifecycle and attestation first-class while remaining a portable Markdown/YAML knowledge format. It should carry discovery and descriptive governance, not pretend to be the runtime policy decision point or provider system of record. [S-OKF-SPEC]

**Recommendation.** Physical separation of open, PSGA and commercial stores, caches, keys, identities and deployments is proportionate. Licence tier, security classification, personal-data status, query sensitivity and commercial entitlement remain separate policy dimensions.

## Build now / prepare next / defer

| Horizon | Scope | Evidence gate |
| --- | --- | --- |
| **Build now** | Stage 0 evidence foundation; Stage 1 static open discovery pack; public HMLR worked example; OKF bundle; safe linked JSON; optional read-only WebMCP experiment. | All artefacts public/synthetic, schemas valid, source ledger complete, WCAG 2.2 AA acceptance. |
| **Prepare next** | Stage 2 open read-only MCP service; 12-tool capability surface; ONS/Nomis/LandIS/HMLR open adapters; deterministic maps and receipts. | MCP host interoperability, provider conformance, threat tests and result reproducibility. |
| **Defer** | PSGA credential brokerage, protected OS cache, commercial entitlement, mutating/transactional HMLR operations, national scale and federated operators. | Identity, device posture, licences/contracts, DPIA, ATRS, isolated protected hosting and formal assurance. |

## First 30 days

- **Days 1–5:** approve the 20 decisions; clear the Stage 0 scope; create the new repository only after approval; add governance files, source ledger, schemas and architecture decision records.
- **Days 6–10:** implement the OKF 0.2 research/domain profile and deterministic static build; import only the public HMLR metadata example; validate every source and rights field.
- **Days 11–15:** build search, facets, graph, timeline, map and evidence-card journeys; add non-JavaScript fallbacks and WCAG tests.
- **Days 16–20:** scaffold the TypeScript MCP gateway and Python execution boundary with synthetic fixtures; implement `catalogue.search`, `catalogue.describe` and `evidence.inspect` first.
- **Days 21–25:** implement authority-context, policy-decision and evidence-receipt contracts; add OPA policy tests with synthetic open/PSGA/commercial identities.
- **Days 26–30:** run the 25-case evaluation, host interoperability tests and a threat-model review; issue a go/no-go decision for Stage 2.

## Top ten risks

| Risk | Why it matters | Primary control |
| --- | --- | --- |
| RK01 Prompt injection through metadata | high | treat content as data, schema-bound tools, content isolation |
| RK02 Tool poisoning | high | signed/pinned manifests, reviewed registry, schema hashes |
| RK03 Confused deputy | critical | authority context, OPA, transaction permits |
| RK04 Agent identity substitution | high | signed tokens, client metadata verification, mTLS/DPoP where justified |
| RK05 Token theft or replay | critical | short lifetimes, DPoP/mTLS for sensitive calls, secret isolation |
| RK06 Overbroad scopes | high | least privilege, resource indicators, transaction permits |
| RK07 False device posture | high | trusted Entra/Intune attestation, freshness limits |
| RK08 Policy bypass | critical | central PEP library, deny-by-default, architecture tests |
| RK09 Provider credential misuse | critical | brokered credentials, managed identity, egress controls |
| RK10 SSRF/arbitrary URL fetch | high | no arbitrary fetch tool, allowlisted providers, egress proxy |

## Working name

**Recommendation.** Use **Locus Accord** as the working codename: *locus* identifies place; *accord* makes authority, policy, data, workflow and evidence an explicit agreement. It does not bind the product to MCP or imply endorsement by OS, ONS, HMLR, Defra or government.

**Unresolved question.** Formal package, domain, UKIPO and wider product-name clearance has not been completed. The name is reversible until public launch.

## Exact first artefact for Codex

Give Codex [`codex/CODEX_HANDOFF.md`](../codex/CODEX_HANDOFF.md) first. It constrains Codex to **Stage 0 only**, points to the accepted decisions and schemas, prohibits modification of MCP-Geo and requires verification pauses. It should be accompanied by this whole pack so Codex can follow the linked evidence rather than repeat the research.
