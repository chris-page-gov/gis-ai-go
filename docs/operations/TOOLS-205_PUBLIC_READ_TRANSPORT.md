# TOOLS-205 inactive public-read transport candidate

Reviewed on 21 August 2026.

## Outcome and publication boundary

This candidate gives the accepted `selection.resolve` and `data.query`
applications equivalent explicit local-conformance faces over the direct JSON API,
modern MCP HTTP and canonical modern MCP STDIO. It also proves that receipts newly
persisted by either application can be inspected through the existing
`evidence.inspect` tool and `evidence.receipt` resource.

Nothing is activated or deployed. All constructor defaults still register no API
operation, MCP tool or MCP resource. The production HTTP and STDIO entrypoints do
not inject either application, the production activation document is unchanged,
readiness remains `503`, and the current callable registry is the empty frozen
array. There is no environment or command-line activation override and no live ONS
call in the assurance suite.

## Explicit transport matrix

| Application | Direct JSON API | Modern MCP HTTP | Modern MCP STDIO |
| --- | --- | --- | --- |
| `selection.resolve` | `POST /selection/resolve` | `tools/call` | `tools/call` |
| `data.query` | `POST /data/query` | `tools/call` | `tools/call` |
| `evidence.inspect` | `POST /evidence/inspect` when separately mounted | `tools/call` | `tools/call` |
| persisted receipt | not a separate direct route | `gis-ai-go://evidence/receipts/{receipt_id}` | the same resource URI |

Each face requires the exact application instance to be injected and the exact
operation or resource name to be enabled. The direct face returns the canonical
JSON success or problem. MCP success and application problems return the same
object in `structuredContent` and the byte-identical compact JSON in the text
content block. The MCP tool marks an application problem with `isError: true`.
The canonical STDIO server remains modern-only at MCP `2026-07-28`.

The OpenAPI document embeds closed request, result and problem schemas for both
new direct operations. Every `$ref` is document-local: path responses refer to
`#/components/schemas/...`, while embedded schemas refer to their own local
`#/$defs/...`. The selection path records statuses `200`, `400`, `404`, `406`,
`409`, `422`, `429`, `500` and `503`; the data path records `200`, `400`, `403`,
`406`, `408`, `429`, `500`, `502`, `503` and `504`.

The separately named legacy `2025-06-18` conformance factory remains structurally
catalogue-only. It rejects evidence, selection and data tool or resource
registration. No legacy script or shipped entrypoint changes.

## Cancellation, deadlines and timeouts

The Node ingress uses separate bounded time planes:

- headers, request bodies and keep-alive: 5 seconds;
- the ONS adapter's complete call ceiling: 20 seconds, exported as
  `ONS_CALL_DEADLINE_MS`; and
- gateway socket inactivity headroom: 25 seconds.

Node `server.setTimeout()` is an inactivity guard, not an absolute processing or
socket-lifetime deadline. Its 25-second headroom is deliberately greater than the
adapter's absolute 20-second call ceiling, so the adapter can return a controlled
result before an inactive socket is destroyed. Tests compare these constants and
use controlled transports rather than waiting 20 seconds.

For a direct API call, the Node request and response lifecycle is bridged into the
Fetch `Request.signal` used by `data.query`. Listeners are installed before the
initial destroyed-state check and removed after settlement. A completed request
body is not treated as cancellation; a request abort, destroyed request, destroyed
response or response close before `writableEnded` is. A response close after a
completed write is not.

For MCP HTTP, the pinned SDK owns the Node-to-Fetch signal. SDK 2.0.0 otherwise
turns an aborted Fetch request into HTTP `499`, even after `data.query` constructs
its closed `query_cancelled` result. A narrow compatibility seam therefore applies
only after strict validation of a modern `POST` `tools/call` for `data.query`, with
the exact protocol, method and name headers and a bounded request ID. It combines
the original caller signal with the SDK handler signal for the application while
giving only the SDK response lifecycle a fresh signal. Invalid, header-mismatched,
legacy and non-data requests retain the SDK's pinned behaviour. Async-local signal
state is isolated between concurrent requests and listeners are removed after use.
Canonical STDIO uses the raw SDK cancellation signal.

Real loopback listener tests close both a direct data socket and an MCP data socket
after adapter execution starts. Both cancellations reach the adapter and produce
no ledger event. In-process direct and MCP tests prove `query_cancelled`. A modern
STDIO `notifications/cancelled` message stops the adapter; neither the notification
nor the now-abandoned original request produces a wire response, while internal
application settlement proves cancellation and zero evidence. Caller cancellation
and caller deadline expiry remain fixed `408` application problems. An adapter or
provider-local timeout remains `504 provider_timeout`.

## Evidence and registry state

Selection and data successes take the same verified durable-ledger path as their
application functions. Assurance persists one result through each application,
then verifies exact parity among the application result's `evidence_storage`,
direct ledger inspection, modern `evidence.inspect` structured and text results,
and the corresponding `evidence.receipt` resource. Cancellation and all problem
paths write no evidence.

Registry profiles T03 and T04 now describe implemented but suspended candidates.
Discovery is false, all seven activation gates are false and the current callable
list remains empty. Their schema references, current provider dependencies,
controlled errors, non-spatial CRS state and bounded inline cursor state are
validated against substitution. T03's non-executing required-choice fallback is
implemented. T04's approved-cache or alternate-provider fallback remains
`not-implemented`, so its fallback activation gate remains false.

`data.query` has `readOnlyHint: true`, `openWorldHint: true` and
`idempotentHint: false`. A repeat can make another provider attempt and persist
another ledger event.

## Threat and residual boundary

The transport accepts bounded JSON only. It preserves the existing exact Host and
Origin checks, rejects ambiguous headers and transfer encoding, does not accept a
caller URL or credential, and returns closed non-reflective problems. The tests use
controlled fake provider transports, fixed clocks and temporary ledgers; they do
not contact ONS or expose provider bodies, credentials or local ledger paths.

`HOST-015` remains explicitly unresolved and expected-failing. If a success response
is lost after evidence persistence, the caller does not know its receipt ID. There
is no request idempotency key, governed result store, receipt lookup by request, or
result replay. `evidence.inspect` can verify a known receipt ID but cannot recover
one lost with the response. This candidate therefore makes no exactly-once,
at-most-once reconciliation or replay claim.

Public activation still requires a separately reviewed release and activation
decision, independent-host interoperability, T04 fallback, deployment security,
accessibility and operational rollback evidence. The OpenAPI description records
those remaining gates rather than claiming a public service.

## Reproducible local verification

From a clean repository checkout with the locked Node and Python dependencies:

```bash
pnpm install --frozen-lockfile
uv sync --locked
pnpm --filter @gis-ai-go/mcp-gateway run test
pnpm --filter @gis-ai-go/tool-registry run test
pnpm run validate:public-read-v2
pnpm run validate:contracts
pnpm run validate:links
pnpm run test:interoperability
pnpm run check
```

The focused gateway test is
`apps/mcp-gateway/test/public-read-transport.test.ts`. It covers the complete
success/problem matrix, hostile registration and request cases, local OpenAPI
references, durable evidence parity, direct/MCP/STDIO cancellation, real listener
disconnects, registry absence by default and the catalogue-only legacy boundary.
