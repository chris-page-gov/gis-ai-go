# Delivery progress

Last updated: 24 August 2026

## Current outcome

Deliver `v0.2.0`: expose the supported governed catalogue and evidence model through
an open, read-only MCP and direct API without weakening the static `v0.1.0` product.
The supported target active set is exactly `catalogue.search`,
`catalogue.describe`, `evidence.inspect`, `selection.resolve` and `data.query`.

## Active workstream

`QUAL-206 — Progress from repository preflight to independent-host evidence`

- retain the repository-local STDIO and client/version matrix bound to the
  protected-main v3 inspection-receipt runtime as preflight only;
- retain the source-bound Claude Code `2.1.204` legacy STDIO transport-readiness
  result separately from capability scoring, then complete the remaining
  independent desktop-STDIO and remote-HTTP host evidence; and
- stop before any public runtime, live provider call, host credential, registry
  publication, activation, tag or release that requires separate authority.

Supporting `EVID-204` release assurance remains inactive and does not replace that
main flow. A provider-independent candidate now checkpoints one stopped linked
ledger/index pair, binds it with one path-free content-addressed manifest and a
separately retained tail checkpoint, and restores only into empty private roots
before completing both verifiers. It selects no storage provider and supplies no
deployment, operator-fencing, schedule, RPO/RTO, disposal or release evidence.

## Completed

- Stage 0 foundation verified at `983b1a102aa8038c9f50ae1b1894315c3ae0b89f`;
- project identity changed from the historical codename to GIS AI GO;
- MIT licensing applied to code, documentation, schemas and research;
- `chris-page-gov/gis-ai-go` created on GitHub;
- clean public repository recreated under the owner's personal account with only the
  corrected history;
- original commit metadata corrected to the owner's GitHub `noreply` identity;
- private vulnerability reporting, secret scanning, push protection, Dependabot and
  CodeQL enabled;
- roadmap milestones and delivery labels provisioned;
- `CTRL-002` merged through protected `main` with passing assurance;
- `main` protected by a no-bypass, squash-only pull request ruleset;
- `v0.1.0` delivery issues 3 to 7 created and assigned;
- `DISC-101` merged at `4ff9cc79946b1977a2022428336687a3dedb04b3` with
  passing main assurance and CodeQL;
- canonical OKF generation now produces 18 source-locked public metadata records in
  equivalent Markdown, JSON and JSON-LD projections;
