# Architecture review maintenance disposition

This is the engineering disposition prepared on 17 October 2026 under the
authorised release-preparation work. It accounts for **all 34 findings** in the
[architecture review][review]: **four repaired and 30 remaining**. It records
maintenance priorities and conditions; it does not claim owner acceptance of
debt, waive release gates or approve a deployment.

The original implementation evidence remains pinned to
`97bc45635a91064cd78f06bf0848ad7636f05439`. Each finding link below points to its
exact review entry at `72bc5aaf66242db219cdde5e2754a1a5e635a532`, including those
original source references. The repair records at that revision cover commits
`70249136` and `72bc5aaf`. This document does not rewrite the historical review or
infer that an unreferenced exported API is safe to delete.

## Meaning and release effect

| Disposition | Count | Meaning |
| --- | ---: | --- |
| Fixed | 4 | Implemented, independently reviewed and locally verified in the linked repair record; exact release-candidate assurance still applies. |
| Scheduled follow-up | 24 | Recommended bounded maintenance work at the stated trigger. Scheduling here establishes an engineering sequence, not a booked date, new issue or owner commitment. |
| Retain compatibility | 1 | Keep the public surface until consumer evidence and an explicit compatibility decision support changing it. |
| Accepted bounded debt | 5 | Engineering recommendation to retain the current implementation within the stated limits and revisit it at the stated trigger. This label is not an owner waiver. |
| Fix before stable release | 0 | None of the remaining review findings demonstrates a current behavioural defect that independently requires blocking release of an unchanged, already bounded profile. Conditional promotion requirements below still apply. |

This last conclusion is limited to these findings. It does not establish that a
stable release is ready, that dependencies are free of vulnerabilities, or that
every possible defect has been found. For example, EX-06 becomes required work
before promoting the private pilot to a declared stable output contract, and
EX-03 must be resolved before introducing concurrent builds across different
roots. A newly demonstrated defect or a change outside a documented bound
requires fresh triage rather than inheriting this disposition.

Safe local cleanup can precede larger extraction work. For the latter, first
characterise behaviour, then extract one responsibility while retaining public
facades, closed operation sets and independent verification. The existing
[improvement plan][improvement] provides the programme context; this document
does not restart paused preservation work or create a new runtime capability.

## Gateway

| Finding | Disposition and rationale | Trigger and verification |
| --- | --- | --- |
| [GW-01][gw01] — unused declarations | **Scheduled follow-up.** Private unused imports, arguments, locals and an unconsumed returned inventory field add confusion. The local byte accumulator remains a live safety check. | Next gateway cleanup: recheck callers and remove only unused declarations. Use unused-symbol diagnostics and the inventory oversize, policy and discovery suites; preserve byte-cap enforcement. |
| [GW-02][gw02] — resource-size conditional | **Scheduled follow-up.** The SSE representation contains the JSON representation plus fixed framing, so one conditional arm is unreachable. Existing bounds remain effective. | Next transport cleanup: express the SSE bound directly. Preserve Unicode, escaped content, long request identifiers and exact size-boundary results. |
| [GW-03][gw03] — repeated authority predicates | **Scheduled follow-up.** Duplication warrants pure internal predicates, but a broad registry rewrite could widen activation or weaken authority checks. | Next change to activation or mounting: retain the exact-five set, operation order, object identity and diagnostics. Run forged-brand, proxy/accessor, suspension, discovery and direct/MCP parity cases. |
| [GW-04][gw04] — repeated sorting | **Accepted bounded debt.** Re-sorting during validation wastes work, but inventories are capped and the review found no measured latency failure. | Revisit if inventory caps grow or measurements show material validation/start-up cost. Compare sorted, unsorted, duplicate and maximum-size cases, rejection behaviour and measured cost before optimising. |
| [GW-05][gw05] — body-failure redispatch | **Scheduled follow-up.** Fabricated requests obscure error precedence; no incorrect response was established. Extracting a mapper without characterisation could alter the contract. | Before the next body/error-mapping change, capture malformed lengths, oversized bodies, route/media combinations, GET/HEAD and disconnects. An explicit mapper must preserve status, problem bodies and precedence. |
| [GW-06][gw06] — query/OpenAPI responsibilities | **Scheduled follow-up.** Large orchestration and projection modules increase change risk but already have bounded responsibilities and behavioural assurance. | At the next query or schema evolution, extract internal modules while keeping transition order visible. Preserve schema identifiers/references and output bytes; run receipt fixtures, cancellation, cache classification, same-key concurrency and publication-order cases. Do not share away independent verification. |

