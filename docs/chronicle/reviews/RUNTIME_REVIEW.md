# Runtime review at the Volume 1 checkpoint

Review date: 14 September 2026. Source checkpoint:
`6c76c92a18da779766f8d49acbbd7dbbd31abb97`.
Review author: a Codex subagent delegated by the lead coding agent.
This is a review artefact, not an activation or release acceptance.

## Assessment

The reviewed critical paths show a coherent and unusually explicit approach to
authority: the same immutable assembly supplies direct API and MCP operations;
successful results carry evidence; discovery can be reduced by policy and provider
state; new provider work is admitted before it consumes an immutable claim; and
provider results preserve their native identifiers and rights. Those are observed
code properties, not evidence that the process has eliminated defects.

The main engineering debt is the cost of repeatedly proving those properties in
large, tightly connected runtime modules. Local evaluation is already useful, but
its time-limited approved cache and session-only state mean that an enduring local
product needs its own completion contract. No P0 or P1 defect was established in
the inspected paths. The scoped review covers all 80 maintained source files,
with complete-file reading or direct critical-path inspection identified below.
It is not a claim of exhaustive line-by-line assurance or absence of defects.

## Method and coverage

All 80 maintained TypeScript, Python and JSON source files under the gateway,
shared packages and execution service received direct code inspection. Review followed
startup, assembly, provider admission, policy, query, persistence, reconciliation,
readiness, transport registration and private execution cancellation. Component
README guidance was compared with the current sources. Source/test cross-checks
were used to distinguish accepted limits from unexpected behaviour.

Coverage codes:

- **D**: the complete source file was read in this review.
- **T**: named critical sections and their dependencies were inspected. This is
  risk-based code review, not a representation that every line was read.

The completed scope comprises 59 complete-file reads and 21 critical-path reviews;
no source file remains inventory-only. Targeted sections are recorded below, with
finding-specific evidence in the findings and strengths. Tests, build scripts,
front ends and repository-wide security assessment are companion review scopes.
Historical CI is supporting evidence only; it is not a fresh test run.

## Findings and opportunities

### RUN-01: readiness repeats full synchronous evidence replay

Classification: confirmed implementation behaviour; performance risk, medium
priority for the separate optimisation stage.

