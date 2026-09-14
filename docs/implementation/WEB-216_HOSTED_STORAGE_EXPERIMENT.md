# WEB-216: hosted-storage foundation

Status: inactive application and storage implementation; not a deployed service.  
Recorded on 14 September 2026 for X05/X07 and M5 of the
[public-data workbench](WEB-216_PUBLIC_DATA_WORKBENCH.md).

## Why the local store is not enough

The local workbench retains evidence in an owner-only filesystem store. A Site
cannot use that laptop directory as its durable storage. The hosted variant needs
its own atomic writes, lost-response recovery, capacity checks and restart proof.
These controls must work in the actual hosting runtime, not merely in a mock.

| Layer | Responsibility | What it cannot establish |
| --- | --- | --- |
| [Transaction model](../../packages/evidence/src/web216-transactional-contract.ts) | Validate complete, content-addressed records, events and head; construct an append plan. | A plan or hash is not a database commit. |
| [D1-compatible adapter](../../packages/evidence/src/web216-transactional-d1.ts) | Read the whole snapshot, compare-and-swap its head, then verify read-back. | Structural API compatibility is not a deployed D1 binding, attestation or disaster-recovery proof. |
| [Hosted capture application](../../apps/mcp-gateway/src/web216-hosted-cpih-application.ts) | Resolve a non-authorising selection, retrieve the admitted capture, replay a key and inspect existing evidence. | There is no mounted HTTP endpoint, live provider, user identity or release activation. |

The original local application, old two-tool Site, port 8787 candidate and
inactive production defaults are unchanged. The new application still admits
only the source-verified L522/MM23 capture for January and July 2026.

## Atomic storage decision

For this small experiment, keep one complete canonical JSON snapshot in a
singleton database row. A fixed, parameterised `UPDATE` replaces it only if the
expected store ID, checkpoint and sequence still match. The record, key hash,
event chain and head therefore change together in one statement. A competing
writer receives a stale-head outcome rather than silently appending to a changed
history. The application makes no automatic retry.

This is a bounded alternative to a multi-table transaction. A zero-row comparison
is not necessarily an SQL error: placing later inserts after it in a batch would
need additional enforcement. The single-row design avoids that failure class at
the cost of reading and rewriting the complete snapshot. It is not the proposed
storage design for a large public service.

The adapter uses only fixed prepared statements and bound values. Normal requests
never create tables or initialise missing state. Schema migration and initial
provisioning belong to a separate, trusted deployment step. Missing or corrupt
state fails closed rather than creating a fresh history.

