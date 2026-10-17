# Five-tool local acceptance

Observed: 17 October 2026. Status: the maintained provider-free local acceptance
and focused refusal/recovery checks passed. This record supplies local release
evidence; hosted, live-provider and supported-release acceptance remain separate.
The [release closure record](RELEASE_CLOSURE.md) tracks those remaining gates.

## Exact inputs and observed checks

The final clean-checkout runs used commit
[`0eae2d0f9262dc119f9313a6c45ef3ee18666e6a`][source] and tree
`deac5e4069bb0c0c6e79f999a73dc5afeb043214`. The maintained acceptance started at
16:13:22 UTC; the final preflight completed at 16:14:10 UTC. The checkout was
still clean when inspected at 16:14:11 UTC. This document was added afterwards;
it is not a self-referential claim about its eventual commit.

Environment: Linux `6.18.55`, x86_64; Node.js `24.19.0`; pnpm `10.33.2`;
uv `0.12.2`; Python `3.12.14`; pinned MCP client `2.0.0`, protocol `2026-07-28`.
Dependencies were installed already and operating-system caches were uncontrolled.
This is not a fresh-clone installation or a performance benchmark. Temporary
command search paths selected the exact pinned pnpm and uv binaries; repository
scripts and their assertions were unchanged. Socket permission was enabled for
the genuine loopback tests. Their provider-egress guards remained enabled.

| Check | Observed result | Source and scope |
| --- | --- | --- |
| `pnpm run test:local-candidate` | **15 passed, zero failed/skipped**: 14 gateway tests plus the real launcher acceptance. | Clean commit above. Builds catalogue/dependencies/gateway; checks all five tools, three resource classes, exact approved cache, expiry, guarded zero provider egress, occupied-port failure, orderly stop and removal of private session state. [Package command][command]; [independent runtime client][runtime-client]; [launcher][launcher]. |
| Node local HTTP preflight | **11 passed, zero failed/skipped**, including two nested schema-tamper checks. | Same clean commit. Real loopback socket, bounded query cancellation, exact schemas, complete text/structured parity, unsupported-method refusal and independent Python replay. [Preflight assertions][preflight]. |
| HOST-015 recovery and local-edition client guards | **6 passed, zero failed/skipped**. | Earlier run at 16:11:39 UTC, before the merge checkpoint. The relevant runtime, test and client sources are unchanged between `72bc5aaf66242db219cdde5e2754a1a5e635a532` and the clean commit above; this pass is reused, not presented as a second run. [Recovery][recovery]; [client guards][client-guards]. |
| Python preflight verifier | **24 passed**. | Run at 16:11:54 UTC after merge commit `0a046021c203c05abc029bd068e70186a3133a8f`; verifier and test sources are unchanged at the clean checkpoint. Includes hostile replay/input checks. [Verifier tests][verifier-tests]. |

The launcher also ran the existing independent SDK demonstration, which reported
`outcome: passed`, five distinct verified current-call receipts and three exact
negative cases. It made 15 MCP HTTP requests totalling 333,259 response bytes.
Its diagnostic timings were 10.372 seconds to start and 1.483 seconds for the
client journey. These are individual warm-environment observations, not latency
targets. The SDK report alone does not measure provider egress or process cleanup;
those checks belong to the separate guarded runtime and launcher tests above.

Two initial attempts were not acceptance passes. The first stopped before testing
when Corepack could not download pinned pnpm through the restricted socket. The
next reached 12 passing tests but failed because another task changed checkout
status during an assertion, and the extracted launcher had mode `0700` while its
test requires all executable bits. Restoring `0755` matched the tracked `100755`
launcher, with no content or Git executable-mode change. The final run above used
the pinned tools and a frozen clean checkout; no failed assertion was waived.

## The five tools, in ordinary language

| Tool | What the acceptance journey checks |
| --- | --- |
| `catalogue.search` | Finds the ONS Data API source in the verified catalogue. |
| `catalogue.describe` | Reads that source record, including its identity and context. |
| `selection.resolve` | Turns the supported question into an explicit bounded selection. A selection is not permission to call arbitrary data services. |
| `data.query` | Returns the single admitted England/week-24/2026 observation from the approved cache, labelled with its source and expiry. |
| `evidence.inspect` | Looks up the stored receipt and checks its link to the earlier query. It does not replay the original query result. |

The [SDK journey][sdk-journey] also verifies three resource classes:
`catalogue.public`, `catalogue.record` and `evidence.receipt`. Its result is
`10471` for the fixed `weekly-deaths-region` / `time-series` / version `121`
selection. This is a cached historical observation, not current live statistics.
The cache expires at `2027-02-20T20:21:08.947Z`; direct-API and MCP tests exercise
the instant before expiry, expiry itself and the instant after it. They require
query refusal at and after the cutoff while earlier session evidence remains
inspectable ([expiry tests][expiry]).

## Failure and evidence recovery

An idempotency key identifies one query attempt. If a response disappears after
its receipt has been stored, sending the same key again must not execute the
provider again. [HOST-015][recovery] injects that precise failure, opens new ledger
and reconciliation-index instances over the same test directories, and retries
with the provider suspended. It requires `409 idempotency_completed`, then uses
`evidence.inspect` with the original key to recover the query receipt. Exactly one
fixture provider execution and one ledger record/event remain. The raw key and
original observation are absent from the retained reconciliation data; recovery
returns evidence, not the original result.

This is a store-reopen, fault-injection test. The ordinary local launcher removes
its session stores at orderly shutdown; it does not promise receipts survive
stopping and restarting a normal local demonstration. Retain permitted results
before stopping if they are needed later ([shutdown check][shutdown]).

