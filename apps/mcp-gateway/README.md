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
- `createEvidenceInspectApplication` reads only verified anonymous-open records. Its
  unchanged v1 request uses a receipt identity; its additive v2 request uses a
  caller-known `data.query` idempotency key and a linked reconciliation index to
  recover the original verified receipt after a lost response. It never replays the
  original result. Explicit local-conformance options can mount the same reconciled
  instance as a direct route or MCP HTTP/STDIO tool. The only MCP evidence resource
  remains the receipt-ID URI; no URI contains a raw idempotency key. Every default
  registration remains empty.
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
  builds and fully verifies one v2 receipt. A reconciled instance also requires an
  exact linked ledger and reconciliation index. Its transport request wraps the
  unchanged parameters with one mandatory caller-generated 256-bit idempotency key.
  A repeated pending or completed key returns a receipt-free `409` before provider
  preflight; a conflicting semantic fingerprint also returns `409`. The caller then
  uses `evidence.inspect` v2 to recover the receipt, not the original result.
  Discovery may remain suspended; an invocation-suspended adapter cannot execute a
  new key. There is no default adapter, environment activation or live-provider call
  in ordinary tests. Caller signal cancellation and caller deadline expiry are
  checked before and after execution and remain distinct from an adapter-local
  provider timeout. An optional explicit `ApprovedOnsDataQueryCache` may serve the
  one fixed ONS result only after the allowed policy decision and the current
  execution of an exact, pristine ONS adapter returns an internally classified
  network failure or HTTP 500 to 599 response. The owner-bound outage proof is
  consumed once in the same invocation. A replayed proof, substituted adapter, 3xx
  or 4xx response, local timeout, unsafe address, malformed response, opaque error
  or externally constructed fault remains closed.
  It exposes retrieval, stale-after and check times in the receipt-bound result,
  forbids stale use, and has no default loader or environment
  switch. Explicit local-conformance options mount only a reconciliation-
  branded instance on the direct API, modern MCP HTTP and modern MCP STDIO. Every
  data face must also mount the inspector branded with the exact same index. Direct
  data requests ignore caller request-ID headers and use a server-generated
  identity. Shared HTTP and STDIO ingress also rejects a complete raw, prefixed,
  percent-encoded or multiply encoded key in request IDs, methods, tool names and
  protocol-version claims before SDK dispatch; HTTP applies the same rule to its
  parity headers. Requests use a fixed `id: null` error, notifications remain silent
  and ordinary bounded protocol controls retain their behaviour. A genuinely new
  key is refused before ownership publication at the fixed 4,096-claim local
  index ceiling; this maps to the existing non-reflective `503 evidence_unavailable`
  problem. Every default remains empty.
- the HTTP candidate listens only on `127.0.0.1:8787` and exposes `GET /healthz`,
  `GET /readyz` and `GET /openapi.json`. Readiness always returns `503` with zero
  active tools and zero active API operations.
- a separate container entrypoint binds `0.0.0.0:8787` only inside the reviewed
  image so its offline Compose bridge can reach it. It verifies fixed private,
  disjoint ledger and reconciliation volumes, but supplies no operation, resource,
  application or provider seam. Compose declares only `127.0.0.1:8787`. Acceptance
  separately records whether the engine realised that host-loopback mapping or the
  permitted no-port internal-network fallback. The checker validates the exact
  exposed port and loopback host binding, then normalises only the reviewed Docker
  omitted, `null` and empty-list serialisations to that fallback; it is not
  host-ingress evidence.
- `startCatalogueStdio` and the shipped STDIO entrypoint remain modern-only at
  MCP `2026-07-28` and reject every legacy opening. A separately named
  `startCatalogueLegacyConformanceStdio` constructor can negotiate the bounded
  `2025-06-18` fallback for isolated host conformance only. It requires the exact
  exported `MCP_LEGACY_CONFORMANCE_ONLY` symbol, which cannot be reconstructed
  from an environment variable, command-line value or JSON configuration.

The cursor digest detects corruption; it conveys no identity, authentication or
authority.

## Deliberate activation block

`createGovernedCandidateAssembly` and its direct, MCP HTTP, MCP STDIO and combined
Node wrappers provide one compile-time exact-five integration candidate. Registry,
policy, provider lifecycle, verified snapshot and linked evidence dependencies can
only reduce its discovery set; every wrapper reports production registration as
false. The shipped entrypoints do not call these constructors. The evidence
inspector's top-level identity belongs to the current inspection, while its nested
receipt and policy decision belong to the earlier inspected call; inspection
creates no replacement receipt or ledger event.

The shipped entrypoints do not mount application functions on HTTP routes. Explicit
constructor options exist for local conformance tests, including `evidence.inspect`,
`selection.resolve` and `data.query`, but there is no default catalogue, evidence,
selection or data endpoint, active MCP tool or resource, public deployment,
provider call or external policy service.
The portable evidence store and inspector are inactive embedding components; no
active application receives their configuration. The blocked container entrypoint
opens fixed roots only to prove that the durable volume boundary is safe and
restart-verifiable.
There is no environment-variable or command-line activation override. The
selection and data applications and their explicit transport options are not
referenced by any shipped entrypoint or default capability list.
The blocked image is built from a materialised, checksum-bound Git-tracked and OKF
context. Environment files are rejected and ignored, dependency fetching precedes
the broad source copy, and subsequent install, build and runtime mutations have no
BuildKit network. Its final image gate requires canonical OCI/source/runtime
verification, exact repeat-build bytes, a full Syft SBOM, replayable Trivy evidence,
container acceptance and the closed 12-file evidence manifest. Those controls do
not enable this package.
The test-only legacy launcher is separately named, requires both the existing
conformance gate and an exact `--legacy-stdio-conformance-only` argument, and is
not referenced by a package script or shipped entrypoint.

Protocol-conformant direct and MCP transport candidates now cover catalogue,
evidence inspection, selection and the bounded data query. Activation remains
hard-blocked until independent-host interoperability, release, deployment and full
lifecycle evidence receive their own review. A later reviewed
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
the
[inactive public-read transport boundary](../../docs/operations/TOOLS-205_PUBLIC_READ_TRANSPORT.md),
the [QUAL-206 interoperability runbook](../../docs/operations/QUAL-206_INTEROPERABILITY.md),
the [inactive selection resolver boundary](../../docs/operations/TOOLS-205_SELECTION_RESOLVE.md),
and the [blocked container runbook](../../docs/operations/DEPLOY-207_GATEWAY_CONTAINER.md).
