---
type: Index
title: Decisions
description: Index of decisions in the research pack.
generated:
  by: process:research-pack-builder
  at: '2026-08-19T13:30:00+01:00'
---

# Decisions

- [D01: Product identity and boundary](d01.md) — Build a governed geospatial knowledge and action platform with four separable planes. MCP is one interface, not the product identity.
- [D02: Six-control governance spine](d02.md) — Use the six-control spine as the primary governance view and map it to presentation, control, execution/data and evidence planes.
- [D03: Role of OKF](d03.md) — Use OKF 0.2 as the canonical knowledge, discovery, provenance and policy-description layer. Do not make it the runtime authority, policy decision point or evidence store.
- [D04: MCP primitive mapping](d04.md) — Use resources for catalogue/schema/licence/style/evidence descriptions; tools for deterministic actions; Tasks for long jobs; Apps for optional UI; Arazzo for durable workflows.
- [D05: Tool surface](d05.md) — Expose 12 composable, schema-rich tools instead of the 103-tool MCP-Geo catalogue. Keep provider selection behind policy-aware adapters.
- [D06: MCP protocol and SDK target](d06.md) — Target MCP 2026-07-28 and the official TypeScript SDK at a pinned release/commit. Keep protocol conformance tests against official fixtures and major hosts.
- [D07: WebMCP adoption level](d07.md) — Run a bounded, open-data, read-only WebMCP experiment in the static HMLR/Explorer site. Do not expose privileged operations, credentials or policy decisions through it.
- [D08: MCP Apps approach](d08.md) — Use MCP Apps for optional map, inspector, provenance and approval views. Every capability must return a complete deterministic non-UI result and use the same policy/evidence path.
- [D09: Authentication and delegated authority](d09.md) — Use OIDC/OAuth 2.1, authorisation code with PKCE for humans, workload identity for services, token exchange/on-behalf-of where supported, and short-lived transaction-bound permits for sensitive actions.
- [D10: ABAC and policy engine](d10.md) — Use Open Policy Agent/Rego as the principal portable PDP, with policy information from trusted identity, entitlement, licence, provider and risk services. Keep relationship data available as input rather than adopting a separate ReBAC engine initially.
- [D11: Trusted device posture](d11.md) — Use Entra Conditional Access and Intune-compliance claims as trusted posture evidence for the first protected pilot. Never accept posture asserted directly by the MCP client.
- [D12: Access and cache isolation](d12.md) — Operate open, PSGA and commercial data planes as physically separate deployments/stores/caches/keys/identities. Share source code, schemas and reviewed policy definitions only.
- [D13: Canonical geospatial storage and formats](d13.md) — Use PostGIS for authoritative/queryable vector state and indexes; object storage for GeoParquet, PMTiles, COG and downloadable artefacts; DuckDB Spatial for isolated embedded analytics; GeoJSON only for bounded results.
- [D14: Live API versus cache strategy](d14.md) — Prefer live provider APIs for volatile, transactional or legally authoritative results; use governed versioned caches for reference geographies, approved open bulk data, performance-critical tiles and outage resilience.
- [D15: Open demonstrator hosting](d15.md) — Publish the research pack and Stage 1 open demonstrator as a static, portable site, initially compatible with GitHub Pages or Cloudflare Pages. Treat ChatGPT Sites as an optional open/synthetic mirror only after UK account availability is verified.
- [D16: Protected production hosting](d16.md) — Use Azure UK for the first protected pilot: Container Apps/App Service, Azure Database for PostgreSQL/PostGIS, Blob Storage, Entra ID/Conditional Access, managed identities, Key Vault, API Management and Monitor. Keep contracts portable to GCP and AWS.
- [D17: Language and runtime](d17.md) — Use a TypeScript MCP/control gateway and a Python deterministic geospatial execution service. Keep it to these two deployable services initially.
- [D18: Repository reset and migration](d18.md) — Create a new repository for Locus Accord only after this decision phase. Archive MCP-Geo as a learning journal. Migrate selected assets through a tested harvest, never by copying the repository wholesale.
- [D19: Minimum viable scope](d19.md) — Stage 0 creates evidence, schemas and test harness; Stage 1 publishes an HMLR/ONS/LandIS open discovery pack; Stage 2 adds a small open read-only MCP service. Identity, PSGA and commercial work follow only after evidence gates.
- [D20: Working project name](d20.md) — Use Locus Accord (`locus-accord`) as the working codename. It expresses place plus an explicit agreement between authority, policy, data and action. Do not claim legal clearance.
