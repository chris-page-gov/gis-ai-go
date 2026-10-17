# Release closure record

Opened: 17 October 2026. Owner: Chris Page. Status: release work authorised;
acceptance and publication pending.
Tracking: [REVIEW-222, issue #151](https://github.com/chris-page-gov/gis-ai-go/issues/151).

This is the tracked checklist for taking the repaired repository to a verified
release and continuing the existing private OpenAI Sites exemplar. The source
checkpoint is [`72bc5aaf66242db219cdde5e2754a1a5e635a532`][candidate]. Source links
below are pinned to that checkpoint. Later candidate commits and observations
belong in the evidence register; a changed commit does not inherit deployment or
CI acceptance from this record.

The supported public product remains `v0.1.0`. The [roadmap's `v0.2.0` contract][roadmap]
is the exact-five public MCP gateway. The [Sites pilot][sites-adr] is a separate
six-tool Workers/D1 assembly with a private audience. Releasing or updating that
exemplar does not close the exact-five gateway gates. A proposed supported Sites
product needs a separately recorded support boundary and acceptance decision;
this checklist does not change the roadmap or weaken DEPLOY-207.

On 17 October the owner agreed to finish the **existing private Sites teaching
exemplar first**. Porting the full five-tool gateway is a separate milestone.
Continue the applicable common and Sites checks for that private scope while
keeping G01–G05 as the later supported-gateway gates. The dependency repair in
[issue #142](https://github.com/chris-page-gov/gis-ai-go/issues/142) changes the
hosted workbench's bundled client and therefore requires a rebuilt and published
Site before claiming hosted remediation; the four earlier review repairs alone
did not establish a reason to redeploy an unchanged hosted runtime.

## Four repaired review findings

These implementation repairs have local regression evidence. Their inclusion in
a supported release still depends on the final candidate's canonical assurance.
The [maintenance disposition](MAINTENANCE_DISPOSITION.md) accounts for all 34
findings: four repaired and 30 retained with explicit conditions and verification.
Completing this table does not claim that all review findings are closed.

| Finding | Implemented result | Recorded verification |
| --- | --- | --- |
| UI-01: navigation focus | Rendered navigation headings accept programmatic focus; controls, skip links and restored scroll retain their intended behaviour. | A real Chromium regression failed before repair. The completed Explorer checks passed 45 browser tests, including four automated accessibility scans, and 51 Vitest tests. [Repair and evidence][ui-repairs]. |
| UI-02: Unicode query round trips | Input, canonical state and URL admission share a 200 UTF-16-unit budget; normalisation precedes truncation, which preserves complete code points. | Four state regressions failed before repair; state and browser coverage includes supplementary characters, normalisation expansion and URL reloads. The 45/51 totals above are shared suites, not additional tests. [Repair and evidence][ui-repairs]. |
| EX-07: missing OKF+ schemas | All three schema definitions are required before records are read. Invalid or absent schemas fail the build while preserving a previous output bundle. | Eight missing-schema subcases failed before repair; all 181 affected OKF+ tests passed. Eleven generated files remained byte-identical for the same complete fixture and revision. [Repair and evidence][validation-repairs]. |
| CT-02: intake descriptor conformance | Package assurance validates both published schema definitions and representative actual planner/ZIP outputs, while retaining stricter runtime checks. | All 21 intake tests passed; the added checks cover 43 labelled cases. Four deliberate descriptor/output mutations failed for the intended reason. [Repair and evidence][validation-repairs]. |

The repair records identify the actual browser environment, dependency pins and
local execution limits. They do not establish hosted accessibility, a deployed
provider result or protected-main acceptance.

## Current evidence register

The coordinating task owns remote observations and fills the pending references
below. Private Site identifiers, endpoint origin, user identity, plugin identifier,
credentials and raw deployment records stay in the private operating record.
Public evidence may identify the kind of observation, date, source revision,
version, result and permitted digests.

| Item | Current observation | Evidence reference or next observation |
| --- | --- | --- |
| Source checkpoint | Review repairs at `72bc5aaf66242db219cdde5e2754a1a5e635a532`; newer `main` security and CI changes integrated at `0a046021`. | Final release/source commit and tree: **pending**. |
| Product metadata | `VERSION`, all 12 npm manifests and both Python manifests report `0.1.0`. Only `RELEASE_NOTES/0.1.0.md` exists; material fragments are unconsumed. | Proposed release version, consolidated changelog and release notes: **pending**. |
| Native Sites readback | Native `get_site` and version-history readback on 17 October 2026 confirms version **8** active, custom private audience with one user and no groups/editors, native endpoint path **`/mcp`**, and a provisioned plugin identifier. | Site source `757ba5f98fec83c0d09ec19e88a829f8da38f040`, matching the [version-8 acceptance comment][version-eight]. Native records remain private. |
| Native authentication and client use | Native declaration and provisioned connection metadata are now reported. OAuth, installed-client access and an authenticated native tool call are **not yet established** by that readback. | Exact client/version, authentication mode, capability call and receipt observations: **pending**. |
| Existing hosted evidence | The [version-7 record][hosted-history] retains its bounded provider and operation observations. The subsequent [version-8 acceptance comment][version-eight] records prior exact-source CI, smoke and rollback acceptance. | Compare the proposed candidate's source/configuration with each historical observation before reusing it. Neither establishes acceptance of the current repairs. |
| Persistent provider allowance | Native read-only database inspection on 17 October 2026 found used attempts: ONS CPIH **16**, ONS geography **9**, OS Names **10** and OS open-product metadata **9**; each lifetime maximum is **120**. | Complete four-row, untruncated `sites_pilot_allowance_v1` read after database overview; no provider requests or writes made. These are application attempt counters, not provider-account usage or financial limits; read again before any live run. |
| GitHub access | Native GitHub connector access works. Shell Git fetch and push dry-run also succeed. Shell access to `api.github.com` still returns `Forbidden`, but the available alternatives remove the remote-publication blocker. | Candidate PR/checks and protected-main evidence: **pending coordinator entry**. Remote `main` was reported at `5e9c948c`, ahead of the local review baseline; integrate before final candidate acceptance. |
| Updated Sites build tooling | The required `site-workflow.mjs` helper is absent from the available filesystem; both attempted skill-resource paths are unavailable. The returned saved archive also could not be authorised or resolved by the file-download tool. This blocks source recovery/update through the expected workflow; it does not establish a missing deployment or native-MCP platform capability. | Run source updates in an environment with the installed Sites helper bundle. The existing version 8 remains unchanged. Do not invent a substitute publishing path. |
| Database operations | The fresh exposed toolset provides database read access; no full backup, restore or row-deletion action was identified. | Supported recovery/deletion workflow and exercised result: **pending**. Do not promote read projections or checkpoint export into a restore claim. |
| Final publication | No new release, tag, deployment or accepted support transition is recorded here. | Immutable publication and acceptance references: **pending**. |
| Dependency repair | Pinned pnpm 10.33.2 resolved Hono 4.13.7, jsdom's Undici 8.10.2, source-map-js 1.2.2 and both MCP client pins 2.2.0. Current local registry audit reports zero advisories, compared with 14 before the repair. | [Disposition and retained reports](../operations/DEPENDENCY_SECURITY_2026-10-17.md). Exact-source CI/image/provenance, GitHub alert state and served Site bytes remain separate observations. |

After integration with `main` at `0a046021`, all **191** affected OKF+ tests
passed, including the newer archive/source-family security cases. The maintained
Sites evaluator/native-mount suite passed all **22** tests with local socket and
subprocess access; this closes the earlier sandbox-only verification limitation.
These tests use synthetic identities and provider responses and make no live
provider request.

The [five-tool acceptance record](FIVE_TOOL_ACCEPTANCE.md) binds the clean
`0eae2d0f` source to 15 maintained acceptance tests, an SDK journey with five
verified receipts and three refusal cases, and focused recovery/replay checks.
The source-bound QUAL-206 local receipt set was then regenerated through its
actual selected suites. Only material hashes and derived identities changed;
assertions, outcomes, limits and historical evidence guards were preserved.
All 33 local/strict receipt contract tests passed. These are local results, not
live hosting or a complete scored release evaluation.

The current native registration readback supersedes the historical version-7
`has_mcp: false` blocker for registration. Keep the historical observation intact.
It does not close OAuth, user consent, plugin installation, independent-client or
current-source deployment acceptance.

## Common closure checklist

Use these stable item identifiers in the PR and evidence handover. Check an item
only when its evidence identifies the actual candidate and the tested boundary.
Unavailable and failed prerequisites remain visible; independent work continues.

- [x] **C01 — Four authorised repairs:** implement UI-01, UI-02, EX-07 and CT-02,
  retain regression evidence and the recorded patch reviews. Local evidence is
  recorded above; canonical integration is C03.
- [ ] **C02 — Release identity and scope:** record the final source commit/tree,
  intended product/version, audience, advertised tools, support boundary,
  deployment target and rollback baseline. Preserve the distinction between the
  supported exact-five gateway and the private Sites exemplar.
- [ ] **C03 — Canonical source assurance:** obtain passing required PR and exact
  protected-main repository/image/provenance and CodeQL results. Preserve the
  independent image derivation and verification. The [stable CI aggregate][ci]
  requires all producers; the impact recommendation remains shadow-only.
- [ ] **C04 — Dependencies and release artifacts:** retain dependency locks, SBOM,
  source integrity, current advisory disposition and exact artifact digests.
  Reuse old observations only for their unchanged inputs and explicit scope.
  The [image release conditions][image-exit] govern the proposed gateway image;
  a previous image scan does not cover changed bytes.
- [ ] **C05 — Truthful acceptance record:** reconcile each applicable Sites or
  supported-gateway item below. Record passed, failed, unavailable and pending
  outcomes, their timestamps and evidence pointers. No synthetic observation may
  be relabelled as a hosted result.
- [ ] **C06 — Stable release metadata, when tagging a supported software release:**
  synchronise `VERSION`, npm/Python manifests and locks, consume material
  fragments, and prepare dated changelog and matching release notes. Run the
  explicit [release metadata gate][metadata-gate]. It is necessary metadata
  validation, not operational acceptance.
- [ ] **C07 — Immutable publication and handover:** follow the [delivery model][delivery]
  for exact-commit tagging, checksummed artifacts, deployment verification and
  rollback. Record Site publication separately from a GitHub supported release.
  After acceptance, update canonical status through the evidence follow-up; never
  move a published tag or replace accepted release assets.

## Private Sites exemplar checklist

These items apply to the existing private six-tool assembly. A newly published
candidate may remain explicitly experimental while wider acceptance is pending;
its support claims must list those limitations. They do not substitute for the
supported public gateway checklist below.

- [ ] **S01 — Current platform contract:** retain the version-8 native readback,
  supported updated build/publishing instructions and exact OAuth connection
  metadata. Preserve the existing project and private audience. Verify what the
  current tooling actually supports before changing its configuration.
- [ ] **S02 — Exact-source package:** package a clean assured GIS AI GO commit and
  bind the separate Site-source revision, dependency locks, runtime manifest and
  archive hashes. The [packager][packager] requires esbuild `0.28.1`; establish
  compatibility with recovered tooling rather than silently ignoring that pin.
- [ ] **S03 — Assembled build and migrations:** follow the [assembly instructions][assembly],
  preserve legacy routes and published migration SQL/journal bytes, and retain
  both hosting manifests and the complete generated migration tree. Run the
  actual host's pinned typecheck, lint and production build, then the built
  Worker/D1 and page probes. The overlay is not a standalone build.
- [ ] **S04 — Deployed identity:** verify the returned saved version/archive,
  terminal deployment status, actual tables, configured runtime revision and
  unchanged audience. A successful save or deployment status alone does not prove
  migration application or acceptance of newly built bytes.
- [ ] **S05 — Native authenticated connection:** use the provisioned App/plugin
  and exact returned connection metadata; establish an authenticated native
  `sites_capabilities` call before live-provider tests. Verify unauthorised
  rejection and record actual client/version. A test-token route, browser login,
  plugin identifier or local synthetic identity is not this result. Record each
  additional independent client's outcome separately. [Connection procedure][connection].
- [ ] **S06 — Bounded questions and accessible journeys:** run only admitted
  cases from the [pilot evaluation][evaluation], retaining source/semantic checks,
  inspectable receipts, safe measurements and failures. Check real manual-page
  keyboard/accessibility and provider-error journeys. Read existing allowance and
  receipt totals first; never refill counters or retry without accounting. Keep
  protected PSGA/NGD tools and unimplemented question classes unavailable.
- [ ] **S07 — Deployed operation:** observe allowance exhaustion/concurrency,
  cancellation and uncertain-write handling, provider suspension, credential
  revocation where applicable, receipt retention, an independent complete
  checkpoint, code rollback and restoration of the candidate. Reuse historical
  evidence only after verifying that the relevant inputs and boundary are unchanged.
- [ ] **S08 — Recovery and support decision:** investigate supported full D1
  export/restore and deletion in the updated platform. Demonstrate any claimed
  restoration or deletion separately from checkpoint comparison and code rollback.
  Record retention, recovery ownership and any accepted objectives. The existing
  [operating instructions][recovery] have no proved full database restoration,
  automatic deletion or accepted service level; retain that experimental limit
  unless new evidence closes it. Broader supported acceptance requires an explicit
  scope and decision, not merely checking the deployment items above.

## Supported exact-five `v0.2.0` checklist

These are the existing roadmap gates. The Sites six-tool deployment neither
implements nor waives them. The [admission verifier][admission] validates document
shape and cross-document identities offline; it does not authenticate observers
or prove the stated observations occurred.

- [ ] **G01 — Exact release candidate:** satisfy C02–C04 for the supported gateway;
  retain independently reproduced OCI bytes, current scan/SBOM, complete evidence
  manifest and protected-source attestations. Review the exact active topology.
- [ ] **G02 — Runtime admission:** complete the DEPLOY-207 plan with the canonical
  origin, non-static workload identity, enforceable spending stop, ownership,
  fencing, log/disposal decisions and recovery objectives.
- [ ] **G03 — External transport and operation:** independently observe direct
  public DNS/TLS/Host/Origin and rejection cases; exact five tools/three resources;
  API/MCP/readiness and text/structured-result parity; shared writer admission;
  admitted egress; separate digest-bound filesystem receipts; and tested
  checkpoint, restore and previous-image rollback without rebuilding.
- [ ] **G04 — Live provider and qualification:** after accepted transport, retain
  the bounded live ONS observation bound to that transport's bytes, durable receipt
  inspection and current source/rights evidence. Complete the scored candidate and
  independent-host observations, suspension/outage evidence and remaining
  [QUAL-206 release conditions][qualification].
- [ ] **G05 — Supported publication:** reconcile QUAL-206/DEPLOY-207 on the exact
  final candidate, complete C05–C07, and verify the tagged deployed artifact before
  declaring support or closing #23, #24 and #25.

The separately proposed `v0.2.0-local.1` edition is not a shortcut through G01–G05.
Its own [acceptance][local-acceptance] requires macOS and Linux observations and an
actual unaided colleague walkthrough, followed by a prerelease marked not latest.

## Finite local command plan

These are commands to execute and record, not a claim that this release run has
passed them. Use the pinned repository tools and locked dependencies. Canonical
CI remains required. Do not repeat the focused repair suites when unchanged,
valid observations already cover their inputs and the complete check is running.

```sh
pnpm install --frozen-lockfile
uv sync --locked --group dev --cache-dir .uv-cache
pnpm run check
pnpm run preview:v0.2.0
```

`check` covers typechecks, maintained unit/contract tests, browser checks,
reproducibility, contracts, versions/fragments, source links, secrets, diagrams,
SBOM, OKF+ and experience checks. The preview is a preparation artifact; it does
not consume fragments or change the release. With the pinned image-builder
environment used by CI, run `pnpm run check:gateway-image`; protected-main CI
separately produces the independent image, compares bytes and attests evidence.
See the [actual command graph][commands] and [CI source][ci].

For changed repair inputs, the bounded affected checks are:

```sh
pnpm --filter @gis-ai-go/public-explorer run typecheck
pnpm --filter @gis-ai-go/public-explorer run test:unit
pnpm run build:explorer
pnpm --filter @gis-ai-go/public-explorer run test:browser
uv run --locked --cache-dir .uv-cache python -m unittest discover -s tests -p 'test_okf_plus_*.py'
pnpm --filter @gis-ai-go/experience-intake run test
```

Once recovered Site tooling and a new output directory are selected, use the
exact `package_sites_pilot_runtime.mjs --tooling-root ... --output-dir ...` and
`test_sites_pilot_built_worker.mjs` invocations in the [assembly guide][assembly].
Run `node scripts/test_sites_pilot_page.mjs` with the built Site preview on the
documented loopback port. These probes use synthetic identity/provider responses;
they cannot complete S04–S08. Execute live evaluation only after admission and
through the documented bounded harness, without placing credentials in commands.

After preparing a supported release's metadata, run
`pnpm run validate:release-readiness`. Record the precise result and source
identity under C06. Before merging this record, run `pnpm run validate:links`,
`pnpm run validate:changelog-fragments` and `git diff --check`.

[candidate]: https://github.com/chris-page-gov/gis-ai-go/tree/72bc5aaf66242db219cdde5e2754a1a5e635a532
[roadmap]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/implementation/ROADMAP.md#L29-L54
[sites-adr]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/decisions/ADR-0018-private-sites-live-pilot.md#L171-L207
[review]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/architecture/REVIEW.md#L1-L29
[ui-repairs]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/implementation/EXPLORER_UI_REPAIRS.md#L8-L71
[validation-repairs]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/implementation/VALIDATION_REPAIRS.md#L9-L85
[hosted-history]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/implementation/SITES-218_HOSTED_OBSERVATION.md#L1-L36
[version-eight]: https://github.com/chris-page-gov/gis-ai-go/issues/143#issuecomment-5959134932
[ci]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/.github/workflows/ci.yml#L303-L327
[image-exit]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/operations/QUAL-206_IMAGE_VULNERABILITY_DISPOSITION.md#L170-L202
[metadata-gate]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/scripts/check_versions.py#L38-L94
[delivery]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/implementation/DELIVERY_AND_RELEASE.md#L42-L94
[packager]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/scripts/package_sites_pilot_runtime.mjs#L11-L30
[assembly]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/sites/private-pilot/README.md#L8-L98
[connection]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/sites/private-pilot/README.md#L116-L139
[evaluation]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/operations/SITES_MCP_PILOT_EVALUATION.md#L10-L48
[recovery]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/sites/private-pilot/README.md#L167-L199
[admission]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/operations/DEPLOY-207_PROVIDER_NEUTRAL_ADMISSION.md#L69-L210
[qualification]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/threat-model/QUAL-206_STAGE_2_RELEASE.md#L126-L149
[local-acceptance]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/docs/operations/LOCAL-214_ACCEPTANCE.md#L31-L90
[commands]: https://github.com/chris-page-gov/gis-ai-go/blob/72bc5aaf66242db219cdde5e2754a1a5e635a532/package.json#L13-L64
