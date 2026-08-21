# TOOLS-205 inactive data query application

Reviewed on 21 August 2026.

This record preserves the application-only boundary at the time it was accepted and
documents the later inactive lost-response reconciliation extension. The explicitly
mounted local-conformance transport candidate is recorded in
[`TOOLS-205_PUBLIC_READ_TRANSPORT.md`](TOOLS-205_PUBLIC_READ_TRANSPORT.md). Neither
extension changes the original slice's historical activation or publication claims.

## Outcome and boundary

This slice implements the transport-neutral application function for the exact
public ONS `data.query` selected by the accepted public-read v2 contracts. It does
not add an HTTP route, MCP tool, MCP resource, OpenAPI operation, registry
implementation state, activation override, shipped adapter configuration, public
listener or deployment. Production and default capability arrays remain empty.

`createDataQueryApplication()` has no default adapter and reads no environment
variable. Its caller must explicitly inject an `OnsDataApiAdapter` instance and an
exact gateway software identity. The adapter's invocation lifecycle plane must be
active. Its discovery plane may remain suspended because this application neither
lists providers nor changes capability advertising. Discovery-active with
invocation-suspended still fails before provider transport.

The legacy unmounted application-only seam accepts the closed five-key
`gis-ai-go.data-query-parameters.v1` object. A transport-mountable reconciled
application requires the exact linked evidence ledger and reconciliation index, and
accepts only this additive wrapper:

```json
{
  "schema": "gis-ai-go.data-query-request.v1",
  "idempotency_key": "gis-ai-go:ik:v1:<64 lowercase hexadecimal>",
  "parameters": { "schema": "gis-ai-go.data-query-parameters.v1" }
}
```

The non-zero 256-bit key is generated and retained by the caller. The complete
parameters object remains the unchanged five-key contract and binds:

- the exact accepted public-read resource identity;
- ONS dataset `weekly-deaths-region`, edition `time-series`, version `121`;
- native selection order `time`, `geography`, `week`, `causeofdeath` with the four
  reviewed options; and
- one observation.

A different value, order, property or shape fails before adapter execution. The
application accepts no URL, query string, credential, provider choice, wildcard,
SQL, lifecycle setting or output bound from the caller. The receipt parameter digest
continues to cover only the inner parameters, so accepted receipt bytes and meaning
are not widened by the recovery wrapper.

Mounted direct HTTP ignores caller `x-request-id` for `/data/query` and creates an
opaque server request identity; mounted MCP uses a server-created context. Explicit
identity factories are trusted test seams. The application context is therefore a
server-owned input, while the public key contract requires callers not to encode
personal or secret material in the key.

## Execution order

Every new reconciled call follows one fixed order:

1. detach and compare the exact wrapper, five-key parameters, context and optional
   execution controls;
2. check the caller signal and absolute deadline using the application's trusted
   clock, with cancellation taking precedence;
3. derive the operation-scoped key digest and semantic fingerprint, then inspect the
   index before policy or provider preflight. A different fingerprint returns
   `idempotency_conflict`; pending returns `idempotency_pending`; completed returns
   `idempotency_completed`;
4. only for an absent key, evaluate and verify the server-owned anonymous-open
   authority, checked
   default-deny v2 policy, per-call allow decision and exact public-read resource;
5. require an invocation-active health record, independently compare the adapter's
   upper-bound estimate, OGL rights and provenance with the accepted resource;
6. recheck caller controls, publish exclusive key ownership and a complete canonical
   claim, recheck controls again, then call the explicitly injected adapter's
   `execute()` exactly once with the shared
   cancellation signal and absolute RFC 3339 deadline;
7. recheck caller controls in the execution rejection path before mapping an adapter
   error, and immediately after a resolved execution before validating its result;
8. independently detach and check the returned provider, adapter, dataset, edition,
   version URI, native dimension order, one 15-digit-or-smaller integer string,
   `unit: null`, empty ONS Data Marking, OGL rights, provenance and 256 KiB
   canonical-result ceiling;
9. project the receipt-free result core, construct a public-read v2 receipt and
   immediately verify it with the full parameter, result, policy, authority,
   decision, resource and software material; and
10. publish and synchronise the receipt-only resolution, persist and re-verify the
    receipt in the exact linked ledger, then re-read completion and compare the
    receipt, resolution, record, event and storage identities before adding
    `evidence_storage` and returning the first success.

There is no provider call during policy, health, estimate, rights or provenance
failure. An evidence-clock, receipt-verification or storage failure returns no
success result, receipt, ledger record or ledger event. A cancelled signal or
elapsed caller deadline also returns no result, receipt, record or event. Once
exclusive ownership has been published, however, any cancellation, adapter failure
or uncertain evidence failure leaves that immutable key pending. It is not released
for another execution. Neither the abort reason nor the deadline value can appear in
a problem.

## Results and problems

