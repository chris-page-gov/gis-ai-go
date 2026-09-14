# WEB-216 development journal

This is a source-time supplement to [How we built GIS AI GO](README.md), not a
rewrite of Volume 1's fixed product baseline. All times below are UTC. It records
permitted operational summaries, provenance and outcomes, not hidden model
reasoning. Detailed private capture remains local under
[EVID-211](../operations/EVID-211_CONTINUOUS_EVIDENCE_PRESERVATION.md).

## 14 September 2026: inception and experiment design

- Owner authority: continue implementation until blocked, merge verified increments
  and preserve evidence for the continuing chronicle. Source repositories,
  especially the competition entry, remain read-only.
- Source reconciliation: the accepted source commits and proposed staff stories
  are recorded in [the crosswalk](../implementation/WEB-216_SOURCE_AND_STORY_CROSSWALK.md).
  One existing agent reviewed the inception independently; two existing agents
  investigated the metadata import and private preservation procedure. These are
  delegated assignments created by the main model, not newly commissioned people.
  Reusing the existing agents also avoids adding preservation topology mid-capture.
- 14:59:04: inception commit `e9a2ed029fc73e12b4875132389f7cf6367d5c3d`.
  [Issue #125](https://github.com/chris-page-gov/gis-ai-go/issues/125) opened at
  15:00:43; [PR #126](https://github.com/chris-page-gov/gis-ai-go/pull/126) opened at
  15:08:47. The four-document independent review found no actionable defect.
- Local inception checks: 765 links, 183 research hashes, two ledger snapshots,
  71 source identifiers, 86 changelog fragments and 1,001 secret-scanned text files
  passed. No runtime build or provider call was needed for that documentation diff.
- 15:17:51: PR #126 squash-merged as
  `87c5997eecc6b6ddf4487cc226d3905544f5595f`. Required PR assurance and CodeQL
  passed; protected-main verification is a separate checkpoint, not inferred
  from the PR result.
- Protected-main [CI run 34861232967](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34861232967)
  subsequently passed, including independent image derivation, attestation and
  provenance. [CodeQL run 34861232580](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34861232580)
  passed for that same merge commit.
- Experiment design: prefer seven pinned rich records for clone-local tests and
  339 precisely scoped records for the first comparison. Do not run the dirty
  upstream build. Preserve exact raw records and separately hash derivative scope.
- A leakage risk was found before benchmarking: upstream search can index
  evaluation aliases. This experiment excludes those and gold-answer material
  from ranking; labels enter only the scorer. Public development questions remain
  explicitly non-independent, even after removing that mechanical leakage.
- The [experiment protocol](../implementation/WEB-216_EXPERIMENTS.md) was written
  before the new benchmark was run. JSON transfer counts are modelled bytes,
  not measured browser performance. Provider requests are zero for the offline
  experiments; task-wide agent usage/cost is not yet measured.
- Independent implementation review found a real refresh defect before publication:
  changing the concept vocabulary could reuse stale edges even when source records
  were unchanged. Reuse now binds both version labels and the vocabulary mapping
  digest; regressions cover each change. The first 25 integrated tests passed.
- A local assurance attempt caught an incorrectly formatted changelog fragment.
  It was corrected to the repository's single-bullet format; this was an authoring
  error, not a runtime failure. Passing unchanged checks are not rerun merely to
  consume CI wait time.
- Final importer review found that checking only the supplied source directory
  was insufficient: Git accepts a repository subdirectory. Output checks now
  protect the actual worktree, Git directory and common Git directory, including
  resolved symlink destinations. No protected source was written. The integrated
  set now passes 32 tests, including the new regression and related worktree cases.

## 14 September 2026, 15:28:13–15:28:14: first recorded experiment

The import and experiment ran from clean commit
`f515814848c904982cc8964327da9f64eb862585`, both exiting successfully.
The [original result](data/web216-offline-experiment-20260914.json) and
[path-redacted source-time manifest](data/web216-offline-source-time-20260914.json)
retain exact source/configuration hashes, environment, timings, ranks and outcomes.
The full local manifest additionally retains the actual operator command paths.
The result-file SHA-256 is
`c0b2a955730551fcb5cd9e0e14bc7bf4d47c3095a349141ee66e3d44f5041ee9`.

| Layout | Records | Initial canonical JSON bytes | Median local build, five repeats |
| --- | --- | --- | --- |
| Story subset | 7 | 18,926 | 0.378 ms |
| Rich comparison | 339 | 744,770 | 14.996 ms |
| Comparison with lazy details | 339 | 239,298 | 15.734 ms |

The lazy layout uses 67.9% fewer initial uncompressed JSON bytes than the rich
comparison; exact details add 1,579–6,019 bytes for the top-ranked record in these
cases. This is a byte model, not measured browser transfer, compressed size or a
claim that lazy loading speeds up local index building. Full and lazy rankings
are identical because their searchable projections are identical.

In the wider corpus, the expected CPIH, population and weekly-deaths records ranked
first with either mode. The expected rooms record ranked seventh with keywords
and third with author-supplied concept hints. The small subset ranked all three
in-subset positive cases first but cannot return the weekly-deaths target because
it is absent. The no-match lexical control returned no candidates in either mode.

The synthetic add/change/delete schedule reused 337 of 339 projections and produced
the same complete logical hash as rebuilding from scratch, with the deleted
identity absent from records, keyword postings and concept edges. Version and
vocabulary-change invalidation are separately covered by regression tests.

**Decision:** carry the compact summary plus exact lazy-detail design into the
next prototype, retain the rich reference and small portable fixtures, and keep
concept hints explicit. Do not add a vector database or assert an optimal design
on these five developer-visible cases. Rooms remains third even with hints:
show alternatives and source caveats instead of automatically selecting the top
result. Real user selection and independent relevance evaluation remain necessary.

The two subprocesses took 0.461 seconds combined, including import and interpreter
startup; the measured experiment body took 0.219 seconds. No provider or model
requests occurred inside the experiment. Task-wide Codex effort and cost are not
measured by this number and must not be reported as zero.

## 14 September 2026: maintained CPIH retrieval and corrective review

- 15:30:57: [PR #127](https://github.com/chris-page-gov/gis-ai-go/pull/127)
  opened from `a30d2fdb1359ec67386da9de206b2507761320ba`; it merged at 15:41:15
  as `52c46d9cd619d5c349472c250d2d03aebb3beb3c`. Required PR checks passed.
  Exact protected-main [CI](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34863798079),
  including independent derivation, attestation and both provenance lanes, and
  [CodeQL](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34863799028)
  subsequently passed.
- Primary-source inspection found that `cpih01` version 67 ends in January 2026
  and is no longer updated. Frozen OKF metadata was preserved unchanged, with a
  separately dated lifecycle notice. Discovery ranking alone cannot establish
  currency or execution support.
- The main model checked the official migration guide and maintained L522/MM23
  series page before making two bounded GET requests. At 15:42:57.497076–
  15:42:57.906633 both returned HTTP 200, retaining 3,070 and 125,682 bytes.
  The original source-time outcome remains “raw responses collected, schema
  validation pending”; later validation is a separate derived result.
- An existing child agent implemented the pure validator and a two-month public
  projection. A second existing child reviewed it independently. That review
  found that retrieval-time bounds alone admitted rows newer than the declared
  release, and optional headline metadata could conceal a truncated latest row.
  Both now fail closed. Source identity now binds the validator and its imported
  corpus helper. The final 21 focused tests passed, then the main model ran the
  corrected validator on both requested periods using the original full capture.
- The [validated summary](data/web216-current-cpih-20260914.json) records 463
  monthly rows covering January 1988–July 2026. July is `142.7` and January 2026
  is `139.4`: index values with base 2015=100, not inflation percentages. The
  source release timestamp is retained alongside its London date, 19 August 2026.
  This dated observation does not promise perpetual freshness.
- An earlier historical CMD probe draft passed eighteen mocked tests but was
  rejected by the main model before integration: its assumed observation shape
  differed from the official example. Its visible source and tests are preserved
  outside Git as rejected evidence. No historical endpoint request was made.
  The maintained route supplies both months, so the redundant eight/nine-request
  route was not pursued. Passing mocks did not justify shipping it.
- The source-time result distinguishes two provider requests from zero model
  calls inside the probe. It is not an MCP-client success or gateway receipt.
  Task-wide Codex effort and cost remain unknown here, not zero. See the
  [full protocol and limitations](../implementation/WEB-216_ONS_RETRIEVAL_EXPERIMENT.md).
- Local documentation assurance caught a second fragment-authoring mistake: the
  new filename omitted its required `.added` category. This was corrected using
  the existing checker contract before commit. It did not require rerunning the
  provider observation or unchanged parser tests.

## 14 September 2026: spatial boundaries and local storage

- 16:09:55: [PR #128](https://github.com/chris-page-gov/gis-ai-go/pull/128)
  merged as `4c8e6144dfb02ea5d9dcf4cb34fbe34f36529f3e`, after its exact-head
  repository assurance, image assurance and CodeQL passed. The following
  protected-main checks remain a separate acceptance step.
- The main model assigned two existing agents separate geography-contract and
  storage-comparison modules, then reused the independent reviewer. No additional
  agent was spawned, no Site file was delegated and no provider call was required
  for these synthetic/local tests.
- X04 review reproduced a geometry defect: fractional inputs could round to an
  apparent boundary under the default Decimal precision. The deliberately
  synthetic geometry model now admits bounded integers and uses exact integer
  predicates, including ray comparisons. The fixture is unchanged; fifteen
  tests cover edge/overlap/outside, identity/vintage/category errors and the
  precision/backtracking regressions. This is not a general-purpose GIS engine
  or a verified join of actual OS/ONS payloads.
- X05 review found an unbounded initial corpus read and source hashes taken only
  at the end. Reads are now byte-bounded before parsing, and authored source hashes
  are checked before/after the experiment. A changed source or partial-write failure
  keeps incomplete evidence but produces no success result. Nine focused tests pass.
- The actual X05 run at 16:09:08.553850–16:09:08.744957 used source checkpoint
  `7ef61bebb52a4c8e0f4cb3caea097d3cc3796d60`, before rebasing its unchanged source
  onto accepted PR #128. The [public result summary](data/web216-storage-experiment-20260914.json)
  retains the original full-result hash, code/configuration/input identities and
  metric definitions. The complete result, detailed samples and file inventories
  remain in the source-time experiment directory; this publication is a projection,
  not the byte-identical full result.

| Local layout | Persisted file bytes | Median fresh-reader detail lookup | Median immediate repeat |
| --- | --- | --- | --- |
| Static JSON | 744,770 | 2.662 ms | 0.00146 ms |
| SQLite | 1,638,400 | 0.0949 ms | 0.0206 ms |
| Digest-prefix JSON partitions | 754,476 | 0.204 ms | 0.00204 ms |

All three reconstructed the same 339 records and the same full ranked identifier
lists for the five development cases. Each lookup summary contains fifteen
samples: five identifiers across three repetitions. Initial partition-manifest
read was 1,576 bytes; that is not the cost of loading searchable summaries or
answering a query. SQLite's initial/page I/O is unmeasured, not zero. Operating
system caches were uncontrolled; “fresh reader” does not mean a cold disk.

**Provisional decision:** retain the compact searchable summaries and lazy exact
details selected by X01. SQLite is a viable later server-side identifier store,
but its faster local fresh-reader lookup does not justify adding hosted database
complexity for this corpus. The partition arm tests access mechanics, not a complete
search-serving replacement. No D1, Parquet, object-store, multi-user or hosting
performance was measured. The experiment body took 0.191 seconds, with zero
provider/model/Sites requests; that is not total development effort or cost.

See the [protocol and geographic source limits](../implementation/WEB-216_GEOGRAPHY_AND_STORAGE_EXPERIMENTS.md).

### PR #129 assurance correction

The first repository-assurance run, [34867314043](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34867314043),
failed on 14 September at 16:18:24 UTC in an existing collector privacy assertion:
`raw value leaked: 10471`. The preceding independent schema and replay checks had
passed. The assertion searched the complete serialised log, including hashes,
random identifiers and measured timings, for the observation's digits. The
ephemeral failing capture had already been removed by test cleanup, so its exact
matching field is unknown; a deterministic synthetic digest reproduces the
incidental-substring failure but is not claimed to be that CI value.

The main model assigned one reused agent the diagnostic and test-only correction.
The assertion now uses the closed event schema to distinguish declared numeric
measurements and validated identity fields from semantic payloads. Regression
cases retain rejection of string/numeric observations, raw keys, nested errors,
JSON-escaped content, malformed identities and unexpected fields. Runtime logging
and independent replay validation are unchanged. The affected Python wrapper ran
all nine Node collector tests successfully in 1.942 seconds. The first sandboxed
attempt stopped at the existing macOS process-inspection restriction; its bounded
local-permission rerun passed. Local validation used the working tree, including
uncommitted later component builds, not an isolated PR #129 runtime; canonical CI
must independently establish the exact corrected PR outcome.

## Preservation scope

The most recent independently checked continuous checkpoint at inception completed
on 14 September 2026 at 07:02:11: 3,361 journal events and 3,293 objects, with zero
expiry warnings. Its preceding capture had two declared exclusions and four
unavailable sources. Those limits remain; “verified” is not “everything recovered”.

The new milestone capture was started after PR #127's protected-main checks passed.
It selected explicit WEB-216 GitHub discussions, available run logs, permitted
user-visible root and transitive-agent projections, and public experiment artefacts.
It failed after 34.56 minutes because the final selected source-path inventory
differed from the initial one. The comparison covers resolved paths, not ordinary
append growth. The permitted diagnostic evidence does not identify which file
appeared, disappeared or moved; agent-count changes must not be inferred.

The selected closure contained 1,052 source files. It reused 1,040 projections and
regenerated twelve, but **no new Codex generation was committed**. GitHub and local
artefacts are committed separately before the closure stage, so some may already
have entered the store. The earlier successful verification cannot be extended to
this later store state without another complete verifier run.

Recovery separates source-only capture from the changing conversation closure.
The full thread-path guard is retained; its retry needs a quiet window. Source-only
capture does not claim conversation completeness. Failure sidecars and source-time
originals remain retained. Public material contains no private store paths, raw
sessions, identity credentials or granular private cost records.

## Inactive CPIH application and independent review

The main model composed a closed two-period selection and application, then reused
two agents for separate ledger and reconciliation implementations and independent
review. The evidence family remains distinct from the existing weekly-deaths
operation; the older application and policy reject genuine CPIH records rather
than treating missing legacy authority fields as permission.

Review found two application issues before activation: closed options did not
reject symbol/non-enumerable properties, and an exhausted ledger could still
appear ready and consume a claim it could not complete. Both were corrected.
Headroom now comes from the ledger's actual verified event limit; a new key checks
it before claim acquisition, while completed retries and inspection still work.
Regression tests reproduce the one-event capacity failure without filling a real
store. Two initial application-test fixtures also needed authoring corrections:
the internal helper must reference the compiled dependency, and changing a key's
digest must not alter its fixed namespace prefix.

The complete evidence package passed 122 tests in 13.877 seconds. The application
and selection slice passed fourteen tests in 0.861 seconds, covering both months,
restart, replay/conflict, pending publication, corruption, cancelled admission,
closed options and full-store behaviour. These are local component results, not an
MCP/provider execution observation. See the
[contract explanation](../implementation/WEB-216_CPIH_CONTRACTS.md) for the next
wire, browser and activation gates.

All 27 selected existing readiness, governed-assembly and inspection regressions
also passed: 25 in the sandbox and two real-loopback cases after a permission-only
rerun of those cases. The initial two failures were `listen EPERM`, not failed
assertions. Contract validation checked 100 existing schemas and 153 records;
link, changelog and baseline secret/path checks also passed. The new finite result
core export supports later static wire schemas; exporting those public constants
does not establish execution.

## PR #130 source-bound receipt refresh

Repository assurance on the initial PR #130 head found a stale deterministic
QUAL-206 receipt set. Six changed source-material files altered suite identities;
the selected scenario outcomes did not fail. The set was regenerated in a
detached checkout of `1f4b05178544d2cb2f8a82f7a9b9956bf60bddc8`, isolated from
later MCP transport work. Seventeen suites and 87 selected tests passed, as did
six receipt-contract tests and a repeat byte-identical check. Six suite IDs, four
case receipt IDs and the set ID changed; outcomes, limits and test selection did
not. Canonical CI on the corrected PR head remains the acceptance gate.

The next canonical run exposed a second stale binding in the historical-evidence
compiler: its exact compiled `digest.js` and `index.js` hashes predated the
additive v3 domain and export. Those two pins were refreshed from clean
`4e6a842e2793efde5f6a58807274ce2368e40cf6`; canonicalisation and the fixed
historical identity vector were unchanged. A regenerable local receipt set was
also separated from genuinely immutable historical observations, while retaining
an exact reviewed baseline. Thirty-two targeted tests passed, including rejection
of drift in every pinned runtime before child execution. No historical observed
artefact, scenario outcome or release boundary was rewritten. These sequential
failures document cross-suite source-binding maintenance costs, not failed Claude
observations or a reason to remove the bindings.

## Accepted component checkpoints and local browser journey

PR #129 was squash-merged at `2026-09-14T16:50:54Z` as
`806fdcc5b39cee75c6a9144ffa18cc92a66bfc2a`. Protected-main CI
[34871132679](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34871132679)
and CodeQL [34871132304](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34871132304)
completed successfully. PR #130 was squash-merged at `2026-09-14T17:28:47Z` as
`f4b1a90d64b4aea4c6be3f4b08bcbee1cdfe68ec`; complete CI
[34874999240](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34874999240)
and CodeQL [34874999775](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34874999775)
passed, including independent image derivation and attestation verification.

The next increment adds a separately named local workbench on port 8788, leaving
the supported candidate's port 8787, default inactive operations, Site `/demo` and
release boundaries unchanged. One reused agent implemented the closed three-tool
MCP transport, bounded listener and retained state launcher. The main model built
the seven-record browser projection, accessible manual controls and four page tools.
A second reused agent independently reviewed the runtime; another reviewed the
browser controller and assurance integration. These are bounded assignments,
not hundreds of concurrent agents or human-authored agent definitions.

Review found and corrected four browser issues: delayed selection could restore
an old month; returned periods and inspection receipt IDs were not bound tightly
enough; inherited object properties could reach the search postings lookup; and a
failed page-tool search could leave stale result cards. Thirteen focused controller
tests passed after correction. Browser values are never taken from the metadata
projection or invented by the front end.

Real-loopback and retained-state tests covered the three MCP tools, wire schemas,
Host/Origin admission, bounded assets and request bodies, corrupt-state readiness,
duplicate requests and restart. The production Vite build exposed a separate
integration error before publication: its `./assets/…` references were stricter
than the listener's accepted spelling. The listener now normalises only the two
approved root/relative asset forms while rejecting traversal, query, fragment,
external and bare paths. Both real built assets returned exact bytes. A shared
request-clone overflow cancellation hang was also fixed, with an existing
catalogue-path regression; no input limit was relaxed.

The root model exercised all four real page tools in the in-app browser: metadata
search, July selection, retrieval of `142.7` and inspection of the same persisted
record. Exact JSON serialisation matched between retrieval and inspection, and
again after graceful server restart. The manual in-app path returned January
`139.4`. Chrome `153.0.8010.36` returned July `142.7`; Edge `153.0.4234.32` returned
and inspected July. Installed versions were read from application metadata. Both
external-browser connections lacked a callable WebMCP capability, despite the
page reporting four registrations. No Gemini or Copilot success is inferred.

Four invalid real page-tool calls were rejected: too many normalised terms,
unsupported month, unissued plan ID and missing receipt ID. The old matches were
cleared after the invalid search. No external provider or model API request was
introduced by these local tools. The conversation's own model usage is not zero;
an attributable currency total is not available from this observation.

The private source-time record retains original viewport screenshots and the
actual page-tool outputs. A malformed full-page stitched screenshot was retained
but excluded from the public illustrations. Narrow/desktop checks found no
horizontal document overflow at effective CSS widths 325/1,200; these are not
full accessibility or user-research certification. The first graceful-stop
command hit the sandbox permission boundary; an attempted second launcher failed
closed on the occupied port. A narrowly authorised stop then succeeded, followed
by the successful retained-receipt restart check. No unrelated process was stopped.

The browser observations used an explicitly unattested working-tree build based
on `1f9fc53f91578ec1d86bbe01841869c41c393a31`, not the later exact accepted source.
Lifecycle output distinguished checkout HEAD from runtime/static attestation.
The final production front-end build passed. Independent review found its build
missing from the canonical browser-build chain; the new package was added without
removing either existing build. Typechecking and unit-test routing were already
present. Canonical PR and protected-main acceptance remain required.

The [illustrated local walkthrough](../implementation/WEB-216_LOCAL_WORKBENCH_WALKTHROUGH.md)
and [OS/ONS observation record](../implementation/WEB-216_OS_ONS_SOURCE_OBSERVATIONS.md)
separate the now-observed local path from unfinished real geography and hosted
persistence. Read-only source inspection found no accessible, provenance-complete
MSOA polygon payload. The unavailable external cache and postcode best-fit
lookups cannot be substituted for the missing point-in-polygon evidence.

PR #131's first CodeQL gate flagged a substring assertion in a negative test as
incomplete URL sanitisation. The line was checking that a rejected caller URL was
not echoed; it did not authorise an outbound request. The test was strengthened
to compare the entire MCP error envelope, including closed fields and validated
server-generated identifiers, instead of dismissing the alert or loosening runtime
admission. A same-pattern search found no sibling host-substring assertion in the
new app or gateway tests. The deterministic receipt refresh preceding this gate
took 21.76 seconds across generation, repeat check and 32 contract tests; no
historical observed-host evidence or compiler runtime pin changed.

The next canonical repository check found 16 failures in three integration
contracts: 14 newly introduced workbench paths lacked explicit shadow routing;
the workspace-version inventory omitted the new app; and the historical protocol
matrix still required the changed MCP HTTP source to match its original bytes.
The deterministic seven-receipt check itself passed. A reused assurance agent
diagnosed and corrected the routing/inventory omissions and added a separately
pinned, explicitly non-attesting current-source compatibility record. The original
v1 matrix, original Git-blob assertions and deterministic receipts remain unchanged.
Sibling-path, version-drift and compatibility-tampering regressions were added;
71 affected tests passed in 2.572 seconds. The root reviewed the exact changes
before submission. These are integration omissions, not evidence that the
successful browser observations occurred on an accepted protected-main build.

The owner then supplied screenshots comparing the in-app browser with a separate
Chrome ChatGPT-extension session. The latter could read the page but reported no
WebMCP capability, even after a duplicated tab resolved an ownership conflict.
A fresh Edge connection likewise exposed only `pageAssets` and `cdp`; its manual
selection call succeeded. The requested repeat retrieval was not executed after
the approval layer refused its durable-write side effect in the side-check scope.
Earlier successful Edge retrieval/inspection remains separately recorded above.
The owner's Gemini screenshot reports no tool-definition or execution access.
This is recorded as an owner-observed client limitation, not a universal claim
about Gemini or an inferred tool execution. No browser settings were changed.
