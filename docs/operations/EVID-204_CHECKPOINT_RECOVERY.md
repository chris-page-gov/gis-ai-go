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
is also the transaction commit record. Publication first claims one deterministic
private `0700` transaction directory beside the target. Its canonical bytes are
written, synchronised and closed at the fixed `0600` `stage` path inside that
directory before an atomic no-replace hard link can make the final path visible.
Both names are retained with a link count of 2 until the final directory entry is
durable, so the standalone checker rejects every pre-durable visible target. The
external checkpoint must be retained outside the backup directory. Comparing a
current pair with this separate value detects a structurally valid rollback or
deletion of a complete ledger tail that the ledger's internal chain alone cannot
detect.

All checkpoint directories are `0700`; every manifest, descriptor, evidence
document and marker is `0600`. Symbolic links, file hard links, special files,
unexpected entries, broader modes and changing source bytes fail closed. Writes are
exclusive and never overwrite an existing backup, external checkpoint or restored
file. An exact canonical late claimant that independently verifies with the complete
backup is accepted as idempotent success; partial, different, linked, symbolic-link
and special-file claimants remain collisions. Directory enumeration and aggregate
bytes are bounded by the evidence-root role before hostile names are sorted or file
content is read.

## Filesystem capability preflight

Before admitting any persistent or backup filesystem, build the evidence package
and probe an existing directory on that exact mounted filesystem:

```bash
pnpm --filter @gis-ai-go/evidence run build
node scripts/check_evidence_filesystem_capabilities.mjs \
  --classification direct-filesystem-observation \
  --observed-at "$EVIDENCE_FILESYSTEM_OBSERVED_AT" \
  --mount-identity-sha256 "$EVIDENCE_FILESYSTEM_MOUNT_IDENTITY_SHA256" \
  --probe-directory "$EVIDENCE_FILESYSTEM_PROBE_DIRECTORY"
```

`--observed-at` must be the observation time in canonical UTC with milliseconds,
for example `2026-08-30T08:30:00.000Z`. The caller must derive one stable,
non-secret SHA-256 identity for the exact mount being observed and pass only its
lower-case digest through `--mount-identity-sha256`. Do not derive a published
identity from a path, credential or other secret. Use
`direct-filesystem-observation` only when the command is running directly against
the intended mounted filesystem. `synthetic-test-fixture` is reserved for tests
and deterministic local rehearsals.

The probe creates one private temporary child, checks `0700` directories and `0600`
regular files, exclusive file creation, sibling hard links, atomic no-replace hard
linking, regular-file and directory `fsync`, and synchronised clean-up. It removes
its own child on success. Its closed
`gis-ai-go.evidence-filesystem-capability-check.v1` result contains no path or
provider name. It records the caller-supplied mount digest, canonical observation
time and classification, and binds the receipt to the SHA-256 of the exact current
schema bytes through `schema_contract`. The mount identity is explicitly
`caller-supplied-not-attested`: the probe does not independently prove that the
directory belongs to a named provider, resource or mount. A pass applies only to
the one caller-identified filesystem that was probed. It does not establish
`F_FULLFSYNC`, storage durability beyond successful `fsync` returns, provider
backup behaviour or deployment admission.

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

The provider-neutral operator command wraps that exact API and additionally
requires the operator to assert both stopped-writer fencing and exclusive ownership
of this checkpoint operation:

```bash
node scripts/create_evidence_checkpoint.mjs \
  --ledger-root-directory "$EVIDENCE_LEDGER_ROOT" \
  --reconciliation-index-root-directory "$EVIDENCE_RECONCILIATION_INDEX_ROOT" \
  --checkpoint-directory "$EVIDENCE_CHECKPOINT_DIRECTORY" \
  --external-checkpoint-file "$EVIDENCE_EXTERNAL_CHECKPOINT_FILE" \
  --stopped-single-writer-confirmed \
  --exclusive-checkpoint-owner-confirmed
```

