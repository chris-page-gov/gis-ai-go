# TOOLS-205 public-read v2 contract candidate

## Status and boundary

This is an inactive prerequisite candidate for `selection.resolve` and
`data.query`. It adds a parallel authority, policy and evidence contract plane;
it does not implement either application, register a route or MCP tool, call a
provider, activate a lifecycle plane, add an environment override or deploy a
service. The suspended `evidence.inspect` profile changes only its accepted output
reference to the closed version dispatcher described below; its current discovery
and activation gates remain false.

The integrated candidate is based on protected `main` at
`ef960f70fe409b0dcf7d75b0b92ac28802b5b6db`, which includes the accepted
QUAL-206 evidence and ADAPT-203B inactive ONS adapter. The public-read contract
is still an inactive prerequisite: this commit does not activate, publish or
deploy either operation.

## Closed contract identities

| Contract | Schema | Content identity |
| --- | --- | --- |
| Server authority | `gis-ai-go.public-authority-context.v2` | `gis-ai-go:public-authority-context:sha256:5d97a93aaa9c8fcbf9f02d2812275cf59b4c0e0e923de89ac975035c741bc1f1` |
| Reviewed resource | `gis-ai-go.public-read-resource.v1` | `gis-ai-go:public-read-resource:sha256:c7130712a40d75e71bcf0259792404389bea2e549adf6733f34d491f83e99f68` |
| Checked policy | `gis-ai-go.public-policy.v2` | `gis-ai-go:public-policy:sha256:b1a37b2ebf6900e2b5d62dfa20bcdaa1232e1c4c9f9630f90ac9d3dde738624a` |
| Decision | `gis-ai-go.public-policy-decision.v2` | Content-addressed per request, trace and outcome |
| Success receipt | `gis-ai-go.evidence-receipt.v2` | Content-addressed per successful evidence binding |
| Durable record | `gis-ai-go.public-evidence-record.v2` | Content-addressed per receipt, ledger and persistence time |

The authority is constructed by the server and accepts no caller-supplied person,
organisation, role, client, device, credential, token, entitlement or request-time
claim. It is anonymous, open, read-only, non-personal and non-protected, and names
only `data.query` and `selection.resolve`.

The exact resource binds reviewed profile `PV-ONS-DATA` at immutable research
pointer `/providers/1` and SHA-256
`535e6eb65fc9af4507e30700d425393a658a085a3a240689f4b37124dc8f8622` to
provider `ons-data-api`, adapter `gis-ai-go.ons-data-api` version `1`, dataset
`weekly-deaths-region`, edition `time-series`, version `121`, release date
`2026-07-01` and four fixed provider-native selections. It also binds the Open
Government Licence evidence, attribution, obligations, reviewed exceptions and the
single-observation, attempt and byte bounds.

Adapter version `1` is taken from accepted ADAPT-203B. Every resource field is
compared with the merged adapter preflight, estimate, fixed selection and rights
evidence; any mismatch requires a new resource and policy content identity, not an
alias.
`pnpm run validate:public-read-v2` rebuilds the relevant TypeScript packages,
independently recomputes the resource, authority and policy identities, verifies
the immutable provider record and publication pointer against the checker-owned
accepted `PV-ONS-DATA` record SHA-256 shown above, and compares every
resource, authority and policy runtime projection with its checked JSON and
relevant schema constants, decision and receipt bindings without a provider call.
It also pins the accepted ADAPT-203B preflight as Git blob
`fc511965db5d575ef4c2165aa40e6bf5ed3cae34` and SHA-256
`552bed362c6c01252a5251238815819f9966af04d675a62b6479e723f040e7b7`, so a
coordinated edit cannot move the provider boundary and its checker together.

## Policy and evidence semantics

The checked JSON policy is default-deny. Its only allow rules are:

- `data.query` for the exact resource, with a bounded single observation and
  profile, provider, version, rights and attribution obligations; and
- `selection.resolve` for the same resource, with `no-provider-execution` and the
  same preservation obligations.

A different resource, any other governed operation or an unknown operation is
denied. Unknown operations deliberately receive no schema-invalid hashed decision.
The evaluator is local and deterministic; it is not an identity, entitlement or
remote policy service.

Receipt parameter and result digests use distinct operation domains:

| Operation | Parameter domain | Result-core domain |
| --- | --- | --- |
| `data.query` | `gis-ai-go.data-query-parameters.v1` | `gis-ai-go.data-query-result-core.v1` |
| `selection.resolve` | `gis-ai-go.selection-resolve-parameters.v1` | `gis-ai-go.selection-resolve-result-core.v1` |

