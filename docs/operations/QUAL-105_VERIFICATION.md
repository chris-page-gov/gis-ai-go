# QUAL-105 release-assurance verification record

- status: complete for supported `v0.1.0`
- reviewed on: 20 August 2026
- work item: [QUAL-105](https://github.com/chris-page-gov/gis-ai-go/issues/7)
- release target: `v0.1.0`
- supported release:
  [`v0.1.0`](https://github.com/chris-page-gov/gis-ai-go/releases/tag/v0.1.0)
- public product: <https://chris-page-gov.github.io/gis-ai-go/>

## Outcome

QUAL-105 is the final assurance gate for the first supported public discovery
release. It does not add runtime capability. It closes evidence gaps for
whole-product reproducibility, optional browser-API non-use, visible keyboard focus
and durable post-deployment verification.

The release remains a static, public, metadata-only discovery product. This gate
does not claim an MCP listener, provider execution, identity integration, policy
engine, protected-data integration or production service assurance.

## Accepted pre-release baseline

- DISC-104 deployment evidence is merged on protected `main` at
  `5cc1626c9e412393a520b463c6ba670ee51799f0`;
- main assurance and provenance passed in
  [run 32325393703](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32325393703);
- CodeQL for Actions, JavaScript/TypeScript and Python passed in
  [run 32325393339](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32325393339);
- the final DISC-104 restore passed in
  [run 32324490516](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32324490516),
  deployment `5994580314`; and
- on 20 August 2026, the repository had no open CodeQL, Dependabot or secret-scanning
  alerts.

The pre-release candidate reported source
`a0e826384cf50d9d81b87489dbf3580e8e3602f7`, version `0.0.0`, payload root
`cbc0893a46a4674ef7d13aa4aebcbeb0355f9c8a08286a6500bfc954cb5d6ef6` and OKF
content root `a620158911cc60259f0ceab2af0dfdd886783a50bfe98000d692fd534bd08ec0`.

## Acceptance matrix

### Release journeys and negative cases

The release candidate retained the complete catalogue, direct-route, back/forward, download,
hostile-state, CSP, network, forced-colours, reduced-motion and small-viewport
browser suites. It adds a WebMCP-present case with inert sentinels and proves that
the Explorer neither invokes, replaces nor mutates them. This is graceful non-use
evidence, not a WebMCP capability claim.

### Security and accessibility findings

The required repository scan, CodeQL, dependency and secret-alert state must remain
clear of unresolved Critical or High findings. Axe WCAG A/AA checks, keyboard use,
visible focus, forced colours, reduced motion and 320 CSS-pixel reflow must pass.
The 320 CSS-pixel case is the reflow equivalent of a 1,280 CSS-pixel viewport at
400% zoom; it does not claim optical-zoom testing.

### Record evidence contract

The canonical build and Explorer parser require every one of the 36 public records
to provide authority, access, rights, freshness and one or more resolved source
references. Selected HMLR, ONS and LandIS records retain their stricter rights,
provenance and legal caveat checks.

### Clean-build and archive reproducibility

The release gate removes only the three declared generated roots, runs the complete
locked OKF and Explorer build twice, packages each result through the production
Pages packager, then requires byte equality for `artifact.tar`,
`artifact.tar.sha256` and `archive-receipt.json`. It fails on any output difference
and reports the common archive SHA-256 on success.

### Deployed identity and console

DISC-104 proved the exact live commit, payload, OKF root, checksum ledger, primary
journeys, clean console and publication-path-only network boundary across original
deployment, rollback and restoration. The tagged release repeated this public gate
and retained a successful `public-verification-receipt.json` before the immutable
GitHub Release was published.

### Release evidence and metadata

A supported non-`0.0.0` version must have synchronised manifests and workspace
locks, a dated changelog section, exact release link, matching release-notes file
and no unconsumed material changelog fragments. Required CI invokes
`pnpm run validate:release-readiness` when `VERSION` changes, while post-release
feature branches with an unchanged version may retain their required changelog
fragments. The public workflow must upload a canonical verification receipt even
when the passing browser run produces no trace or failure file.

## Pre-release candidate verification

The working-tree candidate passed:

- TypeScript type checking, 4 gateway tests, 16 Explorer build-policy tests and 42
  Explorer unit and component tests;
- 82 repository Python tests and 2 execution-boundary tests, including 5 release
  reproducibility contracts, 15 Pages workflow contracts and release-metadata
  regressions;
- 27 local real-browser tests, including the added WebMCP-present, visible-focus and
  400%-equivalent reflow cases;
- two complete clean locked builds with byte-identical `artifact.tar`, checksum and
  archive receipt outputs;
- validation of 291 local Markdown links, 183 immutable research hashes and 2 source
  ledger snapshots resolving 71 source identifiers;
- a scan of 450 text files with no baseline secret or machine-path match; and
- an unchanged immutable research tree.

The complete local `pnpm run check` passed on 20 August 2026. It also validated 8
schemas and 53 records, rendered 9 diagrams and generated a 145-component CycloneDX
SBOM. Independent accessibility review repeated the corrected browser evidence and
found no P0-P2 or material evidence error. A final exact-snapshot Codex Security
diff scan covered all 17 changed or added files and directly supporting controls;
no P0-P2 finding survived validation and reportability review.

The exact candidate commit `8c0e6ada8e691cb36b03f989fe9fd1446f25a486`
merged through [pull request 16](https://github.com/chris-page-gov/gis-ai-go/pull/16)
as protected-main commit `24925fc7f77b416d557c719942c86eaa3578b4b1`.
Pull-request assurance passed in
[run 32328952442](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32328952442)
and CodeQL passed for Actions, JavaScript/TypeScript and Python in
[run 32328951632](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32328951632).
Resulting main assurance and provenance passed in
[run 32329062233](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32329062233),
and main CodeQL passed in
[run 32329061657](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32329061657).

## Supported release evidence

Release [pull request 17](https://github.com/chris-page-gov/gis-ai-go/pull/17)
merged as protected-main commit
`f1bda209e6309bf4f14f7ab7f524c442e59917b8`. Assurance and provenance passed in
[run 32330917042](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32330917042),
and CodeQL passed for Actions, JavaScript/TypeScript and Python in
[run 32330916721](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32330916721).

The annotated `v0.1.0` tag resolves through tag object
`2f566c6e26dd17b13799e2976500e14701f04d11` to that exact release commit. A
no-bypass tag ruleset blocks update and deletion. GitHub's immutable-release control
is enabled, and
[`v0.1.0`](https://github.com/chris-page-gov/gis-ai-go/releases/tag/v0.1.0)
is the immutable latest, non-prerelease release.

The attested release archive has SHA-256
`acf072986dafc34795039e363d0d5d09af44432fa392ff3aee5525887e1081a4`, payload
root `80a649a5e4bebc36fb38c7b6d51d84056d1b2ff4c8b5f6b96c75bb6d03c6d245`
and OKF content root
`f6da572916ea850f6825e276867504a835bc783d76cea8038f72c8d1d42c2750`.
[Attestation 41776630](https://github.com/chris-page-gov/gis-ai-go/attestations/41776630)
binds the archive to the exact protected-main source and CI workflow.

[Pages run 32331337338](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32331337338)
deployed that verified payload as deployment `5995702325`. All four public-browser
tests passed, and the public receipt records version `0.1.0`, the exact source
commit, payload root, OKF root and public checksum-ledger digest
`75d3a3c9ad8fad2cd7d5a8ee67851fd7655457aae9473ae717f0f4dbc67da815`.

The immutable release contains exactly nine assets. GitHub release verification and
all nine per-asset checks pass. A fresh post-publication download passed
`RELEASE-ASSETS.sha256`; its ledger has SHA-256
`8c062a5872dbc50760380f9826b153abbd14e10f015694b99b6af4f298ce89e4`.
The top-level CycloneDX dependency SBOM contains 145 components, while the separate
52-file publication inventory remains bound inside the canonical archive.

## Limitations and residual risks

- The product is a static metadata catalogue, not an HMLR, ONS, Ordnance Survey or
  LandIS operational service and is not endorsed by those providers.
- HMLR INSPIRE polygons are indicative and do not establish the exact legal extent
  of a title. The schematic view is not a property or parcel map.
- Source currency, access and reuse remain record- and provider-specific; users must
  follow the displayed evidence and official source terms.
- Automated axe and browser checks are strong regression evidence but do not replace
  a specialist accessibility audit or user research with disabled people.
- CodeQL, dependency alerts and the repository secret scan are baselines, not a
  penetration test or a security assessment of later service, identity or provider
  integrations.
- The WebMCP-present test proves inert compatibility only. No WebMCP tool is exposed
  or supported in `v0.1.0`.
- GitHub Pages supplies the hosting boundary. The application enforces its exact
  meta Content Security Policy, but the repository does not control response-header
  policies such as `frame-ancestors`.
- Actions artefacts expire. The immutable release therefore retains the canonical
  archive, checksum, receipt, SBOM, attestation verification and public-verification
  evidence as durable assets.

The protected-main merge of this final record closes QUAL-105: the tagged artefact
is deployed, its public receipt passes, and the immutable GitHub Release and durable
assets exist.
