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

## Preservation scope

The most recent independently checked continuous checkpoint at inception completed
on 14 September 2026 at 07:02:11: 3,361 journal events and 3,293 objects, with zero
expiry warnings. Its preceding capture had two declared exclusions and four
unavailable sources. Those limits remain; “verified” is not “everything recovered”.

The new milestone capture will include explicit WEB-216 GitHub discussions and
available run logs, permitted user-visible root and transitive-agent projections,
and selected public experiment artefacts. A new `commit-complete` capture and
complete offline verification are required before claiming it is preserved. The
existing verified checkpoint is not changed. Public material contains no private
store paths, raw sessions, identity credentials or granular private cost records.
