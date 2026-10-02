# OKF-220: independent producer assurance review

Reviewed: 2 October 2026. Scope: the new metadata model, bounded capture,
frozen-source importer, bundle producer and local retrieval integration.

This review examines the working implementation against base revision
`357aa6c85c787f29710ff208c938eb54af02a488`. It is a bounded independent review,
not a claim of repository-wide security certification, current upstream
statistical accuracy, publication or installed Ask OKF acceptance. No provider
request, browser automation, deployment or external repository edit was made
for these checks.

## Review method and evidence

The reviewer inspected `scripts/okf_plus/model.py`, `harvest.py`,
`import_sources.py`, `freeze_locators.py` and `build.py`; used synthetic local
fixtures to reproduce the source-binding, date and path boundaries; and added
`tests/contract/test_okf_plus_build.py`. All request tests use a mocked opener.
The relocated-build check generates the same fixture in two unrelated
temporary directories and compares every output byte and output checksum.

The source cache and capture ledger were read only. At that observation the
ledger held 750 top-level request attempts and no entry whose final URL
differed from its requested URL. This establishes no observed redirect in that
snapshot; the redirect-accounting finding below concerns latent behaviour,
not an allegation of unrecorded calls. Later authorised captures have their
own ledger entries and are not covered by that historical count.

## Findings and remediation

| Finding | Consequence | Remediation and acceptance evidence |
| --- | --- | --- |
| Capture followed redirects without separately admitting each wire request. A socket timeout was described more strongly than its actual bound. | A redirect could bypass the request-count interpretation; a slowly delivered response could outlast the socket timeout. | Redirects now fail closed. The synchronous POSIX capture wraps the complete opener/body operation in a 30-second wall deadline. Offline tests exercise redirect rejection, deadline interruption, handler restoration and refusal to replace an existing alarm. This capture runner requires a POSIX main thread. |
| Import derived original locators from ignored raw captures and otherwise fell back to a catalogue receipt. | Re-import in a clean clone could silently change the provenance of records from later pages or attach an unrelated successful response to a failed request. | The explicit freeze stage verifies raw hashes, byte counts and native JSON pointers or reviewed whole-document identity before creating the public locator index. Explicit document evidence must match the receipt URL, retrieval time and hash. No unrelated receipt fallback remains. Failed requests and browser observations use separate evidence kinds without successful-response claims. Offline re-import requires only the frozen public index. |
| A response digest was checked independently of the cited URL/time and source identity. | A changed URL, retrieval timestamp, native ID or source family could retain an apparently valid provenance binding. | The builder now checks the exact receipt tuple, native identity/family, normalised source record hash and frozen locator fields. Synthetic mutations are rejected. |
| Reference validation accepted encoded credential parameter names, invalid ports, control characters or spaces. | Unsafe reference strings could enter provenance or generated navigation. | Shared reference validation rejects these cases. Closed capture routes still separately prohibit features and observations. Opaque native details remain inert source metadata and are not dereferenced by the producer. |
| Typed dates were emitted without verifying the calendar value. | An impossible date could be labelled `xsd:date`. | Date and date-time lexical values are now parsed, with time zones required for date-times. Reversed extents and mixed date/date-time precision are rejected. Native period codes retain their explicit precision instead of being labelled calendar dates. |
| Normalised source paths were checked lexically but could be symbolic links outside the checkout. | A source lock could depend on unrecorded external file contents. | Source and locator paths now require containment and reject symbolic links, including parent-directory links. The synthetic source-link escape regression passes. |
| Documentation routes accepted dot segments and encoded separators. | The closed route interpretation could differ from the provider or intermediary's normalised path. | Literal and encoded traversal are rejected before the opener is called; all three original regression cases pass. |
| A rebuild deleted the previous marked bundle before validation. | Invalid new inputs could remove the last generated result. | Builds now validate in a staging directory, then install the result. A regression checks that every previous bundle byte survives a rejected rebuild and that temporary staging is removed. Locator freezing similarly preserves the previous public index on failure. |

The three boundary groups that failed at the initial regression checkpoint
(reverse-order temporal extent, normalised-source symlink containment and
noncanonical documentation paths) now pass. The later locator review also
identified one HTTP 500 Nomis request; it now remains failed-request evidence
rather than inheriting an unrelated successful capture. HTTP 200 responses
with invalid source contracts retain that separate contract status.

## Metadata and evidence boundaries