Both flags are assertions, not process discovery, a lease or a lock. Missing,
duplicate or unknown arguments fail before the runtime is called. Success and
failure use the closed path-free
`gis-ai-go.evidence-checkpoint-create-result.v1` contract. Existing checkpoint or
external-checkpoint paths are collisions and are never replaced.

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
8. atomically claims one deterministic sibling `0700` transaction directory, writes
   the canonical external bytes to its fixed `0600` `stage`, synchronises and closes
   the file, then synchronises the transaction directory and target parent;
9. atomically hard-links that stage to the unclaimed final path without overwrite,
   retains the verifier-rejected link count of 2 until the target directory entry is
   synchronised, then removes the exact inode-matched stage, synchronises the held
   inode and transaction directory, removes the empty transaction directory, and
   synchronises its removal from the target parent; and
10. freshly verifies the published external checkpoint and complete backup before
    returning success.

If any step fails, keep the stopped writer stopped. Do not promote a checkpoint
without both complete documents and a passing checker. A partial backup may contain
a valid manifest, but a missing, incomplete or colliding external commit record makes
it deterministically unverifiable. This prevents a late valid ledger-tail or index
advance observed by the final source check from leaving an older restorable
checkpoint. The library deliberately does not remove a partial output.

The deterministic transaction-directory name contains a bounded digest of the
canonical target path; the only allowed child is the fixed `stage`. An ordinary
creator that finds the transaction directory already present returns
`publication-indeterminate` and does not open, adopt or alter it. Publication never
scans for or removes similarly named siblings. While holding the transaction
directory descriptor as its namespace lock, it removes `stage` only after proving
the expected inode, bytes and link state.

The target parent must be a trusted directory that is not renamed or remounted
during publication. Its filesystem must support hard links between the private
transaction directory and sibling target, plus file and directory `fsync`.
Unsupported provider filesystems fail closed; there is no rename, copy or
direct-target fallback. Successful reconciliation establishes that the required
filesystem `fsync` calls returned successfully. Node.js does not expose macOS
`F_FULLFSYNC`, so this is not a claim of the strongest physical power-loss guarantee
available on every device. This transaction changes no successful
`gis-ai-go.evidence-checkpoint-manifest.v1` or
`gis-ai-go.evidence-external-checkpoint.v1` document bytes.

### Indeterminate publication and reconciliation

`publication-indeterminate` means the caller must not infer either success or
absence from the create error. Keep the single writer stopped and preserve the
checkpoint, target and deterministic transaction directory. The bounded states are:

- an exact one-link stage can remain inside the transaction directory before target
  publication, while the missing target makes the checker fail;
- if the atomic target link is visible but its first directory synchronisation did
  not complete, the stage and target remain the same inode with link count 2 and the
  checker rejects them;
- if the target entry was synchronised but stage removal did not complete, the same
  deliberately unverifiable two-link state may remain; or
- an exact one-link target can coexist with a separate exact one-link stage, an
  empty transaction directory, or no transaction directory after a currently
  visible removal. The target can then pass a read-only check, but that pass does not
  prove that the preceding directory operation will survive a crash.

Reconcile only after confirming both that the source writer remains stopped and
that no checkpoint publisher or other reconciler can be running. The two CLI flags
below are explicit operator assertions of those conditions, not process discovery:

```bash
pnpm --filter @gis-ai-go/evidence run build
node scripts/reconcile_evidence_checkpoint_publication.mjs \
  --checkpoint-directory "$EVIDENCE_CHECKPOINT_DIRECTORY" \
  --external-checkpoint-file "$EVIDENCE_EXTERNAL_CHECKPOINT_FILE" \
  --stopped-single-writer-confirmed \
  --exclusive-publication-owner-confirmed
```

