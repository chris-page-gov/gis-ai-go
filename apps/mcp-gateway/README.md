# MCP gateway

This package contains a local-only, unregistered candidate for the GIS AI GO gateway.
Its generic HTTP and STDIO entrypoints remain inactive; only the fixed container
entrypoint mounts the reviewed exact-five assembly. It is an implementation
workbench, not a supported or deployed service.

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
  key first acquires a module-branded, time-bounded and no-egress provider lease.
  Process concurrency and first-attempt rate rejection therefore occur before
  immutable ownership; an unused lease is released on a claim race or capacity
  failure. Transport can start only after durable ownership. A new key is refused
  before ownership publication at the fixed 4,096-claim local index ceiling; this
  maps to the existing non-reflective `503 evidence_unavailable` problem. Every
  default remains empty.
- the HTTP candidate listens only on `127.0.0.1:8787` and exposes `GET /healthz`,
  `GET /readyz` and `GET /openapi.json`. Readiness always returns `503` with zero
  active tools and zero active API operations.
- a separate container entrypoint binds `0.0.0.0:8787` only inside the reviewed
  image so its offline Compose bridge can reach it. It verifies fixed private,
  disjoint ledger and reconciliation volumes and the byte- and semantic-identity of
  the sole approved T04 cache record. It then constructs the fixed active ONS
  adapter and mounts exactly `catalogue.search`, `catalogue.describe`,
  `selection.resolve`, `data.query` and `evidence.inspect`, with the three matching
  MCP resources and `productionRegistration: false`. Compose declares only
  `127.0.0.1:8787`. Acceptance
  separately records whether the engine realised that host-loopback mapping or the
  permitted no-port internal-network fallback. The checker validates the exact
  exposed port and loopback host binding, then normalises only the reviewed Docker
  omitted, `null` and empty-list serialisations to that fallback; it is not
  host-ingress evidence. At the fixed claim ceiling, `/readyz` reports
  `503 reconciliation-capacity-exhausted` while health, exact-five discovery,
  existing-key reconciliation and evidence inspection remain mounted.
- `startCatalogueStdio` and the shipped STDIO entrypoint remain modern-only at
  MCP `2026-07-28` and reject every legacy opening. A separately named
  `startCatalogueLegacyConformanceStdio` constructor can negotiate the bounded
  `2025-06-18` fallback for isolated host conformance only. It requires the exact
  exported `MCP_LEGACY_CONFORMANCE_ONLY` symbol, which cannot be reconstructed
  from an environment variable, command-line value or JSON configuration.

The cursor digest detects corruption; it conveys no identity, authentication or
authority.

## Deliberate production activation block

`createGovernedCandidateAssembly` and its direct, MCP HTTP, MCP STDIO and combined
Node wrappers provide one compile-time exact-five integration candidate. Registry,
policy, provider lifecycle, verified snapshot and linked evidence dependencies can
only reduce its discovery set; every wrapper reports production registration as
false. The closed `createCandidateActivation` builder fixes the full candidate set,
active ONS lifecycle and approved cache internally, and only the container
entrypoint calls it. The evidence
inspector's top-level identity belongs to the current inspection, while its nested
receipt and policy decision belong to the earlier inspected call; inspection
creates no replacement receipt or ledger event.

The generic HTTP and STDIO entrypoints do not mount application functions. Explicit
constructor options remain local-conformance seams and every default constructor
still has no active tool or resource. The container is the sole shipped exception:
it mounts the closed local exact-five candidate from fixed image inputs. It does not
make a provider call during startup or assurance, publish a service, contact an
external policy service or register the candidate for production.
There is no environment-variable or command-line activation override. The
selection and data applications and their explicit transport options are not
referenced by any generic shipped entrypoint or default capability list.
The unregistered image is built from a materialised, checksum-bound Git-tracked and OKF
context. Environment files are rejected and ignored, dependency fetching precedes
the broad source copy, and subsequent install, build and runtime mutations have no
BuildKit network. The fixed `linux/amd64` runtime composes an exact UBI 10 micro root,
the checked official Node.js 24.19.0 executable and licence, UBI micro's exact
`libgcc_s`, and only the checked versioned `libstdc++` object and notices from the
exact UBI Node.js 24 minimal donor. It retains
the unmodified UBI EULA, source-container provenance and an explicit no-Red-Hat-
support boundary. Its final image gate requires canonical OCI/source/runtime
verification, exact repeat-build bytes, a full Syft SBOM with receipt-bound donor
files, replayable Trivy evidence, container acceptance and the closed 25-file
evidence directory: 24 subjects plus its manifest. Those controls do not register
or deploy the local candidate for production.
The test-only legacy launcher is separately named, requires both the existing
conformance gate and an exact `--legacy-stdio-conformance-only` argument, and is
not referenced by a package script or shipped entrypoint.

Protocol-conformant direct and MCP transport candidates now cover catalogue,
evidence inspection, selection and the bounded data query. The local container
activation does not relax the production block: independent-host interoperability,
release, deployment and full lifecycle evidence remain separate gates. The compiled
public document is not OPA, authentication, identity or an enterprise entitlement
service.

## Local verification

From the repository root:

```bash
pnpm --filter @gis-ai-go/mcp-gateway run test
```

To inspect the deliberately blocked generic HTTP surface after building the candidate:

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
and the [unregistered container runbook](../../docs/operations/DEPLOY-207_GATEWAY_CONTAINER.md).