- Source-native period-code extrema, dataset reference periods, release dates,
  metadata modification, geographic vintage and publication cadence are
  separate claims. Nomis `FREQ` is not evidence of release cadence. Missing
  source values remain explicitly unknown.
- Generated records use a structured `generated` field and an explicit draft
  lifecycle. A producer run does not create a human verification event. The
  OKF core version is a root declaration.
- Catalogue counts have source-specific grains. A retained record, a
  successful version-metadata response and a complete statistical product are
  different denominators. Failed acquisition evidence must survive alongside
  partial coverage; raw record count alone does not establish completeness.
- Normalised source and receipt checks bind retained metadata to the recorded
  capture evidence. They do not independently replay an omitted private raw
  response or certify every upstream statement. Raw provider observations and
  protected NGD feature values are outside this public metadata build.
- The bundle's `globalCompleteness` remains `not-established`. Search returns
  discovery evidence with explicit candidate and byte omissions. Neither
  structural validation nor lexical ranking establishes answer sufficiency.
- The GIS extension profile remains a candidate until its own semantic and
  consumer checks pass. The installed Ask OKF connector still needs separate
  source/engine admission. A context projection is not a deployed connector.

## Secret-scan classification

The earlier token-like match in an official OS documentation identifier came
from the suffix of an ordinary word in a public slug. It was not a supplied
credential. The revised pattern requires a token boundary; synthetic bare,
quoted, bearer and project-token examples remain detected in
`tests/contract/test_secret_token_boundary.py`. No actual token value is
included in this report or its fixtures.

A literal blocked-query regex in capture code also resembled an assigned
secret to the conservative scanner. Splitting those constant fragments avoids
the false positive without weakening credential rejection. The targeted scan
over OKF+ source records, producer scripts and the new build tests returned
zero findings after those changes. The full canonical secret scan remains a
separate integration check.

## Unattended operation

The owner reported an overnight browser/CDP permission wait. That is an
operational precondition failure, not evidence of a provider or metadata
failure. No browser or CDP tools are used for the remainder of this work.
Before a future unattended run, check whether each planned interface is
available without an interactive approval. When it is not, record the exact
UI-only gap and continue independent authorised source/build checks. Do not
repeat permission prompts or represent a waiting process as active progress.

The capture lane is keyless, serial, request-count and byte bounded, with no
automatic retry and an explicit stop on provider rate limiting. The existing
included-allowance boundary remains unchanged. These controls do not establish
an account's commercial entitlement; metadata discovery does not admit live
feature execution.

## Acceptance record

The focused command is:

```sh
uv run --locked --cache-dir .uv-cache python -m unittest \
  tests.contract.test_okf_plus_build \
  tests.contract.test_okf_plus_model \
  tests.contract.test_okf_plus_search \
  tests.contract.test_secret_token_boundary
```

The focused suite passes 61 tests: 30 build/capture/locator checks, six model
checks, 23 retrieval checks and two secret-pattern boundary checks. A read-only
locator dry run verified all captured bindings across the 14 source families
present at that checkpoint; it did not replace the production locator index
while enrichment was running. The rebuilt full-catalogue retrieval result
remains pending the final source enrichment. Context
projection must use vendored, digest-pinned contracts for clean-clone CI;
requiring a sibling checkout would not be a portable acceptance result.
Mandatory canonical GIS CI remains the final integration gate. This review
does not relax publication, exact-commit runtime or live-client acceptance.

## Deterministic hand-off

`scripts/okf_plus/export.py` packages only the declared public source roots,
metadata producer, pinned dependency manifests, applicable tests and OKF-220
documents. The minimal execution-service project metadata is included because
the root Python lock declares it as a workspace member; the service code and
other repository components are excluded. Private captures never enter the
archive.

The optional generated pack requires a successful final offline verification
report. Export checks its seven artefact references, exact bundle/search
bytes, bundle checksums, current source-lock inputs and every declared context
output. The source revision label accompanies the actual input digest; it
does not turn an uncommitted working tree into accepted main. Four semantic
review questions remain unassessed.

Every payload file has a relative path, byte count and SHA-256 hash in the
manifest. Tar member ownership, permissions and timestamps, gzip timestamp and
file ordering are fixed. The adjacent receipt binds the archive and embedded
manifest; the manifest excludes its own hash to avoid self-reference.
Archive verification reads without extraction and rejects links, unsafe or
duplicate paths, changed checksums and byte/count-limit violations. Export
scans plain text and decoded context shards for the repository's secret and
machine-path patterns. These controls support a public metadata hand-off,
not a new upstream licence claim.

