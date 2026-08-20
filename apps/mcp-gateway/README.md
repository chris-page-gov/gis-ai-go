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
- an optional explicit ledger embedding seam persists a fully verified inline
  receipt into content-addressed record and event files. Only a completed,
  re-verified write adds `evidence_storage` to the result. Storage failure fails the
  operation. The default remains inline-only.
- `createEvidenceInspectApplication` reads only verified anonymous-open records by
  receipt identity. Explicit local-conformance options can mount the same instance
  as a direct route, MCP HTTP or STDIO tool and receipt resource. It remains absent
  from every default registration.
- the HTTP candidate listens only on `127.0.0.1:8787` and exposes `GET /healthz`,
  `GET /readyz` and `GET /openapi.json`. Readiness always returns `503` with zero
  active tools and zero active API operations.

The cursor digest detects corruption; it conveys no identity, authentication or
authority.

## Deliberate activation block

The shipped application functions are not mounted on HTTP routes. Explicit
constructor options exist for local conformance tests, including
`evidence.inspect`, but there is no default catalogue or evidence endpoint, active
MCP tool or resource, public deployment, provider call or external policy service.
The portable evidence store and inspector are inactive embedding components; no
shipped entry point supplies their configuration or a ledger path.
There is no environment-variable or command-line activation override.

Protocol-conformant MCP and direct transport candidates already exist. Activation
remains hard-blocked until the inspection transport, independent-host
interoperability, fallback and full lifecycle evidence receive their own review. A
later reviewed change must satisfy that activation policy before it may mount or
advertise any operation. The compiled public document is not OPA, authentication,
identity or an enterprise entitlement service.

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
and [EVID-204 inspection transport boundary](../../docs/operations/EVID-204_INSPECT_TRANSPORT.md).
