# EVID-204 durable public evidence candidate

- status: accepted storage candidate on protected `main`; not activated or deployed
- work item: [EVID-204](https://github.com/chris-page-gov/gis-ai-go/issues/22)
- decision: [ADR-0011](../decisions/ADR-0011-durable-public-evidence-ledger.md)
- base: protected `main` commit `66507f9a6e6c0da23a8af4682268f9362d93bc06`

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
creates the record and event without overwrite, synchronises both files, verifies
the complete ledger again, and only then returns a `status: persisted` reference.

`createCatalogueApplication` has an explicit embedding option for this ledger. The
default remains unchanged and returns only the ADR-0010 inline receipt. With a
ledger, the result adds `evidence_storage` only after persistence succeeds. The
inline receipt continues to record its issue-time policy decision; the separate
storage reference and event record the later durable action.

`createEvidenceInspectApplication` is transport-neutral. It accepts only a closed
receipt identity and returns the verified public record, event and storage
reference. It does not retain or claim to replay the original query or result
material.

## Restart and readiness contract

Opening or verifying the ledger checks:

1. immutable descriptor identity and retention;
2. real directories and regular files, with no symbolic links;
3. exact canonical bytes and complete record terminators;
4. record and event content identities;
5. contiguous sequence numbers and prior-event links;
6. one record and one event for each accepted receipt;
7. unique replay keys;
8. the anonymous-open receipt boundary; and
9. the declared privacy exclusions.

Any failure throws a controlled `PublicEvidenceLedgerError`. A configured catalogue
application does not convert that failure into an inline-only success. Future
readiness may depend on this verification, but the current production readiness
contract remains deliberately blocked for the wider `v0.2.0` lifecycle gate.

## Corruption response

Do not repair or truncate a failed ledger in place.

1. stop the writer and any affected operation;
2. quarantine the complete ledger directory;
3. retain the controlled error code and surrounding operational logs, without
   copying private payloads;
4. restore a complete copy whose descriptor, records and events pass `verify()`;
   and
5. investigate the file-system and writer boundary before resuming.

There is no automated deletion. `retain_until` is a minimum; records remain
inspectable afterwards. A future disposal process must be separately authorised and
must append its own governed evidence.

## Residual boundary

This is an application-level append-only store, not a signature, attestation, WORM
medium or malicious-operator defence. A complete tail deletion cannot be detected
without an external checkpoint. One writer owns a root; concurrent-process
coordination, backups, external checkpoints, disaster recovery and production
retention assurance remain open.

This accepted storage slice included no direct route, MCP registration, listener
activation, deployment or public registry entry. The later
[inspection transport candidate](EVID-204_INSPECT_TRANSPORT.md) adds only explicit
constructor seams. `evidence.inspect` remains absent from all production activation
arrays.

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
inspection transport candidate and any activation still require their own review.
