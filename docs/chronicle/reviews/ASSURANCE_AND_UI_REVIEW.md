# Assurance, tooling and interface review

Reviewed on 14 September 2026 against
`6c76c92a18da779766f8d49acbbd7dbbd31abb97`.

This is the assurance and interface contribution to the whole-programme code
review. It assesses checked-in source and tests. It does not claim a new live
browser observation, penetration test, complete line-by-line audit of every
script, or fresh execution of the full assurance gate. Runtime and provider review
are covered separately in this chronicle. Findings below distinguish observed
defects, maintainability risks and proposed improvements.

## Assessment

The implementation gives unusually concrete expression to its governance model.
The same catalogue semantics support manual interaction and page tools; inputs
are checked at execution time; build artefacts have explicit inventories; private
evidence has a separate verification path; and release publication consumes
identified, verified artefacts. These are useful qualities to teach and retain.

The principal weakness in the reviewed scope is the accumulated cost of operating
the assurance machinery. Large scripts combine multiple responsibilities, several
commands rebuild the same dependencies, and the impact planner does not yet change
which CI jobs run. This is evidence of maintainability and efficiency debt. It
does not establish how many hours or tokens that debt consumed; that attribution
needs the separate attempt and timing ledger.

Two actionable assurance gaps were found: WebMCP browser failure artefacts are
omitted from the repository CI upload, and the baseline secret scanner recognises
fewer credential formats than the private evidence scanner. Several short
guidance files also retain Stage 0 statements after later capabilities were
accepted. These findings should be visible in the narrative alongside the stronger
parts of the implementation.

## Review coverage

The review inventoried maintained scripts, contract tests, interoperability
fixtures, both Explorer applications and the two checked-in Actions workflows.
It traced the package-command graph and inspected these representative paths in
detail:

- CI impact planning, repository/image assurance, independent image derivation,
  provenance and Pages publication;
- catalogue validation, WebMCP registration and disposal, manual rendering,
  navigation state, build inventories and malicious-input/browser tests;
- preservation module boundaries, streamed projection verification, schema
  validation, secret scanning and representative contract mutation tests; and
- component, security, policy, interoperability and accessibility instructions.

The accompanying [source inventory](ASSURANCE_SOURCE_INVENTORY.json) identifies
every maintained source file in this scope, its reviewed-baseline digest, line
count and review depth. It also inventories executable tests separately. A
`complete-source-read` means the source was read, not that every behaviour was
proved. A `targeted-source-review` identifies the inspected ranges and leaves the
remaining helper bodies explicitly open. `structural-only` is not substantive
code-review completion. Test inventories are primarily structural, with detailed
mutation and browser examples inspected separately.

The inventory contains 110 maintained source/build-control files: 70 complete
source reads and 40 targeted source reviews. It separately lists 87 executable
test and fixture files: 85 structural entries and two completely read synthetic
fixtures. These are review-depth counts, not quality scores or executed-test
counts. The report's selected test examples do not upgrade the depth of an entire
large test file.

The extension pass traced the entrypoints and acceptance flow of every maintained
assurance-script family, including exact-five host observation, generated-runtime
closure, non-synthetic deployment admission and descriptor-pinned Pages staging.
All Explorer application modules, styles and local build helpers were read.
Large preservation, privacy, image and host-observation modules retain explicitly
listed helper-level gaps: this is comprehensive source inventory plus scoped
source review, not a completed line-by-line audit of those remaining bodies.
Their deeper decomposition review is an explicit follow-on activity. The
checked-in workflows do not contain a CodeQL
workflow; repository-hosted CodeQL configuration and historical runs must be
captured separately before making claims about their current configuration.

No full test suite, live provider, AI client or cloud deployment was run for this
review. One small, offline probe exercised the baseline scanner's existing
regular expressions with fabricated credential-shaped strings; it emitted only
the matched category names.

## Findings and opportunities

### AUI-01 — WebMCP browser failure evidence is not uploaded

**Observed defect; medium priority for diagnosis and preservation.**

