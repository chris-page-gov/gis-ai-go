# MCP-201 blocked transport candidate

- status: local candidate; acceptance, activation and publication blocked
- work item: [MCP-201](https://github.com/chris-page-gov/gis-ai-go/issues/19)
- protected-main base: `997d5fdd478797b20b05d1980be8f986645d410e`
- supported public product: immutable
  [`v0.1.0`](https://github.com/chris-page-gov/gis-ai-go/releases/tag/v0.1.0)
- current activation block: `transport-and-interoperability-unverified`

## Purpose

This local slice adds MCP 2026-07-28 HTTP and STDIO transports and direct HTTP
`catalogue.search` and `catalogue.describe` routes over the already accepted shared
application. The MCP and direct faces use the same canonical request and result
schemas, policy decisions and inline evidence receipts.

The implementations are available only through explicit constructor options used
for local conformance and embedding tests. The production activation document
still contains empty MCP-tool and direct-API arrays, MCP resources default to none,
the shipped HTTP and STDIO entry points supply no override, and readiness remains
`503`. There is no environment-variable or command-line activation path.

## Candidate boundary

The checksum-verified catalogue loader:

- accepts an absolute, canonical directory only and follows no symbolic link;
- streams directory entries so file and directory limits apply before a complete
  listing is materialised;
- bounds total bytes, individual control files and relative path lengths, reads no
  more than the recorded file length plus one byte, and rechecks the same file's
  identity and metadata after reading;
- requires the generated marker and an exact checksum-ledger match for the complete
  inventory;
- verifies every payload digest and cross-checks the manifest, build receipt,
  content root, record order and public discovery bundle identity; and
- rejects the complete load on any ambiguity, returning no partial catalogue.

The resulting catalogue and record index are immutable for the life of the
application. Staleness is reported as a warning: the candidate does not silently
represent a governed snapshot as current source authority.

The transport-neutral application implements deterministic
`catalogue.search` and `catalogue.describe` functions. Both transports and the
direct API call that same application, which uses:

- closed request, result and problem envelopes;
- bounded Unicode query analysis, facet arrays, page sizes, cursors and record IDs;
- fail-closed validation that every snapshot can fit the narrower public result
  schema without truncation or semantic reinterpretation;
- stable sorting and catalogue-native source relationships; and
- opaque deterministic cursors bound to the exact catalogue content root and
  normalised search criteria; and
- after the bounded EVID-204A follow-up, a server-owned anonymous-open authority,
  compiled default-deny public policy and required canonical inline receipt on
  every successful result.

Cursor digests detect corruption and misuse across catalogue or query boundaries.
They are not an authentication mechanism and convey no authority.

## Local HTTP surface

The supplied HTTP executable binds to `127.0.0.1:8787`. The server factory does not
choose a bind address, so an embedding caller remains responsible for preserving
that local-only boundary. The default executable exposes:

| Method and path | Status | Meaning |
| --- | ---: | --- |
| `GET /healthz` | `200` | The process has loaded a verified catalogue snapshot. |
| `GET /readyz` | `503` | Activation is blocked; active tool and API lists are empty. |
| `GET /openapi.json` | `200` | The exact default contract, with no catalogue operation path. |
| `/mcp` | protocol-defined | Modern MCP HTTP transport with zero default tools and resources. |

`POST /catalogue/search` and `POST /catalogue/describe` exist in the application
handler and appear in OpenAPI only when the exact operations are selected through
the explicit constructor seam. They remain absent from the default executable.
The same seam can register the two MCP tools for conformance. It is not a production
activation mechanism.

The Node ingress requires one unambiguous Host header and rejects duplicate
singleton transport headers and any `Transfer-Encoding` before body receipt. MCP
hostname and exact Origin allow-lists are also enforced before body receipt. Direct
exact Host and Origin checks run after its bounded ingress read but before route or
application dispatch. No surface accepts wildcard cross-origin access. Direct JSON
bodies are limited to 32,768 bytes and the serialised direct result value to
4,194,304 bytes. MCP HTTP JSON bodies are limited to 65,536 bytes. The shared strict
parser rejects malformed UTF-8 or JSON, decoded duplicate object keys, invalid
Unicode values, non-finite numbers and nesting beyond 16 levels. Malformed or
oversized framing closes the connection after its bounded error response.

The listener limits request targets to 4,096 characters, header blocks to 16,384
bytes and 64 headers, 100 requests per socket and 32 concurrent requests by
default; the constructor accepts a tested range from 1 to 128. Header and
request-body expiry thresholds are 5 seconds and are checked every 1 second;
keep-alive and socket-inactivity timeouts are 5 seconds. These are ingress and
idle controls, not an end-to-end application execution deadline, service-level
objective or durable rate limit. Admission beyond the
concurrency bound returns a face-appropriate `429` response and `Retry-After: 1`,
then recovers when an admitted request finishes or is abandoned.

## MCP transport and resources

The candidate supports only protocol revision `2026-07-28`; legacy MCP is rejected.
HTTP callers must send both `application/json` and `text/event-stream` in `Accept`.
That revision is stateless and has no `initialize` or `initialized` exchange. Local
evidence uses pinned version negotiation and `server/discover`; legacy `initialize`
requests are rejected with `-32022` over HTTP and STDIO.
The pinned `@modelcontextprotocol/server` 2.0.0 handler has a
[published missing-version-header defect][sdk-header-defect]. A narrow pre-handler
shim rejects only a modern POST whose body declares `2026-07-28` while the required
`MCP-Protocol-Version` header is absent. Other protocol-version disagreement is
left to the pinned SDK.

STDIO uses the same server factory and legacy rejection with a 1,048,576-byte
framing buffer. MCP tool results contain the complete canonical result in both
`structuredContent` and a JSON text fallback; the combined encoded result is
limited to 1,048,576 bytes. The Node server's idempotent shutdown closes MCP state
before it stops the HTTP listener.

Explicit local conformance activation can expose the serialised, already verified
public bundle at `gis-ai-go://catalogue/public` and individual records through
`gis-ai-go://catalogue/records/{record_id}`. Each resource text is limited to
262,144 bytes and its complete encoded MCP response to 1,048,576 bytes. Resource
registration is separate from tool activation and is empty by default.

Catalogue descriptions, titles, links and other record fields remain untrusted
metadata. The gateway returns them as data; they are not instructions, authority or
permission to fetch a provider. Neither resource reads nor tool calls make a
provider network request.

## Packaging and supported-product boundary

The direct OpenAPI and MCP schema advertisements are generated from the same
repository-level canonical schema files. The compiled gateway therefore depends on
the full checkout layout retaining `schemas/`; `apps/mcp-gateway/dist/` is not a
standalone package.

This candidate has no public deployment, service URL or registry entry; provider
adapter or provider call; external policy decision point, OPA or identity
integration; durable rate service; or evidence store, ledger, lookup or
attestation. The static Explorer remains the only supported public product and has
no dependency on this process.

## Activation gate

The production activation value remains frozen with zero active MCP tools and zero
active direct-API operations; resources also default to zero. The constructor seam
does not change the frozen activation document and is not used by either executable.

Raw transcript and pinned SDK-client conformance can establish the protocol shape,
but they do not prove interoperability with independent major MCP hosts. Complete
non-App result representations exist in the candidate, but host-specific fallback,
lifecycle and usability evidence is still pending. The complete locked local gate
and independent reviews now pass, but protected pull-request checks, an explicit
reviewed activation decision and deployment rollback evidence must also pass before
activation or publication. Until then, the supported capability list remains empty.

See the [MCP-201 verification record](MCP-201_VERIFICATION.md) and
[EVID-204A evidence boundary](EVID-204_INLINE_EVIDENCE.md) for the distinction
between merged capability foundations and inactive follow-up work.

[sdk-header-defect]: https://github.com/modelcontextprotocol/typescript-sdk/issues/2589
