# Data, cache and mapping: deterministic, versioned and rights-aware

> **Evidence notation.** Bracketed identifiers such as `[S-MCP-SPEC]` resolve through [`data/sources.json`](../data/sources.json). **Verified fact**, **assumption**, **recommendation** and **unresolved question** are deliberately separated. Retrieval date: **19 August 2026**.


## Canonical representations

- **PostGIS:** indexed feature/reference state, spatial joins, topology-aware queries and workflow state that benefits from transactions.
- **Object storage:** immutable source packages, GeoParquet extracts, PMTiles, COG, reports and expiring exports.
- **DuckDB Spatial:** isolated embedded/batch analytics over approved artefacts, including browser/Wasm only for public bounded data.
- **GeoPackage:** portable offline exchange.
- **GeoJSON:** small interactive responses; not national-scale boundaries or bulk exports.

Every result retains provider-native attributes alongside canonical fields. `canonical_id` never replaces the provider namespace/id/version.

## Identifier model

Each UPRN, BLPU, USRN, TOID, OSID or ONS geography code carries:

- namespace and issuing authority;
- identifier value and feature/entity type;
- valid from/to and observed/source version;
- predecessor/successor/split/merge relationships;
- source-native name/status and cross-reference evidence;
- confidence and match method for derived links.

A current code is not silently substituted for a historic code when answering an `as_of` query.

## CRS and geometry

Use WGS84/EPSG:4326 as the default interchange CRS and EPSG:27700 for Great Britain metric operations where appropriate. Record axis order, source CRS, transformation operation, PROJ/software version, geometry repair/simplification and output CRS. Do not repair invalid geometry silently; the caller and receipt must see the policy and operation.

## When to stream, page, tile or export

| Result shape | Delivery |
| --- | --- |
| ≤100 catalogue records or small tabular response | Inline JSON with deterministic cursor |
| Small geometry for inspection | Bounded GeoJSON with coordinate/vertex/byte limits |
| Large vector result | GeoParquet or GeoPackage artefact; preview/simplified geometry inline |
| Interactive national map | MVT/PMTiles with scale-dependent generalisation |
| Large raster | COG/Zarr only where the source/use case genuinely warrants it |
| Long-running process | MCP Task with explicit state/expiry/cancellation and artefact output |

## Governed cache classes

| Cache | Use | Mandatory metadata/isolation |
| --- | --- | --- |
| Live query cache | Short-lived provider response reuse | Actor/organisation/entitlement-sensitive key where protected; no-store for sensitive queries |
| Reference geography/code cache | Boundaries, lookups and change history | Provider/vintage/rights/checksum/CRS; open and protected stores separate |
| Tile cache | Map performance | Layer/fields/style/licence/audience/expiry; protected tiles token-bound |
| Object/download cache | Bulk provider packages and approved exports | Immutable checksum, malware/archive validation, licence, retention |
| Derived-result cache | Repeated deterministic analysis | Inputs, transformations, software, policy version, audience and invalidation lineage |
| Durable licensed replica | Approved PSGA/commercial data | Dedicated deployment, identity, keys, database, audit and deletion/withdrawal process |

## Live versus cached

Use live provider services for legal/transactional authority, highly volatile data and operations where caching is prohibited. Use approved caches for stable reference geographies, public bulk datasets, performance-critical map assets and controlled outage resilience. A cached response always reports source version, retrieved time, expiry/staleness and the policy that allowed stale use.

## Capacity assumptions

| Scale | Working assumption | Implication |
| --- | --- | --- |
| Personal prototype | Single user; public/synthetic; <20 GB | Static pack and local DuckDB/PostGIS fixtures |
| Departmental pilot | 10–200 concurrent users; 0.1–2 TB including artefacts | Managed PostGIS/object storage, queues, quotas and tier isolation |
| Multi-organisation | Hundreds–thousands; 1–20 TB | Tenant/organisation isolation, regional capacity, dedicated evidence and entitlement services |
| National scale | Thousands+; 10–100+ TB and high tile traffic | Formal capacity model, CDN, distributed jobs, DR and federated operating model |

**Assumption.** These are architecture-order estimates, not sizing evidence or procurement quotes.