## Core contracts, policy, providers and evidence

| Finding | Disposition and rationale | Trigger and verification |
| --- | --- | --- |
| [CR-01][cr01] — unused core/Python imports | **Scheduled follow-up.** The identified bindings are unused; removal is a narrow clarity improvement with no demonstrated behaviour repair. | Next cleanup: confirm each is neither a re-export nor needed for module side effects, then run affected TypeScript checks and existing Python tests. No mirror tests are needed for import removal. |
| [CR-02][cr02] — unreferenced public surfaces | **Retain compatibility.** `publicEvidenceDocumentSha256`, `w3cTraceId` and `ExecutionBoundary` are public or test-used surfaces. Repository searches do not establish absence of external consumers. | Remove or deprecate only after consumer/export review and an explicit API compatibility decision. Preserve public import/export checks meanwhile; record the migration and version impact if a removal is proposed. |
| [CR-03][cr03] — persistence/versioned validation boundaries | **Scheduled follow-up.** Large checkpoint and receipt-validation modules are maintainability risks; their persistence and historical-version semantics make a hurried split riskier than bounded retention. | Before substantial checkpoint or receipt-family changes, separate inventory, publication and orchestration behind the existing facade. Require golden hashes, hostile mutations, crash/recovery, corruption, replay, retention and mode cases, plus independent verification. |
| [CR-04][cr04] — ONS adapter responsibilities | **Scheduled follow-up.** Transport, admission, reservations and one-shot outage proofs need clearer boundaries. Private capabilities are intentional and must survive extraction. | At the next adapter lifecycle change, document ownership states before moving code. Verify cancellation/reservation races, no-egress paths, deadlines, decompression bounds and replay/forgery rejection. |
| [CR-05][cr05] — dense CPIH transaction predicates | **Scheduled follow-up.** Dense statements obscure all-or-none and compare-and-swap rules; the review did not find an incorrect transaction. | Expand formatting and name family-specific predicates before changing transaction behaviour. Preserve concurrent-head, copied-plan, store/software substitution, corrupt-state, lost-acknowledgement/readback-failure and post-write-abort cases. Keep persistence evidence distinct from formal-model claims. |
| [CR-06][cr06] — canonical-number parity | **Accepted bounded debt.** Python canonicalisation and TypeScript number serialisation have a tested but limited shared domain; no wrong hash was demonstrated. The synthetic execution lane is a separate boundary. | Before changing accepted numeric domains, canonicalisation or supported runtimes, extend a common corpus consumed independently by both implementations: rounding/exponents, negative zero, UTF-16 key order, depth and malformed values. Treat any demonstrated mismatch for accepted inputs as a correctness defect requiring repair. |
| [CR-07][cr07] — inactive/future comments | **Scheduled follow-up.** One header was corrected during the review, but remaining historical wording can still confuse implemented models with public activation. It does not itself activate a capability. | Before publishing changed module documentation, audit remaining wording against actual consumers and retain the candidate/public distinction. Use source/token equivalence where appropriate and type checks for comment-only edits; CT-01 covers schema prose separately. |

## Explorer and experience UI

