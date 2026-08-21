# TOOLS-205 inactive selection resolver

## Status and boundary

This candidate implements the transport-neutral `selection.resolve` application
without activating it. It adds no HTTP route, MCP tool or resource, OpenAPI
operation, registry implementation flag, entrypoint, environment override or
deployment. It has no provider-adapter, execution-service or network dependency
and never calls ONS.

The application is constrained to the accepted public-read v2 resource for
research profile `PV-ONS-DATA`, ONS Data API provider `ons-data-api`, dataset
`weekly-deaths-region`, edition `time-series`, version `121` and the exact four
provider-native selections. The existing v1 and v2 receipt, record, event and
replay domains remain unchanged.

## Checked selection profile and plan

The closed profile is
[`profiles/public-selection-profile.v1.json`](../../profiles/public-selection-profile.v1.json).
Its content identity is:

`gis-ai-go:public-selection-profile:sha256:344fe6d8cbec7c355735ee711cd19b067be306f4087b30c341efec6c5e819f8e`

It contains exactly one reviewed candidate and the following fixed score weights:

| Constraint | Weight |
| --- | ---: |
| candidate record | 128 |
| research profile | 64 |
| provider | 32 |
| dataset | 16 |
| edition | 8 |
| version | 4 |
| each of time, geography, week and cause of death | 2 |

The algorithm uses exact ASCII identifier comparisons after a safe canonical JSON
snapshot. It does not use an LLM, locale collation, network lookup or caller-defined
weights. Input ordering cannot change the score. The only candidate is never
chosen by a hidden tie-break: multiple alternative values return
`ambiguous_selection` with `plan: null`. The profile records the same fail-closed
tie rule for any later multi-candidate profile revision.

The success schema enumerates all 60 valid ordered ranking pairs: every non-empty
subset of the four provider anchors, every absent-or-present combination for
optional edition and version, and all four required dimensions. Each branch fixes both
`matched_constraints` and its exact weighted score. The public-read checker derives
the branches again from the separately checked profile and rejects any missing,
reordered or mutually edited schema branch.

Successful constraints produce the exact plan:

`gis-ai-go:selection-plan:sha256:dbae1e78051a3a3bdfd0b49c0318d54df3a500effcb85df8cf34ad4e3cd31d9e`

The plan states `execution: forbidden`, `provider_execution: false`,
`network: not-used`, `caller_url: false` and `credentials: false`. Its `data_query`
member is the accepted v2 parameter projection only. It is data for a later,
independently validating application; it is not an authority or executable token.

## Request and outcome grammar

The request requires a bounded `question` and non-empty closed `constraints`.
The question is untrusted display context: the resolver checks its encoding and
bounds but never interprets, reflects, hashes into a receipt, persists or sends it
to a provider. Resolution uses only the finite arrays for candidate, profile,
provider, dataset, edition, version and the four named dimensions.

A success needs at least one matching provider anchor and all four exact dimension
values. The deterministic failure precedence is:

1. malformed, unsafe or over-limit material returns `invalid_request`;
2. no provider anchor returns `missing_dimension`;
3. supplied anchors with no match return `no_compatible_provider`;
4. a matching anchor plus an incompatible constraint returns
   `contradictory_constraints`;
5. multiple alternatives containing the reviewed value return
   `ambiguous_selection`; and
6. absent provider dimensions return `missing_dimension`.

Every problem uses the closed `selection-resolve-problem.v1` schema, supplies only
reviewed choices, returns `plan: null` and has no success receipt or durable storage
claim. Raw hostile values are not reflected.

## Policy and evidence

Only an unambiguous resolution reaches the accepted server-owned anonymous-open
authority and public-read v2 policy. Its unchanged normalised parameter contract
binds the exact profile, provider, dataset and selections. The operation-specific
result core additionally binds the full content-addressed plan, deterministic
ranking, exact resource and rights evidence. A v2 success receipt is built and
verified before return.

An optional explicitly supplied public evidence ledger persists the same verified
receipt. The result gains `evidence_storage` only after the ledger write and
restart-style verification succeed. A configured ledger fault returns
`evidence_unavailable` with `plan: null`; it cannot fall back to an apparently
successful inline-only result.

## Verification

Focused verification is:

```bash
pnpm --filter @gis-ai-go/evidence run test
pnpm --filter @gis-ai-go/mcp-gateway run test
pnpm run validate:public-read-v2
pnpm run validate:contracts
```

Tests cover exact ranking and content identities, every unresolved outcome,
receipt and durable-ledger success, persistence failure, proxy and accessor
inputs, cycles, unsafe and malformed Unicode, byte and code-point bounds, unknown
properties and prompt-injection text. Static checks also confirm that the module
does not import an adapter or contain a network, registry or activation path.

The next slice may consume only `plan.data_query` after independently validating
it against the accepted data-query contract. Transport wiring, lifecycle changes,
host evidence, activation and deployment remain separate reviewed gates.
