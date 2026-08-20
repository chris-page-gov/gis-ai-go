# ADR-0011: Durable public evidence ledger

- status: proposed candidate; inactive
- date: 20 August 2026
- decision owner: Chris Page
- work item: [EVID-204](https://github.com/chris-page-gov/gis-ai-go/issues/22)

## Context

ADR-0010 produces a complete content-addressed inline receipt for each successful
anonymous-open catalogue result. Its policy decision and receipt honestly describe
the state at issue time: `inline-only`, `not-persisted` and `not-attested`. The
receipt contains digests rather than the raw query, cursor or result material.

EVID-204 also requires a portable durable store and `evidence.inspect`. Persistence
must not be inferred from an attempted write, and a storage fault must not allow a
successful operation to claim durable evidence.

## Decision

Use a directory of RFC 8785 canonical JSON files with three immutable surfaces:

- one content-addressed ledger descriptor;
- one content-addressed public evidence record for each accepted inline receipt;
  and
- one exclusively created, content-addressed event file per sequence number.

Each event binds the ledger, sequence, prior event identity, record and receipt
identities, replay key, persistence time and minimum retention time. Record and
event files are created with no-overwrite semantics and synchronised before the
operation returns. A complete verification pass runs before and after every write
and whenever the ledger is opened.

The stored record contains the exact inline receipt. It does not rewrite the
receipt's issue-time policy decision. A catalogue result gains a separate
`evidence_storage` reference only after the record and event have both been written
and the restarted-style verification pass succeeds. If no ledger is configured,
the accepted inline-only result is unchanged. If a configured ledger fails, the
catalogue operation fails rather than returning a success without its promised
storage reference.

The descriptor permits only anonymous-open `evidence.inspect`. The transport-neutral
inspector accepts one closed receipt identity, re-verifies the ledger, and returns
the record, event and storage reference. It does not register a route or tool. It
states that original parameter and result material was verified at ingest but is
not retained, so restart inspection verifies storage and receipt content binding
rather than replaying the original result.

The ledger stores no raw query, cursor, prompt, geometry, credential, personal data
or machine path. A deterministic replay key uses request and trace identifiers plus
the parameter and result digests. An existing binding is rejected rather than
appended again.

Retention is a minimum retention period fixed in the immutable descriptor. This
candidate implements no deletion or expiry job. Evidence remains inspectable after
`retain_until`; any future disposal process needs its own policy, event and review.

## Failure and recovery

Unexpected entries, symbolic links, non-canonical bytes, missing terminators,
sequence gaps, broken hash links, missing records, orphan records, duplicate replay
keys, content collisions and changed retention all fail closed. The supported
response is to stop the affected operation, quarantine the directory and restore a
complete verified copy. This candidate deliberately provides no in-place repair or
silent truncation recovery.

One writer owns a ledger root. Concurrent writers are not coordinated; exclusive
creation makes contention fail closed and can leave an orphan that blocks later
verification. Multi-process coordination is deferred to a later operational store.

## Consequences and residual boundary

- The storage API cannot overwrite an accepted record or event.
- Restart verifies canonical bytes, content identities, sequence, hash chain,
  receipt boundary, replay keys, retention and privacy claims.
- File-system write access is still a trust boundary. The chain is not a signature,
  WORM medium or malicious-operator defence, and deletion of a complete unanchored
  tail cannot be detected without an external checkpoint.
- No receipt or event is attested.
- No public listener, direct route, MCP tool, deployment or registry entry is
  activated by this decision.
- Full material replay, external checkpoints, backups, disaster recovery,
  multi-writer coordination and reviewed production retention remain release gates.
