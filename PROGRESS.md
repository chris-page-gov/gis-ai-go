# Delivery progress

Last updated: 20 August 2026

## Current outcome

Deliver `v0.1.0`: an accessible public GIS AI GO discovery product with a canonical
OKF bundle, reviewed open geospatial examples, linked machine-readable data and a
reproducible GitHub Pages deployment.

## Active workstream

`DISC-103 — Add reviewed public geospatial examples`

- add digest-locked HM Land Registry journeys LR-Q003, LR-Q006 and LR-Q012;
- add non-executing ONS data, ONS geography and LandIS capability records;
- preserve exact source, release, retrieval, review, rights and access semantics;
- fail closed on forbidden fields, unresolved evidence or mixed rights presented as
  open;
- prove the new journeys through contract, Explorer and real-browser assurance.

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

## Next

1. Complete and merge the reviewed examples through `DISC-103`.
2. Publish the immutable static product through `DISC-104` after the final gate.
3. Assemble, tag and verify the first supported `v0.1.0` release.

## Current blockers

- GitHub Pages stays disabled until the hardened Explorer, attribution review and
  browser/accessibility gates pass.
- Protected PSGA and commercial deployments require separate rights, credentials
  and isolated infrastructure; they do not block the open product.

## Latest evidence

- canonical OKF content and Explorer: merged on protected `main` at `6984f30`;
- main assurance and CodeQL: passing at `6984f30` on 20 August 2026;
- Explorer assurance includes
  16 build-policy tests, 36 unit and component tests, 18 browser journeys and
  production integrity checks;
- bounded security diff review: all changed runtime, interface and build-assurance
  files covered; the confirmed Low CSP/origin assurance gap, exact HTML-attribute
  parsing, fresh preview-server enforcement, and defensive symlink and lock-strict
  hardening are remediated with passing regressions;
- DISC-103 source review: exact provider snapshots and HMLR `v0.3.0` inputs are
  selected; the 36-record local candidate passes the complete repository gate,
  including 25 browser journeys, and independent review is complete;
- DISC-103 security review: the selected HMLR inputs and copied licence are
  independently bound to approved v0.3.0 digests, and coordinated source, rights,
  licence and lock mutations now fail closed;
- public repository: verified with personal `noreply` commit identity;
- deployed product: none;
- latest supported release: none.