The reconciler completely verifies the candidate backup, reconstructs the one exact
canonical external document, and accepts only the bounded absent, empty, exact
one-link and matching two-link states above. It never adopts a transaction while
another actor may own it. Under the asserted exclusive-owner precondition it
synchronises the exact file and final directory entry, removes only the proven
stage, synchronises the clean-up and freshly verifies the complete checkpoint. Its
successful canonical JSON sets `publication_durability` to
`file-and-parent-directory-synchronised`. An unexpected entry, mismatch, symbolic
link, special file or unrelated hard link is preserved and fails closed. There is no
recursive clean-up.

## Verify a checkpoint

Build the evidence package, then run the path-free read-only checker:

```bash
pnpm --filter @gis-ai-go/evidence run build
node scripts/check_evidence_checkpoint.mjs \
  --checkpoint-directory "$EVIDENCE_CHECKPOINT_DIRECTORY" \
  --external-checkpoint-file "$EVIDENCE_EXTERNAL_CHECKPOINT_FILE"
```

Success returns a canonical JSON summary containing identities and counts, never
paths. It sets `publication_durability` to
`not-established-by-read-only-check`: verification proves the bytes and current
namespace state, not crash persistence of a preceding directory operation. Use the
reconciler after `publication-indeterminate`. Failure returns a fixed error code and
no path. The checker rejects:

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

The corresponding operator command requires explicit stopped-writer and exclusive
restore-owner assertions:

```bash
node scripts/restore_evidence_checkpoint.mjs \
  --checkpoint-directory "$EVIDENCE_CHECKPOINT_DIRECTORY" \
  --external-checkpoint-file "$EVIDENCE_EXTERNAL_CHECKPOINT_FILE" \
  --ledger-destination-root "$EVIDENCE_LEDGER_DESTINATION_ROOT" \
  --reconciliation-index-destination-root \
    "$EVIDENCE_RECONCILIATION_INDEX_DESTINATION_ROOT" \
  --stopped-single-writer-confirmed \
  --exclusive-restore-owner-confirmed
```

Its closed `gis-ai-go.evidence-checkpoint-restore-result.v1` output contains no
path. It reports only the verified checkpoint and restored-store identities and
counts. It deliberately records deployment readiness as `not-evaluated`.
Non-empty destinations fail before either root is copied; a later I/O failure can
still leave a partial pair which must be quarantined together.

The runtime verifies the backup first, refuses either non-empty destination before
copying, creates every child exclusively, opens the restored pair and completes
both `verify()` calls. It then compares the restored complete roots and ledger tail
with the external checkpoint. A late filesystem failure can leave a partial restore;
quarantine both destinations and start again with two new empty roots. There is no
automatic cleanup or disposal.

## Deterministic non-live recovery rehearsal

The repository can exercise the whole provider-independent operator journey before
a deployment is selected:

```bash
pnpm --filter @gis-ai-go/mcp-gateway run prepare:test
pnpm --filter @gis-ai-go/mcp-gateway run build
node scripts/rehearse_evidence_checkpoint_recovery.mjs
```

The rehearsal starts one synthetic fixture writer in a separate process and waits
for it to exit before asserting quiescence. It probes the temporary filesystem with
the `synthetic-test-fixture` classification, a fixed observation time and a
deterministic caller-supplied fixture mount identity. The resulting filesystem
observation is embedded in the rehearsal result. The rehearsal creates and verifies
one non-empty linked checkpoint, moves the stopped source pair into a temporary
quarantine without deleting it, restores into two new empty roots, and invokes the
gateway's exact evidence-storage readiness verifier on the restored pair. It then
removes its temporary rehearsal root. The closed path-free
`gis-ai-go.evidence-checkpoint-recovery-rehearsal.v1` result fixes provider calls
at zero and records that no service was started and deployment readiness was not
evaluated.

This is a deterministic synthetic local rehearsal of the repository mechanics. It
is not evidence of a provider supervisor, an admitted mounted volume, an
independently retained external checkpoint, a running service or a production
recovery exercise.

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