The result core must bind the exact resource, profile hash, provider, adapter,
dataset, edition, version, rights digest and returned-item count. It must have the
matching request and trace and the operation-specific successful state. The receipt
retains the parameter and result digests, not the raw parameter object or result.

ADR-0010 success semantics remain strict: `buildPublicReadReceipt()` accepts only
an exact `allow-with-obligations` decision and a successful result core. A denial,
ambiguous selection or failed query does not fabricate a success receipt. Those
future application outcomes need their own closed problem envelope, not weaker
evidence.

## Durable ledger compatibility

`PublicEvidenceLedger.persistReceipt()` now accepts the verified union
`InlineEvidenceReceipt | PublicReadEvidenceReceipt`. Existing v1 records continue
to use `gis-ai-go.public-evidence-record.v1` and the original
`gis-ai-go.public-evidence-record.v1` content-address domain. V2 receipts use a new
record schema and domain. The ledger descriptor, storage layout, event schema,
event domain, replay key, retention semantics and `inspect()` API are unchanged.

The regression fixture proves the pre-existing v1 identities remain:

- receipt `a70f8e6f752de3a6128989e8f88dab448b55aeac76831462e56b5f236be3f033`;
- record `f4afb5dcffb1ed6ad9a878633c6139b26787f69c2fb69a286a0d18052c8460ea`;
  and
- first event `a170a3be16c911fe477972ed8d24b3c462f3d95a02f2ab16a48a6858c7dc12ca`.

Mixed ledgers re-verify after restart. Exact and semantic replay, receipt-material
substitution, record tampering, private paths, credentials, prompts and retained raw
parameter or result material fail closed. The existing transport-neutral
`evidence.inspect` application and its direct API, MCP HTTP, STDIO, resource and
plain-text projections accept either record version without changing the request,
route or activation state. A v1 record returns
`gis-ai-go.evidence-inspect-result.v1`; a v2 record returns the distinct
`gis-ai-go.evidence-inspect-result.v2`. The accepted v1 result-schema bytes and
meaning remain unchanged. The inactive operation registry and OpenAPI/MCP contract
point to `evidence-inspect-operation-result.schema.json`, a closed dispatcher whose
two branches reference the exact v1 and v2 result schemas. Its runtime projection
embeds every transitive schema and has no unresolved external reference.

## Public APIs

The evidence package exports:

- `PUBLIC_READ_ONS_RESOURCE_CORE`, `PUBLIC_READ_ONS_RESOURCE`,
  `buildPublicReadResource()` and `verifyPublicReadResource()`;
- `buildPublicReadAuthorityContext()` and
  `verifyPublicReadAuthorityContext()`;
- `buildPublicReadPolicy()`, `verifyPublicReadPolicy()`,
  `buildPublicReadPolicyDecision()` and `verifyPublicReadPolicyDecision()`;
- `publicReadResultEvidenceBinding()`, `buildPublicReadReceipt()`,
  `verifyPublicReadReceiptStructure()` and `verifyPublicReadReceipt()`; and
- the v1-or-v2 public receipt, verification-material and durable-record union
  types.

The authority package exports `PUBLIC_READ_AUTHORITY_CONTEXT` and
`getPublicReadAuthorityContext()`. The policy package exports
`PUBLIC_READ_POLICY_CORE`, `PUBLIC_READ_POLICY`, `evaluatePublicReadPolicy()` and
`isAllowedPublicReadOperation()`.

## Remaining gates

The next slices must remain inactive until they add, in order:

1. deterministic `selection.resolve` normalisation and explicit ambiguity/problem
   results without provider execution;
2. an injected call from `data.query` to the accepted fixed ONS adapter, with no
   caller URL, credential or lifecycle override;
3. shared application results and exact direct API, MCP HTTP, STDIO, resource and
   plain-text byte parity;
4. lifecycle, suspension and zero-default activation tests; and
5. fresh review and release evidence on the then-current protected `main`.

The first item is implemented by the separate
[inactive selection resolver candidate](TOOLS-205_SELECTION_RESOLVE.md). That
application remains unmounted and does not satisfy the later transport, lifecycle,
host, activation or deployment gates.

Owner approval, credentials and deployment are not required for this contract-only
candidate. A later public ONS live query still needs explicit activation and
operational approval. No reusable provider credential is expected for this exact
anonymous ONS resource.