Both browser configurations save screenshots and Playwright traces when tests
fail. The WebMCP configuration writes them to its own `test-results` directory.
The CI upload names only `apps/public-explorer/test-results/`, alongside the root
`artifacts/` tree. WebMCP failure traces therefore have no corresponding upload
entry and disappear with the runner unless another mechanism captures them.

Sources: [CI evidence upload](../../../.github/workflows/ci.yml#L192),
[WebMCP browser artefacts](../../../apps/webmcp-explorer/playwright.config.ts#L6).

**Proposed change:** include the WebMCP failure directory in the existing
always-run evidence upload. Keep ordinary successful runs free of unnecessary
video or trace capture. Verify the resolved upload inventory with a synthetic
failure artefact in each application, and confirm the workflow contract rejects
omission of either path.

### AUI-02 — The impact planner remains advisory

**Confirmed optimisation opportunity; no check has been silently skipped.**

The impact map and emitted plan explicitly use shadow mode. CI says that every
current assurance job still runs. Neither repository assurance nor gateway image
assurance is conditional on the planner's output. Consequently a documentation
change still invokes `pnpm run check` and the complete image job. The planner
currently provides evidence for an optimisation; it has not delivered the runtime
saving itself.

Sources: [shadow plan](../../../scripts/plan_ci_impact.py#L407),
[workflow statement](../../../.github/workflows/ci.yml#L72),
[unconditional repository assurance](../../../.github/workflows/ci.yml#L92),
[unconditional image assurance](../../../.github/workflows/ci.yml#L203),
[impact map](../../../.github/ci/verification-impact-map.v2.json).

**Proposed change:** first measure representative recent plans against actual
jobs and build-context changes. Then admit a narrow documentation-only PR lane
from a trusted planner and map, with unknown paths, deleted or renamed inputs,
planner changes and toolchain changes falling back to full assurance. A plan
computed by changed PR code must not independently grant itself permission to
skip checks. Retain the required aggregate gate, and keep protected-main and
release assurance complete until a separately reviewed policy says otherwise.

**Verification:** replay representative historical changes; mutate the planner
and map; rename a build input into a documentation path; remove a mapped file;
and introduce an unknown path. Every affected lane must run. Measure median and
95th-percentile PR waiting time and runner minutes before and after; the target
is fewer unrelated jobs with zero missed affected lanes in the evaluation set.

### AUI-03 — Build orchestration repeats ordinary preparation

**Confirmed optimisation opportunity; distinguish it from reproducibility work.**

`test:typescript` executes packages in sequence, each with its own preparation
chain. The gateway test prepares its dependencies and builds the gateway;
`test:interoperability` then prepares and builds them again. Browser assurance
builds both Explorers, whose builds each build contracts. Later release
reproducibility deliberately performs two clean Explorer builds. Image assurance
also deliberately builds a repeat image, while protected-main CI uses an
additional independent builder.

Sources: [root command graph](../../../package.json#L13),
[gateway preparation](../../../apps/mcp-gateway/package.json#L14),
[Explorer build](../../../apps/public-explorer/package.json#L15),
[two clean Explorer builds](../../../scripts/check_release_reproducibility.py#L356),
[image repeat](../../../scripts/check_gateway_image_reproducibility.py#L34),
[independent image job](../../../.github/workflows/ci.yml#L355).

**Proposed change:** introduce one orchestrator that builds the dependency graph
once for ordinary tests, then executes explicit test-only commands. Preserve
standalone commands that prepare their own dependencies for developer convenience.
Do not reuse one build as both sides of a reproducibility comparison, or remove
the independent builder merely because its output matches.

**Verification:** compare the complete set of executed tests and their outcomes;
record compiler/build invocation counts, elapsed time and output digests. Preserve
clean-build and independent-build evidence as separate named phases. A successful
first implementation should eliminate repeated ordinary compilation in one
`check` invocation without changing any executable test inventory.

### AUI-04 — Assurance code has outgrown individual script modules

**Maintainability risk; staged decomposition recommended.**

At the reviewed commit, `capture_delivery_evidence.py` has 7,765 lines,
`verify_delivery_evidence.py` 4,321, `gateway_image.py` 5,764, and the preservation
contract test module 9,116. Line counts are navigation indicators, not defects or
quality scores. The substantive issue is responsibility concentration:
preservation capture combines filesystem admission, archive inspection, secret
handling, journal/object storage, Codex lineage projection, GitHub acquisition and
command-line orchestration. Its verifier imports many private capture helpers.
The image helper combines pinned material identity, privacy checks, build-context
policy, OCI inspection and runtime composition.

Sources: [capture domains](../../../scripts/capture_delivery_evidence.py),
[verifier imports](../../../scripts/verify_delivery_evidence.py#L28),
[image construction and verification](../../../scripts/gateway_image.py).

**Proposed change:** extract a small internal library by responsibility, retaining
the existing CLI entrypoints and output bytes. Suitable modules are filesystem
admission; canonical formats; redaction primitives; immutable object/journal I/O;
Codex projection; GitHub acquisition; and verifier-only semantics. Apply the same
approach to image material identity, OCI inspection and build orchestration.

Shared low-level encoders or validators are useful, but verification must still
recompute the claims that the producer makes. Avoid one shared high-level
function becoming both producer and acceptance oracle. Split tests by invariant
and keep a few explicit integration tests over the complete CLI journey.

**Verification:** replay frozen synthetic fixtures through old and new versions;
require byte-identical accepted outputs and the same rejected mutations. For
preservation, verify all current supported schemas and retain legacy failure
classifications. Measure peak memory, bytes read and elapsed time on the same
admitted store before proposing any faster verification mode.

### AUI-05 — Baseline public secret scanning has known coverage gaps

**Observed assurance limitation; strengthen before publishing a rich chronicle.**

The baseline scanner recognises classic GitHub tokens, OpenAI-style keys, AWS
access keys, Slack tokens, private keys, selected assignments and machine paths.
It excludes generated artefacts and image formats and skips non-UTF-8 files. An
offline probe found no match for fabricated fine-grained GitHub-token or Google
API-key shapes, while a fabricated classic GitHub-token shape matched. This
demonstrates a signature gap, not the presence of a real secret in the repository.
The preservation verifier already lists a broader set of categories.

Sources: [baseline signatures and exclusions](../../../scripts/scan_secrets.py#L10),
[preservation categories](../../../scripts/verify_delivery_evidence.py#L87).

**Proposed change:** give publication a bounded, tested allowlist of files and
credential-signature coverage appropriate to the material being published. Add
missing signatures to the baseline using synthetic positive and negative cases;
apply separate text extraction and visual review to PDFs and screenshots. A
pattern scan cannot establish that all personal or confidential information has
been removed. Keep private source evidence and public approved projections
separate throughout the chronicle build.

**Verification:** retain expected category matches for synthetic examples, test
false-positive controls, verify generated publication files are included, and
confirm failure messages do not print matched credentials. Record which binary
or visual formats require an explicit review.

### AUI-06 — Browser support evidence must remain distinct from mock coverage

**Existing design strength with an explicit evidence limit.**

The WebMCP tests inject a mock `document.modelContext`, exercise both callbacks,
check absent browser storage and external requests, and test malicious fields.
Accessibility tests deliberately remove the API and exercise the manual fallback.
These establish application behaviour and graceful fallback. They cannot prove
that a current AI host discovers tools or that a later browser version implements
the same API. The checked-in browser configurations use runner Chrome, not a
Chrome/Edge/Firefox/WebKit matrix.

Sources: [mock registration and privacy checks](../../../apps/webmcp-explorer/test/browser/security.spec.ts#L11),
[fallback accessibility tests](../../../apps/webmcp-explorer/test/browser/accessibility.spec.ts#L22),
[registration lifecycle](../../../apps/webmcp-explorer/src/webmcp-adapter.ts#L186),
[browser configuration](../../../apps/webmcp-explorer/playwright.config.ts#L16).

**Recommendation:** retain the small deterministic browser suite for normal
changes. Refresh real host observations when the relevant browser, host, model,
protocol or adapter changes. Each compatibility claim should cite its observed
versions, source commit, date and actual call evidence. Automated accessibility
checks also need manual screen-reader and reading-order review for the final
published learning path.

### AUI-07 — Public Explorer rendering is a future scaling seam

**Bounded optimisation opportunity; no present performance failure established.**

The public Explorer cleanly separates catalogue functions, URL state and four
views. Its 625-line main module still owns history, controls and rendering. Every
render searches records, derives facets, finds the selected record and replaces
the whole root. The validated catalogue is small enough that this may be the
most understandable design today; no latency measurements were collected here.

Sources: [main render](../../../apps/public-explorer/src/main.ts#L484),
[navigation state](../../../apps/public-explorer/src/state.ts),
[view modules](../../../apps/public-explorer/src/views/cards.ts).

**Proposed change if measurements justify it:** extract controller/history code
and memoise catalogue-derived indexes by immutable catalogue revision. Avoid a
framework migration purely to reduce line count. Verify back/forward behaviour,
focus restoration, URL canonicalisation, empty results and malformed record
links, as well as response time on an explicitly sized synthetic catalogue.

### AUI-08 — Guidance has not consistently advanced with the implementation

**Observed documentation drift at the reviewed baseline.**

The accessibility and policy test READMEs still describe Stage 0. The
interoperability README retains preparation-only descriptions for work whose
accepted outcomes are recorded elsewhere. Component development instructions can
also cause repeated work: the public Explorer's “focused” browser command runs
both Explorers, and the WebMCP example builds before invoking a command that builds
again.

Sources: [accessibility boundary](../../../tests/accessibility/README.md),
[policy-test boundary](../../../tests/policy/README.md),
[policy boundary](../../../policies/README.md),
[interoperability guide](../../../tests/interoperability/README.md),
[public Explorer guide](../../../apps/public-explorer/README.md),
[WebMCP guide](../../../apps/webmcp-explorer/README.md).

The companion guidance update in this work package corrects the four scoped
guides: the policy-test README now links the accepted compiled policy suite;
the interoperability README distinguishes the generic, fixed-container and
provider-free entrypoints and links the accepted ChatGPT observation; the public
Explorer uses a filtered browser command; and the WebMCP sequence no longer
invokes a second application build. The root guidance pass also reconciles the
accessibility and policy boundary guides. These are documentation changes only;
the reviewed baseline remains the historical evidence.
Future acceptance should update one canonical capability record and give short
component guides stable links to it; historical observations should retain their
dates and original boundaries.

### AUI-09 — The baseline scanner filters after directory traversal

**Confirmed implementation-level optimisation opportunity.**

`scan_secrets.py` uses `ROOT.rglob("*")` and only then filters out `node_modules`,
`.uv-cache`, `.git` and other excluded path parts. The exclusion prevents reading
those files as text, but it does not prune their directory trees from enumeration;
`path.is_file()` is also evaluated before the exclusion check. Large dependency
or artefact trees therefore add traversal and metadata work to every baseline
scan, even though their contents are intentionally outside its scan scope.

Source: [scanner traversal](../../../scripts/scan_secrets.py#L40).

**Proposed change:** enumerate the intended scan inventory directly, or prune
excluded directory names before descent with a top-down walk. Preserve the
explicit publication scan inventory proposed in AUI-05. Verify identical included
file sets, a bounded synthetic excluded subtree, and no change to credential
classification. Measure visited directory entries and elapsed time before claiming
a speed improvement.

### AUI-10 — Some local child commands lack a deadline

**Observed reliability and unattended-operation gap; not evidence of a past hang.**

The execution-container check's `subprocess.run` wrapper supplies no timeout.
The local-evaluation receipt generator limits captured output but both selected
test subprocess paths omit a timeout. The recovery rehearsal's general child
command helper also omits one. CI job timeouts bound a workflow overall, but do
not give a directly invoked local command a deadline or a useful phase-specific
timeout classification. A stalled child can therefore keep those local callers
waiting without a caller-enforced deadline.

Sources: [execution-container command](../../../scripts/check_execution_container.py#L58),
[selected local tests](../../../scripts/qual_206_local_evaluations.mjs#L568),
[recovery command](../../../scripts/rehearse_evidence_checkpoint_recovery.mjs#L67).

**Proposed change:** define measured, configurable per-phase deadlines and bounded
termination for these helpers. Preserve already stronger controls in the
[Claude launcher](../../../scripts/qual_206_claude_capability_harness.mjs#L1454)
and [ChatGPT observation windows](../../../scripts/qual_206_chatgpt_tunnel_exact_five_observer.mjs#L677).
Use a synthetic never-exiting child to check timeout classification, termination
and no accepted receipt after failure. Avoid declaring a timeout solely because a
legitimate large capture exceeds a small arbitrary default.

### AUI-11 — New transcript projection is sequential and uses maximum gzip effort

**Confirmed implementation detail; potential optimisation requires measurement.**

`capture_codex_thread_closure` passes the worker count into reuse validation, then
iterates through selected records sequentially when constructing new projections.
`_gzip_projection` fixes gzip compression at level 9. It is therefore inaccurate
to describe the entire capture as parallel merely because reuse workers were
enabled. On a large first capture, projection, redaction, compression and storage
can still dominate; source reading alone does not establish which is limiting.

Sources: [reuse and fresh-projection loop](../../../scripts/capture_delivery_evidence.py#L6031),
[deterministic gzip](../../../scripts/capture_delivery_evidence.py#L5034).

**Proposed change:** first measure bytes, CPU time, read/write throughput and peak
memory separately for discovery, reuse verification, projection and compression.
Benchmark bounded fresh-projection workers against one worker on both local and
external storage. Keep single-writer journal publication, deterministic ordering,
space reserves, redaction and independent verification unchanged. Benchmark gzip
levels before changing policy; a compression-level change changes stored object
bytes and hashes even when decoded content is identical, so version its profile
and preserve verification of existing archives. Acceptance requires identical
decoded projections, no missing source events, compatible historical verification
and evidence-backed resource savings, not simply a faster-looking progress log.

### AUI-12 — Three existing dependency alerts need a recorded disposition

External scanner observation, recorded on 14 September 2026; exploitability has
not been established by this review.

GitHub reported three open medium-severity Dependabot alerts against the locked
`hono` dependency. The [lockfile](../../../pnpm-lock.yaml) pins `4.13.3`; the alert
records identify versions below `4.13.5` as affected and `4.13.5` as the first
patched version. All three alerts were created on 10 September 2026, before this
review's baseline:

| Public advisory | Reported concern |
| --- | --- |
| [GHSA-gqvv-2mrq-wpjv](https://github.com/honojs/hono/security/advisories/GHSA-gqvv-2mrq-wpjv) | `toSSG()` output-directory escape; incomplete earlier fix |
| [GHSA-crvj-82cr-hjcx](https://github.com/honojs/hono/security/advisories/GHSA-crvj-82cr-hjcx) | Query parsing after a URL fragment can differ from cache/proxy interpretation |
| [GHSA-g6gw-c38x-mqfc](https://github.com/honojs/hono/security/advisories/GHSA-g6gw-c38x-mqfc) | Unbounded dot-notation nesting in `parseBody()` can exhaust memory |

A matching dependency version is not proof that GIS AI GO exposes each affected
API to an attacker. This review does not establish the complete caller, input and
control path for any of these three claims, and does not dismiss them as harmless.
Static CodeQL success does not close dependency-advisory findings.

The separate improvement stage must record one disposition per advisory, establish
supported-path reachability and apply a tested compatible dependency update where
required. Recreate relevant SDK/HTTP, lockfile, SBOM and image evidence before a
local-edition acceptance claim. Do not silently waive the alerts or rewrite
historical accepted evidence as if it used the later dependency.

## Separate implementation stage

The following stage is a proposal, not a claim that the refactors have happened.
Sequence it after this review and the local-candidate completion decision.

1. **Preserve diagnostics and establish measurements.** Fix AUI-01, record
   per-phase wall time, test counts, build invocations, runner minutes, peak memory
   and artefact sizes. Separate active execution, CI waiting, authentication,
   offline time and retries in the retrospective. Do not infer model cost from
   elapsed time or agent count. Add AUI-10's local deadlines and record timeout
   outcomes as distinct from cancellation or a failed assertion.
2. **Remove ordinary duplicate builds.** Implement AUI-03 with a dependency-aware
   orchestrator. Retain clean reproducibility and independent derivation phases.
3. **Admit limited PR routing.** Implement AUI-02 only after historical replay and
   hostile planner/map tests. Keep full fallback and required aggregate status.
4. **Decompose assurance modules.** Address AUI-04 one responsibility and one
   source-compatible PR at a time. Preserve deterministic output bytes and
   verifier independence. Evaluate AUI-11's projection/compression changes only
   after profiling; keep their output-format implications separate from pure
   module extraction.
5. **Strengthen publication assurance.** Address AUI-05 with synthetic cases,
   approved projection inventory and screenshot/PDF review before publication.
   Apply AUI-09's directory pruning while retaining the same intended file set.
6. **Optimise UI only from measured need.** Use AUI-07's benchmark and interaction
   checks; retain the small existing component boundaries where they work well.

Set numerical latency and memory targets after collecting the baseline. The
initial non-negotiable measures are unchanged test coverage, unchanged accepted
artefact bytes for behaviour-preserving refactors, no skipped affected lane in
the evaluation set, and explicit failure rather than an unverifiable success.

## Learning-path material supported by this review

Readers should encounter each concept through a working example and then an
exercise that demonstrates its limit:

1. **Contract:** a precise agreement about accepted input and returned output.
   Inspect the WebMCP schema, submit a valid query, then add an unknown field and
   observe its executable rejection.
2. **Deterministic core and AI interpretation:** the host interprets a question;
   catalogue code validates structured arguments and calculates the answer.
   Compare the manual call and AI call over the same function.
3. **Progressive enhancement and accessibility:** the manual journey continues
   when the experimental browser API is absent. Follow the keyboard journey and
   inspect a deliberately unsupported-host result.
4. **Threat model and malicious-input test:** state what could go wrong before
   designing a control. Trace an unwanted endpoint argument from threat to
   rejection test, and explain why a passing test is narrower than a penetration
   test or security certification.
5. **Reproducibility, provenance and receipt:** show the distinction between
   identical build bytes, a statement identifying who built them, and an
   application record of a particular operation. None substitutes for the others.
6. **Independent verification and a gate:** deliberately alter one retained
   evidence field and observe refusal. Explain that failure is useful information
   and that a gate must say exactly what it establishes.
7. **Efficient assurance:** use the dependency graph to explain which checks a
   change affects. Compare useful independent repetition with repeated ordinary
   preparation, and show measured savings alongside retained coverage.
8. **Maintenance after model changes:** connect outdated guidance and accumulated
   script responsibilities to explicit review findings, measured improvements and
   new acceptance records. A more capable model changes how work can be organised;
   it does not by itself establish the correctness of existing code.

For the A4 edition, use one small diagram per concept: a four-step input contract
flow; manual and AI paths meeting at one catalogue function; source/build/receipt
evidence as separate boxes; and a dependency graph with no more than six nodes.
Render as vector graphics, provide a prose equivalent and check the final PDF at
its printed size. The existing deterministic
[diagram renderer](../../../scripts/render_diagrams.mjs) supplies a useful pattern
for source and output digests, but rendering SVG successfully does not establish
A4 readability or pagination.
