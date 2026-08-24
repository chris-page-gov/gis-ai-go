# EVID-204 evidence checkpoint and recovery candidate

- status: provider-independent, inactive repository candidate; not deployed
- work item: [EVID-204](https://github.com/chris-page-gov/gis-ai-go/issues/22)
- storage decisions: [ADR-0011](../decisions/ADR-0011-durable-public-evidence-ledger.md)
  and [ADR-0012](../decisions/ADR-0012-receipt-only-lost-response-reconciliation.md)

## Outcome

The evidence package can checkpoint one exact public evidence ledger and linked
reconciliation index as a coherent pair, verify that backup against a separately
retained checkpoint, and restore it only into two existing empty private roots.

The backup directory has one content-addressed canonical manifest:

```text
manifest.json
ledger/
reconciliation-index/
```

`manifest.json` contains no source or destination path. It binds both descriptor
identities, both complete domain-separated root digests, counts, the ledger's event
count and last event identity, and the recovery boundary. The small external
checkpoint repeats those identities and roots plus the manifest file SHA-256. It
is also the transaction commit record: until its exclusive durable write completes,
the candidate backup is unpublished and the standalone checker rejects it. It must
be retained outside the backup directory. Comparing a current pair with this separate
value detects a structurally valid rollback or deletion of a complete ledger tail
that the ledger's internal chain alone cannot detect.

All checkpoint directories are `0700`; every manifest, descriptor, evidence
document and marker is `0600`. Symbolic links, file hard links, special files,
unexpected entries, broader modes and changing source bytes fail closed. Writes are
exclusive and never overwrite an existing backup, external checkpoint or restored
file. Directory enumeration and aggregate bytes are bounded by the evidence-root
role before hostile names are sorted or file content is read.

## Stopped-writer precondition

One writer owns the pair. Stop it through the deployment's service supervisor and
confirm that it is stopped before calling `createEvidenceCheckpoint`. Pass
`stoppedSingleWriter: true` only after that check.

This value is an explicit operator assertion, not process discovery or a lock. The
runtime completes `ledger.verify()` and reconciliation-index `verify()` before and
after copying and rejects any observed change, but it cannot prove that an unknown
process is fenced. The provider-specific deployment must define the supervisor,
maintenance mode and evidence for this stop.

The final complete source verification is the snapshot's linearisation point. A
source advance observed before that point prevents publication. Resuming or allowing
a writer to advance either source after that point violates the operator's
`stoppedSingleWriter` assertion; the resulting checkpoint remains an exact snapshot
at the declared point rather than evidence of the later source state.

## Create a checkpoint

The embedding operator calls the exported runtime with the stopped pair's two
existing roots and two new, disjoint output paths:

```typescript
import { createEvidenceCheckpoint } from "@gis-ai-go/evidence";

const verified = createEvidenceCheckpoint({
  ledgerRootDirectory,
  reconciliationIndexRootDirectory,
  checkpointDirectory,
  externalCheckpointFile,
  stoppedSingleWriter: true,
});
```

The parents of both outputs must already be real directories. Neither output may
exist, overlap either source root, or overlap each other. The runtime:

1. completes both source `verify()` calls;
2. inventories all allowed entries and bytes without following links;
3. copies each file with exclusive creation and synchronises it;
4. repeats both complete source verifications and inventories;
5. writes and reopens the content-addressed manifest last within the backup;
6. completely verifies the copied ledger/index pair against that manifest;
7. repeats both source verifications and inventories after every backup write and
   copied-pair check, establishing the snapshot linearisation point; and
8. exclusively and durably writes the external checkpoint as the final transaction
   commit record.

If any step fails, keep the stopped writer stopped. Do not promote a checkpoint
without both complete documents and a passing checker. A partial backup may contain
a valid manifest, but a missing, incomplete or colliding external commit record makes
it deterministically unverifiable. This prevents a late valid ledger-tail or index
advance observed by the final source check from leaving an older restorable
checkpoint. The library deliberately does not remove a partial output.

## Verify a checkpoint

Build the evidence package, then run the path-free read-only checker:

```bash
pnpm --filter @gis-ai-go/evidence run build
node scripts/check_evidence_checkpoint.mjs \
  --checkpoint-directory "$EVIDENCE_CHECKPOINT_DIRECTORY" \
  --external-checkpoint-file "$EVIDENCE_EXTERNAL_CHECKPOINT_FILE"
```

Success returns a canonical JSON summary containing identities and counts, never
paths. Failure returns a fixed error code and no path. The checker rejects:

- a missing manifest, root entry, record, event, claim, resolution or marker;
- a ledger from one checkpoint paired with an index or manifest from another;
- changed bytes, modes or identities;
- a symbolic link, file hard link, special file or unexpected entry; and
- an external checkpoint that does not match the manifest and both complete roots.

### Fixed traversal ceilings

The checkpoint contract has role-specific ceilings derived from the bounded ledger
and reconciliation-index storage contracts. They are evidence format limits, not a
provider quota:

| Root | Entries | Files | Aggregate bytes |
| --- | ---: | ---: | ---: |
| Ledger | 2,000,003 | 2,000,001 | 4,259,840,016,384 |
| Reconciliation index | 20,486 | 20,481 | 201,342,976 |

Each child directory is enumerated incrementally only up to its role limit before
the accepted names are sorted. During verification, the smaller file, entry and
byte totals in the already validated manifest become additional ceilings. A file
whose metadata would cross the remaining byte total is rejected before its content
is allocated or read. The same bounds apply to creation, verification, current-root
comparison and restore.

A sibling file on the same writable filesystem satisfies the runtime's disjoint-path
check but is not an independent security boundary. Before the writer resumes, copy
the external checkpoint value to a separately administered, access-controlled and
preferably immutable system. The repository does not select or authenticate to that
system.

## Restore

Do not repair or truncate the failed stores in place.

1. Stop and fence the single writer.
2. Quarantine the linked failed roots as one pair without deleting them.
3. Select one complete backup and its separately retained external checkpoint.
4. Run the checker above.
5. Provision two disjoint, real, existing, empty directories at mode `0700`.
6. Call `restoreEvidenceCheckpoint` with those destination roots.
7. Resume only after the returned status is `verified` and the deployment's own
   readiness checks pass.

```typescript
import { restoreEvidenceCheckpoint } from "@gis-ai-go/evidence";

const verified = restoreEvidenceCheckpoint({
  checkpointDirectory,
  externalCheckpointFile,
  ledgerDestinationRoot,
  reconciliationIndexDestinationRoot,
});
```

The runtime verifies the backup first, refuses either non-empty destination before
copying, creates every child exclusively, opens the restored pair and completes
both `verify()` calls. It then compares the restored complete roots and ledger tail
with the external checkpoint. A late filesystem failure can leave a partial restore;
quarantine both destinations and start again with two new empty roots. There is no
automatic cleanup or disposal.

## Release boundary and open operational decisions

This candidate changes no operation registration, readiness state, image contract,
deployment, provider or release claim. It does not sign or attest evidence and is
not WORM storage or a malicious-operator defence.

Before deployment admission, the owner still needs to decide and evidence:

- the persistent-volume and backup provider, region, encryption and access control;
- where the external checkpoint is independently retained and how it is advanced;
- the supervisor/fencing procedure and named operator role;
- checkpoint schedule, retention, monitoring, RPO and RTO;
- a real deployment recovery exercise and readiness evidence; and
- separately authorised retention expiry and disposal. This implementation does
  not automate disposal.