- `DISC-102` merged through [pull request 9](https://github.com/chris-page-gov/gis-ai-go/pull/9)
  at `6984f3097cff578f0d22088ca8582ebe55725115` with passing assurance and
  CodeQL;
- the accessible static Explorer now provides search, facets, governed cards,
  graph, timeline, non-legal schematic map, durable URLs and machine-readable
  downloads;
- full local `pnpm run check` passed on 20 August 2026;
- `DISC-103` merged through [pull request 10](https://github.com/chris-page-gov/gis-ai-go/pull/10)
  at `e5a522ee17f3a0a6f5857245c5ae3acd767efc25` with passing assurance and
  CodeQL;
- the canonical public bundle now contains 36 records covering reviewed HMLR
  discovery journeys, HMLR datasets and non-executing ONS and LandIS provider
  capabilities with exact rights and provenance boundaries;
- `DISC-104` merged through [pull request 14](https://github.com/chris-page-gov/gis-ai-go/pull/14)
  at `a0e826384cf50d9d81b87489dbf3580e8e3602f7` with passing main assurance,
  provenance and CodeQL;
- two accepted protected-main source artefacts were deployed successfully through
  GitHub's pinned official Pages transport;
- artefact-only rollback to source commit `eced0ae` and restoration of source
  commit `a0e8263` both completed without rebuilding the product; and
- the public product is verified at
  <https://chris-page-gov.github.io/gis-ai-go/>;
- QUAL-105 merged through [pull request 16](https://github.com/chris-page-gov/gis-ai-go/pull/16)
  at `24925fc7f77b416d557c719942c86eaa3578b4b1` with passing pull-request and
  protected-main assurance, provenance and CodeQL; and
- two clean release builds are byte-identical, while browser, accessibility,
  security and release-metadata gates have no unresolved P0-P2 findings;
- release [pull request 17](https://github.com/chris-page-gov/gis-ai-go/pull/17)
  merged as protected-main commit
  `f1bda209e6309bf4f14f7ab7f524c442e59917b8` with passing assurance,
  provenance and CodeQL;
- annotated tag `v0.1.0` is protected against update and deletion with no bypass;
- the exact attested release artefact was deployed in
  [run 32331337338](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32331337338),
  deployment `5995702325`, and passed all four public-browser acceptance tests; and
- [`v0.1.0`](https://github.com/chris-page-gov/gis-ai-go/releases/tag/v0.1.0)
  is published as the immutable latest release with nine checksummed evidence
  assets; and
- the supported-release hand-off reached protected `main` through
  [pull request 18](https://github.com/chris-page-gov/gis-ai-go/pull/18) at
  `80ac89d89e04751045693cecff4a3a714d121ebe`;
- [`ADR-0009`](docs/decisions/ADR-0009-read-only-mcp-tool-lifecycle.md) defines the
  exact read-only tool lifecycle and supported five-tool `v0.2.0` target;
- the first MCP-201 contract slice reached protected `main` at
  `e5e6d4db5ac7036198cde64279e815f214f3defd`, with passing assurance and provenance
  in [run 32338916345](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32338916345),
  passing CodeQL in
  [run 32338916269](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32338916269)
  and [attestation 41792357](https://github.com/chris-page-gov/gis-ai-go/attestations/41792357);
- that slice defines closed catalogue search, description and problem schemas,
  query-analysis bounds and the shared catalogue core without activating a tool;
  and
- the existing Explorer adopts a reusable shared catalogue foundation without
  gaining any dependency on a running service;
- the inactive gateway candidate merged through
  [pull request 27](https://github.com/chris-page-gov/gis-ai-go/pull/27) as
  `4948890c10adb4f0ac6f427cda21cb0c0c4607dd`, after passing pull-request assurance,
  all CodeQL language analyses and an independent no-P0-P2 review; and
- the candidate verifies the immutable catalogue, supplies deterministic bounded
  in-process search and description, and exposes only loopback health, blocked
  readiness and OpenAPI with zero active tools or API operations; and
- EVID-204A merged through
  [pull request 29](https://github.com/chris-page-gov/gis-ai-go/pull/29) as
  `af9043955470568c146397d1a25dd8813eb7aa55`; it adds RFC 8785
  canonicalisation, content-addressed anonymous-open authority and policy decisions,
  and independently verified inline receipts to every in-process catalogue success
  while keeping activation blocked;
- protected `main` now also contains the deterministic EXEC-202 service
  (`6837af6`), durable public ledger (`cb6b817`), bounded adapter preflight
  (`364c868`), tool registry (`76103c1`), receipt inspection transport (`c4d43f9`),
  fixed ONS adapter (`ef960f7`), public-read v2 contracts (`5a7e441`), selection
  resolver (`99426de`), data-query application (`b5f8edc`), inactive public-read
  transports (`51147e0`) and receipt-only reconciliation (`5253041`);
- EVID-204 reconciliation merged through
  [pull request 46](https://github.com/chris-page-gov/gis-ai-go/pull/46) with its
  exact reviewed tree, passing protected-main assurance and provenance in
  [run 32456796186](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32456796186),
  passing CodeQL in
  [run 32456796369](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32456796369)
  and strict SLSA
  [attestation 42067801](https://github.com/chris-page-gov/gis-ai-go/attestations/42067801);
- those protected-main slices remain explicitly injected and suspended: production
  operation arrays are empty, readiness is `503`, and there is no public MCP service,
  live provider capability, deployment or `v0.2.0` release;
- the completed repository/private boundaries for
  [MCP-201](https://github.com/chris-page-gov/gis-ai-go/issues/19) and
  [EXEC-202](https://github.com/chris-page-gov/gis-ai-go/issues/20) were reconciled
  and closed on 23 August 2026. Their successor activation, live-host and deployment
  gates remain open under TOOLS-205, QUAL-206 and DEPLOY-207;
- DEPLOY-207 repository assurance merged through
  [pull request 48](https://github.com/chris-page-gov/gis-ai-go/pull/48) as protected-main
  commit `e65071dc1f1bb0baab852bbf8218f9b5f953ad02`. Protected-main
  [run 32553285859](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32553285859)
  passed repository, exact gateway-image, aggregate and provenance assurance, while
  [run 32553285746](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32553285746)
  passed CodeQL for Actions, JavaScript/TypeScript and Python. CI rebuilt and verified
  the pinned non-root blocked image, canonical repeat-build identity, full SBOM,
  retained offline-replayable vulnerability evidence, internal Compose boundary,
  persistence, suspension and exact-image restore. Strict protected-main attestations
  bind the OCI archive, SBOM and closed evidence manifest to that exact source. The
  accepted Docker 28 empty-port representation remains a zero-realisation form only:
  the declared loopback binding, internal network and host-closed probes remain exact.
  Generated text and bounded phase output share the privacy gate; incomplete evidence
  remains private and is never uploaded. This is not a published image or deployment;
- QUAL-206 repository preflight merged through
  [pull request 49](https://github.com/chris-page-gov/gis-ai-go/pull/49) as protected-main
  commit `f0e3ccc1dceeba6b3f7d0ecd56c5dd083dee405a`. Protected-main
  [run 32567301935](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32567301935)
  passed repository, exact gateway-image, aggregate and provenance assurance, while
  [run 32567301734](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32567301734)
  passed CodeQL for Actions, JavaScript/TypeScript and Python;
- the current repository-only receipt set retains deterministic local receipts for
  E01, E02, E09, E13, E15, E17 and E20 across 17 source-bound suites and 82 exact
  selected tests. Every receipt remains non-live, unscored and explicitly
  incomplete as release evidence;
- the accepted tree integrates all 30 Stage-2 threat-record risks, with a hold outcome for
  activation and release, and records the three retained unfixed High image
  vulnerabilities as unresolved rather than accepting them;
- T04 has one exact, content-addressed ONS cache fallback that must be injected
  explicitly and can run only when the current execution of an exact, pristine ONS
  adapter returns an internally classified network failure or HTTP 500 to 599
  response. Its owner-bound outage proof is consumed once in that invocation, and
  its source, result, rights, observation, approval and freshness identities are
  fixed;
  all other failures remain closed, production registration remains empty and
  readiness remains `503`;
- EVID-204 trace and readiness integrity merged through
  [pull request 51](https://github.com/chris-page-gov/gis-ai-go/pull/51) as protected-main
  commit `d2e8bb8b6d0f6ee9c693d117b4a238861a5129c3`. Protected-main
  [run 32650741280](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32650741280)
  passed repository, exact gateway-image, aggregate and provenance assurance, while
  [run 32650741234](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32650741234)
  passed CodeQL for Actions, JavaScript/TypeScript and Python;
- the exact-five candidate merged through
  [pull request 53](https://github.com/chris-page-gov/gis-ai-go/pull/53) as protected-main
  commit `27d76e1149ce1711e1af98fe0bb52a3666471a58`. Protected-main
  [run 32656337673](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32656337673)
  passed repository, exact gateway-image, aggregate and provenance assurance, while
  [run 32656337308](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32656337308)
  passed CodeQL for Actions, JavaScript/TypeScript and Python. The immutable
  `candidate-unregistered` assembly is shared across direct HTTP, MCP HTTP, MCP
  STDIO, OpenAPI and plain text. Production registration remains false, shipped
  activation arrays remain empty;
- the bounded governance research intake merged through
  [pull request 52](https://github.com/chris-page-gov/gis-ai-go/pull/52) as
  `37a71cdcc55bf3708527596d47ea9839d150fed5`. Protected-main
  [run 32658667714](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32658667714)
  passed repository, exact gateway-image, aggregate and provenance assurance, while
  [run 32658667650](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32658667650)
  passed CodeQL for Actions, JavaScript/TypeScript and Python. The
  non-redistributable PDF and privacy-sensitive original DOCX remain local-only and
  ignored; protected `main` contains the supplied advisory Markdown, a
  privacy-scrubbed DOCX derivative, the source-by-source findings matrix and only
  the supported threat-evidence crosswalk. It changes no runtime, activation or
  release state;
- EVID-204 current-call inspection receipts merged through
  [pull request 54](https://github.com/chris-page-gov/gis-ai-go/pull/54) as protected-main
  runtime commit `7fa8b720d3cbaa3e0a1ebfadf0fb355a7330a04c`. Protected-main
  [run 32664382129](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32664382129)
  passed repository, exact gateway-image, aggregate and provenance assurance, while
  [run 32664382047](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32664382047)
  passed CodeQL for Actions, JavaScript/TypeScript and Python. Every current v3
  inspection result carries a distinct verifiable inline receipt without persisting
  or attesting it or creating a ledger record or event. Historical v1 and v2
  contracts remain unchanged, and production registration remains false; and
- the repository-local QUAL-206 protocol matrix merged through
  [pull request 55](https://github.com/chris-page-gov/gis-ai-go/pull/55) as
  protected-main commit `30b575beb27ff805745a2864c1acf44392774046` with
  passing protected-main assurance and provenance in
  [run 32667087755](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32667087755)
  and passing CodeQL in
  [run 32667087601](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32667087601).
  It binds four pinned
  official-client and raw-transcript HTTP and STDIO source-coverage rows to exact
  Git blobs from the protected-main v3 runtime. Seven in-process suspension
  scenarios produce nine suspensions, reduced discovery, rejected calls and zero
  provider calls. The JSON records no test-runner outcome; it remains non-live and
  unscored and does not complete independent-host evidence; and
- Claude Code `2.1.204` subsequently completed legacy STDIO initialisation and
  `tools/list` through the constructor-only two-tool conformance launcher from a
  clean, detached checkout of exact protected-main commit
  `30b575beb27ff805745a2864c1acf44392774046`. This is source-bound transport
  readiness with capability unscored. It does not alter the earlier modern-only
  `not_ready` or exploratory records and exercised no model authentication, model task,
  tool call, resource read, exact-five production assembly, live provider, remote
  HTTP host, registration, activation, deployment or release; and
- acceptance requires both the complete local repository gate, which passes on this
  matrix tree, and the protected pull-request and protected-main checks. The local
  gate includes all TypeScript and Python tests, 27 real-browser tests,
  deterministic release builds, contract, link and secret validation, the execution
  container, diagrams and the repository SBOM.

## Next

1. Complete bounded Claude capability evidence and the remaining independent
   desktop-STDIO and remote-HTTP host evidence. The local protocol matrix and
   Claude transport-only result do not complete issue #24's live-host criteria.
2. Monitor official supported glibc base releases. Re-probe Bookworm and Trixie
   only when immutable upstream bytes or package fix status changes; accept a
   replacement only if complete repository and image assurance, reproducible OCI
   builds, SBOM, current scanning and compatibility review pass.
3. Keep DEPLOY-207 at `status: decision needed` until an authorised public runtime,
   hostname/TLS, identity, egress, storage and operator boundary exists.
4. Only after that separate authority exists, deploy an unregistered
   candidate and complete live QUAL-206 evidence before any activation, registry
   publication, tag or `v0.2.0` release.

## Current blockers

- The repository-only image and Compose candidate are accepted on protected `main`.
  There is still no authorised public runtime, hostname/TLS boundary, workload
  identity, admitted persistent volume or backup target, independently administered
  external checkpoint, operator-fencing/schedule/disposal model, service deployment
  workflow or previous deployed image for a real rollback. The provider-independent
  checkpoint mechanics are not deployed disaster-recovery evidence.
- The gateway assertion is a typed private hand-off, not workload authentication or
  a signed policy decision. Any non-loopback deployment remains blocked on explicit
  service identity and network-policy evidence.
- Activating or publishing a catalogue service remains hard-blocked. Raw protocol
  transcripts, deterministic local host fixtures and the pinned SDK clients do not
  establish independent live major-host interoperability. The source-bound Claude
  transport check establishes initialisation and listing only, not capability.
  Security, accessibility, governed ingress/storage admission, retention/disposal
  and host-specific lifecycle evidence remain activation gates.
- Direct routes and MCP transports now exist on protected `main`, but the
  exact-five assembly is `candidate-unregistered`, production registration is
  false, the production/default capability arrays are empty, shipped readiness is
  `503`, and there is no public service deployment or activation override. The
  repository-local matrix is non-live and cannot close issue #23 or issue #24;
  independent hosts, a live provider, authorised deployment and release evidence
  remain outstanding.
- The 23 August Bookworm and Trixie probe found no supported official glibc
  replacement that both resolves all three retained High image vulnerabilities and
  satisfies the current compatibility boundary. Re-probe only after immutable
  upstream bytes or package fix status changes. Activation and release require
  either a fully assured patched base or an explicit owner risk decision; repository
  containment is not remediation or acceptance.
- The accepted ONS adapter and reconciliation storage are local, explicitly injected
  components. The fixed 4,096-claim pre-publication index ceiling and accepted ledger
  event ceiling are local safety bounds, not deployment quotas. There is no
  cluster-wide admission, reclamation, durable shared rate service or operator
  resolution for permanently pending claims; production provider dispatch remains
  blocked.
- Protected PSGA and commercial deployments require separate rights, credentials
  and isolated infrastructure. They remain outside this release and do not block
  the open product.

## Latest evidence

- Claude Code `2.1.204` protected-main legacy STDIO readiness: the
  [source-bound summary](tests/interoperability/evidence/claude-code-legacy-stdio-readiness-2026-08-23.json)
  records a clean, detached checkout of exact protected-main commit
  `30b575beb27ff805745a2864c1acf44392774046`, current-wrapper telemetry and a
  successful `mcp list` transport check. Initialisation and `tools/list` passed
  through the constructor-only two-tool conformance launcher. Capability remains
  unscored; no model authentication, model task, tool call, resource read, exact-five
  production assembly, live provider, remote HTTP host, registration, activation,
  deployment or release was exercised. The historical modern-only `not_ready` and
  uncommitted exploratory records remain unchanged;

- current protected-main runtime hand-off: EVID-204 inspection receipts
  [pull request 54](https://github.com/chris-page-gov/gis-ai-go/pull/54) merged as
  `7fa8b720d3cbaa3e0a1ebfadf0fb355a7330a04c`; protected-main assurance and
  provenance passed in
  [run 32664382129](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32664382129)
  and CodeQL passed in
  [run 32664382047](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32664382047).
  The [source attestation is 42456194](https://github.com/chris-page-gov/gis-ai-go/attestations/42456194),
  and the gateway [OCI](https://github.com/chris-page-gov/gis-ai-go/attestations/42456249),
  [SBOM](https://github.com/chris-page-gov/gis-ai-go/attestations/42456257) and
  [manifest](https://github.com/chris-page-gov/gis-ai-go/attestations/42456259)
  attestations bind the same commit. The current local QUAL receipt set retains 7
  receipts, 17 suites and 82 exact tests at set ID
  `gis-ai-go:qual-206-local-evaluation-set:sha256:160298c85fb3db5394c5c27d4905e1e5cf086bad60aae3b7512f2890dcbeb43d`
  and file SHA-256
  `f93e0988a966e0387cde1bdb89261fe40308e733f1ac7725e8735818094e1dea`;
- QUAL-206 local protocol-matrix acceptance: protected
  [pull request 55](https://github.com/chris-page-gov/gis-ai-go/pull/55) merged as
  `30b575beb27ff805745a2864c1acf44392774046`; protected-main assurance and
  provenance passed in
  [run 32667087755](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32667087755)
  and CodeQL passed in
  [run 32667087601](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32667087601).
  The matrix binds the
  official MCP client 2.0.0 and MCP 2026-07-28 source coverage across four
  semantically fixed HTTP and STDIO rows to exact Git blobs from protected-main
  runtime `7fa8b720d3cbaa3e0a1ebfadf0fb355a7330a04c`. Seven in-process suspension
  scenarios produce nine suspensions with zero provider calls. The JSON records no
  test-runner outcome; current execution is established separately by the complete
  local gate. Matrix ID
  `gis-ai-go:qual-206-local-protocol-evidence-matrix:sha256:472798d1207dcdd7fc9c001f3ae67e733b4fb7bbbae1514ec1d81dea2182e3f7`
  has file SHA-256
  `c74f1433605cd783d14933a8ce18efed4d1ddcb9843b4b8dc380eccb47921a58`.
  It remains repository-only, non-live and unscored;
- advisory research
  [pull request 52](https://github.com/chris-page-gov/gis-ai-go/pull/52) merged as
  `37a71cdcc55bf3708527596d47ea9839d150fed5`; protected-main assurance and
  provenance passed in
  [run 32658667714](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32658667714)
  and CodeQL passed in
  [run 32658667650](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32658667650).
  Its sources are bounded evidence inputs, the two privacy-sensitive or
  non-redistributable originals remain local-only and ignored, and the merge makes
  no runtime or release claim;
- TOOLS-205 exact-five candidate: protected
  [pull request 53](https://github.com/chris-page-gov/gis-ai-go/pull/53) merged as
  `27d76e1149ce1711e1af98fe0bb52a3666471a58`; protected-main assurance and
  provenance passed in
  [run 32656337673](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32656337673)
  and CodeQL passed in
  [run 32656337308](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32656337308).
  The same immutable assembly drives direct and MCP discovery and invocation;
  registry, policy, provider lifecycle and suspension are subtractive, and
  production registration remains false;
- EVID-204 trace and readiness integrity: protected
  [pull request 51](https://github.com/chris-page-gov/gis-ai-go/pull/51) merged as
  `d2e8bb8b6d0f6ee9c693d117b4a238861a5129c3`; protected-main assurance and
  provenance passed in
  [run 32650741280](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32650741280)
  and CodeQL passed in
  [run 32650741234](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32650741234).
  Server-owned trace context crosses direct HTTP, MCP HTTP, MCP STDIO and the
  execution boundary without widening provider authority, and readiness re-verifies
  the configured evidence pair;
- QUAL-206 repository-preflight acceptance: the
  [content-addressed local receipt set](evaluation/qual-206-local-evaluation-receipts.v1.json)
  binds 7 applicable cases, 17 suites and 82 exact tests to their current source and
  fixtures. The approved T04 cache, rebuild and provider-result identities
  independently reproduce. Earlier exact-diff reviews found forged-cache, broad-outage,
  HTTP-parser, stale-control-record, proxy-minted transport, discarded DNS-failure,
  replayable-outage and truncated-response P2s. The current replacement uses private
  instance, transport and outage brands; binds network eligibility to the module-owned
  fixed transport and the exact pristine adapter that performed the current call;
  consumes each owner-bound proof once; preserves recognised DNS failures; rejects
  proxies, method substitution and HTTP parser framing; and treats premature response
  closure, including a truncated redirect, as malformed while retaining pre-response
  connection resets as network failures. Only unchanged exact bytes with a terminal
  no-P2 review and protected pull-request checks progressed through
  [pull request 49](https://github.com/chris-page-gov/gis-ai-go/pull/49) as
  `f0e3ccc1dceeba6b3f7d0ecd56c5dd083dee405a`. Protected-main CI and CodeQL passed.
  This is accepted local, non-live and unscored evidence, not host interoperability or
  release acceptance;
- DEPLOY-207 protected-main evidence: the final aggregator rebuilds the OKF projection,
  materialises only Git-tracked allowlisted source plus checksummed OKF outputs,
  proves canonical repeat-build OCI identity, generates an unfiltered full Syft
  SBOM, retains all High and Critical Trivy evidence with a fixable-only block and
  deterministic offline database replay, and exercises the strict local Compose
  boundary. Its exact directory is closed to 11 subjects plus one evidence manifest;
  protected-main provenance attests the OCI archive, SBOM and manifest only after a
  clean-source run. Dynamic tool versions and timings stay outside the
  reproducible OCI. Compose declares only host loopback, while acceptance records
  either the realised loopback or a no-port internal fallback. This makes no
  host-ingress, public deployment, provider, activation or production-rollback claim.
  [Run 32567301935](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32567301935)
  passed on protected-main commit `f0e3ccc1dceeba6b3f7d0ecd56c5dd083dee405a`;
  strict [OCI archive](https://github.com/chris-page-gov/gis-ai-go/attestations/42310989),
  [SBOM](https://github.com/chris-page-gov/gis-ai-go/attestations/42310990) and
  [evidence manifest](https://github.com/chris-page-gov/gis-ai-go/attestations/42310993)
  attestations bind the exact subjects to that source;
- the exact-five repository candidate is compile-time and unregistered; every
  shipped production/default operation array remains empty;
- EVID-204 reconciliation acceptance: protected-main assurance and provenance pass
  in [run 32456796186](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32456796186),
  CodeQL passes in
  [run 32456796369](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32456796369),
  open code-scanning alerts are zero and strict SLSA
  [attestation 42067801](https://github.com/chris-page-gov/gis-ai-go/attestations/42067801)
  binds archive SHA-256
  `8a477ba0f7abd207c72f3d762661067b3cc52ed9d4a749ee169063e0084712b7`
  to the exact merge. The accepted slice remains inactive, undeployed and non-live;
- ADAPT-203B local candidate: the complete locked gate passes 409 tests, with one
  deliberately skipped opt-in live-provider test, including 31 provider-adapter,
  99 gateway and 27 real-browser tests;
- ADAPT-203B repository assurance: 27 schemas and 67 records validate; 338 local
  links, 183 immutable research hashes, 2 ledgers and 71 source identifiers
  resolve; the 607-file secret scan, 9 diagrams and 165-component SBOM pass; two
  clean Explorer release builds are byte-identical;
- ADAPT-203B live evidence: the final opt-in no-credential probe at
  `2026-08-20T20:21:08.947Z` reached the exact fixed version `121` selection in
  one attempt over TLS 1.3 with HTTP 200. The 2,399-byte canonical result has
  domain-separated SHA-256
  `309a7c0a374f93f20d4b4cc8aaa4530c4a828ea27e4e26e266b367e59b7da3bd`.
  The evidence record and live-probe output retain only version, rights, status,
  hash/size and safe timing/TLS/byte metadata, with no raw response body,
  observation value, address, credential or path. A deterministic test fixture
  separately retains the public aggregate scalar `10471` to reproduce that digest;
- EXEC-202 local candidate: the complete locked gate passes with 19 shared-contract,
  25 canonical-evidence, 2 authority-context, 6 policy, 95 gateway, 16 Explorer
  build-policy, 42 Explorer unit/component, 99 repository Python, 20 execution
  service and 27 real-browser tests;
- EXEC-202 execution assurance: deterministic gateway/Python fixtures validate
  against 3 new closed schemas; malformed geometry, CRS/axis, feature, coordinate,
  byte, output, complexity, deadline, cancellation, compression, hostile Host and
  non-reflective error regressions pass; the actual container passes non-root,
  read-only, network-none, no-capability and no-exposed-port acceptance;
- EXEC-202 repository assurance: 23 schemas and 63 records validate; 314 links, 183
  immutable research hashes, 2 ledgers and 71 source identifiers resolve; the
  555-file secret scan, 9 diagrams, 164-component SBOM and npm high-severity audit
  pass; two clean release builds are byte-identical. The exact candidate-commit
  archive identity is recorded in the pull-request assurance evidence rather than
  self-referentially in this commit;
- MCP-201 blocked transport foundation: exact local implementation commit
  `fb0234b9a6a968fe68c2fbe98388f2415393c9c1`, based on protected-main commit
  `997d5fdd478797b20b05d1980be8f986645d410e`, passes the complete locked gate with
  19 contract, 20 evidence, 2 authority-context, 6 policy, 86 gateway, 16 Explorer
  build-policy, 42 Explorer unit and component, 95 repository Python, 2
  execution-boundary and 27 browser tests;
- MCP-201 blocked transport assurance: two clean release builds are byte-identical
  at archive SHA-256
  `ff7d3e19bfbf12d610526e3e62a3fc14e6c7960a34ddbf3190eb044a74767035`;
  15 schemas, 55 records and 3 evaluation manifests validate; 308 links, 183
  research hashes, 2 ledgers and 71 source identifiers resolve; the 516-file scan,
  9 diagrams and 163-component SBOM pass; two independent current-byte reviews and
  the completed security diff review report no P0–P2 finding;
- MCP-201 transport acceptance: protected
  [pull request 31](https://github.com/chris-page-gov/gis-ai-go/pull/31) at exact
  head `3a92c005e67ca1d239c1f4a3c0a955b19c59bd7a` passed assurance in
  [run 32389353007](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32389353007)
  and CodeQL in
  [run 32389350801](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32389350801),
  then merged as `edc26c0396ecd230570de1ab0fd402338567f67d`; protected-main
  assurance and provenance passed in
  [run 32389721338](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32389721338),
  CodeQL passed in
  [run 32389721461](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32389721461),
  and [attestation 41912276](https://github.com/chris-page-gov/gis-ai-go/attestations/41912276)
  binds archive SHA-256
  `20ddcfeb54d40ed3c55784856d608d94e81e6a73f7870d03f2cf7a85e11b8fd5`
  to that exact commit and run; no deployment or independent major-host evidence
  is claimed;
- MCP-201 shared catalogue contract: protected-main commit
  `e5e6d4db5ac7036198cde64279e815f214f3defd`, passing assurance and provenance in
  [run 32338916345](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32338916345),
  passing CodeQL in
  [run 32338916269](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32338916269)
  and [attestation 41792357](https://github.com/chris-page-gov/gis-ai-go/attestations/41792357);
- MCP-201 gateway candidate: exact implementation commit
  `442f788108106744e1e2ed7283e38c2a22aac5f1` passed the complete local gate and an
  independent no-P0-P2 review; protected
  [pull request 27](https://github.com/chris-page-gov/gis-ai-go/pull/27) passed
  assurance in
  [run 32344360889](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32344360889)
  and CodeQL in
  [run 32344358198](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32344358198),
  then merged as `4948890c10adb4f0ac6f427cda21cb0c0c4607dd`; the candidate exposes no
  catalogue operation, MCP tool or public deployment;
- EVID-204A accepted slice: protected
  [pull request 29](https://github.com/chris-page-gov/gis-ai-go/pull/29) merged as
  `af9043955470568c146397d1a25dd8813eb7aa55`; assurance and provenance passed in
  [run 32357424957](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32357424957),
  CodeQL passed in
  [run 32357427549](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32357427549),
  and [attestation 41836254](https://github.com/chris-page-gov/gis-ai-go/attestations/41836254)
  binds archive SHA-256
  `5253b24944e2579791bcb22f42fa6792fa5a27e34e6b36f29ffde0162b509362`
  to that exact protected-main commit and workflow;
- EVID-204A complete gate: 19 shared-contract tests, 20 canonical-evidence tests,
  2 authority-context tests, 6 public-policy tests and 41 gateway tests pass; all
  94 repository Python tests, 2 execution-boundary tests, 16 Explorer build-policy
  tests, 42 Explorer unit and component tests and 27 real-browser tests also pass;
  the gate validates 11 manifests and locks, 15 schemas and 55 records, 308 local
  links, 183 immutable research hashes, 2 ledgers and 71 source identifiers, scans
  508 text files, renders 9 diagrams and emits a 149-component SBOM;
- EVID-204A reproducibility: two clean locked builds produced the same Pages archive
  SHA-256 `f6adb7998c26bef62a651ec825e3a4426d955af4a09167b264dfa221d0ef28b0`;
  the OKF content root is
  `157ccef25e03043b69bf1f2be180b4b0242b5056c17edcfcd15acbd94c6e2007`;
- latest accepted protected-main local gate: type checking, 41 gateway tests,
  16 Explorer build-policy tests, 42 Explorer unit and component tests,
  94 repository Python tests, 2 execution-boundary tests and 27 real-browser tests
  pass;
- QUAL-105 reproducibility: two complete clean locked builds produce byte-identical
  Pages archives, checksums and receipts; the public workflow now emits a mandatory
  canonical verification receipt after a successful deployed-browser gate;
- QUAL-105 independent security and accessibility reviews: no P0-P2 finding or
  material evidence error remains;
- supported release: immutable latest
  [`v0.1.0`](https://github.com/chris-page-gov/gis-ai-go/releases/tag/v0.1.0),
  protected tag object `2f566c6e26dd17b13799e2976500e14701f04d11` and release commit
  `f1bda209e6309bf4f14f7ab7f524c442e59917b8`;
- release commit assurance and provenance: passing in
  [run 32330917042](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32330917042);
- release commit CodeQL for Actions, JavaScript/TypeScript and Python: passing in
  [run 32330916721](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32330916721);
- canonical release archive SHA-256
  `acf072986dafc34795039e363d0d5d09af44432fa392ff3aee5525887e1081a4`,
  payload root `80a649a5e4bebc36fb38c7b6d51d84056d1b2ff4c8b5f6b96c75bb6d03c6d245`
  and OKF content root
  `f6da572916ea850f6825e276867504a835bc783d76cea8038f72c8d1d42c2750`;
- GitHub release and all nine assets pass GitHub release attestation verification,
  while a fresh post-publication download passes the published checksum ledger;
- canonical OKF content, Explorer, reviewed public examples and supported Pages
  transport: merged on protected `main` at
  `a0e826384cf50d9d81b87489dbf3580e8e3602f7`;
- main assurance and provenance: passing in
  [run 32329062233](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32329062233);
- CodeQL for Actions, JavaScript/TypeScript and Python: passing in
  [run 32329061657](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32329061657);
- Explorer assurance includes
  16 build-policy tests, 42 unit and component tests, 25 browser journeys and
  production integrity checks;
- bounded security diff review: all changed runtime, interface and build-assurance
  files covered; the confirmed Low CSP/origin assurance gap, exact HTML-attribute
  parsing, fresh preview-server enforcement, and defensive symlink and lock-strict
  hardening are remediated with passing regressions;
- DISC-103 source review: exact provider snapshots and HMLR `v0.3.0` inputs are
  selected; the merged 36-record product passed the complete repository gate,
  including 25 browser journeys, and independent review;
- DISC-103 security review: the selected HMLR inputs and copied licence are
  independently bound to approved v0.3.0 digests, and coordinated source, rights,
  licence and lock mutations now fail closed;
- DISC-104 supported transport: the complete local gate passes with 27
  archive and staging contracts, 11 workflow contracts, 69 repository Python
  tests, 25 browser journeys and the full integrity, link, secret, diagram and SBOM
  checks;
- DISC-104 artefact A: protected-main run `32322035483`, source commit
  `eced0ae697818b4989ebe95c5bf1572cc6ec90c2`, archive SHA-256
  `b20ba6cab1811b976417aef6ca4c61bc33270063d7646ab8469e3273399edd11`,
  payload root `7d0adda69e77b815e75e860426cb3ac107b89a70abdd91d771070024c459444b`
  and OKF content root
  `c8415e83643b43b6fbde43cf30cf80ce8e5440f69770cfd9433337a5087f37fd`;
- DISC-104 artefact B: protected-main run `32324008595`, source commit
  `a0e826384cf50d9d81b87489dbf3580e8e3602f7`, archive SHA-256
  `262231b123bd9fbd9ae01c5d3c138bd63a53d189a55436f6c1b37eff3b2f9194`,
  receipt SHA-256
  `75b7e3d8d6eaaf54a12a22176ba1eda1e8c3ceee2892058e1d04437b7b8bdb6b`,
  payload root `cbc0893a46a4674ef7d13aa4aebcbeb0355f9c8a08286a6500bfc954cb5d6ef6`
  and OKF content root
  `a620158911cc60259f0ceab2af0dfdd886783a50bfe98000d692fd534bd08ec0`;
- DISC-104 deployment evidence: artefact A in run `32324162767`, artefact B in
  run `32324285041`, rollback to A in run `32324385218` and restore to B in run
  `32324490516`; each public acceptance suite passed and the final live receipt is
  bound to `a0e826384cf50d9d81b87489dbf3580e8e3602f7`;
- public repository: verified with personal `noreply` commit identity;
- deployed product: <https://chris-page-gov.github.io/gis-ai-go/>;
- latest supported release:
  [`v0.1.0`](https://github.com/chris-page-gov/gis-ai-go/releases/tag/v0.1.0).
