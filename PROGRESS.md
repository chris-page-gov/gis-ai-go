# Delivery progress

Last updated: 21 August 2026

## Current outcome

Deliver `v0.2.0`: expose the supported governed catalogue and evidence model through
an open, read-only MCP and direct API without weakening the static `v0.1.0` product.
The supported target active set is exactly `catalogue.search`,
`catalogue.describe`, `evidence.inspect`, `selection.resolve` and `data.query`.

## Active workstream

`DEPLOY-207 — Prepare an unregistered v0.2.0 service candidate`

- package a pinned, minimal, non-root gateway image and an offline local Compose
  harness without changing production activation;
- prove exact-source image construction, repeat-build identity, SBOM, vulnerability
  scanning, health, blocked-readiness, storage and rollback boundaries;
- define deployment-neutral HTTPS ingress, workload identity, private persistent
  storage, admission and log-minimisation requirements; and
- stop before any public runtime, provider call, registry publication, activation,
  tag or release that requires separate operational authority.

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
  and
- those protected-main slices remain explicitly injected and suspended: production
  operation arrays are empty, readiness is `503`, and there is no public MCP service,
  live provider capability, deployment or `v0.2.0` release; and
- the repository-only DEPLOY-207 implementation now has a pinned, non-root blocked
  gateway image, materialised checksum-bound source context, strict local Compose
  topology, canonical OCI/source/runtime verification, repeat-build identity, a full
  image SBOM, retained offline-replayable vulnerability evidence, persistence,
  suspension, exact-image restore acceptance and a closed evidence manifest. This
  has passed the full local exact-source aggregator and two independent exact-commit
  reviews. Draft [pull request 48](https://github.com/chris-page-gov/gis-ai-go/pull/48)
  remains blocked. Its latest remote run proved the independently reviewed
  Docker-engine identity repair, repeat-build OCI identity, full SBOM, native-Linux
  scanner ownership repair and retained no-network replay. It then exposed a separate
  classic-Docker import boundary: the valid OCI-only layout had no Docker-save
  `manifest.json`, so Docker 28's classic store rejected it after all scan gates had
  passed. The committed branch repair derives and strictly verifies that one
  compatibility envelope inside the same canonical OCI archive, without duplicating
  or changing image blobs, and incrementally counts bounded binary load-failure
  streams only to enforce the limit while disclosing fixed status and reason metadata.
  Hostile fixture tests cover archive aliasing, links and exact
  tag/layer closure; an exact Docker Desktop/containerd import passes. A fresh remote
  run proved that hybrid load, both builds, SBOM and retained scan/replay, then failed
  closed because Docker 28 serialised the deliberately suppressed internal-network
  port as `null` rather than Docker Desktop's empty list. The current branch repair
  validates the complete one-port map, normalises only those two reviewed no-binding
  forms, brackets container-local probes with bounded host-closed checks and rechecks
  transport after restart. The branch now also applies one bounded privacy boundary
  to generated textual evidence and captured phase output, builds candidate evidence
  in an owner-private quarantine, and promotes or uploads it only after complete
  verification. Those controls are source-bound: only clean evidence and independent
  reviews naming the exact commit are valid, and any later source change supersedes
  the older bundle. Fresh exact-head remote assurance remains mandatory before merge.
  This is not a published image or deployment.

## Next

1. Require the exact privacy-hardened branch head to pass complete clean-source local
   evidence and independent review, then repository, gateway-image, final-assurance
   and CodeQL checks on that same head in draft pull request 48.
2. If the reviewed head remains exact, merge it through the protected branch and
   verify the protected-main image artefact, evidence bundle and SLSA attestations.
3. Complete the repository-only QUAL-206 release preflight, including required local
   evaluation receipts, the integrated release threat record, T04 fallback and a
   disposition for retained High vulnerabilities.
4. Only after a separately authorised public runtime exists, deploy an unregistered
   candidate and complete live QUAL-206 evidence before any activation, registry
   publication, tag or `v0.2.0` release.

## Current blockers

- There is no known external blocker for completing repository assurance of the
  image and Compose candidate. The first draft-PR image run rejected a legitimate
  classic-Docker image identity; the second proved that repair and reached the
  online Trivy scan, whose captured failure output was not surfaced. The third run's
  bounded diagnostic exposed the native-Linux scanner/cache ownership mismatch. The
  next run proved that UID/GID repair and the complete online/offline scan, then failed
  closed when Docker 28's classic store could not import an OCI-only layout. That
  loader incompatibility is exactly reproduced and its compatibility repair passed
  exact local review, clean evidence regeneration and the complete local aggregator.
  The following remote run proved that repair, then exposed Docker 28's reviewed
  `null` representation for a published loopback port suppressed by an internal
  bridge. That closed-map normalisation repair passed the complete exact-clean local
  image gate and independent evidence review. Subsequent adversarial review found a
  wider generated-text privacy and partial-evidence publication boundary; the branch
  now centralises bounded path and credential checks, separates captured output into
  reserved boundary-terminated phase frames, applies the 8 MiB privacy limit
  cumulatively to parsed JSON, and makes the evidence directory publish-only after
  complete verification. Every
  accepted source change still requires matching clean evidence, independent review
  and fresh exact-head remote assurance. Local evidence remains candidate-only and
  protected CI must regenerate it before any attestation.
  There is still no public runtime, workload identity, admitted persistent volume or
  service deployment workflow.
- The gateway assertion is a typed private hand-off, not workload authentication or
  a signed policy decision. Any non-loopback deployment remains blocked on explicit
  service identity and network-policy evidence.
- Activating or publishing a catalogue service remains hard-blocked. Raw protocol
  transcripts, deterministic local host fixtures and the pinned SDK clients do not
  establish independent live major-host interoperability. Security, accessibility,
  governed ingress/storage admission, retention/disposal and host-specific lifecycle
  evidence remain activation gates.
- Direct routes and MCP transports now exist on protected `main`, but the
  production/default capability arrays are empty, readiness is `503`, and there is
  no public service deployment or activation override.
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

- DEPLOY-207 assurance design: the final aggregator rebuilds the OKF projection,
  materialises only Git-tracked allowlisted source plus checksummed OKF outputs,
  proves canonical repeat-build OCI identity, generates an unfiltered full Syft
  SBOM, retains all High and Critical Trivy evidence with a fixable-only block and
  deterministic offline database replay, and exercises the strict local Compose
  boundary. Its exact directory is closed to 11 subjects plus one evidence manifest;
  protected-main provenance will attest the OCI archive, SBOM and manifest only
  after a clean-source run. Dynamic tool versions and timings stay outside the
  reproducible OCI. Compose declares only host loopback, while acceptance records
  either the realised loopback or a no-port internal fallback. This makes no
  host-ingress, public deployment, provider, activation or production-rollback claim;
- every accepted public-read operation and transport remains inactive by default;
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
