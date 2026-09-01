# ADR-0015: Provider-free loopback local candidate

- status: accepted
- date: 1 September 2026
- decision owner: Chris Page
- release target: unreleased `v0.2.0` local candidate

## Context

Protected `main` contains the governed exact-five MCP assembly, but the ordinary
HTTP and STDIO entrypoints deliberately mount no tools. The fixed container is an
assurance and later-deployment candidate rather than a simple first run from a
fresh checkout. A contributor can run the one-shot local demonstration, but another
MCP client cannot remain connected to it.

People need a reproducible way to clone the repository and explore the complete
provider-independent `v0.2.0` candidate before a public runtime, hostname and Azure
budget are authorised. Making the generic or production entrypoints configurable
would weaken their existing fail-closed boundary.

## Decision

Supply one separately named launcher, `./scripts/start-local-candidate`, for an
explicit provider-free local evaluation. It must:

- bind only to `127.0.0.1:8787` and expose MCP Streamable HTTP at `/mcp`;
- mount exactly `catalogue.search`, `catalogue.describe`, `evidence.inspect`,
  `selection.resolve` and `data.query`, with the matching three MCP resources;
- use the reviewed, checksum-bound catalogue material, one deterministic in-memory
  HTTP `503` and the exact byte-verified approved T04 cache, with no live-provider
  fallback and `read-approved-provider-cache` recorded in the receipt;
- require, read and use no provider credential, and give its provider execution no
  DNS, socket, HTTPS or fetch transport seam;
- use owner-only temporary ledger and reconciliation state for one running session;
- remove that temporary state after an orderly `SIGINT` or `SIGTERM`; and
- identify itself as `candidate-unregistered`, with production registration false,
  `provider_egress: false`, provider observation
  `deterministic-in-memory-http-503` and data-query source
  `byte-verified-approved-cache`.

The launcher is a closed assembly, not a general activation switch. It accepts no
operation list, provider URL, provider credential, public binding, production
registration or evidence-store override. The shipped generic HTTP, generic STDIO
and production/default operation arrays remain empty and blocked.

The local candidate may serve the direct API contract generated from the same
assembly, but MCP and direct API discovery must remain identical. Readiness is
`200` only while the exact-five assembly and its session-local evidence
dependencies pass their checks. Health does not substitute for readiness.

## Evidence and release boundary

Repository acceptance must prove a clean checkout can install locked dependencies,
start the loopback candidate, receive `200` from `/healthz` and `/readyz`, discover
exactly five tools and three resources, complete the fixed five-operation journey,
observe the approved-cache warning, status and receipt transformation after the
deterministic outage, and stop without changing tracked files.

The prospective shared warning and its schema remain byte-for-byte unchanged because
historical QUAL-206 evidence binds that schema digest. In this local profile its
“ONS request failed” wording refers to the injected in-memory `503`, not a live
network request. The lifecycle provenance above removes that ambiguity without
rewriting historical receipts.

This decision does not change the supported-release boundary. `v0.1.0` remains the
latest supported public release until the existing `v0.2.0` gates pass. In
particular, the local candidate does not prove current provider data, public HTTPS,
identity, shared durable storage, monitoring, remote interoperability, deployment,
rollback, registry publication or production activation. It must not cause a
`v0.2.0` tag or release to be published by itself.

The fixed in-memory outage transport is not an operating-system network sandbox.
Dependency installation may use the package registry, and this decision does not
claim that the Node.js process is incapable of every possible network operation.
Session receipts disappear after an orderly stop and are not evidence of restart
recovery, backup or durable service operation.
If state removal fails, the launcher must emit the fixed path-free
`local_candidate_cleanup_failed` event, return a failure status and leave its process
exit hook able to retry deletion.
The approved cache remains admissible only until its recorded `stale_after` time;
the local `data.query` must fail closed after that boundary until a separately
reviewed cache replaces it.

## Consequences

- A colleague can evaluate the whole exact-five candidate from a clean clone on one
  machine without Azure, a provider account or a public hostname.
- Local MCP clients gain a stable loopback endpoint without opening a public
  listener or weakening production activation controls.
- The one-shot STDIO demonstration remains useful for its separate real-pipe and
  deterministic journey evidence.
- Azure or another authorised runtime remains necessary for the public TLS,
  workload identity, governed egress and storage, operational and rollback evidence
  required by the supported `v0.2.0` release.