The SDK demonstration also checks `missing_dimension`, `invalid_request` and
`idempotency_completed` refusals. Separate [client tests][client-guards] reject
changed receipt/result/source bindings, incomplete plain text, other endpoints,
excessive response sizes and too many requests. The real-socket preflight
deliberately aborts a second query after its fixture provider starts. That distinct
key must remain pending without a completed receipt, resolution, record or ledger
event. An interrupted request is not silently labelled successful.

## Reproduce

Use a clean checkout and the pinned prerequisites in the
[LOCAL-212 quick start](../operations/LOCAL-212_CLEAN_CLONE_LOCAL_CANDIDATE.md).
Complete its locked dependency install first. From the repository root, these are
the commands and argument vectors used for the four check groups above, with the
temporary environment-specific command paths omitted:

```sh
pnpm run test:local-candidate
node --test --test-isolation=none --test-reporter=tap \
  apps/mcp-gateway/dist/test/qual-206-host-015.test.js \
  tests/test_local214_demo.mjs
node --test --test-reporter=tap \
  tests/interoperability/test_qual_206_local_http_preflight.mjs
uv run --locked --cache-dir .uv-cache python -m unittest \
  tests.interoperability.test_qual_206_local_http_preflight
```

The first command builds the governed catalogue, workspace dependencies and
gateway before running its maintained acceptance tests. Keep port 8787 free and
allow loopback sockets. Do not edit the checkout while the harness is running:
it checks that source state is unchanged, and its SDK demonstration requires
clean source. The in-process runner option affects only the focused recovery and
client tests. It does not replace the real-socket acceptance or child-process
lifecycle checks. In this sandbox, an earlier default isolated run reported only
two file-level passes; only the explicit six named test results are counted here.

For a manual repeat, run `./scripts/start-local-candidate` in one terminal and
`pnpm run demo:local-edition` in another. Inspect the reported source, cache warning
and five distinct verified receipts, then stop the launcher with Ctrl-C. These
commands make no model call and need no provider credential. The
[illustrated walkthrough](../demonstrations/LOCAL-214_LOCAL_EDITION_WALKTHROUGH.md)
explains this journey step by step.

## Limits and remaining release gates

The preflight's clean-source branch passed its independent verifier. Its source
material binding nevertheless remains explicitly incomplete for the whole loaded
runtime closure. The test removes its temporary capture and projection; this
document does not publish a new durable protected-main transport projection.
The [preflight runbook](../operations/QUAL-206_LOCAL_HTTP_TRANSPORT_PREFLIGHT.md)
defines the separate retained-evidence procedure and its exact limits.

Public HTTPS/TLS, cloud persistence and backup/restore, independent remote clients,
live-provider acceptance, native Sites identity, deployed artefact identity and
canonical release/tag acceptance remain separate gates. The six-tool Sites pilot
and captured-CPIH workbench are different profiles and are not covered by this
five-tool result. Full local-edition acceptance also retains its macOS,
fresh-source, unaided-colleague and publication gates; see the
[local-edition acceptance policy](../operations/LOCAL-214_ACCEPTANCE.md).

[source]: https://github.com/chris-page-gov/gis-ai-go/commit/0eae2d0f9262dc119f9313a6c45ef3ee18666e6a
[command]: https://github.com/chris-page-gov/gis-ai-go/blob/0eae2d0f9262dc119f9313a6c45ef3ee18666e6a/apps/mcp-gateway/package.json#L14-L16
[runtime-client]: https://github.com/chris-page-gov/gis-ai-go/blob/0eae2d0f9262dc119f9313a6c45ef3ee18666e6a/apps/mcp-gateway/test/local-candidate-acceptance.test.ts#L344-L615
[launcher]: https://github.com/chris-page-gov/gis-ai-go/blob/0eae2d0f9262dc119f9313a6c45ef3ee18666e6a/apps/mcp-gateway/test/local-candidate-launcher.acceptance.ts#L168-L267
[preflight]: https://github.com/chris-page-gov/gis-ai-go/blob/0eae2d0f9262dc119f9313a6c45ef3ee18666e6a/tests/interoperability/test_qual_206_local_http_preflight.mjs#L139-L315
[recovery]: https://github.com/chris-page-gov/gis-ai-go/blob/0eae2d0f9262dc119f9313a6c45ef3ee18666e6a/apps/mcp-gateway/test/qual-206-host-015.test.ts#L149-L267
[client-guards]: https://github.com/chris-page-gov/gis-ai-go/blob/0eae2d0f9262dc119f9313a6c45ef3ee18666e6a/tests/test_local214_demo.mjs#L24-L77
[verifier-tests]: https://github.com/chris-page-gov/gis-ai-go/blob/0eae2d0f9262dc119f9313a6c45ef3ee18666e6a/tests/interoperability/test_qual_206_local_http_preflight.py#L21-L43
[sdk-journey]: https://github.com/chris-page-gov/gis-ai-go/blob/0eae2d0f9262dc119f9313a6c45ef3ee18666e6a/scripts/local214_demo.mjs#L117-L195
[expiry]: https://github.com/chris-page-gov/gis-ai-go/blob/0eae2d0f9262dc119f9313a6c45ef3ee18666e6a/apps/mcp-gateway/test/local-candidate-main.test.ts#L266-L399
[shutdown]: https://github.com/chris-page-gov/gis-ai-go/blob/0eae2d0f9262dc119f9313a6c45ef3ee18666e6a/apps/mcp-gateway/test/local-candidate-acceptance.test.ts#L617-L669
