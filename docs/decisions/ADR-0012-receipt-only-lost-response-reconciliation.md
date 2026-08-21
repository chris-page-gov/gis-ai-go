# ADR-0012: Receipt-only lost-response reconciliation

- status: proposed candidate; inactive
- date: 21 August 2026
- decision owner: Chris Page
- work item: [EVID-204](https://github.com/chris-page-gov/gis-ai-go/issues/22)
- base: protected `main` commit `51147e0c7af438c28bb8dc4c66c8eb7fb27d3ded`

## Context

A successful `data.query` can complete provider execution and durable evidence
persistence, then lose or truncate its response. The caller then lacks the receipt
identity required by the accepted `evidence.inspect` v1 request. Re-executing could
repeat provider work and add another ledger event; retaining a complete result for
replay would create an ungoverned result cache.

The recovery input must therefore be known before execution, work after restart,
preserve the accepted receipt and ledger bytes, and reveal only the already public
evidence record. It must not retain the caller key, parameters, observation or
result material.

## Decision

Require every explicitly mounted `data.query` transport request to use
`gis-ai-go.data-query-request.v1`. It wraps the unchanged
`gis-ai-go.data-query-parameters.v1` object with one caller-generated, non-zero
256-bit identity in the form `gis-ai-go:ik:v1:<64 lowercase hexadecimal>`.
The receipt's parameter digest continues to bind only the inner parameters.

Add a separate ledger-linked reconciliation index. It stores:

- an operation-scoped SHA-256 digest of the key;
- a semantic request fingerprint over operation, reviewed resource identity and
  the unchanged parameter digest;
- a content-addressed claim with bounded request and trace identities;
- a content-addressed resolution linking that claim to one receipt identity; and
- content-free exclusive ownership and ready markers.

The raw key, query parameters, observation and complete result are not stored in the
ledger or index. The key is a public correlation identity rather than a credential,
but the application and evidence-storage boundaries treat its complete text as
prohibited persisted or reflected material. Separate transport and host telemetry
must keep the existing digest-only contract.

The application performs an early lookup after request and caller-control checks.
A matching pending key returns receipt-free `idempotency_pending`; a matching
completed key returns receipt-free `idempotency_completed`; a different semantic
fingerprint returns `idempotency_conflict`. All three are fixed `409` problems and
perform no provider preflight or execution. Only an absent key passes policy and
provider preflight, claims ownership immediately before execution, rechecks caller
controls, and executes once.

For success, the index publishes the resolution before the exact linked ledger
persists the receipt. The application then re-reads the key and emits success only
after it verifies the completed resolution, receipt, record, event and storage
identities. A caller that lost that success uses the additive
`gis-ai-go.evidence-inspect-request.v2` key lookup. The existing v1 receipt lookup,
receipt resource URI, receipt/result schemas and content-addressed domains remain
unchanged. Inspection returns only the existing verified evidence result; it does
not replay the original `data.query` result.

## Publication and crash semantics

The index has exact private POSIX modes (`0700` directories and `0600` files) and a
canonical, symbolic-link-free root disjoint from its linked ledger. An exclusive
empty ownership marker is durable before execution. Complete canonical claim and
resolution JSON is written and synchronised before its corresponding ready marker.
The resolution ready marker is durable before ledger persistence.

A genuinely new key is admitted only while the verified index has fewer than
4,096 owned claims. Existing pending, completed and conflicting keys are resolved
before this check. Reaching the fixed local ceiling therefore publishes no ownership,
claim or ready file and does not prevent receipt recovery. Verification remains
linear in the admitted local claim count; this safety bound is not a production or
cluster quota.

An ownership marker without a ready claim, a claim without a resolution, or a
resolution without its ledger receipt is pending and blocks another execution.
`data.query` reports the pending state as `409`; `evidence.inspect` reports a known
but unverifiable state as `503 evidence_unavailable`. An absent key returns `404
evidence_not_found`. Corruption, collisions, unsafe paths, retention disagreement
and identity mismatch fail closed.

## Consequences and residual boundary

- Direct API, modern MCP HTTP and modern MCP STDIO share the wrapper, problem and
  inspection dispatchers. MCP marks a repeated call as an application error; it
  does not replay the first success.
- `data.query` may advertise `idempotentHint: true` because one governed key cannot
  repeat side effects, even though a repeat returns `409` rather than `200`.
- A module-private application brand prevents a legacy or ledger-only application
  from being mounted under the reconciled transport contract. A data-query face must
  mount an inspector closed over the exact same index.
- Direct `/data/query` ignores caller `x-request-id` and creates an opaque server
  identity. MCP identities are likewise server-generated; explicit factories are
  trusted test seams. The shared MCP ingress rejects a complete raw, prefixed,
  percent-encoded or multiply encoded key in JSON-RPC request IDs, methods, tool
  names and protocol-version claims before SDK dispatch; HTTP applies the same
  rule to its parity headers. Requests return a fixed key-free error and
  notifications remain silent. The caller key contract prohibits personal or
  secret material.
- The index coordinates the same key across processes sharing one governed index.
  It does not provide cluster-wide exactly-once execution for unrelated keys.
- One writer still owns the linked ledger. The ledger and index are not signatures,
  WORM media, external checkpoints, backups or malicious-operator defences.
- Claims are immutable. Cancellation, pre-egress rejection or an uncertain failure
  after ownership can leave a key permanently pending. The fixed 4,096-claim local
  admission ceiling bounds this candidate's filesystem growth and linear verification
  work, but provides no cluster admission, rate quota, reclamation, operator resolution
  or retention-disposal process. It is not sufficient for production activation.
- Production registrations, discovery, activation gates and readiness remain empty
  or false. No live provider, tunnel, host, deployment or release is authorised by
  this decision.
