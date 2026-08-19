# Architecture decisions

The machine-readable register is canonical: [`../data/decisions.json`](../data/decisions.json).

## D01 — Product identity and boundary

**Status:** accepted  
**Recommendation:** Build a governed geospatial knowledge and action platform with four separable planes. MCP is one interface, not the product identity.  
**Confidence:** high  
**Changes if:** A narrowly scoped internal-only server could justify a smaller product boundary

## D02 — Six-control governance spine

**Status:** accepted  
**Recommendation:** Use the six-control spine as the primary governance view and map it to presentation, control, execution/data and evidence planes.  
**Confidence:** high  
**Changes if:** A mandated enterprise reference architecture may require renamed planes

## D03 — Role of OKF

**Status:** accepted  
**Recommendation:** Use OKF 0.2 as the canonical knowledge, discovery, provenance and policy-description layer. Do not make it the runtime authority, policy decision point or evidence store.  
**Confidence:** high  
**Changes if:** A future normative OKF revision could change core fields or packaging

## D04 — MCP primitive mapping

**Status:** accepted  
**Recommendation:** Use resources for catalogue/schema/licence/style/evidence descriptions; tools for deterministic actions; Tasks for long jobs; Apps for optional UI; Arazzo for durable workflows.  
**Confidence:** high  
**Changes if:** Host interoperability tests may require compatibility shims

## D05 — Tool surface

**Status:** accepted  
**Recommendation:** Expose 12 composable, schema-rich tools instead of the 103-tool MCP-Geo catalogue. Keep provider selection behind policy-aware adapters.  
**Confidence:** high  
**Changes if:** Evaluation may show a small number of provider-specific tools are safer

## D06 — MCP protocol and SDK target

**Status:** accepted  
**Recommendation:** Target MCP 2026-07-28 and the official TypeScript SDK at a pinned release/commit. Keep protocol conformance tests against official fixtures and major hosts.  
**Confidence:** high  
**Changes if:** A critical host lacks final-protocol support and cannot be upgraded

## D07 — WebMCP adoption level

**Status:** accepted  
**Recommendation:** Run a bounded, open-data, read-only WebMCP experiment in the static HMLR/Explorer site. Do not expose privileged operations, credentials or policy decisions through it.  
**Confidence:** high  
**Changes if:** W3C standards-track status, stable browser support and resolved security model could justify wider adoption

## D08 — MCP Apps approach

**Status:** accepted  
**Recommendation:** Use MCP Apps for optional map, inspector, provenance and approval views. Every capability must return a complete deterministic non-UI result and use the same policy/evidence path.  
**Confidence:** high  
**Changes if:** Host support remains too limited to justify maintenance

## D09 — Authentication and delegated authority

**Status:** accepted  
**Recommendation:** Use OIDC/OAuth 2.1, authorisation code with PKCE for humans, workload identity for services, token exchange/on-behalf-of where supported, and short-lived transaction-bound permits for sensitive actions.  
**Confidence:** high  
**Changes if:** Enterprise identity constraints mandate a different federation pattern

## D10 — ABAC and policy engine

**Status:** accepted  
**Recommendation:** Use Open Policy Agent/Rego as the principal portable PDP, with policy information from trusted identity, entitlement, licence, provider and risk services. Keep relationship data available as input rather than adopting a separate ReBAC engine initially.  
**Confidence:** medium-high  
**Changes if:** AWS becomes the mandated platform with Verified Permissions already operated; Relationship-heavy entitlements dominate

## D11 — Trusted device posture

**Status:** accepted  
**Recommendation:** Use Entra Conditional Access and Intune-compliance claims as trusted posture evidence for the first protected pilot. Never accept posture asserted directly by the MCP client.  
**Confidence:** high  
**Changes if:** Pilot identity estate is not Entra/Intune

## D12 — Access and cache isolation

**Status:** accepted  
**Recommendation:** Operate open, PSGA and commercial data planes as physically separate deployments/stores/caches/keys/identities. Share source code, schemas and reviewed policy definitions only.  
**Confidence:** high  
**Changes if:** A formal risk assessment proves logical separation sufficient for a narrowly bounded dataset

## D13 — Canonical geospatial storage and formats

**Status:** accepted  
**Recommendation:** Use PostGIS for authoritative/queryable vector state and indexes; object storage for GeoParquet, PMTiles, COG and downloadable artefacts; DuckDB Spatial for isolated embedded analytics; GeoJSON only for bounded results.  
**Confidence:** high  
**Changes if:** The MVP remains metadata-only and needs no spatial database

## D14 — Live API versus cache strategy

**Status:** accepted  
**Recommendation:** Prefer live provider APIs for volatile, transactional or legally authoritative results; use governed versioned caches for reference geographies, approved open bulk data, performance-critical tiles and outage resilience.  
**Confidence:** high  
**Changes if:** Provider terms prohibit caching or provide guaranteed low-latency services

## D15 — Open demonstrator hosting

**Status:** accepted  
**Recommendation:** Publish the research pack and Stage 1 open demonstrator as a static, portable site, initially compatible with GitHub Pages or Cloudflare Pages. Treat ChatGPT Sites as an optional open/synthetic mirror only after UK account availability is verified.  
**Confidence:** high  
**Changes if:** A mandated publishing platform provides equivalent portability and accessibility

## D16 — Protected production hosting

**Status:** accepted  
**Recommendation:** Use Azure UK for the first protected pilot: Container Apps/App Service, Azure Database for PostgreSQL/PostGIS, Blob Storage, Entra ID/Conditional Access, managed identities, Key Vault, API Management and Monitor. Keep contracts portable to GCP and AWS.  
**Confidence:** medium-high  
**Changes if:** Departmental landing zone mandates GCP or AWS; Protected pilot lacks Entra integration

## D17 — Language and runtime

**Status:** accepted  
**Recommendation:** Use a TypeScript MCP/control gateway and a Python deterministic geospatial execution service. Keep it to these two deployable services initially.  
**Confidence:** medium-high  
**Changes if:** Official Python SDK closes all control-plane gaps and a single-service implementation passes the same assurance

## D18 — Repository reset and migration

**Status:** accepted  
**Recommendation:** Create a new repository for Locus Accord only after this decision phase. Archive MCP-Geo as a learning journal. Migrate selected assets through a tested harvest, never by copying the repository wholesale.  
**Confidence:** high  
**Changes if:** Organisational policy requires continuity in the existing repository

## D19 — Minimum viable scope

**Status:** accepted  
**Recommendation:** Stage 0 creates evidence, schemas and test harness; Stage 1 publishes an HMLR/ONS/LandIS open discovery pack; Stage 2 adds a small open read-only MCP service. Identity, PSGA and commercial work follow only after evidence gates.  
**Confidence:** high  
**Changes if:** A funded protected pilot supplies its identity, licence and governance prerequisites from day one

## D20 — Working project name

**Status:** accepted-working-codename  
**Recommendation:** Use Locus Accord (`locus-accord`) as the working codename. It expresses place plus an explicit agreement between authority, policy, data and action. Do not claim legal clearance.  
**Confidence:** medium  
**Changes if:** UKIPO/package/domain checks identify a conflict; Stakeholder research rejects the name
