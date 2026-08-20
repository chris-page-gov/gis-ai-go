# MCP-201 verification record

- status: shared catalogue, inactive gateway and EVID-204A slices accepted on
  protected `main`; MCP and direct-API transport slice remains a local candidate
- reviewed on: 20 August 2026
- work item: [MCP-201](https://github.com/chris-page-gov/gis-ai-go/issues/19)

## Protected-main shared catalogue contract

- protected-main base: `80ac89d89e04751045693cecff4a3a714d121ebe`
- candidate implementation commit: `5150cc25a56fb4263f4f6ec832f8995ad2a9d4c9`
- security remediation commit: `2e6094e4c81d0cb60fa19e5cf0a4f6dc4ae30082`
- pull request: [26](https://github.com/chris-page-gov/gis-ai-go/pull/26)
- pull-request assurance:
  [passing](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32338159020)
- pull-request CodeQL:
  [passing](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32338156959)
- protected-main merge: `e5e6d4db5ac7036198cde64279e815f214f3defd`
- protected-main assurance and provenance:
  [passing](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32338916345)
- protected-main CodeQL:
  [passing](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32338916269)
- protected-main provenance:
  [attestation 41792357](https://github.com/chris-page-gov/gis-ai-go/attestations/41792357)

### Outcome

The protected-main slice establishes a shared catalogue contract over the existing
checksum-verified public catalogue. The Explorer adopts that shared core through
thin compatibility adapters, while closed request, result and problem schemas
define a bounded foundation for later read-only catalogue delivery.

It does not provide an MCP listener, catalogue API, provider adapter, execution
path or evidence store. `catalogue.search` and `catalogue.describe` are not
registered, advertised or active. EVID-204A subsequently replaces the earlier
receiptless candidate result with a required inline receipt that expressly says it
is not persisted and not attested.

### Contract scope

- the catalogue parser, search, facet, graph, timeline and link helpers are owned by
  the shared contracts package and consumed by the existing Explorer;
- query analysis exposes the 256-code-point and 10-normalised-term boundaries so a
  later network surface can reject over-limit input consistently;
- closed request, result and problem schemas bound catalogue search and description
  inputs, source-native detail values and public record provenance; and
- repository contract validation checks every schema against JSON Schema Draft
  2020-12 and the GIS AI GO URN namespace.

### Accepted evidence

The exact pull-request candidate passed the complete locked `pnpm run check` on
20 August 2026. The gate included:

- 19 of 19 shared catalogue contract tests;
- 4 of 4 existing non-networked gateway boundary tests;
- 6 of 6 catalogue API schema tests;
- 16 of 16 Explorer build-policy tests and 42 of 42 Explorer unit and component
  tests;
- 88 of 88 repository Python tests and 2 of 2 execution-boundary tests;
- 27 of 27 real-browser tests;
- two clean locked builds with byte-identical Pages archives, checksum files and
  archive receipts;
- validation of the product version across 8 manifests and locks, 12 schemas and
  53 evaluation records;
- 300 local Markdown links, 183 immutable research hashes, 2 ledger snapshots and
  71 source identifiers;
- a 461-file baseline secret and machine-path scan, 9 rendered diagrams and a
  146-component CycloneDX SBOM;
- the Explorer production build and built ESM contracts-package runtime import;
- confirmation that the immutable research tree was unchanged from its
  protected-main base; and
- an independent current-byte review with a `SHIP` verdict and no P0, P1 or P2
  finding.

The first pull-request CodeQL run identified a high-severity polynomial regular
expression in the inherited HTML-like-content guard. The issue was reproduced on
the real parser path, replaced by a linear-time scanner and covered by adversarial
and legitimate controls. The remediation commit passed the complete local gate,
pull-request assurance, all three CodeQL language analyses and the aggregate
"No new alerts" check. The protected-main assurance, CodeQL and provenance evidence
listed above completed this slice's remote gate.

## Inactive gateway candidate

- protected-main base: `e5e6d4db5ac7036198cde64279e815f214f3defd`
- candidate implementation commit: `442f788108106744e1e2ed7283e38c2a22aac5f1`
- complete local gate: passing at the candidate implementation commit on
  20 August 2026
- independent current-byte review: `SHIP`; no P0, P1 or P2 finding
- pull request: [27](https://github.com/chris-page-gov/gis-ai-go/pull/27)
- pull-request assurance:
  [passing](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32344360889)
- pull-request provenance: skipped as designed for the pull-request event
- pull-request CodeQL:
  [passing](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32344358198)
- protected-main merge: `4948890c10adb4f0ac6f427cda21cb0c0c4607dd`
- acceptance-evidence pull request:
  [28](https://github.com/chris-page-gov/gis-ai-go/pull/28)
- protected-main acceptance run:
  [passing](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32346195668)
- protected-main acceptance CodeQL:
  [passing](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32346195675)
- protected-main acceptance attestation:
  [41809248](https://github.com/chris-page-gov/gis-ai-go/attestations/41809248)

### Candidate outcome

The protected-main bytes add a fail-closed, checksum-verified immutable catalogue
loader and a deterministic, transport-neutral application for
`catalogue.search` and `catalogue.describe`. The functions use closed envelopes,
bounded inputs and outputs, and deterministic cursors bound to the exact catalogue
content root and normalised search criteria. The loader streams its bounded
inventory, reads only the recorded file length plus one byte and rechecks file
identity and metadata after each read. The application rejects any verified
snapshot that cannot fit the closed result schema.

The HTTP candidate binds to loopback and exposes only:

- `GET /healthz` for process and verified-catalogue health;
- `GET /readyz`, which always returns `503` with empty active tool and API lists;
  and
- `GET /openapi.json`, whose contract contains no catalogue operation path.

There is no search or description route, MCP listener or tool registration, public
deployment, provider call, external policy service or evidence store. The
application code can be tested directly, but it cannot be activated through an
environment variable, command-line option or test mode.

Malformed request identities, hostile unknown keys and non-canonical URL paths fail
through bounded problem envelopes rather than escaping as raw server errors. The
exact regression suite covers schema-boundary overflow, same-inode file growth,
over-limit directory inventories and malformed path encodings.

### Accepted local evidence

The exact candidate implementation commit passed the complete locked
`pnpm run check` gate on 20 August 2026. The gate included:

- 19 of 19 shared catalogue contract tests and 38 of 38 gateway tests;
- 16 of 16 Explorer build-policy tests, 42 of 42 Explorer unit and component
  tests and 27 of 27 real-browser tests;
- 88 of 88 repository Python tests and 2 of 2 execution-boundary tests;
- two clean locked builds with byte-identical Pages archives
  (`99586ce3156255c0c5942d6eca8d1f004581123d86f4e19153e6cbaac774c6c4`),
  checksum files and archive receipts;
- validation of version `0.1.0` across 8 manifests and locks, 12 schemas and
  53 evaluation records;
- 305 local Markdown links, 183 immutable research hashes, 2 ledger snapshots and
  71 source identifiers;
- a 479-file baseline secret and machine-path scan, 9 rendered diagrams and a
  146-component CycloneDX SBOM; and
- deterministic OKF content root
  `57bfb5a190424289ea09b7eb0729ecdad08292ec7cb8abed148ddf29c9f975d1`,
  with the immutable research tree unchanged from protected `main`.

The formal pre-remediation security diff scan covered all 14 changed runtime
surfaces and found no security-reportable issue under the inactive, loopback-only
and operator-write-only boundary. It also validated five merge-blocking contract
and resource-bound defects. Those defects were fixed before the implementation
commit; the repaired current bytes then received an independent `SHIP` review and
passed all 38 gateway tests. This does not claim that the absent public service has
been security-tested as a deployed service.

The pull-request gate and implementation merge completed, but GitHub did not emit a
push workflow for that runtime merge during the 15-minute monitored acceptance
window. The unchanged runtime tree was therefore accepted through the subsequent
docs-only [pull request 28](https://github.com/chris-page-gov/gis-ai-go/pull/28),
which merged as `87d6a1b4f8fb15597e5ae91132aa9b61dca57667`. Protected-main assurance and
provenance passed in
[run 32346195668](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32346195668),
CodeQL passed in
[run 32346195675](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32346195675),
and [attestation 41809248](https://github.com/chris-page-gov/gis-ai-go/attestations/41809248)
binds archive SHA-256
`f6adb7998c26bef62a651ec825e3a4426d955af4a09167b264dfa221d0ef28b0` to that exact
protected-main commit and run.

The pull-request head and protected-main merge both resolve to tree
`5b04c4552a0d750aa7a904fbcde4aebd7b1bd1d4`, and the repository had zero open
code-scanning alerts at the end of that window. No job failed: GitHub created no
check suite or workflow run for the merge.

## Local MCP and direct-API transport candidate

- protected-main base: `997d5fdd478797b20b05d1980be8f986645d410e`
- candidate implementation commit:
  `fb0234b9a6a968fe68c2fbe98388f2415393c9c1`
- pull request, remote CI, CodeQL and attestation: not yet created
- deployment, public service URL and registry entry: none
- activation state: blocked; default MCP tool and direct-API arrays empty;
  resources default to none

### Candidate outcome

The exact local candidate commit adds direct POST search and description handlers,
an MCP 2026-07-28 HTTP route and a protocol-clean STDIO entry point. All use one
checksum-verified catalogue snapshot, the same application, exact canonical
request and result schemas, and the existing canonical inline evidence path.

Explicit constructor options can register the two direct operations, MCP tools and
read-only catalogue resources for local conformance and embedding tests. Omission
uses the frozen activation document, which advertises no direct operation or MCP
tool; MCP resources also default to none. Neither shipped entry point supplies an
override. The default OpenAPI document has no catalogue path and readiness remains
`503`.

The pinned split SDK roles are:

- `@modelcontextprotocol/server@2.0.0` for the modern server factory, HTTP handler
  and STDIO transport;
- `@modelcontextprotocol/node@2.0.0` for the streaming Node adapter, with its Node
  adapter dependencies locked transitively; and
- development-only `@modelcontextprotocol/client@2.0.0` for conformance tests.

The published server 2.0.0 HTTP handler can dispatch a modern request whose body
declares protocol revision 2026-07-28 even when the required
`MCP-Protocol-Version` header is absent. The candidate applies a narrow guard for
that exact case and returns HTTP `400` with JSON-RPC code `-32020`; legacy requests,
notifications and other revision disagreement continue through the pinned SDK.
See [upstream issue 2589][sdk-header-defect].

The local conformance registration can return the serialised verified public bundle
and individual verified records as MCP resources. Repository and catalogue text is
untrusted metadata, not instruction or authority. No resource read or tool call
causes a provider network request.

Protocol revision `2026-07-28` is stateless and has no modern `initialize` or
`initialized` exchange. Conformance therefore uses pinned version negotiation and
`server/discover`; explicit legacy `initialize` probes are rejected with `-32022`
over HTTP and STDIO.

The compiled gateway loads its direct and MCP schemas from the repository-level
canonical `schemas/` directory. It is verified in the full checkout layout;
`apps/mcp-gateway/dist/` is not claimed as a standalone distribution.

### Bounds and hostile-input boundary

- direct JSON request: 32,768 bytes; serialised direct result value: 4,194,304
  bytes;
- MCP HTTP JSON request: 65,536 bytes;
- MCP tool result, complete encoded resource response and STDIO frame buffer:
  1,048,576 bytes; individual resource text: 262,144 bytes;
- strict JSON nesting: at most 16 levels, with malformed UTF-8 or JSON, invalid
  Unicode, non-finite numbers and decoded duplicate keys rejected;
- request target: 4,096 characters; header block: 16,384 bytes; header count: 64;
- default concurrent requests: 32, with a validated constructor range of 1 to 128;
- requests per socket: 100; and
- header and request-body expiry thresholds: 5 seconds, checked every 1 second;
  keep-alive and socket inactivity: 5 seconds.

The time controls bound ingress and idle sockets. They are not evidence of a
wall-clock application execution deadline, service-level objective or durable rate
limit. MCP exact Origin rejection happens before body receipt; direct exact Origin
rejection happens after its bounded ingress read and before dispatch. Malformed or
oversized framing closes the connection after a bounded response. Admission beyond the
concurrency limit returns a face-appropriate `429` response with `Retry-After: 1`;
capacity is released after a completed or abandoned request. Shutdown is
idempotent and closes MCP state before the HTTP listener.

### Current verification state

Focused development checks exercise:

- zero default discovery and explicit registration ordering;
- exact direct/MCP schemas, successful result parity and canonical invalid-input
  problem parity;
- fresh server-generated identities independent of reused JSON-RPC IDs;
- modern raw HTTP and STDIO transcripts, legacy rejection, required headers,
  dual `Accept` media types and pinned SDK-client conformance;
- bounded complete structured results with JSON text fallback;
- public bundle and record-template resources without provider calls;
- malformed, duplicate-key and oversized JSON, ambiguous headers, Host and Origin
  rejection, concurrent admission and clean shutdown; and
- built-runtime entry points and the full-checkout canonical-schema dependency.

The exact frozen local candidate passes:

- 19 of 19 shared-contract, 20 of 20 canonical-evidence, 2 of 2
  authority-context, 6 of 6 policy-client and 86 of 86 gateway tests;
- 16 of 16 Explorer build-policy, 42 of 42 Explorer unit and component, 95 of
  95 repository Python, 2 of 2 execution-boundary and 27 of 27 real-browser tests;
- two clean byte-identical release builds at archive SHA-256
  `ff7d3e19bfbf12d610526e3e62a3fc14e6c7960a34ddbf3190eb044a74767035`,
  checksum-file SHA-256
  `ef853c93e2344ade0acbc1d86bb9fd4fa63edebb4e6b1cf0bba529f166fad595`
  and receipt SHA-256
  `878126c9d05652889e35a45e653ca084b0aacd6c12d89180e018ad21324218d6`;
- validation of 11 version manifests and locks, 15 schemas, 55 records and 3
  evaluation manifests;
- 308 local links, 183 immutable research hashes, 2 ledger snapshots and 71 source
  identifiers; a clean 516-file secret and machine-path scan; 9 diagrams; and a
  163-component CycloneDX SBOM; and
- two independent final reviews with no P0–P2 finding in the frozen
  post-remediation working tree. A separate completed security diff review also
  found no P0–P2 issue but retained its original snapshot warning. Post-snapshot
  corrections were manually reviewed and dynamically tested; the candidate commit,
  tree and attestation remain the durable identity.

Pull-request assurance, CodeQL and protected-main evidence remain pending. None of
the historical accepted evidence above accepts these candidate bytes.

Pinned SDK-client conformance is not independent major-host interoperability.
Complete non-App result values exist, but host-specific fallback, lifecycle and
usability journeys remain unverified. These are activation blockers, not deferred
documentation.

## Activation and publication boundary

No service or new public endpoint is published by any accepted or local slice. The
supported public product remains the static `v0.1.0` Explorer.

EVID-204A changed the activation reason to
`transport-and-interoperability-unverified` after adding reviewed public policy
decisions and required canonical inline result receipts. The current local slice
implements the transport and direct route code without changing that activation
document. Independent major-host interoperability, fallback and lifecycle evidence,
protected pull-request and protected-main assurance, and a separate reviewed
activation decision are still required before either operation can be advertised or
published.

The durable candidate boundary is documented in
[MCP-201 blocked transport candidate](MCP-201_GATEWAY_CANDIDATE.md).

[sdk-header-defect]: https://github.com/modelcontextprotocol/typescript-sdk/issues/2589
