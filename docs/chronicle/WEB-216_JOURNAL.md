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

## Preservation scope

The most recent independently checked continuous checkpoint at inception completed
on 14 September 2026 at 07:02:11: 3,361 journal events and 3,293 objects, with zero
expiry warnings. Its preceding capture had two declared exclusions and four
unavailable sources. Those limits remain; “verified” is not “everything recovered”.

The new milestone capture was started after PR #127's protected-main checks passed.
It includes explicit WEB-216 GitHub discussions and
available run logs, permitted user-visible root and transitive-agent projections,
and selected public experiment artefacts. A new `commit-complete` capture and
complete offline verification are required before claiming it is preserved. The
existing verified checkpoint is not changed. Public material contains no private
store paths, raw sessions, identity credentials or granular private cost records.
