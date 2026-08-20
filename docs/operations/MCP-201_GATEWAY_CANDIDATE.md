# MCP-201 inactive gateway candidate

- status: local candidate; activation and publication blocked
- work item: [MCP-201](https://github.com/chris-page-gov/gis-ai-go/issues/19)
- protected-main base: `e5e6d4db5ac7036198cde64279e815f214f3defd`
- supported public product: immutable
  [`v0.1.0`](https://github.com/chris-page-gov/gis-ai-go/releases/tag/v0.1.0)
- activation block: `inline-evidence-and-public-policy-unavailable`

## Purpose

This slice establishes the smallest fail-closed application and process boundary
needed before introducing an MCP transport or catalogue API. It can verify and load
the canonical public catalogue, execute deterministic search and description in
process, and report that the gateway is deliberately not ready.

It does not make either catalogue operation available to a client. The presence of
application code is not evidence of an active tool or API operation.

## Candidate boundary

The checksum-verified catalogue loader:

- accepts an absolute, canonical directory only and follows no symbolic link;
- bounds the number of files and directories, total bytes, individual control
  files and relative path lengths;
- requires the generated marker and an exact checksum-ledger match for the complete
  inventory;
- verifies every payload digest and cross-checks the manifest, build receipt,
  content root, record order and public discovery bundle identity; and
- rejects the complete load on any ambiguity, returning no partial catalogue.

The resulting catalogue and record index are immutable for the life of the
application. Staleness is reported as a warning: the candidate does not silently
represent a governed snapshot as current source authority.

The transport-neutral application implements deterministic in-process
`catalogue.search` and `catalogue.describe` functions. It uses:

- closed request, result and problem envelopes;
- bounded Unicode query analysis, facet arrays, page sizes, cursors and record IDs;
- stable sorting and catalogue-native source relationships; and
- opaque deterministic cursors bound to the exact catalogue content root and
  normalised search criteria.

Cursor digests detect corruption and misuse across catalogue or query boundaries.
They are not an authentication mechanism and convey no authority.

## HTTP surface

The local candidate binds to `127.0.0.1:8787` only. Its complete surface is:

| Method and path | Status | Meaning |
| --- | ---: | --- |
| `GET /healthz` | `200` | The process has loaded a verified catalogue snapshot. |
| `GET /readyz` | `503` | Activation is blocked; active tool and API lists are empty. |
| `GET /openapi.json` | `200` | The exact inactive-candidate contract. |

The listener accepts only explicit loopback Host and same-origin Origin values,
does not emit wildcard cross-origin permissions, rejects request bodies and applies
bounded URL, header, request and keep-alive settings. The OpenAPI document contains
no catalogue operation path.

## Capabilities that do not exist

This candidate has no:

- HTTP search or description route;
- MCP listener, discovery response or tool registration;
- public deployment, public service URL or registry entry;
- provider adapter or provider network call;
- public policy decision point, identity integration or rate service; or
- canonical evidence store or reviewed inline result receipt.

The static Explorer remains the only supported public product. It does not depend
on this process.

## Activation gate

The production activation value is frozen with zero active MCP tools and zero
active direct-API operations. It has no environment-variable, command-line or test
escape hatch.

EVID-204 must provide reviewed public policy decisions and canonical inline
evidence receipts on the shared application path. A later pull request must then
add and verify the protocol-conformant MCP listener, direct catalogue routes,
matching lifecycle discovery, malicious-input controls and client
interoperability. Only that reviewed change may replace the block and advertise a
catalogue capability.

See the [verification record](MCP-201_VERIFICATION.md) for the distinction between
protected-main evidence and pending local-candidate evidence.
