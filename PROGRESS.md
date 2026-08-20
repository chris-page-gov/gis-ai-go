# Delivery progress

Last updated: 20 August 2026

## Current outcome

Deliver `v0.2.0`: expose the supported governed catalogue and evidence model through
an open, read-only MCP and direct API without weakening the static `v0.1.0` product.
The supported target active set is exactly `catalogue.search`,
`catalogue.describe`, `evidence.inspect`, `selection.resolve` and `data.query`.

## Active workstream

`MCP-201 — Implement the first catalogue transport slice`

- use the accepted lifecycle boundary from
  [`ADR-0009`](docs/decisions/ADR-0009-read-only-mcp-tool-lifecycle.md);
- pass the inactive loopback gateway candidate through the protected pull-request
  gate without changing the supported public product;
- retain the checksum-verified immutable catalogue loader and deterministic,
  transport-neutral `catalogue.search`/`catalogue.describe` application;
- expose only health, blocked readiness and OpenAPI while policy and inline
  evidence are unavailable;
- advertise no tool and mount no catalogue API operation in this candidate;
- retain policy, evidence, rate and complexity boundaries in every public contract;
  and
- require EVID-204 and later non-App MCP, direct API and static-product
  interoperability evidence before any public service or registry entry.

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
  gaining any dependency on a running service.

## Next

1. Pass the inactive gateway candidate through the complete local and protected
   pull-request gates while keeping readiness blocked and the public product
   unchanged.
2. EVID-204 must add reviewed public policy decisions and canonical inline evidence
   receipts to the shared application path.
3. Add and verify the protocol-conformant MCP listener and direct catalogue routes,
   then activate `catalogue.search` and `catalogue.describe` only when their full
   policy, evidence, lifecycle and interoperability gates pass.
4. Activate `evidence.inspect`, `selection.resolve` and `data.query` only after
   their separate evidence gates pass; keep the other seven profiles planned.

## Current blockers

- No blocker is known for merging the deliberately inactive local gateway
  candidate.
- Activating or publishing a catalogue service is hard-blocked until EVID-204 adds
  reviewed public policy and canonical inline evidence receipts. The current
  candidate has no activation override.
- The candidate has no MCP listener, catalogue API operation, provider adapter or
  evidence store; those remain implementation work, not implied capabilities.
- Protected PSGA and commercial deployments require separate rights, credentials
  and isolated infrastructure. They remain outside this release and do not block
  the open product.

## Latest evidence

- MCP-201 shared catalogue contract: protected-main commit
  `e5e6d4db5ac7036198cde64279e815f214f3defd`, passing assurance and provenance in
  [run 32338916345](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32338916345),
  passing CodeQL in
  [run 32338916269](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32338916269)
  and [attestation 41792357](https://github.com/chris-page-gov/gis-ai-go/attestations/41792357);
- MCP-201 gateway candidate: local implementation and verification remain pending
  protected pull-request evidence; the candidate exposes no catalogue operation,
  MCP tool or public deployment;
- QUAL-105 complete local gate: type checking, 4 gateway tests, 16 Explorer
  build-policy tests, 42 Explorer unit and component tests, 82 repository Python
  tests, 2 execution-boundary tests and 27 real-browser tests pass;
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
