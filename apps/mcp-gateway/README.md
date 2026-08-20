# MCP gateway

This package contains an inactive, local-only candidate for the GIS AI GO gateway.
It is an implementation workbench, not a supported or deployed service.

## Implemented candidate components

- `loadCatalogueSnapshot` loads the generated public catalogue only after its exact
  inventory, checksum ledger, manifest, build receipt, content root and public-bundle
  identity agree. It rejects links, unsafe paths, unexpected files, changed files and
  over-limit inputs. Directory enumeration is streamed and file reads are bounded to
  the recorded length plus one byte with identity checks before and after reading.
  It then returns one immutable snapshot with an explicit freshness warning when its
  review date has passed.
- `createCatalogueApplication` binds deterministic `catalogue.search` and
  `catalogue.describe` functions to that snapshot. The transport-neutral functions
  use closed request, result and problem envelopes, bounded inputs and outputs, and
  cursors bound to both the catalogue content root and normalised search criteria.
  A snapshot that cannot fit the public result schema is rejected rather than
  truncated. Every successful result follows one evidence-producing path through
  the server-owned anonymous-open authority context and checked-in default-deny
  public policy. Its canonical inline receipt binds the exact catalogue, normalised
  parameter digest, result core, gateway revision and record-specific licence
  evidence while stating `not-persisted` and `not-attested`.
- the HTTP candidate listens only on `127.0.0.1:8787` and exposes `GET /healthz`,
  `GET /readyz` and `GET /openapi.json`. Readiness always returns `503` with zero
  active tools and zero active API operations.

The cursor digest detects corruption; it conveys no identity, authentication or
authority.

## Deliberate activation block

The application functions are not mounted on HTTP routes. There is no
`catalogue.search` or `catalogue.describe` endpoint, MCP listener, MCP tool
registration, public deployment, provider call, external policy service or evidence
store.
There is no environment-variable or command-line activation override.

Activation remains hard-blocked as
`transport-and-interoperability-unverified`. A later reviewed change must add and
verify the protocol-conformant transports and client interoperability before it may
mount or advertise either operation. The compiled public document is not OPA,
authentication, identity or an enterprise entitlement service.

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
and [EVID-204 inline-evidence boundary](../../docs/operations/EVID-204_INLINE_EVIDENCE.md).
