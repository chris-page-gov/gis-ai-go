# MCP gateway

This package contains an inactive, local-only candidate for the GIS AI GO gateway.
It is an implementation workbench, not a supported or deployed service.

## Implemented candidate components

- `loadCatalogueSnapshot` loads the generated public catalogue only after its exact
  inventory, checksum ledger, manifest, build receipt, content root and public-bundle
  identity agree. It rejects links, unsafe paths, unexpected files, changed files and
  over-limit inputs, then returns one immutable snapshot with an explicit freshness
  warning when its review date has passed.
- `createCatalogueApplication` binds deterministic `catalogue.search` and
  `catalogue.describe` functions to that snapshot. The transport-neutral functions
  use closed request, result and problem envelopes, bounded inputs and cursors bound
  to both the catalogue content root and normalised search criteria.
- the HTTP candidate listens only on `127.0.0.1:8787` and exposes `GET /healthz`,
  `GET /readyz` and `GET /openapi.json`. Readiness always returns `503` with zero
  active tools and zero active API operations.

The cursor digest detects corruption; it conveys no identity, authentication or
authority.

## Deliberate activation block

The application functions are not mounted on HTTP routes. There is no
`catalogue.search` or `catalogue.describe` endpoint, MCP listener, MCP tool
registration, public deployment, provider call, policy engine or evidence store.
There is no environment-variable or command-line activation override.

Activation remains hard-blocked as
`inline-evidence-and-public-policy-unavailable`. EVID-204 must add reviewed public
policy decisions and canonical inline evidence receipts before a later reviewed
change may mount or advertise either operation.

## Local verification

From the repository root:

```bash
pnpm --filter @gis-ai-go/mcp-gateway run test
```

To inspect the deliberately blocked HTTP surface after building the candidate:

```bash
pnpm run build:okf
pnpm --filter @gis-ai-go/contracts run build
pnpm --filter @gis-ai-go/mcp-gateway run build
pnpm --filter @gis-ai-go/mcp-gateway run start:http
```

See the [candidate boundary](../../docs/operations/MCP-201_GATEWAY_CANDIDATE.md)
and [verification record](../../docs/operations/MCP-201_VERIFICATION.md).
