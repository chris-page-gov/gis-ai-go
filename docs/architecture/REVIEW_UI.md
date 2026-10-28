# Browser and intake review

Baseline: `97bc45635a91064cd78f06bf0848ad7636f05439`.
Follow-up: UI-01 and UI-02 are addressed in [the Explorer repair record](../implementation/EXPLORER_UI_REPAIRS.md).
This report retains the original findings and immutable references.

Scope: every tracked file in `apps/public-explorer`, `apps/webmcp-explorer`, `apps/public-data-workbench`, `packages/experience-intake` (110 files; exact inventory below). Runtime sources, tests/fixtures, schemas, HTML/CSS/SVG, manifests, configuration, build scripts and component READMEs were read. Untracked generated build trees, downloaded dependencies and browser reports are excluded from the source review. No tracked file in the assigned scope was excluded. No live provider, public-deployment or real AI-host claim is established by this review.

## Findings

### UI-01 — P2: restore focus to focusable navigation targets

Confirmed defect; high confidence. [focusAfterRender](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/main.ts#L105-L115) invokes `.focus()` on IDs passed by [record navigation](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/main.ts#L159-L175) and [view navigation](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/main.ts#L325-L359). After [root.replaceChildren](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/main.ts#L519-L534), the destination headings in [graph](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/views/graph.ts#L182-L194), [cards](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/views/cards.ts#L288-L303), timeline/map and About have no tabindex. About sets tabindex on the section but focuses its heading. Keyboard users lose focus to the document body after navigation and may restart traversal at the page top.

Reproduced with the actual source graph renderer loaded through Vite SSR into jsdom: `{"case":"Actual graph renderer focus","target":"view-heading-graph","tabindexAttribute":null,"activeElement":"BODY"}`. This is a DOM-level reproduction, not a new real-browser observation. The existing [keyboard journey](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/browser/journeys.spec.ts#L293-L310) asserts skip-link focus but only visibility/aria-current after view navigation.

Proposed change: one focus-target helper setting `tabIndex=-1` for destination headings (or target an existing focusable region), including record, view and About targets. Validation: Playwright keyboard activation of every view, record/back and About must assert `document.activeElement`; test history restoration without losing preserved scroll. Preserve modified-click/native link behaviour. No fix applied in this documentation task.

### UI-02 — P3: make URL query length units consistent

Confirmed contract inconsistency; high confidence. [normaliseQuery](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/state.ts#L23-L32) limits code points while [parseExplorerUrl](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/state.ts#L135-L150) checks UTF-16 `.length`. A valid caller-created state with 101 supplementary-plane letters survives canonicalise/serialise then returns an empty query when parsed: `{"case":"Unicode query roundtrip","canonicalCodePoints":101,"canonicalUtf16Units":202,"parsedQuery":""}`. This contradicts the round-trip property exercised only for ASCII in [state tests](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/unit/state.test.ts#L61-L82).

Impact is bounded: the current manual input also sets HTML maxlength 200 (UTF-16), so the reproduction concerns programmatically supplied state/serialized links and inconsistent contracts, not an assertion that normal typing already reaches this exact case. Proposed change: document one character unit and apply it across normalisation, parsing and input bounds, preserving intentional rejection instead of silent truncation for invalid URLs. Validation: supplementary-plane letters, combining forms and NFKC expansion around the limit, plus `parse(serialise(state)) === canonicalise(state)` for admitted states. No fix applied.

### UI-03 — P3: remove confirmed unused local helpers and arguments

Dead-code candidates; high confidence within the checked repository. Repository-wide `rg` across runtime, tests and build scripts found no consumers of [viewHeadingId](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/dom.ts#L136-L138) or the DOM module's [setStatus](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/dom.ts#L156-L158). The similarly named React setter in the private pilot is a different binding. [renderGraphView's `_records`](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/views/graph.ts#L182-L185) is never read; its only callers are public main and graph component tests. [SOURCES.tiff/kml](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/experience-intake/src/index.ts#L13-L21) are never used by the static format-description table. `JsonValue` in cards and `PageToolInputError` in the catalogue-tools test are also unused imports.

Proposed change: delete the unused local helpers/entries/imports and remove `_records` from the function/call sites in a small cleanup. Validate typecheck plus graph/component/intake tests. Do not classify the compatibility re-exports, test fixtures or test-used `explorerStatesEqual` as dead. No deletion applied.

### UI-04 — P3: extract readable hosted evidence display checks

Refactoring recommendation; high confidence in maintainability risk, no additional defect claimed. [hostedEvidence](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/src/controller.ts#L49-L91) mixes schema closure, series/receipt identities, event/head ordering, duplicated receipt equality and literal limitations in one long Boolean expression. It is hard to review which clause protects which claim; changing the controller risks broadening a display boundary unintentionally.

Proposed change: move pure display checks to an internal module with named predicates/checks for result identity, receipt-record binding, event/head consistency and limitation literals. Retain construction-time mode and the explicit statement that the page does not independently verify cryptographic content or the omitted chain. Validate with the existing [hosted mutation/substitution matrix](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/test/controller.test.ts#L114-L220); compare accepted/rejected fixtures before and after extraction. No refactor applied.

### UI-05 — P3: separate browser orchestration by responsibility

Refactoring recommendation; high confidence. [public main](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/main.ts#L96-L175) owns URL/history, focus/scroll, global state, rendering and loading; the [learning page](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/src/experience.ts#L7-L173) combines catalogue types/rendering, page registration, file reading, archive aggregation, cancellation and downloads in dense multi-statement lines. Four public views also repeat the same navigation interface and modified-click guard.

Proposed change: internal modules for navigation/focus, learning catalogue presentation and intake orchestration, with ordinary formatting and a shared record-navigation callback contract. Preserve the deliberate manual/tool shared action paths and generation checks. Add a declared workspace intake dependency before replacing the current relative source import. Validation: existing URL/history/browser tests, learning tools tests, folder cancellation tests and offline learning journeys; specifically test clear/new selection while file reads complete late. No refactor applied.

### UI-06 — P3: consolidate build primitives without merging build policies

Refactoring recommendation; high confidence. Static [build-boundary](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/scripts/build-boundary.mjs#L12-L119), [prepare-data](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/scripts/prepare-data.mjs#L22-L97), [check-dist](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/scripts/check-dist.mjs#L24-L88) and WebMCP [build-boundary](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/scripts/build-boundary.mjs#L8-L133) repeat path, regular-tree and checksum parsing logic. Variants already differ in validation details, so future repairs must find every copy.

Proposed change: a Node-only internal utility for bounded relative paths, no-symlink inventory and checksum rows; retain separate generated markers, public inventories and CSP/HTML policies. Do not import Node build helpers into browser runtime. Validation: both build-boundary suites, dist-policy suite, full Explorer builds and exact output inventories. No extraction applied.

### UI-07 — P3: make copied strict-JSON maintenance explicit

Refactoring recommendation; high confidence. [Intake strict JSON](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/experience-intake/src/strict-json.ts#L1-L155) is an intentional local copy of the provider parser. It is live through GeoJSON previews, not dead code. Isolation avoids adding provider/network capability to the browser, but duplicate-key/numeric/surrogate/depth repairs can diverge.

Proposed change: first share a neutral conformance corpus with both implementations; only extract a dependency-free pure parser package if ownership/dependency costs justify it. Preserve distinct limits/error messages where intentional. Validate the same duplicate-key, escaped-key, surrogate, unsafe-number and nesting cases in both packages. No extraction applied.

## Deliverables and validation

- `docs/architecture/USER_INTERFACES.md`: 4 Mermaid diagrams, formal state/controller/intake contracts, beginner contract table, manual/WebMCP/build/lifecycle/accessibility boundaries; 78 immutable line references verified against baseline `git show` across 55 files.
- Comment-only source edits: `apps/public-explorer/src/state.ts`, `apps/webmcp-explorer/src/webmcp-adapter.ts`, `apps/public-data-workbench/src/controller.ts`, `apps/public-data-workbench/src/experience.ts`, `packages/experience-intake/src/zip.ts` (10 lines added).
- `git diff --check` passed for owned files.
- Existing Vitest suites: static state+graph **8 passed**; WebMCP adapter **3 passed**; workbench controller+learning tools+folder drop **36 passed**. Total **47 passed**.
- Intake native `tsc` build passed; `node --test dist/test/*.test.js` reported both test files passing (the files define 19 test cases; this runner output summarised 2 file-level tests, so do not assert a newly observed 19-case count).
- Pinned Corepack pnpm initially could not download the absent 10.33.2 tarball because the sandbox network connection returned EPERM. Safe fallback used the already installed pinned Vitest 4.1.11 and native TypeScript binaries directly, without dependency changes. This is not an automatic approval-review rejection. No browser port/host/deployment test was run.
- Clean reproduction used Vite SSR with `server:{middlewareMode:true,hmr:false,ws:false}`, `configFile:false`, loading actual source state and graph modules plus the existing valid catalogue fixture into jsdom. It canonicalised/serialised/parsed `'𐐀'.repeat(101)` and rendered the real graph, replaced a focused link, then focused `view-heading-graph`. Outputs are recorded under UI-01/UI-02. Early harness attempts were corrected (HMR bind EPERM; missing jsdom `Node` global); final reproduction completed with the outputs above.

## Exact reviewed file inventory

- `apps/public-data-workbench/.gitignore`
- `apps/public-data-workbench/README.md`
- `apps/public-data-workbench/experience.html`
- `apps/public-data-workbench/index.html`
- `apps/public-data-workbench/package.json`
- `apps/public-data-workbench/src/controller.ts`
- `apps/public-data-workbench/src/discovery.ts`
- `apps/public-data-workbench/src/experience-drop.ts`
- `apps/public-data-workbench/src/experience-tools.ts`
- `apps/public-data-workbench/src/experience.css`
- `apps/public-data-workbench/src/experience.ts`
- `apps/public-data-workbench/src/main.ts`
- `apps/public-data-workbench/src/mcp-client.ts`
- `apps/public-data-workbench/src/styles.css`
- `apps/public-data-workbench/src/webmcp.ts`
- `apps/public-data-workbench/test/controller.test.ts`
- `apps/public-data-workbench/test/experience-drop.test.ts`
- `apps/public-data-workbench/test/experience-tools.test.ts`
- `apps/public-data-workbench/test/mcp-client.test.ts`
- `apps/public-data-workbench/tsconfig.json`
- `apps/public-data-workbench/vite.config.ts`
- `apps/public-data-workbench/vitest.config.ts`
- `apps/public-explorer/README.md`
- `apps/public-explorer/index.html`
- `apps/public-explorer/package.json`
- `apps/public-explorer/playwright.config.ts`
- `apps/public-explorer/playwright.public.config.ts`
- `apps/public-explorer/public/favicon.svg`
- `apps/public-explorer/scripts/build-boundary.mjs`
- `apps/public-explorer/scripts/check-build-boundary.mjs`
- `apps/public-explorer/scripts/check-dist.mjs`
- `apps/public-explorer/scripts/dist-policy.mjs`
- `apps/public-explorer/scripts/prepare-data.mjs`
- `apps/public-explorer/src/catalogue.ts`
- `apps/public-explorer/src/dom.ts`
- `apps/public-explorer/src/links.ts`
- `apps/public-explorer/src/main.ts`
- `apps/public-explorer/src/state.ts`
- `apps/public-explorer/src/styles.css`
- `apps/public-explorer/src/types.ts`
- `apps/public-explorer/src/views/cards.ts`
- `apps/public-explorer/src/views/graph.ts`
- `apps/public-explorer/src/views/map.ts`
- `apps/public-explorer/src/views/timeline.ts`
- `apps/public-explorer/test/browser/accessibility.spec.ts`
- `apps/public-explorer/test/browser/downloads.spec.ts`
- `apps/public-explorer/test/browser/journeys.spec.ts`
- `apps/public-explorer/test/browser/public-deployment.spec.ts`
- `apps/public-explorer/test/browser/reviewed-examples.spec.ts`
- `apps/public-explorer/test/browser/security.spec.ts`
- `apps/public-explorer/test/build/build-boundary.test.mjs`
- `apps/public-explorer/test/build/dist-policy.test.mjs`
- `apps/public-explorer/test/component/cards.test.ts`
- `apps/public-explorer/test/component/fixtures.ts`
- `apps/public-explorer/test/component/graph.test.ts`
- `apps/public-explorer/test/component/map.test.ts`
- `apps/public-explorer/test/component/timeline.test.ts`
- `apps/public-explorer/test/fixtures/assurance.ts`
- `apps/public-explorer/test/fixtures/network.ts`
- `apps/public-explorer/test/fixtures/publication.ts`
- `apps/public-explorer/test/unit/catalogue.test.ts`
- `apps/public-explorer/test/unit/fixtures.ts`
- `apps/public-explorer/test/unit/links.test.ts`
- `apps/public-explorer/test/unit/network.test.ts`
- `apps/public-explorer/test/unit/publication.test.ts`
- `apps/public-explorer/test/unit/state.test.ts`
- `apps/public-explorer/tsconfig.json`
- `apps/public-explorer/vite.config.ts`
- `apps/public-explorer/vitest.config.ts`
- `apps/webmcp-explorer/README.md`
- `apps/webmcp-explorer/index.html`
- `apps/webmcp-explorer/package.json`
- `apps/webmcp-explorer/playwright.config.ts`
- `apps/webmcp-explorer/public/favicon.svg`
- `apps/webmcp-explorer/scripts/build-boundary.mjs`
- `apps/webmcp-explorer/scripts/check-dist.mjs`
- `apps/webmcp-explorer/scripts/chrome-preflight.mjs`
- `apps/webmcp-explorer/scripts/html-boundary.mjs`
- `apps/webmcp-explorer/scripts/prepare-data.mjs`
- `apps/webmcp-explorer/src/catalogue-tools.ts`
- `apps/webmcp-explorer/src/dom.ts`
- `apps/webmcp-explorer/src/main.ts`
- `apps/webmcp-explorer/src/styles.css`
- `apps/webmcp-explorer/src/webmcp-adapter.ts`
- `apps/webmcp-explorer/test/browser/accessibility.spec.ts`
- `apps/webmcp-explorer/test/browser/journeys.spec.ts`
- `apps/webmcp-explorer/test/browser/security.spec.ts`
- `apps/webmcp-explorer/test/build/build-boundary.test.mjs`
- `apps/webmcp-explorer/test/build/chrome-preflight.test.mjs`
- `apps/webmcp-explorer/test/unit/catalogue-tools.test.ts`
- `apps/webmcp-explorer/test/unit/fixture.ts`
- `apps/webmcp-explorer/test/unit/webmcp-adapter.test.ts`
- `apps/webmcp-explorer/tsconfig.json`
- `apps/webmcp-explorer/vite.config.ts`
- `apps/webmcp-explorer/vitest.config.ts`
- `packages/experience-intake/README.md`
- `packages/experience-intake/examples/journey-counts.csv`
- `packages/experience-intake/examples/meeting-places.geojson`
- `packages/experience-intake/examples/source-note.txt`
- `packages/experience-intake/package.json`
- `packages/experience-intake/schema/request.v1.schema.json`
- `packages/experience-intake/schema/result.v1.schema.json`
- `packages/experience-intake/src/index.ts`
- `packages/experience-intake/src/previews.ts`
- `packages/experience-intake/src/strict-json.ts`
- `packages/experience-intake/src/types.ts`
- `packages/experience-intake/src/zip.ts`
- `packages/experience-intake/test/intake.test.ts`
- `packages/experience-intake/test/zip.test.ts`
- `packages/experience-intake/tsconfig.json`

## Reproduction commands

Run `node docs/architecture/examples/reproduce-ui.mjs` from the repository root.
The [retained reproduction](examples/reproduce-ui.mjs) loads the actual source and
installed app dependencies without opening a browser listener or calling a provider.
It prints the two observations described above. Later behavioural fixes may change
these baseline observations; this demonstration is separate from the future
regression tests recommended for those fixes.

Focused checks executed directly after Corepack could not download its pinned pnpm:

```sh
# cwd: apps/public-explorer
node node_modules/vitest/vitest.mjs run test/unit/state.test.ts test/component/graph.test.ts
# cwd: apps/webmcp-explorer
node node_modules/vitest/vitest.mjs run test/unit/webmcp-adapter.test.ts
# cwd: apps/public-data-workbench
node node_modules/vitest/vitest.mjs run test/controller.test.ts test/experience-tools.test.ts test/experience-drop.test.ts
# cwd: packages/experience-intake
../../node_modules/.bin/tsc --project tsconfig.json && node --test dist/test/*.test.js
```
