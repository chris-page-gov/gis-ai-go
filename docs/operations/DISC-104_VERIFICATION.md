# DISC-104 GitHub Pages verification record

- status: implementation candidate
- reviewed on: 20 August 2026
- work item: DISC-104
- public URL: not deployed

## Outcome

DISC-104 packages the checked Explorer distribution once and separates build,
attestation and deployment. The deployment workflow can publish, roll back or
restore only a successful protected-`main` artefact whose source run, commit,
SHA-256 digest, deterministic receipt and GitHub provenance all agree.

No workflow publishes the repository root, immutable research viewer, source tree,
provider payload, credential or protected data. Deployment performs no build.

Deployment-time verifier and browser-test code always comes from the current
protected-main workflow commit. A dispatch-selected source commit remains
non-executable archive identity data.

## Candidate gates

Before merge, record:

- deterministic archive tests, including repeated byte-for-byte output;
- malicious path, symlink, hard-link, special-file, inventory and checksum
  rejection;
- workflow event, source-run, branch, commit, artefact-name, digest, attestation and
  least-privilege contract tests;
- complete repository assurance and CodeQL at the pull-request head; and
- independent review of the archive, workflow and public-browser boundaries.

The complete local candidate gate most recently passed on 20 August 2026 against
the supported-transport candidate based on protected `main` at
`eced0ae697818b4989ebe95c5bf1572cc6ec90c2`:

- 27 deterministic archive, safe-staging and hostile-input contract tests;
- 11 workflow event, identity, provenance, staging, permission and no-build
  deployment contract tests;
- 4 gateway tests, 16 Explorer build-policy tests, 42 Explorer unit and component
  tests, 69 repository Python tests and 2 execution-boundary tests;
- 25 existing local real-browser journeys;
- 8 schemas and 53 evaluation records, 290 local links, 183 immutable research
  hashes, 2 source-ledger snapshots and 71 source identifiers;
- 446 text files scanned without a baseline secret or machine-path match;
- 9 rendered diagrams and a 145-component repository CycloneDX SBOM.

Before the Pages header compatibility correction, packager and verifier contract
`1.0.0` reproduced uncompressed canonical POSIX ustar archive SHA-256
`aca0decf3637e836e0818619456deec75601b0a99475ca6d71b17a23c8fc0f31`
and payload root
`9b0f95f52bc77f45924a767cf774f70e9806b5b10b0ccbe0e460701e3e05ee55`
from merged source commit `e5a522e` and OKF content root
`c3fdadf975194580d1f659e7f3f3b609099b720129b9d8149801115f659c4040`.
This is a historical local rehearsal identity, not a compatible protected-main
publication artefact. The archive was extracted under the `/gis-ai-go/` mount and
the separate public suite passed all 4 identity, accepted-manifest payload,
trusted-ledger checksum, reviewed-journey, history, network, CSP, accessibility and
320 CSS-pixel tests.

All ten external Action pins were independently resolved against their official
GitHub tag refs; the annotated pnpm tag was dereferenced to its exact commit.

## Pages ingestion compatibility evidence

The first four deployment attempts stopped after validation, provenance,
configuration and artefact staging had passed:

- runs
  [`32319998787`](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32319998787)
  and
  [`32320096985`](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32320096985)
  selected the artefact from source commit `9ff1281`;
- run
  [`32320645861`](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32320645861)
  selected the artefact from source commit `8e48e68` after restoring the standard
  compressed Actions transport;
- run
  [`32322255222`](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32322255222)
  selected the corrected, attested source artefact from commit `eced0ae`;
- all four reached `actions/deploy-pages`, created a Pages deployment and then
  returned GitHub's generic `deployment_failed` state; public verification was
  correctly skipped.

The exact staged archive from the third run retained SHA-256
`d151284c48467c7420f37c1bca7a99619c3230711a0c5d6a9162f7f12c8ac573`.
It contained 57 regular members, but all member paths omitted the required `./`
root and all used numeric owner and group `0`. GitHub's Pages maintainer documents
the `./` prefix as an intentional ingestion requirement in
[`actions/deploy-pages` issue 203](https://github.com/actions/deploy-pages/issues/203#issuecomment-1652804586),
and the same tracker documents root-owned members as a cause of the opaque failure
in
[`actions/deploy-pages` issue 58](https://github.com/actions/deploy-pages/issues/58#issuecomment-1367490639).

Packager and verifier contract `1.0.1` therefore requires `./` member paths and
fixed non-root numeric ownership. Regressions reject an unprefixed path and a
root-owned member. Protected-main run `32322035483` then produced and attested
corrected source archive SHA-256
`b20ba6cab1811b976417aef6ca4c61bc33270063d7646ab8469e3273399edd11`.
All 57 members used the corrected metadata and the fourth workflow uploaded those
exact bytes, but Pages still rejected its custom tar encoding.

ADR-0008 therefore retains that deterministic tar as attested source evidence but
supersedes the unchanged-tar deployment claim. The current workflow candidate
safely materialises and rechecks its exact logical files, then uses the exact pinned
official `actions/upload-pages-artifact` implementation to create only the platform
transport envelope. If that supported path also fails, the run evidence must be
escalated to GitHub Support rather than prompting another speculative archive
change.

## Protected-main source evidence

- source commit: `eced0ae697818b4989ebe95c5bf1572cc6ec90c2`;
- successful CI push run: [`32322035483`](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32322035483),
  including successful `assurance` and `provenance` jobs;
- source artefact: `pages-source-eced0ae697818b4989ebe95c5bf1572cc6ec90c2`,
  ID `9390109262`;
- `artifact.tar` SHA-256:
  `b20ba6cab1811b976417aef6ca4c61bc33270063d7646ab8469e3273399edd11`;
- outer receipt SHA-256:
  `c5ad1ee357b7a098c09aab355a3e174ac31c8a24c90ec30f74f6c47b1bd44596`;
- strict GitHub attestation verification: protected `main`, source commit
  `eced0ae`, `.github/workflows/ci.yml`, GitHub-hosted runner and CI invocation
  `32322035483` all matched;
- product version `0.0.0`, payload root
  `7d0adda69e77b815e75e860426cb3ac107b89a70abdd91d771070024c459444b`
  and OKF content root
  `c8415e83643b43b6fbde43cf30cf80ce8e5440f69770cfd9433337a5087f37fd`.

## Repository configuration evidence

- Pages build type is `workflow`, the site is public, HTTPS is enforced and no
  custom domain is set;
- the `github-pages` environment is restricted to exact branch `main`;
- repository Actions require complete-SHA pins;
- the no-bypass protected-main ruleset still requires strict `assurance`, linear
  squash-only pull requests and resolved review threads; and
- the default workflow token remains read-only and cannot approve pull requests.

## Deployment and public evidence

Complete after first deployment:

- deployment workflow run, Pages deployment ID and public URL: pending;
- live receipt identity equals selected source artefact: pending;
- checksum and JSON/JSON-LD parity: pending;
- default, Price Paid, ONS, LandIS, direct-route and history journeys: pending;
- exact CSP, clean console and publication-path-only requests: pending;
- keyboard, axe A/AA and 320 CSS-pixel acceptance: pending.

## Rollback rehearsal

Complete with two accepted protected-main artefacts:

- artefact A identities and original deployment: pending;
- artefact B identities and original deployment: pending;
- rollback run redeploying A without a build and its public evidence: pending;
- restore run redeploying B without a build and its public evidence: pending.

DISC-104 remains incomplete while any item in this record is pending.
