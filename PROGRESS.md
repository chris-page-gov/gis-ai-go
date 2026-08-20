# Delivery progress

Last updated: 20 August 2026

## Current outcome

Deliver `v0.1.0`: an accessible public GIS AI GO discovery product with a canonical
OKF bundle, reviewed open geospatial examples, linked machine-readable data and a
reproducible GitHub Pages deployment.

## Active workstream

`DISC-104 — Publish immutable GitHub Pages artefacts`

- package only the checked Explorer distribution as a deterministic publication
  artefact with checksums, provenance, receipt and SBOM;
- deploy the exact artefact from a successful protected-`main` assurance run;
- verify the public product, catalogue journeys, CSP, network boundary,
  accessibility and source identity in a real browser;
- rehearse rollback to a previous accepted artefact and restore the current one
  without rebuilding either artefact.

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
  capabilities with exact rights and provenance boundaries.

## Next

1. Publish and verify the immutable static product through `DISC-104`.
2. Prove artefact-only rollback and restore the current accepted deployment.
3. Assemble, tag and verify the first supported `v0.1.0` release.

## Current blockers

- GitHub Pages is configured but has no successful deployment. Four verified
  deployment attempts reached Pages ingestion and failed closed, including the
  corrected deterministic tar from protected `main` at `eced0ae`. The active
  candidate retains that tar as attested source evidence, safely materialises and
  rechecks its exact files, then uses GitHub's pinned official Pages transport. If
  that supported path fails, deployment stops for escalation to GitHub Support.
- Protected PSGA and commercial deployments require separate rights, credentials
  and isolated infrastructure; they do not block the open product.

## Latest evidence

- canonical OKF content, Explorer, reviewed public examples and the corrected
  source-archive contract: merged on protected `main` at `eced0ae`;
- main assurance, provenance and CodeQL: passing at `eced0ae` on 20 August 2026;
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
- DISC-104 supported-transport candidate: the complete local gate passes with 27
  archive and staging contracts, 11 workflow contracts, 69 repository Python
  tests, 25 browser journeys and the full integrity, link, secret, diagram and SBOM
  checks;
- DISC-104 protected-main source evidence: run `32322035483` built and attested
  archive SHA-256 `b20ba6cab1811b976417aef6ca4c61bc33270063d7646ab8469e3273399edd11`;
- DISC-104 transport candidate: the independently verified source files are staged
  without rebuilding and passed to the pinned official GitHub Pages uploader;
  candidate assurance, deployment and rollback evidence remain to be produced;
- public repository: verified with personal `noreply` commit identity;
- deployed product: none;
- latest supported release: none.
