# Formal model and verification boundaries

This chapter defines the system-level vocabulary and proof obligations for the
implemented code at `97bc45635a91064cd78f06bf0848ad7636f05439`. Component chapters
refine it with state machines, preconditions, postconditions and implementation/test
references. These are source-derived specifications. No theorem prover or model
checker was run, and passing examples do not prove a universal property.

## Vocabulary

Let `R` be a request, `o` its operation, `a` its arguments, `C` the server authority
context, `P` the compiled policy, `D` an admitted provider result, `E` an evidence
receipt and `S` the store state. `V_x(y)` means validator `x` accepts `y`.
`H_d(y)` means the project's canonical content hash in domain `d`; a digest's
domain and canonical representation are part of its contract.

`Pre ⇒ {operation} ⇒ Post` is a partial-correctness claim: if the preconditions
hold and the operation returns successfully, its postconditions hold. It does not
assert termination, provider availability, authenticity of an external source or
continued persistence after an unmodelled storage failure.

The formal catalogue is [all versioned schemas and other contracts](CONTRACT_REGISTER.md).
The [beginner guide](CONTRACTS.md) explains how these definitions relate to JSON,
TypeScript, policy, runtime checks and concrete tests.

## S1: advertised authority is bounded by the selected assembly

For the core candidate, let
`T = {catalogue.search, catalogue.describe, selection.resolve, data.query, evidence.inspect}`.
Let `A` be the active operation set after applicable suspension rules.

```text
A ⊆ T
MCP_operations = API_operations = A
productionRegistration = false
generic_production_operations = ∅
```

The invariant is local to this candidate; the pilot has a different tool set.
The [registry](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/tool-registry/src/registry.ts#L45-L110),
[assembly options and checks](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/governed-assembly.ts#L57-L125)
and [blocked production default](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/activation.ts#L1-L25)
establish the vocabulary. [Gateway invariants and tests](GATEWAY.md) cover equality,
suspension propagation and transport exposure.

## S2: shape, semantics, authority and capability are separate predicates

```text
eligible(R, C, S) =
    valid_shape(R)
  ∧ valid_semantics(R)
  ∧ admitted_operation(R.operation)
  ∧ policy_allows(C, R)
  ∧ required_capabilities_available(S)

valid_shape(R) does not imply eligible(R, C, S)
discovered_resource(x) does not imply permitted_read(x)
```

This is an explanation of the layered acceptance conditions, not a claim that one
function computes them in that exact order for every surface. Each application
fixes its order to avoid unnecessary side effects. The [contracts guide](CONTRACTS.md)
and [gateway](GATEWAY.md) trace the actual validators and policy decisions. The
[experimental chapter](EXPERIMENTAL_AND_KNOWLEDGE.md) describes the pilot's separate
host, input and allowance predicates.

## S3: a successful core result binds its evidence to its content

```text
success(result) ⇒
    receipt.operation.name = requested_operation
  ∧ receipt.request_id = result.request_id
  ∧ receipt.trace_id = result.trace_id
  ∧ receipt.result.sha256 = H_result_domain(result_core)
  ∧ receipt.receipt_id = identity(H_receipt_domain(receipt_without_its_id))
```

The definition of `result_core` is version-specific; it must not accidentally
include the receipt itself or storage metadata excluded by that schema. Receipt
versions, domains, persistence distinctions and independent verification are defined
in [core and evidence](CORE_AND_EVIDENCE.md). An internally consistent receipt
does not establish that a source is correct or that an external party signed it.

## S4: idempotency claims prevent the core from silently repeating work

For a claim key `k` in one admitted reconciliation store:

```text
Unclaimed(k) → Owned(k) → Claimed(k, request_fingerprint)
Claimed(k, f) → ResolutionPublished(k, f, receipt_identity)
ResolutionPublished(k, f, e) → Completed(k, f, e)      after ledger persistence and verified lookup
Owned / Claimed / ResolutionPublished → pending      when completion is not established
Completed + repeated data.query(k) → receipt-free idempotency_completed problem
Completed + separate evidence.inspect(k) → retained receipt, without original result replay
```

Publishing a resolution is not completion: a crash before ledger persistence leaves
the key pending. Repeating `data.query` does not return its receipt; callers use the
separate inspection operation. See [resolution-before-ledger enforcement](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/reconciliation-index.ts#L1586-L1621)
and [verified completion lookup](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/reconciliation-index.ts#L1635-L1659).

There is no successful transition that changes an existing key's fingerprint or
replays a completed original result. The guarantee concerns this store and its
ownership protocol; it is not global exactly-once delivery to arbitrary external
providers. Publication/recovery ordering and the conditions under which a claim
can remain unresolved are in [gateway](GATEWAY.md) and
[core and evidence](CORE_AND_EVIDENCE.md). The pilot's live reads and transactional
CPIH snapshots have different contracts and must not inherit this state machine by
analogy.

## S5: a data value retains its execution and freshness meaning

```text
fixed_fixture_result ≠ live_provider_observation
approved_cache_result ≠ current_provider_observation
captured_CPIH_result ≠ live_CPIH_read
source_metadata_discovery ≠ dataset_execution_authority
```

These are distinct semantic states even if their numeric values coincide. The
[local candidate contract](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/README.md#L111-L133)
states the provider-free cache path. [Experimental and knowledge](EXPERIMENTAL_AND_KNOWLEDGE.md)
specifies captures, live providers, bounds and the independent limits of metadata
coverage. The UI must preserve those labels when projecting a result for a person.

## S6: storage integrity has an explicit scope

```text
hash_valid(bytes) ⇒ identity_matches_expected_content
chain_valid(snapshot) ⇒ internal_links_match_that_snapshot
chain_valid(snapshot) does not imply snapshot_is_latest
locally_persisted(E) does not imply independent_attestation(E)
```

Rollback detection needs an independently retained expected state; it cannot be
deduced from a self-consistent earlier snapshot alone. [Core and evidence](CORE_AND_EVIDENCE.md)
specifies filesystem verification, stopped-writer checkpoint/restore and transactional
compare-and-swap. [Build and operations](BUILD_AND_OPERATIONS.md) specifies the
separate preservation and release evidence boundaries.

## Verification map

| Obligation | Concrete implementation and tests | Principal failure to preserve during refactoring |
| --- | --- | --- |
| S1 activation and parity | [Gateway](GATEWAY.md) | Planned or suspended operation appears on one transport |
| S2 layered acceptance | [Contracts](CONTRACTS.md), [gateway](GATEWAY.md), [experimental](EXPERIMENTAL_AND_KNOWLEDGE.md) | Schema validity mistaken for authority or execution capability |
| S3 content binding | [Core and evidence](CORE_AND_EVIDENCE.md) | Changed projection or digest domain silently accepts a different result |
| S4 claim ownership | [Gateway](GATEWAY.md), [core and evidence](CORE_AND_EVIDENCE.md) | Duplicate execution, unresolved ownership deleted, or original result replayed |
| S5 semantic labels | [User interfaces](USER_INTERFACES.md), [experimental](EXPERIMENTAL_AND_KNOWLEDGE.md) | Capture or cache displayed as current live data |
| S6 storage scope | [Core and evidence](CORE_AND_EVIDENCE.md), [operations](BUILD_AND_OPERATIONS.md) | Self-consistency promoted to freshness, rollback detection or attestation |

For changes, preserve the existing negative tests as well as success cases. Add a
regression for a newly reproduced defect before repairing it. Reuse of small
encoding utilities is different from making an independent verifier call the
producer's high-level acceptance function. The [review](REVIEW.md) marks the
duplication that should remain independent and the duplication suitable for staged
extraction.
