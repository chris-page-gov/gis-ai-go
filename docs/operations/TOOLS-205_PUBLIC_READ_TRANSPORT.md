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
operation or resource name to be enabled. A mounted `data.query` additionally
requires `evidence.inspect` on the same face. Module-private index identities prove
that both applications close over the exact same ledger-linked reconciliation
index; separate, legacy or proxy-wrapped instances are rejected at construction.
The direct face returns the canonical JSON success or problem. MCP success and
application problems return the same object in `structuredContent` and the
byte-identical compact JSON in the text content block. The MCP tool marks an
application problem with `isError: true`. The canonical STDIO server remains
modern-only at MCP `2026-07-28`.

The mounted data request is `gis-ai-go.data-query-request.v1`: exactly a non-zero
caller-generated 256-bit `idempotency_key` plus the unchanged v1 parameters. Direct
HTTP ignores `x-request-id` on `/data/query` and generates an opaque server request
identity; MCP already generates its context internally. Explicit identity factories
are trusted test seams only. The raw key is a public correlation label, not a
credential, but callers must not encode personal or secret material in it. Shared
MCP HTTP and STDIO ingress rejects a raw, prefixed, percent-encoded or multiply
encoded complete key in a JSON-RPC request ID, method, tool name or
protocol-version claim before SDK dispatch. HTTP applies the same rule to the
corresponding parity headers. The fixed request reply uses `id: null`; ordinary
bounded protocol controls retain their behaviour, while HTTP notifications receive
an empty `202` acknowledgement and STDIO notifications produce no frame.

The OpenAPI document embeds closed request, result and problem schemas for both
new direct operations. Every `$ref` is document-local: path responses refer to
`#/components/schemas/...`, while embedded schemas refer to their own local
`#/$defs/...`. The selection path records statuses `200`, `400`, `404`, `406`,
`409`, `422`, `429`, `500` and `503`; the data path records `200`, `400`, `403`,
`406`, `408`, `409`, `429`, `500`, `502`, `503` and `504`. The data operation's
problem schema is a closed dispatcher over the unchanged ten-code v1 problem and a
separate three-code reconciliation problem.

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
application settlement proves cancellation and no receipt, record or ledger event.
Once key ownership is durable, these paths can leave an immutable pending claim; no
second execution is allowed for that key. Caller cancellation and caller deadline
expiry remain fixed `408` application problems. An adapter or provider-local timeout
remains `504 provider_timeout`.

## Evidence and registry state

Selection and data successes take the same verified durable-ledger path as their
application functions. Assurance persists one result through each application,
then verifies exact parity among the application result's `evidence_storage`,
direct ledger inspection, modern `evidence.inspect` structured and text results,
and the corresponding `evidence.receipt` resource. Cancellation and all problem
paths write no receipt, ledger record or event, although a failure after ownership
can leave the reconciliation key pending.

Registry profiles T03, T04 and T11 describe implemented but suspended candidates.
Discovery is false, all seven activation gates are false and the current callable
list remains empty. T04 uses the wrapper and closed operation-problem dispatcher;
T11 uses the closed v1/v2 inspect-request dispatcher and accepted catalogue problem
schema. Their current provider dependencies,
controlled errors, non-spatial CRS state and bounded inline cursor state are
validated against substitution. T03's non-executing required-choice fallback is
implemented. T04's approved-cache or alternate-provider fallback remains
`not-implemented`; T11 likewise has no alternate receipt, result replay or challenge
route. Their fallback activation gates remain false.

`data.query` has `readOnlyHint: true`, `openWorldHint: true` and
`idempotentHint: true`. The key is part of the arguments and cannot repeat provider
or ledger side effects. A repeat does not replay success: it returns receipt-free
`idempotency_pending`, `idempotency_completed` or `idempotency_conflict` with status
`409`; completed evidence is retrieved separately through `evidence.inspect` v2.

## Threat and residual boundary

The transport accepts bounded JSON only. It preserves the existing exact Host and
Origin checks, rejects ambiguous headers and transfer encoding, does not accept a
caller URL or credential, and returns closed non-reflective problems. The tests use
controlled fake provider transports, fixed clocks and temporary ledgers; they do
not contact ONS or expose provider bodies, credentials or local ledger paths.

`QUAL-206-HOST-015` now passes one deterministic, non-live application-level case.
The first result is deliberately dropped only after verified persistence, fresh
ledger/index/application instances reopen, the retry returns completed `409` before
provider preflight, and `evidence.inspect` v2 recovers the original receipt. The
fixture proves exactly one provider execution, record and event and no result replay.
It remains unscored, supplies no live-host evidence and activates nothing.

The guarantee is limited to a governed key shared through one index and a
single-writer ledger. Claims are immutable. Cancellation, pre-egress adapter
rejection or an uncertain post-ownership failure can leave a key permanently
pending. The index now refuses a genuinely new key before publication at 4,096
owned claims and
reuses one verified index and ledger snapshot per steady lookup. The linked ledger
also refuses a new receipt before either write at its accepted event ceiling. These
local bounds preserve at-cap recovery and bound individual linear work; they are not
cluster admission or a deployment quota. This candidate supplies no reclamation,
operator resolution, retention disposal or general unrelated-key multi-writer
coordination.

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
references, exact-linked recovery construction, server-owned direct request IDs,
durable evidence parity, completed-retry and v2-inspection parity,
direct/MCP/STDIO cancellation, real listener disconnects, registry absence by
default and the catalogue-only legacy boundary. The separately named
`QUAL-206-HOST-015` test performs the fault-drop, fresh-instance restart and
receipt-only recovery sequence; `pnpm run test:interoperability` executes it.