| Finding | Disposition and rationale | Trigger and verification |
| --- | --- | --- |
| [UI-01][ui01] — navigation focus | **Fixed** in `70249136`; [repair and verification record][ui-repair]. Rendered destination headings accept programmatic focus, while controls, skip-link behaviour and stored-scroll navigation retain their intended behaviour. | Keep real-browser active-element, keyboard, history, modified-click, skip-link and accessibility regressions in release-candidate checks. The repair record reports all 45 local browser tests passing. |
| [UI-02][ui02] — query length units | **Fixed** in `70249136`; [repair and verification record][ui-repair]. State, input and URL handling consistently use 200 UTF-16 units; normalisation precedes truncation without splitting code points. | Preserve supplementary-character boundaries, NFKC expansion, serialisation/parsing and browser reload cases. Oversized incoming URLs must continue to fail admission. |
| [UI-03][ui03] — unused helpers/arguments | **Scheduled follow-up.** The identified local helpers, arguments and test imports are unused; similarly named live bindings and compatibility exports must not be swept up. | Next UI/intake cleanup: repeat caller/export searches, then run affected type, graph/component and intake checks. Delete only declarations whose lack of use is established. |
| [UI-04][ui04] — hosted display predicate | **Scheduled follow-up.** Named pure predicates would make the large Boolean check reviewable. It remains a display-subset check, not full cryptographic or chain verification. | Before changing displayed evidence fields or mode support, preserve the existing mutation matrix and explicit verification limits while extracting predicates. |
| [UI-05][ui05] — browser orchestration | **Scheduled follow-up.** Navigation, URL/history, loading, rendering and file intake need smaller modules. Existing focus and Unicode repairs provide behavioural baselines. | Before substantial journey changes, isolate one orchestration responsibility at a time. Cover late file-read generations, cancel/clear/new selection, history, offline behaviour and manual tool actions. Declare an intake workspace dependency before replacing relative source imports. |
| [UI-06][ui06] — duplicate build primitives | **Scheduled follow-up.** Filesystem/path/checksum primitives can be shared; CSP, public inventories and publication markers intentionally differ between products. | Next build-tool change: extract only pure Node-side primitives. Run both build-boundary/distribution suites and compare generated bytes. Keep product policies separate and Node dependencies out of browser bundles. |
| [UI-07][ui07] — copied strict-JSON parser | **Accepted bounded debt.** The browser copy intentionally avoids provider/network dependencies. Sharing the whole provider module would weaken that boundary. | Any parser fix, limit change or new JSON intake format must update a shared conformance corpus: duplicate/escaped keys, surrogates, unsafe numbers and depth. Preserve intentional limit/error differences; a neutral package is optional, synchronised assurance is required. |

## Operations and assurance

| Finding | Disposition and rationale | Trigger and verification |
| --- | --- | --- |
| [OP-01][op01] — private helpers without callers | **Scheduled follow-up.** Four private helpers have definition-only evidence. Related underlying parser/classification helpers are still active. | Next operations cleanup: repeat repository caller searches before removing the exact four declarations. Run privacy, quarantine and parser regressions; retain `_classify_codex_text_key_fragments` and `_leading_jsonc_comments`. |
| [OP-02][op02] — gateway-image module size | **Scheduled follow-up.** Privacy parsing, BuildKit, context pins and OCI inspection deserve separate modules, but a large pre-release rewrite would create unnecessary assurance churn. | Extract one bounded responsibility behind the stable facade during image-tool maintenance. Preserve image/privacy/container/OCI, advisory and provenance checks and output bytes. Independent image derivation and exact-image release assurance remain mandatory now. |
| [OP-03][op03] — preservation capture boundaries | **Accepted bounded debt.** Capture, storage, redaction, projection and private imports need clearer interfaces. The separate preservation acquisition lane is paused and is not the hosted-product runtime. | Before resuming preservation or changing its formats/storage, define low-level interfaces while retaining independent verifier semantics. Use synthetic crash/quarantine, legacy projection, serial/parallel and recovered-index checks. This disposition does not authorise restarting private acquisition. |
| [OP-04][op04] — contract validator orchestration | **Scheduled follow-up.** Named family checks would clarify the large validator; explicit aggregate coverage currently guards against omissions. | Next contract-family addition or validator maintenance: retain a closed central registry and explicit counts rather than reflection-based discovery. Explain intentional changes to the review baseline of 102 schemas, 153 records and ten bad selections; retain dedicated tests and the distinction between receipt shape and cryptographic verification. |
| [OP-05][op05] — unused Python imports | **Scheduled follow-up.** Five AST-unused imports are cleanup candidates, subject to export and side-effect review. | At the next narrow cleanup, verify each use/re-export and run existing affected tests. Do not treat AST non-use alone as permission to remove externally visible names. |