The success shape is `gis-ai-go.data-query-result.v1`. It contains one
numeric-string observation with a `null` unit, the fixed evidence binding and a
fully verified `gis-ai-go.evidence-receipt.v2`. The receipt preserves the reviewed
profile hash, provider and adapter identity, dataset version, dimension order,
rights, attribution and byte/attempt limits. Durable storage remains optional only
for the unmounted legacy application seam. A transport-mountable reconciled instance
requires the exact ledger and index, and every successful response includes verified
`evidence_storage`.

Ordinary failures retain the byte-identical `gis-ai-go.data-query-problem.v1` and
exactly one of ten codes:

- `invalid_request`;
- `query_cancelled`;
- `query_deadline_exceeded`;
- `policy_denied`;
- `provider_suspended`;
- `provider_rate_limited`;
- `provider_timeout`;
- `provider_unavailable`;
- `provider_contract_failed`; or
- `evidence_unavailable`.

`query_cancelled` and `query_deadline_exceeded` are fixed `408` problems owned by
the caller-control plane. Cancellation wins when both controls have ended.
`provider_timeout` remains a `504` only for an adapter or provider-local timeout
while the external signal and deadline are still live.

Reconciliation failures use the distinct
`gis-ai-go.data-query-reconciliation-problem.v1` contract. Its three fixed codes all
have status `409`:

- `idempotency_pending` for a key whose ownership or durable completion is not yet
  verifiable;
- `idempotency_completed` for a key already linked to verified durable evidence;
  and
- `idempotency_conflict` for reuse against a different semantic fingerprint.

The closed `data-query-operation-problem.schema.json` dispatcher accepts either
problem version. It does not relabel the widened operation contract as v1. Every
reconciliation problem is receipt-free and cannot reflect the raw key or its digest.

Problem titles, details, types and status values are fixed. They cannot represent
an adapter error message, provider status, payload, path, stack, credential,
parameter/result material or evidence receipt. Adapter failures are normalised and
checked before this closed non-reflective mapping.

## Public API and contracts

The gateway package exports:

- `PUBLIC_ONS_DATA_QUERY_PARAMETERS`;
- `createDataQueryApplication()`;
- `DataQueryApplication`, `DataQueryApplicationOptions` and
  `DataQueryInvocationOptions`;
- `DataQueryParameters`, `DataQueryRequest`, `DataQueryResultCore` and
  `DataQueryResult`;
- `isReconciledDataQueryApplication()` as the module-private identity-backed
  transport-coherence predicate and `haveExactlyLinkedReconciliationApplications()`
  for the mandatory data/inspection pair; and
- `DATA_QUERY_PROBLEM_CODES`, `DATA_QUERY_RECONCILIATION_PROBLEM_CODES`,
  `DataQueryProblem`, `DataQueryReconciliationProblem` and
  `DataQueryApplicationError`.

The promoted schemas and examples are:

- [`data-query-parameters.schema.json`](../../schemas/data-query-parameters.schema.json)
  and
  the promoted `data-query-parameters.example.json` fixture;
- [`data-query-request.schema.json`](../../schemas/data-query-request.schema.json)
  and
  [`data-query-request.example.json`](../../providers/fixtures/data-query-request.example.json);
- [`data-query-result.schema.json`](../../schemas/data-query-result.schema.json) and
  [`data-query-result.example.json`](../../providers/fixtures/data-query-result.example.json);
  and
- [`data-query-problem.schema.json`](../../schemas/data-query-problem.schema.json)
  and
  [`data-query-problem.example.json`](../../providers/fixtures/data-query-problem.example.json),
  [`data-query-cancelled-problem.example.json`][cancelled-problem]
  and
  [`data-query-deadline-exceeded-problem.example.json`][deadline-problem]; and
- [`data-query-reconciliation-problem.schema.json`](../../schemas/data-query-reconciliation-problem.schema.json)
  plus the closed
  [`data-query-operation-problem.schema.json`](../../schemas/data-query-operation-problem.schema.json)
  dispatcher and pending, completed and conflict fixtures.

[cancelled-problem]: ../../providers/fixtures/data-query-cancelled-problem.example.json
[deadline-problem]: ../../providers/fixtures/data-query-deadline-exceeded-problem.example.json

The successful fixture retains the already documented public aggregate scalar
`10471` solely to reproduce the complete application result and receipt. It is not
a stored provider response, fresh live observation or activation claim.

## Remaining gates

This application still cannot be called through a shipped product. Local direct API
and modern MCP HTTP/STDIO parity, receipt-only restart recovery and the suspended
registry profile are implemented, but every production/default registration and
activation gate remains empty or false. Approved fallback, live independent-host
evidence, accessibility, release assurance, deployment security and rollback still
require separate review before activation. No live ONS call is used or required for
this inactive reconciliation assurance.

The guarantee is deliberately narrow: one caller key cannot repeat provider work
when all contenders share one governed index, and the linked ledger has one writer.
There is no result cache, result replay, unrelated-key multi-writer coordination or
cluster-wide exactly-once claim.
