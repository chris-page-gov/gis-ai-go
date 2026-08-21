# TOOLS-205 inactive data query application

Reviewed on 21 August 2026.

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

The only accepted request is the closed five-key
`gis-ai-go.data-query-parameters.v1` object. It binds:

- the exact accepted public-read resource identity;
- ONS dataset `weekly-deaths-region`, edition `time-series`, version `121`;
- native selection order `time`, `geography`, `week`, `causeofdeath` with the four
  reviewed options; and
- one observation.

A different value, order, property or shape fails before adapter execution. The
application accepts no URL, query string, credential, provider choice, wildcard,
SQL, lifecycle setting or output bound from the caller.

## Execution order

Every successful call follows one fixed order:

1. detach and compare the exact five-key parameters, context and optional execution
   controls;
2. check the caller signal and absolute deadline using the application's trusted
   clock, with cancellation taking precedence, before policy evaluation, before
   adapter preflight and immediately before execution;
3. evaluate and verify the server-owned anonymous-open authority, checked
   default-deny v2 policy, per-call allow decision and exact public-read resource;
4. require an invocation-active health record, independently compare the adapter's
   upper-bound estimate, OGL rights and provenance with the accepted resource;
5. call the explicitly injected adapter's `execute()` exactly once with the shared
   cancellation signal and absolute RFC 3339 deadline;
6. recheck caller controls in the execution rejection path before mapping an adapter
   error, and immediately after a resolved execution before validating its result;
7. independently detach and check the returned provider, adapter, dataset, edition,
   version URI, native dimension order, one 15-digit-or-smaller integer string,
   `unit: null`, empty ONS Data Marking, OGL rights, provenance and 256 KiB
   canonical-result ceiling;
8. project the receipt-free result core, construct a public-read v2 receipt and
   immediately verify it with the full parameter, result, policy, authority,
   decision, resource and software material; and
9. when an explicit verified public ledger is injected, complete and re-verify its
   append-only write before adding `evidence_storage`.

There is no provider call during policy, health, estimate, rights or provenance
failure. An evidence-clock, receipt-verification or storage failure returns no
success result or receipt. A cancelled signal or elapsed caller deadline also
returns no result, receipt or durable write. Neither the abort reason nor the
deadline value can appear in a problem.

## Results and problems

The success shape is `gis-ai-go.data-query-result.v1`. It contains one
numeric-string observation with a `null` unit, the fixed evidence binding and a
fully verified `gis-ai-go.evidence-receipt.v2`. The receipt preserves the reviewed
profile hash, provider and adapter identity, dataset version, dimension order,
rights, attribution and byte/attempt limits. Durable storage is optional and
explicit; the default remains verified inline evidence only.

Failures use `gis-ai-go.data-query-problem.v1` and exactly one of ten codes:

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
- `DataQueryParameters`, `DataQueryResultCore` and `DataQueryResult`; and
- `DATA_QUERY_PROBLEM_CODES`, `DataQueryProblem` and
  `DataQueryApplicationError`.

The promoted schemas and examples are:

- [`data-query-parameters.schema.json`](../../schemas/data-query-parameters.schema.json)
  and
  the promoted `data-query-parameters.example.json` fixture;
- [`data-query-result.schema.json`](../../schemas/data-query-result.schema.json) and
  [`data-query-result.example.json`](../../providers/fixtures/data-query-result.example.json);
  and
- [`data-query-problem.schema.json`](../../schemas/data-query-problem.schema.json)
  and
  [`data-query-problem.example.json`](../../providers/fixtures/data-query-problem.example.json),
  [`data-query-cancelled-problem.example.json`][cancelled-problem]
  and
  [`data-query-deadline-exceeded-problem.example.json`][deadline-problem].

[cancelled-problem]: ../../providers/fixtures/data-query-cancelled-problem.example.json
[deadline-problem]: ../../providers/fixtures/data-query-deadline-exceeded-problem.example.json

The successful fixture retains the already documented public aggregate scalar
`10471` solely to reproduce the complete application result and receipt. It is not
a stored provider response, fresh live observation or activation claim.

## Remaining gates

This application-only slice still cannot be called through a shipped product. A
later integration must add and review direct API and MCP schema/result/problem
parity, registry implementation state, complete non-App rendering, lifecycle
agreement, independent-host evidence, operational cache/fallback behaviour and
deployment rollback before any activation. No new live ONS call is needed for this
inactive application test slice.
