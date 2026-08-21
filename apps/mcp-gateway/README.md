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
- `createSelectionResolveApplication` applies one checked finite constraint grammar
  to the accepted `PV-ONS-DATA` resource. It returns either an exact
  content-addressed non-executable plan with public-read v2 evidence, or a closed
  problem with `plan: null`. Question text is untrusted and is never interpreted,
  reflected, persisted or sent to a provider. The application has no adapter,
  execution or network dependency. A later inactive transport candidate can mount
  it only through explicit direct, modern MCP HTTP or modern MCP STDIO options.
- `createDataQueryApplication` is an inactive transport-neutral application seam
  for the exact reviewed ONS single-observation query. It requires an explicitly
  injected `OnsDataApiAdapter`, verifies public-read v2 policy plus the adapter's
  invocation health, estimate, rights, provenance and result independently, then
  builds and fully verifies one v2 receipt. Discovery may remain suspended; an
  invocation-suspended adapter cannot execute. There is no default adapter,
  environment activation or live-provider call in ordinary tests. Caller signal
  cancellation and caller deadline expiry are checked before and after execution
  and remain distinct from an adapter-local provider timeout. Explicit local
  conformance options can mount the same application on the direct API, modern MCP
  HTTP and modern MCP STDIO; every default remains empty.
- the HTTP candidate listens only on `127.0.0.1:8787` and exposes `GET /healthz`,
  `GET /readyz` and `GET /openapi.json`. Readiness always returns `503` with zero
  active tools and zero active API operations.
- `startCatalogueStdio` and the shipped STDIO entrypoint remain modern-only at
  MCP `2026-07-28` and reject every legacy opening. A separately named
  `startCatalogueLegacyConformanceStdio` constructor can negotiate the bounded
  `2025-06-18` fallback for isolated host conformance only. It requires the exact
  exported `MCP_LEGACY_CONFORMANCE_ONLY` symbol, which cannot be reconstructed
  from an environment variable, command-line value or JSON configuration.

The cursor digest detects corruption; it conveys no identity, authentication or
authority.

## Deliberate activation block

The shipped entrypoints do not mount application functions on HTTP routes. Explicit
constructor options exist for local conformance tests, including `evidence.inspect`,
`selection.resolve` and `data.query`, but there is no default catalogue, evidence,
selection or data endpoint, active MCP tool or resource, public deployment,
provider call or external policy service.
The portable evidence store and inspector are inactive embedding components; no
shipped entry point supplies their configuration or a ledger path.
There is no environment-variable or command-line activation override. The
selection and data applications and their explicit transport options are not
referenced by any shipped entrypoint or default capability list.
The test-only legacy launcher is separately named, requires both the existing
conformance gate and an exact `--legacy-stdio-conformance-only` argument, and is
not referenced by a package script or shipped entrypoint.

Protocol-conformant direct and MCP transport candidates now cover catalogue,
evidence inspection, selection and the bounded data query. Activation remains
hard-blocked until independent-host interoperability, T04 fallback, release,
deployment and full lifecycle evidence receive their own review. A later reviewed
change must satisfy that activation policy before a shipped entrypoint may mount or
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

See the [candidate boundary](../../docs/operations/MCP-201_GATEWAY_CANDIDATE.md),
the [EVID-204 inspection transport boundary](../../docs/operations/EVID-204_INSPECT_TRANSPORT.md),
the [inactive public-read transport boundary](../../docs/operations/TOOLS-205_PUBLIC_READ_TRANSPORT.md),
the [QUAL-206 interoperability runbook](../../docs/operations/QUAL-206_INTEROPERABILITY.md)
and the [inactive selection resolver boundary](../../docs/operations/TOOLS-205_SELECTION_RESOLVE.md).
