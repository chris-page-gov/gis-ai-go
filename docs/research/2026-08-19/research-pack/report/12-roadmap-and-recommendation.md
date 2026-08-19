# Roadmap and recommendation: build evidence before protected capability

> **Evidence notation.** Bracketed identifiers such as `[S-MCP-SPEC]` resolve through [`data/sources.json`](../data/sources.json). **Verified fact**, **assumption**, **recommendation** and **unresolved question** are deliberately separated. Retrieval date: **19 August 2026**.


## Staged delivery

| Stage | Entry criteria | Deliverables | Exit tests | Rollback |
| --- | --- | --- | --- | --- |
| 0 — Repository and evidence foundation | 20 decisions approved; new-repository authority | Governance files, source ledger, schemas, ADRs, synthetic fixtures, CI/test harness | Schemas validate; links/sources resolve; threat and acceptance baselines approved | Delete unshared new repo or revert Stage 0 commit; MCP-Geo untouched |
| 1 — Open static discovery pack | Stage 0 passed; public HMLR source review | OKF bundle, static Explorer, HMLR worked example, linked JSON/JSON-LD, optional read-only WebMCP | Search/facets/graph/timeline/map/data-card/accessibility and exact-source checks | Republish previous immutable static artefact |
| 2 — Open MCP service | Stage 1 evidence; final-protocol host matrix | TypeScript gateway, Python execution, first open adapters, 12-tool registry subset, receipts | MCP conformance, malicious inputs, deterministic provider fixtures, non-App fallback | Disable server registry entry; static pack remains |
| 3 — Identity and policy | Enterprise test tenant; approved authority model | OIDC/OAuth, OPA, trusted actor chain, filtered discovery, permits, policy evidence | Synthetic open/PSGA/commercial tests and challenge reconstruction | Disable protected discovery and revert policy bundle |
| 4 — PSGA protected pilot | Current agreements; Entra/Intune; DPIA/security approval; isolated Azure landing zone | OS credential broker, protected cache, approval/export controls | No cross-tier leakage; device downgrade/deny; licence obligations; incident drills | Revoke provider credential, suspend tier, quarantine caches |
| 5 — Commercial/multi-organisation | Contracts, billing/quota and tenant model approved | Contract entitlements, cost controls, tenant isolation, federation | Contract-bound outputs and cross-tenant red-team tests | Disable tenant/tier and revoke artefacts |
| 6 — Production assurance | Pilot evidence and service ownership | DR, performance, red team, transparency, accessibility, operational controls | Service Standard/security/operational acceptance | Blue/green rollback and provider/tool suspension |

## Work-mode assessment

- **Deep Research:** best current capability for broad, current, cited evidence synthesis. It remains necessary for provider roadmaps, standards, licensing and public-sector requirements.
- **GitHub-connected analysis:** necessary for exact repository commits, files, history, issues, tests and forensic harvest.
- **Static research pack / optional ChatGPT Sites:** the pack is the canonical portable artefact. Sites may provide an optional open sharing surface if current UK availability and constraints are acceptable.
- **Codex:** receives the decision pack and implements one verified stage at a time; it should not repeat the architecture research or modify MCP-Geo.
- **Codex Security:** becomes useful once a new codebase or diff exists, first to validate the threat model and later for standard/deep scans and finding remediation.
- **Notebooks/dashboards:** use only for quantitative cost, performance, capacity and evaluation analysis where reproducibility benefits from executable calculations.

No newer single capability replaces Deep Research for this commission. The effective workflow is evidence synthesis → repository forensics → decision pack → Codex stage implementation → Codex Security/review → measured evaluation → next gate.

## Decision register