## Experimental, local, hosted and metadata paths

| Finding | Disposition and rationale | Trigger and verification |
| --- | --- | --- |
| [EX-01][ex01] — local CPIH key constant | **Scheduled follow-up.** The stale local constant is superseded by shared input schemas. It does not change the advertised contract. | Next local CPIH cleanup: remove the unused binding after a caller search; run unused-symbol checks and existing local MCP tests. |
| [EX-02][ex02] — local/hosted output fragments | **Scheduled follow-up.** Receipt and vocabulary fragments repeat, while result envelopes and storage checks differ legitimately. | Before changing shared receipt fields, extract only the common vocabulary/shape. Preserve Workers validator copies, error codes and separate storage validators. Snapshot both tool contracts and run both wire suites. |
| [EX-03][ex03] — implicit mutable build root | **Accepted bounded debt.** The maintained CLI builds sequentially; the risk arises with interleaved library calls for different roots, not the current use. EX-07's schema repair does not remove this limitation. | **Fix before introducing concurrent/multi-root library builds.** Pass root or a per-build context explicitly; verify two-root interleaving and byte-identical relocated builds. Until then, keep one build context per process. |
| [EX-04][ex04] — source-format-dependent coverage extraction | **Scheduled follow-up.** The regex inventory can reject harmless formatting changes. It is an active assurance dependency, not dead code; no missed operation was demonstrated. | Before refactoring the recognised declarations or changing the inventory, use inert manifests or syntax parsing while retaining independent source-to-catalogue equality. Test true additions/removals and format-only changes. |
| [EX-05][ex05] — compressed metadata stages | **Scheduled follow-up.** Named pure mappings and expanded control flow would clarify provenance, validation and mutation stages. EX-07 separately repaired the demonstrated schema-admission gap. | At the next metadata change, format/extract before redesigning performance. Compare every generated fixture file byte-for-byte and preserve frozen locators, record counts and source-import admission. |
| [EX-06][ex06] — pilot output discoverability | **Scheduled follow-up; required before promoting a stable pilot output contract.** Inputs are declared and receipt integrity is checked at runtime, but clients lack advertised output schemas. Their absence is not by itself an MCP protocol violation or a blocker for the unchanged experimental/private profile. | Before stable pilot promotion, review versioned result/problem/capability schemas as a compatibility change; verify SDK output validation, complete non-App results, protocol versions and schema/fixture parity. Retain pilot receipt prefixes/limits and distinguish structural validity from source accuracy. Do not apply the pilot finding to the separate exact-five gateway by analogy. |
| [EX-07][ex07] — missing-schema fallback | **Fixed** in `72bc5aaf`; [metadata repair record][metadata-repair]. Normal builds require and validate all three schemas before records are read; failure preserves an existing bundle. | Preserve missing-each/all-schema cases for fresh/existing output and schema-only invalid inputs. The repair record reports 181 passing metadata tests and byte-identical output for all 11 generated fixture files. |

## Contract catalogue

| Finding | Disposition and rationale | Trigger and verification |
| --- | --- | --- |
| [CT-01][ct01] — stale schema activation wording | **Scheduled follow-up.** Descriptions saying inactive/future conflict with current local/candidate consumers; architecture documentation now explains the actual boundary. Editing schema prose can change pinned schema digests, so it needs deliberate compatibility handling. | Before the next schema publication/version update, reconcile descriptions with consumers, review all pinned hashes and OpenAPI/MCP parity, and preserve the public-registration distinction. Never rewrite historical evidence to match new prose. |
| [CT-02][ct02] — intake descriptor parity | **Fixed** in `72bc5aaf`; [intake repair record][intake-repair]. Existing package assurance now validates both schema definitions and actual planner/ZIP outputs using locked development tools. Runtime path/UTF-8 checks remain intentionally stricter. | Keep the package test in canonical assurance. The record reports 21 passing tests, 43 labelled conformance cases including 16 rejected mutations, and four mutation proofs detecting schema/producer drift. No runtime dependency or published schema byte changed. |

