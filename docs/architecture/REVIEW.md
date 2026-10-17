# Repository review: dead code, clarity and refactoring

Reviewed source: [`97bc45635a91064cd78f06bf0848ad7636f05439`](https://github.com/chris-page-gov/gis-ai-go/tree/97bc45635a91064cd78f06bf0848ad7636f05439).
Follow-up: UI-01 and UI-02 are addressed in [the Explorer repair record](../implementation/EXPLORER_UI_REPAIRS.md).
The findings and immutable source references below describe the original review baseline.

The review records **34 findings** across six areas. It identifies small unused
fragments, two reproduced UI defects, contract-assurance gaps and concrete module
boundaries for refactoring. It does not establish that a whole runtime subsystem
can be removed. Runtime changes in this work are explanatory comments only.

The resulting [architecture guide](README.md), [formal model](FORMAL_MODEL.md),
[beginner contracts guide](CONTRACTS.md) and [complete contract register](CONTRACT_REGISTER.md)
describe the implementation rather than treating roadmap goals as deployed behaviour.

## Highest-value follow-up work

| Finding | Evidence and consequence | Recommended action |
| --- | --- | --- |
| **UI-01, P2: keyboard focus is lost after navigation** | The [focus helper](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/main.ts#L105-L115) focuses replacement headings that lack `tabindex`, including the [graph heading](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/views/graph.ts#L182-L194). A source-rendered DOM reproduction left `activeElement` on `BODY`. | Make navigation destinations programmatically focusable and add real-browser assertions for active focus after each navigation route. [Details](REVIEW_UI.md#ui-01--p2-restore-focus-to-focusable-navigation-targets). |
| **EX-07, P2: absent metadata schemas silently skip schema validation** | The [OKF+ loader](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/okf_plus/build.py#L44-L50) returns `None` when a schema is missing. This supports minimal fixtures but also applies to a damaged normal checkout; other provenance checks still run. | Make fixture mode explicit; require complete schemas for the normal build. [Details](REVIEW_EXPERIMENTAL.md). |
| **CT-02, P2: intake descriptors lack an identified automated parity gate** | The [published request/result descriptors](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/experience-intake/README.md#L32) sit outside the [root schema scan](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/validate_contracts.py#L182-L194). Direct planner tests do not establish descriptor/output conformance. No actual mismatch was proved. | Validate both descriptors and representative real outputs in package assurance while retaining stricter runtime checks. [Details](REVIEW_CONTRACTS.md#ct-02--intake-schema-descriptors-have-no-identified-automated-parity-gate). |
| **UI-02, P3: Unicode query round trips use inconsistent length units** | [Normalisation](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/state.ts#L23-L32) counts code points; [URL parsing](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/state.ts#L135-L150) counts UTF-16 units. A canonical state containing 101 supplementary-plane letters serialises and then parses to an empty query. Manual input has its own UTF-16 limit, so this is a state/link inconsistency, not a claim about all normal typing. | Choose and document one unit across state, URL and input; add boundary cases for supplementary-plane characters and normalisation expansion. [Details](REVIEW_UI.md#ui-02--p3-make-url-query-length-units-consistent). |

Priorities are maintenance priorities: P2 should be addressed in a scheduled
improvement increment; P3 is lower-impact cleanup or clarity work. High confidence
means the code pattern or reproduction is directly supported. It does not imply a
production incident, public reachability or a security vulnerability.

## Unused code and misleading surface area

The compiler diagnostic `--noUnusedLocals --noUnusedParameters` found **11 unique
TypeScript declarations** across the 11 project configurations. Repeated diagnostics
through transitive imports are counted once. The ordinary configurations still
typecheck. The exact command, project outcomes and diagnostics are retained in
[unused-declarations.json](unused-declarations.json).

| Classification | Findings | Removal boundary |
| --- | --- | --- |
| Definition-only private Python helpers | OP-01: `_mode`, two obsolete Codex key-classifier wrappers, `_strip_leading_jsonc_comments` | Remove only the four wrappers after the existing parser/privacy regressions; their underlying classifiers are used. |
| Unused local UI helpers, parameter and table entries | UI-03: `viewHeadingId`, DOM `setStatus`, graph `_records`, unused TIFF/KML source-reference entries | Search all local callers and adjust call sites together. Similar names in other modules are different bindings. |
| Compiler-confirmed imports, parameter and local values | GW-01, CR-01, EX-01, UI-03; the complete compiler register also identifies unused test declarations | A small cleanup is appropriate. Preserve the import of modules whose other bindings or side effects remain necessary. |
| Python import noise | CR-01, OP-05 and experimental candidates | Check re-export/import side effects before removal; an AST load count alone is insufficient. |
| Unconsumed return field and unreachable conditional arm | GW-01 `Inventory.totalBytes`; GW-02 JSON/SSE maximum-size ternary | Preserve the local byte-cap calculation. The SSE envelope strictly contains the JSON payload, so simplifying the comparison must preserve its size limit. |
| Public helper with no repository caller; test-only public APIs | CR-02 | `publicEvidenceDocumentSha256`, `w3cTraceId` and `ExecutionBoundary` require an API ownership/compatibility decision, not automatic deletion. |

Each item has exact definition, caller or test links in the detailed reports:
[gateway](REVIEW_GATEWAY.md), [core](REVIEW_CORE.md), [UI](REVIEW_UI.md),
[operations](REVIEW_OPERATIONS.md), [experimental](REVIEW_EXPERIMENTAL.md).
No deletion was made as part of this documentation change.

## Refactoring plan derived from the review

| Order | Cohesive change | Why this boundary | Acceptance evidence |
| --- | --- | --- | --- |
| 1 | Repair the two reproduced UI contracts and explicit schema-admission gaps in separate patches | Observable defects/gaps have smaller scope than architectural extraction | New failing regression first; existing keyboard/state/intake/metadata cases preserved |
| 2 | Remove confirmed local unused declarations/helpers; clarify stale maintained prose | Reduces noise and makes compiler unused checks useful | Typecheck, affected existing suites, consumer review; keep public compatibility and pinned schema identities |
| 3 | Extract contract-family checks from `validate_contracts.main` | OP-04: 957-line orchestration mixes fixture construction, mutations and counts | Same 102 schemas, 153 records and ten rejected selection mutations at this baseline; labelled family results |
| 4 | Extract image privacy parsing, build execution, context admission and OCI inspection | OP-02: the 6,155-line module combines unrelated responsibilities; consumers import both privacy and I/O helpers | Identical image/archive/evidence fixtures; independent derivation and provenance checks retained |
| 5 | Separate capture store primitives, projection logic and source acquisition | OP-03: the 7,873-line capture command exposes an implicit underscored API to its verifier and recovery index | Crash, quarantine, historical projection and serial/parallel verification regressions on synthetic stores |
| 6 | Split evidence checkpoint/receipt validation by semantic responsibility | CR-03/05: storage publication, recovery, versioned content and dense CAS predicates are hard to review together | Golden canonical identities, hostile mutations, crash recovery and uncertain-write outcomes unchanged |
| 7 | Extract ONS admission/payload helpers and query application stages | CR-04/GW-06: private brands and resource lifetimes span parsing, leases, execution, fallback and publication | Keep one visible orchestrator; preserve one-shot outage proof, cancellation, deadlines, key ownership and publication order |
| 8 | Consolidate pure transport/schema/build primitives and clarify browser state modules | GW-03/05, EX-02/04/05/06, UI-04/05/06 | Preserve distinct result/storage envelopes, host lifecycles, CSPs and independent display validation; characterise current error precedence first |
| 9 | Broaden shared conformance vectors and measure repeated work | CR-06, UI-07, GW-04, EX-03 | Independent implementations consume the same accepted/rejected corpus; keep root dependencies explicit; measure before claiming speedups |

The [existing IMPROVE-215 programme](../chronicle/IMPROVEMENT_PLAN.md) already
separates reliability, orchestration, evidence and runtime decomposition. These
findings refine its scope at a later source baseline. Do one responsibility per
patch, retain stable façades during extraction and preserve byte-level identity
where contracts require it. File length identifies a review hotspot; the detailed
findings explain the actual mixed responsibilities.

## Duplication and inactive code with a purpose

- Generic production activation is deliberately blocked while explicit candidate
  entrypoints mount reviewed operations. Empty defaults do not make the candidate
  or its tests dead.
- Planned registry profiles record capability lifecycle. Catalogue discovery is
  separate from execution authority.
- Receipt versions, historical qualification formats and compatibility exports
  retain explicit readers or evidence roles. A newer schema is not proof that an
  older schema can be deleted.
- Producer and independent image derivation/verification remain separate assurance
  boundaries. Sharing one high-level acceptance implementation would weaken the
  comparison.
- TypeScript/Python request validation and browser/server display/receipt validation
  protect different boundaries. The page validates the visible subset; it does not
  independently establish the omitted ledger chain or external attestation.
- Test-only fault/capacity seams are deliberate. CLI entrypoints may have no normal
  import caller. Static exported-symbol searches alone cannot establish removability.
- Imported metadata records, locked captures, vendor files and immutable research
  are data or evidence, not unused executable code.

## Review coverage and method

The complete baseline tree has **32,138 tracked files**. The reproducible
[source register](SOURCE_REGISTER.md) lists **484 code, presentation, migration,
launcher and CI files**, totalling **204,809 lines**: **479 project-authored files**
and **five pinned vendor files**. The authored subset has 202,937 lines; vendor
coverage traces a dependency boundary rather than proposing local rewrites. Imported metadata dominates
the tracked count: 30,833 OKF+ records were inventoried as data, not individually
audited for semantic truth or rights. Root configuration, schemas, profile manifests
and documentation were traced as architectural inputs alongside the source review.

| Area | Scope and depth | Detailed evidence |
| --- | --- | --- |
| Core gateway | All 34 core source modules read; all core tests inventoried; 294 exported names searched across consumers; targeted test and state-transition tracing | [Gateway review](REVIEW_GATEWAY.md) and [architecture](GATEWAY.md) |
| Core packages and Python execution | Every source inventoried and reference-reviewed; direct boundary/state-machine reading of authority, policy, adapters, receipt/store/checkpoint and geometry/HTTP; large helper sections targeted | [Core review](REVIEW_CORE.md) and per-file depth in [architecture](CORE_AND_EVIDENCE.md) |
| Interfaces and intake | All 110 tracked files in the three frontends and intake package read, including source, tests, build policy, styles, examples and configuration | [UI review](REVIEW_UI.md) and [architecture](USER_INTERFACES.md) |
| Build and operations | 207 owned files inventoried; 104 Python ASTs and 52 JS/TS syntax checks; deep tracing of release, privacy, storage and publication boundaries; large assurance modules received structural plus targeted reading | [Operations review](REVIEW_OPERATIONS.md) and [architecture](BUILD_AND_OPERATIONS.md) |
| Experimental and knowledge | 31 flow-reviewed implementations, nine structural implementation reviews and 27 test-contract files; profiles, captures and metadata inventory traced | [Experimental review](REVIEW_EXPERIMENTAL.md) and [architecture](EXPERIMENTAL_AND_KNOWLEDGE.md) |
| Contracts | 102 root and 13 other JSON Schemas; 469 exported TypeScript declarations (438 authored, 31 vendored); 21 non-test Python dataclasses; 116 embedded definition/registration sites; two OpenAPI projections and the pilot SQL constraints | [Contract review](REVIEW_CONTRACTS.md), [guide](CONTRACTS.md), [register](CONTRACT_REGISTER.md) |

These scopes overlap at shared boundaries and must not be added as disjoint file
counts. Structural coverage means inventory, declarations/imports, entrypoints and
reference checks. It is not an exhaustive line-by-line semantic proof. Tests were
used to establish intended contracts and gaps; tests passing do not mean that all
defects were found. External consumers and runtime reflection remain limits of
static dead-code analysis.

Six domain reviews were integrated and cross-checked. The cross-review corrected
the distinction between resolution publication and completed evidence, operator
assertions versus actually stopping a writer, the scope of legacy inline-only
receipts, and the indirect authored references from learning content to OKF+.
These corrections are reflected in the architecture rather than left as competing
descriptions.

## Verification

| Check | Observed result and limit |
| --- | --- |
| Ordinary TypeScript typecheck | All 11 application/package configurations passed `tsc --project … --noEmit`. |
| Unused declarations diagnostic | 11 distinct findings with stricter optional compiler flags; [exact results](unused-declarations.json). This is not a regression in the normal configuration. |
| Python structural review | All 148 maintained Python files parsed successfully; 3,094 function definitions inventoried. |
| Runtime edit equivalence | All 24 changed implementation files contain comment-only changes. Modified Python ASTs equal the baseline; added/removed JS/TS lines are comments. |
| Contract inventory | Deterministic generator `--check` passed; documented valid/invalid examples were evaluated with JSON Schema Draft 2020-12. |
| Existing contract validation | 102 schemas and 153 records validated; ten forbidden selection mutations rejected; counts and unique IDs checked in three evaluation manifests. |
| Browser/intake focused tests | 47 Vitest tests passed; intake build and both Node test files passed. Reproductions use actual source in jsdom, not a fresh real-browser acceptance claim. |
| Metadata tests | 178 unique OKF+ tests passed, including the 97-test contract subset. No full-corpus semantic revalidation is implied. |
| Experimental tests | 18 experience/native-mount tests, 60 tests against existing compiled experimental modules and 12 selected Sites evaluator tests passed. Compiled-module checks supplement the source-equivalence/type checks. |
| Sites evaluator limitation | Three protocol cases remain unverified: the harness's Python subprocess reports `EPERM` in this sandbox. Bounded full-suite attempts timed out; the partial passing suite did not weaken those assertions. |
| Canonical CI and remote publication | Not run/published for this change. The GitHub API request returned `Forbidden`; a remote pull request and required canonical CI remain separate hand-off steps. |

The source-reference, Mermaid, local-link/research-integrity and whitespace checks
are recorded in [the final verification record](VERIFICATION.md). Validation is
proportionate to documentation, generators and comments; no live provider, hosting,
private evidence acquisition or full image rebuild was needed. Existing release
and independent-assurance requirements remain applicable to a future integration.

## How to keep the documentation current

1. Keep this review baseline immutable; do not retarget its line links to `main`.
2. When recording a new review, regenerate inventories from an identified commit,
   re-check producer/consumer claims and record the new scope and test results.
3. Update the relevant architecture diagram and invariant when a responsibility or
   protocol changes. A diagram edge is a claim that needs an implementation link.
4. Keep the beginner explanation readable; put exhaustive declarations and machine
   evidence in the registers.
5. Treat refactoring acceptance as behavioural and identity preservation, not fewer
   lines or fewer modules alone.