Nine offline export tests pass, including byte-identical archives from
relocated source trees, private-cache exclusion, source and archive tampering,
stale verification, unsafe links/paths, size limits and fail-safe preservation
of an existing export. The actual generated hand-off awaits final build and
verification; no unverified generated pack is silently substituted.

The owner also authorised a separate private hand-off of original
specifications and guides. `scripts/okf_plus/export_documents.py` admits only
captured official OS Markdown/navigation documents and exact reviewed official
ONS specification pins. It checks original hashes, byte counts, source URLs,
redirect evidence and credential patterns; literal public key placeholders
have a narrow reviewed hash exception. Unrelated catalogue, statistical,
feature, contact/account response payloads remain excluded. Its archive,
manifest and receipt have owner-only file permissions and an explicit
no-publication label. Seven further offline tests cover this separate lane.
Run it after the public export; a subsequent public export rebuild replaces
its output directory, so the private archive must then be regenerated from
the retained original evidence.

The refreshed [reuse review](OKF-220_REUSE_REVIEW.md) separates the accepted ONS
publication contract from the new immutable semantic candidate being merged
by the owner. The source repositories were inspected read-only; no working-tree
compiler bytes were copied into this implementation.

## Final production-path review

A further bounded review on 2 October inspected the no-argument
`pnpm run check:okf-plus` dispatch, the complete input lock, the generated export
chain and canonical CI upload paths. It used only local source and synthetic
fixtures. It did not repeat provider capture, the full corpus run or packaging.

Two actionable gaps were reproduced and repaired:

| Finding | Repair and regression evidence |
| --- | --- |
| Export checked every previous lock entry but did not detect newly added build inputs. A synthetic record added after verification entered an archive labelled `verified-automated-checks`. | Build and export now share `build.source_inputs`, and export requires exact ordered inventory and hash equality with the verified lock. Regressions reject added records, snapshots, schemas and producer scripts while preserving the previous archive. |
| Canonical CI uploaded all `artifacts/`, including diagnostics labelled local-only and any retained original-document files. | The upload explicitly excludes OKF+ captures, specifications, probe directories, raw/private material, private diagnostics and private original-document exports. A regression checks representative private paths are excluded and public assurance outputs remain admitted. The full canonical assurance command remains unchanged. |

The no-argument dispatch was exercised with the long-running verification
function substituted: it resolved the canonical output directory, a full current
Git revision and a UTC timestamp. That check proves argument/default wiring,
not a completed production verification. The source archive's documented
explicit `--revision` remains necessary outside a Git checkout. The pinned
Explorer schemas and engine are vendored; no sibling repository is required.
CI already provisions the pinned Node version and locked Python dependencies.

The following focused command passed 50 tests, including the existing relocated
build, export digest-chain and offline verifier regressions; the scoped
`git diff --check` also passed:

```sh
uv run --locked --cache-dir .uv-cache python -m unittest \
  tests.contract.test_okf_plus_build \
  tests.contract.test_okf_plus_export \
  tests.contract.test_okf_plus_verify \
  tests.contract.test_ci_okf_plus_evidence_privacy
```

The command was executed with the existing locked environment's Python
interpreter. A fresh final corpus verification, generated export and canonical
CI remain integration gates for the final input bytes. No generated receipt was
refreshed by this review. The earlier reuse-review paragraph describes its
initial checkpoint: ONS PR #14 is now confirmed merged at
`125981a2f29d2114da34128b3a5031ec55006709`; the updated reuse review retains
separate inspected-source, source-acceptance and live-consumer identities.

## Shadow planner scale boundary

The final metadata import exceeds the CI shadow planner's former 20,000-path
ceiling. The planner now admits at most 65,536 changed paths, matching the
source-package file ceiling. Its separate 64 MiB Git inventory and 4,096-byte
path bounds remain unchanged. Both names in a rename count towards the path
limit, and exceeding it still fails closed before deduplication. Unknown paths
still select full assurance; the impact map, lane decisions and shadow-only
status have not changed. Canonical assurance remains mandatory and full.

All 34 focused planner tests passed, including the exact 65,536-path boundary,
one-over rejection through both planning entry points, rename counting,
unknown-path full assurance at the limit and UTF-8 path-byte bounds:

```sh
uv run --locked --cache-dir .uv-cache python -m unittest tests.contract.test_ci_impact_plan
```

This bounded synthetic evidence does not replace the final committed-revision
Git inventory or canonical CI result.