| ID | Decision | Status | Recommendation | Confidence |
| --- | --- | --- | --- | --- |
| D01 | Product identity and boundary | accepted | Build a governed geospatial knowledge and action platform with four separable planes. MCP is one interface, not the product identity. | high |
| D02 | Six-control governance spine | accepted | Use the six-control spine as the primary governance view and map it to presentation, control, execution/data and evidence planes. | high |
| D03 | Role of OKF | accepted | Use OKF 0.2 as the canonical knowledge, discovery, provenance and policy-description layer. Do not make it the runtime authority, policy decision point or evidence store. | high |
| D04 | MCP primitive mapping | accepted | Use resources for catalogue/schema/licence/style/evidence descriptions; tools for deterministic actions; Tasks for long jobs; Apps for optional UI; Arazzo for durable workflows. | high |
| D05 | Tool surface | accepted | Expose 12 composable, schema-rich tools instead of the 103-tool MCP-Geo catalogue. Keep provider selection behind policy-aware adapters. | high |
| D06 | MCP protocol and SDK target | accepted | Target MCP 2026-07-28 and the official TypeScript SDK at a pinned release/commit. Keep protocol conformance tests against official fixtures and major hosts. | high |
| D07 | WebMCP adoption level | accepted | Run a bounded, open-data, read-only WebMCP experiment in the static HMLR/Explorer site. Do not expose privileged operations, credentials or policy decisions through it. | high |
| D08 | MCP Apps approach | accepted | Use MCP Apps for optional map, inspector, provenance and approval views. Every capability must return a complete deterministic non-UI result and use the same policy/evidence path. | high |
| D09 | Authentication and delegated authority | accepted | Use OIDC/OAuth 2.1, authorisation code with PKCE for humans, workload identity for services, token exchange/on-behalf-of where supported, and short-lived transaction-bound permits for sensitive actions. | high |
| D10 | ABAC and policy engine | accepted | Use Open Policy Agent/Rego as the principal portable PDP, with policy information from trusted identity, entitlement, licence, provider and risk services. Keep relationship data available as input rather than adopting a separate ReBAC engine initially. | medium-high |
| D11 | Trusted device posture | accepted | Use Entra Conditional Access and Intune-compliance claims as trusted posture evidence for the first protected pilot. Never accept posture asserted directly by the MCP client. | high |
| D12 | Access and cache isolation | accepted | Operate open, PSGA and commercial data planes as physically separate deployments/stores/caches/keys/identities. Share source code, schemas and reviewed policy definitions only. | high |
| D13 | Canonical geospatial storage and formats | accepted | Use PostGIS for authoritative/queryable vector state and indexes; object storage for GeoParquet, PMTiles, COG and downloadable artefacts; DuckDB Spatial for isolated embedded analytics; GeoJSON only for bounded results. | high |
| D14 | Live API versus cache strategy | accepted | Prefer live provider APIs for volatile, transactional or legally authoritative results; use governed versioned caches for reference geographies, approved open bulk data, performance-critical tiles and outage resilience. | high |
| D15 | Open demonstrator hosting | accepted | Publish the research pack and Stage 1 open demonstrator as a static, portable site, initially compatible with GitHub Pages or Cloudflare Pages. Treat ChatGPT Sites as an optional open/synthetic mirror only after UK account availability is verified. | high |
| D16 | Protected production hosting | accepted | Use Azure UK for the first protected pilot: Container Apps/App Service, Azure Database for PostgreSQL/PostGIS, Blob Storage, Entra ID/Conditional Access, managed identities, Key Vault, API Management and Monitor. Keep contracts portable to GCP and AWS. | medium-high |
| D17 | Language and runtime | accepted | Use a TypeScript MCP/control gateway and a Python deterministic geospatial execution service. Keep it to these two deployable services initially. | medium-high |
| D18 | Repository reset and migration | accepted | Create a new repository for Locus Accord only after this decision phase. Archive MCP-Geo as a learning journal. Migrate selected assets through a tested harvest, never by copying the repository wholesale. | high |
| D19 | Minimum viable scope | accepted | Stage 0 creates evidence, schemas and test harness; Stage 1 publishes an HMLR/ONS/LandIS open discovery pack; Stage 2 adds a small open read-only MCP service. Identity, PSGA and commercial work follow only after evidence gates. | high |
| D20 | Working project name | accepted-working-codename | Use Locus Accord (`locus-accord`) as the working codename. It expresses place plus an explicit agreement between authority, policy, data and action. Do not claim legal clearance. | medium |

## Conditions that should stop implementation

- no authority to create the new repository;
- unresolved product licence prevents the Stage 1 data publication;
- public pack contains protected/secret/licensed payloads;
- selected host cannot meet policy-filtered discovery or complete non-UI results;
- authority/device/entitlement evidence cannot be trusted for the protected pilot;
- physical tier isolation is not available where required;
- result receipts cannot reconstruct source, decision and transformation;
- accessibility acceptance fails.

## Final recommendation

Approve Stage 0 and Stage 1 only. Keep Locus Accord as a working codename, keep MCP-Geo unchanged as history, and pass [`codex/CODEX_HANDOFF.md`](../codex/CODEX_HANDOFF.md) plus this entire pack to Codex. Do not authorise protected implementation from this research pack alone.