## Release gates this disposition cannot clear

The repaired defects have local evidence. The linked repair records explicitly
do not establish remote canonical CI, immutable publication or deployed acceptance
for a release candidate. Subsequent release work must attach current evidence;
historical access failures are not evidence that access remains unavailable.

Before tagging a stable release, the [delivery model][delivery] still requires
the exact commit, a clean tree, required remote checks, locked dependencies and
SBOM/provenance, affected assurance, checksummed artefacts, the deployment target,
support/deviation boundaries and rollback. A version change also requires
synchronised manifests, the dated changelog, release notes and release-readiness
validation. These are actual release gates: an absent or failed required item
blocks the corresponding release step even though none of the remaining
maintenance findings alone mandates a broad refactor.

The [open MCP roadmap gate][roadmap] additionally requires real protocol and host
interoperability, deterministic provider evidence, advertised-tool parity and
deployment/rollback acceptance. A supported deployment must use the exact tagged,
attested artefact and pass real browser/client verification. Publishing a private
Sites page does not establish this public service evidence. The
[private Sites pilot record][sites] has its own audience, receipt, allowance and
identity/restore boundaries; its dated observations must not be presented as a
current deployment probe. A stable promotion invokes EX-06's contract work and
the applicable service acceptance gates.

If the selected deliverable is instead the [local evaluation edition][local], its
separately identified prerelease, exact archive/checksum evidence and acceptance
gates still apply, including the unaided colleague walkthrough. A clean-room
agent run cannot replace that human check. It must not be labelled a stable
public service or silently reuse public-release version/support claims.

No deletion, runtime refactor, release tag, publication or debt waiver is performed
by this document. Completion evidence should update the relevant disposition in
a later change while retaining the original finding and its pinned sources.

[review]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW.md#L1
[gw01]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_GATEWAY.md#L14
[gw02]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_GATEWAY.md#L15
[gw03]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_GATEWAY.md#L16
[gw04]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_GATEWAY.md#L17
[gw05]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_GATEWAY.md#L18
[gw06]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_GATEWAY.md#L19
[cr01]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_CORE.md#L6
[cr02]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_CORE.md#L12
[cr03]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_CORE.md#L18
[cr04]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_CORE.md#L24
[cr05]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_CORE.md#L30
[cr06]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_CORE.md#L36
[cr07]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_CORE.md#L42
[ui01]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_UI.md#L11
[ui02]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_UI.md#L19
[ui03]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_UI.md#L25
[ui04]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_UI.md#L31
[ui05]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_UI.md#L37
[ui06]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_UI.md#L43
[ui07]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_UI.md#L49
[op01]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_OPERATIONS.md#L8
[op02]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_OPERATIONS.md#L27
[op03]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_OPERATIONS.md#L39
[op04]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_OPERATIONS.md#L51
[op05]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_OPERATIONS.md#L63
[ex01]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_EXPERIMENTAL.md#L16
[ex02]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_EXPERIMENTAL.md#L17
[ex03]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_EXPERIMENTAL.md#L18
[ex04]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_EXPERIMENTAL.md#L19
[ex05]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_EXPERIMENTAL.md#L20
[ex06]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_EXPERIMENTAL.md#L21
[ex07]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_EXPERIMENTAL.md#L22
[ct01]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_CONTRACTS.md#L7
[ct02]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW_CONTRACTS.md#L15
[ui-repair]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/implementation/EXPLORER_UI_REPAIRS.md#L8
[metadata-repair]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/implementation/VALIDATION_REPAIRS.md#L9
[intake-repair]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/implementation/VALIDATION_REPAIRS.md#L26
[improvement]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/chronicle/IMPROVEMENT_PLAN.md#L1
[delivery]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/implementation/DELIVERY_AND_RELEASE.md#L43
[roadmap]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/implementation/ROADMAP.md#L29
[sites]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/implementation/SITES-218_PRIVATE_MCP_PILOT.md#L1
[local]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/decisions/ADR-0017-local-evaluation-edition.md#L15