The [D1 binding reference](https://developers.cloudflare.com/d1/worker-api/d1-database/)
documents prepared statements and auto-commit/batch behaviour. The
[read-replication guide](https://developers.cloudflare.com/d1/best-practices/read-replication/)
states that calls without the Sessions API go to the primary. This adapter does
not use sessions or replica bookmarks. Documentation establishes the platform
contract, not that an arbitrary supplied binding meets it; the application does
not label a structurally compatible test database as a verified D1 primary.

## Evidence and failure meanings

- A complete snapshot verifies exact source capture and software identity,
  record/event identities, sequence, key uniqueness and the complete chain.
  Unknown fields, inconsistent columns, extra rows, altered canonical bytes and
  repeated receipt identities are rejected.
- The reconciliation key is domain-separated and hashed; its raw value is not
  included in a receipt. Reusing a key for the other period is a conflict.
- Success requires the record to be present in fully verified read-back. Another
  legitimate writer may have advanced the checkpoint meanwhile. The result
  describes the returned snapshot, not independently proven freshness.
- Cancellation before issuing the update proves that this operation did not
  issue that write. Cancellation, timeout or an untrustworthy acknowledgement
  after issuance means **uncertain write**, not definite failure or absence.
  A subsequent read with the same key can recover a committed result without
  making a second record. Signals gate calls but do not interrupt database I/O.
- Initial provisioning follows the same uncertainty rule: if its insert was
  acknowledged but read-back fails, the result is uncertain, not “uninitialised”.
- Inspection returns existing evidence; it does not invent a new inspection
  receipt or claim to have witnessed the original write acknowledgement.

The separate result family is `gis-ai-go.web216-hosted-cpih-result.v1`. It does
not masquerade as the local filesystem receipt format. Full-chain verification
happens inside the application; the returned record, event and checkpoint are a
subset, not sufficient material for a consumer to reconstruct the entire chain.

Without an independently retained checkpoint, replacing the entire store with
an older, internally consistent snapshot is **not** detected. The software-bound
descriptor also prevents silently adopting old records under a different software
identity. Upgrades require reviewed migration or a separately retained generation,
not automatic reinitialisation. These limits are not attestation or disaster
recovery guarantees.

## Capacity and retention

The model has a hard ceiling of 128 records; a trusted assembly can choose less.
The adapter additionally limits canonical snapshot bytes to 1 MiB. The provisional
first hosted experiment should use 32 records, pending actual platform measures.
This is below the documented [D1 value-size limit](https://developers.cloudflare.com/d1/platform/limits/),
but does not establish acceptable end-to-end latency or hosting cost. Longer
admitted values can exhaust the byte limit before the record limit.

At record capacity, readiness becomes read-only: existing evidence remains
inspectable and same-key replay remains available; new writes are refused.
Readiness is a snapshot, not a reservation. Complete verification and write
amplification remain scaling constraints.

`retention_days: 365` and `retain_until` record retention requirements, **not an
implemented expiry/deletion service or a platform retention guarantee**. No record
is automatically deleted. Capacity rollover, backup, restore and the retention
operating procedure still need acceptance before wider deployment.

## Verification and reproducibility

On 14 September 2026 both affected TypeScript packages built successfully. The
35 focused checks passed: 13 transaction-model, 12 adapter and 10 application
tests. They cover real SQLite files and separate connections, exact reopen,
competing writes, post-commit response loss, malformed state, capacity, same-key
recovery, missing migration and cancellation during either pending read.
Local SQLite is a genuine storage test, but not hosted D1 execution.

After installing the pinned workspace dependencies and building the existing
gateway prerequisites:

```bash
pnpm --filter @gis-ai-go/evidence build
pnpm --filter @gis-ai-go/mcp-gateway build
node --test --test-skip-pattern='32/128 record comparison' \
  packages/evidence/dist/test/web216-transactional-contract.test.js \
  packages/evidence/dist/test/web216-transactional-d1.test.js \
  apps/mcp-gateway/dist/test/web216-hosted-cpih-application.test.js
```

The separate 32/128-record experiment records canonical bytes, SQLite allocation,
three warm and three reopened full-verification timings, and one compare-and-swap
including validation/read-back. It does not measure cloud networking, throughput
or provider costs. Run it explicitly when inputs change; canonical assurance
still includes the test file without reducing existing gates:

```bash
node --test --test-name-pattern='32/128 record comparison' \
  packages/evidence/dist/test/web216-transactional-d1.test.js
```

### Actual local Workers and D1

The optional [probe runner](../../scripts/web216_worker_storage_probe.mjs) bundles
the separately labelled [test fixture](../../scripts/web216_worker_storage_fixture.ts),
performs two writes in real workerd/D1, disposes the runtime, opens a fresh one
over the same database and compares the complete canonical snapshot. It refuses
provider egress and disables telemetry. It installs nothing and requires an
existing trusted tooling installation containing exactly Miniflare
`5.20260911.1-alpha`, workerd `1.20260911.1` and esbuild `0.28.1`:

```bash
node scripts/web216_worker_storage_probe.mjs --tooling-root /path/to/existing/tooling
```

Output is a fresh owner-only temporary directory, printed by the command. It
retains sources, compiled input hashes, executed bundle, plan, response bodies,
timings and either outcome or failure. The prerequisite compiled evidence is
trusted local input; these hashes are not a clean-build attestation. The fixture
uses synthetic software identity and fixed timestamps and must never be deployed
as an application endpoint. Local socket permission is required.

The portable probe passed from `2026-09-14T18:39:43.835Z` to
`2026-09-14T18:39:44.421Z`: two HTTP 200 responses, two restored records/events,
identical canonical snapshot and zero outbound attempts. The executed bundle
SHA-256 was `5b343f7501b96516a4f5355062cb41bbd6c5982ff04d759cb9ce1a77c3912959`.
Single-run write/read-back observations were 10 ms and 9 ms. This is local
dispose/recreate evidence, not hosted durability, crash recovery or cloud latency.

An earlier harness used the obsolete `d1Persist` option, silently discarded by
this Miniflare version. It wrote successfully but lost ephemeral state on disposal.
Reading the installed persistence contract led to `resourcePersistencePath` and
the successful restart. Both the failure and correction remain in the journal.

## Remaining hosted acceptance

Before presenting this as a working Site: prove Workers/D1 compatibility and
exact restart, apply schema-only migrations, provision a reviewed store identity,
add closed MCP/HTTP ingress and deadlines, verify the unchanged private audience,
and exercise manual and genuine page-tool journeys. Then prove retention across
deployment and an explicit rollback/restore procedure. None of those outcomes
can be inferred from this inactive application increment.

Security review must cover the assembled service, including origin/host checks,
identity, body/result limits and cancellation. A stronger review model can assist;
its availability or opinion is not a substitute for a reproduced finding,
executable regression or deployment evidence.
