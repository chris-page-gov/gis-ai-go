# Delivery progress

Last updated: 20 August 2026

## Current outcome

Deliver `v0.1.0`: an accessible public GIS AI GO discovery product with a canonical
OKF bundle, reviewed open geospatial examples, linked machine-readable data and a
reproducible GitHub Pages deployment.

## Active workstream

`QUAL-105 — Complete release assurance`

- complete the integrity, security, real-browser and WCAG acceptance gate against
  protected `main` and the live public product;
- keep deterministic artefact, deployment and rollback evidence bound to the
  accepted source commits; and
- resolve any release-blocking findings before assembling `v0.1.0`.

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
- full local `pnpm run check` passed on 20 August 2026.
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
  <https://chris-page-gov.github.io/gis-ai-go/>.

## Next

1. Complete `QUAL-105` integrity, security, browser and WCAG release assurance.
2. Resolve any release-blocking findings and rerun the affected gates.
3. Assemble, tag and verify the first supported `v0.1.0` release.

## Current blockers

- No blocker is known for the open `v0.1.0` discovery product.
- Protected PSGA and commercial deployments require separate rights, credentials
  and isolated infrastructure. They remain outside this release and do not block
  the open product.

## Latest evidence

- canonical OKF content, Explorer, reviewed public examples and supported Pages
  publication: merged on protected `main` at
  `a0e826384cf50d9d81b87489dbf3580e8e3602f7`;
- main assurance and provenance: passing in
  [run 32324008595](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32324008595);
- CodeQL for Actions, JavaScript/TypeScript and Python: passing in
  [run 32324008614](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32324008614);
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
- latest supported release: none.
