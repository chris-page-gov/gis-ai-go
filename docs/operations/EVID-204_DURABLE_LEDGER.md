# EVID-204 durable public evidence candidate

- status: accepted inactive storage on protected `main`; not activated or deployed
- work item: [EVID-204](https://github.com/chris-page-gov/gis-ai-go/issues/22)
- decisions: [ADR-0011](../decisions/ADR-0011-durable-public-evidence-ledger.md)
  and [ADR-0012](../decisions/ADR-0012-receipt-only-lost-response-reconciliation.md)
- accepted implementation: [pull request 33](https://github.com/chris-page-gov/gis-ai-go/pull/33),
  protected `main` commit `cb6b817ea7a2e025b3fe9a42c085d117467ced04`

## Implemented boundary

`openPublicEvidenceLedger` creates or opens a portable directory containing:

```text
ledger.json
records/<record-sha256>.json
events/<16-digit-sequence>-<event-sha256>.json
```

Every document is RFC 8785 canonical JSON with one terminating newline. The ledger
descriptor fixes anonymous-open scope, the `evidence.inspect` permission and a
minimum retention period. Records contain only the accepted inline receipt and
storage metadata. Events form an ordered hash chain and include a digest-only replay
key.

`PublicEvidenceLedger.persistReceipt` accepts a receipt only with the independently
supplied parameter, result, policy and rights material required by
`verifyInlineReceipt`. It verifies the existing ledger, rejects private fields,
rejects replay, and refuses a genuinely new receipt before either immutable write
when the accepted one-million-event ceiling is full. It then creates the record and
event without overwrite, synchronises both files, verifies the complete ledger
again, and only then returns a `status: persisted` reference. Replay rejection and
inspection remain available at the ceiling.

`createCatalogueApplication` has an explicit embedding option for this ledger. The
default remains unchanged and returns only the ADR-0010 inline receipt. With a
ledger, the result adds `evidence_storage` only after persistence succeeds. The
inline receipt continues to record its issue-time policy decision; the separate
storage reference and event record the later durable action.

The accepted v1 `createEvidenceInspectApplication` seam is transport-neutral. Its
unchanged request accepts one closed receipt identity and returns the verified public
record, event and storage reference. The additive v2 reconciliation request is
described below. Neither request retains or claims to replay the original query or
result material.

## Inactive receipt-only reconciliation extension

The later inactive candidate adds a separate
`PublicEvidenceReconciliationIndex` linked to one exact ledger:

```text
index.json
claim-ownership/<key-sha256>
claims/<key-sha256>.json
claim-ready/<key-sha256>
resolutions/<key-sha256>.json
resolution-ready/<key-sha256>
```

The raw `gis-ai-go:ik:v1` key is domain-separated and hashed before it becomes a
file name or document field. Claims retain only the operation, reviewed resource,
parameter digest, semantic fingerprint and bounded request/trace identities.
Resolutions retain only claim, fingerprint and receipt identities. Parameters,
observations and result material are not retained. The ledger and index recursively
reject a complete raw key in stored strings; storage roots cannot contain one.

An exclusive, content-free ownership marker is synchronised before a new provider
execution. Canonical claim and resolution JSON is fully synchronised before its
ready marker is published. Resolution publication must precede ledger persistence.
After ledger persistence, a completed re-read must verify the exact receipt, record,
event and storage identities before the first success is returned. Ownership without
a ready claim, or a resolution without the linked ledger receipt, remains pending
and can never authorise another execution.

Ownership and claim documents are immutable. No expiry, release, reclamation or
operator-resolution procedure is implemented. Cancellation, an adapter rejection or
an uncertain failure after ownership can therefore leave a key permanently pending.
The index refuses a genuinely new key before publication once 4,096 claims are
owned; pending, completed and conflicting existing keys remain available first.
This bounds local filesystem growth and linear verification work. It is not a
cluster quota or an activation-safe admission service.

## Restart and readiness contract

Opening or verifying the ledger checks:

1. immutable descriptor identity and retention;
2. real directories and regular files, with no symbolic links and exact POSIX
   modes `0700` and `0600` respectively;
3. exact canonical bytes and complete record terminators;
4. record and event content identities;
5. contiguous sequence numbers and prior-event links;
6. one record and one event for each accepted receipt;
7. unique replay keys;
8. the anonymous-open receipt boundary; and
9. the declared privacy exclusions.

Any failure throws a controlled `PublicEvidenceLedgerError`. A configured catalogue
application does not convert that failure into an inline-only success.

The later EVID-204 completion slice adds a branded, inactive readiness-integrity
seam over one exact linked ledger and reconciliation index. Construction verifies
both roots. Every `GET /readyz` evaluation repeats both complete checks through
captured base-class methods and rechecks the exact ledger/index link. Method
substitution, proxying, relinking, corruption or I/O failure cannot make readiness
pass. The response remains the existing path-free `503` blocked document with empty
tool and API-operation arrays; a failed integrity check produces only a controlled
path-free `gateway_readiness_integrity_failed` lifecycle event. It does not add an
activation state or a readiness override.

Both checks are linear in the accepted event and claim counts. Running them on an
unauthenticated public readiness route would therefore require governed ingress,
request admission and operational capacity evidence. The current candidate remains
blocked and undeployed, so this seam is repository evidence rather than a public
availability claim.

## Corruption response

Do not repair or truncate a failed ledger or linked reconciliation index in place.

1. stop the writer and any affected operation;
2. identify which verified root failed, then quarantine the linked ledger and index
   directories as one coherent pair;
3. retain the controlled error code and surrounding operational logs, without
   copying private payloads;
4. restore a complete pair whose descriptors, claims, resolutions, records and
   events pass both `verify()` calls;
   and
5. investigate the file-system and writer boundary before resuming.

There is no automated deletion. `retain_until` is a minimum; records remain
inspectable afterwards. A future disposal process must be separately authorised and
must append its own governed evidence.

Exact private modes are now part of verification. An existing local candidate with
broader modes such as `0750` or `0640` must be migrated only while its writer and
all inspectors are stopped: take a recoverable copy, set every store directory to
`0700` and every descriptor, document and marker to `0600`, then reopen the ledger
and index and require both verification passes before resuming. Do not chmod a live
store or treat a permission-only change as repair for any other verification fault.

## Residual boundary

These are application-level append-only stores, not signatures, attestations, WORM
media or malicious-operator defences. A complete tail deletion cannot be detected
without an external checkpoint. One writer owns the ledger root. The index excludes
same-key execution across processes that share it, but does not make different-key
ledger appends generally multi-writer safe. Backups, external checkpoints, disaster
recovery and production retention assurance remain open.

This accepted storage slice included no direct route, MCP registration, listener
activation, deployment or public registry entry. The later
[inspection transport candidate](EVID-204_INSPECT_TRANSPORT.md) adds only explicit
constructor seams. `evidence.inspect` remains absent from all production activation
arrays.

## Inactive public-read v2 compatibility candidate

The later TOOLS-205 prerequisite extends `persistReceipt` and `inspect` with a
verified v1-or-v2 receipt and durable-record union. V1 receipt, record, descriptor,
event and replay identities retain their original domains and bytes. A public-read
v2 receipt is stored only in `gis-ai-go.public-evidence-record.v2`, whose separate
content domain prevents an identity collision with v1. Mixed ledgers pass restart,
tamper, replay and privacy tests. The accepted
`evidence-inspect-result.schema.json` v1 contract remains byte-identical at
SHA-256 `ab6973053b58bdb59c94cd8c5db9c354e1954cb84a188d5d7db579442e6f7b61`
and accepts only v1 records. A v2 record returns the separate
`gis-ai-go.evidence-inspect-result.v2` discriminator and v2 result schema. The
inactive operation contract advertises a separately identified closed dispatcher
over those two unchanged per-version meanings. This compatibility change does not
activate `selection.resolve`, `data.query` or `evidence.inspect`; see
[TOOLS-205 public-read v2 contracts](TOOLS-205_PUBLIC_READ_V2_CONTRACTS.md).

## Verification

Focused verification commands are:

```bash
pnpm --filter @gis-ai-go/evidence run test
pnpm --filter @gis-ai-go/mcp-gateway run test
pnpm run validate:contracts
```

The accepted storage slice includes regressions for restart, canonical bytes,
corruption, truncation, sequence gaps, identity collision, orphan records, replay,
retention, private material, inspection and catalogue persistence failure. Its
pull-request, CodeQL, protected-main and attestation evidence are complete. The
inspection transport was separately accepted through
[pull request 37](https://github.com/chris-page-gov/gis-ai-go/pull/37) as protected
`main` commit `c4d43f9d0f7af143e01eb3381e5adc4625fac2f0` and remains inactive. Any
activation still requires its own review.

The reconciliation extension was accepted through
[pull request 46](https://github.com/chris-page-gov/gis-ai-go/pull/46) as protected
`main` commit `525304145088bda558687438c87440bde1f642a4`. It additionally tests
atomic same-key ownership,
competing and reopened instances, incomplete publication and restart states, exact
private modes, symbolic-link and overlapping-root rejection,
resolution-before-ledger ordering, linear bulk linkage verification, raw-key
exclusion, pre-publication index and ledger capacity refusal, at-cap recovery,
conflict and retention handling. This acceptance changes no activation, deployment
or release claim.
