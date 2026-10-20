# Current progress

Last updated: 20 October 2026

## Repository assurance time allowance

The post-merge [CI run](https://github.com/chris-page-gov/gis-ai-go/actions/runs/39431969961)
for `9f2ab130` and its ordinary retry both reached a cancelled repository-assurance
result around the 20-minute job limit. Both completed the assurance tests, clean
source-archive journey and evidence uploads successfully, but the aggregate gate
failed and downstream provenance and attestation jobs were skipped. On retry,
assurance took 18 minutes 1 second, the archive journey 71 seconds and evidence
upload 31 seconds, leaving insufficient time for setup and cleanup.

The [issue #153](https://github.com/chris-page-gov/gis-ai-go/issues/153)
maintenance follow-up raises this job's bounded allowance to 30 minutes and
updates its exact workflow contract. The five-minute archive step cap, all checks,
permissions and mandatory gates remain in force. At preparation, canonical
acceptance of this repair and the resulting main-commit provenance remained
pending; no deployment is included.

## Local GML recovery method

The owner authorised continuing [issue #153](https://github.com/chris-page-gov/gis-ai-go/issues/153)
on the existing local Docker installation and external drives. The
[generic GML method](docs/implementation/OS_LOCAL_GML_PROCESSING.md) adds
provider-free complete selected-input traversal, bounded archive admission and
small source-bound JSON-LD field cards. Independent feature-membership counts
remain distinct from conversion success. Raw payloads are retained; schema
closure, format-mapping completeness and authoritative PSGA coverage remain open.
Only generic methods and synthetic tests belong in this increment. Private
restoration, source selections and operating state remain outside the repository.
All 36 affected synthetic tests passed in the pinned Python 3.12 Linux runtime.
Local links, changelog fragments and secret/machine-path checks passed. Canonical
source assurance remains pending; no public deployment, installed connector or
full-coverage claim follows.

## OS small-file knowledge and acquisition recovery

The owner authorised unattended OS/PSGA recovery on 19 October. Work is tracked
in [issue #153](https://github.com/chris-page-gov/gis-ai-go/issues/153) and the
[recovery record](docs/implementation/OKF_OS_RECOVERY.md). The accessible bounded
pass is complete: all 2,303 frozen documentation targets are accounted for,
with 2,302 captured and one documented HTTP 307 redirect gap. All captured pages
passed an independent audit of 216,765 lossless private passages, including exact
reconstruction, checksums and the 16 KiB passage ceiling. Six newer documentation
pages were captured and audited separately; the redirect target is recorded
without asserting source equivalence. No frozen targets remain unresolved.

The local build reproduces 30,833 metadata records and 2,915 native field nodes.
The verified private export `run-d78f08085053400e9475393f0b4aaaa6` provides matched
explanation candidates for all 2,915 fields, with zero missing or ambiguous
matches. Its 3,347 files are at most 16,383 bytes each. These are candidate links
to source explanations; documentation versions have not been independently
matched to every collection version, and universal question-answering coverage
has not been established. Small cards and explanatory passages retain native
definitions, schema nuances, provenance and explicit observed scope.

Fresh schema and queryables capture completed for all 94 current NGD collections:
188 successful metadata requests retained complete native definitions and 3,755
small property cards across the two lanes. All 44 WFS feature-type schemas were
also captured. Bounded first pages from all 94 NGD collections returned 186
records in total, completely profiled into 3,968 small field knowledge cards.
Their temporary raw payloads were disposed after verification, with zero remaining
in that workset. This completes those selected first pages, not national feature
traversal or all PSGA data. The existing key, configured account metadata and
licensed payloads remain excluded from Git and public publication.

All 374 configured download-package versions were inventoried, listing 4,973 file
entries and about 1.81 TB compressed, including history and repetition; the
largest file is about 15.6 GB. Live access identified 47 configured packages,
which does not establish the full entitlement denominator. Bulk archive transfers
remain deferred pending the exact Azure host network adjustment. The draft save
was rejected as uneditable; the proposed one-host change remains local.
The owner requires transient processing and verified disposal, not permanent
national storage. Retrieval recipes and knowledge can persist after raw disposal.

Query capability profiles and a field-coverage planner distinguish server/local
projection, separate response bundles and reviewed equivalent fields. Live Road
Link v5 equality-OR batching succeeded; documented IN requests failed and
`properties` was explicitly rejected. A bounded two-ID extraction and a fresh
repeat verified both records, EPSG:7405 and disposal. A same-identity WFS comparison
matched three width fields on both sampled roads, reducing response bytes from
4,668 to 2,084. WFS-to-NGD measurement equivalence remains unassessed. Source
ambiguities remain explicit. Private unsent support drafts retain sanitised calls
and hashes for NGD IN/OR differences and malformed WFS GeoJSON when geometry is
omitted from projection. No support ticket was sent.

All 353 affected tests and final-source CI/CodeQL passed; the initial recovery
increment merged through [PR #154](https://github.com/chris-page-gov/gis-ai-go/pull/154)
as `9a492dba`. Protected-main CI/CodeQL, independent image derivation and
provenance all passed; results are recorded on that PR and issue #153.
A bounded follow-up reviews all seven advertised WFS operations, including
property-value retrieval and stored queries, and records the documented precedence
of `bbox` over a separately supplied attribute filter. Combined WFS conditions
must use a single XML filter. Advertised capabilities and validated behaviour
remain separate. The follow-up requires its own canonical assurance.
No full national acquisition, complete PSGA coverage, feature archive, new live
OS connector or installed-client admission is claimed.

New [availability reporting](docs/implementation/OS_DATA_AVAILABILITY.md) keeps
request access, expected presence, observations and retrieval completion separate.
Null, zero, missing properties, empty selections, incomplete pages and denied
requests have distinct outcomes. [Presentation research](docs/implementation/OS_RETRIEVAL_PRESENTATION_RESEARCH.md)
and a small output-intent profile record map/table/analysis requirements and
VizQL research. Optional planner constraints require explicit native-value,
geometry or portrayal evidence before cost comparison. Tableau-hosted pages remain blocked, but its vendor GitHub OpenAPI contract
was inspected at a pinned commit. It documents data/model queries rather than a
rendering endpoint; no Tableau service integration is claimed.

Latest implementation checkpoint: bounded dependency security repairs under
[issue #142](https://github.com/chris-page-gov/gis-ai-go/issues/142), following
[REVIEW-222 issue #151](https://github.com/chris-page-gov/gis-ai-go/issues/151).

The owner agreed to finish the existing private Sites teaching exemplar first;
the full five-tool gateway port remains a separate milestone. Pinned pnpm 10.33.2
resolved the minimum current fixes for Hono, Undici, source-map-js and both
installed MCP clients. The before/after registry audit reports 14 then zero
advisories for the checked lockfiles. The server and Node adapter stay on SDK
2.0.0; the client and its own core dependency use 2.2.0. Historical observations
retain their original versions. The [dependency disposition](docs/operations/DEPENDENCY_SECURITY_2026-10-17.md)
records source exposure, exact changes and verification limits.

The hosted workbench ships the client library, so its remediation needs a new
build and Site publication. The existing six-tool Worker server uses a separate
dependency graph. Local patched builds are not evidence that version 8 serves
new bytes. Updated Sites source/build tooling and actual installed-client
authentication remain pending; no new deployment or release is claimed.

The owner authorised continuing towards release and checking the updated OpenAI
Sites hosting path. Native readback confirms the existing private Site is active
at version 8 with its `/mcp` endpoint and provisioned connection plugin. Actual
installed-client authentication and tool execution remain unconfirmed.
The later CI governance and OKF security changes from `main` were integrated at
`0a046021` before exact-source assurance. The GitHub connector and Git transport
now work, although direct shell API requests remain blocked.

The [maintenance disposition](docs/implementation/MAINTENANCE_DISPOSITION.md)
accounts for all 34 findings. The [release closure record](docs/implementation/RELEASE_CLOSURE.md)
separates the private Sites milestone from supported exact-five release gates.
After integration, all 191 affected metadata tests and 22 Sites evaluator/native
mount tests passed. A clean-source five-tool acceptance run passed all 15 tests;
the SDK walkthrough verified five distinct receipts and three refusal cases.
The [five-tool acceptance record](docs/implementation/FIVE_TOOL_ACCEPTANCE.md)
binds the observed source, commands, recovery checks and limits.
Source-bound local evaluation receipts were regenerated by executing their exact
selected suites; only material hashes and derived identities changed. Outcomes,
assertions, limitations and historical evidence guards remain unchanged.

## Metadata and intake validation repairs

The owner authorised the next two validation improvements after the UI fixes.
OKF+ builds now require all three schema files before reading records, and failed
validation preserves an existing generated bundle. Minimal fixtures copy the real
schemas. Intake package assurance checks both published schema definitions and
actual planner/ZIP results, including rejected mutations and the distinction
between structural schema validity and stricter runtime checks. These changes
reuse locked development dependencies and add no runtime dependency.

Local verification passed all 181 affected OKF+ tests and all 21 intake package
tests. The intake conformance checks cover 43 cases; four deliberate mutation
checks demonstrated detection of descriptor and producer-output drift. All 11
generated files from an unchanged complete metadata fixture remain byte-identical.

The [validation repair record](docs/implementation/VALIDATION_REPAIRS.md) records
regression evidence, affected test results and integration limits. Supported hosted
gateway deployment remains a later milestone; no provider or deployment was
activated by this increment.

## Explorer focus and Unicode repairs

The owner authorised fixing both UI defects from the repository review. Navigation
headings now accept programmatic focus, including record/error views, About and
history restoration, while skip links and form-control focus retain their intended
targets. Search input, canonical state and URL admission now share the existing
200 UTF-16-unit budget; truncation after normalisation preserves complete Unicode
characters. The implementation and validation record is in
[Explorer UI repairs](docs/implementation/EXPLORER_UI_REPAIRS.md).
Committed as `70249136`, with all 45 local Chromium browser tests and 51
Vitest unit/component tests passing, plus type and build/distribution checks.

The original architecture review remains pinned to its historical source revision.
These fixes do not remove unused code, activate a gateway or publish a deployment.

## Architecture and maintainability review

The owner requested a whole-repository review of dead/unclear code and refactoring
opportunities, with architecture diagrams, formal specifications, inline comments
and a beginner explanation of every contract family. The
[architecture guide](docs/architecture/README.md) and
[prioritised review](docs/architecture/REVIEW.md) provide that source-bound record.
The complete tree inventory covers 32,138 files; 484 code/presentation/migration/
launcher/CI files have individual references and explicit review depth, separating
479 authored files from five pinned vendor files. The contract
register covers 115 JSON Schemas (102 under the root schema directory), embedded
schemas, exported types, dataclasses and OpenAPI projections.

The original review's implementation edits were comments only. The subsequent
repair sections above record the behavioural changes. Local verification and its
limits are recorded in the review; the original checkpoint did not establish a
new release, deployment or canonical CI acceptance. Remote publication is now
being completed through the available GitHub connector and Git transport.

## CI governance case-study correction

The owner requested verification and implementation of the missing trusted-base
agreement identified in a case-study peer review. The baseline at `97bc456` runs
candidate-only shadow planning; the review's policy re-routing example reproduces.
The [ASSURE-209 agreement increment](docs/implementation/CI_IMPACT_AGREEMENT.md)
adds isolated base-owned comparison, conservative bootstrap and regression tests.
It remains shadow-only: full assurance continues, and canonical PR acceptance is
separate from local verification. [Issue #97](https://github.com/chris-page-gov/gis-ai-go/issues/97)
remains open for an externally protected gate and promotion evidence. No repository
ruleset, deployment, release or provider entitlement is changed.

The [owner-supplied meeting briefing and peer review](docs/research/2026-10-13/governance-as-code/README.md)
are retained with provenance and separate source rights. The review assessed the
earlier 11-page case study, not the revised briefing or the implementation in
[PR #147](https://github.com/chris-page-gov/gis-ai-go/pull/147).

## Current checkpoint

- Supported public product: [v0.1.0 static Explorer](https://github.com/chris-page-gov/gis-ai-go/releases/tag/v0.1.0).
- Accepted local runtime: LOCAL-212 through [PR #112](https://github.com/chris-page-gov/gis-ai-go/pull/112),
  commit `57e49322e305b499fccfbb6c46bc15e2a0ff38f9`. A clean clone can run
  the five tools and three resources with approved cached data and no provider egress.
- Chronicle baseline: `6c76c92a18da779766f8d49acbbd7dbbd31abb97`, following
  preservation repairs #114/#115. Protected-main [CI](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34810081520)
  and [CodeQL](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34810081562) passed.
- Public MCP hosting, live deployment acceptance and the `v0.2.0` tag/release
  remain open in #23, #24 and #25.

## Previous implementation checkpoint: EXPERIENCE-221

The latest exact-commit CI, publication and client-acceptance checkpoint is
[EXPERIENCE-221 issue #143](https://github.com/chris-page-gov/gis-ai-go/issues/143),
with implementation review in [PR #144](https://github.com/chris-page-gov/gis-ai-go/pull/144).
The following local verification snapshot was recorded before those final gates.

The preceding task was [EXPERIENCE-221](docs/implementation/EXPERIENCE-221_LEARNING_AND_EVALUATION.md),
authorised on 2 October: establish actual MCP/client facilities; cover every
current feature with personas, stories, questions, sources, presentation forms
and plain-language learning help; prepare voice-driven page actions and bounded
file intake. The owner selected facilitator-led use and offline activities for
the 7 October event with students aged 13 to 14. Individual accounts, devices and
wider access remain unconfirmed; the Site stays private.

Implementation is complete locally on `codex/experience-221` from
`387e86695e7002e78f005e972703f5c5e51fa546`. The catalogue currently distinguishes
45 baseline facilities, 29 new local facilities and eight planned facilities.
It contains nine personas, 222 questions and 904 language variants. Authored
coverage is separate from actual user/AI outcomes. Native Sites registration,
Claude and spoken Voice acceptance require their own observed evidence. Local
folder/ZIP inventory discovers Shapefile companions; full binary feature import
and arbitrary URL downloading remain separate work.

Local verification passed: 47 pilot/native-mount tests, 44 workbench tests,
19 intake tests, 11 evaluation-harness tests, 30 deterministic intake fixtures
and 20 offline browser journeys. The browser checks include keyboard use and
320/390/1280-pixel layouts at normal and doubled text size, with no page network
requests, page errors or automated accessibility violations. The page-tool bridge
is mocked for these checks. All 222 natural-language questions remain unobserved;
canonical CI, private publication and actual client/Voice acceptance are pending.

The preceding [OKF-220](docs/implementation/OKF-220_METADATA_KNOWLEDGE_FRAMEWORK.md)
metadata increment was merged through [PR #141](https://github.com/chris-page-gov/gis-ai-go/pull/141)
at `387e86695e7002e78f005e972703f5c5e51fa546`. Protected-main CI `36990326268` and
CodeQL `36990336704` passed, including independent image derivation and provenance.
The complete 30,833-record build has zero omitted retained records or semantic
fields, 36 automated retrieval passes and four pinned-engine passes. Four
interpretation questions remain unassessed. Public metadata and separate private
original-document archives were verified, including a fresh-directory offline
replay. Global catalogue completeness and installed Ask OKF admission remain open.
The final acceptance record is [issue #140](https://github.com/chris-page-gov/gis-ai-go/issues/140#issuecomment-5949786558).
Unchanged macOS harnesses reject this host's sandbox executable identity; their
checks remain intact. Dependency maintenance is separately tracked in #142.

At the EXPERIENCE-221 starting usage check, 59% of the weekly allowance was used
(41% remaining), with 62,460.4597875 existing credits. These are account-wide
figures, not task cost. No new service, purchase, overage or reset is authorised
by this checkpoint.

Unattended execution correction (2 October): an optional browser/CDP permission
prompt held the coordinating task overnight. Remaining work uses non-interactive
capture and offline checks; optional UI acceptance is separate. The preflight and
continuation rule is now recorded in `AGENTS.md` and the OKF-220 operating record.

The preceding Sites increment was merged through PR #139. Protected-main CI
`36945982145` and CodeQL `36945982033` passed. Its remaining hosting/registration
conditions below stay open and do not block the metadata work.

On 1 October the owner authorised an unattended, owner-private Sites MCP pilot
with live OS/ONS APIs, a PSGA suitability assessment with an open-data fallback,
common-question evaluations and performance observations. This is the current
preceding task; the retained LOCAL-214 and WEB-216 checkpoints below remain evidence.
Work is tracked in [SITES-218](docs/implementation/SITES-218_PRIVATE_MCP_PILOT.md).
The baseline is `7496595a1c09f3cac7ca9da2bef69a25443516a9` on branch
`codex/sites-mcp-pilot`. Private Site version 7 is deployed from runtime revision
`8ab0f592ce949f136501122f93bb81becbeb1af1`. Its guarded `/pilot/mcp` route passed
nine live correctness/refusal cases and 25 repeated performance checks. The
signed-in owner browser retrieved ONS area codes. All three tested protocol
versions passed their bounded discovery/refusal checks. A complete private
checkpoint contains 33 independently hash-checked receipts; stopping and
reinstating the application preserved the checked receipts and allowance counts.
See the [hosted observation](docs/implementation/SITES-218_HOSTED_OBSERVATION.md)
for timings, rollback evidence and precise limits. The version 7 Site still lacks native MCP registration. The new Sites MCP skill
now documents `capabilities: ["mcp"]` and `POST /mcp`; EXPERIENCE-221 implements
and separately verifies that route without treating it as completed OAuth acceptance.
Native OAuth, independent AI-client acceptance and full public release remain
separate gates. Required PR assurance for the runtime revision passed. Integration
and exact-head canonical acceptance are tracked in [PR #139](https://github.com/chris-page-gov/gis-ai-go/pull/139);
this deployment observation does not establish protected-main acceptance.

The owner authorised existing OS credentials and, on 2 October, explicitly
authorised PSGA/NGD validation. Bounded local Building v4 and Road Link v5 samples
both returned successfully and passed structural checks; no licensed feature
contents were retained. Account evidence and hosted recipient arrangements remain
separate from this demonstrated access. The entitlement assessment is private.
Spending authority is existing included allowances only, with no new paid
services or chargeable overage. Open-data work proceeds independently of PSGA.
The owner also authorised replacement of the private Sites API test token only
if needed; such a token does not establish signed-in end-user identity.

The owner selected [LOCAL-214 #118](https://github.com/chris-page-gov/gis-ai-go/issues/118)
as the immediate delivery track: finish a dependable standalone local evaluation
edition while keeping Sites support separate. The implementation adds visible
cache-expiry capability health, source-only packaging, a separate MCP demonstration,
an illustrated walkthrough and an additive prerelease policy in
[ADR-0017](docs/decisions/ADR-0017-local-evaluation-edition.md). Required acceptance
is recorded in the [local profile](evaluation/local-edition-profile.v1.json).
Implementation, protected-main acceptance, an unaided colleague walkthrough and
prerelease publication are distinct gates; none is implied by this status note.
The version remains `0.1.0`, targeting `0.2.0`; `v0.2.0-local.1` is reserved for
a separately accepted local prerelease, not an already published release.

### WEB-216: retained progress and separate dependencies

The aggregate #125 work item must remain open until its wider milestones pass.
M1 inception and the bounded M3 local CPIH vertical slice are implemented;
M2 is partial, M4 geospatial/story expansion is unfinished and M5 hosted
acceptance remains partial. The source documents below retain the actual
experiments, failures and scope rather than treating one merged increment as
completion of the whole work package.

Browser authentication to the private Site succeeded on 19 September. The
remaining direct-client gate is the platform's supported MCP declaration and
authentication discovery, not another request for the owner to sign in.
An independent authenticated Claude connection has not been proved. No wider
MCP port or audience change is justified by browser login alone. An OpenAI support
receipt is retained privately; specialist resolution is not recorded.

The owner authorised [WEB-216 #125](https://github.com/chris-page-gov/gis-ai-go/issues/125):
advance WebMCP into OKF-led ONS discovery and governed retrieval, with OS/ONS
geography, consistent staff stories, reproducible experiments and a shared
person/AI evidence interface. Continue until blocked and merge verified increments.
The inception is merged through [PR #126](https://github.com/chris-page-gov/gis-ai-go/pull/126)
at `87c5997eecc6b6ddf4487cc226d3905544f5595f`.
The metadata foundation is merged through [PR #127](https://github.com/chris-page-gov/gis-ai-go/pull/127)
at `52c46d9cd619d5c349472c250d2d03aebb3beb3c`, with complete protected-main CI,
CodeQL and provenance passing. A bounded maintained-CPIH API observation returned
two HTTP 200 responses; the full captured series passes the new offline validator.
This is empirical API evidence, not a new live MCP operation or Site deployment.
The retired `cpih01` source is explicitly distinguished from maintained L522/MM23.
PR #128 is accepted at `4c8e6144dfb02ea5d9dcf4cb34fbe34f36529f3e`, with complete
protected-main CI and CodeQL passing. PR #129 is accepted at
`806fdcc5b39cee75c6a9144ffa18cc92a66bfc2a`; PR #130's closed CPIH contracts and
application are accepted at `f4b1a90d64b4aea4c6be3f4b08bcbee1cdfe68ec`. Both
complete protected-main CI and CodeQL runs passed. The separate local workbench
increment has demonstrated genuine in-app-browser page tools calling MCP,
durable July retrieval/inspection, and identical receipt inspection after restart.
Manual January retrieval and Chrome/Edge July retrieval also passed. This working
tree observation is not an accepted-build attestation or hosted capability claim.
See the [local walkthrough](docs/implementation/WEB-216_LOCAL_WORKBENCH_WALKTHROUGH.md).
PR #131 is merged at `fd8106691bb5c3d63e5f11c21b16f1e7c26f4321`; required PR
checks and protected-main source assurance passed. Both main image builds failed
during packaging, including the single unchanged-source retry; the inner failure
cause was not retained. The following PR #132 storage foundation is now accepted at
`b9729b5cacc77e9f2b12790c40ad6349fae7b370`: complete protected-main
[assurance](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34884325687)
and [CodeQL](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34884325565)
passed, including both image derivations, attestation verification and provenance.
This does not retrospectively explain the earlier failure. Bounded diagnostic
improvements are isolated separately. The inactive storage foundation passes 35
focused tests and a real local Workers/D1 restart experiment. It adds no endpoint
or deployment. PR #133's diagnostic repair and PR #134's hosted transport are now
accepted at `67ab535ff4d16f54f777dd45787c2f4742a5150c` and
`1a89c73c7e8dec671cb3abd92c271d3d071c2830`, with complete protected-main
assurance and CodeQL passing. A subsequent guarded Workers experiment passed
19 wire requests, five negative cases and exact receipt inspection after restart,
with no provider egress. The reviewed HTTP/pure-evidence extraction is accepted
through PR #135 at `cbdda51d2753a668670ad3a4dd4cf2b019fdb883`, with complete
protected-main assurance and CodeQL passing. The separately assembled private
Site candidate was deployed on 14 September 2026 at 20:26 UTC. Its schema is
present and its store is empty; operator access remains disabled. The final
built-Site local test passed 19 requests and exact receipt inspection after restart,
but used synthetic identity. At that 14 September checkpoint sign-in awaited the
owner's passkey. That sign-in blocker is superseded by the 19 September update
above; it is not evidence that hosted initialisation, retention and direct-client
acceptance passed.
The old Site demonstration and local workbench are unchanged. See the
[storage experiment](docs/implementation/WEB-216_HOSTED_STORAGE_EXPERIMENT.md).
The OS Open Names Warwick point is captured; ONS boundary metadata succeeded but
three bounded point queries timed out (two GETs and one POST). A real MSOA join
and hosted persistence acceptance remain open. The private candidate deployment
is not a public MCP service or a supported release.
See the [retrieval experiment](docs/implementation/WEB-216_ONS_RETRIEVAL_EXPERIMENT.md), the
[work package](docs/implementation/WEB-216_PUBLIC_DATA_WORKBENCH.md),
[experiment protocol](docs/implementation/WEB-216_EXPERIMENTS.md) and
[source-time journal](docs/chronicle/WEB-216_JOURNAL.md).
`mcp-geo`, `okf-ons` and the `govuk-webmcp` competition entry remain read-only.

## Earlier chronicle checkpoint

The owner started [RETRO-208 #86](https://github.com/chris-page-gov/gis-ai-go/issues/86)
and [CHRON-213 #117](https://github.com/chris-page-gov/gis-ai-go/issues/117) at this
natural break. Work covers the private evidence analysis, public draft chronicle,
agent history, beginner learning path, A4 illustrations, repository code review,
GPT-6 Astra guidance review and a plan for local completion without hosted service.

The code review produces a separate modularisation and optimisation stage. The
local-completion investigation proposes scope and acceptance before changing runtime
or supported-release definitions. Public drafts use evidence cleared for that purpose;
private evidence remains local.

The review edition contains 12 chapters, eight diagrams, a 14-part learning path,
source-linked code findings and a pseudonymous census of 1,043 task threads.
The recovery edition reconciles 23 public outcomes with additional permitted
private evidence into a reviewed minimum of 31 outcomes. It corrects completion
timestamps, joins the recovered asynchronous launches and keeps granular timing,
costs and provenance private. Earlier archives are unchanged. The public revision
contains reviewed paraphrases and aggregates, not private logs or identifiers.
Issue #86 was closed on 14 September 2026 with owner approval on the basis
“all recoverable evidence reconciled; irrecoverable gaps documented”. A
first-ever/exhaustive count still cannot be certified across the remaining
redaction/quarantine gaps. Follow-ons #122/#123 cover client-contract
preflight and source-time attempt journalling without starting implementation.
[LOCAL-214 #118](https://github.com/chris-page-gov/gis-ai-go/issues/118)
defines the next local-edition stages; [IMPROVE-215 #119](https://github.com/chris-page-gov/gis-ai-go/issues/119)
holds the separate optimisation plan. LOCAL-214 implementation is now the active
track; broad optimisation remains separate.

## Preservation

**Scheduled EVID-211 preservation is paused by the owner as of 24 September 2026.**
It has not been restarted by LOCAL-214 work. The post-#115 capture reached
`commit-complete` and complete four-worker offline verification passed for that
snapshot: 3,293 objects and 3,110 projections. Current store identity, inventory and
subsequent results are held in the private operating record. The predecessor remains
unchanged with its recorded semantic failure. [Issue #116](https://github.com/chris-page-gov/gis-ai-go/issues/116)
tracks future incremental-parallel optimisation; it does not block the chronicle.

The 14 September WEB-216 milestone passed complete verification at 3,676 objects
and 4,456 events. A separately verified, owner-only text-recovery supplement
retains 191 objects across 198 events, including previously unsupported source
representations and the private deployment checkpoint. Seven secret-pattern
exclusions remain explicit; the existing stores and daily destination are unchanged.
These are separate verification scopes, not a new whole-history completeness claim.
Later scheduled attempts were blocked and do not supersede that verified
checkpoint. No new complete-verification pass is claimed for those attempts.

## Handoff and historical evidence

Read [AGENTS.md](AGENTS.md) for the working rules, [CONTEXT.md](CONTEXT.md) for
authority, the [roadmap](docs/implementation/ROADMAP.md) for product stages and the
[chronicle](docs/chronicle/README.md) for the learning record. GitHub issues are
authoritative for current item state.

The former 1,147-line progress history is preserved in the
[fixed baseline snapshot](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/PROGRESS.md).
Historical evidence remains in the operation runbooks, changelog and immutable
research pack. This short checkpoint replaces repeated loading of that history.