[Readiness](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/apps/mcp-gateway/src/governed-assembly.ts#L534)
first invokes `verifyEvidenceReadinessIntegrity` and later invokes
`evidenceReconciliationClaimCapacity`. Both call the same complete linked-store
verifier. Within each linked verification,
[the ledger is verified](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/apps/mcp-gateway/src/readiness-integrity.ts#L115)
and the reconciliation verifier calls
[`ledger.inspectReceipts`](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/packages/evidence/src/reconciliation-index.ts#L1223),
which verifies the ledger again. A ready response therefore has four complete
ledger replays through these paths, in addition to two index checks.

The ledger uses synchronous directory enumeration, reads, canonical parsing and
digest verification. Its
[record/event loops](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/packages/evidence/src/public-ledger.ts#L1193)
grow with retained evidence. Each
[governed operation](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/apps/mcp-gateway/src/governed-assembly.ts#L517)
also performs complete dependency verification. This is strong tamper detection
with an unmeasured latency cost; it is not yet a demonstrated production outage.

First improvement: return verified capacity from the first readiness pass and
reuse it during that same synchronous assessment. Keep the existing replay
semantics until the combined result's authority is tested. Then consider one
verified ledger snapshot for a single linked check. Do not introduce an
mtime-only cache, bypass a full restart verification, or suppress tamper detection.

Acceptance: count replay invocations deterministically; prove one combined
readiness pass; preserve corruption, foreign-store, capacity, mutation and
same-key recovery failures. Measure p50/p95 latency, CPU, bytes read and event-loop
delay at 0, 10, 100 and 1,000 ledger events before proposing longer-lived caching.

### RUN-02: the only local data path expires without a readiness freshness check

Classification: confirmed future usability limitation; medium priority before
claiming an enduring local evaluation release.

The approved record's `stale_after` is `2027-02-20T20:21:08.947Z`.
[The cache reader rejects it at that instant](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/packages/provider-adapter-sdk/src/ons-approved-cache.ts#L446).
[The local launcher](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/apps/mcp-gateway/src/local-candidate-main.ts#L183)
always injects an in-memory 503, so it has no alternate success path after expiry.
Assembly readiness checks stores, lifecycle and claim capacity; it does not ask
whether the approved cache remains usable. Thus its current contract can report
ready while every new local `data.query` fails due to cache age.

This conclusion is from source tracing, not a newly executed future-clock
end-to-end test. The refusal to serve stale data is correct. The gap is in
communicating whether the advertised local journey remains executable.

Acceptance: test the instant before, exactly at and after expiry; make local
readiness or an explicit local capability-health field explain the unavailable
data path; preserve evidence inspection. Add an owned refresh plan, or a separately
reviewed synthetic learning profile with explicit provenance. Never change the
system clock, extend historical approvals or relabel fixture observations as
current provider evidence.

### RUN-03: execution cancellation has no reserved capacity

Classification: confirmed admission behaviour; medium priority before expanding
the Python service to long-running or saturated workloads.

[The private server](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/services/geo-execution/src/gis_ai_go_execution/http.py#L242)
reserves one of eight slots for each accepted connection before inspecting its
method/path. At eight occupied slots every next connection gets 429, including
the DELETE request that would cancel one of the active executions.
[Cancellation dispatch](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/services/geo-execution/src/gis_ai_go_execution/http.py#L480)
is therefore unavailable at full admission.

Existing tests separately prove normal cancellation and rejection of the ninth
connection. Both passed in this review (two tests, 2.038 seconds, Python 3.14.6).
The combined saturated-cancellation case is not covered by those tests. The first
run was blocked by the sandbox's socket permission; the authorised repeat passed.

The fixed tiny synthetic workload and deadline bound reduce impact, and the
current exact-five local ONS journey does not invoke this Python service.
This is not a blocker for today's local demonstration. Before broader execution,
reserve bounded control-plane capacity or separate the internal cancellation
channel. A fix must retain an overall connection/thread ceiling and cover both
saturated work admission and successful cancellation of an active request.

### RUN-04: domain contracts and runtime orchestration need smaller modules

Classification: maintainability opportunity; medium priority, separate stage.

At the checkpoint, `checkpoint.ts` is 2,530 lines,
`public-read-receipt.ts` 2,045, `receipt.ts` 1,746,
`reconciliation-index.ts` 1,553 and `public-ledger.ts` 1,420.
Gateway `data-query-application.ts` is 1,307 lines,
`catalogue-application.ts` 1,224, `mcp-server.ts` 1,064 and
`http-app.ts` 1,017. Line counts identify review cost, not defects.

The
[data-query transaction](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/apps/mcp-gateway/src/data-query-application.ts#L985)
contains request validation, policy, provider admission, durable ownership,
execution, cache eligibility, result checking and evidence commit. It is a strong
candidate for named internal stages that retain their ordering explicitly.

There is also a narrower canonicalisation duplication:
[`cursor.ts`](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/apps/mcp-gateway/src/cursor.ts#L35)
contains an older recursive serializer, while the evidence package additionally
rejects sparse arrays, accessors, proxies, cycles and invalid Unicode. Current
cursor inputs are constrained strings, integers and normalised search criteria;
this is maintenance debt, not an established injection path. Consider a shared
implementation only after proving compatibility for every existing cursor and
digest fixture. Different canonical byte contracts must not be silently merged.

Extract small cohesive modules: canonical file I/O, ledger records/events,
checkpoint manifests/publication/restore, operation contracts, query admission,
query execution and evidence commit. Keep v1/v2/v3 schema and digest domains
unchanged. Preserve independent builder/verifier checks: deduplicating both into
the same unchecked helper can remove the independence that currently catches errors.

Acceptance: one module family per PR, unchanged public exports and canonical
fixtures, dependency-cycle checks, negative cases at every extracted boundary,
and before/after diff of operation discovery, schemas and accepted evidence bytes.

### RUN-05: the ONS profile is a deliberately narrow vertical slice

Classification: documented design trade-off; future extensibility work.

[Selection](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/apps/mcp-gateway/src/selection-application.ts#L368)
chooses from one candidate and
[policy](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/packages/policy-client/src/public-read-v2.ts#L29)
allows one exact ONS resource. The adapter, query, cache and receipt contract bind
that same query. This is an intentional authority boundary, not a generic
geospatial query engine.

For a second dataset, define a reviewed immutable dataset profile and an explicit
provider capability contract. Generalise only after adding that second concrete
case. Do not replace the existing closed selection with caller-supplied URLs,
unbounded SQL or arbitrary code. The learning path must distinguish the working
vertical slice from the future platform.

### RUN-06: component guidance retained earlier lifecycle wording

Classification: documentation defects; corrected in this work package.

The gateway README did not clearly describe the distinct current inspection
receipt and its blocked-server build recipe omitted required workspace builds.
Authority/policy READMEs omitted the v3 inspection plane; contracts and evidence
READMEs described now-used components as future or inactive; evidence guidance
did not distinguish existing checkpoint helpers from an operated backup service;
the provider README did not distinguish local construction from production
registration. The narrow README corrections retain the production boundary.

### RUN-07: a held provider lease does not recheck its prepared deadline

Classification: source-confirmed deadline-enforcement defect; medium priority
for reliability work before expanding live-provider use. No live failure was
reproduced in this review.

[Preparation](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/packages/provider-adapter-sdk/src/ons-data-api.ts#L928)
captures `startedAt` and an absolute `deadline`. The public reservation interface
allows a caller to start the lease later. However,
[execution](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/packages/provider-adapter-sdk/src/ons-data-api.ts#L968)
schedules its timeout using `deadline - startedAt`, without subtracting time
already spent holding that reservation. The admission check enforces a separate
20-second lease expiry, not the potentially shorter caller deadline.

For example, a two-second caller deadline can expire while a still-valid lease is
held for three seconds; `start()` can then initiate transport and grant the
original timeout again. This is a deterministic source trace, not a claim about
the duration of an observed provider request. Current gateway orchestration
normally starts the lease synchronously after claiming evidence ownership, and
the local teaching path does not contact the provider, reducing immediate impact.

[Existing tests](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/packages/provider-adapter-sdk/test/ons-data-api.test.ts#L959)
cover expired lease admission and a deadline already expired at preparation,
but not a shorter deadline expiring between reservation and start. Acceptance:
recheck the effective deadline at start, reject expiry without consuming an
attempt, time only the remaining execution window, and test a partially elapsed
reservation with a deterministic clock. Retain independent process-wide admission
clocking, cancellation, lease cleanup and retry budgets.

## Strengths supported by inspected code

- [One immutable assembly](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/apps/mcp-gateway/src/governed-assembly.ts#L437)
  assigns the same operation array to API and MCP. Suspension only subtracts.
- [Query admission precedes immutable ownership](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/apps/mcp-gateway/src/data-query-application.ts#L1055);
  result delivery follows linked receipt persistence and reconciliation.
- [Fixed HTTPS](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/packages/provider-adapter-sdk/src/fixed-https.ts#L334)
  validates DNS answers, pins a checked address, verifies TLS and bounds the response.
- [Authority context](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/packages/authority-context/src/public-read-v2.ts#L12)
  is server-owned and anonymous-open; it does not trust caller entitlement claims.
- [Geometry](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/services/geo-execution/src/gis_ai_go_execution/geometry.py#L68)
  is deterministic, bounds coordinates, rejects malformed polygons and includes
  boundary points. Its simple outer-ring scope is explicit.
- [Catalogue pagination](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/apps/mcp-gateway/src/catalogue-application.ts#L1023)
  binds cursors to both content identity and normalised criteria.
- [Local startup and shutdown](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/apps/mcp-gateway/src/local-candidate-main.ts#L289)
  use fixed loopback authority, private per-session stores and retryable cleanup.

## Separate implementation stage

1. Triage the seven findings against the local-edition promise, combining the
   completed source coverage with the companion tests, scripts, schemas, front-end
   and security reviews. Record each accepted fix or support limitation.
2. Capture performance baselines using deterministic workloads and record hardware,
   runtime, source revision and commands. A size ceiling is not a measured latency SLO.
3. Correct local cache-health communication, held-lease deadline enforcement and
   the clone/start guidance with focused boundary regressions.
4. Remove same-assessment duplicate verification with corruption regressions.
5. Extract file-storage and query orchestration modules without changing contracts.
6. Add bounded cancellation control capacity before expanding execution workloads.
7. Consider catalogue search indexing or a second provider only after a measured
   need and a concrete accepted use case.

Each step has its own issue, changed-path checks, independent review and rollback
point. Public completion claims must identify which steps were accepted; this
review does not implicitly implement any runtime change.

## Source coverage register

The scope excludes generated `dist`, installed dependencies and external vendor
code. D/T state review depth, not a certification that the file is defect-free.

| Source | Coverage |
| --- | --- |
| [apps/mcp-gateway/src/activation.ts](../../../apps/mcp-gateway/src/activation.ts) | D |
| [apps/mcp-gateway/src/candidate-activation.ts](../../../apps/mcp-gateway/src/candidate-activation.ts) | D |
| [apps/mcp-gateway/src/catalogue-application.ts](../../../apps/mcp-gateway/src/catalogue-application.ts) | T |
| [apps/mcp-gateway/src/catalogue-snapshot.ts](../../../apps/mcp-gateway/src/catalogue-snapshot.ts) | T |
| [apps/mcp-gateway/src/container-healthcheck.ts](../../../apps/mcp-gateway/src/container-healthcheck.ts) | D |
| [apps/mcp-gateway/src/container-ingress.ts](../../../apps/mcp-gateway/src/container-ingress.ts) | D |
| [apps/mcp-gateway/src/container-main.ts](../../../apps/mcp-gateway/src/container-main.ts) | D |
| [apps/mcp-gateway/src/cursor.ts](../../../apps/mcp-gateway/src/cursor.ts) | D |
| [apps/mcp-gateway/src/data-query-application.ts](../../../apps/mcp-gateway/src/data-query-application.ts) | T |
| [apps/mcp-gateway/src/evidence-application.ts](../../../apps/mcp-gateway/src/evidence-application.ts) | D |
| [apps/mcp-gateway/src/execution-envelope.ts](../../../apps/mcp-gateway/src/execution-envelope.ts) | D |
| [apps/mcp-gateway/src/governed-assembly.ts](../../../apps/mcp-gateway/src/governed-assembly.ts) | T |
| [apps/mcp-gateway/src/http-app.ts](../../../apps/mcp-gateway/src/http-app.ts) | T |
| [apps/mcp-gateway/src/http-main.ts](../../../apps/mcp-gateway/src/http-main.ts) | D |
| [apps/mcp-gateway/src/http-server.ts](../../../apps/mcp-gateway/src/http-server.ts) | T |
| [apps/mcp-gateway/src/index.ts](../../../apps/mcp-gateway/src/index.ts) | D |
| [apps/mcp-gateway/src/local-candidate-main.ts](../../../apps/mcp-gateway/src/local-candidate-main.ts) | D |
| [apps/mcp-gateway/src/mcp-http.ts](../../../apps/mcp-gateway/src/mcp-http.ts) | D |
| [apps/mcp-gateway/src/mcp-request-signal.ts](../../../apps/mcp-gateway/src/mcp-request-signal.ts) | D |
| [apps/mcp-gateway/src/mcp-server.ts](../../../apps/mcp-gateway/src/mcp-server.ts) | T |
| [apps/mcp-gateway/src/mcp-stdio-main.ts](../../../apps/mcp-gateway/src/mcp-stdio-main.ts) | D |
| [apps/mcp-gateway/src/mcp-stdio.ts](../../../apps/mcp-gateway/src/mcp-stdio.ts) | D |
| [apps/mcp-gateway/src/metadata.ts](../../../apps/mcp-gateway/src/metadata.ts) | D |
| [apps/mcp-gateway/src/openapi.ts](../../../apps/mcp-gateway/src/openapi.ts) | T |
| [apps/mcp-gateway/src/problem.ts](../../../apps/mcp-gateway/src/problem.ts) | D |
| [apps/mcp-gateway/src/public-origin.ts](../../../apps/mcp-gateway/src/public-origin.ts) | D |
| [apps/mcp-gateway/src/readiness-integrity.ts](../../../apps/mcp-gateway/src/readiness-integrity.ts) | D |
| [apps/mcp-gateway/src/reconciliation-applications.ts](../../../apps/mcp-gateway/src/reconciliation-applications.ts) | D |
| [apps/mcp-gateway/src/selection-application.ts](../../../apps/mcp-gateway/src/selection-application.ts) | T |
| [packages/authority-context/src/evidence-inspect-v3.ts](../../../packages/authority-context/src/evidence-inspect-v3.ts) | D |
| [packages/authority-context/src/index.ts](../../../packages/authority-context/src/index.ts) | D |
| [packages/authority-context/src/public-read-v2.ts](../../../packages/authority-context/src/public-read-v2.ts) | D |
| [packages/contracts/src/catalogue/catalogue.ts](../../../packages/contracts/src/catalogue/catalogue.ts) | T |
| [packages/contracts/src/catalogue/index.ts](../../../packages/contracts/src/catalogue/index.ts) | D |
| [packages/contracts/src/catalogue/links.ts](../../../packages/contracts/src/catalogue/links.ts) | D |
| [packages/contracts/src/catalogue/types.ts](../../../packages/contracts/src/catalogue/types.ts) | D |
| [packages/contracts/src/execution/index.ts](../../../packages/contracts/src/execution/index.ts) | D |
| [packages/contracts/src/execution/types.ts](../../../packages/contracts/src/execution/types.ts) | D |
| [packages/contracts/src/index.ts](../../../packages/contracts/src/index.ts) | D |
| [packages/evidence/src/canonical-json.ts](../../../packages/evidence/src/canonical-json.ts) | D |
| [packages/evidence/src/checkpoint-publication-test-seam.ts](../../../packages/evidence/src/checkpoint-publication-test-seam.ts) | D |
| [packages/evidence/src/checkpoint.ts](../../../packages/evidence/src/checkpoint.ts) | T |
| [packages/evidence/src/digest.ts](../../../packages/evidence/src/digest.ts) | D |
| [packages/evidence/src/evidence-inspect-receipt.ts](../../../packages/evidence/src/evidence-inspect-receipt.ts) | T |
| [packages/evidence/src/index.ts](../../../packages/evidence/src/index.ts) | D |
| [packages/evidence/src/public-ledger-capacity.ts](../../../packages/evidence/src/public-ledger-capacity.ts) | D |
| [packages/evidence/src/public-ledger.ts](../../../packages/evidence/src/public-ledger.ts) | T |
| [packages/evidence/src/public-read-receipt.ts](../../../packages/evidence/src/public-read-receipt.ts) | T |
| [packages/evidence/src/receipt.ts](../../../packages/evidence/src/receipt.ts) | T |
| [packages/evidence/src/reconciliation-index-capacity.ts](../../../packages/evidence/src/reconciliation-index-capacity.ts) | D |
| [packages/evidence/src/reconciliation-index.ts](../../../packages/evidence/src/reconciliation-index.ts) | T |
| [packages/policy-client/src/evidence-inspect-v3.ts](../../../packages/policy-client/src/evidence-inspect-v3.ts) | D |
| [packages/policy-client/src/index.ts](../../../packages/policy-client/src/index.ts) | D |
| [packages/policy-client/src/public-catalogue-v1.json](../../../packages/policy-client/src/public-catalogue-v1.json) | D |
| [packages/policy-client/src/public-evidence-inspect-v3.json](../../../packages/policy-client/src/public-evidence-inspect-v3.json) | D |
| [packages/policy-client/src/public-read-v2.json](../../../packages/policy-client/src/public-read-v2.json) | D |
| [packages/policy-client/src/public-read-v2.ts](../../../packages/policy-client/src/public-read-v2.ts) | D |
| [packages/provider-adapter-sdk/src/contract.ts](../../../packages/provider-adapter-sdk/src/contract.ts) | D |
| [packages/provider-adapter-sdk/src/fixed-https.ts](../../../packages/provider-adapter-sdk/src/fixed-https.ts) | T |
| [packages/provider-adapter-sdk/src/index.ts](../../../packages/provider-adapter-sdk/src/index.ts) | D |
| [packages/provider-adapter-sdk/src/ons-approved-cache.ts](../../../packages/provider-adapter-sdk/src/ons-approved-cache.ts) | T |
| [packages/provider-adapter-sdk/src/ons-data-api.ts](../../../packages/provider-adapter-sdk/src/ons-data-api.ts) | T |
| [packages/provider-adapter-sdk/src/ons-live-probe-record.ts](../../../packages/provider-adapter-sdk/src/ons-live-probe-record.ts) | D |
| [packages/provider-adapter-sdk/src/ons-live-probe.ts](../../../packages/provider-adapter-sdk/src/ons-live-probe.ts) | D |
| [packages/provider-adapter-sdk/src/strict-json.ts](../../../packages/provider-adapter-sdk/src/strict-json.ts) | D |
| [packages/provider-adapter-sdk/src/synthetic-fixture.ts](../../../packages/provider-adapter-sdk/src/synthetic-fixture.ts) | D |
| [packages/provider-adapter-sdk/src/trace-context.ts](../../../packages/provider-adapter-sdk/src/trace-context.ts) | D |
| [packages/provider-adapter-sdk/src/types.ts](../../../packages/provider-adapter-sdk/src/types.ts) | D |
| [packages/tool-registry/src/index.ts](../../../packages/tool-registry/src/index.ts) | D |
| [packages/tool-registry/src/registry.ts](../../../packages/tool-registry/src/registry.ts) | T |
| [packages/tool-registry/src/types.ts](../../../packages/tool-registry/src/types.ts) | D |
| [services/geo-execution/src/gis_ai_go_execution/__init__.py](../../../services/geo-execution/src/gis_ai_go_execution/__init__.py) | D |
| [services/geo-execution/src/gis_ai_go_execution/__main__.py](../../../services/geo-execution/src/gis_ai_go_execution/__main__.py) | D |
| [services/geo-execution/src/gis_ai_go_execution/boundary.py](../../../services/geo-execution/src/gis_ai_go_execution/boundary.py) | D |
| [services/geo-execution/src/gis_ai_go_execution/canonical.py](../../../services/geo-execution/src/gis_ai_go_execution/canonical.py) | D |
| [services/geo-execution/src/gis_ai_go_execution/errors.py](../../../services/geo-execution/src/gis_ai_go_execution/errors.py) | D |
| [services/geo-execution/src/gis_ai_go_execution/fixtures.py](../../../services/geo-execution/src/gis_ai_go_execution/fixtures.py) | D |
| [services/geo-execution/src/gis_ai_go_execution/geometry.py](../../../services/geo-execution/src/gis_ai_go_execution/geometry.py) | D |
| [services/geo-execution/src/gis_ai_go_execution/http.py](../../../services/geo-execution/src/gis_ai_go_execution/http.py) | T |
| [services/geo-execution/src/gis_ai_go_execution/service.py](../../../services/geo-execution/src/gis_ai_go_execution/service.py) | D |

### Critical-path depth record

Ranges below refer to the pinned checkpoint, not lines shifted by later edits.
Declarations and call sites were also searched to trace dependencies. This records
what T means; it does not silently promote those files to complete-file reading.

| Source (relative to its component's `src`) | Direct inspection focus |
| --- | --- |
| Gateway `catalogue-application.ts` | Validation and method structure; search, cursor and result path, lines 1023–1098 |
| Gateway `catalogue-snapshot.ts` | Immutable map, safe-path inventory, bounded reads and checksum-linked loader, lines 1–450 and 700–838 |
| Gateway `data-query-application.ts` | Complete query transaction, lines 985–1307; validator and dependency call sites |
| Gateway `governed-assembly.ts` | Dependency admission, immutable assembly, operation verification and readiness, lines 190–603 |
| Gateway `http-app.ts` | Strict JSON scanner, bounded body reader, exact application linkage, Host/Origin, readiness and operation dispatch, lines 273–636 and 647–1017 |
| Gateway `http-server.ts` | Node ingress configuration and validation, lines 1–230; route, timeout and admission call sites |
| Gateway `mcp-server.ts` | Request/privacy limits and operation registration, lines 110–245 and 480–660; factory call sites |
| Gateway `openapi.ts` | Schema/operation declarations, lines 1–145; shared-operation use and public-origin call sites |
| Gateway `selection-application.ts` | Candidate/policy selection and result construction, lines 325–465; request validator call sites |
| Contracts `catalogue/catalogue.ts` | Catalogue contract parsing and primitive validation, lines 1–170; parser/export map |
| Evidence `checkpoint.ts` | Private file reads, publication/copy and linked verification, lines 289–423 and 1561–1810; capture/verification/reconciliation, lines 2038–2390; restore, lines 2444–2530 |
| Evidence `evidence-inspect-receipt.ts` | Current inspection receipt construction, structural and independent-material verification, lines 800–945 |
| Evidence `public-ledger.ts` | Append, full replay and receipt inspection, lines 1046–1275 and 1345–1410; store operation map |
| Evidence `public-read-receipt.ts` | Receipt construction, policy linkage and independent-material verification, lines 1802–2045 |
| Evidence `receipt.ts` | Catalogue receipt construction, structural and independent-material verification, lines 1524–1746 |
| Evidence `reconciliation-index.ts` | Claim acquisition, full verification, capacity and reconciliation, lines 1073–1553 |
| Adapter SDK `fixed-https.ts` | DNS validation, pinned connection, response limits and abort, lines 222–504 |
| Adapter SDK `ons-approved-cache.ts` | Cache construction/read authority, query and freshness, lines 310–490; closed declaration guards |
| Adapter SDK `ons-data-api.ts` | Process admission, lines 148–235; deadline parser, lines 751–812; complete adapter class, lines 840–1100; lease start/release wrappers, lines 1274–1364 |
| Registry `registry.ts` | Tool capability/schema generation and exact operation selection, lines 760–914; registry/validator call sites |
| Python `http.py` | Private boundary, request handling, cancellation and connection admission, lines 1–190 and 242–549; remaining configuration call sites |

## Verification record

- Fresh focused execution check: normal HTTP cancellation and ninth-connection
  admission tests both passed, 2.038 seconds, on Python 3.14.6. This is a focused
  diagnostic, not the locked repository assurance environment.
- No live provider call, package installation, runtime mutation, full-suite rerun
  or new performance measurement was performed for this review.
- README corrections were checked against current exports, orchestration and
  package scripts. The package installation/build recipe still needs its clean
  clone acceptance in the local completion stage.
- All 82 local Markdown links across this review and its local completion plan
  resolve; `git diff --check` passed after the edits.
- Primary architectural evidence is the pinned source above. Prior CI must be
  cited separately by run and commit when used in the chronicle.
