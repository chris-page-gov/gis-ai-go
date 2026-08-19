# Technical specification: Locus Accord

## Selected stack

- static OKF 0.2/Explorer-compatible public pack;
- TypeScript gateway, official MCP SDK, MCP `2026-07-28`;
- Python deterministic geospatial execution, typed internal OpenAPI contract;
- OPA/Rego PDP;
- PostgreSQL/PostGIS plus object storage;
- GeoParquet 1.1, PMTiles v3, COG, GeoPackage and bounded GeoJSON;
- OpenTelemetry and W3C Trace Context;
- Arazzo 1.1 workflows, MCP Tasks/MRTR where appropriate;
- Azure managed platform for first protected pilot, but Stage 0 is local/CI only.

## Component contracts

### Gateway

Validates MCP protocol/client metadata, constructs authority context, filters discovery, calls OPA, enforces obligations, controls workflow/permits, selects provider/execution route and emits canonical audit events.

### Execution service

Accepts only typed, bounded operation requests from the gateway; validates geometry/CRS/complexity; calls provider adapters or tier-local data; returns canonical result plus source/transformation/software metadata. It has no end-user authentication logic and cannot decide policy.

### Provider adapter

`describe()`, `health()`, `estimate()`, `execute()`, `normalise_error()`, `licence_evidence()` and `provenance()`; no provider can omit source/version/rights metadata.

### Evidence service

Writes canonical audit events and immutable result receipts. Provides authorised challenge/reconstruction reads. It never stores access tokens or unnecessary query content.

## Core tool contracts

Canonical catalogue: [`../data/tool-catalogue.json`](../data/tool-catalogue.json). Initial implementation order: `catalogue.search`, `catalogue.describe`, `evidence.inspect`, `selection.resolve`, `data.query`, then remaining tools behind evaluation evidence.

## Identity/policy

Schemas: authority context, policy decision and evidence receipt under [`../schemas/`](../schemas/). PEPs exist at discovery, invocation, workflow, credential, cache, projection, map, export and audit routes.

## Data/cache

Separate deployment/storage/keys/identity for open, PSGA and commercial. Cache manifests bind provider, dataset/version, source checksum, retrieval, licence, entitlement context, policy version, transformation, expiry, audience and permitted operations.

## Environment/secrets

Stage 0 uses no live secrets. Later environments use managed identity and secret stores. No `.env` is committed; local provider integration is opt-in and uses synthetic/public fixtures by default.

## Observability

Trace ID crosses host/gateway/PDP/execution/provider/evidence. Logs are structured, minimised and classified. Metrics cover policy outcomes, provider health, latency/cost, cache freshness, geometry complexity, export volume and evidence integrity.
