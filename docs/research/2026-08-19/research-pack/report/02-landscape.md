# Landscape: standards have matured, but the edges remain uneven

> **Evidence notation.** Bracketed identifiers such as `[S-MCP-SPEC]` resolve through [`data/sources.json`](../data/sources.json). **Verified fact**, **assumption**, **recommendation** and **unresolved question** are deliberately separated. Retrieval date: **19 August 2026**.


## The successor can target a final MCP baseline

**Verified fact.** MCP 2026-07-28 is the final general-availability specification. The new core is stateless and supports self-describing requests, `server/discover`, routable method/name headers, deterministic cacheable catalogue results and multi-round-trip requests. Tasks, Apps and enterprise-managed authorisation remain extensions and require host-specific conformance tests. [S-MCP-SPEC] [S-MCP-TASKS] [S-MCP-APPS] [S-MCP-EMA]

**Implication.** Protocol compatibility should be a test matrix, not a set of unverified conditionals embedded in provider code. Pin the specification, SDK release/commit and fixtures in each release manifest.

## Discovery and workflow standards form a coherent stack

- **OKF 0.2** is the human/agent knowledge corpus and source-led provenance layer. [S-OKF-SPEC]
- **DCAT 3 and GeoDCAT-AP 3.1** provide catalogue interoperability, not a replacement for rich source-native records. [S-DCAT] [S-GEODCAT]
- **OGC API – Records 1.0** is the geospatial record-service interface; **STAC** is appropriate for spatiotemporal assets. [S-OGC-RECORDS] [S-STAC]
- **OpenAPI/OGC API** describe direct request/response contracts; **AsyncAPI** describes events; **Arazzo 1.1** describes explicit API workflows. [S-OPENAPI] [S-ASYNCAPI] [S-ARAZZO]
- **W3C PROV** is an interchange mapping for lineage; **Trace Context** is cross-component correlation; the platform’s canonical evidence schemas remain stricter operational contracts. [S-PROV] [S-TRACE]
- **ODRL** can represent policy/rights concepts, but the provider contract or licence remains legal authority. [S-ODRL]

## Browser agents are an experiment, not a privileged channel

**Verified fact.** WebMCP remains a W3C Community Group draft and was still receiving API corrections immediately before this retrieval. It should not be equated with MCP. [S-WEBMCP]

**Recommendation.** Expose only safe public page operations: search catalogue, apply facets, inspect a record, retrieve relationships, select public map features, obtain evidence for the current view and export selected public metadata. The same operations must remain available through ordinary controls, linked JSON/JSON-LD/OKF and a separate remote MCP service.

## Current geospatial architecture points to open, cloud-native formats

Use a deliberately small set:

- **PostGIS** for indexed, authoritative/queryable vector state and spatial joins;
- **GeoParquet 1.1** for bulk vector artefacts and DuckDB analytics;
- **PMTiles v3/MVT** for portable vector-map delivery;
- **COG** for range-readable raster assets;
- **GeoPackage** for interoperable offline exchange;
- **GeoJSON** only for bounded interactive results;
- **STAC** where there are real asset/collection semantics;
- **OGC API** for provider/service interoperability and legacy WMS/WFS adapters only where unavoidable.

DuckDB Spatial is valuable for isolated embedded analysis and static/public packs, but it should not become the multi-user policy authority or protected primary store.

## UK public-sector controls apply to the query, not only the dataset

An open dataset can participate in a sensitive query; licensed data is not necessarily security-classified. Address/property data, user location, vulnerable-person sites, critical infrastructure and commercially sensitive search patterns can create risk through combination or inference. The design therefore applies identity, purpose, minimisation, DPIA, accessibility, records, transparency and incident controls across all six governance controls. [S-ICO-DPIA] [S-NCSC-CLOUD] [S-SERVICE-STANDARD] [S-ATRS]

## Standards register

| Standard | Version/maturity | Principal role | Canonical authority |
| --- | --- | --- | --- |
| Open Knowledge Format | 0.2 — current normative specification in project context | Human- and agent-readable knowledge, provenance, trust, lifecycle and attestation description | Markdown with YAML frontmatter; source repository |
| Model Context Protocol | 2026-07-28 — final general availability | Agent-facing discovery and invocation | Official MCP specification |
| WebMCP | draft as at 2026-08-19 — W3C Community Group draft; not standards-track | Page-provided browser-resident tools | Draft browser specification |
| Arazzo | 1.1.0 — published specification | Explicit multi-step API workflow description | OpenAPI Initiative |
| OGC API – Records | 1.0 — approved OGC standard | Geospatial catalogue search and records | Provider record service |
| OGC API – Features | 1.x — approved OGC standard | Feature retrieval and filtering | Provider service |
| STAC | 1.x — stable community standard | Spatiotemporal asset and collection discovery | Provider STAC catalogue |
| DCAT | 3 — W3C Recommendation | Dataset and data-service catalogue vocabulary | W3C |
| GeoDCAT-AP | 3.1 — published application profile | Geospatial extension/profile for public-sector catalogues | European Commission profile |
| W3C PROV-O | Recommendation — W3C Recommendation | Interchange model for entities, activities, agents and derivation | Evidence receipt/audit model remains platform schema; PROV is exchange mapping |
| ODRL | 2.2 — W3C Recommendation | Machine-readable permissions, prohibitions and duties | Provider licence and contract remain legal authority |
| W3C Trace Context | Recommendation — W3C Recommendation | Cross-component trace correlation | Trace headers and telemetry store |
| GeoParquet | 1.1 — stable | Cloud-friendly vector storage and analytics exchange | Object artefact manifest |
| PMTiles | 3 — stable | Single-file tiled map delivery from object storage | Published artefact manifest |
| Cloud Optimized GeoTIFF | OGC standard — approved | Range-readable raster delivery | Provider/object artefact |
