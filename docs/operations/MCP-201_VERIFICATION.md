# MCP-201 verification record

- status: shared catalogue contract verified on protected `main`; inactive gateway
  candidate verified locally with pull-request evidence pending
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
registered, advertised or active. Its candidate result schema rejects an opaque
evidence reference rather than implying persistence or attestation that does not
exist.

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
- pull request: `local-candidate/pending`
- pull-request assurance and provenance: `local-candidate/pending`
- pull-request CodeQL: `local-candidate/pending`
- protected-main merge and post-merge evidence: `local-candidate/pending`

### Candidate outcome

The current local bytes add a fail-closed, checksum-verified immutable catalogue
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
deployment, provider call, policy engine or evidence store. The application code
can be tested directly, but it cannot be activated through an environment variable,
command-line option or test mode.

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

The pull request, remote CodeQL, protected-main merge and post-merge evidence remain
deliberately `local-candidate/pending` until they exist.

## Activation and publication boundary

No service or new public endpoint is published by either slice. The supported
public product remains the static `v0.1.0` Explorer.

Activation is hard-blocked as
`inline-evidence-and-public-policy-unavailable`. EVID-204 must add reviewed public
policy decisions and canonical inline result receipts to the shared application
path. A later reviewed MCP-201 change must add and test the protocol-conformant MCP
listener, direct catalogue routes, lifecycle agreement and interoperability before
either operation can be advertised or published.

The durable candidate boundary is documented in
[MCP-201 inactive gateway candidate](MCP-201_GATEWAY_CANDIDATE.md).
