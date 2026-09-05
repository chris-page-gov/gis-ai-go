# EVID-211 continuous evidence preservation

## Purpose and boundary

This runbook preserves primary delivery evidence before a source becomes unavailable.
It supports the later, separately authorised retrospective in
[issue 86](https://github.com/chris-page-gov/gis-ai-go/issues/86), but it does not
start that retrospective. Preservation means retaining an exact source object where
that is safe and authorised, or a closed, secret-redacted projection where the raw
record contains private client state, recording the transformation and making the
result independently checkable.

EVID-211 does not count or classify attempts, infer causes, calculate cost, assess
delivery performance, draw conclusions, redact material for a public report or
publish anything. It does not request hidden model reasoning or claim access to
unexposed chain-of-thought. It changes no product, gateway, evidence-ledger,
deployment, provider, registry, activation, version, tag or release state and is not
a `v0.2.0` gate.

## Private store boundary

The operator supplies `PRIVATE_STORE`. It must be an owner-only location outside
the repository checkout and outside the repository's `artifacts/` directory. The
actual path is private and must not appear in repository files, pull requests,
issues, logs or a future public projection.

The containing volume must enforce POSIX ownership and permissions. On macOS, the
capture and verifier attest the backing device rather than trusting its mount path.
They require an internal, non-ejectable, non-removable FileVault-encrypted volume
with global permissions enabled, and reject `noowners` or `unknownpermissions`.
This deliberately excludes the current External SSD even if it is mounted at an
unusual path. The SSD may still hold reproducible, non-sensitive build material,
but not this private store.

The capture process must:

- create store directories with mode `0700` and regular files with mode `0600`;
- refuse symbolic links, special files, path traversal and replacement of an
  existing source object;
- retain exact source bytes unchanged where permitted and identify them by SHA-256
  digest;
- never retain opaque Codex rollout files. Project only the user-visible
  conversation, agent and subagent metadata, delivery status and bounded tool-event
  evidence; exclude internal reasoning, compacted context, world state and
  instruction bodies, and record the excluded record types without their content;
- keep derived indexes or summaries separate and bind each one to the source
  digests it describes;
- make an unchanged repeat a true no-op, while recording a new event whenever a
  source generation, disposition or retained object changes; and
- exclude credentials, authentication codes, session tokens, private keys and
  other high-confidence secrets from text, JSONL, validated PNG and JPEG metadata,
  ZIP raw bytes, ZIP metadata and inspected ZIP members, including recognised
  UTF-16 and BOM-marked UTF-32 forms. Compressed PNG metadata is expanded within a
  fixed boundary before scanning, and recognised key containers inside ZIPs are
  excluded. Record the exclusion without copying the secret value. Do not retain
  an unclassified local opaque binary: record it as unavailable. Local binary
  capture is limited to a complete checksum-valid PNG, a bounded structurally
  valid JPEG or an inspected ZIP; generated Codex gzip projections have their own
  closed role and verifier.

Owner-only does not mean redistributable. Licensing, personal-data,
security-classification and confidentiality constraints remain attached to every
source. A later public retrospective requires a separate, evidence-by-evidence
review and explicit publication decision.

## Capture triggers

| Trigger | When to capture | Minimum action |
| --- | --- | --- |
| Client observation, failure or incident | Immediately after the bounded activity | Preserve available request and response material, client and version metadata, timestamps, exit state, screenshots and related verification output. |
| Context or machine transition | Before compaction, restart, client update, temporary-directory cleanup or removal of a local capture | Preserve available user-visible conversation, agent and subagent assignments and results, terminal evidence and selected local files. |
| Delivery milestone | After a feature, pull request, merge, protected-main verification or accepted release checkpoint | Preserve identifiers, commit and tree, review and check metadata, logs and the selected accepted artefacts. |
| Time sweep | At least once every 24 hours while the programme is active | Discover new or changed source records and check recorded retention deadlines. The command does not install a scheduler. |
| Expiry warning | As soon as a known retention deadline is 14 days away | Raise a visible warning and prioritise capture or record why capture is not authorised or possible. |

An event trigger does not wait for the 24-hour sweep. A sweep supplements event
captures and is safe to repeat. Every GitHub collection expands the explicit
`--since` boundary backwards by exactly 48 hours, so a daily sweep overlaps the
previous successful window and idempotently closes late-arriving metadata.

## Selective artefact policy

Always preserve the bounded metadata needed to locate and interpret a source:
repository, source identifier, pull request or issue, workflow run and job
identifiers, timestamps, commit and tree where known, retention information, byte
count, media type and SHA-256 digest. Preserve available timelines, reviews,
comments, check conclusions, job logs and transport metadata when they are in
scope.

The current GitHub Actions retention setting is preserved as provider context,
but it is not projected onto historical run logs. [GitHub documents that a
changed setting applies only to newly created logs and
artefacts](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository),
so a later policy snapshot cannot attest the creation-time policy of an older
run. Historical log expiry therefore remains `unknown` unless an independently
evidenced creation-time deadline is available. Retention values outside GitHub's
documented 1-to-400-day range fail closed.

Prioritise short-lived material in this order:

1. `ci-impact-plan-*` artefacts and other evidence with a 30-day retention period;
2. failed, cancelled or anomalous client and assurance runs;
3. accepted feature, interoperability and protected-main milestones; and
4. sources explicitly identified for the future retrospective.

Do not copy every large binary artefact by default. Retain a gateway image, Pages
source package, browser bundle or comparable heavy object only when it represents
an accepted milestone, is needed to investigate a failure, is the exact source of a
release or observation claim, or has another recorded reason. Use
`--artifact-max-bytes` to make the limit explicit. Artefact names are not unique:
key a GitHub artefact by its immutable identifier, workflow run and recorded
digest, not by its display name alone. Bind every retained archive or bounded
observation back to one captured provider metadata row for that repository and
run. The provider-reported byte count must match the download; when GitHub supplies
a SHA-256 digest, the download must match it before capture. Snapshot identities
for repository, retention, run, job, artefact and discussion JSON must equal the
digest of their retained canonical object. Every artefact archive or observation
also records the digest of the exact preceding artefact-metadata snapshot. The
offline verifier rejects rebinding to an older or later mutable snapshot.

If material has expired, cannot be accessed or is outside authority, add an
unavailable record with the source identifier, time, reason and available metadata.
Never manufacture or silently substitute the missing bytes.

## Capture

Capture GitHub source material from an explicit lower time bound and record the
trigger:

```bash
uv run --locked --cache-dir .uv-cache python scripts/capture_delivery_evidence.py \
  --store "$PRIVATE_STORE" \
  --repository chris-page-gov/gis-ai-go \
  --since <ISO-8601> \
  --trigger <trigger> \
  --download-run-logs
```

Add a repeated `--local-file <path>` or `--local-directory <path>` only for an
owner-selected local source. The programme sweep includes workflow logs through
`--download-run-logs`; omit it only when logs are explicitly outside that capture's
scope. Set `--artifact-max-bytes <bytes>` before selecting heavy GitHub artefacts.
Set `--max-capture-bytes <bytes>` to an explicit per-invocation ceiling (8 GiB by
default, at most 64 GiB); capture also preserves a 5 GiB free-space reserve. A
ceiling is cumulative across every retained object in that invocation, including a
Codex projection and its generation manifest.
The capture must not scan the home directory, client stores or unrelated projects
implicitly.

GitHub workflow discovery includes the documented maximum 35-day run duration
before the overlap window, then selects completed records by their update time. It
fails closed if a filtered result reports more runs than pagination returned. Run
artefacts are captured once at run scope; attempt-specific run metadata, jobs and
logs remain bound to their exact attempt.

GitHub collection is bounded by command invocations, elapsed time, metadata bytes
and retained/downloaded bytes. A paginated `gh api` invocation can make more than
one provider request internally, so the invocation counter is not described as an
HTTP-request count; the 60-second command timeout and 16 MiB response ceiling still
apply to each metadata invocation. A transient provider-unavailable result may be
retried at most twice after the first attempt with a fixed 0.1-second delay. Every
attempt consumes the same invocation, metadata-byte and wall-clock budgets.
Structural, byte-limit and JSON failures are not retried.

Preserve an explicit issue or pull-request discussion with a repeated
`--discussion-number <number>`. Preserve the current Codex task and its transitive
subagents as a user-visible projection only by supplying both its identifier and
each explicit session root:

```bash
uv run --locked --cache-dir .uv-cache python scripts/capture_delivery_evidence.py \
  --store "$PRIVATE_STORE" \
  --trigger pre-compaction \
  --codex-thread-id <thread-id> \
  --codex-session-root <explicit-session-root>
```

The projection reads session metadata to establish the task closure, uses an
immutable temporary read boundary for an active file, redacts high-confidence
credentials and authentication codes before retaining content, compresses the
result deterministically and writes a generation manifest. Raw rollout files and
non-user-visible reasoning are not retained. All projections in one closure and
their generation manifest are committed as one ordered recoverable transaction:
after an interruption the next writer either completes that exact transaction once
or fails closed on an unprovable state.

The source task-completion field `time_to_first_token_ms` is a latency measurement,
but its name is credential-shaped. The initial immutable capture therefore retains
only a fixed-length mask for that field. Later projections preserve the same
non-negative finite value as `first_output_latency_ms`, while generic `token` keys
remain secret-masked. The verifier accepts the legacy mask only at the exact
task-completion path.

Codex child agents may legitimately share their root task's `session_id`. The
capture therefore keys each source by its unique thread identifier and verifies
the parent-thread graph from one unambiguous target root; a shared session value is
grouping metadata, not a thread or ancestor identity. The capture represents the
alias separately and rejects a closure if that alias collides with a selected
non-ancestor thread. Self-parenting and cycles wholly inside the selected closure
fail closed; a selected child may retain an explicit parent outside the requested
subtree.

A rollout may restate its `session_meta` record after an internal client boundary.
The first source record remains authoritative and must identify the exact thread,
session and parent recorded in the projection header. A later restatement may
identify the current thread, its transitive parent lineage or the shared session
alias. A known thread must repeat its exact raw session and parent tuple: a
non-root parent cannot be omitted, set to `null` or supplied with another type,
and a root cannot acquire a parent. The pure alias form is admissible only as the
same session value with no parent. A restatement outside that rule is retained only
as a digest-bound exclusion stub, so it cannot silently change the projection's
provenance. `forked_from_id` is independent provenance rather than a parent edge:
the authoritative first record may identify a fork source outside the selected
subtree, while a later record may only repeat that same exact raw value. Projection
v2 and v3 bind that raw value with a domain-separated SHA-256 digest before URL
display sanitisation; the private query or fragment is not retained. The verifier
continues to read a legacy v1 fork value only when it is a complete canonical UUID,
for which the old transformation was injective. V1 does not attest cross-record
fork equality: an ancestor restatement may retain its own distinct UUID. An
overlapping capture regenerates every retained v1 or v2 projection under v3, whose
raw-value digest supplies the stronger equality rule.
Placement of a valid restatement is not treated as a new session or a second source
file.

Early v1 capture could also replace one over-deep projected record with the exact
closed `maximum-depth` omission marker before adding that record's source-line
digest and byte count. The verifier treats this only as a bounded legacy gap: it
requires the exact marker, counts it against the footer's retained-record total and
requires the unexplained footer byte residual to be at least one byte for every
marker and no larger than the per-line limit multiplied by the number of markers.
V2 and v3 never emit that form; they emit a source-line-digest-bound exclusion stub
instead. The overlapping refresh
therefore supersedes, but does not rewrite or overstate, the immutable v1 record.

Early v2 capture proved one redaction pass but did not require the output to be a
fixed point. The verifier recognises only the exact historical wrapper-depth form:
the complete record must normalise to the closed maximum-depth marker, depth alone
must explain the difference, every direct child must remain within the node and
depth bounds and every direct child must pass current redaction unchanged. This
private compatibility path does not make v2 reusable.

Every v3 line must be a redaction fixed point before it is staged: applying
the complete structural normalisation a second time must leave the first-pass
value unchanged. A bounded source value can become too deep when its final string
is replaced with a structured omission descriptor. Capture does not retain that
unstable intermediate form. It emits a source-line-digest-bound
`projection:redaction-maximum-depth` exclusion stub instead; any other
non-idempotent transformation uses the corresponding closed fixed-point stub.
Headers, footers and stubs have no fallback and fail the transaction if they are
not already stable. Codex projection serialisation requires strict canonical JSON
and rejects non-finite numbers, including numeric overflow. If final byte masking
changes the serialised bytes, capture repeats the fixed-point and canonical-JSON
checks before staging them. Byte-identical output retains the already established
strict canonical fixed-point proof. The ordinary secret checks still run, and the
offline verifier independently checks every retained line.

The text classifier distinguishes terminal `=` padding with no following value
from an assignment delimiter only in the closed whole-text or quoted-token forms.
This is a lexical distinction, not a claim that the token is valid encoded data or
safe content. The ordinary sensitive-key, excluded-internal-field and secret checks
still apply independently to the complete text. Malformed mixed text receives no
general padding or legacy exemption, and an actual assignment remains subject to
key classification.

Some v1 records also crossed the depth limit only after the closed projection
wrapper was added, although every direct wrapper child remained independently
within the limit. The verifier recognises that historical wrapper artefact only
for a v1 or intermediate-v2 projected record and only when every direct child
independently passes the current depth and redaction checks unchanged, the complete
record remains within the aggregate node cap and depth alone explains the old omission. It is
rejected for v3, and any deep, over-wide or newly redacted child still fails closed.

V1 and the intermediate v2 generation may also contain an owner-only user-message
path which the current path scrubber would omit. The verifier recognises only that
exact drift: the record must be a closed `user_message`, path replacement must be
the sole redaction category and every other payload and top-level field must be
unchanged. V3 removes the local path and rejects this compatibility rule. This is a
private compatibility boundary,
not permission to publish the v1 or v2 projection.

Before considering a prior generation for reuse, capture re-reads the durable
journal, validates the closed generation manifest and its source events, and hashes
every compressed projection against its declared object binding. It then reads the
closed projection header from the same open file descriptor, retains that descriptor
through semantic verification and then rechecks its inode, metadata and path. If any
captured projection uses v1 or v2, the whole generation is incompatible with v3: none of
its rows is accepted from the generation-level reuse result. The new sweep
re-evaluates the complete closure. An unchanged objectless exclusion may then reuse
its existing immutable event only after an exact source, disposition and repository
fingerprint comparison; this permits a mixed generation to commit its new v3
projections and manifest without duplicating the exclusion. A current v3 header is
only a candidate signal; the existing full projection, redaction, lineage and
generation verification must still pass before reuse. An unknown or malformed
schema, wrong header binding, missing object, path replacement, byte mismatch or
digest mismatch is an error rather than a cache miss. This avoids expanding a large,
valid obsolete generation twice without weakening content-address or structural
checks.

The closure topology is fixed by the initial inventory. An existing active rollout
may append after its immutable APFS snapshot without invalidating that point-in-time
projection. The projection source event and footer retain the before-and-after
snapshot-acquisition stats, while its generation-manifest row separately records
the final closure-inventory stat and whether it differs from the acquisition. This
keeps an append or same-inode rewrite visible without pretending that the later
bytes are in the immutable projection. Source identity replacement and truncation
still fail closed. Reuse considers only the newest manifest observation for a
source path and requires both mutation markers to be false; the next overlapping
sweep therefore captures the later generation rather than falling back to an older
stable projection. A new child path appearing during the transaction changes the
closure topology and requires a retry.

Codex closure capture writes path-free aggregate progress records to standard
error. Records contain only the phase, completed and total file counts, accounted
source bytes, staged projection bytes, reused-file count and elapsed seconds. They
never contain a store path, source path, task or session identifier, digest, trigger
or retained text. `projection-progress` means work is staged, not captured;
`commit-complete` is emitted only after the atomic batch commit or a verified
whole-generation no-op completes. A topology change after `final-topology-start`
therefore has no success record and leaves the journal and content-addressed store
unchanged. Standard output remains the single final machine-readable summary.

Each journal event records the capture time in UTC, the corresponding
`Europe/London` time, trigger, repository and source identifiers, source commit and
tree where known, retained objects, unavailable records and exclusions. Original
objects remain immutable; a repeated capture may reuse an existing digest but must
not overwrite it.

## Verification

Verify the complete private store offline after each capture and before relying on
it:

```bash
uv run --locked --cache-dir .uv-cache python scripts/verify_delivery_evidence.py \
  --progress \
  --store "$PRIVATE_STORE"
```

`--progress` writes only aggregate, path-free records to standard error. The
integrity phase reports completed and total object counts and unique object bytes;
the Codex phase reports completed and total projection counts, decompressed bytes
and elapsed time. It emits at bounded object, byte or time intervals so a long
verification is visibly advancing. Standard output remains the single final
machine-readable result.

The default is one verification worker. When a store contains several large Codex
projections, an operator may opt into 2 to 4 processes without changing the checks:

```bash
uv run --locked --cache-dir .uv-cache python scripts/verify_delivery_evidence.py \
  --progress \
  --workers 4 \
  --store "$PRIVATE_STORE"
```

Only the independent decompressed Codex projection checks run concurrently. Store
shape, object digests, journal continuity, generation manifests and topology remain
parent-process checks. Capture reuse and schema-compatibility validation always use
the serial path with their already-open descriptors. The process pool keeps at most
twice the worker count in flight, each worker holds at most one bounded projection
line, and the worker ceiling is 4. Parallel progress retains the same aggregate,
path-free and monotonic fields; failures are reported in manifest projection order.

Verification must fail closed when:

- an indexed object is missing or an unindexed object is present;
- a byte count or SHA-256 digest differs;
- a journal entry is malformed, out of sequence or breaks journal continuity;
- a source identity, repository, run, commit, tree or derivation binding conflicts
  with its recorded value;
- an object was overwritten instead of captured as a new source event;
- a directory or regular file has a broader mode than `0700` or `0600`;
- an entry has an unindexed extended ACL, resource fork or extended attribute
  (apart from the exact SIP-managed macOS provenance marker);
- a symbolic link, special file, unsafe relative path or path outside the store is
  present; or
- an unavailable source is presented as if its original bytes were retained.

The verifier independently rescans the journal and retained objects for the same
high-confidence secret forms. It also re-applies the Codex projection redaction
normalisation, so a self-consistent rewrite cannot introduce a sensitive key,
private local path or excluded internal field merely by recomputing hashes.

A content-addressed object that is conclusively bound by every journal claim as a
generated Codex projection gzip is size- and SHA-256-checked, format-checked and
then decompressed for complete line-by-line semantic, canonical, UTF-8, secret and
redaction verification. The verifier does not additionally treat its compressed
bytes as arbitrary UTF-16 text: that duplicate binary scan cannot inspect the
compressed plaintext and previously dominated verification time. Mixed,
mislabelled, plain or otherwise unclassified objects retain the generic binary
scan or fail closed. Projection secret-pattern checks use reviewed mandatory
markers to avoid applying all current patterns to a line that cannot match them;
any future pattern without an explicit marker automatically retains the full scan.

One store has a hard lifetime ceiling of 100,000 journal events, 128 MiB of journal
bytes and 64 MiB of expiry-ledger bytes. Create and verify a successor owner-only
store before any ceiling is reached; do not silently roll over, delete or overwrite
the first store.

Keep the verifier independent of network access. A passing result proves only that
the captured store is internally closed and byte-consistent; it does not attest the
truth of a source statement or establish that uncaptured evidence never existed.

## Recovery from failed verification

A historical capture can be byte-consistent while failing current semantic or
redaction verification. Keep that distinction explicit. Do not edit an old object,
rebuild its journal to make a check pass or add a broad legacy exemption.

1. Retain the predecessor store unchanged on its admitted owner-only volume. Record
   its complete private inventory, journal checkpoint and the verifier's precise
   limit, including which checks completed and which did not. Keep paths, digests
   and retained content out of repository and public records.
2. Create a fresh owner-only successor on an admitted volume. Re-capture only the
   authorised current source scope using the current projection schema. Preserve
   the selected source identifiers and capture bounds privately; record an expired
   or unavailable source explicitly. Re-capture is a new observation and does not
   reproduce an unavailable historical generation.
3. Run the complete offline verifier against the successor. A successful inventory
   check, partial semantic check or capture command alone is insufficient. Record
   the complete result and its store identity privately, including expiry warnings
   and exclusions.
4. Admit the repair through protected `main` with all mandatory checks passing.
   Switch scheduled captures only after the selected current successor has passed
   complete verification. Record the operational cutover, admitted inventory and
   complete verification result privately. Retain the predecessor and its
   verification limit as historical evidence. If the successor fails, leave the
   failed capture unpromoted.

Daily captures require complete offline verification. Each pass applies to the
privately identified store snapshot; it does not attest a later capture. The private
operating record holds the current inventory and cutover state, while repository
checkpoint figures remain dated historical measurements.

A passing successor does not mean the predecessor's semantics passed. This is
separate, non-blocking preservation maintenance; it does not start a retrospective,
publish source material, deploy a service or change the product release state.

## Measured operating envelope

These figures are measurements and planning estimates from the initial checkpoint,
not service-level promises:

- a warm event-triggered Codex closure with little change should take about 1 to 5
  minutes, plus about 1 minute 28 seconds for each changed source GiB;
- a cold or whole-root no-change closure currently takes about 25 to 30 minutes
  because reusable-generation validation remains serial;
- a selected GitHub sweep, including recovery of the initial bounded source set,
  takes about 90 minutes;
- a complete four-worker offline verification takes about 22 to 25 minutes; and
- a sequential 24-hour sweep, Codex closure and complete verification should take
  about 2 hours 18 minutes to 2 hours 25 minutes. An exceptional day on which all
  40 GB of source changes should remain within about 3 hours 15 minutes to 3 hours
  25 minutes.

Event triggers should be debounced while one capture owns the store lock. An
identical generation is a verified no-op, so capture frequency alone does not grow
the store. A future optimisation may parallelise descriptor-bound reusable-generation
validation, but it is not required for this preservation package.

## Initial protected-main checkpoint

The first capture is anchored to the protected-main state accepted through
[pull request 108](https://github.com/chris-page-gov/gis-ai-go/pull/108):

- commit `c331d3d7c04fee1a4a168abcc7ee762b46b07834`;
- protected-main assurance run
  [`33301768557`](https://github.com/chris-page-gov/gis-ai-go/actions/runs/33301768557);
  and
- protected-main CodeQL run
  [`33301768447`](https://github.com/chris-page-gov/gis-ai-go/actions/runs/33301768447).

The checkpoint should also retain the available issue, pull-request, review,
workflow and client-observation source records from the explicit `--since` bound.
Record the actual capture event and verifier result in the private journal. Do not
claim the checkpoint exists merely because this runbook defines it.

The initial checkpoint completed on 1 September 2026:

- the Codex closure inventory contained 986 source files and 40,119,920,014 source
  bytes;
- the Codex capture took 3,525.977 seconds and retained 866,345,623 compressed
  object bytes plus 2,466,179 metadata bytes;
- after the selected GitHub capture and bounded recovery, the complete journal
  contained 5,925 events and the store contained 5,126 immutable objects occupying
  2,649,437,251 bytes;
- the expiry ledger reported nine warnings; and
- the final complete verifier passed. Its integrity phase took about 3 minutes 52
  seconds and its four-worker Codex phase took about 17 minutes 56 seconds, about
  21 minutes 48 seconds in total.

The checkpoint's current closure used projection v3. Earlier v1 and v2 records
remain immutable historical evidence and are accepted only through their narrow documented
compatibility rules. The result does not attest source truth or timestamps, and it
has no independent anchor capable of detecting a coordinated whole-store rewrite.
It did not start retrospective analysis, calculate costs, authorise publication,
deploy a service, call a provider, activate the candidate, register tools, change a
version, create a tag or release `v0.2.0`. The owner-only path and journal-head
digest remain private.

## Recovery status on 5 September 2026

The later verifier reports from 1 and 2 September were assessed on 5 September.
The initial checkpoint's pass remains a historical observation. The predecessor
retained unchanged contains
6,011 journal events and 5,193 immutable objects occupying 2,651,662,328 bytes. All
5,193 objects passed integrity checks. Complete semantic verification then failed
at a known legacy v1 record. Because semantic verification stops at a failure, this
does not establish the absence of further semantic failures. A separate read-only
checkpoint comparison confirmed that the predecessor journal, ledger and inventory
remain unchanged. The terminal-padding correction does not justify accepting
malformed mixed text or adding a general legacy exemption.

An owner-only successor on the same admitted encrypted internal volume completed
its initial authorised source capture on 5 September 2026:

- the source inventory contained 1,028 files and 44,572,464,083 bytes;
- capture recorded 1,029 journal events: 1,023 retained capture events and six
  policy exclusions, with no unavailable records or warnings;
- retained compressed projections occupied 925,615,899 bytes and generation-manifest
  metadata occupied 2,124,447 bytes, totalling 927,740,346 captured bytes; and
- capture took 3,863.086 seconds; the final topology check and atomic commit passed.

Complete offline verification then passed for that initial successor baseline on
5 September 2026: 1,029 journal events, 1,023 immutable objects, 927,740,346 bytes
and no warnings. Both object integrity and complete projection semantics passed.
This result applies to that baseline only.

A later selected GitHub capture on 5 September 2026 completed 143 captures and
added 157 journal events, with nine no-ops, no exclusions, 14 unavailable records
and no warnings. Eleven unavailable records were outside the selected large-artefact
size policy; three Pages archives failed archive validation. Their precise
validation subreason was not established. Unavailable records remain explicit
coverage limits, and the capture result does not attest complete verification of
the combined store.

Operational admission follows the recovery procedure above: accepted protected-main
repair with passing mandatory checks and complete verification of the selected
current successor are both required. The operational cutover, current inventory and
subsequent verification results are recorded privately. These dated checkpoints do
not claim a later combined-store pass or scheduler resumption. The predecessor's
private checkpoint and exact verification limit remain separate from every
successor result.

## Future retrospective hand-off

Starting issue 86 remains a separate owner decision at a natural break after local
`v0.2.0` finalisation. At that point, the retrospective may read verified preserved
sources and create a distinct analysis layer. Any attempt chronology, outcome
classification, elapsed-time or cost calculation must cite the retained primary
record and state gaps or uncertainty. The private full-detail report stays in an
owner-approved private destination; a public redacted report is a separate
publication product with its own security, privacy, licensing and provenance
review.
